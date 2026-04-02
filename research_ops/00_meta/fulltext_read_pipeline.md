# Full-text read pipeline (摘要 → OA 全文 HTML → PDF)

Three layers; each layer has its own TODO id and **must** respect `LICENSE_POLICY.md` + manifest-before-delete.

## Layer A — Abstract (OpenAlex)
- **Source**: `GET https://api.openalex.org/works/{W}` → `abstract_inverted_index`
- **Artifact**: `research_ops/parsed/abstracts/openalex_abstracts_YYYY.jsonl` (one JSON object per line)
- **FTS index** (T207): `research_ops/parsed/abstracts/abstract_index.sqlite` — rebuild via `scripts/build_abstract_fts.py` (gitignored)
- **Registry**: `paper_reading_status.csv` → `abstract_status=ingested|missing|error`

## Policy gate (T212)
- Rows with **no** usable `oa_url_cached` after enrichment: call OpenAlex `open_access.is_oa`. If **`false`**, set `fulltext_html_status=skipped_policy` (avoid blind publisher fetches). Script: `scripts/t212_openalex_policy_gate.py`.

## Europe PMC full text (T205)
- **DOI → search** (`Europe PMC REST`) → **`/{pmcid}/fullTextXML`** when `inEPMC=Y`.
- **Registry**: `research_ops/02_papers/paper_epmc_fulltext_pilot.csv`
- **Script**: `scripts/fetch_epmc_fulltext_pilot.py`

## OA URL enrichment (T206)
- **Crossref** `works/{doi}` `link[]` (polite `User-Agent` with mailto): `scripts/enrich_oa_url_crossref.py`
- **Europe PMC** search by DOI → PMC landing (when `inEPMC=Y`): `scripts/enrich_oa_url_epmc.py`
- **OpenAlex** `oa_url` only (often empty when already missing): `scripts/enrich_oa_url_openalex.py`

## Layer B — OA full text (HTML/XML landing page)
- **When**: `open_access.is_oa` and `primary_location.landing_page_url` (or Europe PMC / Unpaywall later)
- **Cache**: `research_ops/cache/fulltext/` (gitignored); PDF-shaped responses → `research_ops/cache/pdfs/T203_*.pdf` (see **D-006**)
- **Manifest**: `download_manifest.csv` before any delete
- **Registry**: `fulltext_html_status` (`ingested` | `pdf_cached` | `error` | …)
- **Pilot script**: `scripts/pilot_fetch_oa_html.py` (T202; uses `oa_url_cached` from `paper_reading_status.csv`)
- **Batch script**: `scripts/batch_fetch_oa_html.py` (T203; arXiv `/abs/` fallback, `Accept: text/html`, `--skip-pdf-primary` / `--retry-errors`)

## Layer C — PDF
- **When**: explicit OA + policy allow; **manifest + hash** mandatory
- **Cache**: `research_ops/cache/pdfs/` (gitignored)
- **Registry**: `pdf_status`
- **Text extraction**: `scripts/extract_pdf_text.py` — **PyMuPDF** `page.get_text("text")` → `research_ops/parsed/pdfs/<stem>.txt` (gitignored). Run `pip install -r requirements.txt` first. Flags: `--self-test` (sanity on cached PDFs), `--from-status --limit N` (rows with `fulltext_html_status=pdf_cached`). Optional `--parse-manifest` appends `parse_manifest.csv`. **Scanned PDFs** need a separate OCR path (not in this script).

## Section extraction pilot (T210)
- **Naive path** (no GROBID): `scripts/pilot_section_extract_html.py` — strips tags, regex-splits on common headings → `parsed/section_extractions_pilot.jsonl` (gitignored).
- **GROBID** remains optional when a local service or policy allows.

## Year rollout
Process **2026 → 2025 → 2024 → …** so “最近的 paper”优先读完 Layer A，再向下扩展 B/C。

## Monthly maintenance (T208)
After new rows land in `papers_master.csv` for calendar month **YYYY-MM**:
1. Run `python3 scripts/harvest_openalex_monthly.py` (or equivalent) to append works.
2. Run `python3 scripts/ingest_openalex_abstracts.py --years YYYY` for the new publication year(s) touched by those rows (or full year if mixed).
3. Optionally refresh FTS: `python3 scripts/build_abstract_fts.py` (rebuilds `abstract_index.sqlite`).
4. Append RUN_LOG with row deltas and any API errors.
