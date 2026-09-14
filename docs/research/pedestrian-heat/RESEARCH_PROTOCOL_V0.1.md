# RESEARCH_PROTOCOL_V0.1 — Pedestrian Heat-Exposure Decision-Reliability Extension

**Status: Gate 0 record — FROZEN. Version 0.1 · transcribed 2026-09-14.**

> This file is the local, version-controlled record of the **Gate 0 protocol** for the
> pedestrian-heat research extension of HATI-Madrid. Gate 0 is **CLOSED**. This document
> did not previously exist in the repository; it is transcribed here verbatim-in-substance
> from the Gate 0 verdict so that later gates have an auditable frozen premise to build on.
> It **records** the Gate 0 decisions; it does not re-open or re-decide them.
>
> If a material reason to change any decision below is discovered, do **not** silently edit
> this file. Create `AMENDMENT_001.md` (see §7) stating what should change, why, whether the
> issue was found before or after examining outcome data, and which claims are affected.

---

## 1. Relationship to the locked HATI preprint

The HATI-Madrid preprint (single Madrid pilot, 21 Aug 2023, 27 curated assets,
operational-proxy vs SOLWEIG/UTCI screening comparison, 8 decision scenarios) is
**`RELEASE_LOCKED`** — archived under an immutable Zenodo DOI
(`10.5281/zenodo.22707470`) and republished on ResearchGate. See `PROJECT_STATUS.md`.

This extension **must not** modify, rewrite, reinterpret, or silently extend the locked
preprint or any of its validated/locked claims. It is a **separate, new research line** that
reuses the same corridor and some of the same open-data infrastructure. Its documents live
under `docs/research/pedestrian-heat/` and never alter a locked number, table, or figure.

The existing 21 Aug 2023 episode **must not** be used as independent validation of this
extension. It may later be retained **only** as a legacy stress-test, because it used
Barajas forcing, older (PNOA-LiDAR 1st-coverage, ~2008–2015) vegetation geometry, three
timestamps (12:00/15:00/18:00), and **no** direct pedestrian-level Tmrt/UTCI measurement.

## 2. Gate 0 verdict

**MODIFY.**

The originally-tempting novelty claims were **rejected** as already well-served by prior
research:

- heat-aware pedestrian routing itself;
- UTCI mapping itself;
- finding a "cooler" route;
- simply recommending a later visit time.

## 3. The narrowed candidate contribution (research object)

The research object is **not route optimisation**. It is:

> **Decision reliability + evidence sufficiency + uncertainty + abstention** for *modeled*
> comparative pedestrian thermal-exposure decisions relevant to tourism planning.

Stated as the defensible question Gate 0 kept:

> **When do open urban, meteorological and geospatial data provide sufficient evidence to
> support a comparative pedestrian thermal-exposure decision, and when is the uncertainty
> large enough that the scientifically correct result is ABSTAIN / NO EVIDENCE?**

## 4. Provisional study area

The Atocha–Prado–Retiro corridor, Madrid (the same bounding box as the locked pilot:
lat 40.4040–40.4210, lon −3.6960 to −3.6775; ~1.9 km N–S × 2.1 km E–W, ~3.5 km²).

## 5. Claim ceiling at this stage (hard cap)

The maximum scientific claim permitted is:

> **"robustness and evidence sufficiency of modeled comparative exposure."**

The following are **explicitly NOT** claimable at this stage:

- observed tourist exposure;
- validated pedestrian UTCI accuracy;
- thermal comfort (subjective);
- tourist behaviour;
- physiological heat stress;
- health benefit;
- realised adaptation benefit.

## 6. Standing prohibitions (epistemic guardrails)

- Do **not** treat another model run, ERA5-Land, the same meteorological forcing, or the
  previous HATI output as independent validation of pedestrian UTCI.
- Do **not** treat Sentinel-2 (or any optical product) as a thermal sensor or a direct
  land-surface-temperature observation.
- Do **not** equate UTCI with subjective thermal comfort; LST with pedestrian thermal
  exposure; tourists with generic pedestrians; modeled stability with accuracy; or
  reproducibility with validation.
- Do **not** infer behavioural response or health effects.
- Do **not** choose the route pair after seeing thermal outputs.
- Do **not** choose uncertainty ranges after seeing which ones preserve a preferred answer.
- Do **not** invent a "material UTCI difference" threshold (e.g. 1 °C, 2 °C) without a
  literature or data-provenance justification specific to this comparison type.

## 7. Amendment procedure

Any material change to §1–§6 requires a clearly-labelled `AMENDMENT_001.md` (then `_002`,
…) stating: (1) what should change; (2) why; (3) whether the issue was discovered **before
or after** examining outcome data; (4) which claims would be affected. Silent edits to this
frozen record are prohibited.
