# STATUS

副标题：Scalable Discovery Agent 运行状态

## Current Focus
- 当前阶段：Harvest + linking + case lake + hypothesis stack 已大幅推进
- 当前目标：补齐论文主表与 challenge 链接、完成 CVPR/Swin 全表 benchmark 抽取（T140）
- 当前任务 ID：T140
- 当前工作流：Benchmark Forensics
- 当前运行模式：API 批量抓取 + CSV 资产沉淀

## Current Task
- Title：Swin UNETR（`openalex:W4312428231`）全表 Dice 从全文/CVF 页抽取
- Deliverable：更新 `research_ops/05_benchmarks/benchmark_tables.csv`（替换 BT006 占位）
- Done When：Medical Decathlon / BTCV 任务级指标落表且注明 split
- Blocking Dependencies：需全文或官方 leaderboard 抓取权限（非仅 abstract）

## Completed In This Run（摘要）
- `papers_master.csv` 扩展至 **396** 行（MICCAI/MIDL/IPMI/ISBI/MedIA/TMI/Rad/NeurIPS/ICML/ICLR/CVPR/ICCV/ECCV/Nature/Science/Cell/转化刊/顶刊临床 AI 等批次）
- 数据生态：Grand Challenge、TCIA、PhysioNet、CT.gov；`datasets_master` 70 行；`challenges_master` 50 行；`trials_master` 30 行
- 病例湖：Europe PMC **200** OA case + manifest + `phenopackets` 占位行；罕见病 retrieval seed；阴性体征 checklist
- Repro：`repo_registry`、`issue_mining`、`repro_audit`；benchmark forensic 种子（C-CAM）
- Agent harness：`skill_template` + 10 skill cards + promotion_tests + benchmark_tasks + reflection_log
- Hypothesis：`hypothesis_market`、`cheap_tests`、`evidence_gaps`、`idea_queue`、`reviewer_attacks`
- Trend：`trend_to_problem_links`、`anti_hype_checks`、`scaling_opportunities`
- Maintenance：T102–T104 通过 **T141–T170** 任务块落地

## Key Findings So Far
- OpenAlex **venue-scoped** 抓取可快速铺量，但会议论文年份覆盖需按年 source 解析（CVPR 2022 示例）
- Europe PMC **cursor** 可稳定拉到百级 OA case；全字段 phenotyping 需 PubTator / 全文阶段
- GitHub URL 常出现在 **abstract_inverted_index**，不在顶层字段

## Current Assets
- 见 `research_ops/**`；核心计数：`wc -l research_ops/02_papers/papers_master.csv` → 397（含表头）

## Risks / Blockers
- 大量任务依赖 **标题/摘要启发式**，需 T133/T152 等升级为全文或人工 spot-check
- `paper_challenge_links` 中论文尚未全部并入 `papers_master`（T138）

## Next Best Task
- Task ID：**T140**
- Title：Swin UNETR 全表 benchmark 抽取
- Why Next：BT006 仍为 abstract 占位，影响横向可比性

## Immediate Follow-ups
- T138：challenge DOI 论文并入主表
- T123：`venue_type` 列
- T124：authors 回填

## Working Rules For This Run
- 原子任务；状态写入本目录；每轮结束同步 `SCALABLE_DISCOVERY_AGENT_TODO.md`

## Resume Instructions
1. 打开本文件与 `TODO.md`
2. 执行 **DOING**（T140）
3. `git pull` 后检查 CSV 行数与 manifest
