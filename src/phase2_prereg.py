"""
PHASE 2 PRE-REGISTRATION — written and committed BEFORE any Tmrt/UTCI raster
is inspected or any asset-level statistic is computed. Nothing here may be
edited after results are seen (see docs/PHASE2_VALIDATION_REPORT.md, which
states the wall-clock order of operations, mirroring the Phase 1.2 practice
in src/shade_proxy_prereg.py).

=== ASSET SELECTION ===

Representative subset (8 assets, per the task's "approximately 6-8" spanning
all 4 morphologies, prioritising Phase 1.2's proxy-sensitive assets):
  plaza_hardscape:      A14 (Puerta de Alcalá), A16 (Fuente de Neptuno),
                         A18 (Palacio de Cibeles)
  street_corridor:      A17 (Estatua de Goya)  [only street_corridor asset
                         in the pilot - see docs/PHASE1_2 morphology table]
  park_garden:          A21 (Real Jardín Botánico), A25 (Jardín del Parterre)
  attraction_exterior:  A19 (Real Observatorio), A26 (Monumento a Alfonso XII)
These 8 are exactly the 8 outdoor assets flagged proxy-sensitive in Phase 1.2
(docs/PHASE1_2_SHADE_EVIDENCE_GATE.md S5) - selected for that reason, not
cherry-picked afterward for a favourable physical-model result.

Full set: because SOLWEIG's computational cost is dominated by the one-time
per-raster shadow/SVF precomputation and per-timestep Tmrt/UTCI grid
calculation (both independent of how many point locations are later
queried), extracting statistics for all 14 outdoor assets from the same
already-computed rasters is genuinely free - so the full 14-asset set IS
reported throughout, per the task's "preserve... where computationally
trivial" instruction. The 8 above are the ones narratively highlighted.

=== ASSET EXPOSURE SPATIAL STATISTIC (decided in advance) ===

PRIMARY statistic: MEAN Tmrt / UTCI within a 10 m circular buffer around
each asset's representative point (data/processed/pilot_assets.csv
latitude/longitude - the same real point geometry used throughout Phase 1/
1.1/1.2).

Rationale for 10 m, not chosen after seeing which buffer flatters agreement:
  - Tmrt/UTCI at 2.5 m raster resolution has fine spatial structure driven
    directly by shade-edge geometry (a shadow boundary can fall within a few
    metres) - this is precisely the spatial detail a physical model is
    expected to reveal that a 50 m tree-count buffer (Phase 1/1.1/1.2's
    proxy convention) cannot. Reusing the proxies' 50 m buffer here would
    blend sun and shade pixels together and erase the very differentiation
    this phase exists to test for.
  - 10 m approximates the immediate pedestrian standing footprint at a
    monument, bench, or garden path - smaller than a full plaza but larger
    than a single pixel, so the statistic is not overly sensitive to exactly
    where within that footprint the asset's point was digitised.

SENSITIVITY (reported, not the primary/gate statistic): centroid (nearest
single pixel) and the buffer's 90th-percentile value (worst-case exposure
within the same 10 m footprint) are also extracted for every asset and
reported alongside the mean, exactly as the task's "report more than one
statistic as sensitivity analysis" instructs.

=== SOLWEIG CONFIGURATION (decided in advance) ===

Working resolution: 2.5 m (see docs/PHASE2_INPUT_FEASIBILITY.md), matching
the native resolution of the building/vegetation normalized height models -
the two geometrically decisive inputs for shadow-casting.

Ground-cover/land-cover: SOLWEIG's package default (no custom land_cover
grid supplied) - the land_cover input is documented as optional, and no
open, study-area-specific land-cover classification at matching resolution
was acquired in this bounded spike (would require additional acquisition
beyond what Step 0 judged necessary to avoid the blocking-input STOP
condition). This is a documented simplification, not a silent one - see
docs/PHASE2_INPUT_FEASIBILITY.md.

Wind: single station-scale value per timestep (real Barajas hourly wind
speed), applied uniformly across the whole raster. No CFD/URock, per the
task's explicit prohibition. Street-level wind heterogeneity is NOT
resolved - documented as a first-class limitation, not a silent
simplification.

=== COMPARISON THRESHOLDS ===

Every threshold used to translate Tmrt/UTCI into a hazard/exposure/
feasibility_state for the Phase 1-vs-Phase 2 comparison is the OFFICIAL
UTCI thermal-stress category system (Bröde et al. 2012, the standard,
published UTCI category boundaries - see docs/PHASE2_UTCI_METHOD.md) - not
a value invented for this project, and not re-tuned after seeing results.
"""

REPRESENTATIVE_ASSET_IDS = ["A14", "A16", "A18", "A17", "A21", "A25", "A19", "A26"]
PRIMARY_BUFFER_M = 10
SENSITIVITY_PERCENTILE = 90
