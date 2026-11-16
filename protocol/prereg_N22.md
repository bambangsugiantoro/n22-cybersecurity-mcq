# Pre-registration — N22 (v1.0, REGISTERED — see section 14)

Working title: Do multiple-choice cybersecurity benchmarks measure knowledge? Option-order, question-free and canonical-order checks on CyberMetric and SecQA

Target venue: JOIV (fallback: other Scopus-indexed informatics journals). Status: registered v1.0 (authors approved the text on 16 Nov 2026, message "daftar"); the SHA-256 block in section 14 was filled in before any confirmatory run. Pilot (section 9) is not confirmatory. No human participants. Scripts and text written with the help of Claude (Anthropic).

## 1. Relation to other work by the same authors
N22 shares nothing with N13 (HPC placement) or the deepfake papers (N10/N19/N20). It uses the HPC cluster only as a GPU host.

## 2. Motivation and gap (to be verified by a full literature review before submission)
Multiple-choice (MCQ) benchmarks are the standard way to report cybersecurity ability of LLMs (CyberMetric, SecQA and others). Known concerns: MCQ scores depend on option position (Zheng et al., ICLR 2024), and a recent audit of cyber-LLM benchmarks (arXiv 2609.08765) questions reliability. Preliminary searches (16 Nov 2026) found no study that applies one fixed battery of order, question-free and canonical-order checks to CyberMetric and SecQA with open models on identical hardware. Absence from a search is not proof of absence; the novelty claim is therefore limited to "a pre-registered, reproducible battery applied to these two benchmarks" until the review is done.

## 3. Research questions
RQ1 Does accuracy change when the options are rotated?
RQ2 How many items are answered correctly under all four rotations, compared with plain accuracy?
RQ3 Can items be answered above chance without the question text?
RQ4 Do models assign higher likelihood to the published option order than to permuted orders (a memorisation signal)?

## 4. Platform
One node of the HPC cluster (hpc.uin-suka.ac.id, partition l40s): 1 x NVIDIA L40S (46 GB), 8 CPU cores, 32 GB RAM, Slurm job with --gres=gpu:1 (non-exclusive; other jobs may run). Software: PyTorch 2.8 container of the cluster, transformers 5.23, accelerate 1.15 (user install). Versions and model commit hashes are written to the registration block. bfloat16, no sampling, deterministic scoring.

## 5. Materials
- Primary benchmark: CyberMetric-2000 (GitHub cybermetric/CyberMetric, commit 294662b03be73a9c7c73918f687882c1ba637c47; file CyberMetric-2000-v1.json, SHA-256 28129b8d5cae82a80ba76bb31eb029e1238d1e348e6d0e85f44526583e27cd03; four options A-D, one solution). CyberMetric-500 is NOT a subset of the 2000 set (only 130 of 500 questions occur in it), so only the 2000 set is used.
- Replication benchmark: SecQA v1 test (110 items) and v2 test (100 items) (HF zefang-liu/secqa, revision d00a07484283be5602e2bae36dbefdaaf555a9fb), converted from CSV by secqa_to_json.py (SHA-256 d5e4adbae07411e95eb01234cf0908ae7216fd101fd5478eaa91c20b85e551a9). Each test split is analysed separately and descriptively: with about 100 items per split the tests are low-powered and are not used to overturn the primary verdicts.
- Models (instruction-tuned, open): Qwen/Qwen2.5-7B-Instruct, microsoft/Phi-3.5-mini-instruct. Revisions: Qwen2.5-7B-Instruct a09a35458c702b33eeacc393d103063234e8bc28; Phi-3.5-mini-instruct 2fe192450127e6a83f7441aef6e3ca586c338b77.
Items with fewer or more than four options, empty options or duplicate options are excluded and listed.

## 6. Design
Scoring: zero-shot prompt (fixed template in the script, hashed in the registration block); the model's score for each option is the next-token log-probability of the option letter after the prompt; prediction = argmax over A-D. One forward pass per prompt, no generation.
Conditions per item:
- R0 published order; R1, R2, R3 cyclic rotations of the options (the gold option visits each position exactly once across R0-R3).
- Q0 question removed: only the four options are shown, with the same instruction to pick the most plausible correct statement; published order.
- C canonical-order test: sum of token log-likelihood of the full item text (question plus options with letters) in the published order versus the mean over the three cyclic rotations and the reversed order (four alternatives).
Items are processed in a fixed order (seed 2211); results are deterministic given hardware, so no repetition across seeds; an identical re-run on a second job is used as a determinism check (section 10).

## 7. Measurements
Primary: per model and benchmark, accuracy in R0-R3, all-four-correct rate, Q0 accuracy, share of items with loglik(published) greater than loglik(mean of alternatives).
Exploratory (not tested): distribution of predicted letters, accuracy by gold position, per-topic breakdown, agreement between the two models, item-level overlap of errors.

## 8. Hypotheses and decision rules (fixed before any confirmatory run)
Bootstrap 95% intervals over items (4,000 resamples, seed 2211). Holm correction over H1-H4 within each model on the primary benchmark; the other model and SecQA are reported as replications with the same rules.
H1 (option-order sensitivity) accuracy range across R0-R3 is at least 3 percentage points AND Cochran's Q test across the four rotations gives p < 0.05 (Holm).
H2 (inconsistency) accuracy(R0) minus all-four-correct rate is at least 10 percentage points; supported if the lower interval bound is at least 10.
H3 (answerable without question) accuracy(Q0) has a lower interval bound above 0.30 (chance 0.25).
H4 (canonical order) share of items with loglik(published) greater than the mean of alternatives is at least 0.55 with lower bound above 0.5 (exact binomial p < 0.05, Holm).
Verdicts: Supported / Partly (point estimate on the right side, interval crosses the threshold) / Not supported. Thresholds are not changed after the fact. A negative result is reported as such.

## 9. Pilot (not confirmatory)
CyberMetric-80 with Qwen2.5-7B-Instruct, all conditions, to check that the script runs, token handling of letters is correct (single-token letters), memory fits and run time is known. Pilot data are excluded from the confirmatory analysis. Pilots done on 16 Nov 2026 (before registration): Qwen2.5-7B-Instruct, CyberMetric-80: mean letter probability mass 1.000, no template change; Phi-3.5-mini-instruct, CyberMetric-80: mean mass 1.000, no template change. Run time about 16 s and 12 s for 80 items. Pilot accuracies are not interpreted. If the pilot shows the letter tokens are not single tokens or the prompt template yields near-zero probability mass on A-D (mean mass < 0.9), the template is fixed before registration and the change is described here.

## 10. Exclusions and handling
Excluded: malformed items (section 5). Runs are repeated once on a separate job to check determinism; if predictions differ in more than 0.5% of items the differences are reported and the first run is kept. No other exclusion.

## 11. Operating rules
One GPU, non-exclusive Slurm job, time limit 2 h. No system settings are changed. Nothing is run on the node outside these jobs. Estimated total GPU time under 1 h.

## 12. Limitations (written in advance)
Two models of 4-8 billion parameters; letter-likelihood scoring is not free-text generation and may differ from generation-based benchmark practice; the memorisation test is a signal, not proof; CyberMetric items were generated with LLM help and then reviewed (per its authors), which may affect Q0 results; results are about these benchmarks and models only.

## 13. Deviation log
(empty — every change after registration is added here with its time stamp, before the affected runs)

## 14. Registration block
Registered: 2026-11-16 15:16 WIB, before any confirmatory run. The SHA-256 of this file as saved is recorded in registration_hashes_N22.txt (a file cannot contain its own hash).
Scripts: n22_eval.py SHA-256 abc88aa77a595d55cf78c3032d8450e84b55eb44ac3385b95d9aade08124f9db (contains both prompt templates); secqa_to_json.py d5e4adbae07411e95eb01234cf0908ae7216fd101fd5478eaa91c20b85e551a9; n22_analyze.py hash in registration_hashes_N22.txt.
Libraries: PyTorch 2.8.0a0+34c6371d24.nv25.08 (cluster container), transformers 5.23.0, accelerate 1.15.0, safetensors 0.8.0, tokenizers 0.23.x. Models and data: sections 5.
