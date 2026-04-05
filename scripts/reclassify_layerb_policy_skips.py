#!/usr/bin/env python3
"""Reclassify persistent Layer B publisher blocks into policy skips."""
from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

from fetch_policy import classify_policy_skip, classify_terminal_error

ROOT = Path(__file__).resolve().parents[1]
PM = ROOT / "research_ops/02_papers/papers_master.csv"
RS = ROOT / "research_ops/02_papers/paper_reading_status.csv"


def doi_map() -> dict[str, str]:
    out: dict[str, str] = {}
    with PM.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            oid = (row.get("openalex_id") or "").strip()
            if oid:
                out[oid] = (row.get("doi") or "").strip()
    return out


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    dois = doi_map()

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
        url = (row.get("oa_url_cached") or "").strip()
        if not url:
            continue
        oid = (row.get("openalex_id") or "").strip()
        reason = classify_policy_skip(url, dois.get(oid, ""))
        if not reason:
            reason = classify_terminal_error(url, row.get("notes", ""), dois.get(oid, ""))
        if not reason:
            continue
        row["fulltext_html_status"] = "skipped_policy"
        row["fulltext_html_artifact"] = ""
        row["last_fetch_utc"] = now
        note = row.get("notes", "")
        row["notes"] = (note + f"; reclassified_policy_skip={reason}")[:240]
        changed += 1

    with RS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("reclassified_rows", changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
