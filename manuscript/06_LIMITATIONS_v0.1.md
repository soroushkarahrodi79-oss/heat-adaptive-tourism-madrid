# 6. Limitations and scope conditions

The findings should be read against a set of boundaries that fix what the study can
and cannot support. These are stated in order of consequence and are not argued away;
several are permanent properties of the design rather than gaps a minor extension
would close.

## 6.1 Physical-model validation boundary

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

## 6.2 Spatial and temporal scope

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

## 6.3 Input and uncertainty limitations

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

## 6.4 Tourism and accessibility limitations

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

## 6.5 Operational-data and retrospective-alignment limitations

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

## 6.6 Scope conditions and transferability

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

## 6.7 Future work

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
