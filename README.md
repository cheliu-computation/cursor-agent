# cursor-agent

Research operations live under **`research_ops/`**. Automation lives under
**`scripts/`** — see **`scripts/README.md`** for a grouped index.

## Repository layout

- `research_ops/02_papers/`
  - `papers_master.csv`: canonical paper metadata including title and venue.
  - `paper_reading_status.csv`: abstract/fulltext fetch status by paper.
- `research_ops/00_meta/`
  - `SOURCE_POLICY.md`: source-tier and fetch-policy rules.
  - `LICENSE_POLICY.md`: retention and cache cleanup policy.
  - `fulltext_read_pipeline.md`: title/abstract/fulltext processing notes.
  - `2026-04-04_source_success_report.md`: per-source success-rate report.
  - `2026-04-04_5.4_fix_record.md`: cleanup and 5.4 fix record.
- `research_ops/manifests/`
  - `download_manifest.csv`: provenance for downloaded artifacts.
- `scripts/`
  - harvesting, enrichment, policy, cleanup, and reporting utilities.

Bulk downloads and large binaries are **gitignored**; provenance stays in
`research_ops/manifests/download_manifest.csv`.

## Storage model

- Structured research state lives in CSV / Markdown / manifest files under
  `research_ops/`.
- Raw full text is **not** stored in a database table in this repository.
- Downloaded HTML / XML / PDF bytes are cached under `research_ops/cache/`
  (gitignored).
- Extracted text and derived artifacts live under `research_ops/parsed/`
  (mostly gitignored for bulky outputs).
- The durable, tracked layer is therefore:
  - metadata tables
  - reading status tables
  - manifests / provenance
  - current reports
