# Rare disease retrieval benchmark seed (T067)

## Definition
- **Corpus**: first 200 OA case reports from Europe PMC (`case_reports_master.csv`).
- **Positives**: cases whose title/abstract contains `rare` or `orphan` (weak label).
- **Negatives**: random pool from non-matching cases in the same harvest.

## Limitations
- Labels are **noisy**; upgrade with ICD/ORPHA codes from full text or PubTator.

## Next steps
- Add human adjudication column.
- Expand with explicit ORDO IDs when available.
