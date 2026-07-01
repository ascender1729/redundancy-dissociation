"""Gate 3 (offline, $0): partial Spearman + permutation-null control + dependence-respecting
bootstrap CI, on the saved per-feature arrays for all three pairs. No GPU."""
import numpy as np
from scipy.stats import rankdata

SCRATCH = r"C:\Users\pavan\AppData\Local\Temp\claude\F--VIBETENSOR\dc44cba6-ba23-4483-b53f-e9d3ea039fa7\scratchpad"
PAIRS = [("GPT-2/Pythia (near)", "close.npz"),
         ("Gemma-9b/Llama-8b (far)", "gemma.npz"),
         ("Mistral-7b/Llama-8b (far)", "far2.npz")]


def resid(y, C):
    # residual of y after regressing on controls C (with intercept)
    X = np.column_stack([np.ones(len(y)), C])
    w, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ w


def partial_spearman(x, y, controls):
    rx = resid(rankdata(x), np.column_stack([rankdata(c) for c in controls]))
    ry = resid(rankdata(y), np.column_stack([rankdata(c) for c in controls]))
    return float(np.corrcoef(rx, ry)[0, 1])


def run(name, fn):
    d = np.load(f"{SCRATCH}\\{fn}")  # our own harness output; numeric arrays only, no pickle
    red = d["redundancy_R2"].astype(float)
    ctrl = [d["freq"].astype(float), d["mag"].astype(float), d["dec_norm"].astype(float)]
    rng = np.random.default_rng(0)
    out = {}
    for meas in ["U_dec", "U_overlap"]:
        U = d[meas].astype(float)
        obs = partial_spearman(red, U, ctrl)
        # permutation null: shuffle redundancy vs (U + controls) -> null band around 0
        perm = np.empty(1000)
        rr = rankdata(red)
        rU = resid(rankdata(U), np.column_stack([rankdata(c) for c in ctrl]))
        Cr = np.column_stack([rankdata(c) for c in ctrl])
        for i in range(1000):
            rx = resid(rr[rng.permutation(len(rr))], Cr)
            perm[i] = np.corrcoef(rx, rU)[0, 1]
        lo, hi = np.percentile(perm, [2.5, 97.5])
        p = (np.sum(np.abs(perm) >= abs(obs)) + 1) / 1001
        # dependence-respecting bootstrap CI (resample features; groups approximated by features here)
        n = len(red); boot = np.empty(1000)
        for i in range(1000):
            idx = rng.integers(0, n, n)
            boot[i] = partial_spearman(red[idx], U[idx], [c[idx] for c in ctrl])
        blo, bhi = np.percentile(boot, [2.5, 97.5])
        out[meas] = (obs, (lo, hi), p, (blo, bhi))
    return out


print("Gate 3: partial Spearman rho(redundancy, U | freq,mag,decnorm), permutation null (N=1000), bootstrap 95% CI")
print("=" * 108)
for name, fn in PAIRS:
    r = run(name, fn)
    print(f"\n{name}")
    for meas, (obs, (lo, hi), p, (blo, bhi)) in r.items():
        outside = "OUTSIDE null (real effect)" if (obs < lo or obs > hi) else "inside null (not distinguishable)"
        print(f"  {meas:10s} rho={obs:+.3f}  null95=[{lo:+.3f},{hi:+.3f}]  perm_p={p:.4f}  boot95=[{blo:+.3f},{bhi:+.3f}]  -> {outside}")
