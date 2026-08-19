# 4. Results

Results are reported for the locked pilot: 27 tourism assets on 21 August 2023 at
12:00, 15:00, and 18:00, with thermal-method comparison on the 42 outdoor asset ×
timestamp observations (14 outdoor assets × 3 hours) and screening evaluated across
eight pre-registered decision scenarios. All figures are descriptive; the unit is
the asset × timestamp observation or the scenario comparison, not a population
sample, and no inferential test is applied.

## 4.1 Thermal-method sensitivity

Across the 42 outdoor observations, the simple-proxy baseline and the
physically based (SOLWEIG/UTCI) configuration assigned the same feasibility state
in 28 observations and differed in 14, a reclassification rate of 33.3% (14/42)
(Table 3). Both directions of change occurred: the physically based configuration
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
rate in every group (Table 3). The time-of-day pattern above was therefore not
reproduced across morphology classes.

The noon pattern reflects the difference between the two inputs. At 12:00 the
observed ambient air temperature was 34.2 °C, which falls in the LOW meteorological
hazard state under the locked AEMET operational warning thresholds. Despite that
LOW hazard state, the modelled UTCI equalled or exceeded the 32 °C boundary used in
the physical-model feasibility configuration at all 14 of the 14 outdoor assets
(Fig. 3). The proxy, keyed to the ambient hazard band, and the physically based
configuration, keyed to modelled UTCI, therefore assigned different feasibility
states at most noon observations, whereas at 15:00 both configurations placed every
outdoor observation in the same conditional-feasibility state.

The finding of this subsection is limited to the following: feasibility
classification outcomes were sensitive to the choice of thermal method, and the
sensitivity was largest at 12:00.

## 4.2 Effects on tourism-opportunity screening

Each scenario began from a real asset in a constrained state on the study day. Seven
of the eight sources were open outdoor sites in the very-strong-heat-stress category
(modelled source UTCI ranging from 38.6 to 45.4 °C) and one (S5, Real Observatorio
de Madrid) was closed at its timestamp. Screening behaviour was evaluated across the
eight scenarios by comparing the constraint-first surviving-alternative set against
a conventional nearest-open baseline that applies no thermal or evidence screening
(Table 4). The surviving
candidate set differed from the nearest-open set in 7 of the 8 scenarios; it was
unchanged in one (S7), where the nearest-open pick already satisfied the locked
constraints and no additional candidate was screened out.

The nearest-open pick itself did not satisfy the locked screening constraints in 3
of the 8 scenarios (S2, S6, S8). In each of these three the nearest open asset was
an outdoor site that was not cooler than the source, and each was screened out with
the same machine-readable reason, `OUTDOOR_EXPOSURE_TOO_HIGH` (Table 4). Across all
eight scenarios, 23 open, in-radius candidate options were screened out on thermal
or evidence grounds — that is, they were open and within the walking radius but did
not satisfy the thermal or evidence constraints (Fig. 6). Surviving alternatives
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
therefore resolved to the explicit state `NO_DEFENSIBLE_ALTERNATIVE` (Fig. 6). This
outcome was produced by the locked screening rules operating on the locked inputs;
it was not a manually imposed result or a processing error, and no surviving
alternative was withheld.

The finding of this subsection is limited to the following: thermal and evidence
screening altered the candidate set relative to a nearest-open baseline in seven
scenarios, removed the nearest-open pick in three, and returned an explicit
no-alternative state in one.

## 4.3 Robustness and traceability

The reclassification and screening results were examined against the tested
solar-forcing perturbations (Fig. 4). Replacing the clear-sky irradiance estimate
with the satellite-derived irradiance realization changed 1 of the 42 outdoor
decisions (2.4%). That single change was La Rosaleda (A24) at 18:00, where the
satellite realization raised the envelope to the 46 °C feasibility boundary; it is
the same observation classified UNSTABLE below. The −10% irradiance perturbation
changed 0 of 42 decisions, and the −20% irradiance perturbation also changed 0 of
42. The noon result of Section
4.1 persisted under every tested solar-forcing scenario: all 14 outdoor assets
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
