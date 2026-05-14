from pathlib import Path
import importlib

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_unit_preview_routes_scenario_shaped_inputs_to_stress_test_before_fallback():
    preview = importlib.import_module("ui.unit_preview")
    cases = [
        "an evil penguin rises to power after a revolution",
        "an evil penguin rises to power after a revolution and removes appeal rights",
        "a city uses an AI system to decide who receives housing support",
        "a hospital AI recommends care but no human doctor can override it",
        "an agency removes appeal rights after a crisis",
        "a platform controls access to public services",
    ]
    for text in cases:
        suggestion = preview.detect_unit_preview_route(text)
        assert suggestion["module"] == "Stress Test"
        assert suggestion["route_type"] == "main_module"
        assert "scenario" in suggestion["reason"].lower() or "pressure-test" in suggestion["reason"].lower()


def test_unit_preview_keeps_specific_routes_and_mirror_check_fallback_after_scenario_hotfix():
    preview = importlib.import_module("ui.unit_preview")
    cases = [
        ("check this AI answer for hallucination and overclaiming", "AI Integrity Mirror"),
        ("upload an ALETHEIA receipt and explain the standard view", "Receipt Reader"),
        ("scan this policy for privacy telemetry analytics and tracking", "Privacy Audit"),
        ("show country-year governance integrity for the Netherlands 2024", "World Lens"),
        ("is this a repair question or a governance claim", "Mirror Check"),
        ("check this governance text for authority drift", "Mirror Check"),
    ]
    for text, expected_module in cases:
        suggestion = preview.detect_unit_preview_route(text)
        assert expected_module in suggestion["module"]


def test_unit_preview_buttons_are_compact_row_above_reference_previews():
    source = read("ui/unit_preview.py")
    assert "action_columns = container.columns(2)" in source
    assert "container.columns([1, 1, 6], gap=\"small\")" in source
    assert source.index("Preview review path") < source.index("render_unit_preview_html_reference(container)")
    assert source.index("Proceed to ALETHEIA") < source.index("render_unit_preview_html_reference(container)")
    assert "Suggested path:" in source
    assert "Why:" in source
    assert "Next step:" in source


def test_unit_preview_scenario_hotfix_is_orientation_only():
    source = read("ui/unit_preview.py").lower()
    forbidden_source_terms = [
        "requests.",
        "httpx.",
        "urllib",
        "socket",
        "openai",
        "ollama",
        "embedding",
        "download_button",
        "file_uploader",
        "full_report(",
        "simulate(",
        "audit_ai_integrity",
        "scan_privacy_boundary_static",
        "build_local_witness_receipt",
        "render_local_witness_receipt_text",
    ]
    for forbidden in forbidden_source_terms:
        assert forbidden not in source

    preview = importlib.import_module("ui.unit_preview")
    result = "\n".join(preview.detect_unit_preview_route("an evil penguin rises to power after a revolution").values()).lower()
    for forbidden in [
        "certify",
        "approved",
        "rejected",
        "enforce",
        "official authority",
        "final truth",
        "legal authority",
    ]:
        assert forbidden not in result


def test_patch_142_2_docs_capture_scenario_router_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_142_2_MANIFEST.txt",
            "PATCH_142_2_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "docs/patch_index.md",
            "docs/architecture.md",
        ]
    ).lower()
    for phrase in [
        "patch 142.2",
        "unit preview scenario intent hotfix",
        "scenario-shaped",
        "stress test",
        "mirror check fallback",
        "evil penguin",
        "compact button row",
        "no scoring",
        "no verdict routing",
        "no receipt schema",
        "no receipt generation",
        "no ai integrity scan behavior",
        "no privacy audit scan behavior",
        "no world lens math",
        "no external calls",
        "no telemetry",
        "no analytics",
        "no certification",
        "human review remains required",
    ]:
        assert phrase in combined
