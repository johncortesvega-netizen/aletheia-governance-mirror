from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_patch_159_applies_shared_template_to_remaining_surfaces() -> None:
    source = read("app.py")

    assert 'module_name="Boundary Cases"' in source
    assert 'module_name="Evidence Lab"' in source
    assert 'module_name="World Lens"' in source
    assert source.count("render_module_page_template_intro(") >= 5


def test_patch_159_boundary_cases_keeps_edge_case_content() -> None:
    source = read("app.py")

    expected_phrases = (
        "consent pressure, free agency",
        "Consent pressure",
        "Free-agency risk",
        "Emergency drift",
        "Ambient capture",
        "Failure typing",
        "Start with one edge case and read it as a calibration reference",
        "Boundary-case notes should support later human review",
        "render_boundary_cases_intro(st)",
    )
    for phrase in expected_phrases:
        assert phrase in source


def test_patch_159_evidence_lab_keeps_evidence_specific_content() -> None:
    source = read("app.py")

    expected_phrases = (
        "Separate claims from evidence quality",
        "Evidence sufficiency",
        "Source quality",
        "Coverage gaps",
        "Evidence inflation",
        "Extraordinary-claim pressure",
        "Empirical bridge readiness",
        "unsupported or extraordinary claims as unverified",
        "Evidence status + extraordinary claim protocol",
    )
    for phrase in expected_phrases:
        assert phrase in source


def test_patch_159_world_lens_keeps_world_lens_specific_boundaries() -> None:
    source = read("app.py")

    expected_phrases = (
        "Explore selected-year country evidence",
        "Selected-year context",
        "Coverage limits",
        "Allocation context",
        "Internal taxonomy distribution",
        "Collapse-pressure patterns",
        "no Global ID, no real 9k selection",
        "Treat 9k allocation as an anti-tyranny scaffold",
        "not as ranking, certification, legitimacy judgment, or policy decision",
    )
    for phrase in expected_phrases:
        assert phrase in source


def test_patch_159_copy_layout_only_boundary() -> None:
    helper_source = read("ui/module_page_template.py")
    source = read("app.py")

    assert "full_report" not in helper_source
    assert "build_local_witness_receipt" not in helper_source
    assert "score_" not in helper_source
    assert "requests." not in helper_source
    assert "telemetry" not in helper_source
    assert "Global ID sync" not in helper_source
    assert "render_shared_protocol_state_notice(\"Boundary Cases\")" in source
    assert "render_shared_protocol_state_notice(\"Evidence Lab\")" in source
    assert "render_shared_protocol_state_notice(\"World Lens\", expanded=True)" in source
