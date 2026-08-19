# PHASE5_4B2_PRE_SUBMISSION_REVISION_PLAN.md — HATI-Madrid

Version 1.0 · 2026-08-19. Consolidated, prioritised plan from the four-reviewer QA. No
revisions implemented here. Every fix uses **existing locked evidence only** — no new
analysis, no new study. Locations refer to `manuscript/MANUSCRIPT_TMP_v0.2.md`.

Panel tally: **FATAL 0 · MAJOR 4 · MINOR 8 (1 ignore-eligible) · SHOULD-FIX 1.**

---

## MUST FIX BEFORE SUBMISSION (the 4 MAJORs)

**M1 — Disclose the single-valued physical result (I01).**
- *Where:* Results §3.1 (add one sentence); Discussion §4.1 (adjust interpretation); Intro
  §1 (soften the "additional information" implication).
- *Smallest defensible change:* in §3.1 add, e.g., *"Under the physical configuration all 42
  outdoor observations fell in the 32–46 °C band and were therefore classified FEASIBLE WITH
  CONDITIONS; the reclassification thus reflects the proxy's three-state banding diverging
  from this single physically based band."* In §4.1, replace any implication that the
  physical method is more decision-informative with the honest reading that on this extreme
  day the radiant index places every outdoor site in strong/very-strong stress, so the
  proxy's FEASIBLE and NOT RECOMMENDED calls are not corroborated. Do not add new numbers.

**M2 — Sharpen the tourism-management contribution and "so what" (I02).**
- *Where:* Introduction (final two paragraphs); Discussion §4.5; Conclusion.
- *Smallest defensible change:* add 2–4 sentences framing the concrete DMO/operator decision
  the screen supports (which attractions to flag/deprioritise by hour, with an auditable
  reason), and connect once more to the already-cited governance/adaptation literature
  (Scott 2026; OECD 2026; Mombelli et al. 2025). No new sections; no new data.

**M3 — Reframe RQ2 away from the trivial nearest-open contrast (I03).**
- *Where:* Results §3.2 finding sentence; Discussion §4.2.
- *Smallest defensible change:* state that differing from a proximity-only pick is expected;
  relocate the contribution to (a) every removal carrying one machine-readable reason and
  (b) the explicit-decline capability. Keep the 7/8, 3/8, 23 numbers but subordinate them to
  the traceability point.

**M4 — Make S8's radius-contingency explicit (I04).**
- *Where:* Results §3.2 (S8 paragraph); Discussion §4.3.
- *Smallest defensible change:* one clause noting S8 uses a constrained 500 m reach (vs the
  800 m primary), so it demonstrates the *capability* to return no defensible alternative
  under a tighter reach, not that no-alternative is a common outcome. The accessibility
  sensitivity (category stable 7/8) already supports this.

## SHOULD FIX

**S1 — Length trim toward ~7,700–7,900 words (I09).**
- Move software/environment detail (§2.4 package/version specifics) to Supplementary S5
  (already partly there); de-duplicate Discussion §4.5 transferability vs Limitations §5.6.
  ~600–900 words recoverable. Bounded, prose-only.

**S2 — Qualify "uncertainty-aware" once (I05)** at first prominent use (Abstract or §1),
e.g. "uncertainty-aware (across the tested dimensions)"; the partiality is already in §5.3.

**S3 — Soften RQ1 "physically interpretable" → "mechanistically consistent with the radiant
term" (I06).**

## OPTIONAL (MINOR)

- O1 (I07): one Limitations sentence on untested scalability beyond curated assets.
- O2 (I08): half-sentence flagging the default land-cover simplification in §5.3.
- O3 (I10): de-emphasise the Wang et al. (2026) preprint; ensure the LST-≠-comfort point
  also rests on Gál & Kántor (2019) / Bröde (2012). **Verdict: KEEP BUT DE-EMPHASISE.**
- O4 (I11): optionally replace one "materially" with "appreciably" (descriptive framing is
  already explicit).
- O5 (I12): remind the reader (once, §3.2) that indoor survivals are assumed refuges.

## DO NOT FIX / SCOPE CREEP (refuse)
- Field Tmrt/UTCI campaign; second city; heatwave series; tourist/behavioural survey;
  mobile-phone data; routing/least-cost engine; ML/optimisation; automated city-scale
  candidate generator; dashboard features. None is required to remove a fatal flaw (there is
  none); all are FUTURE WORK.
- I13 (title jargon): title was deliberately selected in Phase 5.2I; leave unless the editor
  requests otherwise — **IGNORE for now.**

---

## Critical-attack dispositions

- **Attack 1 (two unvalidated methods):** manuscript's "sensitivity, not accuracy" defence
  is largely sufficient (A); the gap is the undisclosed single-valued physical side (B → M1).
  Fixing needs no new validation (C = no). Severity: **MAJOR**, not fatal (D).
- **Attack 2 (weak baseline):** does **not invalidate** RQ2; it changes how RQ2 is framed
  (→ M3). No new comparator built (would need new analysis).
- **Attack 3 (thresholds):** AEMET = operationally grounded; 32/46 °C = literature
  (Bröde), pre-registered; Δ=0.8 °C = empirically grounded; terciles + 800/500/1200 m =
  pre-registered-but-contextual; evidence-confidence map = weakly justified. The result most
  dependent on a soft parameter is **S8 (500 m)** → M4. 33.3% depends on the Bröde-grounded
  32/46 mapping (defensible).
- **Attack 4 (tourism contribution):** the contribution does read as generic environmental
  decision support if tourism words are removed → M2. Tourism-specific anchors that remain:
  asset eligibility, opening hours, opportunity substitution, the pre-routing decision stage,
  scenario design, experience-typed alternatives, temporal operating context.
- **Attack 5 (Wang preprint):** KEEP BUT DE-EMPHASISE (O3); no argument collapses without it.
- **Attack 6 (statistics):** descriptive framing is explicit; **MINOR** wording only (O4).
- **Attack 7 (figures):** figures are sound (visual QA holds); Fig. 2 does not imply physical
  truth (agreement/direction matrix, not a flow), but its reading is tightened by M1's prose
  disclosure. No redesign required.
