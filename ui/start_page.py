"""Start Page gate for ALETHEIA.

This helper renders static first-entry copy plus one session-only proceed
button. It does not score, route modules, inspect inputs, or alter receipts.
"""
from __future__ import annotations


START_GATE_SESSION_KEY = "aletheia_start_gate_passed"


def render_start_page(container=None) -> bool:
    """Render the first-entry Start Page and return True when the user proceeds."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.title("ALETHEIA Governance Mirror")
    container.markdown("### Mirror, not throne.")
    container.markdown(
        """
ALETHEIA helps inspect pressure around power, consent, evidence, appeal,
capture risk, and human review.

ALETHEIA gives readings, not verdicts.

It does not certify truth, safety, legality, ethics, compliance, or legitimacy.

Human judgment remains required.

For sensitive material, run locally. Hosted deployments may have platform-level
logs outside ALETHEIA's app-code boundary.
        """.strip()
    )

    container.markdown("### How to start")
    container.markdown(
        """
1. Start with Mirror Check for a short policy, claim, prompt, governance text, or AI output.
2. Read the risk reading as a review prompt, not a verdict.
3. Inspect the observed reasons and repair questions.
4. Use Evidence Lab or other modules only when you need more context.
5. Download receipts only when you want a local review record.
        """.strip()
    )

    return bool(container.button("Proceed to ALETHEIA", type="primary"))
