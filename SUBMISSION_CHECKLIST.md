# SUBMISSION_CHECKLIST.md
# Paper: redundancy_dissociation.tex (reliability / two-artifacts-plus-dissociation)
# Target: BlackboxNLP 2026, reliability / negative-results (R&R) track
# Deadline believed ~2026-07-17 (UNVERIFIED - see VENUE_NOTES.md, verify FIRST)
# Estimated total effort: ~3 working days core path (matches audit's days_to_submittable=3);
#   ~5-6 days if the optional robustness reruns (item E1) are included.
# Do NOT edit numbers in the .tex without re-verifying against contracts/gate3-reconciliation.md
# and rerunning recompute_partials.py. Freeze SHA 37a266f is the reference state.

Status legend: [ ] open, [x] done. Every item lists an effort estimate.
Items marked BLOCKER must be done before submission. Items marked SHOULD are
strongly recommended. Items marked OPTIONAL can slip if the deadline is tight.

---

## Phase 0 - Venue verification (do first, everything else depends on it)

- [ ] 0.1 BLOCKER - Verify BlackboxNLP 2026 CFP: exact deadline, track names,
      page limits (short vs long), archival vs non-archival options, style file
      version, and anonymity policy. Believed deadline 2026-07-17 is UNVERIFIED.
      Effort: 0.5 h.
- [ ] 0.2 BLOCKER - Download the required ACL style file kit named in the CFP
      (acl.sty / *.cls + template) and confirm it compiles standalone.
      Effort: 0.5 h.

## Phase A - ACL template conversion (BLOCKER)

- [ ] A.1 BLOCKER - Convert from plain article class (11pt, 1-column,
      \date{Draft \today}) to the ACL style file with the [review] option:
      two-column, ACL front matter, no \date, line numbers on. Reflow the 4-page
      draft and check the results table fits a column or use table* spanning.
      Effort: 2-3 h.
- [ ] A.2 BLOCKER - Move Limitations to the ACL-mandated position: unnumbered
      section immediately after the body, before References (currently a normal
      numbered section). Effort: 0.5 h.
- [ ] A.3 BLOCKER - Add the missing Ethics statement (the paper's own P7/P8 TODO
      comment). Port and adapt the Ethics statement from the rejected TMLR
      version (nl_universality_paper_tmlr.tex). Low-risk content: open-weights
      models, no human subjects, no PII. Effort: 0.5 h.
- [ ] A.4 BLOCKER - Page-limit fit check after the Related Work and appendix
      ports (Phase C/D below add material). Decide short vs long paper based on
      the verified limits from 0.1; appendices typically do not count but
      confirm in the CFP. Effort: 0.5 h (recheck at the end).

## Phase B - Anonymization (BLOCKER)

- [ ] B.1 Confirmed OK in audit: tex body uses [anonymized for review], no
      identity strings. Re-grep after every edit pass anyway:
      grep -i for author names, "vibetensor", "pavan", "ascender1729",
      dubasipavankumar, ORCID, and Windows user paths. Effort: 0.25 h per pass.
- [ ] B.2 BLOCKER - recompute_partials.py has a hardcoded path that leaks the
      username (C:/Users/pavan/...). Repoint to a relative path or an
      ARRAYS_DIR environment variable before the script ships with the
      submission package. Effort: 0.5 h.
- [ ] B.3 BLOCKER - Any repo/code/data link in the paper must go through an
      anonymous host (anonymous.4open.science, or Zenodo/OSF anonymized link,
      per whatever the CFP allows). No github.com/ascender1729 links.
      Effort: covered by B.2 + C.1.
- [ ] B.4 SHOULD - Check PDF metadata after final compile (pdflatex embeds no
      author by default with anonymized front matter, but verify with
      pdfinfo/exiftool that Author/Creator fields are clean). Effort: 0.25 h.

## Phase C - Reproducibility package (BLOCKER - the released-arrays claim is currently unbacked)

- [ ] C.1 BLOCKER - The per-feature arrays (close.npz, gemma.npz, far2.npz)
      exist ONLY in a session temp scratchpad
      (C:/Users/pavan/AppData/Local/Temp/...) and *.npz is gitignored. They are
      at deletion risk. TODAY: copy them into a durable local location inside
      the repo tree (or an _archive/ sibling), then upload to a durable
      anonymous host and put that link in the paper. Do this before anything
      else in this phase - if the temp dir is cleaned, the reproducibility
      claim and the paper's verification story die. Effort: 1-2 h (mostly
      upload + link plumbing).
- [ ] C.2 BLOCKER - Repoint recompute_partials.py to the released arrays
      (relative path / env var per B.2) and re-run it end-to-end against the
      uploaded copies to confirm all 6 table cells, both CIs, the
      [-0.04,+0.04] permutation band, p=0.001 and Gemma p=0.836 still
      reproduce exactly. Effort: 0.5 h.
- [ ] C.3 BLOCKER - Figures: fig_*.pdf and their generation script are
      gitignored / not committed. Commit the generation script and either the
      PDFs or a make-figures entry point; the submission PDF must embed the
      final figures. Effort: 0.5 h.
- [ ] C.4 BLOCKER - Add a Reproducibility statement: port the one from the TMLR
      version, including the transformer_lens 2.18 vs 3.x numerics pinning
      gotcha, the CPU-only recompute path (recompute_partials.py), the
      regression test test_harness_bug.py (pre-fix -3.48e4, floored -1.0), and
      freeze SHA 37a266f. Effort: 0.5-1 h.

## Phase D - Content: citations and ports from the rejected TMLR paper (BLOCKER for D.1-D.2)

- [ ] D.1 BLOCKER - Citations: the salvage has ZERO citations and no
      bibliography - desk-reject risk at any ACL venue. Port
      nl_universality_references.bib and wire \cite calls. Effort: 1 h
      mechanical, plus writing time in D.2/D.3.
- [ ] D.2 BLOCKER - Port Related Work nearly wholesale from the TMLR version:
      Lan 2024 (measuring universality), Thasarathan 2025 (joint universal
      SAE), Paulo 2025 (SAEs learn different features), Platonic Representation
      Hypothesis, CKA/stitching. Add a reliability/reproducibility-of-
      interpretability paragraph to match the R&R track framing. Effort: 2-3 h.
- [ ] D.3 SHOULD - Condense the TMLR Sec 2 Background into ~2 paragraphs:
      natural latents, mediation as conditional independence / common-cause
      screening (Pearl), redundancy as recoverability (Cover), PID distinction
      (Williams-Beer). Update for the ridge-R2 recoverability
      operationalization. Effort: 1-2 h.
- [ ] D.4 SHOULD - Port the Statistical Caveats paragraph (max-over-g selection
      bias, bootstrap CI understatement) into Methods/Limitations - it applies
      directly to the co-firing target. Effort: 0.5-1 h.
- [ ] D.5 SHOULD - Port the KSG mediation structural null as a short appendix
      (mediator near-constant: mean 0.0004, std 0.0038; calibrated estimator
      separation 0.52). It is a second, independent measurement-reliability
      finding, directly on-theme for the track. Effort: 1-2 h.
- [ ] D.6 OPTIONAL - Port the intervention appendix (redundancy penalty and
      density inseparable in L1/top-k SAE families, per-seed table), rescoped
      as structural, NOT causal. Effort: 1-2 h.
- [ ] D.7 SHOULD - Port the semantic-correspondence appendix as the explicit
      caveat on the surviving co-firing positive (document-level co-firing vs
      concept identity; overlap-matched random-partner null; anti-placebo
      AUROC 0.94 gate). Effort: 1 h.
- [ ] D.8 BLOCKER (negative constraint) - Do NOT port: TMLR Table 1/panel
      numbers, the sufficiency/screening/forest figures, the cross-scale Gemma
      positives, or ANY rho produced by the pre-fix pipeline. The scatter +
      binned-mean presentation STYLE is reusable for the co-firing panel; the
      artifact-era numbers are not. Effort: 0 h (vigilance during D.2-D.7).

## Phase E - Pre-registration honesty (BLOCKER - must be scoped in the text)

- [ ] E.0 BLOCKER - Fix the C1 narration: Mistral co-firing +0.169 is BELOW the
      frozen AC1 threshold (rho > +0.20), so per contracts/analysis-plan.md C1
      is confirmed on only 1 of 3 pairs, not the "2 of 3 positive" currently
      narrated. Either report against the frozen threshold honestly (1/3
      confirmed, 1/3 positive-but-below-threshold, 1/3 null) or explicitly
      mark the descriptive "2 of 3 positive" as post-hoc and separate from the
      pre-registered confirmation. Effort: 1 h.
- [ ] E.1 BLOCKER - Declare the bootstrap deviation: per-feature bootstrap was
      used instead of the frozen co-firing-clustered group bootstrap. One
      sentence in Methods + one in Limitations. Effort: 0.5 h.
- [ ] E.2 BLOCKER - Declare the un-run BE3 firing-rate control for co-firing as
      a pre-registered analysis not executed; scope the co-firing claim
      accordingly (it may retain co-activation base-rate structure - the paper
      already concedes this). Effort: 0.5 h.
- [ ] E.3 BLOCKER - Report N per cell (2500 features/pair) in the results
      table, as required by contracts/measures.md. Effort: 0.25 h.
- [ ] E.4 SHOULD - Housekeeping outside the tex: add a superseded-by-Gate-3
      note to harness-bug.md Gate 2, which still cites the stale pre-Gate-3
      pilot value +0.41 (superseded by the frozen rank-based partial Spearman
      +0.29/+0.17). Prevents future self-confusion and reviewer confusion if
      contracts are released. Effort: 0.25 h.
- [ ] E.5 SHOULD - Limitations must name the two open scoping runs from the
      frozen plan (multi-layer sweep - currently one layer per pair; third far
      pair not anchored on Llama-3.1-8B) and state that AC4 of the frozen plan
      is unmet, with claims scoped to the layers/pairs actually run. The
      TMLR depth-matrix design can be cited as the planned scoping frame.
      Effort: 0.5 h.
- [ ] E.6 OPTIONAL - Add one honest paragraph on the unresolved Gemma/Llama
      co-firing null (p=0.836) vs the Mistral/Llama positive - flagged but not
      explained. Offer hypotheses only, no new claims. Effort: 0.5-1 h.

## Phase F - Optional analysis reruns (OPTIONAL - only if deadline allows)

- [ ] F.1 OPTIONAL - Rerun the four TMLR robustness designs under the frozen
      rank-based estimator for the co-firing target: density-binned matching
      null, Hungarian one-to-one assignment, coefficient-of-variation control,
      disjoint even/odd split. Designs are portable; all numbers must be
      regenerated - none of the TMLR numbers may be reused. This is the
      strongest possible answer to the base-rate caveat in E.2, but it is
      compute + analysis time. Effort: 1-2 days. If skipped, E.2's scoping
      language carries the weight.

## Phase G - Final gate (BLOCKER)

- [ ] G.1 Full recompile on the ACL style: 0 errors; rerun the number
      verification (every table cell vs recompute_partials.py output on the
      released arrays); confirm test_harness_bug.py passes at the tagged
      commit. Effort: 0.5 h.
- [ ] G.2 Anonymity grep pass (B.1) + PDF metadata check (B.4) on the final
      PDF. Effort: 0.25 h.
- [ ] G.3 Page limit + formatting checklist against the verified CFP (0.1):
      Limitations placement, Ethics present, references style, line numbers.
      Effort: 0.5 h.
- [ ] G.4 Tag the submission commit; record it next to freeze SHA 37a266f.
      Effort: 0.25 h.

---

## Effort roll-up

| Phase | Blockers | Should | Optional |
|---|---|---|---|
| 0 Venue verify | 1 h | - | - |
| A ACL template | 3.5-4.5 h | - | - |
| B Anonymization | 0.75 h + passes | 0.25 h | - |
| C Repro package | 2.5-4 h | - | - |
| D Ports/citations | 3-4 h | 3.5-5.5 h | 1-2 h |
| E Pre-reg honesty | 2.25 h | 1.25 h | 0.5-1 h |
| F Robustness rerun | - | - | 1-2 days |
| G Final gate | 1.5 h | - | - |
| Total | ~14-18 h (~2 days) | ~5-7 h (~1 day) | +1-2 days |

Core path (all BLOCKER + SHOULD): ~3 working days. With F.1: 5-6 days.
Deadline believed 2026-07-17 leaves ~10 calendar days - F.1 is feasible but
verify the deadline (0.1) before committing to it.
