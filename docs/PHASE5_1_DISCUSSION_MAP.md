# PHASE5_1_DISCUSSION_MAP.md — HATI-Madrid Phase 5.1

Version 1.0 · 2026-08-18. Maps each locked headline finding to the literature it
must be discussed against, and fixes the *allowed* interpretive frame for each.
**No Discussion prose drafted.** Citations key to
`docs/PHASE5_1_LITERATURE_MATRIX.csv`; findings key to
`docs/PHASE5_0_RESULTS_HIERARCHY.md` / `PHASE5_0_EVIDENCE_MATRIX.csv`.

**Standing rule for the whole Discussion:** the proxy-vs-physical comparison is
**method sensitivity**, never accuracy validation. No sentence may imply the
physical model is correct or the proxy is wrong.

---

### Finding H1 — 33.3% proxy-vs-physical reclassification (C1)
- **Compare against:** the composite tourism-climate-index tradition (HCI/TCI
  inter-comparison 2016; reliability of tourism climate indices 2016) and the
  LST-is-not-comfort literature ("Beyond LST" 2026); SOLWEIG-mapping precedent
  (Sustainable Cities and Society 2024).
- **Frame:** consistent with the established point that simple/air-temperature/
  surface proxies diverge from radiant-load indices — extended here to *tourism
  screening decisions*, which prior work did not quantify.
- **Forbidden:** "the model corrects the proxy"; "more accurate decisions".

### Finding H2 — 64.3% divergence at noon (C2, C3)
- **Compare against:** SOLWEIG/MRT literature showing shading/geometry drive Tmrt
  far more than air temperature (Urban Climate 2019; WRF-UCM-SOLWEIG 2024);
  radiation-estimation sensitivity in tourism-city UTCI (2022).
- **Frame:** mechanism — at low midday air temperature the radiant load already
  reaches strong-heat-stress UTCI, so an air-temperature-based proxy is blindest
  exactly when radiant load is high; a physically interpretable, not incidental,
  divergence.
- **Forbidden:** claiming the noon UTCI values are measured/validated.

### Finding H (both directions) — 9 more- / 5 less-restrictive (C4)
- **Compare against:** proxy-fragility evidence within the project's own lineage
  (Phase 1.2 proxy non-convergence, `shade_proxy_agreement.csv`) and MCDA
  weight-sensitivity work (GIS-MCDA sensitivity 2016).
- **Frame:** the divergence is not a one-way bias correction; method choice
  reshapes decisions in both directions, which is why it is a *decision variable*,
  not a calibration offset.
- **Forbidden:** "net conservative/liberal" framing implying a validated direction.

### Finding H3 — candidate set changes in 7/8 vs nearest-open baseline (C5, C6)
- **Compare against:** routing/accessibility work that presupposes destinations
  (Cool Routes 2026; CoolWalks 2025; UTCI-adjusted accessibility 2026) and
  conventional proximity/popularity recommenders (problem framing).
- **Frame:** heat-aware *screening* changes the option set a proximity tool would
  return — an upstream effect the routing literature cannot produce because it
  starts after the destination is chosen.
- **Forbidden:** claiming tourists would actually switch (behavioural).

### Finding H3b — naive nearest-open pick fails in 3/8 (C6)
- **Compare against:** tourism heat-governance framing (Annals of Tourism Research
  2026) — attraction closures/warnings as management levers.
- **Frame:** illustrates a concrete failure mode of proximity-only guidance under
  heat; motivates screening as a management-support layer.
- **Forbidden:** "prevents harm"/outcome claims.

### Finding H4 — no-defensible-alternative result, S8 (C7)
- **Compare against:** climate-shelter/refuge accessibility work where proximity
  alone is insufficient (Barcelona mobility justice 2025; refuge networks 2026).
- **Frame:** the architecture's ability to *decline* is a feature shared with
  equity-aware accessibility critiques — sometimes nothing nearby qualifies, and
  saying so is more honest than a forced recommendation.
- **Forbidden:** implying a behavioural "stay indoors" instruction.

### Finding H5 — robustness to tested solar forcing (C8, C9)
- **Compare against:** uncertainty-aware spatial decision support (participatory
  GIS under uncertainty 2025; Monte-Carlo UTCI/PET reliability 2025).
- **Frame:** we treat uncertainty as first-class but *categorical and separated*
  rather than propagated into one composite — a transparency choice; results are
  stable under the solar forcing actually tested.
- **Forbidden:** "fully quantified"/"validated"; naming untested uncertainties
  (humidity/wind/structural) as covered.

---

**Coverage check:** every Tier-1 headline in `PHASE5_0_RESULTS_HIERARCHY.md` has a
literature comparison set and a fixed non-accuracy frame. Tier-2/Tier-3 findings
(proxy non-convergence, exclusion traceability, geometry audit) are discussed only
as support and receive no independent comparison block.
