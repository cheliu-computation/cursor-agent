#!/usr/bin/env python3
"""Reclassify arXiv/preprint full-text rows under the narrowed scope policy."""
from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from fetch_policy import allow_arxiv_fallback

ROOT = Path(__file__).resolve().parents[1]
PM = ROOT / "research_ops/02_papers/papers_master.csv"
RS = ROOT / "research_ops/02_papers/paper_reading_status.csv"


def load_meta() -> dict[str, dict[str, str]]:
    meta: dict[str, dict[str, str]] = {}
    with PM.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            oid = (row.get("openalex_id") or "").strip()
            if not oid:
                continue
            meta[oid] = {
                "year": (row.get("year") or "").strip(),
                "venue": (row.get("venue") or "").strip(),
                "doi": (row.get("doi") or "").strip(),
                "tags_modality": (row.get("tags_modality") or "").strip(),
            }
    return meta


def main() -> int:
    meta = load_meta()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    with RS.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    if not fieldnames:
        raise SystemExit("paper_reading_status.csv missing header")

    changed = 0
    for row in rows:
        status = (row.get("fulltext_html_status") or "").strip()
        if status not in {"pending", "error", "pdf_cached", "ingested"}:
            continue
        url = (row.get("oa_url_cached") or "").strip()
        if "arxiv.org" not in urlparse(url).netloc.lower():
            continue
        oid = (row.get("openalex_id") or "").strip()
        m = meta.get(oid, {})
        if allow_arxiv_fallback(
            url,
            m.get("year", ""),
            m.get("venue", ""),
            m.get("doi", ""),
            m.get("tags_modality", ""),
        ):
            continue
        row["fulltext_html_status"] = "skipped_policy"
        row["fulltext_html_artifact"] = ""
        row["last_fetch_utc"] = now
        note = row.get("notes", "")
        row["notes"] = (note + "; scope_skip=preprint_fulltext_filtered")[:240]
        changed += 1

    with RS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("reclassified_preprint_scope_rows", changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
