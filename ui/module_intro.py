"""Small copy-only module introductions for ALETHEIA."""
from __future__ import annotations


def render_stress_test_scan_intro(container=None) -> None:
    """Render the static Stress Test scan-mode note."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.info(
        "Scan my idea is for your own text. Demo scenarios are there if you choose them, "
        "but they never run by themselves."
    )


def render_boundary_cases_intro(container=None) -> None:
    """Render the static Boundary Cases calibration note."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.info(
        "Boundary cases calibrate the review model. They do not create authority, "
        "enforcement, or final decisions."
    )


def render_consent_audit_intro(container=None) -> None:
    """Render the static Consent-Audit Engine heading and intro copy."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown("### Consent-Audit Engine")
    container.write(
        "Consent is treated as valid only when refusal is realistically possible. "
        "This check looks for structural pressure, basic-rights dependency, "
        "withdrawal gaps, and unclear alternatives."
    )
