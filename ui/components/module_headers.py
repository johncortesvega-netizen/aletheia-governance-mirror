from __future__ import annotations

from collections.abc import Mapping, Sequence

import pandas as pd
import streamlit as st


def render_shared_protocol_state_notice_panel(
    *,
    current_mode: str,
    state: Mapping[str, object],
    expanded: bool = False,
) -> None:
    """Render the shared protocol-state notice and details table.

    UI-only helper. The caller remains responsible for computing/updating the
    shared protocol state. This component does not mutate scoring, routing,
    receipts, evidence data, or session-state values.
    """
    st.info(
        "**Shared Protocol State** — Mirror Check, Stress Test, Boundary Cases, Evidence Lab, and World Lens are different windows into the same protocol heart. "
        "Changes to empirical evidence, scoring calibration, the Sydney Protocol overlay, doctrine thresholds, or the selected evidence year may echo across modes. "
        "That is intentional shared-state behavior, not an error. Scenario-only controls stay local unless you explicitly apply them to the shared protocol state."
    )
    with st.expander("Shared state details", expanded=expanded):
        rows = [
            ("Current mode", state.get("current_mode", current_mode)),
            ("Empirical master active", "Yes" if state.get("empirical_master_active") else "No"),
            ("Scored evidence active", "Yes" if state.get("scored_evidence_active") else "No"),
            ("Trust calibration active", "Yes" if state.get("trust_calibration_active") else "No"),
            ("WGI active", "Yes" if state.get("wgi_active") else "No"),
            ("V-Dem active", "Yes" if state.get("vdem_active") else "No"),
            ("Demo data active", "Yes" if state.get("synthetic_demo_active") else "No"),
            ("Sydney Protocol overlay active", "Yes" if state.get("sydney_protocol_overlay_active") else "No"),
            ("Selected evidence year", state.get("selected_evidence_year", "—")),
            ("Selected case / scenario", state.get("selected_context", "—")),
            ("Evidence basis", state.get("grid_basis", "—")),
            ("Last protocol update source", state.get("last_update_source", "—")),
        ]
        st.dataframe(pd.DataFrame(rows, columns=["State field", "Value"]), use_container_width=True, hide_index=True)


def render_module_reference_points(points: Sequence[str], *, title: str = "Module reference points") -> None:
    """Render compact review bullets for module intro/guide sections.

    UI-only helper for later page extraction.
    """
    clean_points = [str(point).strip() for point in points if str(point).strip()]
    if not clean_points:
        return
    with st.expander(title, expanded=False):
        for point in clean_points:
            st.markdown(f"- {point}")
