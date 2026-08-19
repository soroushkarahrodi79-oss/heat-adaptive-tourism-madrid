# 1. Introduction

In the tourism cities of Southern Europe, extreme-heat episodes increasingly overlap
with the summer season and with the daytime, outdoor conditions under which much
urban tourism takes place. Open plazas, monument forecourts, gardens, and the walking
segments between attractions become heat-exposed during these hours, and aggregate
studies show that urban activity contracts and shifts as temperatures rise (extreme
heat reshapes urban mobility, 2025). For destination management this is an
operational problem rather than only a long-run climatic one: on a given afternoon,
some outdoor opportunities become uncomfortable or unsuitable while others, and most
indoor options, remain usable, and visitors and the organisations that guide them
must decide among these options in near-real time. Yet heat governance has developed
largely around residents and public-health warning systems, and frameworks for
embedding tourism in heat action planning are only now being articulated (heat risk
action planning for tourism, Annals of Tourism Research 2026; OECD Tourism Trends and
Policies 2026). Southern-European destinations are already adapting in practice
(tourism in a warming climate, Sustainability 2026), and destination demand and
development are increasingly shaped by these conditions (tourist demand and
destination development under climate change, Journal of Sustainable Tourism 2025).
Critically, the exposure of tourism to heat is spatially uneven at the intra-urban
scale (mapping tourism exposure to weather extremes, ERL 2024), which is exactly the
scale at which visitors experience comfort in a historic core (outdoor thermal
comfort and tourist visits in Madrid and Sevilla plazas, Env Sci Pollut Res 2022).
The practical decision is opportunity-level and time-specific: which of the
attractions in front of a visitor this afternoon should remain on the table.

The dominant way to characterise tourism and climate has been the composite climate
index. Instruments such as the Tourism Climate Index and the Holiday Climate Index
combine several weather variables into an aggregate suitability score, and they are
well suited to comparing destinations or seasons at a broad scale (HCI/TCI
inter-comparison, Atmosphere 2016; recent HCI/TCI applications, IJB 2025). These
indices remain useful for their intended purpose, but two features limit their reach
for opportunity-level screening. First, their outputs are known to depend on the
choice of component weights and thresholds, so the same conditions can yield
different suitability readings under different, defensible parameterisations
(reliability and usability of tourism climate indices, Earth Perspectives 2016) — a
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
city-scale comfort mapping and design (WRF-UCM-SOLWEIG mapping, Sustainable Cities
and Society 2024), with a growing literature cautioning that surface- or
air-temperature summaries are not interchangeable with human-centred heat stress
(beyond land surface temperature, 2026). To date, however, these radiation-resolving
models have mostly served design, planning, and mapping; they are rarely wired
transparently into an auditable, opportunity-level tourism decision, so their
information reaches the screening stage only indirectly, if at all. It is important to be exact about what this
buys. These approaches provide a different representation of the thermal environment,
resolving additional physical dimensions relevant to pedestrian exposure; they are
not, on their own and without in-situ measurement, a validated ground truth against
which a simpler method can be called wrong (Tmrt validation ranges, Gál & Kántor
2019). The question this raises for tourism decision-support is therefore not which
thermal method is correct, but whether the choice of thermal representation
materially changes a tourism-screening decision — a question that can be answered by
comparison even where neither representation has been field-validated.

A fast-moving strand of heat-mobility research has begun to connect thermal exposure
to movement, and it defines the boundary of the present study most sharply. Thermal
routing takes an origin and a destination as given and finds the path of least
thermal exposure between them (Cool Routes, Building and Environment 2026; CoolWalks,
Scientific Reports 2025). Thermal-adjusted accessibility takes a destination set as
given and measures how many destinations remain reachable under heat-adjusted travel
(UTCI-adjusted pedestrian accessibility, Sustainable Cities and Society 2026), and
related work maps sidewalk-level heat risk along pedestrian networks (Colaninno et
al., 2025) or examines whether cool refuges are equitably reachable (Barcelona
climate-shelter accessibility, Cities 2025). These methods are advancing quickly and
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
(decision-making under uncertainty in participatory GIS, IJGIS 2025; Monte-Carlo
reliability of UTCI and PET, Scientific Reports 2025). Because the architecture places the thermal input in an
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
