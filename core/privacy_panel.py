"""Privacy/local-first explanatory panel for ALETHEIA.

Patch 104 adds reusable text and a Streamlit renderer. It does not add data
collection, telemetry, downloads, external calls, or placeholder controls.
"""
from __future__ import annotations

PRIVACY_PANEL_MARKDOWN = """
**Privacy & local-first boundary**

ALETHEIA is local-first by design. The repository includes no built-in telemetry, analytics SDKs, trackers, backend upload endpoint, public ledger sync, Global ID sync, or central user-input storage.

- Inputs are processed in the active app session.
- Receipts are user-held downloads.
- No external AI/model calls are required by default.
- For sensitive audits, run ALETHEIA locally from the repository.
- Hosted deployments may have platform-level logs outside ALETHEIA's application code.

This is a repository/application-code boundary, not a privacy guarantee about browsers, networks, operating systems, app stores, proxies, or hosting providers.
""".strip()

LOCAL_FIRST_TIP = "For maximum privacy, run ALETHEIA locally with `streamlit run app.py`."


def get_privacy_panel_text() -> str:
    """Return the reusable privacy/local-first panel text."""
    return PRIVACY_PANEL_MARKDOWN


def render_privacy_panel(container=None, *, expanded: bool = False) -> None:
    """Render the privacy/local-first panel in Streamlit.

    Importing Streamlit is delayed so this helper can be tested without running
    the Streamlit app. No buttons or placeholder downloads are included.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st
    with container.expander("🔒 Privacy & Local-First Info", expanded=expanded):
        container.markdown(PRIVACY_PANEL_MARKDOWN)
        container.info(LOCAL_FIRST_TIP)
