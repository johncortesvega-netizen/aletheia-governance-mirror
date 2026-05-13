from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_107_files_exist():
    required = [
        "core/boundary.py",
        "core/privacy_panel.py",
        "tests/test_patch_107_boundary_privacy_ui_wiring.py",
        "PATCH_107_MANIFEST.txt",
        "PATCH_107_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_patch_107_app_wires_existing_helpers_without_scoring_changes():
    text = read("app.py")
    required = [
        "from core.boundary import render_boundary_statement",
        "from core.privacy_panel import render_privacy_panel",
        "render_privacy_panel(st, expanded=False)",
        'render_boundary_statement("footer", st)',
    ]
    for phrase in required:
        assert phrase in text


def test_patch_107_helper_text_preserves_hosted_caveat():
    combined = read("core/boundary.py") + "\n" + read("core/privacy_panel.py") + "\n" + read("docs/BOUNDARY.md")
    required = [
        "Mirror, not throne",
        "Human judgment required",
        "local-first by design",
        "hosted deployments may have platform-level logs",
        "not a privacy guarantee",
    ]
    for phrase in required:
        assert phrase.lower() in combined.lower()


def test_patch_107_status_declares_narrow_runtime_wiring_only():
    combined = "\n".join(
        read(rel)
        for rel in [
            "PATCH_107_MANIFEST.txt",
            "PATCH_107_RECOVERY_NOTE.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
        ]
    ).lower()
    required = [
        "narrow runtime ui wiring",
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


def test_patch_107_no_accidental_internal_work_notes():
    scan_files = [
        "PATCH_107_MANIFEST.txt",
        "PATCH_107_RECOVERY_NOTE.md",
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
