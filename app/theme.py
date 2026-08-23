"""Design tokens for the HATI-Madrid Spatial Decision Cockpit (Phase 4.2).

Single source of truth for colour, spacing, radius, elevation, motion and
type. Consumed in three places:

  * ``CSS_VARIABLES`` -> emitted into a ``<style>`` block on ``:root`` so the
    stylesheet and the Python components can never drift apart;
  * ``mantine_theme()`` -> the ``dmc.MantineProvider`` theme object;
  * component modules -> import the named constants instead of literals.

NOTHING here is a scientific value. The two decision hues are re-exported
from :mod:`app.constants`, which holds the locked Phase 4.0 visual-semantics
palette; this module must never redefine them.
"""
from __future__ import annotations

from . import constants as C

# ── Foundation ─────────────────────────────────────────────────────────────
BG = "#EFEBE2"
SURFACE = "#FBFAF6"
SURFACE_RAISED = "#FFFFFF"
SURFACE_MUTED = "#F2EEE5"
SURFACE_INVERSE = "#2B2B31"
BORDER_SUBTLE = "#E4DED2"
BORDER_STRONG = "#CBC3B4"
TEXT_PRIMARY = "#23232A"        # 14.9:1 on surface
TEXT_SECONDARY = "#5E594F"      # 6.7:1 on surface
TEXT_TERTIARY = "#6F6A61"       # 5.1:1 on surface, 4.5:1 on bg
TEXT_INVERSE = "#F7F5EF"        # 12.9:1 on inverse

# ── Semantic (deliberately scarce) ─────────────────────────────────────────
# decision_state hues are LOCKED in Phase 4.0 visual semantics.
DECISION_RUST = C.DECISION_STATE_COLOR["AVOID_PROLONGED_OUTDOOR_EXPOSURE"]
DECISION_TEAL = C.DECISION_STATE_COLOR["INDOOR_REFUGE"]
DECISION_UNKNOWN = "#8A8A8A"    # neutral fill for a decision_state the
                                # palette does not know; belongs to no channel
CONFIDENCE_INK = "#3A3A42"      # ring stroke, all confidence levels
EVIDENCE_INK = "#5E594F"        # evidence chip only
UNCERTAINTY_ACCENT = "#795C26"  # UNSTABLE rule + A24 note; NOT an alarm colour
VERDICT_INK = "#2B2B31"         # NO_DEFENSIBLE_ALTERNATIVE
EXCLUDED_INK = "#6B665E"        # 5.4:1 on surface
SELECTION = "#23232A"           # interface state, never a data channel
FOCUS = "#1F5F7A"
DISABLED_FG = "#8B857A"

# ── Scales ─────────────────────────────────────────────────────────────────
SPACE = {"2xs": 2, "xs": 4, "s": 6, "sm": 8, "md": 12, "lg": 16,
         "xl": 20, "2xl": 24, "3xl": 32, "4xl": 40}
RADIUS = {"sm": 4, "md": 6, "lg": 10, "pill": 999}
SHADOW = {
    "s1": "0 1px 2px rgba(35,35,42,.06)",
    "s2": "0 2px 8px rgba(35,35,42,.10)",
    "s3": "0 8px 28px rgba(35,35,42,.14)",
}
MOTION = {"fast": "120ms", "base": "160ms", "slow": "200ms",
          "ease": "cubic-bezier(.2,0,.2,1)"}
CONTROL_H = {"sm": 28, "md": 34, "lg": 40}

# ── Type ───────────────────────────────────────────────────────────────────
FONT_SERIF = ('"Iowan Old Style","Palatino Linotype",Palatino,'
              '"Book Antiqua",Georgia,serif')
FONT_SANS = ('system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,'
             'Arial,sans-serif')
FONT_MONO = ('"SF Mono","Cascadia Code",Consolas,"Liberation Mono",monospace')
# The whole scale. Nothing outside it.
TYPE_SCALE = (11, 12.5, 14, 17, 20, 22)

# ── Geometry of the map marker (one definition, used by CSS and Python) ────
MARKER_SIZE = 28
MARKER_SIZE_SELECTED = 34
MARKER_HIT = 40                 # DivMarker iconSize; keeps the target >= 34px

# ── Panel widths (fluid; CSS owns the clamp, Python owns the class names) ──
PANEL_CLASS_ASSET = "cockpit-panel--asset"
PANEL_CLASS_ALTERNATIVES = "cockpit-panel--alternatives"


def css_variables() -> str:
    """The token layer as a ``:root`` declaration block."""
    rows = {
        "--bg": BG,
        "--surface": SURFACE,
        "--surface-raised": SURFACE_RAISED,
        "--surface-muted": SURFACE_MUTED,
        "--surface-inverse": SURFACE_INVERSE,
        "--border-subtle": BORDER_SUBTLE,
        "--border-strong": BORDER_STRONG,
        "--text-primary": TEXT_PRIMARY,
        "--text-secondary": TEXT_SECONDARY,
        "--text-tertiary": TEXT_TERTIARY,
        "--text-inverse": TEXT_INVERSE,
        "--decision-rust": DECISION_RUST,
        "--decision-teal": DECISION_TEAL,
        "--confidence-ink": CONFIDENCE_INK,
        "--evidence-ink": EVIDENCE_INK,
        "--uncertainty-accent": UNCERTAINTY_ACCENT,
        "--verdict-ink": VERDICT_INK,
        "--excluded-ink": EXCLUDED_INK,
        "--selection": SELECTION,
        "--focus": FOCUS,
        "--disabled-fg": DISABLED_FG,
        "--serif": FONT_SERIF,
        "--sans": FONT_SANS,
        "--mono": FONT_MONO,
        "--marker-size": f"{MARKER_SIZE}px",
        "--marker-size-selected": f"{MARKER_SIZE_SELECTED}px",
    }
    rows.update({f"--space-{k}": f"{v}px" for k, v in SPACE.items()})
    rows.update({f"--radius-{k}": f"{v}px" for k, v in RADIUS.items()})
    rows.update({f"--shadow-{k}": v for k, v in SHADOW.items()})
    rows.update({f"--motion-{k}": v for k, v in MOTION.items()})
    rows.update({f"--control-h-{k}": f"{v}px" for k, v in CONTROL_H.items()})
    body = "\n".join(f"  {k}: {v};" for k, v in rows.items())
    return f":root {{\n{body}\n}}"


def mantine_theme() -> dict:
    """Theme object for ``dmc.MantineProvider``.

    Mantine's own palette is neutralised: the primary colour ramp is the
    project's charcoal, so no stock Mantine blue can appear anywhere.
    """
    charcoal = ["#F3F2EF", "#E4E2DC", "#C9C6BD", "#ADA89C", "#8B857A",
                "#6F6A61", "#5E594F", "#43424A", "#33333A", SURFACE_INVERSE]
    return {
        "fontFamily": FONT_SANS,
        "fontFamilyMonospace": FONT_MONO,
        "headings": {"fontFamily": FONT_SERIF, "fontWeight": "600"},
        "primaryColor": "hati",
        "primaryShade": 9,
        "defaultRadius": "md",
        "white": SURFACE,
        "black": TEXT_PRIMARY,
        "colors": {"hati": charcoal},
        "radius": {k: f"{v}px" for k, v in RADIUS.items() if k != "pill"},
        "spacing": {"xs": "4px", "sm": "8px", "md": "12px",
                    "lg": "16px", "xl": "24px"},
        "shadows": {"sm": SHADOW["s1"], "md": SHADOW["s2"], "lg": SHADOW["s3"]},
        "focusRing": "auto",
        "components": {
            "Tooltip": {"defaultProps": {"withArrow": True, "openDelay": 250,
                                         "color": "hati.9"}},
        },
    }
