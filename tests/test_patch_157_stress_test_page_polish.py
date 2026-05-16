from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_157_stress_test_uses_shared_module_template() -> None:
    source = read("app.py")

    assert "from ui.module_page_template import ModulePageTemplateCopy, render_module_page_template_intro" in source
    assert 'module_name="Stress Test"' in source
    assert "Try a governance scenario under pressure" in source
    assert "scenario-pressure reading" in source
    assert "Stress Test receipts are local review artifacts" in source


def test_patch_157_stress_test_copy_keeps_stress_specific_content() -> None:
    source = read("app.py")

    expected_phrases = (
        "Power under pressure",
        "Safeguard gaps",
        "Governance stress",
        "Capture pressure",
        "Failure-mode pressure",
        "Repair needs",
        "Write one scenario as a governance pattern, not a personal accusation",
        "Use fictional roles or the Invisibility Filter",
        "Use Scan my idea for text-derived features",
        "not as proof that a person, group, or institution is good or bad",
        "ALETHEIA does not read examples by default. You lead.",
    )
    for phrase in expected_phrases:
        assert phrase in source


def test_patch_157_stress_test_polish_preserves_existing_controls() -> None:
    source = read("app.py")

    assert "render_shared_protocol_state_notice(\"Stress Test\")" in source
    assert "input_mode = st.radio" in source
    assert "Scan my idea" in source
    assert "Manual test" in source
    assert "simulation_scenario_text" in source
    assert "Invisibility Filter" in source
    assert "Run review" in source
    assert "Stress Test Batch Testing" in source


def test_patch_157_stress_test_page_polish_is_copy_layout_only() -> None:
    helper_source = read("ui/module_page_template.py")
    source = read("app.py")

    assert "full_report" not in helper_source
    assert "simulate(" not in helper_source
    assert "score_" not in helper_source
    assert "requests." not in helper_source
    assert "telemetry" not in helper_source
    assert "Global ID sync" not in helper_source
    assert "run_audit(analysis_query, manual_features" in source
