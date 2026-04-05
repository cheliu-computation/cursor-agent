#!/usr/bin/env python3
"""Final cleanup for terminal Layer-B error tail."""
from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
RS = ROOT / "research_ops/02_papers/paper_reading_status.csv"

TERMINAL_403_HOSTS = {
    "doi.org",
    "academic.oup.com",
    "pmc.ncbi.nlm.nih.gov",
    "onlinelibrary.wiley.com",
    "ir.ymlib.yonsei.ac.kr",
    "hub.hku.hk",
    "s-rsa.com",
    "www.ahajournals.org",
}

TERMINAL_404_HOSTS = {
    "lirias.kuleuven.be",
    "ieeexplore.ieee.org",
    "www.dovepress.com",
}


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
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
        host = urlparse(url).netloc.lower()
        notes = (row.get("notes") or "").lower()
        reason = ""
        if host in TERMINAL_403_HOSTS and ("403" in notes or "forbidden" in notes):
            reason = "terminal_blocked_host"
        elif host in TERMINAL_404_HOSTS and ("404" in notes or "not found" in notes):
            reason = "terminal_missing_artifact"
        elif host == "hdl.handle.net" and (
            "connection reset by peer" in notes
            or "500" in notes
            or "404" in notes
        ):
            reason = "terminal_handle_unstable"
        if not reason:
            continue
        row["fulltext_html_status"] = "skipped_policy"
        row["fulltext_html_artifact"] = ""
        row["last_fetch_utc"] = now
        row["notes"] = ((row.get("notes") or "") + f"; reclassified_policy_skip={reason}")[:240]
        changed += 1

    with RS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("reclassified_terminal_tail_rows", changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
