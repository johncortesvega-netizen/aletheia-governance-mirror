import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_118_files_exist():
    required = [
        "ui/beginner_guide.py",
        "docs/beginner_ux.md",
        "tests/test_patch_118_beginner_ux_polish_v2.py",
        "PATCH_118_MANIFEST.txt",
        "PATCH_118_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_beginner_guide_exposes_reviewable_static_copy():
    guide = read("ui/beginner_guide.py")
    required = [
        "get_try_this_first_markdown",
        "render_try_this_first_guide",
        "First-audit checklist",
        "What this means",
        "What this does not mean",
        "Stop and review if",
        "risk reading",
        "observed reasons",
        "repair questions",
        "platform-level logs",
    ]
    for phrase in required:
        assert phrase in guide


def test_beginner_guide_is_copy_only_and_boundary_safe():
    guide = read("ui/beginner_guide.py")
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
        assert phrase not in guide

    lower = guide.lower()
    required_denials = [
        "not a verdict",
        "certification",
        "approval",
        "legal finding",
        "safety guarantee",
        "privacy guarantee",
        "compliance approval",
        "final-truth",
        "should not be used to punish",
        "run aletheia locally",
    ]
    for phrase in required_denials:
        assert phrase in lower


def test_patch_118_docs_record_beginner_polish_boundary():
    combined = "\n".join(
        read(rel)
        for rel in [
            "docs/beginner_ux.md",
            "README.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/public_trust_package.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "PATCH_118_MANIFEST.txt",
            "PATCH_118_RECOVERY_NOTE.md",
        ]
    ).lower()
    required = [
        "patch 118",
        "beginner ux polish v2",
        "first-audit checklist",
        "what this means",
        "what this does not mean",
        "stop and review",
        "rights",
        "reputation",
        "safety",
        "missing evidence",
        "legal",
        "medical",
        "political",
        "institutional",
        "financial",
        "static beginner ux copy",
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


def test_patch_118_python_files_parse():
    ast.parse(read("ui/beginner_guide.py"))
    ast.parse(read("app.py"))


def test_patch_118_no_accidental_internal_notes_or_placeholders():
    changed = "\n".join(
        read(rel)
        for rel in [
            "ui/beginner_guide.py",
            "docs/beginner_ux.md",
            "docs/architecture.md",
            "docs/patch_index.md",
            "docs/public_trust_package.md",
            "PATCH_118_MANIFEST.txt",
            "PATCH_118_RECOVERY_NOTE.md",
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
