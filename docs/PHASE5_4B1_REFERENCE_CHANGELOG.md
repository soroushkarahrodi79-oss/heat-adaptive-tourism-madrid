# PHASE5_4B1_REFERENCE_CHANGELOG.md — HATI-Madrid

Version 1.0 · 2026-08-19. Every bibliographic correction made while resolving the 23
references from authoritative sources (publisher pages, Crossref, PubMed/ADS). No manuscript
argument, result, or literature-positioning claim was changed. Full record:
`docs/PHASE5_4B1_REFERENCE_VERIFICATION.csv`; verified list:
`manuscript/REFERENCES_VERIFIED_v1.md`; updated manuscript: `manuscript/MANUSCRIPT_TMP_v0.2.md`.

---

## A. Placeholders resolved

All **18** `[REFERENCE METADATA TO VERIFY]` placeholders from v0.1 were replaced with verified
authors, journals, volumes, issues, pages/article numbers, and DOIs. Remaining placeholders in
v0.2: **0**.

## B. In-text citation changes (short-key → verified author–year)

Every provisional short-key was replaced with a verified author–year form (mechanical citation
edit only; surrounding prose unchanged):

| Old in-text key | New in-text | Note |
|---|---|---|
| Extreme heat and urban mobility, 2025 | **Renninger & Cabrera, 2026** | year corrected (preprint 2025 → final 2026) |
| Heat risk action planning for tourism, 2026 | Scott, 2026 | |
| Tourism in a warming climate, 2026 | Ketter & Farkash, 2026 | |
| Tourist demand under climate change, 2025 | Gössling & Scott, 2025 | |
| Tourism exposure to weather extremes, 2024 | Camatti et al., 2024 | |
| Plaza thermal comfort in Madrid and Sevilla, 2022 | Karimi & Mohammad, 2022 | |
| HCI/TCI inter-comparison, 2016 | Scott et al., 2016 | |
| Hungarian HCI/TCI, 2025 | Kovács et al., 2025 | |
| Reliability of tourism climate indices, 2016 | Dubois et al., 2016 | |
| WRF-UCM-SOLWEIG mapping, 2024 | Ding et al., 2024 | |
| GIS-AHP tourism suitability, 2011 | Bunruamkaew & Murayama, 2011 | |
| Beyond land surface temperature, 2026 | Wang et al., 2026 | preprint |
| Cool Routes, 2026 | Buo et al., 2026 | |
| CoolWalks, 2025 | Wolf et al., 2025 | |
| UTCI-adjusted pedestrian accessibility, 2026 | Aydin et al., 2026 | |
| Barcelona climate-shelter accessibility, 2025 | Mombelli et al., 2025 | |
| Participatory-GIS under uncertainty, 2025 | Huck et al., 2025 | |
| Monte-Carlo UTCI/PET reliability, 2025 | Sargazi et al., 2025 | |
| OECD, 2026 | OECD, 2026 | unchanged (organisation author) |

Already author–year in v0.1 and unchanged: Lindberg et al. (2008); Bröde et al. (2012);
Colaninno et al. (2025); Gál & Kántor (2019).

## C. Preprint → final-publication upgrades (Task 4)

1. **Renninger & Cabrera** — arXiv:2501.03978 (2025 preprint) → *PNAS Nexus* 5(4):pgag078
   (2026, DOI 10.1093/pnasnexus/pgag078). **Year corrected 2025 → 2026** in-text.
2. **Wolf, Vierø & Szell (CoolWalks)** — arXiv:2405.01225 (preprint, title "CoolWalks: Assessing
   the potential of shaded routing for active mobility in urban street networks") → *Scientific
   Reports* 15:14911 (2025, DOI 10.1038/s41598-025-97200-2), final title "CoolWalks for active
   mobility in urban street networks". Reference **title corrected** to the final version;
   in-text year unchanged (2025).

## D. Title corrections in reference entries (metadata only; no in-text effect)

- **Colaninno et al. (2025):** full published title restored ("A sidewalk-level urban heat risk
  assessment framework using pedestrian mobility and urban microclimate modeling").
- **Ding et al. (2024):** full title restored (WRF-UCM-SOLWEIG framework … at city scale).
- **Aydin et al. (2026):** full title restored (UTCI-adjusted pedestrian accessibility …).
- **Karimi & Mohammad (2022):** exact published title ("… on visit of tourists in historical
  urban plazas of Sevilla and Madrid").
- **Bunruamkaew & Murayama (2011):** exact title with subtitle (Surat Thani Province, Thailand).

## E. Online-first / volume-year boundary notes (no change; recorded for transparency)

- **Gál & Kántor (2019):** *Urban Climate* 32:100571 — online 2019, volume dated 2020. Kept 2019
  (matches DOI and common citation).
- **Barcelona / Mombelli et al. (2025):** *Cities* 168:106487 — online-first 2025, volume 168
  dated 2026. Kept 2025 (online-first; DOI 10.1016/j.cities.2025.106487).
- **Gössling & Scott (2025):** *J. Sustainable Tourism* 34(5):1193–1223 — online Aug 2025, print
  May 2026. Kept 2025 (online-first).
- **Sargazi et al. (2025):** *Scientific Reports* — online 24 Dec 2025; DOI encodes 2025;
  Crossref lists volume 16 (year-boundary). Kept 2025; final volume to confirm on publisher page.

## F. Duplicate / identity-collision check (Task 5)

- **Daniel Scott** appears in three references — Scott et al. (2016) [HCI/TCI], Gössling & Scott
  (2025) [tourist demand], Scott (2026) [heat-risk action planning]. Distinct years/co-authors;
  **no 2025a/2025b or 2016a/2016b collision** and no duplicate. ✓
- No article appears twice (preprint + final both listed): only the **final** version of each
  upgraded preprint (Renninger & Cabrera; CoolWalks) is retained. ✓
- Author-name spelling normalised: Bröde (ö), Kántor (á), Kovács (á/cs), Gössling (ö),
  Vierø (ø), Błażejczyk, Holmér, Frías. ✓

## G. Claim-to-source check (Task 3) — load-bearing citations

All load-bearing citations checked against source abstracts: **all SUPPORTED**; none
PARTIALLY SUPPORTED or NOT SUPPORTED. Examples: Scott (2026) — "existing Heat Action Plans
rarely account for tourism" (Intro/Discussion governance claim); Wolf et al. (2025) & Buo et al.
(2026) — routing takes O/D or path as given (routing-boundary claim); Aydin et al. (2026) —
reachability under heat-adjusted travel (accessibility-boundary claim); Mombelli et al. (2025) —
"proximity alone insufficient" (Discussion refuge-equity claim); Sargazi et al. (2025) & Huck et
al. (2025) — Monte-Carlo / uncertainty-aware spatial decision support (uncertainty framing);
Wang et al. (2026) — LST ≠ human-centric heat stress (Intro/Discussion). See CSV column
`claim_support_status`.

## H. Unresolved / residual

- **Wang et al. (2026), "Beyond LST":** identity resolved to arXiv:2604.22433, but the title
  differs between the search snippet ("Beyond Land Surface Temperature: Explainable Spatial
  Machine Learning …") and the current arXiv abstract page ("From physical surfaces to
  human-centric heat stress …"), consistent with a cross-version title revision. Retained as a
  **preprint**; the arXiv-abstract-page title and author list are used. No peer-reviewed version
  located. This is the single reference whose published identity is not a final journal article.
- Minor fields flagged "confirm on publisher page" in the CSV (Camatti et al. exact ERL article
  number; Sargazi et al. final volume) — DOIs are authoritative and resolve correctly regardless.

## I. Files produced/updated

- `docs/PHASE5_4B1_REFERENCE_VERIFICATION.csv` (23 rows, full metadata + verification sources)
- `manuscript/REFERENCES_VERIFIED_v1.md` (verified author–year list)
- `manuscript/MANUSCRIPT_TMP_v0.2.md` (in-text author–year updates + verified reference list;
  no other prose change)
- this changelog
