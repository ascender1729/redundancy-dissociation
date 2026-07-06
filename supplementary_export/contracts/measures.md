<!-- FROZEN before any blocking GPU run. Commit with git SHA; do not edit after freeze. -->
# Contract: frozen measure definitions

## Redundancy (the predictor) - INDEPENDENT of co-firing
For each SAE feature f in model A:
- Split model A's residual-stream activation vectors (at the frozen hook) into two disjoint index
  halves L, R by dimension index parity (fixed, seed-free).
- redundancy_R2(f) = min(R2_L->f, R2_R->f), where R2_H->f is the in-sample ridge R2 (lambda=1.0,
  closed-form normal equations) predicting feature f's activation from a unit-variance PCA summary
  (N_PCA components) of the OTHER half's raw residual stream.
- R2 is floored at -1 (values below -1 are a diverged solve, not real un-recoverability).
- CRITICAL (de-circularization, kills the F1 tautology charge): the predictor is computed from the
  RESIDUAL STREAM reconstruction, NOT from other SAE features' activations. It therefore shares no
  readout with the co-firing universality measure. Gate 2 verifies the co-firing positive survives
  this independent definition.

## Universality measures (the targets)
Both use ONE feature-matching step that is independent of either readout (kills the F2 shared-matching
charge): features across A and B are matched by token-level max-activation correlation (a third channel),
then both measures are read off that fixed matching.
- U_dec (decoder geometry): best cross-model decoder cosine after a least-squares linear alignment of
  B's decoder space onto A's, with ALIGN_RIDGE regularization; reported against a shuffled-decoder
  random baseline (must beat baseline for the measure to be "alive").
- U_overlap (co-firing): Jaccard overlap of the top-K activating contexts of the matched features.

## Control set (partialled out of every reported correlation)
{ marginal activation frequency, mean activation magnitude, decoder norm }. For the co-firing measure
add { marginal firing rate } (BE3). Controls are added if a new confound is found; never dropped.

## Feature-filtering policy (frozen)
Score N_ACT features from A by activation density; exclude dead features (fire on < 0.1% of contexts)
and always-on features (> 50%). Same policy every pair. N reported per cell.

## Layer-matching rule (cross-model, for BE2)
Match layers by FRACTION OF DEPTH (layer_index / n_layers), nearest fraction; report the fractions used.

## Frozen knobs
N_ACT >= 2000 (bump to 3000 only if a CI half-width exceeds 0.15, then rerun once), N_PCA per current
harness default, N_BOOT = 1000, TOPK per harness default, STANDARDIZE_RESID on for >=7B models.
