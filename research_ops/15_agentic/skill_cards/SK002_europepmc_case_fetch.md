# SK002 — Europe PMC OA case metadata fetch

- **Inputs**: CQL query string, `cursorMark`, page size  
- **Outputs**: `cache/metadata/epmc_case_pmid*.json`, `download_manifest.csv`, `case_reports_master.csv`  
- **Scope**: OA-flagged records; metadata JSON only unless full-text policy allows  
- **Failure modes**: Empty result; license ambiguity; cursor loop  
- **Validation**: PT-EPMC-001  
- **Provenance**: `LICENSE_POLICY.md`, `case_report_cache_lifecycle.md`
