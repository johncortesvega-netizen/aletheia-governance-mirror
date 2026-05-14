from pathlib import Path
import importlib

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_unit_preview_intent_router_detects_specific_paths_before_mirror_fallback():
    preview = importlib.import_module("ui.unit_preview")
    cases = [
        ("check this AI answer for hallucination and overclaiming", "AI Integrity Mirror"),
        ("review this model response for manipulation and false authority", "AI Integrity Mirror"),
        ("upload an ALETHEIA receipt and explain the standard view", "Receipt Reader"),
        ("read this receipt file without rescoring it", "Receipt Reader"),
        ("scan this policy for privacy, telemetry, analytics, and tracking", "Privacy Audit"),
        ("does this app collect personal data or store user identifiers", "Privacy Audit"),
        ("show country-year governance integrity for the Netherlands 2024", "World Lens"),
        ("compare institutional trust and collapse probability by country", "World Lens"),
        ("stress test this governance scenario for capture pressure", "Stress Test"),
        ("pressure test this institutional decision scenario", "Stress Test"),
        ("is this a repair question or a governance claim", "Mirror Check"),
        ("check this governance text for authority drift", "Mirror Check"),
        ("what is ALETHEIA and how do I use it", "Why ALETHEIA"),
    ]
    for text, expected_module in cases:
        suggestion = preview.detect_unit_preview_route(text)
        assert expected_module in suggestion["module"]
        assert suggestion["reason"]
        assert suggestion["next_step"]
        assert suggestion["route_type"] in {"main_module", "support_utility", "guidance", "fallback"}


def test_unit_preview_rich_route_is_orientation_only_and_ui_displays_reason_and_next_step():
    unit_preview = read("ui/unit_preview.py")
    assert "def detect_unit_preview_route" in unit_preview
    assert "suggestion = detect_unit_preview_route(preview_text)" in unit_preview
    assert "Suggested path:" in unit_preview
    assert "Why:" in unit_preview
    assert "Next step:" in unit_preview
    assert "This is orientation only" in unit_preview

    # The compatibility wrapper must keep older patch checks stable.
    preview = importlib.import_module("ui.unit_preview")
    legacy = preview.suggest_review_path("System prompt for an AI model output")
    assert set(legacy) == {"path", "reason"}
    assert legacy["path"] == "AI Integrity Mirror"


def test_unit_preview_router_results_do_not_claim_authority_or_mutate_analysis_layers():
    preview = importlib.import_module("ui.unit_preview")
    samples = [
        "check this AI answer for hallucination",
        "upload an ALETHEIA receipt and explain the standard view",
        "scan this for privacy telemetry analytics and tracking",
        "show country-year governance integrity",
        "stress test this governance scenario",
        "short governance claim",
    ]
    forbidden_result_terms = [
        "certify",
        "approved",
        "rejected",
        "enforce",
        "official authority",
        "final truth",
        "legal authority",
    ]
    for sample in samples:
        result = "\n".join(preview.detect_unit_preview_route(sample).values()).lower()
        for forbidden in forbidden_result_terms:
            assert forbidden not in result

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
        "from core.scoring",
        "from core.ai_integrity_mirror",
        "from core.world_lens",
    ]
    for forbidden in forbidden_source_terms:
        assert forbidden not in source


def test_patch_142_docs_and_manifest_record_router_calibration_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_142_MANIFEST.txt",
            "PATCH_142_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "docs/patch_index.md",
            "docs/architecture.md",
        ]
    ).lower()
    for phrase in [
        "patch 142",
        "unit preview intent router calibration",
        "mirror check is the fallback",
        "ai integrity mirror",
        "receipt reader",
        "privacy audit",
        "world lens",
        "stress test",
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
        "no final-truth",
    ]:
        assert phrase in combined
