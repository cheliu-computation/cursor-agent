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

- [ ] T006 Build broad source registry
  - Status: DOING
  - Priority: P0
  - Workstream: Source Atlas
  - Parent: ROOT
  - Title: Build broad `source_registry.csv`
  - Deliverable: `research_ops/01_sources/source_registry.csv`
  - Done When: 至少纳入 40 个跨层来源，并包含 source type、layer、role、priority、signal/noise、license notes
  - Why It Matters: 所有抓取、筛选、下载、解析、链接流程都依赖来源地图

## 3. READY / TODO

### P0 Setup / Governance

- [ ] T000 Initialize `research_ops/` directory and subfolders
  - Status: TODO
  - Priority: P0
  - Workstream: Setup
  - Parent: ROOT
  - Title: Initialize repository research system
  - Deliverable: 完整目录结构
  - Done When: 所有核心目录创建完成
  - Why It Matters: 所有资产都依赖稳定目录结构

- [ ] T001 Create all core CSV headers
  - Status: TODO
  - Priority: P0
  - Workstream: Setup
  - Parent: ROOT
  - Title: Create all master CSV headers
  - Deliverable: 所有核心 CSV 空表头
  - Done When: 全部 CSV 已可写入
  - Why It Matters: 统一 schema，避免后期混乱

- [ ] T002 Create meta control files
  - Status: TODO
  - Priority: P0
  - Workstream: Setup
  - Parent: ROOT
  - Title: Create `STATUS.md`, `RUN_LOG.md`, `DECISIONS.md`, `SOURCE_POLICY.md`, `SCORING_POLICY.md`, `LICENSE_POLICY.md`
  - Deliverable: 全部元文件
  - Done When: 文件存在且含初始内容
  - Why It Matters: 确保可恢复、可追踪、可审计

- [ ] T003 Write initial TODO system
  - Status: TODO
  - Priority: P0
  - Workstream: Setup
  - Parent: ROOT
  - Title: Write long-horizon task system into `TODO.md`
  - Deliverable: 当前文件
  - Done When: 初始 backlog 完整可执行
  - Why It Matters: 避免 Agent 漫游式工作

- [ ] T004 Create scoring policy
  - Status: TODO
  - Priority: P0
  - Workstream: Governance
  - Parent: ROOT
  - Title: Define scoring criteria for papers, datasets, trends, ideas, and scaling-fit problems
  - Deliverable: `research_ops/00_meta/SCORING_POLICY.md`
  - Done When: 各类对象均有统一评分维度
  - Why It Matters: 让筛选与优先级排序可复用

- [ ] T005 Create license and retention policy
  - Status: TODO
  - Priority: P0
  - Workstream: Governance
  - Parent: ROOT
  - Title: Define file retention, cache cleanup, and license-aware download policy
  - Deliverable: `research_ops/00_meta/LICENSE_POLICY.md`
  - Done When: 明确保留、删除、重下、gitignore、版权策略
  - Why It Matters: 支持远端下载与读后删除流程

### P0 Download / Cache / Cleanup Infrastructure

- [ ] T006A Define repository-local download workspace layout
  - Status: TODO
  - Priority: P0
  - Workstream: Download Infrastructure
  - Parent: T005
  - Title: Define `cache/`, `manifests/`, and `parsed/` layout
  - Deliverable: 目录规范文档
  - Done When: 至少定义 `cache/metadata`, `cache/fulltext`, `cache/pdfs`, `cache/tmp`, `manifests`, `parsed`
  - Why It Matters: 大规模下载需要稳定缓存拓扑

- [ ] T006B Create download and parse manifest schemas
  - Status: TODO
  - Priority: P0
  - Workstream: Download Infrastructure
  - Parent: T005
  - Title: Define `download_manifest.csv` and `parse_manifest.csv`
  - Deliverable: 两个 manifest schema
  - Done When: 至少包含 source URL、retrieval time、local path、hash、mime type、license、parse status、delete eligibility
  - Why It Matters: 支持读后删除但不丢 provenance

- [ ] T006C Define file retention rules
  - Status: TODO
  - Priority: P0
  - Workstream: Download Infrastructure
  - Parent: T005
  - Title: Define retention policy for raw PDF/TXT/XML/HTML files
  - Deliverable: `LICENSE_POLICY.md`
  - Done When: 明确哪些长期保留、哪些解析后删除、哪些只保留 metadata
  - Why It Matters: 控制仓库体积并降低合规风险

- [ ] T006D Define cleanup-after-parse workflow
  - Status: TODO
  - Priority: P0
  - Workstream: Download Infrastructure
  - Parent: T005
  - Title: Define download -> parse -> extract -> manifest -> delete workflow
  - Deliverable: `cache_cleanup_workflow.md`
  - Done When: 形成完整缓存生命周期规范
  - Why It Matters: 支持海量抓取与仓库控体积

- [ ] T006E Define redownloadable artifacts policy
  - Status: TODO
  - Priority: P0
  - Workstream: Download Infrastructure
  - Parent: T005
  - Title: Mark which files are safely redownloadable and deletable
  - Deliverable: manifest 字段与规则
  - Done When: 可区分“可删可重建”和“建议保留”的文件
  - Why It Matters: 降低存储负担

- [ ] T006F Define parser output survival rules
  - Status: TODO
  - Priority: P0
  - Workstream: Download Infrastructure
  - Parent: T005
  - Title: Specify which extracted outputs must survive after raw file deletion
  - Deliverable: `LICENSE_POLICY.md`
  - Done When: 明确保留 metadata、checksums、extraction outputs、note path、provenance
  - Why It Matters: 删原文后仍能继续研究

- [ ] T006G Define repository-safe download policy
  - Status: TODO
  - Priority: P0
  - Workstream: Download Infrastructure
  - Parent: T005
  - Title: Define which downloaded files are gitignored by default
  - Deliverable: gitignore policy memo
  - Done When: 原始缓存默认不纳入版本控制的策略明确
  - Why It Matters: GitHub repo 运行必须防止仓库膨胀

### P1 Source Atlas

- [ ] T007 Build broad `venue_registry.csv`
  - Status: TODO
  - Priority: P1
  - Workstream: Source Atlas
  - Parent: ROOT
  - Title: Build broad venue registry
  - Deliverable: `research_ops/01_sources/venue_registry.csv`
  - Done When: 覆盖领域核心、方法前沿、临床高影响、agentic/frontier 四类 venue
  - Why It Matters: venue 是信号筛选骨架

- [ ] T008 Register domain-core venues
  - Status: TODO
  - Priority: P1
  - Workstream: Source Atlas
  - Parent: T007
  - Title: Register MICCAI / MIDL / IPMI / ISBI / MedIA / TMI / Radiology / Radiology: AI
  - Deliverable: 更新 `venue_registry.csv`
  - Done When: 领域主战场 venue 完整登记
  - Why It Matters: 医学 AI 主线图谱入口

- [ ] T009 Register general ML/CV frontier venues
  - Status: TODO
  - Priority: P1
  - Workstream: Source Atlas
  - Parent: T007
  - Title: Register NeurIPS / ICML / ICLR / CVPR / ICCV / ECCV
  - Deliverable: 更新 `venue_registry.csv`
  - Done When: 方法前沿 venue 完整登记
  - Why It Matters: 方法迁移主入口

- [ ] T010 Register high-impact science and clinical venues
  - Status: TODO
  - Priority: P1
  - Workstream: Source Atlas
  - Parent: T007
  - Title: Register Nature / Science / Cell / Nature Medicine / NBE / npj / JAMA / NEJM / Lancet Digital Health
  - Deliverable: 更新 `venue_registry.csv`
  - Done When: 临床和高影响科学 venue 登记完成
  - Why It Matters: 问题重要性与证据标准来源

- [ ] T011 Register data, challenge, and infrastructure sources
  - Status: TODO
  - Priority: P1
  - Workstream: Source Atlas
  - Parent: T006
  - Title: Register Grand Challenge, TCIA, PhysioNet, ClinicalTrials.gov, Europe PMC, PMC OA, PubTator, SemMedDB, OpenAlex
  - Deliverable: 更新 `source_registry.csv`
  - Done When: 数据与基础设施来源登记完成
  - Why It Matters: 文献湖与数据湖底盘

- [ ] T012 Create first `query_registry.csv`
  - Status: TODO
  - Priority: P1
  - Workstream: Query Design
  - Parent: ROOT
  - Title: Create reusable query registry
  - Deliverable: `research_ops/01_sources/query_registry.csv`
  - Done When: 包含任务词、模态词、方法词、临床词、frontier 词族
  - Why It Matters: 可复用搜索体系比一次性搜索更重要

### P1 Frontier / Agentic / Scaling Radar

- [ ] T013 Build `frontier_queries.csv`
  - Status: TODO
  - Priority: P1
  - Workstream: Frontier Radar
  - Parent: T012
  - Title: Build reusable frontier query families
  - Deliverable: `research_ops/14_frontier/frontier_queries.csv`
  - Done When: 至少 30 条 agent/scaling/scientific-discovery 查询模板
  - Why It Matters: 支持趋势长期跟踪

- [ ] T014 Harvest frontier papers on scientific discovery agents
  - Status: TODO
  - Priority: P1
  - Workstream: Frontier Radar
  - Parent: T013
  - Title: Harvest AI scientist / agent laboratory / scientific discovery agent papers
  - Deliverable: `frontier_papers.csv`
  - Done When: 一批 frontier papers 已入库且含 tool_use、memory、自进化标记
  - Why It Matters: 捕捉科学发现方向前沿

- [ ] T015 Harvest frontier papers on biomedical and clinical agents
  - Status: TODO
  - Priority: P1
  - Workstream: Frontier Radar
  - Parent: T013
  - Title: Harvest biomedical / clinical agent papers
  - Deliverable: 更新 `frontier_papers.csv`
  - Done When: 一批 biomedical agent 系统入库
  - Why It Matters: 识别真实医学场景中的 agent 应用

- [ ] T016 Build first `agent_systems.csv`
  - Status: TODO
  - Priority: P1
  - Workstream: Agentic Systems
  - Parent: T014
  - Title: Build agent systems registry
  - Deliverable: `research_ops/15_agentic/agent_systems.csv`
  - Done When: 至少 15 个系统统一建表
  - Why It Matters: 让 agent 设计空间可比较

- [ ] T017 Build first `self_evolution_patterns.csv`
  - Status: TODO
  - Priority: P1
  - Workstream: Agentic Systems
  - Parent: T016
  - Title: Build self-evolution pattern table
  - Deliverable: `research_ops/15_agentic/self_evolution_patterns.csv`
  - Done When: 至少总结 10 种自进化机制及其验证方式
  - Why It Matters: 区分真升级与 prompt 炒作

- [ ] T018 Write memo on real agent self-evolution
  - Status: TODO
  - Priority: P1
  - Workstream: Agentic Systems
  - Parent: T017
  - Title: Write `what_counts_as_real_agent_self_evolution.md`
  - Deliverable: 备忘录
  - Done When: 明确真正可审计自进化边界
  - Why It Matters: 作为整个系统的判断准则

### P1 Domain-Core Harvest

- [ ] T019 Harvest MICCAI metadata
  - Status: TODO
  - Priority: P1
  - Workstream: Domain Core
  - Parent: ROOT
  - Title: Harvest MICCAI metadata
  - Deliverable: `papers_master.csv`
  - Done When: 最近若干年核心 metadata 入库
  - Why It Matters: 医学影像主战场

- [ ] T020 Harvest MIDL metadata
  - Status: TODO
  - Priority: P1
  - Workstream: Domain Core
  - Parent: ROOT
  - Title: Harvest MIDL metadata
  - Deliverable: 更新 `papers_master.csv`
  - Done When: 一批 MIDL metadata 入库
  - Why It Matters: 医疗 ML 方法主线入口

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

- [ ] T035 Register literature infrastructure sources
  - Status: TODO
  - Priority: P1
  - Workstream: Literature Lake
  - Parent: T011
  - Title: Register Europe PMC, PMC OA, PubTator, SemMedDB, OpenAlex, PubMed, ClinicalTrials.gov
  - Deliverable: 更新 `source_registry.csv`
  - Done When: 基础设施来源具有 layer、role、license、bulkability、parseability 标记
  - Why It Matters: 支撑 Web-scale 文献湖

- [ ] T036 Build parseability and reuse table
  - Status: TODO
  - Priority: P1
  - Workstream: Literature Lake
  - Parent: T035
  - Title: Build literature parseability / reuse table
  - Deliverable: 备忘录
  - Done When: 明确哪些来源可抓 metadata、全文、bulk、text-mined annotations
  - Why It Matters: 直接决定下载策略

- [ ] T037 Define paper-trial links schema
  - Status: TODO
  - Priority: P1
  - Workstream: Literature Lake
  - Parent: T035
  - Title: Define schema for `paper_trial_links.csv`
  - Deliverable: `research_ops/19_linking/paper_trial_links.csv`
  - Done When: 可表达 paper <-> trial 关系
  - Why It Matters: 连接研究与临床试验

- [ ] T038 Define paper-guideline links schema
  - Status: TODO
  - Priority: P1
  - Workstream: Literature Lake
  - Parent: T035
  - Title: Define schema for `paper_guideline_links.csv`
  - Deliverable: `research_ops/19_linking/paper_guideline_links.csv`
  - Done When: 可表达 paper <-> guideline 关系
  - Why It Matters: 连接研究与临床规范

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

- [ ] T059 Define schema for `case_reports_master.csv`
  - Status: TODO
  - Priority: P1
  - Workstream: Case Lake
  - Parent: ROOT
  - Title: Define case report master schema
  - Deliverable: `research_ops/16_case_reports/case_reports_master.csv`
  - Done When: 包含 disease、features、negative findings、outcome、figure existence、license 等字段
  - Why It Matters: case report 是长尾病例与 hypothesis 的弱证据高价值源

- [ ] T060 Define schema for `phenopackets.csv`
  - Status: TODO
  - Priority: P1
  - Workstream: Case Lake
  - Parent: T059
  - Title: Define phenopacket-like schema
  - Deliverable: `research_ops/16_case_reports/phenopackets.csv`
  - Done When: 可表达 age、sex、phenotypes、negated phenotypes、timeline、tests、treatment、response、outcome
  - Why It Matters: 将病例文本转为可计算表示

- [ ] T061 Define schema for `case_report_figures.csv`
  - Status: TODO
  - Priority: P1
  - Workstream: Case Lake
  - Parent: T059
  - Title: Define case report figure schema
  - Deliverable: `research_ops/16_case_reports/case_report_figures.csv`
  - Done When: 可记录 caption、modality hint、diagnostic value、weak supervision value、license notes
  - Why It Matters: 插图虽弱，但可作为 multimodal clue

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

- [ ] T071 Build first `pain_points.csv`
  - Status: TODO
  - Priority: P1
  - Workstream: Scaling Fit
  - Parent: ROOT
  - Title: Build clinical pain points table
  - Deliverable: `research_ops/18_clinical_pull/pain_points.csv`
  - Done When: 至少整理 20 个临床信息负担或 workflow bottleneck
  - Why It Matters: 从临床需求倒推 AI 机会

- [ ] T072 Build `workflow_bottlenecks.csv`
  - Status: TODO
  - Priority: P1
  - Workstream: Scaling Fit
  - Parent: T071
  - Title: Build workflow bottlenecks table
  - Deliverable: `research_ops/18_clinical_pull/workflow_bottlenecks.csv`
  - Done When: 至少提炼 20 个 bottlenecks
  - Why It Matters: 真价值往往在流程层

- [ ] T073 Build `unmet_needs.csv`
  - Status: TODO
  - Priority: P1
  - Workstream: Scaling Fit
  - Parent: T071
  - Title: Build unmet needs table
  - Deliverable: `research_ops/18_clinical_pull/unmet_needs.csv`
  - Done When: 至少整理 20 个 unmet needs
  - Why It Matters: 为临床优先级排序打底

- [ ] T074 Score top 20 clinical problems for scaling fit
  - Status: TODO
  - Priority: P1
  - Workstream: Scaling Fit
  - Parent: T071
  - Title: Score the top 20 clinical problems for scaling-fit
  - Deliverable: `research_ops/18_clinical_pull/scaling_fit_scores.csv`
  - Done When: 至少 20 个问题完成 why-scalable / data-source / risk 打分
  - Why It Matters: 找出最适合 web-scale + agent + retrieval 的问题

- [ ] T075 Build first `scalable_problem_map.csv`
  - Status: TODO
  - Priority: P1
  - Workstream: Scaling Fit
  - Parent: T074
  - Title: Build scalable problem map
  - Deliverable: `research_ops/17_scaling/scalable_problem_map.csv`
  - Done When: 形成 top scalable clinical problems 列表
  - Why It Matters: 后续 hypothesis 排序依据

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
  - Parent: T017
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

- [ ] T095 Define article download policy by content type
  - Status: TODO
  - Priority: P1
  - Workstream: Download Infrastructure
  - Parent: T005
  - Title: Define when to download metadata, abstract, XML, TXT, HTML, or PDF
  - Deliverable: `LICENSE_POLICY.md`
  - Done When: 明确不同内容类型的优先级和保留策略
  - Why It Matters: 避免无意义 PDF 堆积

- [ ] T096 Build article acquisition decision tree
  - Status: TODO
  - Priority: P1
  - Workstream: Download Infrastructure
  - Parent: T095
  - Title: Create a decision tree for article acquisition and deletion
  - Deliverable: `article_acquisition_decision_tree.md`
  - Done When: 能明确指导何时下载、何时解析、何时删除
  - Why It Matters: 远端 Agent 需要稳定执行规则

- [ ] T097 Define raw-file deletion checkpoints
  - Status: TODO
  - Priority: P1
  - Workstream: Download Infrastructure
  - Parent: T006D
  - Title: Define checkpoints after which raw files may be deleted
  - Deliverable: policy update
  - Done When: parse success、hash recorded、extract saved、note created 后可删的规则明确
  - Why It Matters: 读完即删需要明确闸门

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

- [ ] T105 Write first run summary
  - Status: TODO
  - Priority: P2
  - Workstream: Maintenance
  - Parent: ROOT
  - Title: Write `summary_001.md`
  - Deliverable: `research_ops/13_exports/run_summaries/summary_001.md`
  - Done When: 总结已完成资产、关键发现、下一步
  - Why It Matters: 方便人类接管和复核

- [ ] T106 Update next best action in `STATUS.md`
  - Status: TODO
  - Priority: P2
  - Workstream: Maintenance
  - Parent: ROOT
  - Title: Update `STATUS.md` with next best action
  - Deliverable: `STATUS.md`
  - Done When: 下一任务和原因明确写出
  - Why It Matters: 保证可中断可恢复

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

- [ ] None yet
  - Status: DONE
  - Priority: P4
  - Workstream: Placeholder
  - Parent: ROOT
  - Title: No completed tasks yet
  - Deliverable: N/A
  - Done When: N/A
  - Why It Matters: 占位

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
