#!/usr/bin/env python3
"""Aggregate per-source fetch success rates and sample-based validation."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

FULLTEXT_SUCCESS_STATUSES = {"ingested", "pdf_cached"}


@dataclass(frozen=True)
class Record:
    source: str
    paper_id: str
    title_ok: bool
    abstract_ok: bool
    fulltext_ok: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compute per-source title/abstract/fulltext success rates and "
            "optionally validate each source with an isolated subprocess sample."
        )
    )
    parser.add_argument(
        "--papers",
        type=Path,
        default=Path("research_ops/02_papers/papers_master.csv"),
        help="Path to papers_master.csv",
    )
    parser.add_argument(
        "--reading-status",
        type=Path,
        default=Path("research_ops/02_papers/paper_reading_status.csv"),
        help="Path to paper_reading_status.csv",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        help="Write the Markdown report to this path.",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=0,
        help=(
            "Validate up to N rows per source in isolated subprocesses. "
            "Set to 0 to skip validation."
        ),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=54,
        help="Deterministic seed for sample-based validation.",
    )
    parser.add_argument(
        "--worker-source",
        help=argparse.SUPPRESS,
    )
    return parser.parse_args()


def normalize_source(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return "NO_OA_URL"
    host = urlparse(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host or "NO_OA_URL"


def load_titles(path: Path) -> dict[str, bool]:
    titles: dict[str, bool] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            titles[row["paper_id"]] = bool((row.get("title") or "").strip())
    return titles


def load_records(papers_path: Path, reading_status_path: Path) -> list[Record]:
    title_index = load_titles(papers_path)
    records: list[Record] = []
    with reading_status_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            source = normalize_source(row.get("oa_url_cached", ""))
            records.append(
                Record(
                    source=source,
                    paper_id=row["paper_id"],
                    title_ok=title_index.get(row["paper_id"], False),
                    abstract_ok=(row.get("abstract_status") or "").strip()
                    == "ingested",
                    fulltext_ok=(row.get("fulltext_html_status") or "").strip()
                    in FULLTEXT_SUCCESS_STATUSES,
                )
            )
    return records


def aggregate(records: Iterable[Record]) -> list[dict[str, object]]:
    grouped: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "total": 0,
            "title_ok": 0,
            "abstract_ok": 0,
            "fulltext_ok": 0,
        }
    )
    for record in records:
        bucket = grouped[record.source]
        bucket["total"] += 1
        bucket["title_ok"] += int(record.title_ok)
        bucket["abstract_ok"] += int(record.abstract_ok)
        bucket["fulltext_ok"] += int(record.fulltext_ok)

    rows: list[dict[str, object]] = []
    for source, counts in grouped.items():
        row = {"source": source, **counts}
        rows.append(row)
    rows.sort(key=lambda row: (-int(row["total"]), str(row["source"])))
    return rows


def overall_row(rows: Iterable[dict[str, object]]) -> dict[str, object]:
    total = title_ok = abstract_ok = fulltext_ok = 0
    for row in rows:
        total += int(row["total"])
        title_ok += int(row["title_ok"])
        abstract_ok += int(row["abstract_ok"])
        fulltext_ok += int(row["fulltext_ok"])
    return {
        "source": "ALL_SOURCES",
        "total": total,
        "title_ok": title_ok,
        "abstract_ok": abstract_ok,
        "fulltext_ok": fulltext_ok,
    }


def pct(count: int, total: int) -> str:
    return f"{(100.0 * count / total):.1f}%" if total else "0.0%"


def format_metric(ok_count: int, total: int) -> str:
    return f"{ok_count}/{total} ({pct(ok_count, total)})"


def render_exact_table(rows: Iterable[dict[str, object]]) -> str:
    lines = [
        "| 来源 | 样本总数 | 标题成功率 | 摘要成功率 | 正文成功率 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        total = int(row["total"])
        lines.append(
            "| {source} | {total} | {title} | {abstract} | {fulltext} |".format(
                source=row["source"],
                total=total,
                title=format_metric(int(row["title_ok"]), total),
                abstract=format_metric(int(row["abstract_ok"]), total),
                fulltext=format_metric(int(row["fulltext_ok"]), total),
            )
        )
    return "\n".join(lines)


def render_validation_table(rows: Iterable[dict[str, object]]) -> str:
    lines = [
        "| 来源 | 验证抽样数 | 标题成功率 | 摘要成功率 | 正文成功率 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        sample_size = int(row["sample_size"])
        lines.append(
            "| {source} | {sample_size} | {title} | {abstract} | {fulltext} |".format(
                source=row["source"],
                sample_size=sample_size,
                title=format_metric(int(row["title_ok"]), sample_size),
                abstract=format_metric(int(row["abstract_ok"]), sample_size),
                fulltext=format_metric(int(row["fulltext_ok"]), sample_size),
            )
        )
    return "\n".join(lines)


def top_findings(rows: list[dict[str, object]]) -> list[str]:
    eligible = [row for row in rows if int(row["total"]) >= 20]
    findings: list[str] = []
    if not eligible:
        return findings

    best_abstract = max(eligible, key=lambda row: int(row["abstract_ok"]) / int(row["total"]))
    best_fulltext = max(eligible, key=lambda row: int(row["fulltext_ok"]) / int(row["total"]))
    weakest_fulltext = min(
        eligible,
        key=lambda row: int(row["fulltext_ok"]) / int(row["total"]),
    )

    findings.append(
        (
            f"`{best_abstract['source']}` 在样本量 >=20 的来源里摘要成功率最高，"
            f"为 {format_metric(int(best_abstract['abstract_ok']), int(best_abstract['total']))}。"
        )
    )
    findings.append(
        (
            f"`{best_fulltext['source']}` 在样本量 >=20 的来源里正文成功率最高，"
            f"为 {format_metric(int(best_fulltext['fulltext_ok']), int(best_fulltext['total']))}。"
        )
    )
    findings.append(
        (
            f"`{weakest_fulltext['source']}` 在样本量 >=20 的来源里正文成功率最低，"
            f"为 {format_metric(int(weakest_fulltext['fulltext_ok']), int(weakest_fulltext['total']))}。"
        )
    )
    return findings


def worker_sample(records: list[Record], source: str, sample_size: int, seed: int) -> dict[str, object]:
    source_records = [record for record in records if record.source == source]
    digest = hashlib.sha256(f"{seed}:{source}".encode("utf-8")).hexdigest()
    worker_seed = int(digest[:16], 16)
    rng = random.Random(worker_seed)
    chosen = (
        rng.sample(source_records, min(sample_size, len(source_records)))
        if source_records
        else []
    )
    return {
        "source": source,
        "sample_size": len(chosen),
        "title_ok": sum(record.title_ok for record in chosen),
        "abstract_ok": sum(record.abstract_ok for record in chosen),
        "fulltext_ok": sum(record.fulltext_ok for record in chosen),
    }


def run_worker(args: argparse.Namespace) -> int:
    records = load_records(args.papers, args.reading_status)
    result = worker_sample(records, args.worker_source, args.sample_size, args.seed)
    print(json.dumps(result, ensure_ascii=True))
    return 0


def run_validation(args: argparse.Namespace, rows: list[dict[str, object]]) -> list[dict[str, object]]:
    validation_rows: list[dict[str, object]] = []
    script_path = Path(__file__).resolve()
    for row in rows:
        source = str(row["source"])
        completed = subprocess.run(
            [
                sys.executable,
                str(script_path),
                "--papers",
                str(args.papers),
                "--reading-status",
                str(args.reading_status),
                "--sample-size",
                str(args.sample_size),
                "--seed",
                str(args.seed),
                "--worker-source",
                source,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        validation_rows.append(json.loads(completed.stdout))
    validation_rows.sort(key=lambda row: (-int(row["sample_size"]), str(row["source"])))
    return validation_rows


def build_markdown(
    exact_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
    sample_size: int,
) -> str:
    overall = overall_row(exact_rows)
    lines = [
        "# 爬取来源成功率汇总",
        "",
        "日期：2026-04-04",
        "",
        "## 统计口径",
        "",
        "- 标题成功：`papers_master.csv` 中 `title` 非空。",
        "- 摘要成功：`paper_reading_status.csv` 中 `abstract_status=ingested`。",
        "- 正文成功：`paper_reading_status.csv` 中 `fulltext_html_status in {ingested, pdf_cached}`。",
        "- 来源：按 `oa_url_cached` 的域名归一化分组；无 URL 记为 `NO_OA_URL`。",
        "",
        "## 总体结果",
        "",
        render_exact_table([overall]),
        "",
        "## 主要发现",
        "",
    ]
    for finding in top_findings(exact_rows):
        lines.append(f"- {finding}")
    if not top_findings(exact_rows):
        lines.append("- 当前没有满足最小样本量阈值的来源。")

    lines.extend(
        [
            "",
            "## 分来源精确统计",
            "",
            render_exact_table(exact_rows),
            "",
        ]
    )

    if sample_size > 0:
        lines.extend(
            [
                f"## 分来源抽样验证（每个来源最多 {sample_size} 条）",
                "",
                "- 每个来源使用独立 Python 子进程重新加载 CSV 并抽样，作为隔离 session 的验证近似。",
                "- 抽样验证复核的是**当前仓库中记录的状态一致性**，不是在线重新抓取远端页面。",
                "",
                render_validation_table(validation_rows),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    if args.worker_source:
        return run_worker(args)

    records = load_records(args.papers, args.reading_status)
    exact_rows = aggregate(records)
    validation_rows: list[dict[str, object]] = []
    if args.sample_size > 0:
        validation_rows = run_validation(args, exact_rows)

    markdown = build_markdown(exact_rows, validation_rows, args.sample_size)
    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(markdown, encoding="utf-8")
    else:
        sys.stdout.write(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
