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
- **T218**：统一抓取策略模块 `scripts/fetch_policy.py`，修复无效 `User-Agent`/请求头，给 OA HTML / OpenAlex / Europe PMC 相关脚本复用
- **T219**：默认禁用 `fetch_case_pmc_fulltext_pilot.py`；只有显式 `--allow-case-report-fetch` 才允许抓 case-report 全文
- **T220**：`reclassify_layerb_policy_skips.py` 将 **949** 条明显高阻拦 / 持续 403 的 Layer-B 旧错误改标为 `skipped_policy`
- **T221**：第二轮来源策略收敛：JAMA / NEJM 保留为高价值临床来源，但当前环境下页面直抓默认视为高阻拦；MDPI 明确降权，不再作为修复重点
- **T222**：缩小 preprint/arXiv 全文范围：默认过滤纯 preprint 全文抓取，只保留“近年 + 非 preprint 主来源 + DOI 匹配”的 arXiv 兜底路径
- **当前 Layer-B 状态**：`error` **1119 → 111**；`skipped_policy` **1523 → 3678**

## Key Findings So Far
- **Crossref** 仍是缺 OpenAlex `oa_url` 时的主力补链；**T212** 对「无 URL」行用 OpenAlex `is_oa=false` 打 **`skipped_policy`**，避免误抓付费墙
- Layer-B 里大量旧 `error` 实际属于 **publisher 403 / 高阻拦来源 / 不应直抓的 PDF 直链**，应归类为策略跳过而不是无限重试
- 对当前目标而言，**研究文献（medical + AI）** 优先级明显高于 case-report 全文；case report 默认只保留 metadata / 弱信号定位
- JAMA / NEJM 值得保留在来源层，但在当前执行环境里更适合依赖 Crossref / OpenAlex / Unpaywall / Europe PMC 这类 OA 路由，而不是直接抓 publisher 页面
- 当前仓库里的“正文”并不是存进数据库的全文库；raw 正文在 `cache/`（gitignored），提取后的文本/JSONL/索引在 `parsed/`，长期保留的是 CSV / manifest / extracted outputs
- arXiv 相关 URL 历史上占比偏大；当前策略已将其缩到“metadata-first，full-text 仅作近年 publisher-backed 兜底”

## Current Assets
- `scripts/harvest_openalex_year_slice.py` — 按 **年 × source_id** 拉取并 merge
- `scripts/fetch_case_pmc_fulltext_pilot.py`、`scripts/pilot_section_extract_html.py`
- `paper_epmc_fulltext_pilot.csv`、`case_reading_status.csv`

## Risks / Blockers
- Publisher ToS / 403 / 429；部分 publisher landing/PDF 直链仍不适合脚本直抓
- `cache/pdfs` 体量大（见 RUN_LOG T216）

## Next Best Task
- **T127**（MedIA/TMI 全量分页）→ **T217**（Unpaywall，需 email key）→ 对剩余 **111** 条 `error` 做来源专项分流（尤其 `doi.org` / `academic.oup.com` / repository mirrors）

## Immediate Follow-ups
- 对剩余 `doi.org` / `mdpi` / `jamanetwork` 错误行，优先走更稳的 OA 路由补链，而不是继续撞 publisher 直链
- 保持 case reports 为 metadata-only 默认策略，除非有明确需求再显式 opt-in 全文抓取

## Working Rules For This Run
- manifest 先行；删缓存前核对 `LICENSE_POLICY.md`

## Resume Instructions
1. `TODO.md` → **DOING T127**
2. OpenAlex `cursor` 分页脚本或手工分批 `harvest_openalex_year_slice.py` 提高 `limit-per-source`
3. `cp research_ops/00_meta/TODO.md SCALABLE_DISCOVERY_AGENT_TODO.md` → commit
