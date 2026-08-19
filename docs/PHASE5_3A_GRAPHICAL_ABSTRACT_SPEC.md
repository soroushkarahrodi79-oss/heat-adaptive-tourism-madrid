# PHASE5_3A_GRAPHICAL_ABSTRACT_SPEC.md — HATI-Madrid Phase 5.3A

Version 1.0 · 2026-08-18. Specification (not rendering) for the Tourism Management
Perspectives graphical abstract. No new analysis; numeric anchors are locked values.
The graphical abstract is a standalone communication object, independent of the dashboard.

---

## 1. Central narrative (the one message)

Switching the **thermal representation** — a simple operational proxy versus a physically
based SOLWEIG/UTCI model — changes some feasibility classifications, in both directions,
and therefore changes the surviving tourism-opportunity set that a constraint-first screen
returns (sometimes to none). **The pivot is method *choice*, not method *accuracy*.**

## 2. Content hierarchy (what the eye must get, in order)

1. thermal-method **choice** (two equal representations);
2. classification **divergence** (33.3%, both directions);
3. constraint-first **screening consequence** (surviving set changes);
4. explicit **no-defensible-alternative** is a possible output.

Readable in ~5 seconds. Priority 1–2 dominate; 3–4 support.

## 3. Layout wireframe (text)

Landscape, four stages left→right, with a thin pivot banner along the top and one small
footer stat. Both thermal branches are vertically symmetric and equal in size/weight.

```
┌───────────────────────────────────────────────────────────────────────────┐
│  PIVOT BANNER:  Method choice, not method accuracy                          │
├───────────────┬───────────────────────┬───────────────┬────────────────────┤
│  STAGE 1      │  STAGE 2              │  STAGE 3      │  STAGE 4           │
│  Context      │  Two representations  │  Decision     │  Constraint-first  │
│               │  (symmetric)          │  effect       │  screen            │
│               │                       │               │                    │
│  [urban       │  ┌─ Simple proxy ──┐  │   33.3%       │  open? reach?      │
│   tourism     │  │ air temp +      │  │  (14/42)      │  thermal? evid?    │
│   asset       │  │ nearby trees    │  │  classes      │  improvement?      │
│   cluster,    │  └─────────────────┘  │  changed      │        │           │
│   sun/heat    │        —— vs ——       │  ↕ both       │   ┌────┴─────┐     │
│   glyph]      │  ┌─ Physical model ┐  │  directions   │   │ surviving │     │
│               │  │ SOLWEIG→Tmrt→   │  │               │   │ alts      │     │
│               │  │ UTCI            │  │               │   └───────────┘     │
│               │  └─────────────────┘  │               │   ┌───────────┐     │
│               │                       │               │   │ NO DEFENS-│     │
│               │                       │               │   │ IBLE ALT. │     │
│               │                       │               │   └───────────┘     │
├───────────────┴───────────────────────┴───────────────┴────────────────────┤
│  FOOTER STAT:  Candidate set changed in 7 of 8 scenarios                     │
└───────────────────────────────────────────────────────────────────────────┘
```

Stage 2's "vs" is a neutral connector (equal-weight), never an arrow from proxy to
physical. Stage 3's "both directions" is shown with a two-headed neutral indicator (↕),
not a one-way improvement arrow. Stage 4 shows the ordered gates leading to *either* a
surviving set *or* the explicit no-alternative box (both outcomes visible, equal weight).

## 4. Exact visible text (verbatim; ≤45 words)

- Pivot banner: **Method choice, not method accuracy**
- Stage 1: **Urban tourism opportunities under extreme heat**
- Stage 2 header: **Two thermal representations**
  - Branch A: **Simple operational proxy — air temperature + nearby trees**
  - Branch B: **Physical model — SOLWEIG → Tmrt → UTCI**
- Stage 3: **Feasibility classifications changed — in both directions**  · label **33.3% (14/42)**
- Stage 4 header: **Constraint-first screening**
  - gate labels: **open? · reachable? · thermally feasible? · evidence? · improvement?**
  - outcome A: **Surviving alternatives**
  - outcome B: **No defensible alternative**
- Footer stat: **Candidate set changed in 7 of 8 scenarios**

**Word count (excluding numeric labels 33.3%, 14/42, 7 of 8 and the acronyms
SOLWEIG/Tmrt/UTCI): 41 words** — within the ≤45 limit. The Abstract is not pasted in.

## 5. Numerical anchors (locked)

- **33.3% (14/42)** outdoor asset-time classifications changed — `phase2_asset_thermal_exposure.csv` / `proxy_vs_physical_comparison.csv`.
- **both directions** — 9 more restrictive, 5 less restrictive (shown as text, not counts).
- **7 of 8 scenarios** candidate set changed — `phase3_hati_vs_baseline.csv`.

**Deliberately excluded:** the 64.3% noon result (too easily misread without construct
context), the 3/8 baseline-failure count (optional; omitted to keep a 5-second read), and
the confidence distribution.

## 6. Neutral visual semantics

- Two thermal branches: **equal size, equal visual authority, distinct neutral hues**
  (e.g. two mid-tone categorical colours from the project palette). No green/red, no
  primitive/advanced, no before/after, no wrong/right, no arrow from proxy to physical.
- "Divergence in both directions" uses a symmetric two-hue split (one hue = physical more
  restrictive, one = physical less restrictive, neutral grey = agree), each with a text
  label — the same categorical vocabulary as Figure 2.
- Palette: neutral charcoal base, restrained categorical accents, high contrast, minimal
  decoration; no dashboard chrome, cards, shadows, 3D, or skyline decoration (a plain
  asset/heat glyph only if it adds meaning).
- The two outcome boxes (surviving / no defensible alternative) are equal-weight; the
  no-alternative box is not styled as failure or alarm.

## 7. Accessibility

- Colour-blind-safe hue pairs; never colour alone — every category and branch also carries
  a text label.
- Legible in grayscale: distinguish branches/categories by label + pattern/position, not
  only hue.
- Minimum text sized to remain readable at ~5 × 13 cm; sans-serif; high foreground/
  background contrast (WCAG AA target).

## 8. Dimensions and formats

- Orientation: **landscape**. TMP minimum 531 (H) × 1328 (W) px; readable at ~5 × 13 cm.
- Target aspect ≈ **1 : 2.5** (H:W). Recommended master canvas ≥ **1062 × 2656 px**
  (2× the minimum) to guarantee crisp export.
- **Master:** SVG (or editable vector/PDF). **Submission export:** PDF or high-resolution
  TIFF/PNG meeting or exceeding 531 × 1328 px. Do not upscale any existing screenshot.

## 9. Prohibited visual interpretations (must not be implied)

- physical model = correct / proxy = wrong (no check/cross, no "error"/"correction"/
  "accuracy");
- a one-way flow or improvement arrow from proxy to physical, or a collapse of the proxy's
  three states into the physical single state (this would imply convergence to truth —
  the exact risk created by the single-valued physical side);
- AEMET failure or that air temperature "missed" heat (the noon result is excluded);
- any behavioural/outcome message (tourist redistribution, safety, optimisation);
- product/dashboard framing; no HATI acronym required;
- novelty superlatives ("first," "novel," etc.).

---

**Handoff:** this spec seeds Phase 5.3B rendering. Do not render here. On render, the
graphical abstract and Figure 2 must share the agreement/direction categorical vocabulary
and palette so the "method choice, not accuracy" framing is visually identical across both.
