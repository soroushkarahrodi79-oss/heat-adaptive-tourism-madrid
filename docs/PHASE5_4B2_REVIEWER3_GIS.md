# PHASE5_4B2_REVIEWER3_GIS.md — Reviewer 3 (GIS / Spatial Decision Support / Methods)

Adversarial review of the architecture and spatial logic in
`manuscript/MANUSCRIPT_TMP_v0.2.md`.

## Overall verdict: MAJOR REVISION

The architecture is transparent and reproducible, and the separate decision fields are a
genuine (if modest) transparency contribution. My objections are that two headline results
lean on weak comparators/parameters, and that "uncertainty-aware" and "architecture"
oversell what is, mechanically, ordered rule-filtering over a hand-curated 27-asset set.

## Top 3 criticisms

**1. RQ2's "candidate set changed in 7/8" rests on a straw-man baseline. [MAJOR]**
- *Evidence:* §2.8 defines the comparator as "a deliberately naive nearest-open baseline …
  with no thermal or evidence screening." Any thermal filter necessarily changes a
  proximity-only pick, so "7/8 changed" is close to tautological.
- *Required action:* reframe RQ2 so the *contribution* is the auditable structure of the
  removals (one machine-readable reason each) and the explicit decline, not the bare "we
  differ from nearest-open." All from existing outputs; no new comparator required. (A
  proxy-screen-vs-physical-screen comparator would be stronger but needs new analysis — do
  NOT build it here.)

**2. S8's NO_DEFENSIBLE_ALTERNATIVE is contingent on a hand-picked 500 m radius. [MAJOR]**
- *Evidence:* S8 uses a 500 m reach (§Table 3), tighter than the 800 m primary; the
  accessibility sensitivity (500/1200 m) shows the recommendation category is stable in 7/8,
  with S8 the intended exception. So the one no-survivor case is produced by choosing the
  restrictive radius for that scenario.
- *Required action:* present S8 honestly as a *capability under a stated tighter constraint*
  ("the engine can return no defensible alternative when the reach is constrained"), not as
  evidence that no-alternative is a common real outcome. The manuscript half-does this
  ("valid no-survivor test"); make the contingency explicit.

**3. "Uncertainty-aware" overstates a two-source partial envelope; scalability unaddressed.
[MAJOR/MINOR]**
- *Evidence:* the envelope is solar forcing (4 realizations) + targeted geometry (2 assets);
  §5.3 already calls it partial. "Uncertainty-aware" (title-adjacent, keyword, Abstract) is
  strong for that. Separately, the engine is demonstrated on 27 manually curated assets;
  the paper claims a "transferable architecture" but the candidate-set construction is
  manual and its behaviour at realistic asset counts is untested.
- *Required action:* qualify "uncertainty-aware" once as "tested-uncertainty-aware" or
  equivalent at first prominent use; add one sentence acknowledging that scaling beyond a
  curated pilot set is untested (Limitations). No new analysis.

## Answers to the numbered challenges
1. *Contribution or rule filtering?* Mechanically rule-filtering; the contribution is
   transparency/traceability + the method-sensitivity comparison — state this plainly.
2. *Thresholds arbitrary?* Mostly grounded (see Critical Attack 3): AEMET (official),
   32/46 UTCI (Bröde, pre-registered), Δ=0.8 °C (empirical median), terciles (empirical but
   within-sample). Evidence-confidence mapping is the softest.
3. *First-failing-gate-wins defensible?* Yes, and it aids traceability — keep.
4. *Separate evidence confidence adds info?* Yes — it propagates the one UNSTABLE case into
   an exclusion (S4); a genuine, if small, demonstration.
5. *800 m straight-line undermines logic?* A real weakness (no routing, no slope); disclosed.
6. *500/1200 m sensitivity bounds it?* Partly — category stable 7/8; adequate for a pilot.
7. *Nearest-open a weak straw man?* Yes — criticism 1.
8. *Candidate sets spatially dependent, unacknowledged?* The dependence on radius/source
   location is real; S8 shows it. Acknowledge that candidate sets are configuration-dependent.
9. *2026 hours on a 2023 scenario?* Compromises specific availability (some CLOSED/open
   flags); disclosed (§5.5). Bounded.
10. *Indoor assets too generous?* Refuge-bypass with capped evidence; disclosed (§5.4) — OK
    but the reader should be reminded S1/S5 lean on indoor refuges.
11. *Scales beyond 27 curated assets?* Untested — flag (criticism 3).
12. *"Uncertainty-aware" too strong?* Slightly — criticism 3.
13. *No-survivor from meaningful evidence or restrictive params?* Both; radius-contingent —
    criticism 2.
14–15. *Figures/tables reproducible; would I reproduce the engine?* Table 2 + supplementary
    + open pipeline make it plausibly reproducible; the exact gate code is referenced, not
    printed, but the logic is specified. Adequate.

## Requests I would REFUSE as scope creep
- A routing/least-cost-path engine; slope/walk-cost model; ML ranking.
- A city-scale automated candidate-set generator (that is future work, not a fix).
