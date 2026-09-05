# Spike validation — 5 September 2026

Technical disposition: **PR_READY** after a bounded project-owner desk review.
The owner judged the spatial replay useful for inspecting scenario membership,
exclusions and provenance and authorized promotion to a pull request. This is
not formal usability validation, a user study, accessibility certification,
scientific validation or physical field validation.

## Repository verification

Remote main was verified as `036c50b273b539140260097760a148893176f7ec`
before work. Phase 4.2's parent was verified as `c317d80`, and its changed-file
scope contained only app/UI, UI tests and UI documentation. It applied without
conflicts as `b4074d0` in the isolated branch.

Protected paths have an empty diff against canonical main: data, scientific
code, outputs, manuscript, supplementary material, submission files, assembly
scripts, README and REPRODUCIBILITY. Existing scientific documentation is
unchanged; the foundation adds its historical UI docs and the spike adds only
`docs/replay/`. No publication or targeted-revision branch was incorporated.

The original checkout remains on `claude/phase-4-2-ui-ux-redesign-swywzi` at
`e96baff`, with no tracked changes. Its `.claude/` directory was not edited.
Worktree/branch creation and fetch necessarily updated shared Git metadata;
neither changed the original checked-out files or local main.

All seven hashes matched before implementation and at final verification.
See [qa/integrity-results.json](qa/integrity-results.json) for expected and
actual values. No scientific pipeline was run. Runtime changes consist of
validation, lookups, joins, counts, formatting and UI state transitions; no new
scientific calculation or external scientific feed is present.

## Clean-environment and Python regression results

A separate temporary Python 3.12 virtual environment was created outside the
repository. Installation from the complete 53-line
`app/requirements.lock.txt` succeeded without fallback to global packages or
the existing app/SOLWEIG environments. The clean interpreter loaded and
validated the manifest, produced record counts 27/81/208, imported Dash,
constructed a `Div` layout with nine callbacks, and started the HTTP app.

The final test and browser results below were produced against this clean
environment. No dependency or setup defect required a code or lock change.

Final command: `python -B -m pytest -p no:cacheprovider tests -q`.
**122 passed in 24.61 seconds** in the clean environment: all 95 existing
tests plus 27 replay tests.
The new tests exercise actual hash failure on a temporary copy, blocked error
layout, schema/identity/binding failures, exact map-role and survivor sets,
source/candidate separation, deterministic reads and invalid state clearing.

Clean environment: Python 3.12.10; Dash 4.4.1; dash-leaflet 1.1.3;
dash-mantine-components 2.8.0; dash-svg 0.0.12; pandas 2.3.3; pytest 8.4.2.
These direct package versions match the app pins, and the complete transitive
lock was installed successfully.

## Scenario fidelity

27 catalog assets, 81 asset-time records and 208 scenario-candidate records.
Every scenario has 26 candidates, with the source represented separately.
Exact survivor IDs are checked against immutable scenario outputs and their
summary records, not merely against these counts.

| Scenario | Survivors | Excluded |
|---|---:|---:|
| S1 | 9 | 17 |
| S2 | 6 | 20 |
| S3 | 4 | 22 |
| S4 | 8 | 18 |
| S5 | 7 | 19 |
| S6 | 9 | 17 |
| S7 | 6 | 20 |
| S8 | 0 | 26 |

S8 first-failure groups: 15 ACCESSIBILITY_CONSTRAINT,
6 OUTDOOR_EXPOSURE_TOO_HIGH, 5 CLOSED_AT_TIMESTAMP. The copy now correctly
describes the full candidate universe, not 26 assets inside 500 m.
A24 is an EXCLUDED/INSUFFICIENT_EVIDENCE candidate in S4 and the explicitly
UNSTABLE/LOW source in S7. No noon scenario is inferred.

## Browser and accessibility results

[qa/browser-results.json](qa/browser-results.json) is the machine-produced
result of `tests/replay/browser.cjs`.

- Chromium 149.0.7827.55 against the clean environment: **PASS**. All eight scenario map/list counts,
  candidate selection, pinned provenance, source/candidate distinction,
  back/close, timestamp invalidation, refresh reset and integrity blocking.
- Real basemap run: **28 loaded tiles, 0 failed** at the initial sampled view.
  This is actual CARTO/OSM tile rendering, not a synthetic tile fixture.
- Separate blocked-tile run: markers, candidate records and provenance remain
  available; the UI states that the basemap is unavailable.
- Desktop 1440×900, narrow 900×844 and mobile 390×844 exercised. No horizontal
  overflow; header and panel remain within the viewport after selection.
- Keyboard candidate activation, Space marker activation, Escape overlay
  dismissal and selected-record focus exercised.
- Firefox executable: **UNAVAILABLE**, not tested.
- Screen reader: **NOT EXECUTED**. No running NVDA/Narrator session or
  controllable native screen-reader execution surface was available. No
  screen-reader certification is claimed.

Screenshots were inspected for the actual desktop evidence and mobile states.
The first responsive run exposed a real viewport overflow: focus scrolling
could move the command bar offscreen because the old 55vh map plus 45vh panel
ignored header height. The fix sizes them within the remaining workspace.
The final browser test checks this invariant. The test also waits for scenario
focus completion before keyboard candidate selection to avoid testing an
unfinished transition.

## Remaining limitations

No formal usability study or field validation has occurred. Markers/badges can
overlap at broad zoom levels; all candidates remain accessible through the
list and asset picker. Small screens require panel scrolling. Refresh resets
rather than restoring a shareable URL state. Basemap availability is external;
scientific records remain local. Confidence/thermal semantics still warrant
broader reviewer comprehension testing. Broader browser, zoom and
assistive-technology coverage remains future verification, not an implied pass.

No merge, push, PR, deployment, public release or publication-status change.
See [DESK_REVIEW.md](DESK_REVIEW.md) for the bounded owner disposition and the
protocol for any future review.
