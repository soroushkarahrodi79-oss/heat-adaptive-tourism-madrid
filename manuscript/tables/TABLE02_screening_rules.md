# Table 2. Constraint-first screening architecture

Source: `docs/PHASE3_DECISION_ARCHITECTURE.md`, `src/thresholds.py` (locked). Each candidate
is evaluated against the ordered gates below; the **first failing gate wins** and records
the exclusion reason. There is no weighted or composite score.

## (a) Ordered gate chain and exclusion vocabulary

| Order | Gate | Condition to pass | Exclusion reason if failed (machine-readable) |
|---|---|---|---|
| 1 | Pilot scope | Candidate is one of the 27 pilot assets | `OUTSIDE_PILOT_SCOPE` (reserved; unused in-pilot) |
| 2 | Open | Open at the timestamp (per catalog opening hours) | `CLOSED_AT_TIMESTAMP` |
| 3 | Accessibility | Straight-line distance ≤ scenario walking radius | `ACCESSIBILITY_CONSTRAINT` |
| 4 | Thermal limit (outdoor) | Modelled UTCI < 46 °C | `THERMAL_LIMIT_EXCEEDED` |
| 5 | Evidence sufficiency | `evidence_confidence` ≠ LOW | `INSUFFICIENT_EVIDENCE` |
| 6 | Meaningful improvement | ≥ Δ cooler / lower UTCI category / refuge / confidence gain, and not hotter (outdoor) | `NO_MEANINGFUL_THERMAL_IMPROVEMENT` or `OUTDOOR_EXPOSURE_TOO_HIGH` (outdoor & hotter) |
| — | Survives all gates | — | `CANDIDATE_ALTERNATIVE` (surviving alternative) |

## (b) Key thresholds

| Parameter | Value | Origin |
|---|---|---|
| Hazard bands (proxy) | 36 / 39 / 42 °C air temperature | AEMET civil-protection warning scale |
| Exposure bands (proxy) | tree-count terciles (q1 = 0.33, q2 = 3.67 trees) | empirical within-pilot split (14 outdoor assets); not a transferable constant |
| UTCI feasibility map (physical) | ≥ 46 → NOT RECOMMENDED; 32–46 → FEASIBLE WITH CONDITIONS; < 32 → FEASIBLE | pre-registered; UTCI category boundaries (Bröde et al., 2012) |
| Accessibility reach | 800 m primary; 500 / 1200 m sensitivity | straight-line at 4.8 km/h (lower bound on walking distance) |
| Meaningful-improvement margin Δ | 0.8 °C | median per-row demonstrated UTCI sensitivity across the 42 outdoor rows |

## (c) Separate decision fields (never collapsed)

| Field | Domain |
|---|---|
| `thermal_state` | official UTCI category / `INDOOR_NOT_MODELLED` |
| `decision_state` | OUTDOOR_FEASIBLE / AVOID_PROLONGED_OUTDOOR_EXPOSURE / AVOID_OUTDOOR_EXPOSURE / INDOOR_REFUGE |
| `decision_confidence` | ROBUST / BOUNDARY / UNSTABLE / INDOOR_BYPASS |
| `evidence_confidence` | HIGH / MODERATE / LOW (weakest link of opening-hours completeness and thermal-evidence quality) |
| `exclusion_reason` | one machine enum from (a), or empty if the candidate survives |

*Note:* the scenario-level outcome `NO_DEFENSIBLE_ALTERNATIVE` is returned when no candidate
clears every gate; `ALTERNATIVES_FOUND` when at least one does.
