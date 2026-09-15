# GATE2_DECISION — GO_TO_FIRST_THERMAL_EXPERIMENT / MODIFY / NO_GO

**Version 1.0 · 2026-09-15.**

## Verdict

# GO_TO_FIRST_THERMAL_EXPERIMENT

Proceed to the first thermal experiment **as a Path-B robustness / evidence-
sufficiency / abstention study** — not as a routing, accuracy, comfort, behaviour, or
health study. The Gate-1 claim ceiling and all Gate-0/Gate-1 frozen decisions remain
in force and are not reopened. ABSTAIN remains a first-class outcome.

> This verdict authorises **only** the pre-registered experiment frozen in
> `GATE2_FREEZE_MANIFEST.json` on the two hashed routes, the frozen study day/hours,
> the frozen metrics, and the frozen perturbations/controls. It does **not** authorise
> a recommender, a dashboard, a city-wide map, future-climate scenarios, a physiological
> "dose", any accuracy/comfort/behaviour/health claim, or reuse of any locked HATI
> thermal result.

## Evaluation against the GO_TO_FIRST_THERMAL_EXPERIMENT conditions (all required)

| # | Condition | Status | Evidence |
|---|---|---|---|
| 1 | Two continuously auditable frozen pedestrian routes | **MET** | Route A (2657.8 m) and Route B (2365.7 m) frozen as EPSG:25830 GeoJSON, hashed; segment audit has **0 REJECT, 0 UNRESOLVED**; 0 park-gate dependence. `GATE2_ROUTE_AUDIT.csv`. |
| 2 | Study day + target hours frozen independently of thermal outcomes | **MET** | 2023-08-24; 14:00 & 17:00 Europe/Madrid; chosen on R1–R7 data-quality rule before any A-vs-B thermal difference could exist. |
| 3 | Complete model forcing at those hours | **MET** | Barajas 08221 hourly complete & valid at 14:00 (37.0 °C) and 17:00 (40.0 °C); clear sky (coco=1). |
| 4 | Verified independent urban meteorological check | **MET** | Escuelas Aguirre Ta/RH downloaded and verified at **file level** — all target-hour values present, flagged "V", tracking Barajas within ~0–2 °C. Independent of the forcing series. |
| 5 | Defensible terrain / surface / building classification | **MET** | MDT 2019 + MDS 2023 (obtainable, services live) → normalized surface height; **Catastro INSPIRE footprints audited live** to classify nSH into buildings (height from nSH, not Catastro floors). L17 building side resolved. |
| 6 | Defensible vegetation/canopy strategy **or** bounded uncertainty compatible with Path B | **MET** | Strategy stated as known/inferred/unresolved; tree inventory covers OD1 (1322 park + 1528 street trees); canopy = nSH behind a justified mask; residual bounded by E-P2 with an explicit ABSTAIN hook (NC7). |
| 7 | Outcome metrics frozen | **MET** | `GATE2_METRIC_SPEC.md` — M1–M4 decision-bearing, M5 descriptor-only; ∫UTCI dt removed; authoritative UTCI boundaries. |
| 8 | Perturbation values frozen or explicitly demoted | **MET** | `GATE2_PERTURBATION_SPEC.md` — E-P1/E-P2/E-P4/E-P5/E-P6 frozen with justified values; E-P3 wind demoted. |
| 9 | Negative controls operationalised | **MET** | NC1–NC7 pre-declared with exact ABSTAIN evidence conditions (Evidence Report §2I), before any thermal output. |
| 10 | Hashes / provenance recorded | **MET** | `gate2_hash_manifest.json` (14 artifacts) + `route_freeze_hashes.json` + per-source provenance JSONs. |
| 11 | No unresolved issue that makes the route ordering uninterpretable before modeling | **MET** | Seven residual limitations are each bounded by a frozen perturbation or wired to an explicit ABSTAIN condition; none pre-determines or obscures the A-vs-B ordering. |

**All eleven conditions are met.**

## Why GO and not MODIFY

MODIFY would apply if only a *smaller* defensible Path-B experiment remained after
narrowing. No such narrowing is needed: both Gate-1 blockers are resolved — the routes
are now acquired, audited, continuous and hashed (B1), and the study day is frozen on
R1–R7 with a verified urban check (B2); the previously-OPEN geometry classification
(B2b/L17 building side) is resolved via an audited Catastro footprint source, with the
canopy residual bounded and ABSTAIN-wired; metrics and perturbations are frozen (B2c).
The experiment can run at full frozen scope.

## Why GO and not NO_GO

NO_GO would apply if the comparison could not be made auditable without inventing
connectivity, geometry, forcing, or unsupported parameterisation. None of that was
needed:
- The routes were **not** repaired opportunistically — where the shortest path would
  have invented a park-gate dependence, the route was held on the street per the frozen
  Alt-B identity (documented in 2B), and it remains continuous with 0 UNRESOLVED
  segments.
- Forcing and the independent check are real, verified observations at the exact hours.
- Geometry classification uses an **audited** footprint source; canopy uncertainty is
  **bounded and declared**, not classified away.
- No canyon-wind multiplier and no ∫UTCI "dose" were invented; unsupported dimensions
  were demoted, not fabricated.

A NO_GO is preferable to manufacturing evidence — but no evidence had to be
manufactured here, so NO_GO is not warranted.

## Constraints that ride along with GO (binding on the first thermal experiment)

1. **Path B only** — robustness / sensitivity / decision-reversal / evidence
   sufficiency of *modeled* comparative exposure; ABSTAIN is a valid, first-class result.
2. **Frozen inputs are immutable** — route geometry, study day/hours, metrics, category
   boundaries, and perturbation values change only via an `AMENDMENT_00x.md`.
3. **ABSTAIN hooks are live** — NC1–NC7 and the decision rule must be honoured; a
   canopy-state or side-of-street reversal, a boundary straddle, a forcing/pixel gap, or
   a decision-critical unresolved spatial wind each forces ABSTAIN.
4. **Prohibitions restated** — 21 Aug 2023 is not independent validation of the locked
   run and 24 Aug 2023 reuses no locked thermal/asset result; no Sentinel-2/optical as
   thermal/LST; no ERA5-Land/same-forcing/another-run as independent pedestrian-UTCI
   validation; no invented material-UTCI-difference threshold.

## Amendment note

No Gate-0 or Gate-1 amendment is required. Gate 2 resolved the OPEN preconditions inside
the existing Gate-0 research object and Gate-1 claim ceiling and changed no frozen
decision. Should the first thermal experiment reveal that OD1 cannot yield an
interpretable ordering even under this frozen design, the correct outcome is the
pre-declared **ABSTAIN**, not a silent redesign.

---

*Gate 2 ends here — before the first thermal output. No SOLWEIG/URock/UTCI/Tmrt was
run; no thermal map or route-thermal difference was produced; no large raster was
committed.*
