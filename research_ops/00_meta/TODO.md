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

- [ ] T020 Harvest MIDL metadata
  - Status: DOING
  - Priority: P1
  - Workstream: Domain Core
  - Parent: ROOT
  - Title: Harvest MIDL metadata
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 一批 MIDL metadata 入库
  - Why It Matters: 医疗 ML 方法主线入口

## 3. READY / TODO

### P0 Setup / Governance (follow-ups)

### P0 Download / Cache (follow-up)

### P1 Agentic / Frontier follow-ups

- [ ] T111 Link `agent_systems.csv` rows to future `papers_master.csv` entries with shared `paper_id`
  - Status: TODO
  - Priority: P1
  - Workstream: Agentic Systems
  - Parent: T016
  - Title: Unify IDs between registries
  - Deliverable: 更新两表或链接表
  - Done When: 每个 agent_system 能解析到 bibliographic 主键
  - Why It Matters: Link — 避免孤立的 OpenAlex 引用

- [ ] T112 Normalize `frontier_papers.csv` venue and type fields via OpenAlex API enrichment pass
  - Status: TODO
  - Priority: P1
  - Workstream: Frontier Radar
  - Parent: T014
  - Title: Enrich frontier paper metadata
  - Deliverable: 更新 CSV
  - Done When: venue 列非空或显式 `preprint`
  - Why It Matters: Validate — 支持按 venue 过滤噪声

- [ ] T117 Document `paper_trial_links` relation_type vocabulary
  - Status: TODO
  - Priority: P1
  - Workstream: Literature Lake
  - Parent: T037
  - Title: Add controlled vocabulary to `DECISIONS.md`
  - Deliverable: `DECISIONS.md` subsection
  - Done When: 至少 5 个 relation_type 值有定义与示例
  - Why It Matters: Deepen — 避免链接语义漂移

- [ ] T118 Create `guideline_registry.csv` stub for guideline IDs
  - Status: TODO
  - Priority: P1
  - Workstream: Literature Lake
  - Parent: T038
  - Title: Normalize guideline references
  - Deliverable: `research_ops/19_linking/guideline_registry.csv` (headers only)
  - Done When: guideline_id 可映射到组织、版本、URL
  - Why It Matters: Link — paper–guideline 可维护

- [ ] T119 Seed `paper_trial_links` from OpenAlex → ClinicalTrials.gov abstract mentions (pilot 50 rows)
  - Status: TODO
  - Priority: P1
  - Workstream: Literature Lake
  - Parent: T037
  - Title: Pilot automated trial linking
  - Deliverable: 更新 `paper_trial_links.csv`
  - Done When: 50 条可人工 spot-check 的链接
  - Why It Matters: Exploit — 验证链接管线

### P1 Domain-Core Harvest

- [ ] T120 Filter `papers_master` seed rows to MICCAI-proceedings only (venue / conference series match)
  - Status: TODO
  - Priority: P1
  - Workstream: Domain Core
  - Parent: T019
  - Title: Remove OpenAlex search noise from MICCAI harvest
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 非 MICCAI 论文已移除或标记 `notes=noise`
  - Why It Matters: Validate — 搜索词会混入非会议论文

- [ ] T121 Deduplicate `papers_master` against `frontier_papers` by `openalex_id`
  - Status: TODO
  - Priority: P1
  - Workstream: Paper Master
  - Parent: T019
  - Title: Single paper spine across tables
  - Deliverable: 去重后的 papers_master 或链接说明
  - Done When: 同一 OpenAlex ID 只保留一行主记录
  - Why It Matters: Link — 防止多表分裂

- [ ] T122 Ingest official MICCAI open bibliography (if available) into `source_batches/`
  - Status: TODO
  - Priority: P1
  - Workstream: Domain Core
  - Parent: T019
  - Title: Replace search-based seed with curator-grade list
  - Deliverable: manifest + batch note
  - Done When: provenance 指向官方来源而非仅 OpenAlex search
  - Why It Matters: Deepen — 会议论文应用官方元数据

- [ ] T021 Harvest IPMI / ISBI metadata
  - Status: TODO
  - Priority: P1
  - Workstream: Domain Core
  - Parent: ROOT
  - Title: Harvest IPMI and ISBI metadata
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 一批历史和方法脉络论文入库
  - Why It Matters: 补足领域时间轴

- [ ] T022 Harvest MedIA metadata
  - Status: TODO
  - Priority: P1
  - Workstream: Domain Core
  - Parent: ROOT
  - Title: Harvest MedIA metadata
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 一批 MedIA 元数据入库
  - Why It Matters: 核心期刊高信号来源

- [ ] T023 Harvest TMI metadata
  - Status: TODO
  - Priority: P1
  - Workstream: Domain Core
  - Parent: ROOT
  - Title: Harvest TMI metadata
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 一批 TMI 元数据入库
  - Why It Matters: 核心期刊高信号来源

- [ ] T024 Harvest Radiology / Radiology: AI metadata
  - Status: TODO
  - Priority: P1
  - Workstream: Domain Core
  - Parent: ROOT
  - Title: Harvest Radiology and Radiology: AI metadata
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 一批临床影像 AI 元数据入库
  - Why It Matters: 连接方法与临床转化

### P1 General Method Frontier Harvest

- [ ] T025 Harvest NeurIPS candidates
  - Status: TODO
  - Priority: P1
  - Workstream: Method Frontier
  - Parent: ROOT
  - Title: Harvest NeurIPS candidate papers relevant to vision, multimodal, representation, agent, robustness
  - Deliverable: `papers_master.csv` + `transfer_candidates.csv`
  - Done When: 一批可迁移 NeurIPS 候选入库
  - Why It Matters: 方法迁移主来源

- [ ] T026 Harvest ICML candidates
  - Status: TODO
  - Priority: P1
  - Workstream: Method Frontier
  - Parent: ROOT
  - Title: Harvest ICML candidate papers relevant to transferable methods
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 一批 ICML 候选入库
  - Why It Matters: 泛化方法线索

- [ ] T027 Harvest ICLR candidates
  - Status: TODO
  - Priority: P1
  - Workstream: Method Frontier
  - Parent: ROOT
  - Title: Harvest ICLR candidate papers relevant to pretraining, foundation, representation, agents
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 一批 ICLR 候选入库
  - Why It Matters: foundation / representation / agent 关键来源

- [ ] T028 Harvest CVPR candidates
  - Status: TODO
  - Priority: P1
  - Workstream: Method Frontier
  - Parent: ROOT
  - Title: Harvest CVPR candidate papers relevant to medical imaging transfer
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 一批 CVPR 候选入库
  - Why It Matters: 视觉方法迁移入口

- [ ] T029 Harvest ICCV / ECCV candidates
  - Status: TODO
  - Priority: P1
  - Workstream: Method Frontier
  - Parent: ROOT
  - Title: Harvest ICCV and ECCV candidate papers for 3D/video/segmentation/VLM transfer
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 一批 ICCV/ECCV 候选入库
  - Why It Matters: 3D / 视频 / VLM 迁移价值高

- [ ] T030 Build first `transfer_candidates.csv`
  - Status: TODO
  - Priority: P1
  - Workstream: Transfer
  - Parent: T025
  - Title: Build transfer candidate table
  - Deliverable: `research_ops/10_transfer/transfer_candidates.csv`
  - Done When: 至少列出 30 个迁移机会
  - Why It Matters: 把方法前沿压缩成可执行清单

### P1 Clinical / High-Impact Signal Harvest

- [ ] T031 Harvest Nature / Science / Cell candidates
  - Status: TODO
  - Priority: P1
  - Workstream: Clinical Signal
  - Parent: ROOT
  - Title: Harvest high-impact science candidates relevant to biomedical AI and computational medicine
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 高影响科学层候选入库
  - Why It Matters: 获取真正重要的问题定义

- [ ] T032 Harvest Nature Medicine / NBE / npj / Communications Medicine candidates
  - Status: TODO
  - Priority: P1
  - Workstream: Clinical Signal
  - Parent: ROOT
  - Title: Harvest translational and digital medicine candidates
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 一批临床转化候选入库
  - Why It Matters: 获取 workflow 和证据模式

- [ ] T033 Harvest JAMA / JAMA Network Open / NEJM / Lancet Digital Health candidates
  - Status: TODO
  - Priority: P1
  - Workstream: Clinical Signal
  - Parent: ROOT
  - Title: Harvest clinical high-impact candidates
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 一批高影响临床候选入库
  - Why It Matters: 提炼 endpoint 和真实临床需求

- [ ] T034 Extract endpoints and evidence patterns
  - Status: TODO
  - Priority: P1
  - Workstream: Clinical Signal
  - Parent: T031
  - Title: Extract endpoints, validation patterns, workflow constraints, reader studies, multicenter signals
  - Deliverable: `clinical_signal.csv`, `endpoint_registry.csv`, `evidence_patterns.csv`
  - Done When: 形成一版临床证据模式库
  - Why It Matters: 避免做 benchmark 漂亮但临床价值弱的题

### P1 Biomedical Literature Lake

### P1 Data / Challenge / Trial Map

- [ ] T039 Harvest Grand Challenge metadata
  - Status: TODO
  - Priority: P1
  - Workstream: Data Ecosystem
  - Parent: ROOT
  - Title: Harvest Grand Challenge metadata
  - Deliverable: `challenges_master.csv`
  - Done When: 一批 challenge 元数据入库
  - Why It Matters: active / ended / stale 任务地图

- [ ] T040 Split challenges into active / ended / stale
  - Status: TODO
  - Priority: P1
  - Workstream: Data Ecosystem
  - Parent: T039
  - Title: Separate challenge states
  - Deliverable: 更新 `challenges_master.csv`
  - Done When: 所有 challenge 状态分类明确
  - Why It Matters: 支持墓地与复活分析

- [ ] T041 Harvest TCIA collections
  - Status: TODO
  - Priority: P1
  - Workstream: Data Ecosystem
  - Parent: ROOT
  - Title: Harvest TCIA collections relevant to medical imaging AI
  - Deliverable: `datasets_master.csv`
  - Done When: 一批 TCIA metadata 入库
  - Why It Matters: 医学影像公开数据关键入口

- [ ] T042 Harvest PhysioNet datasets
  - Status: TODO
  - Priority: P1
  - Workstream: Data Ecosystem
  - Parent: ROOT
  - Title: Harvest PhysioNet datasets relevant to imaging, multimodal medicine, and clinical AI
  - Deliverable: 更新 `datasets_master.csv`
  - Done When: 一批 PhysioNet dataset metadata 入库
  - Why It Matters: 多模态和临床数据入口

- [ ] T043 Harvest ClinicalTrials.gov entries
  - Status: TODO
  - Priority: P1
  - Workstream: Data Ecosystem
  - Parent: ROOT
  - Title: Harvest ClinicalTrials.gov entries relevant to AI, imaging, diagnostics, workflow, decision support
  - Deliverable: trial metadata / linking tables
  - Done When: 一批 trial metadata 可检索
  - Why It Matters: 从真实临床研究需求反推机会

- [ ] T044 Build first `datasets_master.csv`
  - Status: TODO
  - Priority: P1
  - Workstream: Data Ecosystem
  - Parent: T041
  - Title: Build datasets master table
  - Deliverable: `research_ops/03_datasets/datasets_master.csv`
  - Done When: 包含 modality、task、label granularity、license、access friction 等字段
  - Why It Matters: 数据地图比泛读 paper 更值钱

- [ ] T045 Build first `challenges_master.csv`
  - Status: TODO
  - Priority: P1
  - Workstream: Data Ecosystem
  - Parent: T039
  - Title: Build challenges master table
  - Deliverable: `research_ops/04_challenges/challenges_master.csv`
  - Done When: 可按 task/status/metric/dataset 检索
  - Why It Matters: 支持 benchmark 与墓地分析

### P1 Paper Master Assembly

- [ ] T046 Merge all harvested papers into first `papers_master.csv`
  - Status: TODO
  - Priority: P1
  - Workstream: Paper Master
  - Parent: ROOT
  - Title: Build unified paper master
  - Deliverable: `research_ops/02_papers/papers_master.csv`
  - Done When: 形成统一 paper 主表
  - Why It Matters: 所有 linking 与分析依赖它

- [ ] T047 Normalize task / modality / anatomy / disease tags
  - Status: TODO
  - Priority: P1
  - Workstream: Paper Master
  - Parent: T046
  - Title: Normalize domain tags
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 同义标签初步统一
  - Why It Matters: 支持横向分析

- [ ] T048 Normalize method tags
  - Status: TODO
  - Priority: P1
  - Workstream: Paper Master
  - Parent: T046
  - Title: Normalize method tags
  - Deliverable: 更新 `papers_master.csv`
  - Done When: foundation / multimodal / agent / SSL / uncertainty 标签统一
  - Why It Matters: 支持趋势统计与迁移搜索

- [ ] T049 Link papers to datasets and challenges
  - Status: TODO
  - Priority: P1
  - Workstream: Linking
  - Parent: T046
  - Title: Link papers to datasets / challenges where possible
  - Deliverable: 更新 paper 表和 linking 表
  - Done When: 至少一批论文已连接数据和 challenge
  - Why It Matters: 防止论文脱离可执行资源

### P2 Benchmark / Repro / Failure

- [ ] T050 Select top 50 high-value papers for audit
  - Status: TODO
  - Priority: P2
  - Workstream: Repro Audit
  - Parent: T046
  - Title: Select 50 papers for deeper audit
  - Deliverable: 审计对象清单
  - Done When: 高价值审计列表完成
  - Why It Matters: 节约精读成本

- [ ] T051 Build `repo_registry.csv`
  - Status: TODO
  - Priority: P2
  - Workstream: Repro Audit
  - Parent: T050
  - Title: Register high-value repos
  - Deliverable: `research_ops/06_repro/repo_registry.csv`
  - Done When: 高价值论文相关 repo 已登记
  - Why It Matters: 复现入口

- [ ] T052 Mine GitHub issues for reproducibility blockers
  - Status: TODO
  - Priority: P2
  - Workstream: Repro Audit
  - Parent: T051
  - Title: Mine issue-level blockers
  - Deliverable: `research_ops/06_repro/issue_mining.csv`
  - Done When: 一批复现阻塞点已提取
  - Why It Matters: 失败点常藏在 issue 里

- [ ] T053 Build first `repro_audit.csv`
  - Status: TODO
  - Priority: P2
  - Workstream: Repro Audit
  - Parent: T052
  - Title: Build repro audit table
  - Deliverable: `research_ops/06_repro/repro_audit.csv`
  - Done When: 高价值论文具有 green/yellow/red 标签
  - Why It Matters: 确定值得投入的工作

- [ ] T054 Extract benchmark tables for one major subfield
  - Status: TODO
  - Priority: P2
  - Workstream: Benchmark Forensics
  - Parent: T050
  - Title: Extract benchmark tables
  - Deliverable: `research_ops/05_benchmarks/benchmark_tables.csv`
  - Done When: 至少一条主线 benchmark 可横向对比
  - Why It Matters: 找出真正可比与不可比结果

- [ ] T055 Build first `split_audit.csv`
  - Status: TODO
  - Priority: P2
  - Workstream: Benchmark Forensics
  - Parent: T054
  - Title: Audit split / metric drift
  - Deliverable: `research_ops/05_benchmarks/split_audit.csv`
  - Done When: 一批 benchmark drift 已记录
  - Why It Matters: 防止被虚假 SOTA 误导

- [ ] T056 Extract limitations and build failure database
  - Status: TODO
  - Priority: P2
  - Workstream: Failure Mining
  - Parent: T050
  - Title: Extract limitations from papers, supplements, and issues
  - Deliverable: `research_ops/07_failures/failure_modes.csv`
  - Done When: 至少一版 failure 数据库形成
  - Why It Matters: 好 idea 更多来自失败而非成功摘要

### P2 Task Graveyard / Resurrection

- [ ] T057 Identify ended challenges and stale tasks
  - Status: TODO
  - Priority: P2
  - Workstream: Task Graveyard
  - Parent: T040
  - Title: Identify dead/stale tasks
  - Deliverable: `research_ops/08_tasks/task_graveyard.csv`
  - Done When: 一批死掉或冷却任务已分类
  - Why It Matters: 从旧任务中挖复活机会

- [ ] T058 Score resurrection potential
  - Status: TODO
  - Priority: P2
  - Workstream: Task Graveyard
  - Parent: T057
  - Title: Build resurrection candidates table
  - Deliverable: `research_ops/08_tasks/resurrection_candidates.csv`
  - Done When: 一批任务具有复活评分
  - Why It Matters: foundation models / agents 可能重启旧方向

### P1/P2 Case Report Lake + Phenopacket Factory

- [ ] T114 Add `case_report_cache_lifecycle.md` cross-link to `cache_cleanup_workflow.md`
  - Status: TODO
  - Priority: P1
  - Workstream: Case Lake
  - Parent: T059
  - Title: Align case pipeline wording with global cache policy
  - Deliverable: memo + one-line cross-ref in `cache_cleanup_workflow.md`
  - Done When: T065 执行时不会与全局 manifest 规则冲突
  - Why It Matters: Repair — 单一生命周期故事

- [ ] T115 Validate case report CSV headers against Phenopacket minimal fields checklist
  - Status: TODO
  - Priority: P1
  - Workstream: Case Lake
  - Parent: T060
  - Title: Map columns to Phenopacket core concepts
  - Deliverable: 表格或 `schema_notes.md` 增补
  - Done When: 每个 phenopacket 列有定义来源
  - Why It Matters: Validate — 避免后期返工

- [ ] T116 Draft Europe PMC case-report query templates for T062 harvest
  - Status: TODO
  - Priority: P1
  - Workstream: Case Lake
  - Parent: T062
  - Title: OA case report search templates (PMC OA / Europe PMC)
  - Deliverable: `query_registry.csv` 新增行或 sidecar memo
  - Done When: 至少 5 条可执行查询模板
  - Why It Matters: Exploit — 降低首次抓取试错成本

- [ ] T062 Harvest first batch of open-access case reports
  - Status: TODO
  - Priority: P1
  - Workstream: Case Lake
  - Parent: T059
  - Title: Download first batch of OA case reports into cache
  - Deliverable: cache + manifest + updated `case_reports_master.csv`
  - Done When: 首批可合法下载 case reports 已抓取并登记
  - Why It Matters: 启动病例湖

- [ ] T063 Extract first 200 structured case records
  - Status: TODO
  - Priority: P1
  - Workstream: Case Lake
  - Parent: T062
  - Title: Extract 200 structured case records
  - Deliverable: 更新 `case_reports_master.csv`
  - Done When: 至少 200 条病例结构化完成
  - Why It Matters: 建立初始病例湖

- [ ] T064 Extract first 200 phenopacket-like records
  - Status: TODO
  - Priority: P1
  - Workstream: Case Lake
  - Parent: T063
  - Title: Convert 200 cases into phenopacket-like records
  - Deliverable: 更新 `phenopackets.csv`
  - Done When: 至少 200 条记录可检索
  - Why It Matters: rare disease retrieval 和 clustering 基础

- [ ] T065 Define case report download-parse-delete pipeline
  - Status: TODO
  - Priority: P1
  - Workstream: Case Lake
  - Parent: T062
  - Title: Specify how to download, parse, extract, manifest, and optionally delete raw case report files
  - Deliverable: `case_report_cache_lifecycle.md`
  - Done When: 流水线规则明确
  - Why It Matters: 大规模病例抓取必须可控

- [ ] T066 Build first `case_report_figures.csv`
  - Status: TODO
  - Priority: P2
  - Workstream: Case Lake
  - Parent: T061
  - Title: Build case report figure table
  - Deliverable: `research_ops/16_case_reports/case_report_figures.csv`
  - Done When: 一批图像/图注记录完成
  - Why It Matters: 支持 text+figure clue mining

### P2 Rare Disease / Case Intelligence

- [ ] T067 Build rare disease retrieval mini-benchmark
  - Status: TODO
  - Priority: P2
  - Workstream: Rare Disease
  - Parent: T064
  - Title: Build rare disease retrieval mini-benchmark from case reports
  - Deliverable: benchmark seed + memo
  - Done When: 一个可执行 retrieval benchmark 形成
  - Why It Matters: scaling 对长尾病例帮助最大

- [ ] T068 Build atypical presentation clustering memo
  - Status: TODO
  - Priority: P2
  - Workstream: Rare Disease
  - Parent: T063
  - Title: Analyze atypical presentation clustering opportunities
  - Deliverable: memo
  - Done When: 总结一批 atypical presentation 模式
  - Why It Matters: 长尾病例依赖大规模病例语料

- [ ] T069 Build differential diagnosis seed benchmark
  - Status: TODO
  - Priority: P2
  - Workstream: Rare Disease
  - Parent: T064
  - Title: Build differential diagnosis seed benchmark
  - Deliverable: benchmark seed file
  - Done When: 一个差异诊断种子基准形成
  - Why It Matters: 连接病例湖与可评测任务

- [ ] T070 Build negative-finding extraction checklist
  - Status: TODO
  - Priority: P2
  - Workstream: Rare Disease
  - Parent: T064
  - Title: Build checklist for extracting diagnostically important negative findings
  - Deliverable: checklist
  - Done When: 形成标准化抽取规范
  - Why It Matters: rare disease 和鉴别诊断中阴性特征很关键

### P1/P2 Clinical Pull / Scaling Fit

### P2 Trend Linking / Anti-Hype / Opportunities

- [ ] T076 Link frontier trends to historical bottlenecks
  - Status: TODO
  - Priority: P2
  - Workstream: Trend Linking
  - Parent: T014
  - Title: Connect frontier trends to old failures, stale tasks, and old literature bottlenecks
  - Deliverable: `research_ops/19_linking/trend_to_problem_links.csv`
  - Done When: 一批 trend -> old bottleneck 链接完成
  - Why It Matters: 真机会来自新能力 + 老痛点的交叉

- [ ] T077 Build `anti_hype_checks.csv`
  - Status: TODO
  - Priority: P2
  - Workstream: Trend Linking
  - Parent: T076
  - Title: Build anti-hype checks for hot trends
  - Deliverable: `research_ops/20_hypotheses/anti_hype_checks.csv`
  - Done When: 对高热 trend 形成“解决了什么 / 没解决什么”检查表
  - Why It Matters: 防止被 buzzword 误导

- [ ] T078 Build `scaling_opportunities.csv`
  - Status: TODO
  - Priority: P2
  - Workstream: Trend Linking
  - Parent: T074
  - Title: Build scaling opportunities table
  - Deliverable: `research_ops/17_scaling/scaling_opportunities.csv`
  - Done When: 形成一批高价值 research opportunities
  - Why It Matters: 将趋势、临床痛点、数据基础变成行动项

### P2 Agent Self-Improvement Harness

- [ ] T079 Define stable skill card format
  - Status: TODO
  - Priority: P2
  - Workstream: Agent Self-Improvement
  - Parent: T018
  - Title: Define reusable skill template
  - Deliverable: skill template memo
  - Done When: skill card 含 name、io、scope、failure modes、validation
  - Why It Matters: Agent 增长的是技能资产，不是上下文长度

- [ ] T080 Create first 10 skill cards
  - Status: TODO
  - Priority: P2
  - Workstream: Agent Self-Improvement
  - Parent: T079
  - Title: Create first 10 `skill_cards`
  - Deliverable: `research_ops/15_agentic/skill_cards/*.md`
  - Done When: 至少 10 个技能卡片完成
  - Why It Matters: 自进化需要显式资产

- [ ] T081 Create `promotion_tests.csv`
  - Status: TODO
  - Priority: P2
  - Workstream: Agent Self-Improvement
  - Parent: T079
  - Title: Define validation tests for skills
  - Deliverable: `research_ops/15_agentic/promotion_tests.csv`
  - Done When: 关键技能均有测试
  - Why It Matters: 没有验证就不是可审计升级

- [ ] T082 Build `benchmark_tasks.csv`
  - Status: TODO
  - Priority: P2
  - Workstream: Agent Self-Improvement
  - Parent: T081
  - Title: Build benchmark task table
  - Deliverable: `research_ops/15_agentic/benchmark_tasks.csv`
  - Done When: 一批稳定 benchmark tasks 可用于验证技能
  - Why It Matters: 让改进可比较

- [ ] T083 Start `reflection_log.csv`
  - Status: TODO
  - Priority: P2
  - Workstream: Agent Self-Improvement
  - Parent: T079
  - Title: Start reflection log
  - Deliverable: `research_ops/15_agentic/reflection_log.csv`
  - Done When: 可记录失败、修正、升级原因
  - Why It Matters: 支持错误回放和技能提炼

### P2 Hypothesis / Idea / Reviewer

- [ ] T084 Build `hypothesis_market.csv`
  - Status: TODO
  - Priority: P2
  - Workstream: Hypothesis
  - Parent: T078
  - Title: Build hypothesis market
  - Deliverable: `research_ops/20_hypotheses/hypothesis_market.csv`
  - Done When: 一批 hypothesis 已结构化登记
  - Why It Matters: 把发现机会变成候选市场

- [ ] T085 Build `cheap_tests.csv`
  - Status: TODO
  - Priority: P2
  - Workstream: Hypothesis
  - Parent: T084
  - Title: Build cheap tests table
  - Deliverable: `research_ops/20_hypotheses/cheap_tests.csv`
  - Done When: 高优 hypothesis 具有低成本验证路径
  - Why It Matters: 降低从想法到实验的距离

- [ ] T086 Build `evidence_gaps.csv`
  - Status: TODO
  - Priority: P2
  - Workstream: Hypothesis
  - Parent: T084
  - Title: Build evidence gap table
  - Deliverable: `research_ops/20_hypotheses/evidence_gaps.csv`
  - Done When: 每条 hypothesis 有证据不足说明
  - Why It Matters: 防止自我说服

- [ ] T087 Build first `idea_queue.csv`
  - Status: TODO
  - Priority: P2
  - Workstream: Hypothesis
  - Parent: T084
  - Title: Build idea queue
  - Deliverable: `research_ops/11_ideas/idea_queue.csv`
  - Done When: 一批 idea 已可排序
  - Why It Matters: 形成行动队列

- [ ] T088 Build `reviewer_attacks.csv`
  - Status: TODO
  - Priority: P2
  - Workstream: Hypothesis
  - Parent: T087
  - Title: Build reviewer attack list
  - Deliverable: `research_ops/12_reviewer/reviewer_attacks.csv`
  - Done When: top ideas 有 attack list 与 reviewer risk
  - Why It Matters: 让想法更抗打

### P3 Specialized Explorations

- [ ] T089 Build off-label drug response mining mini-benchmark
  - Status: TODO
  - Priority: P3
  - Workstream: Specialized Exploration
  - Parent: T062
  - Title: Build off-label response benchmark seed
  - Deliverable: benchmark seed
  - Done When: 一个可执行小 benchmark 形成
  - Why It Matters: case reports 与 repurposing 的直接连接点

- [ ] T090 Build adverse event mining mini-benchmark
  - Status: TODO
  - Priority: P3
  - Workstream: Specialized Exploration
  - Parent: T062
  - Title: Build adverse event mining benchmark seed
  - Deliverable: benchmark seed
  - Done When: 一个 AE 小基准形成
  - Why It Matters: 低频高价值临床信号

- [ ] T091 Build oncology MDT support memo
  - Status: TODO
  - Priority: P3
  - Workstream: Specialized Exploration
  - Parent: T075
  - Title: Build oncology MDT support opportunity memo
  - Deliverable: memo
  - Done When: 描述问题、数据、scaling fit、cheap test
  - Why It Matters: 文献和病例负担极高，适合 scaling

- [ ] T092 Build evidence-synthesis opportunity memo
  - Status: TODO
  - Priority: P3
  - Workstream: Specialized Exploration
  - Parent: T075
  - Title: Build evidence synthesis opportunity memo
  - Deliverable: memo
  - Done When: 一条证据综合机会说明形成
  - Why It Matters: AI 最适合信息压缩工作

- [ ] T093 Build trial-matching opportunity memo
  - Status: TODO
  - Priority: P3
  - Workstream: Specialized Exploration
  - Parent: T043
  - Title: Build trial matching opportunity memo
  - Deliverable: memo
  - Done When: 形成 trial matching 的 problem/data/risk 分析
  - Why It Matters: 典型 retrieval + linking + scaling 问题

- [ ] T094 Build rare-disease support opportunity memo
  - Status: TODO
  - Priority: P3
  - Workstream: Specialized Exploration
  - Parent: T067
  - Title: Build rare disease support opportunity memo
  - Deliverable: memo
  - Done When: rare disease scaling opportunity 分析形成
  - Why It Matters: 长尾问题非常适合大语料与病例库方法

### P1/P2 File Download / Cleanup Special Tasks

- [ ] T098 Define curated keep-set policy
  - Status: TODO
  - Priority: P2
  - Workstream: Download Infrastructure
  - Parent: T006C
  - Title: Define a small canonical keep-set of high-value full-text/PDF files
  - Deliverable: `research_ops/manifests/keep_set_manifest.csv`
  - Done When: 少量高价值原文样本的保留标准明确
  - Why It Matters: 并不是所有原始文件都该删

- [ ] T099 Define parse-failure retry queue
  - Status: TODO
  - Priority: P2
  - Workstream: Download Infrastructure
  - Parent: T006B
  - Title: Define queue for failed downloads and failed parses
  - Deliverable: `research_ops/manifests/retry_queue.csv`
  - Done When: 所有失败项可重试、可追踪
  - Why It Matters: 批处理不可能一次全成功

- [ ] T100 Define storage budget and cleanup triggers
  - Status: TODO
  - Priority: P2
  - Workstream: Download Infrastructure
  - Parent: T006D
  - Title: Define storage budget thresholds and cleanup triggers for cache directories
  - Deliverable: policy or memo
  - Done When: 缓存超过阈值时有明确清理策略
  - Why It Matters: 防止仓库失控膨胀

### P2 Maintenance / Continuation

- [ ] T101 Reprioritize backlog by information gain
  - Status: TODO
  - Priority: P2
  - Workstream: Maintenance
  - Parent: ROOT
  - Title: Reprioritize backlog based on information gain
  - Deliverable: `STATUS.md` update
  - Done When: backlog 排序与最新发现一致
  - Why It Matters: 防止任务树僵化

- [ ] T102 Add 10 follow-up tasks from frontier discoveries
  - Status: TODO
  - Priority: P2
  - Workstream: Maintenance
  - Parent: T014
  - Title: Add follow-up tasks from trend discoveries
  - Deliverable: TODO expansion
  - Done When: 新趋势进入执行层
  - Why It Matters: 让趋势变成行动

- [ ] T103 Add 10 follow-up tasks from case mining
  - Status: TODO
  - Priority: P2
  - Workstream: Maintenance
  - Parent: T062
  - Title: Add follow-up tasks from case report mining
  - Deliverable: TODO expansion
  - Done When: 病例新线索进入任务队列
  - Why It Matters: 防止病例湖成为死仓库

- [ ] T104 Add 10 follow-up tasks from skill failures
  - Status: TODO
  - Priority: P2
  - Workstream: Maintenance
  - Parent: T083
  - Title: Add follow-up tasks from skill failures and reflection log
  - Deliverable: TODO expansion
  - Done When: skill failure 变成改进任务
  - Why It Matters: 支持可审计自进化

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
