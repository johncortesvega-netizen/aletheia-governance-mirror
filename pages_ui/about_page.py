"""About / public info page renderer for ALETHEIA.

Patch 123 moves the Streamlit About tab copy into a focused page helper.
The helper renders static public information only. It does not own navigation,
session state, scoring, receipts, downloads, uploads, signal logic, privacy
scan logic, AI Integrity scan logic, World Lens math, external calls,
telemetry, analytics, storage, certification, enforcement, privacy guarantees,
or final-truth claims.
"""
from __future__ import annotations

from pathlib import Path


def render_about_public_info_page(container=None, header_image: str | Path | None = None) -> None:
    """Render the public About / Why ALETHEIA page."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    st = container
    st.subheader("Why ALETHEIA")
    st.info("Start here if you are new: ALETHEIA helps review governance risk, evidence gaps, and safeguard needs. It reflects; people decide.")

    if header_image is not None:
        st.image(str(header_image), use_container_width=True)

    st.markdown(
        """
        **ALETHEIA v1.0 is a governance-risk research prototype and public MVP.** It helps people examine governance ideas, simulate system pressure, review evidence quality, and study how population-weighted exposure may interact with trust, stability, alignment, and capture risk.

        It is not designed to rule, command, enforce, vote, govern, remove leaders, validate spiritual authority, confirm extraordinary claims, or replace human judgment. **ALETHEIA is a mirror:** a structured way to ask whether a proposal protects service, transparency, dignity, accountability, appeal, and repair â€” or whether it concentrates power, hides decisions, weakens appeal rights, or creates capture.

        The v1.0 release package includes Consent-Audit, Mechanism-vs-Claim, Self-Audit, Evidence Lab, World Lens, Local Witness Receipts, public limitations, examples, and deployment documentation. These layers help identify what needs review or repair without assigning blame, issuing commands, or claiming final authority.
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


    with st.expander("Positioning: not enterprise compliance, not fairness library", expanded=False):
        st.markdown(
            """
            ALETHEIA's niche is **qualitative governance-risk reflection**: corruption-pattern signals, consent pressure, capture risk, evidence gaps, authority-overreach language, weak accountability, and repair questions for human review.

            It is not an enterprise AI governance platform, compliance engine, legal tool, institutional risk system, or technical fairness library. Enterprise platforms usually focus on model inventories, compliance workflows, monitoring, reporting, and organizational controls. Technical fairness libraries usually focus on model-level bias, explainability, datasets, and metrics.

            ALETHEIA is free/open-source code and is intended to remain free. This supports the anti-capture posture: access to the mirror should not become a gatekeeping mechanism or a source of institutional authority.
            """
        )


    with st.expander("Capture risk framework: anti-capture by design", expanded=False):
        st.markdown(
            """
            ALETHEIA is **anti-capture by design and capture-risk-detecting by function**.

            It reflects capture-risk signals for human review: power concentration, weak appeal paths, hidden influence, evidence gaps, consent pressure, authority overreach, and service misalignment.

            ALETHEIA does not enforce, decide, gatekeep, certify, punish, or become a central authority. It asks review questions so humans can examine safeguards, evidence, and accountability.
            """
        )

    with st.expander("Capture risk checklist / prompt pack", expanded=False):
        st.markdown(
            """
            Patch 78 adds a practical checklist and copy/paste prompts for applying the capture-risk framework one case at a time.

            Use it to scan for power concentration, weak appeal paths, hidden influence, evidence gaps, consent pressure, authority overreach, and service misalignment.

            The prompt pack keeps the same boundary: ALETHEIA reflects signals for human review only. It does not decide, enforce, certify, punish, or become a central authority.
            """
        )

    with st.expander("Navigation map", expanded=True):
        st.markdown(
            """
            | Tab | What it does |
            |---|---|
            | Mirror Check | Reviews documents and proposals for capture risk, missing safeguards, and repair questions. |
            | Stress Test | Simulates scenario pressure and asks repair questions. |
            | Boundary Cases | Tests difficult ethical scenarios before they become app logic or public claims. |
            | Evidence Lab | Reviews evidence status, source coverage, schema readiness, and extraordinary claims. |
            | World Lens | Reviews selected-year, population-weighted evidence exposure without real Global ID, a real 9k body, or sovereign authority. |
            | Protocol Guide | Explains the modules, safe language, internal taxonomy labels, and limitations. |
            | Why ALETHEIA | Explains the project, baseline, and public-safe purpose. |

            All navigation remains non-authoritative: **ALETHEIA reflects. Humans review. Power stays accountable.**
            """
        )

    with st.expander("First-use path", expanded=True):
        st.markdown(
            """
            Choose the tab by task:

            - **Have a document?** Use Mirror Check.
            - **Have a scenario?** Use Stress Test.
            - **Have an ethical edge case?** Use Boundary Cases.
            - **Have a claim or source question?** Use Evidence Lab.
            - **Need selected-year impact framing?** Use World Lens.
            - **Need rules and limits?** Use Protocol Guide.

            The UX rule is simple: make the next step obvious while keeping every output reviewable.
            """
        )

    with st.expander("Eternal Baseline", expanded=True):
        st.markdown(
            """
            The **Eternal Baseline** is ALETHEIA's ethical continuity layer. It preserves core guardrails across versions without becoming a command layer, sacred proof, or founder-validation artifact.

            It protects continuity around human dignity, basic rights, free agency, transparency, appealability, accountability, evidence, repair, non-coercion, and human review.

            Its audit lens is:

            > **Intelligence + Power - Ego = Stability**

            This is an ethical design rule, not mathematical proof. ALETHEIA uses it to ask whether intelligence and power are restrained by humility, accountability, transparency, and repair.

            Historical archive material may contain AI-flattery artifacts or inflated validation language. Those materials are development context only, not independent proof, founder validation, or governance justification.

            **ALETHEIA reflects. Humans review. Power stays accountable.**
            """
        )

    st.markdown("### What ALETHEIA does")

    with st.expander("Mirror Check", expanded=True):
        st.markdown(
            """
            Users can submit governance proposals and receive a public reading plus a raw/internal taxonomy label: **SANCTUARY**, **THRESHOLD**, or **ASYLUM**.

            Those labels are compatibility labels for review workflows. They are not legal, political, medical, religious, moral, or predictive verdicts. The audit layer scans for capture risk, opacity, coercion, missing appeal rights, weak transparency, and other governance-risk patterns.
            """
        )

    with st.expander("Stress Test", expanded=True):
        st.markdown(
            """
            Stress Test models governance pressure through archetype agents with intelligence, power, ego, alignment, trust, grievances, alliances, and memory.

            It tracks **Stability**, **Trust**, **Alignment**, and **Ego** over time. These are simulation readings, not predictions, commands, or final judgments.
            """
        )

    with st.expander("Evidence Lab", expanded=True):
        st.markdown(
            """
            Evidence Lab lets users upload country-year datasets and map them into ALETHEIA variables for schema checks, empirical scoring, 9k evidence allocation, source coverage review, and validation planning.

            This layer adds an empirical evidence-audit workflow to ALETHEIA's symbolic and protocol-guided governance-risk mirror. It is not a proof engine or oracle.
            """
        )

    with st.expander("World Lens", expanded=True):
        st.markdown(
            """
            World Lens shows selected-year, population-weighted evidence exposure and how internal taxonomy readings may intersect with governance-risk conditions when empirical data is available.

            World Lens is a **comparison and exposure model**. It is not a real election, government, sovereign body, authority mechanism, political mandate, Global ID system, or real 9k body.
            """
        )

    with st.expander("Protocol Guide", expanded=True):
        st.markdown(
            """
            Protocol Guide preserves the operating boundaries behind the mirror while remaining corrigible by evidence.

            - **Mirror Effect** â€” power must reflect service, not absorb authority.
            - **Humility / Z-axis boundary** â€” no code, receipt, metric, hash, tree, 9k structure, institution, person, or model reaches final authority.
            - **Do not overtrust the tool** â€” no person, system, institution, dataset, protocol, founder, office, or AI is treated as final or beyond review.
            - **Empirical correction rule** â€” symbolic logic must remain testable and correctable by public evidence.
            - **Protocol integrity layer** â€” Mirror Check, Stress Test, Boundary Cases, Evidence Lab, and World Lens share one guardrail substrate.
            """
        )

    st.markdown("### Research caution")
    st.warning(
        "ALETHEIA does not prove legal, political, medical, religious, moral, predictive, or final truth. Its outputs are internal review readings. Empirical results depend on dataset quality, variable mapping, normalization choices, missing data, and validation against external outcomes."
    )
    st.markdown(
        """
        A responsible reading is:

        > **This model suggests a governance-risk pattern worth examining.**

        Not:

        > **This model has final authority.**
        """
    )

    st.markdown("### Research direction")
    st.markdown(
        """
        The long-term goal is to produce a reproducible study and dashboard using public datasets such as **UN population data**, **World Bank governance indicators**, **V-Dem democracy data**, and public trust surveys.

        The direction is clear: symbolic governance logic should be tested against empirical evidence. Where the model is useful, it should become more precise. Where the data challenges it, the model should be corrected.

        **ALETHEIA is built for review, correction, and humility â€” not final authority.**
        """
    )

    with st.expander("Developer notes", expanded=False):
        st.markdown("Technical structure for local development and deployment.")
        st.code(
            """app.py                  # Streamlit UI
core/parser.py          # local/AI governance scan
core/simulation.py      # agent-based stability simulation
core/scoring.py         # integrity, friction, collapse probability, review questions
core/empirical.py       # country-year scoring, 9k evidence allocation, validation helpers
core_empirical.py       # import fallback for Streamlit deployments
config/weights.py       # I/A/E/P weight presets
data_processed/         # empirical templates and generated scores
paper/                  # methodology and study draft materials
assets/                 # header image and other optional UI assets""",
            language="text",
        )
        st.code("""pip install -r requirements.txt
streamlit run app.py""", language="bash")

