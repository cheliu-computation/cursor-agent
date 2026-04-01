# SK008 — Paper–trial link via DOI in CT.gov text

- **Inputs**: CT.gov study JSON, DOI regex, OpenAlex resolver  
- **Outputs**: `paper_trial_links.csv`  
- **Scope**: `cited_in_protocol_text` relation only until full-text confirms  
- **Failure modes**: DOI false positives; OpenAlex miss  
- **Validation**: PT-LINK-001  
- **Provenance**: `DECISIONS.md` D-005
