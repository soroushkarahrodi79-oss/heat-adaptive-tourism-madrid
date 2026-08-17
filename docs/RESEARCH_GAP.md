# RESEARCH_GAP.md — HATI-Madrid

Rigorous gap analysis. Version 0.1 · 2026-08-17

The purpose of this document is to protect the project from its own enthusiasm. It separates what is already known, what the field is actively fighting over, what is genuinely missing, what is merely a technology that has not yet been pointed at Madrid, and — only after all of that — what HATI-Madrid can honestly claim to add.

A recurring error in this space is to treat *"nobody has combined heat maps + tourism POIs + routing + Madrid"* as a research gap. It is not. Absence of a specific mashup is not a scientific gap; it is an empty cell in a table. A gap exists only where a **defensible question cannot currently be answered** with existing methods and knowledge. The analysis below is organised to expose that distinction.

---

## A. Established knowledge (settled — do not claim as contribution)

1. **Extreme heat is a major and rising health hazard in Madrid and Southern Europe.** Multi-decadal temperature–mortality relationships for Madrid are documented, and continental excess-mortality estimates for recent summers are large and peer-reviewed. Restating this is background, not novelty.
2. **LST is not air temperature and is not human thermal comfort.** This is textbook and now re-confirmed by 2025 remote-sensing work explicitly testing satellite LST as a proxy for intra-urban daytime heat stress and finding it inadequate on its own. Any project treating LST as comfort is not novel — it is wrong.
3. **UTCI, PET, and WBGT are established human-biometeorological indices**, each with known domains, thresholds, and limitations; comparative reliability (including Monte Carlo treatments of PET/UTCI) is itself a studied topic. Choosing among them is a methodological decision, not a discovery.
4. **Street trees, shade, and urban form measurably reduce pedestrian radiant load and improve outdoor thermal comfort.** The radiative-cooling-per-tree and mean-radiant-temperature literature is mature.
5. **Heat suppresses and reshapes urban activity and mobility.** Card-transaction and mobile-phone studies (Australia, China) show daytime activity collapse and temporal shifting under heat. That heat changes behaviour *in aggregate* is established — for residents, with proprietary or national data.
6. **Spatial multi-criteria decision analysis (MCDA) for tourism/site suitability is a decades-old, well-trodden method**, and its weakness — sensitivity of results to arbitrary weights — is equally well documented.

## B. Active research frontier (crowded — competing here is high-risk)

1. **Heat-aware / shade-optimised pedestrian routing.** This is the single most important finding for the gate. In 2025–2026 alone there are multiple peer-reviewed entries: CoolWalks (Scientific Reports 2025, using **Barcelona and Valencia** with Spanish cadastre data), solar-exposure pedestrian routing (Transactions in GIS 2025), dynamic shade-oriented pathfinding for arid cities (Computers, Environment and Urban Systems 2025), real-time thermal-exposure "cool routes" (Building and Environment 2026), and thermal-discomfort route choice in dense subtropical cities (Sustainable Cities and Society 2025), plus preprints. **A HATI contribution framed primarily as "heat-aware routing for Madrid" is not novel; it would be a late, incremental entry into a saturated frontier that already covers Spanish cities.**
2. **Fusing remote sensing with mobility to estimate travel-related heat exposure** (e.g., Chengdu 2025). Frontier, data-heavy, and dependent on mobility data HATI does not have.
3. **Attractiveness/POI quantification from mobility or Wi-Fi/behavioural data** (Scientific Reports 2025; Current Issues in Tourism 2024). Frontier, but again behavioural-data dependent.
4. **Climate-shelter accessibility and mobility justice** (Barcelona, Cities 2025). Active, and — importantly — currently framed around *residents/vulnerable groups*, not visitors.
5. **Tourism-sector heat governance/action planning** (Annals of Tourism Research 2026). Active at the policy/framework level, largely qualitative.

## C. Genuine gaps (defensible questions currently unanswerable)

These are stated as questions, not mashups:

1. **The suitability-screening gap.** The routing frontier answers *"given that I go from A to B, what is the coolest path?"* No established method answers *"which tourism opportunities should even be candidates at this hour, and why — including the option of an indoor/cool alternative — under explicit, auditable thermal constraints?"* Routing presupposes the destination set; suitability screening produces it. This upstream decision is under-served.
2. **The transparency/uncertainty gap in tourism heat-suitability.** The dominant tourism-suitability tradition is the weighted composite index, whose results are known to be weight-sensitive, yet composite tourism-climate/suitability indices rarely propagate input uncertainty or grade the confidence of each input. A **constraint-first, uncertainty-propagating, evidence-graded** alternative for tourism heat-suitability is largely absent.
3. **The integration-honesty gap.** Environmental heat modelling, cooling-resource accessibility, and tourism value are each mature in isolation but are typically integrated *by collapsing them into one number*, which hides trade-offs and conflates hazard with comfort with value. A framework that keeps hazard / exposure / comfort / accessibility / tourism-value explicitly *separate and traceable* — and states what it cannot conclude about behaviour — is methodologically underdeveloped.
4. **The Madrid-visitor gap.** Madrid heat work is health/mortality- and resident-oriented; Spanish climate-shelter accessibility work is Barcelona-and-resident-oriented. The *visitor* population in *Madrid's* specific monumental, low-shade tourist geometry is an empirical blank — but only descriptively, and only to the extent open data allows.

## D. Merely underused technology (NOT a scientific gap)

The following are tempting to dress up as gaps and must be resisted:

- "Nobody has combined Landsat/Sentinel + OSM + Madrid POIs + a heat index." That is a *pipeline that has not been built*, not a question that cannot be answered. Building it is engineering; it earns publication only if it answers B/C-type questions or is validated in a way others have not.
- "AI / machine learning has not been applied to heat-adaptive Madrid tourism." There is no defined prediction task with validation labels here. Adding ML without a supervised target and ground truth would be method theatre, and is explicitly excluded.
- "There is no dashboard for this." Product absence is a market observation, not a research gap.
- "Remote sensing at higher resolution now exists." Better sensors do not by themselves create a scientific question.

## E. Proposed contribution (what survives the filter)

After removing settled knowledge (A), crowded frontiers (B), and mere technology (D), the residue that is both *novel enough* and *supportable* is:

> **A constraint-first, uncertainty-aware, fully reproducible decision-support framework that screens Madrid tourism opportunities (outdoor and indoor/cool alternatives) by explicit thermal-exposure and cooling-resource-accessibility constraints during specific extreme-heat hours, keeping hazard/exposure/comfort/value traceably separate, grading the confidence of every input, and validating the environmental layer — while formally declining every behavioural claim the data cannot support.**

This contribution is **incremental-but-real**: its novelty is in the *decision architecture and epistemic honesty* (constraint-first + uncertainty + evidence-confidence + explicit non-claims), applied and validated for a real Southern-European destination, not in any single metric, sensor, or algorithm. That framing is defensible precisely because it does not compete on the saturated routing frontier and does not over-reach into behaviour.

### The three sentences a reviewer will use to reject a weaker version
1. "This is another heat-aware routing paper, and CoolWalks already did Barcelona/Valencia." → Avoided by making *suitability screening*, not routing, the object.
2. "This is a weighted tourism-suitability index with arbitrary weights." → Avoided by the constraint-first design and sensitivity analysis.
3. "The authors claim their tool redistributes tourists but never observe a tourist." → Avoided by the explicit behavioural non-claim and the environmental-only validation.
