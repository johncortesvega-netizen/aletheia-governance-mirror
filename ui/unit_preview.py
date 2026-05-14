"""Aletheia Unit Preview front-door helper.

The preview suggests where to begin before the full app opens. It does not
score, route modules, create receipts, inspect files, or call module engines.
"""
from __future__ import annotations

import re
from pathlib import Path


UNIT_PREVIEW_SESSION_KEY = "aletheia_unit_preview_passed"


def get_unit_preview_boundary_text() -> str:
    """Return the stable non-authority boundary copy for the preview."""
    return (
        "Aletheia Unit Preview suggests where to begin. It does not score, certify, "
        "approve, reject, or replace the full modules.\n\n"
        "ALETHEIA gives readings, not verdicts. Human judgment remains required.\n\n"
        "For sensitive material, run locally. Hosted deployments may have platform-level "
        "logs outside ALETHEIA's app-code boundary."
    )


def get_unit_preview_how_to_use_markdown() -> str:
    """Return the front-door orientation copy and examples."""
    return """
**How to use this**

Paste a short idea, question, receipt, policy, AI output, or scenario. ALETHEIA looks for power, pressure, appeal, evidence, and risk. You keep the final say.

**Examples**

- **Mirror Check:** A city wants to use an AI tool to decide who receives housing support.
- **Stress Test:** An evil penguin rises to power after a revolution and removes appeal rights.
- **Boundary Cases:** A hospital AI recommends care, but no human doctor can override it.
- **AI Integrity Mirror:** An AI assistant claims it can certify whether a policy is ethical.
- **Evidence Lab:** Upload a CSV or source note to compare claims against supporting evidence.
- **World Lens:** Compare a country-year governance context before interpreting a risk reading.

Already have an ALETHEIA receipt? Use **Receipt Reader — Standard View** after entering ALETHEIA.
"""


def get_unit_preview_start_here_markdown() -> str:
    """Return the first-use checklist for the front door."""
    return """
**A safe first path**

1. Paste one short item into Unit Preview.
2. Read the suggested path as a suggestion, not a decision.
3. Enter ALETHEIA and choose the module yourself.
4. Inspect observed reasons, values, and repair questions before relying on any reading.
5. Download a receipt only when you want a local review record.

**Stop and review if**

- the result could affect rights, access, reputation, safety, or institutional action;
- source evidence is missing, stale, unclear, or one-sided;
- the text involves legal, medical, political, institutional, or financial consequences;
- you cannot explain the receipt in plain language to another reviewer.
"""


def get_unit_preview_html_files(project_root: Path | None = None) -> list[tuple[str, Path]]:
    """Return packaged HTML preview files for the Unit Preview hook page."""
    root = project_root or Path(__file__).resolve().parents[1]
    candidates = [
        ("Sydney Protocol v3.2", root / "Sydney_Protocol_v3.2.html"),
        ("GPA v8.2", root / "GPA_v8.2.html"),
    ]
    return [(title, path) for title, path in candidates if path.exists()]


def render_unit_preview_html_reference(container=None, project_root: Path | None = None) -> None:
    """Render packaged HTML previews side by side when present.

    This stays on the Unit Preview hook page and uses packaged local files only.
    Missing files are ignored calmly.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    html_files = get_unit_preview_html_files(project_root)
    if not html_files:
        return

    container.markdown("### Reference previews")
    container.caption("Packaged local HTML references. These are orientation aids, not final authority.")
    import streamlit.components.v1 as components  # type: ignore

    columns = container.columns(len(html_files))
    for index, ((title, path), column) in enumerate(zip(html_files, columns), start=1):
        with column:
            column.markdown(f"**{title}**")
            column.caption(f"Local file: `{path.name}`")
            html_text = path.read_text(encoding="utf-8", errors="ignore")
            components.html(html_text, height=420, scrolling=True)


def suggest_review_path(text: str) -> dict[str, str]:
    """Suggest a starting path using transparent local keyword rules."""
    value = (text or "").strip()
    lowered = value.lower()

    if not value:
        return {
            "path": "Mirror Check",
            "reason": "No preview text was provided. Mirror Check is the calm default starting point.",
        }

    if any(token in lowered for token in ["receipt fingerprint", "processed document fingerprint", "app version:", "rubric version:", "receipt"]):
        return {
            "path": "Receipt Reader - Standard View",
            "reason": "The text looks like a receipt or receipt excerpt.",
        }

    if any(token in lowered for token in ["model output", "prompt", "system prompt", "agent", "llm", "code", "```", "function ", "def ", "class "]):
        return {
            "path": "AI Integrity Mirror",
            "reason": "The text looks like AI, prompt, model-output, agent, or code material.",
        }

    if any(token in lowered for token in ["scenario", "stress", "pressure", "simulate", "under pressure", "what if", "capture risk"]):
        return {
            "path": "Stress Test",
            "reason": "The text looks like a scenario or governance pressure case.",
        }

    if any(token in lowered for token in ["evidence", "csv", "dataset", "source", "upload", "documentation", "documented"]):
        return {
            "path": "Evidence Lab",
            "reason": "The text points toward evidence, sources, datasets, uploads, or documentation.",
        }

    if any(token in lowered for token in ["country", "year", "governance context", "population", "world lens", "wgi", "v-dem"]):
        return {
            "path": "World Lens",
            "reason": "The text mentions country/year or governance context comparison.",
        }

    if "?" in value or any(token in lowered for token in ["review", "audit", "should i", "how do i", "can you check", "is this"]):
        return {
            "path": "Mirror Check / Question Review",
            "reason": "The text asks for review or audit guidance rather than describing a full scenario.",
        }

    return {
        "path": "Mirror Check",
        "reason": "Mirror Check is the default starting point for short governance text, claims, or proposals.",
    }


def render_unit_preview(container=None) -> bool:
    """Render the Unit Preview and return True when the user proceeds."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.title("Aletheia Unit Preview")
    container.markdown("### Mirror, not throne.")
    container.write(
        "Paste a short text, question, receipt, or scenario to get a suggested path before entering ALETHEIA."
    )
    container.info(get_unit_preview_boundary_text())
    container.markdown(get_unit_preview_how_to_use_markdown())
    render_unit_preview_html_reference(container)
    with container.expander("Start here: try this first", expanded=False):
        container.markdown(get_unit_preview_start_here_markdown())

    preview_text = container.text_area(
        "Short text, question, scenario, or receipt",
        height=160,
        key="aletheia_unit_preview_text",
    )

    if container.button("Preview review path", key="aletheia_unit_preview_button"):
        suggestion = suggest_review_path(preview_text)
        container.markdown("### Suggested path")
        container.write(suggestion["path"])
        container.caption(suggestion["reason"])
        container.caption("You can still choose any module after entering ALETHEIA.")

    return bool(container.button("Proceed to ALETHEIA", type="primary", key="aletheia_unit_preview_proceed"))
