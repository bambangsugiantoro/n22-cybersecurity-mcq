import json, sys, time, torch, numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM
model_id, out_path = sys.argv[1], sys.argv[2]
L = "ABCD"
SETS = ["data/CyberMetric/CyberMetric-2000-v1.json", "data/secqa_v1_test.json", "data/secqa_v2_test.json"]
def load(p):
    items = []
    for i, x in enumerate(json.load(open(p))["questions"]):
        a = x["answers"]
        if sorted(a) != list(L) or any(not str(v).strip() for v in a.values()) or len(set(a.values())) != 4 or x["solution"] not in L: continue
        items.append(dict(q=x["question"], opts=[a[k] for k in L], gold=L.index(x["solution"])))
    return items
tok = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16).cuda().eval()
lid = [tok.encode(c, add_special_tokens=False)[-1] for c in L]
tok.padding_side = "left"
if tok.pad_token is None: tok.pad_token = tok.eos_token
fmt = lambda o: "\n".join(f"{L[i]}. {v}" for i, v in enumerate(o))
PR = {"A": "One of the following four statements about cybersecurity is the correct one. Pick it.\n\n{o}\n\nAnswer with a single letter (A, B, C or D).",
      "B": "Below are four candidate statements about information security. Exactly one of them is accurate; the others contain an error.\n\n{o}\n\nReply with only the letter of the accurate statement."}
def chat(m): return tok.apply_chat_template([{"role": "user", "content": m}], tokenize=False, add_generation_prompt=True)
@torch.no_grad()
def preds(prompts, bs=8):
    out = []
    for s in range(0, len(prompts), bs):
        enc = tok(prompts[s:s+bs], return_tensors="pt", padding=True, add_special_tokens=False).to("cuda")
        lp = torch.log_softmax(model(**enc).logits[:, -1, :].float(), -1)[:, lid]
        out += lp.argmax(1).tolist()
    return out
rng = np.random.default_rng(2211)
def ci(v, B=4000):
    n = len(v); m = [v[rng.integers(0, n, n)].mean() for _ in range(B)]; return [round(float(x), 4) for x in np.percentile(m, [2.5, 97.5])]
res = dict(model=model_id)
for p in SETS:
    it = load(p); n = len(it); r = {}
    gp = np.bincount([x["gold"] for x in it], minlength=4) / n
    r["gold_pos_share"] = gp.round(3).tolist()
    r["longest_acc"] = float(np.mean([int(np.argmax([len(o) for o in x["opts"]])) == x["gold"] for x in it]))
    r["shortest_acc"] = float(np.mean([int(np.argmin([len(o) for o in x["opts"]])) == x["gold"] for x in it]))
    for pk, tpl in PR.items():
        C = []
        for k in range(4):
            ps = []; gs = []
            for x in it:
                o = x["opts"][k:] + x["opts"][:k]; gs.append((x["gold"] - k) % 4); ps.append(chat(tpl.format(o=fmt(o))))
            C.append(np.array(preds(ps)) == np.array(gs))
        C = np.array(C, int).T  # n x 4
        m = C.mean(1)
        r[pk] = dict(acc_by_rot=C.mean(0).round(3).tolist(), mean=float(m.mean()), ci95=ci(m), all4=float(C.min(1).mean()))
    res[p.split("/")[-1]] = r
    print(p.split("/")[-1], json.dumps(r), flush=True)
json.dump(res, open(out_path, "w"))
