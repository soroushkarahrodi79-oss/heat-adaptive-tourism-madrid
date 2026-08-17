"""
PHASE 1.2 PRE-REGISTRATION — written and committed BEFORE any proxy value is
computed or any agreement result is inspected. This module is imported by
src/shade_proxy_comparison.py; nothing here may be edited after results are
seen (see docs/PHASE1_2_SHADE_EVIDENCE_GATE.md, which states the wall-clock
order of operations).

=== COMMON SPATIAL UNIT (decided in advance) ===

PRIMARY_BUFFER_M = 50 metres, a circular buffer around each outdoor pilot
asset's representative point (latitude/longitude from
data/processed/pilot_assets.csv), applied UNIFORMLY to P1, P2, and P3.

Rationale for 50 m, not chosen from a range of options after seeing which
produces the best agreement:
  - It is the SAME buffer already used and documented for the Phase 1
    baseline's point-type assets (src/thresholds.py EXPOSURE_BUFFER_M) and for
    Phase 1.1 Audit 4's Proxy 2/3 (src/audit4_shade_proxy_test.py BUFFER_M).
    Reusing an already-justified, already-documented project convention is
    the opposite of tuning a new number to manufacture agreement.
  - It approximates the immediate pedestrian standing/queueing area around a
    tourism asset (Madrid city blocks in this area run ~80-120 m per side, so
    50 m stays within the local block rather than reaching into an unrelated
    neighbouring micro-environment).

P0 (the OSM tree-count baseline) is EXEMPT from this uniform buffer rule: per
the task specification, P0 retains the exact Phase 1 historical computation
unchanged (point+50m for monument/building assets, OR the asset's own real
polygon+15m for the 8 assets that are themselves park/garden polygons - see
src/build_classifications.py:count_trees_for_asset). This is intentional
inconsistency for the sake of NOT "improving it retrospectively" - P0 is a
frozen historical reference, not a fourth arm of the new, consistently-built
comparison.

=== SENSITIVITY (NOT the gate decision) ===

25 m and 100 m circular buffers are ALSO computed for P1/P2/P3, reported
separately in docs/PHASE1_2_SHADE_EVIDENCE_GATE.md as a sensitivity check on
the 50 m choice. They do NOT feed the predefined 85%/20% gate criteria and
are never used to pick a "better" buffer after the fact.

=== CLASSIFICATION METHOD (decided in advance) ===

Every proxy's raw value is converted to LOW/MODERATE/HIGH exposure_state by
an EMPIRICAL TERCILE split of that proxy's own distribution across the 14
outdoor pilot assets - the same method already used throughout this project
(src/thresholds.py EXPOSURE_METHOD_NOTE) because no literature threshold
exists for "trees per 50 m" or "% canopy cover per 50 m near a tourism POI"
as a shade-sufficiency criterion. This is explicitly labelled an empirical
sensitivity-grade category, not a physically justified threshold, exactly as
the task's NORMALISATION/CLASSIFICATION section requires. No composite score
or weighting is used anywhere.

P0 is exempt from re-tercile-ing: it reuses its own already-published Phase 1
exposure_state values verbatim (q1=0.33, q2=3.67 trees, computed once in
Phase 1 and never touched since).

P3 (green-polygon coverage) is exempt from re-tercile-ing here too: it reuses
Phase 1.1 Audit 4's already-published Proxy 2 exposure_state values verbatim
(q1=48.27%, q2=100.0%), per the task's explicit instruction to "retain" it.

Only P1 and P2 have their tercile cutpoints computed fresh in this phase,
because they are new proxies with no prior published cutpoint.

=== FEASIBILITY TRANSLATION (decided in advance) ===

Each proxy's exposure_state feeds the SAME, UNMODIFIED
src/thresholds.py:FEASIBILITY_RULES_OUTDOOR / feasibility_decision() logic
already in production since Phase 1 (meteorological hazard gate unchanged;
adaptation indicator remains demoted per Phase 1.1). Only the exposure_state
input varies by proxy. This isolates the proxy's marginal effect exactly as
Phase 1.1 Audit 4 did, extended from 3 to 4 proxies.

Real hazard timestamps used: the same three 2023-08-21 local times as every
prior phase (12:00, 15:00, 18:00) - see src/build_classifications.py
TIMESTAMPS. No new episode is introduced.
"""

PRIMARY_BUFFER_M = 50
SENSITIVITY_BUFFERS_M = (25, 100)
