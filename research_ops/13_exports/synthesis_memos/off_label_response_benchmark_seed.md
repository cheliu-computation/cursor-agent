# Off-label drug response mining — benchmark seed (T089)

**Task**: Given case-report narratives, extract (drug, indication, response class) triplets where indication is off-label vs drug label.

**Seed protocol**
1. Filter `case_reports_master` for drug + response keywords.
2. Human label 50 triplets for precision@k evaluation.
3. Negative sampling from unrelated case abstracts.

**Data**: Europe PMC OA case harvest (T062).
