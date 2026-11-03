# How methodological choices shape heat classifications of outdoor tourism opportunities: an exploratory sensitivity analysis for central Madrid

*Working draft v0.3 — exploratory, not peer reviewed. It revises the framing of the archived preprint (`manuscript/MANUSCRIPT_TMP_v0.2.md`, Zenodo 10.5281/zenodo.22707470), which is left unchanged. Target journal: not selected.*

**Authors / affiliations / corresponding author / ORCID:** [TO VERIFY — not drafted on the authors' behalf]

---

## Abstract

Heat classifications of outdoor tourism assets are the product of a chain of methodological decisions: how heat is represented, how that representation is mapped onto classes, which thresholds and data sources are used, and over what spatial and temporal support. When no field measurement of thermal exposure exists at asset scale, as in most destinations, these decisions cannot be checked against truth, but their influence on the resulting classes can be described. We do so for 14 outdoor tourism assets in central Madrid at 12:00, 15:00 and 18:00 on 21 August 2023 (42 asset–hour observations). Two classification systems are kept separate: system A, built from hourly air temperature (AEMET warning thresholds) and a tree-count exposure grade, and system B, built from modelled UTCI (SOLWEIG). Air temperature and UTCI are not compared as equivalent quantities; only their classified outputs are. Question A asks how each system's classes change under alternative rules, data sources and spatial supports, varied one at a time. Question B asks how four tree/shade proxies relate, by Kendall's τ-b, to the spatial differences of modelled UTCI. The 14 disagreements between systems (9 at 12:00, 0 at 15:00, 5 at 18:00) arise from two rules of system A and from system B placing all 42 observations in one class; with the hazard bands and the single class of system B held fixed, their number is the same for any tercile-graded shade proxy (five assets are HIGH by construction), while their identity changes with the proxy. Reading the AEMET thresholds as daily maxima changes 19 of 42 classes of system A, whereas three air-temperature sources change none. In system B, spatial support changes more classes than irradiance, and every class change is a crossing of the 46 °C limit. Tree and shade proxies are mostly negatively associated with UTCI (τ-b −0.46 to +0.06), but the association is unstable across spatial supports. The study is exploratory, covers one day and three hours, and contains no field validation. It describes sensitivity; it does not establish which system is more accurate or which places are safer.

**Keywords:** outdoor thermal comfort; UTCI; urban tourism; classification sensitivity; extreme heat; Madrid

---

## 1. Introduction and research problem

Extreme-heat episodes increasingly coincide with the daytime, outdoor conditions under which much urban tourism takes place, and aggregate evidence shows that urban activity contracts and shifts under heat (Renninger & Cabrera, 2026). Heat governance has been built mainly around residents, and frameworks that embed tourism in heat action planning are only now being articulated (Scott, 2026). Exposure to heat is spatially uneven at intra-urban scale (Camatti et al., 2024), which is the scale at which visitors experience a historic core (Karimi & Mohammad, 2022). Destination managers and information services therefore face a practical question that is local and time-specific: which outdoor opportunities are described as more or less heat-compatible at a given hour?

Any answer is a classification, and any classification is built from decisions that are rarely reported together: the physical quantity used (air temperature, or an index that also contains radiation, humidity and wind), the rule that turns that quantity into classes, the thresholds in that rule, the source and period of the input data, and the spatial support over which the quantity is evaluated. Composite tourism-climate indices are known to depend on component weights and thresholds (Dubois et al., 2016), and radiation-resolving models represent features that air temperature and simple vegetation counts do not (Lindberg et al., 2008; Bröde et al., 2012; Wang et al., 2026). In the case studied here no independent measurement exists at asset scale against which to judge a classification, and models of this class require such measurement before accuracy claims are made (Gál & Kántor, 2019).

This draft therefore does not ask which representation is correct. It asks how much of what a classification says is attributable to identifiable methodological choices, and where the classes are sensitive to them, using a documented case and only the data available. We distinguish three things that are often conflated: the thermal variability of the real environment, which is not observed here; its representation by a model or proxy; and the classes derived from that representation. Disagreement between two representations is evidence about the second and third, not about the first.

---

## 2. Knowledge gap, bounded against the verifiable literature

What the cited literature establishes, and what this draft relies on rather than claims:

- Aggregate tourism-climate indices depend on parameterisation (Dubois et al., 2016; Scott et al., 2016).
- UTCI is a standardised index of physiological heat stress with fixed categories (Bröde et al., 2012); SOLWEIG-class models compute the radiant component at pedestrian scale (Lindberg et al., 2008) and require independent measurement for accuracy claims (Gál & Kántor, 2019).
- Surface or air temperature is not interchangeable with human-centred heat stress (Wang et al., 2026), and the reliability of thermal indices can itself be studied under uncertainty (Sargazi et al., 2025).
- Heat-aware routing and accessibility methods take the origin and destination, or the destination set, as given (Wolf et al., 2025; Buo et al., 2026; Aydin et al., 2026; Colaninno et al., 2025). Buo et al. (2026) additionally compare their routes with mobile measurements [abstract and press coverage consulted; full text to be checked].

The gap this draft addresses is narrower than the one claimed in the archived preprint. It is the absence, in the sources we could verify, of a transparent decomposition of how much of the disagreement between an air-temperature-based and a UTCI-based classification of individual outdoor tourism assets is due to the rules, thresholds, data sources and spatial supports involved. **Whether such a decomposition exists elsewhere is NOT established: the search behind this statement was limited and non-systematic, and a systematic search of the index-comparison and tourism-climate literature is pending before any claim of originality is made.**

---

## 3. Research questions

The study is exploratory. The data had already been inspected before the analysis was specified, so no hypothesis is tested, no significance test or interval is reported, and no equivalence between systems is claimed.

**Question A — sensitivity of classifications.** How do the tourism classes produced by each system change when its rule, threshold definition, input source or spatial support is varied one at a time, and how does the number and identity of disagreements between the two systems change as a consequence?

**Question B — spatial association.** How are four tree/shade proxies associated, hour by hour, with the spatial differences in modelled UTCI among the 14 assets? This is an association between a territorial covariate and the output of a model. It is not agreement between two thermal methods, not a validation of either, and not evidence about real exposure.

Explicitly outside scope: the accuracy of any representation, the safety or health of any place, tourist behaviour, and decision value for destination managers.

---

## 4. Study area and data

**Area and assets.** The area is a ≈3.5 km² box in central Madrid (Prado–Retiro–Atocha). Twenty-seven OpenStreetMap-based assets were purposively selected; this draft uses the 14 outdoor assets (indoor assets bypass the outdoor models). They are not a representative sample of Madrid tourism sites. Morphology: 6 park/garden, 4 plaza/hardscape, 3 monument exteriors, 1 street corridor.

**Day and hours.** 21 August 2023, within an AEMET-designated heat episode, at 12:00, 15:00 and 18:00 CEST. The unit of observation is the asset × hour pair (n = 42); the three observations of one asset are not independent, and the three hours are a design factor of one day, not a sample of days.

**Data (all versioned in the repository).**

| Role | Source | File |
|---|---|---|
| Hourly air temperature, system A | AEMET Madrid/Barajas (WMO 08221), ≈9 km NE of the area; 34.2, 38.8, 40.5 °C | `data/raw/aemet_barajas_08221_hourly_202308.csv` |
| Alternative air temperature | Ayuntamiento de Madrid, Escuelas Aguirre station | `data/raw/madrid_meteo_municipal/meteo_municipal_202308.csv` |
| Warning thresholds | AEMET Meteoalerta Annex 1, zone 722802: 36 / 39 / 42 °C, listed for maximum temperatures | `data/raw/aemet_official_pdfs/`, `src/thresholds.py` |
| Tree/shade proxies | OSM tree points; Madrid tree inventory; Copernicus tree-cover density (2018); OSM green polygons | `data/processed/shade_proxy_comparison.csv` |
| Modelled UTCI, system B | SOLWEIG 0.1.0b92 on IGN/CNIG LiDAR geometry, 2.5 m; Barajas forcing; clear-sky irradiance estimated with Ineichen–Perez | `data/processed/phase2_asset_thermal_exposure.csv` |
| Irradiance variants of B | Satellite-derived irradiance (EUMETSAT CM SAF), −10 %, −20 % | `data/processed/phase2_1_solar_scenario_assets.csv` |

Escuelas Aguirre is used only as an alternative air-temperature source for system A. System B is not recomputed with it. UTCI is a model output throughout; no Tmrt or UTCI was measured.

---

## 5. Methods

### 5.1 The two systems and the classes they produce

Two kinds of category are kept distinct throughout (Table 1).

**Table 1. Standard physiological categories versus classes defined by HATI.**

| | Quantity | Cut-points | Origin of the cut-points |
|---|---|---|---|
| Standard UTCI heat-stress categories | UTCI (index of physiological stress) | 9 / 26 / 32 / 38 / 46 °C: no stress, moderate, strong, very strong, extreme | Standard (Bröde et al., 2012) |
| HATI tourism classes of system B | modelled UTCI, mean within 10 m of the asset | < 32: FEASIBLE; 32 to < 46: FEASIBLE WITH CONDITIONS; ≥ 46: NOT RECOMMENDED | 32 and 46 coincide with standard category limits, but their reading as tourism classes, and the merging of "strong" and "very strong" (32–46 °C) in one class, is a HATI decision; 38 °C is not used |
| Hazard band of system A | air temperature (°C of air) | 36 / 39 / 42 °C: LOW, ELEVATED, SEVERE, EXTREME | AEMET warning thresholds, listed for maximum temperatures; HATI applies them to hourly values, which is an adaptation |
| Exposure grade of system A | OSM tree count (50 m around points; polygon + 15 m for the 8 area assets) | terciles of the 14 assets' own distribution (0.33 and 3.67 trees): HIGH = no mapped tree (5 assets) | Sample-relative; no standard |

**System A** combines the hazard band and the exposure grade through a first-match rule (Table 2). **System B** applies the UTCI mapping above. The standard categories are reported only as a description of the UTCI values (Section 6.3); they are never cross-tabulated with the tourism classes.

**Table 2. Outdoor rule of system A (numbered as in `src/thresholds.py`).**

| Rule | Condition | Class |
|---|---|---|
| 1 | hazard EXTREME | NOT RECOMMENDED |
| 2 | SEVERE and exposure HIGH | NOT RECOMMENDED |
| 3 | SEVERE, other exposure | FEASIBLE WITH CONDITIONS |
| 4 / 5 | ELEVATED (with / without exposure HIGH) | FEASIBLE WITH CONDITIONS |
| 6 | LOW and exposure HIGH | FEASIBLE WITH CONDITIONS |
| 7 | LOW, other exposure | FEASIBLE |

The two systems are never compared by subtracting air temperature from UTCI, nor by treating them as measures of one quantity. They are compared only through their classified outputs.

### 5.2 Analysis A: sensitivity of the classifications

1. **Baseline.** Cross-tabulation of the class of A by the class of B for each hour; list of the disagreeing observations, with the rule of A responsible and the UTCI of B.
2. **One-at-a-time variants, each against the baseline of its own system, with the other system held at its baseline.** For each variant we report how many classes of the varied system change, by hour, and the resulting number of disagreements with the other system. Families are kept separate and are not pooled into a common "noise level":
   - *Air-temperature source (A):* Barajas instantaneous (baseline); Barajas mean of the preceding hour; Escuelas Aguirre hour-ending mean; Escuelas Aguirre interpolated to the hour.
   - *Temporal definition of the AEMET rule (A):* thresholds applied to the daily maximum (Barajas, Escuelas Aguirre) instead of the hourly value. This is a sensitivity to how the rule is defined, not an equivalent hourly substitution.
   - *Shade proxy (A):* exposure grade from the Madrid inventory, Copernicus tree-cover density, or green-polygon coverage, each graded by terciles of its own distribution, instead of OSM trees.
   - *Irradiance (B):* satellite-derived, −10 %, −20 % (existing model runs).
   - *Spatial support (B):* UTCI at the asset centroid, or the 90th percentile within 10 m, instead of the 10 m mean.
3. **Coverage rule.** A variant is included only if it has comparable data for all 42 observations. Canopy-geometry variants exist for 3 of 14 assets (A23, A24, A27) and are excluded.
4. **Standard UTCI categories.** Distribution by hour for the baseline and for each B variant, and the number of observations that change category; no cross-tabulation with the tourism classes.
5. **Hour convention of Escuelas Aguirre.** The station reports hourly values labelled H01–H24 (the dataset only states "hour index"; project documentation assumes hour-ending local time). Before using it we compared it with Barajas, converted from UTC to CEST, for 31 days of August 2023.

### 5.3 Analysis B: association between proxies and modelled UTCI

For each hour separately (n = 14 assets, 91 pairs), Kendall's τ-b between each proxy and the 10 m mean UTCI, with the sign as observed (a negative sign is expected if more vegetation corresponds to lower UTCI). τ-b corrects for ties; we report the number of distinct values and of tied pairs in each variable. The UTCI at the centroid and the 90th percentile are used only as a secondary check. No significance test or interval is computed. Observations are not pooled across hours or assets. Proxy values are constant per asset.

The proxies are not the input of the physical model: SOLWEIG uses a LiDAR-derived canopy and building geometry. The OSM count additionally mixes two buffer definitions (50 m around points; polygon + 15 m for area assets). Associations are therefore properties of the modelled field, confounded by morphology and built geometry.

### 5.4 Reproducibility and integrity

All numbers come from `src/exploratory_sensitivity.py` (numpy and pandas only; no SOLWEIG, rasters or network). It checks that asset × hour keys are unique, that tables align (14 assets × 3 hours), that no value is missing, that the rule of A and the mapping of B reproduce the stored classifications in 42/42 rows, that the four proxy classifications are reproduced from their grades, and that the 14/42 results match the existing table `outputs/tables/proxy_vs_physical_comparison.csv`. It asserts every headline value in the Results and writes six tables under `outputs/tables/exploratory/`; two runs gave identical files (SHA-256). It was run under pandas 3.0.5 / numpy 2.5.3 and under the versions pinned in the repository, pandas 2.3.3 / numpy 2.4.6 (isolated environment, Python 3.13.18), with byte-identical outputs; Python 3.14.5, also pinned in the repository, was not available and was not tested. The Kendall implementation was tested on three cases of known value (scipy is not installed in the environment).

---

## 6. Results

### 6.1 Baseline: where the disagreements come from

System A and system B assign the same class to 28 of 42 observations and different classes to 14: 9 at 12:00, 0 at 15:00 and 5 at 18:00 (Table 3). B places all 42 observations in FEASIBLE WITH CONDITIONS (UTCI 32.4–45.4 °C), so every disagreement is a case where A assigns another class.

**Table 3. Classes of A against classes of B, baseline (n = 14 per hour).**

| Hour | A: FEASIBLE | A: FEASIBLE WITH COND. | A: NOT RECOMMENDED | B: FEASIBLE WITH COND. | Disagreements |
|---|---|---|---|---|---|
| 12:00 | 9 | 5 | 0 | 14 | 9 |
| 15:00 | 0 | 14 | 0 | 14 | 0 |
| 18:00 | 0 | 9 | 5 | 14 | 5 |

Two rules of A account for all 14: rule 7 at 12:00 (LOW hazard with exposure LOW or MODERATE gives FEASIBLE: 9 observations, 9 disagreements; modelled UTCI 32.4–40.4 °C) and rule 2 at 18:00 (SEVERE hazard with exposure HIGH gives NOT RECOMMENDED: 5 observations, 5 disagreements; UTCI 41.7–45.2 °C). The other four rules (3, 4, 5, 6; 28 observations) coincide with B. At 15:00 both systems assign every observation to the same class, but A does so for all 14 because the hour is in the ELEVATED band irrespective of exposure, and B because all values lie between 32 and 46 °C. Agreement at that hour therefore carries no information about spatial discrimination.

By morphology the 12:00 disagreements are 6 parks/gardens, 1 plaza, 1 monument exterior and 1 street corridor; those at 18:00 are 3 plazas and 2 monument exteriors.

### 6.2 Sensitivity of the classes (Question A)

**Table 4. One-at-a-time variants. "Changes" are classes that change against the baseline of the varied system; "disagreements" are disagreements with the other system at its baseline (baseline 14 = 9/0/5). All variants cover 42/42 observations.**

| Family | Variant | Classes changed (12/15/18 h; total) | Disagreements (12/15/18 h; total) |
|---|---|---|---|
| A: air-temperature source | Barajas mean of preceding hour (33.2 / 38.2 / 40.4 °C) | 0/0/0; 0 | 9/0/5; 14 |
| | Escuelas Aguirre hour-ending (32.6 / 37.5 / 40.8 °C) | 0/0/0; 0 | 9/0/5; 14 |
| | Escuelas Aguirre interpolated (33.4 / 38.4 / 40.6 °C) | 0/0/0; 0 | 9/0/5; 14 |
| A: temporal definition of rule | AEMET thresholds on daily maximum, Barajas (40.5 °C) | 14/5/0; 19 | 5/5/5; 15 |
| | idem, Escuelas Aguirre (40.8 °C) | 14/5/0; 19 | 5/5/5; 15 |
| A: shade proxy | Madrid inventory | 4/0/4; 8 | 9/0/5; 14 |
| | Copernicus tree-cover density | 4/0/4; 8 | 9/0/5; 14 |
| | Green-polygon coverage | 4/0/4; 8 | 9/0/5; 14 |
| B: irradiance | Satellite-derived | 0/0/1; 1 | 9/0/6; 15 |
| | −10 % | 0/0/0; 0 | 9/0/5; 14 |
| | −20 % | 0/0/0; 0 | 9/0/5; 14 |
| B: spatial support | UTCI at centroid | 0/0/1; 1 | 9/0/6; 15 |
| | UTCI 90th percentile within 10 m | 0/1/1; 2 | 9/1/6; 16 |

*Air-temperature source.* The three alternative sources keep every hour in the same hazard band as the baseline (LOW, ELEVATED, SEVERE), so no class changes. The 15:00 values of Escuelas Aguirre (37.5 and 38.4 °C) are below the 39 °C threshold. The hour-ending convention of Escuelas Aguirre was checked beforehand (Table 5): in the daytime its values are best aligned with Barajas at the same clock hour (RMSE 1.08 °C) or with the mean of the preceding hour (1.13 °C; bias −0.01 °C), and a shift of one hour in either direction is clearly worse (1.68 and 1.97 °C). The data are consistent with hour-ending values but do not separate an hourly mean from a clock-hour reading; the residual uncertainty is about half an hour. The comparison is between two different stations (urban and airport).

**Table 5. Escuelas Aguirre (H*nn*) against Barajas converted to CEST, 31 days of August 2023, 10–20 h (n = 341).**

| Compared with Barajas | RMSE (°C) | Bias (°C) |
|---|---|---|
| clock hour *n* | 1.08 | −0.58 |
| mean of (*n*−1, *n*) | 1.13 | −0.01 |
| clock hour *n*−1 | 1.68 | +0.56 |
| clock hour *n*+1 | 1.97 | −1.32 |

*Temporal definition of the rule.* Applying the thresholds to the daily maximum (40.5 or 40.8 °C, both in the SEVERE band) places all three hours in the same band. A then assigns NOT RECOMMENDED to the five assets with HIGH exposure and FEASIBLE WITH CONDITIONS to the rest, at every hour; 19 of 42 classes change and no observation is classified FEASIBLE. This is a sensitivity to the definition of the rule, not an hourly equivalent.

*Shade proxy.* With any of the three alternative proxies the number of disagreements remains 14 (9 at 12:00, 5 at 18:00). This is a consequence of the design: each proxy assigns five assets to HIGH, so there are always nine non-HIGH assets at 12:00 and five HIGH assets at 18:00. What changes is which observations disagree: 10 of the 14 baseline disagreements persist and 4 are replaced, for each alternative proxy, and 6 observations are disagreements under all four proxies. The green-polygon grade has no LOW class (coverage reaches 100 % for several assets).

*Irradiance.* The satellite-derived irradiance changes one class, A24 at 18:00 (modelled UTCI 45.4 to 46.0 °C, crossing into NOT RECOMMENDED). The −10 % and −20 % reductions change none. Changes in modelled UTCI relative to the baseline range from −1.1 to +1.0 °C (satellite), −1.1 to +0.2 °C (−10 %) and −2.3 to +0.2 °C (−20 %).

*Spatial support.* UTCI at the centroid differs from the 10 m mean by −7.0 to +6.3 °C (median −0.4 °C) and changes one class, A22 at 18:00 (mean 42.9 °C, centroid 46.0 °C). The 90th percentile within 10 m differs by −0.1 to +6.9 °C (median +1.7 °C) and changes two: A18 at 15:00 (44.5 to 46.2 °C) and A22 at 18:00. In each case the class that changes is one that crosses the 46 °C limit (variant values of 46.0–46.2 °C at A24, A22 and A18).

### 6.3 Standard physiological categories (description only)

Computed from the numeric UTCI values, not from the label columns stored in the repository (Section 8). At the baseline, 12:00 has 8 observations in "strong" (32–38 °C) and 6 in "very strong" (38–46 °C), and 15:00 and 18:00 have all 14 in "very strong"; none is in "extreme". The number of observations whose standard category changes against the baseline is 1 for the satellite irradiance (A24 at 18:00, to "extreme"), 0 for −10 %, 1 for −20 % (12:00), 5 for the centroid and 8 for the 90th percentile. These counts are not related to the tourism classes; the 32–46 °C range merged by HATI in one class contains the two standard categories "strong" and "very strong".

### 6.4 Association between proxies and modelled UTCI (Question B)

**Table 6. Kendall τ-b between each proxy and the 10 m mean UTCI (n = 14 assets, 91 pairs per cell). Pairs tied in the proxy: OSM 11, Madrid 6, tree-cover density 0, green polygons 21. Distinct proxy values: 9, 11, 14, 8. Pairs tied in UTCI: 1 (12:00), 4 (15:00), 2 (18:00).**

| Proxy | 12:00 | 15:00 | 18:00 |
|---|---|---|---|
| OSM tree count | −0.271 | −0.204 | −0.356 |
| Madrid tree inventory | −0.023 | +0.058 | −0.126 |
| Copernicus tree-cover density | −0.309 | −0.326 | −0.456 |
| Green-polygon coverage | −0.139 | −0.115 | −0.266 |

The association is negative in 11 of the 12 proxy–hour cells (range −0.456 to +0.058). The tree-cover density has the largest magnitude at every hour; the Madrid inventory count is close to zero. One discordant pair changes τ-b by about 0.02. With the centroid instead of the 10 m mean, the sign differs from the primary result in 6 of 12 cells (OSM and tree-cover density at 15:00; Madrid, tree-cover density and green polygons at 18:00; green polygons at 15:00) and the values at 15:00 are positive (+0.07 to +0.47); with the 90th percentile it differs in 3 cells (the Madrid inventory, at all hours, with |τ-b| ≤ 0.07). These values describe how the modelled field ranks the 14 assets against four territorial covariates. They are not agreement between methods, a validation of the model, or evidence about real shade.

---

## 7. Discussion

**What the results show.**

1. *The headline reclassification rate is a joint property of rules and design.* The 14 disagreements come from two rules of system A, set against a system B that places every observation in one class. Given the hourly hazard bands and the single class of B, their number is fixed by the tercile design of the exposure grade: any proxy yields five HIGH assets, hence nine at 12:00 and five at 18:00. A different grading (another number of grades or other cut-points) would give a different count, so the 33.3 % should not be read as a measure of how far two thermal representations differ.
2. *In this case, defining the rule mattered more than the choice among air-temperature sources.* Replacing the air-temperature source or its temporal averaging within the hour changed nothing, because all alternatives fell in the same band. Reading thresholds listed for maximum temperatures as daily maxima changed 19 of 42 classes. A report of how a hazard band was built from a station should therefore state this definition explicitly.
3. *For system B, support matters more than irradiance.* Spatial support (centroid, percentile) changed more standard categories (5 and 8) than the tested irradiance variants (1, 0 and 1), and every change of tourism class is a crossing of the 46 °C limit. This is consistent with a coarse classifier acting on a continuous index; it does not show that any support is closer to what visitors experience.
4. *Proxy associations with modelled UTCI are weak to moderate and unstable.* They are mostly negative, as expected for vegetation, but small and sensitive to the spatial support of UTCI.

**Potential implications for tourism planning (not demonstrated).** If these patterns hold in other cases, then (i) heat classes used to describe outdoor opportunities should be accompanied by the rule, the thresholds and the support used; (ii) classes built from sample-relative grades, such as terciles, should not be compared across areas or days; (iii) reporting a class together with its sensitivity, for example whether it changes under a plausible alternative, may be more informative than a single class. None of this has been tested with managers or visitors, and no improvement in decisions or outcomes is claimed.

**Scope relative to the archived preprint.** The earlier preprint also reported a constraint-first screening architecture, eight decision scenarios and a comparison with a nearest-open baseline. Those results are not re-examined here and are not part of the claims of this draft. A re-reading of the scenario tables (`data/processed/phase3_scenarios.csv`, `phase3_candidate_screening.csv`), not reproduced by the script of this draft, suggests that they need a separate, more cautious treatment: the outcome of one scenario (S2) rests on a modelled difference of 0.1 °C between candidates whose uncertainty envelopes overlap, and a count of candidates removed by additional filters is expected by construction. This is flagged for a later revision, not decided here.

---

## 8. Limitations and future validation needs

- **No physical validation.** No Tmrt, globe temperature or UTCI measurement exists for the area or the day. Nothing here supports a statement that system A or system B is more accurate, nor that any asset is safer.
- **One day, three hours, 14 purposively chosen assets, one air-temperature source in the physical model.** Observations are not independent (three per asset), the hour is a design factor, and the results cannot be extrapolated to other conditions, seasons or places.
- **Exploratory.** The data were inspected before the analysis was specified; there are no pre-registered hypotheses, tests or equivalence margins. Absence of a difference in a variant is not evidence of equivalence.
- **Inputs of system B.** Forcing comes from an airport station about 9 km away; wind and humidity are single station values; irradiance is estimated for clear sky; canopy geometry is dated and was explored for only 3 of 14 assets (excluded from the comparison for lack of coverage). The sensitivity of B to air temperature, wind, humidity and geometry is not tested, and the Escuelas Aguirre series cannot be used to recompute UTCI without a new model run.
- **Rules and grades.** The AEMET thresholds are listed for maximum temperatures and are used hourly as an adaptation; terciles are sample-relative; the OSM count combines two buffer definitions; the green-polygon grade has no LOW class; and the mapping of B groups two standard UTCI categories in one tourism class.
- **Hour convention of Escuelas Aguirre** is supported empirically within about half an hour but not independently documented in the dataset itself; the Barajas time stamps rely on the documented UTC convention of the archive.
- **Shifted UTCI category labels in locked outputs.** The category lookups in `src/extract_asset_thermal_exposure.py` and `src/phase2_2_decision_confidence.py` pair each label with the *lower* limit of its category (26, 32, 38, 46) but compare values as if those were *upper* limits (`value < limit`), so each value receives the label of the next-higher category. Fields affected: `utci_category` (`phase2_asset_thermal_exposure.csv`, 42 of 42 outdoor rows; `phase2_1_solar_scenario_assets.csv`, 125 of 126), `utci_category_official` (`phase2_2_decision_confidence.csv`, 42 of 42: 34 rows of 38.4–45.4 °C read "Extreme", standard "very strong"; 8 rows of 32.4–37.6 °C read "Very strong", standard "strong") and, for the 8 rows at 12:00 only, `thermal_stress_state` / `thermal_state` (`phase2_2_decision_confidence.csv`, `phase3_candidate_screening.csv`: "very strong" instead of "strong"; the 34 rows at 38.4–45.4 °C are correctly labelled). The scenario tables (15:00 and 18:00) contain no mislabelled row, and the read-only prototype would display "Very strong heat stress" for those 8 rows if 12:00 is selected. No class, decision or result in this draft is affected: feasibility classes, `decision_state` and the 32/46 °C mapping use numeric limits, the category comparison used in the screening step has the correct 32/38 boundaries (its two upper categories share a label, which changes no outcome because no scenario value reaches 46 °C), and this draft computes categories from the numeric values. The locked files, code and prototype are left unchanged; correcting them is a decision for the repository owner [PENDING].
- **Excluded from the study:** indoor assets, accessibility and routing, screening scenarios, tourist behaviour and the usefulness of any class for decisions.

**Validation needed before any claim beyond sensitivity:** in-situ measurement of Tmrt or globe temperature and air conditions at a subset of the 14 assets, repeated across days and hours; additional days and cities; propagation of the uncertainty of air temperature, wind, humidity and canopy in the physical model; a systematic literature search to establish what is and is not new; and consultation with destination managers to find out which classes, thresholds and supports are meaningful for an actual decision.

---

## 9. Conclusions

In this documented case, the apparent disagreement between an air-temperature-based and a UTCI-based classification of outdoor tourism assets is, descriptively, accounted for by a small number of identifiable choices: two rules of one system, the single class into which the other system places all observations, the tercile design of the exposure grade, the temporal definition of the warning thresholds, and, within the modelled system, the spatial support of the index. Changing the air-temperature source did not change any class, while changing the definition of the rule changed almost half of them. Tree and shade proxies are mostly negatively, but weakly and unstably, associated with the modelled UTCI. These are descriptions of sensitivity for one day and 14 assets.

**Table 7. Status of the claims.**

| Statement | Status |
|---|---|
| 14 of 42 observations are classified differently by A and B, produced by two rules of A | Reproduced from versioned data (this draft) |
| The number of disagreements is invariant to the shade proxy by design; their identity is not | Reproduced |
| Reading AEMET thresholds as daily maxima changes 19 of 42 classes of A; three air-temperature sources change none | Reproduced |
| In B, spatial support changes more classes than irradiance, near 46 °C | Reproduced for the tested variants only |
| Tree/shade proxies are mostly negatively associated with modelled UTCI | Reproduced; descriptive, n = 14 per hour, unstable across supports |
| B is more accurate than A, or the reverse | **Not established** (no measurements) |
| Any asset is safer or less safe | **Not established** |
| A and B are equivalent where variants agree | **Not established** (no equivalence test) |
| Findings hold on other days, cities or with other inputs | **Not established** |
| A decomposition of this kind has not been published | **Pending** systematic literature search |
| Reporting sensitivity improves planning decisions | **Not tested** |

---

## Declarations

**Funding, competing interests, author contributions, acknowledgements, generative-AI disclosure:** [TO VERIFY — not drafted on the authors' behalf].
**Ethics.** No human participants or personal data. [Confirm against the target journal's policy.]
**Data and code availability.** Analysis script: `src/exploratory_sensitivity.py`; derived tables: `outputs/tables/exploratory/`; input tables: `data/processed/` and `data/raw/` in the project repository. Third-party data retain their original licences. A persistent public archive of this version has not been created [TO VERIFY].

---

## References

Aydin, E. E., Chen, Z., Ortner, F. P., Tay, J. Z., Li, K., & Chua, R. (2026). Universal Thermal Climate Index (UTCI)-adjusted pedestrian accessibility: Urban design exploration for climate-resilience in tropical climates. *Sustainable Cities and Society*, 143, 107335. https://doi.org/10.1016/j.scs.2026.107335

Bröde, P., Fiala, D., Błażejczyk, K., Holmér, I., Jendritzky, G., Kampmann, B., Tinz, B., & Havenith, G. (2012). Deriving the operational procedure for the Universal Thermal Climate Index (UTCI). *International Journal of Biometeorology*, 56(3), 481–494. https://doi.org/10.1007/s00484-011-0454-1

Buo, I., Khan, W. H., Crabtree, E., Emmott, F., Hariyani, D., & Middel, A. (2026). Cool routes: Real-time human thermal exposure routing. *Building and Environment*, 298, 114622. https://doi.org/10.1016/j.buildenv.2026.114622

Camatti, N., Hrast Essenfelder, A., & Giove, S. (2024). Mapping the exposure of tourism to weather extremes: the need for a spatially-explicit gridded dataset for disaster risk reduction. *Environmental Research Letters*, 19(6), 064008. https://doi.org/10.1088/1748-9326/ad3e91

Colaninno, N., Basu, R., Hosseini, M., Alhassan, A., Liu, L., & Sevtsuk, A. (2025). A sidewalk-level urban heat risk assessment framework using pedestrian mobility and urban microclimate modeling. *Environment and Planning B: Urban Analytics and City Science*, 52(5), 1071–1090. https://doi.org/10.1177/23998083241280746

Dubois, G., Ceron, J. P., Dubois, C., Frías, M. D., & Herrera, S. (2016). Reliability and usability of tourism climate indices. *Earth Perspectives*, 3(1), 2. https://doi.org/10.1186/s40322-016-0034-y

Gál, C. V., & Kántor, N. (2019). Modeling mean radiant temperature in outdoor spaces, A comparative numerical simulation and validation study. *Urban Climate*, 32, 100571. https://doi.org/10.1016/j.uclim.2019.100571

Karimi, A., & Mohammad, P. (2022). Effect of outdoor thermal comfort condition on visit of tourists in historical urban plazas of Sevilla and Madrid. *Environmental Science and Pollution Research*, 29(40), 60641–60661. https://doi.org/10.1007/s11356-022-20058-8

Lindberg, F., Holmer, B., & Thorsson, S. (2008). SOLWEIG 1.0 – Modelling spatial variations of 3D radiant fluxes and mean radiant temperature in complex urban settings. *International Journal of Biometeorology*, 52(7), 697–713. https://doi.org/10.1007/s00484-008-0162-7

Renninger, A., & Cabrera, C. (2026). Extreme heat reduces and reshapes urban mobility. *PNAS Nexus*, 5(4), pgag078. https://doi.org/10.1093/pnasnexus/pgag078

Sargazi, M. A., Heidari, A., Davtalab, J., & Piri, J. (2025). Comparative reliability assessment of PET and UTCI thermal comfort indices using Monte Carlo simulation in urban microclimates. *Scientific Reports*, 16, 3431. https://doi.org/10.1038/s41598-025-33440-6

Scott, D. (2026). A framework for heat risk action planning for tourism. *Annals of Tourism Research*, 118, 104141. https://doi.org/10.1016/j.annals.2026.104141

Scott, D., Rutty, M., Amelung, B., & Tang, M. (2016). An inter-comparison of the Holiday Climate Index (HCI) and the Tourism Climate Index (TCI) in Europe. *Atmosphere*, 7(6), 80. https://doi.org/10.3390/atmos7060080

Wang, Y., Yi, S., Li, X., Liu, P., Yang, Z., Bardhan, R., & Stouffs, R. (2026). From physical surfaces to human-centric heat stress: LST and UTCI heat mapping reveals nonlinear effects of urban morphology. *arXiv preprint* arXiv:2604.22433. https://arxiv.org/abs/2604.22433

Wolf, H., Vierø, A. R., & Szell, M. (2025). CoolWalks for active mobility in urban street networks. *Scientific Reports*, 15, 14911. https://doi.org/10.1038/s41598-025-97200-2

*All entries are taken from `manuscript/REFERENCES_VERIFIED_v1.md` (verified by the repository owner against publisher/Crossref records). The characterisation of each work in the text follows the use made of it in the archived preprint; for Buo et al. (2026) the field comparison was read at abstract and press-coverage level only. No reference has been added in this draft.*
