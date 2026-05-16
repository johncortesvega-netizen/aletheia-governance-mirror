from pathlib import Path

from ui.module_page_template import (
    MODULE_PAGE_TEMPLATE_BOUNDARY_NOTE,
    ModulePageTemplateCopy,
    get_module_page_template_boundary_note,
    get_module_page_template_markdown,
    get_module_page_template_sections,
)


ROOT = Path(__file__).resolve().parents[1]


def test_patch_155_shared_section_order_is_stable():
    sections = get_module_page_template_sections()
    assert sections == (
        "Plain-language purpose",
        "What this module looks for",
        "Safe first path",
        "Input area",
        "Result / mirror reading",
        "Observed reasons",
        "Repair questions",
        "Receipt / export",
        "Boundary note",
    )


def test_patch_155_boundary_note_preserves_non_authority_language():
    note = get_module_page_template_boundary_note()
    assert note == MODULE_PAGE_TEMPLATE_BOUNDARY_NOTE
    for phrase in (
        "not a verdict",
        "certification",
        "legal/medical/political finding",
        "final-truth claim",
        "Human review remains required",
    ):
        assert phrase in note


def test_patch_155_markdown_scaffold_keeps_module_specific_content():
    copy = ModulePageTemplateCopy(
        module_name="Mirror Check",
        purpose="Review one short item for pressure signals.",
        looks_for=("authority drift", "evidence gaps"),
        safe_first_path=("Paste one short item.", "Read observed reasons before relying on it."),
    )
    markdown = get_module_page_template_markdown(copy)
    assert "## Mirror Check" in markdown
    assert "### Plain-language purpose" in markdown
    assert "Review one short item for pressure signals." in markdown
    assert "- authority drift" in markdown
    assert "- evidence gaps" in markdown
    assert "- Paste one short item." in markdown
    assert "not a verdict" in markdown


def test_patch_155_template_helper_import_contract_is_stable():
    source = (ROOT / "ui" / "module_page_template.py").read_text(encoding="utf-8")
    assert "class ModulePageTemplateCopy" in source
    assert "def render_module_page_template_intro" in source
    assert 'container.expander("What this module looks for"' in source
    assert 'container.expander("Safe first path"' in source


def test_patch_155_helper_is_copy_layout_only():
    source = (ROOT / "ui" / "module_page_template.py").read_text(encoding="utf-8")
    forbidden_runtime_hooks = (
        "full_report",
        "score_",
        "create_receipt",
        "generate_receipt",
        "requests.",
        "telemetry",
        "analytics",
        "database",
        "public ledger",
        "Global ID sync",
    )
    for token in forbidden_runtime_hooks:
        assert token not in source
    assert "import streamlit" not in source


def test_patch_155_documentation_records_patch_boundary():
    doc = (ROOT / "docs" / "module_page_template.md").read_text(encoding="utf-8")
    assert "Patch 155" in doc
    assert "layout/copy scaffold only" in doc
    assert "does not wire the template into active modules" in doc
    assert "No scoring changes" in doc
    assert "No verdict-routing changes" in doc
    assert "Human review remains required" in doc
