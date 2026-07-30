# VENUE_NOTES.md
# Paper: redundancy_dissociation.tex - two measurement artifacts + a sign
# dissociation in SAE-feature universality, full CPU reproducibility.
# Primary target: BlackboxNLP 2026. Fallbacks: ATTRIB (NeurIPS workshop), SoLaR.
# All deadline/page-limit/anonymity facts below are working assumptions and are
# marked VERIFIED or UNVERIFIED. Verify everything marked UNVERIFIED against the
# live CFP before planning around it.

---

## 1. Primary target: BlackboxNLP 2026

### Why it fits
- BlackboxNLP is the long-running workshop on interpreting and analyzing
  neural networks for NLP, co-located with an ACL venue. It has historically
  welcomed analysis/interpretability methodology papers and, in recent
  editions, explicitly solicited negative results, reproduction, and
  methodological-pitfall papers - the audit and comparison both reference a
  reliability / R&R (reproducibility and replicability) style track as the
  target. UNVERIFIED for 2026: confirm the track exists this year and its
  exact name in the CFP.
- The paper is close to an ideal fit for that framing:
  1. Artifact 1: unfloored ridge R2 blow-up (~-1.4e5) fabricates a positive
     decoder-geometry correlation; fix is regression-tested.
  2. Artifact 2: raw-control vs rank-based partialling flips a decoder result
     from ~0 to -0.12 on identical arrays.
  3. The surviving dissociation: the CHOICE of universality
     operationalization (decoder geometry vs co-firing) decides the sign.
  4. Every number regenerates on CPU from released per-feature arrays.
  This is a methodology-reliability paper, not a SOTA paper - exactly what a
  negative-results/reliability track wants, and it doubles as a cautionary
  postmortem of a rejected headline claim.
- The honest pre-registration accounting (frozen thresholds, declared
  deviations - see SUBMISSION_CHECKLIST.md Phase E) is a strength at this
  venue, not a weakness. Lead with it.

### Deadline
- Believed: ~2026-07-17. STATUS: UNVERIFIED. This figure comes from working
  notes, not from a checked CFP. Verify at the BlackboxNLP site
  (blackboxnlp.github.io) and the host conference's workshop page BEFORE
  scheduling the remaining work. Also record: notification date, camera-ready
  date, and workshop date.
- Check whether submission is via OpenReview or Softconf/START, and whether
  ARR (ACL Rolling Review) commitment is an accepted path in addition to
  direct submission (recent BlackboxNLP editions accepted both direct and
  ARR-committed papers). UNVERIFIED for 2026.

### Page limits (UNVERIFIED - typical pattern for recent BlackboxNLP editions)
- Archival long papers: 8 pages content + unlimited references/appendices.
- Archival short papers: 4 pages content + unlimited references/appendices.
- Often also a non-archival / extended-abstract or dual-submission track
  (useful if we later want a main-conference resubmission).
- Camera-ready usually gets +1 page.
- Current draft is 4 pages in plain article, 1-column, 11pt; after ACL
  two-column conversion plus Related Work/Background ports it will likely
  land as a comfortable short paper or a thin long paper with appendices
  (KSG null, intervention, semantic-correspondence ports go to appendix).
  Decide short vs long only after the ACL-style recompile.

### Anonymity policy (CHECK - do not assume)
- Expect standard ACL-style double-blind review for archival submissions:
  anonymized PDF, [review] style option, anonymous code/data links.
- Since 2024 the ACL-wide anonymity EMBARGO period (no preprints before
  submission) was dropped, but the SUBMISSION itself must still be anonymous.
  UNVERIFIED whether BlackboxNLP 2026 adds its own preprint restrictions -
  check the CFP. Practical consequence: an arXiv preprint is probably
  allowed, but do not put the paper on arXiv with author names and then link
  it from the submission.
- Current tex is already anonymized ([anonymized for review], no identity
  strings) but two leaks must be fixed regardless of policy:
  recompute_partials.py hardcoded C:/Users/pavan path, and any
  github.com/ascender1729 link. Use anonymous.4open.science or an anonymized
  OSF/Zenodo link for arrays + code (SUBMISSION_CHECKLIST.md Phase B/C).

### Things to verify in one CFP-reading session (30 min)
1. Deadline, notification, camera-ready dates.
2. Track names; whether a negative-results/reliability track exists and
   whether it changes review criteria.
3. Long vs short limits; whether appendices are unlimited.
4. Style file version (ACL 2026 kit vs host-conference kit).
5. OpenReview vs START; ARR commitment option.
6. Anonymity + preprint policy.
7. Archival vs non-archival choice and its dual-submission implications.
8. Whether an Ethics statement and Limitations section are mandatory
   (assume yes for both; the checklist treats them as blockers).

---

## 2. Fallback venues

### Fallback A: ATTRIB workshop (NeurIPS)
- Workshop on Attributing Model Behavior at Scale, historically at NeurIPS.
  Scope: attribution, interpretability methodology, understanding what drives
  model behavior - the artifact/reliability story and the
  operationalization-decides-the-sign result fit the methodology axis.
- UNVERIFIED: whether ATTRIB runs at NeurIPS 2026 and its deadline. NeurIPS
  workshop deadlines typically fall late Aug - early Oct 2026, which gives a
  1.5-3 month buffer after BlackboxNLP. Non-archival in past editions, so a
  BlackboxNLP reject could be revised and sent here without dual-submission
  problems - but verify both venues' dual-submission rules.
- Fit note: ATTRIB skews toward attribution/causal methods; the KSG mediation
  null appendix and the redundancy-density inseparability appendix would
  carry more weight here - if targeting ATTRIB, promote those from appendix
  toward the body.

### Fallback B: SoLaR workshop (Socially Responsible Language Modelling Research)
- Historically at NeurIPS/ICLR. Scope includes transparency, evaluation
  reliability, and responsible research practice. The paper's angle for SoLaR
  is the research-integrity one: how two silent estimator choices fabricated
  a publishable positive result, plus the pre-registration/frozen-estimator
  discipline that caught it.
- UNVERIFIED: 2026 edition, host conference, and deadline. Weaker technical
  fit than BlackboxNLP/ATTRIB - the interpretability content is a means, not
  the end, for this audience. Rank it third. If submitting here, rewrite the
  intro around measurement reliability and reporting incentives.

### Other options (not primary fallbacks, note for completeness)
- Host-conference Findings or main track via ARR: only if the robustness
  reruns (checklist F.1) and the two open scoping runs (multi-layer sweep,
  third far pair) get done; as-is the paper is scoped like a workshop paper.
- TMLR resubmission: NOT appropriate - this is the salvage of a rejected TMLR
  paper (nl_universality_paper_tmlr.tex); the surviving content is
  workshop-shaped. The separate TMLR submission under review (SAE feature
  transfer, 2026-06-28) is a different paper - keep the two clearly distinct
  in any correspondence.

---

## 3. Decision rule
1. Verify BlackboxNLP 2026 CFP first (Section 1 checklist).
2. If deadline is ~2026-07-17 and the core path (~3 days) fits: submit to
   BlackboxNLP as an archival paper on the reliability/negative-results
   track; include robustness reruns (F.1) only if time allows.
3. If the deadline has passed or the track does not exist: pivot to ATTRIB
   (NeurIPS 2026 cycle), using the buffer to complete F.1 and the two open
   scoping runs, which upgrades the paper.
4. SoLaR is the third option with an integrity-focused reframe.
