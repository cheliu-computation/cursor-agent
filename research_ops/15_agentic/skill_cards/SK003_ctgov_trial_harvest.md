# SK003 — ClinicalTrials.gov v2 harvest

- **Inputs**: `query.term`, `pageSize`, optional `pageToken`  
- **Outputs**: `trials_master.csv` or JSONL batch; manifest optional  
- **Scope**: Public protocol JSON; US gov data terms  
- **Failure modes**: Empty studies; pagination gaps; schema drift  
- **Validation**: PT-CTGOV-001  
- **Provenance**: CT.gov API terms
