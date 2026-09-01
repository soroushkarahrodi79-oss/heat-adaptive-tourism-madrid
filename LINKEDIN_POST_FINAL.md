# LINKEDIN_POST_FINAL — HATI-Madrid

**Thesis:** Eligibility before ranking
**Repository:** https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid
**Publication date:** Wednesday, 2 September 2026
**Publication time:** 16:00 Europe/Madrid (CEST)
**Recommended visual:** `outputs/publication/figures/FIG03_SCREENING_CONSEQUENCE_v0.1.png`
(8-scenario screening consequence with the S8 no-survivor state highlighted) — or text-only.

> ⚠️ **Gate before posting:** the corrected README currently lives on PR #1
> (`claude/hati-madrid-publication-readiness-ofw1p1`), not yet on `main`. The **public landing
> page still shows the "Repository: private" badge until PR #1 is merged.** Merge PR #1 and update
> the repo *description* (still ends "Private.") before the repository link is truthful.

---

## VERSION A — RECOMMENDED (balanced: credible + readable)

A recommendation system can rank the wrong things perfectly.

Most decision tools jump straight from a list of options to a score. But an option that breaks a hard constraint should never enter the ranking in the first place — no matter how well it scores.

In HATI-Madrid, a research pilot on heat-adaptive urban tourism, I put eligibility before ranking. Every candidate first passes an ordered set of hard gates — open? reachable? thermally tolerable? enough evidence? a real improvement? — and only the survivors are compared.

Across 8 pre-registered decision scenarios on one extreme-heat day in central Madrid, constraint-first screening changed the candidate set in 7 of 8 cases versus a simple "nearest open option" baseline.

The most interesting case returned nothing. Under one scenario's exact constraints — including a 500 m reach limit — no candidate survived, so the system reported "no defensible alternative" instead of forcing a recommendation. Widen the radius and options reappear; the point is that a system should be allowed to say "none, under these constraints."

The lesson travels well beyond heat and tourism: before optimising among choices, define which choices are actually admissible.

HATI-Madrid is a pre-submission research prototype — several thermal values are model-derived, and it is not an operational or real-time product. Code, data provenance and figures are public here:
https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid

Where in your field does a hard constraint quietly get treated as just another weighted factor — and what breaks when it does?

#DecisionIntelligence #TourismResearch #Geospatial #ClimateAdaptation

---

## VERSION B — ACADEMIC (methods-forward, for researchers)

Eligibility before ranking — a note from a heat-adaptive tourism pilot.

Screening and scoring are different operations, and conflating them is a common failure mode in decision-support design: a composite score can rank an option that violates a hard constraint, when the constraint should have removed it upstream.

HATI-Madrid tests a constraint-first alternative for heat-adaptive tourism opportunity screening. Candidates pass an ordered gate chain — opening hours, straight-line reach, an outdoor thermal limit (model-derived UTCI), evidence sufficiency, and a meaningful-improvement check — with the first failing gate recording a single machine-readable exclusion reason. No weighted composite; thermal state, decision confidence, and evidence confidence stay as separate fields.

On one AEMET-designated extreme-heat day in a ~3.5 km² central-Madrid pilot (27 curated assets), the surviving candidate set diverged from a proximity-only nearest-open baseline in 7 of 8 pre-registered scenarios. In one scenario (Parque del Retiro, 15:00, 500 m reach), zero evaluated candidates survived and the pipeline returned an explicit NO_DEFENSIBLE_ALTERNATIVE state; the same source at 800 m and 1200 m yielded surviving alternatives, so the null is constraint-contingent, not a general claim about the area.

Two boundaries worth stressing: the thermal fields are modelled (SOLWEIG → Tmrt → UTCI), not field-validated, and this is pre-submission work, not an operational system.

Repository (code, provenance, figures):
https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid

For methodologists: when is an explicit "no defensible option" output preferable to returning a least-bad ranked candidate — and how should such systems be evaluated?

#DecisionIntelligence #TourismResearch #Geospatial #ClimateAdaptation

---

## RECOMMENDATION

**Post Version A.** It carries the same evidence and boundaries as B but leads with the idea, not
the method, so it reaches destination-management and decision-intelligence readers as well as
researchers. Keep B in reserve if the audience skews academic.

## Suggested hashtags
`#DecisionIntelligence #TourismResearch #Geospatial #ClimateAdaptation`
(Add `#Madrid` only if you want local reach; 4 focused tags read better than 5.)

## Optional first comment (posted by you, right after publishing)
> Method note: the two thermal paths — a simple open-data proxy and a physically based
> SOLWEIG→UTCI configuration — are treated as alternatives of equal standing, not one as ground
> truth. Full limitations and reproducibility notes are in the repo README.

## Recommended visual — decision
Attach **FIG03_SCREENING_CONSEQUENCE_v0.1.png** — it shows all 8 scenarios and the S8 no-survivor
state, which is exactly the "eligibility before ranking" story, and it is a locked publication
figure (accurate to the evidence). If you prefer a cleaner feed, **TEXT-ONLY is also fine** — the
post stands on its own.

---

## HOW TO SCHEDULE NATIVELY IN LINKEDIN (two steps)
1. Start a post, paste Version A, attach the visual (optional), then click the **clock / "Schedule"
   icon** at the bottom-right of the post box (next to "Post").
2. Set **date = Wed 2 Sep 2026**, **time = 16:00**, confirm the timezone shows **CEST (Europe/Madrid)**,
   click **Next → Schedule**. Then add the optional first comment manually once it publishes.
