# Gitignore policy (repository-safe downloads)

副标题：哪些下载默认不进入版本控制

## Ignored by default
- All files under `research_ops/cache/**` except `.gitkeep` markers.
- Large binary dumps accidentally placed under `parsed/` (see root `.gitignore` patterns).

## Tracked by default
- All `research_ops/**/*.csv` manifests and master tables unless explicitly excluded.
- Markdown memos, skill cards, and policy files under `research_ops/00_meta/` and workstreams.

## Rationale
Agents may download gigabytes of PDFs/HTML; git is for **structured assets and provenance**, not raw corpora.

## Exceptions
- Curated high-value artifacts explicitly listed in `manifests/keep_set_manifest.csv` require a **human or policy decision** before adding to git.
