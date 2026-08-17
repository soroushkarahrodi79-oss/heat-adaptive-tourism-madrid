# PHASE1_1_GATE.md — Phase 1.1 gate decision

Version 1.0 · 2026-08-17

---

## VERDICT: REVISE BASELINE AGAIN

The five explicit conditions for **GO TO SOLWEIG / UTCI** are evaluated below.
Four are met. One is not, and the task specification requires **all** of them.

| # | Condition | Met? | Evidence |
|---|---|---|---|
| 1 | Meteorological provenance is scientifically acceptable | **Yes** | Audit 1: a thorough, documented attempt to obtain real Retiro hourly data failed for concrete, stated reasons (API key required, paid manual service, non-scrapable aggregator, previously-rejected model-derived source); Barajas is retained with an explicit, quantified representativeness bound (+0.5°C daily-max, +0.11°C monthly-mean vs. Retiro's official figures) rather than an unquantified hand-wave. |
| 2 | Hazard terminology is corrected | **Yes** | Renamed to METEOROLOGICAL HAZARD gate throughout code and docs, with an explicit statement that it is not, and must not be read as, a thermal-comfort index (UTCI/PET/WBGT). No prior mischaracterisation was found, so this is a precision hardening, not a bug fix. |
| 3 | No unvalidated branch is presented as validated | **Yes** | The EXTREME branch, previously implemented-but-untested, is now empirically validated against a real, AEMET-confirmed 2021-08-14 reading (Audit 2) and behaves exactly as designed. No other branch is claimed validated without support. |
| 4 | Adaptation gate is demonstrably useful or removed/demoted | **Yes** | Audit 3: three independent real-data tests (27 core assets, a threshold-sensitivity grid, a 6-asset real ring extension) all found zero discriminatory power at any defensible distance. The exclusionary rule was removed; the underlying data remains as reported context, not a decorative gate. |
| 5 | **Classifications are not excessively sensitive to the choice of simple shade proxy** | **No** | Audit 4: 10 of 14 outdoor assets (71%) have a feasibility classification that changes depending on which of three defensible, real-data shade proxies is used. Even the two most comparable, both-legitimate vegetation proxies (tree count vs. green-polygon coverage) disagree on 19% of outdoor-asset-timestamps. |

Because condition 5 fails, the verdict cannot be GO TO SOLWEIG / UTCI, however
strong the other four results are. STOP is not indicated either: nothing found
in any of the four audits invalidates the project's premise, contradicts
Phase 0's findings, or reveals an unsupportable claim already made — three of
four audits produced clean, positive, strengthening results, and the fourth
identified a specific, diagnosable, fixable weakness rather than a fatal flaw.

## Why condition 5 is treated as decisive, not a rounding error

A reviewer could reasonably ask whether 71% "unstable" overstates the problem,
since some of that instability comes from Proxy 3 (building density), which
Audit 4 also showed has a specific, explicable failure mode (it inverts for
park interiors — zero buildings there means "deep in parkland," not "unshaded").
Excluding Proxy 3 and looking only at the two most comparable, both-legitimate
vegetation proxies (tree count vs. green-polygon coverage), agreement is still
only 81% — a real 1-in-5 disagreement rate between two defensible ways of
measuring the same physical concept (nearby vegetation) using real, current
open data. Combined with Phase 1's own buffer-radius sensitivity finding
(`docs/PHASE1_VALIDATION_REPORT.md` §4), the exposure gate is the least stable
part of an otherwise now-hardened architecture. Publishing a classification
this sensitive to an arbitrary proxy choice, without resolving or at least
narrowing that sensitivity, would reopen exactly the "arbitrary weights"-style
critique the constraint-first design was built to avoid
(`docs/METHOD_OPTIONS.md`) — just relocated from the decision weights to the
input proxy.

## Specific, bounded revision before reconsidering SOLWEIG

Two paths, in order:

1. **Try one more, better simple proxy first**, per the project's standing
   "prefer the simplest reproducible stack" discipline. `docs/DATA_SOURCE_INVENTORY.csv`
   already rates the Copernicus HRL Tree Cover Density raster (10 m, continuous
   canopy-density %, not a point count) and Madrid Open Data's official Arbolado
   layer (per-tree, non-crowdsourced, with some size/species attributes) as
   "USE" but neither has been pulled into this project yet. Either is a
   same-architecture, same-engineering-budget swap-in for the exposure proxy
   (replace `tree_count_50m` with a canopy-density or verified-per-tree metric)
   that could plausibly narrow the Proxy-1-vs-Proxy-2 disagreement found here,
   without any SOLWEIG-class investment.
2. **Re-run Audit 4's exact comparison** (`src/audit4_shade_proxy_test.py`) with
   this improved proxy substituted for Proxy 1, and check whether agreement
   with Proxy 2 (green coverage) rises meaningfully above 81%. If it does not —
   i.e. if even a better point/raster-based proxy still disagrees substantially
   with an independent real vegetation signal — that result becomes the
   concrete, evidence-based justification for SOLWEIG: it would show that
   simple-proxy resolution has genuinely hit its ceiling and only real
   geometry (heights + canopy + sun-path, i.e. SOLWEIG's actual inputs) can
   adjudicate between competing simple measures. That is a legitimate way to
   arrive at "GO TO SOLWEIG" — earned by demonstrating simple proxies cannot
   converge, not skipped past because a comparison was never attempted.

Neither path requires PNOA LiDAR, Spanish Cadastre, or SOLWEIG itself. Both
stay within the same ~3.5 km² pilot footprint and the same engineering budget
already used throughout Phase 1 and Phase 1.1.

## What should NOT happen next

Per the task's explicit instruction and this project's standing scope
discipline: no SOLWEIG/Tmrt/UTCI computation, no dashboard, no ML, no
city-wide expansion, and no Phase 2 work of any kind until the revision above
is complete and re-evaluated against these same five conditions.
