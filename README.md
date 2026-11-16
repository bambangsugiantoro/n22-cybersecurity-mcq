# N22 - Do cybersecurity multiple-choice benchmarks measure knowledge?

Replication package for: B. Sugiantoro and F. A. Hafizuddin, "Do Cybersecurity Multiple-Choice Benchmarks Measure Knowledge? Option-Order, Question-Free and Canonical-Order Checks on CyberMetric and SecQA" (submitted to JOIV).

## Contents
- `code/n22_eval.py` - scoring (zero-shot chat template, next-token log-probability over A-D; rotations R0-R3, question-free Q0, canonical-order likelihood C).
- `code/n22_analyze.py` - registered analysis (hypotheses H1-H4; bootstrap 4000 resamples, seed 2211; Cochran Q, Holm, exact binomial).
- `code/n22_post.py`, `code/n22_post2.py` - post hoc robustness analyses (addenda D2, D2b).
- `code/secqa_to_json.py` - converts SecQA to the common JSON format.
- `protocol/` - pre-registration (v1.0), addenda D1, D2, D2b, and `registration_hashes_N22.txt` (SHA-256 recorded before the runs).
- `results/` - result summaries; `figures/` - manuscript figures.
- `SHA256SUMS.txt` - SHA-256 of every file in `code/`, `protocol/`, `results/`.

## Data and models (not redistributed)
- CyberMetric-2000-v1: github.com/cybermetric/CyberMetric (commit 294662b0).
- SecQA v1/v2: huggingface.co/datasets/zefang-liu/secqa (revision d00a0748; CC BY-NC-SA 4.0).
- Models (bfloat16, no quantisation): Qwen2.5-7B-Instruct (a09a3545), Phi-3.5-mini-instruct (2fe19245), Qwen2.5-14B-Instruct (cf98f3b3), phi-4 (2db69c1c), OLMo-2-1124-7B-Instruct (470b1fba).

## Environment
One NVIDIA L40S GPU (Slurm, Apptainer, PyTorch + Transformers). No human participants and no personal data.

## Status of the analyses
Qwen2.5-7B and Phi-3.5-mini were registered before any confirmatory run. The three other models (addendum D1) and the option-length and position-neutral analyses (addenda D2, D2b) are post hoc.

## Licence
Code: MIT. Documents, figures and results: CC BY 4.0.
