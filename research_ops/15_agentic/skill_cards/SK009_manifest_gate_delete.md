# SK009 — Manifest-gated cache delete

- **Inputs**: `download_manifest.csv` row id  
- **Outputs**: Deleted raw file; updated `delete_eligibility`  
- **Scope**: Only when gates in `LICENSE_POLICY.md` satisfied  
- **Failure modes**: Partial parse; missing hash  
- **Validation**: PT-MANIFEST-001  
- **Provenance**: `cache_cleanup_workflow.md`
