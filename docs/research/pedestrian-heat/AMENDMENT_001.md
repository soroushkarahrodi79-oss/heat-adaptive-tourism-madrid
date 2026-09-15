# AMENDMENT_001 — Terrain source: Madrid MDT 2019 → MDT 2023

**Date:** 2026-09-15 · **Raised at:** Gate 3A (first thermal experiment), geometry
acquisition step, **before any thermal output was produced or inspected.**
**Status:** APPROVED by project owner (2026-09-15) to proceed for Gate 3A; ratification
for the robustness gate (3B) carried by this record.

## 1. What changes
The frozen Gate-2 baseline terrain source **"Madrid MDT 2019"** is replaced by
**"Madrid MDT 2023"** for the normalized surface height `nSH = MDS 2023 − MDT`.
No other frozen element changes (MDS 2023 surface, Catastro building footprints,
vegetation mask, routes, study day, departure times, forcing, metrics, perturbations,
controls all unchanged).

> **CORRECTION (2026-09-15, Gate-3A review).** The original v1 justification for this
> amendment contained factual errors about MDT-2019 availability and made unquantified
> invariance claims. Both are corrected below. The *decision* (use MDT 2023 for bounded,
> same-epoch execution, taken before any thermal output) stands, but it is reframed as an
> **acquisition/governance** choice, not a "2019 is impossible" claim.

## 2. Why (acquisition/governance choice — corrected)
- **Madrid MDT 2019 IS available** — as 10 cm ESRI-ASCII (.asc) tiles (`…/ELEVACIONES/2019/
  MDT/`) **and** as an associated **generalized 1 m COG mosaic** download. The earlier
  statement that "2019 has no COG" was **false** and is withdrawn.
- **Gate-2 record error:** the Gate-2 manifest/ledger described the terrain source as
  "10 cm COG tiles"; that too was inaccurate (the 10 cm 2019 product is ASC; the COG is a
  generalized 1 m mosaic). Recorded here as a freeze-record correction.
- **Choice made:** MDT **2023** is used because it is the **same 2023 campaign as the frozen
  MDS 2023**, giving a same-epoch `nSH = MDS 2023 − MDT 2023` from one consistent COG source
  clippable to the bounded OD1 domain via `/vsicurl`. This is an execution/consistency choice
  decided **before** any thermal output was produced or inspected — not forced by an
  impossibility.

## 3. Scientific impact (bounded; not quantified as "invariant")
- The decision-bearing quantity is **nSH (above-ground height)**; the change is to the
  **terrain datum** under it, applied identically to both routes.
- The earlier claims that 2019→2023 terrain is "essentially invariant" and "cannot by itself
  flip the ordering" are **removed** — they were **not quantified**. A direct MDT-2019 vs
  MDT-2023 comparison over OD1 has not been computed here, so no invariance is asserted.
- What *is* stated: terrain is applied identically to A and B, and Path-B forbids any
  accuracy/comfort/health claim resting on terrain vintage. Whether the terrain datum could
  affect the A−B ordering is left to be demonstrated, not assumed; if a reviewer requires it,
  an MDT-2019 vs MDT-2023 sensitivity run can be added under a further amendment.

## 4. Discovery timing & anti-cherry-pick
Discovered and decided **before** any Tmrt/UTCI was computed or inspected; the change is
forced by data format/availability, **not** chosen to favour any route or result.

## 5. Effect on records
- `GATE2_FREEZE_MANIFEST.json` / `GATE2_GEOMETRY_LEDGER.csv`: terrain source reads
  "Madrid MDT 2023 (per AMENDMENT_001)". The Gate-2 files are **not** silently edited;
  this amendment is the authoritative override, cited wherever terrain is used.
- Gate-3A provenance records MDT 2023 tile hashes and the exact windowed-acquisition.
