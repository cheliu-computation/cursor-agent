# STATUS

副标题：Scalable Discovery Agent 运行状态

## Current Focus
- 当前阶段：**三层阅读栈** — 摘要（已完成全库）→ OA 网页/PDF 缓存（试点完成）→ 规模化 HTML（进行中）
- 当前目标：把 **T203** 扩到数百条可解析全文缓存，并接 **T204** PDF 试点
- 当前任务 ID：**T203**
- 当前工作流：Literature Lake / full-text cache
- 当前运行模式：`download_manifest` 门禁 + `cache/fulltext`（gitignore）

## Current Task
- Title：**T203** — 按年（2026→…）批量拉取 `oa_url_cached` 的 HTML/PDF，写入 manifest，失败进 `retry_queue`
- Deliverable：更新 `download_manifest.csv`、`paper_reading_status.csv`
- Done When：**≥500** 行 `fulltext_html_status=ingested`（或等价 `pdf_cached`）或显式 `blocked/skipped_policy`
- Blocking Dependencies：站点反爬、超时 → 需退避与 T206 Unpaywall 补链

## Completed In This Run（摘要）
- **T200**：`paper_reading_status.csv`、`fulltext_read_pipeline.md`、`parsed/abstracts/.gitkeep`
- **T201**：OpenAlex **摘要** 全量 — **6401** 篇与 `papers_master` 一一对应；按年 JSONL（**gitignored**）
- **T201b**：补登记后新增的 **80** 篇
- **T202**：试点 **50** 次成功下载；manifest **+68**（两趟脚本：18+50）；`fulltext_html_status`：**ingested 68**、**error 73**（其余仍 `pending`）
- **TODO**：新增 **T200–T213** 全文栈任务；**DOING=T203**

## Key Findings So Far
- OpenAlex 对旧文献 **abstract 常缺失**（`abstract_status=missing` 正常）
- 约 **4497** 行带 `oa_url_cached`，但不少链接为 **403/反爬** — T203 需更长超时、重试与合规跳过
- 同一脚本第二次运行需 **跳过已 ingested**，避免覆盖 manifest 计数

## Current Assets
- `papers_master.csv`：**6401** 行
- `paper_reading_status.csv`：**6401** 行（与主表对齐）
- `scripts/ingest_openalex_abstracts.py`：按年/全量摘要
- `scripts/pilot_fetch_oa_html.py`：**T202** 试点

## Risks / Blockers
- 大规模 HTML 抓取：**ToS + 速率**；默认只处理 OpenAlex 给出的 `oa_url`
- `cache/**` 不入库；依赖 manifest 做审计

## Next Best Task
- **T203**（扩量）→ **T204**（20 PDF）→ **T207**（摘要 FTS 索引）

## Immediate Follow-ups
- **T212**：对明确非 OA 的行写 `skipped_policy`，减少无效请求
- **T206**：Unpaywall 礼貌补 `oa_url`

## Working Rules For This Run
- 每层：**manifest 先行**；删缓存前核对 `LICENSE_POLICY.md`

## Resume Instructions
1. `TODO.md` → **DOING T203**
2. 扩展 `pilot_fetch_oa_html.py` 或新脚本：按年循环 + `retry_queue`
3. `cp research_ops/00_meta/TODO.md SCALABLE_DISCOVERY_AGENT_TODO.md` → commit
