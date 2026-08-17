"""Fixed presentation constants for the HATI-Madrid Phase 4.1 MVP.

Everything here is *presentation* metadata: the study date/timestamps that
the science was computed for, the visual channel palette locked in
PHASE4_0_VISUAL_SEMANTICS.md, and fixed token -> plain-language lookups
transcribed verbatim from PHASE4_0_INTERACTION_SPEC.md / the handoff.

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
        "Another hot outdoor location — doesn't solve the heat problem.",
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

# ── Sort keys allowed in View 3 (organisation, never ranking) ──────────────
SORT_KEYS = {
    "distance": "Distance (straight-line)",
    "indoor_outdoor": "Indoor / outdoor",
    "experience_type": "Experience type",
}
