#!/usr/bin/env python3
"""T203: batch fetch OA landing pages (HTML preferred), with arXiv fallbacks."""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RS = ROOT / "research_ops/02_papers/paper_reading_status.csv"
PM = ROOT / "research_ops/02_papers/papers_master.csv"
MNF = ROOT / "research_ops/manifests/download_manifest.csv"
CACHE_FT = ROOT / "research_ops/cache/fulltext"
CACHE_PDF = ROOT / "research_ops/cache/pdfs"

UA = "Mozilla/5.0 (compatible; research-ops-bot/1.0; +https://example.invalid)"


def manifest_next_id(rows: list[dict]) -> int:
    last = 0
    for r in rows:
        mid = r.get("manifest_id", "")
        m = re.match(r"DL(\d+)", mid or "")
        if m:
            last = max(last, int(m.group(1)))
    return last


def arxiv_id_from_url(url: str) -> str | None:
    u = url.split("?", 1)[0].strip()
    m = re.search(r"arxiv\.org/(?:pdf|abs)/([^/]+?)(?:\.pdf)?$", u, re.I)
    if m:
        return m.group(1).rstrip("/")
    m = re.search(r"doi\.org/10\.48550/arxiv\.(.+)$", u, re.I)
    if m:
        return m.group(1).rstrip("/")
    return None


def url_attempts(primary: str) -> list[str]:
    """Ordered list of URLs to try (primary first, then fallbacks)."""
    primary = primary.strip()
    seen: set[str] = set()
    out: list[str] = []
    for u in _expand_arxiv(primary):
        if u and u not in seen:
            seen.add(u)
            out.append(u)
    return out


def _expand_arxiv(url: str) -> list[str]:
    aid = arxiv_id_from_url(url)
    if not aid:
        return [url]
    ulow = url.lower()
    alts = [url]
    if "arxiv.org/pdf/" in ulow or "export.arxiv.org" in ulow:
        alts.append(f"https://arxiv.org/abs/{aid}")
        alts.append(f"https://export.arxiv.org/pdf/{aid}.pdf")
    elif "arxiv.org/abs/" in ulow:
        alts.append(f"https://export.arxiv.org/pdf/{aid}.pdf")
    return alts


def fetch_url(url: str, timeout: int = 60) -> tuple[bytes, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        ctype = resp.headers.get("Content-Type", "")
    return data, ctype


def load_pm_year() -> dict[str, str]:
    by_id: dict[str, str] = {}
    with PM.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            oid = (r.get("openalex_id") or "").strip()
            if not oid:
                continue
            wid = oid if oid.startswith("W") else "W" + oid
            by_id[wid] = (r.get("year") or "").strip()
    return by_id


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--years",
        default="2026,2025,2024,2023,2022,2021,2020,2019,2018,2017,2016,2015",
        help="Comma-separated publication years (newest first within list)",
    )
    ap.add_argument("--limit", type=int, default=500, help="Max new successful fetches")
    ap.add_argument("--sleep", type=float, default=0.12, help="Seconds after each attempt")
    ap.add_argument(
        "--retry-errors",
        action="store_true",
        help="Also retry rows with fulltext_html_status=error",
    )
    ap.add_argument(
        "--skip-pdf-primary",
        action="store_true",
        help="Skip rows whose oa_url_cached is clearly a PDF link (boost HTML ingested count)",
    )
    args = ap.parse_args()
    year_order = [y.strip() for y in args.years.split(",") if y.strip()]
    year_rank = {y: i for i, y in enumerate(year_order)}

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    CACHE_FT.mkdir(parents=True, exist_ok=True)
    CACHE_PDF.mkdir(parents=True, exist_ok=True)

    with MNF.open(newline="", encoding="utf-8") as f:
        rdr_m = csv.DictReader(f)
        mf = rdr_m.fieldnames
        rows_m = list(rdr_m)
    last_id = manifest_next_id(rows_m)

    with RS.open(newline="", encoding="utf-8") as f:
        rdr_s = csv.DictReader(f)
        sf = rdr_s.fieldnames
        status_rows = list(rdr_s)

    pm_year = load_pm_year()
    by_oid: dict[str, dict] = {r["openalex_id"].strip(): r for r in status_rows}

    allowed_status = {"", "pending"}
    if args.retry_errors:
        allowed_status = {"", "pending", "error"}

    pool: list[tuple[int, str, str, dict]] = []
    for r in status_rows:
        if r.get("abstract_status") != "ingested":
            continue
        url = (r.get("oa_url_cached") or "").strip()
        if not url.lower().startswith("http"):
            continue
        if args.skip_pdf_primary and url.lower().split("?", 1)[0].endswith(".pdf"):
            continue
        st = (r.get("fulltext_html_status") or "").strip()
        if st not in allowed_status:
            continue
        oid = r["openalex_id"].strip()
        wid = oid if oid.startswith("W") else "W" + oid
        y = pm_year.get(wid, "")
        rank = year_rank.get(y, 999)
        pool.append((rank, wid, url, r))

    pool.sort(key=lambda x: (x[0], x[1]))

    new_manifest: list[dict] = []
    n_ok = 0
    for rank, wid, url, rec in pool:
        if n_ok >= args.limit:
            break
        oid_key = rec["openalex_id"].strip()
        cur = by_oid.get(oid_key, rec)
        if (cur.get("fulltext_html_status") or "").strip() not in allowed_status:
            continue

        data: bytes | None = None
        ctype_hdr = ""
        used_url = ""
        last_err: str | None = None
        for attempt in url_attempts(url):
            try:
                data, ctype_hdr = fetch_url(attempt)
                used_url = attempt
                break
            except Exception as e:
                last_err = str(e)[:180]
                time.sleep(args.sleep)
        time.sleep(args.sleep)

        if data is None:
            cur["fulltext_html_status"] = "error"
            cur["fulltext_html_artifact"] = ""
            cur["notes"] = (cur.get("notes", "") + f"; batch_fetch_error={last_err}")[:240]
            cur["last_fetch_utc"] = now
            by_oid[oid_key] = cur
            continue

        is_pdf = (
            "pdf" in ctype_hdr.lower()
            or used_url.lower().split("?", 1)[0].endswith(".pdf")
        )
        short = wid.replace(":", "_")
        if is_pdf:
            local = CACHE_PDF / f"T203_{short}.pdf"
            mime = ctype_hdr.split(";")[0].strip()[:80] or "application/pdf"
            parse_path = "research_ops/cache/pdfs/"
            status_ft = "pdf_cached"
        else:
            local = CACHE_FT / f"T203_{short}.html"
            mime = ctype_hdr.split(";")[0].strip()[:80] or "text/html"
            parse_path = "research_ops/cache/fulltext/"
            status_ft = "ingested"

        local.write_bytes(data)
        h = hashlib.sha256(data).hexdigest()
        last_id += 1
        mid = f"DL{last_id:05d}"
        new_manifest.append({
            "manifest_id": mid,
            "source_url": used_url[:900],
            "retrieval_time_utc": now,
            "local_path": str(local.relative_to(ROOT)),
            "file_hash": h,
            "mime_type": mime,
            "license_note": "OpenAlex oa_url; verify at source",
            "parse_status": "raw_cached",
            "parse_output_path": parse_path,
            "delete_eligibility": "eligible",
            "redownloadable": "true",
            "provenance_note": f"paper_reading_status openalex_id={wid}",
            "notes": "T203 batch OA fetch",
        })
        cur = by_oid.get(oid_key, rec)
        cur["fulltext_html_status"] = status_ft
        cur["fulltext_html_artifact"] = str(local.relative_to(ROOT))
        cur["last_fetch_utc"] = now
        note = "; T203_fetched"
        if used_url != url:
            note += f"; url_fallback={used_url[:80]}"
        cur["notes"] = (cur.get("notes", "") + note)[:240]
        by_oid[oid_key] = cur
        n_ok += 1

    rows_m.extend(new_manifest)
    with MNF.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=mf)
        w.writeheader()
        w.writerows(rows_m)

    with RS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=sf)
        w.writeheader()
        for r in sorted(by_oid.values(), key=lambda x: x["openalex_id"]):
            w.writerow({k: r.get(k, "") for k in sf})

    print("new_fetches", n_ok, "manifest_rows", len(rows_m))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
