# SCORING_POLICY

副标题：论文、数据集、趋势、想法与 scaling-fit 的统一评分维度

## Papers (0–5 each; document in notes)
- **Novelty / advance**: method or evidence advance over clear baselines.
- **Clinical or scientific impact potential**: plausible path to patients or to important science questions.
- **Evidence strength**: prospective, external validation, multicenter, reader study, preregistration.
- **Reproducibility signal**: code, data availability, clarity of splits and metrics.
- **Transferability**: relevance to medical imaging, multimodal medicine, or agentic discovery loops.

## Datasets & challenges
- **Label quality and granularity**
- **License and access friction**
- **Community usage** (citations, leaderboard activity)
- **Task alignment** with clinical or method frontier needs

## Trends (frontier radar)
- **Empirical depth**: benchmarks vs position pieces.
- **Tool use and evaluability**: can we build a cheap test?
- **Hype risk**: marketing language vs measurable capability (tie to `anti_hype_checks.csv`).

## Ideas & hypotheses
- **Scalability of verification**: can scaling data/compute improve the answer?
- **Data source clarity**
- **Reviewer risk** (what would kill the claim?)
- **Cheap test availability**

## Scaling-fit problems (clinical pull)
- **Information burden**: volume/complexity that humans struggle to integrate.
- **Retrieval / synthesis fit**: whether RAG, agents, or literature-scale methods plausibly help.
- **Safety and governance risk**: autonomy boundaries and oversight needs.
