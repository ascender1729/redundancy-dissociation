# Supplementary material: Two Measurement Artifacts, an Unenforced Null, and What Survives

Anonymous supplementary package. Every number in the paper regenerates from the released
per-feature arrays on a CPU in seconds.

## Contents
- data/close.npz, data/gemma.npz, data/far2.npz: per-feature arrays for the three model pairs
  (GPT-2/Pythia near; Gemma-2-9b/Llama-3.1-8B far; Mistral-7B/Llama-3.1-8B far). Each contains,
  per feature (N=2500): redundancy_R2 (real), redundancy_R2_shuf (position-shuffle null),
  U_dec (decoder-cosine universality), U_overlap (co-firing Jaccard), freq, mag, dec_norm
  (the three controls).
- recompute_partials.py: regenerates Table 2 (Block 1-3: partials, permutation nulls,
  bootstrap CIs), Table 1 (Block 4: position-shuffle null and incremental partials), and the
  bootstrap CIs quoted in Section 6 (Block 4b).
- robustness_checks.py: even/odd split, Kendall tau, frequency-quintile-matched partials.
- make_figs.py: regenerates the forest figure from the arrays.
- test_harness_bug.py: regression test for Artifact 1 (the ridge floor); fails pre-fix,
  passes post-fix.
- contracts/: the frozen pre-registration (measures, analysis plan, artifact documentation,
  gate-3 reconciliation).

## Reproduce
python recompute_partials.py
python robustness_checks.py
python test_harness_bug.py
python make_figs.py

Requirements: python 3.10+, numpy, scipy, matplotlib. No GPU, no model downloads; runtime is
seconds for Blocks 1-4 and a few minutes for the bootstrap blocks.
