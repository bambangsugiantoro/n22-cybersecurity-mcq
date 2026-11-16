# N22 - hasil ekstensi post-hoc (16 Nov 2026), addendum D1
CyberMetric-2000 (n=2000)
| Model | R0/R1/R2/R3 | Range | H1 | Gap (lo95) | H2 | Q0 (lo95) | H3 | Canon (p Holm) | H4 |
|---|---|---|---|---|---|---|---|---|---|
| Qwen2.5-14B-Instruct | .919/.915/.918/.912 | 0.7 | NOT (holm 1) | 5.6 (4.6) | NOT | .431 (.408) | SUPPORTED | .495 (1) | NOT |
| phi-4 | .917/.902/.898/.910 | 1.9 | NOT (holm .0059, range<3) | 6.9 (5.8) | NOT | .446 (.424) | SUPPORTED | .511 (.168) | NOT |
| OLMo-2-1124-7B-Instruct | .804/.794/.805/.786 | 1.9 | NOT (holm .084) | 14.3 (12.8) | SUPPORTED | .374 (.353) | SUPPORTED | .525 (.024) | NOT (<.55) |
SecQA (range / Q0 / canon): v1 OLMo .9/.573/.545; Q14 0/.645/.564; phi-4 0/.709/.427. v2 OLMo 2.0/.670/.570; Q14 2.0/.720/.570; phi-4 2.0/.750/.540.
Sumber: ~/n22/analysis_N22_ext.txt, results_ext/*.json.
