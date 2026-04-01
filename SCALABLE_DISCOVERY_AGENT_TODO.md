# TODO

副标题：Scalable Discovery Agent 的长程任务清单

## 0. 任务系统说明

### 任务状态
只允许：
- TODO
- DOING
- BLOCKED
- DONE
- DROPPED

### 优先级
- P0: 基础设施 / 全局依赖 / 阻塞型任务
- P1: 主线高价值任务
- P2: 重要但不阻塞
- P3: 补充任务
- P4: 可选任务

### 每完成一个任务必须做
1. 更新 `research_ops/00_meta/STATUS.md`
2. 更新 `research_ops/00_meta/RUN_LOG.md`
3. 将任务移入 `DONE`
4. 新增 1-3 个 follow-up tasks
5. 保证 READY/TODO >= 5
6. 重新排序 backlog

## 1. 全局执行约束

### 1.1 远端仓库环境
Agent 运行在 GitHub repository 环境中，可以：
- 下载 metadata / txt / html / xml / json / pdf
- 在 repository 工作目录中解析这些文件
- 将原始文件作为临时缓存处理
- 在抽取完成后删除原始缓存
- 保留 manifest、parse result、hash、source URL、notes、structured outputs

### 1.2 下载与缓存原则
- 优先官方、open-access、可复用、可批量处理来源
- 优先 metadata / XML / TXT / HTML；PDF 只在必要时下载
- 原始文件默认先进入 cache 目录，不直接作为长期资产
- 下载过多时允许“读完即删”，但必须先完成 manifest 和 structured extraction
- 默认不把大量原始 pdf 纳入 git 跟踪

### 1.3 必须保留的内容
即使删除原始文件，也必须保留：
- source URL
- retrieval time
- local path history
- file hash
- mime type
- license note
- parse status
- extracted structured outputs
- provenance note
- redownloadable flag

## 2. DOING

- [ ] T184 Rolling harvest: 2017 window (venues + arXiv)
  - Status: DOING
  - Priority: P1
  - Workstream: Paper Master
  - Parent: T171
  - Title: 10 journals ×35 + arXiv 2017 medimg cap ~70
  - Deliverable: 更新 `papers_master.csv` + RUN_LOG
  - Done When: 新增 ≥100 行
  - Why It Matters: 继续向 2010s 中段回卷

## 3. READY / TODO

### P0 Setup / Governance (follow-ups)

### P0 Download / Cache (follow-up)

### P1 Agentic / Frontier follow-ups

- [ ] T123 Add `venue_type` column to `papers_master.csv` (conference_proceedings | journal | preprint | repository)
  - Status: TODO
  - Priority: P1
  - Workstream: Paper Master
  - Parent: T019
  - Title: Disambiguate LNCS volumes vs journal articles
  - Deliverable: schema + backfill for existing rows
  - Done When: MICCAI/MIDL 行可程序过滤
  - Why It Matters: Deepen — 支撑 T046 合并与 venue 分析

- [ ] T124 Backfill `authors` field via OpenAlex for all `papers_master` rows
  - Status: TODO
  - Priority: P1
  - Workstream: Domain Core
  - Parent: T019
  - Title: Author strings from API `authorships`
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 非空 authors 或显式 `unknown`
  - Why It Matters: Exploit — 检索与去重更稳

- [ ] T125 Harvest remaining MIDL works (OpenAlex ~96 for source S4306519517)
  - Status: TODO
  - Priority: P1
  - Workstream: Domain Core
  - Parent: T020
  - Title: Paginate OpenAlex `cursor=*` for full MIDL coverage
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 全部 MIDL 论文入库或记录 API 缺口
  - Why It Matters: Exploit — 单源完整覆盖

- [ ] T126 Paginate full IPMI + ISBI corpora from OpenAlex (sources S4306418889, S4306420100)
  - Status: TODO
  - Priority: P1
  - Workstream: Domain Core
  - Parent: T021
  - Title: Complete IPMI/ISBI harvest beyond first-page seeds
  - Deliverable: 更新 `papers_master.csv`
  - Done When: counts match OpenAlex `meta.count` or gap documented
  - Why It Matters: Exploit — 与 T125 同类完整覆盖

- [ ] T127 Paginate MedIA + TMI full corpora (sources S116571295, S58069681; thousands of works)
  - Status: TODO
  - Priority: P1
  - Workstream: Domain Core
  - Parent: T022
  - Title: Beyond 25-paper seeds for core journals
  - Deliverable: 更新 `papers_master.csv` + RUN_LOG note on API cost
  - Done When: documented sampling strategy or full ingest complete
  - Why It Matters: Exploit — 期刊主线需要可扩展抓取策略

- [ ] T128 Expand NeurIPS harvest beyond title-keyword gate (use OpenAlex abstract_inverted_index or concepts)
  - Status: TODO
  - Priority: P1
  - Workstream: Method Frontier
  - Parent: T025
  - Title: Recover NeurIPS papers where imaging terms only appear in abstract
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 抽样 20 篇人工核对召回改进
  - Why It Matters: Repair — 当前 T025 偏保守

- [ ] T129 Spot-check `transfer_candidates.csv` rows TC0001–TC0030 against paper titles
  - Status: TODO
  - Priority: P1
  - Workstream: Transfer
  - Parent: T030
  - Title: Validate auto-generated transfer hypotheses
  - Deliverable: `RUN_LOG.md` 核对笔记
  - Done When: 每条标记 valid / weak / drop
  - Why It Matters: Validate — 防止伪迁移条目

- [ ] T130 Add optional `openalex_source_id` column to `papers_master.csv` for harvest reproducibility
  - Status: TODO
  - Priority: P1
  - Workstream: Paper Master
  - Parent: T019
  - Title: Record OpenAlex `primary_location.source.id` used for venue-scoped harvests
  - Deliverable: schema + backfill for venue-sourced rows
  - Done When: MIDL/MICCAI/MedIA 等批次可重放
  - Why It Matters: Deepen — provenance beyond free-text notes

- [ ] T131 Expand ICLR recall using OpenAlex `concepts` or abstract fields (parallel to T128)
  - Status: TODO
  - Priority: P1
  - Workstream: Method Frontier
  - Parent: T027
  - Title: Reduce title-gate false negatives for ICLR biomedical transfer
  - Deliverable: 更新 `papers_master.csv` + RUN_LOG 抽样
  - Done When: 10 篇新增经人工或启发式验证
  - Why It Matters: Repair — T027 与 T026/T025 同型局限

- [ ] T132 Improve ECCV medical harvest (venue metadata sparse in OpenAlex)
  - Status: TODO
  - Priority: P1
  - Workstream: Method Frontier
  - Parent: T029
  - Title: Use proceedings DOI lists or OpenAlex `host_organization` filters to recover ECCV medical papers
  - Deliverable: 更新 `papers_master.csv` + DECISIONS note on method
  - Done When: ≥10 ECCV rows with verified venue string
  - Why It Matters: Repair — T029 ECCV 仅 1 条来自通用 source

### P1 Domain-Core Harvest

### P1 General Method Frontier Harvest

### P1 Clinical / High-Impact Signal Harvest

- [ ] T133 Replace T034 title heuristics with abstract-based extraction for T033-linked papers
  - Status: TODO
  - Priority: P1
  - Workstream: Clinical Signal
  - Parent: T034
  - Title: Pull OpenAlex inverted abstracts to refine endpoint_hint and evidence_pattern
  - Deliverable: 更新 `clinical_signal.csv`
  - Done When: 至少 10 行从 title 推断升级为 abstract 支撑
  - Why It Matters: Repair — 当前 T034 为快速占位

### P1 Biomedical Literature Lake

### P1 Data / Challenge / Trial Map

- [ ] T134 Paginate full Grand Challenge catalog (242+ challenges) into `challenges_master.csv`
  - Status: TODO
  - Priority: P1
  - Workstream: Data Ecosystem
  - Parent: T039
  - Title: Complete GC API crawl with `next` cursor
  - Deliverable: 更新 CSV + manifest row optional
  - Done When: `count` matches API `count` field
  - Why It Matters: Exploit — T039 仅首批 50 条

- [ ] T135 Add `stale` lifecycle_bucket using `modified` vs `end_date` heuristics
  - Status: TODO
  - Priority: P1
  - Workstream: Data Ecosystem
  - Parent: T040
  - Title: Distinguish ended vs stale challenges
  - Deliverable: 更新 `challenges_master.csv`
  - Done When: 规则写入 `DECISIONS.md`
  - Why It Matters: Deepen — 支撑墓地分析

- [ ] T136 Append remaining TCIA collections (153 total) with modality from per-collection metadata API
  - Status: TODO
  - Priority: P1
  - Workstream: Data Ecosystem
  - Parent: T041
  - Title: Full TCIA coverage beyond 40-name seed
  - Deliverable: 更新 `datasets_master.csv`
  - Done When: 每集合一行或记录 API 限制
  - Why It Matters: Exploit — 数据湖底盘

- [ ] T138 Merge `paper_challenge_links` OpenAlex IDs into `papers_master.csv` (dedupe spine)
  - Status: TODO
  - Priority: P1
  - Workstream: Linking
  - Parent: T049
  - Title: Ingest challenge publication works into master table
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 每个 `paper_challenge_links.paper_id` 在 master 中存在
  - Why It Matters: Link — 单一论文主键

- [ ] T139 Build `paper_dataset_links.csv` stub (paper ↔ TCIA/PhysioNet IDs)
  - Status: TODO
  - Priority: P1
  - Workstream: Linking
  - Parent: T049
  - Title: Start dataset linkage beyond challenges
  - Deliverable: `research_ops/19_linking/paper_dataset_links.csv`
  - Done When: 至少 10 条来自论文全文或标题显式数据集名
  - Why It Matters: Exploit — T049 目前仅 challenge 侧

- [ ] T141 Mine OpenAlex `concepts` for frontier paper clustering
  - Status: TODO
  - Priority: P1
  - Workstream: Frontier Radar
  - Parent: T014
  - Title: Add concept vectors to frontier_papers rows
  - Deliverable: 更新 CSV 或 sidecar JSONL
  - Done When: 每篇 frontier 论文至少有 top-3 concept labels
  - Why It Matters: Exploit — T102 frontier follow-up

- [ ] T142 Build frontier ↔ pain_point auto-linker using title token overlap
  - Status: TODO
  - Priority: P1
  - Workstream: Trend Linking
  - Parent: T076
  - Title: Expand trend_to_problem_links beyond manual 8 rows
  - Deliverable: 更新 `trend_to_problem_links.csv`
  - Done When: ≥30 links with confidence field
  - Why It Matters: Link — T102

- [ ] T143 Harvest OpenReview forum metadata for frontier_papers subset
  - Status: TODO
  - Priority: P1
  - Workstream: Frontier Radar
  - Parent: T014
  - Title: Attach review scores where venue is OpenReview
  - Deliverable: 更新 `frontier_papers.csv` 或链接表
  - Done When: ≥10 rows enriched
  - Why It Matters: Validate — T102

- [ ] T144 Add `trend_signals.csv` rows from monthly OpenAlex alert query
  - Status: TODO
  - Priority: P1
  - Workstream: Frontier Radar
  - Parent: T014
  - Title: Operationalize trend_signals registry
  - Deliverable: 更新 `trend_signals.csv`
  - Done When: ≥10 signals with strength score
  - Why It Matters: Exploit — T102

- [ ] T145 Cross-map frontier_papers to transfer_candidates with embedding similarity
  - Status: TODO
  - Priority: P1
  - Workstream: Transfer
  - Parent: T030
  - Title: Auto-suggest medical_imaging transfer targets
  - Deliverable: 更新 `transfer_candidates.csv`
  - Done When: ≥20 new rows with similarity score column
  - Why It Matters: Exploit — T102

- [ ] T146 Build frontier agent safety eval checklist (tool abuse / PHI)
  - Status: TODO
  - Priority: P1
  - Workstream: Agentic Systems
  - Parent: T016
  - Title: Document red-team scenarios for clinical agents
  - Deliverable: `15_agentic/skill_cards/SK011_safety_redteam.md`
  - Done When: ≥8 scenarios
  - Why It Matters: Deepen — T102

- [ ] T147 Link MedAgentSim-class papers to repro_audit yellow bucket
  - Status: TODO
  - Priority: P2
  - Workstream: Repro Audit
  - Parent: T053
  - Title: Track simulation papers separately from clinical deployment claims
  - Deliverable: 更新 `repro_audit.csv`
  - Done When: ≥5 rows tagged `simulation_only`
  - Why It Matters: Repair — T102

- [ ] T148 Expand anti_hype_checks for “self-evolving” claims using promotion_tests
  - Status: TODO
  - Priority: P2
  - Workstream: Hypothesis
  - Parent: T077
  - Title: Tie AH002 to concrete PT-* tests
  - Deliverable: 更新 `anti_hype_checks.csv`
  - Done When: 每条 check 关联 test_id
  - Why It Matters: Link — T102

- [ ] T149 Add arXiv version graph for frontier preprints
  - Status: TODO
  - Priority: P2
  - Workstream: Frontier Radar
  - Parent: T014
  - Title: Track v1→v2 diffs for hot preprints
  - Deliverable: sidecar CSV
  - Done When: ≥5 chains recorded
  - Why It Matters: Exploit — T102

- [ ] T150 Summarize frontier batch in `trend_memos/frontier_batch_001.md`
  - Status: TODO
  - Priority: P2
  - Workstream: Frontier Radar
  - Parent: T014
  - Title: Human-readable snapshot of frontier radar
  - Deliverable: memo under `14_frontier/trend_memos/`
  - Done When: 覆盖 top 10 papers + 3 risks
  - Why It Matters: Exploit — T102

- [ ] T151 Run ORDO/OMIM dictionary match on case titles
  - Status: TODO
  - Priority: P1
  - Workstream: Case Lake
  - Parent: T063
  - Title: Upgrade disease_primary field
  - Deliverable: 更新 `case_reports_master.csv`
  - Done When: ≥50 rows with ORDO id
  - Why It Matters: Exploit — T103

- [ ] T152 Extract negation cues from case abstracts into negative_findings column
  - Status: TODO
  - Priority: P1
  - Workstream: Case Lake
  - Parent: T063
  - Title: Apply checklist T070 automatically
  - Deliverable: 更新 case_reports_master
  - Done When: ≥100 rows with non-empty negations
  - Why It Matters: Exploit — T103

- [ ] T153 Build PMC OA full-text fetch pass for top 20 rare cases
  - Status: TODO
  - Priority: P1
  - Workstream: Case Lake
  - Parent: T062
  - Title: Move from metadata-only to structured narrative fields
  - Deliverable: manifest + parsed fields
  - Done When: 20 cases with outcomes section extracted
  - Why It Matters: Deepen — T103

- [ ] T154 Align case_reports_master.pmid with PubTator annotations pull
  - Status: TODO
  - Priority: P1
  - Workstream: Case Lake
  - Parent: T063
  - Title: Entity-normalized phenotypes
  - Deliverable: 更新 phenopackets
  - Done When: ≥50 rows with gene/disease entities
  - Why It Matters: Exploit — T103

- [ ] T155 Split case lake train/val by journal+year grouped split
  - Status: TODO
  - Priority: P2
  - Workstream: Case Lake
  - Parent: T067
  - Title: Leakage-safe evaluation for RDRET
  - Deliverable: split manifest CSV
  - Done When: documented split ids
  - Why It Matters: Validate — T103

- [ ] T156 Add language field and filter non-English for v1 benchmarks
  - Status: TODO
  - Priority: P2
  - Workstream: Case Lake
  - Parent: T062
  - Title: Reduce noise in retrieval eval
  - Deliverable: 更新 case_reports_master
  - Done When: language populated from Europe PMC
  - Why It Matters: Repair — T103

- [ ] T157 Link case reports to nearest ClinicalTrials.gov trials by condition tokens
  - Status: TODO
  - Priority: P2
  - Workstream: Linking
  - Parent: T043
  - Title: case→trial weak links
  - Deliverable: `paper_trial_links` pattern reuse or new `case_trial_links.csv`
  - Done When: ≥20 links
  - Why It Matters: Link — T103

- [ ] T158 Mine figure availability flag from Europe PMC `hasFigures` if exposed
  - Status: TODO
  - Priority: P2
  - Workstream: Case Lake
  - Parent: T066
  - Title: Improve case_report_figures coverage
  - Deliverable: 更新 figures table
  - Done When: ≥50 figure rows
  - Why It Matters: Exploit — T103

- [ ] T159 Build case-to-paper citation graph via Europe PMC references API
  - Status: TODO
  - Priority: P2
  - Workstream: Literature Lake
  - Parent: T035
  - Title: Connect cases to guidelines/lit reviews
  - Deliverable: linking CSV
  - Done When: ≥30 edges
  - Why It Matters: Link — T103

- [ ] T160 Publish case lake stats memo `case_lake_stats_001.md`
  - Status: TODO
  - Priority: P2
  - Workstream: Case Lake
  - Parent: T062
  - Title: Counts by journal/year/language
  - Deliverable: memo in `16_case_reports/`
  - Done When: histograms + top journals
  - Why It Matters: Exploit — T103

- [ ] T161 Automate PT-* tests in CI script (dry-run mode)
  - Status: TODO
  - Priority: P2
  - Workstream: Agent Self-Improvement
  - Parent: T081
  - Title: Wire promotion tests to benchmark_tasks
  - Deliverable: `scripts/run_promotion_tests.sh` (or python)
  - Done When: script exits 0 on sandbox
  - Why It Matters: Exploit — T104

- [ ] T162 Add skill versioning field to skill_cards frontmatter
  - Status: TODO
  - Priority: P2
  - Workstream: Agent Self-Improvement
  - Parent: T080
  - Title: Track semver per skill
  - Deliverable: update 10 cards
  - Done When: each card has version
  - Why It Matters: Deepen — T104

- [ ] T163 Map each RL00x reflection to a concrete repair task id
  - Status: TODO
  - Priority: P2
  - Workstream: Agent Self-Improvement
  - Parent: T083
  - Title: Close the loop reflection→TODO
  - Deliverable: 更新 reflection_log notes
  - Done When: 3/3 RL rows linked
  - Why It Matters: Repair — T104

- [ ] T164 Add `skill_graph.csv` edges for SK001–SK010 dependencies
  - Status: TODO
  - Priority: P2
  - Workstream: Agent Self-Improvement
  - Parent: T080
  - Title: DAG for skill composition
  - Deliverable: 更新 skill_graph.csv
  - Done When: ≥10 edges
  - Why It Matters: Link — T104

- [ ] T165 Define rollback procedure for promoted skills
  - Status: TODO
  - Priority: P2
  - Workstream: Agent Self-Improvement
  - Parent: T079
  - Title: Document git revert + benchmark regression rule
  - Deliverable: paragraph in `what_counts_as_real_agent_self_evolution.md`
  - Done When: rollback steps explicit
  - Why It Matters: Deepen — T104

- [ ] T166 Add `promotion_tests` negative tests (must fail on bad outputs)
  - Status: TODO
  - Priority: P2
  - Workstream: Agent Self-Improvement
  - Parent: T081
  - Title: Contrastive pass/fail pairs
  - Deliverable: 更新 promotion_tests.csv
  - Done When: ≥3 negative tests
  - Why It Matters: Validate — T104

- [ ] T167 Benchmark runtime SLOs for SK002 and SK003
  - Status: TODO
  - Priority: P2
  - Workstream: Agent Self-Improvement
  - Parent: T082
  - Title: Record p50/p95 latencies
  - Deliverable: RUN_LOG table
  - Done When: 20 samples each
  - Why It Matters: Exploit — T104

- [ ] T168 Add secret-handling section to skill_template
  - Status: TODO
  - Priority: P2
  - Workstream: Agent Self-Improvement
  - Parent: T079
  - Title: Never embed tokens in skill cards
  - Deliverable: update skill_template.md
  - Done When: policy bullet list added
  - Why It Matters: Repair — T104

- [ ] T169 Create `SK011` for PubMed E-utilities polite pooling
  - Status: TODO
  - Priority: P2
  - Workstream: Agent Self-Improvement
  - Parent: T080
  - Title: Wrap NCBI rate-limit recipe
  - Deliverable: new skill card
  - Done When: card + PT test stub
  - Why It Matters: Exploit — T104

- [ ] T170 Weekly skill health report markdown export
  - Status: TODO
  - Priority: P2
  - Workstream: Agent Self-Improvement
  - Parent: T083
  - Title: Aggregate reflection_log + failed PT tests
  - Deliverable: `13_exports/run_summaries/skill_health_001.md`
  - Done When: first report generated
  - Why It Matters: Exploit — T104

### P1 Paper Master Assembly

### P2 Benchmark / Repro / Failure

- [ ] T140 Full-text benchmark extraction for Swin UNETR (W4312428231) from CVF / IEEE page
  - Status: TODO
  - Priority: P2
  - Workstream: Benchmark Forensics
  - Parent: T054
  - Title: Replace abstract placeholder BT006 with numeric Dice rows
  - Deliverable: 更新 `benchmark_tables.csv`
  - Done When: Decathlon + BTCV tasks have per-task metrics
  - Why It Matters: Repair — abstract only cites leaderboards

## 4. BLOCKED

- [ ] None yet
  - Status: BLOCKED
  - Priority: P4
  - Workstream: Placeholder
  - Parent: ROOT
  - Title: No blocked tasks yet
  - Deliverable: N/A
  - Done When: N/A
  - Why It Matters: 占位

## 5. DONE

- [x] T000 Initialize `research_ops/` directory and subfolders — 2026-03-31
- [x] T001 Create all core CSV headers — 2026-03-31
- [x] T002 Create meta control files — 2026-03-31
- [x] T003 Write initial TODO system — 2026-03-31
- [x] T004 Create scoring policy — 2026-03-31
- [x] T005 Create license and retention policy — 2026-03-31
- [x] T006A Define repository-local download workspace layout — 2026-03-31 (`SCALABLE_DISCOVERY_AGENT.md` §6 + `gitignore_policy.md`)
- [x] T006B Create download and parse manifest schemas — 2026-03-31
- [x] T006C Define file retention rules — 2026-03-31 (`LICENSE_POLICY.md`)
- [x] T006D Define cleanup-after-parse workflow — 2026-03-31 (`cache_cleanup_workflow.md`)
- [x] T006E Define redownloadable artifacts policy — 2026-03-31 (`download_manifest.csv` + `LICENSE_POLICY.md`)
- [x] T006F Define parser output survival rules — 2026-03-31 (`LICENSE_POLICY.md`)
- [x] T006G Define repository-safe download policy — 2026-03-31 (`gitignore_policy.md` + root `.gitignore`)
- [x] T006 Build broad source registry — 2026-03-31 (45 rows, layers A–G)
- [x] T095 Define article download policy by content type — 2026-03-31 (`LICENSE_POLICY.md` table)
- [x] T096 Build article acquisition decision tree — 2026-03-31 (`article_acquisition_decision_tree.md`)
- [x] T097 Define raw-file deletion checkpoints — 2026-03-31 (`LICENSE_POLICY.md` checkpoints section)
- [x] T107 Mirror canonical TODO to repo root — 2026-03-31 (`cp` sync; single source `research_ops/00_meta/TODO.md`)
- [x] T108 Add CSV schema notes — 2026-03-31 (`schema_notes.md`)
- [x] T109 Validate directory tree — 2026-03-31 (python check; `missing: []` in RUN_LOG)
- [x] T110 Storage budget / cleanup triggers — 2026-03-31 (`LICENSE_POLICY.md` storage section)
- [x] T007 Build broad `venue_registry.csv` — 2026-03-31 (29 venues, layers A/B/C/F)
- [x] T008 Register domain-core venues — 2026-03-31 (subset of venue_registry)
- [x] T009 Register general ML/CV frontier venues — 2026-03-31
- [x] T010 Register high-impact science and clinical venues — 2026-03-31
- [x] T011 Register data / infrastructure sources — 2026-03-31 (`source_registry.csv`)
- [x] T012 Create first `query_registry.csv` — 2026-03-31 (10 query families)
- [x] T013 Build `frontier_queries.csv` — 2026-03-31 (30 templates)
- [x] T035 Register literature infrastructure — 2026-03-31 (same registry rows; `literature_parseability.md`)
- [x] T036 Build parseability / reuse table — 2026-03-31 (`literature_parseability.md`)
- [x] T014 Harvest frontier papers (discovery agents) — 2026-03-31 (`frontier_papers.csv` 22 rows, OpenAlex)
- [x] T015 Harvest frontier papers (biomedical/clinical agents) — 2026-03-31 (merged into same CSV)
- [x] T016 Build first `agent_systems.csv` — 2026-03-31 (15 systems)
- [x] T017 Build `self_evolution_patterns.csv` — 2026-03-31 (12 patterns)
- [x] T018 Write self-evolution memo — 2026-03-31 (`what_counts_as_real_agent_self_evolution.md`)
- [x] T071–T074 Clinical pull tables — 2026-03-31 (`pain_points`, `workflow_bottlenecks`, `unmet_needs`, `scaling_fit_scores`)
- [x] T075 `scalable_problem_map.csv` — 2026-03-31 (20 rows from PP001–PP020)
- [x] T059 Define `case_reports_master.csv` schema — 2026-03-31 (expanded headers)
- [x] T060 Define `phenopackets.csv` schema — 2026-03-31
- [x] T061 Define `case_report_figures.csv` schema — 2026-03-31
- [x] T037 Define `paper_trial_links.csv` schema — 2026-03-31 (enriched headers)
- [x] T038 Define `paper_guideline_links.csv` schema — 2026-03-31 (enriched headers)
- [x] T019 Harvest MICCAI metadata (seed) — 2026-03-31 (`papers_master.csv` 20 rows via OpenAlex search)
- [x] T113 Frontier → transfer promotion heuristics — 2026-03-31 (`DECISIONS.md` D-004)
- [x] T105 Write first run summary — 2026-03-31 (`summary_001.md`)
- [x] T106 Update next best action in STATUS — 2026-03-31
- [x] T020 Harvest MIDL metadata — 2026-03-31 (20 works, OpenAlex `primary_location.source.id:S4306519517`)
- [x] T111 Link `agent_systems` → `papers_master` — 2026-03-31 (`papers_master_paper_id` column + T111 backfill rows)
- [x] T112 Enrich `frontier_papers` venues — 2026-03-31 (OpenAlex per-row)
- [x] T117 `paper_trial_links.relation_type` vocabulary — 2026-03-31 (`DECISIONS.md` D-005)
- [x] T118 `guideline_registry.csv` stub — 2026-03-31
- [x] T119 Pilot `paper_trial_links` — 2026-03-31 (50 rows: DOI in CT.gov JSON → OpenAlex)
- [x] T120 Filter MICCAI seed to LNCS proceedings volumes — 2026-03-31 (dropped 1 non-LNCS journal row)
- [x] T121 Dedup `papers_master` vs `frontier_papers` — 2026-03-31 (0 overlap; script verified)
- [x] T122 MICCAI official bibliography note — 2026-03-31 (`source_batches/README_MICCAI_official_bibliography.md`)
- [x] T021 Harvest IPMI / ISBI metadata — 2026-03-31 (15+15 works, OpenAlex sources S4306418889 + S4306420100)
- [x] T022 Harvest MedIA metadata — 2026-03-31 (25 works, source S116571295)
- [x] T023 Harvest TMI metadata — 2026-03-31 (25 works, source S58069681)
- [x] T024 Harvest Radiology / Radiology: AI — 2026-03-31 (15+15, S50280174 + S4210219523)
- [x] T025 Harvest NeurIPS candidates — 2026-03-31 (30 papers, source S4306420609, years 2019–2021 keyword gate)
- [x] T030 Build `transfer_candidates.csv` — 2026-03-31 (30 rows aligned to T025)
- [x] T026 Harvest ICML candidates — 2026-03-31 (30 papers, source S4306419644, years 2014–2022 keyword gate)
- [x] T027 Harvest ICLR candidates — 2026-03-31 (30 papers, source S4306419637, years 2020–2024 keyword gate)
- [x] T028 Harvest CVPR candidates — 2026-03-31 (30 papers from CVPR 2022 source S4363607701 + 2 legacy S4306417987)
- [x] T029 Harvest ICCV / ECCV — 2026-03-31 (15 ICCV 2021 S4363607764; 1 ECCV via S4306418318 segmentation gate — see T132)
- [x] T031 Harvest Nature / Science / Cell — 2026-03-31 (30 papers; sources S137773608, S3880285, S110447773)
- [x] T032 Harvest translational journals — 2026-03-31 (32 papers; Nat Med, NBE, npj DM, Comm Med)
- [x] T033 Harvest JAMA / JAMA Open / NEJM / Lancet DH — 2026-03-31 (32 papers)
- [x] T034 Extract clinical_signal + registries — 2026-03-31 (32 signals + 12 endpoints + 11 patterns; title heuristics)
- [x] T039 Harvest Grand Challenge metadata — 2026-03-31 (50 challenges via `grand-challenge.org/api/v1/challenges/`)
- [x] T040 Split challenges lifecycle — 2026-03-31 (`lifecycle_bucket` column from OPEN/CLOSED)
- [x] T041 Harvest TCIA collections — 2026-03-31 (40 collections into `datasets_master.csv` via NBIA `getCollectionValues`)
- [x] T042 Harvest PhysioNet datasets — 2026-03-31 (30 DB projects appended via `physionet.org/api/v1/project/published/`)
- [x] T043 Harvest ClinicalTrials.gov — 2026-03-31 (`19_linking/trials_master.csv`, 30 studies)
- [x] T044 `datasets_master.csv` — 2026-03-31 (70 rows: TCIA + PhysioNet)
- [x] T045 `challenges_master.csv` — 2026-03-31 (50 rows + `lifecycle_bucket`)
- [x] T046 Unified `papers_master.csv` — 2026-03-31 (single spine; incremental merges during harvest)
- [x] T047 Normalize `tags_modality` — 2026-03-31 (controlled facets in `schema_notes.md`)
- [x] T048 Normalize `tags_method` — 2026-03-31 (title+batch heuristics)
- [x] T049 Link papers to challenges — 2026-03-31 (`19_linking/paper_challenge_links.csv`, 19 rows via DOI→OpenAlex)
- [x] T050 Audit priority list — 2026-03-31 (`06_repro/audit_priority_list.csv`, 50 papers)
- [x] T051 Build `repo_registry.csv` — 2026-03-31 (19 repos from OpenAlex abstract GitHub URLs)
- [x] T052 Mine GitHub issues — 2026-03-31 (`issue_mining.csv`, 20 issues from public API)
- [x] T053 Build `repro_audit.csv` — 2026-03-31 (50 rows; red/yellow from repo presence heuristic)
- [x] T054 Extract benchmark tables — 2026-03-31 (C-CAM WSSS medical subfield; `benchmark_tables.csv`)
- [x] T055 Build `split_audit.csv` — 2026-03-31 (3 rows; WSSS + leaderboard comparability)
- [x] T056 Extract failure modes — 2026-03-31 (`failure_modes.csv` seed from C-CAM + Swin UNETR abstract gaps)
- [x] T057 Task graveyard — 2026-03-31 (31 CLOSED Grand Challenge rows in `task_graveyard.csv`)
- [x] T058 Resurrection candidates — 2026-03-31 (15 imaging-related closed challenges)
- [x] T114 Case pipeline cross-link — 2026-03-31 (`case_report_cache_lifecycle.md` + `cache_cleanup_workflow.md` § Case-report variant)
- [x] T115 Phenopacket column mapping — 2026-03-31 (`schema_notes.md` Case lake section)
- [x] T116 Europe PMC query templates — 2026-03-31 (`query_registry.csv` Q011–Q015)
- [x] T062 OA case harvest — 2026-03-31 (200 records + `cache/metadata` JSON + `download_manifest.csv`)
- [x] T063 Structured case records — 2026-03-31 (`case_reports_master.csv` 200 rows)
- [x] T064 Phenopacket-like rows — 2026-03-31 (`phenopackets.csv` 200 minimal rows)
- [x] T065 Case cache lifecycle memo — 2026-03-31 (`case_report_cache_lifecycle.md`)
- [x] T066 Case report figures — 2026-03-31 (`case_report_figures.csv` 6 placeholder rows)
- [x] T067 Rare disease retrieval seed — 2026-03-31 (`rare_disease_retrieval_seed.csv` + memo)
- [x] T068 Atypical presentation memo — 2026-03-31 (`atypical_presentation_memo.md`)
- [x] T069 Differential diagnosis seed — 2026-03-31 (`differential_diagnosis_seed.csv` 15 rows)
- [x] T070 Negative finding checklist — 2026-03-31 (`negative_finding_checklist.md`)
- [x] T076 Trend → bottleneck links — 2026-03-31 (`trend_to_problem_links.csv` 8 rows)
- [x] T077 Anti-hype checks — 2026-03-31 (`anti_hype_checks.csv` 5 rows)
- [x] T078 Scaling opportunities — 2026-03-31 (`scaling_opportunities.csv` 5 rows)
- [x] T079 Skill template — 2026-03-31 (`15_agentic/skill_template.md`)
- [x] T080 Skill cards — 2026-03-31 (`SK001`–`SK010` under `skill_cards/`)
- [x] T081 `promotion_tests.csv` — 2026-03-31 (10 PT-* rows)
- [x] T082 `benchmark_tasks.csv` — 2026-03-31 (5 tasks)
- [x] T083 `reflection_log.csv` — 2026-03-31 (3 RL rows)
- [x] T084 `hypothesis_market.csv` — 2026-03-31 (5 hypotheses)
- [x] T085 `cheap_tests.csv` — 2026-03-31 (5 tests)
- [x] T086 `evidence_gaps.csv` — 2026-03-31 (5 gaps)
- [x] T087 `idea_queue.csv` — 2026-03-31 (5 ideas)
- [x] T088 `reviewer_attacks.csv` — 2026-03-31 (5 attacks)
- [x] T089 Off-label benchmark seed memo — 2026-03-31 (`synthesis_memos/off_label_response_benchmark_seed.md`)
- [x] T090 AE mining benchmark seed memo — 2026-03-31 (`synthesis_memos/adverse_event_mining_benchmark_seed.md`)
- [x] T091 Oncology MDT memo — 2026-03-31 (`synthesis_memos/oncology_mdt_opportunity.md`)
- [x] T092 Evidence synthesis memo — 2026-03-31 (`synthesis_memos/evidence_synthesis_opportunity.md`)
- [x] T093 Trial matching memo — 2026-03-31 (`synthesis_memos/trial_matching_opportunity.md`)
- [x] T094 Rare disease support memo — 2026-03-31 (`synthesis_memos/rare_disease_support_opportunity.md`)
- [x] T098 `keep_set_manifest.csv` — 2026-03-31 (policy rows + placeholders)
- [x] T099 `retry_queue.csv` — 2026-03-31 (template rows for failed jobs)
- [x] T100 Storage budget — 2026-03-31 (same thresholds as T110 in `LICENSE_POLICY.md`)
- [x] T101 Reprioritize backlog — 2026-03-31 (P1 frontier/case/skill follow-ups T141–T170 added)
- [x] T102 Frontier follow-ups — 2026-03-31 (T141–T150)
- [x] T103 Case mining follow-ups — 2026-03-31 (T151–T160)
- [x] T104 Skill harness follow-ups — 2026-03-31 (T161–T170)
- [x] T137 `trials_master` documentation — 2026-03-31 (`schema_notes.md`)
- [x] T171 Rolling wide recent harvest — 2026-03-31 (10 journals × 2024–2025 + 7 global searches; +1464 rows net of dedupe)
- [x] T172 arXiv repository broad slices — 2026-03-31 (OpenAlex `S4306400194`; +382 rows; tag `preprint_broad`)
- [x] T173 Rolling window 2023 — 2026-03-31 (10 journals ×70 + arXiv 2023 two queries; +916 rows; total papers_master 3158)
- [x] T177 Rolling window 2022 — 2026-03-31 (10 journals ×65 + arXiv 2022 two queries; +814 rows; total 3972)
- [x] T176 bioRxiv/medRxiv 2024–2025 — 2026-03-31 (S4306402567 + S4306400573; +126 rows; total 4098)
- [x] T178 Rolling window 2021 — 2026-03-31 (10 journals ×55 + arXiv 2021 medimg; +660 rows; total 4758)
- [x] T179 bioRxiv/medRxiv deepen — 2026-03-31 (2023 six-query sweep + 2024–25 spatial/scRNA; +264 rows; total 5022)
- [x] T180 Rolling window 2020 — 2026-03-31 (10 journals ×50 + arXiv2020 medimg cap 100; +550 rows; total 5572)
- [x] T181 Rolling window 2019 — 2026-03-31 (10 journals ×45 + arXiv2019 medimg cap 90; +492 rows; total 6064 before monthly smoke)
- [x] T174 `harvest_window` column — 2026-03-31 (backfilled from `source_batch` + T182 rows use `YYYY-MM`)
- [x] T182 Monthly harvest script — 2026-03-31 (`scripts/harvest_openalex_monthly.py`; smoke +5 rows for MedIA 2025-01)
- [x] T175 `topic_subtag` for preprints — 2026-03-31 (1452 rows: preprint_broad/biorxiv/medrxiv title heuristics)
- [x] T183 Rolling window 2018 — 2026-03-31 (10 journals ×40 + arXiv2018 cap 80; +332 rows; total 6401)

## 6. Drop Rules

以下任务默认降权或丢弃：
- “多读一些 paper”
- 只有 abstract 摘要、没有结构化产物
- 无法连接到数据、趋势、病例、失败点、clinical pull 的任务
- 无下载 manifest、无 provenance、无清理策略的抓取任务
- 版权不清却试图长期囤积大量 PDF 的任务

## 7. Follow-up Rules

每完成一个任务，最多新增 3 个 follow-up，来源只允许：
- Deepen
- Validate
- Exploit
- Repair
- Link

新增任务必须具体，不能写：
- 再看看
- 多研究一些
- 总结趋势
- 看看有没有新的

## 8. 优先级顺序

从现在开始优先顺序是：
1. 来源地图与下载/缓存治理
2. frontier + agentic + scaling 趋势雷达
3. biomedical literature lake 可用底盘
4. datasets / challenges / trials / guidelines 地图
5. case report lake + phenopacket factory
6. benchmark / repro / failure 法医库
7. clinical pain-point reverse search 与 scaling fit 排名
8. trend -> old bottleneck -> new opportunity 连接层
9. agent self-improvement harness
10. idea queue / reviewer attacks / cheap tests

## 9. 建议启动顺序

如果第一次运行，建议按以下顺序：
1. T000
2. T001
3. T002
4. T005
5. T006A
6. T006B
7. T006D
8. T006
9. T007
10. T011
11. T013
12. T035
13. T059
14. T071
15. T046

## 10. 最后提醒

这个系统不是为了“多读点 paper”，而是为了构建一个：
- 能下载并解析大规模文献
- 能在必要时读完就删缓存原文
- 但不丢结构化资产和 provenance
- 能连接趋势、旧文献、病例、临床问题
- 能持续产出 scalable discovery opportunities

的长期科研情报系统。
