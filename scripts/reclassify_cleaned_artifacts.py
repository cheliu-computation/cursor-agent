#!/usr/bin/env python3
"""Reclassify rows whose cached artifacts were intentionally cleaned."""
from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RS = ROOT / "research_ops/02_papers/paper_reading_status.csv"


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with RS.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    if not fieldnames:
        raise SystemExit("paper_reading_status.csv missing header")

    changed = 0
    for row in rows:
        if (row.get("fulltext_html_status") or "").strip() != "error":
            continue
        notes = (row.get("notes") or "").lower()
        if "corpus_cleanup_missing_file" not in notes and "pdf_cache_missing_cleaned" not in notes:
            continue
        row["fulltext_html_status"] = "skipped_policy"
        row["fulltext_html_artifact"] = ""
        row["last_fetch_utc"] = now
        row["notes"] = ((row.get("notes") or "") + "; scope_skip=artifact_cleaned")[:240]
        changed += 1

    with RS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("reclassified_cleaned_artifact_rows", changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
