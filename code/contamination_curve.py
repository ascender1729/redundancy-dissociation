"""How many degenerate predictor values does it take to move the headline?

The first artifact was an unfloored ridge R^2: for a feature with a large activation mean and a
small residual variance, ss_tot is tiny, so an imperfect fit returns a huge negative number. The
released arrays are already floored, so the pre-floor values cannot be regenerated from them. What
CAN be measured on the released arrays is the sensitivity of the headline to that class of
corruption: send a fraction of features to the bottom of the predictor ranking (which is what an
unfloored blow-up does under a rank statistic) and watch the frozen partial correlation move.

Three selection rules for which features get corrupted:
  random     - a uniformly random subset (expected effect)
  large-mag  - the highest mean-activation features, the class the blow-up actually hit
  adversarial- the features with the highest U_dec (worst case, an upper bound on the damage)

This is a labelled simulation of the mechanism, not a reconstruction of the historical number.
CPU only. Run: python contamination_curve.py
"""
import os
import numpy as np
from scipy.stats import rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
PAIRS = [("near", "close.npz"), ("gemma", "gemma.npz"), ("mistral", "far2.npz")]


def resid(y, C):
    X = np.column_stack([np.ones(len(y)), C])
    w, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ w


def psp(x, y, ctrls):
    C = np.column_stack([rankdata(c) for c in ctrls])
    return float(np.corrcoef(resid(rankdata(x), C), resid(rankdata(y), C))[0, 1])


def corrupt(red, idx, rng):
    """Send the selected features to the bottom of the ranking with distinct garbage values,
    exactly as an unfloored, hugely negative R^2 would."""
    out = red.astype(float).copy()
    out[idx] = -1e5 * (1.0 + rng.random(len(idx)))
    return out


rng = np.random.default_rng(0)
FRACS = [0.0, 0.005, 0.01, 0.02, 0.05, 0.10, 0.20]
print("Contamination sensitivity of the frozen partial Spearman (controls: freq, mag, dec_norm)")
print("=" * 104)
for pname, fn in PAIRS:
    d = np.load(os.path.join(HERE, "data", fn))
    red = d["redundancy_R2"].astype(float)
    ctrl = [d[c].astype(float) for c in ("freq", "mag", "dec_norm")]
    n = len(red)
    for meas in ["U_dec", "U_overlap"]:
        U = d[meas].astype(float)
        order_mag = np.argsort(-d["mag"].astype(float))
        order_adv = np.argsort(-U)
        line = {"random": [], "large-mag": [], "adversarial": []}
        for f in FRACS:
            k = int(round(f * n))
            if k == 0:
                base = psp(red, U, ctrl)
                for r in line:
                    line[r].append(base)
                continue
            reps = [psp(corrupt(red, rng.choice(n, k, replace=False), rng), U, ctrl) for _ in range(20)]
            line["random"].append(float(np.mean(reps)))
            line["large-mag"].append(psp(corrupt(red, order_mag[:k], rng), U, ctrl))
            line["adversarial"].append(psp(corrupt(red, order_adv[:k], rng), U, ctrl))
        print("\n%s  %s   (fraction of the 2500 features corrupted)" % (pname, meas))
        print("   %-12s %s" % ("", "  ".join("%7.1f%%" % (100 * f) for f in FRACS)))
        for r in ["random", "large-mag", "adversarial"]:
            print("   %-12s %s" % (r, "  ".join("%+8.3f" % v for v in line[r])))
