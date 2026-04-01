# STATUS

副标题：Scalable Discovery Agent 运行状态

## Current Focus
- 当前阶段：**Rolling literature ingest**（多读、读广、读最近）+ 预印本噪声治理
- 当前目标：`papers_master` **6000+** 行；`harvest_window` 可筛；预印本有 `topic_subtag`
- 当前任务 ID：**T184**
- 当前工作流：Paper Master / OpenAlex harvest
- 当前运行模式：按年 venue + arXiv 回卷；按月脚本 `scripts/harvest_openalex_monthly.py`

## Current Task
- Title：**T184** — **2017** 窗口（10 期刊 ×35 + arXiv 2017 ~70）
- Deliverable：`papers_master.csv` + `RUN_LOG.md`
- Done When：新增 **≥100** 行

## Completed In This Run（摘要）
- **T171–T172**：宽谱近期（期刊 + arXiv）首批暴涨
- **T173–T181**：按年回卷 **2023→2019**（venue + arXiv）；**T176/T179** 加深 bioRxiv/medRxiv（含 2023 genomics/single-cell/spatial）
- **T180**：2020 窗口 **+550**（至 **5572**）
- **T181**：2019 **+492**（至 **6064**）
- **T174**：新增 **`harvest_window`** 列并从 `source_batch` 回填
- **T182**：`scripts/harvest_openalex_monthly.py` + MedIA **2025-01** 烟测 **+5** 行
- **T175**：**`topic_subtag`** 列，**1452** 条预印本行标题启发式打标
- **T183**：**2018** 窗口 **+332**（至 **6401**）

## Current Assets
- `papers_master.csv`：**6401** 数据行（`wc -l` → **6402** 含表头）

## Next Best Task
- **T184** → **T123**（`venue_type`）→ **T124**（authors 回填）

## Immediate Follow-ups
- **T138**：challenge 链接论文并入主表
- **T140**：Swin UNETR 全表（与 ingest 并行）

## Resume Instructions
1. `TODO.md` → **DOING T183**
2. 跑 2018 批次后 `wc -l research_ops/02_papers/papers_master.csv`
3. `cp research_ops/00_meta/TODO.md SCALABLE_DISCOVERY_AGENT_TODO.md` → commit → push
