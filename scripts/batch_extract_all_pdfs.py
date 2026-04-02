#!/usr/bin/env python3
"""Extract text from all PDFs under cache/pdfs; write index + markdown report."""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from extract_pdf_text import extract_text  # noqa: E402
CACHE_PDF = ROOT / "research_ops/cache/pdfs"
OUT_TXT = ROOT / "research_ops/parsed/pdfs"
INDEX_CSV = ROOT / "research_ops/parsed/pdfs/pdf_extract_index.csv"
REPORT_MD = ROOT / "research_ops/00_meta/PDF_CORPUS_REPORT.md"

def domain_bucket(url: str) -> str:
    if not url or not url.lower().startswith("http"):
        return "unknown"
    try:
        host = urlparse(url).netloc.lower()
    except Exception:
        return "unknown"
    if "arxiv.org" in host or "export.arxiv.org" in host:
        return "arxiv"
    if "doi.org" in host:
        return "doi.org (resolver)"
    if "biomedcentral" in host or "springer" in host or "nature.com" in host:
        return "springer/nature/bmc"
    if "frontiersin.org" in host:
        return "frontiers"
    if "hal.science" in host or "hal.archives" in host:
        return "hal"
    if "pmc.ncbi.nlm.nih.gov" in host or "nih.gov" in host:
        return "nih/pmc"
    if "ieee.org" in host or "ieee" in host:
        return "ieee"
    if "elsevier" in host:
        return "elsevier"
    return host[:50] or "unknown"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-chars", type=int, default=200, help="Count as 'has body' if >= this")
    ap.add_argument("--clean-txt", action="store_true", help="Remove existing parsed/pdfs/*.txt first")
    args = ap.parse_args()

    if args.clean_txt:
        for p in OUT_TXT.glob("*.txt"):
            p.unlink()

    OUT_TXT.mkdir(parents=True, exist_ok=True)

    # manifest: local_path -> source_url
    mnf_by_path: dict[str, str] = {}
    mnf_path = ROOT / "research_ops/manifests/download_manifest.csv"
    if mnf_path.exists():
        with mnf_path.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                lp = (r.get("local_path") or "").strip()
                if lp.endswith(".pdf"):
                    mnf_by_path[lp] = (r.get("source_url") or "").strip()

    # reading_status: artifact -> openalex_id
    art_to_oid: dict[str, str] = {}
    rs_path = ROOT / "research_ops/02_papers/paper_reading_status.csv"
    if rs_path.exists():
        with rs_path.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                art = (r.get("fulltext_html_artifact") or "").strip()
                if art.lower().endswith(".pdf"):
                    art_to_oid[art] = (r.get("openalex_id") or "").strip()

    # papers_master by openalex_id (normalize W prefix)
    pm_by_oid: dict[str, dict] = {}
    pm_path = ROOT / "research_ops/02_papers/papers_master.csv"
    if pm_path.exists():
        with pm_path.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                oid = (r.get("openalex_id") or "").strip()
                if not oid:
                    continue
                key = oid if oid.startswith("W") else "W" + oid
                pm_by_oid[key] = r
                pm_by_oid[oid] = r

    pdfs = sorted(CACHE_PDF.glob("*.pdf"))
    rows_out: list[dict] = []
    stem_re = re.compile(r"^T\d+_(W\d+)$")  # T202_/T203_ pilot prefixes

    for pdf_path in pdfs:
        rel_pdf = str(pdf_path.relative_to(ROOT))
        err_note = ""
        try:
            if pdf_path.stat().st_size == 0:
                raise ValueError("empty file")
            text, meta = extract_text(pdf_path)
            char_count = meta["char_count"]
        except Exception as e:
            text = ""
            meta = {"page_count": 0, "char_count": 0, "pdf_path": rel_pdf}
            char_count = 0
            err_note = str(e)[:200]
        has_body = char_count >= args.min_chars

        txt_path = OUT_TXT / (pdf_path.stem + ".txt")
        if has_body:
            txt_path.write_text(text, encoding="utf-8")
        elif txt_path.exists():
            txt_path.unlink()

        oid = art_to_oid.get(rel_pdf, "")
        if not oid:
            m = stem_re.match(pdf_path.stem)
            if m:
                oid = m.group(1)

        pm = pm_by_oid.get(oid, {}) if oid else {}
        src_url = mnf_by_path.get(rel_pdf, "")
        row = {
            "openalex_id": oid,
            "pdf_path": rel_pdf,
            "txt_path": str(txt_path.relative_to(ROOT)) if has_body else "",
            "char_count": str(char_count),
            "page_count": str(meta.get("page_count", 0)),
            "has_body": "yes" if has_body else "no",
            "extract_error": err_note,
            "source_url": src_url[:500],
            "source_domain_bucket": domain_bucket(src_url),
            "year": (pm.get("year") or "").strip(),
            "venue": (pm.get("venue") or "")[:120],
            "source_batch": (pm.get("source_batch") or "")[:80],
            "tags_modality": (pm.get("tags_modality") or "").strip(),
            "tags_method": (pm.get("tags_method") or "").strip(),
            "topic_subtag": (pm.get("topic_subtag") or "").strip(),
            "title": (pm.get("title") or "")[:200],
        }
        rows_out.append(row)

    fieldnames = list(rows_out[0].keys()) if rows_out else []
    with INDEX_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows_out)

    with_body = [r for r in rows_out if r["has_body"] == "yes"]
    n_pdf = len(rows_out)
    n_body = len(with_body)
    years = [int(r["year"]) for r in with_body if r["year"].isdigit()]
    y_min = min(years) if years else None
    y_max = max(years) if years else None

    dom_c = Counter(r["source_domain_bucket"] for r in with_body)
    batch_c = Counter(r["source_batch"] for r in with_body if r["source_batch"])
    mod_c = Counter()
    for r in with_body:
        for part in (r["tags_modality"] or "").replace("|", ",").split(","):
            p = part.strip()
            if p:
                mod_c[p] += 1
    sub_c = Counter(r["topic_subtag"] for r in with_body if r["topic_subtag"])

    lines = [
        "# PDF corpus report",
        "",
        "Generated by `scripts/batch_extract_all_pdfs.py`.",
        "",
        "## Summary",
        "",
        f"- **PDF files on disk** (`research_ops/cache/pdfs/*.pdf`): **{n_pdf}**",
        f"- **With extractable text body** (≥ {args.min_chars} chars after PyMuPDF): **{n_body}**",
        f"- **Empty / scan-only / failed text** (below threshold): **{n_pdf - n_body}**",
        f"- **Plain-text sidecars**: `research_ops/parsed/pdfs/T203_*.txt` (gitignored except `.gitkeep`)",
        f"- **Row-level index** (committed): `research_ops/parsed/pdfs/pdf_extract_index.csv`",
        "",
        "## (a) Literature with readable full text",
        "",
        f"**Count**: **{n_body}** papers have a `.txt` extract meeting the character threshold.",
        "OpenAlex IDs and titles are in `pdf_extract_index.csv` (filter `has_body=yes`).",
        "",
        "## (b) Where PDFs were fetched from",
        "",
        "By **download URL host bucket** (from `download_manifest.source_url`):",
        "",
    ]
    for k, v in dom_c.most_common():
        lines.append(f"- **{k}**: {v}")
    lines.extend(["", "Top **source_batch** (OpenAlex harvest provenance in `papers_master`):", ""])
    for k, v in batch_c.most_common(15):
        lines.append(f"- `{k}`: {v}")
    lines.extend(["", "## (c) Year span (papers with body, matched to `papers_master`)", ""])
    if y_min is not None:
        lines.append(f"- **Min year**: {y_min}")
        lines.append(f"- **Max year**: {y_max}")
        lines.append(f"- **Span**: {y_min}–{y_max}")
    else:
        lines.append("- No matched years (check `openalex_id` join).")
    lines.extend(["", "## (d) Topic-style classification", "", "### `tags_modality` (from `papers_master`)", ""])
    for k, v in mod_c.most_common(20):
        lines.append(f"- **{k}**: {v}")
    lines.extend(["", "### `topic_subtag` (preprint heuristics)", ""])
    if sub_c:
        for k, v in sub_c.most_common(15):
            lines.append(f"- **{k}**: {v}")
    else:
        lines.append("- (mostly empty for this PDF subset)")
    lines.extend(["", "### `tags_method` (top buckets)", ""])
    meth_c = Counter()
    for r in with_body:
        for part in (r["tags_method"] or "").replace("|", ",").split(","):
            p = part.strip()
            if p:
                meth_c[p] += 1
    for k, v in meth_c.most_common(15):
        lines.append(f"- **{k}**: {v}")
    lines.append("")

    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"pdfs": n_pdf, "with_body": n_body, "index": str(INDEX_CSV.relative_to(ROOT)), "report": str(REPORT_MD.relative_to(ROOT))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
