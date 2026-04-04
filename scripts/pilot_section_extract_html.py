#!/usr/bin/env python3
"""T210 pilot: naive HTML→text + heuristic section splits (no external GROBID)."""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RS = ROOT / "research_ops/02_papers/paper_reading_status.csv"
OUT = ROOT / "research_ops/parsed/section_extractions_pilot.jsonl"


def strip_html(html: str) -> str:
    html = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    html = re.sub(r"(?is)<style.*?>.*?</style>", " ", html)
    html = re.sub(r"<[^>]+>", " ", html)
    html = re.sub(r"\s+", " ", html)
    return html.strip()


def split_sections(text: str) -> dict[str, str]:
    markers = [
        "abstract", "introduction", "background", "methods", "methodology",
        "results", "discussion", "conclusion", "references",
    ]
    low = text.lower()
    found: list[tuple[int, str]] = []
    for m in markers:
        for mo in re.finditer(rf"\b{re.escape(m)}\b", low):
            found.append((mo.start(), m))
    found.sort()
    out: dict[str, str] = {}
    for i, (pos, name) in enumerate(found):
        end = found[i + 1][0] if i + 1 < len(found) else len(text)
        chunk = text[pos:end].strip()
        if len(chunk) > 80:
            out.setdefault(name, chunk[:8000])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args()

    rows = []
    with RS.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("fulltext_html_status") != "ingested":
                continue
            art = (r.get("fulltext_html_artifact") or "").strip()
            if not art.lower().endswith(".html"):
                continue
            fp = ROOT / art
            if fp.is_file():
                rows.append((r["openalex_id"].strip(), fp))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with OUT.open("w", encoding="utf-8") as jf:
        for oid, fp in rows[: args.limit]:
            raw = fp.read_text(encoding="utf-8", errors="replace")
            text = strip_html(raw)
            sec = split_sections(text)
            obj = {
                "openalex_id": oid,
                "source_html": str(fp.relative_to(ROOT)),
                "plain_char_count": len(text),
                "sections": sec,
                "notes": "T210 naive pilot (regex sections; not GROBID)",
            }
            jf.write(json.dumps(obj, ensure_ascii=False) + "\n")
            n += 1

    print("wrote", n, "->", OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
