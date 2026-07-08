from __future__ import annotations

import html
from collections.abc import Sequence

import streamlit as st


def render_receipt_sky_panel(
    *,
    kicker: str,
    title: str,
    body: str,
    pills: Sequence[str] | None = None,
    hash_pills: Sequence[str] | None = None,
) -> None:
    """Render the shared local-receipt visual panel.

    Visual-only helper. It does not build, alter, store, publish, sync,
    validate, or authorize receipt payloads.
    """
    pills = list(pills or [])
    hash_pills = set(hash_pills or [])
    pill_html = "".join(
        f"<span class='receipt-boundary-pill{' receipt-hash-pill' if pill in hash_pills else ''}'>{html.escape(str(pill))}</span>"
        for pill in pills
    )
    st.markdown(
        f"""
        <div class="receipt-sky-panel">
          <div class="receipt-kicker">{html.escape(str(kicker))}</div>
          <div class="receipt-title">{html.escape(str(title))}</div>
          <div class="receipt-body">{html.escape(str(body))}</div>
          <div class="receipt-boundary-strip">
            {pill_html}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
