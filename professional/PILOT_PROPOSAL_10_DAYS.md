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

## 0. What this pilot is, and is not

The pilot has **two clearly separated products**. They must not be merged into a single
"apply the model to my tours" promise.

| | **A. Historical analytical demonstration** | **B. Applied business diagnostic** |
|---|---|---|
| **What it uses** | The existing, already-modelled evidence for **21 Aug 2023**, 12:00/15:00/18:00, at the 27 existing pilot assets | The client's real stops, restrictions, schedules and available data |
| **What it produces** | An explained, reproduced illustration of how the HATI method works and what it showed on that one historical day, optionally mapped to the client's stops **where they coincide with or can be defensibly matched to the existing assets** | A diagnosis of the client's needs, candidate substitutes, data gaps and the feasibility conditions for an operational tool |
| **What it does NOT produce** | An operational recommendation for any date other than 21 Aug 2023 | Any substitution recommendation for the client's **current or future** tours |
| **Why** | The thermal evidence is fixed to one historical day; it cannot describe conditions on any other day | Answering "what should the client do on the next extreme-heat day" requires **new** thermal modelling for the client's actual stops and dates, which this pilot does not produce (§3) |

**Without new, adequate thermal data for the client's own stops and dates, this pilot
cannot and does not recommend operational substitutions for future hot days.** Historical
data from 21 Aug 2023 at 27 unrelated (or only spatially coincident) assets is evidence
about how the *method* behaves, not evidence about what the client should do next summer.
Any statement that appears to combine the two is an error in this document, not an
intended claim.

## 1. Business problem

On extreme-heat days, some outdoor stops on the client's tours may be very hot at the
hour a group arrives. Today, substitutions are probably decided informally on the day,
and "nearest open place" is a common default. In the historical pilot (Product A), that
default picked a candidate the screening would exclude in 3 of 8 scenarios. That shows
the two procedures can diverge **under the study's 2023 evidence and rules**. It says
nothing about the client's current practice, and it is not, by itself, a reason to change
that practice without new evidence for the client's actual stops.

## 2. Decision questions (two, kept separate)

**A. Demonstration question**

> Using the existing 21 Aug 2023 evidence, how does the HATI screening method behave —
> which candidates are admissible, which are excluded and why, and where does it abstain
> with "no substitution recommended"? What does this show about the value and the limits
> of the method?

**B. Diagnostic question**

> What are the client's outdoor stops, their restrictions, their candidate substitutes
> and their available data — and **what would be needed**, in scope, data and cost, to
> produce a genuine, current, operational contingency screening for those specific stops?

The output of B is a **feasibility and gap diagnosis**, not a set of substitution
recommendations. It is not an on-the-day instruction and not a route. Producing actual
operational recommendations for the client's stops is explicitly **out of scope** for
this 10-day pilot (§3) because it requires new thermal modelling this engagement does not
include.

## 3. Scope

| Dimension | Covered by the 10-day pilot | Not covered (would need a separate, scoped engagement) |
|---|---|---|
| **Space (Product A)** | Illustrative mapping of client stops/substitutes that coincide with, or can be defensibly matched to, the 27 existing pilot assets in the ≈3.5 km² Prado–Retiro–Atocha area | Stops outside the area or not matchable to an existing asset |
| **Time (Product A)** | The three **discrete** modelled hours, 12:00, 15:00 and 18:00, of the reference extreme-heat day (21 Aug 2023) only. Not a time series and not representative of other days | Other hours (no interpolation), other dates, current or forecast conditions |
| **Thermal evidence (Product A)** | Existing SOLWEIG-derived UTCI for the 14 outdoor assets; existing operational proxy, both dated to 21 Aug 2023 | New SOLWEIG runs, new geometry, new forcing, any thermal evidence for the client's actual stops or dates |
| **Diagnostic scope (Product B)** | Cataloguing the client's stops, restrictions, candidate substitutes and available data; identifying data gaps; scoping and costing what new thermal modelling would be required | Producing substitution recommendations for the client's current or future tours; any claim that 2023 evidence determines what the client should do next |
| **Rules** | The published gates and thresholds, described and illustrated unchanged on the 2023 evidence. Client parameters (distance limit, candidate venues, hours) are recorded as diagnostic inputs for a future engagement, not applied to produce a current recommendation | New thresholds, weights or scoring |

Any client stop is reported as `HISTORICAL_DEMONSTRATION_ONLY` (covered by Product A,
illustrative), `DIAGNOSTIC_ONLY_NO_THERMAL_EVIDENCE` (covered by Product B, needs new
modelling before any recommendation), or `OUT_OF_SCOPE`. No stop is given an estimated
operational substitution answer from the 2023 evidence.

## 4. Required client inputs (by day 2)

These inputs feed the **diagnostic (Product B)**: cataloguing the client's real
situation, not producing a current substitution answer from 2023 evidence.

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

| Existing (verified) — feeds Product A | Pending within this pilot — Product B diagnostic | Pending beyond this pilot |
|---|---|---|
| Screening code, re-executed to identical tables | Cataloguing client stops, venues and restrictions; matching against pilot assets where spatially defensible, for illustration only | Thermal modelling for the client's actual stops, dates or hours |
| Modelled UTCI and stability labels for 14 outdoor assets at 3 hours (21 Aug 2023 only) | Identifying data and coverage gaps; scoping and costing the modelling a genuine engagement would need | Field measurement of Tmrt/UTCI |
| Documented method and limitations | Feasibility assessment: go / reduce-scope / abstain for a future operational engagement | Operational trial with guides and visitors |

## 6. Work plan

**Week 1: data and feasibility**

| Day | Activity | Output |
|---|---|---|
| 1 | Kick-off; confirm the two decision questions (§2) and constraints | Signed-off scope note |
| 2 | Receive and audit client inputs | Data audit; **go / reduce-scope / abstain decision** (§9) |
| 3 | Match client stops and venues to pilot assets where defensible; flag unmatched ones | Coverage table (illustrative, Product A) |
| 4 | Reproduce and illustrate the HATI method on the 2023 evidence; draft the diagnostic criteria for Product B | Illustrative scenario outputs (2023 only); diagnostic checklist |
| 5 | Internal consistency checks; catalogue client stops, restrictions and data gaps | Draft materials; checkpoint call with the client |

**Week 2: analysis and delivery**

| Day | Activity | Output |
|---|---|---|
| 6 | Sensitivity of the 2023 demonstration: distance limit, heat method (proxy vs physical), stability label | Sensitivity tables (Product A, illustrative) |
| 7 | Evidence and uncertainty matrix for every statement in both products | Matrix |
| 8 | Comparative map and tables for the historical demonstration; feasibility/gap tables for the diagnostic | Map and tables (A); gap and cost-scope tables (B) |
| 9 | Demonstration brief (A) and feasibility/diagnostic report (B); reproducibility pack | Two written deliverables and pack |
| 10 | Client review session; record agreed corrections | Final versions; session notes |

## 7. Deliverables

1. **Historical demonstration brief (Product A, 2–3 pages, Spanish).** How the HATI
   method behaves on the existing 21 Aug 2023 evidence, illustrated against the client's
   stops where they coincide with the 27 pilot assets: admissible substitutes, "no
   substitution recommended", or "insufficient evidence" under that one historical day's
   evidence, each with its reason. Explicitly labelled as a historical illustration, not
   a current-day recommendation.
2. **Feasibility and diagnostic report (Product B, 2–4 pages, Spanish).** The client's
   catalogued stops, restrictions, candidate substitutes and data gaps; what new thermal
   modelling and other work would be required to produce a genuine, current, operational
   contingency tool; a scoped recommendation on whether and how to proceed. **Contains no
   substitution recommendation for the client's current or future tours.**
3. **Evidence and uncertainty matrix.** Every statement, in both deliverables, is
   classified as IMPLEMENTED, REPRODUCED, MODEL-DERIVED, HYPOTHETICAL or PENDING.
4. **Comparative geographic analysis (Product A).** A map and tables of the 2023
   demonstration: stops, candidates and first-failing exclusion reasons, compared with
   the nearest-open default.
5. **Reproducibility documentation.** Inputs, commands and versions for Product A, so
   that every historical number can be regenerated.
6. **Final client review session** (about 90 minutes), with written notes.

## 8. Acceptance criteria

- Every in-scope stop × hour in Product A has exactly one status, with a traceable
  reason, and is labelled as a **historical illustration for 21 Aug 2023**, not a current
  recommendation.
- Every number in the demonstration brief is regenerated by the reproducibility pack.
- Every limitation in §10 appears in both deliverables in plain language.
- **No deliverable presents the 21 Aug 2023 evidence as a basis for a substitution
  decision on the client's current or future tours.** Product B contains a diagnosis and
  a scope proposal, never a substitution recommendation derived from 2023 data.
- No deliverable claims a validated prediction, an optimal route, or a reduction in risk,
  cost, cancellations or health effects.
- The client confirmed the inputs used (day 2), and the review session took place
  (day 10).

## 9. Conditions for abstention or scope reduction

| Condition | Consequence |
|---|---|
| Client inputs not received or unusable by day 2 | Pause, or reduce to the Product A method demonstration only |
| Fewer than a useful share of client stops fall inside the existing thermal coverage (agreed on day 1) | Reduce Product A's illustrative mapping to the covered stops; Product B's diagnosis still covers all client stops, since it does not depend on thermal coverage |
| No substitute survives for a stop in the 2023 demonstration | Report "no substitution recommended" for that illustration. This is a valid result, and it is **not** a statement that remaining at the stop is safe ([`CASE_STUDY_HEAT_OPPORTUNITY_SCREENING.md`](CASE_STUDY_HEAT_OPPORTUNITY_SCREENING.md), §7) |
| Evidence is LOW or the decision is UNSTABLE (Product A) | Report `INSUFFICIENT_EVIDENCE`; no recommendation |
| The client needs current or forecast conditions | Out of scope for both products; say so and do not approximate |
| Licensing of an input cannot be cleared for commercial use (§11) | Exclude that input from paid deliverables, or pause that part of the engagement until cleared |

## 10. Scientific and operational limitations (stated in every deliverable)

- The thermal values are **model outputs for one historical day** (21 Aug 2023). They
  are not measurements and do not describe current conditions, and they do not
  determine what substitutions are appropriate for the client's current or future tours.
- Only three discrete hours are covered (12:00, 15:00, 18:00), with no interpolation
  and no continuity between them; they are not a time series.
- UTCI describes modelled physiological stress. It is not tourist comfort or health risk.
- Stability labels cover the tested perturbations only. They are not accuracy.
- Distances are **straight-line**, not walking-network distances, in both the historical
  demonstration and the client's diagnostic inputs.
- The client's **current** opening hours and restrictions, gathered for Product B, are
  never applied retroactively to the 2023 thermal evidence as if they were observed
  together; the two are diagnostic inputs collected at different times, not a joint
  historical record.
- A `NO_DEFENSIBLE_ALTERNATIVE` result (2023 demonstration) means no admissible
  substitute was identified under the tested constraints. It does **not** mean that
  remaining at the original stop is safe, thermally recommendable or preferable; that is
  a separate operational judgement HATI does not make.
- Indoor venues are assumed cooler, without verification of air conditioning or queues.
- The related pedestrian-route research **abstained**, so no route recommendation is made.
- Final operational decisions, including the use of current AEMET warnings, remain with
  the client and its guides.

## 11. Licensing and provenance: what matters for a paid engagement

*This is a working review, not legal advice. Items marked "verify" need confirmation of
the provider's current terms before a contract is signed.*

These are **five different legal questions**, and clearing one does not clear the
others:

1. **Software licence** — the terms under which a tool (e.g., SOLWEIG) may be run.
2. **Data access/use terms** — the terms under which a data provider (e.g., Meteostat,
   Open-Meteo) lets its data be fetched and used at all.
3. **Database rights** — obligations attached to a *database* as a compiled work (e.g.,
   ODbL share-alike on OpenStreetMap), separate from the licence on any single fact in it.
4. **Commercial use of derived results** — whether a *paid report* that presents outputs
   computed from an input (e.g., UTCI rasters computed using Meteostat-sourced forcing)
   is itself restricted by that input's terms. This does not automatically follow from
   (1)–(3) and is the least settled question below.
5. **Distribution of code/datasets to a client** — separate again from analysing data or
   delivering a written report; handing over the code or the raw/processed dataset
   itself triggers different obligations (e.g., GPL-3.0 on SOLWEIG, ODbL share-alike on
   an OSM-derived table) than handing over a report about them.

| Material | Terms as recorded in the repository | Dimension(s) affected | Implication for a paid pilot |
|---|---|---|---|
| **OpenStreetMap** | ODbL (`data/raw/osm/README.md`) | Database rights (3), distribution (5) | Analysis and maps are allowed with the attribution "© OpenStreetMap contributors". If a **derived database**, such as a cleaned asset table, is handed over or published, share-alike obligations may apply. Deliver maps and reports; treat handing over data tables as a separate licensing decision. |
| **IGN/CNIG PNOA LiDAR** | CC BY 4.0 / IGN terms | Data use (2) | Commercial use is allowed with attribution. |
| **Ayuntamiento de Madrid open data** (tree inventory) | CC BY 4.0 / free reuse with attribution | Data use (2) | Commercial use is allowed with attribution. |
| **Copernicus HRL / EEA** | open, attribution required | Data use (2) | Commercial use is allowed with attribution. |
| **Meteostat** (source of the Barajas hourly series used as SOLWEIG forcing and for hazard bands) | The repository records "free for **non-commercial** and attributed use" (`docs/PHASE1_DATA_PROVENANCE.md`) | Data use (2), and — **unresolved** — commercial use of derived results (4) | **Real impediment, broader than it first appears.** The raw series must not be resold or redistributed commercially. Separately, and **not yet verified either way**: whether a *paid report* may present UTCI/Tmrt outputs that were computed using this series as model forcing is a derived-use question that Meteostat's terms do not clearly answer here. Until this is verified or permission is obtained, the existing 21 Aug 2023 UTCI/Tmrt outputs (Product A) should be treated as **not cleared for paid commercial delivery**, only for non-commercial/academic presentation, or the meteorology must be re-sourced from **AEMET OpenData** (attribution-based reuse, verify current terms) and the affected outputs regenerated — which is new modelling, out of scope for this 10-day pilot. |
| **Open-Meteo** (radiation used in one solar-forcing realisation) | Not recorded in the repository | Data use (2), commercial use of derived results (4) | **Verify both.** The free API tier is typically intended for non-commercial use, and whether derived thermal outputs may be sold is unverified. Re-source this input or clear it before any commercial use of outputs that depend on it. |
| **SOLWEIG** (`solweig` 0.1.0b92) | GPL-3.0 (package metadata) | Software licence (1), distribution (5) | GPL-3.0 governs the **software**, not the **outputs** it produces; running it and delivering its results as a report is not restricted by GPL merely because the tool is GPL-licensed. If HATI code that imports SOLWEIG is itself **distributed** to a client (code handed over, not just results), GPL's copyleft terms may then apply to that code. Deliver results and documentation, not bundled software, unless this has been reviewed. Do not treat GPL-3.0 as a blanket prohibition on paid services that merely use the tool internally. |
| **HATI repository code and text** | No licence assigned; "all rights reserved" per README | Software licence (1) / ownership, distribution (5) | The **absence of a repository licence does not, by itself, establish exclusive authorship or ownership of every line**, because the code was substantially AI-assisted and provenance of individual contributions is not fully recorded (see §3 of the case study). It also does not remove the owner's ability to offer services using the code internally. Before handing any code to a client, choose a licence and review provenance; delivering analysis *results* (not code) is not blocked by this open question. |
| **Published preprint and figures** | Zenodo record licence not verified in the repository | Data use (2), distribution (5) | Verify before reusing figures in client material. |

**Net assessment, corrected:** nothing here blocks the **diagnostic labour** of
Product B (cataloguing the client's stops, restrictions and data gaps, and scoping
future work) as a paid service, because that labour does not depend on the
Meteostat/Open-Meteo-derived outputs. **Product A's specific 2023 UTCI/Tmrt outputs are
not yet cleared for paid commercial delivery**, pending verification of point 4 above for
Meteostat and Open-Meteo; until cleared, present them as non-commercial/academic
background context within the engagement rather than as a billed deliverable, or
exclude them and describe the method in words and published-figure references only.
Code must not be delivered to a client until a licence has been chosen and reviewed.
Every "verify" item above is a real open question, not a formality, and stays open until
someone actually checks the provider's current terms.

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
