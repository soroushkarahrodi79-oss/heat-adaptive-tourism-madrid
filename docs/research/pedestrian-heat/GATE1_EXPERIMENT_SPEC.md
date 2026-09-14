# GATE1_EXPERIMENT_SPEC — Frozen minimal comparison / perturbation experiment

**Version 0.2 · 2026-09-14. Status: FROZEN specification of a FUTURE experiment. NOT executed.**

> **Revised 2026-09-14 (evidence correction):** E-P1 constant-offset deleted (empirical-hourly
> or ABSTAIN); E-P2/E-P4 geometry now use Madrid MDS 2023 / MDT 2019 + tree inventory; study
> day now prefers a fresh 2023/2024 heat event; independent check is Escuelas Aguirre hourly
> Ta/RH. See `GATE1_FEASIBILITY_DOSSIER.md` §GATE1_EVIDENCE_CORRECTION_2026-09-14.

> This is a pre-registration-style freeze of the *smallest defensible* Gate 2 experiment. It
> is written now, **before** any thermal output exists, precisely so that route pair, day,
> perturbation ranges, and decision rules cannot be chosen after seeing results. Changing any
> frozen element after Gate 2 begins requires an `AMENDMENT_00x.md`. No SOLWEIG/URock/UTCI is
> run in this document.

---

## 1. Fixed design (frozen)

| Element | Frozen value |
|---|---|
| **O-D case** | OD1: Atocha (A09, 40.404557, −3.688683) → Puerta de Alcalá (A14, 40.419987, −3.688724). |
| **Alt A** | Paseo del Prado / Recoletos monumental axis (open, low continuous canopy). |
| **Alt B** | Real Jardín Botánico / Retiro western edge + Calle Alfonso XII (tree-lined). |
| **Study day** | To be frozen at Gate 2 start on rules R1–R7 (`GATE1_FEASIBILITY_DOSSIER.md` §1B; updated 2026-09-14). **Preferred: a fresh 2023/2024 AEMET heat-warning day (≠ 21 Aug 2023)** — aligns Barajas/municipal hourly forcing, the Escuelas Aguirre urban hourly check, and MDS-2023 geometry. 2021-08-14 = PNOA-vintage alternative; 2023-08-21 = legacy stress-test only. |
| **Target hours** | A small fixed set within the confirmed clear-sky daylight envelope (e.g. one near solar noon + one late-afternoon), fixed before running. |
| **Claim ceiling** | Path B — robustness / sensitivity / decision-reversal / evidence sufficiency of *modeled* comparative exposure. No accuracy/comfort/behaviour/health claim. |
| **Primary exposure statistic** | Cumulative along-route modeled UTCI exposure integral (∫ UTCI dt over the walk), plus a category-boundary flag. Buffer-mean sampling (not raw centroid) per the locked pilot's own validated choice. |

## 2. Preconditions that MUST be satisfied before any thermal run (from Gate 1)

- **P-A:** L05 pedestrian network acquired for the two routes via a bounded Overpass query
  (two corridors only — not city-wide) and stored as versioned GeoJSON in EPSG:25830.
- **P-B:** L06 access/crossing audit: both routes verified legally + physically walkable
  end-to-end on the study day; every controlled crossing and park gate (with opening hours)
  recorded. Any unresolved access → the case moves to an ABSTAIN negative control, not a run.
- **P-C:** Study day frozen on R1–R7; forcing (Barajas or a municipal met station) and the
  independent **urban** check (Escuelas Aguirre hourly Ta/RH) are **different** series.
- **P-D:** Both route polylines frozen and hashed before any UTCI field is generated.
- **P-E (added 2026-09-14):** Geometry frozen — terrain = MDT 2019, building surface =
  MDS 2023 − MDT 2019, canopy bounded per E-P2; obtained by **bounded bbox clip to OD1 only**
  (not a city-wide raster download), with PNOA retained as cross-check.

## 3. Perturbation dimensions (frozen ranges + justification)

Each dimension is included **only** because it can change the *decision*; each range is
justified by data provenance or literature, never invented.

| Dim | Perturbation | Frozen alternatives | Justification of the range |
|---|---|---|---|
| E-P1 (revised 2026-09-14) | Forcing representativeness | (a) Barajas as-is; (b) an **empirical hourly** Escuelas-Aguirre-minus-Barajas Ta/RH difference at the target hours. **If** the urban station is incomplete for the chosen day/hours → forcing uncertainty is an **ABSTAIN** condition. | Airport-vs-centre bias measured hourly from a real corridor-adjacent station. **The former +0.5 °C daily-max constant offset is DELETED** — a daily-max gap does not license a constant hourly offset. |
| E-P2 (revised 2026-09-14) | **Canopy geometry** | (a) PNOA veg nDSM (2008–2015); (b) **MDS 2023** surface-derived canopy height; (c) **municipal tree-inventory** presence/removal audit; (d) Copernicus TCD 2018 density. | Four *real, independent* canopy states bound the change; MDS 2023 + inventory add 2023/current vintages the old set lacked. |
| E-P3 | Wind treatment | (a) uniform station wind; (b) simple open-plaza vs street-canyon multiplier (documented, no CFD/URock). | Bounds plaza-vs-canyon cooling contrast without introducing an unvalidated CFD field. |
| E-P4 (revised 2026-09-14) | Building/shadow geometry | (a) **MDS 2023 − MDT 2019** building surface (2023, preferred); (b) PNOA 2008–2015 building nDSM as cross-check. | 2023 surface is near-contemporaneous with a 2023+ study day; PNOA tests geometry-source sensitivity. IGN 2nd-coverage sheet pull only if (a)/(b) still leave the pair fragile. |
| E-P5 | Network / side-of-street | Two audited traces where sidewalk side is ambiguous (side A vs side B). | Side-of-street changes sun/shade exposure along the identical corridor. |
| E-P6 | Walking speed / pauses | 1.1 m/s vs 1.4 m/s; optional endpoint pause. | Standard pedestrian speed range; changes the exposure integral and can reorder near-ties. |

**Explicitly excluded** (would violate scope or add complexity without changing the
decision): CFD/URock wind fields, city-wide modelling, future-climate scenarios, land-cover
refinement (unless a route crosses a strongly contrasting surface, per L12), any ML.

## 4. Decision rule (frozen — no invented threshold)

Framed on decision stability (pairwise rank-reversal robustness), **not** a fixed °C cut:

- **ROBUST COMPARISON** — sign of the Alt A − Alt B exposure difference is preserved across
  **all** of E-P1…E-P6 AND the difference is clear of a UTCI category boundary.
- **NO ROBUST DIFFERENCE** — routes indistinguishable, or sign stable but magnitude inside
  the modeled uncertainty interval.
- **ABSTAIN / NO EVIDENCE** — the sign **reverses** under ≥1 justified perturbation, OR an
  essential input is MISSING (L05/L06), OR the comparison straddles a UTCI category boundary,
  OR the uncertainty interval spans the decision.

A "material difference" threshold will be adopted **only** if the Gate-2 literature update
finds a defensible, comparison-specific value; otherwise the stability formulation above
governs. (Gate 1 found none — see `GATE1_LITERATURE_LOG.md`.)

## 5. Negative controls that MUST return ABSTAIN

NC1–NC7 (`GATE1_FEASIBILITY_DOSSIER.md` §1F) are run alongside OD1. If the method confidently
resolves any negative control, the evidence-sufficiency logic has failed and the method — not
the control — is rejected.

## 6. What this experiment will and will not output

- **Will:** a ROBUST / NO-ROBUST-DIFFERENCE / ABSTAIN label for OD1 with its perturbation
  audit trail; negative-control behaviour; an explicit statement of the vintage each result
  rests on.
- **Will NOT:** a validated UTCI accuracy figure, a comfort/behaviour/health claim, a
  recommender, a dashboard, a city-wide map, or a route "recommendation" derived from thermal
  output.
