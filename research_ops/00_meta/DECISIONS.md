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
