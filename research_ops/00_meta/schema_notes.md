# Core CSV schema notes

Short column semantics for high-churn registries. See header row as source of truth.

## `harvest_window` (T174)
Rolling-ingest provenance bucket, **not** necessarily calendar month:
- `YYYY-MM` — from `T182_month_*` script batches
- `YYYY_venue_rolling` / `YYYY_preprint_rolling` / `YYYY_topic_search` — inferred from `source_batch` pattern
- `YYYY_legacy_or_mixed` — early seeds where only `year` is reliable
- `unknown` — missing signals

## `papers_master.csv`
- **paper_id**: Stable internal ID (e.g. `openalex:W123`, `doi:10.x/...`, or generated UUID).
- **harvest_window**: Rolling slice label for audits (see § `harvest_window` above).
- **source_batch**: Provenance batch label (which harvest run or query).
- **tags_***: Pipe- or comma-separated controlled vocabulary (normalize in T047–T048).
- **topic_subtag**: For `preprint_*` rows (T175), pipe-separated coarse buckets from title keywords: `imaging` | `clinical` | `genomics` | `other_preprint`.

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

## `tags_modality` controlled values (T047)
Pipe-separated facets, primary bucket first:

- `medical_imaging` — MICCAI/MIDL/IPMI/ISBI/MedIA/TMI style imaging ML
- `clinical_imaging` — Radiology / Radiology AI harvests
- `machine_learning` — NeurIPS/ICML/ICLR venue-scoped harvests
- `computer_vision` — CVPR/ICCV/ECCV medical-oriented rows
- `biomedical_science` — Nature/Science/Cell AI×bio crossovers
- `clinical_translational` — Nat Med, NBE, npj DM, Comm Med
- `clinical_high_impact` — JAMA, NEJM, Lancet Digital Health family
- `clinical_ai` — agent/clinical simulator papers (T111 backfill heuristic)
- `unspecified` — legacy or unknown provenance
- `preprint_broad` — arXiv / repository slice via OpenAlex `primary_location.source.id:S4306400194` (T172; title-keyword recall)
- `preprint_biorxiv` — bioRxiv via `S4306402567` (T176)
- `preprint_medrxiv` — medRxiv via `S4306400573` (T176)

Optional secondary facets: `radiology`, `pathology` (inferred from venue string).

## `tags_method` buckets (T048)
Pipe-separated, alphabetically sorted:

`agents`, `computer_vision`, `computational_biomedicine`, `deep_learning`, `foundation_models`, `federated_privacy`, `generative`, `representation_learning`, `segmentation`, `self_supervised`, `transformers`, `unspecified`

Heuristic: title keywords + venue batch (ML conferences vs vision vs clinical journals).

## `19_linking/trials_master.csv` (T043)
Trial snapshot rows from ClinicalTrials.gov API v2: `trial_id` / `nct_id`, `brief_title`, `overall_status`, pipe-friendly `conditions`, `study_type`, canonical `url`.

## `19_linking/paper_challenge_links.csv` (T049)
Links Grand Challenge `challenge_id` (e.g. `gc:VESSEL12`) to `paper_id` (OpenAlex spine) via DOI resolution; **merge into `papers_master`** when missing (see T138).

## `06_repro/audit_priority_list.csv` (T050)
Ranked queue for deeper repro audit; scores are heuristic (venue + source_batch + recency), not citation counts.

## `06_repro/repo_registry.csv` (T051)
`paper_id` → GitHub repo URL; URLs parsed from OpenAlex `abstract_inverted_index` when present (validate against official project pages).

## `06_repro/issue_mining.csv` (T052)
Public GitHub Issues API results (title keyword gate); unauthenticated rate limits apply.

## `06_repro/repro_audit.csv` (T053)
Heuristic triage for audit queue; **not** a reproduction result until `repro_status` is updated after a run.

## Case lake CSVs (T115 mapping)
- `case_reports_master.presentation_summary`: Europe PMC `abstractText` snippet (not full case narrative until full-text).
- `phenopackets.*`: Minimal regex-derived demographics only; HPO/phenotypes require NLP or manual curation.
- `case_report_figures`: Placeholder rows until figure captions are parsed from XML/HTML full text.
