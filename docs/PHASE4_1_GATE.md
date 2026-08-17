# PHASE4_1_GATE.md — HATI-Madrid

Version 1.0 · 2026-08-18. Verdict decided against the Phase 4.1 validation
conditions set in the user's implementation charter and the Phase 4.0 gate
checks (`docs/PHASE4_0_GATE.md`), reproduced against the running app — not
re-derived criteria, and not a re-litigation of Phase 4.0's design.

## Validation conditions

| # | Condition | Status | Evidence |
|---|---|---|---|
| 1 | All three views work | Met | Drill-down map → asset → trade-off verified live; PHASE4_1_VISUAL_QA.md |
| 2 | Locked science preserved (no recompute; presentation only) | Met | `data_loader` has no write path; only filter/join/sort/count/translate; test `test_loader_is_read_only` |
| 3 | S8 works correctly | Met | `NoDefensibleAlternativePanel` (26 evaluated · 0 survived, excluded list expanded, no retry); test `test_s8_no_defensible` |
| 4 | A24 @ 18:00 uncertainty works | Met | Distinct UNSTABLE treatment + "irreducible boundary case" flag, distinct from BOUNDARY; test `test_a24_1800_unstable` |
| 5 | No opaque score / ranking | Met | No score/rank/rating/best column or label anywhere; "no ranking" framing explicit; test `test_no_score_or_ranking_fields` |
| 6 | Limitations remain visible | Met | Tier-1 context strip on all views + Tier-2 7-item drawer; tests + QA |
| 7 | Baseline mode uses pre-computed evidence only | Met | Renders `phase3_hati_vs_baseline.csv` row, "not recalculated"; test `test_baseline_uses_precomputed_row` |
| 8 | Protected artifacts unchanged | Met | `git diff` vs baseline `901954e` over protected paths is empty; 7-file SHA-256 match; test `test_protected_file_hashes` |
| 9 | Automated tests pass | Met | 14/14 pass (11 contract + 3 smoke), `tests/phase4_1/` |
| 10 | Visual QA finds no blocking communication defect | Met | PHASE4_1_VISUAL_QA.md; two defects found were fixed and re-verified |

Additional charter checks:
- Exactly the 3 valid timestamps offered, fixed date 2023-08-21, "not live"
  caption always visible — test `test_exactly_three_timestamps`, QA.
- 27 assets load — test `test_twenty_seven_assets`.
- Every exclusion token has a human-readable mapping — test
  `test_every_exclusion_token_mapped`.
- No live/real-time/forecast wording in user-facing copy — test
  `test_no_live_realtime_forecast_copy`.
- Five concepts stay on five separate channels — test
  `test_concepts_stay_separate`, QA channel table.

## Carried-forward risk

The Phase 4.0 gate's "discipline under implementation pressure" risk remains
the standing one: the no-score / five-separate-channels / always-visible-
uncertainty / S8-as-verdict guarantees are enforced by automated contract
tests, which any future change must keep green. The basemap depends on
network tiles at runtime (decision content does not). No field validation of
Tmrt/UTCI exists — surfaced permanently in Tier-2, unchanged from Phase 3.

## Verdict

# MVP IMPLEMENTATION VALIDATED

All ten validation conditions and all additional charter checks are met
against the running application, with protected Phase 0–3 artifacts proven
unchanged from the pre-implementation baseline. No Phase 5 work was started.
