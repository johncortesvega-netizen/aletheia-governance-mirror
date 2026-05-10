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
    st.subheader("About ALETHEIA")
    st.info("ALETHEIA helps review governance risk. It does not decide, enforce, or replace human judgment.")
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
            """
        )

    st.markdown(
        """
        **ALETHEIA is a governance-risk research prototype with a gentle guardian tone.** It helps users examine governance ideas, simulate systemic pressure, and study how population-weighted representation may interact with trust, stability, alignment, and capture risk.

        It is not designed to rule, command, or replace human judgment. **ALETHEIA is a mirror, not a throne:** a careful way to ask whether a proposal strengthens service, transparency, dignity, accountability, repair, and stability — or whether it concentrates power, hides decisions, weakens appeal rights, or creates systemic capture.

        The v0.1 public-safe baseline adds explicit limits: ALETHEIA may identify risk, evidence gaps, safeguard gaps, and repair gaps, but it must not command, enforce, vote, govern, remove leaders, validate spiritual authority, or replace human judgment.

        The updated doctrine style is warmer and more descriptive: soft voice, firm safeguards, evidence before certainty, and no final human or machine authority.
        """
    )


    with st.expander("Eternal Baseline", expanded=True):
        st.markdown(
            """
            The **Eternal Baseline** is ALETHEIA's ethical continuity layer. It preserves core guardrails across versions: human dignity, basic rights, free agency, transparency, appealability, accountability, evidence, repair, non-coercion, and human review.

            It is not a lawbook that punishes, and it is not an authority above people. It is a versioned reference layer for consistency.

            Its audit lens is:

            > **Intelligence + Power - Ego = Stability**

            This is treated as an ethical design rule, not mathematical proof. Intelligence and power become unstable when detached from humility, accountability, transparency, and repair.

            Historical archive material may contain AI-flattery artifacts or inflated validation language. Those materials are treated as development context, not independent proof or founder authority.
            """
        )



    with st.expander("ALETHEIA v1.0 release complete", expanded=True):
        st.write("ALETHEIA v1.0 is the finished public MVP package for the Governance Mirror line. It includes the baseline, safe-language layer, Eternal Baseline, Boundary Cases, Failure Classification, Consent-Audit, Mechanism-vs-Claim, Self-Audit, Evidence Lab, Local Witness Receipt v2, World Lens Simulation, Protocol Guide, sample reports, demo inputs, GitHub cleanup, and release documentation.")
        st.write("The v1.0 boundary remains strict: no Global ID sync, no real 9k selection, no World Leader logic, no automatic reset, no public ledger authority, no neural validation, no religious validation, no legal authority, and no automated enforcement.")
        st.write("Next planning documents live in docs/v02_roadmap.md, docs/feature_backlog.md, and docs/deployment_prep.md.")

    st.markdown("### What ALETHEIA does")

    with st.expander("Audit", expanded=True):
        st.write("Users can submit governance proposals and receive an internal prototype classification: SANCTUARY, THRESHOLD, or ASYLUM. The audit layer scans for capture risk, opacity, coercion, missing appeal rights, weak transparency, and other governance-risk patterns.")

    with st.expander("Simulation", expanded=True):
        st.write("The system models governance pressure through archetype agents with intelligence, power, ego, alignment, trust, grievances, alliances, and memory. It tracks Stability, Trust, Alignment, and Ego over time.")

    with st.expander("Empirical Study", expanded=True):
        st.write("Users can upload country-year datasets and map them into ALETHEIA variables for empirical scoring, schema checks, 9k allocation, and internal correlation checks. This layer is the bridge from symbolic prototype to reproducible research workflow.")

    with st.expander("Global Grid", expanded=True):
        st.write("The Grid shows selected-year, population-weighted governance-risk exposure across country-year rows. Full years may sum to 9,000 seats; partial or filtered years must use active-seat language. The Grid is a comparison and exposure model, not a real election, government, sovereign body, authority mechanism, or political mandate.")

    with st.expander("Boundary Cases", expanded=True):
        st.write("The Boundary Cases layer stress-tests difficult edge cases before they become app logic or public claims. It covers prediction vs free agency, consent under pressure, basic-rights scarcity, ambient capture, extraordinary claims, neural-data consent, performative ethics, and ALETHEIA self-audit. These cases calibrate the mirror; they do not create automated authority.")

    with st.expander("Failure Classification", expanded=True):
        st.write("Failure Classification separates governance-risk findings into Actor Failure, Policy Failure, Implementation Failure, and Data Failure. The goal is better repair targeting, not blame, enforcement, or automated authority.")

    with st.expander("Consent-Audit Engine", expanded=True):
        st.write("Consent-Audit checks whether a yes is genuinely voluntary. It asks whether refusal is realistically possible without losing basic rights, safety, dignity, essential services, appeal, exit, or correction. It reflects consent pressure for human review; it does not void agreements, punish people, or replace legal judgment.")

    with st.expander("Mechanism-vs-Claim Scanner", expanded=True):
        st.write("The Mechanism-vs-Claim Scanner checks whether ethical value language is backed by concrete safeguards. It compares claims like freedom, justice, dignity, service, transparency, or accountability against mechanisms such as appeal, audit trail, time limits, correction, evidence requirements, exit rights, independent oversight, and human review. It flags missing mechanisms for review; it does not infer bad faith or assign final intent.")

    with st.expander("Self-Audit Mode", expanded=True):
        st.write("Self-Audit Mode points the mirror back at ALETHEIA itself. It checks the baseline, prompts, rubrics, README language, app copy, architect-context language, and reports for founder capture, ideological lock-in, unverifiable authority, weak appeal mechanisms, overclaiming, spiritual authority leakage, insufficient human review, and missing correction loops. It reflects risk for human review; it does not prove correctness or grant authority.")


    with st.expander("Evidence Lab + Extraordinary Claim Protocol", expanded=True):
        st.write("Evidence Lab marks whether claims have strong, partial, weak, or no supplied evidence. Extraordinary claims — including spiritual, divine, prophetic, alien, neural, metaphysical, or otherwise exceptional claims — are treated as unverified unless supported by public, testable, non-coercive evidence. ALETHEIA may audit the consequences of a claim for rights, coercion, transparency, accountability, and repair; it must not validate spiritual authority or remove human review.")

    with st.expander("Local Witness Receipt v2", expanded=True):
        st.write("Local Witness Receipt v2 records a local, user-held fingerprint of a review: document fingerprint, processed document fingerprint, report fingerprint, timestamp, app/rubric/prompt version, active modules, and authority boundary. It explicitly states public ledger: No, Global ID sync: No, central storage: No, authority claim: No, and human review required: Yes.")

    with st.expander("World Lens Simulation", expanded=True):
        st.write("World Lens Simulation is a non-sovereign impact mirror. It helps users review affected groups, power gains, protection losses, basic-rights risk, minority-rights risk, ambient capture risk, appealability, exit, and repair. It uses simulated threshold signal language only; it does not activate Global ID, select a real 9k, create World Leader logic, issue automatic resets, or make governance decisions.")

    with st.expander("Protocol Guide Consolidation", expanded=True):
        st.write("Patch 43 consolidates the v0.1 logic into one user-facing Protocol Guide: Baseline, Safe Language Layer, Eternal Baseline, Boundary Cases, Failure Classification, Consent-Audit, Mechanism-vs-Claim, Self-Audit, Evidence Lab, Local Witness Receipt v2, and World Lens Simulation. It helps users understand how the modules connect while preserving the rule that ALETHEIA reflects and people decide.")

    with st.expander("Patch Workflow", expanded=False):
        st.write("Patch 36 adds a local automation toolkit: run `tools\\run_checks.bat` from Command Prompt for safe checks, use `tools\\run_patch_checks.bat 44` for patch-specific checks, and package patched items only through the manifest packager. Patch 44 hardens local continuity through `PATCH_STATUS.md`, `docs/progress_database.md`, and `docs/patch_workflow.md`.")

    with st.expander("Progress Database", expanded=False):
        st.write("The Progress Database keeps the roadmap, module map, current patch state, next-patch convention, and check commands inside the repo. It preserves development continuity without giving ALETHEIA any governance authority.")

    with st.expander("Public Release Limits", expanded=False):
        st.write("Patch 45 adds public-facing limitations, ethics, and release notes. The release boundary is explicit: ALETHEIA is a research and review prototype. It is not legal advice, political authority, religious authority, medical authority, a sovereign system, an election mechanism, or an automated enforcement tool. Outputs are diagnostic and correctable, not final verdicts.")

    with st.expander("Sample Reports", expanded=False):
        st.write("Patch 46 adds sample reports so users can inspect ALETHEIA output before uploading their own documents: a policy audit, boundary-case report, self-audit report, and local witness receipt. These examples demonstrate structure only; they are not legal advice, policy commands, governance decisions, religious validation, or final judgments.")

    with st.expander("App Navigation + Smoke Test Cleanup", expanded=False):
        st.write("Patch 47 makes the visible app path explicit: Mirror Check, Stress Test, Boundary Cases, Evidence Lab, World Lens, Protocol Guide, and Why ALETHEIA. The navigation map helps users find the right module while preserving the rule that every tab reflects or explains; no tab commands, enforces, validates spiritual authority, or replaces human judgment.")

    with st.expander("Doctrine Reference", expanded=True):
        st.markdown(
            """
            **ALETHEIA is a mirror, not a throne.** The doctrine layer preserves the symbolic principles behind the prototype in a warmer guardian style while remaining corrigible by public evidence.

            The practical tone is: care first, power accountable, evidence visible, labels humble, and every judgment open to review.

            - **Shared Protocol State** — Audit, Simulation, Empirical Evidence, and Global Grid are synchronized views over one protocol substrate.
            - **Mirror Effect** — power must reflect service, not absorb authority.
            - **V-Axis Compass** — intelligence and power only stabilize when ego is restrained and alignment, trust, transparency, and appealability rise.
            - **Non-divinization** — no person, system, institution, office, monarch, founder, dataset, doctrine, protocol, or AI is treated as divine or final truth.
            - **Empirical evidence rule** — public datasets provide the observed baseline; ALETHEIA maps that evidence into governance-risk variables and applies the Sydney Protocol overlay.
            - **Trust evidence rule** — raw survey trust and trust priors are distinct; neutral/default priors are not observed trust.
            - **Coverage and confidence** — coverage applies to the active selected view and does not imply whole-world completeness.
            - **9k representation doctrine** — population-weighted seats show proportional exposure by selected year; partial views use active-seat language and never create sovereign authority, a political mandate, or a real governance body.
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

    st.markdown("### Scientific caution")
    st.warning("ALETHEIA does not prove legal, political, medical, or religious truth. Its classifications are internal model outputs. Empirical results depend on dataset quality, variable mapping, normalization choices, missing data, and validation against external outcomes.")

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
core/simulation.py      # agent-based V-Axis stability simulation
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
        st.write("Patch 55 prepares ALETHEIA for public repository review through a repository map, contribution guide, and GitHub cleanup checklist. It is documentation-only and adds no governance authority, Global ID sync, real 9k selection, World Leader logic, automatic reset, public ledger, neural validation, religious validation, legal authority, or automated enforcement.")
