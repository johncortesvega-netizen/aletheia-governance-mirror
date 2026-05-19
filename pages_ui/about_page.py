"""About / public info page renderer for ALETHEIA.

Patch 123 moves the Streamlit About tab copy into a focused page helper.
The helper renders static public information only. It does not own navigation,
session state, scoring, receipts, downloads, uploads, signal logic, privacy
scan logic, AI static scan logic, World Lens math, external calls,
telemetry, analytics, storage, certification, enforcement, privacy guarantees,
or final-truth claims.
"""
from __future__ import annotations

from pathlib import Path


def _render_about_panel_rows(st, panels: list[tuple[str, str]], header_image: str | Path | None = None) -> None:
    """Render the About page as compact opt-in side-by-side panels.

    This helper is UI/copy only. It does not call scoring engines, alter
    navigation, create receipts, upload/download files, or mutate app state.
    """
    for row_start in range(0, len(panels), 2):
        columns = st.columns(2, gap="large")
        row = panels[row_start : row_start + 2]
        for index, (title, body) in enumerate(row):
            with columns[index]:
                with st.expander(title, expanded=False):
                    if title == "1. Identity & visual theme" and header_image is not None:
                        st.image(str(header_image), use_container_width=True)
                    st.markdown(body)


def render_about_public_info_page(container=None, header_image: str | Path | None = None) -> None:
    """Render the public About / Why ALETHEIA page."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    st = container
    st.subheader("Why AI Patrol / ALETHEIA")
    # Patch 182: visual-only sky/gold alignment anchor for the public Why page.
    st.markdown(
        """
        <div class="sky-gold-page-anchor">
            <strong><span class="pillar-pair"></span>Why AI Patrol</strong>
            <span class="sky-gold-rule"></span>
            <span>The rebrand uses sky-blue clarity, white civic structure, and gold emphasis while preserving the mirror-not-throne boundary.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(
        "AI Patrol is the friendlier public face of ALETHEIA: a compact stop/go "
        "review layer for human judgment. Science investigates, philosophy structures, "
        "theological humility restrains final claims, and people decide."
    )
    st.caption(
        "Open only the panels you need. This page explains the public identity, "
        "module map, research boundary, and non-authority limits without changing any app logic."
    )

    panels = [
        (
            "1. Identity & visual theme",
            """
**AI Patrol is the friendlier public face of ALETHEIA v1.0.**

The visual identity is a kind patrol mascot in a cartoon data-center setting: a cardboard robot, blue patrol uniform, red siren, and STOP / GO paddle.

The meaning is bounded:

> **AI Patrol signals. Humans review. Power stays accountable.**

It is not a judge, enforcer, oracle, certification engine, legal authority, political authority, religious authority, medical authority, investment authority, or automated decision system.
""",
        ),
        (
            "2. Why it exists",
            """
AI Patrol / ALETHEIA exists because many systems can look orderly while still moving power out of reach.

A policy can have compliance language and still hide appeal failure. An AI output can sound neutral while carrying flattery pressure or provider-shaped assumptions. A governance process can be documented while still concentrating power.

AI Patrol does not answer that problem with more command, automation, or institutional control. It uses a restrained mirror: make pressure visible, name missing safeguards, and return the reading to human review.
""",
        ),
        (
            "3. What this is / is not",
            """
**This is:** a friendly integrity patrol and mirror for pressure, authority drift, evidence gaps, capture risk, consent pressure, weak appeal paths, and human-review needs.

**This is not:** a judge, oracle, certification engine, truth machine, legal authority, political authority, religious authority, medical authority, investment authority, or automated decision system.

Internal taxonomy labels such as **SANCTUARY**, **THRESHOLD**, and **ASYLUM** are review-workflow labels only. They do not claim truth, purity, safety, legitimacy, moral authority, or final status.
""",
        ),
        (
            "4. Science, philosophy, humility, and review",
            """
> **Science is the investigative base. Philosophy is the interpretive structure. Theology is the humility boundary. Human review is the action layer.**

ALETHEIA is a science-grounded, philosophically structured governance mirror with theological humility boundaries. It does not replace evidence with faith, and it does not claim final authority.

- **Base layer:** inspectable signals, heuristics, metrics, receipts, and repair questions.
- **Philosophical layer:** power, capture, authority drift, evidence integrity, and self-certification.
- **Theological / humility layer:** restraint around final claims about soul, life, consciousness, dignity, and ultimate truth.
- **Action layer:** human review, appeal, correction, and accountable decision-making outside the tool.

Compared with mainstream AI ethics, ALETHEIA is less compliance-centered and more focused on upstream power, epistemic restraint, and preventing ethics itself from becoming a throne.
""",
        ),
        (
            "5. First-use path & navigation",
            """
Choose the tab by task:

| Tab | What it does |
|---|---|
| Mirror Check | Reviews documents and proposals for capture risk, missing safeguards, and repair questions. |
| Stress Test | Simulates scenario pressure and asks repair questions. |
| Boundary Cases | Tests difficult ethical scenarios before they become app logic or public claims. |
| Evidence Lab | Reviews evidence status, source coverage, schema readiness, and extraordinary claims. |
| World Lens | Reviews selected-year, population-weighted evidence exposure without real Global ID, a real 9k body, or sovereign authority. |
| Patrol Guide | Explains modules, safe language, internal taxonomy labels, and limitations. |
| Why AI Patrol | Explains the project, baseline, and public-safe purpose. |

The UX rule is simple: make the next patrol step obvious while keeping every output reviewable.
""",
        ),
        (
            "6. Failure modes watched",
            """
AI Patrol watches for pressure patterns that can make systems appear more legitimate, neutral, certain, or authoritative than the evidence supports.

- **Authority drift** — when a system sounds like it can decide, certify, command, legitimize, rank, punish, or replace human judgment.
- **Evidence inflation** — when claims become stronger than the evidence actually inspected.
- **Flattery pressure** — when approval or reassurance is disguised as neutral analysis.
- **Capture pressure** — when power concentrates in one actor, platform, institution, committee, model owner, funder, or gatekeeper.
- **Sanctification drift** — when symbolic or higher-truth language becomes operational authority.
- **False neutrality** — when hidden defaults are presented as objective reasoning.
- **No-appeal automation** — when people are affected without review, contestation, explanation, or repair path.
""",
        ),
        (
            "7. Scope layers & anti-capture posture",
            """
**Current operational layer:** corruption-pattern and governance-risk review for human interpretation.

**Research layer:** benchmarks, empirical mappings, scenario tests, validation work, and documentation. These remain reviewable and correctable.

**Vision layer:** a theoretical horizon for governance that follows transparency, consent, accountability, proportionality, dignity, appealability, repair, and limits on concentrated power.

**Out-of-scope layer:** ALETHEIA does not govern, enforce, allocate authority, select representatives, create a real 9k body, issue mandates, validate spiritual or political authority, or replace human judgment.

AI Patrol is anti-capture by design: it reflects capture-risk signals but does not become a central authority.
""",
        ),
        (
            "8. What the modules do",
            """
**Mirror Check** reviews one document, idea, proposal, policy text, or AI output for pressure signals and repair questions.

**Stress Test** models governance pressure through stability, trust, alignment, ego, grievances, friction, safeguards, and collapse risk.

AI-specific static scan context is now subordinate to **Mirror Check** and **Stress Test**. It is not a standalone module or separate verdict path.

**Evidence Lab** separates claims from evidence and prepares empirical review support.

**World Lens** shows selected-year, population-weighted evidence exposure. It is not a real election, government, sovereign body, mandate, Global ID system, or real 9k body.

**Patrol Guide** preserves operating boundaries while remaining corrigible by evidence.
""",
        ),
        (
            "9. Research caution & developer notes",
            """
ALETHEIA does not prove legal, political, medical, religious, moral, predictive, or final truth. Its outputs are internal review readings. Empirical results depend on dataset quality, variable mapping, normalization choices, missing data, and validation against external outcomes.

A responsible reading is:

> **This model suggests a governance-risk pattern worth examining.**

Not:

> **This model has final authority.**

Local development:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Key files include `app.py`, `core/parser.py`, `core/simulation.py`, `core/scoring.py`, `core/empirical.py`, `config/weights.py`, `data_processed/`, `paper/`, and `assets/`.
""",
        ),
    ]

    _render_about_panel_rows(st, panels, header_image=header_image)
