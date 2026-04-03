# DECISIONS

副标题：架构与策略决策记录

## D-001 — Repository layout
- **Decision**: Use `research_ops/` as the single root for all structured research assets; raw downloads go under `research_ops/cache/` with manifests under `research_ops/manifests/`.
- **Rationale**: Keeps git-tracked artifacts separate from disposable cache; matches `SCALABLE_DISCOVERY_AGENT.md`.
- **Date**: 2026-03-31

## D-002 — Manifest-before-delete
- **Decision**: No deletion of raw cached files until a row exists in `download_manifest.csv` with hash, URL, retrieval time, and parse status recorded.
- **Rationale**: Provenance and redownloadability require auditable trails.

## D-003 — CSV as primary interchange
- **Decision**: Registries and masters are CSV with documented headers; heavy analytics may later add Parquet/DuckDB without replacing manifest CSVs.
- **Rationale**: Human-diffable, agent-friendly, low tooling friction.

## D-004 — Frontier → transfer promotion heuristics
- **Rule 1**: If a `frontier_papers` row tags **tool_use=yes** and abstract/title mentions **benchmark or dataset**, enqueue `transfer_candidates` with target_domain `medical_imaging` after one human or script spot-check.
- **Rule 2**: If title contains **multi-agent** + **(clinical OR biomedical OR EHR)**, link to `pain_points` PP-family (workflow / inbox) in `trend_to_problem_links` when a matching pain_id exists.
- **Rule 3**: If **self_evolve=yes** but no **promotion_tests** or public code, mark as **hype-risk** in `anti_hype_checks` before any transfer promotion.
- **Date**: 2026-03-31

## D-005 — `paper_trial_links.relation_type` vocabulary
Use one primary label per row (add detail in `relation_subtype` / `notes`).

| Value | Meaning | Example |
|-------|---------|---------|
| `registers` | Paper is a trial **registration** or protocol-only publication for the trial | Protocol paper with NCT in structured field |
| `reports_results` | Paper **reports outcomes** of the registered trial (primary or secondary results) | NEJM results article ↔ NCT |
| `cited_in_protocol_text` | Trial record **embeds the DOI/PMID** in text (background, rationale, references) | T119 pilot links from CT.gov JSON |
| `mentions` | Free-text mention without clear bibliographic ID | Legacy / low confidence |
| `protocol_only` | Link is to trial **documentation** on CT.gov only (no paper ID yet) | Placeholder rows |
| `unknown` | Insufficient evidence to classify | Default when ambiguous |

**Confidence**: pair `cited_in_protocol_text` with `confidence=low|medium` unless independently verified in PubMed/ publisher site.
- **Date**: 2026-03-31

## D-006 — `fulltext_html_status=pdf_cached` for Layer B
- **Decision**: When the OA URL is nominally an HTML landing page but the HTTP response is **PDF** (`Content-Type` or `.pdf` URL), set `fulltext_html_status=pdf_cached`, store bytes under `cache/pdfs/` with prefix **`T203_`**, and record the row in `download_manifest.csv` with accurate `mime_type`.
- **Rationale**: Avoid mislabeling binary PDF as HTML; keeps Layer B “fetched fulltext bytes” auditable while **T204** can later normalize `pdf_status` for explicit PDF-layer tracking.
- **Date**: 2026-04-01
