"""Evidence Lab static UI copy helpers for ALETHEIA.

Patch 125 starts the Evidence Lab UI extraction by moving only stable
introductory copy and public-data build guidance out of app.py. This module
does not own uploads, scoring, dataframe processing, session state, downloads,
receipts, routing, signal logic, privacy scan logic, AI Integrity scan logic,
World Lens math, external calls, telemetry, analytics, storage, certification,
enforcement, privacy guarantees, or final-truth claims.
"""
from __future__ import annotations


def _render_evidence_lab_panel_rows(container, panels: list[tuple[str, str]]) -> None:
    """Render Evidence Lab orientation as compact opt-in side-by-side panels.

    This helper is UI/copy only. It does not call empirical builders, run
    scoring, inspect uploads, create receipts, mutate session state, or alter
    World Lens behavior.
    """
    for row_start in range(0, len(panels), 2):
        columns = container.columns(2, gap="large")
        row = panels[row_start : row_start + 2]
        for index, (title, body) in enumerate(row):
            with columns[index]:
                with columns[index].expander(title, expanded=False):
                    container.markdown(body)


def render_evidence_lab_intro(container=None) -> None:
    """Render the static Evidence Lab page introduction."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.subheader("Evidence Lab")
    # Patch 192: visual-only warm original governance-mirror anchor for Evidence Lab.
    container.markdown(
        """
        <div class="sky-gold-page-anchor">
            <strong><span class="pillar-pair"></span>Evidence Lab</strong>
            <span class="sky-gold-rule"></span>
            <span>Evidence review uses the same warm governance-mirror frame: source clarity first, certainty restrained, human review required.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    container.info(
        "Evidence Lab is the ALETHEIA evidence desk: it separates claims from sources, "
        "checks coverage, and prepares public data for human review. It signals what can "
        "be supported, what is missing, and what must stay unverified."
    )
    container.caption(
        "Open only the evidence panels you need. These notes are guidance for review, not proof, "
        "certification, debunking, legal judgment, religious authority, or final truth."
    )

    panels = [
        (
            "1. Evidence boundary",
            """
**Evidence does not come from ALETHEIA.** Public datasets, user-supplied sources, and uploaded tables provide the material.

ALETHEIA maps, reflects, and flags limits. It does not certify sources, prove claims, debunk claims, or become a truth authority.

> **Evidence Lab signals. Humans review. Power stays accountable.**
""",
        ),
        (
            "2. Evidence status protocol",
            """
Evidence Lab uses four ordinary review levels:

- **Strong evidence** — multiple public, relevant, reviewable sources support the claim.
- **Partial evidence** — some evidence exists, but coverage, independence, relevance, or completeness is limited.
- **Weak evidence** — the claim is mostly asserted, anecdotal, internally sourced, or insufficiently documented.
- **No evidence supplied** — no reviewable support is provided.

These are review signals, not final truth labels.
""",
        ),
        (
            "3. Public-source rule",
            """
Use public, relevant, reviewable, non-coercive sources wherever possible.

Watch for:

- stale evidence;
- self-referential sources;
- missing dates or geography;
- claims stronger than the inspected data;
- unreviewable private assertions;
- evidence used as authority instead of support.
""",
        ),
        (
            "4. Data flow",
            """
Evidence Lab reads the flow as:

> **public evidence → variable mapping → empirical scoring → protocol overlay → review**

The flow is useful only when every step remains inspectable. A clean table cannot override weak source coverage, missing fields, or hard protocol boundaries.
""",
        ),
        (
            "5. Needed columns",
            """
Minimum identity columns:

```text
country, iso3, year
```

Needed for real 9k allocation:

```text
population
```

Helpful empirical columns include WGI, V-Dem, trust, identity/coverage, and source-diagnostic fields. Missing columns lower confidence; they do not prove absence.
""",
        ),
        (
            "6. Extraordinary claim rule",
            """
Extraordinary claims — including spiritual, prophetic, alien, neural, metaphysical, or otherwise exceptional claims — stay **unverified** unless supported by public, testable, non-coercive evidence and human review.

ALETHEIA may review policy consequences around rights, coercion, transparency, accountability, appealability, and repair. It must not validate spiritual authority, confirm invisible sources, remove guardrails, or replace human review.
""",
        ),
        (
            "7. Build / upload path",
            """
A simple empirical path:

1. Start with World Bank WGI.
2. Add population for country-level allocation.
3. Optionally enrich rows with V-Dem and trust data.
4. Inspect diagnostics before relying on outputs.
5. Use the prepared master uploader only when the table is already ALETHEIA-ready.

Uploads remain local to the running app session unless the host platform logs separately.
""",
        ),
        (
            "8. Export / World Lens boundary",
            """
Evidence Lab exports support review and World Lens preparation. They do not certify countries, claims, institutions, beliefs, datasets, or governance legitimacy.

World Lens can use prepared evidence context, but it still remains a selected-year evidence mirror — not a sovereign body, real 9k selection, Global ID system, public ledger, or policy decision.
""",
        ),
    ]

    _render_evidence_lab_panel_rows(container, panels)


def render_evidence_lab_public_data_build_intro(container=None) -> None:
    """Render the static public-data build guidance."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown("### Build a country-year table from public data")
    container.caption(
        "A simple path is: start with World Bank WGI, add population for country-level allocation, "
        "and optionally enrich the result with V-Dem and trust data. The separate merged-evidence uploader "
        "is for a fully prepared ALETHEIA-ready master CSV."
    )
    container.info(
        "Empirical build flow: WGI plus population create the core country-year base; V-Dem and trust enrich matching rows. "
        "By default, scoring stays in the modern era from 1996 onward so historical V-Dem rows are not accidentally mixed "
        "with modern population or seat allocation."
    )
