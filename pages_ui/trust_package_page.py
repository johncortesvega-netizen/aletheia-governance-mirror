"""Public trust package page renderer for ALETHEIA.

Patch 124 exposes the review path from the public trust package inside the app
without moving the documentation source of truth. This module renders static
document pointers and review prompts only. It does not own routing, session
state, scoring, receipts, downloads, uploads, signal logic, privacy scan logic,
AI Integrity scan logic, World Lens math, external calls, telemetry, analytics,
storage, certification, enforcement, privacy guarantees, or final-truth claims.
"""
from __future__ import annotations


TRUST_PACKAGE_REVIEW_PATH = [
    (
        "Boundary and authority",
        ["docs/BOUNDARY.md", "docs/scope_layers.md", "docs/ethics.md"],
        "Confirm the mirror-not-throne boundary and the human-review requirement.",
    ),
    (
        "Privacy and hosted use",
        [
            "docs/privacy_boundary.md",
            "docs/hosting_limits.md",
            "docs/go_live_privacy_review_statement.md",
            "docs/privacy_audit_panel_v1.md",
        ],
        "Check local-first posture and hosted-platform caveats before using sensitive material.",
    ),
    (
        "Signal basis and limits",
        ["docs/signal_detection.md", "docs/SIGNAL_DICTIONARY.md"],
        "Review rule-based and heuristic limits, including English/Dutch calibration boundaries.",
    ),
    (
        "Architecture and maintainability",
        [
            "docs/architecture.md",
            "docs/structural_improvement_entrypoint.md",
            "docs/new_contributor_start_here.md",
            "CONTRIBUTING.md",
        ],
        "Check whether the system remains reviewable as app.py is reduced gradually.",
    ),
    (
        "Beginner path",
        ["docs/beginner_ux.md", "ui/beginner_guide.py"],
        "Confirm a first-time reviewer is guided toward reasons, repair questions, and human review.",
    ),
    (
        "Patch history",
        [
            "docs/patch_index.md",
            "PATCH_STATUS.md",
            "docs/progress_database.md",
            "latest PATCH_*_MANIFEST.txt",
            "latest PATCH_*_RECOVERY_NOTE.md",
        ],
        "Inspect one patch at a time without treating history as proof of correctness.",
    ),
    (
        "Public-review checklist",
        ["docs/public_review_checklist.md"],
        "Use the checklist before relying on a reading, adapting the code, or contributing a patch.",
    ),
]


def render_public_trust_package_page(container=None) -> None:
    """Render the public trust package review route."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    st = container
    with st.expander("Public Trust Package", expanded=False):
        st.markdown(
            """
            The public trust package is a review route, not a certification package.
            Its source of truth remains the documentation in `docs/public_trust_package.md`
            and `docs/public_review_checklist.md`.
            """
        )
        st.caption(
            "Use this map to find the relevant docs. It does not prove truth, safety, legality, ethics, privacy, security, compliance, or legitimacy."
        )

        st.markdown("#### Review posture")
        st.write(
            "ALETHEIA treats regulation as a floor, not the final measure of integrity. "
            "The trust package is therefore organized around boundary, privacy, signal basis, "
            "appeal, and reviewability rather than automatic approval. Its public question is: "
            "where is power moving, what is hidden, who can appeal, and where is human review being weakened?"
        )

        for title, paths, question in TRUST_PACKAGE_REVIEW_PATH:
            st.markdown(f"#### {title}")
            st.write(question)
            st.code("\n".join(paths), language="text")

        st.info("If a reviewer cannot answer a checklist item, the next step is more human review, not automatic trust or automatic rejection.")
        st.markdown("**ALETHEIA surfaces signals. Humans keep the judgment.**")
