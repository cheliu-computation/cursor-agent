#!/usr/bin/env python3
"""
OpenAlex monthly harvest helper (T182).

Fetches works for one calendar month using publication_date filter.
Example:
  python3 scripts/harvest_openalex_monthly.py \\
    --source-id S116571295 \\
    --year-month 2025-03 \\
    --limit 200 \\
    --append research_ops/02_papers/papers_master.csv

Requires network. Polite use: do not run in tight loops without backoff.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone


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


def fetch_month(source_id: str, year_month: str, limit: int) -> list[dict]:
    """year_month = YYYY-MM"""
    y, m = year_month.split("-")
    start = f"{y}-{m.zfill(2)}-01"
    if m in ("12",):
        next_y, next_m = str(int(y) + 1), "01"
    else:
        next_y, next_m = y, str(int(m) + 1).zfill(2)
    end = f"{next_y}-{next_m.zfill(2)}-01"
    flt = (
        f"primary_location.source.id:{source_id},"
        f"from_publication_date:{start},to_publication_date:{end}"
    )
    rows = []
    cursor = "*"
    while len(rows) < limit and cursor:
        n = min(200, limit - len(rows))
        params = {"filter": flt, "per_page": n, "sort": "publication_date:desc"}
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
            batch = f"T182_month_{year_month}_src_{source_id}"
            rows.append({
                "paper_id": f"openalex:{wid}",
                "title": (w.get("display_name") or "").replace('"', "'")[:500],
                "authors": author_string(w),
                "year": str(w.get("publication_year") or ""),
                "venue": (host.get("display_name") or "")[:200],
                "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
                "pmid": "",
                "arxiv_id": arx[:40],
                "openalex_id": wid,
                "url_abstract": f"https://openalex.org/{wid}",
                "url_pdf": oa[:300],
                "source_batch": batch,
                "tags_modality": "",
                "tags_anatomy": "",
                "tags_disease": "",
                "tags_method": "",
                "notes": f"T182 harvest_window={year_month}; {datetime.now(timezone.utc).date()}",
            })
            if len(rows) >= limit:
                return rows
        cursor = data.get("meta", {}).get("next_cursor")
        if not data.get("results"):
            break
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-id", required=True, help="OpenAlex source id without URL prefix, e.g. S116571295")
    ap.add_argument("--year-month", required=True, help="YYYY-MM")
    ap.add_argument("--limit", type=int, default=200)
    ap.add_argument("--append", required=True, help="Path to papers_master.csv")
    args = ap.parse_args()

    new_rows = fetch_month(args.source_id, args.year_month, args.limit)
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
        existing.append(r)
        ids.add(r["openalex_id"])
        merged += 1
    with open(args.append, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(existing)
    print(f"fetched {len(new_rows)} merged {merged} total {len(existing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
