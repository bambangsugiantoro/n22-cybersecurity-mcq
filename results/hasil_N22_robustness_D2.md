# N22 - D2/D2b robustness results (post hoc, 16 Nov 2026). Source: ~/n22/post/*.json, post/post2_longest.json on the cluster.
Gold-position share: CyberMetric-2000 .25/.25/.25/.25; SecQA v1 .191/.291/.255/.264; SecQA v2 .21/.31/.27/.21.
Model-free rule (longest option correct): CyberMetric .406 (shortest .178); SecQA v1 .609 (.082); v2 .770 (.100).
Question-free accuracy, mean over 4 rotations (prompt A [95% CI] / prompt B):
| Model | CyberMetric | SecQA v1 | SecQA v2 |
|---|---|---|---|
| Qwen2.5-7B | .418 [.402,.436] / .423 | .682 [.609,.757] / .693 | .772 [.705,.840] / .715 |
| Phi-3.5-mini | .404 [.388,.419] / .421 | .707 [.639,.775] / .707 | .730 [.658,.800] / .728 |
| Qwen2.5-14B | .426 [.410,.443] / .446 | .680 [.607,.752] / .709 | .745 [.673,.815] / .738 |
| phi-4 | .437 [.420,.455] / .433 | .734 [.661,.805] / .711 | .767 [.690,.840] / .767 |
| OLMo-2-7B | .375 [.361,.389] / .390 | .589 [.525,.652] / .607 | .660 [.593,.730] / .698 |
D2b (CyberMetric, published-order Q0, registered prompt): Q0 | longest correct / Q0 | longest wrong / share of Q0-correct coinciding with longest-correct:
Qwen7B .490/.354 [.326,.380]/.487; Phi .489/.374 [.347,.402]/.472; Qwen14B .494/.388 [.359,.416]/.465; phi-4 .527/.391 [.364,.417]/.480; OLMo .435/.332 [.306,.359]/.472.
R0 accuracy when longest correct / wrong: Qwen7B .910/.866; Phi .899/.824; Qwen14B .929/.912; phi-4 .932/.907; OLMo .845/.776.
Hashes: n22_post.py 262f04ebc5396959ca53ac268730de6b84b0e6c82cc1fe00d5f6128897958ead; n22_post2.py 5e0ad7b0eb5f42b6...(prefix); addendum D2 d5f4754e9ab9f3cf...; D2b d5e1e39383a27d40...
Note: CI for prompt B and bootstrap details are in the json files; the SecQA gold-position share is not uniform.
