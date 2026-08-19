# PHASE5_3A_PUBLICATION_FIGURE_ARCHITECTURE.md — HATI-Madrid Phase 5.3A

Version 1.0 · 2026-08-18. Publication figure and table architecture for the locked
manuscript. **No figures rendered in this phase.** No new analysis; no locked number
changed; every panel maps to locked evidence (`PHASE5_3A_VISUAL_DATA_SOURCE_MAP.csv`).
Primary target: Tourism Management Perspectives (TMP).

Supersedes the six-figure `docs/PHASE5_0_FIGURE_PLAN.md` where they differ: the main set
is reduced to **5 figures** by folding the decision-architecture schematic into Figure 1
and folding the S8 no-survivor case into the scenario figure.

---

## 1. Governing data constraint (drives the centerpiece design)

From `data/processed/phase2_asset_thermal_exposure.csv` (42 outdoor rows):

- proxy feasibility states: FEASIBLE 9 · FEASIBLE WITH CONDITIONS 28 · NOT RECOMMENDED 5
- physical feasibility states: **FEASIBLE WITH CONDITIONS for all 42**
- transitions: 9 (FEASIBLE→FWC, physical more restrictive) · 28 (FWC→FWC, unchanged) ·
  5 (NOT RECOMMENDED→FWC, physical less restrictive)

Because the physical side is single-valued, **any proxy→physical flow/alluvial/Sankey
would read as "the physical model collapses everything to one (correct) answer."** The
centerpiece must instead encode **agreement vs direction of divergence per cell**, never
a flow toward the physical state. This is the paper's largest visual overclaim risk and
governs Figure 2 and the graphical abstract (see §7).

## 2. Figure necessity audit

| Candidate (old plan) | Claim supported | Clearer than text/table? | Evidence or illustration? | From locked data? | Redundant? | Class |
|---|---|---|---|---|---|---|
| Study area map + pipeline (old F1) | pilot scope; two-track method into one screen | yes — orientation | evidence (design) | yes | no | **ESSENTIAL → F1** |
| Proxy-vs-physical divergence (old F2) | H1/H2 method sensitivity | yes — matrix beats prose | evidence | yes | no | **ESSENTIAL → F2** |
| UTCI spatial/timestamp field (old F3) | C3 mechanism: radiant field structured; noon ≥32 | yes — shows the field text cannot | evidence | yes (rasters) | no | **USEFUL → F3 (main; demotable)** |
| Decision architecture schematic (old F5) | C13 constraint-first, no composite | partly — compact enough to embed | evidence (design) | yes (docs) | overlaps F1 pipeline | **MERGE into F1b** |
| Baseline-vs-screening scenarios (old F6) | C5/C6 candidate-set change | yes — 8 scenarios at a glance | evidence | yes | no | **ESSENTIAL → F4** |
| S8 spotlight (old F6b) | C7 explicit no-survivor | marginal as standalone | evidence | yes | subset of F4 | **MERGE into F4 (highlighted row/panel)** |
| Uncertainty/robustness (old F4) | H5/C8-C9 tested-uncertainty stability | yes — sensitivity + confidence | evidence | yes | no | **ESSENTIAL → F5** |
| Dashboard/visual prototype (old F7) | presentability (not a result) | no scientific need | illustration | yes (screenshot) | — | **SUPPLEMENTARY (S-Fig, optional)** |

## 3. Selected main figures (5)

**Figure 1 — Study design and screening architecture.**
- *Purpose:* orient the reader and show that two thermal representations feed one
  transparent, constraint-first screen.
- *Panel (a):* Prado–Retiro–Atocha **Madrid pilot** study-area map (≈3.5 km²) with the 27
  assets marked by indoor/outdoor; scale bar; "Madrid pilot study area" label (never
  "Madrid study area").
- *Panel (b):* compact pipeline — tourism assets → [simple operational proxy | physically
  based SOLWEIG/UTCI] → ordered gate chain (open? → reachable? → thermally feasible? →
  evidence sufficient? → meaningful improvement?) → surviving alternatives / no
  defensible alternative. The gate chain absorbs the old decision-architecture figure.
- *Source:* `data/processed/study_area.geojson`, `pilot_assets.csv`,
  `docs/PHASE3_DECISION_ARCHITECTURE.md` §1–3.

**Figure 2 — Thermal-method divergence (empirical centerpiece).**
- *Purpose:* H1/H2 — thermal-method choice changes feasibility classifications, in both
  directions, concentrated in time.
- *Panel (a):* 14 outdoor assets × 3 timestamps **agreement/divergence matrix**; each cell
  one of three categorical states — *agree* (28), *physical more restrictive* (9),
  *physical less restrictive* (5). Encodes both directions; **not** a proxy→physical flow.
- *Panel (b):* reclassification rate by timestamp bar — 12:00 = 64.3%, 15:00 = 0.0%,
  18:00 = 35.7% (n = 14 each).
- *Optional annotation (see §5):* small two-construct noon note, only if elegant.
- *Source:* `phase2_asset_thermal_exposure.csv`, `outputs/tables/proxy_vs_physical_comparison.csv`.

**Figure 3 — Modelled UTCI field across the day (mechanism).**
- *Purpose:* C3 — the physical field carries spatially and temporally structured
  information that ambient air temperature does not; at noon the buffer-mean UTCI is
  ≥32 °C at all 14 outdoor assets.
- *Panel:* three-timestamp small-multiple of modelled UTCI (12:00/15:00/18:00), one shared
  colour ramp, 32/46 °C category breaks marked, outdoor asset points overlaid; scale bar.
- *Note:* labelled as **model-derived UTCI**, never "measured"; supports the *why* behind
  Figure 2. Demotable to supplementary if the handling editor prefers a leaner,
  tourism-facing main set.
- *Source:* `outputs/maps/utci_1200.tif`, `utci_1500.tif`, `utci_1800.tif`;
  `outputs/tables/solar_forcing_sensitivity.csv` (noon 14/14 ≥32 °C); `pilot_assets.csv`.

**Figure 4 — Screening consequence versus a conventional baseline (incl. S8).**
- *Purpose:* C5/C6/C7 — heat-aware screening changes the option set a proximity tool
  returns, and can return an explicit no-survivor state.
- *Panel (a):* per-scenario grid S1–S8 — nearest-open pick, whether it survives screening,
  count removed on thermal/evidence grounds, and the surviving-set size; annotated totals
  (candidate set changed 7/8; nearest-open pick fails 3/8; 23 options removed).
- *Panel (b) / highlighted row:* **S8** (Parque del Retiro, 15:00, 500 m) — 26 candidates
  evaluated, 0 survive → NO_DEFENSIBLE_ALTERNATIVE. Presented as an architectural outcome,
  not a normative "responsible" choice. No ranked "best destination" chart.
- *Source:* `outputs/tables/phase3_hati_vs_baseline.csv`,
  `data/processed/phase3_scenarios_summary.csv`, `phase3_scenarios.csv` (S8 rows).

**Figure 5 — Decision robustness under tested uncertainty.**
- *Purpose:* H5/C8–C9 — decisions are stable under the solar forcing actually tested, and
  the single unstable case is shown honestly; tested uncertainty ≠ total uncertainty.
- *Panel (a):* decisions changed vs solar-forcing realization — real-satellite 1/42 (2.4%),
  −10% 0/42, −20% 0/42.
- *Panel (b):* decision-confidence distribution — ROBUST 35, BOUNDARY 6, UNSTABLE 1 (of 42),
  with A24 @ 18:00 flagged as the sole UNSTABLE 46 °C-boundary case.
- *Title:* "Decision robustness under tested uncertainty" — never "model validation"; a
  caption line states the envelope covers solar forcing + targeted geometry only.
- *Source:* `outputs/tables/solar_forcing_sensitivity.csv`,
  `data/processed/phase2_2_decision_confidence.csv`.

## 4. Narrative sequence

F1 *where/what/how* → F2 *does thermal representation change classifications?* → F3 *why
(radiant field)* → F4 *does it propagate into the tourism option set, and what when
nothing survives?* → F5 *how stable is all this?* One argument, in order.

## 5. Noon-result handling (Task 5)

Include the noon contrast only as a **small caption annotation on Figure 2(b)**, and only
if it renders elegantly: label the two quantities as different constructs — "Operational
air-temperature hazard state (LOW, 34.2 °C)" vs "Model-derived UTCI thermal-stress
category (≥32 °C, 14/14 assets)" — on **separate, non-shared axes/legends**, with no arrow
implying one corrects the other and no wording implying AEMET failure. If it cannot be
shown cleanly, leave it to text (Results §4.1 already carries it). Default recommendation:
**annotation, not a shared-axis panel.**

## 6. Table architecture (Task 9)

Reduced from five to **three main tables**; the rest move to supplementary or text.

| Table | Content | Placement | Rationale |
|---|---|---|---|
| T1 | Data sources / provenance (layer, dataset, vintage, licence, "what it does NOT measure") | **Main (compact)** | supports the open-data reproducibility claim; not duplicated by any figure; demotable to supplementary if the editor wants fewer tables |
| T2 | Decision architecture — ordered gates, thresholds, machine-readable exclusion vocabulary | **Main** | the constraint-first contribution in exact form; complements F1(b) with precise thresholds |
| T3 | Thermal-method comparison — exact rates by overall/timestamp/direction/morphology | **Supplementary** | Figure 2 is the main-text carrier; the table holds exact per-category values incl. morphology invariance |
| T4 | Scenario comparison S1–S8 — source, nearest-open pick, distance, survives?, removed IDs, surviving-set | **Main** | exact per-scenario detail a figure cannot show legibly; readable for a tourism audience |
| T5 | Limitations / evidence boundaries | **Text only** | fully carried by Limitations §6 prose; a table would duplicate it |
| T6 | Proxy-family agreement (Phase 1.2) | **Supplementary** | motivates physical modelling; not a headline |
| T7 | Solar-forcing & accessibility sensitivity detail | **Supplementary** | exact detail behind Figure 5 and the radius sensitivity |

Scientific tables remain editable text, never rasterized images.

## 7. Biggest visual overclaim risks and mitigations

1. **Physical side is single-valued (all 42 → FWC).** A proxy→physical flow implies
   convergence to a "correct" answer. → Figure 2 uses an agreement/direction matrix, not a
   flow; the graphical abstract shows "changed, in both directions," not a merge.
2. **Traffic-light semantics** (green physical / red proxy) would imply superiority. →
   neutral categorical palette; both representations equal visual weight; direction encoded
   by two distinct neutral hues + text labels, colour-blind safe.
3. **UTCI map read as measured truth.** → label "model-derived UTCI"; category breaks only;
   no "validation" language.
4. **S8 moralised** ("responsible choice"). → framed as an architectural outcome of hard
   constraints.
5. **Figure 5 read as validation.** → titled "under tested uncertainty"; caption states
   tested ≠ total.

## 8. Output resolution strategy

| Figure | Master (editable/vector) | Journal export | Dimensions / aspect | Raster resolution |
|---|---|---|---|---|
| F1 | SVG (map panel from GeoJSON/matplotlib → SVG; schematic native SVG) | TIFF or PDF | 2-panel, ~full width (≈190 mm) | ≥600 dpi line/300 dpi map |
| F2 | SVG (matrix + bar) | TIFF/PDF | ~1.5-column, ~140 mm | ≥600 dpi |
| F3 | PDF/SVG (rasters embedded from `utci_*.tif` at native res + vector overlays) | TIFF/PDF | 3-up small-multiple, full width | map ≥300 dpi |
| F4 | SVG (grid) | TIFF/PDF | full width | ≥600 dpi |
| F5 | SVG (two charts) | TIFF/PDF | ~1.5-column | ≥600 dpi |

Prefer SVG/PDF masters + TIFF/PNG exports. **Do not upscale** existing analysis PNGs;
re-render F1a/F3 from the source rasters/geometry.

## 9. Dashboard rule

The Dash MVP is **not** a main scientific figure. At most one supplementary
implementation illustration (annotated screenshot), clearly labelled "not a result," and
**never** in the graphical abstract.

## 10. Shared figure style

One typographic family; shared categorical-state vocabulary (agree / physical more
restrictive / physical less restrictive; surviving / excluded-by-reason;
ROBUST/BOUNDARY/UNSTABLE); consistent asset (A01…A27) and timestamp (12:00/15:00/18:00)
notation; no shadows, UI cards, dashboard chrome, decorative icons, or 3D. Journal
figures, not product design.

---

## FIGURE ARCHITECTURE GATE

Five main figures, each supporting a named manuscript claim; the decision-architecture and
S8 figures were merged rather than kept as standalone; no decorative or redundant main
figure; no new analysis (every panel from locked tables/rasters/docs); the centerpiece and
graphical abstract are designed to avoid any accuracy/superiority visual implication;
units and denominators (14/42, 64.3/0/35.7, 7/8, 3/8, 26→0, 1/42, 35/6/1) are correct;
uncertainty is labelled explicitly partial; the dashboard is excluded from main evidence;
and TMP technical requirements (editable tables, vector masters, publication resolution)
are respected.

**PUBLICATION FIGURE ARCHITECTURE APPROVED**
