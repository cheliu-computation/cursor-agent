# Negative finding extraction checklist (T070)

When reading case full text (or structured discharge summaries), capture **explicit negations** that change the differential.

## Checklist
1. **Symptom negations**: fever absent, no night sweats, denies chest pain.
2. **Exam negations**: no lymphadenopathy, no murmur, cranial nerves intact.
3. **Lab negations**: negative blood cultures, normal troponin, negative D-dimer.
4. **Imaging negations**: no acute infarct, no pneumothorax, no free fluid.
5. **Temporal negations**: symptoms not progressive, no prior similar episodes.

## Encoding
- Store as short phrases in `case_reports_master.negative_findings` (pipe-separated).
- For phenopackets, mirror with `negated_phenotypes` / `negated_hpo_ids` once normalized.

## QA
- Prefer **verbatim clinical negation** over inferred absence.
