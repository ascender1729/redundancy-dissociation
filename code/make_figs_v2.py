"""Figures for the reliability redraft. Everything is recomputed from data/ so a figure cannot
drift from a table. Outputs PDF and PNG. Okabe-Ito palette, serif 8pt.

  fig1_spec_curve  - the specification curve (headline figure)
  fig2_forest      - frozen partial correlations with feature-bootstrap CIs
  fig3_null        - real predictor versus position-shuffle null, per cell

Run: python make_figs_v2.py
"""
import itertools
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import rankdata, spearmanr, kendalltau

HERE = os.path.dirname(os.path.abspath(__file__))
OK = dict(black="#000000", orange="#E69F00", sky="#56B4E9", green="#009E73",
          blue="#0072B2", verm="#D55E00", purple="#CC79A7", grey="#8c8c8c")
plt.rcParams.update({"font.family": "serif", "font.size": 8, "axes.labelsize": 8,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 6.5,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 200, "savefig.bbox": "tight"})

PAIRS = [("near", "close.npz", "GPT-2 / Pythia"),
         ("gemma", "gemma.npz", "Gemma-2-9b / Llama-3.1-8B"),
         ("mistral", "far2.npz", "Mistral-7B / Llama-3.1-8B")]
CTRLS = ["freq", "mag", "dec_norm"]
N, K = 2500, 3
SE = 1.0 / np.sqrt(N - K - 1)


def resid(y, C):
    if C.shape[1] == 0:
        return y - y.mean()
    X = np.column_stack([np.ones(len(y)), C])
    w, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ w


def psp(x, y, ctrls):
    C = np.column_stack([rankdata(c) for c in ctrls]) if ctrls else np.empty((len(x), 0))
    return float(np.corrcoef(resid(rankdata(x), C), resid(rankdata(y), C))[0, 1])


def spec(x, y, arrs, how, stat):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if how == "none" or not arrs:
        rx, ry = x, y
    elif how == "ranks":
        C = np.column_stack([rankdata(c) for c in arrs])
        rx, ry = resid(rankdata(x), C), resid(rankdata(y), C)
    else:
        C = np.column_stack(arrs)
        rx, ry = resid(x, C), resid(y, C)
    if stat == "pearson":
        return float(np.corrcoef(rx, ry)[0, 1])
    if stat == "spearman":
        return float(spearmanr(rx, ry).statistic)
    return float(kendalltau(rx, ry).statistic)


DATA = {k: np.load(os.path.join(HERE, "data", f)) for k, f, _ in PAIRS}

specs = {}
for key, _, _ in PAIRS:
    d = DATA[key]
    red = d["redundancy_R2"].astype(float)
    pool = {c: d[c].astype(float) for c in CTRLS}
    for meas in ["U_dec", "U_overlap"]:
        U = d[meas].astype(float)
        rows = []
        for k in range(4):
            for sub in itertools.combinations(CTRLS, k):
                for how in (["none"] if not sub else ["ranks", "raw"]):
                    for stat in ["pearson", "spearman", "kendall"]:
                        rows.append(dict(how=how, stat=stat, controls="+".join(sub) or "none",
                                         rho=spec(red, U, [pool[c] for c in sub], how, stat)))
        specs[(key, meas)] = rows

frozen = {k: next(r["rho"] for r in v if r["how"] == "ranks" and r["stat"] == "pearson"
                  and r["controls"] == "freq+mag+dec_norm") for k, v in specs.items()}
harness = {k: next(r["rho"] for r in v if r["how"] == "raw" and r["stat"] == "spearman"
                   and r["controls"] == "freq+mag+dec_norm") for k, v in specs.items()}

# ------------------------------------------------------------------ figure 1
fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.1, 2.9), gridspec_kw={"width_ratios": [1.05, 1]})

rows = sorted(specs[("near", "U_dec")], key=lambda r: r["rho"])
col = {"ranks": OK["blue"], "raw": OK["verm"], "none": OK["grey"]}
lab = {"ranks": "residualise on ranks", "raw": "residualise on raw values", "none": "no controls"}
xs = np.arange(len(rows))
fz = frozen[("near", "U_dec")]
axL.axhline(0, color="0.6", lw=0.7)
for how in ["ranks", "raw", "none"]:
    m = [i for i, r in enumerate(rows) if r["how"] == how]
    axL.scatter(xs[m], [rows[i]["rho"] for i in m], s=14, color=col[how], label=lab[how], zorder=3)
i_f = min(range(len(rows)), key=lambda i: abs(rows[i]["rho"] - fz))
i_h = min(range(len(rows)), key=lambda i: abs(rows[i]["rho"] - harness[("near", "U_dec")]))
axL.errorbar(-3.0, fz, yerr=1.96 * SE, color=OK["black"], capsize=3, lw=1.1, zorder=4,
             label="95% CI of one estimate")
axL.annotate("pre-registered\nestimator", (xs[i_f], rows[i_f]["rho"]),
             xytext=(xs[i_f] + 6, rows[i_f]["rho"] - 0.040), fontsize=6.5,
             arrowprops=dict(arrowstyle="-", lw=0.6, color="0.3"))
axL.annotate("original harness\nestimator", (xs[i_h], rows[i_h]["rho"]),
             xytext=(xs[i_h] - 4, rows[i_h]["rho"] + 0.040), fontsize=6.5,
             arrowprops=dict(arrowstyle="-", lw=0.6, color="0.3"))
axL.set_xlim(-6, 48)
axL.set_ylim(-0.198, 0.098)
axL.set_xlabel("45 estimator specifications, sorted")
axL.set_ylabel("partial correlation rho")
axL.set_title("GPT-2 / Pythia, decoder geometry", fontsize=8)
axL.legend(loc="upper left", framealpha=0.95)

labels, ticks = [], []
y = 0
axR.axvline(0, color="0.6", lw=0.7)
for key, _, disp in PAIRS:
    for meas, mk in [("U_dec", "o"), ("U_overlap", "s")]:
        v = np.array([r["rho"] for r in specs[(key, meas)]])
        axR.plot([v.min(), v.max()], [y, y], color=OK["grey"], lw=1.0, zorder=2)
        axR.scatter(v, np.full(len(v), y), s=5, color=OK["grey"], alpha=0.45, zorder=2)
        axR.errorbar(frozen[(key, meas)], y, xerr=1.96 * SE, fmt=mk, ms=4.5, color=OK["blue"],
                     capsize=2, lw=1, zorder=4)
        axR.scatter([harness[(key, meas)]], [y], marker="x", s=24, color=OK["verm"], zorder=5)
        labels.append("%s  %s" % (disp.split(" / ")[0], "decoder" if meas == "U_dec" else "co-firing"))
        ticks.append(y)
        y += 1
    y += 0.5
axR.set_yticks(ticks)
axR.set_yticklabels(labels)
axR.invert_yaxis()
axR.set_xlim(-0.30, 0.86)
axR.set_xlabel("partial rho across the same 45 specifications")
axR.scatter([], [], marker="o", s=20, color=OK["blue"], label="pre-registered (95% CI)")
axR.scatter([], [], marker="x", s=24, color=OK["verm"], label="original harness")
axR.scatter([], [], marker="o", s=6, color=OK["grey"], label="other 43 specs")
axR.legend(loc="center right", framealpha=0.95, fontsize=6, handletextpad=0.4, borderpad=0.35)
fig.tight_layout()
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(HERE, "fig1_spec_curve." + ext))
plt.close(fig)

# ------------------------------------------------------------------ figure 2
rng = np.random.default_rng(0)
fig, ax = plt.subplots(figsize=(4.6, 2.7))
ax.axvspan(-0.043, 0.040, color="0.9", zorder=0)
ax.axvline(0, color="0.55", lw=0.8, zorder=1)
ys, labels = [], []
y = 0
for key, _, disp in PAIRS:
    d = DATA[key]
    red = d["redundancy_R2"].astype(float)
    ctrl = [d[c].astype(float) for c in CTRLS]
    for meas, c in [("U_dec", OK["verm"]), ("U_overlap", OK["blue"])]:
        U = d[meas].astype(float)
        obs = psp(red, U, ctrl)
        b = np.empty(1000)
        for j in range(1000):
            idx = rng.integers(0, len(red), len(red))
            b[j] = psp(red[idx], U[idx], [cc[idx] for cc in ctrl])
        lo, hi = np.percentile(b, [2.5, 97.5])
        ax.errorbar(obs, y, xerr=[[obs - lo], [hi - obs]], fmt="o", color=c, capsize=3, ms=5, zorder=3)
        ys.append(y)
        labels.append("%s  %s" % (disp.split(" / ")[0], "decoder" if meas == "U_dec" else "co-firing"))
        y += 1
    y += 0.5
ax.set_yticks(ys)
ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.set_xlabel("partial rho (controls: frequency, magnitude, decoder norm)")
ax.set_xlim(-0.27, 0.42)
ax.scatter([], [], c=OK["verm"], label="decoder geometry")
ax.scatter([], [], c=OK["blue"], label="co-firing overlap")
ax.legend(loc="center right", framealpha=0.95)
fig.tight_layout()
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(HERE, "fig2_forest." + ext))
plt.close(fig)

# ------------------------------------------------------------------ figure 3
fig, ax = plt.subplots(figsize=(4.6, 2.7))
ax.axvline(0, color="0.55", lw=0.8)
ys, labels = [], []
y = 0
for key, _, disp in PAIRS:
    d = DATA[key]
    red = d["redundancy_R2"].astype(float)
    shf = d["redundancy_R2_shuf"].astype(float)
    ctrl = [d[c].astype(float) for c in CTRLS]
    for meas in ["U_dec", "U_overlap"]:
        U = d[meas].astype(float)
        a, b = psp(red, U, ctrl), psp(shf, U, ctrl)
        ax.plot([a, b], [y, y], color="0.7", lw=0.9, zorder=2)
        ax.scatter(a, y, marker="o", s=26, color=OK["blue"], zorder=3)
        ax.scatter(b, y, marker="D", s=22, color=OK["orange"], zorder=3)
        ys.append(y)
        labels.append("%s  %s" % (disp.split(" / ")[0], "decoder" if meas == "U_dec" else "co-firing"))
        y += 1
    y += 0.5
ax.set_yticks(ys)
ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.set_xlabel("partial rho with the universality measure")
ax.set_xlim(-0.33, 0.62)
ax.scatter([], [], marker="o", color=OK["blue"], label="redundancy score")
ax.scatter([], [], marker="D", color=OK["orange"], label="position-shuffled score")
ax.legend(loc="upper right", framealpha=0.95)
fig.tight_layout()
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(HERE, "fig3_null." + ext))
plt.close(fig)

r = [x["rho"] for x in specs[("near", "U_dec")]]
print("wrote fig1_spec_curve, fig2_forest, fig3_null (pdf + png)")
print("near U_dec spec range %.3f = %.1f x the sampling SE of %.4f" %
      (max(r) - min(r), (max(r) - min(r)) / SE, SE))
