#!/usr/bin/env python3
"""T202: pilot download OA landing pages (HTML preferred)."""
from __future__ import annotations

import csv
import hashlib
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from fetch_policy import browser_headers, canonicalize_url, classify_policy_skip, url_attempts

ROOT = Path(__file__).resolve().parents[1]
RS = ROOT / "research_ops/02_papers/paper_reading_status.csv"
MNF = ROOT / "research_ops/manifests/download_manifest.csv"
CACHE_FT = ROOT / "research_ops/cache/fulltext"
CACHE_PDF = ROOT / "research_ops/cache/pdfs"


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    CACHE_FT.mkdir(parents=True, exist_ok=True)
    CACHE_PDF.mkdir(parents=True, exist_ok=True)

    with MNF.open(newline="", encoding="utf-8") as f:
        rdr_m = csv.DictReader(f)
        mf = rdr_m.fieldnames
        rows_m = list(rdr_m)
    last = 9200
    for r in rows_m:
        mid = r.get("manifest_id", "")
        m = re.match(r"DL(\d+)", mid)
        if m:
            last = max(last, int(m.group(1)))

    with RS.open(newline="", encoding="utf-8") as f:
        rdr_s = csv.DictReader(f)
        sf = rdr_s.fieldnames
        status_rows = list(rdr_s)

    # Load papers_master for year
    pm_year = {}
    with (ROOT / "research_ops/02_papers/papers_master.csv").open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            oid = (r.get("openalex_id") or "").strip()
            if oid.startswith("W"):
                key = oid
            else:
                key = "W" + oid
            pm_year[key] = r.get("year", "").strip()

    candidates = []
    for r in status_rows:
        if r.get("abstract_status") != "ingested":
            continue
        url = canonicalize_url((r.get("oa_url_cached") or "").strip())
        if not url.lower().startswith("http"):
            continue
        oid = r["openalex_id"].strip()
        wid = oid if oid.startswith("W") else "W" + oid
        y = pm_year.get(wid, "")
        if y not in ("2026", "2025"):
            continue
        if r.get("fulltext_html_status") not in ("", "pending"):
            continue
        is_pdf = url.lower().split("?", 1)[0].endswith(".pdf")
        candidates.append((not is_pdf, wid, url, r))  # prefer HTML first

    candidates.sort(key=lambda x: (not x[0], x[1]))
    target = 50

    by_oid = {r["openalex_id"].strip(): r for r in status_rows}

    new_manifest = []
    for prefer_html, wid, url, rec in candidates:
        if len(new_manifest) >= target:
            break
        oid_key = rec["openalex_id"].strip()
        # Skip if a previous run already cached this paper
        cur = by_oid.get(oid_key, rec)
        if cur.get("fulltext_html_status") not in ("", "pending"):
            continue
        policy_skip = classify_policy_skip(url)
        if policy_skip:
            cur["fulltext_html_status"] = "skipped_policy"
            cur["fulltext_html_artifact"] = ""
            cur["notes"] = (cur.get("notes", "") + f"; T202_policy_skip={policy_skip}")[:240]
            cur["last_fetch_utc"] = now
            by_oid[oid_key] = cur
            continue
        short = wid.replace(":", "_")
        is_pdf = url.lower().split("?", 1)[0].endswith(".pdf")
        if is_pdf:
            local = CACHE_PDF / f"T202_{short}.pdf"
            mime = "application/pdf"
            parse_path = "research_ops/cache/pdfs/"
        else:
            local = CACHE_FT / f"T202_{short}.html"
            mime = "text/html"
            parse_path = "research_ops/cache/fulltext/"

        data = None
        ctype = mime
        used_url = url
        last_err = ""
        for attempt in url_attempts(url):
            req = urllib.request.Request(attempt, headers=browser_headers())
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = resp.read()
                    ctype = resp.headers.get("Content-Type", mime)
                    used_url = attempt
                    break
            except urllib.error.HTTPError as e:
                last_err = f"HTTP Error {e.code}: {e.reason}"
                if e.code == 403:
                    skip = classify_policy_skip(attempt)
                    if skip:
                        policy_skip = skip
                        break
            except Exception as e:
                last_err = str(e)
        if policy_skip:
            rec = by_oid.get(oid_key, rec)
            rec["fulltext_html_status"] = "skipped_policy"
            rec["fulltext_html_artifact"] = ""
            rec["notes"] = (rec.get("notes", "") + f"; T202_policy_skip={policy_skip}")[:240]
            rec["last_fetch_utc"] = now
            by_oid[oid_key] = rec
            continue
        if data is None:
            rec = by_oid.get(oid_key, rec)
            rec["fulltext_html_status"] = "error"
            rec["fulltext_html_artifact"] = ""
            rec["notes"] = (rec.get("notes", "") + f"; fetch_error={last_err}")[:240]
            rec["last_fetch_utc"] = now
            by_oid[oid_key] = rec
            continue

        local.write_bytes(data)
        h = hashlib.sha256(data).hexdigest()
        last += 1
        mid = f"DL{last:05d}"
        new_manifest.append({
            "manifest_id": mid,
            "source_url": used_url[:900],
            "retrieval_time_utc": now,
            "local_path": str(local.relative_to(ROOT)),
            "file_hash": h,
            "mime_type": ctype.split(";")[0].strip()[:80],
            "license_note": "OpenAlex oa_url; verify at source",
            "parse_status": "raw_cached",
            "parse_output_path": parse_path,
            "delete_eligibility": "eligible",
            "redownloadable": "true",
            "provenance_note": f"paper_reading_status openalex_id={wid}",
            "notes": "T202 pilot OA fetch",
        })
        rec = by_oid.get(oid_key, rec)
        rec["fulltext_html_status"] = "ingested" if not is_pdf else "pdf_cached"
        rec["fulltext_html_artifact"] = str(local.relative_to(ROOT))
        rec["last_fetch_utc"] = now
        note = "; T202_fetched"
        if used_url != url:
            note += f"; url_fallback={used_url[:80]}"
        rec["notes"] = (rec.get("notes", "") + note)[:220]
        by_oid[oid_key] = rec

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

    print("fetched", len(new_manifest), "manifest now", len(rows_m))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
