#!/usr/bin/env python3
"""Upgrade the 10-year catalog sample using alternate-version fallbacks."""
from __future__ import annotations

import argparse
import csv
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from fetch_policy import (
    api_headers,
    browser_headers,
    canonicalize_url,
    classify_policy_skip,
    classify_terminal_error,
    url_attempts,
)
from source_catalog import HarvestSource, load_harvest_source_ids


ROOT = Path(__file__).resolve().parents[1]
TODAY = date.today().isoformat()
DEFAULT_CATALOG = ROOT / "research_ops/01_sources/fetch_source_catalog.csv"
DEFAULT_INPUT_CSV = ROOT / "research_ops/02_papers/catalog_10yr_sample_status.csv"
DEFAULT_OUTPUT_CSV = ROOT / "research_ops/02_papers/catalog_10yr_sample_status_upgraded.csv"
DEFAULT_OUTPUT_MD = ROOT / "research_ops/00_meta/2026-04-04_catalog_10yr_sample_upgraded_report.md"
FULLTEXT_SUCCESS = {"success_html", "success_pdf"}
ALT_HOST_KEYWORDS = {
    "arxiv.org",
    "export.arxiv.org",
    "biorxiv.org",
    "medrxiv.org",
    "researchgate.net",
    "pmc.ncbi.nlm.nih.gov",
    "europepmc.org",
}


@dataclass
class UpgradedRow:
    catalog_id: str
    source_name: str
    source_kind: str
    year: int
    rank_within_source_year: int
    openalex_id: str
    title: str
    doi: str
    baseline_oa_url: str
    baseline_title_status: str
    baseline_abstract_status: str
    baseline_fulltext_status: str
    upgraded_title_status: str
    upgraded_abstract_status: str
    upgraded_fulltext_status: str
    abstract_strategy: str
    fulltext_strategy: str
    fallback_source_label: str
    fallback_host: str
    final_oa_url: str
    fulltext_detail: str
    fulltext_used_url: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Upgrade the 10-year journal/conference sample by searching "
            "alternate copies for missing abstract/fulltext."
        )
    )
    parser.add_argument(
        "--catalog",
        type=Path,
        default=DEFAULT_CATALOG,
        help="Path to the unified journal/conference fetch catalog.",
    )
    parser.add_argument(
        "--input-csv",
        type=Path,
        default=DEFAULT_INPUT_CSV,
        help="Baseline sample CSV produced by run_catalog_ten_year_sample.py.",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=DEFAULT_OUTPUT_CSV,
        help="Where to write the upgraded sample CSV.",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=DEFAULT_OUTPUT_MD,
        help="Where to write the upgraded markdown report.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Concurrent workers for fallback upgrades.",
    )
    parser.add_argument(
        "--detail-timeout",
        type=int,
        default=45,
        help="Timeout in seconds for OpenAlex detail/search calls.",
    )
    parser.add_argument(
        "--fulltext-timeout",
        type=int,
        default=20,
        help="Timeout in seconds for each fulltext request.",
    )
    return parser.parse_args()


def pct(ok_count: int, total: int) -> str:
    return f"{(100.0 * ok_count / total):.1f}%" if total else "0.0%"


def format_metric(ok_count: int, total: int) -> str:
    return f"{ok_count}/{total} ({pct(ok_count, total)})"


def normalize_title(title: str) -> str:
    value = (title or "").casefold()
    value = value.replace("—", "-").replace("–", "-")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def host_of(url: str) -> str:
    host = urlparse(canonicalize_url(url)).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def alt_host_rank(url: str) -> tuple[int, str]:
    host = host_of(url)
    priority = 0
    if host in {"pmc.ncbi.nlm.nih.gov", "europepmc.org"}:
        priority = 100
    elif host in {"arxiv.org", "export.arxiv.org"}:
        priority = 95
    elif host in {"biorxiv.org", "medrxiv.org"}:
        priority = 90
    elif host == "researchgate.net":
        priority = 85
    elif host.endswith(".edu") or host.endswith(".ac.uk") or host.endswith(".nl"):
        priority = 70
    elif host:
        priority = 50
    return (-priority, host, canonicalize_url(url))


def read_baseline_rows(path: Path) -> list[UpgradedRow]:
    rows: list[UpgradedRow] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for item in csv.DictReader(handle):
            rows.append(
                UpgradedRow(
                    catalog_id=(item.get("catalog_id") or "").strip(),
                    source_name=(item.get("source_name") or "").strip(),
                    source_kind=(item.get("source_kind") or "").strip(),
                    year=int(item.get("year") or 0),
                    rank_within_source_year=int(item.get("rank_within_source_year") or 0),
                    openalex_id=(item.get("openalex_id") or "").strip(),
                    title=(item.get("title") or "").strip(),
                    doi=(item.get("doi") or "").strip(),
                    baseline_oa_url=(item.get("oa_url") or "").strip(),
                    baseline_title_status=(item.get("title_status") or "").strip(),
                    baseline_abstract_status=(item.get("abstract_status") or "").strip(),
                    baseline_fulltext_status=(item.get("fulltext_status") or "").strip(),
                    upgraded_title_status=(item.get("title_status") or "").strip(),
                    upgraded_abstract_status=(item.get("abstract_status") or "").strip(),
                    upgraded_fulltext_status=(item.get("fulltext_status") or "").strip(),
                    abstract_strategy="baseline",
                    fulltext_strategy="baseline",
                    fallback_source_label="",
                    fallback_host=host_of(item.get("oa_url") or ""),
                    final_oa_url=(item.get("oa_url") or "").strip(),
                    fulltext_detail=(item.get("fulltext_detail") or "").strip(),
                    fulltext_used_url=(item.get("fulltext_used_url") or "").strip(),
                )
            )
    return rows


def write_rows(rows: list[UpgradedRow], path: Path) -> None:
    fieldnames = [
        "catalog_id",
        "source_name",
        "source_kind",
        "year",
        "rank_within_source_year",
        "openalex_id",
        "title",
        "doi",
        "baseline_oa_url",
        "baseline_title_status",
        "baseline_abstract_status",
        "baseline_fulltext_status",
        "upgraded_title_status",
        "upgraded_abstract_status",
        "upgraded_fulltext_status",
        "abstract_strategy",
        "fulltext_strategy",
        "fallback_source_label",
        "fallback_host",
        "final_oa_url",
        "fulltext_detail",
        "fulltext_used_url",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: getattr(row, name) for name in fieldnames})


def openalex_json(url: str, timeout: int) -> dict[str, Any]:
    req = urllib.request.Request(url, headers=api_headers())
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def openalex_detail(openalex_id: str, timeout: int) -> dict[str, Any]:
    wid = openalex_id if openalex_id.startswith("W") else f"W{openalex_id}"
    return openalex_json(f"https://api.openalex.org/works/{wid}", timeout)


def openalex_search(title: str, timeout: int) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({"search": title, "per_page": 10})
    payload = openalex_json(f"https://api.openalex.org/works?{params}", timeout)
    return list(payload.get("results", []))


def host_label(url: str) -> str:
    host = host_of(url)
    return host or "unknown_host"


def collect_urls_from_work(work: dict[str, Any], fallback_only: bool = False) -> list[tuple[str, str]]:
    candidates: list[tuple[str, str]] = []

    def add(url: str, label: str) -> None:
        clean = canonicalize_url(url or "")
        if not clean.lower().startswith("http"):
            return
        candidates.append((clean, label))

    if not fallback_only:
        add(((work.get("open_access") or {}).get("oa_url") or ""), "open_access.oa_url")

    best = work.get("best_oa_location") or {}
    add(best.get("pdf_url") or "", "best_oa_location.pdf_url")
    add(best.get("landing_page_url") or "", "best_oa_location.landing_page_url")

    for idx, location in enumerate(work.get("locations") or []):
        src_name = ((location.get("source") or {}).get("display_name") or f"location_{idx}")[:60]
        add(location.get("pdf_url") or "", f"locations[{idx}].pdf_url::{src_name}")
        add(location.get("landing_page_url") or "", f"locations[{idx}].landing_page_url::{src_name}")

    dedup: dict[str, str] = {}
    for url, label in candidates:
        dedup.setdefault(url, label)
    return sorted(((url, label) for url, label in dedup.items()), key=lambda item: alt_host_rank(item[0]))


def pick_alt_work(base_title: str, base_doi: str, candidates: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, str]:
    wanted = normalize_title(base_title)
    doi_low = (base_doi or "").strip().lower()
    best: dict[str, Any] | None = None
    best_reason = ""
    best_score = -1
    for work in candidates:
        title = (work.get("display_name") or work.get("title") or "").strip()
        title_norm = normalize_title(title)
        doi = ((work.get("doi") or "").replace("https://doi.org/", "").strip().lower())
        urls = [u for u, _ in collect_urls_from_work(work)]
        hosts = {host_of(url) for url in urls}
        alt_hint = any(host in ALT_HOST_KEYWORDS for host in hosts) or any(
            token in ((work.get("primary_location") or {}).get("landing_page_url") or "").lower()
            for token in ("arxiv", "biorxiv", "medrxiv", "researchgate")
        )
        exact_title = bool(wanted and title_norm == wanted)
        same_doi = bool(doi_low and doi == doi_low)
        if not (exact_title or same_doi):
            continue
        score = 0
        if same_doi:
            score += 100
        if exact_title:
            score += 80
        if bool(work.get("abstract_inverted_index")):
            score += 20
        if alt_hint:
            score += 15
        if urls:
            score += 5
        if score > best_score:
            best = work
            best_score = score
            if same_doi:
                best_reason = "same_doi"
            elif exact_title:
                best_reason = "same_title"
    return best, best_reason


def probe_candidate_urls(
    row: UpgradedRow,
    candidates: list[tuple[str, str]],
    timeout: int,
) -> tuple[str, str, str, str, str]:
    last_err = ""
    for url, label in candidates:
        policy = classify_policy_skip(url, row.doi)
        if policy:
            last_err = policy
            continue
        for attempt in url_attempts(url):
            try:
                req = urllib.request.Request(attempt, headers=browser_headers())
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    ctype = (resp.headers.get("Content-Type") or "").lower()
                    _ = resp.read(2048)
                status = "success_pdf" if ("pdf" in ctype or attempt.lower().split("?", 1)[0].endswith(".pdf")) else "success_html"
                return status, ctype[:120], attempt, label, host_label(attempt)
            except urllib.error.HTTPError as exc:
                last_err = f"HTTP {exc.code}: {exc.reason}"
            except Exception as exc:  # noqa: BLE001
                last_err = str(exc)[:180]
    terminal = classify_terminal_error(row.final_oa_url or row.baseline_oa_url, last_err, row.doi)
    return "skipped_policy" if terminal else "error", terminal or last_err[:120], "", "", ""


def upgrade_single(row: UpgradedRow, detail_timeout: int, fulltext_timeout: int) -> UpgradedRow:
    needs_abstract = row.upgraded_abstract_status != "success"
    needs_fulltext = row.upgraded_fulltext_status not in FULLTEXT_SUCCESS
    if not (needs_abstract or needs_fulltext):
        return row

    detail: dict[str, Any] | None = None
    detail_error = ""
    try:
        detail = openalex_detail(row.openalex_id, detail_timeout)
    except Exception as exc:  # noqa: BLE001
        detail_error = str(exc)[:180]

    if detail and needs_abstract and detail.get("abstract_inverted_index"):
        row.upgraded_abstract_status = "success"
        row.abstract_strategy = "same_work_detail"

    all_candidates: list[tuple[str, str]] = []
    if detail:
        all_candidates.extend(collect_urls_from_work(detail, fallback_only=False))

    alt_work = None
    alt_reason = ""
    if (row.upgraded_abstract_status != "success" or row.upgraded_fulltext_status not in FULLTEXT_SUCCESS):
        try:
            candidates = openalex_search(row.title, detail_timeout)
            alt_work, alt_reason = pick_alt_work(row.title, row.doi, candidates)
        except Exception:  # noqa: BLE001
            alt_work = None

    if alt_work:
        alt_urls = collect_urls_from_work(alt_work, fallback_only=False)
        all_candidates.extend(alt_urls)
        alt_label = ((alt_work.get("primary_location") or {}).get("landing_page_url") or "")
        if not alt_label and alt_urls:
            alt_label = alt_urls[0][0]
        row.fallback_source_label = f"alt_work:{alt_reason}"
        row.fallback_host = host_label(alt_label)
        if row.upgraded_abstract_status != "success" and alt_work.get("abstract_inverted_index"):
            row.upgraded_abstract_status = "success"
            row.abstract_strategy = f"alternate_version:{row.fallback_host or alt_reason}"

    if needs_fulltext:
        dedup: dict[str, str] = {}
        for url, label in all_candidates:
            dedup.setdefault(url, label)
        if dedup:
            status, detail_msg, used_url, label, host = probe_candidate_urls(
                row,
                sorted(((url, label) for url, label in dedup.items()), key=lambda item: alt_host_rank(item[0])),
                fulltext_timeout,
            )
            row.upgraded_fulltext_status = status
            row.fulltext_detail = detail_msg
            if used_url:
                row.fulltext_used_url = used_url
                row.final_oa_url = used_url
                row.fallback_host = host or row.fallback_host
                if not row.fallback_source_label:
                    row.fallback_source_label = label
                row.fulltext_strategy = "alternate_location" if label != "open_access.oa_url" else "primary_or_equivalent_location"
            elif status in {"error", "skipped_policy"} and detail_error and not detail_msg:
                row.fulltext_detail = detail_error
        elif detail_error:
            row.fulltext_detail = detail_error

    if not row.fallback_host:
        row.fallback_host = host_label(row.final_oa_url or row.baseline_oa_url)
    return row


def upgrade_rows(rows: list[UpgradedRow], detail_timeout: int, fulltext_timeout: int, workers: int) -> list[UpgradedRow]:
    upgraded: list[UpgradedRow] = []
    with ThreadPoolExecutor(max_workers=max(workers, 1)) as executor:
        future_map = {
            executor.submit(upgrade_single, row, detail_timeout, fulltext_timeout): row
            for row in rows
        }
        for future in as_completed(future_map):
            upgraded.append(future.result())
    upgraded.sort(key=lambda row: (row.source_kind, row.source_name, row.year, row.rank_within_source_year))
    return upgraded


def aggregate(rows: list[UpgradedRow], catalog_rows: list[HarvestSource]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], dict[str, int]] = defaultdict(
        lambda: {"total": 0, "title_ok": 0, "abstract_ok": 0, "fulltext_ok": 0}
    )
    for item in catalog_rows:
        grouped[(item.source_kind, item.source_name)]
    for row in rows:
        key = (row.source_kind, row.source_name)
        grouped[key]["total"] += 1
        grouped[key]["title_ok"] += int(row.upgraded_title_status == "success")
        grouped[key]["abstract_ok"] += int(row.upgraded_abstract_status == "success")
        grouped[key]["fulltext_ok"] += int(row.upgraded_fulltext_status in FULLTEXT_SUCCESS)
    output = []
    for (source_kind, source_name), counts in grouped.items():
        output.append({"source_kind": source_kind, "source_name": source_name, **counts})
    output.sort(key=lambda row: (row["source_kind"], row["source_name"]))
    return output


def aggregate_baseline(rows: list[UpgradedRow]) -> dict[str, int]:
    counts = {"total": 0, "title_ok": 0, "abstract_ok": 0, "fulltext_ok": 0}
    for row in rows:
        counts["total"] += 1
        counts["title_ok"] += int(row.baseline_title_status == "success")
        counts["abstract_ok"] += int(row.baseline_abstract_status == "success")
        counts["fulltext_ok"] += int(row.baseline_fulltext_status in FULLTEXT_SUCCESS)
    return counts


def overall_row(rows: list[dict[str, object]]) -> dict[str, object]:
    total = title_ok = abstract_ok = fulltext_ok = 0
    for row in rows:
        total += int(row["total"])
        title_ok += int(row["title_ok"])
        abstract_ok += int(row["abstract_ok"])
        fulltext_ok += int(row["fulltext_ok"])
    return {
        "source_kind": "all",
        "source_name": "ALL_SOURCES",
        "total": total,
        "title_ok": title_ok,
        "abstract_ok": abstract_ok,
        "fulltext_ok": fulltext_ok,
    }


def render_table(rows: list[dict[str, object]]) -> str:
    lines = [
        "| 来源类型 | 来源 | 样本数 | 标题成功率 | 摘要成功率 | 正文成功率 |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        total = int(row["total"])
        lines.append(
            "| {source_kind} | {source_name} | {total} | {title} | {abstract} | {fulltext} |".format(
                source_kind=row["source_kind"],
                source_name=row["source_name"],
                total=total,
                title=format_metric(int(row["title_ok"]), total),
                abstract=format_metric(int(row["abstract_ok"]), total),
                fulltext=format_metric(int(row["fulltext_ok"]), total),
            )
        )
    return "\n".join(lines)


def build_report(
    rows: list[UpgradedRow],
    aggregate_rows: list[dict[str, object]],
    baseline_counts: dict[str, int],
    output_csv: Path,
) -> str:
    overall = overall_row(aggregate_rows)
    csv_label = str(output_csv.resolve().relative_to(ROOT))
    strategy_counts = Counter(row.abstract_strategy for row in rows if row.abstract_strategy != "baseline")
    fulltext_strategy_counts = Counter(row.fulltext_strategy for row in rows if row.fulltext_strategy != "baseline")
    host_counts = Counter(row.fallback_host for row in rows if row.fallback_host and row.fulltext_strategy != "baseline")
    lines = [
        "# 升级版：全部期刊会议 10 年样本爬取成功率",
        "",
        f"日期：{TODAY}",
        "",
        "## 升级策略",
        "",
        "- 基于基线样本 `research_ops/02_papers/catalog_10yr_sample_status.csv` 做二次增强，不改变样本集合。",
        "- 当 abstract 或正文缺失时，先看同一篇 work 的 `locations` / `best_oa_location`。",
        "- 若仍缺失，再按标题搜索 OpenAlex 中的同题/同 DOI 备用版本，优先接受 arXiv、bioRxiv/medRxiv、ResearchGate、PMC/Europe PMC 与机构仓库副本。",
        f"- 升级后样本明细：`{csv_label}`。",
        "",
        "## 总体对比",
        "",
        "| 版本 | 样本数 | 标题成功率 | 摘要成功率 | 正文成功率 |",
        "| --- | ---: | ---: | ---: | ---: |",
        "| 基线 | {total} | {title} | {abstract} | {fulltext} |".format(
            total=baseline_counts["total"],
            title=format_metric(baseline_counts["title_ok"], baseline_counts["total"]),
            abstract=format_metric(baseline_counts["abstract_ok"], baseline_counts["total"]),
            fulltext=format_metric(baseline_counts["fulltext_ok"], baseline_counts["total"]),
        ),
        "| 升级后 | {total} | {title} | {abstract} | {fulltext} |".format(
            total=int(overall["total"]),
            title=format_metric(int(overall["title_ok"]), int(overall["total"])),
            abstract=format_metric(int(overall["abstract_ok"]), int(overall["total"])),
            fulltext=format_metric(int(overall["fulltext_ok"]), int(overall["total"])),
        ),
        "",
        "## 升级后分来源结果",
        "",
        render_table(aggregate_rows),
        "",
        "## fallback 使用情况",
        "",
    ]
    if strategy_counts:
        lines.append("- 摘要 fallback：")
        for key, value in strategy_counts.most_common():
            lines.append(f"  - `{key}`: {value}")
    else:
        lines.append("- 摘要 fallback：无新增命中。")
    if fulltext_strategy_counts:
        lines.append("- 正文 fallback：")
        for key, value in fulltext_strategy_counts.most_common():
            lines.append(f"  - `{key}`: {value}")
    else:
        lines.append("- 正文 fallback：无新增命中。")
    if host_counts:
        lines.append("- 命中的备用 host：")
        for key, value in host_counts.most_common(15):
            lines.append(f"  - `{key}`: {value}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    catalog_rows = load_harvest_source_ids(args.catalog, source_kind="all")
    rows = read_baseline_rows(args.input_csv)
    baseline_counts = aggregate_baseline(rows)
    upgraded = upgrade_rows(rows, args.detail_timeout, args.fulltext_timeout, args.workers)
    write_rows(upgraded, args.output_csv)
    aggregate_rows = aggregate(upgraded, catalog_rows)
    report = build_report(upgraded, aggregate_rows, baseline_counts, args.output_csv)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(report, encoding="utf-8")
    print(f"upgraded_rows {len(upgraded)}")
    print(f"report {args.output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
