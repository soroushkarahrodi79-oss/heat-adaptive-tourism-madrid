# PHASE5_0_REVIEWER_ATTACK_MAP.md — HATI-Madrid Phase 5.0

Version 1.0 · 2026-08-18. Ten anticipated reviewer criticisms. For each:
criticism, whether it is valid or invalid, repository evidence that addresses it,
wording strategy, and whether it remains a standing limitation. Ends with the
publication ceiling (Task 10). No new analysis.

---

### R1 — "No field validation of Tmrt/UTCI."
- **Valid?** Valid, and permanent. No in-situ Tmrt/UTCI measurement exists.
- **Evidence:** `PHASE2_VALIDATION_REPORT.md` §4 states this as first-class;
  plausibility checks (§3) are offered as *not* a substitute.
- **Wording:** claim method *divergence* and physical *interpretability*, never
  accuracy or superiority; the paper's contribution does not require the model to
  be right, only to differ interpretably (see charter claim ceiling).
- **Remains a limitation?** YES — headline limitation; named as the top future
  investment.

### R2 — "Single day, single city — a case study, not a method."
- **Valid?** Partly. Scope is real; but the *contribution* is the architecture and
  the method-sensitivity demonstration, which a single well-characterized pilot
  can legitimately establish.
- **Evidence:** `PROJECT_CHARTER.md` §5 unit-of-analysis; reproducible pipeline
  (`PHASE3_VALIDATION_REPORT.md` reproducibility); transfer-by-re-run design.
- **Wording:** "demonstration on a bounded pilot"; "transferable in principle";
  never "generalizes".
- **Remains a limitation?** YES — generalization explicitly disclaimed.

### R3 — "Comparing two unvalidated methods proves nothing."
- **Valid?** Invalid as stated. The claim is *decision-relevant sensitivity to
  method choice*, which is established by the disagreement itself and is
  *actionable regardless of which is right* — plus the noon mechanism makes the
  divergence interpretable, not arbitrary.
- **Evidence:** C1–C4; `proxy_vs_physical_comparison.csv` timestamp breakdown; the
  air-temp-vs-radiant-load mechanism in `PHASE5_0_PROXY_DEFINITION.md` §8.
- **Wording:** "method choice materially changes decisions" — never "the model
  corrects the proxy".
- **Remains a limitation?** PARTIAL — cannot say which method is correct; stated.

### R4 — "This overlaps the heat-aware routing literature."
- **Valid?** Invalid. Routing presupposes the destination set; this produces it
  (upstream screening). The paper complements, does not compete.
- **Evidence:** `RESEARCH_GAP.md` B.1 / C.1 (CoolWalks etc. already cover Spanish
  cities; screening is the under-served upstream step).
- **Wording:** position as *suitability screening*, explicitly cite the routing
  frontier as adjacent and out of scope.
- **Remains a limitation?** NO — but must be pre-empted in §2 or a reviewer will
  pattern-match.

### R5 — "Arbitrary thresholds / this is a disguised scoring system."
- **Valid?** Partly valid (thresholds are chosen) but the design answer is
  strong: constraint-first, first-failing-gate, no weighted sum, and every
  threshold sourced and sensitivity-tested.
- **Evidence:** C13; `PHASE3_DECISION_ARCHITECTURE.md`; UTCI breaks from Bröde et
  al.; exposure terciles *labelled* as empirical/relative
  (`PHASE5_0_PROXY_DEFINITION.md` §4); accessibility sensitivity C11.
- **Wording:** "auditable thresholds, each cited or explicitly empirical"; never
  "objective" or "assumption-free".
- **Remains a limitation?** PARTIAL — threshold choice disclosed; the empirical
  exposure tercile is the softest and is flagged.

### R6 — "Accessibility is straight-line distance, not real walking exposure."
- **Valid?** Valid. Straight-line is a reach *lower bound*, not a route.
- **Evidence:** `PHASE3_VALIDATION_REPORT.md` (no routing); C11 shows category
  stable across radii; routing explicitly out of scope.
- **Wording:** "straight-line reach constraint (lower bound); en-route exposure not
  modelled".
- **Remains a limitation?** YES.

### R7 — "Opening hours from 2026 applied to a 2023 date."
- **Valid?** Valid. A real temporal mismatch.
- **Evidence:** handoff §7 item 7; `PHASE3_VALIDATION_REPORT.md` (point-in-time
  documented hours, `evidence_completeness` flags PARTIAL rows).
- **Wording:** disclose as a documented data-vintage caveat; note the Monday/August
  closures used are real and cited.
- **Remains a limitation?** YES.

### R8 — "Indoor 'refuge' assumes cooling without verifying A/C."
- **Valid?** Valid. A/C and queue/approach exposure unverified.
- **Evidence:** handoff §7 item 6; indoor thermal evidence capped at MODERATE by
  design (`PHASE3_DECISION_ARCHITECTURE.md` §2).
- **Wording:** "assumed thermal buffering, A/C unverified; indoor evidence capped
  at MODERATE".
- **Remains a limitation?** YES.

### R9 — "The authors are really claiming a behavioural / tourism-flow benefit."
- **Valid?** Invalid — and pre-empted throughout. No behavioural claim is made.
- **Evidence:** C14; `PROJECT_CHARTER.md` §3; `PHASE3_VALIDATION_REPORT.md`
  "no behavioural claim".
- **Wording:** screening of *options*, never prediction of *choice*; no
  redistribution or outcome language anywhere.
- **Remains a limitation?** NO — it is a deliberate boundary, stated as such.

### R10 — "This is just a dashboard / an engineering artefact."
- **Valid?** Invalid as the paper's object. The dashboard is a C-tier appendix; the
  contribution is the architecture + method-sensitivity result.
- **Evidence:** `RESEARCH_GAP.md` D (product absence is not a gap); MVP kept to an
  optional appendix (Figure 7); results rest on tables, not the UI.
- **Wording:** the visual prototype is "an auditable presentation of the locked
  outputs", explicitly not a contribution.
- **Remains a limitation?** NO — but the paper must keep the UI subordinate.

---

## Most dangerous criticism

**R1 (no field validation) fused with R3 (two unvalidated methods).** Together
they are the one line that can sink the paper if the framing slips: "you compare
two unvalidated surfaces and cannot show either is right." The *only* durable
defence is the disciplined claim ceiling — the contribution is **decision-relevant
sensitivity to method choice plus a transparent architecture**, which does not
depend on either method being validated. Any sentence that drifts toward "physical
modelling gives better/safer decisions" hands the reviewer R1+R3 and must be
struck.

## Publication ceiling (Task 10)

**Realistic manuscript class:** an **applied methods / decision-support** paper
with a **reproducible case-based framework** character, sitting at the
intersection of **tourism-climate adaptation** and **geospatial tourism/urban
management**. It is an integration-transparency-reproducibility contribution, not
a metric/algorithm breakthrough.

**Journal *type* that is realistic** (no shopping here — type only): solid applied
/ regional venues in sustainable cities, urban climate applications, applied
geospatial analysis, or tourism-climate adaptation — venues that reward
transparent methodology, reproducibility, and honest scope over novelty of
technique.

**Journal *type* that would likely reject on the evidence ceiling:** top-tier
remote-sensing or biometeorology venues demanding **field-validated** Tmrt/UTCI
(R1 is disqualifying there); high-impact methods venues demanding a
**generalizable, multi-city or multi-day** result (R2); and behavioural/tourism-
economics venues expecting an **observed tourist-outcome** effect (R9, which the
paper deliberately does not provide). Aiming there would force exactly the
overclaims this charter forbids.
