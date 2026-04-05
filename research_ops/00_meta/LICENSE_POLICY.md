# LICENSE_POLICY

副标题：下载、保留、删除、许可与 git 策略

## Principles
- Only bulk-download and retain content **compatible with the source terms** (API ToS, CC licenses, OA subsets).
- **Default**: structured extractions and manifests are retained; **raw bulk files are not** committed to git.
- Every downloaded artifact must have **source URL, retrieval time, license note, hash**, and **redownloadable** flag in `download_manifest.csv`.

## What is stored today
- Full text is **not** stored as a centralized database of article bodies.
- Current storage model is:
  - **raw bytes** under `research_ops/cache/` (gitignored, disposable after parse/policy checks)
  - **parsed text / JSONL / indices** under `research_ops/parsed/` where applicable
  - **structured registries / manifests / status tables** under git
- In other words, the durable layer is mainly **manifests + parsed outputs + CSV state**, not a permanent full-body corpus in git.

## Content-type acquisition (summary)
| Content type | Typical priority | Git default | After successful parse |
|--------------|------------------|-------------|---------------------------|
| Metadata JSON/XML | High | Track derived CSV rows only | Raw may delete if redownloadable |
| Abstract HTML | High | Do not commit raw | Delete eligible |
| OA XML/HTML full text | High | Do not commit raw | Delete eligible after extraction |
| Non-OA PDF | Use only when licensed/permitted | Never commit by default | Delete after extraction or do not download |
| Supplementary archives | Medium | Do not commit | Extract structured tables; delete archive if allowed |

## Retention classes
- **Long retain**: CSV/JSONL outputs, manifests, parsed structured extracts, memos, cards.
- **Short retain (cache)**: raw PDF/HTML/TXT/XML under `cache/` until parse + manifest complete.
- **Keep-set (curated)**: rare exceptions listed in `manifests/keep_set_manifest.csv` with rationale.

## Parser output survival
After raw deletion, **must still exist**: extraction outputs path, parse_manifest row, checksum/hash, provenance note, parse status, and pointers to structured fields in master tables.

## Gitignore
- `research_ops/cache/**` is ignored except `.gitkeep` markers.
- Do not add large binaries under `parsed/` without explicit keep-set decision.

## Storage budget and cleanup triggers (operational)
Per-worktree soft limits for `research_ops/cache/` (tune per runner):
- **Warning**: total cache > **2 GiB** → pause new bulk downloads; run cleanup on `cache/tmp` and failed partials first.
- **Hard stop**: total cache > **8 GiB** → block new downloads except manual override logged in `RUN_LOG.md`.
- **Priority order for eviction**: `cache/tmp` → duplicate re-downloads (same hash) → `cache/fulltext` with `delete_eligibility=eligible` → `cache/pdfs` with eligible flag → never delete without manifest row.
- **Per-subfolder hints**: `cache/pdfs` should stay smallest; spill to external volume or delete post-parse before `cache/fulltext`.

## Redownloadable
- If `redownloadable=true` and structured outputs are persisted, **delete_eligibility** may be `eligible` after successful parse.
- If not redownloadable, prefer retaining raw in cache until a human decision is recorded in `keep_set_manifest.csv`.

## Raw-file deletion checkpoints (gates)
Raw bytes under `cache/` may be removed only when **all** applicable checks pass:
1. **Manifest**: `download_manifest.csv` row complete for URL, retrieval time, local path, hash, mime type, license note, `redownloadable`.
2. **Parse record**: `parse_manifest.csv` records final `parse_status` and output paths (or documented waiver for metadata-only artifacts).
3. **Structured survival**: extracted rows or files referenced from master tables or `parsed/` exist and are referenced from the parse manifest.
4. **Provenance**: a short `provenance_note` (or note file path) explains source and transformation.
5. **Policy**: `delete_eligibility` set to `eligible`; if `redownloadable=false`, require `keep_set_manifest` decision or retain raw.

Partial parses: default **do not delete** until retry queue resolves or a human marks acceptable loss scope in notes.
