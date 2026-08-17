# PHASE4_0_VISUAL_SEMANTICS.md — HATI-Madrid

Version 1.0 · 2026-08-17. Specification artifact only.

## 1. The problem this solves

Five locked concepts (`thermal_state`, `decision_state`,
`decision_confidence`, `evidence_confidence`, `exclusion_reason`) must stay
visually distinguishable. A single red/yellow/green scale collapses all of
them into "how bad is it," which is exactly the false single-score
impression the handoff prohibits. This doc assigns each concept its own
visual channel, chosen so channels don't cue the same interpretation.

## 2. Channel assignment

| Concept | Channel | Why this channel |
|---|---|---|
| `decision_state` | **Fill color** (categorical, 2 hues in current data) | It's the concept users scan the map for first; color is the fastest pre-attentive channel, so it should carry the single most decision-relevant fact — not severity, not confidence. |
| `decision_confidence` | **Marker shape / ring style** (solid ring / dashed ring / dotted ring / no ring) | Shape reads as "structural difference," which matches confidence being a property of the *decision's* reliability, not of the world's state. Never reuse color-brightness for this — brightness reads as severity, not reliability. |
| `evidence_confidence` | **Border weight / fill opacity of the identity chip** (solid / medium / faint) in the asset panel only | Evidence is about the underlying data, not the outcome — a "quieter" channel (opacity) matches its supporting-fact role, and keeping it off the map avoids a fifth simultaneous map channel. |
| `thermal_state` | **Icon/glyph inside the marker** (e.g. a small heat-stress pictogram vs. an indoor pictogram), plus explicit text label in every panel | This is the physical fact; it should never be inferred solely from `decision_state`'s color, because the same thermal state can map to different decisions and vice versa if either changes independently in a future dataset. |
| `exclusion_reason` | **Desaturation / ghosting + a dedicated icon badge**, never color-coded by severity | Exclusion is categorical ("why removed"), not a point on a good→bad gradient. Coding it with hue would imply some exclusion reasons are "worse" than others, which the screening logic does not assert. |

No channel is reused across two concepts. No channel uses a 3-stop
red/yellow/green ramp — see §4.

## 3. Color palette (decision_state + thermal glyph)

Two `decision_state` values exist in the current data
(`AVOID_PROLONGED_OUTDOOR_EXPOSURE`, `INDOOR_REFUGE`); the palette is
designed as an extensible categorical set, not a 2-color special case, so a
future third decision state doesn't force a redesign.

- `AVOID_PROLONGED_OUTDOOR_EXPOSURE` → **muted rust/terracotta** (`~#B5502E`
  range) — warm without being alarm-red; reads as "caution, outdoor heat,"
  not "danger/stop."
- `INDOOR_REFUGE` → **muted slate teal** (`~#2E6B6B` range) — cool without
  being a "success green," since indoor refuge is a category, not a reward.
- Reserve pure red and pure green entirely. Neither `decision_state` value
  is "good" or "bad" in isolation — an `INDOOR_REFUGE` asset that's closed is
  not a green outcome, and this must not be implied by palette choice.
- `NO_DEFENSIBLE_ALTERNATIVE` (a scenario-level, not marker-level, fact) uses
  a **distinct neutral charcoal/ink treatment**, deliberately outside the
  rust/teal pair — it is not a third point on the same severity scale, it is
  a structurally different kind of result (see Interaction Spec §S8).

## 4. Explicitly avoided patterns

- **Traffic-light gradients.** No continuous or 3-stop red-yellow-green
  anywhere, including for `evidence_confidence` or `decision_confidence` —
  both are reliability facts, not severity facts, and a stoplight ramp
  always reads as severity to users regardless of intent.
- **Gauge charts / dials.** Nothing in this dataset is a single continuous
  quantity meant to be read against a threshold at a glance (UTCI values are
  shown as numbers with units, in context, not as a dial).
- **KPI counters.** No "27 assets · 9 alternatives · 33% flagged" summary
  tile row. Counts appear only in context (e.g. "9 alternatives" as a link
  into the trade-off view), never as a standalone dashboard metric wall.
- **Magic percentages.** `decision_confidence` and `evidence_confidence` are
  categorical labels (ROBUST/BOUNDARY/UNSTABLE, HIGH/MODERATE/LOW), not
  percentages — Phase 2.2 explicitly derives these per-row from demonstrated
  sensitivity, not from a fixed numeric band, and the UI must not imply a
  number exists where the science produced a category.
- **Decorative AI/futuristic elements.** No glow, gradient fills on markers,
  particle effects, or "AI-generated insight" framing anywhere.

## 5. Typography and hierarchy (supporting, not a channel per se)

- One serif or high-contrast grotesque for headings/asset names (editorial
  register), one neutral sans for data labels and body text, one monospace
  for machine-readable tokens (`exclusion_reason` codes, field names) so raw
  and translated forms are typographically distinguishable at a glance (see
  Interaction Spec §Exclusion explainability).
- Numbers (UTCI values, distances) are right-aligned, tabular-figure, always
  paired with units — never bare.
- Category labels (`thermal_state`, `decision_state`, etc.) render as small
  caps or a label+value pair, never disguised as a headline number.

## 6. Uncertainty treatment (detail)

Confidence must be visible without a tooltip-only escape hatch (handoff/brief
requirement). Concretely:

- `decision_confidence` ring style is drawn directly on the map marker at
  default zoom — no hover required to see *that* a marker is boundary or
  unstable, only to see *why* (the "why" — the per-row demonstrated
  sensitivity — is a hover/click detail, since it's supporting evidence, not
  the headline fact).
- In the Asset Decision View, confidence gets its own labelled row with a
  one-line plain-language gloss, distinct from the thermal/decision rows:
  - `ROBUST` → "This decision held under every tested scenario variation."
  - `BOUNDARY` → "This decision is close to a threshold; some tested
    variations would flip it."
  - `UNSTABLE` → "This decision changed under tested variations — treat as
    uncertain."
  - `INDOOR_BYPASS` → "Confidence categories don't apply — this asset's
    thermal state is not physically modelled (indoor)."
- **A24 @ 18:00** (the one `UNSTABLE` source case, S7) is the canonical
  worked example bundled with the prototype's demo data: it must render
  distinctly from `BOUNDARY` (different ring style, different gloss text,
  different explicit label "genuine solar-boundary case, not a data
  artefact" per handoff §3) — never softened into the same "somewhat
  uncertain" bucket as `BOUNDARY` rows.
- The distinction the brief asks for — "high thermal stress with robust
  evidence" vs. "high thermal stress but boundary-sensitive" — is produced
  by keeping `thermal_state` (glyph + text) and `decision_confidence`
  (ring + gloss) visually independent per §2; a `VERY_STRONG_HEAT_STRESS`
  marker can carry a solid ring (robust) or a dashed ring (boundary) and the
  difference must be legible at normal map zoom, not just in the panel.

## 7. Exclusion treatment (detail)

- Excluded candidates in the Alternative/Trade-off View render desaturated
  (lower saturation/opacity of their category color) with a small "excluded"
  badge icon — visually "receding" relative to survivors, not hidden.
- Clicking/expanding an excluded item reveals its `exclusion_reason` in
  plain language (see Interaction Spec) plus the raw token in monospace.
- Exclusion styling never borrows the same rust/teal decision-state palette
  — it uses a third, neutral gray-scale treatment so "excluded" cannot be
  misread as "outdoor-heat-flagged" or any specific decision state.
