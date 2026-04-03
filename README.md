# cursor-agent

Research operations live under **`research_ops/`** (CSVs, manifests, meta docs). Automation lives under **`scripts/`** — see **`scripts/README.md`** for a grouped index.

- **Task backlog**: `research_ops/00_meta/TODO.md` (mirrored at `SCALABLE_DISCOVERY_AGENT_TODO.md`)
- **Current focus**: `research_ops/00_meta/STATUS.md`
- **Run history**: `research_ops/00_meta/RUN_LOG.md`
- **Pipelines**: `research_ops/00_meta/fulltext_read_pipeline.md`, `LICENSE_POLICY.md` (under `research_ops/00_meta/`)

Bulk downloads and large binaries are **gitignored**; provenance stays in `research_ops/manifests/download_manifest.csv`.

## Storage model

- Structured research state lives in CSV / Markdown / manifest files under `research_ops/`.
- Raw full text is **not** stored in a database table in this repository.
- Downloaded HTML / XML / PDF bytes are cached under `research_ops/cache/` (gitignored).
- Extracted text and derived artifacts live under `research_ops/parsed/` (also mostly gitignored for bulky outputs).
- The durable, tracked layer is therefore:
  - metadata tables
  - reading status tables
  - manifests / provenance
  - summary notes / reports
