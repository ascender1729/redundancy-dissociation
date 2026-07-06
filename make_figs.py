"""Regenerate fig_forest.pdf from data/ with NO in-figure title (the ACL caption carries the message).
Recomputes the six frozen partials + feature-bootstrap CIs directly, so the figure cannot drift from
the tables."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
PAIRS = [("GPT-2 / Pythia\n(near)", "close.npz"),
         ("Gemma-2-9b / Llama-3.1-8B\n(far)", "gemma.npz"),
         ("Mistral-7B / Llama-3.1-8B\n(far)", "far2.npz")]


def resid(y, C):
    X = np.column_stack([np.ones(len(y)), C])
    w, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ w


def psp(x, y, controls):
    C = np.column_stack([rankdata(c) for c in controls])
    return float(np.corrcoef(resid(rankdata(x), C), resid(rankdata(y), C))[0, 1])


rng = np.random.default_rng(0)
rows = []
for name, f in PAIRS:
    d = np.load(os.path.join(HERE, "data", f))
    red = d["redundancy_R2"].astype(float)
    ctrl = [d["freq"].astype(float), d["mag"].astype(float), d["dec_norm"].astype(float)]
    for meas, col in [("U_dec", "#c0392b"), ("U_overlap", "#1f6fb2")]:
        U = d[meas].astype(float)
        obs = psp(red, U, ctrl)
        n = len(red); boot = np.empty(1000)
        for i in range(1000):
            idx = rng.integers(0, n, n)
            boot[i] = psp(red[idx], U[idx], [c[idx] for c in ctrl])
        lo, hi = np.percentile(boot, [2.5, 97.5])
        rows.append((name, meas, col, obs, lo, hi))

fig, ax = plt.subplots(figsize=(6.2, 3.4))
ax.axvspan(-0.043, 0.040, color="0.88", zorder=0)      # widest per-cell permutation band
ax.axvline(0, color="0.55", lw=0.8, zorder=1)
ys, labels = [], []
y = 0
for name, _ in PAIRS:
    for meas in ("U_dec", "U_overlap"):
        r = next(x for x in rows if x[0] == name and x[1] == meas)
        ax.errorbar(r[3], y, xerr=[[r[3] - r[4]], [r[5] - r[3]]], fmt="o", color=r[2],
                    capsize=3, ms=6, zorder=3)
        ys.append(y); labels.append(f"{name.splitlines()[0]}  {meas.replace('U_', '')}")
        y += 1
    y += 0.5
ax.set_yticks(ys); ax.set_yticklabels(labels, fontsize=8)
ax.set_xlabel("partial Spearman rho (controls: frequency, magnitude, decoder norm)", fontsize=9)
ax.invert_yaxis()
ax.scatter([], [], c="#c0392b", label="decoder geometry")
ax.scatter([], [], c="#1f6fb2", label="co-firing overlap")
ax.legend(fontsize=8, loc="lower right", framealpha=0.9)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_forest.pdf"))
print("fig_forest.pdf regenerated (no in-figure title)")
for r in rows:
    print(f"  {r[0].splitlines()[0]:28s} {r[1]:10s} {r[3]:+.3f} [{r[4]:+.3f},{r[5]:+.3f}]")
