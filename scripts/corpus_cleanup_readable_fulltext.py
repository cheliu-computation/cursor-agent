#!/usr/bin/env python3
"""
Keep only readable full-text artifacts:
- PDFs: rows in pdf_extract_index.csv with has_body=yes (+ their .txt)
- HTML: fulltext_html_status=ingested, artifact exists, stripped text >= min_chars
- XML: keep Europe PMC fullTextXML (T205_*.xml, T211_*.xml) as structured full text

Delete other cache PDFs/HTML under research_ops/cache/{pdfs,fulltext}.
Prune download_manifest; fix paper_reading_status; rebuild pdf_extract_index if needed.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from pilot_section_extract_html import strip_html  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-html-chars", type=int, default=200)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    idx_path = ROOT / "research_ops/parsed/pdfs/pdf_extract_index.csv"
    if not idx_path.exists():
        print("missing pdf_extract_index.csv — run batch_extract_all_pdfs.py first", file=sys.stderr)
        return 1

    keep_pdfs: set[str] = set()
    with idx_path.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if (r.get("has_body") or "").strip().lower() != "yes":
                continue
            p = (r.get("pdf_path") or "").strip()
            if p:
                keep_pdfs.add(p)

    keep_html: set[str] = set()
    rs_path = ROOT / "research_ops/02_papers/paper_reading_status.csv"
    with rs_path.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if (r.get("fulltext_html_status") or "").strip() != "ingested":
                continue
            art = (r.get("fulltext_html_artifact") or "").strip()
            if not art.lower().endswith(".html"):
                continue
            fp = ROOT / art
            if not fp.is_file():
                continue
            try:
                raw = fp.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if len(strip_html(raw)) >= args.min_html_chars:
                keep_html.add(art)

    keep_xml: set[str] = set()
    ft_dir = ROOT / "research_ops/cache/fulltext"
    if ft_dir.is_dir():
        for p in ft_dir.glob("T205_*.xml"):
            keep_xml.add(str(p.relative_to(ROOT)))
        for p in ft_dir.glob("T211_*.xml"):
            keep_xml.add(str(p.relative_to(ROOT)))

    keep_all_rel = keep_pdfs | keep_html | keep_xml

    def do_delete(path: Path) -> None:
        if args.dry_run:
            return
        path.unlink(missing_ok=True)

    n_del_pdf = n_del_html = 0
    pdf_dir = ROOT / "research_ops/cache/pdfs"
    if pdf_dir.is_dir():
        for p in pdf_dir.glob("*.pdf"):
            rel = str(p.relative_to(ROOT))
            if rel not in keep_pdfs:
                do_delete(p)
                n_del_pdf += 1
            txt = ROOT / "research_ops/parsed/pdfs" / (p.stem + ".txt")
            if rel not in keep_pdfs and txt.exists():
                do_delete(txt)

    if ft_dir.is_dir():
        for p in ft_dir.iterdir():
            if not p.is_file():
                continue
            rel = str(p.relative_to(ROOT))
            if rel in keep_all_rel:
                continue
            if p.suffix.lower() in (".html", ".htm", ".pdf"):
                do_delete(p)
                n_del_html += 1

    # Prune manifest: drop rows whose local_path is under cache and file missing
    mnf = ROOT / "research_ops/manifests/download_manifest.csv"
    with mnf.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        fn = rdr.fieldnames
        rows = list(rdr)
    kept_m = []
    lp_norm = lambda s: s.replace("\\", "/")
    for r in rows:
        lp = (r.get("local_path") or "").strip()
        if not lp:
            kept_m.append(r)
            continue
        p = ROOT / lp
        ln = lp_norm(lp)
        if ln.startswith("research_ops/cache/") or ln.startswith("cache/"):
            if not p.is_file():
                continue
        kept_m.append(r)
    if not args.dry_run:
        with mnf.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fn)
            w.writeheader()
            w.writerows(kept_m)

    # paper_reading_status: clear artifacts pointing to deleted files
    with rs_path.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        rfn = rdr.fieldnames
        rs_rows = list(rdr)
    n_fix = 0
    for r in rs_rows:
        art = (r.get("fulltext_html_artifact") or "").strip()
        if not art:
            continue
        p = ROOT / art
        if not p.is_file():
            st = (r.get("fulltext_html_status") or "").strip()
            if st in ("ingested", "pdf_cached"):
                r["fulltext_html_status"] = "error"
                r["fulltext_html_artifact"] = ""
                r["notes"] = (r.get("notes", "") + "; corpus_cleanup_missing_file")[:240]
                n_fix += 1
    if not args.dry_run:
        with rs_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=rfn)
            w.writeheader()
            for r in rs_rows:
                w.writerow({k: r.get(k, "") for k in rfn})

    # Write html readable index for downstream stats
    html_idx = ROOT / "research_ops/parsed/fulltext/html_readable_index.csv"
    if not args.dry_run:
        html_idx.parent.mkdir(parents=True, exist_ok=True)
        # enrich from papers_master
        pm_by_oid: dict[str, dict] = {}
        with (ROOT / "research_ops/02_papers/papers_master.csv").open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                oid = (row.get("openalex_id") or "").strip()
                if oid:
                    pm_by_oid[oid] = row
                    if not oid.startswith("W"):
                        pm_by_oid["W" + oid] = row

        out_rows = []
        oid_re = re.compile(r"^T\d+_(W\d+)")
        for rel in sorted(keep_html):
            fp = ROOT / rel
            raw = fp.read_text(encoding="utf-8", errors="replace")
            text = strip_html(raw)
            m = oid_re.search(fp.stem)
            oid = m.group(1) if m else ""
            pm = pm_by_oid.get(oid, {})
            out_rows.append({
                "openalex_id": oid,
                "html_path": rel,
                "char_count": str(len(text)),
                "year": (pm.get("year") or "").strip(),
                "venue": (pm.get("venue") or "")[:120],
                "source_batch": (pm.get("source_batch") or "")[:80],
                "tags_modality": (pm.get("tags_modality") or "").strip(),
                "tags_method": (pm.get("tags_method") or "").strip(),
                "title": (pm.get("title") or "")[:200],
            })
        if out_rows:
            with html_idx.open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
                w.writeheader()
                w.writerows(out_rows)

    # Shrink pdf_extract_index to kept PDFs only
    idx_rows_after: int | None = None
    if not args.dry_run and idx_path.exists():
        with idx_path.open(newline="", encoding="utf-8") as f:
            rdr = csv.DictReader(f)
            ifn = rdr.fieldnames
            idx_rows = [r for r in rdr if (r.get("has_body") or "").lower() == "yes"]
        idx_rows = [r for r in idx_rows if (ROOT / (r.get("pdf_path") or "").strip()).is_file()]
        idx_rows_after = len(idx_rows)
        with idx_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=ifn)
            w.writeheader()
            for r in idx_rows:
                w.writerow({k: r.get(k, "") for k in ifn})

    print(
        json.dumps(
            {
                "keep_pdfs": len(keep_pdfs),
                "keep_html": len(keep_html),
                "keep_xml": len(keep_xml),
                "deleted_pdf_files": n_del_pdf,
                "deleted_html_like": n_del_html,
                "manifest_rows": len(kept_m),
                "reading_status_fixed": n_fix,
                "pdf_index_rows_after": idx_rows_after,
                "dry_run": args.dry_run,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    import json
    raise SystemExit(main())
