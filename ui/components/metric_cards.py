from __future__ import annotations

import html

import streamlit as st


def _clean(value: object) -> str:
    """Return escaped text for small HTML cards."""
    return html.escape("" if value is None else str(value))


def metric_card(label: str, value: str, helper: str = "") -> None:
    """Render the shared ALETHEIA metric card used across modules.

    This is a UI helper only. It does not calculate or alter any metric value.
    Callers must pass already-computed display values.
    """
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{_clean(label)}</div>
            <div class="metric-value">{_clean(value)}</div>
            <div class="metric-help">{_clean(helper)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def soft_card(title: str, body: str) -> None:
    """Render the shared soft explanatory card used in result summaries.

    This is a presentation helper only. It does not decide, score, or classify.
    """
    st.markdown(
        f"""
        <div class="soft-card">
            <strong style="color:#d4b88a;">{_clean(title)}</strong><br>
            <span style="color:#e8e0d0;">{_clean(body)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
