# STATUS

副标题：Scalable Discovery Agent 运行状态

## Current Focus
- 当前阶段：文献脊 **6583** 篇（+**2017** 期刊切片）+ 阅读栈（摘要 FTS、Layer B、PMC 病例/论文 XML、审计 `read_priority`）
- 当前目标：**T127** — 扩大 MedIA/TMI 等核心刊 OpenAlex 分页覆盖（与 T213 脚本同族）
- 当前任务 ID：**T127**
- 当前工作流：Literature Lake + Case Lake + Repro link
- 当前运行模式：`download_manifest` + `cache/**`（gitignore）

## Current Task
- Title：**T127** — 对 OpenAlex `S116571295`（MedIA）、`S58069681`（TMI）等做 cursor 分页直至 `meta.count` 或记录采样策略
- Deliverable：`papers_master.csv` + RUN_LOG
- Done When：文档化完整抓取或明确 cap 理由
- Blocking Dependencies：API 成本与速率

## Completed In This Run（摘要）
- **T204–T212、T208、T214–T216**：见 `RUN_LOG.md` 顶部条目（PDF 校验、EPMC、Crossref、FTS、policy gate、retry、footprint）
- **T209**：`audit_priority_list` / `repro_audit` 增加 **`read_priority=high`**（50 行）
- **T210**：`pilot_section_extract_html.py` → **10** 条 naive 分段 JSONL（gitignored）
- **T211**：**20** 病例 `fullTextXML` + `case_reading_status.csv` + manifest
- **T213**：`harvest_openalex_year_slice.py` — **2017** ×7 刊 ×35 → **+182** `papers_master`；`ingest_openalex_abstracts` **2017** 摘要 **92** ingested；**FTS 6671** 行；Crossref 再 **+139** `oa_url`；T212 二遍 **+80** `skipped_policy`

## Key Findings So Far
- **Crossref** 仍是缺 OpenAlex `oa_url` 时的主力补链；**T212** 对「无 URL」行用 OpenAlex `is_oa=false` 打 **`skipped_policy`**，避免误抓付费墙
- **6583** 行 `paper_reading_status` 与主表对齐；**~2364** manifest 数据行（含论文 Layer B、EPMC、病例 XML）

## Current Assets
- `scripts/harvest_openalex_year_slice.py` — 按 **年 × source_id** 拉取并 merge
- `scripts/fetch_case_pmc_fulltext_pilot.py`、`scripts/pilot_section_extract_html.py`
- `paper_epmc_fulltext_pilot.csv`、`case_reading_status.csv`

## Risks / Blockers
- Publisher ToS / 429；`cache/pdfs` 体量大（见 RUN_LOG T216）

## Next Best Task
- **T127**（MedIA/TMI 全量分页）→ **T217**（Unpaywall，需 email key）→ **T214** 续跑（可选）

## Immediate Follow-ups
- 新入库 **2017** 行：可再跑 `batch_fetch_oa_html.py` 消化带 URL 的 `pending`
- 重建本地摘要索引：`build_abstract_fts.py`（已在 T213 后执行）

## Working Rules For This Run
- manifest 先行；删缓存前核对 `LICENSE_POLICY.md`

## Resume Instructions
1. `TODO.md` → **DOING T127**
2. OpenAlex `cursor` 分页脚本或手工分批 `harvest_openalex_year_slice.py` 提高 `limit-per-source`
3. `cp research_ops/00_meta/TODO.md SCALABLE_DISCOVERY_AGENT_TODO.md` → commit
