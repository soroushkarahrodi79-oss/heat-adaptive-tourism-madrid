# GATE2_PERTURBATION_SPEC — Frozen perturbation values

**Version 1.0 · 2026-09-15 · FROZEN before any thermal output.**
Every value below has a provenance or literature justification recorded next to it.
Nothing is an arbitrary sweep. Changing a value requires an `AMENDMENT_00x.md`.

## E-P1 — Meteorological forcing representativeness  [FROZEN]
- **(a)** Barajas 08221 as-is (the common forcing for both routes).
- **(b)** Empirical **hourly** Escuelas-Aguirre-minus-Barajas Ta/RH difference at the
  target hours, applied identically to both routes. **Measured values (24 Aug 2023):**
  - 14:00 h: ΔTa ≈ −1.7 °C (H14) to +0.1 °C (H15); ΔRH ≈ +3 to +6 %.
  - 17:00 h: ΔTa ≈ −0.2 °C (H17) to −0.1 °C (H18); ΔRH ≈ +3 to +4 %.
- **Justification.** Real corridor-adjacent urban station vs airport forcing, measured
  hourly (Escuelas Aguirre, verified complete/valid at target hours). The former
  +0.5 °C daily-max constant offset stays **DELETED** (a daily-max gap does not license
  a constant hourly offset).
- **ABSTAIN hook.** If the urban station were incomplete at a target hour → forcing
  uncertainty becomes ABSTAIN. **Not triggered here** (Escuelas Aguirre complete, all
  flags V).

## E-P2 — Canopy / vegetation geometry  [FROZEN — dominant dimension]
Four real, independent canopy states bound the decade of canopy change:
- **(a)** PNOA veg nDSM 2008–2015 (in-repo `veg_ndsm_025.tif`).
- **(b)** MDS 2023 normalized surface height **masked to vegetation** (mask = union of
  municipal tree-inventory buffers + OSM green polygons + Copernicus TCD ≥ threshold;
  Sentinel-2/optical **never** as thermal/LST — greenness only).
- **(c)** Municipal tree-inventory presence/removal audit (2025/2026) — flags canopy
  pixels contradicted by current reality (1322 park + 1528 street trees in-corridor;
  drop the single 139 m ALTURA outlier).
- **(d)** Copernicus TCD 2018 density (in-repo `tcd_2018_study_area.tif`).
- **Justification.** Four independent provenance sources, not a parametric sweep.
- **ABSTAIN hook (NC7).** If the A−B ordering flips across (a)–(d) → ABSTAIN.

## E-P3 — Wind treatment  [DEMOTED — not a frozen perturbation]
Removed from the frozen set (Gate-1). No published canyon-multiplier method for this
context, so none is invented. Uniform station wind is the only justified treatment.
Spatial wind heterogeneity remains an **unresolved limitation / ABSTAIN trigger** (see
`GATE2_EVIDENCE_REPORT.md` §2F). Complexity is not evidence; URock is not added to
rescue the case.

## E-P4 — Building / shadow geometry  [FROZEN]
- **(a)** MDS 2023 − MDT 2019 normalized surface height **classified to buildings via
  audited Catastro INSPIRE footprints** (footprint polygons verified available; height
  from nSH within footprints, **not** from Catastro floor count, which is a proxy and
  frequently nil).
- **(b)** PNOA 2008–2015 building nDSM (in-repo `building_ndsm_025.tif`) as an
  independent cross-vintage check.
- **Justification.** Raw MDS−MDT is *surface* height; buildings require classification.
  PNOA tests geometry-source/vintage sensitivity. IGN 2nd-coverage pull only if (a)/(b)
  still leave the pair fragile.

## E-P5 — Pedestrian network / side-of-street  [FROZEN]
- **Base:** the two frozen route polylines (Route A on the Paseo del Prado axis
  approach; Route B on the **park-side/east** sidewalk of Calle Alfonso XII).
- **Alternatives (side-of-street, where ambiguous):**
  - Route A: west sidewalk of Paseo del Prado vs the central Salón del Prado promenade.
  - Route B: **west** sidewalk of Alfonso XII vs the frozen **east (park-side)**
    sidewalk.
- **Justification.** OSM shows Alfonso XII sidewalks tagged mostly `right`/`both` and
  fragmented, and the Prado axis offers a central promenade plus flanking sidewalks —
  side-of-street measurably changes sun/shade exposure along the identical corridor.
  This is a real mapped ambiguity, not an invented offset.
- **ABSTAIN hook (NC/­E-P5).** If A−B ordering flips between sidewalk sides → ABSTAIN.

## E-P6 — Walking speed / pauses  [FROZEN]
- **Speeds:** 1.1 m/s and 1.4 m/s.
- **Optional endpoint pause:** a single fixed pause added identically to both routes
  (sensitivity only).
- **Justification.** Standard pedestrian preferred-speed range (slow/tourist ≈ 1.1;
  brisk ≈ 1.4 m/s); changes trip duration (M1) and the time-weighted / in-category
  metrics (M2, M4) and can reorder near-ties.

## Category-boundary guard band (operationalising "clear of a boundary")
A category-based metric (M2, M4) is **"clear of a UTCI category boundary"** iff its
**perturbation-ensemble uncertainty interval** (min–max across E-P1, E-P2, E-P4, E-P5,
E-P6) does **not** contain any of the cut-points +26/+32/+38/+46 °C. This ties the
guard to the model's own perturbation-derived uncertainty — **no fixed °C guard is
invented**. If the interval contains a cut-point → the metric straddles a boundary →
ABSTAIN (NC6).

## Explicitly excluded (scope / no decision change)
CFD/URock wind fields; city-wide modelling; future-climate scenarios; land-cover
refinement (unless a route crosses a strongly contrasting surface, L12); any ML.
