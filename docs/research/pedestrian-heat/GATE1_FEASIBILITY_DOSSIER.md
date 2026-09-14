# GATE1_FEASIBILITY_DOSSIER — Pedestrian Heat-Exposure Decision-Reliability Extension

**Gate 1 — bounded feasibility study. Version 0.1 · 2026-09-14.**
**Verdict (full justification in `GATE1_DECISION.md`): MODIFY.**

> **Scope guard.** This document does *not* run SOLWEIG/URock, does *not* compute UTCI,
> does *not* build a recommender/dashboard, does *not* optimise routes on thermal results,
> and does *not* download large raster/LiDAR/remote-sensing datasets. It answers exactly
> one question: *can we assemble ONE pre-specified pedestrian route comparison in the
> Atocha–Prado–Retiro corridor with sufficiently auditable open data to justify a later
> robustness / abstention experiment?*

---

## 0. Repository forensics (what HATI has, and has NOT, established)

The extension inherits a mature, `RELEASE_LOCKED`, publicly-archived project. The single
most important forensic discipline here is separating *implemented / modeled* from
*independently validated*. The repository is unusually honest about this itself; the table
below is a compression of `PROJECT_STATUS.md`, `docs/PHASE2_VALIDATION_REPORT.md`,
`docs/PHASE1_2_TEMPORAL_ALIGNMENT.md`, `docs/PHASE1_1_SENSITIVITY_REPORT.md` and
`docs/RESEARCH_GAP.md`.

| Claim class | What is actually true in-repo |
|---|---|
| **Implemented / reproducible** | Operational-proxy classification (AEMET hazard bands + OSM tree-count exposure); constraint-first screening logic; the 33.3% proxy-vs-physical reclassification count; 8 decision scenarios; read-only replay app. |
| **Modeled (only)** | SOLWEIG Tmrt and the UTCI derived from it — for 21 Aug 2023, 3 timestamps (12/15/18). |
| **Independently validated** | **Nothing thermal.** No field Tmrt/UTCI measurement (globe thermometer, 6-directional radiometer, or any in-situ reading) exists anywhere in the project. AEMET validates *forcing inputs* (Ta/RH/wind/pressure) only — it cannot validate the radiant field. |
| **Independent check available** | Weak. Retiro official *daily-max* (+0.5 °C) and *monthly-mean* (+0.11 °C) only. **No hourly in-city observation is obtainable** (Phase 1.1 Audit 1). |
| **Geometry vintage** | PNOA-LiDAR **1st coverage ~2008–2015**. Canopy geometry is repeatedly flagged as the single largest, direction-changing uncertainty. No geolocated 2023 tree inventory exists. |
| **Solar forcing** | Modeled (pvlib Ineichen clear-sky), not measured. |
| **Published** | Preprint on Zenodo (DOI `10.5281/zenodo.22707470`) + ResearchGate; non-peer-reviewed; no journal selected. |
| **Proposed / not built** | A pedestrian *routable network*. Every OSM pull to date fetched POIs/buildings/trees/water/transit — **never the walkable path graph**. |

**Forensic conclusion.** Evidence does not exist merely because a file or feature exists.
The locked pilot proves a *screening decision architecture* and demonstrates that
*thermal-method choice changes the screening outcome* — it proves **nothing** about
pedestrian-level UTCI accuracy, and it built no route network. The extension therefore
starts from: a validated-input / unvalidated-output thermal model, stale-but-auditable
geometry, and a **missing** route graph.

---

## GATE 1A — Candidate decision cases

### Selection criteria (fixed BEFORE selecting; no thermal output inspected)

Each criterion is scored 1 (weak) – 3 (strong). Weights are equal and stated; no weight was
tuned to favour an outcome.

| # | Criterion | Rationale |
|---|---|---|
| C1 | Tourism relevance | A trip a real visitor would plausibly make on foot. |
| C2 | ≥2 genuinely plausible, non-artificial alternatives | Alternatives must be distinct corridors, not offset variants of one geometry. |
| C3 | Geometric / shade contrast | Enough structural difference that a future thermal comparison *could* be informative (informativeness, not a known answer). |
| C4 | Network auditability | Can both routes be traced on a real, checkable walkable network and legally walked? |
| C5 | Manageable extent / duration | Walkable pilot scale (roughly 10–30 min), inside the corridor box. |
| C6 | Independence from HATI's locked outputs | Endpoints may reuse asset *coordinates*; the case must not reuse any locked thermal/asset-ranking *result* as evidence. |

### Candidate O-D pairs (endpoints from `data/processed/pilot_assets.csv`)

| ID | Origin → Destination | Alt A | Alt B | C1 | C2 | C3 | C4 | C5 | C6 | Σ |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **OD1** | **Atocha (A09) → Puerta de Alcalá (A14)** | **Paseo del Prado monumental axis (open, low canopy)** | **Calle Alfonso XII / Retiro–Botánico western edge (tree-lined)** | 3 | 3 | 3 | 2 | 2 | 3 | **16** |
| OD2 | Reina Sofía (A02) → Retiro Estanque (A20/A26) | Prado axis then enter at Alcalá | Calle Alfonso XII park-edge street | 3 | 3 | 3 | 2 | 2 | 3 | 16 |
| OD3 | Prado (A01) → Palacio de Cristal (A22) | Retiro interior shaded paths | Perimeter streets | 2 | 2 | 2 | 2 | 2 | 3 | 13 |
| OD4 | Thyssen (A03) → Puerta de Alcalá (A14) | Paseo del Prado (open) | Recoletos sidewalk (open) | 2 | 1 | 1 | 3 | 3 | 3 | 13 |
| OD5 | Atocha (A09) → Reina Sofía (A02) | Direct Ronda de Atocha | Glorieta detour | 2 | 1 | 1 | 3 | 3 | 3 | 13 |

Notes: OD1 and OD2 tie numerically; OD1 is selected (see 1A decision) because its endpoints
are the corridor's two canonical termini (a real arrival-to-icon walk), its two alternatives
are maximally distinct (a wide sun-exposed civic axis vs. a tree-lined park-edge street),
and Puerta de Alcalá is an *outdoor* endpoint (so the comparison is not dominated by an
indoor-refuge endpoint). **OD4 and OD5 are deliberately retained as negative-control seeds**
(§1F): their low geometric contrast is a feature — a sound method should *not* confidently
separate them.

### 1A decision

**Primary Gate 1 case: OD1 — Atocha (A09, 40.404557, −3.688683) → Puerta de Alcalá
(A14, 40.419987, −3.688724).**

- **Alt A (Prado axis):** north up the Paseo del Prado / Paseo de Recoletos civic axis past
  Neptuno and Cibeles to Alcalá. Wide, monumental, hard-paved, intermittent plane-tree
  alignment; high sky-view, low continuous canopy.
- **Alt B (park-edge):** north-east along the Real Jardín Botánico / Parque del Retiro
  western edge and Calle Alfonso XII, rejoining Alcalá from the park side. Tree-lined
  street plus park-margin canopy; lower sky-view in stretches.

Both are ~1.5–1.9 km, ~20–25 min walk, fully inside the corridor box, and (subject to the
network audit that Gate 1 flags as still-required) legally walkable.

### Rejected candidates + reasons

- **OD3** rejected: contrast is *inside-park vs street*, strongly dependent on which park
  gate is used and on gate opening hours (adds an avoidable access confound at Gate 1).
- **OD4, OD5** rejected *as primary* (kept as negative controls): both alternatives are
  open, low-canopy sidewalks — little geometric contrast, so a confident thermal separation
  would be a red flag, not a result.
- **OD2** rejected *as primary* only on the tie-break above (indoor-ish museum origin,
  Estanque endpoint slightly less canonical than Alcalá); it is the designated **backup**.

---

## GATE 1B — Historical hot-day selection protocol

**21 Aug 2023 is NOT auto-selected.** Per protocol it may only be retained later as a
*legacy stress-test*, never as independent validation of this extension.

### Selection rules (fixed before any day is chosen; reproducible)

A candidate day is admissible only if it satisfies **all** of R1–R5; among admissible days,
prefer higher R6.

| Rule | Requirement | Why |
|---|---|---|
| R1 | Genuine high-heat event: AEMET official daily-max ≥ the AEMET *aviso* threshold for Madrid (heat warning in effect), independently attributable from AEMET *avance climatológico* / METEOALERTA, not from this project's own model. | The comparison is only interesting under real heat stress. |
| R2 | Complete hourly forcing coverage (Ta/RH/wind/pressure) for the full daylight envelope at the forcing station, no gaps at target hours. | SOLWEIG needs uninterrupted hourly forcing. |
| R3 | Confirmed clear-sky (or documented sky state) at target hours, so the modeled-GHI clear-sky assumption is defensible (station `coco`/weather code). | The only available radiation is a clear-sky estimate; it is valid only when the sky was actually clear. |
| R4 | Temporal compatibility with available urban geometry: the day must post-date nothing that invalidates the 2008–2015 geometry more than the vintage gap already does (i.e. no major known construction/canopy event between geometry vintage and the day that is undocumented). | Keeps the geometry-vintage gap bounded and stated. |
| R5 | An **independent** meteorological cross-check exists for that day (≥ Retiro official daily-max; ERA5-Land as context). | Every study day needs at least one non-forcing check. |
| R6 (preference, not gate) | Availability of the diurnal variables a departure-time comparison would later need. | Supports the optional time-shift analysis. |

**Explicit anti-cherry-pick rule:** the day is chosen on R1–R6 (heat + data quality) **only**.
It is prohibited to choose a day because it maximises the Alt A – Alt B route difference. The
route difference must never be inspected before the day is fixed.

### Distinction (these are NOT automatically one dataset)

- **Weather-event selection** — attribution of "this was a real heat event" (AEMET official
  daily-max / warning record).
- **Model forcing** — the hourly series driving SOLWEIG (Barajas 08221).
- **Independent meteorological checking** — a *different* record used to bound forcing
  representativeness (Retiro official summaries; ERA5-Land context). It must not be the same
  series as the forcing.

### Candidate dates + sources (selection stops here — no large download)

From material already in-repo plus small metadata:

| Candidate day | Evidence in-repo | R1 heat | R2/R3 hourly+clear | Notes |
|---|---|---|---|---|
| 2023-08-21 | Barajas hourly + AEMET avance 202308 PDF | Yes (40.5 °C) | Yes (coco=1 at 12/15/18) | **Legacy stress-test only** — not independent validation. |
| 2021-08-14 | `data/raw/extreme_aug2021_barajas_raw.csv`; AEMET avance 202108 PDF | Yes (42.7 °C official) | To verify hourly/clear | Closer to geometry vintage; strong EXTREME-branch day (already used as a stress test in Audit 2). |
| A fresh 2022–2025 AEMET heat-warning day | AEMET OpenData API (small query) | To select | To verify | Allowed: small metadata/API query only. |

**Provisional recommendation (to be frozen at Gate 2 start, not now):** shortlist
**2021-08-14** as the primary candidate (nearest to geometry vintage, officially hotter,
already has a raw Barajas extract) with a fresh AEMET-warning day as an alternative, and
retain 2023-08-21 strictly as the legacy stress-test. Final selection requires only small
AEMET metadata queries to confirm R2/R3 — no bulk download.

---

## GATE 1C — Input feasibility ledger

The full structured ledger is `GATE1_INPUT_LEDGER.csv` (14 essential inputs, each with
source/publisher/product/URL/vintage/resolution/CRS/licence/role/status/independence/
direction-risk/limitations/Gate-2 treatment). Status summary:

| Status | Inputs |
|---|---|
| **ACCEPT** | L07 timestamps/timezone; L08 vintage register; L09 licensing; L14 O-D endpoints. |
| **ACCEPT WITH UNCERTAINTY** | L01 Barajas forcing; L02 independent met check; L03 buildings/terrain; L04 canopy; L10 departure-time support; L11 solar GHI; L13 wind. |
| **MISSING** | **L05 pedestrian network**; **L06 route access/crossing plausibility**; L12 land cover (package default — non-blocking). |
| **REJECT** | none. |

**Two MISSING inputs are load-bearing for a *route* comparison** and are the headline Gate 1
finding: L05 (the routable pedestrian graph) and L06 (crossing/access plausibility). Neither
was ever assembled by HATI. Both are **acquirable within Gate-1 rules** (a bounded Overpass
query for the two fixed routes + a manual walkability audit — small, not a bulk download),
but until acquired and audited the "auditable routes" precondition for GO is **not met**.

Specific attention points (per Gate 1C):
- **Barajas vs central Madrid:** forcing is an airport ~13 km NE; independent in-city check
  is daily/monthly only. Applied identically to both routes, so it is largely *differenced
  out* of a within-pair comparison — but this is an assumption to test, not to assert.
- **Radiation & wind:** GHI is a clear-sky *estimate*; wind is a single station value, not
  spatially resolved. Both are perturbation dimensions, not validated fields.
- **Historical canopy vintage:** 2008–2015; the dominant direction-changing risk.
- **Crown geometry vs tree points:** the canopy is a *height raster*, not crown polygons or
  a per-tree inventory — shadow extent is approximated.
- **Building geometry date & OSM incompleteness / side-of-street ambiguity:** unmodelled;
  the network audit (L06) must resolve which sidewalk each route uses.
- **Crossings / pedestrian restrictions & historical opening hours:** required if a
  time-shift comparison is later attempted; 2026 hours applied to a historical day is a
  stated mismatch.
- **Sentinel-2:** never used as a thermal sensor or LST source (guardrail restated).

Do not confuse source resolution (2.5 m geometry) with pedestrian-scale *accuracy*: the
canopy raster is high-resolution **and** ~decade-stale simultaneously.

---

## GATE 1D — Claim ceiling

**Path A (independent pedestrian-level thermal measurements exist): NOT AVAILABLE.**
No field Tmrt/UTCI exists in-repo, and no credible open route to obtain 2023/2021 (or even
current) pedestrian-level radiometric measurements for this corridor was identified. A
future field campaign is conceivable but is out of scope and unfunded here.

**Path B (no such measurements): FORCED.**

Therefore the **maximum honest claim ceiling** for this extension is:

> **Robustness, sensitivity, decision-reversal behaviour, and evidence sufficiency of
> *modeled* comparative pedestrian thermal exposure — including a first-class ABSTAIN /
> NO-EVIDENCE outcome — for one auditable tourism O-D case.**

Explicitly **excluded** from the ceiling (restated from protocol §5): observed tourist
exposure; validated pedestrian UTCI accuracy; subjective comfort; behaviour; physiological
stress; health/adaptation benefit. None of {another model run, ERA5-Land, the same forcing,
the locked HATI output} counts as independent validation of pedestrian UTCI.

This lowered ceiling is **not** a project failure: the Gate-0 research object *is* decision
reliability + evidence sufficiency + abstention, which lives entirely inside Path B.

---

## GATE 1E — Minimal perturbation set (designed, NOT executed)

Full frozen spec in `GATE1_EXPERIMENT_SPEC.md`. Summary of the smallest defensible set —
each dimension included **only** because it can change the *decision* and each range has a
data/literature justification (no arbitrary parameter sweeps):

| Dim | Uncertainty source | Justified alternatives | Why it can flip the decision |
|---|---|---|---|
| E-P1 | Meteorological forcing representativeness | Barajas as-is vs a Retiro-anchored daily-max offset applied to the diurnal shape | Airport-vs-centre bias; tests whether the pair survives a plausible forcing shift. |
| E-P2 | **Canopy / vegetation geometry** | 2008–2015 nDSM as-is vs current Madrid arbolado per-tree points vs Copernicus TCD 2018 as bounding canopy states | The dominant risk: a decade of canopy change can add/remove the shade separating Alt A from Alt B. |
| E-P3 | Wind treatment | Uniform station wind vs a simple open-vs-canyon adjustment (no CFD) | Plaza-vs-canyon cooling could differentially favour one route. |
| E-P4 | Building/shadow representation | 1st-coverage building nDSM vs (only if E-P2/E-P3 prove decision-sensitive) 2nd-coverage sheet pull | Building edits alter cast shadow on one route. |
| E-P5 | Pedestrian network representation | Two independently-audited route traces (e.g. sidewalk side A vs side B where ambiguous) | Side-of-street choice changes exposure along the same corridor. |
| E-P6 | Walking speed / pauses | 1.1 vs 1.4 m/s; optional queue/pause at endpoints | Changes cumulative exposure integral and could reorder near-ties. |

**Decision framework — no invented °C threshold.** The literature check (below and in
`GATE1_LITERATURE_LOG.md`) found **no** defensible universal "material UTCI difference"
threshold for *this* comparison type, but a **mature rank-reversal / decision-stability
formalism** (pairwise-comparison robustness under uncertainty bounds). The comparison is
therefore framed on decision stability, not on a magic number:

- **ROBUST COMPARISON** — the *direction* of the paired Alt A − Alt B difference is
  preserved across all justified perturbations (E-P1…E-P6) and the difference sits clear of
  any UTCI category boundary.
- **NO ROBUST DIFFERENCE** — the routes are statistically/materially indistinguishable, or
  the sign is stable but the magnitude is within the modeled uncertainty interval.
- **ABSTAIN / NO EVIDENCE** — the decision *reverses* under at least one justified
  perturbation, OR an essential input is MISSING/near a category boundary, OR the
  uncertainty interval spans the decision.

Statistical significance is explicitly **not** conflated with practical/physiological
relevance (no physiological claim is made at all).

---

## GATE 1F — Negative controls (pre-specified)

A method that confidently resolves any of these has **failed** its evidence-sufficiency
logic and must ABSTAIN:

1. **NC1 — effectively identical routes:** OD4 / OD5 seeds (two open low-canopy sidewalks).
2. **NC2 — missing network link:** a route deliberately traced across an unmapped/again-to-
   verify connection (tests L05 gap handling).
3. **NC3 — uncertain pedestrian access:** a route using a park gate whose opening hours /
   legality on the study day is unresolved (tests L06).
4. **NC4 — unresolved canopy vintage:** a route whose Alt A/Alt B separation depends entirely
   on canopy pixels in the 2008–2015 nDSM that current arbolado points contradict.
5. **NC5 — missing meteorological variable:** a target hour with a forcing gap or non-clear
   sky (violates R2/R3) — the method must refuse, not interpolate silently.
6. **NC6 — category-boundary case:** a pair whose modeled UTCI difference straddles a UTCI
   stress-category boundary.
7. **NC7 — justified-assumption reversal:** any pair whose ordering flips between E-P2 canopy
   states — the canonical ABSTAIN trigger.

---

## GATE 1G — GO / MODIFY / NO-GO (rules + result)

Decision rules were fixed before scoring; the row-by-row evaluation is in
`GATE1_DECISION.md`. In one line: **GO** requires (among other things) auditable routes AND
usable forcing AND ≥1 independent check AND a legitimate ABSTAIN outcome AND a non-trivial
surviving question. Here forcing, ABSTAIN, and the surviving question hold; **auditable
routes are not yet in hand (L05/L06 MISSING)** and **pedestrian-level validation is
structurally unavailable (Path B forced)**. That combination is the textbook **MODIFY**
trigger, not GO — and it is **not** NO-GO, because a genuine, non-saturated
evidence-sufficiency / abstention question survives the literature review and at least one
(weak) independent check exists.

**VERDICT: MODIFY** — proceed to Gate 2 with (a) the claim ceiling reduced to
robustness/sensitivity/abstention (Path B), and (b) two hard preconditions that must be
satisfied *before* any thermal run: acquire + manually audit the L05 pedestrian network and
L06 access/crossings for the two OD1 routes, and freeze the study day on R1–R6.

---

## Principal uncertainties (ranked)

1. **Canopy vintage (2008–2015)** — dominant, direction-changing; the whole ABSTAIN logic
   exists largely to handle it.
2. **No pedestrian-level validation (Path B forced)** — caps the claim permanently.
3. **Missing route network + access audit (L05/L06)** — a precondition gap, resolvable but
   currently open.
4. **Forcing representativeness (Barajas airport; no hourly in-city check)** — mitigated by
   identical-forcing differencing, but assumed not proven.
5. **Modeled GHI + unresolved wind field** — perturbation dimensions, not validated fields.

## Unresolved blockers carried to Gate 2

- **B1:** L05 pedestrian network and L06 crossing/access plausibility are MISSING and must be
  acquired + manually audited before any thermal computation.
- **B2:** Study day not yet frozen (R1–R6 shortlist only; small AEMET queries pending).
- **B3:** A closely-adjacent 2026 paper ("How fine is fine enough? … heat-aware pedestrian
  routing") narrows the novelty envelope; Gate 2 framing must assert the abstention/
  evidence-sufficiency distinction sharply (see `GATE1_LITERATURE_LOG.md`).

---

*This dossier stops before thermal modeling by design. No SOLWEIG/URock/UTCI was run; no
large dataset was downloaded; no synthetic validation evidence was created.*
