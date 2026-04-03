#!/usr/bin/env python3
"""Build a first-pass trend/gap layer from existing research_ops tables."""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PM = ROOT / "research_ops/02_papers/papers_master.csv"
FP = ROOT / "research_ops/14_frontier/frontier_papers.csv"
CS = ROOT / "research_ops/09_clinical/clinical_signal.csv"
SFS = ROOT / "research_ops/18_clinical_pull/scaling_fit_scores.csv"
PP = ROOT / "research_ops/18_clinical_pull/pain_points.csv"
TS = ROOT / "research_ops/14_frontier/trend_signals.csv"
MEMO = ROOT / "research_ops/13_exports/synthesis_memos/trend_gap_summary_001.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def year_int(row: dict[str, str]) -> int:
    try:
        return int((row.get("year") or "").strip())
    except ValueError:
        return -1


def count_recent(rows: list[dict[str, str]], predicate) -> int:
    return sum(1 for r in rows if year_int(r) >= 2023 and predicate(r))


def count_window(rows: list[dict[str, str]], predicate, start: int = 2019, end: int = 2025) -> int:
    return sum(1 for r in rows if start <= year_int(r) <= end and predicate(r))


def modality_counts(rows: list[dict[str, str]]) -> Counter:
    ctr = Counter()
    for r in rows:
        for token in (r.get("tags_modality") or "").split("|"):
            token = token.strip()
            if token:
                ctr[token] += 1
    return ctr


def method_counts(rows: list[dict[str, str]]) -> Counter:
    ctr = Counter()
    for r in rows:
        for token in (r.get("tags_method") or "").split("|"):
            token = token.strip()
            if token:
                ctr[token] += 1
    return ctr


def venue_counts(rows: list[dict[str, str]]) -> Counter:
    ctr = Counter()
    for r in rows:
        venue = (r.get("venue") or "").strip()
        if venue:
            ctr[venue] += 1
    return ctr


def write_signals(rows: list[dict[str, str]]) -> None:
    fieldnames = ["signal_id", "topic", "strength", "source_refs", "anti_hype_notes", "notes"]
    with TS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def write_memo(lines: list[str]) -> None:
    MEMO.parent.mkdir(parents=True, exist_ok=True)
    MEMO.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    papers = read_csv(PM)
    frontier = read_csv(FP)
    clinical = read_csv(CS)
    scaling = read_csv(SFS)
    pain_points = read_csv(PP)

    papers_main = [r for r in papers if 2019 <= year_int(r) <= 2025]
    papers_recent = [r for r in papers if year_int(r) >= 2023]
    venue_ctr = venue_counts(papers_main)
    modality_ctr = modality_counts(papers_main)
    method_ctr = method_counts(papers_main)

    signals: list[dict[str, str]] = []
    signal_idx = 1

    def add_signal(topic: str, strength: str, refs: list[str], anti_hype: str, notes: str) -> None:
        nonlocal signal_idx
        signals.append(
            {
                "signal_id": f"TS{signal_idx:03d}",
                "topic": topic,
                "strength": strength,
                "source_refs": "; ".join(refs)[:400],
                "anti_hype_notes": anti_hype[:300],
                "notes": notes[:300],
            }
        )
        signal_idx += 1

    # Signal 1: domain-core imaging corpus is already large enough.
    add_signal(
        "domain_core_medical_imaging_is_large",
        "high",
        [
            f"papers_master 2019-2025={len(papers_main)}",
            f"Medical Image Analysis={venue_ctr.get('Medical Image Analysis', 0)}",
            f"TMI={venue_ctr.get('IEEE Transactions on Medical Imaging', 0)}",
            f"Radiology={venue_ctr.get('Radiology', 0)}",
        ],
        "Volume alone does not imply solved clinical value; inspect validation/workflow evidence separately.",
        "Core imaging venues already support trend analysis without expanding to year-by-year full crawl.",
    )

    # Signal 2: preprint signal remains large even after full-text narrowing.
    preprint_recent = count_recent(
        papers,
        lambda r: "preprint" in (r.get("tags_modality") or "") or "arxiv" in (r.get("venue") or "").lower(),
    )
    add_signal(
        "preprint_signal_large_but_fulltext_filtered",
        "medium",
        [
            f"preprint_recent_2023plus={preprint_recent}",
            f"preprint_broad={modality_ctr.get('preprint_broad', 0)}",
            f"preprint_biorxiv={modality_ctr.get('preprint_biorxiv', 0)}",
        ],
        "Use preprints as recency radar, not as the default evidence base for gap claims.",
        "Recent preprint metadata remains useful for frontier monitoring, but full-text is no longer a default path.",
    )

    # Signal 3: high-value clinical venues are materially present.
    clinical_hi = sum(
        venue_ctr.get(v, 0)
        for v in [
            "Nature Medicine",
            "npj Digital Medicine",
            "The Lancet Digital Health",
            "Radiology",
            "Radiology Artificial Intelligence",
        ]
    )
    add_signal(
        "clinical_high_value_venues_present",
        "high",
        [
            f"clinical_high_value_rows={clinical_hi}",
            f"clinical_signal_rows={len(clinical)}",
        ],
        "Metadata and abstracts from JAMA/NEJM-like sources are valuable even when direct publisher full-text is blocked.",
        "Clinical problem framing can already be derived from current venue coverage plus the seeded clinical_signal table.",
    )

    # Signal 4: agent/scientific-discovery layer is visible but still sparse.
    agent_recent = count_recent(
        papers,
        lambda r: "agents" in (r.get("tags_method") or "") or "agent" in (r.get("title") or "").lower(),
    )
    add_signal(
        "agentic_medical_signal_emerging_but_small",
        "medium",
        [
            f"frontier_papers={len(frontier)}",
            f"agent_like_recent_rows={agent_recent}",
        ],
        "Many agent papers are framework-heavy; separate operational clinical value from benchmark or simulation-only claims.",
        "Agentic/LLM signals exist, but the layer is much smaller than the mainstream medical-AI literature spine.",
    )

    # Signal 5: scaling-fit problems are already seeded before full trend analysis.
    add_signal(
        "scaling_fit_problem_layer_seeded",
        "medium",
        [
            f"pain_points={len(pain_points)}",
            f"scaling_fit_scores={len(scaling)}",
        ],
        "Current scaling-fit rows are heuristic seeds; they still need alignment to literature density and validation evidence.",
        "A usable bridge already exists from literature trends to operational clinical problems.",
    )

    # Signal 6: method frontier is heavily tilted toward FM/generative/deep learning.
    add_signal(
        "foundation_and_deep_learning_dominate_recent_tags",
        "medium",
        [
            f"deep_learning={method_ctr.get('deep_learning', 0)}",
            f"foundation_models={method_ctr.get('foundation_models', 0)}",
            f"generative={method_ctr.get('generative', 0)}",
        ],
        "Tag volume can overstate novelty; full-text audit should test whether validation and deployment maturity keep pace.",
        "Recent corpora are concentrated in foundation/deep-learning themes, suggesting a hype-risk layer worth explicit checks.",
    )

    write_signals(signals)

    top_venues = venue_ctr.most_common(10)
    top_methods = method_ctr.most_common(8)
    top_modalities = modality_ctr.most_common(8)

    memo_lines = [
        "# Trend and gap summary 001",
        "",
        "## Scope used",
        f"- Main literature window: 2019-2025",
        f"- Papers in main window: {len(papers_main)}",
        f"- Recent papers (2023+): {len(papers_recent)}",
        f"- Frontier seed papers: {len(frontier)}",
        f"- Clinical signal rows: {len(clinical)}",
        f"- Scaling-fit score rows: {len(scaling)}",
        "",
        "## Top venues in the current spine",
    ]
    memo_lines.extend([f"- {venue}: {count}" for venue, count in top_venues])
    memo_lines.extend(
        [
            "",
            "## Top modality tags",
        ]
    )
    memo_lines.extend([f"- {tag}: {count}" for tag, count in top_modalities])
    memo_lines.extend(
        [
            "",
            "## Top method tags",
        ]
    )
    memo_lines.extend([f"- {tag}: {count}" for tag, count in top_methods])
    memo_lines.extend(
        [
            "",
            "## First-pass gap interpretation",
            "- The corpus is already large enough to support trend work without year-by-year full-crawl expansion.",
            "- High-value clinical venues are present, but direct publisher-page full text is often blocked; trend work should stay metadata/abstract-first.",
            "- Preprints remain useful for frontier recency, but should not dominate evidence-weighted conclusions.",
            "- Agentic/LLM medical papers exist as a visible frontier layer, yet they are still sparse compared with mainstream medical-AI literature.",
            "- The strongest immediate opportunity is to connect current venue/method trends to the existing scaling-fit and pain-point tables.",
        ]
    )
    write_memo(memo_lines)
    print("trend_signals_rows", len(signals), "memo", MEMO.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
