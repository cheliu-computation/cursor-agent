#!/usr/bin/env python3
"""Classify journal type; build year × source × type counts; write markdown tables."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


def domain_channel(url: str) -> str:
    if not url or not url.lower().startswith("http"):
        return "unknown"
    try:
        h = urlparse(url).netloc.lower()
    except Exception:
        return "unknown"
    if "arxiv.org" in h:
        return "arXiv"
    if "doi.org" in h:
        return "DOI resolver"
    if "biomedcentral" in h or "springer" in h or "nature.com" in h:
        return "Springer/Nature/BMC"
    if "ieee.org" in h or "ieee" in h:
        return "IEEE"
    if "frontiersin.org" in h:
        return "Frontiers"
    if "hal.science" in h or "hal.archives" in h:
        return "HAL"
    if "pmc.ncbi" in h or "nih.gov" in h:
        return "NIH/PMC"
    if "biorxiv" in h:
        return "bioRxiv"
    if "medrxiv" in h:
        return "medRxiv"
    if "jmir.org" in h:
        return "JMIR"
    if "cambridge.org" in h:
        return "Cambridge"
    if "thieme" in h:
        return "Thieme"
    return h.split(":")[0] or "other_host"


def coarse_source(ch: str) -> str:
    """Few columns for summary table."""
    if ch == "arXiv":
        return "arXiv"
    if ch == "Springer/Nature/BMC":
        return "Springer/Nature/BMC"
    if ch == "IEEE":
        return "IEEE"
    if ch == "HTML_cache":
        return "HTML（缓存全文页）"
    if ch == "Europe_PMC_XML":
        return "Europe PMC（论文XML）"
    if ch == "Europe_PMC_XML_case":
        return "Europe PMC（病例XML）"
    if ch in ("NIH/PMC", "DOI resolver", "Frontiers", "HAL", "bioRxiv", "medRxiv"):
        return ch
    if ch == "unknown":
        return "其他/未知"
    return "机构库及其他主机"


def classify_journal_type(venue: str, tags_modality: str, tags_method: str, source_batch: str) -> str:
    """1) 算法类 2) 医学类 3) Nature/综合高影响 — 见 YEAR_SOURCE_JOURNAL_TABLE.md"""
    v = (venue or "").lower()
    tm = (tags_modality or "").lower()
    meth = (tags_method or "").lower()
    batch = (source_batch or "").lower()

    # 1) 算法 / ML / CV
    method_venues = (
        "neurips", "icml", "iclr", "cvpr", "iccv", "eccv",
        "machine learning", "computer vision", "artificial intelligence",
    )
    method_tags = (
        "machine_learning", "computer_vision", "deep_learning", "transformers",
        "generative", "segmentation", "self_supervised", "federated_privacy",
        "representation_learning", "agents",
    )
    if any(x in v for x in method_venues):
        return "算法/ML/CV"
    if any(x in tm for x in ("machine_learning", "computer_vision")):
        return "算法/ML/CV"
    if any(x in meth for x in method_tags):
        return "算法/ML/CV"
    if any(x in batch for x in ("neurips", "icml", "iclr", "cvpr", "iccv", "eccv")):
        return "算法/ML/CV"

    # 2) 通用高影响 / Nature 系（先于宽泛 clinical 词，避免 “Nature Medicine” 被 medicine 命中）
    general_kw = (
        "nature", "science", "cell ", "cell systems", "science advances",
        "pnas", "national academy", "plos one", "elife",
        "nature machine intelligence", "nature computational", "nature methods",
        "npj ", "nature medicine", "nature biomedical",
    )
    if any(k in v for k in general_kw):
        return "通用高影响/Nature系"
    if any(k in batch for k in ("nature_", "science_", "cell_", "npj_", "pnas")):
        if "radiology" not in v and "tmi" not in v and "medical image" not in v:
            return "通用高影响/Nature系"

    # 3) 医学 / 临床 / 医学影像
    clinical_kw = (
        "radiology", "jama", "nejm", "lancet", "bmj", "clinical",
        "health", "hospital", "patient", "oncology",
        "pathology", "surgery", "medical imaging", "transactions on medical imaging",
        "medical image analysis", "journal of digital imaging", "digital health",
    )
    clinical_tags = (
        "clinical_", "medical_imaging", "clinical_imaging", "radiology", "pathology",
        "clinical_translational", "clinical_high_impact", "clinical_ai",
    )
    if any(k in v for k in clinical_kw):
        return "医学/临床/影像"
    if "medicine" in v and "nature" not in v:
        return "医学/临床/影像"
    if any(t in tm for t in clinical_tags):
        return "医学/临床/影像"

    if "arxiv" in v or "preprint" in tm or "preprint" in batch:
        return "预印本/未细分"

    return "其他/混合"


def main() -> int:
    idx_pdf = ROOT / "research_ops/parsed/pdfs/pdf_extract_index.csv"
    idx_html = ROOT / "research_ops/parsed/fulltext/html_readable_index.csv"
    out_md = ROOT / "research_ops/00_meta/YEAR_SOURCE_JOURNAL_TABLE.md"
    pm_path = ROOT / "research_ops/02_papers/papers_master.csv"

    pm_by_oid: dict[str, dict] = {}
    if pm_path.exists():
        with pm_path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                oid = (row.get("openalex_id") or "").strip()
                if oid:
                    pm_by_oid[oid] = row
                    if not oid.startswith("W"):
                        pm_by_oid["W" + oid] = row

    records: list[dict] = []

    if idx_pdf.exists():
        with idx_pdf.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if (r.get("has_body") or "").lower() != "yes":
                    continue
                pdf_p = ROOT / (r.get("pdf_path") or "").strip()
                if not pdf_p.is_file():
                    continue
                y = (r.get("year") or "").strip()
                if not y.isdigit():
                    continue
                jt = classify_journal_type(
                    r.get("venue", ""),
                    r.get("tags_modality", ""),
                    r.get("tags_method", ""),
                    r.get("source_batch", ""),
                )
                ch = domain_channel(r.get("source_url", ""))
                records.append({"year": int(y), "channel": ch, "journal_type": jt, "format": "PDF"})

    if idx_html.exists():
        with idx_html.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                hp = ROOT / (r.get("html_path") or "").strip()
                if not hp.is_file():
                    continue
                y = (r.get("year") or "").strip()
                if not y.isdigit():
                    continue
                jt = classify_journal_type(
                    r.get("venue", ""),
                    r.get("tags_modality", ""),
                    r.get("tags_method", ""),
                    r.get("source_batch", ""),
                )
                records.append({"year": int(y), "channel": "HTML_cache", "journal_type": jt, "format": "HTML"})

    epmc = ROOT / "research_ops/02_papers/paper_epmc_fulltext_pilot.csv"
    if epmc.exists():
        with epmc.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                pmcid = (r.get("pmcid") or "").strip()
                xml_rel = f"research_ops/cache/fulltext/T205_{pmcid}.xml"
                if not (ROOT / xml_rel).is_file():
                    continue
                oid = (r.get("openalex_id") or "").strip()
                pm = pm_by_oid.get(oid, {})
                y = (pm.get("year") or "").strip()
                if not y.isdigit():
                    y = (r.get("retrieval_time_utc") or "2025")[:4]
                if not str(y).isdigit():
                    continue
                jt = classify_journal_type(
                    pm.get("venue", ""),
                    pm.get("tags_modality", ""),
                    pm.get("tags_method", ""),
                    pm.get("source_batch", ""),
                )
                records.append({"year": int(y), "channel": "Europe_PMC_XML", "journal_type": jt, "format": "XML"})

    cases = ROOT / "research_ops/16_case_reports/case_reading_status.csv"
    if cases.exists():
        with cases.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                pmcid = (r.get("pmcid") or "").strip()
                xml_rel = f"research_ops/cache/fulltext/T211_{pmcid}.xml"
                if not (ROOT / xml_rel).is_file():
                    continue
                y = int((r.get("retrieval_time_utc") or "2026")[:4])
                records.append({
                    "year": y,
                    "channel": "Europe_PMC_XML_case",
                    "journal_type": "医学/临床/影像",
                    "format": "XML_case",
                })

    agg: dict[int, dict[tuple[str, str], int]] = defaultdict(lambda: defaultdict(int))
    agg_coarse: dict[int, dict[tuple[str, str], int]] = defaultdict(lambda: defaultdict(int))
    for rec in records:
        agg[rec["year"]][(rec["channel"], rec["journal_type"])] += 1
        cs = coarse_source(rec["channel"])
        agg_coarse[rec["year"]][(cs, rec["journal_type"])] += 1

    years = sorted(agg.keys())
    channels = sorted({rec["channel"] for rec in records})
    coarse_channels = sorted({coarse_source(c) for c in channels})
    jtypes = ["算法/ML/CV", "医学/临床/影像", "通用高影响/Nature系", "预印本/未细分", "其他/混合"]

    ch_totals_by_year: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for y in years:
        for (ch, _jt), n in agg[y].items():
            ch_totals_by_year[y][ch] += n

    jt_by_year: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for y in years:
        for (_ch, jt), n in agg[y].items():
            jt_by_year[y][jt] += n

    ch_jt: dict[tuple[str, str], int] = defaultdict(int)
    for rec in records:
        ch_jt[(rec["channel"], rec["journal_type"])] += 1

    lines = [
        "# 年份 × 来源渠道 × 期刊类型 统计表",
        "",
        "## 期刊类型定义（三类 + 补充）",
        "",
        "优先级：**算法类 → Nature/通用高影响 → 医学类 → 预印本 → 其他**（避免 “Nature Medicine” 被宽泛 `medicine` 词误分）。",
        "",
        "| 类型 | 含义 | 规则要点 |",
        "|------|------|----------|",
        "| **算法/ML/CV** | 算法、机器学习、计算机视觉路线 | venue 含 NeurIPS/ICML/ICLR/CVPR/ICCV/ECCV 等；或 `tags_modality` 为 machine_learning / computer_vision；或 `tags_method` 为 deep_learning、transformers、segmentation 等；或 `source_batch` 含上述会议缩写 |",
        "| **医学/临床/影像** | 临床医学与医学影像应用 | venue 含 Radiology、Lancet、NEJM、MedIA、IEEE TMI、clinical、pathology 等；或 `tags_modality` 含 clinical_*、medical_imaging、radiology、pathology 等 |",
        "| **通用高影响/Nature系** | Nature / Science / Cell / npj 等综合刊与交叉科学 | venue 含 nature、science、cell、npj、PNAS 等；或批次名含对应前缀（且 venue 非明显专科影像刊） |",
        "| **预印本/未细分** | 主要为 arXiv 等预印本、尚未被上类规则吸收 | arXiv venue 或 preprint 标签 |",
        "| **其他/混合** | 不满足以上 | — |",
        "",
        "## 数据来源（仅保留可读全文后）",
        "",
        "- **PDF**：`pdf_extract_index.csv` 且 `has_body=yes` 且 **PDF 文件仍存在**。",
        "- **HTML**：`html_readable_index.csv` 且 **HTML 文件仍存在**（去标签后 ≥200 字符）。",
        "- **XML**：Europe PMC `fullTextXML`，**T205_*.xml / T211_*.xml 文件仍存在**。",
        "",
        f"- **统计条数**（PDF/HTML/XML 分别计数，同一篇可多种形式）：**{len(records)}**",
        "",
        "## 表 1：按年份 × 来源大类（篇数，便于阅读）",
        "",
    ]

    ch_coarse_totals: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for y in years:
        for (cs, _jt), n in agg_coarse[y].items():
            ch_coarse_totals[y][cs] += n

    header = "| 年份 | " + " | ".join(coarse_channels) + " | **合计** |"
    sep = "|---|" + "|".join(["---"] * len(coarse_channels)) + "|---|"
    lines.append(header)
    lines.append(sep)
    for y in years:
        tot = 0
        cells = []
        for c in coarse_channels:
            v = ch_coarse_totals[y].get(c, 0)
            tot += v
            cells.append(str(v) if v else "0")
        lines.append(f"| {y} | " + " | ".join(cells) + f" | **{tot}** |")

    lines.extend(
        [
            "",
            "<details>",
            "<summary>表 1b：按年份 × 细粒度主机（展开）</summary>",
            "",
        ]
    )
    header_b = "| 年份 | " + " | ".join(channels) + " | **合计** |"
    sep_b = "|---|" + "|".join(["---"] * len(channels)) + "|---|"
    lines.append(header_b)
    lines.append(sep_b)
    for y in years:
        tot = sum(ch_totals_by_year[y].values())
        cells = [str(ch_totals_by_year[y].get(c, 0)) for c in channels]
        lines.append(f"| {y} | " + " | ".join(cells) + f" | **{tot}** |")
    lines.extend(["", "</details>", ""])

    lines.extend(["", "## 表 2：按年份 × 期刊类型（各来源合并）", ""])
    lines.append("| 年份 | " + " | ".join(jtypes) + " | **合计** |")
    lines.append("|---|" + "|".join(["---"] * len(jtypes)) + "|---|")
    for y in years:
        tot = sum(jt_by_year[y].values())
        cells = [str(jt_by_year[y].get(jt, 0)) for jt in jtypes]
        lines.append(f"| {y} | " + " | ".join(cells) + f" | **{tot}** |")

    lines.extend(["", "## 表 3：按来源渠道 × 期刊类型（全时期）", ""])
    lines.append("| 来源渠道 | " + " | ".join(jtypes) + " | **合计** |")
    lines.append("|---|" + "|".join(["---"] * len(jtypes)) + "|---|")
    for c in channels:
        row = [str(ch_jt.get((c, jt), 0)) for jt in jtypes]
        t = sum(ch_jt.get((c, jt), 0) for jt in jtypes)
        lines.append(f"| {c} | " + " | ".join(row) + f" | **{t}** |")

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", out_md.relative_to(ROOT), "records", len(records))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
