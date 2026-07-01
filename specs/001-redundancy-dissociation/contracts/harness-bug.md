<!-- Gate 1 + Gate 2 results. Part of the reliability contribution. -->
# Contract: exhibited harness bug + de-circularization

## Gate 1 - the bug, exhibited and locked (PASS)
Symptom: `redundancy_R2_mean` reached ~ -1.4e5 on large-activation (Gemma/Llama) runs, producing a
spurious decoder-universality positive (+0.27 near pair).
Mechanism: for a feature with a large mean and small residual variance, the in-sample ridge
$R^2 = 1 - \mathrm{ss\_res}/\mathrm{ss\_tot}$ has a tiny denominator, so any imperfect prediction gives a
hugely negative garbage value; garbage redundancy scores then correlate spuriously with the target.
Fix (corrected harness): floor $R^2$ at $-1$ (line 92 of
`cloud_job_sae_corrected/sae_redundancy_universality_corrected.py`) and unit-variance-condition the
residual PCA.
Regression test: `test_harness_bug.py` (in the paper dir). Pre-fix path returns -3.48e4 on a
large-mean/low-variance construction; corrected path floors to exactly -1; a well-posed case is
untouched (R2 > 0.8, floor changes nothing). The test FAILS on the pre-fix code and PASSES on the fix.
Status: PASS. This is the paper's core reliability asset for the Special Track.

## Gate 2 - de-circularization (PASS by construction, no GPU run)
Concern (F1): if redundancy were computed from other SAE features' activations, its correlation with a
co-firing universality measure could be tautological.
Resolution: the redundancy predictor is computed from model A's OWN RESIDUAL STREAM
(`redundancy_min_r2`: predict a feature's left-half activation from a PCA summary of the right-half
RESIDUAL, and vice versa; take the min). It uses no other SAE feature and is computed on model A ALONE,
before any cross-model matching and independent of model B. The co-firing universality measure
(U_overlap) is the Jaccard of top-K activating contexts of matched features. The two share no readout,
so the co-firing positive (+0.41 near) cannot be circular. Independence is by construction, which is a
stronger guarantee than an empirical control.
Status: PASS by construction. Cited from `contracts/measures.md`.

## Consequence
Both invalidating gates pass: the reliability story is real and the positive leg is not an artifact of
circularity. Remaining gates (alignment-null positive control, far-pair CIs, multi-layer sweep, third
far pair) SCOPE and HARDEN the claims but cannot kill the paper.
