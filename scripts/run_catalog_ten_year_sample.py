#!/usr/bin/env python3
"""Run a 10-year journal/conference crawl sample and report success rates."""
from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date
from pathlib import Path

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
DEFAULT_OUTPUT_CSV = ROOT / "research_ops/02_papers/catalog_10yr_sample_status.csv"
DEFAULT_OUTPUT_MD = ROOT / "research_ops/00_meta/2026-04-04_catalog_10yr_sample_report.md"
FULLTEXT_SUCCESS = {"success_html", "success_pdf"}


@dataclass
class SampleRow:
    catalog_id: str
    source_name: str
    source_kind: str
    year: int
    rank_within_source_year: int
    openalex_id: str
    title: str
    doi: str
    oa_url: str
    title_status: str
    abstract_status: str
    fulltext_status: str
    fulltext_detail: str
    fulltext_used_url: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Sample all catalog journals/conferences over the last decade and "
            "report title/abstract/fulltext crawl success rates."
        )
    )
    parser.add_argument(
        "--catalog",
        type=Path,
        default=DEFAULT_CATALOG,
        help="Path to the unified journal/conference fetch catalog.",
    )
    parser.add_argument(
        "--start-year",
        type=int,
        default=2016,
        help="First year to sample (inclusive).",
    )
    parser.add_argument(
        "--end-year",
        type=int,
        default=2026,
        help="Last year to sample (inclusive).",
    )
    parser.add_argument(
        "--per-source-per-year",
        type=int,
        default=10,
        help="How many papers to fetch per source per year.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.05,
        help="Pause between OpenAlex list calls.",
    )
    parser.add_argument(
        "--fulltext-timeout",
        type=int,
        default=20,
        help="Timeout in seconds for each fulltext request.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Concurrent workers for fulltext probes.",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=DEFAULT_OUTPUT_CSV,
        help="Where to write the sample status CSV.",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=DEFAULT_OUTPUT_MD,
        help="Where to write the markdown report.",
    )
    parser.add_argument(
        "--from-csv",
        type=Path,
        help="Reuse an existing sample-status CSV instead of re-running network fetches.",
    )
    return parser.parse_args()


def pct(ok_count: int, total: int) -> str:
    return f"{(100.0 * ok_count / total):.1f}%" if total else "0.0%"


def format_metric(ok_count: int, total: int) -> str:
    return f"{ok_count}/{total} ({pct(ok_count, total)})"


def openalex_works(source_id: str, year: int, limit: int) -> list[dict]:
    params = {
        "filter": f"primary_location.source.id:{source_id},publication_year:{year}",
        "per_page": limit,
        "sort": "cited_by_count:desc",
    }
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=api_headers())
    with urllib.request.urlopen(req, timeout=60) as resp:
        payload = json.loads(resp.read().decode())
    return list(payload.get("results", []))


def harvest_sample(
    catalog_rows: list[HarvestSource],
    start_year: int,
    end_year: int,
    per_source_per_year: int,
    sleep_seconds: float,
) -> list[SampleRow]:
    samples: list[SampleRow] = []
    for year in range(start_year, end_year + 1):
        for source in catalog_rows:
            results = openalex_works(source.openalex_source_id, year, per_source_per_year)
            for idx, work in enumerate(results, start=1):
                openalex_id = (work.get("id") or "").rsplit("/", 1)[-1]
                title = (work.get("display_name") or work.get("title") or "").strip()
                doi = (work.get("doi") or "").replace("https://doi.org/", "").strip()
                oa_url = ((work.get("open_access") or {}).get("oa_url") or "").strip()
                samples.append(
                    SampleRow(
                        catalog_id=source.catalog_id,
                        source_name=source.source_name,
                        source_kind=source.source_kind,
                        year=year,
                        rank_within_source_year=idx,
                        openalex_id=openalex_id,
                        title=title,
                        doi=doi,
                        oa_url=oa_url,
                        title_status="success" if title else "missing",
                        abstract_status=(
                            "success"
                            if bool(work.get("abstract_inverted_index"))
                            else "missing"
                        ),
                        fulltext_status="pending",
                        fulltext_detail="",
                        fulltext_used_url="",
                    )
                )
            time.sleep(sleep_seconds)
    return samples


def _probe_single(row: SampleRow, timeout: int) -> SampleRow:
    if not row.oa_url:
        row.fulltext_status = "missing_url"
        row.fulltext_detail = "oa_url_missing"
        return row

    url = canonicalize_url(row.oa_url)
    policy_skip = classify_policy_skip(url, row.doi)
    if policy_skip:
        row.fulltext_status = "skipped_policy"
        row.fulltext_detail = policy_skip
        return row

    last_err = ""
    for attempt in url_attempts(url):
        try:
            req = urllib.request.Request(attempt, headers=browser_headers())
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                ctype = (resp.headers.get("Content-Type") or "").lower()
                _ = resp.read(2048)
            row.fulltext_used_url = attempt
            row.fulltext_detail = ctype[:120]
            if "pdf" in ctype or attempt.lower().split("?", 1)[0].endswith(".pdf"):
                row.fulltext_status = "success_pdf"
            else:
                row.fulltext_status = "success_html"
            return row
        except urllib.error.HTTPError as exc:
            last_err = f"HTTP {exc.code}: {exc.reason}"
            maybe_skip = classify_policy_skip(attempt, row.doi)
            if maybe_skip:
                row.fulltext_status = "skipped_policy"
                row.fulltext_detail = maybe_skip
                row.fulltext_used_url = attempt
                return row
        except Exception as exc:  # noqa: BLE001
            last_err = str(exc)[:180]

    terminal = classify_terminal_error(url, last_err, row.doi)
    if terminal:
        row.fulltext_status = "skipped_policy"
        row.fulltext_detail = terminal
    else:
        row.fulltext_status = "error"
        row.fulltext_detail = last_err[:120]
    return row


def probe_fulltext(rows: list[SampleRow], timeout: int, workers: int) -> list[SampleRow]:
    out: list[SampleRow] = []
    with ThreadPoolExecutor(max_workers=max(workers, 1)) as executor:
        future_map = {executor.submit(_probe_single, row, timeout): row for row in rows}
        for future in as_completed(future_map):
            out.append(future.result())
    out.sort(key=lambda row: (row.source_kind, row.source_name, row.year, row.rank_within_source_year))
    return out


def write_csv(rows: list[SampleRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "catalog_id",
        "source_name",
        "source_kind",
        "year",
        "rank_within_source_year",
        "openalex_id",
        "title",
        "doi",
        "oa_url",
        "title_status",
        "abstract_status",
        "fulltext_status",
        "fulltext_detail",
        "fulltext_used_url",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "catalog_id": row.catalog_id,
                "source_name": row.source_name,
                "source_kind": row.source_kind,
                "year": row.year,
                "rank_within_source_year": row.rank_within_source_year,
                "openalex_id": row.openalex_id,
                "title": row.title,
                "doi": row.doi,
                "oa_url": row.oa_url,
                "title_status": row.title_status,
                "abstract_status": row.abstract_status,
                "fulltext_status": row.fulltext_status,
                "fulltext_detail": row.fulltext_detail,
                "fulltext_used_url": row.fulltext_used_url,
            })


def read_csv(path: Path) -> list[SampleRow]:
    rows: list[SampleRow] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for item in csv.DictReader(handle):
            rows.append(
                SampleRow(
                    catalog_id=(item.get("catalog_id") or "").strip(),
                    source_name=(item.get("source_name") or "").strip(),
                    source_kind=(item.get("source_kind") or "").strip(),
                    year=int(item.get("year") or 0),
                    rank_within_source_year=int(item.get("rank_within_source_year") or 0),
                    openalex_id=(item.get("openalex_id") or "").strip(),
                    title=(item.get("title") or "").strip(),
                    doi=(item.get("doi") or "").strip(),
                    oa_url=(item.get("oa_url") or "").strip(),
                    title_status=(item.get("title_status") or "").strip(),
                    abstract_status=(item.get("abstract_status") or "").strip(),
                    fulltext_status=(item.get("fulltext_status") or "").strip(),
                    fulltext_detail=(item.get("fulltext_detail") or "").strip(),
                    fulltext_used_url=(item.get("fulltext_used_url") or "").strip(),
                )
            )
    return rows


def aggregate_rows(rows: list[SampleRow]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], dict[str, int]] = defaultdict(
        lambda: {
            "total": 0,
            "title_ok": 0,
            "abstract_ok": 0,
            "fulltext_ok": 0,
        }
    )
    for row in rows:
        key = (row.source_kind, row.source_name)
        grouped[key]["total"] += 1
        grouped[key]["title_ok"] += int(row.title_status == "success")
        grouped[key]["abstract_ok"] += int(row.abstract_status == "success")
        grouped[key]["fulltext_ok"] += int(row.fulltext_status in FULLTEXT_SUCCESS)

    ordered: list[dict[str, object]] = []
    for (source_kind, source_name), counts in grouped.items():
        ordered.append(
            {
                "source_kind": source_kind,
                "source_name": source_name,
                **counts,
            }
        )
    ordered.sort(key=lambda row: (row["source_kind"], row["source_name"]))
    return ordered


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
    rows: list[SampleRow],
    aggregate: list[dict[str, object]],
    start_year: int,
    end_year: int,
    per_source_per_year: int,
    output_csv: Path,
) -> str:
    overall = overall_row(aggregate)
    csv_label = str(output_csv)
    try:
        csv_label = str(output_csv.resolve().relative_to(ROOT))
    except ValueError:
        csv_label = str(output_csv)
    lines = [
        "# 全部期刊会议 10 年样本爬取成功率",
        "",
        f"日期：{TODAY}",
        "",
        "## 抽样口径",
        "",
        f"- 统一抓取清单：`research_ops/01_sources/fetch_source_catalog.csv`。",
        f"- 时间范围：**{start_year}–{end_year}**（按“10 年前到现在”口径）。",
        f"- 抽样规则：每个期刊/会议、每个年份最多抓 **{per_source_per_year}** 篇。",
        f"- 样本明细：`{csv_label}`。",
        "- 标题成功：OpenAlex 返回标题非空。",
        "- 摘要成功：OpenAlex 列表结果中 `abstract_inverted_index` 非空。",
        "- 正文成功：对 `oa_url` 实际发起抓取请求，并成功拿到 HTML/PDF 响应。",
        "",
        "## 总体结果",
        "",
        render_table([overall]),
        "",
        "## 分来源结果",
        "",
        render_table(aggregate),
        "",
    ]

    year_counts: dict[int, int] = defaultdict(int)
    for row in rows:
        year_counts[row.year] += 1
    lines.extend(
        [
            "## 各年份样本量",
            "",
            "| 年份 | 样本数 |",
            "| --- | ---: |",
        ]
    )
    for year in range(start_year, end_year + 1):
        lines.append(f"| {year} | {year_counts.get(year, 0)} |")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    if args.from_csv:
        probed = read_csv(args.from_csv)
        output_csv = args.from_csv
    else:
        catalog_rows = load_harvest_source_ids(args.catalog, source_kind="all")
        harvested = harvest_sample(
            catalog_rows=catalog_rows,
            start_year=args.start_year,
            end_year=args.end_year,
            per_source_per_year=args.per_source_per_year,
            sleep_seconds=args.sleep,
        )
        probed = probe_fulltext(
            rows=harvested,
            timeout=args.fulltext_timeout,
            workers=args.workers,
        )
        write_csv(probed, args.output_csv)
        output_csv = args.output_csv
    aggregate = aggregate_rows(probed)
    report = build_report(
        rows=probed,
        aggregate=aggregate,
        start_year=args.start_year,
        end_year=args.end_year,
        per_source_per_year=args.per_source_per_year,
        output_csv=output_csv,
    )
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(report, encoding="utf-8")
    print(f"sample_rows {len(probed)}")
    print(f"report {args.output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
