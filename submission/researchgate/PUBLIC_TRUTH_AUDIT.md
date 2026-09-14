# PUBLIC_TRUTH_AUDIT - HATI-Madrid

Audit date: 2026-09-11. Scope: `README.md`, `REPRODUCIBILITY.md`, `manuscript/`,
`supplementary/`, `submission/`, `outputs/publication/`, `outputs/tables/`, `tests/`,
and the relevant phase/provenance/limitations records in `docs/` and `data/processed/`.

## Canonical manuscript determination

- **MATCH** - `manuscript/MANUSCRIPT_TMP_v0.2.md` is the latest assembled manuscript on the
  public `main` history and is named canonical by the 2026-08-22 closeout audit. It incorporates
  the verified 23-reference list.
- **UNKNOWN for public release / local-only** - `MANUSCRIPT_TMP_v0.3.md` exists in local Git
  history on `phase-5.4b3-targeted-revision`, but that branch is absent from the remote and v0.3
  is not present on public `main`. It is therefore not treated as public canonical material.
- **STALE** - `MANUSCRIPT_TMP_v0.2.md` still says it was prepared for Tourism Management
  Perspectives and contains unresolved administrative placeholders. The ResearchGate builder
  neutralizes only those administrative fields; its scientific body remains unchanged.

## Headline and scope audit

| Status | Public statement | Authoritative trace |
|---|---|---|
| MATCH | Single-day Madrid pilot: 21 Aug 2023, Prado-Retiro-Atocha, 27 assets, 14 outdoor and 13 indoor, 42 outdoor asset-time observations, 8 scenarios. | `data/processed/pilot_assets.csv`, `pilot_classifications.csv`, `phase3_scenarios_summary.csv`; `tests/test_outputs.py`; manuscript and README. |
| MATCH | 14/42 = 33.3% classifications changed; 9 physical more restrictive and 5 less restrictive. | `outputs/tables/proxy_vs_physical_comparison.csv`; Figure 2 render assertions/manifest. |
| MATCH | Candidate set changed in 7/8 scenarios; nearest-open pick failed in 3/8; 23 open in-radius options were removed on thermal/evidence grounds. | `outputs/tables/phase3_hati_vs_baseline.csv`; Figure 3 render assertions/manifest. |
| MATCH | S8 evaluated 26 candidates at 15:00 with 500 m reach and returned 0 survivors / `NO_DEFENSIBLE_ALTERNATIVE`; the same source/hour has 2 alternatives at 800 m and 7 at 1200 m. | `data/processed/phase3_scenarios.csv`, `phase3_scenarios_summary.csv`, and `outputs/tables/phase3_accessibility_sensitivity.csv`. |
| MATCH | Phase 2.2 confidence distribution is ROBUST 35/42, BOUNDARY 6/42, UNSTABLE 1/42; A24 at 18:00 is the only unstable row. | `data/processed/phase2_2_decision_confidence.csv`; `docs/PHASE2_2_DECISION_UNCERTAINTY.md`; Figure 4 manifest. |
| MATCH | Satellite-derived irradiance changed 1/42 decisions; -10% and -20% perturbations changed 0/42. | `outputs/tables/solar_forcing_sensitivity.csv`. |
| CONTRADICTION (resolved by provenance) | `outputs/tables/decision_robustness.csv` reports 19 ROBUST / 20 BOUNDARY / 3 UNSTABLE. | The file is the earlier Phase 2.1 fixed +/-2 C classification. Phase 2.2 explicitly replaced that rule with an evidence-derived envelope and names `phase2_2_decision_confidence.csv` as source of truth. The historical table was not edited. |
| MATCH | All 42 physical-configuration outdoor rows fall in `FEASIBLE WITH CONDITIONS`; this is sensitivity to end-to-end thermal representation, not physical-method superiority. | `data/processed/phase2_2_decision_confidence.csv`; README; manuscript/supplement claim limits. |

## Publication-status audit

| Status | Location / finding | Release treatment |
|---|---|---|
| STALE | README badge/status/table said pre-submission, named Tourism Management Perspectives as the current primary orientation, claimed a pending remote branch merge, and said submission had not occurred. | Updated to ResearchGate release-candidate status, non-peer-reviewed, no future journal selected, and historical 2026-08-22 submission / 2026-08-23 desk rejection. |
| STALE | README manuscript section used the older provisional title. | Updated to the title in the canonical assembled manuscript. |
| STALE | `CITATION.cff` used an older provisional title, journal target, placeholder repository URL, and pre-targeted-revision version. | Updated to factual author/repository/current title and a journal-free release-candidate citation. Affiliation and ORCID remain unstated. |
| STALE | `LINKEDIN_POST_FINAL.md` described the work as pre-submission. | Updated only to non-peer-reviewed ResearchGate release wording; all scientific caveats remain. |
| STALE but historical | `submission/SUBMISSION_INVENTORY_v0.1.md`, Phase 5 journal-fit/assembly records, and `MANUSCRIPT_TMP_v0.2.md` contain the former journal framing. | Preserved as dated historical/audit material. The ResearchGate package does not treat them as current routing instructions. |
| MATCH / historical | User-verified history: submitted 2026-08-22; desk rejected 2026-08-23. | Preserved explicitly as history, not presented as peer review or publication. |
| UNKNOWN | Affiliation, ORCID, funding, competing interests, acknowledgements, and any Zenodo record/DOI. | Not invented. Affiliation/ORCID must be supplied by the owner if applicable; no Zenodo DOI or record URL exists yet. |
| RESOLVED (2026-09-14) | ResearchGate URL. | The preprint is confirmed publicly uploaded: https://www.researchgate.net/publication/414226835_Thermal_representation_as_a_decision_variable_in_heat-adaptive_tourism_opportunity_screening_evidence_from_a_Madrid_pilot — added to README, CITATION.cff, and `RESEARCHGATE_METADATA.md`. |

## Branch verification

- Local branch: `phase-5.4b3-targeted-revision` exists at commit
  `0c96e016857576eccd39fb9c154ef222b3d87743`.
- Remote branch: `git ls-remote --heads origin phase-5.4b3-targeted-revision` returned no ref on
  2026-09-11. The branch does **not** currently exist on `origin`.

## Claim ceiling

The release does not claim field or ground-truth validation of Tmrt/UTCI, observed tourist
behaviour, safety or health benefit, operational/readiness status, generalisation beyond the
single day and bounded Madrid pilot, physical-method superiority, or peer review.
