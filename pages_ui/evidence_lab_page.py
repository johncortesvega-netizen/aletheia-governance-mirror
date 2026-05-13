"""Evidence Lab static UI copy helpers for ALETHEIA.

Patch 125 starts the Evidence Lab UI extraction by moving only stable
introductory copy and public-data build guidance out of app.py. This module
does not own uploads, scoring, dataframe processing, session state, downloads,
receipts, routing, signal logic, privacy scan logic, AI Integrity scan logic,
World Lens math, external calls, telemetry, analytics, storage, certification,
enforcement, privacy guarantees, or final-truth claims.
"""
from __future__ import annotations


def render_evidence_lab_intro(container=None) -> None:
    """Render the static Evidence Lab page introduction."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.subheader("Evidence Lab — Data Check")
    container.write(
        "Build or upload a country-year evidence table from public sources, then let ALETHEIA carry it through "
        "variable mapping, empirical scoring, and the Sydney Protocol overlay. "
        "This layer is where symbolic doctrine meets public evidence in a reproducible, inspectable way."
    )
    container.info(
        "Evidence does not come from ALETHEIA. Public datasets provide the baseline. ALETHEIA only maps and reflects it."
    )


def render_evidence_lab_public_data_build_intro(container=None) -> None:
    """Render the static public-data build guidance."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown("### Build a country-year table from public data")
    container.caption(
        "A simple path is: start with World Bank WGI, add population for country-level allocation, "
        "and optionally enrich the result with V-Dem and trust data. The separate merged-evidence uploader "
        "is for a fully prepared ALETHEIA-ready master CSV."
    )
    container.info(
        "Empirical build flow: WGI plus population create the core country-year base; V-Dem and trust enrich matching rows. "
        "By default, scoring stays in the modern era from 1996 onward so historical V-Dem rows are not accidentally mixed "
        "with modern population or seat allocation."
    )
