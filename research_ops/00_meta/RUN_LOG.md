# RUN_LOG

副标题：执行记录（新条目在顶部）

---

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
