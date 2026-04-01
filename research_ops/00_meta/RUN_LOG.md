# RUN_LOG

副标题：执行记录（新条目在顶部）

---

## 2026-04-01 — Full-text read stack: abstracts + T202 OA pilot

- **T200–T201**: Added `paper_reading_status.csv`, `fulltext_read_pipeline.md`, `scripts/ingest_openalex_abstracts.py`, `.gitignore` for `openalex_abstracts_*.jsonl`. Ingested OpenAlex `abstract_inverted_index` for **all 6401** `papers_master` rows (years 2026→1988 + backfill 80 late-added papers). JSONL files under `parsed/abstracts/` (not committed).
- **T202**: `scripts/pilot_fetch_oa_html.py` — prioritized HTML over PDF for 2025–2026 with `abstract_status=ingested` and `oa_url_cached`; **50** successful downloads; **68** new `download_manifest` rows total across two invocations; **73** rows marked `fulltext_html_status=error` (403/timeouts).
- **TODO**: New tasks **T200–T213** (HTML scale, PDF pilot, PMC, Unpaywall, FTS sqlite, monthly sync, audit link, GROBID, case fulltext, policy gate); **DOING=T203**.

## 2026-03-31 — T183 2018 window

- **T183**: 2018 — 10 journals ×40 + arXiv2018 `medical imaging deep learning` cap 80 → **+332** (total **6401**). New rows set `harvest_window=2018_*`; new arXiv rows get `topic_subtag` heuristics.
- **Next DOING**: **T184** (2017).

## 2026-03-31 — T181 / T174 / T182 / T175 + monthly smoke

- **T181**: 2019 window — journals ×45 + arXiv2019 cap 90 → **+492** (total **6064** before script).
- **T174**: Added **`harvest_window`** column; backfilled from `source_batch` patterns (`YYYY_venue_rolling`, `YYYY_preprint_rolling`, `YYYY_topic_search`, `YYYY_legacy_or_mixed`).
- **T182**: Added `scripts/harvest_openalex_monthly.py`; smoke test MedIA `S116571295` **2025-01** limit 5 → **+5** merged (total **6069**).
- **T175**: Added **`topic_subtag`** for `preprint_broad|preprint_biorxiv|preprint_medrxiv` rows via title regex buckets (**1452** rows tagged).
- **Next DOING**: **T183** (2018).

## 2026-03-31 — T179 / T180 preprint deepen + 2020 slice

- **T179**: bioRxiv `S4306402567` + medRxiv `S4306400573` — **2023** full sweep (single cell, genomics+ML, DL, ML, prediction, AI) plus **2024–2025** spatial + scRNA atlas queries → **+264** (total **5022**).
- **T180**: **2020** — 10 journals ×50 + arXiv 2020 `medical imaging deep learning` cap 100 → **+550** (total **5572**).
- **Next DOING**: **T181** (2019 window).

## 2026-03-31 — Rolling 2022 / 2021 + bioRxiv-medRxiv (T177 / T178 / T176)

- **T177**: 2022 — 10 journals ×65 + arXiv 2022 (`medical imaging deep learning`, `transformer medical`) → **+814** (total **3972**).
- **T176**: bioRxiv `S4306402567` + medRxiv `S4306400573`, 2024–2025, ML/DL/AI/prediction queries → **+126** (total **4098**).
- **T178**: 2021 — 10 journals ×55 + arXiv 2021 `medical imaging deep learning` cap 110 → **+660** (total **4758**).
- **Next DOING**: **T179** (deeper bioRxiv/medRxiv + 2023 + genomics/single-cell).

## 2026-03-31 — Rolling window 2023 (T173)

- **Scope**: Same 10 journals as T171, **70** works each for **publication_year:2023**; arXiv `S4306400194` for 2023 with searches `medical imaging deep learning` (130) and `large language model medicine` (100).
- **Counts**: `papers_master` rows **2242 → 3158** (Δ **+916**). File lines **3159** with header.
- **Next DOING**: **T177** (2022 window).

## 2026-03-31 — Rolling wide + recent ingest (T171 / T172)

- **Scope**
  - **T171**: For each of 10 sources (MedIA, TMI, Radiology, Radiology AI, Nat Med, npj Digital Medicine, Lancet Digital Health, Nature Machine Intelligence, Nature Computational Science, Cell Systems), fetch up to **60** works per **2024** and **2025** (`sort=publication_date:desc`, OpenAlex cursor pagination). Then seven global `search` queries (years 2023–2025, `sort=cited_by_count:desc`, ~45 hits each): LLM+clinical, FM+medical imaging, AI+radiology, generative+pathology, federated+healthcare, multimodal+biomedical, scientific discovery agent.
  - **T172**: arXiv repository source `S4306400194` with four search slices (limits 80–120) for 2024–2025; tag `preprint_broad`.
  - New rows include **authors** from `authorships` (up to 12 + “et al.”).
- **Counts**
  - Before → after `papers_master` data rows: **396 → 2242** (delta **+1846**; file lines **2243** incl. header).
  - Year histogram (data rows): 2026→80, 2025→715, 2024→805, 2023→52, 2022→31, 2021→87, older tail.
- **New follow-ups**: T174 `harvest_window` column, T175 subtag arXiv noise, T176 bioRxiv/medRxiv slices.
- **Verification**
  - `wc -l research_ops/02_papers/papers_master.csv` → 2243
  - `python -c` year Counter on `year` column (see above)

## 2026-03-31 — Mega harvest: papers spine + data lake + case lake + repro + hypothesis stack

- **Scope**
  - Domain / frontier / clinical journals → `papers_master.csv` (396 data rows after dedupe passes).
  - Data ecosystem: Grand Challenge (50), TCIA+PhysioNet `datasets_master` (70), CT.gov `trials_master` (30), `challenges_master` lifecycle column.
  - Linking: `paper_trial_links` (50 DOI-in-protocol), `paper_challenge_links` (19), `trend_to_problem_links` (8).
  - Repro: `audit_priority_list` (50), `repo_registry` (19 GitHub URLs from inverted abstracts), `issue_mining` (20), `repro_audit` (50).
  - Benchmark forensics: `benchmark_tables` (C-CAM numeric rows + Swin UNETR placeholder BT006), `split_audit`, `failure_modes`.
  - Task graveyard: `task_graveyard` (31), `resurrection_candidates` (15).
  - Case lake: Europe PMC OA cursor harvest **200** cases → `cache/metadata/epmc_case_pmid*.json` + matching `download_manifest` rows; `phenopackets` (200 minimal); `case_report_figures` (6 placeholders); RDRET seed + memos.
  - Agent harness: `skill_template.md`, SK001–SK010, `promotion_tests`, `benchmark_tasks`, `reflection_log`.
  - Hypothesis stack: `hypothesis_market`, `cheap_tests`, `evidence_gaps`, `idea_queue`, `reviewer_attacks`; P3 exploration memos under `13_exports/synthesis_memos/`.
  - Infra CSVs: `keep_set_manifest`, `retry_queue` templates; `query_registry` Q011–Q015; `case_report_cache_lifecycle.md` + cross-link in `cache_cleanup_workflow.md`.
  - TODO maintenance: closed T079–T104; added T141–T170 follow-up blocks; **DOING=T140** (Swin UNETR full benchmark table).
- **Verification commands**
  - `wc -l research_ops/02_papers/papers_master.csv` → 397
  - `wc -l research_ops/16_case_reports/case_reports_master.csv` → 201
  - `wc -l research_ops/manifests/download_manifest.csv` → 201
  - `wc -l research_ops/03_datasets/datasets_master.csv` → 71
  - `wc -l research_ops/19_linking/paper_trial_links.csv` → 51
- **Risks logged**
  - Heuristic labels (clinical_signal, RDRET, DDX seeds) need human or NLP upgrade (see T133, T151–T156).

## 2026-03-31 — Extended bootstrap + atlas + clinical pull + MICCAI seed

- **Scope**
  - Completed P0 setup through T006G, T095–T097, T107–T110.
  - Source atlas: T007–T013, T035–T036, T037–T038 (schema), T059–T061 (case schemas).
  - Frontier: T014–T016; agentic: T017–T018; T113 heuristics in `DECISIONS.md` D-004.
  - Clinical pull: T071–T075.
  - `papers_master.csv`: T019 seed (20 rows, OpenAlex search `"MICCAI medical imaging"` — **noisy**, follow T120–T122).
- **New follow-ups**
  - T111–T113 (earlier), T114–T116 (case lake), T117–T119 (linking), T120–T122 (MICCAI cleanup).
- **Verification commands**
  - `wc -l research_ops/01_sources/source_registry.csv` → 46
  - `wc -l research_ops/01_sources/venue_registry.csv` → 30
  - `wc -l research_ops/14_frontier/frontier_queries.csv` → 31
  - `wc -l research_ops/14_frontier/frontier_papers.csv` → 23
  - `wc -l research_ops/02_papers/papers_master.csv` → 21
  - Directory diff script: expected tree → `missing: []`

---

## 2026-03-31 — Bootstrap batch (agent)

- **Actions**
  - Created full `research_ops/` tree per `SCALABLE_DISCOVERY_AGENT.md` §6 including `cache/{metadata,fulltext,pdfs,tmp}`, `manifests/`, `parsed/`.
  - Added root `.gitignore` ignoring `research_ops/cache/**` except `.gitkeep`.
  - Initialized all core CSV files with headers (papers, datasets, challenges, benchmarks, repro, failures, tasks, clinical, transfer, ideas, reviewer, frontier, agentic, case reports, scaling, clinical_pull, linking, hypotheses, manifests).
  - Wrote `DECISIONS.md`, `SOURCE_POLICY.md`, `SCORING_POLICY.md`, `LICENSE_POLICY.md` (incl. content-type table, deletion checkpoints, retention).
  - Wrote `cache_cleanup_workflow.md`, `article_acquisition_decision_tree.md`, `gitignore_policy.md`.
  - Populated `source_registry.csv` with **45** sources across layers A–G.
- **Verification**
  - `wc -l research_ops/01_sources/source_registry.csv` → 46 lines (1 header + 45 data).
  - Spot-check: manifest CSVs include URL, retrieval time, local path, hash, mime, license, parse status, delete_eligibility, redownloadable, provenance.
- **TODO updates**
  - Moved T000–T006G, T006, T095–T097 → DONE; added follow-ups T107–T110; set DOING → T007.
- **Commits**: (pending) push to `cursor/agent-b783`.

---
