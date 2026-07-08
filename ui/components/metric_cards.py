from __future__ import annotations

import html

import streamlit as st


def _clean(value: object) -> str:
    """Return escaped text for small HTML cards."""
    return html.escape("" if value is None else str(value))


def metric_card(label: str, value: str, helper: str = "", *, value_is_html: bool = False, helper_is_html: bool = False) -> None:
    """Render the shared ALETHEIA metric card used across modules.

    Presentation-only helper. It must not calculate, rescore, classify, or alter
    metric values. The full-width wrapper keeps cards stable inside Streamlit
    columns after modularization.

    Most callers pass plain text and are escaped. A few legacy cards already
    build sanitized internal HTML snippets for emphasis; those callers must opt
    in explicitly with value_is_html/helper_is_html.
    """
    value_html = str(value) if value_is_html else _clean(value)
    helper_html = str(helper) if helper_is_html else _clean(helper)
    st.markdown(
        f"""
        <div class="metric-card aletheia-metric-card">
            <div class="metric-label aletheia-metric-label">{_clean(label)}</div>
            <div class="metric-value aletheia-metric-value">{value_html}</div>
            <div class="metric-help aletheia-metric-help">{helper_html}</div>
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
