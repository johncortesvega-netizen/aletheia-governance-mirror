"""Patch 267 safe config extraction contract."""
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


def test_patch_267_creates_safe_config_modules():
    config = read("ui/config.py")
    examples = read("ui/examples.py")

    assert 'APP_VERSION = "v1.0-original-governance-mirror-p6"' in config
    assert "SUPPORTED_INPUT_LANGUAGE_NOTE" in config
    assert "English-first" in config
    assert "APP_UX_POLISH_SUMMARY" in examples
    assert "DEMO_INPUT_FILES" in examples
    assert "Sample AI policy" in examples
    assert "examples/demo_inputs/sample_ai_policy.txt" in examples


def test_app_py_imports_safe_config_without_owning_assignments():
    app = read("app.py")
    app_names = assigned_names(app)

    assert "from ui.config import APP_VERSION, SUPPORTED_INPUT_LANGUAGE_NOTE" in app
    assert "from ui.examples import APP_UX_POLISH_SUMMARY, DEMO_INPUT_FILES" in app

    extracted_names = {
        "APP_VERSION",
        "SUPPORTED_INPUT_LANGUAGE_NOTE",
        "APP_UX_POLISH_SUMMARY",
        "DEMO_INPUT_FILES",
    }
    assert extracted_names.isdisjoint(app_names)

    assert "render_controlled_router(" in app
    assert "app_version=APP_VERSION" in app
    mirror_page = read("ui/pages/mirror_check.py")
    assert "render_app_boundary_notices(SUPPORTED_INPUT_LANGUAGE_NOTE, st)" in app
    assert 'DEMO_INPUT_FILES = deps["DEMO_INPUT_FILES"]' in mirror_page
    assert "demo_input_map = dict(DEMO_INPUT_FILES)" in mirror_page


def test_behavior_sensitive_constants_remain_in_app_py_after_patch_267():
    app = read("app.py")
    app_names = assigned_names(app)

    behavior_sensitive_constants = {
        "TOTAL_9K",
        "DEMOGRAPHIC_BRACKETS",
        "WORLD_BANK_AGGREGATE_ISO3",
        "REVIEW_BAND_LABELS",
        "MISSING_SAFEGUARD_NEGATION_PATTERNS",
        "MIN_FULL_GRID_COUNTRIES",
    }
    assert behavior_sensitive_constants.issubset(app_names)

    assert "raw = group[\"population\"] / total_pop * TOTAL_9K" in app
    assert "~out[\"_iso3_norm\"].isin(WORLD_BANK_AGGREGATE_ISO3)" in app
    assert "def review_band_for_state" in app


def test_patch_267_documents_boundary_and_next_step():
    doc = read("docs/config_extraction_patch_267.md")
    summary = read("docs/config_extraction_patch_267_summary.md")
    status = read("PATCH_STATUS.md")
    notes = read("PATCH_NOTES.md")

    assert "Patch 267 — Safe Config Extraction" in doc
    assert "Patch 267 summary" in summary
    assert "No behavior-sensitive constants move" in summary
    assert "Patch 267 — Safe Config Extraction" in status
    assert "Patch 267 — Safe Config Extraction" in notes
