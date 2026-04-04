#!/usr/bin/env python3
"""Fetch works per source + publication_year using the unified source catalog."""
from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from source_catalog import load_harvest_source_ids, resolve_harvest_source


def author_string(w: dict, max_authors: int = 10) -> str:
    parts = []
    for a in (w.get("authorships") or [])[:max_authors]:
        name = (a.get("author") or {}).get("display_name") or ""
        if name:
            parts.append(name)
    if not parts:
        return ""
    s = "; ".join(parts)
    if len(w.get("authorships") or []) > max_authors:
        s += "; et al."
    return s[:800]


def modality_for_source(_sid: str) -> str:
    return "medical_imaging"


def fetch_year(source_id: str, year: int, limit: int) -> list[dict]:
    flt = f"primary_location.source.id:{source_id},publication_year:{year}"
    rows: list[dict] = []
    cursor = "*"
    while len(rows) < limit and cursor:
        n = min(200, limit - len(rows))
        params: dict[str, str | int] = {"filter": flt, "per_page": n, "sort": "cited_by_count:desc"}
        if cursor != "*":
            params["cursor"] = cursor
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url, timeout=120) as resp:
            data = json.loads(resp.read().decode())
        for w in data.get("results", []):
            wid = (w.get("id") or "").rsplit("/", 1)[-1]
            if not wid:
                continue
            host = (w.get("primary_location") or {}).get("source") or {}
            ids = w.get("ids") or {}
            arx = ids.get("arxiv") or ""
            if arx and "/" in arx:
                arx = arx.rsplit("/", 1)[-1]
            oa = (w.get("open_access") or {}).get("oa_url") or ""
            rows.append({
                "paper_id": f"openalex:{wid}",
                "title": (w.get("display_name") or "").replace('"', "'")[:500],
                "authors": author_string(w),
                "year": str(w.get("publication_year") or year),
                "venue": (host.get("display_name") or "")[:200],
                "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
                "pmid": "",
                "arxiv_id": arx[:40],
                "openalex_id": wid,
                "url_abstract": f"https://openalex.org/{wid}",
                "url_pdf": oa[:300],
                "source_batch": f"T213_{year}_src_{source_id}",
                "tags_modality": modality_for_source(source_id),
                "tags_anatomy": "",
                "tags_disease": "",
                "tags_method": "",
                "notes": f"OpenAlex year slice {year}; {datetime.now(timezone.utc).date()}",
                "harvest_window": f"{year}_venue_rolling",
                "topic_subtag": "",
            })
            if len(rows) >= limit:
                return rows
        cursor = data.get("meta", {}).get("next_cursor")
        if not data.get("results"):
            break
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("--limit-per-source", type=int, default=35)
    ap.add_argument("--append", required=True)
    ap.add_argument(
        "--catalog",
        default="research_ops/01_sources/fetch_source_catalog.csv",
        help="Path to the unified journal/conference fetch catalog.",
    )
    ap.add_argument(
        "--source-kind",
        choices=("all", "journal", "conference"),
        default="all",
        help="Filter the catalog by source kind before harvesting.",
    )
    ap.add_argument(
        "--source-name",
        action="append",
        default=[],
        help=(
            "Optional source selector. May be repeated and may match catalog_id, "
            "source_name, openalex_display_name, or openalex_source_id."
        ),
    )
    args = ap.parse_args()
    catalog_path = Path(args.catalog)

    if args.source_name:
        selected_sources = [resolve_harvest_source(catalog_path, token) for token in args.source_name]
    else:
        selected_sources = load_harvest_source_ids(catalog_path, source_kind=args.source_kind)

    new_rows: list[dict] = []
    for item in selected_sources:
        new_rows.extend(fetch_year(item.openalex_source_id, args.year, args.limit_per_source))

    with open(args.append, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        fields = rdr.fieldnames
        existing = list(rdr)
    if not fields:
        print("empty csv", file=sys.stderr)
        return 1
    ids = {r["openalex_id"].strip() for r in existing}
    merged = 0
    for r in new_rows:
        if r["openalex_id"] in ids:
            continue
        row = {k: r.get(k, "") for k in fields}
        existing.append(row)
        ids.add(r["openalex_id"])
        merged += 1
    with open(args.append, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(existing)
    print(
        f"year {args.year} sources {len(selected_sources)} "
        f"fetched {len(new_rows)} merged {merged} total {len(existing)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
