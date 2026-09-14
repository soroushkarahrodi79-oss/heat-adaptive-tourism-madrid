# GATE1_EXPERIMENT_SPEC — Frozen minimal comparison / perturbation experiment

**Version 0.1 · 2026-09-14. Status: FROZEN specification of a FUTURE experiment. NOT executed.**

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
| **Study day** | To be frozen at Gate 2 start on rules R1–R6 (`GATE1_FEASIBILITY_DOSSIER.md` §1B). Shortlist: 2021-08-14 (primary candidate) or a fresh AEMET-warning day; 2023-08-21 is **legacy stress-test only**. |
| **Target hours** | A small fixed set within the confirmed clear-sky daylight envelope (e.g. one near solar noon + one late-afternoon), fixed before running. |
| **Claim ceiling** | Path B — robustness / sensitivity / decision-reversal / evidence sufficiency of *modeled* comparative exposure. No accuracy/comfort/behaviour/health claim. |
| **Primary exposure statistic** | Cumulative along-route modeled UTCI exposure integral (∫ UTCI dt over the walk), plus a category-boundary flag. Buffer-mean sampling (not raw centroid) per the locked pilot's own validated choice. |

## 2. Preconditions that MUST be satisfied before any thermal run (from Gate 1)

- **P-A:** L05 pedestrian network acquired for the two routes via a bounded Overpass query
  (two corridors only — not city-wide) and stored as versioned GeoJSON in EPSG:25830.
- **P-B:** L06 access/crossing audit: both routes verified legally + physically walkable
  end-to-end on the study day; every controlled crossing and park gate (with opening hours)
  recorded. Any unresolved access → the case moves to an ABSTAIN negative control, not a run.
- **P-C:** Study day frozen on R1–R6; forcing (Barajas) and independent check (Retiro/ERA5)
  are **different** series.
- **P-D:** Both route polylines frozen and hashed before any UTCI field is generated.

## 3. Perturbation dimensions (frozen ranges + justification)

Each dimension is included **only** because it can change the *decision*; each range is
justified by data provenance or literature, never invented.

| Dim | Perturbation | Frozen alternatives | Justification of the range |
|---|---|---|---|
| E-P1 | Forcing representativeness | (a) Barajas as-is; (b) diurnal shape re-anchored to Retiro official daily-max (+0.5 °C offset, the *measured* Barajas–Retiro gap). | The gap is a real, quantified value (Phase 1.1 Audit 1), not a guess. |
| E-P2 | **Canopy geometry** | (a) PNOA 1st-coverage veg nDSM (2008–2015); (b) current Madrid arbolado per-tree points rasterised to canopy presence; (c) Copernicus TCD 2018 density as a third bounding state. | Three *real, independent* canopy datasets already in-repo/available bound the decade of unknown canopy change. |
| E-P3 | Wind treatment | (a) uniform station wind; (b) simple open-plaza vs street-canyon multiplier (documented, no CFD/URock). | Bounds plaza-vs-canyon cooling contrast without introducing an unvalidated CFD field. |
| E-P4 | Building/shadow geometry | (a) 1st-coverage building nDSM; (b) 2nd-coverage (2015–2021) sheet pull **only if** E-P2/E-P3 show the pair is decision-sensitive. | Avoids an expensive manual sheet download unless the cheaper perturbations already show fragility. |
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
