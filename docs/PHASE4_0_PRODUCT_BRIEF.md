# PHASE4_0_PRODUCT_BRIEF.md — HATI-Madrid

Version 1.0 · 2026-08-17. Specification artifact only. No implementation in
this phase. See `docs/PHASE3_TO_PHASE4_HANDOFF.md` for the locked scientific
and decision inputs this brief builds on.

## 1. What this phase is

Phase 4.0 designs the **information architecture and interaction model** for
the first HATI-Madrid visual decision-support prototype. It does not build
anything. Phases 0–3 produced a validated thermal model (Phase 2.2, MODEL
LOCKED) and a validated constraint-first screening engine (Phase 3, DECISION
ENGINE VALIDATED). Neither has a user-facing surface. This phase specifies
one, without touching the science underneath it.

## 2. Product question

How can a professional user understand — from a single interaction with the
prototype, without reading source docs —

1. what the thermal situation is,
2. whether a tourism opportunity is currently feasible,
3. how confident the system is,
4. why an option is excluded,
5. what alternative opportunities remain,
6. what trade-offs those alternatives involve,
7. when the system has no defensible alternative,

**without any of those seven questions being answered by the same visual
signal?** Each is a separate, independently-inspectable fact. Compressing
them into one score or one color scale would misrepresent what Phase 2.2/3
actually validated (a screening chain, not a ranking function) — that
compression is the primary failure mode this brief is designed against.

## 3. Audience

Primary: destination managers, tourism/urban-planning professionals, climate
adaptation teams, research and demo audiences evaluating the method.

This is **not** a consumer trip-planning app in Phase 4. It is a professional
research/decision-support interface. A tourist-facing derivative is a
plausible future direction, not a Phase 4 goal — see restrictions below.

## 4. What the prototype must demonstrate

- The screening chain's output (survivors, exclusions, and the reasons for
  each) for the 3 validated timestamps across the 27-asset catalog.
- The 8 validated scenarios (S1–S8), including S8's
  `NO_DEFENSIBLE_ALTERNATIVE` result, as first-class, inspectable content.
- That HATI's screening changes the candidate set relative to a naive
  nearest-open baseline (Phase 3 §6 finding), as an optional analysis mode.
- Uncertainty (`decision_confidence`) and evidence quality
  (`evidence_confidence`) as facts the user can see without hunting, not
  facts buried in tooltips.
- Every permanent scientific limitation (handoff §7) and the opening-hours
  temporal-alignment caveat (handoff §8), visibly and proportionately, not
  as a wall of disclaimers nobody reads.

## 5. Explicit non-goals (carried forward from the handoff, §12)

- No reopening of SOLWEIG, UTCI, thresholds, scenario definitions, candidate
  logic, or baseline comparison methodology.
- No composite/weighted score, no single "HATI score," no ranked "best
  option."
- No ML, LLM ranking, agents, personas, or behavioural prediction.
- No heat-aware route optimisation.
- No expansion beyond the pilot geography (Prado–Retiro–Atocha) or the
  27-asset catalog.
- No implication of real-time/live data — the prototype has exactly 3
  validated timestamps for one historical episode (2023-08-21).
- No treatment of opening hours as verified-for-2023 fact.
- No implementation work in this sub-phase (4.0). Phase 4.0 produces specs
  and low-fidelity wireframes only.

## 6. Success criteria for this brief

A reviewer with no prior context on HATI-Madrid should, after using the
prototype for under five minutes, be able to correctly state: what a given
asset's thermal/decision state is, how confident that state is, why a given
alternative was excluded, and that S8 represents a deliberate "no safe
option" finding rather than a broken query. If any of those requires reading
a document instead of the interface, the design has failed its own brief.

## 7. Relationship to Phase 0–3 (read-only)

All data consumed by this design is already on disk and immutable:
`data/processed/phase3_asset_catalog.csv`,
`data/processed/phase3_candidate_screening.csv`,
`data/processed/phase3_scenarios.csv`,
`data/processed/phase3_scenarios_summary.csv`,
`outputs/tables/phase3_hati_vs_baseline.csv`,
`outputs/tables/phase3_exclusion_reasons.csv`,
`outputs/tables/phase3_accessibility_sensitivity.csv`. Phase 4.0 treats these
as the entire data surface — no new fields, thresholds, or derived scores are
introduced anywhere in this design.
