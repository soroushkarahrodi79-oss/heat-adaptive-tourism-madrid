# PHASE5_3B_VISUAL_QA.md — HATI-Madrid Phase 5.3B

Version 1.0 · 2026-08-18. Final visual QA across all rendered publication figures and the
graphical abstract. Each figure was opened at full size, inspected at journal-column
display size and in grayscale, and its annotations checked against locked data. No new
analysis; no locked number changed.

Style system: `PHASE5_3B_VISUAL_STYLE_SPEC.md`. Traceability: `PHASE5_3B_RENDER_MANIFEST.csv`
(`new_analysis = FALSE` for every panel).

---

## 1. Final figure set

| Manuscript ref | File (base) | Purpose | Status |
|---|---|---|---|
| Figure 1 | FIG01_STUDY_DESIGN_v0.1 | Madrid pilot map + constraint-first architecture | ✓ |
| Figure 2 | FIG02_THERMAL_METHOD_DIVERGENCE_v0.1 | thermal-method divergence (hero) | **F2 VISUAL LOCKED** |
| Figure 3 | FIG03_SCREENING_CONSEQUENCE_v0.1 | screening vs nearest-open baseline (incl. S8) | **F4 VISUAL LOCKED** |
| Figure 4 | FIG04_TESTED_UNCERTAINTY_v0.1 | robustness under tested uncertainty | ✓ |
| Supp. Figure S1 | SFIG01_UTCI_FIELD_v0.1 | modelled UTCI field (demoted from main) | ✓ (supplementary) |
| Graphical abstract | HATI_graphical_abstract_v0.1 | one-sequence paper summary | **GRAPHICAL ABSTRACT VISUAL LOCKED** |

Main figures: **4**. Each has PDF (vector) + SVG (text-as-text) + PNG (≥400 dpi; SFIG01
raster at native resolution). Graphical abstract 2656 × 1062 px.

## 2. Nine-point QA checklist (all figures)

1. **Full-size inspection** — all figures render without truncation; Stage 4 of the
   graphical abstract and the F3/F4 headers were rebalanced after first render to remove
   collisions. ✓
2. **Journal-column display size** — labels remain legible at ~90–190 mm; smallest text is
   6.3–7 pt (asset IDs, sub-labels), acceptable for print. ✓
3. **Grayscale** — F2 verified (luminance agree 0.749 / less 0.636 / more 0.342, plus hatch
   + marker redundancy); F3 uses filled/open markers + bar length (colour non-essential);
   F4 uses hatch on BOUNDARY/UNSTABLE; graphical abstract carries meaning in text. ✓
4. **Text clipping** — none after fixes; long asset/pick names truncated with ellipsis. ✓
5. **Overlapping labels** — none; header collisions in F2 and F3 fixed. ✓
6. **Consistent fonts** — DejaVu Sans throughout; consistent size hierarchy. ✓
7. **State terminology matches manuscript** — "agreement / physical more restrictive /
   physical less restrictive"; "surviving alternatives / no defensible alternative";
   `OUTDOOR_EXPOSURE_TOO_HIGH`, `NO_DEFENSIBLE_ALTERNATIVE`; `ROBUST/BOUNDARY/UNSTABLE`;
   "model-derived UTCI". ✓
8. **Numerical annotations vs locked data** — all render scripts assert values before
   saving: F2 (42/14/9/5; 64.3/0.0/35.7); F3 (7/8, 3/8, 23; S8 26→0); F4 (1/0/0; 35/6/1;
   A24@18:00); SFIG01 (noon min 32.0); graphical abstract (33.3%/14-42; 7 of 8). ✓
9. **No interpretation exceeds the claim ceiling** — see §3. ✓

## 3. Claim-ceiling / method-neutrality sweep

- **No accuracy/superiority visual** anywhere: F2 uses an agreement/direction matrix (no
  proxy→physical flow, despite the physical side collapsing to one state); the graphical
  abstract draws the two representations at equal authority under "method choice, not
  method accuracy". ✓
- **No traffic-light semantics**: divergence = blue/amber (not red/green); confidence =
  charcoal/grey/blue; baseline status = filled/open markers. ✓
- **No behavioural/outcome claim**: no ranked "best", no "safe/responsible", no
  redistribution; S8 framed as an architectural outcome. ✓
- **Uncertainty explicitly partial**: F4 caption "tested uncertainty only … not total
  uncertainty; not a validation." ✓
- **UTCI labelled model-derived** (SFIG01), never observed/validated. ✓
- **No product/dashboard**: the Dash MVP appears in no main or supplementary scientific
  figure and not in the graphical abstract. ✓

## 4. F3 main-vs-supplementary decision (recorded)

The UTCI field was **demoted to Supplementary Figure S1**. Rationale: (1) its decision
signal is indirect — outdoor feasibility collapses to a single category at the pre-registered
10 m buffer-mean, so the spatial texture is not the decision variable; (2) for the primary
target (Tourism Management Perspectives) three UTCI rasters tilt the paper toward an
urban-climate-methods identity, which the Journal Fit doc advises against; (3) the noon
≥ 32 °C mechanism it supports (C3) is already carried by Figure 2's context and the text.
Main figures renumbered to a contiguous 1–4; SFIG01 retained for readers/reviewers who want
the modelled field (and for the SCS/Urban Climate secondary targets).

## 5. Tables (non-duplication check)

No scientific table was rendered as an image. Figures and the three planned main tables (T1
provenance, T2 decision architecture, T4 scenarios) do not duplicate: Figure 2 carries the
divergence *visual* while the exact per-category rates live in supplementary Table T3;
Figure 3 carries the scenario *visual* while T4 holds exact per-scenario detail. ✓

## 6. Output inventory (with SHA-256 in the manifest)

- `outputs/publication/figures/FIG01_STUDY_DESIGN_v0.1.{pdf,svg,png}`
- `outputs/publication/figures/FIG02_THERMAL_METHOD_DIVERGENCE_v0.1.{pdf,svg,png}`
- `outputs/publication/figures/FIG03_SCREENING_CONSEQUENCE_v0.1.{pdf,svg,png}`
- `outputs/publication/figures/FIG04_TESTED_UNCERTAINTY_v0.1.{pdf,svg,png}`
- `outputs/publication/figures/SFIG01_UTCI_FIELD_v0.1.{pdf,svg,png}`
- `outputs/publication/graphical_abstract/HATI_graphical_abstract_v0.1.{svg,pdf,png}`
- Render scripts: `render_fig01.py`, `render_fig02.py`, `render_fig04.py` (→FIG03),
  `render_fig05.py` (→FIG04), `render_fig03.py` (→SFIG01), `render_graphical_abstract.py`.

## 7. Residual notes (non-blocking)

- SFIG01 fine 2.5 m texture is dense at small print size; acceptable for a supplementary
  field figure and readable at full width.
- Render-script filenames retain their Phase-5.3A ordinals (fig03/04/05) while their output
  basenames carry the final manuscript numbering; the manifest maps script → output to avoid
  confusion.

---

## PHASE 5.3B GATE

F2 locked; F4 (screening) locked; F1 scientifically clear; F5 (tested uncertainty) bounded
and non-validation; F3 (UTCI) explicitly classified **supplementary** with main figures
renumbered to 1–4; graphical abstract locked and method-neutral; all outputs
publication-quality (vector masters + high-res raster); every panel traceable with
`new_analysis = FALSE`; no accuracy/superiority visual; no product/dashboard framing; all
numerical annotations render-asserted against locked data.

**PUBLICATION VISUALS LOCKED**
