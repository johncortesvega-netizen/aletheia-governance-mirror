"""Shared Streamlit app-shell notices for ALETHEIA.

Patch 108 starts the gradual app.py router/shell refactor by extracting the
repeated top-of-app boundary notices into a small UI helper. This module only
renders copy; it does not score, route verdicts, collect data, call external
services, or mutate receipts.
"""
from __future__ import annotations

PUBLIC_V1_LABEL = "ALETHEIA Governance Mirror"


def render_app_boundary_notices(supported_input_language_note: str, container=None) -> None:
    """Render the stable top-of-app boundary notices.

    ``container`` may be ``st`` or any object exposing ``markdown``. Streamlit
    is imported lazily so tests can import this helper without opening a UI
    runtime.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown(
        f"""
        <div class="prototype-note">
            <strong>Input language scope:</strong> {supported_input_language_note}
        </div>
        """,
        unsafe_allow_html=True,
    )

    container.markdown(
        """
        <div class="prototype-note">
            <strong>Plain words:</strong> ALETHEIA uses mirror-review language for humans. Sanctuary means low risk inside this prototype, not final safety. Threshold means review and repair. Asylum means high capture or harm pressure. The Z-axis stops at the human/system boundary; a receipt is your local record of what was reviewed.
        </div>
        """,
        unsafe_allow_html=True,
    )

    container.markdown(
        """
        <div class="prototype-note">
            <strong>Privacy by design:</strong> This repository includes no telemetry, trackers, analytics SDKs, backend upload endpoint, public ledger sync, Global ID sync, or central user-input database. Inputs are processed in the running app session; receipts are user-held downloads. Hosting providers may still have their own server logs.
        </div>
        """,
        unsafe_allow_html=True,
    )



def render_app_header(mascot_logo_uri: str, app_version: str, container=None) -> None:
    """Render the stable public header/hero block.

    This is static shell copy only. It does not read or write session state,
    run analysis, alter navigation, or change scoring/receipt behavior.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown(
        f"""
        <div class="botanical-frame hero">
            <div class="hero-grid">
                <div>
                    <div class="hero-kicker">Free · Open Source · Human Review Required</div>
                    <div class="hero-title"><span class="hero-title-main">ALETHEIA</span><span class="hero-title-subline">GOVERNANCE MIRROR</span></div>
                    <div class="hero-sub">Protocol-guided audit and simulation framework for human review.</div>
                    <div class="caption">Audit · Simulation · Evidence · Global comparison · Reports · English-first; Dutch batch-test examples only · Protect people. Keep truth visible.</div>
                </div>
                <div class="hero-emblem" aria-hidden="true"><img class="aletheia-mascot-logo" src="{mascot_logo_uri}" alt="" /></div>
            </div>
            <div class="civic-ribbon">
                <div class="ribbon-item"><span class="ribbon-icon">🛡️</span><div><div class="ribbon-label">Purpose</div><div class="ribbon-body">Protect people. Keep review human.</div></div></div>
                <div class="ribbon-item"><span class="ribbon-icon">📋</span><div><div class="ribbon-label">Method</div><div class="ribbon-body">Reflect pressure. Keep appeal open.</div></div></div>
                <div class="ribbon-item"><span class="ribbon-icon">🪞</span><div><div class="ribbon-label">Boundary</div><div class="ribbon-body">ALETHEIA reflects. People decide. It never rules, certifies, commands, or replaces people.</div></div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_how_to_use_note(container=None) -> None:
    """Render the stable first-use note under the header.

    This helper keeps static public copy outside ``app.py`` while preserving
    behavior. It does not collect inputs, route modules, or run analysis.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown(
        """
        <div class="prototype-note">
            <strong>How to use this:</strong> Paste an idea. ALETHEIA looks for power, pressure, appeal, and risk. It offers a mirror reading for review, and you keep the final say. It is not legal, medical, political, religious, or official advice.
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar_brand(mascot_logo_uri: str, container=None) -> None:
    """Render the stable sidebar identity card.

    This is static shell copy only. It does not read or write session state,
    run analysis, or alter scoring/receipt behavior.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown(
        f"""
        <div class="sidebar-emblem-card">
            <div class="sidebar-emblem-mark"><img class="aletheia-mascot-logo" src="{mascot_logo_uri}" alt="" /></div>
            <div class="sidebar-brand"><span class="sidebar-brand-main">ALETHEIA</span><span class="sidebar-brand-subline">Governance Mirror</span></div>
            <div class="sidebar-tagline">Free open-source governance mirror. Mirror, not throne.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_context(container=None) -> None:
    """Render stable sidebar context above interactive controls.

    The sidebar context explains the review lens, calibrated language scope,
    and application-code privacy boundary. Interactive control state remains in
    ``app.py`` so Patch 109 stays a shell extraction rather than a behavior
    refactor.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.header("Reading controls")
    container.caption("Choose how alert the mirror lens should be to pressure, trust, and fit.")
    container.caption("Input scope: English-first. Dutch/Nederlands examples may be used for batch testing, not as a general app-wide compatibility claim.")
    container.caption(
        "Privacy boundary: no built-in telemetry, trackers, analytics SDKs, backend upload endpoint, "
        "public ledger sync, Global ID sync, or central user-input database."
    )


def render_sidebar_review_lens_intro(container=None) -> None:
    """Render the static Review lens sidebar section heading and note.

    Interactive preset selection remains in ``app.py``. This helper only
    renders copy for the gradual app-shell refactor.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown("#### Review lens")


def render_sidebar_review_lens_note(container=None) -> None:
    """Render the static note below the Review lens selector."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.caption("This only sets the mirror lens. ALETHEIA waits for your idea.")


def render_sidebar_review_rhythm_intro(container=None) -> None:
    """Render the static Review rhythm sidebar section boundary."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown("---")
    container.markdown("#### Review rhythm")


def render_sidebar_review_rhythm_note(container=None) -> None:
    """Render the static note below the Review rhythm sliders."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.caption("The mirror keeps voices small so the pattern is easy to read. The 9k view lives in World Lens.")


def render_sidebar_safety_rails_intro(container=None) -> None:
    """Render the static Safety rails sidebar section boundary."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown("---")
    container.markdown("#### Safety rails")


def render_sidebar_safety_rails_note(container=None) -> None:
    """Render the static note below the Safety rails sliders."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.caption("Gentle voice, firm review rails. These settings change the reading, not the boundary.")

def render_app_footer_banner(app_version: str, container=None) -> None:
    """Render the stable footer banner.

    This is static shell copy only. It does not read or write session state,
    route modules, run analysis, alter scoring, or change receipt behavior.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown(
        f"""<div class="footer-banner"><strong>ALETHEIA reflects.</strong> People decide. · Free/open-source governance mirror · Mirror, not throne.</div>""",
        unsafe_allow_html=True,
    )

