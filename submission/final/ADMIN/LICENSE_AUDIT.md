# LICENSE_AUDIT.md — HATI-Madrid

No licence has been applied by this audit. This documents what exists and recommends a
structure; the actual choice is Soroush's.

## Third-party data terms (as documented in `docs/DATA_SOURCE_INVENTORY.csv` and
`docs/PHASE1_DATA_PROVENANCE.md`, cross-checked against README.md's Data sources table)

| Source | Role | Licence/terms | Redistribution note |
|---|---|---|---|
| AEMET (Barajas station; Meteoalerta thresholds) | meteorological forcing; hazard bands | Spanish open-data terms | Attribute AEMET; do not imply AEMET endorsement |
| IGN/CNIG national LiDAR (PNOA) | 3-D geometry for SOLWEIG | CC-BY 4.0 / IGN terms | CC-BY 4.0 requires attribution; compatible with redistribution of derived geometry if attributed |
| OpenStreetMap | tourism assets, tree points, park/garden polygons, opening hours | ODbL | **Share-alike / attribution obligations attach to the OSM-derived data itself** — any redistributed extract or derived database must credit OSM/OpenStreetMap contributors and, if it counts as a "derivative database" under ODbL, be shared under ODbL or a compatible licence. This affects `data/raw/`, `data/processed/`, and any table/figure that reproduces OSM-derived geometry directly. |
| Madrid open data — Arbolado | per-tree heights (targeted geometry recheck) | Madrid open-data terms | Municipal open-data reuse terms typically permit reuse with attribution; verify current terms before redistribution |
| Copernicus HRL Tree Cover Density (2018) | geometry-evidence cross-read | Copernicus licence (open) | Attribution required per Copernicus terms |
| EUMETSAT CM SAF | satellite irradiance sensitivity realization | EUMETSAT terms | EUMETSAT data terms vary by product; verify the specific CM SAF product's redistribution terms before including raw EUMETSAT data files in any public archive (derived, aggregated statistics are generally safer to redistribute than raw satellite fields) |

**No licence incompatible with these terms should be applied project-wide** — e.g. a
restrictive "all rights reserved" or a licence that purports to relicense OSM-derived data
outside ODbL would misstate the authors' actual rights over that data.

## Recommended structure (not applied — pending Soroush's decision)

Separate the licensing into three explicit scopes, as the closeout brief requires:

1. **Software licence** (for `src/`, `app/`, `scripts_assembly/`, `outputs/publication/*/render_*.py`,
   `tests/`) — a permissive open-source licence (e.g. MIT or Apache-2.0) is the common choice
   for research-pipeline code and is compatible with all the third-party terms above (none of
   them restrict how you licence your *own* code that merely reads their data).
2. **Documentation/content licence** (for `manuscript/`, `supplementary/`, `docs/`,
   `README.md`) — commonly CC-BY 4.0 for research documentation, but note the manuscript
   itself will typically be governed by the **journal's own copyright/licence agreement**
   once accepted (Tourism Management Perspectives, as an Elsevier subscription journal,
   requires an exclusive licence to publish or a CC-BY open-access licence if the OA route is
   paid for — see `PUBLISHING_RUNBOOK.md` for the open-access decision this implies). Do not
   apply a repository-wide content licence to the manuscript text that would conflict with
   whatever agreement is signed at acceptance.
3. **Third-party data terms** (for `data/raw/`, and any `data/processed/`/`outputs/` file that
   is a near-direct derivative of one input) — these are **not relicensed**; the repository
   should carry a `DATA_LICENSE` or a section in `REPRODUCIBILITY.md`/README pointing to each
   source's original terms (README.md's existing Data sources table already does most of
   this — it should be treated as authoritative and simply linked to, not duplicated with new
   claims).

## Explicit non-actions

- No `LICENSE` file has been added to the repository by this audit.
- No CITATION.cff `license:` field has been changed.
- This audit does **not** attribute rights to Soroush that he may not hold (e.g. it does not
  suggest relicensing OSM-derived extracts under a non-ODbL-compatible licence).

**Blocking status:** licence decision is a BLOCKER for Zenodo/DOI release (item 9 in
`HUMAN_INPUT_REQUIRED.md`), not for journal submission.
