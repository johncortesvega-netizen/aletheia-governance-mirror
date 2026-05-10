# ALETHEIA Audit Prototype v9.6.8 — Evidence Audit / Global Grid Build

ALETHEIA is a Streamlit governance-risk research prototype aligned with the Sydney Protocol / ALETHEIA concept. It combines symbolic governance auditing, V-Axis simulation, empirical country-year evidence processing, and a population-weighted Global Grid.

ALETHEIA is a **mirror, not a throne**. It can surface governance-risk patterns for review, but it does not replace evidence, law, religion, medicine, politics, public accountability, or human judgment.

---

## Prototype status

**Current phase:** Global Grid Pass 1 is operational.  
**Recommended next build target:** Global Grid Pass 2 — comparison views and exportable selected-year analysis packets.

Global Grid Pass 1 currently supports selected-year country-year comparison, population-weighted exposure, 9k allocation where complete, active-seat diagnostics where partial, verdict distribution, integrity/collapse metrics, and coverage diagnostics.

Global Grid Pass 2 should focus on comparison and review surfaces:

- highest and lowest integrity systems,
- highest collapse-probability systems,
- largest selected-year seat allocations,
- high-impact governance-risk nodes,
- verdict distribution comparisons,
- trust vs democracy scatter,
- WGI vs V-Dem comparison,
- coverage gaps by country/year,
- trust-materiality diagnostics,
- exportable selected-year comparison packets.

---

## Prototype scope

This is a visionary research prototype and symbolic/evidence-audit workflow. It is **not** a real political system, legal authority, religious authority, medical authority, official institution, election mechanism, sovereign body, or tool for making binding decisions about people or countries.

The responsible interpretation is:

> This model suggests a governance-risk pattern worth examining.

Not:

> This model has final authority.

---

## Operating layers

ALETHEIA currently operates through six coordinated layers:

1. **Audit** — governance-language and scenario risk review using Sanctuary / Threshold / Asylum labels, Sydney Protocol guardrails, and visible module integrity checks.
2. **Simulation** — V-Axis system-health simulation tracking stability, trust, alignment, ego, grievances, friction, safeguards, and collapse risk.
3. **Empirical Evidence Audit Lab** — public country-year evidence ingestion, direct/master upload handling, WGI/WDI/V-Dem/trust carry-through, ALETHEIA variable mapping, scoring, validation checks, and downloadable scored outputs.
4. **Global Grid** — selected-year country-year comparison interface for population-weighted exposure, 9k allocation where complete, active-seat diagnostics where partial, verdict distribution, integrity/collapse metrics, and coverage diagnostics.
5. **Doctrine Reference** — current operating doctrine: mirror not throne, shared protocol state, non-divinization, empirical correction, 9k representation boundaries, and Sydney/GPA HTML references.
6. **About** — plain-language explanation, scientific caution, research direction, and developer notes.

---

## Shared protocol state

Audit, Simulation, Empirical Evidence, and Global Grid are synchronized views over a shared protocol state. Changes to empirical evidence, scoring calibration, doctrine thresholds, Sydney Protocol overlay, selected evidence year, or active Grid basis may propagate across modules.

This is intentional when it reflects shared evidence or shared doctrine. It is not acceptable when caused by accidental widget collisions, hidden demo fallback, stale session state, or unmarked prototype data.

The app distinguishes:

- **Intentional protocol propagation** — evidence, calibration, and doctrine updates affecting all relevant modules.
- **Accidental tab bleed** — unintended UI state changes crossing between modules.

---

## Module integrity and fail-closed behavior

ALETHEIA keeps a Sydney Protocol / module integrity sentinel active. Critical protocol failures should fail closed rather than present unsupported outputs.

Audit includes a visible module integrity check so failures are not hidden behind the global app gate. If a critical Sydney Protocol sentinel, audit function, scoring function, or required module is missing or broken, the system should stop that module until repaired.

Fail-closed behavior is especially important when:

- Sydney Protocol guardrails are unavailable,
- scoring functions cannot be imported,
- empirical evidence has not loaded correctly,
- hidden fallback/demo data would be mistaken for real results,
- required country-year fields are missing,
- Global Grid allocation status is incomplete but displayed as complete.

---

## Doctrine frame

The doctrine layer is the integrity frame for the prototype. It does not replace evidence or human judgment. It keeps ALETHEIA anchored as an anti-capture, service-aligned audit mirror.

Key operating principles:

- **Mirror Effect** — power should reflect service through accountability, dignity, protection, transparency, repair, and appealability.
- **V-Axis Compass** — intelligence + power − ego can support stability only when trust, transparency, appealability, service alignment, and safeguards are present.
- **Non-divinization** — no person, office, institution, nation, company, model, AI, monarch, founder, dataset, doctrine, or protocol is treated as divine, final, or beyond review.
- **Empirical humility** — outputs are diagnostic and correctable; they are not legal, political, medical, religious, moral, or predictive verdicts.
- **No throne condition** — ALETHEIA must never become the authority structure it audits.

---

## Evidence framing

ALETHEIA does not invent the empirical baseline. Public datasets provide observed evidence about governance, corruption, rule of law, political stability, institutional capacity, population, democracy, constraints, and trust.

The empirical workflow is:

```text
public evidence → ALETHEIA variable mapping → empirical scoring → Sydney Protocol overlay → audit interpretation
```

Raw empirical strength cannot override hard protocol failures such as capture, coercion, non-appealability, false divinization, opacity, sovereignty capture, or harmful authority.

---

## Empirical data currently supported

The empirical workflow supports and/or carries through:

- World Bank WDI Population, total (`SP.POP.TOTL`).
- World Bank Worldwide Governance Indicators (WGI).
- V-Dem democracy / executive-constraints fields.
- WVS/OWID generalized trust values.
- Direct uploaded country-year master files.
- Already-scored ALETHEIA master/Grid exports.

The app can generate or consume country-year masters, compute ALETHEIA empirical scores, allocate seats by selected year, preserve raw evidence fields where available, and export scored evidence tables.

---

## Trust evidence rule

ALETHEIA distinguishes raw trust evidence from trust priors.

- **Trust raw coverage** means direct survey-derived trust evidence is available, such as WVS/OWID generalized trust.
- **Trust prior coverage** means the scoring system has a usable trust prior, which may include a neutral/default value when raw survey evidence is unavailable.

A neutral trust prior is not the same as observed trust. It allows scoring continuity, but it should reduce interpretive confidence when raw trust evidence is missing.

---

## Global Grid interpretation

The Global Grid is a selected-year comparison interface, not a sovereign body or mandate.

Full allocation years may sum to 9,000 seats. Partial years, filtered views, or incomplete source years must use **active selected-year seats** language and must not be interpreted as full global allocation.

The Grid distinguishes:

- full empirical selected-year Grid,
- partial empirical subset,
- prototype regional brackets,
- inactive/no dataset state.

Coverage metrics reflect the active selected-year subset after filters. A 100% coverage value over a small subset does not imply whole-world or whole-dataset coverage.

---

## Sanctuary / Threshold / Asylum labels

These are internal prototype labels, not legal, political, medical, religious, moral, or predictive verdicts.

- **SANCTUARY** — the evidence or scenario pattern appears service-aligned, accountable, transparent, safeguarded, and comparatively stable under the current model.
- **THRESHOLD** — safeguards are incomplete, evidence is mixed, uncertainty remains, or the system needs review before being treated as stable.
- **ASYLUM** — high capture, coercion, opacity, harm, collapse pressure, or hard protocol failure is detected.

“ASYLUM” is used only as an internal protocol-risk category. It does not refer to legal asylum status, entitlement, refugee status, or humanitarian determination.

---

## Project structure

```text
app.py                  # Streamlit UI, tab layout, shared protocol state, Global Grid surfaces
about_page.py           # compact About renderer and doctrine-facing summary text
agents.py               # compact Global Grid module/fallback
core/parser.py          # local/AI governance scan helpers
core/protocol.py        # Sydney Protocol / ethics guardrail logic
core/simulation.py      # agent-based V-Axis stability simulation
core/scoring.py         # integrity, friction, collapse probability, recommendations
core/empirical.py       # country-year parsing, source carry-through, scoring, 9k allocation, validation helpers
core_empirical.py       # import fallback for Streamlit deployments
calibration/            # calibration helpers
config/weights.py       # I/A/E/P weight presets
data_processed/         # empirical templates and generated scores
paper/methodology.md    # methodology notes for study development
assets/                 # header image and optional UI assets
Sydney_Protocol_v3.2.html
GPA_v8.2.html
requirements.txt
run_tests.py
```

---

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

For local validation:

```bash
python run_tests.py
```

---

## Validation and research direction

Internal correlation checks are not independent validation when the target variable is also part of the score. Credible validation should compare ALETHEIA outputs against external outcomes that are not already score inputs, such as conflict events, coups, regime breakdown, political violence, civil unrest, forced displacement, future-year governance decline, institutional failure, or documented corruption shocks.

The model should remain testable, falsifiable, and correctable. If reproducible evidence challenges the model, the model should be revised rather than defended as absolute.

Recommended validation priorities:

1. Define external outcome targets that are not included in ALETHEIA scoring inputs.
2. Separate training/calibration data from validation data.
3. Test country-year forecasts against later-year external outcomes.
4. Report uncertainty, missingness, and coverage limitations with every comparison.
5. Preserve raw source fields so reviewers can inspect score construction.

---

## Development guardrails

ALETHEIA development should preserve the following constraints:

- No hidden demo fallback may be presented as empirical output.
- Partial selected-year views must be labeled as partial.
- 9,000-seat language is valid only when the selected-year allocation is complete.
- Raw trust evidence and trust priors must remain visibly distinct.
- Hard protocol failures must override otherwise strong empirical scores.
- Output labels must remain diagnostic, not authoritative.
- The system must remain open to correction when evidence conflicts with doctrine or calibration.

---

## Summary

ALETHEIA is a governance-risk research mirror. It combines doctrine, evidence mapping, empirical scoring, simulation, and population-weighted comparison to surface patterns worth review. It does not issue binding judgments, replace public accountability, or claim final authority.
