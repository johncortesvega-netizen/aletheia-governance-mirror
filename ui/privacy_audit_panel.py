"""Privacy Boundary Audit Panel renderer for ALETHEIA.

Patch 112 moves the already-existing Privacy Boundary Audit Panel display into
one reviewable UI helper. The underlying static audit remains in
``core.ai_integrity_mirror.scan_privacy_boundary_static``. This module only
renders supplied audit data; it does not scan repositories, monitor runtime behavior, call external services, certify privacy, or change scoring/receipts.
"""
from __future__ import annotations

from typing import Any


def _row_for_detection(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "Category": item.get("category"),
        "Signal": item.get("name"),
        "Severity": item.get("severity"),
        "Why it matters": item.get("description"),
    }


def render_privacy_boundary_audit_panel(privacy_boundary_audit: dict[str, Any] | None, container=None) -> None:
    """Render a static privacy-boundary audit result.

    The panel presents review prompts and visible evidence snippets from an
    already-built audit dictionary. It intentionally avoids repository crawling,
    host-log inspection, runtime monitoring, external calls, and privacy or
    compliance guarantees.
    """
    if not privacy_boundary_audit:
        return

    if container is None:
        import streamlit as st  # type: ignore

        container = st

    import pandas as pd  # type: ignore

    container.markdown("#### Privacy Boundary Audit Panel")
    container.caption(privacy_boundary_audit.get("scope_note"))
    container.caption(privacy_boundary_audit.get("non_certification_note"))
    pcols = container.columns(4)
    pcols[0].metric("Privacy detections", privacy_boundary_audit.get("detection_count", 0))
    pcols[1].metric("Active signals", privacy_boundary_audit.get("active_signal_count", 0))
    pcols[2].metric("Local-only stated", "Yes" if privacy_boundary_audit.get("local_only_statement_present") else "No")
    pcols[3].metric("Boundary tension", "Yes" if privacy_boundary_audit.get("privacy_boundary_tension") else "No")
    container.info(privacy_boundary_audit.get("local_only_statement"))
    container.warning(privacy_boundary_audit.get("hosting_caveat"))

    privacy_detections = privacy_boundary_audit.get("detections", []) or []
    if privacy_detections:
        privacy_rows = [_row_for_detection(item) for item in privacy_detections]
        container.dataframe(pd.DataFrame(privacy_rows), use_container_width=True, hide_index=True)
        with container.expander("Privacy evidence snippets — static boundary audit", expanded=False):
            for item in privacy_detections:
                snippets = item.get("evidence_snippets", []) or []
                if snippets:
                    container.write(f"**{item.get('category')} · {item.get('name')}**")
                    for snippet in snippets:
                        container.code(snippet, language="text")
        with container.expander("Privacy boundary review questions", expanded=True):
            for question in privacy_boundary_audit.get("review_questions", [])[:7]:
                container.info(question)
    else:
        container.caption(
            "No privacy-boundary trigger was detected by this static audit. "
            "This is not a privacy guarantee, compliance approval, hosting audit, or proof that no data is collected."
        )
