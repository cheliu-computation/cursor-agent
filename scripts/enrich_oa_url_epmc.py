#!/usr/bin/env python3
"""T206: set oa_url_cached to PMC landing page when Europe PMC finds OA DOI match."""
from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from fetch_policy import api_headers

ROOT = Path(__file__).resolve().parents[1]
PM = ROOT / "research_ops/02_papers/papers_master.csv"
RS = ROOT / "research_ops/02_papers/paper_reading_status.csv"


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers=api_headers())
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=300)
    ap.add_argument("--sleep", type=float, default=0.2)
    args = ap.parse_args()

    doi_by_oid: dict[str, str] = {}
    with PM.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            oid = (r.get("openalex_id") or "").strip()
            doi = (r.get("doi") or "").strip()
            if oid and doi:
                doi_by_oid[oid] = doi

    with RS.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        fieldnames = rdr.fieldnames
        rows = list(rdr)

    # Prefer DOI prefixes that commonly resolve in Europe PMC (journals > LNCS books).
    PREFIX_RANK = (
        "10.1038/",
        "10.1016/",
        "10.1126/",
        "10.1056/",
        "10.1001/",
        "10.1002/",
        "10.1093/",
        "10.3389/",
        "10.1186/",
        "10.1371/",
        "10.2196/",
        "10.1101/",
    )

    def doi_rank(d: str) -> tuple[int, str]:
        dl = d.lower()
        for i, p in enumerate(PREFIX_RANK):
            if dl.startswith(p):
                return (i, dl)
        return (len(PREFIX_RANK), dl)

    candidates = []
    for r in rows:
        if (r.get("oa_url_cached") or "").strip().lower().startswith("http"):
            continue
        oid = (r.get("openalex_id") or "").strip()
        doi = doi_by_oid.get(oid, "").strip()
        if doi:
            candidates.append((doi_rank(doi), r))
    candidates.sort(key=lambda x: x[0])

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    n_api = n_filled = 0
    for _, r in candidates:
        if n_api >= args.limit:
            break
        oid = (r.get("openalex_id") or "").strip()
        doi = doi_by_oid.get(oid, "").strip()
        if not doi:
            continue
        q = "DOI:" + doi
        url = (
            "https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
            + urllib.parse.urlencode({"query": q, "format": "json", "pageSize": "2"})
        )
        try:
            data = fetch_json(url)
        except Exception as e:
            r["notes"] = (r.get("notes", "") + f"; T206_epmc_err={e}")[:220]
            n_api += 1
            time.sleep(args.sleep)
            continue
        n_api += 1
        results = (data.get("resultList") or {}).get("result") or []
        hit = None
        for h in results:
            pmcid = (h.get("pmcid") or "").strip()
            in_epmc = (h.get("inEPMC") or "").upper() == "Y"
            if pmcid and in_epmc:
                hit = h
                break
        if hit:
            pmcid = hit["pmcid"].strip()
            landing = f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/"
            r["oa_url_cached"] = landing[:300]
            r["last_fetch_utc"] = now
            oa = (hit.get("isOpenAccess") or "").upper()
            tag = "T206_epmc_pmc_url_oa" if oa == "Y" else "T206_epmc_pmc_url_inEPMC"
            r["notes"] = (r.get("notes", "") + f"; {tag}")[:220]
            n_filled += 1
        time.sleep(args.sleep)

    with RS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})

    print("epmc_lookups", n_api, "oa_url_filled", n_filled)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
