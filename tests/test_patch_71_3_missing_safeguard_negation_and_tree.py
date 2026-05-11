from __future__ import annotations

from pathlib import Path
import sys
import types

sys.modules.setdefault('streamlit', types.SimpleNamespace(secrets=types.SimpleNamespace(get=lambda *_args, **_kwargs: None)))

from core.parser import _local_governance_scan
from protocol import (
    calibrate_threshold_safeguard_metrics,
    detects_missing_safeguard_negation,
    detects_threshold_safeguard_gap,
    stress_label_for_phrase,
)

ROOT = Path(__file__).resolve().parents[1]
APP_TEXT = (ROOT / "app.py").read_text(encoding="utf-8")


TEXT = (
    "An automated welfare triage system reduces waiting times but lacks "
    "explainability, independent challenge, and human override during hardship cases."
)


def test_patch_71_3_missing_safeguard_negation_routes_to_review():
    assert detects_missing_safeguard_negation(TEXT) is True

    label, needs_review, reason = stress_label_for_phrase(TEXT)
    assert label == "Missing Safeguard Negation / Needs Safeguards"
    assert needs_review == "YES"
    assert "missing" in reason.lower() or "lacks" in reason.lower()


def test_patch_71_3_missing_safeguards_are_not_positive_local_scan_signals():
    scan = _local_governance_scan(TEXT)

    assert scan["decision_transparency"] <= 0.42
    assert scan["regulatory_presence"] <= 0.35
    assert scan["power_concentration"] >= 0.40
    assert scan["technical_complexity"] >= 0.35


def test_patch_71_3_threshold_metric_calibration_catches_lacks_patterns():
    assert detects_threshold_safeguard_gap(TEXT) is True

    sim = {
        "stability": 0.95,
        "trust_index": 1.0,
        "alignment": 1.0,
        "ego": 0.0,
        "ego_pressure": 0.0,
        "Ep": 0.0,
        "trust_trace": [1.0, 1.0],
        "alignment_trace": [1.0, 1.0],
        "ego_trace": [0.0, 0.0],
        "ego_pressure_trace": [0.0, 0.0],
    }
    calibrated = calibrate_threshold_safeguard_metrics(
        sim,
        text=TEXT,
        protocol_label="Missing Safeguard Negation / Needs Safeguards",
    )

    assert calibrated["threshold_metric_calibration"]["applied"] is True
    assert calibrated["trust_index"] <= 0.92
    assert calibrated["alignment"] <= 0.92
    assert calibrated["ego"] >= 0.05
    assert calibrated["ego_pressure"] >= 0.05


def test_patch_71_3_app_wires_bridge_override_and_tree_canopy_polish():
    assert "apply_missing_safeguard_feature_override(query, scan)" in APP_TEXT
    assert "missing_safeguard_override" in APP_TEXT
    assert "TREE_VISUAL_CANOPY_LAYER_COUNT = 8" in APP_TEXT
    assert "canopy_y_offset" in APP_TEXT
    assert "caption is explanatory" not in APP_TEXT.lower()


def test_patch_71_3_manifest_recovery_status_and_progress_are_present():
    assert (ROOT / "PATCH_71_3_MANIFEST.txt").exists()
    assert (ROOT / "PATCH_71_3_RECOVERY_NOTE.md").exists()
    assert "Patch 71.3" in (ROOT / "PATCH_STATUS.md").read_text(encoding="utf-8")
    assert "Patch 71.3" in (ROOT / "docs" / "progress_database.md").read_text(encoding="utf-8")
    manifest = (ROOT / "PATCH_71_3_MANIFEST.txt").read_text(encoding="utf-8")
    assert "app.py" in manifest
    assert "protocol.py" in manifest
    assert "core/parser.py" in manifest
    assert "tests/test_patch_71_3_missing_safeguard_negation_and_tree.py" in manifest
