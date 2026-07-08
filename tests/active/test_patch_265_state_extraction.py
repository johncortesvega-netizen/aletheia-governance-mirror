"""Patch 265 state-extraction contract.

Patch 265 creates ui/state.py, but only for the narrow sidebar review-lens
state extraction prepared by Patch 264.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_patch_265_adds_state_module_for_sidebar_lens_only():
    state = read("ui/state.py")
    doc = read("docs/state_extraction_patch_265.md")

    assert "SIDEBAR_LENS_DEFAULTS" in state
    assert "normalize_sidebar_lens_state" in state
    assert "reset_sidebar_lens_state" in state
    assert "Patch 265 — State Extraction" in doc
    assert "sidebar review-lens" in doc
    assert "Evidence Lab dataframes" in doc
    assert "Evidence/World Lens country-year sync keys" in doc


def test_sidebar_default_values_are_canonical_in_ui_state():
    from ui.state import (
        SIDEBAR_LENS_DEFAULTS,
        SIDEBAR_WEIGHT_PROFILE_KEY,
        SIDEBAR_STEPS_KEY,
        SIDEBAR_AGENT_VOICES_KEY,
        SIDEBAR_CAPTURE_SENSITIVITY_KEY,
        SIDEBAR_ALIGNMENT_FLOOR_KEY,
    )

    assert SIDEBAR_LENS_DEFAULTS[SIDEBAR_WEIGHT_PROFILE_KEY] == "Starting preset"
    assert SIDEBAR_LENS_DEFAULTS[SIDEBAR_STEPS_KEY] == 40
    assert SIDEBAR_LENS_DEFAULTS[SIDEBAR_AGENT_VOICES_KEY] == 6
    assert SIDEBAR_LENS_DEFAULTS[SIDEBAR_CAPTURE_SENSITIVITY_KEY] == 0.55
    assert SIDEBAR_LENS_DEFAULTS[SIDEBAR_ALIGNMENT_FLOOR_KEY] == 0.45


def test_sidebar_state_helpers_preserve_existing_mutation_contract():
    from ui.state import normalize_sidebar_lens_state, reset_sidebar_lens_state

    session_state = {"sidebar_weight_profile": "Default"}
    normalize_sidebar_lens_state(session_state)
    assert session_state["sidebar_weight_profile"] == "Starting preset"

    session_state.update({
        "sidebar_weight_profile": "High control risk",
        "sidebar_steps": 120,
        "sidebar_agent_voices": 3,
        "sidebar_capture_sensitivity": 0.75,
        "sidebar_alignment_floor": 0.20,
    })
    reset_sidebar_lens_state(session_state)
    assert session_state == {
        "sidebar_weight_profile": "Starting preset",
        "sidebar_steps": 40,
        "sidebar_agent_voices": 6,
        "sidebar_capture_sensitivity": 0.55,
        "sidebar_alignment_floor": 0.45,
    }


def test_app_delegates_only_sidebar_reset_state_to_ui_state():
    app = read("app.py")
    state = read("ui/state.py")

    assert "from ui.state import normalize_sidebar_lens_state, reset_sidebar_lens_state" in app
    assert "normalize_sidebar_lens_state(st.session_state)" in app
    assert "reset_sidebar_lens_state(st.session_state)" in app
    assert 'key="sidebar_weight_profile"' in app
    assert 'key="sidebar_steps"' in app
    assert 'key="sidebar_agent_voices"' in app
    assert 'key="sidebar_capture_sensitivity"' in app
    assert 'key="sidebar_alignment_floor"' in app

    forbidden_state_surfaces = [
        "empirical_master_df",
        "empirical_scored_df",
        "empirical_allocation_df",
        "aletheia_synced_iso3",
        "chat_audit_history",
        "stress_batch_summary",
        "last_scan",
        "sydney_protocol_self_check",
        "protocol_state",
        "aletheia_active_module",
        "aletheia_unit_preview_passed",
    ]
    for key in forbidden_state_surfaces:
        assert key not in state, f"Patch 265 should not move {key} into ui/state.py"


def test_patch_265_updates_status_and_notes():
    status = read("PATCH_STATUS.md")
    notes = read("PATCH_NOTES.md")

    assert "Patch 265 — State Extraction" in status
    assert "Status: READY FOR LOCAL REVIEW" in status
    assert "Patch 265 — State Extraction" in notes
    assert "ui/state.py" in notes
