# SCIENTIFIC_INTEGRITY_FINDINGS.md — HATI-Madrid closeout audit

Findings from the pre-submission closeout audit (2026-08-22). **No scientific content was
changed to produce this document or the rest of `submission/final/`.** Findings are
classified FATAL / MAJOR / MINOR per the closeout brief and each states whether it blocks
publication. Nothing below has been silently fixed.

---

## FINDING 1 — MAJOR (blocks Tourism Management Perspectives submission)

**The reviewer-driven "targeted revision" that README.md and CITATION.cff describe as
completed is NOT actually applied to the manuscript body text.**

Evidence:
- `README.md` states: *"A reviewer-driven targeted revision has been completed on a
  development branch (`phase-5.4b3-targeted-revision`); the `main` publication snapshot
  update is pending."*
- `git branch -a` / `git ls-remote origin` show **no branch named
  `phase-5.4b3-targeted-revision`** exists anywhere in this repository, local or remote.
  Only `main` exists (plus this closeout branch, which mirrors `main`).
- `docs/PHASE5_4B2_PRE_SUBMISSION_REVISION_PLAN.md` (dated 2026-08-19, referencing
  `manuscript/MANUSCRIPT_TMP_v0.2.md`) explicitly states: *"No revisions implemented here"*
  and lists **4 MAJOR fixes (M1–M4)** as the consolidated plan from a four-reviewer QA panel.
- `docs/PHASE5_4B2_MASTER_ISSUE_REGISTER.csv` lists all 13 tracked issues (I01–I13,
  including all 4 MAJORs) with `status = OPEN`.
- A diff of `manuscript/MANUSCRIPT_TMP_v0.1.md` vs `manuscript/MANUSCRIPT_TMP_v0.2.md` (the
  two manuscript-assembly versions present in the repo) shows the **only** differences are
  in-text citation identifiers and the References list — i.e. v0.2 completed **only** the
  separate reference-verification phase (`PHASE5_4B1`), not the M1–M4 content revisions from
  `PHASE5_4B2`. No Results, Discussion, Introduction, or Conclusion prose changed between the
  two files.

What M1–M4 require (per the revision plan; **not implemented by this audit**, per §0 of the
closeout brief — scientific/interpretive content must not be edited without explicit
authorization):
- **M1** — Results §3.1 / Discussion §4.1 / Intro §1: disclose that the physically based
  configuration is single-valued (all 42 outdoor observations fall in one UTCI band), and
  stop implying the physical method supplies richer decision information than the proxy.
  Reviewer-flagged as **could cause rejection**.
- **M2** — Introduction / Discussion §4.5 / Conclusion: sharpen the tourism-management "so
  what" contribution. Reviewer-flagged as **could cause rejection (journal fit)**.
- **M3** — Results §3.2 / Discussion §4.2: reframe the "7/8 scenarios changed" finding away
  from a near-tautological contrast with a straw-man nearest-open baseline, toward the
  auditable-removal-reason contribution.
- **M4** — Results §3.2 / Discussion §4.3: make explicit that the S8 "0 survivors" result is
  contingent on the 500 m reach (vs the 800 m primary), not evidence that no-alternative
  outcomes are common.

**Why this blocks submission:** two of the four MAJOR items (M1, M3 implicitly via I03) are
flagged by the review panel itself as capable of causing rejection or credibility damage at
Tourism Management Perspectives. Submitting `MANUSCRIPT_TMP_v0.2.md` as-is would submit a
manuscript the project's own QA process has already identified as containing unaddressed
MAJOR defects.

**Recommended disposition:** Soroush (or whoever is authorized to make the prose edits)
should apply M1–M4 as scoped in `docs/PHASE5_4B2_PRE_SUBMISSION_REVISION_PLAN.md` — the plan
states each fix is a small, existing-evidence-only prose change (no new numbers, no new
analysis). This is an editorial-content decision outside this closeout's mandate ("no
estamos cambiando la metodología... conclusiones"), so it is documented here rather than
applied.

**Blocking:** YES — before Tourism Management Perspectives submission. Not blocking for
internal packaging/QA (this closeout package can still be assembled around the current
`MANUSCRIPT_TMP_v0.2.md` so that no time is lost once M1–M4 land).

---

## FINDING 2 — MAJOR (administrative, blocks DOI release and journal submission)

**CITATION.cff and the manuscript Declarations block are missing author identity,
affiliation, ORCID, funding, competing-interest, CRediT, acknowledgements, and a licence
decision.** All are explicitly marked `TO VERIFY` or `[... TO VERIFY]` in the source files —
none has been fabricated by this audit. See `HUMAN_INPUT_REQUIRED.md` for the itemised list.

**Blocking:** YES for journal submission and DOI release. NOT required to assemble the
packaging/documentation in `submission/final/`.

---

## FINDING 3 — MINOR (administrative inconsistency, does not block, should be fixed before release)

**The manuscript title differs across repository documents.**
- `manuscript/MANUSCRIPT_TMP_v0.2.md` (canonical, most recent): *"Thermal representation as
  a decision variable in heat-adaptive tourism opportunity screening: evidence from a Madrid
  pilot"* (per `docs/PHASE5_2I_TITLE_ENGINEERING.md`, this title was deliberately selected in
  Phase 5.2I).
- `README.md` "Manuscript" section and `CITATION.cff` `preferred-citation.title` still show
  the older title: *"Decision sensitivity to thermal-method choice in heat-adaptive tourism
  opportunity screening: evidence from a Madrid pilot"*, explicitly flagged there as
  provisional/under revision.

**Disposition:** this is an administrative/packaging inconsistency (not a scientific-content
change) to fix by updating README.md and CITATION.cff to match the canonical manuscript
title. **Not fixed in the main repository files by this audit** (out of the closeout's
explicit no-touch list for `README.md`'s scientific narrative) but corrected within
`submission/final/` itself, where the canonical title is used throughout.

**Blocking:** NO — cosmetic/administrative; recommended before any public release or DOI
mint so the title is consistent everywhere.

---

## FINDING 4 — MINOR (git hygiene, does not block)

The remote branch `origin/claude/hati-madrid-publication-closeout-qr0p3m` (this session's
working branch) was pruned from the local remote-tracking refs during the initial `git
fetch --prune` of this audit, with no corresponding pull request found in the repository
(`mcp__github__list_pull_requests` returned zero PRs, open or closed). This branch's commit
history is identical to `main` (`git diff HEAD origin/main` = no differences before this
audit's own commits), so no work was lost. No action required beyond pushing this audit's
commits to the branch as instructed.

**Blocking:** NO.

---

## Explicit non-findings

- No headline number (27 assets, 13/14 split, 42 observations, 33.3%, 64.3%/0.0%/35.7%,
  7/8, 3/8, S8 = 0/26 survivors at 500 m vs 800 m/1200 m, ROBUST 35 / BOUNDARY 6 / UNSTABLE
  1, A24 @ 18:00 boundary case) was recalculated. Spot-checked for internal consistency
  across README.md, `manuscript/MANUSCRIPT_TMP_v0.2.md`, `supplementary/SUPPLEMENTARY_MATERIAL_v0.1.md`,
  and `manuscript/tables/` — all consistent.
- The interpretive safeguards required by the closeout brief (SOLWEIG/UTCI is not ground
  truth; ROBUST means tested-stable, not validated; S8's no-defensible-alternative is
  reach-contingent) **are present** in `README.md`, in `MANUSCRIPT_TMP_v0.2.md` §3.3/§4.4,
  and in the Limitations section — consistently, except that Finding 1 (M1/M4) shows the
  *degree* of disclosure in the Results/Discussion prose itself still falls short of what the
  project's own review panel required.
