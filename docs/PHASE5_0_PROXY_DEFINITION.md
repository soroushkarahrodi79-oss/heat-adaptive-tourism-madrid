# PHASE5_0_PROXY_DEFINITION.md — HATI-Madrid Phase 5.0

Version 1.0 · 2026-08-18. Mandatory pre-manuscript definition of the exact
"proxy" that is compared against the physically based thermal model in
`outputs/tables/proxy_vs_physical_comparison.csv`. Written so the manuscript
can never use vague language such as "shade/LST-type proxy" — because that is
**not** what was implemented. Traced from source, not from memory:
`src/extract_asset_thermal_exposure.py`, `src/build_classifications.py`,
`src/thresholds.py`, `data/processed/pilot_classifications.csv`,
`docs/PHASE1_METHOD.md`, `docs/PHASE1_2_SHADE_EVIDENCE_GATE.md`.

---

## 1. What the "proxy" is, exactly

The proxy baseline is the **Phase 1 constraint-first tourism-feasibility
classification (frozen proxy family P0)**. In the comparison table it is the
field `feasibility_phase1_proxy`, read verbatim from the `feasibility_state`
column of `data/processed/pilot_classifications.csv`. It is **not** a single
environmental variable. It is a two-input decision:

```
Phase 1 feasibility_state  =  feasibility_decision( meteorological_hazard_band ,
                                                    exposure_band )
```

Both inputs are open-data, non-physical, and computed as documented below. The
physically based comparator replaces this whole construct with a single
SOLWEIG-modelled UTCI value passed through UTCI-category feasibility thresholds
(§5).

## 2. Exact variables

**Input A — meteorological hazard band (ambient air temperature).**
- Variable: real hourly 2 m air temperature, Madrid/Barajas AEMET/WMO station
  08221 (LEMD), 2023-08-21, at 12:00 / 15:00 / 18:00 local (34.2 / 38.8 /
  40.5 °C).
- Classification: AEMET official Meteoalerta maximum-temperature civil-
  protection thresholds for zone 722802 "Metropolitana y Henares": amarillo
  36 °C, naranja 39 °C, rojo 42 °C → bands LOW / ELEVATED / SEVERE / EXTREME.
- The three study hours fall in LOW (12:00), ELEVATED (15:00), SEVERE (18:00).

**Input B — exposure band (OSM tree-count shade-availability proxy, family P0).**
- Variable: count of real OpenStreetMap `natural=tree` points (n = 1,353 in the
  study area) within the asset's real extent — a **50 m radius buffer** for
  monument/building-type assets, or the asset's **own OSM polygon buffered
  +15 m** for the 8 park/garden assets.
- Classification: LOW / MODERATE / HIGH exposure by **tercile of the pilot's own
  14-outdoor-asset tree-count distribution** (q1 = 0.33, q2 = 3.67 trees).
  HIGH = fewest trees = "poor shade"; LOW = most trees = "well shaded".

**Combination rule — `feasibility_decision()` (`src/thresholds.py`,
`src/build_classifications.py`):** first-matching-rule decision tree, no
weighted score. For outdoor assets: EXTREME hazard → NOT RECOMMENDED; SEVERE →
NOT RECOMMENDED if exposure HIGH else FEASIBLE WITH CONDITIONS; ELEVATED →
always FEASIBLE WITH CONDITIONS; LOW → FEASIBLE, or FEASIBLE WITH CONDITIONS if
exposure HIGH. (A third input, an adaptation-resource indicator, was **demoted
in Phase 1.1** to reported context and is **not decision-relevant**; it does not
enter the proxy feasibility state.)

## 3. Spatial support

- Asset representative point from OSM (a visitor-standpoint point, not a building
  centroid — see `docs/PHASE2_VALIDATION_REPORT.md` §2).
- Tree-count support: 50 m circular buffer (point assets) or OSM polygon +15 m
  (park/garden assets).
- Air-temperature support: a single station reading applied uniformly to every
  asset at each hour (no spatial field). Barajas is ~9 km from the study area;
  every row carries a `station_representativeness_note` (+0.5 °C daily-max,
  +0.11 °C monthly-mean vs Retiro official figures).
- Comparator (physical) support: 10 m buffer **mean** of the 2.5 m SOLWEIG UTCI
  raster (pre-registered primary statistic, `src/phase2_prereg.py`).

## 4. Thresholds / categories

| Element | Cutpoints | Origin |
|---|---|---|
| Hazard band | 36 / 39 / 42 °C air temp | AEMET official civil-protection warning scale |
| Exposure band | tree-count terciles q1=0.33, q2=3.67 | **empirical** split of this pilot's own 14 outdoor assets — not a literature constant |
| Feasibility | 3 states via decision tree | project rule table, `src/thresholds.py` |
| Physical feasibility | UTCI ≥46 → NOT RECOMMENDED; ≥32 → FEASIBLE WITH CONDITIONS; else FEASIBLE | UTCI category boundaries (Bröde et al. 2012), pre-registered mapping (`docs/PHASE2_UTCI_METHOD.md`) |

The exposure terciles are the single most important caveat about the proxy: they
are a **relative, within-sample sensitivity grade**, because no published
"trees per 50 m near a tourism POI" shade-sufficiency threshold exists.

## 5. Was LST used? — NO

**Land Surface Temperature was never used anywhere in the proxy, or anywhere in
the project's decision logic.** The Phase 1 hazard input is **ambient air
temperature** from a ground station, explicitly classified against a
civil-protection warning scale, and explicitly forbidden from being read as a
comfort index (`docs/PHASE1_METHOD.md` §5.1, §7). Any manuscript sentence
implying LST, satellite surface temperature, or a thermal-infrared proxy is
false and must not appear.

## 6. Were tree count / green polygons / canopy involved?

- **Tree count (OSM `natural=tree`): YES** — this is the proxy's exposure input
  (family P0), and the only vegetation signal in the *frozen comparison
  baseline*.
- **Green polygons, municipal tree inventory, Copernicus canopy density: NO, not
  in this comparison baseline.** They exist in the repository as the Phase 1.2
  *alternative* proxy families P1/P2/P3, built specifically to test whether
  better vegetation proxies would converge. They do **not** feed
  `proxy_vs_physical_comparison.csv`. Their role is separate evidence (§8).

## 7. Which proxy version is the final comparison baseline?

**P0 — the frozen Phase 1 OSM-tree-count feasibility classification**, unmodified
since Phase 1 and reused verbatim (`data/processed/pilot_classifications.csv`).
Phases 1.1 and 1.2 deliberately did **not** recompute or improve it. It is the
correct baseline precisely because it is the simplest defensible open-data
constraint architecture — the honest "before physical modelling" state.

## 8. What physical concept the proxy approximates (and how well)

The proxy tries to approximate **pedestrian-level human heat load** using two
cheap surrogates: ambient air temperature (for the meteorological driver) and
local tree presence (for the radiative shading that modifies it). SOLWEIG/UTCI
instead computes the actual quantity — a radiant-load-inclusive thermal index
from real building and canopy geometry and solar path. The comparison shows the
surrogates and the physical index diverge on **14 of 42 outdoor asset×timestamp
rows (33.3%)**, and the divergence is **concentrated in time, not morphology**:

| Timestamp | Reclassification | Physical interpretation |
|---|---:|---|
| 12:00 | **64.3%** (9/14) | air temp is only 34.2 °C ("LOW" civil-protection band), yet modelled UTCI already ≥ 32 °C everywhere outdoors → proxy **underestimates** midday radiant load |
| 15:00 | 0.0% | both collapse to FEASIBLE WITH CONDITIONS at ELEVATED/peak hazard — agreement is partly an artefact of the rule table being least discriminating here |
| 18:00 | 35.7% (5/14) | mixed: tree-count "poor shade" can over- or under-call vs modelled UTCI near the 46 °C cutoff |

Direction overall: **9 rows physical MORE restrictive (proxy underestimated
hazard), 5 rows physical LESS restrictive (proxy overestimated hazard)** — the
proxy errs in *both* directions, which is why the finding is "method choice
materially changes the decision", not "the proxy is biased one way".

## 9. What the proxy explicitly does NOT measure

- It does **not** measure shade, shadow geometry, canopy cover, or sun position.
  Tree *count* is a presence proxy, not a shadow simulation
  (`docs/PHASE1_METHOD.md` §7).
- It does **not** measure radiant load, Tmrt, UTCI, PET, or WBGT.
- It does **not** measure surface temperature (no LST).
- It does **not** resolve intra-urban air-temperature variation (one station
  value per hour, applied uniformly).
- It does **not** encode building massing, street canyon geometry, or
  orientation.
- Its exposure terciles are **relative within this pilot**, not absolute or
  transferable thresholds.

## 10. Mandatory manuscript wording

**Allowed:** "a constraint-first open-data proxy combining an ambient
air-temperature hazard classification (AEMET civil-protection thresholds) with
an OSM tree-count shade-availability index"; "the simple proxy baseline";
"physically based thermal-exposure modelling (SOLWEIG-derived UTCI)".

**Forbidden:** "shade/LST-type proxy"; "LST proxy"; "satellite temperature
proxy"; "canopy model"; "shade model"; any phrasing that implies the proxy
measured shadow, radiant load, or surface temperature, or that the proxy is
"wrong" in an accuracy sense (it is *different*, and neither side is field-
validated — see `docs/PHASE5_0_REVIEWER_ATTACK_MAP.md`).
