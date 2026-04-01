# Skill card template (T079)

Use one file per skill under `skill_cards/` named `SK###_short_name.md`.

## Required sections
1. **Name** — short verb-noun title  
2. **Skill ID** — `SK###`  
3. **Inputs** — structured inputs the skill expects  
4. **Outputs** — artifacts produced (paths, CSV rows, memos)  
5. **Scope** — in-scope vs out-of-scope boundaries  
6. **Procedure** — numbered steps (tool calls, APIs, file writes)  
7. **Failure modes** — what breaks and how it surfaces  
8. **Validation** — promotion test IDs from `promotion_tests.csv`  
9. **Provenance** — which policy/docs govern the skill (`LICENSE_POLICY`, `SOURCE_POLICY`, …)

## Promotion rule
No skill is “live” until all linked `promotion_tests` pass on a fixed benchmark snapshot.
