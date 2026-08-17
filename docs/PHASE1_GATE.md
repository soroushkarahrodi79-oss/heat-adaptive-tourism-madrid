# PHASE1_GATE.md — Phase 1 gate decision

Version 1.0 · 2026-08-17

---

## VERDICT: REVISE BASELINE

Not STOP: the central Phase 1 question — *can a scientifically defensible,
spatially differentiated tourism thermal-suitability classification be produced
for this pilot from real, open data with a transparent constraint-first
architecture* — is answered **yes**, with real evidence (`docs/PHASE1_VALIDATION_REPORT.md`
§1–§2).

Not (yet) GO TO THERMAL MODEL: the validation report identified one concrete,
cheaply fixable data-quality gap in the baseline's exposure input, and one
decision branch (the adaptation-resource exclusion rule) that this pilot's
geography never exercised. Both should be addressed with more/better **open
data at the same simple-proxy level** before justifying the much larger
SOLWEIG/Tmrt/UTCI investment — spending that effort on top of a demonstrably
gappy shade input would be premature, and `docs/FEASIBILITY_GATE.md` itself
scored scope creep 8/10, the project's single largest risk.

## What worked (do not redo)

- **Real spatial+temporal differentiation, from real data, with no hidden
  weights.** The five SEVERE-hazard exclusions are exactly the five outdoor
  assets with the lowest measured on-site tree density — a finding the rule
  table could not have produced by construction, since it does not know in
  advance which assets are gardens (`PHASE1_VALIDATION_REPORT.md` §1).
- **Monotonic, conservative hazard behaviour**: nothing is excluded below
  SEVERE; every exclusion has a stated, auditable reason (§2).
- **A real data-quality/pipeline bug was caught, not missed.** A structural
  reproducibility test (`tests/test_outputs.py`) failed on a study-area
  boundary check, exposing that an initial, tighter box had clipped real trees
  out of two well-known shaded gardens' tree counts. Fixing the box (not just
  the symptom) recovered their real tree data; a safeguard override rule also
  exists in the code for the same failure mode should it recur with different
  assets (`PHASE1_METHOD.md` §5.2, `PHASE1_VALIDATION_REPORT.md` §5).
- **The official-threshold, no-composite-score architecture is sound** and
  should carry forward unchanged into any thermal-model phase: only the input
  feeding the exposure gate should change, not the gate logic itself.

## Specific, bounded revisions before reconsidering SOLWEIG

1. **Cross-validate the OSM tree-point proxy against Madrid Open Data's Arbolado
   layer** (`docs/DATA_SOURCE_INVENTORY.csv`: rated USE, "best local per-tree
   source"). The specific gap originally found at Jardines de Cecilio Rodríguez
   and Jardines del Arquitecto Herrero Palacios turned out to be substantially a
   study-area bounding-box clipping bug in this project's own Overpass queries,
   not a pure OSM crowdsourcing gap — fixed in this same Phase 1 pass by
   widening the box and re-fetching (`PHASE1_METHOD.md` §2, §5.2). The official
   municipal Arbolado inventory (non-crowdsourced) is still worth pulling as an
   independent cross-check on the corrected OSM tree counts before trusting them
   for a thermal-model input, but is no longer the primary fix. This remains a
   same-baseline-architecture step, not a new model.
2. **Exercise the adaptation-resource exclusion branch.** It never fired in
   this pilot because every one of the 27 assets had a water point within 250 m
   or a transit stop within 400 m (`PHASE1_VALIDATION_REPORT.md` §3). Either
   tighten the thresholds against a cited source, or extend the pilot slightly
   toward a less-served pocket of the existing study area, and re-run.
3. **Add a fourth timestamp near the day's actual peak** (Barajas recorded
   40.5 °C at 18:00 local, 1.5 °C short of AEMET's red/EXTREME threshold) so the
   EXTREME branch of the decision table is empirically exercised at least once,
   not merely present in the code.
4. Re-run `docs/PHASE1_VALIDATION_REPORT.md`'s analysis after 1–3 and confirm
   the differentiation signal (§1) survives with the improved tree input.

None of this requires LiDAR, Cadastre, SOLWEIG, or new infrastructure — it is
the same lightweight geospatial stack, pointed at one better open dataset and a
slightly wider test.

## Is SOLWEIG / Tmrt / UTCI justified next?

**Conditionally yes, but not immediately.** The baseline has done its job: it
shows the underlying signal (real, measurable exposure variation across real
tourism sites, real regional hazard variation across the day) is strong enough
to be worth a more physically grounded model, which is exactly the
justification `docs/METHOD_OPTIONS.md` set out for eventually moving to
SOLWEIG. But two things should happen first, in order:

1. Complete the bounded baseline revision above. If the tree-count-driven
   differentiation in §1 of the validation report survives (or strengthens)
   once the arbolado data closes the known gap, that is the concrete evidence
   `docs/FEASIBILITY_GATE.md` asked for before committing to "the hard part...
   defensible pedestrian Tmrt/UTCI from LiDAR+canopy via SOLWEIG."
2. Only then acquire PNOA LiDAR + Spanish Cadastre for this **same ~3.5 km²
   pilot footprint** (not city-wide) and stand up a minimal SOLWEIG run for the
   same three (or four) timestamps, exactly as `docs/FEASIBILITY_GATE.md`'s
   "Recommended next steps" §4 originally specified — a sanity-check spike, not
   full production modelling.

STOP is not indicated: nothing found in this spike invalidates the project's
premise, contradicts Phase 0's findings, or reveals an unsupportable claim
already made. The scope, method, and non-claims set out in
`docs/PROJECT_CHARTER.md` and `docs/FEASIBILITY_GATE.md` all still hold.
