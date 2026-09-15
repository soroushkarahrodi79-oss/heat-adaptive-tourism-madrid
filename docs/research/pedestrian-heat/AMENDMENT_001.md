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

## 2. Why (frozen assumption impossible to execute as written)
- Madrid publishes the **2019** terrain only as **10 cm ESRI-ASCII (.asc)** tiles
  (`…/ELEVACIONES/2019/MDT/`), which are gigabyte-scale per 1 km tile with **no
  cloud-optimized / windowed (`/vsicurl`) access** — not practically clippable to the
  bounded OD1 domain.
- The **2023** campaign publishes both **MDS 2023 and MDT 2023** as **Cloud-Optimized
  GeoTIFF** with internal overviews (`…/ELEVACIONES/2023/{MDS,MDT}/COG/<tile>.tif`),
  verified live and windowed-readable (2026-09-15).
- The Gate-2 manifest itself labelled the terrain "MDT actualizado (MDT 2019)"; the
  *actualizado* (current) Madrid MDT is the 2023 product. The "2019" was a vintage
  assumption carried from Gate 1, not a scientific requirement.

## 3. Scientific impact (immaterial; arguably improving)
- The decision-bearing quantity is **nSH (above-ground height)**. Bare-earth **terrain
  is essentially invariant 2019→2023** in the protected built heritage core (Prado
  axis / Alfonso XII); no terracing/regrading occurred.
- Using MDT 2023 makes surface and terrain **same-epoch (2023)**, giving a cleaner nSH
  than mixing a 2023 surface with 2019 terrain.
- Terrain is nearly identical under **both** routes and is **differenced out** in the
  Route A − Route B comparison; it cannot by itself flip the ordering.
- Path-B claim ceiling unaffected (no accuracy/comfort/health claim rests on terrain
  vintage).

## 4. Discovery timing & anti-cherry-pick
Discovered and decided **before** any Tmrt/UTCI was computed or inspected; the change is
forced by data format/availability, **not** chosen to favour any route or result.

## 5. Effect on records
- `GATE2_FREEZE_MANIFEST.json` / `GATE2_GEOMETRY_LEDGER.csv`: terrain source reads
  "Madrid MDT 2023 (per AMENDMENT_001)". The Gate-2 files are **not** silently edited;
  this amendment is the authoritative override, cited wherever terrain is used.
- Gate-3A provenance records MDT 2023 tile hashes and the exact windowed-acquisition.
