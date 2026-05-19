"""Shared module-page layout helpers for ALETHEIA.

Patch 155 introduces a reusable page-like module template as a scaffold for
future UI polish. The helpers are copy/layout only: they do not call scoring
engines, route verdicts, create receipts, inspect uploads, store data, or contact
external services.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence


MODULE_PAGE_TEMPLATE_BOUNDARY_NOTE = (
    "This module gives a structured AI Patrol stop/go review signal, not a verdict, certification, "
    "approval, legal/medical/political finding, safety guarantee, or final-truth "
    "claim. Human review remains required."
)


MODULE_PAGE_TEMPLATE_SECTION_TITLES: tuple[str, ...] = (
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


@dataclass(frozen=True)
class ModulePageTemplateCopy:
    """Copy bundle for a future page-like module surface.

    This dataclass is intentionally presentation-only. It lets later patches
    give Mirror Check, Stress Test, Receipt Reader, Evidence Lab, and World Lens
    a shared calm structure while preserving each module's
    inherent content and engine behavior.
    """

    module_name: str
    purpose: str
    looks_for: Sequence[str] = field(default_factory=tuple)
    safe_first_path: Sequence[str] = field(default_factory=tuple)
    input_guidance: str = "Paste or upload only the material this module is meant to review."
    result_guidance: str = "Read the module output as a mirror reading before relying on it."
    observed_reasons_guidance: str = "Inspect the visible reasons and evidence signals before acting."
    repair_questions_guidance: str = "Use repair questions as prompts for human review and better evidence."
    receipt_guidance: str = "Export a receipt only when you want a local review record."
    boundary_note: str = MODULE_PAGE_TEMPLATE_BOUNDARY_NOTE


def get_module_page_template_sections() -> tuple[str, ...]:
    """Return the stable shared section order for page-like modules."""
    return MODULE_PAGE_TEMPLATE_SECTION_TITLES


def get_module_page_template_boundary_note() -> str:
    """Return the standard non-authority boundary note for module pages."""
    return MODULE_PAGE_TEMPLATE_BOUNDARY_NOTE


def _markdown_bullets(values: Iterable[str]) -> str:
    """Format a small bullet list for static module-page copy."""
    cleaned = [str(value).strip() for value in values if str(value).strip()]
    if not cleaned:
        return "- Review the module-specific guidance before continuing."
    return "\n".join(f"- {value}" for value in cleaned)


def get_module_page_template_markdown(copy: ModulePageTemplateCopy) -> str:
    """Build a static markdown scaffold for a page-like module.

    The returned markdown is documentation/UI copy only. It does not contain
    executable module logic and should not be treated as a receipt or reading.
    """
    return f"""## {copy.module_name}

### Plain-language purpose
{copy.purpose}

### What this module looks for
{_markdown_bullets(copy.looks_for)}

### Safe first path
{_markdown_bullets(copy.safe_first_path)}

### Input area
{copy.input_guidance}

### Result / mirror reading
{copy.result_guidance}

### Observed reasons
{copy.observed_reasons_guidance}

### Repair questions
{copy.repair_questions_guidance}

### Receipt / export
{copy.receipt_guidance}

### Boundary note
{copy.boundary_note}
""".strip()


def render_module_page_template_intro(container, copy: ModulePageTemplateCopy) -> None:
    """Render the shared page-like intro for a module.

    ``container`` may be ``st`` or any Streamlit-like container exposing
    ``markdown`` and ``expander``. The helper only renders copy; it is not wired
    into active modules by Patch 155.
    """
    container.markdown(f"## {copy.module_name}")
    container.markdown(f"**Plain-language purpose:** {copy.purpose}")

    with container.expander("What this module looks for", expanded=False):
        container.markdown(_markdown_bullets(copy.looks_for))

    with container.expander("Safe first path", expanded=False):
        container.markdown(_markdown_bullets(copy.safe_first_path))

    container.markdown(f"**Input area:** {copy.input_guidance}")
    container.markdown(f"**Result / mirror reading:** {copy.result_guidance}")
    container.markdown(f"**Observed reasons:** {copy.observed_reasons_guidance}")
    container.markdown(f"**Repair questions:** {copy.repair_questions_guidance}")
    container.markdown(f"**Receipt / export:** {copy.receipt_guidance}")
    container.caption(copy.boundary_note)
