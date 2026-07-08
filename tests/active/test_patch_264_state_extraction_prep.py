"""Patch 264 state-extraction prep contract.

Patch 264 maps Streamlit session-state ownership before Patch 265 creates a
state module. It intentionally does not move runtime state code.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_patch_264_documents_state_extraction_prep_without_runtime_move():
    doc = read("docs/state_extraction_prep_patch_264.md")

    assert "Patch 264 — State Extraction Prep" in doc
    assert "does **not** create `ui/state.py`" in doc
    assert "does **not** move any runtime state code" in doc
    assert "No runtime state movement" in doc
    # Patch 264 was a prep-only boundary. Patch 265 is allowed to create
    # ui/state.py for the narrow extraction documented in Patch 264.
    assert "Patch 265 may create `ui/state.py`" in read("docs/state_extraction_prep_patch_264_summary.md")


def test_patch_264_maps_state_areas_and_lifecycle_risk():
    doc = read("docs/state_extraction_prep_patch_264.md")

    required_state_areas = [
        "Unit Preview gate",
        "Router selection",
        "Sydney Protocol self-check",
        "Sidebar review lens",
        "Shared protocol substrate",
        "Evidence Lab core dataframes",
        "Evidence/World Lens sync",
        "Mirror Check chat state",
        "Mirror Check batch state",
        "Stress Test current result",
        "Stress Test batch state",
    ]
    for area in required_state_areas:
        assert area in doc

    assert "Patch 265 extraction risk" in doc
    assert "cross-page country/year synchronization" in doc
    assert "fail-closed behavior must not drift" in doc


def test_patch_264_preserves_known_state_key_contracts_in_inventory():
    doc = read("docs/state_extraction_prep_patch_264.md")

    required_keys = [
        "aletheia_active_module",
        "aletheia_unit_preview_passed",
        "sydney_protocol_self_check",
        "sidebar_weight_profile",
        "sidebar_steps",
        "sidebar_agent_voices",
        "sidebar_capture_sensitivity",
        "sidebar_alignment_floor",
        "protocol_state",
        "empirical_master_df",
        "empirical_scored_df",
        "empirical_allocation_df",
        "empirical_active_scoring_signature",
        "aletheia_synced_iso3",
        "aletheia_synced_country_name",
        "aletheia_synced_evidence_year",
        "chat_audit_history",
        "audit_chat_query",
        "audit_batch_summary",
        "last_query",
        "last_scan",
        "last_sim",
        "last_report",
        "stress_batch_summary",
    ]
    for key in required_keys:
        assert key in doc, f"Missing state key from Patch 264 inventory: {key}"


def test_current_runtime_state_still_lives_in_existing_owners_after_patch_264():
    app = read("app.py")
    main = read("ui/main.py")
    evidence_lab = read("ui/pages/evidence_lab.py")
    mirror_check = read("ui/pages/mirror_check.py")
    stress_test = read("ui/pages/stress_test.py")

    assert 'key="aletheia_active_module"' in main
    state = read("ui/state.py")
    assert "reset_sidebar_lens_state" in state
    assert "SIDEBAR_STEPS_KEY: 40" in state
    assert 'st.session_state["protocol_state"] = state' in app
    assert 'st.session_state["empirical_master_df"]' in evidence_lab
    assert 'st.session_state["chat_audit_history"]' in mirror_check or "st.session_state.chat_audit_history" in mirror_check
    assert 'st.session_state.last_query' in stress_test or 'st.session_state.get("last_query"' in stress_test


def test_patch_264_next_patch_boundary_is_narrow():
    summary = read("docs/state_extraction_prep_patch_264_summary.md")

    assert "No runtime behavior changes" in summary
    assert "Patch 265 may create `ui/state.py`" in summary
    assert "small proven extraction" in summary
    assert "sidebar defaults/reset helpers" in summary
    assert "Evidence/World Lens sync state" in summary
