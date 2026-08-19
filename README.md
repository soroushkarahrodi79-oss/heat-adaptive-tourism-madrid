# HATI-Madrid — Heat-Adaptive Tourism Opportunity Screening (Madrid pilot)

A reproducible research pilot on **screening urban tourism opportunities under extreme
heat**. On a single documented extreme-heat day in central Madrid, the project compares two
thermal representations — a simple operational proxy and a physically based SOLWEIG/UTCI
configuration — inside one transparent, constraint-first decision architecture, and tests
whether the choice of thermal method changes tourism-feasibility classifications and the
surviving set of candidate alternatives.

> **Status:** research pilot; manuscript **in preparation / pre-submission**. This
> repository is a private preservation snapshot of the scientific work, not a released
> product. Nothing here is a validated operational tool.

## Project overview

Extreme heat is a time- and place-sensitive management problem for urban tourism. Broad
climate-suitability indices operate at a coarse scale, while thermal routing and
heat-adjusted accessibility presuppose the candidate set. This project addresses the
**upstream screening stage**: which tourism opportunities remain defensible candidates at a
given hour under thermal, operational, accessibility, and evidence constraints — and it
quantifies how sensitive that screening is to the choice of thermal method.

## Research question

Guiding questions (see the manuscript for exact wording):
- **RQ1 — method sensitivity:** does the choice of thermal operationalisation (simple proxy
  vs SOLWEIG/UTCI) change tourism-feasibility classifications, and is any difference
  physically interpretable?
- **RQ2 — decision-support value:** does constraint-first screening change the feasible
  candidate set relative to a proximity-only nearest-open baseline, and can it return an
  explicit no-recommendation outcome?
- **RQ3 — robustness/traceability:** do those decisions stay auditable and stable under the
  tested uncertainty?

## Study area

Prado–Retiro–Atocha, central Madrid — a bounded pilot of ≈ 3.5 km² with **27 curated
tourism assets** (13 indoor, 14 outdoor). Study day **21 August 2023** (inside an
AEMET-designated extreme-heat episode); three timestamps: 12:00, 15:00, 18:00.
This is a purposive pilot, not a representative sample; no city-wide or climatological
inference is drawn.

## Methodological architecture

1. **Simple-proxy baseline** — ambient air-temperature hazard band (AEMET civil-protection
   thresholds) × OSM `natural=tree` exposure tercile → constraint-first feasibility.
2. **Physically based configuration** — SOLWEIG → mean radiant temperature (Tmrt) → UTCI
   (10 m buffer-mean), mapped to the same feasibility states.
3. **Thermal-method comparison** — paired reclassification over the 42 outdoor
   asset × timestamp observations.
4. **Uncertainty treatment** — evidence-derived envelope over tested solar-forcing and
   targeted geometry realizations; categorical ROBUST / BOUNDARY / UNSTABLE confidence.
5. **Constraint-first tourism screening** — ordered gate chain (open? → reachable? →
   thermally feasible? → evidence sufficient? → meaningful improvement?), first-failing-gate
   wins, machine-readable exclusion reasons, explicit no-survivor state; benchmarked against
   a proximity-only nearest-open baseline over eight pre-registered scenarios.

## Repository structure

```
manuscript/     manuscript sections, assembled TMP manuscript, tables, verified references
submission/     highlights, submission inventory
supplementary/  supplementary material (Figure S1, Tables S1–S4, reproducibility notes)
outputs/        locked result tables, maps, and publication figures + render scripts
data/           raw open-data inputs (data/raw) and processed/derived data (data/processed)
src/            analysis pipeline (study area, proxy, SOLWEIG runs, screening, validation)
app/            read-only Dash decision-support prototype (illustrative; not a result)
tests/          reproducibility/integrity checks
docs/           method records, provenance, and internal research/QA record (see note)
```

See `REPRODUCIBILITY.md` for the workflow and entry points, and
`docs/DATA_SOURCE_INVENTORY.csv` + `docs/PHASE1_DATA_PROVENANCE.md` for data provenance.

> **Note on `docs/`:** this folder contains both method/provenance records and the internal
> research/QA record (phase gates, audits, reviewer notes). It is kept versioned because the
> repository is **private**; a curated subset would be selected for any public release.

## Reproducibility

The reported tables and figures regenerate from the locked open-data inputs via the scripts
in `src/` and `outputs/publication/figures/`. Two Python environments are used (an analysis
environment and a dedicated SOLWEIG environment). Details, versions, and known limitations
are in `REPRODUCIBILITY.md`. Figure scripts assert their numeric values against the locked
tables before saving.

## Data provenance

All inputs are open data: AEMET (meteorology, warning thresholds), IGN/CNIG national LiDAR
(3-D urban geometry), and OpenStreetMap (tourism assets, tree points, park/garden polygons,
opening-hours tags), plus Madrid municipal open data (tree inventory, used in the targeted
geometry recheck). Each layer, its source, licence, and what it does **not** measure are
recorded in `docs/DATA_SOURCE_INVENTORY.csv`. No land-surface-temperature or satellite
thermal product was used. No AEMET API key or credential is stored in this repository.

## Publication status

Manuscript assembled and internally reviewed; references verified; publication figures
locked; targeted pre-submission revision in progress. Primary target journal: *Tourism
Management Perspectives*. Title is **provisional** (see `CITATION.cff`).

## Citation

See `CITATION.cff`. Author metadata is not yet finalised (placeholders present).

## Licence

**LICENSE DECISION REQUIRED** — no repository licence has been chosen yet. Third-party
datasets retain their original licences (AEMET open-data terms; IGN/CNIG CC-BY 4.0; OSM
ODbL; Madrid open-data terms) regardless of any licence later chosen for this code/text.

## Contact

[CONTACT / CORRESPONDING AUTHOR TO VERIFY]
