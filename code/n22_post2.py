import json, glob, numpy as np
rng = np.random.default_rng(2211)
data = json.load(open("data/CyberMetric/CyberMetric-2000-v1.json"))["questions"]
L = "ABCD"
def ci(v, B=4000):
    n = len(v); m = [v[rng.integers(0, n, n)].mean() for _ in range(B)]; return [round(float(x), 3) for x in np.percentile(m, [2.5, 97.5])]
out = {}
for f in sorted(glob.glob("results/*CyberMetric*.json") + glob.glob("results_ext/*CyberMetric*.json")):
    D = json.load(open(f)); it = D["items"]; name = D["model"].split("/")[-1]
    lon = np.array([int(np.argmax([len(data[x["id"]]["answers"][k]) for k in L])) == L.index(data[x["id"]]["solution"]) for x in it])
    q0 = np.array([x["Q0"]["pred"] == x["R0"]["gold"] for x in it]); r0 = np.array([x["R0"]["pred"] == x["R0"]["gold"] for x in it])
    r = dict(n=len(it), longest=round(float(lon.mean()), 3), q0=round(float(q0.mean()), 3), q0_L=round(float(q0[lon].mean()), 3), q0_notL=round(float(q0[~lon].mean()), 3), q0_notL_ci=ci(q0[~lon].astype(float)), r0_L=round(float(r0[lon].mean()), 3), r0_notL=round(float(r0[~lon].mean()), 3), q0_share_L=round(float((q0 & lon).sum() / q0.sum()), 3))
    out[name] = r; print(name, json.dumps(r), flush=True)
json.dump(out, open("post/post2_longest.json", "w"))
