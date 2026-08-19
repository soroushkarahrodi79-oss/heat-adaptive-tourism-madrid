# PHASE5_2A_METHODS_AUDIT.md — HATI-Madrid Phase 5.2A

Version 1.0 · 2026-08-18. Audit of the Methods draft
`manuscript/03_METHODS_v0.1.md` against the locked Phase 0–5.1 record. No Phase
0–4.1 output was modified; no new analysis was run. This audit checks the draft
for factual traceability, forbidden wording, Results leakage, and claim-boundary
integrity, and ends with a single gate verdict.

Sources of truth consulted: `docs/PHASE5_0_PROXY_DEFINITION.md`,
`docs/PHASE5_0_PAPER_CHARTER.md`, `docs/PHASE5_0_EVIDENCE_MATRIX.csv`,
`docs/PHASE5_0_MANUSCRIPT_ARCHITECTURE.md`, `docs/PHASE5_1_LITERATURE_MATRIX.csv`,
`docs/PHASE5_1_NOVELTY_AUDIT.md`, `docs/PHASE1_METHOD.md`,
`docs/PHASE1_DATA_PROVENANCE.md`, `docs/DATA_SOURCE_INVENTORY.csv`,
`docs/PHASE2_SOLWEIG_METHOD.md`, `docs/PHASE2_UTCI_METHOD.md`,
`docs/PHASE2_2_METHOD.md`, `docs/PHASE2_2_DECISION_UNCERTAINTY.md`,
`docs/PHASE3_DECISION_ARCHITECTURE.md`, `docs/PHASE3_METHOD.md`,
`docs/PHASE3_SCENARIOS.md`.

---

## 1. Factual consistency with locked repository methods

Every methodological statement in the draft was traced to a source document.
Spot-checks of the load-bearing parameters:

| Draft statement | Source | Status |
|---|---|---|
| Study area ≈ 3.5 km², Prado–Retiro–Atocha rectangle to named landmarks | `PHASE1_METHOD.md` §2 | ✓ exact |
| 27 assets (13 indoor / 14 outdoor) | `PHASE1_METHOD.md` §4; charter §5 | ✓ exact |
| Date 21 Aug 2023, AEMET episode 20–25 Aug 2023 | `PHASE1_METHOD.md` §3 | ✓ exact |
| Hours 12/15/18, air temp 34.2/38.8/40.5 °C | `PHASE1_METHOD.md` §3.1 | ✓ exact |
| Unit = asset×timestamp; 42 outdoor pairs (14×3) | charter §5 | ✓ exact |
| Barajas WMO 08221, ~9 km NE, +0.5 °C vs Retiro | `PHASE1_DATA_PROVENANCE.md` §1 | ✓ exact |
| AEMET thresholds 36/39/42 °C, zone 722802 | proxy def §2; `PHASE1_METHOD.md` §5.1 | ✓ exact |
| Tree count OSM `natural=tree`; 50 m buffer / polygon +15 m; terciles 0.33, 3.67 | proxy def §2–3 | ✓ exact |
| feasibility decision tree (EXTREME/SEVERE/ELEVATED/LOW rules) | proxy def §2; `PHASE1_METHOD.md` §5.4 | ✓ exact |
| SOLWEIG v0.1.0b92, 2.5 m, DEM resampled, defaults | `PHASE2_SOLWEIG_METHOD.md` | ✓ exact |
| GHI estimated via Ineichen–Perez clear-sky, clear-sky code gate | `PHASE2_SOLWEIG_METHOD.md` | ✓ exact |
| UTCI = Bröde et al. 2012; built-in module; 10 m buffer mean | `PHASE2_UTCI_METHOD.md`; proxy def §3 | ✓ exact |
| UTCI feasibility map ≥46 / 32–46 / <32 | `PHASE2_UTCI_METHOD.md` | ✓ exact |
| Envelope = 4 solar realizations + 3 geometry variants (2 assets) | `PHASE2_2_METHOD.md` §5; `PHASE2_2_DECISION_UNCERTAINTY.md` §2 | ✓ exact |
| ROBUST/BOUNDARY/UNSTABLE via per-row sensitivity `s` | `PHASE2_2_DECISION_UNCERTAINTY.md` §3 | ✓ exact |
| Gate order scope→open→access→thermal→evidence→improvement | `PHASE3_DECISION_ARCHITECTURE.md` §1 | ✓ exact |
| Exclusion vocabulary; evidence_confidence = weakest link | `PHASE3_DECISION_ARCHITECTURE.md` §2–3 | ✓ exact |
| Δ = 0.8 °C = median per-row UTCI sensitivity | `PHASE3_METHOD.md` §5.2 | ✓ exact |
| Accessibility straight-line @4.8 km/h; 800 m primary, 500/1200 m | `PHASE3_METHOD.md` §5.1 | ✓ exact |
| 8 pre-registered scenarios incl. one no-survivor test | `PHASE3_SCENARIOS.md` | ✓ exact |
| Nearest-open baseline, no thermal/evidence screening | `PHASE3_DECISION_ARCHITECTURE.md` §5 | ✓ exact |

No factual contradiction was found. No statement in the draft required a
repository value that could not be located.

## 2. Proxy described correctly

- Defined as **two inputs → decision rule**: ambient air-temperature hazard band
  (AEMET civil-protection thresholds) × OSM `natural=tree` count exposure tercile,
  combined by a first-matching-rule tree. ✓ (proxy def §1–2)
- Explicit negative list present in the draft (§3.3): "not a land-surface-
  temperature product, a satellite surface-temperature proxy, a canopy or shade
  model, or a shadow simulation." ✓
- Tree count stated as a **presence proxy for shade availability**, explicitly not
  a measure of canopy cover, shadow geometry, or sun position. ✓
- Terciles stated as a **within-sample relative grade**, not a transferable
  threshold. ✓
- The word "naive" is **not** applied to the proxy anywhere in §3.3 (reserved only
  for the deliberately-naive nearest-open *comparison baseline* in §3.8, which is
  the correct target of that word per `PHASE3_DECISION_ARCHITECTURE.md` §5). ✓

## 3. No Results leakage

Automated scan of the draft for the Tier-1 headline statistics returned **no
matches**: `33.3`, `64.3`, `35.7`, `14/42`, `7/8`, `3/8`, `23 options`, `83.3`,
`45.2`, `71.4`, `0.42`, `9 physical`, `5 physical`, and the noon "14/14 ≥32 °C"
finding are all absent. Numbers that do appear are **design/method parameters**,
not outcomes: 3.5 km², 27/13/14 assets, 42 outdoor rows, 3 timestamps, air-temp
inputs 34.2/38.8/40.5 °C, tercile cut-points 0.33/3.67, UTCI thresholds 32/46 °C,
Δ = 0.8 °C, radii 500/800/1200 m, 8 scenarios, opening-hours provenance counts
11/27 and 16/27. None of these is a finding; each is required to describe the test.
✓ No Results leakage.

## 4. No unsupported superiority claim

The draft never states the physical model is more accurate, correct, true, or
validated relative to the proxy. It uses "physically based" and "radiation-
resolving," and states explicitly (§3.4) the model is treated "never as ground
truth or as a more accurate representation of comfort than the baseline," and
(§3.5) that a reclassified row "indicates that the two methods disagree, not that
one is correct and the other wrong." This matches Evidence-Matrix C1/C2 forbidden
wording and the charter §6 claim ceiling. ✓

## 5. No LST misstatement

"LST," "land surface temperature," "satellite temperature," and "surface
temperature" appear **only** inside the §3.3 negative definition that rules them
out. No sentence attributes surface-temperature, radiant, or shadow measurement to
the proxy. ✓ (proxy def §5, §10)

## 6. Modelling vs observation distinction preserved

- Observed: air temperature, humidity, wind, pressure (Barajas). Explicitly
  labelled observed. ✓
- Estimated: global horizontal irradiance — labelled "estimated, not observed" and
  "treated as such throughout." ✓
- Modelled: Tmrt (SOLWEIG) and UTCI — labelled "a model output, not a measured or
  observed quantity," never "observed comfort." ✓
- The draft states the station observations validate only the Ta/RH/wind inputs,
  not the radiant output. ✓ (matches `PHASE2_UTCI_METHOD.md`)

## 7. Permanent limitations represented

All seven permanent limitations (handoff §10) are present in the Methods where
methodologically appropriate (full treatment remains reserved for the Limitations
section):

1. No field validation of Tmrt/UTCI — §3.4, §3.6, §3.9. ✓
2. Genuine residual UNSTABLE solar-boundary case — the UNSTABLE class and its
   propagation are described in §3.6; the specific A24 @ 18:00 instance is a
   Results/Limitations item, not stated here (correctly). ✓ (category represented)
3. Tested uncertainty = solar + targeted geometry only (not humidity/wind/
   structural) — §3.6. ✓
4. Accessibility straight-line only; no route-level heat exposure — §3.8, §3.9. ✓
5. No behavioural claim — §3.1, §3.8, §3.9. ✓
6. Indoor refuge assumed without verified A/C or queue exposure — §3.9. ✓
7. Opening hours 2026-documented, applied to 2023 — §3.2. ✓

## 8. No behavioural claim

The draft asserts screening-only scope in three places (§3.1 "the individual
tourist is explicitly not a unit of analysis…no quantity…describes tourist
behaviour, choice, or flow"; §3.7 "the framework makes no claim that any tourist
will choose, follow, or prefer them"; §3.8 "does not measure, and makes no claim
about, tourist behaviour or travel substitution"). No prediction, redistribution,
adoption, or outcome-improvement language appears. ✓ (Evidence-Matrix C14; charter
§4)

## 9. Word count

Body prose (excluding markdown headings): **≈ 2,799 words** (≈ 2,855 including
headings). Target band was 2,000–2,700 before journal-specific compression. The
draft sits **~100 words (≈4%) above the upper bound** — marginal, and the intended
compression lever is the supplementary-material deferral list below (§11), which
can move software/provenance detail out of the main text to land inside the band
for the target journal. Not a gate blocker.

## 10. Citations

Four citations are used, all present in `PHASE5_1_LITERATURE_MATRIX.csv`:
Lindberg et al. 2008 (SOLWEIG), Bröde et al. 2012 (UTCI), Gál & Kántor 2019 (Tmrt
plausibility range), plus AEMET official publications (institutional, no
author-year). No bibliographic metadata was invented; no `[CITATION TO VERIFY]`
placeholder was required because citation use was kept minimal and every cited item
is already verified in the matrix. ✓

## 11. Recommended supplementary methods (deferred — outside the manuscript)

The following implementation minutiae are correctly kept out of the main Methods
and should be placed in Supplementary Material (consistent with
`PHASE5_0_MANUSCRIPT_ARCHITECTURE.md` §10, which routes per-asset dumps and code
paths to supplementary):

1. **Software environment detail** — dual Python interpreters (3.14 geo stack /
   3.12 `.venv_solweig`), exact dependency pins (rasterio, numpy, pyproj, shapely,
   pvlib), CRS `LOCAL_CS`→EPSG:25830 re-tagging, GPU auto-dispatch note.
2. **SOLWEIG default-parameter table** — transmissivity 0.03/0.5, trunk ratio 0.25,
   leaf-on DOY 97–300, human-geometry constants (Fside/Fup/height/Fcyl), the
   documented L↓ +18–55 W/m² package bias.
3. **Meteorological forcing table** — per-hour Ta/RH/wind/pressure/GHI/solar-
   elevation values (`data/raw/phase2_met_forcing.csv`).
4. **Geometry-recheck procedure (Phase 2.2 Task A)** — per-tree `altura_m`
   inventory query, MATERIALLY/PARTIALLY/REPRESENTATIVE stale rule, crown-radius
   bracket R ∈ {2,3,4} m, A24-as-control verification.
5. **Full exclusion vocabulary and evidence-confidence rank mapping** (T2 material).
6. **Opening-hours source table** — the 27-asset OSM-vs-documented split with each
   source string and completeness flag.
7. **Proxy-family convergence detail (Phase 1.2)** — OSM-tree vs Copernicus-TCD vs
   green-polygon comparison and the pre-registered 85% agreement gate (supports the
   motivation for physical modelling; T6 material). *Note: the draft does not yet
   include the one-sentence "simple proxies did not converge, motivating physical
   modelling" motivation (Evidence-Matrix C12; architecture §4.1). This is optional
   for Methods and can be added in §3.3 or carried in Introduction/§4.1 — flagged,
   not required for approval.*
8. **Data-source provenance table (T1)** — layer/dataset/vintage/licence/"what it
   does not measure," per `DATA_SOURCE_INVENTORY.csv`.
9. **Reproducibility chain** — script execution order and per-file hashes.

## 12. Minor observations (non-blocking)

- The draft numbers Methods as **§3** (per the Phase 5.2A task instruction), whereas
  `PHASE5_0_MANUSCRIPT_ARCHITECTURE.md` places Study area at §3 and Methods at §4
  with a separate preceding "Study area and data" section. This is a
  section-numbering convention only, not a content contradiction; final numbering
  is a compile-time decision when the other sections are drafted.
- C12 (proxy non-convergence) motivation is not yet in the Methods (see §11 item 7).
  Optional; does not affect any factual claim already made.

---

## METHODS GATE

Every methodological statement is traceable to a locked source; the proxy is
defined exactly and correctly guarded against LST/shade/canopy misstatement; the
physical model is described neutrally with no superiority claim; the decision engine
and comparison logic are reproducible; uncertainty is represented as tested-only,
categorical, and non-collapsed; claim boundaries and the seven permanent
limitations are explicit; no numerical Results are reported prematurely; and word
count is marginally over target with a clear supplementary-deferral lever.

**METHODS DRAFT APPROVED**
