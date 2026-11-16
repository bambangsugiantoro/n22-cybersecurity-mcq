import json, sys, numpy as np
from scipy.stats import chi2, binomtest
rng = np.random.default_rng(2211)
def holm(ps):
    o = np.argsort(ps); m = len(ps); adj = np.zeros(m); run = 0
    for r, i in enumerate(o):
        run = max(run, (m - r) * ps[i]); adj[i] = min(1, run)
    return adj
def ci(f, n, B=4000):
    v = [f(rng.integers(0, n, n)) for _ in range(B)]
    return np.percentile(v, [2.5, 97.5])
def cochran_q(M):  # M: n x k binary
    k = M.shape[1]; Cj = M.sum(0); Ri = M.sum(1); T = M.sum()
    den = k * T - (Ri ** 2).sum()
    if den == 0: return 1.0
    Q = (k - 1) * (k * (Cj ** 2).sum() - T ** 2) / den
    return float(chi2.sf(Q, k - 1))
for path in sys.argv[1:]:
    D = json.load(open(path)); it = D["items"]; n = len(it)
    R = np.array([[x[f"R{k}"]["pred"] == x[f"R{k}"]["gold"] for k in range(4)] for x in it], int)
    q0 = np.array([x["Q0"]["pred"] == x["R0"]["gold"] for x in it], int)
    cn = np.array([x["C"]["pub"] > np.mean(x["C"]["alts"]) for x in it], int)
    acc = R.mean(0); rng_pp = (acc.max() - acc.min()) * 100
    a0 = R[:, 0]; all4 = R.min(1)
    h2 = (a0 - all4)
    p1 = cochran_q(R)
    p4 = binomtest(int(cn.sum()), n, 0.5, alternative="greater").pvalue
    adj = holm([p1, p4])
    lo_rng = ci(lambda i: (R[i].mean(0).max() - R[i].mean(0).min()) * 100, n)[0]
    lo_h2 = ci(lambda i: h2[i].mean() * 100, n)[0]
    lo_q0 = ci(lambda i: q0[i].mean(), n)[0]
    lo_cn = ci(lambda i: cn[i].mean(), n)[0]
    print(f"== {D['model']} {path} n={n}")
    print(f"R0..R3 acc={np.round(acc,3).tolist()} range={rng_pp:.1f}pp (lo95 {lo_rng:.1f}) CochranQ p={p1:.4g} holm={adj[0]:.4g}")
    print(f"H1 {'SUPPORTED' if rng_pp>=3 and adj[0]<.05 else 'NOT'}")
    print(f"H2 acc(R0)-all4 = {h2.mean()*100:.1f}pp (lo95 {lo_h2:.1f}) {'SUPPORTED' if lo_h2>=10 else ('PARTLY' if h2.mean()*100>=10 else 'NOT')}")
    print(f"H3 Q0 acc={q0.mean():.3f} (lo95 {lo_q0:.3f}) {'SUPPORTED' if lo_q0>0.30 else ('PARTLY' if q0.mean()>0.30 else 'NOT')}")
    print(f"H4 canon share={cn.mean():.3f} (lo95 {lo_cn:.3f}) p={p4:.4g} holm={adj[1]:.4g} {'SUPPORTED' if cn.mean()>=.55 and adj[1]<.05 else ('PARTLY' if cn.mean()>=.55 else 'NOT')}")
    pl = np.bincount([x["R0"]["pred"] for x in it], minlength=4) / n
    print("pred letter dist R0:", np.round(pl, 3).tolist(), "mean mass", round(float(np.mean([x[f'R{k}']['mass'] for x in it for k in range(4)])), 3))
