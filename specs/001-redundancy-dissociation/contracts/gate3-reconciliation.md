<!-- Gate 3 result. A SECOND methodological artifact; changes the frozen numbers. -->
# Gate 3 - permutation-null control + a second artifact (partial-method sensitivity)

Done offline ($0) on the released per-feature arrays (redundancy_R2, U_dec, U_overlap, freq, mag,
dec_norm; 2500 features/pair). This is the reviewer-reproducible recomputation (P6).

## The second artifact
The harness computed the partial by residualizing RAW redundancy and RAW U on RAW controls
(freq/mag/decnorm), then Spearman of residuals ("multiresid"). Because the controls are skewed, this
non-standard partial is scale-sensitive. The STANDARD partial Spearman (rank all variables, residualize
on RANKED controls, then Pearson) gives different values, most starkly on the near pair:

| Pair | U_dec: standard | U_dec: harness-multiresid |
|---|---|---|
| GPT-2/Pythia (near) | -0.122 | +0.001 |
| Mistral/Llama (far) | -0.159 | -0.177 |

So the previously reported near-pair "corrected +0.001" was itself a partial-method artifact. This is a
second reliability lesson (after the R2 floor).

## FROZEN method (supersedes the harness multiresid)
Partial Spearman = rank(x), rank(y), rank(each control); residualize rank(x) and rank(y) on the ranked
controls (OLS + intercept); Pearson of the residuals. All reported numbers use THIS method, recomputable
by a reviewer from the released arrays via the committed script.

## Reconciled results (standard method; permutation null N=1000; feature-bootstrap 95% CI)
| Pair | U_dec rho | U_dec boot95 | perm_p | U_overlap rho | U_overlap boot95 | perm_p |
|---|---|---|---|---|---|---|
| GPT-2/Pythia (near) | -0.122 | [-0.163,-0.081] | 0.001 | +0.291 | [+0.250,+0.331] | 0.001 |
| Gemma-9b/Llama-8b (far) | -0.169 | [-0.208,-0.128] | 0.001 | +0.005 | [-0.033,+0.047] | 0.836 |
| Mistral-7b/Llama-8b (far) | -0.159 | [-0.200,-0.119] | 0.001 | +0.169 | [+0.130,+0.209] | 0.001 |

## Revised claims (honest)
- C2 (decoder): NOT a clean null. Redundancy is WEAKLY NEGATIVELY associated with decoder-geometry
  universality, consistently across all 3 pairs (rho in [-0.17,-0.12], all outside the permutation
  null). Variance explained 1.5-2.9%. Small but real and consistent, not zero.
- C1 (co-firing): positive on 2 of 3 pairs (near +0.29, Mistral +0.17), null on Gemma (+0.005, inside
  the null band). Pair-dependent, as before.
- The dissociation stands and is sharper: co-firing positive (2/3) vs decoder consistently small-negative.
- Two artifacts now anchor the reliability contribution: the R2 blow-up (Gate 1) and the raw-control
  partial (Gate 3).

## Positive control (measure is alive)
The decoder-cosine universality measure beats its shuffled-decoder random baseline in every run
(U_dec_beats_random = True), so the small negative is a real weak association, not a dead measure.
