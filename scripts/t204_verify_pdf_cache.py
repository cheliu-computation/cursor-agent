#!/usr/bin/env python3
"""T204: verify up to N cached OA PDFs against download_manifest SHA256; set pdf_status."""
from __future__ import annotations

import argparse
import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RS = ROOT / "research_ops/02_papers/paper_reading_status.csv"
MNF = ROOT / "research_ops/manifests/download_manifest.csv"


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=20)
    args = ap.parse_args()

    by_path: dict[str, dict] = {}
    with MNF.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            p = (r.get("local_path") or "").strip()
            if p and p not in by_path:
                by_path[p] = r

    with RS.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        fieldnames = rdr.fieldnames
        rows = list(rdr)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    n_ok = 0
    for r in sorted(rows, key=lambda x: x.get("openalex_id", "")):
        if n_ok >= args.limit:
            break
        if (r.get("fulltext_html_status") or "").strip() != "pdf_cached":
            continue
        if (r.get("pdf_status") or "").strip() == "ingested":
            continue
        art = (r.get("fulltext_html_artifact") or "").strip()
        if not art.endswith(".pdf"):
            continue
        fp = ROOT / art
        if not fp.is_file():
            continue
        man = by_path.get(art)
        if not man:
            continue
        expected = (man.get("file_hash") or "").strip().lower()
        got = file_sha256(fp).lower()
        if got != expected:
            r["notes"] = (r.get("notes", "") + f"; T204_hash_mismatch manifest={expected[:12]}")[:240]
            continue
        r["pdf_status"] = "ingested"
        r["pdf_artifact"] = art
        r["last_fetch_utc"] = now
        r["notes"] = (r.get("notes", "") + "; T204_sha256_verified")[:240]
        n_ok += 1

    with RS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})

    print("verified_pdf_ingested", n_ok)
    return 0 if n_ok >= args.limit else 1


if __name__ == "__main__":
    raise SystemExit(main())
