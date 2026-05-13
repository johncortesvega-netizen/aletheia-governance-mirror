import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


EXPECTED_APP_SHELL_HELPERS = [
    "render_app_boundary_notices",
    "render_app_header",
    "render_how_to_use_note",
    "render_sidebar_brand",
    "render_sidebar_context",
    "render_sidebar_review_lens_intro",
    "render_sidebar_review_lens_note",
    "render_sidebar_review_rhythm_intro",
    "render_sidebar_review_rhythm_note",
    "render_sidebar_safety_rails_intro",
    "render_sidebar_safety_rails_note",
    "render_app_footer_banner",
]


def test_patch_117_files_exist():
    required = [
        "docs/refactor_stabilization_checkpoint.md",
        "tests/test_patch_117_refactor_stabilization_checkpoint.py",
        "PATCH_117_MANIFEST.txt",
        "PATCH_117_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_app_shell_helpers_are_present_and_imported_by_app():
    shell = read("ui/app_shell.py")
    app = read("app.py")

    for helper in EXPECTED_APP_SHELL_HELPERS:
        assert f"def {helper}" in shell
        assert helper in app

    assert "from ui.app_shell import" in app
    assert "render_app_footer_banner(APP_VERSION, st)" in app


def test_app_shell_helpers_remain_static_copy_only():
    shell = read("ui/app_shell.py")
    forbidden = [
        "selectbox(",
        "slider(",
        "button(",
        "download_button(",
        "session_state",
        "audit_ai_integrity",
        "audit_ai_integrity_artifact",
        "full_report(",
        "simulate(",
        "score_",
        "requests.",
        "urllib",
        "socket",
        "httpx",
        "Global ID sync enabled",
        "public ledger sync enabled",
    ]
    for phrase in forbidden:
        assert phrase not in shell


def test_app_still_contains_orchestrator_behavior_after_refactor_checkpoint():
    app = read("app.py")
    required = [
        "st.selectbox(",
        "st.slider(",
        "st.button(",
        "st.download_button(",
        "session_state",
        "audit_ai_integrity_artifact",
        "full_report",
        "simulate",
    ]
    for phrase in required:
        assert phrase in app


def test_patch_117_docs_record_stabilization_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "docs/refactor_stabilization_checkpoint.md",
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/public_trust_package.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_117_MANIFEST.txt",
            "PATCH_117_RECOVERY_NOTE.md",
        ]
    ).lower()
    required = [
        "patch 117",
        "refactor stabilization checkpoint",
        "ui/app_shell.py",
        "app.py",
        "orchestrator",
        "interactive controls",
        "session state",
        "module routing",
        "scoring",
        "receipts",
        "downloads",
        "no runtime behavior change",
        "no scoring",
        "no verdict-routing",
        "no signal-pattern",
        "no signal-weight",
        "no receipt schema",
        "no external calls",
        "no live model calls",
        "no telemetry",
        "no analytics",
        "no central storage",
        "no global id sync",
        "no public ledger sync",
        "no privacy guarantee",
        "no certification",
        "no enforcement",
        "no final truth",
        "humans keep the judgment",
    ]
    for phrase in required:
        assert phrase in combined


def test_patch_117_python_files_parse():
    ast.parse(read("ui/app_shell.py"))
    ast.parse(read("app.py"))


def test_patch_117_no_accidental_internal_notes_or_placeholders():
    changed = "\n".join(
        read(rel)
        for rel in [
            "docs/refactor_stabilization_checkpoint.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/public_trust_package.md",
            "PATCH_117_MANIFEST.txt",
            "PATCH_117_RECOVERY_NOTE.md",
        ]
    )
    forbidden = [
        "Ajustando",
        "afirmação",
        "Preciso",
        "Verwijderen",
        "overmatige",
        "placeholder",
        "TODO",
        "FIXME",
    ]
    for phrase in forbidden:
        assert phrase not in changed
