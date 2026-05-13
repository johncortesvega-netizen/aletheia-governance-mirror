"""Shared non-authority boundary text for ALETHEIA.

Patch 104 centralizes small boundary snippets so UI/docs can reuse the same
bounded language without implying certification, final authority, or a privacy
guarantee for hosted infrastructure.
"""
from __future__ import annotations

from pathlib import Path

BOUNDARY_DOC_PATH = Path("docs/BOUNDARY.md")

BOUNDARY_FOOTER = "**ALETHEIA** — Mirror, not throne. Human judgment required."

BOUNDARY_COMPACT = (
    "ALETHEIA — Mirror, not throne.\n"
    "Human judgment required. Local-first by design; hosted use has platform limits."
)

BOUNDARY_FULL_FALLBACK = (
    "ALETHEIA is a mirror, not a throne. It surfaces governance-risk signals "
    "for human review. It does not certify truth, safety, legality, ethics, "
    "privacy, security, or legitimacy. The repository is local-first by design; "
    "hosted deployments may have platform-level logs outside ALETHEIA's code boundary."
)


def get_boundary_text(level: str = "footer", *, root: str | Path = ".") -> str:
    """Return reusable ALETHEIA boundary text.

    Parameters
    ----------
    level:
        ``footer`` for the shortest footer, ``compact`` for a short plain
        statement, or ``full`` for the full boundary document when available.
    root:
        Project root used to locate ``docs/BOUNDARY.md`` for full rendering.
    """
    normalized = (level or "footer").strip().lower()
    if normalized == "footer":
        return BOUNDARY_FOOTER
    if normalized == "compact":
        return BOUNDARY_COMPACT
    if normalized == "full":
        boundary_path = Path(root) / BOUNDARY_DOC_PATH
        if boundary_path.exists():
            return boundary_path.read_text(encoding="utf-8")
        return BOUNDARY_FULL_FALLBACK
    raise ValueError(f"Unknown boundary text level: {level!r}")


def render_boundary_statement(level: str = "footer", container=None) -> None:
    """Render a boundary statement in Streamlit without changing app behavior.

    ``container`` may be ``st`` or any object exposing ``markdown``. Importing
    Streamlit is delayed so tests can import this module without requiring a UI
    runtime.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st
    container.markdown("---")
    container.markdown(get_boundary_text(level))
