"""Shared copy-only status and boundary cards for ALETHEIA."""
from __future__ import annotations


def render_ai_integrity_boundary_cards(container=None) -> None:
    """Render static AI Integrity boundary/status notes."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.caption("Boundary extension: It does not certify models, vendors, codebases, prompts, agents, or outputs as safe.")
    container.caption("Demo risk examples include phrases such as certified safe only as trigger text, not as an ALETHEIA claim.")
    container.caption(
        "Scope boundary: no live model benchmarking, no external calls, no repository crawl, no public ledger, "
        "and no future-behavior guarantee."
    )
    container.caption(
        "Data boundary: no built-in telemetry, trackers, analytics SDKs, backend upload endpoint, "
        "or central storage of pasted AI Integrity artifacts."
    )
