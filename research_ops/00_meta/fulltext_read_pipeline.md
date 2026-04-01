# Full-text read pipeline (摘要 → OA 全文 HTML → PDF)

Three layers; each layer has its own TODO id and **must** respect `LICENSE_POLICY.md` + manifest-before-delete.

## Layer A — Abstract (OpenAlex)
- **Source**: `GET https://api.openalex.org/works/{W}` → `abstract_inverted_index`
- **Artifact**: `research_ops/parsed/abstracts/openalex_abstracts_YYYY.jsonl` (one JSON object per line)
- **Registry**: `paper_reading_status.csv` → `abstract_status=ingested|missing|error`

## Layer B — OA full text (HTML/XML landing page)
- **When**: `open_access.is_oa` and `primary_location.landing_page_url` (or Europe PMC / Unpaywall later)
- **Cache**: `research_ops/cache/fulltext/` (gitignored)
- **Manifest**: `download_manifest.csv` before any delete
- **Registry**: `fulltext_html_status`
- **Pilot script**: `scripts/pilot_fetch_oa_html.py` (T202; uses `oa_url_cached` from `paper_reading_status.csv`)

## Layer C — PDF
- **When**: explicit OA + policy allow; **manifest + hash** mandatory
- **Cache**: `research_ops/cache/pdfs/` (gitignored)
- **Registry**: `pdf_status`

## Year rollout
Process **2026 → 2025 → 2024 → …** so “最近的 paper”优先读完 Layer A，再向下扩展 B/C。
