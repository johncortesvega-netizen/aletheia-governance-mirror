import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_115_files_exist():
    required = [
        "app.py",
        "ui/app_shell.py",
        "tests/test_patch_115_app_shell_router_refactor_step_4.py",
        "PATCH_115_MANIFEST.txt",
        "PATCH_115_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_app_shell_has_sidebar_tuning_copy_helpers_only():
    shell = read("ui/app_shell.py")
    required = [
        "def render_sidebar_review_lens_intro",
        "def render_sidebar_review_lens_note",
        "def render_sidebar_review_rhythm_intro",
        "def render_sidebar_review_rhythm_note",
        "def render_sidebar_safety_rails_intro",
        "def render_sidebar_safety_rails_note",
        "#### Review lens",
        "This only sets the lens. ALETHEIA waits for your idea.",
        "#### Review rhythm",
        "The test keeps voices small",
        "#### Safety rails",
        "Gentle voice, firm rails",
    ]
    for phrase in required:
        assert phrase in shell

    forbidden = [
        "selectbox(",
        "slider(",
        "button(",
        "session_state",
        "WEIGHT_PRESETS",
        "requests.",
        "urllib",
    ]
    for phrase in forbidden:
        assert phrase not in shell


def test_app_imports_and_calls_sidebar_tuning_helpers_without_removing_controls():
    app = read("app.py")
    required = [
        "render_sidebar_review_lens_intro",
        "render_sidebar_review_lens_note",
        "render_sidebar_review_rhythm_intro",
        "render_sidebar_review_rhythm_note",
        "render_sidebar_safety_rails_intro",
        "render_sidebar_safety_rails_note",
        "st.selectbox(",
        "st.slider(",
        "st.button(\"Reset lens\"",
        "key=\"sidebar_weight_profile\"",
        "key=\"sidebar_steps\"",
        "key=\"sidebar_agent_voices\"",
        "key=\"sidebar_capture_sensitivity\"",
        "key=\"sidebar_alignment_floor\"",
    ]
    for phrase in required:
        assert phrase in app


def test_app_shell_and_app_parse_after_refactor():
    ast.parse(read("ui/app_shell.py"))
    ast.parse(read("app.py"))


def test_patch_115_docs_record_static_shell_extraction_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/public_trust_package.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_115_MANIFEST.txt",
            "PATCH_115_RECOVERY_NOTE.md",
        ]
    ).lower()
    required = [
        "patch 115",
        "app shell router refactor step 4",
        "static sidebar",
        "static shell extraction only",
        "interactive controls",
        "app.py",
        "no scoring",
        "no verdict-routing",
        "no signal-pattern",
        "no signal-weight",
        "no receipt schema",
        "no module-routing",
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


def test_patch_115_no_accidental_internal_notes_or_placeholders():
    changed = "\n".join(
        read(rel)
        for rel in [
            "ui/app_shell.py",
            "docs/architecture.md",
            "docs/patch_index.md",
            "PATCH_115_MANIFEST.txt",
            "PATCH_115_RECOVERY_NOTE.md",
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
