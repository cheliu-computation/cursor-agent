# What counts as real agent self-evolution

副标题：可审计边界（对齐 `SCALABLE_DISCOVERY_AGENT.md` §4.7）

## Counts as real (auditable) self-evolution
Changes that are **stored as artifacts**, **versioned**, and **validated** against explicit tests or metrics:

- Prompt / instruction templates checked into the repo with changelog.
- Tool recipes and retrieval configurations with replay traces.
- Extraction schemas, scoring rubrics, and checklists with before/after inter-rater or gold-set metrics.
- Skill cards plus **promotion tests** that must pass before the skill is “live”.
- Reflection logs that produce **actionable** updates to policies (not vague “try harder”).

## Does not count
- Undocumented drift in free-form chat behavior.
- “It feels smarter” without benchmark or task regression checks.
- Self-modifying weights or code in production paths without holdout evaluation and governance.
- Renaming or rephrasing without measurable delta on fixed tasks.

## Minimum evidence bar
For any claimed upgrade, record: **what changed**, **which files**, **which tests/metrics**, **date**, and **rollback path**.
