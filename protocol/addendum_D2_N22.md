# Addendum D2 - N22 (post-hoc robustness analyses after internal peer review)
Written 16 Nov 2026 (17:15 WIB), after all registered (v1.0) and extension (D1) results were seen, before any D2 run.
Motivation (internal reviewer comments): (a) question-free accuracy was computed with options in published order only, so a gold-position prior could inflate it; (b) one prompt wording; (c) no trivial-heuristic baseline.
Analyses (script n22_post.py, all five models, CyberMetric-2000, SecQA v1/v2):
1. Gold-position share per benchmark.
2. Heuristic baselines without any model: choose the longest option; choose the shortest option.
3. Question-free accuracy averaged over the four cyclic rotations (position-neutral) under prompt A (the registered wording) and prompt B (a paraphrase); bootstrap 95% CI over items (4000, seed 2211); also the share of items correct under all four rotations.
No decision rule of H1-H4 is changed. These results are exploratory and are labelled post-hoc in the paper.
