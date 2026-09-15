# AMENDMENT_003 — SOLWEIG stateful temporal-execution protocol + hardened Catastro acquisition

**Date:** 2026-09-15 · **Raised at:** Gate-3A external review (execution-semantics defect).
**Motivation:** implementation semantics discovered during review — **not** the observed
A-vs-B result. Narrowly scoped: corrects *how* the frozen fields are executed, changing **no**
frozen route, resolution, metric, decision rule, perturbation, or UTCI boundary.

## 1. Defect: non-stateful per-timestamp SOLWEIG execution
Gate-3A `gate3a_run_solweig.py` called `solweig.calculate()` **once per timestamp** (8 separate
calls). For the pinned `solweig` v0.1.0b92:
- a single `Weather` is auto-wrapped into a **one-element** timeseries;
- each `calculate()` call initialises a **fresh `ThermalState`**;
- a one-element run derives a **1-hour** timestep;
- surface/wall thermal history is carried **only within one multi-timestep `calculate()` call**.

So the 14:00/14:15/… fields each **reset** surface/wall thermal state — not a stateful
15-minute series. This can bias Tmrt (wall/ground heat storage) at the decision timestamps.

## 2. Corrective state-initialization protocol (frozen here)
- Build a **continuous 15-minute `Weather` sequence** and pass the **whole list** to a
  **single** `solweig.calculate(surface, weather=[...])` call (the documented stateful path;
  `weather: Weather | list[Weather]`).
- Sequence: **00:00 → 17:45 local (Europe/Madrid), 72 steps at 15 min**. Uniform spacing so
  v0.1.0b92's first-interval-derived timestep is correct. The pre-17:00 steps are **model
  preconditioning / state continuity**, NOT additional decision observations. (Passing only the
  8 sparse decision timestamps is prohibited: the 14:45→17:00 gap would be misread as 15 min.)
- Forcing: interpolate the frozen hourly Barajas Ta/RH/pressure/wind to each 15-min step;
  recompute pvlib Ineichen clear-sky radiation at each **actual** timestamp.
- **Only** the frozen decision/traversal fields enter route metrics: 14:00, 14:15, 14:30,
  14:45, 17:00, 17:15, 17:30, 17:45.
- Record exact SOLWEIG run metadata (`create_run_metadata`/`save_run_metadata`) and the
  stateful protocol.
- **Resource rule:** if RAM prevents the scientifically-correct single stateful run, **STOP
  and report `RESOURCE_BLOCKED`** — do **not** fall back to independent one-timestamp runs.

## 3. Hardened, fail-closed Catastro acquisition
Gate-3A `catastro_footprints()` was fail-open (silent per-subtile except; regex over every
`gml:posList` treated as an independent polygon). Corrected (`src/catastro_bu.py`):
- every WFS subtile **must** succeed; HTTP≠200 raises; OGC `ExceptionReport` detected and
  raised; GML parse errors raise; **incomplete acquisition aborts the geometry build**;
- **EPSG:25830 requested directly** (service DefaultCRS; no 4326 round-trip);
- **structural GML parse** — `bu-ext2d:Building` → `bu-core2d:BuildingGeometry` → `gml:Surface`
  → `gml:PolygonPatch`, preserving **exterior + interior rings** and **multipart** geometry
  (interior courtyards are holes, not filled building);
- **dedup by `gml:id`** across tiled BBOX requests (deterministic first-occurrence);
- per-subtile provenance + SHA-256 recorded (`catastro_provenance.json`).

## 4. Freeze-record nomenclature correction
The Gate-2 manifest/ledger named the building feature type `bu-ext2d:Building`. The **operational
WFS feature type is `bu:Building`** (advertised in GetCapabilities, namespace
`urn:x-inspire:specification:gmlas:Buildings:3.0`; the *returned members* are
`bu-ext2d:Building`). Requesting `bu-ext2d:Building` returns empty. This is a nomenclature
correction to the freeze record; the intended source (Catastro INSPIRE BU Building) is unchanged.

## 5. Geometry impact (measured)
Re-running the build with the hardened Catastro changed the geometry (interior courtyards no
longer filled; dedup; multipart): building-footprint coverage **32.03% → 30.14%**; `dsm_2m` and
`cdsm_2m` hashes changed; `dem_2m`/`veg_mask` unchanged. The corrected geometry is therefore
used for the corrected thermal run.
