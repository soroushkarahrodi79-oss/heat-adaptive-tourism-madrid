# PHASE5_3B_VISUAL_STYLE_SPEC.md — HATI-Madrid Phase 5.3B

Version 1.0 · 2026-08-18. One publication visual system, reused across every figure and
the graphical abstract. Journal-scientific language; no dashboard/product styling. Colour
is never the sole carrier of meaning — every category also carries a text label and a
shape/pattern or position.

---

## 1. Typography
- **Family:** DejaVu Sans (matplotlib default; a Helvetica/Arial-class sans, embeds cleanly
  in SVG/PDF). One family only, across all figures.
- **Sizes (pt at final size):** figure title 11 · panel label (A/B/C) 11 bold · subtitle/
  axis title 9 · tick/annotation 8 · legend 8 · small caption 7.
- Weight: regular for body, bold only for panel letters and the single figure title.

## 2. Lines and markers
- Axis spines 0.8 pt; gridlines 0.4 pt, light grey `#D9D9D9`, only where they aid reading.
- Data line weight 1.2 pt; marker size 5–6 pt.
- Marker shapes carry categorical meaning where colour is used: ● agree/unchanged,
  ▲ physical more restrictive, ▼ physical less restrictive (also used as legend glyphs).
- No shadows, gradients-as-decoration, bevels, or 3D.

## 3. Categorical palette (colour-blind-safe, Okabe–Ito derived)
Neutral, non-traffic-light. The two divergence directions are two *distinct* hues, not
good/bad.

| Token | Meaning | Hex | Grayscale value | Pattern |
|---|---|---|---|---|
| NEUTRAL | agreement / unchanged | `#BFBFBF` (mid grey) | 0.75 | solid, ● |
| DIR_MORE | physical more restrictive | `#0072B2` (blue) | dark | hatch `//`, ▲ |
| DIR_LESS | physical less restrictive | `#E69F00` (amber) | mid | hatch `\\`, ▼ |
| INK | text / ink / axes | `#333333` (charcoal) | — | — |
| ACCENT | single-series bars, robust class | `#4C4C4C` (dark grey) | — | — |
| CONF_ROBUST | ROBUST | `#4C4C4C` | dark | solid |
| CONF_BOUNDARY | BOUNDARY | `#9E9E9E` | mid | hatch `..` |
| CONF_UNSTABLE | UNSTABLE | `#0072B2` (blue, attention w/o alarm) | dark | hatch `xx` |

- **No red/green success semantics anywhere.** Blue and amber are deliberately chosen so
  neither reads as "good/bad."
- Grayscale fallback: distinguishable by the grayscale values + hatch patterns above.

## 4. Two-representation neutrality rule (F1, F2, graphical abstract)
The simple proxy and the physical model are always drawn with **equal box size, equal type
size, equal line weight, equal prominence**. Neither branch is coloured to imply
superiority. Where a single accent is needed for a branch, both branches use the same
neutral charcoal outline.

## 5. Panel-label convention
Upper-left of each panel, bold capital letter "A", "B", "C", 11 pt, charcoal, no
parentheses. Figure caption (in manuscript) carries the full title; the rendered figure
carries a short top title only.

## 6. Notation and vocabulary (must match the manuscript exactly)
- **Timestamps:** `12:00`, `15:00`, `18:00` (24-h, colon). Never "noon/12h/1200".
- **Assets:** `A01`…`A27`.
- **Percentage precision:** one decimal place (`33.3%`, `64.3%`, `35.7%`, `0.0%`, `2.4%`);
  integer counts as `14/42`, `7 of 8`, `26`, `0`.
- **Feasibility / divergence state vocabulary:** "Agreement", "Physical more restrictive",
  "Physical less restrictive" (never "correct/incorrect", "error", "corrected").
- **Screening outcomes:** "Surviving alternatives", "No defensible alternative"
  (`NO_DEFENSIBLE_ALTERNATIVE` shown in monospace only where the machine state is named).
- **Exclusion vocabulary (verbatim):** `CLOSED_AT_TIMESTAMP`, `ACCESSIBILITY_CONSTRAINT`,
  `OUTDOOR_EXPOSURE_TOO_HIGH`, `INSUFFICIENT_EVIDENCE`, `NO_MEANINGFUL_THERMAL_IMPROVEMENT`.
- **Confidence vocabulary:** `ROBUST`, `BOUNDARY`, `UNSTABLE`.
- **Thermal method labels:** "Simple operational proxy (air temperature + nearby trees)"
  and "Physically based model (SOLWEIG → Tmrt → UTCI)". "Model-derived UTCI", never
  "observed/measured UTCI".

## 7. Export policy per figure
- Analytical figures (F2, F4, F5): matplotlib → **PDF + SVG + PNG (400 dpi)**.
- Map / raster-field figures (F1a, F3): raster content at native resolution, vector labels
  overlaid; export **PDF + PNG (≥300 dpi map)**; SVG where the vector overlay dominates.
- Schematics (F1b, graphical abstract): hand-authored **SVG + PDF**, plus **PNG** export.
- Never upscale existing screenshots. Fonts embedded in PDF; text kept as text in SVG.

## 8. Canvas sizing (final print)
- Single column ≈ 90 mm; 1.5-column ≈ 140 mm; full width ≈ 190 mm.
- F2 ≈ 180 mm wide (2-panel). F4 ≈ 180 mm. F1 ≈ 190 mm (2-panel). F5 ≈ 180 mm (2–3 panel).
  F3 ≈ 190 mm (3-up). Graphical abstract landscape ≈ 1 : 2.5, ≥ 1062 × 2656 px master.

## 9. Prohibited
UI cards, rounded dashboard containers, drop shadows, decorative gradients, traffic-light
red/green, correct/incorrect icons (checks/crosses), 3D, skeuomorphism, alarm/warning
iconography on `NO_DEFENSIBLE_ALTERNATIVE`.
