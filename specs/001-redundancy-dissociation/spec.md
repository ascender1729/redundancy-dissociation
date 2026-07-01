# Feature Specification: Redundancy Dissociation in SAE Feature Universality

**Feature Branch**: `001-redundancy-dissociation`
**Created**: 2026-07-01
**Status**: Draft (pre-registration gate open)
**Target venue**: BlackboxNLP 2026, Special Track "Reproducibility and Reliability in Interpretability Analyses" (6pp) OR Full paper (8pp). Deadline 2026-07-17 AoE.
**Input**: Corrected-harness SAE interpretability study. Within-model SAE-feature redundancy predicts co-firing universality across model pairs but does NOT predict decoder-geometry universality. A prior positive decoder claim (+0.27) was a harness artifact and has been corrected to +0.001.

---

## 1. Problem Statement

Practitioners increasingly treat sparse autoencoder (SAE) features as a lens on "universal" structure shared across language models, and reach for cheap, single-model proxies to guess which features will transfer. One intuitive proxy is within-model redundancy: how recoverable a feature is from the rest of one model's own activations, with no access to a second model. The open question this paper answers is narrow and mechanical: does within-model redundancy actually predict cross-model feature universality, and if so, universality under which operationalization?

The finding is a dissociation. Redundancy predicts one kind of universality (co-firing structure) but not another (decoder-geometry alignment), and the co-firing effect is itself pair-dependent (present for near model pairs, absent or weaker for far pairs). This matters because a single earlier version of this work reported a positive decoder-geometry correlation (+0.27) that, on a corrected measurement harness, collapses to +0.001. The corrected result is the contribution: a reliability correction plus a genuine dissociation, not a universality law.

The prior manuscript asserting the positive decoder claim was desk-rejected by TMLR with an empty editor-in-chief comment (a discretionary quality/volume screen, not a formatting defect). The corrected story fits BlackboxNLP's new reliability/reproducibility Special Track directly, and the credibility of a corrected null depends entirely on demonstrable manual harness discipline. This specification exists to freeze the claims, measures, controls, and acceptance thresholds BEFORE the remaining blocking experiments run, so the manuscript reads as confirmatory (pre-registered), not as a story fit to whatever came out.

---

## 2. Claims and Supporting Evidence

Each claim is a testable scientific assertion with a bound acceptance criterion in Section 3. All correlations are partial Spearman rho with the frozen control set (marginal firing frequency, activation magnitude, decoder norm). Raw correlations are never reported as results.

### Claim C1 (primary, positive): Redundancy predicts co-firing universality
Within-model SAE-feature redundancy, recoverable from one model's own activations with no second model, predicts co-firing universality across model pairs.

Current evidence (partial Spearman rho, controls: freq, magnitude, decoder norm):
- GPT-2 / Pythia (near pair): co-firing rho = +0.41
- Gemma-2-9b / Llama-3.1-8B (far pair): co-firing rho = +0.02 (null)
- Mistral-7B / Llama-3.1-8B (far pair): co-firing rho = +0.31

Interpretation: the co-firing effect is real but pair-dependent (strong near, present on one far pair, null on the other). C1 is therefore asserted as a pair-dependent positive effect, not a universal law (see C3).

### Claim C2 (primary, null / dissociation): Redundancy does NOT predict decoder-geometry universality
Within-model redundancy does not predict decoder-geometry universality. The decoder-geometry signal is a tight interval around zero, robust across all three pairs including two far pairs.

Current evidence (partial Spearman rho, same control set):
- GPT-2 / Pythia (near): decoder rho = +0.001 (a prior +0.27 was a HARNESS ARTIFACT, now corrected)
- Gemma-2-9b / Llama-3.1-8B (far): decoder rho = -0.16
- Mistral-7B / Llama-3.1-8B (far): decoder rho = -0.18

Interpretation: the decoder-geometry null/negative is robust across three pairs. Combined with C1 on the SAME data, this is a dissociation, which is a positive structural claim (the two operationalizations behave differently), not a mere absence of an effect.

### Claim C3 (scope / honesty): The co-firing effect is pair-dependent and is not a frequency proxy
The co-firing effect is real but pair-dependent (near vs far) and survives partialling out marginal firing rate, so it is not merely a base-rate/frequency confound.

Supporting evidence: all three pairs reported (C1); the co-firing frequency-confound check (blocking experiment 3) partials out marginal firing rate and C1 must survive it.

### Claim C4 (robustness): The dissociation is not a single-layer accident
The decoder-geometry null (C2) reproduces across multiple layers on at least one far pair, so the dissociation is a property of the phenomenon, not of one arbitrarily chosen layer.

Supporting evidence: multi-layer sweep on one far pair (blocking experiment 2), at least three layers.

---

## 3. Acceptance Criteria

Each criterion names the exact statistic, threshold, and pair(s) that CONFIRM or REFUTE the claim. Thresholds are frozen at commit of this spec (record the git SHA in the reproducibility appendix). A claim that fails its criterion is reported as refuted or scoped down in the manuscript; criteria are not moved after runs. Publishability and desk-reject resistance are treated as first-class acceptance requirements (Section 3.5).

### AC1 (backs C1)
Partial Spearman rho for the co-firing measure, controls {frequency, magnitude, decoder norm}, is > +0.20 with p < 0.01 on at least 2 of the 3 pairs.
- Confirm state (current): +0.41 near (pass), +0.31 far (pass), +0.02 far (fail) -> 2 of 3 pass. C1 CONFIRMED as pair-dependent.
- Because 1 of 3 is null, C1 MUST be stated as pair-dependent (routes to C3); it may not be written as a universal effect.

### AC2 (backs C2)
Partial Spearman rho for the decoder-geometry measure lies within [-0.20, +0.10] (i.e. not positive beyond noise) on ALL 3 pairs, AND the alignment-null control (blocking experiment 1) shows the near-pair decoder signal is statistically indistinguishable from the permutation null.
- Confirm state (current): +0.001 near, -0.16 far, -0.18 far -> all three in interval. Pending alignment-null control.
- The alignment-null control must additionally serve as a positive control: the decoder measure must detect injected/real structure when it exists (so the null is a true absence, not a dead measure).

### AC3 (backs C3)
Report all three pairs in the main text. The co-firing frequency-confound check (blocking experiment 3) must show C1's surviving pairs retain rho > +0.20 after additionally partialling marginal firing rate; if any pair drops below +0.20, that pair is reclassified as frequency-driven and stated as such.

### AC4 (backs C4)
Multi-layer sweep on one far pair (blocking experiment 2) reproduces the AC2 decoder null (rho within [-0.20, +0.10]) at >= 3 distinct layers.

### 3.5 Publishability and desk-reject-resistance criteria (must all hold before submit)
- P1 Every sentence in the abstract maps to a passing acceptance criterion (C1..C4). No abstract claim without a backing AC.
- P2 The decoder null (C2) is reported with confidence intervals demonstrating a TIGHT near-zero interval, plus the alignment-null positive control proving the measure CAN detect structure. (Preempts "you just failed to find it" and "the measure is dead".)
- P3 The dissociation is stated as a positive structural claim in the abstract, with a one-line actionable takeaway: within-model redundancy predicts which SAE features share co-firing structure across models but does NOT predict decoder-geometry alignment; practitioners should not use redundancy as a proxy for representational universality.
- P4 The prior +0.27 decoder value is stated explicitly as a harness artifact, with the corrected +0.001, framed as a reliability contribution aligned to the Special Track theme.
- P5 Robustness shown in a single table across 3 pairs (2 far) plus the multi-layer sweep; co-firing frequency-confound check and the partial-Spearman control set reported in MAIN TEXT, not appendix-only.
- P6 Every numeric value in the PDF traces to an S3 artifact key + the git SHA of `run_big_pair.py` + seed (reproducibility appendix). No orphan numbers.
- P7 Format: unmodified ACL template; <= 8pp (Full) or <= 6pp (Special Track), refs excluded; titled "Limitations" and "Ethical considerations" sections present and excluded from the count; ACL pubcheck clean.
- P8 Double-blind: author names, affiliations, acknowledgements, funding (Lambda/AWS), grant IDs removed from body and PDF metadata; self-citations in third person; code released as an anonymized drop (anonymous.4open.science), not a personal GitHub/S3 link. AI-assistance disclosure statement included; Responsible NLP checklist filled honestly with real section pointers.
- P9 Single archival venue only; not under simultaneous review elsewhere. (The prior TMLR desk-reject imposes no BlackboxNLP restriction; do not arXiv in a way that entangles archival rights if TMLR remains a later target.)

---

## 4. Non-Goals (explicitly out of scope; cut from the manuscript)

- NG1 Concept-identity claims. This paper does NOT claim SAE features encode the "same concept" across models. It claims two specific operationalizations (co-firing universality, decoder-geometry universality) and never silently upgrades either to concept identity or "representational universality" as a proven fact.
- NG2 Self-preservation leg. Any narrative or experimental leg framing redundancy as a model self-preservation / robustness mechanism is CUT. It is unsupported by the measures here and dilutes the dissociation.
- NG3 Boundary / ladder overclaim. Do NOT present a graded "universality ladder" or a claimed near-to-far boundary as an established law. The pair-dependence (C3) is reported as an observation on 3 pairs, not as a calibrated threshold or a monotone boundary function. No "N-rung ladder" framing.
- NG4 Causal claims. No claim that redundancy causes universality; the relationship is predictive/correlational under stated controls.
- NG5 Scale claims. No claim about >3 pairs, no closed/proprietary models, no claim of generality beyond the tested open models and layers.
- NG6 Pre-correction numbers presented as valid. The +0.27 decoder value appears ONLY as an explicitly labeled artifact in the reliability narrative, never in a results table as if valid.

---

## 5. Rigor Principles (constitution-style; enforced on every spec/plan/task and before every compile-and-submit)

These are the scientific-integrity gates. `speckit-analyze` is run against them before each submit build; any abstract sentence not backed by a passing acceptance criterion is a gate failure.

1. Honest scope. Claims are stated at the exact operationalization tested (co-firing universality, decoder-geometry universality), never upgraded to concept identity, causation, or a universality law. Pair-dependence and layer-scope are stated wherever the effect is not universal.
2. Corrected-harness-only. Only numbers produced by the corrected measurement harness enter results. Pre-correction values (the +0.27 decoder) appear solely as labeled artifacts in the reliability narrative. No pre-correction number is ever presented as valid.
3. Harness-artifact firewall. Any positive effect must be reproduced by an independent code path OR pass a null/permutation control before it enters the abstract. This is the direct lesson from the +0.27 artifact. (Operationalized as a clean-checkout reproduction of the +0.41 near co-firing cell.)
4. Partials mandatory. Every reported correlation is a partial Spearman rho with the frozen control set {frequency, magnitude, decoder norm}. A raw correlation is never a result. New confounds identified (marginal firing rate for co-firing; permuted matching for decoder) are added as controls, never dropped.
5. Variance-explained reporting. Report effect sizes with confidence intervals and, where applicable, variance explained, not just point rho and a p-value. A null is reported as a TIGHT interval around zero (an evidenced claim of absence), never as a bare non-significant p-value.
6. Null results are first-class. The decoder-geometry null is a headline finding, not a failure. The paper is a dissociation paper. Runs are never engineered to convert nulls into positives.
7. Falsifiable acceptance criteria only. Each claim names the exact statistic, threshold, and pair(s) that confirm or refute it, frozen before runs (Section 3). Criteria are not moved after seeing results.
8. Reproducibility contract. Every number in the PDF traces to an S3 artifact key + git SHA of `run_big_pair.py` + seed. No orphan numbers. Measures are frozen in `contracts/measures.md` before the first blocking run.
9. Cost/safety rails preserved. All runs stay on the detached Lambda pattern (dead-man switch + self-terminate, ~$0.40 and ~15 min per run, results to S3). No long-lived GPU. Total blocking-experiment budget under ~$6.

---

## 6. Remaining Blocking Experiments (must land before submit)

Frozen measures live in `contracts/measures.md`; the analysis plan (alpha, permutation counts, multiple-comparison handling across the 3 pairs, confirm/refute rules) lives in `contracts/analysis-plan.md`. Both are committed with a SHA before any run.

- BE1 Alignment-null control for the decoder measure. Permutation of the cross-model matching; establishes the AC2 null AND serves as the positive control (measure detects structure when present). Feeds AC2, P2.
- BE2 Multi-layer sweep on one far pair (Mistral-7B / Llama-3.1-8B), >= 3 layers, both measures. Feeds AC4, P5.
- BE3 Co-firing frequency-confound check. Re-run C1 additionally partialling marginal firing rate, all 3 pairs. Feeds AC3, P5.
- BE4 (firewall) Clean-checkout reproduction of the +0.41 near co-firing cell via the corrected harness. Feeds rigor principle 3.

Open design questions for `speckit-clarify` before planning: far pair chosen for the layer sweep (Mistral/Llama vs Gemma/Llama), permutation-null iteration count, alpha and multiple-comparison correction across the 3 pairs.

---

## 7. Definition of Done

- All four ACs (AC1..AC4) evaluated with an explicit CONFIRMED/REFUTED/SCOPED verdict recorded in `acceptance.md`.
- All P1..P9 publishability/desk-reject criteria satisfied.
- PDF compiles with 0 LaTeX errors, no company branding, ACL pubcheck clean, double-blind verified (including PDF metadata).
- Every number cites an S3 key + git SHA + seed.
- `speckit-analyze` passes against the rigor principles in Section 5.
