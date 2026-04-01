# SK010 — Clinical signal triage from titles

- **Inputs**: `papers_master` rows with clinical journal `source_batch`  
- **Outputs**: `clinical_signal.csv` heuristic rows  
- **Scope**: Title/abstract snippets only until upgraded with OpenAlex abstracts  
- **Failure modes**: Misclassified endpoints; overfitting to buzzwords  
- **Validation**: PT-CLIN-001  
- **Provenance**: `SCORING_POLICY.md`
