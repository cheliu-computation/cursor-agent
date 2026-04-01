#!/usr/bin/env python3
"""T211: pilot Europe PMC fullTextXML for case_reports_master PMIDs."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "research_ops/16_case_reports/case_reports_master.csv"
MNF = ROOT / "research_ops/manifests/download_manifest.csv"
REG = ROOT / "research_ops/16_case_reports/case_reading_status.csv"
CACHE = ROOT / "research_ops/cache/fulltext"
UA = "Mozilla/5.0 (compatible; research-ops-bot/1.0; +https://example.invalid)"


def manifest_next_id(rows: list[dict]) -> int:
    last = 0
    for r in rows:
        m = re.match(r"DL(\d+)", r.get("manifest_id", "") or "")
        if m:
            last = max(last, int(m.group(1)))
    return last


def extract_pmid(s: str) -> str:
    m = re.search(r"PMID:\s*(\d+)", s, re.I)
    return m.group(1) if m else ""


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--sleep", type=float, default=0.2)
    args = ap.parse_args()

    CACHE.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    case_rows = list(csv.DictReader(CASES.open(newline="", encoding="utf-8")))

    with MNF.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        mf = rdr.fieldnames
        rows_m = list(rdr)
    last_id = manifest_next_id(rows_m)

    reg_fieldnames = [
        "case_id", "pmid", "pmcid", "source_url", "local_path",
        "file_hash", "retrieval_time_utc", "fulltext_status", "notes",
    ]
    reg_rows: list[dict] = []
    if REG.exists():
        reg_rows = list(csv.DictReader(REG.open(newline="", encoding="utf-8")))
    done_pmids = {r.get("pmid", "").strip() for r in reg_rows if r.get("fulltext_status") == "ingested"}

    new_manifest: list[dict] = []
    new_reg: list[dict] = []
    n_ok = 0

    for cr in case_rows:
        if n_ok >= args.limit:
            break
        pmid = extract_pmid(cr.get("pmid_or_doi", "") or "")
        if not pmid or pmid in done_pmids:
            continue
        q = f"EXT_ID:{pmid}"
        url = (
            "https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
            + urllib.parse.urlencode({"query": q, "format": "json", "pageSize": "3"})
        )
        try:
            data = fetch_json(url)
        except Exception:
            time.sleep(args.sleep)
            continue
        results = (data.get("resultList") or {}).get("result") or []
        hit = None
        for h in results:
            pmcid = (h.get("pmcid") or "").strip()
            if pmcid and (h.get("inEPMC") or "").upper() == "Y":
                hit = h
                break
        if not hit:
            time.sleep(args.sleep)
            continue
        pmcid = hit["pmcid"].strip()
        ft_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
        try:
            xml_bytes = fetch_bytes(ft_url)
        except Exception:
            time.sleep(args.sleep)
            continue

        cid = (cr.get("case_id") or f"pmid:{pmid}").strip()
        local = CACHE / f"T211_{pmcid}.xml"
        local.write_bytes(xml_bytes)
        h = hashlib.sha256(xml_bytes).hexdigest()
        last_id += 1
        mid = f"DL{last_id:05d}"
        new_manifest.append({
            "manifest_id": mid,
            "source_url": ft_url[:900],
            "retrieval_time_utc": now,
            "local_path": str(local.relative_to(ROOT)),
            "file_hash": h,
            "mime_type": "application/xml",
            "license_note": "Europe PMC case fullTextXML; verify OA at source",
            "parse_status": "raw_cached",
            "parse_output_path": "research_ops/cache/fulltext/",
            "delete_eligibility": "eligible",
            "redownloadable": "true",
            "provenance_note": f"case_reading_status case_id={cid} pmid={pmid}",
            "notes": "T211 case PMC fullTextXML pilot",
        })
        new_reg.append({
            "case_id": cid,
            "pmid": pmid,
            "pmcid": pmcid,
            "source_url": ft_url,
            "local_path": str(local.relative_to(ROOT)),
            "file_hash": h,
            "retrieval_time_utc": now,
            "fulltext_status": "ingested",
            "notes": "T211 pilot",
        })
        done_pmids.add(pmid)
        n_ok += 1
        time.sleep(args.sleep)

    rows_m.extend(new_manifest)
    with MNF.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=mf)
        w.writeheader()
        w.writerows(rows_m)

    reg_rows.extend(new_reg)
    REG.parent.mkdir(parents=True, exist_ok=True)
    with REG.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=reg_fieldnames)
        w.writeheader()
        w.writerows(reg_rows)

    print("fetched", n_ok, "registry_total", len(reg_rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
