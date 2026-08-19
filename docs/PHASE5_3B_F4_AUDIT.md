# PHASE5_3B_F4_AUDIT.md — HATI-Madrid Phase 5.3B

Version 1.0 · 2026-08-18. Audit of `outputs/publication/figures/FIG04_SCREENING_CONSEQUENCE_v0.1.{pdf,svg,png}`
(script `render_fig04.py`). No new analysis; values read from locked tables and asserted at
render time.

---

## 1. Numerical checks (asserted in-script)

| Check | Required | Rendered | Status |
|---|---|---|---|
| Scenarios | 8 (S1–S8) | 8 | ✓ |
| Candidate set changed | 7/8 (S7 exception) | 7/8 | ✓ |
| Nearest-open pick removed by screening | 3/8 (S2, S6, S8) | 3/8, all OUTDOOR_EXPOSURE_TOO_HIGH | ✓ |
| Options removed (thermal/evidence) | 23 total | 2+3+6+1+3+2+0+6 = 23 | ✓ |
| Surviving-alternative counts | 9,6,4,8,7,9,6,0 | matches per-row bars | ✓ |
| S8 | 26 evaluated → 0 survive, NO_DEFENSIBLE_ALTERNATIVE | "0 of 26 survive → NO_DEFENSIBLE_ALTERNATIVE" | ✓ |

Source: `outputs/tables/phase3_hati_vs_baseline.csv`, `data/processed/phase3_scenarios_summary.csv`.

## 2. Design-safety checks

- **No ranked-best-option implication.** Bars encode the *count* of surviving alternatives
  (0–9), not a ranking or a single "best destination." No ordering by desirability. ✓
- **No behavioural / recommendation language.** Wording is "surviving alternatives",
  "passes screening", "removed", "no defensible alternative" — no "recommended", "best",
  "safe choice", "responsible", "should visit". ✓
- **S8 highlighted structurally, not morally.** Neutral blue rounded outline; label "an
  architectural outcome, not a ranked pick"; no warning icon, no red alarm, no "safe". ✓
- **No traffic-light semantics.** Baseline status uses neutral filled (●) vs open (○)
  markers with text ("passes screening" / "removed · OUTDOOR_EXPOSURE_TOO_HIGH"), not
  green/red. ✓
- **Exclusion vocabulary verbatim:** `OUTDOOR_EXPOSURE_TOO_HIGH`, `NO_DEFENSIBLE_ALTERNATIVE`
  match the machine enum. ✓

## 3. Tourism-management identity

Rows are named real attractions (Fuente de Neptuno, Puerta de Alcalá, Parque del Retiro…)
with time of day and walking reach; the comparison is against a "nearest-open" tourism
recommender. The figure reads as a tourism decision-support result, not an urban-climate
plot. ✓

## 4. Readability / accessibility

- Colour not sole carrier: ● vs ○ marker shape + text label carry baseline status; bar
  length + printed count carry surviving-set size; S8 uses outline + text.
- Grayscale-safe: filled vs open markers and bar lengths remain legible without colour; the
  single blue accent (S8 outline / S8 bar-text) is non-essential to meaning (text carries it).
- No overlapping labels after header split; long source names truncated with ellipsis; no
  clipping. Legible at ~180 mm width.

## 5. Manuscript-claim support

Directly supports Results §4.2 / Discussion §5.2–5.3 (C5/C6/C7): heat-aware screening
changes the option set a nearest-open tool returns (7/8), removes hot outdoor nearest-open
picks (3/8), and can return an explicit no-defensible-alternative outcome (S8) — with no
ranking or behavioural claim. ✓

---

## GATE

8 scenarios; 7/8 change, 3/8 baseline failures, 23 removed, and S8 26→0 → NO_DEFENSIBLE_ALTERNATIVE
are exact and render-asserted; no ranked-best or behavioural framing; S8 highlighted
structurally not morally; neutral markers, no traffic-light semantics; tourism-management
identity visually clear.

**F4 VISUAL LOCKED**
