# Estimator choice dominates sampling error in correlation-over-features interpretability studies

A reliability study of a natural-latent prediction for sparse autoencoder (SAE)
features: that features which are redundant within a model, meaning recoverable
from disjoint parts of its own activations, are the ones that transfer to
independently trained models.

The prediction does not hold in the direction it was made. The more useful
result is what happened on the way there.

## The headline

Across 45 defensible analysis specifications per cell (270 in total, crossing
the statistic, the control set, and rank versus raw residualisation), the
near-pair decoder estimate runs from **-0.178 to +0.025** on the same 2500
features. Eight of 45 specifications are positive, 37 negative. That spread is
**10.1 standard errors** wide. Across all six cells it is 3.9 to 13.0.

The analytic standard error at N = 2500 with three controls is 0.020, so the 80
percent power minimum detectable effect is 0.056. The study was not
underpowered. Estimator choice was the binding constraint, by an order of
magnitude.

The single largest lever is the control set. Holding everything else at the
frozen setting, controlling for frequency and magnitude gives -0.171;
controlling for frequency and decoder norm gives -0.000. Same data.

Two specific choices moved the original headline from +0.27 to +0.001 to -0.12:

1. Whether the ridge R-squared is floored. Unfloored, it diverges on
   low-variance features and manufactures a positive.
2. Whether the partial correlation residualises on raw skewed controls or on
   ranks.

## What survives

Under a single frozen estimator: a weak and consistent negative association
between the redundancy score and decoder-geometry universality across three
model pairs. Partial rho in [-0.17, -0.12], all outside a permutation null,
with five of six cells surviving Holm correction.

A pre-registered position-shuffle null that the original headline was required
to beat was not enforced in the first confirmatory analysis. Enforcing it, the
co-firing positive does not beat the null on any pair (+0.29 observed against a
+0.38 null on the near pair), and redundancy adds nothing beyond it
(incremental partial rho between -0.09 and +0.02). What predicts co-firing
transfer is the shuffle-invariant context breadth of a feature's activations,
not redundancy structure.

## Setup

Three model pairs, public SAEs, one layer each, 2500 features per pair:

| Pair | Models |
|---|---|
| near | GPT-2-small, Pythia-70m-deduped |
| gemma | Gemma-2-9b-it, Llama-3.1-8B-Instruct |
| mistral | Mistral-7B, Llama-3.1-8B |

Redundancy is min(R2_L, R2_R) from a ridge predicting a feature's activation on
one residual-stream half from a PCA summary of the other half. Universality is
read two ways: cross-model decoder cosine, and Jaccard overlap of top-context
sets.

## Reproducing

Per-feature arrays are attached to the latest release. Download the three
`.npz` files into `data/`, then:

```
pip install numpy scipy matplotlib
python code/recompute_partials.py     # the six frozen cells
python code/robustness_checks.py      # permutation nulls and bootstrap CIs
python code/spec_curve.py             # the 270-specification curve
python code/power_and_spread.py       # power, spread in SE, Holm correction
python code/contamination_curve.py    # contamination sensitivity
python code/make_figs_v2.py           # regenerates all three figures
```

Everything runs on CPU in seconds. Every figure is regenerated from `data/`, so
figures cannot drift from the tables.

`code/test_harness_bug.py` is a regression test that exhibits the unfloored
ridge blowup and locks the floor in place.

## Known limitations of the released data

These are stated here because they bound what the arrays can support:

- `freq` is exactly constant at 1.0 on the gemma pair. The frequency control is
  therefore inert on that pair, which matters because gemma is the one cell
  where a redundancy-structure-specific effect was claimed.
- `dec_norm` is near-degenerate on all three pairs (range 2.9e-07 on gemma) yet
  still moves the near-pair estimate.
- A pre-registered always-on filter (greater than 50 percent firing) was not
  applied. Applying it would empty the gemma cell.
- `U_overlap` has a floor of 6/50 shared contexts against a chance expectation
  of 0.83, and is heavily tied: 38 to 44 distinct values over 2500 features.
- Reported `p = 0.001` is the floor of a 1000-shuffle permutation procedure,
  not an estimate.
- The arrays are post-floor, so the pre-floor divergence and the original +0.27
  cannot be regenerated from them directly. Applying the original harness
  convention (residualise raw on raw, then Spearman) to these arrays does
  reproduce the retracted pilot values to two decimals.

Three model pairs, one layer per model, one SAE seed. The shuffle null was run
once rather than over seeds. The context-breadth reading is post hoc.

## Status

Manuscript, not peer reviewed. `paper/estimator_choice.pdf`.

## Licence

Apache-2.0. See `LICENSE`.
