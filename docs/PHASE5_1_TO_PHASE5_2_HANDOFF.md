# PHASE5_1_TO_PHASE5_2_HANDOFF.md — HATI-Madrid

Version 1.0 · 2026-08-18. The authoritative handoff from **locked literature
positioning** (Phase 5.1) to **manuscript drafting** (Phase 5.2, not yet
chartered). Pointer document — follow the references for full detail. Phase
0–5.1 decisions are **locked** and are not reopened here unless a concrete,
reproducible source contradiction is found in the repository.

---

## 1. Phase 5.0 paper charter and selected framing

**Verdict:** PAPER CHARTER APPROVED (`docs/PHASE5_0_PAPER_CHARTER.md`).
**Selected framing: A+B HYBRID** —
- **Spine (A):** a constraint-first, uncertainty-aware tourism heat-suitability
  decision architecture.
- **Empirical centerpiece (B):** the physical-vs-proxy reclassification result,
  showing thermal-*method* choice is a decision-relevant variable.

## 2. Phase 5.1 literature-positioning verdict

**Verdict:** LITERATURE POSITIONING LOCKED (`docs/PHASE5_1_NOVELTY_AUDIT.md`,
`docs/PHASE5_1_JOURNAL_FIT.md`). No DIRECT precedent found in the targeted
2024–2026 review. Closest CLOSE ADJACENT work: UTCI-adjusted pedestrian
accessibility (*Sustainable Cities and Society*, 2026), Cool Routes (*Building
and Environment*, 2026), CoolWalks (*Scientific Reports*, 2025) — all operate
downstream of candidate/destination selection.

**Editorial correction 1 (binding on all manuscript text):** the paper must never
claim universal absence of prior work. Required phrasing pattern: *"among the
closest studies identified in the targeted review..."* or *"HATI differs from the
closest identified approaches by..."* — never "no prior work exists" or "this is
the first."

## 3. Primary contribution (one, locked)

> A demonstration that thermal-*method* choice is a first-class decision variable
> in heat-adaptive tourism screening — a simple open-data proxy and a physically
> based SOLWEIG/UTCI model disagree on a material, physically interpretable share
> of feasibility classifications — delivered through a constraint-first,
> uncertainty-aware decision architecture that makes each such difference
> auditable rather than hidden inside a composite score.

(`docs/PHASE5_0_PAPER_CHARTER.md` §2.)

## 4. Final research questions

- **RQ1 (method sensitivity):** Does SOLWEIG/UTCI modelling materially alter
  tourism-feasibility classifications vs the locked simple proxy, and is the
  difference physically interpretable?
- **RQ2 (decision-support value):** Does constraint-first heat-aware screening
  change the feasible-alternative set vs a conventional nearest-open baseline,
  and decline to recommend when nothing qualifies?
- **RQ3 (robustness/traceability):** Do those decisions stay auditable and
  stable under tested uncertainty while preserving explicit no-recommendation
  outcomes?

(`docs/PHASE5_0_PAPER_CHARTER.md` §4b.)

## 5. Precise Phase 1 proxy definition (mandatory wording constraint)

The comparison baseline is the **frozen Phase 1 P0 feasibility state**:
`feasibility_decision(` AEMET **ambient air-temperature** hazard band (36/39/42 °C
civil-protection thresholds) **×** **OSM `natural=tree`-count** exposure tercile
(50 m buffer / asset polygon +15 m) `)`. **LST was never used anywhere in this
project.** No shade, shadow, canopy, or surface-temperature measurement is
involved in the baseline. Comparator = SOLWEIG UTCI (10 m-buffer mean) → UTCI
category feasibility.

**Forbidden wording:** "shade/LST-type proxy," "LST proxy," "satellite
temperature proxy," "canopy model," "shade model," or any phrase implying the
proxy measured shadow, radiant load, or surface temperature.

Full trace: `docs/PHASE5_0_PROXY_DEFINITION.md`.

## 6. Five headline findings (Tier 1 — carry the Results section)

1. **H1** Thermal-method choice reclassifies **14/42 (33.3%)** outdoor
   asset×timestamp rows; both directions occur (9 physical-more-restrictive, 5
   physical-less-restrictive). — `proxy_vs_physical_comparison.csv`
2. **H2** Divergence is **time-concentrated and mechanistically explained**:
   12:00 = 64.3%, 15:00 = 0%, 18:00 = 35.7% — at noon, air temp (34.2 °C, "LOW")
   hides modelled UTCI already ≥ 32 °C everywhere outdoors. — same file +
   `solar_forcing_sensitivity.csv`
3. **H3** Constraint-first screening changes the feasible-alternative set vs a
   nearest-open baseline in **7/8** scenarios; the naive pick fails HATI
   screening in **3/8**; 23 options removed. — `phase3_hati_vs_baseline.csv`
4. **H4** The architecture fails safe: S8 returns **NO_DEFENSIBLE_ALTERNATIVE**
   (0/26 candidates survive) rather than a forced pick. —
   `phase3_scenarios_summary.csv`
5. **H5** Core results are **robust to tested solar-forcing uncertainty**
   (real-satellite 1/42 change; ±10/±20% GHI → 0 changes). —
   `solar_forcing_sensitivity.csv`

(`docs/PHASE5_0_RESULTS_HIERARCHY.md` Tier 1.)

## 7. Locked claim ceiling

**Supported:** method choice materially and interpretably changes tourism-
feasibility classifications; a constraint-first architecture exposes these
differences, propagates tested uncertainty, changes the feasible set vs a
conventional baseline, and correctly declines to recommend when nothing
qualifies — with every decision auditable and no behavioural claim.

**NOT supported, ever:** that SOLWEIG is ground truth; that the proxy is "wrong"
in an accuracy sense (neither side is field-validated — the result is
*divergence*, not *error*); that tourist behaviour is predicted; that visitors
are redistributed; that HATI improves observed tourism outcomes; that the
framework is a methodological breakthrough; that the single Madrid pilot
generalizes automatically.

(`docs/PHASE5_0_PAPER_CHARTER.md` §6; core positioning constraints from the
Phase 5.0 charter request.)

## 8. Routing / accessibility / HATI distinction

| | THERMAL ROUTING | THERMAL ACCESSIBILITY | **HATI** |
|---|---|---|---|
| Question | Given O and D, which path is coolest? | Given a destination set, how many are reachable under heat? | **Which tourism opportunities stay feasible at this hour, why, with what confidence, and what alternatives survive?** |
| Input assumed given | origin + destination | destination set | **nothing downstream — HATI produces the candidate set** |
| Exemplars | Cool Routes 2026; CoolWalks 2025 | UTCI-adjusted pedestrian accessibility 2026; RUCS | — |

**Editorial correction 2 (binding):** the routing-literature pattern-match risk
(R4, "this is just another heat-aware routing paper") is treated in all
manuscript text as **strongly mitigated by this distinction, not eliminated**.
The boundary must be asserted explicitly and early (Introduction Step 4 /
Literature §2), not assumed self-evident.

Full table: `docs/PHASE5_1_NOVELTY_AUDIT.md` §3.

## 9. Journal targets

- **PRIMARY:** *Tourism Management Perspectives* — native tourism-decision-
  support home; scope explicitly invites new methods and critiques of existing
  ones; tolerant of single-destination applied studies; least likely to demand
  Tmrt/UTCI field validation.
- **SECONDARY:** *Sustainable Cities and Society* — scope explicitly names
  "decision support for trade-off and uncertainty analysis"; strongest
  geospatial/methodological fit; tourism reframed as application domain.
- **SAFER:** *Urban Climate* — lowest friction with the evidence ceiling
  (single-day, no-field-validation applied UTCI studies are native); tourism
  framing lightened toward urban-climate-methods identity.
- **Rejected as poor fit:** *Journal of Destination Marketing & Management*
  (no marketing/demand contribution), *Tourism Geographies* (no critical-theory
  contribution).

(`docs/PHASE5_1_JOURNAL_FIT.md`.)

## 10. Permanent limitations (must stay visible in Limitations §7)

1. No field validation of Tmrt/UTCI anywhere in the project.
2. A24 @ 18:00 is a genuine, irreducible solar-boundary UNSTABLE case.
3. Tested uncertainty covers only solar forcing + 2-asset geometry — not
   humidity/wind/model-structural uncertainty.
4. Accessibility is straight-line only; no walking-route heat exposure.
5. No behavioural claim — screening only, not prediction of tourist choice.
6. Indoor refuge assumes thermal buffering without verified A/C or
   queue-exposure modelling.
7. Opening hours are 2026-documented values applied to the 2023 study date.

(Carried unchanged from `docs/PHASE4_1_TO_NEXT_PHASE_HANDOFF.md` §7.)

## 11. Highest-priority references/clusters (Introduction & Discussion)

**Introduction (evidence chain, `docs/PHASE5_1_INTRO_LOGIC.md`):**
1. Tourism heat-governance gap — heat risk action planning for tourism (*Annals
   of Tourism Research*, 2026).
2. Composite tourism-climate-index tradition & its weight-sensitivity —
   HCI/TCI inter-comparison (*Atmosphere*, 2016); tourism-climate-index
   reliability (*Earth Perspectives*, 2016).
3. Physical modelling rarely wired to tourism screening — SOLWEIG 1.0 (2008);
   WRF-UCM-SOLWEIG (*Sustainable Cities and Society*, 2024); "Beyond LST" (2026).
4. Routing/accessibility operates downstream — Cool Routes (2026); CoolWalks
   (2025); UTCI-adjusted pedestrian accessibility (2026); sidewalk heat-risk
   (2025).

**Discussion (per-finding comparison sets, `docs/PHASE5_1_DISCUSSION_MAP.md`):**
H1/H2 → composite-index tradition + SOLWEIG/MRT radiant-load literature; H3/H3b →
routing/accessibility literature + tourism heat-governance; H4 → climate-shelter/
refuge accessibility equity literature (Barcelona mobility justice, 2025); H5 →
uncertainty-aware spatial decision support (participatory GIS under uncertainty,
2025; Monte-Carlo UTCI/PET reliability, 2025).

Full 35-source matrix: `docs/PHASE5_1_LITERATURE_MATRIX.csv`.

## 12. Prohibited overclaims (consolidated, binding on all manuscript text)

- SOLWEIG as ground truth / validated accuracy.
- Proxy as "wrong" (accuracy framing rather than divergence framing).
- Any behavioural, adoption, redistribution, or outcome-improvement claim.
- Methodological-breakthrough framing.
- Automatic generalization beyond the single Madrid pilot.
- Universal absence of prior work (editorial correction 1, §2 above).
- Treating the routing pattern-match risk as fully eliminated rather than
  strongly mitigated (editorial correction 2, §8 above).
- LST, shade-model, or canopy-model language for the Phase 1 proxy (§5 above).

## 13. Manuscript architecture (skeleton only — no prose)

Introduction → Literature/conceptual positioning → Study area & data → Methods
(4.1 proxy baseline · 4.2 physical thermal modelling · 4.3 uncertainty treatment
· 4.4 constraint-first tourism screening · 4.5 baseline comparison) → Results
(5.1 method sensitivity · 5.2 decision-support value · 5.3 robustness &
traceability) → Discussion → Limitations → Conclusion → Back matter (data
availability, reproducibility, optional prototype appendix).

Full section-by-section purpose/claims/evidence/exclusions:
`docs/PHASE5_0_MANUSCRIPT_ARCHITECTURE.md`.

## 14. Figure / table plan

**Figures (6 main + 1 optional appendix):** F1 study area + pipeline; **F2
proxy-vs-physical classification difference (centerpiece)**; F3 UTCI spatial/
timestamp differentiation; F4 uncertainty/robustness; F5 decision architecture;
F6 baseline-vs-HATI scenarios incl. S8; F7 (optional) visual prototype. None of
the existing `outputs/maps/*.png` are publication-ready as-is — full detail and
re-render/new-artwork status per figure: `docs/PHASE5_0_FIGURE_PLAN.md`.

**Tables (5 main + 2 supplementary):** T1 data sources/provenance; T2 decision
architecture (gates/thresholds/exclusion vocabulary); **T3 proxy-vs-physical
reclassification (centerpiece)**; T4 scenario comparison S1–S8; T5 limitations/
evidence boundaries — all main text. T6 proxy-family agreement, T7 solar-forcing
& accessibility sensitivity detail — supplementary.
(`docs/PHASE5_0_MANUSCRIPT_ARCHITECTURE.md` §10.)

## 15. Exact repository evidence files per Results subsection

- **5.1 Method sensitivity (RQ1):** `outputs/tables/proxy_vs_physical_comparison.csv`,
  `data/processed/phase2_asset_thermal_exposure.csv`,
  `outputs/tables/solar_forcing_sensitivity.csv`.
- **5.2 Decision-support value (RQ2):** `outputs/tables/phase3_hati_vs_baseline.csv`,
  `data/processed/phase3_scenarios_summary.csv`,
  `outputs/tables/phase3_exclusion_reasons.csv`,
  `outputs/tables/phase3_accessibility_sensitivity.csv`.
- **5.3 Robustness & traceability (RQ3):** `outputs/tables/solar_forcing_sensitivity.csv`,
  `data/processed/phase2_2_decision_confidence.csv`.

Claim-level traceability (every C1–C15 → file → statistic → allowed/forbidden
wording): `docs/PHASE5_0_EVIDENCE_MATRIX.csv`.

---

## 16. Lock status

Phase 0 through 5.1 verdicts, evidence, and framing are **locked** and carried
into Phase 5.2 unchanged. They are not to be reopened, revised, or re-derived
during manuscript drafting **unless a concrete, reproducible source
contradiction is found** in the repository (a specific failing check, a mismatch
between a locked document and the artifact it cites, or a broken data-contract
hash) — general polish, stylistic preference, or a desire to "strengthen" a claim
is not such a contradiction and does not authorize reopening any prior gate.

Phase 5.2 (manuscript drafting) is **not yet chartered**. This document is the
complete, standalone reference for that phase when it begins.
