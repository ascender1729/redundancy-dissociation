"""Specification curve over estimator choices, computed on the released per-feature arrays.

Three axes, all of them choices an analyst faces when running a partial rank correlation
over SAE features:

  A. residualisation   (3): "ranks"  rank x, y and the controls, then residualise (frozen estimator)
                            "raw"    residualise the raw values on the raw controls (harness path)
                            "none"   no controls
  B. final statistic   (3): Pearson | Spearman | Kendall tau-b, applied to the residuals
  C. control subset    (8): every subset of {freq, mag, dec_norm}

The frozen estimator is (ranks, Pearson, freq+mag+dec_norm). The original harness estimator is
(raw, Spearman, freq+mag+dec_norm). When the control subset is empty the residualisation axis
collapses, giving 7*2*3 + 3 = 45 distinct specifications per cell.

CPU only. Run: python spec_curve.py
"""
import itertools, json, os
import numpy as np
from scipy.stats import rankdata, spearmanr, kendalltau

HERE = os.path.dirname(os.path.abspath(__file__))
PAIRS = [("near", "close.npz"), ("gemma", "gemma.npz"), ("mistral", "far2.npz")]
CTRLS = ["freq", "mag", "dec_norm"]
FROZEN = ("ranks", "pearson", "freq+mag+dec_norm")
HARNESS = ("raw", "spearman", "freq+mag+dec_norm")


def resid(y, C):
    if C.shape[1] == 0:
        return y - y.mean()
    X = np.column_stack([np.ones(len(y)), C])
    w, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ w


def spec(x, y, ctrl_arrays, how, stat):
    x = np.asarray(x, float); y = np.asarray(y, float)
    if how == "none" or not ctrl_arrays:
        rx, ry = x, y
    elif how == "ranks":
        C = np.column_stack([rankdata(c) for c in ctrl_arrays])
        rx, ry = resid(rankdata(x), C), resid(rankdata(y), C)
    else:
        C = np.column_stack(ctrl_arrays)
        rx, ry = resid(x, C), resid(y, C)
    if stat == "pearson":
        return float(np.corrcoef(rx, ry)[0, 1])
    if stat == "spearman":
        return float(spearmanr(rx, ry).statistic)
    return float(kendalltau(rx, ry).statistic)


rows = []
for pname, fn in PAIRS:
    d = np.load(os.path.join(HERE, "data", fn))
    red = d["redundancy_R2"].astype(float)
    pool = {c: d[c].astype(float) for c in CTRLS}
    for meas in ["U_dec", "U_overlap"]:
        U = d[meas].astype(float)
        for k in range(4):
            for subset in itertools.combinations(CTRLS, k):
                hows = ["none"] if not subset else ["ranks", "raw"]
                for how in hows:
                    for stat in ["pearson", "spearman", "kendall"]:
                        rows.append(dict(pair=pname, meas=meas, controls="+".join(subset) or "none",
                                         how=how, stat=stat,
                                         rho=spec(red, U, [pool[c] for c in subset], how, stat)))

os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
json.dump(rows, open(os.path.join(HERE, "results", "spec_curve.json"), "w"), indent=1)


def pick(sub, key):
    how, stat, ctl = key
    return next(r["rho"] for r in sub if r["how"] == how and r["stat"] == stat and r["controls"] == ctl)


print("Specification curve: %d specifications total, %d per cell" % (len(rows), len(rows) // 6))
print("=" * 104)
print("%-9s %-10s %8s %8s %8s %8s %8s %6s %6s" %
      ("pair", "measure", "frozen", "harness", "min", "max", "range", "n>0", "n<0"))
for pname, _ in PAIRS:
    for meas in ["U_dec", "U_overlap"]:
        sub = [r for r in rows if r["pair"] == pname and r["meas"] == meas]
        v = np.array([r["rho"] for r in sub])
        print("%-9s %-10s %+8.3f %+8.3f %+8.3f %+8.3f %8.3f %6d %6d" %
              (pname, meas, pick(sub, FROZEN), pick(sub, HARNESS),
               v.min(), v.max(), v.max() - v.min(), (v > 0).sum(), (v < 0).sum()))

print("\nCells where specifications of both signs exist on the same arrays:")
for pname, _ in PAIRS:
    for meas in ["U_dec", "U_overlap"]:
        sub = [r for r in rows if r["pair"] == pname and r["meas"] == meas]
        v = np.array([r["rho"] for r in sub])
        if (v > 0).any() and (v < 0).any():
            pos = max((r for r in sub if r["rho"] > 0), key=lambda r: r["rho"])
            neg = min((r for r in sub if r["rho"] < 0), key=lambda r: r["rho"])
            print("  %-9s %-10s  %+.3f [%s/%s/%s]  to  %+.3f [%s/%s/%s]" %
                  (pname, meas, neg["rho"], neg["how"], neg["stat"], neg["controls"],
                   pos["rho"], pos["how"], pos["stat"], pos["controls"]))

print("\nHow much each axis moves the near-pair decoder cell (holding the others at the frozen setting):")
sub = [r for r in rows if r["pair"] == "near" and r["meas"] == "U_dec"]
for stat in ["pearson", "spearman", "kendall"]:
    print("   statistic=%-9s ranks=%+.3f  raw=%+.3f" %
          (stat, pick(sub, ("ranks", stat, "freq+mag+dec_norm")), pick(sub, ("raw", stat, "freq+mag+dec_norm"))))
for k in range(4):
    for subset in itertools.combinations(CTRLS, k):
        ctl = "+".join(subset) or "none"
        how = "none" if not subset else "ranks"
        print("   controls=%-20s (ranks/pearson) = %+.3f" % (ctl, pick(sub, (how, "pearson", ctl))))
