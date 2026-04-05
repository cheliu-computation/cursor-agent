#!/usr/bin/env python3
"""T205: pilot fetch Europe PMC fullTextXML for papers with DOI (OA in EPMC)."""
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

from fetch_policy import api_headers

ROOT = Path(__file__).resolve().parents[1]
PM = ROOT / "research_ops/02_papers/papers_master.csv"
MNF = ROOT / "research_ops/manifests/download_manifest.csv"
REG = ROOT / "research_ops/02_papers/paper_epmc_fulltext_pilot.csv"
CACHE = ROOT / "research_ops/cache/fulltext"


def manifest_next_id(rows: list[dict]) -> int:
    last = 0
    for r in rows:
        m = re.match(r"DL(\d+)", r.get("manifest_id", "") or "")
        if m:
            last = max(last, int(m.group(1)))
    return last


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers=api_headers())
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers=api_headers())
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=35)
    ap.add_argument("--sleep", type=float, default=0.25)
    args = ap.parse_args()

    CACHE.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    doi_by_oid: dict[str, str] = {}
    with PM.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            oid = (r.get("openalex_id") or "").strip()
            doi = (r.get("doi") or "").strip()
            if oid and doi:
                doi_by_oid[oid] = doi

    with MNF.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        mf = rdr.fieldnames
        rows_m = list(rdr)
    last_id = manifest_next_id(rows_m)

    reg_rows: list[dict] = []
    if REG.exists():
        with REG.open(newline="", encoding="utf-8") as f:
            reg_rows = list(csv.DictReader(f))
    reg_fieldnames = [
        "openalex_id", "doi", "pmcid", "pmid", "source_url",
        "local_path", "file_hash", "retrieval_time_utc", "notes",
    ]
    done_doi = {r.get("doi", "").strip().lower() for r in reg_rows if r.get("doi")}

    PREFIX_RANK = (
        "10.1038/", "10.1016/", "10.1126/", "10.1056/", "10.1001/",
        "10.1002/", "10.1093/", "10.3389/", "10.1186/", "10.1371/",
        "10.2196/", "10.1101/",
    )

    def doi_rank(d: str) -> tuple[int, str]:
        dl = d.lower()
        for i, p in enumerate(PREFIX_RANK):
            if dl.startswith(p):
                return (i, dl)
        return (len(PREFIX_RANK), dl)

    new_manifest: list[dict] = []
    new_reg: list[dict] = []
    n_ok = 0

    for oid, doi in sorted(doi_by_oid.items(), key=lambda x: (doi_rank(x[1]), x[0])):
        if n_ok >= args.limit:
            break
        dk = doi.lower()
        if dk in done_doi:
            continue
        q = "DOI:" + doi
        search_url = (
            "https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
            + urllib.parse.urlencode({"query": q, "format": "json", "pageSize": "3"})
        )
        try:
            data = fetch_json(search_url)
        except Exception as e:
            time.sleep(args.sleep)
            continue
        results = (data.get("resultList") or {}).get("result") or []
        hit = None
        for h in results:
            if (h.get("inEPMC") or "").upper() == "Y" and (h.get("pmcid") or "").strip():
                hit = h
                break
        if not hit:
            time.sleep(args.sleep)
            continue
        pmcid = hit["pmcid"].strip()
        pmid = (hit.get("pmid") or "").strip()
        ft_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
        try:
            xml_bytes = fetch_bytes(ft_url)
        except Exception:
            time.sleep(args.sleep)
            continue

        local = CACHE / f"T205_{pmcid}.xml"
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
            "license_note": "Europe PMC fullTextXML; verify OA at source",
            "parse_status": "raw_cached",
            "parse_output_path": "research_ops/cache/fulltext/",
            "delete_eligibility": "eligible",
            "redownloadable": "true",
            "provenance_note": f"papers_master openalex_id={oid} doi={doi[:60]}",
            "notes": "T205 EPMC fullTextXML pilot",
        })
        new_reg.append({
            "openalex_id": oid,
            "doi": doi,
            "pmcid": pmcid,
            "pmid": pmid,
            "source_url": ft_url,
            "local_path": str(local.relative_to(ROOT)),
            "file_hash": h,
            "retrieval_time_utc": now,
            "notes": "T205 pilot",
        })
        done_doi.add(dk)
        n_ok += 1
        time.sleep(args.sleep)

    rows_m.extend(new_manifest)
    with MNF.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=mf)
        w.writeheader()
        w.writerows(rows_m)

    reg_rows.extend(new_reg)
    with REG.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=reg_fieldnames)
        w.writeheader()
        w.writerows(reg_rows)

    print("fetched_xml", n_ok, "registry_rows", len(reg_rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
