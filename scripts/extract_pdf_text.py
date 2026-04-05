#!/usr/bin/env python3
"""Extract plain text from cached PDFs (PyMuPDF). For scanned PDFs, use OCR separately."""
from __future__ import annotations

import argparse
import csv
import json
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE_PDF = ROOT / "research_ops/cache/pdfs"
OUT_DIR = ROOT / "research_ops/parsed/pdfs"
RS = ROOT / "research_ops/02_papers/paper_reading_status.csv"
MNF = ROOT / "research_ops/manifests/download_manifest.csv"
PARSE_MNF = ROOT / "research_ops/manifests/parse_manifest.csv"


def extract_text(pdf_path: Path) -> tuple[str, dict]:
    try:
        import fitz  # PyMuPDF
    except ImportError as e:
        raise SystemExit(
            "PyMuPDF required: pip install pymupdf\n" + str(e)
        ) from e

    doc = fitz.open(pdf_path)
    meta = {"page_count": doc.page_count, "pdf_path": str(pdf_path.relative_to(ROOT))}
    chunks: list[str] = []
    for i in range(doc.page_count):
        chunks.append(doc.load_page(i).get_text("text") or "")
    doc.close()
    text = "\n\n".join(chunks).strip()
    meta["char_count"] = len(text)
    meta["non_ws_ratio"] = (
        round(sum(1 for c in text if not c.isspace()) / max(len(text), 1), 4)
        if text
        else 0.0
    )
    return text, meta


def manifest_id_for_pdf(local_rel: str) -> str:
    if not MNF.exists():
        return ""
    with MNF.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if (r.get("local_path") or "").strip() == local_rel:
                return (r.get("manifest_id") or "").strip()
    return ""


def append_parse_manifest(
    manifest_id: str,
    parser_version: str,
    parse_status: str,
    out_rel: str,
    err: str,
    notes: str,
) -> None:
    row = {
        "parse_id": "P" + uuid.uuid4().hex[:16],
        "manifest_id": manifest_id,
        "parser_version": parser_version,
        "parse_status": parse_status,
        "structured_output_path": out_rel,
        "error_summary": err[:500],
        "raw_retained": "yes",
        "notes": notes[:300],
    }
    with PARSE_MNF.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        fn = rdr.fieldnames or list(row.keys())
        rows = list(rdr)
    rows.append({k: row.get(k, "") for k in fn})
    with PARSE_MNF.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fn)
        w.writeheader()
        w.writerows(rows)


def self_test(max_files: int = 5, min_chars: int = 80) -> int:
    pdfs = sorted(CACHE_PDF.glob("T203_*.pdf"))[:max_files]
    if not pdfs:
        print("SELF_TEST: no T203_*.pdf under cache/pdfs", file=sys.stderr)
        return 1
    all_ok = True
    for p in pdfs:
        text, meta = extract_text(p)
        ok = len(text) >= min_chars
        all_ok = all_ok and ok
        print(
            json.dumps(
                {"file": p.name, "pages": meta["page_count"], "chars": len(text), "ok": ok},
                ensure_ascii=False,
            )
        )
    return 0 if all_ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", type=Path, help="Single PDF path (absolute or under repo)")
    ap.add_argument("--from-status", action="store_true", help="Use pdf_cached rows from paper_reading_status")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--min-chars", type=int, default=1, help="Skip write if fewer chars (noise guard)")
    ap.add_argument("--self-test", action="store_true", help="Verify extraction on first N cached PDFs")
    ap.add_argument("--parse-manifest", action="store_true", help="Append parse_manifest.csv row per success")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    parser_ver = "pymupdf_text_v1"

    if args.pdf:
        pdf_path = args.pdf if args.pdf.is_absolute() else ROOT / args.pdf
        if not pdf_path.is_file():
            print("missing", pdf_path, file=sys.stderr)
            return 1
        text, meta = extract_text(pdf_path)
        rel_pdf = str(pdf_path.relative_to(ROOT))
        out_path = OUT_DIR / (pdf_path.stem + ".txt")
        if len(text) < args.min_chars:
            print("low_text", rel_pdf, len(text), file=sys.stderr)
            return 1
        out_path.write_text(text, encoding="utf-8")
        print(json.dumps({**meta, "out": str(out_path.relative_to(ROOT))}, ensure_ascii=False))
        if args.parse_manifest:
            mid = manifest_id_for_pdf(rel_pdf)
            append_parse_manifest(
                mid, parser_ver, "text_extracted", str(out_path.relative_to(ROOT)), "", "extract_pdf_text.py",
            )
        return 0

    if args.from_status:
        n = 0
        with RS.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        for r in rows:
            if n >= args.limit:
                break
            if (r.get("fulltext_html_status") or "").strip() != "pdf_cached":
                continue
            art = (r.get("fulltext_html_artifact") or "").strip()
            if not art.lower().endswith(".pdf"):
                continue
            pdf_path = ROOT / art
            if not pdf_path.is_file():
                continue
            text, meta = extract_text(pdf_path)
            if len(text) < args.min_chars:
                continue
            out_path = OUT_DIR / (pdf_path.stem + ".txt")
            out_path.write_text(text, encoding="utf-8")
            oid = (r.get("openalex_id") or "").strip()
            print(json.dumps({"openalex_id": oid, **meta, "out": str(out_path.relative_to(ROOT))}, ensure_ascii=False))
            if args.parse_manifest:
                mid = manifest_id_for_pdf(art)
                append_parse_manifest(
                    mid,
                    parser_ver,
                    "text_extracted",
                    str(out_path.relative_to(ROOT)),
                    "",
                    f"extract_pdf_text.py openalex_id={oid}",
                )
            n += 1
        print("extracted", n, "files", file=sys.stderr)
        return 0

    print("use --pdf PATH | --from-status [--limit N] | --self-test", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
