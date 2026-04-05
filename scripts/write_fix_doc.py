#!/usr/bin/env python3
"""Write the GPT-5.4 fix summary markdown for the cleaned codebase."""
from __future__ import annotations

from pathlib import Path


OUTPUT = Path("research_ops/00_meta/2026-04-04_5.4_fix_record.md")


CONTENT = """# 5.4 修复文档

日期：2026-04-04

## 目标

- 清理 `origin/cursor/agent-b783` 中与抓取修复相关、但不适合作为长期 codebase 入口的历史提交痕迹。
- 保留可接受、可复用的抓取策略、数据表和分析脚本。
- 删除运行期状态 Markdown、阶段性 memo、agent skill card 等历史性文档残留。

## 接收的修复内容

以下改动被纳入清理后的 codebase：

1. **统一抓取策略**
   - `scripts/fetch_policy.py`
   - 统一 browser/API 请求头
   - 统一 URL canonicalization
   - 对高阻拦来源增加策略跳过与 terminal-error 识别

2. **抓取与补链脚本**
   - `scripts/batch_fetch_oa_html.py`
   - `scripts/pilot_fetch_oa_html.py`
   - `scripts/enrich_oa_url_crossref.py`
   - `scripts/enrich_oa_url_epmc.py`
   - `scripts/enrich_oa_url_openalex.py`
   - `scripts/t212_openalex_policy_gate.py`
   - `scripts/fetch_epmc_fulltext_pilot.py`
   - `scripts/ingest_openalex_abstracts.py`

3. **修复与重分类脚本**
   - `scripts/reclassify_layerb_policy_skips.py`
   - `scripts/reclassify_preprint_scope.py`
   - `scripts/reclassify_cleaned_artifacts.py`
   - `scripts/reclassify_terminal_tail.py`

4. **可复用数据层**
   - `research_ops/02_papers/papers_master.csv`
   - `research_ops/02_papers/paper_reading_status.csv`
   - `research_ops/manifests/*.csv`
   - 保留与来源策略、许可、schema 有关的元文档

## 清理动作

本次清理删除了以下不再适合作为长期仓库资产的历史内容：

- 历史运行状态文档
  - `research_ops/00_meta/RUN_LOG.md`
  - `research_ops/00_meta/STATUS.md`
  - `research_ops/00_meta/TODO.md`
- 阶段性汇总/一次性输出
  - `research_ops/00_meta/PDF_CORPUS_REPORT.md`
  - `research_ops/00_meta/YEAR_SOURCE_JOURNAL_TABLE.md`
  - `research_ops/13_exports/run_summaries/summary_001.md`
  - `research_ops/13_exports/synthesis_memos/*.md`
- 历史说明和 skill-card
  - `research_ops/15_agentic/skill_cards/*.md`
  - `research_ops/15_agentic/skill_template.md`
  - `research_ops/15_agentic/what_counts_as_real_agent_self_evolution.md`
  - `research_ops/16_case_reports/*memo*.md`
  - `research_ops/16_case_reports/case_report_cache_lifecycle.md`
  - `research_ops/16_case_reports/negative_finding_checklist.md`
- 未引入当前分支的分支标记文件
  - `GPT_5_4_READ_MARKER_AGENT_B783.md`

## 修复结论

`b783` 分支里关于“修复爬取”的核心价值被保留下来，但其原始历史提交并未原样搬运。清理后的 codebase 采用更少、更聚焦的提交来承载以下结果：

- 以 OpenAlex / Crossref / Europe PMC / PMC OA 为优先路线；
- 对 JAMA / NEJM / Cell / Lancet / RSNA / OUP / MDPI 等高阻拦来源停止无效硬抓；
- 将 arXiv / preprint 收敛为 metadata-first、fulltext-fallback-only；
- 将统计和验证结果固化为可复现脚本与 Markdown 报告。
"""


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(CONTENT, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
