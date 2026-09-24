# Proposal — Heat-aware tourism opportunity assessment (10-day pilot)

*A template for a bounded, paid analytical engagement. It has **not** been sent to or
discussed with any company. Fees are not stated here, and no return on investment,
client feedback or willingness to pay is assumed.*

| | |
|---|---|
| **Potential client** | A tourism company running guided walking experiences in central Madrid |
| **Duration** | 10 working days, **conditional on the client supplying suitable data by day 2** |
| **Nature** | An analytical service with written deliverables. It is not a software platform, a real-time system or a routing engine. |
| **Method base** | The HATI-Madrid screening method (public preprint, not peer reviewed), whose analysis chain has been independently re-executed ([`REPRODUCTION_REPORT.md`](REPRODUCTION_REPORT.md)) |

## 1. Business problem

On extreme-heat days, some outdoor stops on the client's tours may be very hot at the
hour a group arrives. Today, substitutions are probably decided informally on the day,
and "nearest open place" is a common default. In the historical pilot, that default
picked a candidate the screening would exclude in 3 of 8 scenarios. That shows the two
procedures can diverge. It says nothing about the client's current practice.

## 2. Decision question (one)

> For each of the client's **outdoor stops**, at each **hour for which thermal evidence
> exists**, which pre-defined substitute stops are admissible under the client's own
> constraints, and for which stops is the defensible answer **"no substitution
> recommended"**?

The output is a **pre-season contingency diagnosis**. It is not an on-the-day
instruction and not a route.

## 3. Scope

| Dimension | Covered by the 10-day pilot | Not covered (would need a separate, scoped engagement) |
|---|---|---|
| **Space** | Client stops and substitutes that coincide with, or can be defensibly matched to, the 27 existing pilot assets in the ≈3.5 km² Prado–Retiro–Atocha area | Stops outside the area or not matchable to an existing asset |
| **Time** | The three **discrete** modelled hours, 12:00, 15:00 and 18:00, of the reference extreme-heat day (21 Aug 2023) | Other hours (no interpolation), other dates, current or forecast conditions |
| **Thermal evidence** | Existing SOLWEIG-derived UTCI for the 14 outdoor assets; existing operational proxy | New SOLWEIG runs, new geometry, new forcing |
| **Rules** | The published gates and thresholds, applied unchanged. Client parameters (walking limit, candidate venues, hours) are documented inputs, tested for sensitivity | New thresholds, weights or scoring |

Any client stop that falls outside the covered scope is reported as `OUT_OF_SCOPE` or
`INSUFFICIENT_EVIDENCE`. It is **never** given an estimated answer.

## 4. Required client inputs (by day 2)

1. Tour itineraries: stop names, locations, and the hours at which groups are at each
   stop.
2. Group constraints: maximum extra walking distance, accessibility needs, group size.
3. The substitute venues the client could realistically use, with **current** opening
   hours, admission or booking conditions, and whether a group can enter without prior
   booking.
4. The client's existing heat protocol, if any, and the constraints on changing the
   product (licensing, contracts, what the customer was sold).
5. A named contact who can confirm inputs and attend the final review.

## 5. What exists vs what must still be done

| Existing (verified) | Pending within this pilot | Pending beyond this pilot |
|---|---|---|
| Screening code, re-executed to identical tables | Mapping client stops and venues to pilot assets | Thermal modelling for new stops, dates or hours |
| Modelled UTCI and stability labels for 14 outdoor assets at 3 hours | Client-specific scenario configuration and sensitivity runs | Field measurement of Tmrt/UTCI |
| Documented method and limitations | Verification of client venue data | Operational trial with guides and visitors |

## 6. Work plan

**Week 1: data and feasibility**

| Day | Activity | Output |
|---|---|---|
| 1 | Kick-off; confirm the decision question and constraints | Signed-off scope note |
| 2 | Receive and audit client inputs | Data audit; **go / reduce-scope / abstain decision** (§9) |
| 3 | Match client stops and venues to pilot assets; flag unmatched ones | Coverage table |
| 4 | Configure client scenarios with the unchanged rules | Scenario register |
| 5 | Run the screening; internal consistency checks | Draft results; checkpoint call with the client |

**Week 2: analysis and delivery**

| Day | Activity | Output |
|---|---|---|
| 6 | Sensitivity: walking limit, heat method (proxy vs physical), stability label | Sensitivity tables |
| 7 | Evidence and uncertainty matrix for every result | Matrix |
| 8 | Comparative map and tables: stops, substitutes, exclusion reasons | Map and tables |
| 9 | Executive decision brief; reproducibility pack | Brief and pack |
| 10 | Client review session; record agreed corrections | Final versions; session notes |

## 7. Deliverables

1. **Executive decision brief** (2–4 pages, Spanish). Per stop and hour: admissible
   substitutes, or "no substitution recommended", or "insufficient evidence", each with
   its reason.
2. **Evidence and uncertainty matrix.** Every statement is classified as IMPLEMENTED,
   REPRODUCED, MODEL-DERIVED, HYPOTHETICAL or PENDING.
3. **Comparative geographic analysis.** A map and tables of stops, candidates and
   first-failing exclusion reasons, compared with the nearest-open default.
4. **Reproducibility documentation.** Inputs, commands and versions, so that every number
   can be regenerated.
5. **Final client review session** (about 90 minutes), with written notes.

## 8. Acceptance criteria

- Every in-scope stop × hour has exactly one status, with a traceable reason.
- Every number in the brief is regenerated by the reproducibility pack.
- Every limitation in §10 appears in the brief in plain language.
- No deliverable claims a validated prediction, an optimal route, or a reduction in risk,
  cost, cancellations or health effects.
- The client confirmed the inputs used (day 2), and the review session took place
  (day 10).

## 9. Conditions for abstention or scope reduction

| Condition | Consequence |
|---|---|
| Client inputs not received or unusable by day 2 | Pause, or reduce to a method demonstration on the historical scenarios |
| Fewer than a useful share of client stops fall inside the existing thermal coverage (agreed on day 1) | Reduce scope to the covered stops, or recommend a separate modelling engagement instead |
| No substitute survives for a stop | Report "no substitution recommended". This is a valid result. |
| Evidence is LOW or the decision is UNSTABLE | Report `INSUFFICIENT_EVIDENCE`; no recommendation |
| The client needs current or forecast conditions | Out of scope; say so and do not approximate |
| Licensing of an input cannot be cleared for commercial use (§11) | Exclude that input, or pause |

## 10. Scientific and operational limitations (stated in every deliverable)

- The thermal values are **model outputs for one historical day** (21 Aug 2023). They
  are not measurements and do not describe current conditions.
- Only three discrete hours are covered, with no interpolation.
- UTCI describes modelled physiological stress. It is not tourist comfort or health risk.
- Stability labels cover the tested perturbations only. They are not accuracy.
- Distances are straight-line. Indoor venues are assumed cooler, without verification of
  air conditioning or queues.
- The related pedestrian-route research **abstained**, so no route recommendation is made.
- Final operational decisions, including the use of current AEMET warnings, remain with
  the client and its guides.

## 11. Licensing and provenance: what matters for a paid engagement

*This is a working review, not legal advice. Items marked "verify" need confirmation of
the provider's current terms before a contract is signed.*

| Material | Terms as recorded in the repository | Implication for a paid pilot |
|---|---|---|
| **OpenStreetMap** | ODbL (`data/raw/osm/README.md`) | Analysis and maps are allowed with the attribution "© OpenStreetMap contributors". If a **derived database**, such as a cleaned asset table, is handed over or published, share-alike obligations may apply. Deliver maps and results; treat data tables as a licensing decision. |
| **IGN/CNIG PNOA LiDAR** | CC BY 4.0 / IGN terms | Commercial use is allowed with attribution. |
| **Ayuntamiento de Madrid open data** (tree inventory, meteorology) | CC BY 4.0 / free reuse with attribution | Commercial use is allowed with attribution. |
| **Copernicus HRL / EEA** | open, attribution required | Commercial use is allowed with attribution. |
| **Meteostat** (source of the Barajas hourly series used for forcing and hazard bands) | The repository records "free for **non-commercial** and attributed use" (`docs/PHASE1_DATA_PROVENANCE.md`) | **Real impediment.** Do not use this series inside a paid deliverable unless its terms are verified or permission is obtained. The alternative is to source the same station data directly from **AEMET OpenData**, whose terms allow reuse with attribution (verify current terms). |
| **Open-Meteo** (radiation used in one solar-forcing realisation) | Not recorded in the repository | **Verify.** The free API tier is intended for non-commercial use. Re-source this input or clear it before commercial use. |
| **SOLWEIG** (`solweig` 0.1.0b92) | GPL-3.0 (package metadata) | Running it and delivering its **outputs** is unaffected. If HATI code that imports SOLWEIG is **distributed** to a client, GPL obligations may apply. Deliver results and documentation, not bundled software, unless this has been reviewed. |
| **HATI repository code and text** | No licence assigned; "all rights reserved" per README | The absence of a licence does not prove exclusive ownership of every line, because the code was substantially AI-assisted. Before handing any code to a client, choose a licence and review the provenance. Delivering analysis results is not blocked by this. |
| **Published preprint and figures** | Zenodo record licence not verified in the repository | Verify before reusing figures in client material. |

**Net assessment:** nothing blocks an analysis-and-report engagement. Two inputs must be
cleared or replaced before they are used commercially: the **Meteostat-relayed
meteorology** and the **Open-Meteo radiation**. Code must not be delivered until a
licence has been chosen.

## 12. Responsibilities

| Client | Analyst |
|---|---|
| Supplies accurate itineraries, constraints and venue information, and confirms them | Applies the documented method unchanged and records every assumption |
| Decides which recommendations to adopt, and how | States every limitation; abstains when the evidence is insufficient |
| Keeps responsibility for visitor safety and operations | Makes no claim of validation, optimisation or impact |
| Nominates a contact for the checkpoint and the review | Delivers reproducible, attributed material with inputs cleared for licensing |

## 13. Possible follow-up (only if the pilot proves useful to the client)

- A separately scoped thermal-modelling engagement for uncovered stops, dates or hours.
- Field measurement of Tmrt/UTCI at a few stops to test the model.
- A small operational trial to learn whether guides can apply the contingency sheet.

None of these is promised or priced here.
