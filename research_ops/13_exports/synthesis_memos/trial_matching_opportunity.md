# Trial matching opportunity memo (T093)

**Problem**: Manual screening of trials vs patient notes (pain point PP009).

**Data**: `trials_master.csv` + EHR note surrogates.

**Scaling fit**: High — structured eligibility criteria + NLP over notes.

**Cheap test**: Rule-based matcher on 30 synthetic patients (hypothesis H004 / CT004).

**Risks**: Outdated trial status; missing criteria fields in CT.gov JSON.
