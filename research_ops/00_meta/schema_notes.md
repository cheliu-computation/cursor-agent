# Core CSV schema notes

Short column semantics for high-churn registries. See header row as source of truth.

## `papers_master.csv`
- **paper_id**: Stable internal ID (e.g. `openalex:W123`, `doi:10.x/...`, or generated UUID).
- **source_batch**: Provenance batch label (which harvest run or query).
- **tags_***: Pipe- or comma-separated controlled vocabulary (normalize in T047–T048).

## `source_registry.csv`
- **layer**: A–H per `SOURCE_POLICY.md` (domain, method, clinical, data, repro, frontier, infra, case).
- **bulkability** / **parseability**: Qualitative (`high|medium|low` or `json_high` style) for agent planning.
- **redownloadable_default**: `true` / `false` / `varies` — drives `delete_eligibility` after parse.

## `download_manifest.csv`
- **delete_eligibility**: `pending` | `eligible` | `retain` | `blocked`.
- **redownloadable**: Whether bytes can be refetched from the same URL/API under policy.
- **provenance_note**: Human- or agent-readable chain from URL → parse → master row.

## `parse_manifest.csv`
- **raw_retained**: `yes` | `no` | `partial` after cleanup decision.

## `paper_trial_links.csv`
- **relation_type**: `registers` | `reports_results` | `mentions` | `protocol_only` | `unknown`.
- **nct_id**: Normalized `NCTxxxxxxxx` when available alongside internal `trial_id`.

## `paper_guideline_links.csv`
- **guideline_id**: Internal stable ID; pair with **organization** + **version_year** for human disambiguation.
- **relation_type**: `cites` | `implements` | `compares_to` | `derived_from` | `unknown`.
