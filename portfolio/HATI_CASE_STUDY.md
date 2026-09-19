# HATI-Madrid

**Uncertainty-aware geospatial screening for heat-adaptive tourism decision support.**

## The problem

Extreme-heat days are becoming an operational constraint on urban tourism, but most
decision-support tools skip straight to ranking or routing without first asking which
options are admissible under heat, access and opening-hours constraints. HATI-Madrid
asks a narrower, upstream question: on one documented extreme-heat day in central
Madrid, which tourism assets remain defensible candidates at a given time, and how
sensitive is that answer to the thermal method used to define "hot"?

## My contribution

I designed and implemented the full pilot: a constraint-first, first-failing-gate
screening architecture (open? → reachable? → thermally feasible? → evidence
sufficient? → meaningful improvement?) that keeps thermal state, decision confidence
and evidence confidence as separate, auditable fields rather than one composite score.
I built both thermal-method operationalisations compared in the pilot — an open-data
operational proxy and a physically based SOLWEIG → Tmrt → UTCI configuration — ran the
eight pre-registered decision scenarios, and authored the uncertainty audit that
classifies each decision as ROBUST / BOUNDARY / UNSTABLE under tested perturbations. I
later extended the same evidence-first architecture to a bounded pedestrian-route
comparison, including its own phase-gated experiment design (feasibility, evidence
freeze, first thermal experiment, robustness test) and the reproducibility tooling —
figure-assertion checks against locked tables, a pinned two-environment pipeline — that
lets the analysis be re-run and verified. Route-finding and thermal modelling libraries
(SOLWEIG/UMEP, `pvlib`) were used as investigated third-party tools, not built from
scratch.

## Methods and evidence

<p align="center">
  <img src="../outputs/publication/figures/FIG01_STUDY_DESIGN_v0.1.png" width="720" alt="Study area map of the Prado–Retiro–Atocha pilot in central Madrid with 27 curated tourism assets, alongside a diagram of the constraint-first screening pipeline feeding from two alternative thermal methods">
</p>

*Study area and screening architecture from the original locked pilot: the Madrid pilot
area with its 27 curated assets, and the constraint-first pipeline in which two thermal
methods feed one ordered gate chain. Reused unmodified from the published figure set;
does not depict the later pedestrian-route extension or its ABSTAIN result.*

- **Study area & assets:** a ~3.5 km² Prado–Retiro–Atocha pilot, 27 curated
  OpenStreetMap tourism assets, one AEMET-designated extreme-heat day (21 Aug 2023).
- **Thermal methods:** an AEMET hazard-band + OSM tree-count operational proxy versus
  SOLWEIG-modelled mean radiant temperature (Tmrt) and derived UTCI from IGN/CNIG LiDAR
  geometry and meteorological forcing.
- **Decision logic:** ordered hard-constraint screening with a single first-failing-gate
  exclusion reason per candidate, and an explicit `NO_DEFENSIBLE_ALTERNATIVE` state when
  nothing survives.
- **Uncertainty controls:** decisions were stress-tested against solar-forcing
  realizations and targeted canopy-geometry perturbations, classified by stability under
  those tested dimensions only.
- **Reproducibility:** a pinned two-environment pipeline, figure scripts that assert
  headline numbers against locked tables before saving, and a versioned audit trail of
  phase gates, decision records and negative controls.

## What the research found

**Original locked pilot (`RELEASE_LOCKED`).** Switching thermal method reclassified
14/42 (33.3%) of outdoor observations, and constraint-first screening changed the
candidate set in 7/8 scenarios versus a proximity-only baseline, including one
explicit no-survivor state. This pilot is archived under an immutable DOI; its locked
numbers, tables and figures are not revisited here.

**Pedestrian-heat extension (`RESEARCH_FROZEN_AFTER_GATE_3B`).** A separate, later
research thread applied the same evidence-first discipline to a bounded pedestrian
route comparison (Atocha → Puerta de Alcalá). It progressed through four gates —
feasibility, evidence freeze, a first thermal experiment, and a robustness test — and
is not part of the original DOI-bound publication.

**Final Gate 3B verdict: ABSTAIN / NO ROBUST DIFFERENCE.** The modeled thermal
difference between the two candidate routes reversed sign under at least one justified
perturbation (canopy-source vintage, side-of-street mapping) at both tested departure
times, and the perturbation ensemble spanned zero. In plain terms: the evidence could
not support declaring either route robustly cooler than the other — not because the
routes are thermally identical, but because the available data was not strong enough to
resolve which one is better under the uncertainty actually tested.

## Why this matters

The value demonstrated here is not a routing recommendation — it is a workflow that
refuses to manufacture one when the evidence does not support it. Constraint-first
screening that reports "insufficient evidence" as a valid, final outcome — rather than
re-running the analysis until a preferred answer appears — is the discipline
geospatial decision-support work for climate adaptation and tourism planning needs:
transparent gates, explicit exclusion reasons, and abstention treated as a legitimate
result, not a failure to iterate away.

## Evidence and links

- [Repository](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid)
- [PROJECT_STATUS.md](../PROJECT_STATUS.md) — canonical status record for both layers
- [Gate 3B decision](../docs/research/pedestrian-heat/gate3b/GATE3B_DECISION.md) — final ABSTAIN verdict and basis
- [Gate 3A decision](../docs/research/pedestrian-heat/gate3a/GATE3A_DECISION.md) — first thermal experiment
- Published preprint: [ResearchGate](https://www.researchgate.net/publication/414226835_Thermal_representation_as_a_decision_variable_in_heat-adaptive_tourism_opportunity_screening_evidence_from_a_Madrid_pilot) · archived on [Zenodo](https://doi.org/10.5281/zenodo.22707470) (DOI 10.5281/zenodo.22707470)

## Status

- Original published pilot: **`RELEASE_LOCKED`**
- Pedestrian-heat research extension: **`RESEARCH_FROZEN_AFTER_GATE_3B`**

No additional research phase is authorised by this portfolio task.
