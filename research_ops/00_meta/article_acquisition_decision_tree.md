# Article acquisition decision tree

副标题：何时下载 metadata / 摘要 / XML / TXT / HTML / PDF

## Start
- **Need only bibliographic fields?** → Fetch **metadata** (API). Do not download PDF. `delete_eligibility`: n/a (no file) or delete temp after row ingested.

## Abstract available?
- **Yes, sufficient for triage?** → Store abstract text in `papers_master` / notes; skip full text until promoted.
- **Need full text for extraction?** → Prefer **structured XML/HTML** (Europe PMC, PMC OA) over PDF.

## OA full text route
- **XML/HTML available?** → Download to `cache/fulltext/` → parse → extract → manifest → **delete raw if redownloadable**.

## PDF route (last resort)
- **Only PDF available and license permits?** → `cache/pdfs/` → extract → manifest → **delete** unless `keep_set_manifest` exception.
- **License unclear?** → **Do not download**; record gap in notes and use metadata only.

## Post-parse
- If extraction + hash + manifest complete → set `delete_eligibility=eligible` when `redownloadable=true`.
