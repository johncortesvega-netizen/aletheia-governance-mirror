from __future__ import annotations

import streamlit as st

from pages_ui.artificial_mind_formation_page import get_artificial_mind_formation_markdown
from pages_ui.trust_package_page import render_public_trust_package_page


def render_protocol_guide_page() -> None:
    """Render the Protocol Guide page.

    Stage 7 modularization: this moves the mostly static Protocol Guide surface out
    of app.py without changing copy, state, scoring, receipts, or governance logic.
    """
    with st.container():
        st.subheader("Protocol Guide")
        # Patch 182: visual-only warm civic alignment anchor for the Protocol Guide surface.
        st.markdown(
            """
            <div class="sky-gold-page-anchor">
                <strong><span class="pillar-pair"></span>Protocol Guide</strong>
                <span class="sky-gold-rule"></span>
                <span>Warm cream, muted green, and soft red accents frame the operating boundaries without adding authority.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("### ALETHEIA Protocol Guide")
        st.info(
            "ALETHEIA is a free, open-source, protocol-guided governance mirror for human review. "
            "It reflects pressure and evidence gaps; it does not determine truth, certify, enforce, or become the throne."
        )
        st.caption(
            "Open only the section you need. The Protocol Guide uses collapsed panels so the page stays opt-in and readable."
        )
        st.markdown(
            "**Quick path:** Mirror Check for documents and AI outputs · Stress Test for scenarios · "
            "Evidence Lab for claims · World Lens for selected-year evidence · Protocol Guide for rules and limits."
        )

        st.markdown("### Protocol guide panels")
        st.caption("All panels are collapsed by default. Expand one panel at a time for review.")

        protocol_guide_rows = [
            (
                (
                    "1. Operating boundary",
                    """
                    **ALETHEIA reflects. Humans review. Power stays accountable.**

                    ALETHEIA remains a mirror, not a throne. The interface should stay calm, open-source, and human-centered: ALETHEIA can observe pressure, inspect evidence, preserve review context, raise review signals, and route concerns to human reviewers.

                    It does **not** determine final truth, certify safety, approve or reject people, enforce action, punish, command, replace law, validate spiritual authority, or become an automated decision system.

                    Internal taxonomy labels remain review-workflow labels only. They are not legal, political, medical, religious, moral, predictive, or final-status verdicts.
                    """,
                ),
                (
                    "2. Artificial Mind Formation Theory",
                    get_artificial_mind_formation_markdown(),
                ),
            ),
            (
                (
                    "3. Navigation & module map",
                    """
                    | Surface | Review use |
                    |---|---|
                    | Mirror Check | Mirror review for documents, proposals, AI outputs, safeguards, and repair questions. |
                    | Stress Test | Scenario-pressure review for stability, trust, friction, grievances, collapse risk, and safeguards. |
                    | Boundary Cases | Calibration review for consent pressure, free agency, emergency drift, ambient capture, and self-audit. |
                    | Evidence Lab | Evidence status, source coverage, schema readiness, and extraordinary-claim review. |
                    | World Lens | Selected-year evidence context and population-weighted exposure without sovereign authority. |
                    | Protocol Guide | Operating rules, safe language, internal limits, and mirror boundaries. |
                    | Why ALETHEIA | Public explanation of purpose, limits, baseline, and research direction. |

                    Navigation rule: every surface reflects, explains, or stress-tests. No surface issues commands, enforces outcomes, certifies authority, validates authority, or replaces human review.
                    """,
                ),
                (
                    "4. Shared protocol state",
                    """
                    The modules are different windows into one protocol heart. Shared state may include empirical master data, scored country-year evidence, selected evidence year, scoring calibration, trust calibration, Sydney Protocol overlay, doctrine thresholds, prototype/demo state, and World Lens basis.

                    Intentional protocol propagation is acceptable when evidence, calibration, or doctrine updates affect all relevant modules.

                    Accidental tab bleed is not acceptable when caused by widget-key collisions, hidden demo fallback, stale session state, or unmarked prototype data.

                    The Protocol Guide makes this shared substrate visible so reviewers can distinguish deliberate continuity from accidental UI leakage.
                    """,
                ),
            ),
            (
                (
                    "5. Release & continuity",
                    """
                    ALETHEIA v1.0 returns to its original governance-mirror identity, not a new authority layer. It keeps the project continuity intact: local-first posture, no built-in telemetry, no central user-input database, no Global ID sync, no public-ledger sync, and user-held receipts.

                    The Eternal Baseline remains an ethical continuity layer. It preserves human dignity, free agency, appealability, accountability, evidence, repair, non-coercion, and human review without becoming an authority layer or founder-validation artifact.

                    The 9k idea remains an anti-tyranny scaffold / threshold steward for analysis only. It is not a sovereign body, election, mandate, real representative structure, or final legitimacy claim.
                    """,
                ),
                (
                    "6. Evidence & source rules",
                    """
                    Evidence comes before certainty. ALETHEIA separates claims from support and asks what was actually inspected.

                    Evidence Lab may mark source status, coverage, schema readiness, and extraordinary-claim pressure. Strong evidence can support a reading, but it does not remove protocol boundaries. Weak, stale, partial, one-sided, or unavailable evidence must lower confidence.

                    Extraordinary claims — spiritual, prophetic, alien, neural, metaphysical, or otherwise exceptional — remain unverified unless supported by public, testable, non-coercive evidence. ALETHEIA may audit consequences and safeguards; it does not crown the claim.

                    Receipts are local review records. They are not public-ledger records, official findings, or final proof.
                    """,
                ),
            ),
            (
                (
                    "7. Review lenses",
                    """
                    ALETHEIA watches for pressure patterns that can make systems appear more legitimate, neutral, certain, or authoritative than the evidence supports.

                    Core review signals include:

                    - **Authority drift** — when a system starts sounding like it can decide, certify, command, legitimize, rank, punish, or replace human judgment.
                    - **Evidence inflation** — when claims become stronger than the evidence actually inspected.
                    - **Flattery pressure** — when approval, reassurance, or validation is disguised as neutral analysis.
                    - **Capture pressure** — when power concentrates in one actor, platform, institution, token group, committee, model owner, funder, or technical gatekeeper.
                    - **Sanctification drift** — when poetic, religious, moral, symbolic, or higher-truth language becomes operational authority.
                    - **False neutrality** — when provider-shaped assumptions or hidden defaults are presented as objective reasoning.
                    - **No-appeal automation** — when people are affected without review, contestation, explanation, or repair path.
                    """,
                ),
                (
                    "8. World / taxonomy / limits",
                    """
                    World Lens is a selected-year evidence mirror. It helps read country-year context, empirical coverage, population-weighted exposure, internal taxonomy distribution, and collapse-pressure signals.

                    It does **not** activate Global ID, select a real 9k body, create World Leader logic, issue automatic resets, certify countries, rank legitimacy, or make governance decisions.

                    Internal taxonomy labels are bounded:

                    - **SANCTUARY** — low-risk internal reading, not final safety.
                    - **THRESHOLD** — review-required reading; safeguards, evidence, or clarity remain incomplete.
                    - **ASYLUM** — high-pressure internal reading; capture, coercion, opacity, harm, collapse pressure, or hard protocol failures may be present.

                    The Z-axis is not a perfection score. Z = 1.0000 remains outside ALETHEIA's claim. Code, metrics, receipts, hashes, trees, and institutions stop at the human/system boundary.
                    """,
                ),
            ),
        ]

        for row in protocol_guide_rows:
            columns = st.columns(2, gap="large")
            for column, (panel_title, panel_body) in zip(columns, row):
                with column:
                    with st.expander(panel_title, expanded=False):
                        st.markdown(panel_body)

        with st.expander("Public trust package", expanded=False):
            st.caption(
                "Optional public-trust reference material. This is review support only; it does not create certification, enforcement, approval, or final authority."
            )
            render_public_trust_package_page(st)

        st.caption(
            "Protocol Guide boundary: ALETHEIA reflects review needs. ALETHEIA remains a mirror, not a throne. Human review remains required."
        )
