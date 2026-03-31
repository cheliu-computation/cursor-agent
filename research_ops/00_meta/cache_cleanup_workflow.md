# Cache cleanup workflow

副标题：download → parse → extract → manifest → delete

## Stages
1. **Download**: Write target path under `cache/metadata`, `cache/fulltext`, `cache/pdfs`, or `cache/tmp` per acquisition plan.
2. **Register**: Append `download_manifest.csv` with source URL, retrieval time (UTC), local path, mime type, license note, `redownloadable`, `delete_eligibility` (initially `pending`).
3. **Hash**: Compute file hash; update manifest row.
4. **Parse**: Run appropriate parser; append `parse_manifest.csv` with `parse_status`, `structured_output_path`, errors if any.
5. **Extract**: Persist structured fields to the relevant master CSV or JSONL under `parsed/` or domain folders.
6. **Gate** (all must pass before raw delete): parse success or documented partial success policy, hash recorded, outputs path recorded, provenance note present.
7. **Delete** (optional): Set `delete_eligibility=eligible` only when `redownloadable=true` or keep-set exception applies; remove raw bytes from `cache/`.
8. **Audit**: If deletion occurs, retain manifest rows permanently.

## Failure paths
- Download failure → `retry_queue.csv` with failure type `download`.
- Parse failure → `retry_queue.csv` with failure type `parse`; raw may remain until resolved or policy timeout.
