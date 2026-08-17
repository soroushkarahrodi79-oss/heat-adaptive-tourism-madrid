# PHASE3_DECISION_ARCHITECTURE.md — HATI-Madrid Phase 3

Version 1.0 · 2026-08-17. The constraint-first screening architecture, its
separate decision fields, and its machine-readable exclusion vocabulary.

---

## 1. Constraint-first gate chain (no weighted scoring)

Each candidate is evaluated against a fixed, ordered sequence of hard
constraints. **The first failing gate wins**, and its reason is recorded; a
candidate that clears every gate becomes a `CANDIDATE_ALTERNATIVE`. Nothing is
silently dropped, and no gate is a weighted sum.

```
Candidate (for a given source, timestamp)
  │
  ├─ in pilot scope?           no ─▶ OUTSIDE_PILOT_SCOPE
  ├─ open at timestamp?        no ─▶ CLOSED_AT_TIMESTAMP
  ├─ within walking reach?     no ─▶ ACCESSIBILITY_CONSTRAINT
  ├─ thermal within limit?     no ─▶ THERMAL_LIMIT_EXCEEDED        (UTCI ≥ 46 °C, outdoor)
  ├─ evidence sufficient?      no ─▶ INSUFFICIENT_EVIDENCE          (evidence_confidence LOW)
  ├─ materially better than    no ─▶ NO_MEANINGFUL_THERMAL_IMPROVEMENT
  │   the source thermally?         │   (or OUTDOOR_EXPOSURE_TOO_HIGH if outdoor & hotter)
  ▼
  CANDIDATE_ALTERNATIVE  (trade-offs exposed, not ranked into one score)
```

Ordering rationale: cheap, categorical eliminations first (scope, open,
distance), then thermal safety, then evidence adequacy, then the source-relative
thermal-improvement test that is the point of a *heat-adaptive* screen. Because
the improvement test runs last, a candidate excluded for `CLOSED_AT_TIMESTAMP`
is never also mislabelled as thermally inadequate — each candidate carries
exactly one, most-fundamental reason.

## 2. Separate decision fields (never collapsed — carried from Phase 2.2)

The Phase 2.2 architectural rule is preserved and extended. Every candidate
record keeps these as **independent** fields:

| Field | Domain | Meaning |
|---|---|---|
| `thermal_state` | official UTCI category / `INDOOR_NOT_MODELLED` | physiological stress band (Bröde et al. 2012, unchanged) |
| `decision_state` | `OUTDOOR_FEASIBLE` / `AVOID_PROLONGED_OUTDOOR_EXPOSURE` / `AVOID_OUTDOOR_EXPOSURE` / `INDOOR_REFUGE` | tourism action implied by the thermal state |
| `decision_confidence` | `ROBUST` / `BOUNDARY` / `UNSTABLE` / `INDOOR_BYPASS` | Phase 2.2 uncertainty class of the thermal decision |
| `evidence_confidence` | `HIGH` / `MODERATE` / `LOW` | weakest link of (opening-hours completeness, thermal-evidence quality) |
| `exclusion_reason` | machine enum (below) or empty | why a candidate was excluded, or empty if it survives |

`evidence_confidence` is the **minimum** of the opening-hours completeness rank
(COMPLETE→HIGH, PARTIAL→MODERATE, MISSING→LOW) and the thermal-evidence rank
(ROBUST→HIGH, BOUNDARY→MODERATE, UNSTABLE→LOW; indoor→MODERATE because refuge is
assumed but A/C status is unverified and approach exposure is unmodelled). A
`LOW` value triggers `INSUFFICIENT_EVIDENCE`, so the Phase 2.2 UNSTABLE row
(A24 @ 18:00) propagates automatically into an evidence-based exclusion — the
uncertainty is not laundered away.

## 3. Machine-readable exclusion vocabulary

| Reason | Fires when |
|---|---|
| `OUTSIDE_PILOT_SCOPE` | candidate not in the 27-asset pilot (reserved; no in-pilot row uses it) |
| `CLOSED_AT_TIMESTAMP` | not open at the timestamp per catalog opening hours |
| `ACCESSIBILITY_CONSTRAINT` | straight-line distance from source exceeds the scenario's walking radius |
| `THERMAL_LIMIT_EXCEEDED` | outdoor candidate at UTCI ≥ 46 °C (`AVOID_OUTDOOR_EXPOSURE`) |
| `INSUFFICIENT_EVIDENCE` | `evidence_confidence == LOW` (e.g. UNSTABLE thermal decision or missing hours) |
| `NO_MEANINGFUL_THERMAL_IMPROVEMENT` | open/accessible/acceptable, but not ≥ Δ cooler and not a refuge |
| `OUTDOOR_EXPOSURE_TOO_HIGH` | outdoor candidate strictly hotter than the source |

Tourism-relevance is treated as satisfied for every pilot asset (all 27 are
curated tourism assets with OSM tourism/heritage tags and, for 24, Wikidata
IDs); the relevance evidence is carried in the record so a reviewer can audit
it, and experience-type is exposed so different experiences are not presented as
equivalent.

## 4. Output as trade-offs, not a ranking

Surviving candidates are returned as a set annotated with distance/walk-time,
indoor/outdoor, experience type, UTCI and its envelope, and decision/evidence
confidence. There is **no single "best alternative" number**. Where alternatives
serve different experience types (e.g. indoor cultural vs shaded green), the
trade-off is exposed rather than resolved by an opaque weight.

## 5. Baseline for comparison

A deliberately naive **nearest-open-in-radius** recommender (closest open
tourism asset within the same walking radius, with *no* thermal or evidence
screening) is computed for every scenario, to measure whether heat-aware
screening changes the option set a conventional tool would return
(`outputs/tables/phase3_hati_vs_baseline.csv`; results in
`docs/PHASE3_VALIDATION_REPORT.md`).
