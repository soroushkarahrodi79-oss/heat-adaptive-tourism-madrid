# GATE3B_NEGATIVE_CONTROLS — NC1–NC7 evaluation

**Version 1.0 · 2026-09-15.** The negative controls test the **evidence-sufficiency logic**,
not model accuracy. A method that confidently resolves any of them has failed. Pre-declared in
Gate 2 (`GATE2_EVIDENCE_REPORT.md` §2I) before any thermal output.

| NC | Control | Evidence condition (frozen) | Gate-3B outcome |
|---|---|---|---|
| **NC1** | Effectively identical routes | method must NOT confidently separate near-identical routes | **PASS** — for OD1 the modeled A−B (0.05–0.37 °C) is within uncertainty and the method **abstained** rather than declaring a winner; the evidence-sufficiency logic behaved as required. (OD4/OD5 remain the dedicated identical-route seeds for a future run.) |
| **NC2** | Missing network link | any essential route link missing/unverified → ABSTAIN | **not triggered** — frozen routes have 0 UNRESOLVED segments (Gate 2). |
| **NC3** | Uncertain pedestrian access (park gate) | route depends on a gate with unresolved hours → ABSTAIN | **not triggered** — Route B held on the Alfonso XII street (0 park gates on route). |
| **NC4** | Unresolved canopy vintage | A−B separation depends on canopy pixels that another vintage/source contradicts → ABSTAIN | **FIRED** — the A−B ordering depends on the canopy state: PNOA 2008–2015 (EP2b) and the municipal tree-inventory (EP2c) **reverse** the 14:00 ordering vs the MDS-2023 baseline. |
| **NC5** | Missing meteorological variable | forcing gap / non-clear sky / >5 % missing pixels → refuse, do not interpolate | **not triggered** — forcing complete, coco=1, 0 % nodata across all fields. |
| **NC6** | Category-boundary case | a category metric's uncertainty interval contains a UTCI cut-point → ABSTAIN | **BORDERLINE/FLAGGED** — route point-max UTCI 45.0–45.9 °C hugs the +46 °C extreme boundary across perturbations (not crossed in the mean, but within the ensemble margin). |
| **NC7** | Justified-assumption reversal | A−B ordering flips between justified perturbation states → ABSTAIN (canonical trigger) | **FIRED** — the intensity ordering sign reverses under E-P2 canopy states (14:00) and E-P5 side-of-street (both departures). |

## Conclusion
The pre-registered controls behaved exactly as designed: **NC7 and NC4 fired** (canopy /
assumption-reversal), **NC6 is flagged** (boundary proximity), and **NC1 passed** (the method
declined to over-resolve a within-noise difference). No control indicates a broken method; they
collectively mandate **ABSTAIN**. This is the evidence-sufficiency machinery working — the
correct, first-class outcome of the Gate-0 research object, not a failure.
