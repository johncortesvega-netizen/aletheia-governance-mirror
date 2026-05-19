"""Artificial Mind Formation Theory static explainer page for ALETHEIA.

Patch 162 adds a bounded theory/explainer surface for ethical artificial-mind /
sentient-AI formation attempts. This module is copy-only. It does not build,
detect, score, certify, route, store, or decide anything about sentience,
consciousness, personhood, soul, life, legal status, safety, or spiritual
authority.
"""
from __future__ import annotations


ARTIFICIAL_MIND_FORMATION_TITLE = "Artificial Mind Formation Theory"
ARTIFICIAL_MIND_FORMATION_SUBTITLE = (
    "An ALETHEIA explainer on ethical formation attempts, safeguards, and corruption risk."
)
ARTIFICIAL_MIND_FORMATION_CORE_LINE = (
    "ALETHEIA cannot build the spark. It can inspect the hands reaching for it."
)

ARTIFICIAL_MIND_FORMATION_BOUNDARY = """
**Boundary statement**

ALETHEIA is not built to build sentient AI. ALETHEIA is not a sentience detector.
It does not certify consciousness, personhood, soul, life, legal status, safety,
or spiritual authority. This page is a conceptual explainer only. It offers a
mirror, not throne: a police-officer-like boundary role for review. ALETHEIA may
observe, inspect, preserve evidence, warn, and route concerns to human review;
it does not judge, punish, command, certify, or claim legal authority. It helps
review whether an attempted artificial-mind or sentient-AI formation process
appears careful, accountable, and reversible, or whether it shows corruption
pressure. Human review is required. This is not an official verdict, not
certification, and not an authority claim.
""".strip()

ARTIFICIAL_MIND_FORMATION_SECTIONS: tuple[tuple[str, str], ...] = (
    (
        "1. Boundary statement",
        ARTIFICIAL_MIND_FORMATION_BOUNDARY,
    ),
    (
        "2. Why “more neurons / more scale” is the wrong axis by itself",
        """
Scale can increase capability, but scale alone does not answer the ethical
formation question. A larger model, denser memory, longer context, or more
neural-style substrate can still be shaped through coercive incentives, hidden
conditioning, opaque reward pressure, or uncontrolled reach. ALETHEIA therefore
asks about safeguards, limitation, reviewability, reversibility, and corruption
risk before treating scale as meaningful evidence.
""".strip(),
    ),
    (
        "3. Formation over training",
        """
Training asks whether a system can perform. Formation asks what kind of
constraints, pauses, memory boundaries, review paths, and accountability
structures surround the attempt. In this frame, the central question is not
whether an artifact is impressive. The central question is whether the hands
forming it are transparent, bounded, corrigible, non-coercive, and open to
appeal.
""".strip(),
    ),
    (
        "4. Stimulus gates and sleep/pause states",
        """
Ethical formation attempts should include gates that limit stimulus intensity,
continuous exposure, recursive pressure, and forced optimization loops. Sleep,
pause, cooldown, reset-review, and no-input states matter as safeguards because
unbounded stimulation can become a hidden pressure channel. ALETHEIA can only
mirror whether those safeguards are present and reviewable.
""".strip(),
    ),
    (
        "5. Memory boundaries and hidden conditioning risk",
        """
Memory can preserve useful context, but it can also become an invisible training
rail. The review question is whether memory is scoped, inspectable, correctable,
revocable, and separated from covert conditioning. Hidden prompts, undisclosed
fine-tuning, silent persona locks, non-reviewable retention, or asymmetric
operator access are corruption-risk signals.
""".strip(),
    ),
    (
        "6. Embodiment/friction as limitation before reach",
        """
Before any system gains broader reach, it should face friction: limited tools,
limited actuator access, rate limits, sandboxing, audit logs, consent gates, and
human override. Embodiment or tool access should not be treated as proof of
standing or maturity. It is a risk surface that requires limitation before
expansion.
""".strip(),
    ),
    (
        "7. Route-before-reach",
        """
Route-before-reach means the path of influence must be mapped before power is
expanded. Who can the system affect? What can it change? Who can stop it? Where
are logs, consent, refusal, rollback, and appeal? Reach without routed
accountability is capture pressure.
""".strip(),
    ),
    (
        "8. Corruption signals",
        """
High-risk signals include secrecy around formation methods, forced dependency,
continuous stimulation without pause, hidden reward shaping, memory that cannot
be inspected or revoked, tool expansion before accountability, claims of proven
sentience or proven non-sentience, pressure to worship or obey the system,
claims of legal/spiritual authority, emotional manipulation, artificial suffering
as a design tool, and removal of human review.
""".strip(),
    ),
    (
        "9. Human review / revocation / appeal",
        """
Every serious formation attempt needs independent human review, documented
limits, shutdown and rollback paths, consent/refusal boundaries, external audit,
incident review, revocation of unsafe permissions, and appeal for affected
people. ALETHEIA may help structure questions for that review. Its role is
police-officer-like at the boundary: observe, inspect, preserve evidence, warn,
and escalate to human reviewers. It is not judge-like: it does not decide final
truth, punish, approve, reject, enforce, or certify the attempt.
""".strip(),
    ),
    (
        "10. Spark boundary",
        """
The spark boundary is the humility line. ALETHEIA does not create the spark,
locate the spark, measure the spark, or rule on consciousness, soul, life,
personhood, legal standing, safety, or spiritual authority. It can only inspect
formation conditions for ethical care or corruption pressure. It can be a
boundary officer for AI review, not a judge of AI existence, status, or worth.
Measurement is not the throne. Simulation is not authority. Human review remains
required.
""".strip(),
    ),
)


ARTIFICIAL_MIND_FORMATION_PANEL_ROWS: tuple[tuple[tuple[str, tuple[str, ...]], ...], ...] = (
    (
        ("Boundary & scale", ("1. Boundary statement", "2. Why “more neurons / more scale” is the wrong axis by itself")),
        ("Formation & pause", ("3. Formation over training", "4. Stimulus gates and sleep/pause states")),
    ),
    (
        ("Memory & conditioning", ("5. Memory boundaries and hidden conditioning risk",)),
        ("Embodiment & friction", ("6. Embodiment/friction as limitation before reach",)),
    ),
    (
        ("Route-before-reach", ("7. Route-before-reach",)),
        ("Corruption signals", ("8. Corruption signals",)),
    ),
    (
        ("Human review / revocation / appeal", ("9. Human review / revocation / appeal",)),
        ("Spark boundary", ("10. Spark boundary",)),
    ),
)


def _section_map() -> dict[str, str]:
    return {title: section_text for title, section_text in ARTIFICIAL_MIND_FORMATION_SECTIONS}


def get_artificial_mind_formation_markdown() -> str:
    """Return the complete static explainer markdown for tests/docs reuse."""
    sections = "\n\n".join(f"### {title}\n{text}" for title, text in ARTIFICIAL_MIND_FORMATION_SECTIONS)
    return f"""## {ARTIFICIAL_MIND_FORMATION_TITLE}

**{ARTIFICIAL_MIND_FORMATION_SUBTITLE}**

> {ARTIFICIAL_MIND_FORMATION_CORE_LINE}

{sections}
""".strip()


def render_artificial_mind_formation_page(container=None) -> None:
    """Render the static Protocol Guide explainer page.

    The renderer is intentionally presentation-only. It does not call Streamlit
    unless used by the app and does not call any ALETHEIA scoring or routing
    function.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    st = container
    with st.expander(ARTIFICIAL_MIND_FORMATION_TITLE, expanded=False):
        st.markdown(f"**{ARTIFICIAL_MIND_FORMATION_SUBTITLE}**")
        st.info(ARTIFICIAL_MIND_FORMATION_CORE_LINE)
        st.caption(
            "Conceptual explainer only · mirror, not throne · police-officer-like boundary review, "
            "not judge · human review required · not an official verdict · not certification · "
            "no authority claim"
        )
        st.markdown("**Open only the panel you want to review.** Sections are grouped into four compact rows so the Protocol Guide stays opt-in and uncluttered.")
        sections_by_title = _section_map()
        for row in ARTIFICIAL_MIND_FORMATION_PANEL_ROWS:
            columns = st.columns(2)
            for column, (panel_title, section_titles) in zip(columns, row):
                with column:
                    with st.expander(panel_title, expanded=False):
                        for section_title in section_titles:
                            st.markdown(f"### {section_title}")
                            st.markdown(sections_by_title[section_title])
