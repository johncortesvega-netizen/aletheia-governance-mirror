from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_108_files_exist():
    required = [
        "ui/__init__.py",
        "ui/app_shell.py",
        "tests/test_patch_108_app_shell_router_refactor.py",
        "PATCH_108_MANIFEST.txt",
        "PATCH_108_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_patch_108_app_imports_and_calls_app_shell_helper():
    app = read("app.py")
    assert "from ui.app_shell import render_app_boundary_notices" in app
    assert "render_app_boundary_notices(SUPPORTED_INPUT_LANGUAGE_NOTE, st)" in app


def test_patch_108_extracted_helper_contains_only_boundary_notice_copy():
    helper = read("ui/app_shell.py")
    required = [
        "render_app_boundary_notices",
        "Input language scope",
        "Plain words",
        "Privacy by design",
        "no telemetry",
        "Hosting providers may still have their own server logs",
    ]
    for phrase in required:
        assert phrase in helper

    forbidden = [
        "simulate(",
        "full_report(",
        "audit_ai_integrity_artifact(",
        "requests.",
        "httpx.",
        "urllib.request",
        "st.session_state",
        "download_button",
    ]
    for phrase in forbidden:
        assert phrase not in helper


def test_patch_108_status_declares_router_shell_refactor_boundaries():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_108_MANIFEST.txt",
            "PATCH_108_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
        ]
    ).lower()
    required = [
        "gradual app.py router/shell refactor",
        "top-of-app boundary notices",
        "no scoring change",
        "no verdict-routing change",
        "no signal-pattern change",
        "no signal-weight change",
        "no receipt schema change",
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
        "no final truth claim",
    ]
    for phrase in required:
        assert phrase in combined


def test_patch_108_no_accidental_internal_work_notes():
    scan_files = [
        "ui/app_shell.py",
        "PATCH_108_MANIFEST.txt",
        "PATCH_108_RECOVERY_NOTE.md",
        "README.md",
        "PATCH_STATUS.md",
        "docs/progress_database.md",
    ]
    forbidden = [
        "internal repair note",
        "temporary work note",
        "placeholder button",
        "downloaded (placeholder)",
        "ajustando",
        "afirmação",
        "preciso",
        "verwijderen",
        "overmatige",
    ]
    text = "\n".join(read(rel) for rel in scan_files).lower()
    for fragment in forbidden:
        assert fragment not in text
