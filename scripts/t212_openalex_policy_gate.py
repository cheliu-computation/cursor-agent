#!/usr/bin/env python3
"""T212: set fulltext_html_status=skipped_policy when OpenAlex says not OA and no local URL."""
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
    ap.add_argument("--limit", type=int, default=250)
    ap.add_argument("--sleep", type=float, default=0.08)
    args = ap.parse_args()

    with RS.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        fieldnames = rdr.fieldnames
        rows = list(rdr)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    n_api = n_skip = 0
    for r in rows:
        if n_api >= args.limit:
            break
        if (r.get("oa_url_cached") or "").strip().lower().startswith("http"):
            continue
        st = (r.get("fulltext_html_status") or "").strip()
        if st not in ("", "pending"):
            continue
        oid = (r.get("openalex_id") or "").strip()
        if not oid:
            continue
        wid = oid if oid.startswith("W") else f"W{oid}"
        url = f"https://api.openalex.org/works/{wid}"
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=40) as resp:
                w = json.loads(resp.read().decode())
        except Exception as e:
            r["notes"] = (r.get("notes", "") + f"; T212_openalex_err={e}")[:220]
            n_api += 1
            time.sleep(args.sleep)
            continue
        n_api += 1
        oa = w.get("open_access") or {}
        is_oa = oa.get("is_oa")
        if is_oa is False:
            r["fulltext_html_status"] = "skipped_policy"
            r["last_fetch_utc"] = now
            r["notes"] = (r.get("notes", "") + "; T212_openalex_is_oa_false")[:220]
            n_skip += 1
        time.sleep(args.sleep)

    with RS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})

    print("openalex_calls", n_api, "skipped_policy", n_skip)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
