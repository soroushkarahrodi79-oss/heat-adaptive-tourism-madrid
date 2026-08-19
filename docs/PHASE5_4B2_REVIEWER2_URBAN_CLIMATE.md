# PHASE5_4B2_REVIEWER2_URBAN_CLIMATE.md — Reviewer 2 (Urban Climate / SOLWEIG / UTCI)

Adversarial review of the physical modelling in `manuscript/MANUSCRIPT_TMP_v0.2.md`.

## Overall verdict: MAJOR REVISION

The claim ceiling ("method sensitivity, not accuracy") is disciplined and mostly holds,
and the no-field-validation limitation is stated repeatedly and honestly. My rejection
case is not that the physical model is wrong — it is that **the physical configuration is a
decision-constant**, which the manuscript does not disclose and which changes how the
headline result must be read.

## Top 3 criticisms

**1. The physically based configuration assigns the SAME feasibility state
(FEASIBLE WITH CONDITIONS) to all 42 outdoor observations. [MAJOR — highest priority]**
- *Evidence:* by construction the 10 m-buffer-mean UTCI for every outdoor asset×timestamp
  lies in 32–46 °C, so all 42 map to FEASIBLE WITH CONDITIONS; the proxy alone spreads
  across FEASIBLE (9), FWC (28), NOT RECOMMENDED (5). Therefore the entire 33.3% "divergence"
  is the *proxy* moving toward a physical constant (9 FEASIBLE→FWC, 5 NOT RECOMMENDED→FWC).
  The manuscript never states this; §3.1 only hints ("at 15:00 both configurations placed
  every outdoor observation in the same conditional-feasibility state").
- *Why it matters:* the framing that the physical method "carries additional information
  relevant to the decision" (Intro §1; Discussion §4.1) is not supported *at the decision
  level* — at the buffer-mean the physical method makes one decision for everything. Its
  extra information lives in the spatial field (Fig. S1), which the decision collapses.
- *Required action (existing evidence):* disclose the single-valued physical result
  explicitly in §3.1 and interpret it honestly in §4.1 — the radiant index places every
  outdoor site in the strong/very-strong-stress band on this extreme day, so the proxy's
  apparent discrimination (FEASIBLE vs NOT RECOMMENDED) is not corroborated. This can be
  framed as a *strength* (an operational proxy over- and under-states relative to a uniform
  strong-stress reference) without claiming the physical method is richer for the decision.
- *Not required:* field validation or re-modelling.

**2. "Physically interpretable" (RQ1) and the noon mechanism overreach slightly. [MAJOR/MINOR]**
- *Evidence:* RQ1 asks whether the difference is "physically interpretable"; §4.1 infers the
  noon mechanism from method structure, not measurement. This is defensible but the word
  "interpretable" invites "interpreted by whom, validated how?"
- *Required action:* soften to "mechanistically consistent with" / "attributable to the
  radiant term," which the text already does in substance — align RQ1 wording.

**3. Forcing and geometry weaknesses are disclosed but load-bearing. [MAJOR, disclosed]**
- *Evidence:* Barajas is ~9 km away on an airport apron (§2.2); GHI is a clear-sky *estimate*
  (§2.2); canopy geometry is dated for parts of the domain (§5.3). Solar-forcing sensitivity
  (1/42, 0, 0) addresses irradiance only, not Ta/RH/wind spatial fields.
- *Required action:* keep the disclosures; add one sentence noting that the near-uniform
  forcing (single station values across the raster) is itself a reason the outdoor UTCI is
  near-uniform in band — connects to criticism 1. No new analysis.

## Answers to the numbered challenges
1. *Meaningful without ground truth?* Yes as a *sensitivity* demonstration — but see #1.
2. *"Physically based" rhetorical?* Borderline; acceptable if #1 is disclosed.
3–4. *Forcing / Barajas defensible?* Disclosed lower bound; acceptable with the caveat in #3.
5. *Solar sensitivity adequate?* For irradiance only; does not cover Ta/RH/wind — stated.
6. *Stale vegetation material?* Bounded (2 corrected assets; sensitivity carried) — acceptable.
7. *Default land cover important?* A real simplification; disclose it plainly (it is in the
   Methods but not flagged as a limitation).
8. *UTCI appropriate?* Yes for outdoor pedestrian heat load.
9. *Threshold mappings defensible?* 32/46 °C are Bröde-grounded and pre-registered — yes.
10. *Noon AEMET-vs-UTCI construct confusion?* Well-handled in prose (§4.1 "different
    constructs"); keep.
11. *"Physically interpretable" overreach?* Mild — see #2.
12. *Robustness read as validation?* Fig. 4 caption pre-empts it ("not a validation"); OK.
13. *Pseudoreplication?* No inference is claimed; the 42 are treated descriptively — OK, but
    ensure "material/robust" are not read as inferential (Critical Attack 6).
14. *Any implied physical superiority?* Not in explicit wording, but criticism #1 is an
    *implicit* superiority via the "additional information" framing — fix it.

## Requests I would REFUSE as scope creep
- In-situ Tmrt/UTCI measurement campaign; CFD/URock wind fields; a second modelled day.
- Re-running SOLWEIG with a bespoke land-cover grid.
