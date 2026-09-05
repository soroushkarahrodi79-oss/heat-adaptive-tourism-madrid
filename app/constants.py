"""Fixed presentation constants for the HATI-Madrid decision cockpit.

Everything here is *presentation* metadata: the study date/timestamps that
the science was computed for, the visual channel palette locked in
PHASE4_0_VISUAL_SEMANTICS.md, and fixed token -> plain-language lookups
transcribed verbatim from PHASE4_0_INTERACTION_SPEC.md / the handoff,
plus the Phase 4.2 interface copy (bottom half of the file).

No value here is a scientific result, a score, a ranking, or a threshold.
The token maps only *translate* locked machine tokens into human copy; they
never decide anything.
"""

# ── Fixed temporal frame (NOT live; a single historical heat episode) ──────
STUDY_DATE = "2023-08-21"
TIMESTAMPS = ("12:00", "15:00", "18:00")           # the only 3 valid timestamps
NOT_LIVE_CAPTION = (
    "3 modelled timestamps for one historical heat episode — "
    "not live or forecast data"
)

# ── decision_state → fill colour (categorical; Visual Semantics §3) ────────
# Rust = avoid outdoor; teal = indoor refuge. Pure red/green reserved.
DECISION_STATE_COLOR = {
    "AVOID_PROLONGED_OUTDOOR_EXPOSURE": "#B5502E",   # muted rust / terracotta
    "INDOOR_REFUGE": "#2E6B6B",                       # muted slate teal
}
DECISION_STATE_LABEL = {
    "AVOID_PROLONGED_OUTDOOR_EXPOSURE": "Avoid prolonged outdoor exposure",
    "INDOOR_REFUGE": "Indoor refuge",
}

# ── thermal_state → glyph + label (Visual Semantics §2) ────────────────────
# Glyph is an independent channel from decision colour, never inferred from it.
THERMAL_STATE_GLYPH = {
    "VERY_STRONG_HEAT_STRESS": "☀",      # heat-stress pictogram
    "INDOOR_NOT_MODELLED": "⌂",          # indoor pictogram
}
THERMAL_STATE_LABEL = {
    "VERY_STRONG_HEAT_STRESS": "Very strong heat stress (modelled)",
    "INDOOR_NOT_MODELLED": "Indoor — thermal stress not physically modelled",
}

# ── decision_confidence → ring style + plain-language gloss (Vis Sem §6) ────
# ring style is drawn on the map marker itself (never tooltip-only).
CONFIDENCE_RING = {          # maps to a CSS class suffix on ConfidenceRingGlyph
    "ROBUST": "solid",
    "BOUNDARY": "dashed",
    "UNSTABLE": "dotted",
    "INDOOR_BYPASS": "none",
}
CONFIDENCE_GLOSS = {
    "ROBUST": "This decision held under every tested scenario variation.",
    "BOUNDARY": "This decision is close to a threshold; some tested "
                "variations would flip it.",
    "UNSTABLE": "This decision changed under tested variations — treat as "
                "uncertain.",
    "INDOOR_BYPASS": "Confidence categories don't apply — this asset's "
                     "thermal state is not physically modelled (indoor).",
}
CONFIDENCE_SHORT = {
    "ROBUST": "Robust",
    "BOUNDARY": "Boundary",
    "UNSTABLE": "Unstable",
    "INDOOR_BYPASS": "Indoor bypass",
}

# A24 @ 18:00 — the one canonical UNSTABLE worked example (handoff §3/§6).
# Rendered distinctly from ordinary BOUNDARY rows, never softened.
A24_UNSTABLE_ASSET = "A24"
A24_UNSTABLE_TIMESTAMP = "18:00"
A24_UNSTABLE_ANNOTATION = (
    "Genuine solar-boundary case, not a data artefact. This asset's decision "
    "flips under the tested solar-forcing envelope; the instability is "
    "irreducible with the modelled inputs, not a bug in the data."
)

# ── evidence_confidence → opacity channel (Visual Semantics §2) ────────────
EVIDENCE_OPACITY = {"HIGH": 1.0, "MODERATE": 0.66, "LOW": 0.4}
EVIDENCE_NOTE = ("Weakest-link of opening-hours evidence and thermal "
                 "evidence — a supporting fact, separate from decision "
                 "confidence.")

# ── exclusion_reason → plain-language translation (Interaction Spec §4) ─────
# Every token that can appear anywhere in the 7 CSVs has an entry here.
EXCLUSION_TRANSLATIONS = {
    "CLOSED_AT_TIMESTAMP":
        "Closed at this time, based on documented hours.",
    "ACCESSIBILITY_CONSTRAINT":
        "Outside the straight-line search radius from the source.",
    "THERMAL_LIMIT_EXCEEDED":
        "Modelled heat stress here exceeds the tolerable limit.",
    "INSUFFICIENT_EVIDENCE":
        "Not enough reliable data to support a decision.",
    "NO_MEANINGFUL_THERMAL_IMPROVEMENT":
        "Would not be meaningfully cooler than the source "
        "(below the 0.8 °C pre-registered margin).",
    "OUTDOOR_EXPOSURE_TOO_HIGH":
        "Outdoor candidate has a higher recorded UTCI than the source.",
}

# ── experience_type → readable label (display only) ─────────────────────────
EXPERIENCE_TYPE_LABEL = {
    "green_outdoor": "Green outdoor space",
    "indoor_cultural": "Indoor cultural",
    "indoor_green_refuge": "Indoor green refuge",
    "outdoor_monument": "Outdoor monument",
    "shaded_outdoor": "Shaded outdoor",
    "transit_refuge": "Transit refuge",
}

# ── tourism_category → readable label (display only) ──────────────────────
TOURISM_CATEGORY_LABEL = {
    "museum_indoor": "Museum",
    "transit_hub": "Transit hub",
    "transit_hub_green": "Transit hub · green",
    "monument_outdoor": "Monument",
    "park_general": "Park",
    "garden_outdoor": "Garden",
    "outdoor_pavilion_shaded": "Shaded pavilion",
    "outdoor_attraction_mixed_shade": "Attraction · mixed shade",
}

# ── Limitations disclosure copy (handoff §9; Interaction Spec §8) ───────────
# Tier 1: one context-sensitive strip string per view context.
TIER1_LIMITATIONS = {
    "map": "Thermal values are modelled (SOLWEIG/UTCI), not field-measured.",
    "asset": "Opening hours are 2026-documented values applied to the "
             "2023 study date.",
    "alternatives": "Distances are straight-line; walking-route heat "
                    "exposure is not modelled.",
}

# Tier 2: the full permanent-limitations list, verbatim in spirit with the
# handoff §9 six items plus the opening-hours temporal-alignment caveat.
TIER2_LIMITATIONS = [
    "No field validation of modelled Tmrt/UTCI exists anywhere in this "
    "project — all thermal values are model-derived (SOLWEIG/UTCI).",
    "A24 (La Rosaleda) @ 18:00 is a genuine, irreducible solar-boundary "
    "UNSTABLE case — its decision flips under the tested solar envelope and "
    "this is a real result, not a data artefact.",
    "Tested uncertainty covers only solar forcing and 2-asset geometry — "
    "not humidity, wind, or model-structural uncertainty.",
    "Accessibility is straight-line distance only; walking-route heat "
    "exposure is not modelled.",
    "No behavioural claim is made — this is screening only, not a prediction "
    "of which option a tourist will choose.",
    "Indoor refuge assumes thermal buffering without verified air-"
    "conditioning or queue-exposure modelling.",
    "Opening-hours temporal alignment: opening hours are 2026-documented "
    "values applied retrospectively to the 2023-08-21 study date, and are "
    "not verified as fact for 2023.",
]
TIER2_SOURCE_NOTE = ("Full uncertainty derivation: "
                     "docs/PHASE2_2_DECISION_UNCERTAINTY.md.")

# ── View identifiers (interface state only, stored in dcc.Store) ───────────
VIEW_MAP = "map"              # View 1 only (no asset selected)
VIEW_ASSET = "asset"          # View 2 panel open
VIEW_ALTERNATIVES = "alternatives"   # View 3 open


# ═══════════════════════════════════════════════════════════════════════════
# Phase 4.2 — additional presentation copy.
# Everything below is fixed user-facing English or a token→copy lookup.
# No value below is a scientific result, threshold, score, weight or ranking.
# ═══════════════════════════════════════════════════════════════════════════

PRODUCT_NAME = "HATI-Madrid"
PRODUCT_TAGLINE = "Spatial Decision Replay"
PILOT_LABEL = "Madrid pilot · Prado–Retiro–Atocha"
STUDY_DATE_HUMAN = "21 Aug 2023"

# ── Sort keys allowed in View 3 (display organisation, never ranking) ──────
# `name` is added in 4.2: alphabetical order is the most obviously
# non-evaluative order available, and is the natural default for a reader
# looking a specific place up.
SORT_KEYS = {
    "distance": "Distance (straight-line)",
    "name": "Name (A–Z)",
    "indoor_outdoor": "Indoor / outdoor",
    "experience_type": "Experience type",
}

NOT_RANKING_NOTE = (
    "These are the candidates that survived every screening gate, shown on "
    "their own terms. Sorting changes reading order only, not ranking — no "
    "candidate is preferred over another here."
)

# ── Map legend / symbol explanation ────────────────────────────────────────
LEGEND_COMPACT_NOTE = "Colour, ring and glyph are three separate facts."
LEGEND_OPEN_LABEL = "Explain map symbols"
LEGEND_TITLE = "What the map symbols mean"
LEGEND_INTRO = (
    "Each marker carries four independent facts at once. None of them is "
    "derived from another, so they must be read separately."
)
LEGEND_CHANNELS = [
    ("Fill colour", "the decision", "decision_state"),
    ("Ring style", "stability under tested variation", "decision_confidence"),
    ("Inner glyph", "the modelled thermal condition", "thermal_state"),
    ("Dimming", "whether the asset is open at this timestamp", "is_open"),
]
LEGEND_SELECTION_NOTE = (
    "A charcoal halo marks the asset you have selected. It is an interface "
    "state, not a fifth piece of data."
)
LEGEND_TIER1 = TIER1_LIMITATIONS["map"]

MAP_HINT_NO_SELECTION = "Select an asset on the map to see its decision."
MAP_TILE_FALLBACK = (
    "Basemap tiles are unavailable. Asset positions and every screening "
    "result remain available from the pinned local snapshot."
)

# ── Command bar ────────────────────────────────────────────────────────────
TIMESTAMP_LABEL = "Timestamp"
SCENARIO_MENU_LABEL = "Scenario"
SCENARIO_MENU_TITLE = "Pre-computed scenarios"
SCENARIO_MENU_NOTE = (
    "Eight scenarios were computed in Phase 3. Choosing one sets its source "
    "asset and timestamp; nothing is recalculated."
)
ASSET_PICKER_LABEL = "Find asset"
ASSET_PICKER_PLACEHOLDER = "Search 27 assets…"
LIMITATIONS_LABEL = "Limitations"

RECOMMENDATION_MENU_GLOSS = {
    "ALTERNATIVES_FOUND": "defensible alternatives",
    "NO_DEFENSIBLE_ALTERNATIVE": "no defensible alternative",
}

# ── Asset decision panel ───────────────────────────────────────────────────
PANEL_DECISION_LABEL = "Decision"
PANEL_CONFIDENCE_LABEL = "Decision confidence"
PANEL_THERMAL_LABEL = "Thermal condition"
PANEL_EVIDENCE_LABEL = "Evidence confidence"
PANEL_TRACE_LABEL = "Recorded asset state and sources"
PANEL_LIMITATIONS_LABEL = "Relevant limitations"

MODEL_PROVENANCE_NOTE = (
    "Model-derived (SOLWEIG/UTCI). Not field-measured — no field validation "
    "of modelled Tmrt/UTCI exists in this project."
)
INDOOR_NOT_MODELLED_NOTE = (
    "Not physically modelled for indoor assets. The indoor-refuge decision "
    "assumes thermal buffering; it is not a measured indoor temperature."
)
ENVELOPE_NOTE = (
    "The envelope is the range this asset's UTCI took across the tested "
    "solar-forcing variations, not a measurement uncertainty."
)

CONFIDENCE_NOT_SEVERITY_NOTE = (
    "Decision confidence describes how stable the decision is under tested "
    "variation. It is not a statement about physical danger."
)

# Asset-panel exclusion block (the token is context-free, i.e. it says where
# this asset gets excluded when it appears as somebody else's candidate).
PANEL_EXCLUSION_LABEL = "Where this asset is excluded as an alternative"
PANEL_EXCLUSION_NOTE = (
    "This is the context-free screening reason. A scenario may record an "
    "earlier failure, such as its reach constraint. See that scenario record."
)

# ── Alternatives view ──────────────────────────────────────────────────────
ALT_VIEW_KICKER = "Defensible alternatives"
ALT_CTA = "Explore defensible alternatives"
ALT_CTA_NODEF = "See the full finding"
ALT_CTA_UNAVAILABLE = (
    "No candidate screening was pre-computed for this asset at this "
    "timestamp — it is not a scenario source."
)
ALT_SORT_LABEL = "Sort by"
ALT_EXCLUDED_TITLE = "nearby options were excluded — show why"
ALT_EXCLUDED_NOTE = (
    "Screening applies the gates in a fixed order and records the first one "
    "a candidate fails, so each option appears under one reason only."
)
ALT_DISTANCE_NOTE = (
    "Distances are straight-line from the source. Walking-route heat "
    "exposure is not modelled."
)

# ── Reach (accessibility-radius) sensitivity ───────────────────────────────
RADIUS_TITLE = "Reach sensitivity (pre-registered)"
RADIUS_NOTE = (
    "Pre-registered sensitivity values recorded in Phase 3, shown as "
    "evidence. The reach constraint for this scenario is fixed and is not "
    "adjustable in this interface."
)
RADIUS_STABLE = (
    "The screening outcome category is the same at 500 m, 800 m and 1200 m."
)
RADIUS_UNSTABLE = (
    "The screening outcome category is not the same across 500–1200 m: the "
    "surviving set here depends on the reach constraint."
)

# ── Baseline comparison ────────────────────────────────────────────────────
BASELINE_LABEL = "Compare with conventional baseline"
BASELINE_WHAT = (
    "The conventional baseline picks the nearest option that is open. It "
    "applies no thermal or evidence gate."
)
BASELINE_PRECOMPUTED = (
    "Pre-computed in Phase 3 and read here unchanged — not recalculated."
)
BASELINE_NEUTRALITY = (
    "The two approaches answer different questions and neither is labelled "
    "preferable here."
)

# ── S8 / NO_DEFENSIBLE_ALTERNATIVE ─────────────────────────────────────────
NODEF_KICKER = "Screening result"
NODEF_HEADLINE = "No defensible alternative found."
NODEF_SUBLINE = (
    "This is the screening result, not a failed search. Under the specified "
    "source, timestamp and reach constraint, no candidate satisfies all "
    "gates."
)
NODEF_METHOD = (
    "No candidate survived the recorded constraints. Exclusion counts below "
    "describe the first recorded failure across the full candidate universe."
)
NODEF_BREAKDOWN_TITLE = "Why candidates were excluded"
NODEF_BREAKDOWN_NOTE = (
    "Counts of the locked exclusion reason recorded for each candidate."
)
NODEF_FULL_LIST_TITLE = "Every candidate that was evaluated"

# ── Empty / unavailable states ─────────────────────────────────────────────
EMPTY_ASSET_NOT_FOUND = "Asset record unavailable for this identifier."
EMPTY_SCENARIO_NOT_FOUND = "Scenario record unavailable for this identifier."
EMPTY_NO_BASELINE = (
    "No pre-computed baseline comparison exists for this scenario."
)

# ── Accessible names ───────────────────────────────────────────────────────
ARIA_WORKSPACE = "Decision workspace: map and contextual panel"
ARIA_MAP_REGION = "Map of the 27 pilot assets"
ARIA_PANEL_REGION = "Selected asset decision panel"
ARIA_COMMAND_BAR = "Study controls"
ARIA_TIMESTAMP_GROUP = "Modelled timestamp"
ARIA_OPEN_AT = "Open at this timestamp"
ARIA_CLOSED_AT = "Closed at this timestamp"
