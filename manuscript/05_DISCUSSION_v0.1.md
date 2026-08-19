# 5. Discussion

The pilot establishes a single, bounded claim: on this case, different thermal
representations can materially change which tourism opportunities a screening
system treats as feasible, and a constraint-first architecture can make those
changes, the constraints behind them, and their confidence explicit. It does not
establish that the physically based configuration is correct and the proxy wrong;
neither representation was field-validated here, and the interpretation below is
kept to method sensitivity rather than accuracy throughout.

## 5.1 Thermal representation is decision-relevant

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
not air temperature, dominate mean radiant temperature (e.g. Gál & Kántor, 2019;
WRF-UCM-SOLWEIG mapping, 2024), and with work arguing that surface- or
air-temperature summaries are not interchangeable with human-centred heat-stress
indices (the "beyond land surface temperature" argument, 2026).

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
(HCI/TCI inter-comparison, 2016; reliability of tourism climate indices, 2016) — had
not examined at the level of a screening decision. The sensitivity to representation
is not confined to the proxy-versus-physical contrast: within this study, even
simple open-data vegetation proxies did not converge closely with one another,
which is consistent with treating the representation of thermal exposure as a
substantive decision input rather than a settled preprocessing detail. The practical reading is that
thermal representation should be treated as a substantive modelling choice in
spatial tourism decision-support, not merely a technical preprocessing step; the
pilot supports this on one case rather than as a universal conclusion.

## 5.2 Screening before routing: a distinct decision-support layer

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
management levers (heat risk action planning for tourism, 2026). The screening layer
adds an operational step to that governance picture; it does not, on this evidence,
show that using it changes any realised management or visitor outcome.

## 5.3 Explicit non-recommendation and traceability

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

## 5.4 Robustness, uncertainty, and appropriate confidence

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
that propagates input uncertainty into a combined reliability estimate (Monte-Carlo
UTCI/PET reliability, 2025; decision-making under uncertainty in participatory GIS,
2025), the approach here differs by keeping uncertainty categorical and attached to
the individual decision rather than folded into one composite figure — a
transparency choice, not a claim of more complete quantification.

## 5.5 Contribution and transferability

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
