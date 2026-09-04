"""Sampling noise versus estimator spread, and multiple-comparison bookkeeping.

Question: is the disagreement between estimator choices larger than the sampling uncertainty of any
one of them? If it is, the study was never underpowered; the estimator was the binding constraint.
CPU only. Run: python power_and_spread.py
"""
import json, os
import numpy as np
from scipy.stats import rankdata, norm

HERE = os.path.dirname(os.path.abspath(__file__))
PAIRS = [("near", "close.npz"), ("gemma", "gemma.npz"), ("mistral", "far2.npz")]
N, K = 2500, 3          # features per cell, number of controls


def resid(y, C):
    X = np.column_stack([np.ones(len(y)), C])
    w, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ w


def psp(x, y, ctrls):
    C = np.column_stack([rankdata(c) for c in ctrls])
    return float(np.corrcoef(resid(rankdata(x), C), resid(rankdata(y), C))[0, 1])


se = 1.0 / np.sqrt(N - K - 1)
print("Analytic SE of a partial rank correlation at N=%d with %d controls: %.4f" % (N, K, se))
for a, lab in [(0.05, "0.05"), (0.01, "0.01"), (0.001, "0.001")]:
    crit = norm.ppf(1 - a / 2) * se
    mde = (norm.ppf(1 - a / 2) + norm.ppf(0.8)) * se
    print("   alpha=%-5s  significant above |rho|=%.3f   80%%-power MDE |rho|=%.3f" % (lab, crit, mde))

rows = json.load(open(os.path.join(HERE, "results", "spec_curve.json")))
print("\nEstimator spread versus sampling noise, per cell")
print("=" * 92)
print("%-9s %-10s %9s %9s %9s %9s" % ("pair", "measure", "frozen", "spec-range", "range/SE", "boot-CI-width"))
boot = {}
rng = np.random.default_rng(7)
for pname, fn in PAIRS:
    d = np.load(os.path.join(HERE, "data", fn))
    red = d["redundancy_R2"].astype(float)
    ctrl = [d[c].astype(float) for c in ("freq", "mag", "dec_norm")]
    for meas in ["U_dec", "U_overlap"]:
        U = d[meas].astype(float)
        obs = psp(red, U, ctrl)
        b = np.empty(400)
        for i in range(400):
            idx = rng.integers(0, N, N)
            b[i] = psp(red[idx], U[idx], [c[idx] for c in ctrl])
        lo, hi = np.percentile(b, [2.5, 97.5])
        sub = [r["rho"] for r in rows if r["pair"] == pname and r["meas"] == meas]
        rng_spec = max(sub) - min(sub)
        boot[(pname, meas)] = (obs, lo, hi)
        print("%-9s %-10s %+9.3f %9.3f %9.1f %9.3f" % (pname, meas, obs, rng_spec, rng_spec / se, hi - lo))

print("\nHolm-Bonferroni over the six frozen cells (permutation p, 1000 shuffles, floor 0.001):")
praw = {("near", "U_dec"): 0.001, ("near", "U_overlap"): 0.001, ("gemma", "U_dec"): 0.001,
        ("gemma", "U_overlap"): 0.8362, ("mistral", "U_dec"): 0.001, ("mistral", "U_overlap"): 0.001}
order = sorted(praw.items(), key=lambda kv: kv[1])
m = len(order)
for i, (k, p) in enumerate(order):
    adj = min(1.0, p * (m - i))
    print("   %-9s %-10s  p=%.4f  Holm-adjusted <= %.4f  %s" %
          (k[0], k[1], p, adj, "significant at 0.01" if adj < 0.01 else "not significant at 0.01"))

print("\nTie structure of the co-firing target (a rank statistic on a heavily tied variable):")
for pname, fn in PAIRS:
    d = np.load(os.path.join(HERE, "data", fn))
    U = d["U_overlap"].astype(float)
    v, c = np.unique(U, return_counts=True)
    print("   %-9s %d distinct values over %d features; largest tie group %d (%.1f%%)" %
          (pname, len(v), len(U), c.max(), 100 * c.max() / len(U)))
