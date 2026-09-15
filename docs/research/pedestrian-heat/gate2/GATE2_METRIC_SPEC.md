# GATE2_METRIC_SPEC — Frozen route-comparison outcome metrics

**Version 1.0 · 2026-09-15 · FROZEN before any thermal output.**
Changing any definition below requires an `AMENDMENT_00x.md`.

> This freezes the exact metrics, formulas, sampling, weighting and category
> boundaries used to compare Route A vs Route B **before** any UTCI/Tmrt field
> exists. It inherits the Gate-1 decision: the single cumulative ∫UTCI dt scalar is
> **removed**; no output is called a "dose"; the comparison is judged on decision
> stability per metric, never on an invented °C threshold.

## 0. Common sampling definition (applies to every metric)

- **Spatial sampling.** Each frozen route polyline (EPSG:25830) is densified to a
  fixed along-route step **Δs = 5 m**, giving ordered sample points p₁…p_K.
- **Per-point value.** At each sample point the modeled UTCI is the **buffer-mean**
  over a circular buffer of the locked-pilot radius (the Phase-2 validated
  buffer-mean choice, not a raw single-pixel centroid), computed on the modeled
  UTCI raster at the target hour. The buffer radius is inherited from the locked
  pilot's validated sampling and re-stated in the freeze manifest at execution.
- **Temporal semantics — DEPARTURE TIMES, time-resolved traversal (frozen §0.1).**
  14:00 and 17:00 Europe/Madrid are **departure times**, not instantaneous whole-trip
  snapshots. A trip is ~30–40 min long (2366–2658 m at 1.1–1.4 m/s), which is a
  material fraction of an hour, so the thermal field is **not** held static across the
  trip unless the frozen fallback in §0.1 is invoked. Each route/departure is computed
  per §0.1.
- **Missing pixels.** If > 5 % of a route's sample points at a departure/traversal
  step fall on missing/nodata UTCI pixels, every metric for that route/departure is
  **undefined** and the case ABSTAINs for that departure (NC5 logic); no gap-filling.
- **Units.** UTCI in °C (equivalent temperature); durations in minutes; distances in m.

## 0.1 Temporal resolution & traversal sampling (frozen BEFORE any thermal output)

Fixed now from **model capability + authoritative documentation**, not from route
contrast (no thermal output exists yet):

- **Thermal-field temporal resolution Δt = 15 min (primary).** SOLWEIG computes the
  radiant field (Tmrt→UTCI) from the solar position at an **explicitly specified
  timestamp**; over a 30–40 min trip the solar geometry (hence shadow pattern) shifts
  materially, especially in the late-afternoon (17:00) window. The trip window at each
  departure is therefore discretised into Δt = 15 min sub-steps, each with its own
  SOLWEIG field at that timestamp's solar position. Δt = 15 min resolves within-trip
  shadow evolution while staying tractable (≤ 3 sub-steps per departure).
- **Segment traversal timestamp.** For sample point p_k, t_k = t_departure +
  (cumulative along-route distance to p_k) / v. Each route is walked forward from its
  own departure time; both routes use the **same** departure times and the same rule.
- **Thermal sampling at traversal time.** UTCI(p_k) is sampled from the SOLWEIG field
  whose timestamp is **nearest t_k** (nearest of the Δt = 15 min steps). Shadows/solar
  geometry thus evolve along the trip; a route's later segments see later solar
  positions.
- **Meteorological interpolation.** Ta/RH/pressure/wind are the hourly observed Barajas
  values, **linearly interpolated** to each Δt field timestamp where a step falls
  between two hourly observations; clear-sky GHI/DNI/DHI (pvlib Ineichen) are recomputed
  at each Δt timestamp's true solar position. Wind stays uniform in space (2F).
- **Fallback (explicit, claim-lowering).** If producing Δt = 15 min fields proves
  infeasible at execution, the experiment **drops to a single static field per
  departure hour** AND this temporal limitation is stated explicitly and the claim is
  lowered accordingly — it is **not** presented as a time-resolved departure-time
  comparison. Choosing the fallback is a stated downgrade, never a silent one, and is
  decided on feasibility, never on which resolution strengthens the A-vs-B contrast.

The temporal method is identical for Route A and Route B and is fixed here; it will not
be re-chosen after inspecting thermal outputs.

## 1. Frozen metrics

### M1 — Trip duration
- **Formula.** T = L / v, where L = route length (EPSG:25830 planar length of the
  frozen polyline) and v = walking speed (E-P6 alternative). Endpoint pause (E-P6),
  if the alternative includes it, is added as a fixed constant to both routes.
- **Units.** minutes. **Weighting.** none. **Stops.** only the explicit E-P6 pause.
- **Frozen route lengths:** Route A = 2657.8 m; Route B = 2365.7 m (see freeze manifest).
- **Class:** EXPOSURE-DURATION metric (see §1.6).

### M2 — Time-weighted mean modeled UTCI
- **Formula.** ŪTCI = Σ_k (UTCI(p_k) · w_k) / Σ_k w_k, where the weight
  w_k = dwell time on the sub-segment represented by p_k = Δs / v (constant for a
  constant speed, so ŪTCI reduces to the along-route arithmetic mean of the
  buffer-mean samples; the time-weighted form is retained so a variable-speed or
  paused E-P6 alternative weights correctly).
- **Units.** °C. **Class:** THERMAL-INTENSITY metric (§1.6), independent of route length.
- **Category semantics caveat.** The UTCI category boundaries may be *reported* against
  this route-level mean as a descriptive band, but categorising a route-**average** UTCI
  is **not** a physiological classification of the journey. ŪTCI remains a **comparative
  modeled descriptor** of intensity, not a health/physiological statement (Path B).
  Physiologically-meaningful category accounting is done only sample-by-sample in M4.

### M3 — Along-route distribution / range of modeled UTCI
- **Reported.** minimum, 25th percentile, median, 75th percentile, maximum, and IQR
  of {UTCI(p_k)} along the route at each target hour.
- **Role.** descriptive spread; **not** category-thresholded except where a reported
  percentile is used by M4. Distributional spread informs whether a small ŪTCI
  difference is robust or noise. **Class:** THERMAL-INTENSITY descriptor (§1.6),
  independent of route length.

### M4 — Minutes and proportion of trip within each UTCI stress category
- **Formula.** For each UTCI stress category c, minutes_c = (count of p_k whose
  buffer-mean UTCI ∈ category c) · (Δs / v); proportion_c = minutes_c / T.
- **Units.** minutes and dimensionless proportion. **This is the categorical,
  boundary-meaningful metric**, computed **sample-by-sample** at each location/traversal
  time (§0.1) — not from a route-level average. **Class:** EXPOSURE-DURATION metric
  (§1.6); minutes-in-category scale with trip length, proportion-in-category does not.

### M5 — Maximum / high-percentile modeled UTCI — DESCRIPTOR ONLY (not decision-bearing)
- **Reported** (route max and 95th percentile) for transparency, but **excluded from
  the decision rule**: Gate-1 and the Gate-2 literature check found no
  comparison-specific method justifying a maximum/high-percentile as a decision
  driver here. Per the Gate-1 instruction, it is dropped from the decision before
  freezing and retained only as a descriptor. **Class:** THERMAL-INTENSITY descriptor.

## 1.6 Intensity vs duration decomposition (frozen — route-length confound)

Route A (2657.8 m) and Route B (2365.7 m) are real alternatives of **different length**,
so the metrics MUST be read in two separate families and never collapsed:

- **THERMAL-INTENSITY** (microclimate; length-independent): M2 time-weighted mean UTCI,
  M3 distribution/range, M5 high-percentile descriptor.
- **EXPOSURE-DURATION** (accumulated load; length-dependent): M1 trip duration, M4
  minutes-in-category (and its length-normalised partner, proportion-in-category).

**Prohibition.** A route must **not** be called cooler/having a cooler microclimate
merely because it is shorter and therefore accumulates fewer minutes of exposure. A
shorter route can win M1/M4-minutes purely on length while being **hotter** per M2/M3.
The result MUST report intensity and duration separately, and report proportion-in-
category (length-normalised) alongside minutes-in-category so the length effect is
visible.

**Trade-off → ABSTAIN, not a composite.** If the THERMAL-INTENSITY family favours one
route while the EXPOSURE-DURATION family favours the other, that is a genuine
**trade-off** and supports **NO ROBUST DIFFERENCE / ABSTAIN** — it is **not** resolved
into a single winner. **No composite score is created** under any circumstance.

## 2. UTCI stress-category boundaries (frozen; authoritative)

Boundaries adopted verbatim from the operational UTCI assessment scale:

| Category | UTCI range (°C) |
|---|---|
| No thermal stress | +9 to +26 |
| Moderate heat stress | +26 to +32 |
| **Strong heat stress** | **+32 to +38** |
| **Very strong heat stress** | **+38 to +46** |
| **Extreme heat stress** | **> +46** |

(Cold categories exist in the scale but are irrelevant to a 37–40 °C study day and
are not used here.) The heat boundaries **+26, +32, +38, +46 °C** are the only
category cut-points used by M2 and M4.

**Authoritative source.** Bröde P., Fiala D., Błażejczyk K., Holmér I., Jendritzky
G., Kampmann B., Tinz B., Havenith G. (2012), *Deriving the operational procedure
for the Universal Thermal Climate Index (UTCI)*, International Journal of
Biometeorology 56:481–494; and the UTCI assessment scale published at www.utci.org
(ISB Commission 6 / COST Action 730). No boundary is invented or shifted.

## 3. Decision rule (frozen — inherited from Gate-1 §4, no invented threshold)

Judged on **decision stability per metric** across M1–M4 (M5 excluded), read in the two
families of §1.6 (THERMAL-INTENSITY vs EXPOSURE-DURATION):

- **ROBUST COMPARISON** — the sign of the Route A − Route B difference agrees across
  M1–M4 **and** is consistent across **both** metric families (§1.6) **and** is
  preserved across all justified perturbations (E-P1, E-P2, E-P4, E-P5, E-P6) **and**
  the category-based metrics (M2, M4) sit clear of a UTCI category boundary (guard band
  = the perturbation-ensemble interval, frozen in the perturbation spec).
- **NO ROBUST DIFFERENCE** — routes indistinguishable; or sign stable but magnitude
  within the modeled uncertainty interval; or legitimate metrics (M1–M4) disagree on
  ordering; **or the THERMAL-INTENSITY family and the EXPOSURE-DURATION family favour
  different routes (a genuine intensity/duration trade-off — never collapsed into a
  composite).**
- **ABSTAIN / NO EVIDENCE** — the sign reverses under ≥ 1 justified perturbation; OR
  an essential input is MISSING/unresolved; OR a category-based metric straddles a
  category boundary; OR spatial wind is shown decision-critical while unresolved
  (E-P3); OR the uncertainty interval spans the decision; OR the missing-pixel rule
  (§0) fires.

No composite score is formed after inspecting results. Statistical significance is
never conflated with practical/physiological relevance; **no physiological claim is
made at all** (Path B).
