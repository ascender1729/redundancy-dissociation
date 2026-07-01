<!-- NON-CONFIRMATORY pilot values. NOT part of the pre-registration. HARKing defense: these are
what the corrected harness produced BEFORE the frozen blocking runs; the confirmatory runs (contracts/)
either reproduce them or they are reported as refuted. Point estimates are kept OUT of spec.md at
freeze; spec.md Section 2 should be reduced to hypotheses-only in the freeze commit and these values
cited from here. -->
# Pilot notes (non-confirmatory)

Partial Spearman rho (controls: frequency, magnitude, decoder norm), corrected GPU harness, 3 pairs:

| Pair | Decoder-geometry U_dec | Co-firing U_overlap |
|---|---|---|
| GPT-2 / Pythia (near) | +0.001 (prior +0.27 = harness artifact) | +0.41 |
| Gemma-2-9b / Llama-3.1-8B (far) | -0.16 | +0.02 (null) |
| Mistral-7B / Llama-3.1-8B (far) | -0.18 | +0.31 |

S3 keys: 20260701_162802 (Gemma/Llama), 20260701_182729_close (GPT-2/Pythia),
20260701_185208_far2 (Mistral/Llama). Harness: research_papers/cloud_job_sae_corrected/
sae_redundancy_universality_corrected.py + run_big_pair.py (PAIR_PRESET). device=cuda, torch cu121.

CAVEAT (the reason the blocking runs exist): the co-firing +0.41 used a redundancy measure that may
share structure with co-firing (circularity, F1). Gate 2 recomputes redundancy from an INDEPENDENT
residual-stream reconstruction (contracts/measures.md); if the positive does not survive, C1 is dropped
and the paper becomes a pure alignment-artifact reliability result. The decoder null used a least-squares
cross-model alignment that itself produced the prior +0.27 artifact; the alignment-null control (BE1)
must show the corrected null is a true absence, not a dead measure.
