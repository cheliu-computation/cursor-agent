#!/usr/bin/env python3
"""T215: append Layer B fetch errors to retry_queue.csv."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RS = ROOT / "research_ops/02_papers/paper_reading_status.csv"
RQ = ROOT / "research_ops/manifests/retry_queue.csv"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=120)
    args = ap.parse_args()

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    with RQ.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        fn = rdr.fieldnames
        rows = list(rdr)

    existing_urls = {
        (r.get("manifest_id_or_url") or "").strip()
        for r in rows
        if (r.get("manifest_id_or_url") or "").strip().lower().startswith("http")
    }

    n = 0
    with RS.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if n >= args.limit:
                break
            if (r.get("fulltext_html_status") or "").strip() != "error":
                continue
            url = (r.get("oa_url_cached") or "").strip()
            if not url.lower().startswith("http"):
                continue
            if url in existing_urls:
                continue
            oid = (r.get("openalex_id") or "").strip()
            rows.append({
                "queue_id": f"RQ-T215-{n+1:05d}",
                "manifest_id_or_url": url[:500],
                "failure_type": "download",
                "attempt_count": "1",
                "last_attempt_utc": r.get("last_fetch_utc", "") or now,
                "next_action": "retry_with_backoff",
                "notes": f"openalex_id={oid}; layer_b_html"[:200],
            })
            existing_urls.add(url)
            n += 1

    with RQ.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fn)
        w.writeheader()
        w.writerows(rows)

    print("appended", n, "total_rows", len(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
