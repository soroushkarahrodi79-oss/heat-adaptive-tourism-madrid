# GATE1_DECISION — GO / MODIFY / NO-GO

**Version 0.1 · 2026-09-14.**

## Verdict

# MODIFY

Proceed to Gate 2 as a **Path-B robustness / evidence-sufficiency / abstention** study — not
as a routing, accuracy, comfort, behaviour, or health study — and only after two hard
preconditions (route network + study-day freeze) are met.

---

## 1. Decision rules (fixed before evaluation)

**GO** requires ALL of: (G1) one fixed auditable O-D comparison; (G2) plausible,
independently-checked pedestrian routes; (G3) usable hourly meteorological forcing; (G4)
dated/auditable geometry; (G5) documented uncertainty sources; (G6) ≥1 independent check;
(G7) a legitimate ABSTAIN outcome; (G8) a non-trivial scientific question surviving the
literature review.

**MODIFY** if modeling is feasible but pedestrian-level validation is unavailable, and/or
canopy/historical availability is imperfect, such that the valid claim must be reduced to
sensitivity/robustness/abstention — while a bounded, useful methodological question remains.

**NO-GO** if a timed route comparison cannot be supported; or essential
geometry/network/forcing is missing with no route to obtain it; or all plausible comparisons
are trivial; or uncertainty overwhelms every comparison **without** yielding a meaningful
evidence-sufficiency question; or the project requires validation/comfort/health claims that
cannot be independently evaluated.

## 2. Evaluation against GO criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| G1 | One fixed auditable O-D comparison | **PARTIAL** | OD1 (Atocha→Puerta de Alcalá) is fixed with two distinct alternatives, but the routes are not yet auditable because the network graph is not assembled. |
| G2 | Plausible, independently-checked routes | **FAIL (now)** | L05 pedestrian network + L06 access/crossing plausibility are **MISSING** in-repo. Acquirable within Gate-1 rules, but not yet done or audited. |
| G3 | Usable hourly forcing | **PASS** | Barajas 08221 hourly (L01), real observations; complete at target hours on candidate days. |
| G4 | Dated / auditable geometry | **PASS (with vintage caveat)** | PNOA-LiDAR 1st coverage 2008–2015, fully documented; auditable but ~decade-stale. |
| G5 | Documented uncertainty sources | **PASS** | Ledger L01–L14; perturbation set E-P1…E-P6; principal-uncertainty ranking. |
| G6 | ≥1 independent check | **WEAK PASS** | Retiro daily-max/monthly-mean + ERA5-Land context (L02). Real but daily/monthly only; not pedestrian-scale and not validation of Tmrt/UTCI. |
| G7 | Legitimate ABSTAIN outcome | **PASS** | ABSTAIN is a first-class result (NC1–NC7; decision-reversal rule). |
| G8 | Non-trivial surviving question | **PASS** | Abstention/evidence-sufficiency for comparative modeled exposure is unoccupied (`GATE1_LITERATURE_LOG.md`). |

**GO is not satisfied:** G2 fails now and G1 is only partial; pedestrian-level validation is
structurally unavailable (Path A impossible, Path B forced — `…DOSSIER.md` §1D).

## 3. Why MODIFY and not NO-GO

NO-GO would require that *no* meaningful evidence-sufficiency question survives, or that the
comparison is unsupportable in principle. Neither holds:

- The comparison **is** supportable in principle once L05/L06 are acquired (a bounded,
  in-scope task, not a bulk download).
- Uncertainty does **not** merely overwhelm the comparison — it **is the research object**:
  the Gate-0 question is precisely *when the correct answer is ABSTAIN*.
- A genuine, non-saturated question survives the 2026 literature (abstention/evidence
  sufficiency for comparative UTCI is not occupied).
- At least one (weak) independent check exists.

The verdict is therefore MODIFY: feasible, but with the claim ceiling lowered to Path B and
two preconditions attached.

## 4. Why MODIFY and not GO

- **No pedestrian-level validation, no path to it** — permanently caps the claim below
  accuracy/comfort/behaviour/health.
- **Route auditability not yet in hand** — L05/L06 MISSING.
- **Canopy vintage** can change the decision direction — the comparison must be reported as
  robustness/abstention, never as an accuracy statement.

Per the quality rule, MODIFY is **not** rescued into GO by adding model complexity; the fix
is to lower the claim and satisfy the preconditions, not to add SOLWEIG layers.

## 5. Conditions attached to MODIFY (must hold before any Gate-2 thermal run)

1. **Acquire + manually audit** the L05 pedestrian network and L06 access/crossings for both
   OD1 routes (bounded Overpass query for the two corridors only; walkability verified
   against imagery; polylines frozen + hashed).
2. **Freeze the study day** on rules R1–R6 (small AEMET metadata queries only); keep
   2023-08-21 strictly as legacy stress-test.
3. **Fix the claim ceiling** to Path B in all Gate-2 documents before any modeling.
4. **Assert the novelty boundary** against 2026 data-resolution-sensitivity-of-routing work.

If condition 1 cannot be met (routes prove un-auditable or not legally walkable), the case
does not upgrade — it becomes an ABSTAIN negative control, and the O-D case is reselected
from the backup (OD2) under the same rules.

## 6. Amendment note

No Gate-0 amendment is required by Gate 1. The missing-network finding and the
Path-B/MODIFY outcome are consistent with the Gate-0 MODIFY verdict and its claim ceiling; no
frozen Gate-0 decision was changed. Should Gate 2 reveal that even OD1+backup cannot yield an
auditable route pair, that *would* trigger `AMENDMENT_001.md` (re-examining the corridor or
the object), and it would be flagged as discovered **before** examining any outcome data.

---

*Gate 1 ends here — before any thermal modeling. No SOLWEIG/URock/UTCI was run; no large
dataset was downloaded; no synthetic validation evidence was created.*
