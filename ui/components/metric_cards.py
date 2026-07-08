from __future__ import annotations

import html

import streamlit as st


def _clean(value: object) -> str:
    """Return escaped text for small HTML cards."""
    return html.escape("" if value is None else str(value))


def metric_card(label: str, value: str, helper: str = "") -> None:
    """Render the shared ALETHEIA metric card used across modules.

    Presentation-only helper. It must not calculate, rescore, classify, or alter
    metric values. The full-width wrapper keeps cards stable inside Streamlit
    columns after modularization.
    """
    st.markdown(
        f"""
        <div class="metric-card aletheia-metric-card">
            <div class="metric-label aletheia-metric-label">{_clean(label)}</div>
            <div class="metric-value aletheia-metric-value">{_clean(value)}</div>
            <div class="metric-help aletheia-metric-help">{_clean(helper)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def soft_card(title: str, body: str) -> None:
    """Render the shared soft explanatory card used in result summaries.

    Presentation-only helper. Long result text is deliberately wrapped inside
    the parent column/container instead of forcing narrow overflow.
    """
    st.markdown(
        f"""
        <div class="soft-card aletheia-soft-card">
            <div class="aletheia-soft-title">{_clean(title)}</div>
            <div class="aletheia-soft-body">{_clean(body)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
