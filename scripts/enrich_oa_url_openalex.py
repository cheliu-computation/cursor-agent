#!/usr/bin/env python3
"""T206: backfill oa_url_cached from OpenAlex works API where missing."""
from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RS = ROOT / "research_ops/02_papers/paper_reading_status.csv"
UA = "Mozilla/5.0 (compatible; research-ops-bot/1.0; +https://example.invalid)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=250, help="Max rows to fetch from API")
    ap.add_argument("--sleep", type=float, default=0.08)
    args = ap.parse_args()

    with RS.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        fieldnames = rdr.fieldnames
        rows = list(rdr)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    n_api = n_filled = 0
    for r in rows:
        if n_api >= args.limit:
            break
        cur = (r.get("oa_url_cached") or "").strip()
        if cur.lower().startswith("http"):
            continue
        oid = (r.get("openalex_id") or "").strip()
        if not oid:
            continue
        wid = oid if oid.startswith("W") else f"W{oid}"
        url = f"https://api.openalex.org/works/{wid}"
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                w = json.loads(resp.read().decode())
        except Exception as e:
            r["notes"] = (r.get("notes", "") + f"; T206_oa_fetch_error={e}")[:220]
            n_api += 1
            time.sleep(args.sleep)
            continue

        oa = w.get("open_access") or {}
        oa_url = (oa.get("oa_url") or "").strip()
        n_api += 1
        if oa_url:
            r["oa_url_cached"] = oa_url[:300]
            r["last_fetch_utc"] = now
            r["notes"] = (r.get("notes", "") + "; T206_openalex_oa_url")[:220]
            n_filled += 1
        time.sleep(args.sleep)

    with RS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})

    print("api_calls", n_api, "oa_url_filled", n_filled)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
