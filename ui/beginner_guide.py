"""Beginner-facing Streamlit guide for ALETHEIA.

Patch 118 polishes the first-use guide from Patch 111 without changing
scoring, routing, receipts, signal patterns, storage, telemetry, or any
authority boundary. The guide renders copy only and keeps human judgment
outside ALETHEIA.
"""
from __future__ import annotations


def get_try_this_first_markdown() -> str:
    """Return the beginner-guide markdown as static copy.

    Keeping the copy in a small helper makes it easier to test for boundary
    language without opening a Streamlit runtime.
    """
    return """
    **A safe first path**

    1. Open **Mirror Check**.
    2. Paste a short governance, AI-policy, institutional, or product claim.
    3. Run the reading.
    4. Read the **risk reading** and the observed reasons.
    5. Review the repair questions before relying on the result.
    6. Download the receipt if you want a local record.

    **First-audit checklist**

    - Is the input short enough that you can inspect the result yourself?
    - Does the reading show which pressure signals were observed?
    - Are there repair questions you can answer with evidence?
    - Is there any claim about people, law, health, safety, legitimacy, or
      institutional action that requires outside review?
    - Are you using the local version if the material is sensitive?

    **What this means**

    ALETHEIA can help you notice pressure around power, consent, evidence,
    appeal, capture risk, and human review. A stronger pressure reading means
    the input deserves more review; it does not prove wrongdoing.

    Its role is restraint: it asks where power is moving, what is hidden, who can
    appeal, and where human review is being weakened.

    **What this does not mean**

    The reading is not a verdict, certification, approval, legal finding,
    safety guarantee, privacy guarantee, compliance approval, or final-truth
    claim. It should not be used to punish, rank, blacklist, approve, or reject
    people, organizations, AI systems, or institutions.

    **Stop and review if**

    - the result would affect a person's rights, access, reputation, or safety;
    - the source evidence is missing, stale, unclear, or one-sided;
    - the text involves legal, medical, political, institutional, or financial
      consequences;
    - you cannot explain the receipt in plain language to another reviewer.

    **Sensitive material**

    For private audits, run ALETHEIA locally. Hosted deployments may have
    platform-level logs outside ALETHEIA's application-code boundary.
    """


def render_try_this_first_guide(container=None, *, expanded: bool = False) -> None:
    """Render a compact beginner path for first-time users.

    ``container`` may be ``st`` or any object exposing ``expander`` and
    ``markdown``. Streamlit is imported lazily so tests can import this helper
    without opening a UI runtime.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    with container.expander("Start here: try this first", expanded=expanded):
        container.markdown(get_try_this_first_markdown())
