# Case report cache lifecycle (T065)

Aligns with `research_ops/00_meta/cache_cleanup_workflow.md` and `LICENSE_POLICY.md`.

## Pipeline
1. **Query**: Europe PMC REST (or PMC OA) with explicit **open-access** filters; record query URL in `download_manifest.source_url`.
2. **Download**: Write response JSON to `research_ops/cache/metadata/epmc_case_pmid*.json` (gitignored bulk).
3. **Manifest**: Append `download_manifest.csv` with hash, mime, license note, `parse_status=metadata_only`.
4. **Extract**: Map core fields → `case_reports_master.csv`; optional HPO/phenotype pass → `phenopackets.csv`.
5. **Delete raw** (optional): If `redownloadable=true` and structured rows exist, set `delete_eligibility=eligible` and remove JSON from `cache/metadata/`.

## OA / compliance
- Prefer `isOpenAccess=Y` and verify `license` field per record before full-text expansion.
- Do not commit large PDFs; full text stays in cache until policy says otherwise.

## Cross-reference
- Global gates: `cache_cleanup_workflow.md` § Gate list.
