#!/usr/bin/env python3
"""T206: backfill oa_url_cached from Crossref work `link` list (polite User-Agent)."""
from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PM = ROOT / "research_ops/02_papers/papers_master.csv"
RS = ROOT / "research_ops/02_papers/paper_reading_status.csv"
# Polite pool: include mailto per https://github.com/CrossRef/rest-api-doc#good-manners
UA = "research-ops-bot/1.0 (mailto:research-ops@example.invalid)"


def pick_url(links: list[dict]) -> str:
    if not links:
        return ""
    html = [
        x for x in links
        if (x.get("content-type") or "").lower().startswith("text/html")
    ]
    pool = html or links
    vor = [x for x in pool if (x.get("content-version") or "").lower() == "vor"]
    use = vor[0] if vor else pool[0]
    return (use.get("URL") or "").strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=400)
    ap.add_argument("--sleep", type=float, default=0.15)
    args = ap.parse_args()

    meta: dict[str, tuple[str, str]] = {}
    with PM.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            oid = (r.get("openalex_id") or "").strip()
            doi = (r.get("doi") or "").strip()
            yr = (r.get("year") or "").strip()
            if oid and doi:
                meta[oid] = (doi, yr)

    with RS.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        fieldnames = rdr.fieldnames
        rows = list(rdr)

    candidates = []
    for r in rows:
        if (r.get("oa_url_cached") or "").strip().lower().startswith("http"):
            continue
        oid = (r.get("openalex_id") or "").strip()
        if oid not in meta:
            continue
        doi, yr = meta[oid]
        try:
            yint = -int(yr) if yr.isdigit() else 0
        except ValueError:
            yint = 0
        candidates.append((yint, oid, r))
    candidates.sort()

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    n_api = n_filled = 0
    for _, oid, r in candidates:
        if n_api >= args.limit:
            break
        doi, _ = meta[oid]
        enc = urllib.parse.quote(doi, safe="")
        url = f"https://api.crossref.org/works/{enc}"
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                payload = json.loads(resp.read().decode())
        except Exception as e:
            r["notes"] = (r.get("notes", "") + f"; T206_crossref_err={e}")[:220]
            n_api += 1
            time.sleep(args.sleep)
            continue
        n_api += 1
        msg = payload.get("message") or {}
        picked = pick_url(msg.get("link") or [])
        if picked.lower().startswith("http"):
            r["oa_url_cached"] = picked[:300]
            r["last_fetch_utc"] = now
            r["notes"] = (r.get("notes", "") + "; T206_crossref_link")[:220]
            n_filled += 1
        time.sleep(args.sleep)

    with RS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})

    print("crossref_calls", n_api, "oa_url_filled", n_filled)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
