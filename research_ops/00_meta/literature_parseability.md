# Literature infrastructure — parseability and reuse

Cross-walk of primary literature sources in `source_registry.csv` (IDs SRC033–SRC037, SRC028, SRC027). Use this to choose **metadata-only**, **full text**, **bulk**, or **annotations** paths.

| Source | Metadata | Full text (OA) | Bulk / dump | Text-mined annotations | Typical license constraint |
|--------|----------|----------------|-------------|------------------------|----------------------------|
| OpenAlex (SRC028) | API JSON | Via linked OA locations | Snapshot / API | No native entity layer | CC0 data; polite pooling |
| PubMed E-utilities (SRC035) | XML/JSON | No (abstracts) | Entrez history / batch | Link-out to PMC | NCBI usage policies |
| Europe PMC (SRC033) | REST | OA subset XML/HTML | REST paging; OA bulk companion | Links to PubTator | Per-article OA license |
| PMC OA Subset (SRC034) | In XML | Yes (OA articles) | FTP bulk | Optional pipeline to PubTator | License field per article |
| PubTator (SRC036) | API | N/A | Bulk bioc downloads | Yes (entities/relations) | NCBI terms |
| SemMedDB (SRC037) | SQL dump | N/A | DB dump | Predicate graph | UMLS attribution required |
| ClinicalTrials.gov (SRC027) | API / XML | Trial text fields | Bulk XML | No | US public domain metadata |

**Reuse rule**: Prefer **metadata + OA XML** over PDF; attach **PubTator / SemMed** only when entity linking is the deliverable.
