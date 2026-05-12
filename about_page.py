import streamlit as st
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
ABOUT_HEADER_IMAGE = PROJECT_ROOT / "assets" / "about_header.png"


def _header_image() -> str | None:
    candidates = [ABOUT_HEADER_IMAGE, PROJECT_ROOT / "afbeelding.png"]
    for path in candidates:
        if path.exists():
            return str(path)
    return None


def render_about():
    st.subheader("Why ALETHEIA")
    st.info("ALETHEIA helps people review governance risk, evidence gaps, and safeguard needs. It reflects; people decide. Calibrated input language support is English and Nederlands/Dutch.")
    st.caption("ALETHEIA v1.0 complete: public MVP package, release boundary, v0.2 roadmap, and deployment prep are documented.")

    header = _header_image()
    if header:
        st.image(header, use_container_width=True)

    with st.expander("First-use path", expanded=True):
        st.markdown(
            """
            - **Mirror Check** — review a document.
            - **Stress Test** — try a scenario.
            - **Boundary Cases** — test an ethical edge case.
            - **Evidence Lab** — separate evidence from claims.
            - **World Lens** — simulate population-impact risk without authority.
            - **Protocol Guide** — read the operating rules and limits.
            
            **Input language scope:** English and Nederlands/Dutch are calibrated across the app. Other languages may be pasted as text, but risk lexicons are not validated for them yet.
            """
        )

    st.markdown(
        """
        **ALETHEIA is a governance-risk research prototype with a gentle, practical tone.** It helps users examine governance ideas, simulate systemic pressure, and study how population-weighted exposure may interact with trust, stability, alignment, safeguards, and capture risk.

        It is not designed to rule, command, or replace human judgment. **ALETHEIA is a mirror, not a throne:** a careful way to ask whether a proposal strengthens service, transparency, dignity, accountability, repair, and stability — or whether it concentrates power, hides decisions, weakens appeal rights, or creates systemic capture.

        The public-safe baseline is explicit: ALETHEIA may identify risk patterns, evidence gaps, safeguard gaps, and repair questions, but it must not command, enforce, vote, govern, remove leaders, validate extraordinary authority claims, or replace human judgment.

        The current doctrine style is neutral and friendly: soft voice, firm safeguards, evidence before certainty, and no final human or machine authority. The Humility Protocol keeps the Z-axis bounded: it marks the edge of what human and system tools may responsibly claim, not a perfection score.
        """
    )


    with st.expander("Scope layers: tool, research, vision, out of scope", expanded=False):
        st.markdown(
            """
            **Current operational layer:** ALETHEIA is a corruption-pattern and governance-risk detection framework for human review. It surfaces evidence gaps, consent pressure, capture risk, power concentration, missing safeguards, and authority-overreach signals.

            **Research layer:** benchmarks, empirical mappings, scenario tests, validation work, and documentation may make the mirror more precise over time, but they remain reviewable and correctable.

            **Vision layer:** the long-term incorruptible-system idea is a theoretical horizon about what governance would look like if anti-corruption principles were followed consistently: transparency, consent, accountability, proportionality, dignity, appealability, repair, and limits on concentrated power.

            **Out-of-scope layer:** ALETHEIA does not govern, enforce, allocate authority, select representatives, create a real 9k body, issue mandates, validate spiritual or political authority, or replace human judgment.
            """
        )

    with st.expander("Eternal Baseline", expanded=True):
        st.markdown(
            """
            The **Eternal Baseline** is ALETHEIA's ethical continuity layer. It preserves core guardrails across versions: human dignity, basic rights, free agency, transparency, appealability, accountability, evidence, repair, non-coercion, and human review.

            It is not a lawbook that punishes, and it is not an authority above people. It is a versioned reference layer for consistency.

            Its audit lens is:

            > **Intelligence + Power - Ego = Stability**

            This is treated as a design caution, not mathematical proof. Intelligence and power become unstable when detached from accountability, transparency, appeal, and repair.

            Historical archive material may contain AI-flattery artifacts or inflated validation language. Those materials are treated as development context, not independent proof or founder authority.
            """
        )




    with st.expander("Humility Protocol / Z-axis boundary", expanded=True):
        st.write("The Z-axis now describes how close a reading is to the boundary of what human and system tools may responsibly claim. It is not a perfection score and it never grants final safety or final authority.")
        st.write("Z=0.9999 is the highest human/system review boundary shown by ALETHEIA. Z=1.0000 remains outside ALETHEIA's claim: beyond code, metrics, receipts, hashes, trees, 9k structures, and institutional power.")
        st.write("9k is framed as a human anti-tyranny scaffold / threshold steward. It can help examine representation and exposure, but it is not a final safety claim, not a source of final legitimacy, and not an authority claim.")

    with st.expander("ALETHEIA v1.0 release complete", expanded=True):
        st.write("ALETHEIA v1.0 is the finished public MVP package for the Governance Mirror line. It includes the baseline, safe-language layer, Eternal Baseline, Boundary Cases, Failure Classification, Consent-Audit, Mechanism-vs-Claim, Self-Audit, Evidence Lab, Local Witness Receipt v2, World Lens Simulation, Protocol Guide, sample reports, demo inputs, GitHub cleanup, and release documentation.")
        st.write("The v1.0 boundary remains strict: no Global ID sync, no real 9k body, no World Leader logic, no automatic reset, no public ledger authority, no neural validation, no religious validation, no legal authority, and no automated enforcement.")
        st.write("Next planning documents live in docs/v02_roadmap.md, docs/feature_backlog.md, and docs/deployment_prep.md.")

    st.markdown("### What ALETHEIA does")

    with st.expander("Audit", expanded=True):
        st.write("Users can submit governance proposals and receive a public reading plus a raw/internal taxonomy label: SANCTUARY, THRESHOLD, or ASYLUM. These labels are compatibility labels for human review, not final verdicts, final safety claims, or authority claims. The audit layer scans for capture risk, opacity, coercion, missing appeal rights, weak transparency, and other governance-risk patterns.")

    with st.expander("Simulation", expanded=True):
        st.write("The system models governance pressure through archetype agents with intelligence, power, ego, alignment, trust, grievances, alliances, and memory. It tracks Stability, Trust, Alignment, and Ego over time.")

    with st.expander("Empirical Study", expanded=True):
        st.write("Users can upload country-year datasets and map them into ALETHEIA variables for empirical scoring, schema checks, 9k allocation, and internal correlation checks. This layer is the bridge from symbolic and protocol-guided governance-risk mirror to an empirical evidence-audit workflow.")

    with st.expander("World Lens", expanded=True):
        st.write("World Lens shows selected-year, population-weighted governance-risk exposure across country-year rows. Full years may sum to 9,000 evidence seats; partial or filtered years must use active-seat evidence language. World Lens is a comparison and exposure model, not a real election, government, authority mechanism, political mandate, Global ID system, or real 9k body.")

    with st.expander("Boundary Cases", expanded=True):
        st.write("The Boundary Cases layer stress-tests difficult edge cases before they become app logic or public claims. It covers prediction vs free agency, consent under pressure, basic-rights scarcity, ambient capture, extraordinary claims, neural-data consent, performative ethics, and ALETHEIA self-audit. These cases calibrate the review model; they do not create authority, enforcement, or final decisions.")

    with st.expander("Failure Classification", expanded=True):
        st.write("Failure Classification separates governance-risk findings into Actor Failure, Policy Failure, Implementation Failure, and Data Failure. The goal is better repair targeting, not blame, enforcement, or automated authority.")

    with st.expander("Consent-Audit Engine", expanded=True):
        st.write("Consent-Audit checks whether a yes is genuinely voluntary. It asks whether refusal is realistically possible without losing basic rights, safety, dignity, essential services, appeal, exit, or correction. It reflects consent pressure for human review; it does not void agreements, punish people, or replace legal judgment.")

    with st.expander("Mechanism-vs-Claim Scanner", expanded=True):
        st.write("The Mechanism-vs-Claim Scanner checks whether ethical value language is backed by concrete safeguards. It compares claims like freedom, justice, dignity, service, transparency, or accountability against mechanisms such as appeal, audit trail, time limits, correction, evidence requirements, exit rights, independent oversight, and human review. It flags missing mechanisms for review; it does not infer bad faith or assign final intent.")

    with st.expander("Self-Audit Mode", expanded=True):
        st.write("Self-Audit Mode points the mirror back at ALETHEIA itself. It checks the baseline, prompts, rubrics, README language, app copy, architect-context language, and reports for founder capture, ideological lock-in, unverifiable authority, weak appeal mechanisms, overclaiming, final-authority leakage, insufficient human review, and missing correction loops. It reflects risk for human review; it does not prove correctness or grant authority.")


    with st.expander("Evidence Lab + Extraordinary Claim Protocol", expanded=True):
        st.write("Evidence Lab marks whether claims have strong, partial, weak, or no supplied evidence. Extraordinary claims — including spiritual, prophetic, alien, neural, metaphysical, or otherwise exceptional claims — are treated as unverified unless supported by public, testable, non-coercive evidence. ALETHEIA may audit the consequences of a claim for rights, coercion, transparency, accountability, and repair; it must not validate extraordinary authority claims or remove human review.")

    with st.expander("Local Witness Receipt v2", expanded=True):
        st.write("Local Witness Receipt v2 records a local, user-held fingerprint of a review: document fingerprint, processed document fingerprint, report fingerprint, timestamp, app/rubric/prompt version, active modules, and authority boundary. It explicitly states public ledger: No, Global ID sync: No, central storage: No, authority claim: No, and human review required: Yes.")

    with st.expander("World Lens Simulation", expanded=True):
        st.write("World Lens Simulation is a non-authority impact mirror. It helps users review affected groups, power gains, protection losses, basic-rights risk, minority-rights risk, ambient capture risk, appealability, exit, and repair. It uses simulated threshold signal language only; it does not activate Global ID, select a real 9k, create World Leader logic, issue automatic resets, or make governance decisions.")

    with st.expander("Post-61 Regression Smoke Test", expanded=False):
        st.write("Patch 62 verifies that the split Patch 61 calibrations still work together: ASYLUM repair questions, malicious-leadership metric calibration, country-scoped available years, missing raw-trust labels, selected-year World Lens value guards, and Netherlands 2024 fixture stability. It is diagnostic only and adds no authority or enforcement.")

    with st.expander("Protocol Guide Consolidation", expanded=True):
        st.write("Patch 43 consolidates the v0.1 logic into one user-facing Protocol Guide: Baseline, Safe Language Layer, Eternal Baseline, Boundary Cases, Failure Classification, Consent-Audit, Mechanism-vs-Claim, Self-Audit, Evidence Lab, Local Witness Receipt v2, and World Lens Simulation. It helps users understand how the modules connect while preserving the rule that ALETHEIA reflects and people decide.")

    with st.expander("Patch Workflow", expanded=False):
        st.write("Patch 36 adds a local automation toolkit: run `tools\\run_checks.bat` from Command Prompt for safe checks, use `tools\\run_patch_checks.bat 44` for patch-specific checks, and package patched items only through the manifest packager. Patch 44 hardens local continuity through `PATCH_STATUS.md`, `docs/progress_database.md`, and `docs/patch_workflow.md`.")

    with st.expander("Progress Database", expanded=False):
        st.write("The Progress Database keeps the roadmap, module map, current patch state, next-patch convention, and check commands inside the repo. It preserves development continuity without giving ALETHEIA any governance authority.")

    with st.expander("Public Release Limits", expanded=False):
        st.write("Patch 45 adds public-facing limitations, ethics, and release notes. The release boundary is explicit: ALETHEIA is a research and review prototype. It is not legal advice, political authority, religious authority, medical authority, an election mechanism, or an automated enforcement tool. Outputs are diagnostic and correctable, not final verdicts.")

    with st.expander("Sample Reports", expanded=False):
        st.write("Patch 46 adds sample reports so users can inspect ALETHEIA output before uploading their own documents: a policy audit, boundary-case report, self-audit report, and local witness receipt. These examples demonstrate structure only; they are not legal advice, policy commands, governance decisions, extraordinary-claim validation, or final judgments.")

    with st.expander("App Navigation + Smoke Test Cleanup", expanded=False):
        st.write("Patch 47 makes the visible app path explicit: Mirror Check, Stress Test, Boundary Cases, Evidence Lab, World Lens, Protocol Guide, and Why ALETHEIA. The navigation map helps users find the right module while preserving the rule that every tab reflects or explains; no tab commands, enforces, validates extraordinary authority claims, or replaces human judgment.")

    with st.expander("Doctrine Reference", expanded=True):
        st.markdown(
            """
            **ALETHEIA is a mirror, not a throne.** The doctrine layer preserves the symbolic principles behind the prototype in a warmer guardian style while remaining corrigible by public evidence.

            The practical tone is: care first, power accountable, evidence visible, labels humble, and every judgment open to review.

            - **Shared Protocol State** — Audit, Simulation, Empirical Evidence, and World Lens are synchronized views over one protocol substrate.
            - **Mirror Effect** — power must reflect service, not absorb authority.
            - **Humility / Z-axis boundary** — no code, receipt, metric, hash, tree, 9k structure, institution, person, or model reaches final authority.
            - **No final authority claim** — no person, system, institution, office, founder, dataset, doctrine, protocol, or AI is treated as final or beyond review.
            - **Empirical evidence rule** — public datasets provide the observed baseline; ALETHEIA maps that evidence into governance-risk variables and applies the Sydney Protocol overlay.
            - **Trust evidence rule** — raw survey trust and trust priors are distinct; neutral/default priors are not observed trust.
            - **Coverage and confidence** — coverage applies to the active selected view and does not imply whole-world completeness.
            - **9k representation doctrine** — population-weighted seats show proportional exposure by selected year; partial views use active-seat language and never create authority, a political mandate, or a real governance body.
            """
        )



    with st.expander("Release Candidate Checklist", expanded=False):
        st.write("Patch 48 adds a v0.1 release-candidate checklist: included modules, explicit exclusions, safe and forbidden output language, manual smoke-test steps, automated checks, and readiness criteria. A release candidate is treated as a testable package, not a truth claim or authority system.")



    with st.expander("Legacy Test Cleanup", expanded=False):
        st.write("Patch 49 separates current safe checks from older legacy test cleanup. The default command is `tools\\run_checks.bat`, which runs the latest patch-specific test chain and compile checks, then reports legacy cleanup candidates without blocking the current workflow. Known blockers are documented in `docs/legacy_test_cleanup.md`. This is developer workflow only; it adds no governance authority.")



    with st.expander("v0.1 Release Package", expanded=False):
        st.write("Patch 50 packages ALETHEIA v0.1 as a public MVP: included modules, explicit exclusions, quickstart commands, release readiness checks, and sample-report links are gathered in `docs/v01_release_package.md`. This is packaging only; it adds no legal, political, religious, medical, sovereign, or enforcement authority.")

    with st.expander("Git Diff Workflow", expanded=False):
        st.write("Patch 51 adds an optional Git-based patch workflow. `docs/git_diff_workflow.md` explains how to initialize Git, preview `.diff` patches with `git apply --check`, apply them with `git apply`, export local changes, and fall back to patched-items-only zip files when needed. This is developer workflow only; it adds no governance authority.")

    with st.expander("UX Polish", expanded=False):
        st.write("Patch 52 shortens the public navigation language and adds first-use guidance. It does not change scoring, doctrine, evidence handling, governance boundaries, or authority rules.")

    with st.expander("Final v0.1 Smoke Release", expanded=False):
        st.write("Patch 53 adds a final release-level smoke checklist in `docs/final_v01_smoke_release.md`. It confirms required release docs, examples, workflow commands, safe-language boundaries, and non-authority framing remain present before public v0.1 packaging. It adds no doctrine, no enforcement, and no governance authority.")



    with st.expander("Post-62 Release Refresh", expanded=False):
        st.write("Patch 63 refreshes the public release surface after Patch 61A–61E and Patch 62. README, About, public release notes, progress database, and patch status now reflect ASYLUM repair questions, malicious-leadership metric calibration, country-scoped available years, explicit raw-trust fallback wording, and selected-year World Lens value guards. This is release-surface hardening only; it adds no authority or enforcement.")


    with st.expander("Mirror Check Batch Baselines", expanded=False):
        st.write("Patch 71 records the official EN/NL batch-file catalog for examples/batch_questions/ and examples/batch_scenarios/. Mirror Check question banks validate that audit questions are treated as QUESTION_PROMPT review tools rather than governance proposals requiring normal scoring.")
        st.write("Expected batch receipt behavior: 50 receipts, 50 JSON receipts, no scenario-hash mismatches, Audit Question / Review Tool label, no normal scoring for question prompts, and the authority boundary preserved: no public ledger, no Global ID sync, no central storage, no authority claim, and human review required.")
        st.write("See docs/batch_file_catalog.md and docs/mirror_check_batch_baselines.md for the official filenames, contract, and testing notes.")
        st.write("Patch 65 adds Stress Test prompting guidance. Patch 71 catalogs the official scenario batches: stress_test_scenarios_en_v1.txt, stress_test_scenarios_nl_v1.txt, and governance_language_stress_test_en.txt. Stress batch mode is explicit opt-in, local-only, and creates Simulation receipts without authority claims, public ledger, Global ID sync, or central storage.")
        st.write("See docs/stress_test_prompting_guide.md and docs/stress_test_batch_baselines.md for the scenario-writing rules and batch contract.")

    st.markdown("### Scientific caution")
    st.warning("ALETHEIA does not prove legal, political, medical, religious, moral, predictive, or final truth. Its outputs are internal review readings. Empirical results depend on dataset quality, variable mapping, normalization choices, missing data, and validation against external outcomes.")

    st.markdown(
        """
        A responsible reading is:

        > **This model suggests a governance-risk pattern worth examining.**

        Not:

        > **This model has final authority.**
        """
    )

    st.markdown("### Research direction")
    st.write("The long-term goal is to produce a reproducible study and dashboard using public datasets such as UN population data, World Bank governance indicators, V-Dem democracy data, and public trust surveys. Symbolic governance logic should be tested against empirical evidence; where the model is useful, it should become more precise, and where the data challenges it, the model should be corrected.")
    st.markdown("**ALETHEIA is built for that process.**")

    with st.expander("Developer notes", expanded=False):
        st.markdown("Technical structure for local development and deployment.")
        st.code(
            """app.py                  # Streamlit UI
core/parser.py          # local/AI governance scan
core/simulation.py      # agent-based stability simulation
core/scoring.py         # integrity, friction, collapse probability, recommendations
core/empirical.py       # country-year scoring, 9k allocation, validation helpers
core_empirical.py       # import fallback for Streamlit deployments
config/weights.py       # I/A/E/P weight presets
data_processed/         # empirical templates and generated scores
paper/                  # methodology and study draft materials
assets/                 # header image and other optional UI assets""",
            language="text",
        )
        st.code("pip install -r requirements.txt\nstreamlit run app.py", language="bash")

    with st.expander("GitHub Cleanup Package", expanded=False):
        st.write("Patch 55 prepares ALETHEIA for public repository review through a repository map, contribution guide, and GitHub cleanup checklist. It is documentation-only and adds no governance authority, Global ID sync, real 9k body, World Leader logic, automatic reset, public ledger, neural validation, religious validation, legal authority, or automated enforcement.")

PATCH_61A_ASYLUM_REPAIR_NOTE = "High-risk ASYLUM outputs include repair questions for human review only."


PATCH_61B_MALICIOUS_LEADERSHIP_METRIC_NOTE = "Malicious leadership scenarios cannot display perfect trust/alignment without concrete safeguards; human review remains required."


PATCH_61C_COUNTRY_YEAR_AVAILABLE_YEAR_NOTE = "World Lens / Evidence Lab year controls now show only years available for the selected country and avoid silent global/default fallback."


PATCH_61D_MISSING_RAW_TRUST_NOTE = "World Lens now distinguishes observed raw trust from neutral trust-prior fallback values."


PATCH_61E_WORLD_LENS_VALUE_GUARD_NOTE = "World Lens selected-year diagnostics now check seat totals, focus-country values, no-stale-year behavior, and trust-prior clarity without adding authority or enforcement."

# Patch 66 documentation anchor
PATCH_66_STRESS_TEST_RISK_SENSITIVITY_NOTE = "Patch 66 raises Stress Test sensitivity so subtle governance-risk scenarios route to Needs Safeguards instead of being washed into Sanctuary by stable raw metrics."


# Patch 67 note: Stress Test THRESHOLD / Needs Safeguards outputs now include repair prompts and light metric softening while preserving the mirror-only authority boundary.

PATCH_67_1_NOTE = "Patch 67.1 adds Dutch Stress Test lexicon calibration so Dutch governance stress scenarios route to Needs Safeguards instead of being washed into Sanctuary."


PATCH_67_2_NOTE = "Patch 67.2 closes Dutch Stress Test lexicon gaps and adds app-wide English/Nederlands input-scope wording."


PATCH_68_ADVANCED_ENGLISH_STRESS_NOTE = "Patch 68 adds advanced English Stress Test calibration and Asylum metric enforcement so advanced high-risk scenarios do not wash into Sanctuary."

# Patch 69 note for maintainers:
# Stress Test batch mode now recognizes formal audit/repair question banks as
# QUESTION_PROMPT review tools. Baseline: examples/batch_questions/formal_doctrine_repair_questions_nl.txt

PATCH_69_1_STRESS_BATCH_CLASSIFIER_NOTE = "Patch 69.1 separates Stress Test .txt scenario batches from audit-question batches so declarative advanced scenarios remain Simulation USER_INPUT while formal question banks remain QUESTION_PROMPT review tools."


# Patch 68.1: ASYLUM / High receipts keep label and metric presentation consistent.

# Patch 70: Tree visual calibration.
# The tree is a visual state explainer for Mirror Check and Stress Test, not a second protocol metric.
# QUESTION_PROMPT is an input/review-tool mode, not a fourth risk state.
PATCH_70_TREE_VISUAL_CALIBRATION_NOTE = "Patch 70 separates visual tree score from receipt integrity and clarifies Mirror Check, Stress Test, and QUESTION_PROMPT tree modes."


# Patch 71: Batch file repository consolidation.
PATCH_71_BATCH_FILE_CATALOG_NOTE = "Patch 71 catalogs official EN/NL batch filenames, expected question-prompt behavior, and latest Stress Test distributions without changing scoring or authority boundaries."
PATCH_71_1_MODULE_DEMO_LABEL_NOTE = "Patch 71.1 separates Mirror Check and Stress Test demo libraries and load-button labels so each module shows module-specific examples without changing scoring, receipts, tree visuals, or authority boundaries."
