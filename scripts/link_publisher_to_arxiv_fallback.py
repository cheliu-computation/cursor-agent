#!/usr/bin/env python3
"""Link publisher-backed records to arXiv fallback copies by normalized title."""
from __future__ import annotations

import csv
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PM = ROOT / "research_ops/02_papers/papers_master.csv"
RS = ROOT / "research_ops/02_papers/paper_reading_status.csv"
OUT = ROOT / "research_ops/19_linking/publisher_arxiv_fallback_links.csv"

OUT_FIELDS = [
    "link_id",
    "publisher_openalex_id",
    "publisher_title",
    "publisher_year",
    "publisher_venue",
    "publisher_doi",
    "publisher_current_url",
    "publisher_fulltext_status",
    "fallback_openalex_id",
    "fallback_title",
    "fallback_year",
    "fallback_venue",
    "fallback_doi",
    "fallback_url",
    "match_type",
    "eligibility",
    "notes",
]


def norm_title(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def status_map() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with RS.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            oid = (row.get("openalex_id") or "").strip()
            if oid:
                out[oid] = row
    return out


def is_arxiv_like(row: dict[str, str]) -> bool:
    venue = (row.get("venue") or "").lower()
    modality = (row.get("tags_modality") or "").lower()
    doi = (row.get("doi") or "").lower()
    return (
        "arxiv" in venue
        or "preprint" in modality
        or doi.startswith("10.48550/arxiv.")
    )


def publisher_backed(row: dict[str, str]) -> bool:
    return not is_arxiv_like(row)


def main() -> int:
    rs = status_map()

    preprints: dict[str, list[dict[str, str]]] = {}
    publishers: list[dict[str, str]] = []
    with PM.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row = dict(row)
            norm = norm_title(row.get("title", ""))
            if not norm:
                continue
            row["_norm_title"] = norm
            row["_status"] = (rs.get((row.get("openalex_id") or "").strip(), {}) or {}).get(
                "fulltext_html_status", ""
            )
            row["_url"] = (rs.get((row.get("openalex_id") or "").strip(), {}) or {}).get(
                "oa_url_cached", ""
            )
            if is_arxiv_like(row):
                preprints.setdefault(norm, []).append(row)
            elif publisher_backed(row):
                publishers.append(row)

    rows: list[dict[str, str]] = []
    idx = 1
    for pub in publishers:
        matches = preprints.get(pub["_norm_title"], [])
        if not matches:
            continue
        current_url = pub["_url"]
        current_status = pub["_status"]
        for pre in matches:
            fallback_url = (
                (rs.get((pre.get("openalex_id") or "").strip(), {}) or {}).get("oa_url_cached", "")
                or (pre.get("url_pdf") or "")
            )
            eligibility = "no"
            pub_year = (pub.get("year") or "").strip()
            try:
                year_ok = int(pub_year) >= 2024
            except ValueError:
                year_ok = False
            if year_ok and current_status in {"error", "pending", "skipped_policy"}:
                host = urlparse((current_url or "").strip()).netloc.lower()
                if host and "arxiv.org" not in host:
                    eligibility = "yes"
            rows.append({
                "link_id": f"ARXIVFB{idx:04d}",
                "publisher_openalex_id": (pub.get("openalex_id") or "").strip(),
                "publisher_title": (pub.get("title") or "")[:500],
                "publisher_year": pub_year,
                "publisher_venue": (pub.get("venue") or "")[:200],
                "publisher_doi": (pub.get("doi") or "")[:200],
                "publisher_current_url": (current_url or "")[:500],
                "publisher_fulltext_status": current_status,
                "fallback_openalex_id": (pre.get("openalex_id") or "").strip(),
                "fallback_title": (pre.get("title") or "")[:500],
                "fallback_year": (pre.get("year") or "").strip(),
                "fallback_venue": (pre.get("venue") or "")[:200],
                "fallback_doi": (pre.get("doi") or "")[:200],
                "fallback_url": (fallback_url or "")[:500],
                "match_type": "normalized_title_exact",
                "eligibility": eligibility,
                "notes": "publisher-title matched to arXiv/preprint fallback",
            })
            idx += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OUT_FIELDS)
        w.writeheader()
        w.writerows(rows)

    eligible = sum(1 for r in rows if r["eligibility"] == "yes")
    print("fallback_links", len(rows), "eligible_now", eligible)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
