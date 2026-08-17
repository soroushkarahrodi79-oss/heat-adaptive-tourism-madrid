"""
Single source of truth for every threshold used by the Phase 1 constraint-first
baseline. Nothing in build_classifications.py should hardcode a number that isn't
defined and justified here. See docs/PHASE1_METHOD.md for the full write-up.

Every threshold below is either:
  (a) an official published value (AEMET Meteoalerta), or
  (b) a standard, citable urban-planning heuristic (pedestrian catchment distance), or
  (c) an empirically-derived split of the pilot sample's own measured distribution,
      explicitly labelled as such (not disguised as a literature constant).
No threshold is a silently invented number.
"""

# --- METEOROLOGICAL HAZARD GATE: AEMET Meteoalerta max-temperature thresholds ----
# Renamed from the Phase 1 baseline's "hazard gate" in Phase 1.1
# (docs/PHASE1_1_BASELINE_HARDENING.md, Audit 1) purely for terminological
# precision - the underlying thresholds and logic are unchanged from Phase 1.
#
# Source: AEMET "Umbrales y niveles de aviso" v1 (2022-05-31), zone 722802
# "Metropolitana y Henares" (Comunidad de Madrid), which covers the city of Madrid
# including the study area. See data/raw/aemet_official_pdfs/
# AEMET_METEOALERTA_ANX1_Umbrales_y_niveles_de_aviso.pdf, table 3.12.
#
# EXPLICIT SCOPE STATEMENT: this gate classifies a REGIONAL, STATION-MEASURED
# AMBIENT AIR TEMPERATURE against an official METEOROLOGICAL WARNING SCALE. It is
# a meteorological hazard indicator, not a human thermal-comfort index, and its
# bands (LOW/ELEVATED/SEVERE/EXTREME) must never be read as, described as, or
# substituted for UTCI, PET, WBGT, or any other biometeorological comfort metric.
# AEMET's amarillo/naranja/rojo thresholds are civil-protection warning levels,
# calibrated for population-scale risk communication, not individual thermal
# sensation. See docs/PHASE1_METHOD.md, 'What this baseline does not claim'.
AEMET_MADRID_METRO_YELLOW_C = 36.0   # amarillo
AEMET_MADRID_METRO_ORANGE_C = 39.0   # naranja
AEMET_MADRID_METRO_RED_C = 42.0      # rojo

METEOROLOGICAL_HAZARD_STATES_ORDERED = ["LOW", "ELEVATED", "SEVERE", "EXTREME"]


def meteorological_hazard_state(temp_c: float) -> str:
    """Ambient-air-temperature METEOROLOGICAL HAZARD band from the official AEMET
    zone thresholds. This is NOT a thermal-comfort index: it does not account for
    radiation, wind, or humidity, and must not be read as UTCI/PET/WBGT. See
    docs/PHASE1_METHOD.md, 'What this baseline does not claim'.
    """
    if temp_c is None:
        return None
    if temp_c >= AEMET_MADRID_METRO_RED_C:
        return "EXTREME"
    if temp_c >= AEMET_MADRID_METRO_ORANGE_C:
        return "SEVERE"
    if temp_c >= AEMET_MADRID_METRO_YELLOW_C:
        return "ELEVATED"
    return "LOW"


# --- Exposure gate: on-site shade/vegetation proxy -------------------------------
# Proxy variable: count of real OSM natural=tree point nodes within a 50 m radius
# of the asset (see src/build_supporting_layers.py; data/interim/trees.geojson).
# Rationale for 50 m: approximates the immediate pedestrian standing/queueing area
# and its adjoining shade canopy, without reaching into a neighbouring, unrelated
# micro-environment (Madrid city blocks in this area run ~80-120 m per side).
EXPOSURE_BUFFER_M = 50

# Thresholds: EMPIRICAL tercile split of the tree_count_50m distribution actually
# observed across the 27 pilot assets (computed in build_classifications.py and
# printed/logged at run time). This is NOT a literature constant - it is a
# documented, reproducible split of this pilot's own measured data, chosen because
# no literature threshold exists for "tree count within 50 m of a tourism POI" as
# a shade-sufficiency criterion. Sensitivity to this choice is examined in
# docs/PHASE1_VALIDATION_REPORT.md.
EXPOSURE_METHOD_NOTE = (
    "Exposure state (LOW/MODERATE/HIGH regional-hazard-independent exposure, i.e. "
    "well-shaded / moderately-shaded / poor-shade) is assigned by tercile of the "
    "pilot sample's own tree_count_50m distribution across all 27 outdoor+indoor "
    "assets' outdoor surroundings. Indoor assets bypass this gate."
)

# Pilot-asset categories that were selected FROM a real OSM leisure=park/garden tag
# (see src/build_pilot_assets.py CURATED list) - i.e. the site is a real, officially
# mapped green-space polygon regardless of whether the separate OSM tree-point layer
# happens to have any natural=tree nodes inside it. Used as a documented override:
# a bottom-tercile tree count at one of these sites is treated as a known local gap
# in OSM's crowdsourced tree layer (verified case: Jardines de Cecilio Rodríguez has
# a real 32,225 sq m garden polygon and zero mapped tree points - a coverage gap, not
# evidence the site is unshaded) rather than being read as a genuinely unshaded site.
# This prevents a real data-completeness artefact from silently producing a wrong
# ("poor shade") classification for well-documented shaded gardens. See
# docs/PHASE1_VALIDATION_REPORT.md for the specific case list.
GREEN_LAND_USE_CATEGORIES = {"garden_outdoor", "park_general", "outdoor_pavilion_shaded"}

# --- Adaptation-resource INDICATOR: walkable access to water and transit --------
# DEMOTED from an exclusionary gate to an advisory/contextual indicator in
# Phase 1.1 Audit 3 (docs/PHASE1_1_BASELINE_HARDENING.md). Three independent
# real-data tests all found zero discriminatory power at any defensible
# distance threshold for this pilot's geography (a dense, well-served central
# Madrid tourist core): (1) all 27 Phase 1 pilot assets were GOOD/LIMITED,
# never POOR; (2) a threshold-sensitivity grid search found POOR only appears
# once thresholds are tightened to indefensible extremes (<=100 m transit,
# well below the ~250-400 m literature range below); (3) a 6-asset real bounded
# ring extension just beyond the study area, chosen specifically to be more
# peripheral, was STILL all GOOD/LIMITED, and removing the adaptation-based
# exclusion rule changed 0/18 of those rows. adaptation_state, water_dist_m and
# transit_dist_m are still computed and reported (real, useful practical
# context for a reader), but no longer feed a feasibility-EXCLUSION rule - see
# build_classifications.py:feasibility_decision(), which no longer branches on
# adaptation_state. This keeps real information visible without dressing up a
# non-discriminating input as if it were decision-relevant.
#
# 400 m is a standard pedestrian-catchment threshold in urban planning practice
# (approx. a 5-minute walk at ~4.8 km/h), widely used for transit-stop and amenity
# catchment analysis (e.g. Transit-Oriented Development guidelines; "15-minute
# city" walkable-amenity literature). Applied here to public transport access.
TRANSIT_WALK_THRESHOLD_M = 400

# Tightened relative to the general walking threshold for DRINKING WATER
# specifically, reflecting the acute hydration urgency during extreme heat
# emphasised in municipal/regional heat-health action plans (e.g. Comunidad de
# Madrid's heat-health plan messaging on frequent hydration) - approx. a 3-minute
# walk at the same pace.
WATER_WALK_THRESHOLD_M = 250


def adaptation_state(water_dist_m: float, transit_dist_m: float) -> str:
    if water_dist_m is None or transit_dist_m is None:
        return None
    water_ok = water_dist_m <= WATER_WALK_THRESHOLD_M
    transit_ok = transit_dist_m <= TRANSIT_WALK_THRESHOLD_M
    if water_ok and transit_ok:
        return "GOOD"
    if water_ok or transit_ok:
        return "LIMITED"
    return "POOR"


# --- Feasibility gate: constraint-first decision table ---------------------------
# See build_classifications.py:feasibility_decision() for the rule implementation.
# Documented here as a readable table for audit purposes.
#
# CHANGE LOG (Phase 1.1 Audit 3): the Phase 1 baseline had a rule 3 here
# ("hazard == SEVERE and adaptation == POOR -> NOT RECOMMENDED"). It is REMOVED
# in Phase 1.1: adaptation_state was demonstrated non-discriminatory (see the
# adaptation-resource INDICATOR comment above) and never fired this rule in any
# of the 81 Phase 1 rows or the 18 Audit 3 ring-extension rows, so deleting it
# changes zero historical classifications while removing a rule that dressed a
# non-decisive input up as if it were decision-relevant. water_dist_m and
# transit_dist_m remain in every output row as real, reported context.
FEASIBILITY_RULES_OUTDOOR = """
Outdoor-asset feasibility rules, applied in this order (first match wins):

1. hazard == EXTREME
   -> NOT RECOMMENDED
   reason: "regional air temperature at/above AEMET red-warning threshold
            ({red}C) for the Madrid Metropolitana zone; no on-site shade
            combination is treated as sufficient at this baseline evidence
            level"

2. hazard == SEVERE and exposure == HIGH (poor shade)
   -> NOT RECOMMENDED
   reason: "orange-level regional heat warning ({orange}-{red}C) combined with
            low measured tree density at this site (bottom tercile of pilot
            sample, i.e. poor on-site shade)"

3. hazard == SEVERE (remaining cases: exposure LOW/MODERATE)
   -> FEASIBLE WITH CONDITIONS
   reason: "orange-level regional heat warning; on-site shade is adequate but
            a precautionary hydration/shade-break recommendation applies
            (nearest water/transit distance reported for context, see
            water_dist_m / transit_dist_m / adaptation_state columns)"

4. hazard == ELEVATED and exposure == HIGH
   -> FEASIBLE WITH CONDITIONS
   reason: "yellow-level regional heat warning combined with low on-site
            tree density; hydration and shade-seeking recommended"

5. hazard == ELEVATED (remaining cases)
   -> FEASIBLE WITH CONDITIONS
   reason: "yellow-level regional heat warning; standard heat-season
            precaution recommended"

6. hazard == LOW and exposure == HIGH
   -> FEASIBLE WITH CONDITIONS
   reason: "regional hazard modest but on-site tree density is in the lowest
            tercile of the pilot sample (poor shade); precautionary flag only"

7. hazard == LOW (remaining cases)
   -> FEASIBLE
   reason: "regional hazard below yellow-warning threshold and on-site shade
            is average-to-good for the pilot sample"
""".format(
    red=AEMET_MADRID_METRO_RED_C,
    orange=AEMET_MADRID_METRO_ORANGE_C,
)

FEASIBILITY_RULES_INDOOR = """
Indoor-asset feasibility rules (exposure/adaptation gates bypassed - the asset
itself is the shelter):

1. hazard in {{SEVERE, EXTREME}}
   -> FEASIBLE WITH CONDITIONS
   reason: "indoor visit is assumed thermally buffered from the outdoor hazard,
            but air-conditioning operational status is not verified in the
            source data (Madrid Open Data museums layer does not state A/C
            status - see docs/DATA_SOURCE_INVENTORY.csv), and outdoor
            approach/queueing exposure at this regional hazard level is a
            real residual risk not captured by this row"

2. hazard in {{LOW, ELEVATED}}
   -> FEASIBLE
   reason: "indoor visit assumed thermally buffered; regional hazard is not
            severe enough to flag residual approach-exposure risk"
"""

METHOD_VERSION = "phase1.1-baseline-hardening-v1.1"
