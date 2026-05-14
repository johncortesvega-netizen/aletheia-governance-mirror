from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_140_files_exist():
    required = [
        "docs/unit_preview_orientation_cleanup.md",
        "tests/test_patch_140_unit_preview_orientation_cleanup.py",
        "PATCH_140_MANIFEST.txt",
        "PATCH_140_RECOVERY_NOTE.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_orientation_copy_lives_on_unit_preview_not_full_app_surface():
    app = read("app.py")
    unit_preview = read("ui/unit_preview.py")

    assert "render_how_to_use_note(st)" not in app
    assert "render_try_this_first_guide(st, expanded=False)" not in app
    assert "How to use this" in unit_preview
    assert "Start here: try this first" in unit_preview
    assert "get_unit_preview_how_to_use_markdown" in unit_preview
    assert "get_unit_preview_start_here_markdown" in unit_preview


def test_unit_preview_contains_six_core_examples():
    unit_preview = read("ui/unit_preview.py")
    examples = [
        "Mirror Check:",
        "Stress Test:",
        "Boundary Cases:",
        "AI Integrity Mirror:",
        "Evidence Lab:",
        "World Lens:",
    ]
    for example in examples:
        assert example in unit_preview
    assert "evil penguin rises to power" in unit_preview
    assert "Already have an ALETHEIA receipt?" in unit_preview


def test_receipt_reader_is_support_utility_not_main_module_tab():
    app = read("app.py")
    assert "Receipt Reader — Standard View" in app
    assert "render_receipt_reader_standard_view(st)" in app
    assert "tab_receipt_reader" not in app
    assert '"Receipt Reader",' not in app

    labels_block = app.split("APP_NAVIGATION_LABELS = [", 1)[1].split("]", 1)[0]
    assert "Receipt Reader" not in labels_block


def test_core_modules_remain_in_main_navigation():
    app = read("app.py")
    labels_block = app.split("APP_NAVIGATION_LABELS = [", 1)[1].split("]", 1)[0]
    for label in [
        "Mirror Check",
        "Stress Test",
        "Boundary Cases",
        "AI Integrity Mirror",
        "Evidence Lab",
        "World Lens",
        "Protocol Guide",
        "Why ALETHEIA",
    ]:
        assert label in labels_block


def test_patch_140_boundary_preserved():
    unit_preview = read("ui/unit_preview.py").lower()

    forbidden_runtime = [
        "openai",
        "ollama",
        "embedding",
        "requests.",
        "httpx.",
        "analytics sdk",
        "global id sync",
        "public ledger sync",
        "privacy guarantee",
        "final truth claim",
    ]
    for phrase in forbidden_runtime:
        assert phrase not in unit_preview

    assert "does not score, certify" in unit_preview
    assert "readings, not verdicts" in unit_preview
    assert "human judgment remains required" in unit_preview
