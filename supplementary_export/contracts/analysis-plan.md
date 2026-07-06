<!-- FROZEN before any blocking GPU run. Commit with git SHA; do not edit after freeze. -->
# Contract: analysis plan

## Statistic
Partial Spearman rho of (redundancy_R2, U) given the frozen control set, per pair per measure.
Primary effect size: variance explained (rho^2), reported alongside rho. p-values secondary.

## Significance and correction
- alpha = 0.01.
- Family = full grid { 3 pairs x 2 measures x layers tested }. Holm-Bonferroni across the family for
  any claim that aggregates cells.
- Null claims (decoder) require BOTH: (a) the partial rho CI upper bound < +0.10, AND (b) the
  alignment-null positive control passes (measure detects real structure at p < 0.01). A null without
  (b) is unpublishable (dead-measure risk).

## Uncertainty (dependence-respecting)
Feature-bootstrap 95% CI, n = 1000, resampled over CO-FIRING-CLUSTERED feature GROUPS (not individual
features), because features co-fire and are not independent. Report the CI half-width; if > 0.15 the
cell is "underpowered" -> bump N_ACT to 3000 and rerun once, else report as underpowered, not as a result.
Permutation null for the alignment control: N = 1000 shuffles of the cross-model matching.

## Confirm / refute / scope rules (frozen; see spec.md Section 3)
- AC1 (co-firing predictor): partial rho > +0.20, p < 0.01 on >= 2 of 3 pairs -> C1 CONFIRMED, and
  MUST be written pair-dependent (one pair may be null).
- AC2 (decoder null): partial rho in [-0.20, +0.10] on ALL 3 pairs AND alignment-null control passes.
- AC3 (freq confound): surviving co-firing pairs keep rho > +0.20 after also partialling firing rate.
- AC4 (layers): AC2 null reproduces at >= 3 layers on one far pair.
- Any cell below its threshold is reported as refuted/scoped in the manuscript; thresholds never move.

## Min N-per-cell floor
A cell with < 800 retained features after filtering is "underpowered, not reported".

## HARKing defense
This plan and contracts/measures.md are committed with a git SHA BEFORE any blocking run. Point
estimates live only in pilot-notes.md (labeled non-confirmatory) and never in spec.md Section 2 at
freeze time.
