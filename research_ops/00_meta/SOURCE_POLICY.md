# SOURCE_POLICY

副标题：来源分层、优先级与信号/噪声

## Layers (summary)
- **A — Domain core**: MICCAI, MIDL, IPMI, ISBI, MedIA, TMI, Radiology, Radiology: AI — high signal for medical imaging AI problems and benchmarks.
- **B — Method frontier**: NeurIPS, ICML, ICLR, CVPR, ICCV, ECCV — transferable methods; higher noise for clinical fit unless filtered.
- **C — High-impact science/clinical**: Nature family, Cell, JAMA, NEJM, Lancet Digital Health — problem importance and evidence norms; access friction variable.
- **D — Data & tasks**: Grand Challenge, TCIA, PhysioNet, ClinicalTrials.gov, OpenAlex — infrastructure and grounding.
- **E — Repro detail**: GitHub, supplements, model/dataset cards — failure modes and implementation truth.
- **F — Frontier agentic**: arXiv, OpenReview, bioRxiv/medRxiv — fast-moving; validate against peer-reviewed when claiming maturity.
- **G — Literature infrastructure**: Europe PMC, PMC OA, PubMed, PubTator, SemMedDB — bulk metadata and text mining.
- **H — Case narrative**: OA case reports and figure-rich cases where license allows reuse.

## Fetch priority
1. Official APIs and open-access bulk endpoints  
2. Metadata and structured XML/HTML full text  
3. Plain text / HTML snapshots  
4. PDF only when necessary for extraction not available elsewhere  

## Signal vs noise (default)
- Prefer **structured fields** (title, abstract, affiliations, references) over unstructured scrapes.
- Treat **press releases and secondary blogs** as low priority unless they point to primary artifacts.
