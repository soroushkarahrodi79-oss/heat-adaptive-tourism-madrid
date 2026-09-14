# GATE1_LITERATURE_LOG — Targeted novelty update for Gate 1

**Version 0.1 · search date 2026-09-14.** Updates the Gate-0 / Phase-5.1 novelty review only
as far as Gate 1 requires. This is a **targeted** search, **not** a systematic review — no
PRISMA protocol was executed, and no systematic-review completeness is claimed.

Source engine: web search (general index), 2026-09-14. Prior in-repo evidence reused:
`docs/PHASE5_1_NOVELTY_AUDIT.md`, `docs/PHASE5_1_LITERATURE_MATRIX.csv`,
`docs/RESEARCH_GAP.md`, `docs/LITERATURE_MATRIX.csv`.

---

## 1. Search log

| Q | Query | Date | Purpose | Inclusion rationale |
|---|---|---|---|---|
| Q1 | heat-aware pedestrian shade routing SOLWEIG UTCI 2025 2026 thermal exposure route | 2026-09-14 | Confirm routing-frontier saturation | Include items that route/compare paths on modeled thermal fields. |
| Q2 | uncertainty propagation urban thermal comfort model decision robustness UTCI abstention selective prediction | 2026-09-14 | Test whether abstention/selective-prediction is occupied for UTCI | Include uncertainty-propagation / reliability frameworks; note absence of abstention. |
| Q3 | Madrid tourist pedestrian outdoor thermal comfort UTCI heatwave Retiro Prado 2024 2025 | 2026-09-14 | Madrid-visitor grounding | Include Madrid/Iberian tourist-comfort and heat-response items. |
| Q4 | decision reversal robustness paired comparison environmental model when to abstain insufficient evidence geospatial | 2026-09-14 | Find a borrowable decision-stability formalism | Include rank-reversal / pairwise-comparison robustness methods. |

## 2. Key retrieved items and classification

**DIRECT PRECEDENT (would invalidate the extension): none found.** No retrieved study frames
*evidence sufficiency / abstention* for a *comparative modeled pedestrian thermal-exposure
decision*.

**CLOSEST THREATS (narrow the envelope — must be distinguished at Gate 2):**
- *"How fine is fine enough? Impacts of temperature data resolution on heat-aware pedestrian
  routing"* (Sustainable Cities and Society, 2026) — studies how input data resolution
  changes routing decisions. **Adjacent to the evidence-sufficiency angle.** Distinction: it
  measures resolution→routing-cost sensitivity; the HATI extension measures
  evidence-sufficiency→**ABSTAIN** for a *comparative* decision, and treats "no evidence" as a
  valid outcome. Adjacent, not identical.
- *CoolPath Tool* (arXiv 2026) — SOLWEIG-GPU city-wide UTCI + "compute and compare thermal
  exposure of candidate paths." **Comparison is present**, but as a routing/selection tool
  with no abstention/evidence-grading. Distinction: HATI does not select the cooler path; it
  decides *whether the data justify any comparative claim at all*.
- *Cool routes: real-time human thermal exposure routing* (Building and Environment, 2026) —
  SOLWEIG + Dijkstra least-thermal-cost path. Routing, O+D given. Complement, not compete.

**METHOD PRECEDENT (borrowable):**
- *Comparative reliability of PET and UTCI via Monte Carlo* (Scientific Reports, 2025) —
  Thermal Comfort Reliability Index; uncertainty propagation into probabilistic UTCI. HATI
  borrows the propagation idea but keeps a categorical decision-stability output, not a
  composite index.
- *Robustness to rank reversal in pairwise comparison matrices under uncertainty bounds*
  (EJOR, 2022) and *rank-reversal-free MCDA* work — the **decision-stability formalism** the
  experiment spec adopts instead of an invented °C threshold.
- *UTCI-adjusted pedestrian accessibility* (Sustainable Cities and Society, 2026) — reach
  metric; destination set given. Upstream/downstream boundary as in Phase 5.1.

**CONTEXT PRECEDENT:**
- *Outdoor thermal comfort of tourists in historical plazas of Sevilla and Madrid* (Env Sci
  Pollut Res, 2022) — Madrid tourist-comfort grounding; comfort range ~24.5–29.8 °C.
- Madrid 2024 municipal heat-refuge initiatives (news/context) — establishes the operational
  problem; not a method.

## 3. Findings relevant to Gate 1

1. **Routing is more saturated in 2026, not less** — reinforces the Gate-0 rejection of
   "heat-aware routing / cooler route" as novelty. The extension must *not* be framed as
   routing.
2. **Abstention / selective prediction is NOT occupied for comparative UTCI** — the search
   explicitly returned no abstention/selective-prediction mechanism in UTCI models. This is
   the surviving, defensible question and the main reason the verdict is **MODIFY, not NO-GO**.
3. **No defensible universal "material UTCI difference" threshold** for this comparison type
   was found — confirming the protocol prohibition on inventing 1 °C/2 °C cuts and justifying
   the decision-stability / rank-reversal formulation.
4. **A rank-reversal robustness formalism exists and is mature** — borrowable directly, so the
   decision logic rests on established method, not on a bespoke rule.
5. **Madrid-visitor thermal evidence is thin but real** — supports grounding without
   over-claiming; no route-comparison abstention study for Madrid tourists exists.

## 4. Novelty status carried to Gate 2

The narrowed contribution — *when open data are sufficient to support (or must decline) a
comparative modeled pedestrian thermal-exposure decision, with abstention as a first-class
outcome* — survives this targeted search. The **single sharpest boundary to assert** is
against data-resolution-sensitivity-of-routing work (2026): sensitivity of a *cost* is not
the same as *declining a comparison for insufficient evidence*.

## 5. Sources

- [Cool routes: Real-time human thermal exposure routing (Building and Environment, 2026)](https://www.sciencedirect.com/science/article/abs/pii/S0360132326004270)
- [High-resolution thermal exposure and shade maps for cool corridor planning](https://www.sciencedirect.com/science/article/abs/pii/S2210670723001105)
- [How fine is fine enough? Impacts of temperature data resolution on heat-aware pedestrian routing (2026)](https://www.sciencedirect.com/science/article/abs/pii/S2210670726006256)
- [CoolPath Tool: A Thermal Comfort Path Planning Tool for Urban Mobility (arXiv, 2026)](https://arxiv.org/html/2602.02540)
- [UTCI-adjusted pedestrian accessibility (Sustainable Cities and Society, 2026)](https://www.sciencedirect.com/science/article/pii/S2210670726002222)
- [A sidewalk-level urban heat risk assessment framework (Colaninno et al., EPB, 2025)](https://journals.sagepub.com/doi/10.1177/23998083241280746)
- [Comparative reliability of PET and UTCI via Monte Carlo (Scientific Reports, 2025)](https://www.nature.com/articles/s41598-025-33440-6)
- [Robustness to rank reversal in pairwise comparison matrices based on uncertainty bounds (EJOR, 2022)](https://www.sciencedirect.com/science/article/abs/pii/S0377221722003083)
- [Robustness of priority deriving methods against rank reversal: a probabilistic approach (Ann Oper Res, 2023)](https://link.springer.com/article/10.1007/s10479-023-05753-0)
- [Towards robust results in MCDA: ranking-reversal-free methods (2022)](https://www.sciencedirect.com/science/article/pii/S1877050922014193)
- [Effect of outdoor thermal comfort on tourist visits in historical plazas of Sevilla and Madrid (Env Sci Pollut Res, 2022)](https://link.springer.com/article/10.1007/s11356-022-20058-8)
- [Madrid launches new initiative to keep people entertained in the heat (Euronews, 2024)](https://www.euronews.com/green/2024/08/08/madrid-launches-new-initiative-to-keep-people-entertained-in-the-heat)
