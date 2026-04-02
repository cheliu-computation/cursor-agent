# Scripts index

All paths are relative to the repository root. Heavy outputs go to `research_ops/cache/` and selected `research_ops/parsed/` paths (see root `.gitignore`).

## Paper harvest (OpenAlex → `papers_master.csv`)

| Script | Role |
|--------|------|
| `harvest_openalex_monthly.py` | One calendar month per `source_id` (T182). |
| `harvest_openalex_year_slice.py` | One publication year × several journal `source_id`s (T213-style). |

## Abstracts (Layer A)

| Script | Role |
|--------|------|
| `ingest_openalex_abstracts.py` | Fetch `abstract_inverted_index` → JSONL + `paper_reading_status.csv`. |
| `build_abstract_fts.py` | Rebuild `parsed/abstracts/abstract_index.sqlite` (FTS5). |

## OA URLs & policy

| Script | Role |
|--------|------|
| `enrich_oa_url_crossref.py` | Backfill `oa_url_cached` from Crossref `link[]`. |
| `enrich_oa_url_epmc.py` | PMC landing from Europe PMC search by DOI. |
| `enrich_oa_url_openalex.py` | Refresh `oa_url` from OpenAlex (sparse when URL already empty). |
| `t212_openalex_policy_gate.py` | Set `skipped_policy` when `is_oa=false` and no URL. |

## Full text cache (Layer B / PMC / cases)

| Script | Role |
|--------|------|
| `pilot_fetch_oa_html.py` | Small OA HTML/PDF pilot (T202). |
| `batch_fetch_oa_html.py` | Batched OA fetch + arXiv fallbacks (T203/T214). |
| `t204_verify_pdf_cache.py` | SHA256 verify cached PDF vs manifest → `pdf_status`. |
| `extract_pdf_text.py` | PyMuPDF → `.txt` under `parsed/pdfs/` (`--self-test`, `--from-status`). |
| `batch_extract_all_pdfs.py` | All `cache/pdfs/*.pdf` → `.txt` + `pdf_extract_index.csv` + `00_meta/PDF_CORPUS_REPORT.md`. |
| `fetch_epmc_fulltext_pilot.py` | Europe PMC `fullTextXML` for papers (T205). |
| `fetch_case_pmc_fulltext_pilot.py` | Europe PMC `fullTextXML` for case reports (T211). |

## Post-fetch utilities

| Script | Role |
|--------|------|
| `append_layerb_errors_to_retry_queue.py` | Push Layer B errors into `manifests/retry_queue.csv`. |
| `pilot_section_extract_html.py` | Naive HTML→text section split (T210 pilot; output gitignored). |
