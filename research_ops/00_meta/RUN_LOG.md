# RUN_LOG

副标题：执行记录（新条目在顶部）

---

## 2026-04-03 — Source triage round 2 (JAMA/NEJM keep, MDPI de-prioritize)

- Inspected remaining Layer-B `error` tail by host and sampled URLs/notes for:
  - `jamanetwork.com`
  - `www.nejm.org`
  - `academic.oup.com`
  - `doi.org`
  - `www.mdpi.com`
- Live probe from current environment:
  - JAMA landing/article path returns **403**
  - NEJM full/landing path returns **403**
- Updated source policy in code:
  - keep **JAMA / NEJM** as high-value clinical sources, but do **not** keep retrying direct page/PDF fetches from this environment
  - explicitly **de-prioritize MDPI** for gap/trend discovery; do not spend Layer-B repair budget there
- Re-ran `reclassify_layerb_policy_skips.py` after source-policy expansion:
  - **+59** additional rows moved from `error` to `skipped_policy`
  - current Layer-B status distribution:
    - `skipped_policy`: **2531**
    - `pending`: **1916**
    - `error`: **111**
    - `pdf_cached`: **1545**
    - `ingested`: **480**
- Remaining `error` rows now form a smaller residual tail, led by:
  - `doi.org` (**48**)
  - `escholarship.org` (**10**)
  - `academic.oup.com` (**8**)
  - repository mirrors / publisher long tail
- Operational conclusion:
  - for **JAMA / NEJM** class sources, prefer metadata / DOI routing / OA resolution (Crossref, OpenAlex, Unpaywall later), not direct HTML/PDF page fetches from this environment
  - for **MDPI**, stop treating Layer-B repair as worthwhile given lower value density for current objectives

## 2026-04-03 — Layer B policy repair + fetch strategy tightening

- Added shared fetch policy helper `scripts/fetch_policy.py`:
  - browser-like headers for publisher/OA landing fetches
  - API-oriented headers for OpenAlex / Europe PMC style JSON endpoints
  - source-specific URL canonicalization and landing-page fallback helpers
  - policy skip classification for known high-friction publisher/PDF routes
- Updated full-text / enrichment scripts to use the shared policy module:
  - `batch_fetch_oa_html.py`
  - `pilot_fetch_oa_html.py`
  - `ingest_openalex_abstracts.py`
  - `enrich_oa_url_openalex.py`
  - `enrich_oa_url_epmc.py`
  - `fetch_epmc_fulltext_pilot.py`
  - `t212_openalex_policy_gate.py`
- Added `scripts/reclassify_layerb_policy_skips.py` and reclassified historical Layer B terminal errors:
  - **949** rows moved from `fulltext_html_status=error` to `skipped_policy`
  - status distribution after repair:
    - `skipped_policy`: **2472**
    - `pending`: **1916**
    - `error`: **170**
    - `pdf_cached`: **1545**
    - `ingested`: **480**
- Remaining `error` rows are now concentrated in a much smaller tail (`doi.org`, `mdpi.com`, `jamanetwork.com`, `academic.oup.com`, repository mirrors), instead of obvious blocked PDF routes repeatedly retried.
- `fetch_case_pmc_fulltext_pilot.py` is now **disabled by default** and requires explicit `--allow-case-report-fetch` opt-in, matching the current policy of not proactively crawling case-report full text.
- Updated `SOURCE_POLICY.md`:
  - prioritize research literature for **medical + AI** trend / gap finding
  - keep case reports as optional weak-signal metadata rather than default full-text crawl targets
  - prefer metadata / abstracts / structured XML/HTML over brittle publisher PDF fetches

## Implication

- The repo is now less likely to waste retries on publisher-blocked OA/PDF routes.
- The current frontier for useful expansion is:
  1. stronger OpenAlex / metadata spine completion (`T127`)
  2. better OA routing for ambiguous DOI rows (e.g. `T217` / Unpaywall)
  3. remaining true-error hosts instead of re-hitting known blocked URLs
- For the stated research goal (find gaps + trends in medical + AI), the best default crawl targets remain:
  - OpenAlex metadata / abstracts
  - Europe PMC / PMC OA structured full text
  - core medical-imaging / clinical-AI journals
  - selective frontier preprints as metadata-first signals
  - **not** bulk case-report full-text crawling by default

---

## 2026-04-01 — Batch close-out: T204–T211, T209, T213 + corpus 6583

- **T204**–**T212**, **T208**, **T214**–**T216**: prior entries below; this run added scripts + CSV updates end-to-end.
- **T209**: `read_priority=high` on **50** rows in `audit_priority_list.csv` and `repro_audit.csv`; join doc in `schema_notes.md`.
- **T210**: `pilot_section_extract_html.py` — **10** HTML → `section_extractions_pilot.jsonl` (gitignored).
- **T211**: `fetch_case_pmc_fulltext_pilot.py` — **20** case `fullTextXML` + `case_reading_status.csv` + manifest rows.
- **T213**: `harvest_openalex_year_slice.py --year 2017` — **+182** papers (**6583** total); abstract ingest **2017** batch **92** ingested; FTS rebuild **6671** lines; Crossref second pass **+139** `oa_url_cached`; T212 second pass **+80** `skipped_policy` (now **1523** total).
- **Manifest**: **~2364** data rows after case + paper EPMC + Layer B retries.
- **DOING handoff**: **T127** (MedIA/TMI full pagination).

## 2026-04-01 — T214 retry batch + T215 retry_queue + T216 cache baseline

- **T214**: `batch_fetch_oa_html.py --retry-errors --limit 300` — **+300** manifest rows; `ingested+abstract+oa_url` **pending** **854 → 535** (**−37%** vs pre-batch `paper_reading_status` on branch tip before this run).
- **T215**: `scripts/append_layerb_errors_to_retry_queue.py` — **+120** `RQ-T215-*` rows in `retry_queue.csv` (distinct `oa_url_cached` from `fulltext_html_status=error`).
- **T216**: Post-run footprint — `cache/fulltext` ~**294MB** (incl. **40** `T205_PMC*.xml`); `cache/pdfs` ~**5.5GB**; `download_manifest` data rows **2344**.

## 2026-04-01 — T204–T207 + T205 EPMC + T206 Crossref/EPMC + T212 policy gate

- **T204**: `scripts/t204_verify_pdf_cache.py` — **20** rows `pdf_status=ingested`; SHA256(on disk) == `download_manifest.file_hash` for existing `T203_*.pdf` paths.
- **T207**: `scripts/build_abstract_fts.py` — SQLite FTS5 **6481** rows from `openalex_abstracts_*.jsonl` → `parsed/abstracts/abstract_index.sqlite` (gitignored); sample query `MATCH 'segmentation'` → **645** hits.
- **T205**: `scripts/fetch_epmc_fulltext_pilot.py` — **40** `fullTextXML` files `cache/fulltext/T205_PMC*.xml`; manifest **DL2005–DL2044**; new registry `paper_epmc_fulltext_pilot.csv`.
- **T206**: `enrich_oa_url_crossref.py` — **500** API calls, **+450** `oa_url_cached` (polite UA with mailto); `enrich_oa_url_epmc.py` (relaxed `inEPMC=Y`) **+9**; `enrich_oa_url_openalex.py` **+0** on missing-URL sample. **http `oa_url` count → 4956/6401**.
- **T212**: `scripts/t212_openalex_policy_gate.py` — **1445** lookups, **1443** rows `fulltext_html_status=skipped_policy` where OpenAlex `open_access.is_oa=false` and still no URL.
- **TODO**: T204,T205,T206,T207,T212 → DONE; **DOING=T214**; added **T217** (Unpaywall optional).

## 2026-04-01 — Cache audit + T203 Layer B batch fetch (phase summary)

- **Cleanup**: Scanned `research_ops/cache/{fulltext,pdfs,tmp}` against `download_manifest.local_path` — **no orphan files** (tmp only `.gitkeep`). No bulk delete of manifest-linked bytes (policy: manifest retained).
- **Script**: Added `scripts/batch_fetch_oa_html.py` — year-priority queue, `--limit`, `--sleep`, `--retry-errors`, `--skip-pdf-primary`, arXiv `/pdf/` → `/abs/` attempts, `Accept: text/html` on requests.
- **Manifest**: **1736** new rows (**DL09201–DL2004**, notes `T203 batch OA fetch`); total data rows **2004**.
- **`paper_reading_status.csv`** (6401 papers): `fulltext_html_status` — **ingested 482**, **pdf_cached 1322**, **error 892**, **pending 3705** (after multi-pass batch + one error-retry sweep).
- **Observation**: Original T203 gate “≥500 `ingested`” is **not met** because many non-PDF landing URLs still return `application/pdf`; corpus now has **1804** Layer-B bytes on disk (`ingested` + `pdf_cached`). **D-006** + **T214–T216** capture follow-up.
- **Disk** (post-run, local): `cache/fulltext` ~**275MB**; `cache/pdfs` ~**4.8GB**, **1323** `.pdf` files.
- **TODO**: **T203** → DONE; **DOING=T204**; added **T214–T216**.

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
