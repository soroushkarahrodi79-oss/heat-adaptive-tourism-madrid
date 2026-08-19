# GITHUB_INITIALIZATION_REPORT.md — HATI-Madrid

Version 1.0 · 2026-08-19. Record of placing the existing workspace under Git/GitHub version
control. No scientific content was modified.

## Repository
- **Name:** `heat-adaptive-tourism-madrid`
- **Remote URL:** https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid
- **Visibility:** **PRIVATE** (`isPrivate: true`)
- **Default branch:** `main` (renamed from the pre-existing local `master`)
- **Owner:** authenticated `gh` user `soroushkarahrodi79-oss` (personal account; no org)

## Preservation commit
- **SHA:** `beedbb1aaa9d18c7ac8d73892101692308670479`
- **Message:** `chore: preserve pre-submission HATI-Madrid research snapshot`
- Local `HEAD` == `origin/main` == `beedbb1` (verified).
- Tracked files after commit: **305**.

## Snapshot tag
- **Tag:** `pre-targeted-revision-v0.2` (annotated), points at `beedbb1`.
- **Meaning:** the exact scientific state immediately before the Phase 5.4B3 targeted
  pre-submission revision, so later revisions can be diffed against it.
- Pushed to remote (`refs/tags/pre-targeted-revision-v0.2`).

## Git history note
This repository pre-existed with two prior commits (`5364f3f` Phase 4.1; `901954e` Phase
4.0). The new snapshot commit builds on that history; no history was rewritten and no
force-push was used.

## Secret scan result
**CLEAN.** No `.env`, credentials, tokens, API keys, `.pem`/`.key`, or personal secrets found
(file-name scan and content scan). "token" matches are the Dash app's exclusion-reason
machine tokens / CSS; "api_key" mentions are documentation stating the project deliberately
did **not** use the AEMET API key (anonymous request; no key obtained). The `gh` OAuth token
lives in the OS keyring, not in the repo. A private working file of scientific-file hashes
(`.hati_science_baseline.json`) was created for the integrity check and **excluded from
tracking** via `.git/info/exclude`.

## Large-file decisions
Commit payload ≈ **70.5 MB** total; largest file **12.9 MB**; **no file > 50 MB** → **Git LFS
not required/used.** The only two files > 10 MB are Madrid municipal tree-inventory geodata
(`data/interim/madrid_arbolado_points.geojson`, `data/raw/madrid_arbolado/arbolado_parques_historicos_full.geojson`),
publicly downloadable from datos.madrid.es with provenance already documented in
`docs/DATA_SOURCE_INVENTORY.csv` / `docs/PHASE1_DATA_PROVENANCE.md`.
- **Decision:** COMMIT NORMALLY for this private snapshot (faithful preservation; within
  size limits). Flagged as candidates for *exclude + documented download* at public-release
  time (noted in `REPRODUCIBILITY.md`).

## Files excluded from tracking (via `.gitignore`)
Virtual environments (`.venv`, `.venv_solweig`, `.venv_app`), Python caches
(`__pycache__`, `*.pyc`, `.pytest_cache`, `.mypy_cache`, `.ipynb_checkpoints`), heavy
regenerable SOLWEIG interim caches (`data/interim/solweig*`), Dash runtime artefacts
(`*.log`, `.dash_cache`), OS/editor cruft, and defensively `.env*`, `*.pem/*.key/*token*`,
`temp/`, `cache/`, `scratch/`, `*.tmp`. Locked scientific outputs (`data/processed`,
`outputs/tables`, `outputs/maps`, `outputs/publication`) are **not** ignored.

## Files intentionally not pushed
Only the git-ignored categories above. All manuscript, figures, tables, source scripts,
tests, and provenance/QA docs are pushed. `.hati_science_baseline.json` (integrity helper)
is intentionally untracked.

## Reproducibility documentation status
Added: `README.md`, `REPRODUCIBILITY.md` (two-environment workflow, ordered scripts,
expected outputs, known limitations), `requirements.txt` (analysis env, pinned to the
versions actually used; SOLWEIG env documented separately), `CITATION.cff` (placeholders;
provisional title). Reproducibility is documented as a multi-step, two-interpreter workflow
(no fabricated one-command reproduction).

## Licence status
**LICENSE DECISION REQUIRED.** No repository licence exists or was chosen; not invented.
Third-party datasets retain their original licences (AEMET terms; IGN/CNIG CC-BY 4.0; OSM
ODbL; Madrid open-data terms) regardless.

## Git LFS usage
**None.**

## Scientific-content integrity
Hash check of 37 principal scientific files (manuscript, processed data, result tables,
publication figures) before vs after initialization: **0 changed.** The only additions are
repository scaffolding (README, REPRODUCIBILITY, requirements, CITATION, `.gitignore`
updates, this report) and Git metadata.

## Verification summary
Remote URL ✓ · branch `main` exists ✓ · commit `beedbb1` matches local ✓ · tag present ✓ ·
no secrets tracked ✓ · README/manuscript/figures/scripts present in commit ✓ · excluded
datasets documented ✓ · repository PRIVATE ✓.
