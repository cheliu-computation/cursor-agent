# SK001 — OpenAlex venue-scoped harvest

- **Inputs**: `source_id`, year range, keyword list, target `papers_master` columns  
- **Outputs**: Appended `papers_master.csv` rows; `source_batch` tag  
- **Scope**: Metadata only; no paywalled PDF  
- **Failure modes**: API rate limits; empty `meta.count`; duplicate `openalex_id`  
- **Validation**: PT-OPENALEX-001  
- **Provenance**: `SOURCE_POLICY.md`, polite pooling
