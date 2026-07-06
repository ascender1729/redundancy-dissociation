"""Robustness reruns on the frozen per-feature arrays (CPU, $0). Rebuttal assets for the
BlackboxNLP submission: (1) even/odd split stability, (2) Kendall-tau estimator swap,
(3) frequency-quintile-matched partials (nonlinear frequency control), (4) shuffled-predictor
negative control. Same controls as gate 3: freq, mag, dec_norm (rank-based partials)."""
import os
import numpy as np
from scipy.stats import rankdata, kendalltau

HERE = os.path.dirname(os.path.abspath(__file__))
PAIRS = [("GPT-2/Pythia (near)", "close.npz"),
         ("Gemma-9b/Llama-8b (far)", "gemma.npz"),
         ("Mistral-7b/Llama-8b (far)", "far2.npz")]
rng = np.random.default_rng(0)


def resid(y, C):
    X = np.column_stack([np.ones(len(y)), C])
    w, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ w


def partial_spearman(x, y, controls):
    C = np.column_stack([rankdata(c) for c in controls])
    rx, ry = resid(rankdata(x), C), resid(rankdata(y), C)
    return float(np.corrcoef(rx, ry)[0, 1])


def partial_kendall(x, y, controls):
    C = np.column_stack([rankdata(c) for c in controls])
    rx, ry = resid(rankdata(x), C), resid(rankdata(y), C)
    return float(kendalltau(rx, ry).statistic)


print("Robustness checks (controls: freq, mag, dec_norm) - frozen arrays in data/")
print("=" * 100)
for name, f in PAIRS:
    d = np.load(os.path.join(HERE, "data", f))
    red, red_shuf = d["redundancy_R2"], d["redundancy_R2_shuf"]
    ctrl = [d["freq"], d["mag"], d["dec_norm"]]
    print(f"\n{name}  (N={len(red)})")
    for tgt_name in ("U_overlap", "U_dec"):
        y = d[tgt_name].astype(float)
        full = partial_spearman(red, y, ctrl)
        # 1. even/odd split
        e, o = np.arange(len(red)) % 2 == 0, np.arange(len(red)) % 2 == 1
        pe = partial_spearman(red[e], y[e], [c[e] for c in ctrl])
        po = partial_spearman(red[o], y[o], [c[o] for c in ctrl])
        # 2. Kendall
        kt = partial_kendall(red, y, ctrl)
        # 3. frequency-quintile-matched (partial within bins on remaining controls, N-weighted)
        qs = np.quantile(d["freq"], [0.2, 0.4, 0.6, 0.8])
        bins = np.digitize(d["freq"], qs)
        wsum = n = 0.0
        for b in range(5):
            m = bins == b
            if m.sum() > 50:
                r = partial_spearman(red[m], y[m], [d["mag"][m], d["dec_norm"][m]])
                wsum += r * m.sum(); n += m.sum()
        fmatch = wsum / n
        # 4. shuffled-predictor negative control
        shuf = partial_spearman(red_shuf, y, ctrl)
        print(f"  {tgt_name:10s} full={full:+.3f} | even={pe:+.3f} odd={po:+.3f} | "
              f"kendall={kt:+.3f} | freq-matched={fmatch:+.3f} | shuffled-pred={shuf:+.3f}")
print("\nInterpretation guide: even/odd should bracket full; kendall same sign, smaller magnitude;")
print("freq-matched surviving nonzero = effect not a frequency artifact; shuffled-pred ~ 0.")
