# HATI Spatial Decision Replay — isolated spike

This is a read-only inspection interface over the existing historical pilot.
It is not visitor guidance, new science, a field-validation exercise, a
publication revision or an operational service. Usefulness has not been tested
with reviewers. Follow [DESK_REVIEW.md](DESK_REVIEW.md) for that separate step.

## Baselines and boundaries

- Canonical scientific/repository commit: `036c50b273b539140260097760a148893176f7ec`.
- Phase 4.2 UI source: `e96baff16ee721140db13dc13171f571e458676a`.
- Foundation applied without conflicts as `b4074d0` on the isolated spike branch.
- Branch: `codex/hati-spatial-decision-replay-spike`.
- Seven approved scientific CSVs remain byte-identical to their recorded hashes.
- Protected data, scientific code, results, manuscript, publication files and
  existing scientific documentation must remain unchanged.

The original checkout is not the preview directory. Run all commands below
from the isolated worktree. The runtime never imports the scientific pipeline.

## Run

Use a Python 3.12 environment with the existing `app/requirements.lock.txt`.
For a new environment, create it in this isolated worktree, then install the
existing lock; do not install into the SOLWEIG environment.

```powershell
py -3.12 -m venv .venv_replay
.venv_replay/Scripts/python -m pip install -r app/requirements.lock.txt
.venv_replay/Scripts/python -B -m app.app
```

Open `http://127.0.0.1:8050`. The implementation session used the original
checkout's already-installed app interpreter read-only, with `-B`, instead of
changing that environment. This is not evidence of a clean lock-file install.

## Architecture

`replay_manifest.json` records the schema, commit pins, hashes, row keys,
source-column lineage, local-time basis, geography, methods and limitations.
`replay_contract.py` reads each file as bytes, checks SHA-256 before parsing,
then checks schema, identity, coverage, enums and scenario consistency.

Only the validated snapshot is cached. Its manifest is also held in memory.
`data_loader.frame()` returns defensive copies. Restart to validate/load again;
there is no hot reload of scientific data. Integrity failure renders an error
page with no map, candidate list or scientific facts. No permissive fallback
exists. The trust anchor is the versioned application/manifest and pinned Git
history; the app is not a tamper-proof signed distribution.

`replay_state.py` owns the small deterministic UI transition function. Scenario
selection binds source and time together. Asset selection retains that context.
Time changes clear it, and back navigation cannot revive it. Browser stores use
memory only: refresh resets to 12:00 with no asset/scenario, including when a URL
contains an old fragment. No URL scientific state is parsed.

The original persistent Leaflet map remains mounted. The marker layer adds
neutral text badges: `SRC` source, `IN` survivor, `OUT` excluded. These do not
replace thermal glyphs, decision colours, confidence rings or open-status
dimming. Evidence confidence remains an independently labelled panel field.
The searchable asset picker and all 26 candidate buttons provide alternatives
to map interaction. Excluded candidates stay on the map and in the list.

The panel reads the selected scenario-candidate record and its asset-time and
catalog records. It displays the recorded first failure, not a reconstructed
gate trace. Provenance disclosures show the row key, artifact hash, pinned link
and source columns. All 26 candidate buttons use stable asset-ID order, not
ranking. Source assets are shown separately and never counted as candidates.

At 12:00 the UI explicitly says “No precomputed scenario at this timestamp.”
Only asset-state inspection is available. Existing baseline-comparison and
reach-sensitivity components are preserved, but the linked replay panel does
not add those optional views or any controls to change scientific constraints.

## Tests

```powershell
.venv_replay/Scripts/python -B -m pytest -p no:cacheprovider tests -q
```

The browser script uses Node.js and Playwright as QA tooling, not as an app
framework. It expects the preview already running. Install/use Playwright in a
separate QA environment, or expose an existing installation with `NODE_PATH`.

```powershell
$env:HATI_PYTHON = (Resolve-Path .venv_replay/Scripts/python.exe).Path
node tests/replay/browser.cjs
```

Optional environment variables: `HATI_URL` (default localhost:8050),
`CHROMIUM_EXECUTABLE`, `FIREFOX_EXECUTABLE`, `NODE_PATH`.
The script reports missing browser executables as UNAVAILABLE, never PASS.
Set `HATI_PYTHON` to run the browser integrity test on port 8051. That helper
corrupts only a temporary copy of the CSVs and never changes the baseline.

Evidence is saved under `docs/replay/qa/`. Actual network tile rendering and
deliberately blocked tile requests are tested separately. No fixture tiles
or substitute geographic imagery are used.

## Scope limits

- One historical day, three fixed local times and 27 curated assets.
- No precomputed scenario at noon; only S1–S8, with their original bindings.
- Model-derived outdoor UTCI; indoor buffering is assumed and indoor UTCI null.
- Opening hours documented in 2026 are applied to 2023.
- Reach is straight-line, not a route or measured walking time.
- Confidence describes tested uncertainty, not safety or candidate eligibility.
- Browser tests establish implemented behavior, not usefulness or field validity.
- No routing, scores, ranking, new scenarios, live feeds, LLM decisions, 3D,
  publication changes, deployment or release.
