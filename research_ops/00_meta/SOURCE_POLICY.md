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

## Current research focus (operational)
- Prioritize **research literature** for **medical + AI** discovery work:
  - medical imaging AI
  - clinical AI / translational AI
  - multimodal biomedical AI
  - agent / retrieval / scientific-discovery methods that plausibly transfer to medicine
- Prefer sources that help answer:
  - where the field is moving
  - which tasks are saturated vs still open
  - which benchmarks, datasets, and validation gaps define the frontier

## Case report policy (current)
- **Do not proactively fetch case-report full text by default.**
- Case reports may remain a **discovery signal** for:
  - rare disease / atypical presentation trend detection
  - hypothesis generation
  - identifying long-tail evaluation opportunities
- Default handling for case reports:
  1. keep metadata / registry-level signals only
  2. do not expand to bulk full-text crawling unless explicitly requested
  3. do not let case-report harvesting compete with the main literature spine

## Full-text policy by source type
- Prefer **OpenAlex / Europe PMC / PMC OA / Crossref** for metadata, OA routing, and structured full text.
- For publisher-hosted landing pages, treat direct fetch as **opportunistic**, not guaranteed:
  - high-friction publishers often block scripted PDF/landing fetches
  - when a reliable API / PMC route exists, use that instead of direct site fetches
- When the goal is **trend / gap finding**, metadata + abstract coverage is often more valuable than forcing brittle PDF fetches.

## Preprint / arXiv scope cleanup (current)
- **Default: do not bulk-fetch full text from arXiv / preprint sources.**
- Keep preprints primarily as:
  - metadata signals
  - recent-trend candidates
  - title/abstract recall support
- Allow arXiv full-text fallback only when **all** are true:
  1. the item is **recent** (prefer 2024+ unless explicitly overridden)
  2. the primary / publisher-side source is high-value but the正文 cannot be read directly in the current environment
  3. the title (and ideally DOI or other metadata) clearly matches between the publisher record and the arXiv version
- For pure preprint venues, prefer abstract-level analysis first; do not let preprint full text dominate the main reading stack.

## Signal vs noise (default)
- Prefer **structured fields** (title, abstract, affiliations, references) over unstructured scrapes.
- Treat **press releases and secondary blogs** as low priority unless they point to primary artifacts.
