# MICCAI official bibliography ingestion (T122)

## Goal
Replace or supplement OpenAlex LNCS-volume hits with **curator-grade** paper lists from MICCAI organizers when terms allow.

## Suggested primary sources (verify license each year)
- Conference site: https://www.miccai.org/ — proceedings / accepted papers pages.
- Springer LNCS volume pages linked from MICCAI (DOI prefixes `10.1007/`).

## Ingestion steps
1. Download or scrape **accepted paper metadata** (title, authors, DOI) only; avoid bulk PDF unless OA.
2. Append rows to `download_manifest.csv` if raw HTML/JSON is cached under `research_ops/cache/metadata/`.
3. Merge into `papers_master.csv` with `source_batch=miccai_YYYY_official` and dedupe on DOI / OpenAlex ID.
4. Record the **exact landing URL** and retrieval date in `RUN_LOG.md`.

## Status
- **2026-03-31**: Placeholder note only; automated LNCS volume filter applied in T120; per-paper official list still pending human/API confirmation.
