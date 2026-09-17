# Project status

**Audit date: 2026-09-17.**

This file is the canonical status record for this repository. It exists to reconcile
any first-page or badge wording with the actual evidence in this repository, its two
public archival records, and its GitHub pull-request/issue history. Where this file and
any other document disagree, this file governs.

This repository now hosts **two separate layers of work** with two separate statuses.
They must never be collapsed into one status line:

| Layer | Content | Status |
|---|---|---|
| **A. Locked publication** | The archived HATI-Madrid pilot (DOI-bound preprint) | **`RELEASE_LOCKED`** |
| **B. Research extension** | `docs/research/pedestrian-heat/` — a new, bounded research thread hosted in the same repository | **`RESEARCH_FROZEN_AFTER_GATE_3B`** |

Layer B is new research. It does **not** revise, reopen, or alter Layer A's locked
scientific content, DOI, or archived claims, unless and until a separate
publication/release process explicitly says so (see the Layer A/Layer B boundary, §B.4).

---

## A. Locked publication layer

### A.1 Status classification

**`RELEASE_LOCKED`**

The scientific content this repository documents — the single Madrid pilot (21 Aug
2023), the 27 curated assets, the operational-proxy vs SOLWEIG/UTCI comparison, the
eight decision scenarios, the locked result tables, and the four publication figures —
is **fixed**. It is archived under an immutable DOI and republished as a preprint. This
layer's job is to preserve and correctly describe that locked release, not to extend it.
Nothing in this audit changes any locked number, table, figure, threshold, route,
geometry, forcing, perturbation, or decision rule belonging to this layer.

Why this label and not another:

- Not `ACTIVE_BOUNDED`: no PR against this layer's own scientific content is open, and
  no PR has altered a locked number, table, or figure since the DOI'd release. (The
  repository as a whole contains post-release research work — see Layer B, §B —
  but that work is scoped to a separate document tree and does not touch this layer.)
- Not `PAUSED_PENDING_EVIDENCE`: this layer is not idling while waiting on a specific
  external trigger to resume development. Nothing is blocked; the release is simply
  finished and locked.
- Not plain `MAINTENANCE_ONLY`: that label would be accurate too, but it doesn't
  capture *why* — the constraint is that the archived DOI'd artifact (Zenodo
  `10.5281/zenodo.22707470`) is immutable, so any edit to this layer's scientific
  content would desynchronize the repository from the thing it documents.
  `RELEASE_LOCKED` names that constraint explicitly.

### A.2 Current reference

| Artifact | Identifier | Date |
|---|---|---|
| **Repository HEAD / default branch (`main`)** | commit `fcbb9b6` | 2026-09-17 |
| **GitHub release (citable code snapshot)** | tag [`v0.1.0`](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/releases/tag/v0.1.0) | 2026-09-01 |
| **Preserved pre-revision science checkpoint** | tag `pre-targeted-revision-v0.2` | — |
| **Archived preprint (version-specific)** | Zenodo DOI [`10.5281/zenodo.22707470`](https://doi.org/10.5281/zenodo.22707470) | recorded 2026-09-14 |
| **Archived preprint (concept, always latest)** | Zenodo concept DOI `10.5281/zenodo.22707469` | — |
| **Preprint text (human-readable)** | [ResearchGate](https://www.researchgate.net/publication/414226835_Thermal_representation_as_a_decision_variable_in_heat-adaptive_tourism_opportunity_screening_evidence_from_a_Madrid_pilot) | recorded 2026-09-14 |

**Known gap, flagged rather than fixed here:** the GitHub release tag (`v0.1.0`,
2026-09-01) predates the confirmed ResearchGate/Zenodo publication (2026-09-11 →
confirmed 2026-09-14), the four subsequent documentation PRs, and the entire Layer B
research extension. `main` and the Zenodo/ResearchGate text remain consistent with each
other for Layer A's content, but there is currently no GitHub tag/release that matches
the repository's present `main`. This is *not* simply closed by cutting a new tag off
`main`: `main` now carries both the locked Layer A content and the Layer B research
extension, so a tag against current `main` would be a snapshot of both, not a
republication of the locked preprint alone. Any future GitHub release/tag must
explicitly state whether it snapshots the locked publication layer, the later research
extension, or both; no new release is required by this reconciliation, and none is
made here.

### A.3 Demonstrated vs. simulated / derived / provisional / unvalidated

| Demonstrated (in-repo, reproducible) | Simulated / derived / provisional / unvalidated |
|---|---|
| Operational-proxy classification from AEMET hazard bands + OSM tree-count exposure | SOLWEIG-modelled Tmrt and the UTCI derived from it are **model outputs**, never observed thermal comfort |
| Constraint-first, first-failing-gate screening logic and its outputs for the 8 scenarios | "Robust / Boundary / Unstable" confidence labels reflect stability under the *tested* uncertainty dimensions only (solar-forcing realization + targeted canopy geometry), not accuracy or field validation |
| The 14/42 (33.3%) reclassification count and its 9-more-restrictive / 5-less-restrictive split | No field measurement of Tmrt/UTCI exists anywhere in the project |
| The 7/8 scenario change vs. proximity-only baseline, and the S8 no-survivor state | Opening-hours data recorded in 2026 applied retrospectively to the 2023 study day |
| Figure render scripts assert their headline numbers against the locked tables before saving | "Indoor refuge" is an assumed thermal-buffering state, not a physically measured condition |
| ResearchGate URL and Zenodo DOI, owner-confirmed against the live Zenodo record | No tourist behaviour, substitution, or outcome is measured or claimed |
| Publication status (public preprint, non-peer-reviewed, no journal selected) | Author affiliation/ORCID metadata: unresolved, marked `UNKNOWN` in `submission/researchgate/PUBLIC_TRUTH_AUDIT.md`, not invented |

This table summarizes; the authoritative source is the README's *What the project does
not claim* and *Limitations* sections, and `submission/researchgate/PUBLIC_TRUTH_AUDIT.md`.

### A.4 Claim ceiling

HATI-Madrid (Layer A) does **not** claim, and this status record does not raise that
ceiling:

- SOLWEIG/UTCI as ground truth, or the physical method as more accurate than the proxy;
- that the physical method supplied a richer categorical decision signal (in this
  configuration, all 42 physical-outdoor observations fell into one category);
- any change in tourist behaviour, visitor flow, or safety/health outcome;
- behavioural optimality of any specific alternative;
- generalisation beyond this single bounded Madrid pilot and study day;
- peer review, journal acceptance, or operational/real-time product status;
- validation of `ROBUST` beyond the tested uncertainty dimensions.

### A.5 Allowed maintenance changes

Consistent with `RELEASE_LOCKED`, the following are in scope for Layer A without
changing this layer's status:

- Fixing broken links, typos, formatting, and outdated status wording;
- Correcting or completing citation/publication metadata (DOIs, ResearchGate/Zenodo
  URLs, `CITATION.cff`) as new *confirming* evidence arrives (e.g., a human verifies
  affiliation/ORCID text);
- Cutting a new GitHub tag/release, provided it explicitly states whether it snapshots
  the locked Layer A content, the Layer B research extension, or both (see the gap
  noted in §A.2 — `main` no longer contains only Layer A, so an unlabeled tag against
  current `main` would not by itself close that gap);
- Adding a licence file if the owner selects one (the licence choice itself is not
  made here — see the ambiguity noted below);
- Non-scientific repository administration (visibility, description, README badges)
  that does not alter or reinterpret a locked number, table, or figure;
- Hosting the bounded Layer B research extension in its own document tree, provided it
  never edits Layer A's locked numbers, tables, figures, or claims.

Out of scope while Layer A is `RELEASE_LOCKED`: new scenarios, new thermal methods, new
study days/areas, changed thresholds, regenerated/altered locked tables or figures, new
claims of validation, or presentation-layer features beyond the existing read-only
replay prototype in `app/` — **for this layer's own locked pilot.** (Layer B's separate,
bounded pedestrian-heat work is described in §B and is not governed by this
restriction, because it is not part of the locked pilot's content.)

### A.6 What would reopen Layer A development

Any of the following would be grounds to move Layer A's status back toward
`ACTIVE_BOUNDED`:

- Field validation data for Tmrt/UTCI (e.g., in-situ sensor readings) that could be
  compared against the modelled field;
- A journal review decision (the manuscript is not currently submitted anywhere; a new
  submission and its outcome would be new evidence);
- A concrete external user/stakeholder need to extend the pilot itself to a new day,
  season, or district, with the resources to do so under the same evidence standards;
- Observed-behaviour or usability data from the `app/` prototype beyond the existing
  bounded owner desk review recorded in PR #2;
- A formal decision by the repository owner to fold Layer B's findings into a revision
  of the locked pilot (see the Layer A/Layer B boundary, §B.4) — until that happens, Layer B stays a separate research
  thread and does not, by itself, reopen Layer A.

Until one of these occurs, Layer A stays in maintenance/documentation mode.

---

## B. Frozen research-extension layer

### B.1 Status classification

**`RESEARCH_FROZEN_AFTER_GATE_3B`**

`docs/research/pedestrian-heat/` is a separate, phase-gated research thread that began
after Layer A's DOI'd release and progressed through Gate 3B (final verdict below). It
is **new research hosted in the same repository**, not a revision of the DOI-locked
HATI-Madrid preprint, unless and until a separate publication/release process
explicitly says so.

Gate 3B completed the currently authorised research sequence, and the sequence is now
deliberately **frozen** rather than paused pending routine follow-up work. Concretely,
"frozen" means:

- no active scientific development on this extension;
- no new gate opened simply to continue the sequence (no Gate 4, no Gate 3C);
- no rerunning of the experiment until a route winner appears;
- no speculative expansion to new Madrid areas, dates, or OD pairs;
- no dashboard/product expansion presented as scientific progress;
- no reinterpretation of `ABSTAIN` as inconclusive-therefore-unfinished.

`ABSTAIN / NO ROBUST DIFFERENCE` (§B.2) is treated as a valid, final bounded research
outcome. This layer does not need a positive route winner to be complete. §B.3 lists
the narrow, specific conditions under which Layer B may reopen; those are reopening
conditions, not a roadmap or backlog, and none of them has occurred.

Gate history (all merged into `main`, no open PR remains):

| Gate | PR | Merged | Verdict |
|---|---|---|---|
| Gate 1 — feasibility / methodological definition | [#7](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/7) | 2026-09-14 | MODIFY (methodology refined before proceeding) |
| Gate 2 — evidence freeze | [#8](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/8) | 2026-09-15 | `GO_TO_FIRST_THERMAL_EXPERIMENT` |
| Gate 3A — first thermal / pipeline-falsification experiment | [#10](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/10) | 2026-09-16 | `GATE3A_CORRECTED_GO_TO_3B` (corrected stateful SOLWEIG execution, fail-closed structural Catastro acquisition/parsing, date-aware meteorological forcing) |
| Gate 3B — robustness / evidence-sufficiency experiment | [#9](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/9) | 2026-09-16 | **`ABSTAIN / NO ROBUST DIFFERENCE`** (final) |

PR #10 (Gate 3A) was merged before PR #9 (Gate 3B); both carry the same corrected,
date-aware protocol propagated between them. As of this audit there is no open pull
request or open issue associated with either gate, or with any part of this
repository's research content — **0 open research PRs** (see §7).

No work exists in the repository past Gate 3B. This status record does not open, imply,
or schedule a Gate 4, and no such gate is authorised or planned.

### B.2 Scientific ceiling of the extension (current, final for this gate sequence)

At minimum, the following facts must be preserved wherever this extension is described:

- **Gate 3A** established that the corrected pipeline (stateful single-call SOLWEIG,
  fail-closed structural Catastro parsing, date-aware forcing) could produce a
  reproducible, time-resolved modeled comparison under the bounded experiment — a
  baseline difference was observed, with no scientific winner declared.
- **Gate 3B** found that comparative difference was **not robust** under justified
  perturbations (canopy vintage/source, side-of-street mapping): the Route A−B sign
  reverses under ≥1 frozen perturbation at both tested departures, and the perturbation
  ensemble spans zero.
- **Final Gate-3B result: `ABSTAIN / NO ROBUST DIFFERENCE`.**
- **No route is established as cooler, superior, safer, healthier, or preferable.**
  Thermal intensity marginally favours Route A; exposure duration favours Route B — a
  preserved trade-off, not a resolved winner.
- **No pedestrian-level Tmrt/UTCI validation exists.** All thermal fields remain
  model outputs, exactly as in Layer A.
- The result is fundamentally an **evidence-sufficiency / robustness finding**, not a
  failure: ABSTAIN is treated as a first-class outcome of the gate design, not an
  inconclusive experiment to be rerun until it produces a winner.

Full basis, decision rule, and negative-control results are recorded in
`docs/research/pedestrian-heat/gate3b/GATE3B_DECISION.md` and
`docs/research/pedestrian-heat/gate3a/GATE3A_DECISION.md`, which govern over any
summary here if they disagree.

### B.3 Reopening conditions (narrow; not undertaken here)

Layer B may reopen only if new evidence could realistically change the Gate 3B
decision. Per `GATE3B_DECISION.md`, plus one further externally driven condition, the
specific conditions are:

- independent pedestrian-level Tmrt/UTCI measurement (would reopen a Path-A
  comparative claim);
- an authoritative current-vintage classified canopy/crown model (would collapse the
  dominant canopy-source uncertainty dimension);
- resolved, authoritative side-of-street sidewalk mapping;
- a concrete external stakeholder/research requirement that justifies a new,
  separately scoped study.

None of these has occurred. These are reopening conditions, not a roadmap or
backlog — they do not themselves authorise any new gate. Absent them, ABSTAIN stands
as the final result of this research sequence, and this audit does not begin any new
gate to pursue them.

### B.4 Boundary with Layer A

The pedestrian-heat extension is new research hosted in the same repository, but it is
**not** a revision of the DOI-locked HATI-Madrid preprint (Zenodo
`10.5281/zenodo.22707470`) unless and until a separate publication/release process
explicitly says so. Concretely:

- The extension does not alter any locked number, table, figure, threshold, route,
  geometry, forcing, perturbation definition, or decision rule belonging to Layer A.
- The extension uses its own study day, its own OD pair (Atocha → Puerta de Alcalá),
  its own routes, and its own frozen decision rule — none of these are Layer A objects.
- The extension's ABSTAIN verdict does not retroactively weaken, strengthen, or
  reinterpret any Layer A claim; Layer A never made a route-superiority claim for this
  OD pair to begin with.
- Should the repository owner later decide to fold Layer B's findings into a formal
  publication or a revision of the archived preprint, that would be a new, explicit
  publication/release action — not something this status record performs or implies.

---

## Repository-wide facts

### 7. Open issues and pull requests

As of 2026-09-17 (verified live against GitHub): **0 open issues; 0 open pull
requests, across both Layer A and Layer B.** PR #11 (the documentation reconciliation
that introduced this two-layer status model) merged 2026-09-16. This freeze update
(§B.1) is itself made via a new documentation-only pull request against `main`,
touching only this file and one README paragraph and changing no scientific content;
it does not, by itself, reopen this "0 open pull requests" count once merged.

| # | Title | Layer | Disposition |
|---|---|---|---|
| [#1](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/1) | docs: align HATI public status and evidence framing | A | Merged 2026-09-01. Documentation-only. |
| [#2](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/2) | HATI Spatial Decision Replay — linked scenario inspection | A | Merged 2026-09-05. Read-only presentation layer over locked outputs; no new science. Desk-reviewed by owner, not field/usability validated. |
| [#3](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/3) | Release/researchgate v1.0 | A | Merged 2026-09-11. Prepared bounded preprint release package. |
| [#4](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/4) | docs: neutralize preprint release for Zenodo archival | A | Merged 2026-09-11. Platform-neutral PDF/metadata prep; no scientific content changed. |
| [#5](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/5) | docs: confirm ResearchGate + Zenodo publication status | A | Merged 2026-09-14. Recorded owner-confirmed live ResearchGate and Zenodo records. |
| [#6](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/6) | docs: add PROJECT_STATUS.md as canonical status record | A | Merged 2026-09-14. First version of this file; superseded by this revision, which adds Layer B. |
| [#7](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/7) | docs(pedestrian-heat): Gate 1 feasibility dossier — verdict MODIFY | B | Merged 2026-09-14. New bounded research thread, not part of the locked pilot. |
| [#8](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/8) | research: pedestrian-heat Gate 2 — evidence freeze | B | Merged 2026-09-15. `GO_TO_FIRST_THERMAL_EXPERIMENT`. |
| [#9](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/9) | research: pedestrian-heat Gate 3B robustness experiment → ABSTAIN | B | Merged 2026-09-16. Final gate result to date: `ABSTAIN / NO ROBUST DIFFERENCE`. |
| [#10](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/10) | research: pedestrian-heat Gate 3A first thermal + sampling correction | B | Merged 2026-09-16 (before #9). `GATE3A_CORRECTED_GO_TO_3B`. |
| [#11](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/11) | docs: reconcile PROJECT_STATUS with merged pedestrian-heat extension | — | Merged 2026-09-16. Documentation-only (this file + one README paragraph); introduced the two-layer status model and added no scientific content. |

No issue-tracker activity has occurred (0 issues opened to date, either layer).

---

## Ambiguity flagged, not resolved here

**Repository licence.** No `LICENSE` file exists in this repository. The README
states: *"No repository-wide licence has yet been assigned... until then, please
treat the code and text as 'all rights reserved' and contact the author before
reuse."* This is a genuine open decision for the repository owner, not a gap this
audit can close — assigning a licence is a substantive legal choice, not a
documentation fix, so it is intentionally left unresolved and unassigned here. Note
that the Zenodo record's own licensing terms (if any were set during deposit) may
differ from the repository's code/text licensing; that is outside this repository's
version control and was not verified as part of this audit. This ambiguity applies to
the whole repository, both layers.
