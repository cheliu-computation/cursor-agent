# STATUS

副标题：Scalable Discovery Agent 运行状态

## Current Focus
- 当前阶段：Domain-core harvest expansion
- 当前目标：净化 MICCAI 种子并并行扩展 MIDL / IPMI / ISBI 元数据
- 当前任务 ID：T020
- 当前工作流：Domain Core
- 当前运行模式：Metadata harvest + registry hygiene

## Current Task
- Title：Harvest MIDL metadata
- Deliverable：追加到 `research_ops/02_papers/papers_master.csv`
- Done When：一批 MIDL 论文元数据入库且带 `source_batch` 与 `openalex_id`
- Blocking Dependencies：无（OpenAlex API 可用）

## Completed In This Run
- Bootstrap：`research_ops/` 全树、政策、manifest schema、`.gitignore`
- Source / venue / query / frontier query 注册表
- 文献基础设施解析备忘录；链接表 schema 扩展
- 临床 pull 与 scaling problem map 初版
- Agentic：`agent_systems`、`self_evolution_patterns`、自进化判断备忘录
- MICCAI 种子 20 条（待 T120–T122 净化）；frontier 论文与系统登记

## Key Findings So Far
- OpenAlex 搜索种子会混入非目标 venue，需要 T120/T122 用官方书目或 host_venue 过滤
- `paper_trial_links` / `paper_guideline_links` 已具备可扩展列，适合后续半自动链接

## Current Assets
- 见 `research_ops/` 下 CSV 与 `00_meta/*.md`

## Risks / Blockers
- 会议论文官方元数据入口不统一，需逐会验证 API 或页面条款

## Next Best Task
- Task ID：T020
- Title：Harvest MIDL metadata
- Why Next：与 MICCAI 并列的影像 ML 主会，应尽早并入同一 `papers_master` spine

## Immediate Follow-ups
- T120：过滤 MICCAI 噪声
- T111：agent_systems ↔ papers_master ID 对齐
- T119：trial 链接试点

## Working Rules For This Run
- 原子任务；状态写入本目录；每任务更新 RUN_LOG 与 TODO

## Resume Instructions
1. 打开本文件与 `TODO.md`
2. 执行 `DOING` 任务
3. 检查 Deliverable 行数与 schema
4. 更新 DONE 与 follow-ups
