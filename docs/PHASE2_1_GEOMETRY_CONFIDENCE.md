# PHASE2_1_GEOMETRY_CONFIDENCE.md — HATI-Madrid Phase 2.1, Audit 2

Version 1.0 · 2026-08-17. **This is a confidence audit, not a
reconstruction.** No attempt is made to infer the exact 2023 canopy state.
The Phase 2 LiDAR CDSM is not modified anywhere in this document or its
underlying data.

---

## Why this audit exists

Phase 2's vegetation-height model (CDSM) derives from PNOA-LiDAR's first
coverage, nominally captured 2008–2015 (`docs/PHASE2_INPUT_FEASIBILITY.md`)
— up to 15 years before the 2023-08-21 heat episode. Trees grow, are
pruned, are removed, and are planted over such a window. This audit checks,
for a targeted set of decision-relevant assets, whether independent newer
evidence already sitting in this project's own data (Phase 1.2's three
vegetation proxies) is consistent with what the LiDAR CDSM shows.

## Method

**Selected assets (8, per the task's "approximately 6-8, targeted"
instruction):** A20, A21, A23, A24, A25, A27 (all `park_garden` morphology,
the sites where vegetation most directly drives Tmrt) plus A17 and A19
(Phase 1.2 proxy-sensitive, non-park morphologies, included for contrast).

**Independent newer sources compared** (all already acquired in Phase 1.2,
none re-fetched for this audit):

| Source | Vintage | What it measures |
|---|---|---|
| Madrid official tree inventory (P1) | Live, ~2025–2026 | Real per-tree point locations (municipal, non-crowdsourced) |
| Green-polygon coverage (P3) | OSM, 2026 snapshot | % of a buffer covered by real park/garden polygons |
| Copernicus HRL Tree Cover Density (P2) | 2018 | Real satellite-derived canopy-density %, an intermediate-vintage cross-check (newer than the LiDAR, older than the episode) |

**Buffer:** the same pre-registered 10 m circular buffer used throughout
Phase 2 (`src/phase2_prereg.py` `PRIMARY_BUFFER_M`) — reused for
consistency, not re-chosen.

**Classification rule** (fixed before inspecting the resulting mix of
labels): LiDAR is judged to "see vegetation" if mean CDSM height in the
buffer exceeds 1.0 m (a real canopy signal, not sensor noise). Newer
evidence is judged to "confirm vegetation" per source if: Madrid tree count
> 5, green-polygon coverage > 30%, or Copernicus TCD > 20% — each an
independent yes/no signal, and an asset is counted as newer-confirmed if
**at least 2 of the 3** newer sources agree.

| LiDAR sees vegetation? | ≥2 newer sources confirm? | Label |
|---|---|---|
| Yes | Yes | **REPRESENTATIVE** |
| No | Yes | **POSSIBLY STALE** |
| Yes | No | **PARTIALLY REPRESENTATIVE** |
| No | No | **PARTIALLY REPRESENTATIVE** (consistent low-vegetation reading) |

## Results

| Asset | LiDAR CDSM mean (m) | Madrid trees (10 m) | Green coverage % | Copernicus TCD % | Confidence |
|---|---:|---:|---:|---:|---|
| A17 Estatua de Goya | 3.38 | 1 | 55.5 | 71.8 | REPRESENTATIVE |
| A19 Real Observatorio | 6.27 | 0 | 100.0 | 28.0 | REPRESENTATIVE |
| A20 Parque del Retiro | 9.16 | 7 | 100.0 | 38.0 | REPRESENTATIVE |
| A21 Real Jardín Botánico | 7.04 | 0 | 100.0 | 71.2 | REPRESENTATIVE |
| **A23 Jardines de Cecilio Rodríguez** | **0.62** | 8 | 100.0 | 49.2 | **POSSIBLY STALE** |
| **A24 La Rosaleda** | **0.10** | 0 | 100.0 | 26.2 | **POSSIBLY STALE** |
| A25 Jardín del Parterre | 0.08 | 0 | 100.0 | 12.0 | PARTIALLY REPRESENTATIVE |
| **A27 Jardines del Arquitecto Herrero Palacios** | **0.88** | 0 | 100.0 | 65.5 | **POSSIBLY STALE** |

**4 REPRESENTATIVE, 3 POSSIBLY STALE, 1 PARTIALLY REPRESENTATIVE** (of 8
audited; 6 not audited — see Coverage note below).

## Interpretation

Three of the six audited **park/garden** assets — exactly the morphology
where vegetation matters most for Tmrt — show LiDAR canopy heights near
zero (0.10–0.88 m mean) while at least two of three independent, newer
sources each indicate real, substantial vegetation nearby (green-polygon
coverage is 100% at all three; Copernicus TCD 26–66%; Madrid's own tree
inventory finds 8 real trees within 10 m of A23 specifically). This is the
clearest, most concrete evidence available in this project that the
LiDAR-derived CDSM likely **understates** current canopy at these three
specific gardens — plausibly because real canopy has grown in, or these
gardens were replanted or matured, in the years since the ~2008–2015
capture.

**Directional implication (not quantified, per the task's "confidence
audit, not reconstruction" instruction):** if these three gardens'
true 2023 canopy was denser than the LiDAR CDSM represents, SOLWEIG's Tmrt/
UTCI at these sites is more likely to be an **overestimate** of actual
2023 heat exposure (less real shade was modelled than may actually exist)
than an underestimate. This is stated as a directional hypothesis
consistent with the evidence, not as a corrected number.

**A24 (La Rosaleda) is flagged from two independent audits simultaneously**:
solar-forcing sensitivity (Audit 1) already found it the one asset whose
decision flips under the real-satellite scenario at 18:00, and this audit
independently flags its geometry as POSSIBLY STALE. This is the strongest
single candidate in this phase for a genuinely fragile, decision-critical
result — carried into Audit 3 as UNSTABLE.

**No systematic, across-the-board geometry failure was found.** 4 of 8
audited assets (including both non-park contrast assets, A17 and A19, and
half the park/garden sample, A20/A21) are REPRESENTATIVE — the LiDAR
geometry agrees well with newer evidence at these sites. The staleness
pattern is real but concentrated, not universal.

## Coverage note (stated limitation of this audit itself)

Only 8 of the pilot's 14 outdoor assets were audited, per the task's
explicit "targeted... approximately 6-8" scope instruction — this was a
deliberate, bounded sample, not an attempt at full coverage. The six
unaudited outdoor assets (A14, A15, A16, A18, A22, A26 — predominantly
`plaza_hardscape`/`attraction_exterior` morphologies with little on-site
vegetation to begin with, per Phase 1's own exposure classification) are
**not asserted geometry-confirmed** by this audit; they are carried into
Audit 3 with an explicit "not part of the geometry audit sample" note
rather than a default REPRESENTATIVE assumption.
