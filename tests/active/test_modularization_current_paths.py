"""Current post-modularization path contracts.

Patch 257 replaces stale historical tests that searched for extracted page/UI
strings only inside app.py. The current contract is structural: app.py imports
and calls page modules; page modules and components own their extracted source.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_current_page_modules_exist_and_hold_renderers():
    expected_pages = {
        "ui/pages/mirror_check.py": [
            "def render_mirror_check_page",
            "def mirror_check_dependency_map",
        ],
        "ui/pages/stress_test.py": [
            "def render_stress_test_page",
            "def stress_test_dependency_map",
        ],
        "ui/pages/evidence_lab.py": [
            "def render_evidence_lab_page",
            "def evidence_lab_dependency_map",
        ],
        "ui/pages/world_lens.py": [
            "def render_world_lens_page",
            "def world_lens_dependency_map",
        ],
        "ui/pages/boundary_cases.py": ["def render_boundary_cases_page"],
        "ui/pages/protocol_guide.py": ["def render_protocol_guide_page"],
    }

    for relative_path, required_tokens in expected_pages.items():
        source = read(relative_path)
        for token in required_tokens:
            assert token in source, f"{token!r} missing from {relative_path}"


def test_current_component_modules_exist_and_hold_shared_renderers():
    expected_components = {
        "ui/components/semantic_pressure_panel.py": [
            "def render_semantic_pressure",
            "semantic",
        ],
        "ui/components/metric_cards.py": ["def metric_card", "def soft_card"],
        "ui/components/review_cards.py": [
            "def render_soft_card_grid",
            "def render_repair_question_cards",
            "def render_recommendation_cards",
        ],
        "ui/components/tree_visuals.py": ["def render_pulse_tree"],
        "ui/components/receipt_blocks.py": ["def render_receipt_sky_panel"],
        "ui/components/module_headers.py": [
            "def render_shared_protocol_state_notice_panel",
            "def render_module_reference_points",
        ],
    }

    for relative_path, required_tokens in expected_components.items():
        source = read(relative_path)
        for token in required_tokens:
            assert token in source, f"{token!r} missing from {relative_path}"


def test_app_py_is_orchestrator_not_page_source_container():
    app = read("app.py")

    required_imports = [
        "from ui.pages.mirror_check import mirror_check_dependency_map, render_mirror_check_page",
        "from ui.pages.stress_test import render_stress_test_page, stress_test_dependency_map",
        "from ui.pages.evidence_lab import evidence_lab_dependency_map, render_evidence_lab_page",
        "from ui.pages.world_lens import render_world_lens_page, world_lens_dependency_map",
        "from ui.pages.boundary_cases import render_boundary_cases_page",
        "from ui.pages.protocol_guide import render_protocol_guide_page",
    ]
    for token in required_imports:
        assert token in app

    required_calls = [
        "render_mirror_check_page(mirror_check_dependency_map(globals()))",
        "render_stress_test_page(stress_test_dependency_map(globals()))",
        "render_evidence_lab_page(evidence_lab_dependency_map(globals()))",
        "render_world_lens_page(world_lens_dependency_map(globals()))",
        "render_boundary_cases_page(",
        "render_protocol_guide_page()",
    ]
    for token in required_calls:
        assert token in app


def test_no_broad_page_bridge_calls_remain_for_core_pages():
    app = read("app.py")
    stale_calls = [
        "render_mirror_check_page(globals())",
        "render_stress_test_page(globals())",
        "render_evidence_lab_page(globals())",
        "render_world_lens_page(globals())",
    ]
    for token in stale_calls:
        assert token not in app


def test_modularization_audit_documents_path_contract():
    audit = read("docs/modularization_final_audit_v1.md")
    roadmap = read("docs/modularization_post_bridge_cleanup_roadmap_v1.md")

    assert "ui/pages/" in audit
    assert "ui/components/" in audit
    assert "dependency map" in audit.lower()
    assert "direct imports" in roadmap.lower()
    assert "behavior" in roadmap.lower()
