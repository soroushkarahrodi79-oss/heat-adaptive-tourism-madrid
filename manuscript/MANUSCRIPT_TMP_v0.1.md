# Thermal representation as a decision variable in heat-adaptive tourism opportunity screening: evidence from a Madrid pilot

*Prepared for submission to* **Tourism Management Perspectives** *(primary target).*

**Authors:** [AUTHOR NAME(S) TO VERIFY]

**Affiliations:** [AFFILIATION(S) TO VERIFY]

**Corresponding author:** [NAME TO VERIFY], [EMAIL TO VERIFY]

**ORCID:** [ORCID(S) TO VERIFY]

---

## Abstract

Extreme heat is a time- and place-sensitive management problem for urban tourism,
yet broad climate-suitability assessment operates at a coarse scale, while downstream
thermal routing and heat-adjusted accessibility presuppose the candidate set, leaving
open the upstream question of which tourism opportunities should remain feasible
candidates at a given hour. This study develops a constraint-first, uncertainty-aware
architecture for screening urban tourism opportunities under heat and tests how much
the choice of thermal representation matters. On a documented extreme-heat day in
Madrid, across 27 tourism assets at three times of day, feasibility was assessed two
ways: with a simple operational proxy combining ambient air-temperature hazard
thresholds and nearby tree-presence information, and with physically based SOLWEIG/UTCI
modelling. Changing the thermal representation reclassified one third of outdoor
asset-time observations (33.3%, 14 of 42), in both directions. Relative to a
conventional nearest-open baseline, constraint-first screening changed the
feasible-alternative set in 7 of 8 decision scenarios, the nearest-open option failed
screening in 3 of 8, and one scenario returned an explicit no-defensible-alternative
outcome when no candidate qualified. The analysis evaluates decision sensitivity to
thermal-method choice rather than the accuracy of either method against ground truth.
The findings indicate that thermal representation is a substantive modelling choice in
heat-adaptive tourism decision support, and that a constraint-first architecture can
expose that sensitivity while keeping uncertainty, evidence, and exclusion logic
explicit and complementing downstream routing and accessibility methods. Results are
limited to a single Madrid pilot without direct field validation of Tmrt/UTCI or
observed tourist behaviour.

**Keywords:** Urban tourism; Extreme heat; UTCI; Tourism decision support; SOLWEIG;
Uncertainty-aware decision-making

---

# 1. Introduction

In the tourism cities of Southern Europe, extreme-heat episodes increasingly overlap
with the summer season and with the daytime, outdoor conditions under which much
urban tourism takes place. Open plazas, monument forecourts, gardens, and the walking
segments between attractions become heat-exposed during these hours, and aggregate
studies show that urban activity contracts and shifts as temperatures rise (Extreme heat and urban mobility, 2025). For destination management this is an
operational problem rather than only a long-run climatic one: on a given afternoon,
some outdoor opportunities become uncomfortable or unsuitable while others, and most
indoor options, remain usable, and visitors and the organisations that guide them
must decide among these options in near-real time. Yet heat governance has developed
largely around residents and public-health warning systems, and frameworks for
embedding tourism in heat action planning are only now being articulated (Heat risk action planning for tourism, 2026; OECD, 2026). Southern-European destinations are already adapting in practice
(Tourism in a warming climate, 2026), and destination demand and
development are increasingly shaped by these conditions (Tourist demand under climate change, 2025).
Critically, the exposure of tourism to heat is spatially uneven at the intra-urban
scale (Tourism exposure to weather extremes, 2024), which is exactly the
scale at which visitors experience comfort in a historic core (Plaza thermal comfort in Madrid and Sevilla, 2022).
The practical decision is opportunity-level and time-specific: which of the
attractions in front of a visitor this afternoon should remain on the table.

The dominant way to characterise tourism and climate has been the composite climate
index. Instruments such as the Tourism Climate Index and the Holiday Climate Index
combine several weather variables into an aggregate suitability score, and they are
well suited to comparing destinations or seasons at a broad scale (HCI/TCI inter-comparison, 2016; Hungarian HCI/TCI, 2025). These
indices remain useful for their intended purpose, but two features limit their reach
for opportunity-level screening. First, their outputs are known to depend on the
choice of component weights and thresholds, so the same conditions can yield
different suitability readings under different, defensible parameterisations
(Reliability of tourism climate indices, 2016) — a
property shared with weighted multi-criteria site-suitability approaches more broadly
(GIS-AHP tourism suitability, 2011). Second, and more fundamentally here, they are
designed for destination- or season-scale characterisation, not for resolving which
individual microsite is feasible at which hour. A city-scale or daily suitability
summary does not distinguish a sun-exposed plaza from a shaded garden a few hundred
metres away, nor a noon exposure from a late-afternoon one. Screening an individual
opportunity requires a per-site, per-hour eligibility judgement — is this place
usable now, and if not, what nearby option is — which an aggregate score is not
constructed to provide. The limitation is one of spatial and temporal scale and of
decision purpose, not of validity.

Physically based thermal modelling resolves part of what an aggregate or
air-temperature-based summary cannot. Mean radiant temperature (Tmrt) represents the
combined short- and long-wave radiant load on a person, and radiation-resolving
models of the SOLWEIG class compute it at pedestrian scale from building and
vegetation geometry and the solar path (Lindberg et al., 2008); combined with air
temperature, humidity, and wind, it yields the Universal Thermal Climate Index
(UTCI), a modelled index of heat stress on a standardised body (Bröde et al., 2012).
Such models capture the shade- and geometry-driven heterogeneity that ambient
temperature and simple vegetation counts do not, and they have been used for
city-scale comfort mapping and design (WRF-UCM-SOLWEIG mapping, 2024), with a growing literature cautioning that surface- or
air-temperature summaries are not interchangeable with human-centred heat stress
(Beyond land surface temperature, 2026). To date, however, these radiation-resolving
models have mostly served design, planning, and mapping; they are rarely wired
transparently into an auditable, opportunity-level tourism decision, so their
information reaches the screening stage only indirectly, if at all. It is important to be exact about what this
buys. These approaches provide a different representation of the thermal environment,
resolving additional physical dimensions relevant to pedestrian exposure; they are
not, on their own and without in-situ measurement, a validated ground truth against
which a simpler method can be called wrong (Gál & Kántor, 2019). The question this raises for tourism decision-support is therefore not which
thermal method is correct, but whether the choice of thermal representation
materially changes a tourism-screening decision — a question that can be answered by
comparison even where neither representation has been field-validated.

A fast-moving strand of heat-mobility research has begun to connect thermal exposure
to movement, and it defines the boundary of the present study most sharply. Thermal
routing takes an origin and a destination as given and finds the path of least
thermal exposure between them (Cool Routes, 2026; CoolWalks, 2025). Thermal-adjusted accessibility takes a destination set as
given and measures how many destinations remain reachable under heat-adjusted travel
(UTCI-adjusted pedestrian accessibility, 2026), and
related work maps sidewalk-level heat risk along pedestrian networks (Colaninno et al., 2025) or examines whether cool refuges are equitably reachable (Barcelona climate-shelter accessibility, 2025). These methods are advancing quickly and
are complementary to what follows; they operate, however, at a downstream decision
stage. Each presupposes the candidate set — the destinations or refuges whose paths
or reachability are then evaluated. The upstream management question is distinct:
which tourism opportunities should remain eligible candidates at a given hour under
thermal, operational, accessibility, and evidence constraints, before any route is
planned or any reachability computed. That screening step, and the surviving
candidate set it produces, is what a downstream routing or accessibility method would
consume.

Among the closest approaches identified in a targeted review of this literature, we
found that routing, accessibility, thermal mapping, and composite climate suitability
are each addressed separately, and none screens individual tourism opportunities by
explicit physical-thermal, accessibility, and evidence constraints at a specific hour
while keeping hazard, exposure, confidence, and evidence traceably distinct. The
present study addresses that screening stage. It develops a constraint-first,
uncertainty-aware architecture for screening urban tourism opportunities under heat —
one that evaluates each opportunity against an ordered sequence of hard constraints,
records a single machine-readable reason for every exclusion, keeps the thermal state
separate from the confidence in the decision, and returns a set of surviving
alternatives or, where nothing qualifies, an explicit no-recommendation outcome
rather than a forced choice. In treating uncertainty as a first-class, categorical
property of each decision rather than folding it into a single composite score, the
architecture draws on the tradition of uncertainty-aware spatial decision-support
(Participatory-GIS under uncertainty, 2025; Monte-Carlo UTCI/PET reliability, 2025). Because the architecture places the thermal input in an
explicit and swappable position, it also supports a direct empirical test of how much
that input matters: the study compares a simple operational proxy — combining ambient
air-temperature hazard thresholds with nearby tree-presence information — against a
physically based (SOLWEIG/UTCI) configuration, and against a conventional
nearest-open recommender, on a single documented extreme-heat day in central Madrid.
The contribution is thus an applied, reproducible decision-support architecture
together with a case-based demonstration of whether thermal-method choice is
decision-relevant; it does not rest on either thermal method being validated, and it
makes no claim about tourist behaviour, flows, or outcomes. The study is guided by
three research questions:

- **RQ1 (method sensitivity).** Does physically based (SOLWEIG/UTCI) thermal
  modelling materially alter tourism-feasibility classifications relative to the
  simple air-temperature-and-tree-presence proxy, and is any difference physically
  interpretable?
- **RQ2 (decision-support value).** Does constraint-first, heat-aware screening
  change the set of feasible alternatives relative to a conventional nearest-open
  baseline, and does it decline to recommend when nothing accessible qualifies?
- **RQ3 (robustness and traceability).** Do those decisions remain auditable and
  stable under the tested uncertainty while preserving explicit no-recommendation
  outcomes?

---

# 2. Methods

## 2.1 Study design and study area

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
gardens — while remaining small enough to keep every asset individually inspectable (Fig. 1a).

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
indoor assets bypass the outdoor thermal model by construction (Section 2.4). The
individual tourist is explicitly not a unit of analysis, and no quantity in this
study describes tourist behaviour, choice, or flow.

## 2.2 Data sources and preprocessing

All inputs are open data with documented provenance (Table 1). We distinguish three
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

**Modelled and derived physical inputs.** The physical thermal model (Section 2.4)
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

## 2.3 Simple-proxy baseline

The comparison baseline is a constraint-first, open-data feasibility
classification that uses no radiative, surface-temperature, or shadow information.
It combines exactly two inputs through a decision rule. It is not a land-surface-
temperature product, a satellite surface-temperature proxy, a canopy or shade
model, or a shadow simulation; no such quantity enters it.

The first input is an ambient air-temperature hazard band. The observed hourly air
temperature (Section 2.2) is classified against AEMET's official Meteoalerta
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

## 2.4 Physically based thermal-exposure modelling

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

## 2.5 Thermal-method comparison

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

## 2.6 Uncertainty and robustness treatment

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

## 2.7 Constraint-first tourism opportunity screening

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
mislabelled as thermally inadequate. There is no weighted composite score anywhere in the chain (Fig. 1b).

Every candidate carries one machine-readable exclusion reason from a fixed
vocabulary (for example, closed at timestamp, accessibility constraint, thermal
limit exceeded, insufficient evidence, no meaningful thermal improvement, or outdoor
exposure too high), so that each exclusion is traceable to a single most-fundamental cause (Table 2). Thermal state, decision confidence, and evidence confidence are retained as
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

## 2.8 Conventional baseline and decision scenarios

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

## 2.9 Validation strategy and claim boundaries

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

---

# 3. Results

Results are reported for the locked pilot: 27 tourism assets on 21 August 2023 at
12:00, 15:00, and 18:00, with thermal-method comparison on the 42 outdoor asset ×
timestamp observations (14 outdoor assets × 3 hours) and screening evaluated across
eight pre-registered decision scenarios. All figures are descriptive; the unit is
the asset × timestamp observation or the scenario comparison, not a population
sample, and no inferential test is applied.

## 3.1 Thermal-method sensitivity

Across the 42 outdoor observations, the simple-proxy baseline and the
physically based (SOLWEIG/UTCI) configuration assigned the same feasibility state
in 28 observations and differed in 14, a reclassification rate of 33.3% (14/42)
(Table S1). Both directions of change occurred: the physically based configuration
produced a more restrictive feasibility state than the proxy in 9 observations
(the proxy state was less cautious) and a less restrictive state in 5 (Fig. 2).
Reclassification was therefore not one-directional.

The divergence was concentrated in time rather than distributed evenly across the
day (Fig. 2). Reclassification reached 64.3% (9/14) at 12:00, fell to 0.0% (0/14)
at 15:00, and was 35.7% (5/14) at 18:00. The two methods agreed on every outdoor
observation at 15:00 and disagreed most often at noon.

The same rate did not vary with asset morphology. Reclassification was 33.3% within
each of the four morphology groups — attraction exterior (3/9), park or garden
(6/18), plaza or hardscape (4/12), and street corridor (1/3) — matching the overall
rate in every group (Table S1). The time-of-day pattern above was therefore not
reproduced across morphology classes.

The noon pattern reflects the difference between the two inputs. At 12:00 the
observed ambient air temperature was 34.2 °C, which falls in the LOW meteorological
hazard state under the locked AEMET operational warning thresholds. Despite that
LOW hazard state, the modelled UTCI equalled or exceeded the 32 °C boundary used in
the physical-model feasibility configuration at all 14 of the 14 outdoor assets
(Fig. S1). The proxy, keyed to the ambient hazard band, and the physically based
configuration, keyed to modelled UTCI, therefore assigned different feasibility
states at most noon observations, whereas at 15:00 both configurations placed every
outdoor observation in the same conditional-feasibility state.

The finding of this subsection is limited to the following: feasibility
classification outcomes were sensitive to the choice of thermal method, and the
sensitivity was largest at 12:00.

## 3.2 Effects on tourism-opportunity screening

Each scenario began from a real asset in a constrained state on the study day. Seven
of the eight sources were open outdoor sites in the very-strong-heat-stress category
(modelled source UTCI ranging from 38.6 to 45.4 °C) and one (S5, Real Observatorio
de Madrid) was closed at its timestamp. Screening behaviour was evaluated across the
eight scenarios by comparing the constraint-first surviving-alternative set against
a conventional nearest-open baseline that applies no thermal or evidence screening
(Table 3). The surviving
candidate set differed from the nearest-open set in 7 of the 8 scenarios; it was
unchanged in one (S7), where the nearest-open pick already satisfied the locked
constraints and no additional candidate was screened out.

The nearest-open pick itself did not satisfy the locked screening constraints in 3
of the 8 scenarios (S2, S6, S8). In each of these three the nearest open asset was
an outdoor site that was not cooler than the source, and each was screened out with
the same machine-readable reason, `OUTDOOR_EXPOSURE_TOO_HIGH` (Table 3). Across all
eight scenarios, 23 open, in-radius candidate options were screened out on thermal
or evidence grounds — that is, they were open and within the walking radius but did
not satisfy the thermal or evidence constraints (Fig. 3). Surviving alternatives
are reported as a set with their trade-offs (indoor/outdoor, distance, experience
type, UTCI, and confidence) rather than ranked into a single value.

Seven of the eight scenarios returned a non-empty surviving set (state
`ALTERNATIVES_FOUND`), with the number of surviving alternatives ranging from 4 to
9; the eighth returned none. The surviving sets spanned different experience types
within a single scenario — for example indoor cultural refuges, transit refuges,
and cooler outdoor spaces — which were reported as distinct options rather than
merged.

One scenario returned no surviving alternative. In S8 the source was Parque del
Retiro at 15:00 under a 500 m accessibility condition. Of the 26 candidate rows
evaluated, 0 satisfied the full constraint sequence: the accessible outdoor
candidates were not cooler than the already-relatively-cool source and were
screened out as `OUTDOOR_EXPOSURE_TOO_HIGH`, while the indoor refuges fell outside
the 500 m radius and were screened out as `ACCESSIBILITY_CONSTRAINT`. The scenario
therefore resolved to the explicit state `NO_DEFENSIBLE_ALTERNATIVE` (Fig. 3). This
outcome was produced by the locked screening rules operating on the locked inputs;
it was not a manually imposed result or a processing error, and no surviving
alternative was withheld.

The finding of this subsection is limited to the following: thermal and evidence
screening altered the candidate set relative to a nearest-open baseline in seven
scenarios, removed the nearest-open pick in three, and returned an explicit
no-alternative state in one.

## 3.3 Robustness and traceability

The reclassification and screening results were examined against the tested
solar-forcing perturbations (Fig. 4). Replacing the clear-sky irradiance estimate
with the satellite-derived irradiance realization changed 1 of the 42 outdoor
decisions (2.4%). That single change was La Rosaleda (A24) at 18:00, where the
satellite realization raised the envelope to the 46 °C feasibility boundary; it is
the same observation classified UNSTABLE below. The −10% irradiance perturbation
changed 0 of 42 decisions, and the −20% irradiance perturbation also changed 0 of
42. The noon result of Section 3.1 persisted under every tested solar-forcing scenario: all 14 outdoor assets
remained at or above the 32 °C UTCI boundary at 12:00 under the clear-sky baseline,
the satellite-derived realization, and both irradiance reductions.

Decision confidence was carried as a field separate from thermal state, so that the
physiological stress category and the confidence in the feasibility decision were
reported side by side rather than combined. Over the 42 outdoor observations the
confidence classification was ROBUST for 35 (83.3%), BOUNDARY for 6 (14.3%), and
UNSTABLE for 1 (2.4%). The single UNSTABLE observation was La Rosaleda (A24) at
18:00, where a tested realization placed the decision on the opposite side of the
46 °C feasibility boundary from the baseline. The 6 BOUNDARY observations occurred
at 15:00 and 18:00, with envelope maxima between 44.5 and 45.9 °C — within their
demonstrated sensitivity of the 46 °C boundary but not crossing it. All remaining
observations either did not approach a threshold within their demonstrated
sensitivity or did not cross one under any tested realization.

The UNSTABLE observation propagated into screening through the evidence gate rather
than being suppressed. Where A24 was a candidate (S4), its low evidence confidence
produced an `INSUFFICIENT_EVIDENCE` exclusion while other alternatives survived;
where A24 was the source (S7), the screening still returned surviving alternatives
and flagged the source's own decision as uncertain. Across the scenarios every
excluded candidate carried exactly one machine-readable exclusion reason, and the
no-recommendation state (S8) remained an available explicit outcome of the same
rule set.

The finding of this subsection is limited to the following: the reported decisions
remained unchanged under the tested solar-forcing perturbations with the single
noted exception, decision confidence was reported separately from thermal state,
and every exclusion and the no-recommendation outcome were traceable to an explicit
reason.

---

# 4. Discussion

The pilot establishes a single, bounded claim: on this case, different thermal
representations can materially change which tourism opportunities a screening
system treats as feasible, and a constraint-first architecture can make those
changes, the constraints behind them, and their confidence explicit. It does not
establish that the physically based configuration is correct and the proxy wrong;
neither representation was field-validated here, and the interpretation below is
kept to method sensitivity rather than accuracy throughout.

## 4.1 Thermal representation is decision-relevant

Roughly one-third of outdoor observations changed feasibility state when the thermal
input was switched from the simple proxy to the physically based configuration, and
the change ran in both directions — the physical configuration was more restrictive
in nine observations and less restrictive in five. Two properties of this result
matter for interpretation. First, because the reclassification is two-directional,
it cannot be read as a one-way bias that a single offset would remove; the choice of
thermal representation reshapes decisions in both directions, which is what makes it
a decision variable rather than a calibration constant. Second, the divergence is
strongly time-dependent — largest at midday, absent at 15:00, intermediate at 18:00
— so it is a feature of when the two representations carry different information, not
a uniform gap between them.

The noon pattern makes the mechanism concrete. At 12:00 the observed ambient air
temperature was 34.2 °C, which sits in the LOW band of the AEMET civil-protection
warning scale, while the modelled UTCI was at or above the 32 °C strong-heat-stress
boundary at all fourteen outdoor assets. The two methods encode different thermal
information: the operational proxy is keyed to ambient air-temperature warning
thresholds and local tree presence, whereas the physical configuration additionally
resolves radiant exposure through Tmrt and UTCI. Differences between them can
therefore emerge before an air-temperature warning threshold is crossed, precisely
when radiant load is high but the air is not yet at a warning level. This is
consistent with the urban-microclimate literature in which shading and geometry,
not air temperature, dominate mean radiant temperature (e.g. Gál & Kántor, 2019; WRF-UCM-SOLWEIG mapping, 2024), and with work arguing that surface- or
air-temperature summaries are not interchangeable with human-centred heat-stress
indices (Beyond land surface temperature, 2026).

It is important to state what this does not mean. The AEMET warning thresholds and
the UTCI configuration are not two competing measurements of the same quantity. The
warning scale is a civil-protection instrument defined on ambient air temperature;
UTCI is a modelled index of radiant-inclusive heat load on a standardised body. That
a LOW warning state coexists with a strong-heat-stress modelled index does not show
that the warning scale understated conditions or that the proxy failed to detect
real heat; it shows that the two instruments represent different constructs and can
diverge. The contribution here is to quantify that this divergence propagates into
tourism-screening decisions, which the composite tourism-climate-index tradition —
where weight and threshold choices are already known to move suitability outcomes
(HCI/TCI inter-comparison, 2016; Reliability of tourism climate indices, 2016) — had
not examined at the level of a screening decision. The sensitivity to representation
is not confined to the proxy-versus-physical contrast: within this study, even
simple open-data vegetation proxies did not converge closely with one another,
which is consistent with treating the representation of thermal exposure as a
substantive decision input rather than a settled preprocessing detail. The practical reading is that
thermal representation should be treated as a substantive modelling choice in
spatial tourism decision-support, not merely a technical preprocessing step; the
pilot supports this on one case rather than as a universal conclusion.

## 4.2 Screening before routing: a distinct decision-support layer

Heat-aware screening changed the option set that a conventional proximity tool would
return. The surviving candidate set differed from a nearest-open baseline in seven
of eight scenarios, the nearest-open pick itself did not satisfy the screening
constraints in three, and across the scenarios a number of open, in-radius options
were removed on thermal or evidence grounds. These are statements about the option
set, not about what any visitor would do; no behavioural response is claimed or
tested.

The result is best positioned by making the decision-support layer explicit.
Heat-aware routing takes an origin and a destination as given and asks which path
minimises thermal exposure (Cool Routes, 2026; CoolWalks, 2025). Thermal-adjusted
accessibility takes a destination set as given and asks how many destinations remain
reachable under heat (UTCI-adjusted pedestrian accessibility, 2026). The approach
here operates upstream of both: before a route or a reachability count, it asks
which tourism opportunities should remain eligible at a given hour under thermal,
operational, accessibility, and evidence constraints. Among the closest approaches
identified in the targeted review, these routing and accessibility methods
presuppose the candidate set, whereas the constraint-first approach produces and
filters it. This is a complementary upstream layer rather than a replacement: it
does not eliminate the overlap with the routing literature, and a downstream routing
or accessibility method could in principle consume the surviving candidate set.
Routing was deliberately outside the scope of this study, and the boundary is drawn
to complement that frontier, not to compete with it.

The three cases in which the nearest-open pick did not survive screening — each an
outdoor site that was not cooler than the source — illustrate a concrete failure
mode of proximity-only guidance under heat, and connect to the tourism heat-
governance literature that frames attraction-level warnings and closures as
management levers (Heat risk action planning for tourism, 2026). The screening layer
adds an operational step to that governance picture; it does not, on this evidence,
show that using it changes any realised management or visitor outcome.

## 4.3 Explicit non-recommendation and traceability

One scenario returned no surviving alternative. From Parque del Retiro at 15:00
under a 500 m accessibility condition, all twenty-six evaluated candidates were
screened out — accessible outdoor options because they were not cooler than the
already-relatively-cool source, indoor refuges because they lay outside the radius —
and the scenario resolved to an explicit no-alternative state. This is an
architectural property rather than a normative recommendation. A system built on
hard, ordered constraints does not need to return a ranked pick when nothing
satisfies its predefined conditions, which contrasts with recommender designs that
necessarily surface an ordered list or a top choice. The interpretive point is
narrow: an explicit no-alternative outcome preserves the meaning of the constraints
and prevents a weak option from being presented merely because it is the least
unsuitable candidate available.

This behaviour sits alongside equity-oriented accessibility work in which spatial
proximity alone is shown to be insufficient for meaningful access to cool refuges
(Barcelona climate-shelter accessibility, 2025), and alongside uncertainty-aware
spatial decision-support that treats "no defensible option" as a legitimate result
rather than a failure. The traceability of the outcome follows from the same
structure: because each candidate is eliminated by the first constraint it fails,
every exclusion carries a single machine-readable reason, and the no-alternative
state is itself a reason-bearing output rather than a silent gap. This is a property
of the first-failing-gate design and of keeping the decision out of a single
composite score; it is an architectural and transparency distinction, not empirical
proof that the resulting guidance improves management outcomes.

## 4.4 Robustness, uncertainty, and appropriate confidence

The main decision patterns were stable under the solar-forcing perturbations
actually tested. Substituting a satellite-derived irradiance realization for the
clear-sky estimate changed one of forty-two decisions, and ±10% and ±20% irradiance
perturbations changed none; the noon result held under every tested realization.
This is a statement about stability under the tested forcing, not a validation of
the modelled radiant field, which remains unmeasured.

The design keeps thermal state and decision confidence as separate fields, and the
robustness results show why that separation is useful. A high thermal-stress state
can coexist with genuine uncertainty about the precise decision boundary. The one
observation classified UNSTABLE — La Rosaleda at 18:00 — is an example: it is firmly
in a very-strong-heat-stress state, yet a tested realization moves it across the
46 °C feasibility boundary, so the decision is confidently "hot" while the
feasibility call at that specific threshold is not robust. Collapsing stress and
confidence into one number would hide exactly this distinction; reporting them
separately lets the uncertain case be flagged and, through the evidence gate,
excluded when it is a candidate rather than silently carried. The remaining
near-boundary observations behave similarly, sitting close to the 46 °C threshold
within their own demonstrated sensitivity without crossing it.

This treatment is deliberately partial. Uncertainty was propagated only across the
tested dimensions — solar forcing across all outdoor rows and targeted canopy
geometry for two assets — and does not cover air-temperature, humidity, wind, or
model-structural uncertainty. The confidence labels therefore mean robust against
what was tested, not certain. Relative to uncertainty-aware spatial decision-support
that propagates input uncertainty into a combined reliability estimate (Monte-Carlo UTCI/PET reliability, 2025; Participatory-GIS under uncertainty, 2025), the approach here differs by keeping uncertainty categorical and attached to
the individual decision rather than folded into one composite figure — a
transparency choice, not a claim of more complete quantification.

## 4.5 Contribution and transferability

Taken together, these results point to an applied decision-support contribution
rather than a new metric or algorithm. The proposed framework keeps four things
visible as distinct inputs to a screening decision — the thermal representation, the
operational and accessibility constraints, the sufficiency of the underlying
evidence, and the tested uncertainty — instead of collapsing them into a single
composite suitability score. The Madrid pilot is a case-based demonstration that
this separation is not cosmetic: changing one of those inputs, the thermal
representation, materially altered the feasible candidate set, and the architecture
made that change and its confidence auditable. The reproducible pipeline behind the
reported tables is part of this contribution; a read-only visual prototype exists as
a supplementary demonstration of implementation feasibility and is not itself a
result.

Transferability should be read at two levels. The architecture — constraint-first
elimination with a first-failing-gate reason, explicit exclusions, confidence kept
separate from thermal state, an explicit method-sensitivity comparison, and an
explicit no-survivor state — is potentially transferable to other destinations and
episodes. Its operational parameters are not automatically transferable: the hazard
and UTCI thresholds, the accessibility distances, the curated assets and their
opening schedules, the local urban geometry and thermal forcing, and the specific
Madrid results are all setting-dependent. The architecture is therefore potentially
transferable, whereas its operational parameters require local calibration and
validation before use elsewhere.

These interpretations rest on real boundaries that constrain how far they reach.
There is no direct field validation of Tmrt or UTCI; the evidence is one city, one
extreme-heat day, and twenty-seven assets; the canopy geometry is dated for part of
the domain; the uncertainty envelope is partial; accessibility is straight-line with
no en-route thermal exposure; the indoor-refuge assumption is unverified for
air-conditioning and approach exposure; and the opening hours are documented at a
later date than the study day. These limitations bound the interpretation to a
demonstration of method sensitivity and of a transparent screening architecture on a
single well-characterised pilot; they are set out in full in the following section.

---

# 5. Limitations and scope conditions

The findings should be read against a set of boundaries that fix what the study can
and cannot support. These are stated in order of consequence and are not argued away;
several are permanent properties of the design rather than gaps a minor extension
would close.

## 5.1 Physical-model validation boundary

The most consequential boundary concerns the status of the physical thermal fields.
Mean radiant temperature and UTCI were model-derived at every asset; no direct field
measurements of Tmrt or UTCI were collected anywhere in the study. The available
station observations (air temperature, humidity, wind, pressure) support only the
meteorological forcing of the model, not the modelled radiant field: they constrain
the inputs, not the output. SOLWEIG was assessed through plausibility checks and
sensitivity analysis, not against in-situ radiant or comfort measurements, and
consistency with published SOLWEIG-class value ranges is a plausibility statement,
not a validation of this implementation — precedent for the model in general does
not certify the specific configuration used here.

It follows that the proxy-versus-physical comparison evaluates decision sensitivity
to the choice of thermal method, not the accuracy of either method against ground
truth. A reclassified observation shows that the two representations disagree in a
way that changes the screening decision; it does not show that one representation is
correct and the other wrong. This boundary is load-bearing for the whole paper: the
contribution is the demonstration that method choice is decision-relevant, and it
does not require, or assert, that the physical configuration is the more accurate
account of on-site conditions.

## 5.2 Spatial and temporal scope

The empirical evidence is a single case. It covers one city, one pilot area of
approximately 3.5 km², one documented extreme-heat day, three fixed timestamps, 27
curated tourism assets, and 42 outdoor asset × timestamp comparisons. The assets
were purposively selected to span a range of adaptation conditions rather than
sampled at random, so the set is not a statistically representative sample of Madrid
tourism sites, and the reported rates are properties of this configuration rather
than population estimates.

Consequently the study cannot establish seasonal behaviour, climatological averages,
city-wide performance across Madrid, cross-city generalisability, or behaviour under
different meteorological regimes; a single extreme-heat day says nothing about milder
days or other synoptic conditions. This design is appropriate for demonstrating an
architecture and for quantifying method sensitivity on a well-characterised case; it
is not a basis for population-level or climatological inference, and none is drawn.

## 5.3 Input and uncertainty limitations

The uncertainty treatment is partial by construction. The reported confidence
classes rest on an envelope built from the realizations actually computed: solar
forcing across all outdoor rows (a clear-sky estimate, a satellite-derived
realization, and −10% and −20% irradiance perturbations) and, for two assets,
targeted vegetation-geometry variants. Several uncertainty sources were not
propagated — spatial variability in wind, humidity and air-temperature uncertainty,
full vegetation uncertainty across the domain, model-structural uncertainty, and the
range of possible radiation errors; wind and humidity in particular were applied as
single station values across the raster rather than resolved spatially.

The vegetation geometry also carries a temporal-vintage limitation: the LiDAR canopy
is dated for parts of the study area, and the targeted corrections addressed the
identified decision-critical cases rather than reconstructing the entire urban
canopy, so some residual canopy uncertainty remains outside the two corrected sites.

The confidence labels must be read accordingly. A ROBUST, BOUNDARY, or UNSTABLE
classification expresses robustness to the tested uncertainty space, not total
certainty; the per-row demonstrated sensitivity underlying these labels is a lower
bound on the true uncertainty, because it reflects only the dimensions that were
varied. A ROBUST label means robust against what was tested, not validated.

## 5.4 Tourism and accessibility limitations

Accessibility was represented as straight-line distance converted to walking time.
The study used no pedestrian route geometry, modelled no thermal exposure during
travel, and included no slope or walking-cost model; straight-line distance is a
lower bound on true walking distance and an ordinary-reach constraint only. The
screening layer therefore operates on candidate opportunities and does not represent
the journey to them.

The framework is likewise bounded away from behaviour. It used no behavioural
response data, observed no visitor substitution, and was not validated against
revealed or stated preferences. It screens the set of candidate opportunities under
explicit constraints; it does not predict what tourists will choose, whether they
will follow a surviving alternative, whether visitor flows would redistribute, or
whether exposure or health outcomes would improve. Those quantities are outside the
evidence and are not claimed.

Indoor opportunities require particular caution. Indoor status was handled through a
refuge-bypass logic that assumes thermal buffering; indoor air temperature, air
conditioning, queue and entrance-waiting exposure, and actual indoor comfort were
not observed, and indoor thermal evidence was capped below the highest confidence
level by design for this reason. Surviving indoor alternatives should therefore be
read as assumed refuges under this logic, not as physically verified cool refuges.

## 5.5 Operational-data and retrospective-alignment limitations

Opening hours were captured and documented at a later date and applied
retrospectively to the 2023 study day; where machine-readable tags were absent, hours
were filled from documented institutional schedules, each recorded with its source
and a completeness flag. This is sufficient for a reproducible screening
demonstration but is not proof that every establishment kept the same schedule on 21
August 2023 — the real Monday-in-August closures used are cited, but a specific
establishment could have deviated — and the contextual open-data layers carry their
own vintage and completeness limitations of the same kind. This boundary affects the
interpretation of a specific candidate's availability at a given hour, not the
thermal modelling, which is driven by the observed meteorology for the study day.

## 5.6 Scope conditions and transferability

These boundaries separate what may transfer from what does not. The potentially
transferable part is the architecture: constraint-first screening, first-failing-gate
explanations, thermal state kept separate from decision confidence, explicit
machine-readable exclusion reasons, an explicit no-survivor state, and the direct
comparison of alternative thermal representations. Its operational components are
setting-specific and do not transfer automatically: the thermal thresholds, the
accessibility radius, the opening-hours schedules, the asset set and its
tourism-relevance judgements, the local urban geometry, the meteorological forcing,
and the local adaptation resources. The architecture is therefore potentially
transferable, whereas its operational parameters and empirical performance require
local calibration and validation before use in another setting.

Taken together, these limitations bound the interpretation to a demonstration, on a
single well-characterised pilot, that thermal-method choice is decision-relevant for
heat-adaptive tourism screening and that a constraint-first architecture can expose
that sensitivity, its constraints, and its confidence.

## 5.7 Future work

The clearest extensions are those that would raise the evidence ceiling rather than
add features. Direct field measurement of Tmrt and UTCI would move the physical
configuration from plausibility toward accuracy assessment and is the single
highest-value next step. Multi-day and seasonal evaluation, and additional city
contexts, would test whether the method-sensitivity pattern holds beyond one extreme
day and one urban core. Route-level thermal exposure would replace the straight-line
reach constraint with a modelled journey; observed tourist behaviour would test
whether screening relates to any realised choice; and verified indoor thermal
conditions would replace the refuge assumption with measurement. Each targets a
specific boundary named above; none is required for the present claim, and none is
assumed here.

---

# 6. Conclusion

This study examined whether the choice of thermal representation affects
time-specific screening of urban tourism opportunities under extreme heat, and
whether a constraint-first architecture changes the set of feasible alternatives a
conventional proximity tool would return. On a single documented extreme-heat day in
central Madrid, changing the thermal representation from a simple operational proxy
to a physically based (SOLWEIG/UTCI) configuration altered one third of outdoor
asset-time feasibility classifications, and the change ran in both directions and was
concentrated at particular hours rather than spread evenly through the day. Because
it moves in both directions, the divergence is a matter of thermal-method
sensitivity, not of one representation being validated against the other; neither was
field-measured here. Relative to a conventional nearest-open baseline, the
constraint-first screening changed the feasible-alternative set in seven of eight
decision scenarios.

The architecture is what makes these differences legible. It keeps the thermal state,
the implied decision state, the confidence in that decision, the sufficiency of the
underlying evidence, and the reason for each exclusion as separate fields rather than
folding them into a single composite suitability score. Because each candidate is
eliminated by the first constraint it fails, every exclusion carries a single
traceable reason, and the architecture preserves an explicit no-defensible-alternative
state for cases in which no accessible option satisfies the constraints rather than
returning a weak option by default. This screening step sits upstream of route or reachability calculations:
it produces and filters the candidate set that downstream heat-aware routing and
accessibility methods presuppose, and it complements rather than replaces them.

Within these bounds, the implication for building heat-adaptive tourism
decision-support is that thermal representation should be treated as a substantive
modelling choice rather than a technical preprocessing detail. That implication is
drawn from a single Madrid pilot, without field validation of the modelled Tmrt or
UTCI and without any observation of tourist behaviour, and it is bounded accordingly:
the reported rates are properties of this case, not general performance. Multi-day and
multi-site evaluation, direct thermal measurement, and observed visitor behaviour
would be needed to test how far the pattern and the architecture transfer and whether
they relate to any realised outcome. For destination management, the practical point
is not that one thermal representation is universally preferable, but that the
representation chosen can materially shape which tourism opportunities remain feasible
under heat, and should therefore be made explicit, testable, and uncertainty-aware.

---

# Declarations

**Funding.** [FUNDING STATEMENT TO VERIFY — list any grant/support, or state "This
research received no specific grant from any funding agency in the public, commercial,
or not-for-profit sectors."]

**Declaration of competing interest.** [COMPETING-INTEREST STATEMENT TO VERIFY — e.g.
"The authors declare that they have no known competing financial interests or personal
relationships that could have appeared to influence the work reported in this paper."]

**Data availability.** This study uses only open data: meteorological observations from
AEMET (Madrid/Barajas station); three-dimensional urban geometry from Spanish national
LiDAR products (IGN/CNIG); and tourism assets, tree points, park/garden polygons, and
opening-hours tags from OpenStreetMap (ODbL). The derived analytical tables and figures
reported here are produced by the project pipeline from these locked inputs. [PUBLIC
REPOSITORY / DOI FOR DERIVED OUTPUTS TO VERIFY — a persistent public archive URL/DOI has
not yet been established; until then, availability is "on reasonable request."]

**Code availability.** The screening pipeline and figure-rendering scripts are held in
the project repository. [PUBLIC CODE REPOSITORY URL / LICENCE / RELEASE DOI TO VERIFY.]

**Author contributions (CRediT).** [CREDIT ROLES TO VERIFY per author — e.g.
Conceptualization; Methodology; Software; Formal analysis; Data curation; Writing –
original draft; Writing – review & editing; Visualization.]

**Acknowledgements.** [ACKNOWLEDGEMENTS TO VERIFY, or "Not applicable."]

**Ethics.** This study involved no human participants, no personal data, and no
human-subject research; it analyses open environmental and open geographic data only. No
ethics approval was therefore required. [CONFIRM against the target journal's policy.]

**Generative-AI disclosure.** [PUBLISHER-POLICY PLACEHOLDER — the target publisher
requires authors to disclose any use of generative-AI tools in preparing the manuscript.
The authors' actual tool-use disclosure is to be inserted here verbatim once decided; it
is not drafted on the authors' behalf.]

---

# References

*Author–year style. Entries flagged **[REFERENCE METADATA TO VERIFY]** require the full
author list and/or volume, article/page numbers, and DOI to be completed from the
original source before submission; no such metadata has been fabricated. Titles, journals,
and years are drawn from the locked project literature record.*

1. **Barcelona climate-shelter accessibility (2025).** Are Barcelona's climate shelters
   accessible to vulnerable residents? A mobility-justice analysis. *Cities.* [REFERENCE
   METADATA TO VERIFY: authors; volume; article no.; DOI.]
2. **Beyond land surface temperature (2026).** Beyond land surface temperature:
   explainable spatial machine learning on human heat stress. *Preprint.* [REFERENCE
   METADATA TO VERIFY: authors; venue; DOI/arXiv id.]
3. **Bröde, P., et al. (2012).** Deriving the operational procedure for the Universal
   Thermal Climate Index (UTCI). *International Journal of Biometeorology.* [REFERENCE
   METADATA TO VERIFY: full author list; volume; pages; DOI.]
4. **Colaninno, N., et al. (2025).** Sidewalk-level urban heat-risk assessment coupling
   UTCI hazard with pedestrian mobility. *Environment and Planning B.* [REFERENCE
   METADATA TO VERIFY: full author list; volume; pages; DOI.]
5. **Cool Routes (2026).** Cool routes: real-time human thermal-exposure routing.
   *Building and Environment.* [REFERENCE METADATA TO VERIFY: authors; volume; article
   no.; DOI.]
6. **CoolWalks (2025).** CoolWalks: assessing the potential of shaded routing for active
   mobility. *Scientific Reports.* [REFERENCE METADATA TO VERIFY: authors; volume; article
   no.; DOI.]
7. **Extreme heat and urban mobility (2025).** Extreme heat reduces and reshapes urban
   mobility. [REFERENCE METADATA TO VERIFY: authors; journal; volume; pages; DOI.]
8. **Gál, C. V., & Kántor, N. (2019).** Modeling mean radiant temperature in outdoor
   spaces: a comparative numerical validation. *Urban Climate.* [REFERENCE METADATA TO
   VERIFY: volume; pages; DOI.]
9. **GIS-AHP tourism suitability (2011).** Site suitability evaluation for ecotourism
   using GIS and AHP. *Procedia.* [REFERENCE METADATA TO VERIFY: authors; volume; pages;
   DOI.]
10. **HCI/TCI inter-comparison (2016).** Inter-comparison of the Holiday Climate Index
    and the Tourism Climate Index in Europe. *Atmosphere.* [REFERENCE METADATA TO VERIFY:
    authors; volume; article no.; DOI.]
11. **Heat risk action planning for tourism (2026).** A framework for heat-risk action
    planning for tourism. *Annals of Tourism Research.* [REFERENCE METADATA TO VERIFY:
    authors; volume; article no.; DOI.]
12. **Hungarian HCI/TCI (2025).** Projected climate suitability for Hungarian tourism
    (HCI/TCI). *International Journal of Biometeorology.* [REFERENCE METADATA TO VERIFY:
    authors; volume; pages; DOI.]
13. **Lindberg, F., et al. (2008).** SOLWEIG 1.0 — modelling spatial variations of 3D
    radiant fluxes and mean radiant temperature in complex urban settings.
    *International Journal of Biometeorology.* [REFERENCE METADATA TO VERIFY: full author
    list; volume; pages; DOI.]
14. **Monte-Carlo UTCI/PET reliability (2025).** Comparative reliability of PET and UTCI
    under input uncertainty via Monte-Carlo propagation. *Scientific Reports.* [REFERENCE
    METADATA TO VERIFY: authors; volume; article no.; DOI.]
15. **OECD (2026).** *OECD Tourism Trends and Policies 2026: adapting tourism to extreme
    weather.* Organisation for Economic Co-operation and Development. [REFERENCE METADATA
    TO VERIFY: chapter/section; DOI/URL.]
16. **Participatory-GIS under uncertainty (2025).** Decision-making under uncertainty in
    participatory GIS. *International Journal of Geographical Information Science.*
    [REFERENCE METADATA TO VERIFY: authors; volume; pages; DOI.]
17. **Plaza thermal comfort in Madrid and Sevilla (2022).** Effect of outdoor thermal
    comfort on tourist visits in historical plazas of Sevilla and Madrid. *Environmental
    Science and Pollution Research.* [REFERENCE METADATA TO VERIFY: authors; volume;
    pages; DOI.]
18. **Reliability of tourism climate indices (2016).** Reliability and usability of
    tourism climate indices. *Earth Perspectives.* [REFERENCE METADATA TO VERIFY: authors;
    volume; article no.; DOI.]
19. **Tourism exposure to weather extremes (2024).** Mapping the exposure of tourism to
    weather extremes: a gridded dataset. *Environmental Research Letters.* [REFERENCE
    METADATA TO VERIFY: authors; volume; article no.; DOI.]
20. **Tourism in a warming climate (2026).** Tourism in a warming climate: adaptive
    responses in Southern Europe. *Sustainability.* [REFERENCE METADATA TO VERIFY: authors;
    volume; article no.; DOI.]
21. **Tourist demand under climate change (2025).** Tourist demand and destination
    development under climate change. *Journal of Sustainable Tourism.* [REFERENCE METADATA
    TO VERIFY: authors; volume; pages; DOI.]
22. **UTCI-adjusted pedestrian accessibility (2026).** UTCI-adjusted pedestrian
    accessibility in tropical climates. *Sustainable Cities and Society.* [REFERENCE
    METADATA TO VERIFY: authors; volume; article no.; DOI.]
23. **WRF-UCM-SOLWEIG mapping (2024).** City-scale thermal-comfort mapping coupling
    WRF-UCM with SOLWEIG. *Sustainable Cities and Society.* [REFERENCE METADATA TO VERIFY:
    authors; volume; article no.; DOI.]

---

# Figure captions

**Figure 1. Study design and constraint-first screening architecture.** (a) The
Prado–Retiro–Atocha Madrid pilot study area (approximately 3.5 km² in central Madrid),
with the 27 curated tourism assets marked as outdoor (n = 14) or indoor (n = 13); the
extent is a bounded pilot and does not represent city-wide Madrid. (b) The analytical
architecture: 27 tourism assets are screened with two alternative thermal
representations — a simple operational proxy (ambient air-temperature hazard band +
nearby tree presence) and a physically based model (SOLWEIG → Tmrt → UTCI) — through one
ordered, constraint-first gate chain (open? → reachable? → thermally feasible? → evidence
sufficient? → meaningful improvement?), returning either surviving alternatives or an
explicit no-defensible-alternative outcome. Thermal state, decision confidence, evidence
confidence, and exclusion reason are kept as separate fields; no composite score is used.

**Figure 2. Thermal-method choice changes feasibility classifications, in both
directions.** Unit of analysis: the outdoor asset × timestamp observation (14 outdoor
assets × 3 timestamps = 42 observations). (a) Agreement matrix; each cell is one of three
states — agreement (both methods assign the same feasibility state), physical
configuration more restrictive than the proxy, or physical configuration less restrictive
than the proxy. "More restrictive" and "less restrictive" describe the *direction of
classification divergence between the two methods, not the correctness of either*; neither
method is field-validated. (b) Direction of divergence by timestamp as a share of the 14
outdoor assets, with the reclassification rate per timestamp (12:00 = 64.3%, 15:00 = 0.0%,
18:00 = 35.7%). Overall, 14/42 observations (33.3%) were reclassified — 9 physical more
restrictive, 5 physical less restrictive, 28 in agreement.

**Figure 3. Heat-aware screening changes the option set relative to a conventional
nearest-open baseline.** Eight pre-registered decision scenarios (S1–S8), each a real
source asset at one timestamp and walking reach. For each scenario: the nearest-open
baseline pick and whether it passes the constraint-first screen (● passes; ○ removed, with
the machine-readable exclusion reason); the number of surviving alternatives (0–9); and the
count of open, in-radius options removed on thermal or evidence grounds. Across the eight
scenarios the candidate set changed in 7 of 8, the nearest-open pick was removed by
screening in 3 of 8 (each `OUTDOOR_EXPOSURE_TOO_HIGH`), and 23 open, in-radius options were
removed in total. S8 (outlined; Parque del Retiro, 15:00, 500 m reach) evaluated 26
candidates, of which 0 survived, resolving to `NO_DEFENSIBLE_ALTERNATIVE`; this is an
architectural outcome of the locked constraints, not a ranked recommendation.

**Figure 4. Decision robustness under tested uncertainty.** (a) Number of the 42 outdoor
decisions that changed under each tested solar-forcing realization relative to the
clear-sky baseline: a satellite-derived irradiance realization changed 1/42 (2.4%), and
−10% and −20% irradiance perturbations changed 0/42 each. (b) Distribution of the
categorical decision-confidence class over the 42 outdoor observations — ROBUST 35 (83.3%),
BOUNDARY 6 (14.3%), UNSTABLE 1 (2.4%) — with the single UNSTABLE case (A24, 18:00) at the
46 °C feasibility boundary annotated. Robustness here refers only to the tested uncertainty
dimensions (solar forcing across all outdoor rows plus targeted canopy geometry for two
assets); it is not total uncertainty and is not a validation of the modelled field.

---

# Table captions

**Table 1. Data sources and provenance.** Open-data layers used in the analytical chain,
their provider, spatial/temporal support, licence, and what each layer does and does not
measure. See `manuscript/tables/TABLE01_data_sources.md`.

**Table 2. Constraint-first screening architecture.** The ordered gate chain, the
threshold for each gate, the machine-readable exclusion vocabulary, and the separate
decision fields (thermal state, decision confidence, evidence confidence, exclusion
reason). See `manuscript/tables/TABLE02_screening_rules.md`.

**Table 3. Scenario comparison: constraint-first screening versus nearest-open baseline
(S1–S8).** For each scenario, the source asset, timestamp and reach, the nearest-open
baseline pick and whether it survives screening, the number of surviving alternatives, the
count removed on thermal/evidence grounds, and the outcome state. See
`manuscript/tables/TABLE03_scenarios.md`.

*Supplementary Figure S1 and Supplementary Tables S1–S4 are described in
`supplementary/SUPPLEMENTARY_MATERIAL_v0.1.md`.*
