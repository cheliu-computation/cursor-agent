#!/usr/bin/env python3
"""
Fetch OpenAlex abstract_inverted_index for papers in papers_master by year.
Appends JSONL to research_ops/parsed/abstracts/openalex_abstracts_YYYY.jsonl (gitignored).
Updates research_ops/02_papers/paper_reading_status.csv

Usage:
  python3 scripts/ingest_openalex_abstracts.py --years 2026,2025 --limit-per-year 0
"""
from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from fetch_policy import api_headers

ROOT = Path(__file__).resolve().parents[1]
PM = ROOT / "research_ops/02_papers/papers_master.csv"
RS = ROOT / "research_ops/02_papers/paper_reading_status.csv"
ABS_DIR = ROOT / "research_ops/parsed/abstracts"


def inverted_to_text(inv: dict | None) -> str:
    if not inv:
        return ""
    positions = []
    for word, idxs in inv.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort()
    return " ".join(w for _, w in positions)


def load_reading_status() -> dict[str, dict]:
    by_id: dict[str, dict] = {}
    if not RS.exists():
        return by_id
    with RS.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            oid = r.get("openalex_id", "").strip()
            if oid:
                by_id[oid] = r
    return by_id


def save_reading_status(by_id: dict[str, dict], fieldnames: list[str]) -> None:
    RS.parent.mkdir(parents=True, exist_ok=True)
    with RS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in sorted(by_id.values(), key=lambda x: x.get("openalex_id", "")):
            w.writerow({k: r.get(k, "") for k in fieldnames})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", required=True, help="Comma-separated e.g. 2026,2025")
    ap.add_argument("--limit-per-year", type=int, default=0, help="0 = no limit")
    ap.add_argument("--sleep", type=float, default=0.05, help="Seconds between API calls")
    args = ap.parse_args()
    years = {y.strip() for y in args.years.split(",") if y.strip()}

    rows_pm = []
    with PM.open(newline="", encoding="utf-8") as f:
        rows_pm = list(csv.DictReader(f))

    targets = []
    for r in rows_pm:
        if r.get("year", "").strip() in years:
            targets.append(r)
    by_year: dict[str, list] = {y: [] for y in years}
    for r in targets:
        by_year.setdefault(r["year"].strip(), []).append(r)
    if args.limit_per_year > 0:
        for y in list(by_year.keys()):
            by_year[y] = by_year[y][: args.limit_per_year]

    fieldnames = [
        "openalex_id", "paper_id", "abstract_status", "abstract_artifact",
        "fulltext_html_status", "fulltext_html_artifact", "pdf_status", "pdf_artifact",
        "oa_url_cached", "last_fetch_utc", "notes",
    ]
    by_rs = load_reading_status()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    for year in sorted(years, reverse=True):
        ABS_DIR.mkdir(parents=True, exist_ok=True)
        out_path = ABS_DIR / f"openalex_abstracts_{year}.jsonl"
        n_ok = n_miss = n_err = 0
        with out_path.open("a", encoding="utf-8") as jf:
            for r in by_year.get(year, []):
                oid = (r.get("openalex_id") or "").strip()
                if not oid:
                    continue
                wid = oid if oid.startswith("W") else f"W{oid}"
                url = f"https://api.openalex.org/works/{wid}"
                try:
                    req = urllib.request.Request(url, headers=api_headers())
                    with urllib.request.urlopen(req, timeout=45) as resp:
                        w = json.loads(resp.read().decode())
                except Exception as e:
                    rec = by_rs.get(oid, {})
                    rec.update({
                        "openalex_id": oid,
                        "paper_id": r.get("paper_id", ""),
                        "abstract_status": "error",
                        "abstract_artifact": "",
                        "fulltext_html_status": rec.get("fulltext_html_status", "pending"),
                        "fulltext_html_artifact": rec.get("fulltext_html_artifact", ""),
                        "pdf_status": rec.get("pdf_status", "pending"),
                        "pdf_artifact": rec.get("pdf_artifact", ""),
                        "oa_url_cached": rec.get("oa_url_cached", ""),
                        "last_fetch_utc": now,
                        "notes": f"openalex_fetch_error: {e}"[:200],
                    })
                    by_rs[oid] = rec
                    n_err += 1
                    time.sleep(args.sleep)
                    continue

                inv = w.get("abstract_inverted_index")
                text = inverted_to_text(inv)
                oa = w.get("open_access") or {}
                oa_url = oa.get("oa_url") or ""

                obj = {
                    "openalex_id": wid,
                    "paper_id": r.get("paper_id", ""),
                    "year": year,
                    "title": w.get("display_name") or r.get("title", ""),
                    "abstract": text,
                    "abstract_char_count": len(text),
                    "is_oa": oa.get("is_oa"),
                    "oa_url": oa_url,
                    "landing_page_url": (w.get("primary_location") or {}).get("landing_page_url") or "",
                    "fetched_utc": now,
                }
                jf.write(json.dumps(obj, ensure_ascii=False) + "\n")

                rec = by_rs.get(oid, {})
                st = "ingested" if text.strip() else "missing"
                rec.update({
                    "openalex_id": oid,
                    "paper_id": r.get("paper_id", ""),
                    "abstract_status": st,
                    "abstract_artifact": str(out_path.relative_to(ROOT)),
                    "fulltext_html_status": rec.get("fulltext_html_status", "pending"),
                    "fulltext_html_artifact": rec.get("fulltext_html_artifact", ""),
                    "pdf_status": rec.get("pdf_status", "pending"),
                    "pdf_artifact": rec.get("pdf_artifact", ""),
                    "oa_url_cached": oa_url[:300] if oa_url else rec.get("oa_url_cached", ""),
                    "last_fetch_utc": now,
                    "notes": "T200 OpenAlex abstract layer",
                })
                by_rs[oid] = rec
                if st == "ingested":
                    n_ok += 1
                else:
                    n_miss += 1
                time.sleep(args.sleep)

        print(f"year {year}: ingested={n_ok} missing={n_miss} errors={n_err} -> {out_path}")

    save_reading_status(by_rs, fieldnames)
    print("reading_status rows", len(by_rs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
