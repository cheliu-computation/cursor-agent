#!/usr/bin/env python3
"""T207: build FTS5 sqlite over OpenAlex abstract JSONL files."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ABS_DIR = ROOT / "research_ops/parsed/abstracts"
DB_PATH = ROOT / "research_ops/parsed/abstracts/abstract_index.sqlite"


def main() -> int:
    ABS_DIR.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE VIRTUAL TABLE abstracts USING fts5(
            openalex_id UNINDEXED,
            year UNINDEXED,
            paper_id UNINDEXED,
            title,
            abstract,
            tokenize = 'porter unicode61'
        )
    """)

    files = sorted(ABS_DIR.glob("openalex_abstracts_*.jsonl"))
    n = 0
    for fp in files:
        with fp.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    o = json.loads(line)
                except json.JSONDecodeError:
                    continue
                oid = (o.get("openalex_id") or "").strip()
                pid = (o.get("paper_id") or "").strip()
                yr = str(o.get("year") or "").strip()
                title = (o.get("title") or "").strip()
                abstract = (o.get("abstract") or "").strip()
                con.execute(
                    "INSERT INTO abstracts(openalex_id, year, paper_id, title, abstract) VALUES (?,?,?,?,?)",
                    (oid, yr, pid, title, abstract),
                )
                n += 1

    con.commit()
    # smoke query
    cur = con.execute(
        "SELECT COUNT(*) FROM abstracts WHERE abstracts MATCH ?",
        ("segmentation",),
    )
    hit = cur.fetchone()[0]
    con.close()
    print("rows", n, "db", DB_PATH.relative_to(ROOT), "sample_match_segmentation", hit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
