"""Aletheia Unit Preview front-door helper.

The preview suggests where to begin before the full app opens. It does not
score, route modules, create receipts, inspect files, or call module engines.
"""
from __future__ import annotations

import re


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
