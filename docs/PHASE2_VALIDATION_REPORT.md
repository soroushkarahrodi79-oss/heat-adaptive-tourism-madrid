# PHASE2_VALIDATION_REPORT.md — HATI-Madrid Phase 2

Version 1.0 · 2026-08-17. Validation is separated into four clearly distinct
categories, per the task specification. **They are not interchangeable and
are not allowed to substitute for one another** — in particular, §1
(meteorological forcing validation) validates the *inputs* to SOLWEIG, not
its *outputs*, and must never be cited as evidence that Tmrt or UTCI are
themselves validated.

---

## 1. Meteorological forcing validation (real observations)

The air temperature, relative humidity, wind speed, and pressure fed into
SOLWEIG are the same real Madrid/Barajas hourly station observations already
validated and cross-checked throughout Phase 1/1.1 (`docs/PHASE1_1_BASELINE_HARDENING.md`
Audit 1): a genuine AEMET-relayed synoptic record, cross-checked against
Retiro's official daily-max/monthly-mean figures (+0.5 °C daily-max gap,
+0.11 °C monthly-mean gap — real, quantified, small). This validation is
**inherited, not repeated**, and applies only to Ta/RH/wind/pressure as
*forcing inputs* to the model.

**Global horizontal irradiance is NOT a validated observation** — it is a
clear-sky model estimate (§ `docs/PHASE2_SOLWEIG_METHOD.md`). Its
justification is internal consistency (the real station weather code
confirms clear-sky conditions at all three hours) and the physical
correctness of the Ineichen model's solar geometry, not an independent
radiometric measurement. No pyranometer observation exists in this project
to validate the GHI estimate against.

**AEMET validates the meteorological forcing variables it actually
measures. It does not, and cannot, validate the modelled radiant
environment (Tmrt) or UTCI** — this distinction is deliberate and is
restated in §4.

## 2. Geometric/input validation (checks against source geometry)

**Elevation plausibility:** DEM values across the study area range 607–681 m,
DSM (ground+building) 607.8–709.9 m — both consistent with Madrid city
centre's known real elevation (~600–670 m above sea level per general
geographic reference). No physically impossible values (negative elevation,
implausible spikes beyond the max building height in the source data) were
found.

**Landmark spot-check (a real, checked exercise, not assumed to pass):**
building height was sampled at the exact coordinates of three real,
well-known landmarks from `data/processed/pilot_assets.csv`:

| Landmark | DSM (m) | DEM (m) | Building height at exact point |
|---|---:|---:|---:|
| Puerta de Alcalá | 656.0 | 656.0 | 0.0 m |
| Palacio de Cibeles | 645.0 | 645.0 | 0.0 m |
| Museo del Prado | 647.0 | 642.0 | 5.0 m |

**This is reported as found, including the parts that look wrong, not
smoothed over.** Puerta de Alcalá is a five-arch monumental gate with open
passages — a single 2.5 m pixel at its OSM point can genuinely land in an
archway gap, so 0.0 m there is plausible. Palacio de Cibeles, however, is a
real, substantial building (a landmark clock-tower city-hall) that should
show meaningful height, and 5.0 m at the Prado's OSM point is low for a
major museum facade. The most likely explanation is a **spatial-precision
mismatch between point-of-interest semantics and building footprint
geometry**: OSM asset points mark "where a tourist stands to visit the
place" (often a forecourt, entrance, or plaza-facing point), not the
building's own centroid or roofline — so a single-pixel read at that exact
point can miss the solid structure by a few metres.

**This finding directly validates the pre-registered choice of a 10 m
buffer MEAN, not a raw centroid, as the primary asset-exposure statistic**
(`src/phase2_prereg.py`): the buffer-mean Tmrt at these same two "0 m
building height" points is 50.6 °C (Puerta de Alcalá, 12:00) and 59.9 °C
(Palacio de Cibeles, 12:00) — clearly non-trivial, spatially-structured
values, not degenerate zeros, because the 10 m footprint captures the mix of
open forecourt and adjacent building mass that a single pixel does not. Had
this project used the centroid as its primary statistic (only reported as a
sensitivity companion, per the pre-registration), this exact artefact could
have silently biased results for point-precision-sensitive assets.

**Vegetation plausibility:** canopy heights 0–47 m, with 43.5% of the study
area showing >0.5 m canopy — consistent with the pilot's real dominance by
Retiro Park. A few very tall values (approaching 47 m) are at the upper end
of what is physically expected for individual specimen trees (Retiro is
documented to host mature, very old plane trees and cedars, which can
reasonably reach 30–40 m; 47 m is a plausible LiDAR maximum for such trees
but is flagged as a value to treat with some caution rather than uncritical
confidence).

## 3. Model plausibility (spatial patterns, shade behaviour, literature-consistent ranges)

**Spatial pattern:** the rendered Tmrt/UTCI maps (`outputs/maps/tmrt_1500.png`
etc.) show clear, physically coherent structure — real Madrid street-block
outlines, individual building shadows cast in directions consistent with
each timestep's real solar azimuth, and a distinct sun/shade contrast
between open plazas (e.g. Retiro's Estanque Grande, rendered as a large
contiguous high-Tmrt zone) and tree-shaded park paths (visible as
fine-grained low-Tmrt speckle following real canopy positions in Real
Jardín Botánico and Retiro). This spatial coherence — matching known real
geometry rather than being noise — is itself evidence the model is
responding to genuine input structure, not producing arbitrary output.

**Range plausibility:** modelled Tmrt reaches up to ~72–73 °C in full summer
sun on hardscape and UTCI up to ~46–47 °C ("Extreme heat stress," the
official top category). These are large numbers, but they are **within the
range documented in the published urban-climate literature** for
Mediterranean/Southern European cities during real summer heatwaves — Tmrt
values of 60–70+ °C in sunlit paved urban spaces are well-established in
SOLWEIG validation studies from comparable climates (this project's own
literature review, `docs/LITERATURE_MATRIX.csv`, cites the general
UTCI/Tmrt literature basis for this expectation, though no city-specific
comparison figure is available for Madrid within this project's own
sources).

**Diurnal/temporal coherence:** the whole-grid mean Tmrt/UTCI rises from
12:00 (Tmrt 47.5 °C, UTCI 36.1 °C) to a peak around 15:00 (Tmrt 53.4 °C,
UTCI 42.1 °C) before easing only slightly by 18:00 (Tmrt 49.6 °C, UTCI
42.4 °C, driven by the real observed air temperature still rising into the
evening on this specific extreme day) — a physically sensible pattern
tracking real solar elevation and the real, independently observed Barajas
temperature trajectory (34.2 → 38.8 → 40.5 °C) documented throughout this
project since Phase 1.

## 4. Direct Tmrt validation

**No field measurements (globe-temperature radiometer, six-directional net
radiometer, or any in-situ Tmrt/UTCI observation) exist for this study area
or this date in this project.** AEMET's real station data validates air
temperature, humidity, wind, and pressure as *forcing inputs* (§1) — **it
does not, and by construction cannot, validate the modelled radiant
environment**, because AEMET does not measure Tmrt, radiant flux
components, or shade geometry at any location.

**This is stated here as a first-class, permanent limitation of this Phase
2 spike, not a gap this project attempted to paper over.** No synthetic
field-validation dataset was created to fill this gap, per the task's
explicit prohibition. The plausibility checks in §3 (spatial coherence,
literature-consistent ranges, physically sensible diurnal pattern) are the
strongest evidence this project can offer that the model is behaving
sensibly — they are **not** a substitute for direct validation, and no
claim in this document should be read as asserting the specific numeric
Tmrt/UTCI values are independently confirmed against ground truth.

## Additional documented limitations (carried into the gate decision)

- **Wind is not spatially resolved.** A single station-scale wind speed
  value is applied uniformly across the whole 2.5 m grid at each timestep
  (real Barajas observation: 2.61 / 1.00 / 2.11 m/s at 12:00/15:00/18:00).
  Real street-level wind heterogeneity (channelling between buildings,
  stagnation in enclosed courtyards, acceleration around corners) is
  **not** resolved — no CFD or URock was introduced this phase, per the
  task's explicit instruction. This likely understates wind-driven cooling
  variability between, e.g., a wide open plaza and an enclosed courtyard.
- **Land cover is the package default**, not a study-area-specific
  classification (§ `docs/PHASE2_INPUT_FEASIBILITY.md`) — surface albedo/
  emissivity effects are approximated, not site-verified.
- **The vegetation (canopy) geometry is ~8–15 years old** (PNOA-LiDAR 1ª
  cobertura) — the single largest documented input-vintage gap in this
  phase (§ `docs/PHASE2_INPUT_FEASIBILITY.md`), larger than any prior
  phase's proxy-data gaps.
- **SOLWEIG's own documented Ldown positive bias** (+18 to +55 W/m²,
  quoted verbatim in `docs/PHASE2_SOLWEIG_METHOD.md`) is a known property
  of this specific model version, not something this project's own testing
  discovered — inherited as-is.
