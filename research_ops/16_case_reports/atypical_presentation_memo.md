# Atypical presentation clustering opportunities (T068)

## Observed patterns in first 200 OA Europe PMC case abstracts (weak signals)
- **Vague onset + multi-system**: fatigue, fever, weight loss co-occurring suggests broad differential; clustering may separate infection vs malignancy vs autoimmune buckets if more structured phenotypes are extracted.
- **Imaging-first presentations**: cases where diagnosis hinges on a single modality finding; good candidates for multimodal figure+caption mining (T066 follow-up).
- **Laboratory outlier driven**: extreme lab values as presenting complaint; useful for anomaly detection benchmarks.

## Recommended next extraction
- Parse HPO terms via PubTator Central or Europe PMC annotations.
- Build patient embedding from (age, sex, phenotypes) only after HPO normalization.

## Risk
Title/abstract-only clustering overfits publication bias (dramatic cases overrepresented).
