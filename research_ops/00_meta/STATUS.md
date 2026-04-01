# STATUS

副标题：Scalable Discovery Agent 运行状态

## Current Focus
- 当前阶段：**三层阅读栈** — 摘要（全库）→ Layer B 批量 OA 缓存（T203 首遍完成）→ **T204** PDF 试点 + 解析
- 当前目标：完成 **T204**（显式 `pdf_status` + 小批量校验），并行准备 T205/T207
- 当前任务 ID：**T204**
- 当前工作流：Literature Lake / full-text cache
- 当前运行模式：`download_manifest` 门禁 + `cache/{fulltext,pdfs}`（gitignore）

## Current Task
- Title：**T204** — 试点 **20** 条 OA PDF：`pdf_status` + manifest + SHA256 可复验（非 paywall）
- Deliverable：更新 `download_manifest.csv`、`paper_reading_status.csv` 的 `pdf_status` / `pdf_artifact`
- Done When：**20** 行 `pdf_status=ingested`（或等价策略）且 hash 记录在 manifest
- Blocking Dependencies：与 T203 已缓存的 `pdf_cached` 行对齐时需避免重复下载

## Completed In This Run（摘要）
- **T200**：`paper_reading_status.csv`、`fulltext_read_pipeline.md`、`parsed/abstracts/.gitkeep`
- **T201**：OpenAlex **摘要** 全量 — **6401** 篇与 `papers_master` 一一对应；按年 JSONL（**gitignored**）
- **T201b**：补登记后新增的 **80** 篇
- **T202**：试点 **50** 次成功下载；manifest **+68**（两趟脚本：18+50）；`fulltext_html_status`：**ingested 68**、**error 73**（其余仍 `pending`）
- **T203**：`scripts/batch_fetch_oa_html.py` — manifest **+1736**（DL09201–DL2004）；Layer B 状态 **ingested 482**、**pdf_cached 1322**、**error 892**、**pending 3705**（见 **D-006**）
- **TODO**：**DOING=T204**；新增 **T214–T216**（Layer B 长尾、retry_queue、缓存体量记录）

## Key Findings So Far
- OpenAlex 对旧文献 **abstract 常缺失**（`abstract_status=missing` 正常）
- 约 **4497** 行带 `oa_url_cached`；大量 OA 着陆页在 **Content-Type 上仍是 PDF** — 用 **`pdf_cached`** 记录（D-006），不等价于 HTML `ingested`
- 对 arXiv：`oa_url` 常为 `/pdf/…` — **`/abs/` 回退** + 请求头 **`Accept: text/html`** 可提高 HTML 命中
- 非 PDF 的待抓取 URL 耗尽后，仅靠重试 **error** 行难以再推高 `ingested` — **T214** 需新策略（PMC、Unpaywall、更长超时/合规 backoff）

## Current Assets
- `papers_master.csv`：**6401** 行
- `paper_reading_status.csv`：**6401** 行（与主表对齐）
- `scripts/ingest_openalex_abstracts.py`：按年/全量摘要
- `scripts/pilot_fetch_oa_html.py`：**T202** 试点
- `scripts/batch_fetch_oa_html.py`：**T203** 批量 Layer B（可选 `--skip-pdf-primary`、`--retry-errors`）

## Risks / Blockers
- 大规模 HTML 抓取：**ToS + 速率**；默认只处理 OpenAlex 给出的 `oa_url`
- `cache/**` 不入库；依赖 manifest 做审计

## Next Best Task
- **T204**（20 PDF + `pdf_status`）→ **T207**（摘要 FTS）→ **T214**（Layer B 长尾）

## Immediate Follow-ups
- **T212**：对明确非 OA 的行写 `skipped_policy`，减少无效请求
- **T206**：Unpaywall 礼貌补 `oa_url`

## Working Rules For This Run
- 每层：**manifest 先行**；删缓存前核对 `LICENSE_POLICY.md`

## Resume Instructions
1. `TODO.md` → **DOING T203**
2. 扩展 `pilot_fetch_oa_html.py` 或新脚本：按年循环 + `retry_queue`
3. `cp research_ops/00_meta/TODO.md SCALABLE_DISCOVERY_AGENT_TODO.md` → commit
