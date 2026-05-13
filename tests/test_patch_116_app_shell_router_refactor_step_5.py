import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_116_files_exist():
    required = [
        "app.py",
        "ui/app_shell.py",
        "tests/test_patch_116_app_shell_router_refactor_step_5.py",
        "PATCH_116_MANIFEST.txt",
        "PATCH_116_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_footer_banner_extracted_to_app_shell_without_behavior_code():
    shell = read("ui/app_shell.py")
    required = [
        "def render_app_footer_banner",
        "ALETHEIA reflects.",
        "People decide.",
        "footer-banner",
        "unsafe_allow_html=True",
    ]
    for phrase in required:
        assert phrase in shell

    helper_body = shell.split("def render_app_footer_banner", 1)[1]
    forbidden = [
        "selectbox(",
        "slider(",
        "button(",
        "session_state",
        "audit_ai_integrity",
        "full_report(",
        "simulate(",
        "requests.",
        "urllib",
        "socket",
    ]
    for phrase in forbidden:
        assert phrase not in helper_body


def test_app_calls_footer_helper_and_keeps_orchestrator_controls():
    app = read("app.py")
    required = [
        "render_app_footer_banner",
        "render_app_footer_banner(APP_VERSION, st)",
        "st.selectbox(",
        "st.slider(",
        "st.button(",
        "st.download_button(",
        "audit_ai_integrity_artifact",
        "full_report",
        "simulate",
    ]
    for phrase in required:
        assert phrase in app

    assert "<div class=\"footer-banner\"><strong>ALETHEIA reflects.</strong> People decide." not in app


def test_app_shell_and_app_parse_after_patch_116():
    ast.parse(read("ui/app_shell.py"))
    ast.parse(read("app.py"))


def test_patch_116_docs_record_static_shell_extraction_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/public_trust_package.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_116_MANIFEST.txt",
            "PATCH_116_RECOVERY_NOTE.md",
        ]
    ).lower()
    required = [
        "patch 116",
        "app shell router refactor step 5",
        "footer banner",
        "static shell extraction only",
        "app.py",
        "interactive controls",
        "session state",
        "module routing",
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


def test_patch_116_no_accidental_internal_notes_or_placeholders():
    changed = "\n".join(
        read(rel)
        for rel in [
            "ui/app_shell.py",
            "docs/architecture.md",
            "docs/patch_index.md",
            "PATCH_116_MANIFEST.txt",
            "PATCH_116_RECOVERY_NOTE.md",
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
