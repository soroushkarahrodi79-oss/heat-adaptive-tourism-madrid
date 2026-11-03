# BIBLIOGRAPHIC_AUDIT_v0.3.md — HATI-Madrid

Version 1.0 · 2026-11-03. Targeted bibliographic audit of `manuscript/MANUSCRIPT_v0.3_DRAFT.md`,
requested after a university reviewer flagged weaknesses in the project's bibliography (raised
before PR #18; not yet addressed for v0.3). Scope: the 15 references actually cited in v0.3, plus
five named candidate prior-art items, plus a targeted (non-systematic) search of five topic
clusters. Does not touch code, CSVs, tests or SOLWEIG. No reference was added to pad the count;
two were added because they change how the manuscript's own stated knowledge gap must be read.

Reuses `manuscript/REFERENCES_VERIFIED_v1.md` and `docs/PHASE5_4B1_REFERENCE_VERIFICATION.csv`
(frozen metadata-verification records from 2026-08-19) as the base list; this document does not
rewrite them. It audits **claim support** — whether each citation's use in v0.3 matches what the
source actually investigated — which the 2026-08-19 process explicitly checked only at
abstract level (`PHASE5_4B1_REFERENCE_CHANGELOG.md`, §G), not full text. That is the gap the
reviewer's comment was pointing at.

---

## A. Confirmed problem: one citation does not support the claim attached to it

**Manuscript text (§1, Introduction):** "Exposure to heat is spatially uneven at intra-urban
scale (Camatti et al., 2024), which is the scale at which visitors experience a historic core
(Karimi & Mohammad, 2022)."

**What Camatti, Hrast Essenfelder & Giove (2024, *Environmental Research Letters* 19(6):064008,
doi:10.1088/1748-9326/ad3e91) actually did:** built a prototype open-access gridded database of
tourism supply/demand/satisfaction for Europe from TripAdvisor data, on a **5 km** regular grid,
and mapped its exposure to river floods, windstorms and heat (WBGT, ~10 km resolution hazard
layer), with results also reported at NUTS3 regional scale. It is a continental, regional-to-city
scale instrument. It does not measure, model or claim intra-urban or pedestrian-scale thermal
variability; urban heat inequality appears only in its literature review, uncited to any analysis
of its own.

**Verdict: misattribution.** The citation supports "tourism exposure to heat is geographically
uneven across destinations," not "...at intra-urban scale." The intra-urban/pedestrian-scale
claim is in fact supported by the SOLWEIG literature already cited elsewhere in the same
manuscript (Lindberg et al., 2008; Gál & Kántor, 2019), which exists precisely because radiant
load varies within a city at a scale air-temperature and coarse grids cannot resolve.

**Correction applied (§1):** Camatti et al. (2024) is now cited only for the claim it supports
(uneven geographic exposure of tourism to heat extremes); the intra-urban/pedestrian-scale claim
is now attributed to Lindberg et al. (2008), consistent with its use elsewhere in the manuscript.
No reference removed; one misapplied citation corrected.

---

## B. The five named candidate prior-art items (requested check)

| # | Reference | What it actually did | Relation to HATI's claims |
|---|---|---|---|
| A | Velea, Chițu & Bojariu (2024). *Heliyon* 10(2):e24682. doi:10.1016/j.heliyon.2024.e24682 | Evaluated a UTCI-based tourism-climate-service product (WeCENT) for 10 cities in Romania and Italy, UERRA/E-OBS data, summers 2011–2018. Directly tested how the **temporal definition** of the input temperature (12:00 UTC instantaneous vs. daily maximum vs. daily mean) changes the UTCI thermal-stress category, finding shifts of up to several days of the record per year. | **Close, direct precedent**, not previously cited. It demonstrates, for a UTCI-based tourism product, exactly the kind of result v0.3 reports for its air-temperature hazard rule (§6.2: reading AEMET thresholds as daily maxima changes 19/42 classes). HATI's finding is a **replication of this pattern in a different system** (an air-temperature rule, not UTCI; one city, one day, three hours, not a multi-year reanalysis across 10 cities), not a first demonstration of temporal-definition sensitivity. **Added to the manuscript** (§2, §7, references). |
| B | Prinsloo & Fitchett (2026). *Theoretical and Applied Climatology*, doi:10.1007/s00704-026-06574-4 | A critical review of the tourism-climate-index literature (single-index, intercomparison and multi-index approaches; TCI, HCI and variants). Documents that the field routinely proposes new indices as replacements for older ones and surveys how indices have been compared. | Relevant context for how much of the "index-comparison" space is already covered — but at the level of **composite bioclimatic indices** (TCI/HCI-family), not of a rule/threshold/source/support decomposition applied to named individual outdoor assets using a physically modelled index (UTCI/SOLWEIG) against an air-temperature hazard rule. Closes part of the "pending systematic search" flag in v0.3 §2 by showing what the broader index-comparison literature does and does not cover. **Added to the manuscript** (§2, references). |
| C | Karimi & Mohammad (2022). *Environmental Science and Pollution Research* 29(40):60641–60661, doi:10.1007/s11356-022-20058-8 | Field microclimate measurements + 180 tourist questionnaires + ENVI-met simulation (2 m grid) at 3 historic plazas each in Sevilla and Madrid, one hot day per city (not 21 August 2023). Comfort metric is **PET** (RayMan), not UTCI. Reports plaza-level PET comfort ranges (Sevilla 28.4–30.9 °C; Madrid 24.5–29.8 °C) and small intra-city differences in Ta/MRT between plazas. | **Correctly used** in v0.3 — it is cited only for the general point that visitors experience heat at plaza/intra-urban scale, which this study does establish (it is itself an intra-urban, plaza-level comparison). No correction required. Worth flagging for any future use beyond this: it uses PET, not UTCI, and a different day/year than HATI's case, so it cannot be used to benchmark HATI's UTCI values directly. |
| D | Dubois, Ceron, Dubois, Frías & Herrera (2016). *Earth Perspectives* 3(1):2, doi:10.1186/s40322-016-0034-y | Decomposes sources of uncertainty in tourism climate indices: (i) comfort-threshold variation across preference surveys, (ii) computation-method differences (France case), (iii) climate-model-ensemble uncertainty for Mediterranean projections. | **Correctly used** in v0.3 (§2, with Scott et al. 2016) to support "aggregate tourism-climate indices depend on parameterisation." No correction required. |
| E | Camatti et al. (2024) | See §A above. | **Misattributed** — corrected. |

---

## C. Targeted search of the five topic clusters (STAGE 4; non-systematic, not PRISMA)

Searched via Crossref/DOI resolution, OpenAlex-indexed web search and publisher pages (no Scopus
or Web of Science access). Searches run 2026-11-03; queries and platforms are the `WebSearch` /
`WebFetch` calls of this session, not separately logged. Backward/forward citation checks were
limited to the five candidate references above and the existing 15 in-text citations.

1. **Tourism heat exposure / adaptation** — Velea et al. (2024) is the only materially new item;
   the rest of the retrieved material (tourist behavioural adaptation, demand risk) duplicates
   what is already excluded from v0.3's scope (behavioural claims) and is not added.
2. **Tourism climate indices, thresholds, uncertainty** — Prinsloo & Fitchett (2026) added; no
   other item changes the picture already given by Dubois et al. (2016) and Scott et al. (2016).
3. **UTCI/Tmrt/SOLWEIG model uncertainty and spatial support** — no study was found that tests
   classification sensitivity to spatial support (centroid vs. buffer-mean vs. percentile) the
   way v0.3 §6.2 does; general SOLWEIG validation ranges remain as already cited (Gál & Kántor,
   2019). Nothing added.
4. **Spatial classification robustness / geospatial decision support** — no direct precedent found
   for an air-temperature-rule-vs-UTCI classification decomposition at named-asset scale. Nothing
   added.
5. **Urban tourism thermal exposure, Madrid / Southern Europe** — no new Madrid-specific item
   beyond what is already cited (Karimi & Mohammad, 2022). Nothing added.

No study combining (a) a rule/threshold/source/support decomposition, (b) applied jointly to an
air-temperature hazard rule and a SOLWEIG-modelled UTCI classification, (c) compared only through
classified outputs, (d) for a small set of named outdoor tourism assets, was located. This is
reported as **a documented limit of a targeted, non-exhaustive search**, not as proof that no such
study exists.

---

## D. Process observation (not a new citation problem, but worth recording)

The 2026-08-19 verification pass (`PHASE5_4B1_REFERENCE_CHANGELOG.md`, §G) checked "claim-to-source"
support against **source abstracts**, not full text, for all 23 references, and reported "all
SUPPORTED." That process is sound for catching fabricated or garbled metadata (which it did,
thoroughly) but is not sufficient to catch a scale/scope mismatch like Camatti et al. above, which
only becomes visible on reading the full method. Future reference passes on this manuscript should
state explicitly, per reference, whether support was checked at abstract or full-text level.

---

## E. Net effect on the manuscript

- One citation corrected (Camatti et al., 2024 — scope narrowed to what it actually shows).
- Two references added (Velea et al., 2024; Prinsloo & Fitchett, 2026), both because they
  materially change how the "knowledge gap" paragraph (§2) and one Discussion sentence (§7, point
  2) and one status row (Table 7) must be worded — not for bibliography padding.
- Zero references removed. Zero empirical results, tables, or numeric claims changed.
- `manuscript/REFERENCES_VERIFIED_v1.md` is left unchanged (it is a frozen 2026-08-19 record used
  by earlier manuscript versions too); the two new references are verified here instead, with the
  same metadata fields used in that file:

| Field | Velea, Chițu & Bojariu (2024) | Prinsloo & Fitchett (2026) |
|---|---|---|
| Authors | Liliana Velea, Zenaida Chițu, Roxana Bojariu | Ariel S. Prinsloo, Jennifer M. Fitchett |
| Title | Thermal stress information as a tourism-oriented climate product: Performance analysis for selected urban destinations in Romania and Italy | A critical examination of the tourism climate index landscape |
| Journal | Heliyon | Theoretical and Applied Climatology |
| Volume/issue/pages | 10(2), e24682 | online-first (15 Sept 2026); volume/pages not yet assigned at time of writing |
| DOI | 10.1016/j.heliyon.2024.e24682 | 10.1007/s00704-026-06574-4 |
| Verification source | Crossref; PMC full text (PMC10831790) | Crossref; publisher page (Springer) |
| Status | final, open access | final, open access, online-first |
