# 3. Methods

## 3.1 Study design and study area

This study is a single-city, single-day pilot designed to test whether the choice
of thermal-exposure method changes heat-adaptive tourism screening decisions, and
to demonstrate a transparent decision architecture in which any such difference is
made explicit. It deliberately trades breadth for auditability, using a compact
study area, a fixed set of real tourism assets, and a few fixed hours.

The study area is a rectangular box of approximately 3.5 km² in central Madrid,
spanning the Paseo del Prado museum corridor, the Puerta de Alcalá and Cibeles
plazas, the Atocha transit hub, and a western slice of the Retiro park interior
(the Prado–Retiro–Atocha box). The rectangle is pinned to named, independently
verifiable landmarks so that it can be reproduced without any proprietary boundary
file, and was drawn to include a cross-section of adaptation conditions — open
monumental plazas, an indoor museum corridor, a transit interchange, and shaded
gardens — while remaining small enough to keep every asset individually
inspectable.

Within this area we curated 27 real, named tourism assets from OpenStreetMap
(13 indoor, 14 outdoor), each resolved to a specific OSM feature identifier. The
set was hand-selected to span the adaptation conditions above rather than sampled
at random; it is therefore a purposive pilot, not a representative sample, and no
inference to the full population of Madrid tourism sites is drawn from it.

The study day is 21 August 2023, which falls inside an extreme-heat episode
(20–25 August 2023) formally designated by the Spanish State Meteorological Agency
(AEMET) for the Madrid region. Using an officially designated episode, rather than
a self-selected hot day, anchors the "extreme heat" framing to an external
authority. The day is treated as a representative extreme-heat case only; it is
not claimed to represent Madrid climatologically, and no seasonal or multi-day
generalisation is made from it. Three fixed local hours are analysed — 12:00,
15:00, and 18:00 (CEST) — with observed air temperatures of 34.2, 38.8, and
40.5 °C respectively. These hours were fixed by the study design before any data
were retrieved.

The primary unit of analysis is the tourism asset × timestamp pair. Thermal-method
comparison is performed on the 42 outdoor pairs (14 outdoor assets × 3 hours);
indoor assets bypass the outdoor thermal model by construction (Section 3.4). The
individual tourist is explicitly not a unit of analysis, and no quantity in this
study describes tourist behaviour, choice, or flow.

## 3.2 Data sources and preprocessing

All inputs are open data with documented provenance. We distinguish three
categories: observed meteorological data, modelled or derived physical inputs, and
contextual tourism data.

**Observed meteorological data.** Hourly air temperature, relative humidity, wind
speed, and pressure for 21 August 2023 were taken from the Madrid/Barajas station
(WMO 08221, ICAO LEMD), the nearest station with a genuine (non-modelled) hourly
observation record. The station lies approximately 9 km north-east of the study
area on an airport apron; its readings are used as the best available real,
sub-daily anchor for the regional heat signal, not as an estimate of on-site air
temperature at each asset, and each record carries a note quantifying the station's
agreement with AEMET's in-park Retiro reference (about +0.5 °C at daily maximum). A
co-located Retiro hourly series was sought but found to be reanalysis-interpolated
rather than observed, and was not used. The meteorological warning thresholds and
the episode designation are drawn from official AEMET publications.

**Modelled and derived physical inputs.** The physical thermal model (Section 3.4)
is driven by three-dimensional urban geometry from Spanish national LiDAR products
(IGN/CNIG): a 5 m digital elevation model and 2.5 m building- and vegetation-height
layers, each clipped to the study area. Global horizontal
irradiance, which the Barajas hourly archive does not record, was estimated with a
clear-sky radiation model (the Ineichen–Perez formulation) evaluated at the
study-area centroid and true timestamps, a substitution justified by the archive's
own clear-sky weather code at all three hours. This irradiance is an estimated, not
observed, input and is treated as such throughout.

**Contextual tourism data.** Asset locations, categories, tree points, and
park/garden polygons are from OpenStreetMap (ODbL). Opening hours were harvested
from OpenStreetMap tags where present (11 of 27 assets) and otherwise filled from
documented institutional schedules (16 of 27), each recorded with its source and an
evidence-completeness flag. One temporal-alignment limitation is material and is
stated explicitly: the OpenStreetMap snapshot and the institutional opening hours
were retrieved in 2026 and applied retrospectively to the 2023 study date. This
assumes the pilot area's urban form and operating schedules did not change
materially over that window — reasonable for a stable, protected city core, but not
verified — and it is carried forward as a permanent limitation.

## 3.3 Simple-proxy baseline

The comparison baseline is a constraint-first, open-data feasibility
classification that uses no radiative, surface-temperature, or shadow information.
It combines exactly two inputs through a decision rule. It is not a land-surface-
temperature product, a satellite surface-temperature proxy, a canopy or shade
model, or a shadow simulation; no such quantity enters it.

The first input is an ambient air-temperature hazard band. The observed hourly air
temperature (Section 3.2) is classified against AEMET's official Meteoalerta
maximum-temperature civil-protection thresholds for the Madrid metropolitan zone
(warning levels at 36, 39, and 42 °C), yielding bands LOW, ELEVATED, SEVERE, and
EXTREME. Under this scale the three study hours fall in LOW (12:00), ELEVATED
(15:00), and SEVERE (18:00). This is a meteorological hazard classification of a
station reading against a warning scale; it is not, and is never read as, a
thermal-comfort index.

The second input is an exposure band derived from the local count of OpenStreetMap
`natural=tree` points within the asset's real extent — a 50 m radius buffer for
point-type assets, or the asset's own park/garden polygon buffered by 15 m for the
eight area-type assets. The tree count is classified into LOW, MODERATE, or HIGH
exposure by tercile of the pilot's own 14-outdoor-asset tree-count distribution
(tercile cut-points of 0.33 and 3.67 trees), where HIGH denotes the fewest trees
(poorest shade availability). These terciles are an explicit within-sample relative
grade, not a transferable threshold, because no published tree-count shade-
sufficiency standard exists to cite. The tree count is a presence proxy for local
shade availability; it does not measure canopy cover, shadow geometry, or sun
position.

The two bands are combined by a first-matching-rule decision tree, with no weighted
score. For outdoor assets: an EXTREME hazard band yields NOT RECOMMENDED; SEVERE
yields NOT RECOMMENDED where exposure is HIGH and otherwise FEASIBLE WITH
CONDITIONS; ELEVATED yields FEASIBLE WITH CONDITIONS; and LOW yields FEASIBLE, or
FEASIBLE WITH CONDITIONS where exposure is HIGH. Indoor assets bypass the exposure
input. This baseline approximates pedestrian heat load with two inexpensive
surrogates — an ambient hazard signal and local tree presence — and represents the
simplest defensible open-data screening architecture available before any physical
modelling; it does not measure human thermal comfort.

## 3.4 Physically based thermal-exposure modelling

The physical comparator replaces the two-surrogate baseline with a radiation-
resolving estimate of pedestrian-level heat load. Mean radiant temperature (Tmrt)
was modelled with SOLWEIG (Lindberg et al., 2008), a three-dimensional radiant-flux
model, and combined with meteorological forcing to derive the Universal Thermal
Climate Index (UTCI). We used the official standalone `solweig` package
(version 0.1.0b92), with UTCI computed by the package's own built-in module from the
modelled Tmrt and the same observed air
temperature, humidity, and wind. Computation is at a 2.5 m working resolution — the
native resolution of the building- and vegetation-height layers — with the digital
elevation model resampled onto that grid. Each hour was run as an independent
single-timestep calculation. Model parameters were left at the package's documented
defaults (anisotropic sky, deciduous leaf-on transmissivity appropriate to the
August date, standing-posture human geometry, default material set), with no
parameter tuned to a target result and no custom land-cover grid supplied.

Tmrt represents the combined short- and long-wave radiant environment experienced
by a standardised human body; UTCI combines that radiant environment with air
temperature, humidity, and wind into a model-derived thermal-stress index
calibrated by Bröde et al. (2012). UTCI is a model output, not a measured or
observed quantity, and is never interpreted here as observed human comfort. For
each outdoor asset the exposure value is the mean UTCI within a 10 m buffer of the
asset's representative point, a spatial statistic fixed in advance; a buffer mean
rather than a single centre pixel is used because single-pixel radiant values are
sensitive to shadow-edge alignment. Modelled UTCI values are mapped to the same
three feasibility states used by the baseline through a pre-registered rule
(UTCI ≥ 46 °C → NOT RECOMMENDED; 32 ≤ UTCI < 46 °C → FEASIBLE WITH CONDITIONS;
UTCI < 32 °C → FEASIBLE), collapsing the official "strong" and "very strong" stress
bands into a single conditional state for direct comparability with the baseline's
three-state structure. Indoor assets are not assigned a UTCI value; SOLWEIG models
the outdoor environment only, and indoor assets retain their indoor-refuge state.

The modelled Tmrt and UTCI fields are not field-validated anywhere in this study;
the station observations validate only the air-temperature, humidity, and wind
inputs, not the radiant output. The physical model is therefore treated as a
radiation-resolving estimate whose ranges are consistent with published
SOLWEIG-class values for comparable climates (e.g. Gál & Kántor, 2019), and never as
ground truth or as a more accurate representation of comfort than the baseline.

## 3.5 Thermal-method comparison

The proxy and physical classifications were compared as a paired reclassification
analysis over the 42 outdoor asset × timestamp rows. For each row, the baseline
feasibility state and the physically derived feasibility state were placed
side by side, and the row was flagged as reclassified where the two states differ.
Reclassifications were characterised by direction — whether the physically derived
state was more restrictive or less restrictive than the proxy state — and were
stratified by timestamp to locate where in the day the two methods agree or diverge. Indoor rows are excluded from this
comparison by construction, since they carry no modelled UTCI.

This analysis measures the sensitivity of the feasibility decision to the choice of
thermal method, not the accuracy of either method against ground truth: neither
method is field-validated, so a reclassified row indicates that the two methods
disagree, not that one is correct and the other wrong.

## 3.6 Uncertainty and robustness treatment

Rather than attach a false-precision error bar to each modelled UTCI value, we
carried an evidence-derived uncertainty envelope built only from realizations that
were actually computed. For every outdoor row the envelope spans the minimum and
maximum UTCI across four solar-forcing realizations — the clear-sky baseline, a
satellite-derived irradiance realization (EUMETSAT CM SAF), and −10% and −20%
irradiance perturbations — plus, for the two assets whose LiDAR canopy was found
stale against a newer per-tree inventory, three corrected-canopy geometry variants
bracketing the one crown-radius assumption. The envelope is reported as measured
rather than forced to a symmetric band: clear-sky irradiance sits near the physical
upper bound of surface radiation and canopy correction only adds shade, so both
tested sources widen it mainly below the baseline.

Each row's envelope is translated into a categorical decision-confidence class
against the safety-critical 46 °C feasibility boundary (and a secondary 32 °C
boundary), using the row's own demonstrated sensitivity — the largest absolute
deviation of any realization from the baseline — as the reference margin rather than
a fixed tolerance. A row is UNSTABLE if any realization falls on the opposite side
of the 46 °C boundary from the baseline; BOUNDARY if no realization crosses but the
envelope lies within the row's own demonstrated sensitivity of a threshold; and
ROBUST otherwise. Thermal-stress state and decision confidence are kept as separate
fields and are never collapsed into a single score: the official UTCI stress
category is reported alongside, not multiplied by, the confidence class.

This treatment covers tested solar-forcing and targeted geometry uncertainty only;
it does not propagate air-temperature, humidity, wind, or model-structural
uncertainty, and there is no field validation of Tmrt or UTCI. A ROBUST label
therefore means robust against every uncertainty actually tested, not certain, and
the per-row sensitivity is a lower bound on true uncertainty.

## 3.7 Constraint-first tourism opportunity screening

The screening layer evaluates, for a given source asset at a given hour, which
other pilot assets remain feasible candidate alternatives. Each candidate passes
through a fixed, ordered sequence of hard constraints, and the first failing
constraint determines its outcome; a candidate that clears every constraint becomes
a candidate alternative. The order is: pilot scope, then open at the timestamp,
then within the walking radius, then within the outdoor thermal limit
(UTCI < 46 °C), then evidence sufficiency, and finally a source-relative test of
whether the candidate is a meaningful thermal improvement over the source. Cheap
categorical eliminations are applied first and the heat-adaptive improvement test
last, so that a candidate excluded for being closed is never additionally
mislabelled as thermally inadequate. There is no weighted composite score anywhere
in the chain.

Every candidate carries one machine-readable exclusion reason from a fixed
vocabulary (for example, closed at timestamp, accessibility constraint, thermal
limit exceeded, insufficient evidence, no meaningful thermal improvement, or outdoor
exposure too high), so that each exclusion is traceable to a single most-fundamental
cause. Thermal state, decision confidence, and evidence confidence are retained as
independent fields, with evidence confidence set to the weakest link of
opening-hours completeness and thermal-evidence quality; a low value triggers an
insufficient-evidence exclusion, so an uncertain thermal decision propagates into
the screening outcome rather than being hidden. The meaningful-improvement margin is
0.8 °C — the median per-row demonstrated UTCI sensitivity across the outdoor rows —
applied together with categorical rules (an indoor refuge relative to an outdoor
source, a strictly cooler outdoor UTCI category, or a confidence gain without
becoming hotter).

Surviving candidates are returned as a set annotated with distance, walk time,
indoor/outdoor status, experience type, UTCI and its envelope, and the confidence
fields, with trade-offs exposed rather than resolved into a single ranked number.
The output is a set of screened, surviving alternatives; the framework makes no
claim that any tourist will choose, follow, or prefer them.

## 3.8 Conventional baseline and decision scenarios

To test whether heat-aware screening changes the option set a conventional tool
would return, we compare against a deliberately naive nearest-open baseline: the
closest open tourism asset within the same walking radius, selected with no thermal
or evidence screening. Accessibility for both the screening layer and this baseline
is a straight-line (haversine) walking distance converted to time at 4.8 km/h, with
a primary pedestrian reach of 800 m (about ten minutes) and sensitivity re-runs at
500 and 1200 m. Straight-line distance is used only as an ordinary-reach constraint
and is a documented lower bound on true walking distance; no routing or route-level
heat exposure is modelled.

The comparison is run over eight pre-registered decision scenarios, each a real
source asset at one of the three hours with a specified accessibility radius, chosen
to span the required decision classes — an exposed monument screened to an indoor
refuge, an exposed monument screened to a cooler outdoor space, cases with several
alternatives of differing experience type, a case where a candidate is available but
its evidence is too weak, and a case where the source's own thermal decision is
uncertain. One scenario (a source in an already-relatively-cool central park under a
constrained 500 m radius) is included as a valid no-survivor test, in which the
engine is expected to return an explicit no-recommendation outcome rather than a
forced pick. This comparison evaluates whether heat-aware screening changes decision
support relative to a proximity-only tool; it does not measure, and makes no claim
about, tourist behaviour or travel substitution.

## 3.9 Validation strategy and claim boundaries

Validation is separated into internal checks, physical-plausibility checks, and
what was not validated.

**Internal and technical validation.** All reported outputs regenerate from the
open pipeline over locked inputs with per-file integrity checks; every excluded
candidate resolves to exactly one machine-readable reason with no untraceable rows;
and the solar-forcing and accessibility-radius sensitivity analyses test the
stability of the decisions actually reported.

**Physical-model plausibility.** The forcing is drawn from real station
observations, with the single estimated input (irradiance) gated on an observed
clear-sky condition, and the modelled Tmrt and UTCI ranges and their spatial and
temporal behaviour were checked for consistency with published SOLWEIG-class values
for comparable climates. This is a plausibility check, not a validation of the
modelled radiant field.

**What was not validated.** There is no direct field measurement of Tmrt or UTCI
anywhere in this study; no tourist behavioural response, travel substitution, or
observed outcome is measured; accessibility is straight-line only, with no route-
level heat exposure; and indoor assets are treated as refuges without verified
air-conditioning or queue-exposure conditions.

Taken together, these boundaries define what the study evaluates: the sensitivity of
tourism-feasibility decisions to the choice of thermal method, and the behaviour of
a constraint-first, uncertainty-aware screening architecture relative to a
conventional baseline. It does not evaluate the predictive accuracy of either
thermal method against ground truth, nor any causal effect on tourism outcomes.
