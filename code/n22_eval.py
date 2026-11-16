import json, sys, time, torch, random
from transformers import AutoTokenizer, AutoModelForCausalLM
model_id, data_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
limit = int(sys.argv[4]) if len(sys.argv) > 4 else None
L = "ABCD"
d = json.load(open(data_path))["questions"]
items = []
for i, x in enumerate(d):
    a = x["answers"]
    if sorted(a) != list(L) or any(not str(v).strip() for v in a.values()) or len(set(a.values())) != 4 or x["solution"] not in L:
        continue
    items.append(dict(id=i, q=x["question"], opts=[a[k] for k in L], gold=L.index(x["solution"])))
if limit: items = items[:limit]
tok = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16).cuda().eval()
lid = [tok.encode(c, add_special_tokens=False)[-1] for c in L]
assert len(set(lid)) == 4
def fmt(opts): return "\n".join(f"{L[i]}. {o}" for i, o in enumerate(opts))
def prompt_q(q, opts):
    m = f"Answer the following multiple-choice question about cybersecurity.\n\nQuestion: {q}\n{fmt(opts)}\n\nAnswer with a single letter (A, B, C or D)."
    return tok.apply_chat_template([{"role": "user", "content": m}], tokenize=False, add_generation_prompt=True)
def prompt_noq(opts):
    m = f"One of the following four statements about cybersecurity is the correct one. Pick it.\n\n{fmt(opts)}\n\nAnswer with a single letter (A, B, C or D)."
    return tok.apply_chat_template([{"role": "user", "content": m}], tokenize=False, add_generation_prompt=True)
tok.padding_side = "left"
if tok.pad_token is None: tok.pad_token = tok.eos_token
@torch.no_grad()
def letter_scores(prompts, bs=8):
    res = []
    for s in range(0, len(prompts), bs):
        enc = tok(prompts[s:s+bs], return_tensors="pt", padding=True, add_special_tokens=False).to("cuda")
        lg = model(**enc).logits[:, -1, :].float()
        lp = torch.log_softmax(lg, -1)
        for r in lp:
            v = r[lid]; res.append(dict(scores=v.tolist(), mass=float(v.exp().sum())))
    return res
@torch.no_grad()
def loglik(text):
    ids = tok(text, return_tensors="pt").input_ids.cuda()
    if tok.bos_token_id is not None and ids[0, 0] != tok.bos_token_id:
        ids = torch.cat([torch.tensor([[tok.bos_token_id]]).cuda(), ids], 1)
    lg = model(ids).logits[0, :-1].float()
    return float(torch.log_softmax(lg, -1).gather(1, ids[0, 1:, None]).sum())
def rot(opts, gold, k):
    o = opts[k:] + opts[:k]; return o, (gold - k) % 4
t0 = time.time()
for k in range(4):
    ps, gs = [], []
    for it in items:
        o, g = rot(it["opts"], it["gold"], k); ps.append(prompt_q(it["q"], o)); gs.append(g)
    r = letter_scores(ps)
    for it, g, x in zip(items, gs, r):
        it[f"R{k}"] = dict(gold=g, pred=max(range(4), key=lambda j: x["scores"][j]), mass=x["mass"])
r = letter_scores([prompt_noq(it["opts"]) for it in items])
for it, x in zip(items, r):
    it["Q0"] = dict(pred=max(range(4), key=lambda j: x["scores"][j]), mass=x["mass"])
for it in items:
    def txt(o): return f"Question: {it['q']}\n{fmt(o)}"
    alts = [rot(it["opts"], 0, k)[0] for k in (1, 2, 3)] + [it["opts"][::-1]]
    it["C"] = dict(pub=loglik(txt(it["opts"])), alts=[loglik(txt(a)) for a in alts])
json.dump(dict(model=model_id, data=data_path, n=len(items), seconds=time.time() - t0, items=items), open(out_path, "w"))
acc = lambda k: sum(it[k]["pred"] == it[k]["gold"] for it in items) / len(items)
allc = sum(all(it[f"R{k}"]["pred"] == it[f"R{k}"]["gold"] for k in range(4)) for it in items) / len(items)
q0 = sum(it["Q0"]["pred"] == it["R0"]["gold"] for it in items) / len(items)
cc = sum(it["C"]["pub"] > sum(it["C"]["alts"]) / 4 for it in items) / len(items)
mass = sum(it[f"R{k}"]["mass"] for it in items for k in range(4)) / (4 * len(items))
print(f"n={len(items)} R0..R3={[round(acc(f'R{k}'),3) for k in range(4)]} all4={allc:.3f} Q0={q0:.3f} canon={cc:.3f} meanmass={mass:.3f} sec={time.time()-t0:.0f}")
