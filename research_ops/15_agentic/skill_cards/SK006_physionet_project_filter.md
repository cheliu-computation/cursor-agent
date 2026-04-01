# SK006 — PhysioNet published project filter

- **Inputs**: `/api/v1/project/published/` JSON  
- **Outputs**: Filtered rows appended to `datasets_master.csv`  
- **Scope**: Metadata + topics; respect credentialing flags separately  
- **Failure modes**: HTML error page; huge payload memory  
- **Validation**: PT-PHYSIO-001  
- **Provenance**: PhysioNet DUA per project
