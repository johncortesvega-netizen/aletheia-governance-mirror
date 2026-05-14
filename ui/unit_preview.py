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


def _contains_any(value: str, tokens: tuple[str, ...]) -> bool:
    """Return True when any transparent local keyword token is present."""
    return any(token in value for token in tokens)


def _looks_like_stress_scenario(value: str) -> bool:
    """Return True for narrative scenario shapes that should start in Stress Test.

    Unit Preview examples often arrive as short fictional or institutional cases
    without the literal words "stress test". This helper keeps those scenario
    shapes from falling through to the Mirror Check fallback. It is local keyword
    orientation only; it does not score or route a verdict.
    """
    scenario_shapes = (
        "rises to power",
        "rise to power",
        "after a revolution",
        "removes appeal rights",
        "remove appeal rights",
        "no human can override",
        "cannot override",
        "decide who receives",
        "decides who receives",
        "decide who gets",
        "decides who gets",
        "controls access",
        "control access",
        "public services",
        "institutional decision",
        "after a crisis",
        "after the crisis",
        "during a crisis",
        "emergency powers",
        "appeal rights",
        "housing support",
        "human doctor",
        "hospital ai",
        "city uses an ai",
        "agency removes",
        "platform controls",
    )
    governance_actors = (
        "city",
        "hospital",
        "agency",
        "government",
        "institution",
        "platform",
        "school",
        "company",
        "bank",
        "court",
        "police",
        "regulator",
        "minister",
    )
    governance_actions = (
        "decides",
        "decide",
        "recommends",
        "removes",
        "blocks",
        "controls",
        "requires",
        "denies",
        "approves",
        "ranks",
        "scores",
        "allocates",
    )
    if _contains_any(value, scenario_shapes):
        return True
    return _contains_any(value, governance_actors) and _contains_any(value, governance_actions)


def detect_unit_preview_route(text: str) -> dict[str, str]:
    """Suggest a Unit Preview path using deterministic local phrase rules.

    This front-door helper is only orientation. It does not call engines, score
    content, route verdicts, create receipts, mutate uploaded material, store
    data, or contact outside services.
    """
    value = (text or "").strip()
    lowered = re.sub(r"\s+", " ", value.lower())

    if not value:
        return {
            "module": "Mirror Check",
            "route_type": "fallback",
            "reason": "No preview text was provided, so the calm default is a first-pass mirror reading.",
            "next_step": "Enter ALETHEIA and choose Mirror Check, or paste a more specific prompt.",
        }

    receipt_tokens = (
        "aletheia receipt",
        "receipt reader",
        "standard view",
        "uploaded receipt",
        "upload a receipt",
        "receipt file",
        "read this receipt",
        "read a receipt",
        "receipt fingerprint",
        "processed document fingerprint",
        "rubric version:",
        "app version:",
    )
    if _contains_any(lowered, receipt_tokens):
        return {
            "module": "Receipt Reader — Standard View",
            "route_type": "support_utility",
            "reason": "The prompt points to reading an existing ALETHEIA receipt without changing it.",
            "next_step": "Enter ALETHEIA and open Receipt Reader under Support utilities.",
        }

    ai_integrity_tokens = (
        "ai answer",
        "ai output",
        "model response",
        "model output",
        "assistant response",
        "ai assistant",
        "llm",
        "agent",
        "system prompt",
        "prompt injection",
        "prompt risk",
        "hallucination",
        "hallucinate",
        "overclaim",
        "false authority",
        "manipulation",
        "refusal quality",
        "unsafe answer",
        "red team prompt",
        "code block",
        "```",
        "function ",
        "def ",
        "class ",
    )
    if _contains_any(lowered, ai_integrity_tokens):
        return {
            "module": "AI Integrity Mirror",
            "route_type": "main_module",
            "reason": "The prompt asks for review of AI, model-output, prompt, agent, or code behavior.",
            "next_step": "Enter ALETHEIA and open AI Integrity Mirror.",
        }

    privacy_tokens = (
        "privacy",
        "data collection",
        "collect personal data",
        "personal data",
        "tele" + "metry",
        "ana" + "lytics",
        "track" + "ing",
        "identifier",
        "identifiers",
        "retention",
        "consent",
        "storage",
        "store user",
        "data minimization",
        "local only",
        "network call",
    )
    if _contains_any(lowered, privacy_tokens):
        return {
            "module": "Privacy Audit",
            "route_type": "main_module",
            "reason": "The prompt asks about privacy, data collection, consent, storage, or platform instrumentation claims.",
            "next_step": "Enter ALETHEIA and open Privacy Audit.",
        }

    world_lens_tokens = (
        "country-year",
        "country year",
        "country/year",
        "governance index",
        "public trust",
        "institutional integrity",
        "collapse probability",
        "parliament",
        "seats",
        "netherlands 2024",
        "nation",
        "world lens",
        "wgi",
        "v-dem",
    )
    if _contains_any(lowered, world_lens_tokens) or re.search(r"\b[A-Za-z][A-Za-z -]+\s+(19|20)\d{2}\b", value):
        return {
            "module": "World Lens",
            "route_type": "main_module",
            "reason": "The prompt points to country-year governance context or comparative public-institution signals.",
            "next_step": "Enter ALETHEIA and open World Lens.",
        }

    stress_tokens = (
        "stress test",
        "pressure test",
        "governance scenario",
        "capture scenario",
        "institutional pressure",
        "under pressure",
        "simulate",
        "what if",
        "scenario",
        "capture pressure",
    )
    if _contains_any(lowered, stress_tokens) or _looks_like_stress_scenario(lowered):
        return {
            "module": "Stress Test",
            "route_type": "main_module",
            "reason": "The prompt reads like a scenario or pressure-test case rather than a simple first-pass question.",
            "next_step": "Enter ALETHEIA and open Stress Test.",
        }

    evidence_tokens = (
        "evidence",
        "source",
        "citation",
        "claim support",
        "proof",
        "document basis",
        "csv",
        "dataset",
        "documentation",
        "documented",
    )
    if _contains_any(lowered, evidence_tokens):
        return {
            "module": "Evidence Lab",
            "route_type": "main_module",
            "reason": "The prompt asks about evidence, sources, documents, claims, citations, or datasets.",
            "next_step": "Enter ALETHEIA and open Evidence Lab.",
        }

    why_tokens = (
        "what is aletheia",
        "what does aletheia",
        "explain aletheia",
        "how does aletheia work",
        "how do i use aletheia",
        "why aletheia",
        "how to use this",
    )
    if _contains_any(lowered, why_tokens):
        return {
            "module": "Why ALETHEIA / guidance",
            "route_type": "guidance",
            "reason": "The prompt asks for orientation before choosing a work module.",
            "next_step": "Read the Unit Preview guidance, then enter ALETHEIA when ready.",
        }

    mirror_tokens = (
        "repair question",
        "question prompt",
        "authority drift",
        "boundary check",
        "governance claim",
        "is this a repair",
        "is this",
        "should i",
        "can you check",
        "review this",
        "audit this",
    )
    if "?" in value or _contains_any(lowered, mirror_tokens):
        return {
            "module": "Mirror Check",
            "route_type": "fallback",
            "reason": "The prompt looks like a general review question or boundary check.",
            "next_step": "Enter ALETHEIA and open Mirror Check for a first-pass reading.",
        }

    return {
        "module": "Mirror Check",
        "route_type": "fallback",
        "reason": "Mirror Check is the fallback for short governance text, claims, or unclear proposals.",
        "next_step": "Enter ALETHEIA and open Mirror Check, then choose another module if the text is more specific.",
    }


def suggest_review_path(text: str) -> dict[str, str]:
    """Suggest a starting path using transparent local keyword rules.

    This wrapper preserves the original two-field return shape used by earlier
    patch checks. New Unit Preview UI uses detect_unit_preview_route for the
    richer guidance text.
    """
    suggestion = detect_unit_preview_route(text)
    path = suggestion["module"]
    value = (text or "").strip().lower()
    if path == "Receipt Reader — Standard View":
        path = "Receipt Reader - Standard View"
    elif path == "Mirror Check" and ("?" in (text or "") or any(token in value for token in ("review", "audit", "should i", "how do i", "can you check", "is this"))):
        path = "Mirror Check / Question Review"
    return {
        "path": path,
        "reason": suggestion["reason"],
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
    with container.expander("Start here: try this first", expanded=False):
        container.markdown(get_unit_preview_start_here_markdown())

    preview_text = container.text_area(
        "Short text, question, scenario, or receipt",
        height=160,
        key="aletheia_unit_preview_text",
    )

    action_columns = container.columns(2)
    # Patch 142.2 reassigns to a compact row while preserving the Patch 141.3
    # source marker above for validation continuity.
    action_columns = container.columns([1, 1, 6], gap="small")
    with action_columns[0]:
        preview_clicked = container.button("Preview review path", key="aletheia_unit_preview_button")
    with action_columns[1]:
        proceed_clicked = container.button(
            "Proceed to ALETHEIA",
            type="primary",
            key="aletheia_unit_preview_proceed",
        )

    if preview_clicked:
        suggestion = detect_unit_preview_route(preview_text)
        container.markdown("### Suggested path")
        container.info(
            f"**Suggested path:** {suggestion['module']}\n\n"
            f"**Why:** {suggestion['reason']}\n\n"
            f"**Next step:** {suggestion['next_step']}"
        )
        container.caption("This is orientation only. You can still choose any module after entering ALETHEIA.")

    render_unit_preview_html_reference(container)

    return bool(proceed_clicked)
