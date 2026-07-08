"""Controlled top-level router for the ALETHEIA Streamlit app.

Patch 263 moves selected-page resolution and page dispatch out of app.py while
preserving the existing controlled-router behavior. This module intentionally
does not switch to Streamlit native multipage and does not own session-state
initialization, scoring, taxonomy, receipt parsing, or page-local behavior.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any


def render_controlled_router(
    st: Any,
    *,
    app_navigation_labels: Sequence[str],
    app_version: str,
    module_globals: Mapping[str, Any],
    update_protocol_state: Callable[..., dict],
    render_shared_protocol_state_notice: Callable[..., Any],
    resolve_about_header_image: Callable[[], Any],
    render_stress_test_page: Callable[[Any], Any],
    stress_test_dependency_map: Callable[[Mapping[str, Any]], Any],
    render_boundary_cases_page: Callable[..., Any],
    render_evidence_lab_page: Callable[[Any], Any],
    evidence_lab_dependency_map: Callable[[Mapping[str, Any]], Any],
    render_world_lens_page: Callable[[Any], Any],
    world_lens_dependency_map: Callable[[Mapping[str, Any]], Any],
    render_mirror_check_page: Callable[[Any], Any],
    mirror_check_dependency_map: Callable[[Mapping[str, Any]], Any],
    render_protocol_guide_page: Callable[[], Any],
    render_about_public_info_page: Callable[..., Any],
    render_receipt_reader_standard_view: Callable[[Any], Any],
    render_app_footer_banner: Callable[[str, Any], Any],
) -> str:
    """Render the current controlled router and return the selected module label.

    The selector shape, state key, label order, Receipt Reader placement, and
    dispatch targets are kept identical to the pre-Patch-263 app.py block.
    """
    # Patch 226: top-level modules use single-module conditional navigation instead of st.tabs.
    # Streamlit tabs render all tab bodies internally; that can leak inactive module content
    # into one long page after reruns. This radio keeps only the selected module rendered.
    selected_top_module = st.radio(
        "ALETHEIA module",
        app_navigation_labels,
        horizontal=True,
        label_visibility="collapsed",
        key="aletheia_active_module",
    )
    st.caption("Receipt Reader: Why ALETHEIA → Support utilities → Receipt Reader — Standard View.")

    if selected_top_module == '🚀 Stress Test':
        render_stress_test_page(stress_test_dependency_map(module_globals))

    if selected_top_module == '🧭 Boundary Cases':
        render_boundary_cases_page(
            update_protocol_state=update_protocol_state,
            render_shared_protocol_state_notice=render_shared_protocol_state_notice,
            app_version=app_version,
        )

    if selected_top_module == '📊 Evidence Lab':
        render_evidence_lab_page(evidence_lab_dependency_map(module_globals))

    if selected_top_module == '🌐 World Lens':
        render_world_lens_page(world_lens_dependency_map(module_globals))

    if selected_top_module == '🪞 Mirror Check':
        render_mirror_check_page(mirror_check_dependency_map(module_globals))

    if selected_top_module == '📜 Protocol Guide':
        render_protocol_guide_page()

    if selected_top_module == 'ℹ️ Why ALETHEIA':
        with st.container():
            render_about_public_info_page(st, header_image=resolve_about_header_image())

        st.divider()
        st.markdown("### Support utilities")
        st.info(
            "This section contains Receipt Reader — Standard View. "
            "It is intentionally kept as a read-only support utility, not a scoring surface or primary review module."
        )
        st.caption(
            "Optional reading aids that support review without becoming primary modules. "
            "They do not rescore, certify, approve, reject, enforce, or override ALETHEIA receipts."
        )
        with st.expander("Receipt Reader — Standard View", expanded=False):
            st.caption(
                "Have an ALETHEIA receipt? Upload a .txt, .md, or .json receipt file for native values "
                "and a standard review-band explanation. This utility does not rescore, certify, approve, "
                "reject, or override the original receipt."
            )
            render_receipt_reader_standard_view(st)

        render_app_footer_banner(app_version, st)

    return selected_top_module
