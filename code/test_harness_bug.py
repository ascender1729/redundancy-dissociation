"""Gate 1: regression test locking the fix for the harness bug that produced the spurious
decoder-universality positive.

Observed in-harness: redundancy_R2_mean ~ -1.4e5 on large-activation (Gemma/Llama) models. When a
feature's activation has a large mean and small residual variance, the in-sample ridge R2
1 - ss_res/ss_tot has a tiny denominator, so any imperfect prediction yields a hugely negative value.
Those garbage redundancy scores then correlate spuriously with anything, which is how a decoder-
universality "positive" (+0.27) appeared. The fix in the corrected harness: floor R2 at -1 (values
below -1 are numerical garbage, not real un-recoverability) and unit-variance-condition the residual PCA.

This test isolates the FLOOR CONTRACT that caps the blow-up: it FAILS on the pre-fix path and PASSES on
the corrected path. It is not a bit-exact replay of the Gemma numerics; it constructs a case that
deterministically drives the raw R2 far below -1 (large-mean, low-variance target), which is the class
of input that triggered the observed value. Run: python test_harness_bug.py
"""
import numpy as np


def ridge_r2_OLD(X, y, lam=1.0):
    """Pre-fix: no floor (harness before the correction)."""
    X = np.asarray(X, np.float64); y = np.asarray(y, np.float64)
    w = np.linalg.solve(X.T @ X + lam * np.eye(X.shape[1]), X.T @ y)
    pred = X @ w
    ss_res = float(((y - pred) ** 2).sum()); ss_tot = float(((y - y.mean()) ** 2).sum())
    return 0.0 if ss_tot < 1e-12 else 1.0 - ss_res / ss_tot


def ridge_r2_NEW(X, y, lam=1.0):
    """Post-fix: identical solve, R2 floored at -1 (the exact fix at harness line 92)."""
    r = ridge_r2_OLD(X, y, lam)
    return max(-1.0, r)


def make_blowup_case(n=200, d=48):
    """A feature (y) with a large mean and small residual variance that X cannot explain -> the ridge
    prediction cannot capture the constant offset, so ss_res >> ss_tot and raw R2 << -1. This is the
    large-mean / low-variance regime that produced the observed -1.4e5 on Gemma-scale activations."""
    rng = np.random.default_rng(0)
    X = rng.standard_normal((n, d))          # zero-mean features, no intercept column
    y = 10.0 + 0.05 * rng.standard_normal(n)  # large mean, tiny variance
    return X, y


def demo():
    X, y = make_blowup_case()
    old = ridge_r2_OLD(X, y)
    new = ridge_r2_NEW(X, y)
    print("OLD ridge_r2 (pre-fix): %.4e" % old)
    print("NEW ridge_r2 (floored): %.4f" % new)
    # BUG exhibited: the pre-fix path returns garbage far below -1 (the -1.4e5 class).
    assert old < -100.0, "expected pre-fix blow-up (<< -1); got %.4e" % old
    # FIX locked: the corrected path never returns below -1.
    assert new == -1.0, "expected the floor to cap at exactly -1; got %.4f" % new
    # Sanity: on a well-posed case both agree and are sane (guards against over-flooring real values).
    rng = np.random.default_rng(1)
    Xg = rng.standard_normal((300, 10)); wtrue = rng.standard_normal(10)
    yg = Xg @ wtrue + 0.1 * rng.standard_normal(300)
    assert abs(ridge_r2_OLD(Xg, yg) - ridge_r2_NEW(Xg, yg)) < 1e-9, "floor must not alter valid R2"
    assert ridge_r2_NEW(Xg, yg) > 0.8, "well-posed case should have high R2"
    print("PASS: pre-fix blows up (%.2e), corrected floors to -1, valid R2 untouched." % old)


if __name__ == "__main__":
    demo()
