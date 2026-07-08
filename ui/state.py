"""Shared Streamlit state helpers for ALETHEIA.

Patch 265 starts the state split with the safest proven surface: sidebar review
lens defaults and reset behavior. This module intentionally does not own router
selection, Unit Preview gating, Sydney Protocol self-check caching, Evidence Lab
dataframes, World Lens sync keys, Mirror Check state, Stress Test state, or batch
state.
"""
from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any

SIDEBAR_WEIGHT_PROFILE_KEY = "sidebar_weight_profile"
SIDEBAR_STEPS_KEY = "sidebar_steps"
SIDEBAR_AGENT_VOICES_KEY = "sidebar_agent_voices"
SIDEBAR_CAPTURE_SENSITIVITY_KEY = "sidebar_capture_sensitivity"
SIDEBAR_ALIGNMENT_FLOOR_KEY = "sidebar_alignment_floor"

SIDEBAR_STARTING_PRESET_LABEL = "Starting preset"
SIDEBAR_LEGACY_DEFAULT_LABEL = "Default"

SIDEBAR_LENS_DEFAULTS: dict[str, Any] = {
    SIDEBAR_WEIGHT_PROFILE_KEY: SIDEBAR_STARTING_PRESET_LABEL,
    SIDEBAR_STEPS_KEY: 40,
    SIDEBAR_AGENT_VOICES_KEY: 6,
    SIDEBAR_CAPTURE_SENSITIVITY_KEY: 0.55,
    SIDEBAR_ALIGNMENT_FLOOR_KEY: 0.45,
}


def normalize_sidebar_lens_state(session_state: MutableMapping[str, Any]) -> None:
    """Preserve the legacy sidebar profile migration from ``Default``.

    Older sessions may still contain the historical value ``Default``. The
    visible app has already migrated that value to ``Starting preset``; this
    helper keeps the same behavior while moving ownership out of ``app.py``.
    """
    if session_state.get(SIDEBAR_WEIGHT_PROFILE_KEY) == SIDEBAR_LEGACY_DEFAULT_LABEL:
        session_state[SIDEBAR_WEIGHT_PROFILE_KEY] = SIDEBAR_STARTING_PRESET_LABEL



def reset_sidebar_lens_state(session_state: MutableMapping[str, Any]) -> None:
    """Reset sidebar review-lens controls to the existing default values."""
    session_state.update(SIDEBAR_LENS_DEFAULTS)
