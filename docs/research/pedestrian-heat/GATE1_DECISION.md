# GATE1_DECISION — GO / MODIFY / NO-GO

**Version 0.3 · 2026-09-14 (revised after GATE1_EVIDENCE_CORRECTION_2026-09-14 and the
pre-merge methodological consistency pass).**

## Verdict

# MODIFY

Proceed to Gate 2 as a **Path-B robustness / evidence-sufficiency / abstention** study — not
as a routing, accuracy, comfort, behaviour, or health study — and only after two hard
preconditions (route network + study-day freeze) are met.

> **Correction note (2026-09-14):** the verdict is unchanged, but two inputs strengthened —
> an independent **urban hourly** Ta/RH check now exists near OD1 (Escuelas Aguirre; G6 upgraded
> from WEAK PASS to PASS) and geometry vintage improves via Madrid MDS 2023 / MDT 2019 (G4).
> Path A is corrected from *impossible* to *not currently available*. The two GO-blockers
> (Path B; L05/L06 MISSING) remain, so MODIFY holds — now closer to GO, blocked primarily by
> Path B rather than by a weak check.
>
> **Pre-merge consistency pass (2026-09-14):** four methodological fixes — (i) MDS 2023 − MDT
> 2019 is a *normalized surface height*, not a building/canopy raster (classification is a new
> OPEN input, L17); (ii) the single ∫UTCI dt scalar is **removed** for a multi-metric outcome
> set; (iii) E-P3 wind is **demoted** from a frozen perturbation to an unresolved limitation /
> ABSTAIN trigger; (iv) a real FROZEN-vs-OPEN boundary is drawn in the experiment spec. These
> tighten the record and add preconditions (L17; metric freeze); **none invalidates MODIFY** —
> no comparison was over-resolved and no scope was expanded. The verdict stands.

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
| G4 | Dated / auditable geometry | **PASS (vintage improved; classification OPEN)** | Madrid MDS 2023 / MDT 2019 (L15) give a near-contemporaneous *surface* for a 2023+ day; turning it into building/canopy layers needs an audited footprint source + vegetation mask (**L17, OPEN** — a Gate-2 precondition, not a Gate-1 blocker to feasibility). PNOA 2008–2015 (L03/L04) retained as cross-check; tree inventory (L16) audits current canopy. |
| G5 | Documented uncertainty sources | **PASS** | Ledger L01–L17; perturbation dimensions E-P1/E-P2/E-P4/E-P5/E-P6 (E-P3 wind demoted); multi-metric outcome set (∫UTCI dt removed); principal-uncertainty ranking. |
| G6 | ≥1 independent check | **PASS (upgraded 2026-09-14)** | Independent **urban hourly Ta/RH** at Escuelas Aguirre, adjacent to OD1 (L02). Retiro daily/monthly + ERA5-Land are regional context. Still not pedestrian-scale and not validation of Tmrt/UTCI (wind/radiation remain non-corridor-local). |
| G7 | Legitimate ABSTAIN outcome | **PASS** | ABSTAIN is a first-class result (NC1–NC7; decision-reversal rule). |
| G8 | Non-trivial surviving question | **PASS** | Abstention/evidence-sufficiency for comparative modeled exposure is unoccupied (`GATE1_LITERATURE_LOG.md`). |

**GO is not satisfied:** G2 fails now and G1 is only partial; pedestrian-level validation is
**not currently available** (Path B operative — `…DOSSIER.md` §1D). G4 and G6 are no longer
the binding constraints after the correction; **L05/L06 (routes not auditable) and Path B are.**

## 3. Why MODIFY and not NO-GO

NO-GO would require that *no* meaningful evidence-sufficiency question survives, or that the
comparison is unsupportable in principle. Neither holds:

- The comparison **is** supportable in principle once L05/L06 are acquired (a bounded,
  in-scope task, not a bulk download).
- Uncertainty does **not** merely overwhelm the comparison — it **is the research object**:
  the Gate-0 question is precisely *when the correct answer is ABSTAIN*.
- A genuine, non-saturated question survives the 2026 literature (abstention/evidence
  sufficiency for comparative UTCI is not occupied).
- A genuine independent **urban hourly** check exists (Escuelas Aguirre Ta/RH), upgraded from
  the earlier weak daily/monthly one.

The verdict is therefore MODIFY: feasible, but with the claim ceiling lowered to Path B and
two preconditions attached.

## 4. Why MODIFY and not GO

- **No pedestrian-level validation currently available** — caps the claim below
  accuracy/comfort/behaviour/health while Path B holds (Path A is *not currently available*,
  not impossible; an in-situ transect would reopen it).
- **Route auditability not yet in hand** — L05/L06 MISSING.
- **Canopy geometry** can still change the decision direction (even after MDS 2023 + tree
  inventory reduce the vintage gap) — the comparison must be reported as robustness/abstention,
  never as an accuracy statement.

Per the quality rule, MODIFY is **not** rescued into GO by adding model complexity; the fix
is to lower the claim and satisfy the preconditions, not to add SOLWEIG layers.

## 5. Conditions attached to MODIFY (must hold before any Gate-2 thermal run)

1. **Acquire + manually audit** the L05 pedestrian network and L06 access/crossings for both
   OD1 routes (bounded Overpass query for the two corridors only; walkability verified
   against imagery; polylines frozen + hashed).
2. **Freeze the study day** on rules R1–R7 — prefer a fresh 2023/2024 heat day aligned to
   MDS 2023 geometry and the Escuelas Aguirre hourly check (small AEMET + municipal metadata
   queries only); keep 2023-08-21 strictly as legacy stress-test.
3. **Fix the claim ceiling** to Path B in all Gate-2 documents before any modeling.
4. **Assert the novelty boundary** against 2026 data-resolution-sensitivity-of-routing work.
5. **Acquire geometry by bounded clip** — MDT 2019 + MDS 2023 clipped to OD1 only (not a
   city-wide raster download), PNOA retained as cross-check; confirm the Escuelas Aguirre
   hourly file actually covers the chosen day/hours (else forcing uncertainty → ABSTAIN, E-P1).
6. **Resolve geometry classification (L17, OPEN)** — audit a building-footprint source (to
   classify the MDS 2023 − MDT 2019 normalized surface height into buildings) and a justified
   vegetation mask (before reading MDS height as canopy). Unresolved classification is an
   ABSTAIN trigger, not something to assume away.
7. **Freeze outcome metrics** — lock the multi-metric set (∫UTCI dt removed; no
   "heat/physiological dose") and the exact UTCI category boundaries before any thermal output;
   keep spatial wind as a demoted (E-P3) unresolved limitation, not a frozen perturbation.

If condition 1 cannot be met (routes prove un-auditable or not legally walkable), the case
does not upgrade — it becomes an ABSTAIN negative control, and the O-D case is reselected
from the backup (OD2) under the same rules.

## 6. Amendment note

No Gate-0 amendment is required by Gate 1, and none by the 2026-09-14 evidence correction:
the corrected data availability (urban hourly Ta/RH; MDS 2023 geometry; tree inventory)
strengthens feasibility inside the *existing* Gate-0 research object and claim ceiling — it
does not change the research question, so `RESEARCH_PROTOCOL_V0.1.md` is untouched. The
missing-network finding and the Path-B/MODIFY outcome remain consistent with the Gate-0
MODIFY verdict; no frozen Gate-0 decision was changed. Should Gate 2 reveal that even
OD1+backup cannot yield an auditable route pair, that *would* trigger `AMENDMENT_001.md`
(re-examining the corridor or the object), flagged as discovered **before** examining any
outcome data.

---

*Gate 1 ends here — before any thermal modeling. No SOLWEIG/URock/UTCI was run; no large
dataset was downloaded; no synthetic validation evidence was created.*
