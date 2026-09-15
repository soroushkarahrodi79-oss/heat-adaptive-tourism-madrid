# GATE3A_QA_REPORT — Pipeline falsification / physical sanity

**Version 1.0 · 2026-09-15.** Diagnostics reported **before** interpreting Route A vs
Route B. A visually attractive map is not validation.

## 3A.1 Reproducibility preflight — PASS
All 14 Gate-2 artifact hashes recompute-match; both frozen route hashes match the
route-freeze record and the freeze manifest. CRS, study day, timezone, target departure
times, forcing source, independent-check file, building classifier, vegetation inputs,
route geometries and walking assumptions all verified against the freeze. No frozen hash
mismatched → did not fail closed.

## Frozen-assumption execution issue → AMENDMENT_001
Frozen terrain "Madrid MDT 2019" is not practically executable (10 cm ASC only, no
windowed/COG access). **AMENDMENT_001** (user-approved, pre-thermal) substitutes **MDT
2023** (same 2023 campaign as the frozen MDS 2023; COG, windowed-readable). Terrain-only,
same-epoch, immaterial to nSH, differenced out under both routes. Not silent.

## 3A.5 Field-level physical checks (SOLWEIG baseline, 8 timestamps)

| Check | Result | Verdict |
|---|---|---|
| Nodata artefacts (fields) | 0.0% nodata in every Tmrt/UTCI field | PASS |
| Route samples off valid raster | off_raster = False; nan_samples = 0 (all 4 route/departure combos) | PASS |
| Implausible values | out-of-range fraction 0.0 (UTCI∈[10,55], Tmrt∈[10,85]) | PASS |
| Raster-edge discontinuity | edge mean 44.4 °C vs interior 43.0 °C (UTCI, 17:00) — mild finite-domain SVF edge effect | CONFINED: routes are ≥150 m from the boundary (the buffer); no route sample lies in the edge zone |
| Building mask | Catastro 1850 footprints, 32.0% coverage; building heights max 63.6 m, mean 20.9 m | PASS (plausible heritage-core) |
| Vegetation mask | 34.4% coverage; canopy heights max 36.9 m, mean 8.3 m | PASS |
| Building/vegetation misclassification | 15.1% of domain is "tall (≥2 m) nSH" neither in a Catastro footprint nor the veg mask, currently treated as ground | LIMITATION (see below) |
| Impossible shadow patterns | Tmrt bimodal (17:00 p05 38.6 / p50 65.1 / p95 68.2 °C); shaded frac 0.37 | PASS (sun/shade structure present) |
| Timezone / solar-position | 14:00 CEST → solar elevation 60.4° (near solar-noon max 13:47), azimuth 171° (S); 17:00 → 43.7°, 242° (WSW); 17:45 → 35.8° | PASS (correct) |
| Shadow temporal evolution | shaded fraction 0.315 (14:00) → 0.373 (17:00) → 0.418 (17:45) as sun lowers | PASS (physically correct) |
| CRS displacement | domain bounds match requested EPSG:25830 extent; MDS/MDT/Catastro co-registered | PASS |
| Sun/shade on classification | Tmrt 17:00: under-vegetation 48.6 °C < open 57.7 °C < sunlit roof 64.3 °C | PASS (canopy shade cools ~9 °C — model responds to geometry) |

### Limitation: 15% unclassified-tall nSH
15.1% of domain pixels have nSH ≥ 2 m but fall outside both the Catastro building
footprints and the vegetation mask (footprint-edge slivers, boundary walls, monuments,
kiosks, and trees beyond the mask). These are currently modeled as ground, so their
shadows are omitted. Dominant obstacles **are** modeled (buildings 32%, canopy 34%). This
does not invalidate the baseline comparison but is a **classification-refinement item for
the robustness gate** (tighten footprint/veg coverage to reduce the unclassified tail).

## 3A.6 Independent meteorological context (representativeness only)
`GATE3A_METEOROLOGY_CHECK.csv`. Escuelas Aguirre urban Ta tracks the Barajas forcing
within ~0–2 °C at the target hours (14:00: EA 35.3–37.1 vs forcing 37.0; 17:00: EA
39.8–39.9 vs forcing 40.0); RH +3…+6 %. This checks forcing representativeness only — it
**does not validate Tmrt or UTCI**. Corridor-local **wind and radiation remain
unobserved** (uniform wind; modeled clear-sky radiation) — stated limitations.

## TEMPORAL-DISCRETIZATION QA (±7.5 min, frozen 15-min nearest-field method)
Re-sampling each route with the field chosen at −7.5 / nearest / +7.5 min:

| Departure | A−B (−7.5) | A−B (nearest) | A−B (+7.5) | Sign flips? |
|---|---|---|---|---|
| 14:00 | −0.08 | −0.10 | −0.11 | No |
| 17:00 | −0.43 | −0.41 | −0.33 | No |

The ±7.5 min discretization **does not flip the sign** of the Route A − Route B mean-UTCI
difference at either departure; magnitude varies ≤ 0.1 °C. Discretization could **not
plausibly alter the intensity ordering** at the trip-mean level → no MODIFY required on
temporal grounds. (Segment-level shadow timing near individual crossings remains a
sub-trip uncertainty carried, unchanged, into the robustness gate.)

## Overall QA verdict
Fields are reproducible, physically coherent, correctly geo-/time-referenced, and route
sampling is valid (0 off-raster, 0 nan). The only artefacts (edge SVF effect;
15% unclassified-tall) are **confined / non-invalidating** and logged for the robustness
gate. **No unresolved artefact invalidates the Route A vs Route B comparison.**
