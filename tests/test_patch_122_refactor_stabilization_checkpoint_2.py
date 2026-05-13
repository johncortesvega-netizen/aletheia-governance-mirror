import ast
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


HELPERS = {
    "ui.app_shell": [
        "render_app_boundary_notices",
        "render_app_header",
        "render_how_to_use_note",
        "render_app_footer_banner",
    ],
    "ui.module_intro": [
        "render_stress_test_scan_intro",
        "render_boundary_cases_intro",
        "render_consent_audit_intro",
    ],
    "ui.status_cards": [
        "render_ai_integrity_boundary_cards",
    ],
    "ui.beginner_guide": [
        "render_try_this_first_guide",
    ],
    "ui.privacy_audit_panel": [
        "render_privacy_boundary_audit_panel",
    ],
}


def test_patch_122_files_exist():
    required = [
        "docs/refactor_stabilization_checkpoint_2.md",
        "tests/test_patch_122_refactor_stabilization_checkpoint_2.py",
        "PATCH_122_MANIFEST.txt",
        "PATCH_122_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_ui_helpers_import_and_expose_expected_functions():
    for module_name, function_names in HELPERS.items():
        module = importlib.import_module(module_name)
        for function_name in function_names:
            assert hasattr(module, function_name), f"{module_name}.{function_name}"
            assert callable(getattr(module, function_name))


def test_app_py_imports_and_calls_current_ui_helpers():
    app = read("app.py")
    expected = [
        "from ui.app_shell import",
        "from ui.beginner_guide import render_try_this_first_guide",
        "from ui.module_intro import render_boundary_cases_intro, render_consent_audit_intro, render_stress_test_scan_intro",
        "from ui.privacy_audit_panel import render_privacy_boundary_audit_panel",
        "from ui.status_cards import render_ai_integrity_boundary_cards",
        "render_app_boundary_notices(st)",
        "render_app_header(APP_VERSION, st)",
        "render_how_to_use_note(st)",
        "render_try_this_first_guide(st)",
        "render_stress_test_scan_intro(st)",
        "render_boundary_cases_intro(st)",
        "render_consent_audit_intro(st)",
        "render_ai_integrity_boundary_cards(st)",
        "render_app_footer_banner(APP_VERSION, st)",
    ]
    for phrase in expected:
        assert phrase in app


def test_app_py_remains_runtime_orchestrator():
    app = read("app.py")
    required = [
        "st.selectbox(",
        "st.slider(",
        "st.button(",
        "st.download_button(",
        "session_state",
        "full_report",
        "simulate",
        "audit_ai_integrity_artifact",
        "scan_privacy_boundary_static",
    ]
    for phrase in required:
        assert phrase in app


def test_ui_helpers_do_not_contain_runtime_or_network_logic():
    helper_text = "\n".join(
        read(rel)
        for rel in [
            "ui/app_shell.py",
            "ui/module_intro.py",
            "ui/status_cards.py",
            "ui/beginner_guide.py",
            "ui/privacy_audit_panel.py",
        ]
    )
    forbidden = [
        "st.selectbox(",
        "st.slider(",
        "st.button(",
        "st.download_button(",
        "session_state[",
        ".session_state",
        "full_report(",
        "simulate(",
        "audit_ai_integrity(",
        "audit_ai_integrity_artifact(",
        "scan_privacy_boundary_static(",
        "build_local_witness_receipt(",
        "render_local_witness_receipt_text(",
        "requests.",
        "httpx",
        "urllib",
        "socket",
        "openai",
    ]
    for phrase in forbidden:
        assert phrase not in helper_text


def test_patch_122_docs_record_checkpoint_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "docs/refactor_stabilization_checkpoint_2.md",
            "PATCH_122_MANIFEST.txt",
            "PATCH_122_RECOVERY_NOTE.md",
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/progress_database.md",
            "PATCH_STATUS.md",
        ]
    ).lower()
    required = [
        "patch 122",
        "refactor stabilization checkpoint 2",
        "app.py",
        "orchestrator",
        "ui/app_shell.py",
        "ui/module_intro.py",
        "ui/status_cards.py",
        "copy",
        "no runtime behavior change",
        "no scoring",
        "no verdict-routing",
        "no signal-pattern",
        "no signal-weight",
        "no receipt schema",
        "no module-routing",
        "no external calls",
        "no telemetry",
        "no analytics",
        "no storage",
        "no privacy guarantee",
        "no certification",
        "no enforcement",
        "no final truth",
        "humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in combined


def test_patch_122_no_authority_claims_or_repair_notes():
    changed = "\n".join(
        read(rel)
        for rel in [
            "docs/refactor_stabilization_checkpoint_2.md",
            "PATCH_122_MANIFEST.txt",
            "PATCH_122_RECOVERY_NOTE.md",
        ]
    ).lower()
    forbidden = [
        "guarantees privacy",
        "privacy guaranteed",
        "certifies privacy",
        "certifies safety",
        "final truth guaranteed",
        "automatic enforcement",
        "placeholder",
        "todo",
        "fixme",
        "ajustando",
        "afirma",
        "preciso",
        "verwijderen",
        "overmatige",
    ]
    for phrase in forbidden:
        assert phrase not in changed


def test_patch_122_python_files_parse():
    for rel in [
        "app.py",
        "ui/app_shell.py",
        "ui/module_intro.py",
        "ui/status_cards.py",
        "ui/beginner_guide.py",
        "ui/privacy_audit_panel.py",
        "tests/test_patch_122_refactor_stabilization_checkpoint_2.py",
    ]:
        ast.parse(read(rel))
