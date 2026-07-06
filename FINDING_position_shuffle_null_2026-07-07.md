# Finding: the pre-specified position-shuffle null absorbs the co-firing signal (2026-07-07)

Status: CONFIRMED on the frozen arrays (data/, N=2500 per pair). Affects claim C1. Must be
integrated into the BlackboxNLP submission before it goes out.

## What the harness pre-specified
sae_redundancy_universality_corrected.py line 32: "Position-shuffle null: rho(redundancy_R2_shuffled, U)
for both methods (headline must beat this null)." The saved arrays include redundancy_R2_shuf (position
axis permuted independently per context before the half-split). Gate 3 enforced the feature-pairing
permutation null but never enforced this one.

## What the reruns show (controls: freq, mag, dec_norm, rank partials)
1. The headline does NOT beat the position-shuffle null on any pair for co-firing:
   near +0.291 real vs +0.382 null; far2 +0.169 vs +0.213; gemma +0.005 vs +0.081.
2. Real and shuffled redundancy are highly correlated: rho 0.862 (near), 0.807 (far2), 0.638 (gemma).
3. Decisive incremental partials (predictor | controls + other predictor):
   - redundancy beyond null, U_overlap: -0.035 (near), +0.017 (far2), -0.086 (gemma). Nothing left.
   - null beyond redundancy, U_overlap: +0.261 (near), +0.133 (far2), +0.118 (gemma). Signal stays.
   - Asymmetry: the shuffle-INVARIANT component of the predictor carries the co-firing signal; the
     shuffle-SENSITIVE (position-structure) component adds no detectable signal.
4. Decoder-cosine twist: on gemma, redundancy beyond the null is -0.225 (the negative decoder
   relationship strengthens); on near/far2 it is ~0 (+0.057, +0.044).

## Interpretation (honest)
What predicts co-firing transfer is context-level activation breadth (which survives position
shuffling), not position-level redundancy structure. Claim C1 as previously worded ("within-model
redundancy predicts co-firing universality") overstates specificity: the effect is real but is not
about redundancy structure per se. By the harness's own pre-registered standard, the headline fails
the position-shuffle null.

## Consequences
1. The BlackboxNLP paper gains a third reliability finding: "enforce ALL your pre-registered nulls;
   ours absorbed the headline." This FITS the paper's thesis (measurement artifacts and unenforced
   controls produce overclaims) and makes it stronger, not weaker.
2. C1 must be rescoped everywhere: "context-level breadth predicts co-firing transfer; redundancy adds
   no detectable signal beyond the position-shuffle null (red|null partials -0.04 to +0.02)."
3. The data-attribution project hypothesis needs updating: the data-level question becomes "does
   context-breadth of the attributing data explain transfer", which is closer to the frequency/breadth
   confound the venue cross-check flagged - the frequency control is now doubly mandatory.
4. Downstream artifacts (deck, scripts, notes) still say "redundancy predicts co-firing"; purge after
   the paper text is settled.

## Repro
python robustness_checks.py            (even/odd, kendall, freq-matched, shuffled-pred columns)
python - the incremental partials are in this file's tables; script inline in session log; promote to
recompute_partials.py as a fourth block before submission.
