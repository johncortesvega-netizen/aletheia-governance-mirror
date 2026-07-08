"""Patch 266 config-extraction inventory contract.

Patch 266 prepares config/static-data extraction but intentionally does not move
runtime constants yet.
"""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def assigned_names(source: str) -> set[str]:
    tree = ast.parse(source)
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
    return names


def test_patch_266_documents_config_inventory_without_runtime_move():
    doc = read("docs/config_extraction_inventory_patch_266.md")
    summary = read("docs/config_extraction_inventory_patch_266_summary.md")

    assert "Patch 266 — Config Extraction Inventory" in doc
    assert "does **not** create `ui/config.py`" in doc
    assert "does **not** move runtime constants out of `app.py`" in doc
    assert "No runtime behavior change" in doc
    assert "Patch 267 may perform a narrow safe config extraction" in summary


def test_patch_266_classifies_safe_and_risky_config_surfaces():
    doc = read("docs/config_extraction_inventory_patch_266.md")

    safe_candidates = [
        "APP_VERSION",
        "SUPPORTED_INPUT_LANGUAGE_NOTE",
        "APP_UX_POLISH_SUMMARY",
        "DEMO_INPUT_FILES",
        "MIRROR_CHECK_DEMO_SCENARIOS",
        "STRESS_TEST_DEMO_SCENARIOS",
    ]
    risky_surfaces = [
        "TOTAL_9K",
        "DEMOGRAPHIC_BRACKETS",
        "WORLD_BANK_AGGREGATE_ISO3",
        "REVIEW_BAND_LABELS",
        "MISSING_SAFEGUARD_NEGATION_PATTERNS",
        "MIN_FULL_GRID_COUNTRIES",
        "scoring thresholds",
        "taxonomy/Z-axis boundary logic",
        "allocation denominator logic",
    ]
    for name in safe_candidates + risky_surfaces:
        assert name in doc, f"Missing config classification for {name}"

    assert "Patch 267 extraction risk" in doc
    assert "Not safe for Patch 267" in doc


def test_patch_266_recorded_no_runtime_move_at_inventory_time():
    """Patch 266 remains a historical inventory doc even after Patch 267."""
    doc = read("docs/config_extraction_inventory_patch_266.md")

    assert "does **not** create `ui/config.py`" in doc
    assert "does **not** move runtime constants out of `app.py`" in doc
    assert "Patch 267 may extract only clearly static UI/demo surfaces" in doc


def test_behavior_sensitive_constants_still_live_in_app_py_after_patch_266():
    app = read("app.py")
    names = assigned_names(app)

    behavior_sensitive_constants = {
        "TOTAL_9K",
        "DEMOGRAPHIC_BRACKETS",
        "WORLD_BANK_AGGREGATE_ISO3",
        "REVIEW_BAND_LABELS",
        "MISSING_SAFEGUARD_NEGATION_PATTERNS",
        "MIN_FULL_GRID_COUNTRIES",
    }
    assert behavior_sensitive_constants.issubset(names)

    assert "raw = group[\"population\"] / total_pop * TOTAL_9K" in app
    assert "~out[\"_iso3_norm\"].isin(WORLD_BANK_AGGREGATE_ISO3)" in app
    assert "REVIEW_BAND_LABELS" in app
    assert "def review_band_for_state" in app


def test_patch_266_updates_status_and_notes():
    status = read("PATCH_STATUS.md")
    notes = read("PATCH_NOTES.md")

    assert "Patch 266 — Config Extraction Inventory" in status
    assert "Status: READY FOR LOCAL REVIEW" in status
    assert "Patch 266 — Config Extraction Inventory" in notes
    assert "Config Extraction Inventory" in notes
