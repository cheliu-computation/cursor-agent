# SK007 — GitHub issue mining for repro signals

- **Inputs**: Repo URL, keyword regex, `per_page`  
- **Outputs**: `issue_mining.csv` rows  
- **Scope**: Public repos; unauthenticated rate limits  
- **Failure modes**: 403 rate limit; issue spam; false positives  
- **Validation**: PT-GH-001  
- **Provenance**: GitHub ToS
