# PHASE5_3B_F2_AUDIT.md — HATI-Madrid Phase 5.3B

Version 1.0 · 2026-08-18. Audit of the rendered hero figure
`outputs/publication/figures/FIG02_THERMAL_METHOD_DIVERGENCE_v0.1.{pdf,svg,png}`
(script `render_fig02.py`). No new analysis; every value read from locked evidence and
asserted at render time.

---

## 1. Numerical checks (asserted in-script; render aborts if any fail)

| Check | Required | Rendered | Status |
|---|---|---|---|
| Total observations (matrix cells) | 42 | 42 (14 assets × 3 timestamps) | ✓ |
| Reclassified cells | 14 | 14 | ✓ |
| Physical more restrictive | 9 | 9 | ✓ |
| Physical less restrictive | 5 | 5 | ✓ |
| Agree (unchanged) | 28 | 28 | ✓ |
| 12:00 rate | 64.3% | 64.3% (9/14) | ✓ |
| 15:00 rate | 0.0% | 0.0% (0/14) | ✓ |
| 18:00 rate | 35.7% | 35.7% (5/14) | ✓ |

Source: `data/processed/phase2_asset_thermal_exposure.csv` (per-cell state) and
`outputs/tables/proxy_vs_physical_comparison.csv` (timestamp rates). The 9 more-restrictive
cells fall entirely at 12:00 and the 5 less-restrictive entirely at 18:00 — read directly
from the data, not imposed.

## 2. Design-safety checks

- **No correctness hierarchy.** Legend reads "Agreement", "Physical more restrictive than
  proxy", "Physical less restrictive than proxy" — no correct/incorrect, error, or
  correction language. Neither method is labelled right/wrong.
- **No flow-to-truth visual.** No Sankey/alluvial/arrow; the physical side's collapse to a
  single state is never drawn as convergence. Panel A is a categorical agreement matrix;
  Panel B is a neutral 100%-stacked categorical summary. ✓
- **No traffic-light semantics.** Directions use blue (`#0072B2`) and amber (`#E69F00`),
  deliberately not red/green; agreement is neutral grey. ✓
- **Both directions immediately visible.** Panel A shows blue (▲, //) more-restrictive
  cells and amber (▼, \\) less-restrictive cells; Panel B shows both on each timestamp bar;
  Panel C states 9 / 5 explicitly. ✓

## 3. Accessibility

- Colour is not the sole carrier: each category also has a hatch (// vs \\ vs none) and a
  marker (▲ vs ▼ vs none) plus text labels.
- Grayscale render verified: luminance agree 0.749 / less 0.636 / more 0.342, and the hatch
  directions + markers keep all three separable in monochrome (checked on a converted
  grayscale copy). ✓
- Labels legible at journal size: asset IDs 7 pt, timestamps 8 pt, titles 9–10.5 pt; no
  clipping or overlap after title shortening.

## 4. Vocabulary / notation consistency

Timestamps `12:00/15:00/18:00`; assets `A14…A27`; percentages one decimal; states use the
manuscript's "more/less restrictive" and "agreement" vocabulary. Consistent with
`PHASE5_3B_VISUAL_STYLE_SPEC.md`. ✓

## 5. Manuscript-claim support

Directly supports Results §4.1 / Discussion §5.1 (H1/H2/C1/C2/C4): thermal-method choice
changed 33.3% of outdoor asset-time classifications, in both directions, concentrated in
time — with no implication that either representation is correct. ✓

---

## GATE

42 cells, 14 divergences, 9/5 directions, and 64.3/0.0/35.7 timestamp rates are exact and
render-asserted; no correctness hierarchy or flow-to-truth visual; grayscale- and
colour-blind-legible with shape/pattern/label redundancy; vocabulary matches the manuscript.

**F2 VISUAL LOCKED**
