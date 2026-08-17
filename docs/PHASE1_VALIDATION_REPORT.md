# PHASE1_VALIDATION_REPORT.md — HATI-Madrid Phase 1

Version 1.0 · 2026-08-17. Evaluates `data/processed/pilot_classifications.csv`
(81 rows = 27 assets × 3 timestamps, produced by `src/build_classifications.py`).

---

## 1. Does the classification show meaningful spatial differentiation?

**Yes, and it is driven by real measured variation, not by construction.**

At the SEVERE-hazard timestamp (18:00, 40.5 °C), the five NOT RECOMMENDED sites are
exactly the five outdoor assets with the lowest measured on-site tree density
(Puerta de Alcalá, Fuente de Cibeles, Fuente de Neptuno, Real Observatorio de
Madrid, Monumento a Alfonso XII — all open, hard-paved monumental plazas). Every
shaded garden and every museum in the same 27-asset set, under the identical
regional hazard reading, is classified FEASIBLE WITH CONDITIONS rather than NOT
RECOMMENDED. This is real spatial structure recovered from real tree-count data,
not an artefact of the rule design (the rule only distinguishes HIGH exposure from
LOW/MODERATE; it does not know in advance which assets are gardens).

Quantitatively (see `outputs/maps/03_exposure_differentiation.png`): tree count
within site extent ranges from 0 (several monuments) to 355 (Parque del Retiro,
whole visible slice), a two-orders-of-magnitude real spread across a 3.5 km² pilot
— this supports **H1** from `docs/PROJECT_CHARTER.md` ("modelled pedestrian
thermal-exposure proxy differs significantly across tourism microsites") at the
level this baseline can test it: exposure PROXY variation is real and large; this
is not yet a validated Tmrt/UTCI comfort signal (see §5).

## 2. Does the model behave sensibly?

Yes, in the ways that matter for a constraint-first design:

- **Monotonic in hazard.** As regional air temperature rises across the three
  timestamps (34.2 → 38.8 → 40.5 °C), the feasible set only shrinks, never grows:
  LOW hazard (12:00) → 0 NOT RECOMMENDED; ELEVATED (15:00) → 0 NOT RECOMMENDED (by
  rule design, ELEVATED cannot trigger exclusion, only a conditions flag); SEVERE
  (18:00) → 5 NOT RECOMMENDED. No asset improves in feasibility as hazard rises.
- **No asset is excluded at LOW or ELEVATED hazard.** This matches the intended
  conservatism of the rule table (`src/thresholds.py:FEASIBILITY_RULES_OUTDOOR`):
  exclusion is reserved for SEVERE/EXTREME hazard, so the model does not
  over-trigger on a merely warm (not extreme) afternoon.
- **Indoor sites never excluded**, consistent with the design intent, but flagged
  FEASIBLE WITH CONDITIONS at SEVERE hazard rather than silently FEASIBLE — the
  A/C-unverified caveat is surfaced, not hidden.

## 3. Which inputs dominate the decision?

For this specific pilot (dense, well-served central tourist core), **the hazard
gate and the exposure gate jointly determine every NOT RECOMMENDED outcome; the
adaptation-resource gate never independently excluded a site.**

- All 5 exclusions fired on the same rule: `SEVERE hazard AND exposure == HIGH`
  (`src/thresholds.py` rule 2). Rule 3 (`SEVERE hazard AND adaptation == POOR`)
  never fired on its own.
- Checking why: `adaptation_state` across all 27 assets is GOOD for 18 and LIMITED
  for 9 — **POOR never occurs in this pilot.** Every asset in this dense central
  core has either a drinking-water point within 250 m or a transit stop within
  400 m (usually both). This is an honest, expected finding given the study
  area's location, not a bug — but it means **the adaptation-resource gate is
  currently untested by this pilot's data.** A future pilot extension into a
  less-served part of the study area, or a stricter distance threshold, would be
  needed to exercise that branch of the rule table.
- `evidence_confidence` is MEDIUM for 68/81 rows and LOW for 13/81. All 13 LOW
  rows decompose to a single, clean cause: the 13 indoor assets at the one
  SEVERE-hazard timestamp (A/C-unverified caveat, `docs/PHASE1_METHOD.md` §5.4).
  The exposure-gate safeguard override (§5.2 in the method doc) did not fire for
  any of the 81 rows in this final run — see §5 below for why. **No row reached
  HIGH confidence** — every input in this baseline carries at least one real
  caveat (regional-station displacement, proxy-not-measurement, or
  completeness-uncertainty). This is reported as a finding about the current
  evidence base, not a defect in the confidence scheme.

## 4. Sensitivity to thresholds

A quick perturbation of the exposure-gate buffer radius (baseline 50 m for
point-type assets) to 30 m and to 75 m was run directly against the pipeline
(reproducible by editing `thresholds.EXPOSURE_BUFFER_M` and re-running
`src/build_classifications.py`):

| Radius | Tercile cutpoints (q1, q2) | Outdoor assets whose exposure_state changed vs. 50 m baseline |
|---|---|---|
| 30 m | (0.00, 3.33) | 1 of 14 (Palacio de Cibeles: MODERATE→HIGH) |
| 50 m (baseline) | (0.33, 3.67) | — |
| 75 m | (2.67, 22.0) | 7 of 14 (Puerta de Alcalá, Fuente de Cibeles, Fuente de Neptuno, Estatua de Goya, Palacio de Cibeles, Jardines de Cecilio Rodríguez, Jardines del Arquitecto Herrero Palacios) |

**Interpretation:** the baseline is fairly stable to a modest radius reduction
(30 m: only 1 of 14 outdoor assets reclassified) but noticeably more sensitive to
a substantial radius increase (75 m: half of the 14 outdoor assets reclassified,
as the wider ring starts to catch street trees on adjoining blocks and shift
several genuinely open plazas out of the HIGH/poor-shade band). This asymmetry
makes sense given the pilot's geometry — Retiro's paths and the Paseo del Prado
sidewalks put meaningful tree cover 50–75 m from several monument points that
have none within 30–50 m — and is a real, reportable sensitivity, not negligible,
though still far short of the instability a composite weighted index would show
under an equivalent perturbation (per `docs/METHOD_OPTIONS.md`'s H2 prediction,
not separately re-tested here since Option A was never built as a baseline
comparator in this Phase 1 spike — see §6). The 50 m choice is defensible as
"approximates the immediate standing/queueing area" but is not the only
defensible choice, and this table is offered so a reader can judge that for
themselves rather than take the 50 m figure on faith.

The hazard-gate thresholds (36/39/42 °C) are official AEMET values, not tunable
parameters of this project, so no sensitivity analysis is applicable to them.

## 5. Where classifications are unstable

- **A study-area boundary bug was caught by the test suite, not by inspection,
  and its fix changed real results.** An early build used a tighter study-area
  box (south edge 40.4055, east edge -3.6790) to both curate the pilot assets
  and query the tree layer. `tests/test_outputs.py::test_asset_coords_within_study_area`
  failed because three real, legitimately-curated assets' OSM centroids fell
  just outside that box (Atocha station, and the two Retiro gardens Jardines de
  Cecilio Rodríguez and Jardines del Arquitecto Herrero Palacios) — a predictable
  consequence of Overpass reporting a way/relation's full-geometry centroid even
  when only part of the feature intersects the query bbox. Fixing the box
  (widened ~150 m on the affected edges, all OSM layers re-fetched — see
  `docs/PHASE1_METHOD.md` §2) had a second, unanticipated effect: both gardens'
  real tree counts, previously 0 (because the ORIGINAL tighter tree-layer query
  had clipped out trees sitting in the eastern part of those gardens), came back
  as 4 and 22 respectively once re-queried against the wider box. What had
  looked like a genuine OSM crowdsourcing gap (documented in an earlier draft of
  this report and of `docs/PHASE1_METHOD.md`) turned out to be, at least in
  significant part, a bounding-box clipping artefact in this project's own query
  construction. **This is the single most important methodological finding of
  this validation pass**: a structural test written for a different, narrower
  purpose (coordinate-bounds sanity) surfaced a real data-quality bug that
  silent visual inspection of the maps did not catch, and fixing it measurably
  changed the exposure classification of two named, real gardens. The explicit
  safeguard override described in `docs/PHASE1_METHOD.md` §5.2 remains in the
  code for exactly this class of problem, but did not need to activate once the
  underlying box was corrected.
- **Assets near a tercile boundary** (§4): e.g. Palacio de Cibeles shifts under a
  30 m buffer-radius perturbation, and seven of fourteen outdoor assets shift
  under a 75 m perturbation.
- **The three fixed timestamps** happened to avoid AEMET's EXTREME (≥42 °C) band
  entirely, even though the true daily peak (40.5 °C at Barajas, 18:00 local) came
  within 1.5 °C of it. The EXTREME branch of the outdoor rule table (unconditional
  NOT RECOMMENDED) and the indoor EXTREME branch are therefore **logically
  implemented but empirically untested** by this run — see `src/thresholds.py`
  and `src/build_classifications.py:feasibility_decision()` for the rule, and note
  that it did not fire for any of the 81 rows.
- **INSUFFICIENT EVIDENCE never fired.** The defensive missing-input path exists
  in the code but every one of the 81 rows had complete inputs, so this state is
  implemented but unexercised by the current pilot.

## 6. What cannot yet be claimed

- **No behavioural claim of any kind** — unchanged from `docs/PROJECT_CHARTER.md`
  and `docs/FEASIBILITY_GATE.md`; this Phase 1 spike does not touch behaviour and
  reaffirms nothing new here.
- **No composite-index comparison was actually built.** `docs/METHOD_OPTIONS.md`'s
  H2 ("a weighted-index baseline is more fragile than the constraint-first design")
  is a Phase-0 prediction that this Phase 1 spike did not test empirically — no
  Option-A weighted index was implemented alongside Option B. If a future phase
  wants to demonstrate H2 rather than assert it, that comparison still needs to be
  built.
- **No claim that 50 m / 250 m / 400 m are the "correct" distances** — they are
  documented, defensible, and — for the transit/water figures — grounded in
  standard planning heuristics, but §4 shows real sensitivity, and no independent
  ground-truth (e.g. a field shade survey) was used to calibrate them.
- **No claim about the adaptation-resource gate's real-world behaviour**, because
  it was never exercised (POOR never occurred) in this pilot — see §3.
- **No comfort claim.** The hazard gate is ambient air temperature at a station
  ~9 km away, not a measured or modelled on-site thermal-comfort index. A site
  labelled FEASIBLE is not asserted to be thermally comfortable, only that this
  baseline's explicit constraints did not trigger exclusion.
- **No claim of A/C operational status** for any indoor asset — flagged as an
  explicit, uncorrected gap throughout.

## 7. Overall read

The baseline recovers a real, measurable, non-trivial spatial and temporal
pattern from genuinely open data using a fully auditable rule set with no hidden
weights — the core scientific question this spike was built to answer. Building
it also surfaced and fixed a real bounding-box construction bug that had been
silently undercounting trees at two named gardens, caught by a structural test
rather than visual inspection — evidence that the project's own reproducibility
tooling (not just its evidence-confidence labelling) is doing real work. The two
areas most worth strengthening before any further build are (a) a
directly-measured or higher-quality shade/canopy input (e.g. Madrid Open Data's
official Arbolado layer) to replace the still-proxy tree-count-in-buffer measure,
and (b) a pilot extension or threshold change that actually exercises the
adaptation-resource exclusion branch, which this dense central pilot never
triggered.
