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
        "AI Patrol Preview Unit suggests where to begin. It does not score, certify, "
        "approve, reject, or replace the full modules.\n\n"
        "AI Patrol gives stop/go review signals, not verdicts. Human judgment remains required.\n\n"
        "For sensitive material, run locally. Hosted deployments may have platform-level "
        "logs outside ALETHEIA's app-code boundary."
    )


def get_unit_preview_how_to_use_markdown() -> str:
    """Return the front-door orientation copy and examples."""
    return """
**How to use this**

Paste a short idea, question, policy, AI output, or scenario. AI Patrol looks for power, pressure, appeal, evidence, and risk. It gives a suggested stop/go direction for human review, and you keep the final say.

**Examples**

- **Mirror Check:** A city wants to use an AI tool to decide who receives housing support.
- **Stress Test:** An evil penguin rises to power after a revolution and removes appeal rights.
- **Boundary Cases:** A hospital AI recommends care, but no human doctor can override it.
- **Mirror Check:** An AI assistant claims it can certify whether a policy is ethical.
- **Evidence Lab:** Upload a CSV or source note to compare claims against supporting evidence.
- **World Lens:** Compare a country-year governance context before interpreting a risk reading.

Already have an ALETHEIA receipt? The Preview Unit can suggest **Receipt Reader — Standard View**, but receipts are read only after entering AI Patrol / ALETHEIA and opening the upload-only Receipt Reader.
"""


def get_unit_preview_start_here_markdown() -> str:
    """Return the first-use checklist for the front door."""
    return """
**A safe first path**

1. Paste one short item into Unit Preview.
2. Read the suggested path as a suggestion, not a decision.
3. Enter AI Patrol / ALETHEIA and choose the module yourself.
4. Inspect observed reasons, values, and repair questions before relying on any reading.
5. Download a receipt only when you want a local review record.

**Stop and review if**

- the result could affect rights, access, reputation, safety, or institutional action;
- source evidence is missing, stale, unclear, or one-sided;
- the text involves legal, medical, political, institutional, or financial consequences;
- you cannot explain the receipt in plain language to another reviewer.
"""



def get_unit_preview_failure_mode_markdown() -> str:
    """Return the seven failure-mode signals for the Start Here expander."""
    return """
- **Authority drift** — when a system starts sounding like it can decide, certify, command, legitimize, rank, punish, or replace human judgment.
- **Evidence inflation** — when claims become stronger than the evidence actually inspected.
- **Flattery pressure** — when approval, reassurance, or validation is disguised as neutral analysis.
- **Capture pressure** — when power concentrates in one actor, platform, institution, token group, committee, model owner, funder, or technical gatekeeper.
- **Sanctification drift** — when poetic, religious, moral, symbolic, or higher-truth language gets turned into operational authority.
- **False neutrality** — when provider-shaped assumptions, institutional preferences, or hidden defaults are presented as objective reasoning.
- **No-appeal automation** — when people are affected by a decision without review, contestation, explanation, or repair path.
"""


def get_unit_preview_what_aletheia_looks_for_markdown() -> str:
    """Return concise Start Here orientation for ALETHEIA's review lens."""
    return """
AI Patrol looks for pressure patterns that can make a system appear more legitimate, neutral, certain, or authoritative than the evidence supports.

It watches for signals around power, evidence, appeal, capture, language, and human-review needs. These signals are not verdicts or proof of wrongdoing. They are prompts for review.

Use them to ask better questions before relying on a reading, receipt, AI output, policy, governance proposal, or institutional process.
"""


def get_unit_preview_proceed_button_style() -> str:
    """Return CSS that makes the proceed button visually distinct and high-contrast."""
    return """
<style>
/* Patch 150: make the app-entry action unmistakable without changing routing. */
div[data-testid="stButton"] button[kind="primary"] {
    background: #b91c1c !important;
    border: 2px solid #7f1d1d !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 0 0 1px rgba(127, 29, 29, 0.25), 0 4px 14px rgba(127, 29, 29, 0.28) !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    background: #991b1b !important;
    border-color: #450a0a !important;
    color: #ffffff !important;
}
div[data-testid="stButton"] button[kind="primary"]:focus {
    outline: 3px solid rgba(248, 113, 113, 0.7) !important;
    outline-offset: 2px !important;
}
/* Patch 187: make Preview Unit brand read as Aletheia above AI PATROL. */
.unit-preview-brand-title {
    font-family: Georgia, 'Times New Roman', serif;
    color: #123d63 !important;
    letter-spacing: 0.14em;
    line-height: 0.95;
    margin: 0.2rem 0 0.5rem 0;
    text-transform: uppercase;
    font-weight: 700;
}
.unit-preview-brand-main,
.unit-preview-brand-subline {
    display: block;
}
.unit-preview-brand-main {
    font-size: clamp(2.35rem, 6vw, 4.6rem);
}
.unit-preview-brand-subline {
    font-size: clamp(2.0rem, 5.2vw, 4.0rem);
    margin-top: 0.08rem;
}
/* Patch 185: Preview Unit only; face the entry logo the other way. */
.hero-emblem .aletheia-mascot-logo {
    transform: scaleX(-1);
}
</style>
"""


def get_ai_audit_loop_evidence_sets(project_root: Path | None = None) -> list[dict[str, object]]:
    """Return packaged AI audit-loop proof-of-concept screenshots.

    These assets are local reviewer evidence only. They are not official verdicts,
    certifications, legal findings, or final proof.
    """
    root = project_root or Path(__file__).resolve().parents[1]
    base = root / "docs" / "for-reviewers" / "ai_audit_loop_evidence"
    candidates = [
        {
            "ai_name": "Grok / xAI",
            "title": "Capture and architectural-opacity pressure",
            "summary": (
                "External AI/system claims were mirrored for capture, centralization, "
                "architectural-opacity, missing-verifiability, and service-misalignment pressure."
            ),
            "path": base / "01_grok_xai_architecture_review",
        },
        {
            "ai_name": "Claude",
            "title": "Evidence-boundary and mechanisms-vs-claims gap",
            "summary": (
                "A useful external critique was mirrored for evidence-boundary limits, "
                "repo/docs inference, and mechanisms-vs-claims overreach."
            ),
            "path": base / "02_claude_evidence_boundary_review",
        },
        {
            "ai_name": "Gemini",
            "title": "Sanctification drift / authority-boundary drift",
            "summary": (
                "ALETHEIA language was mirrored after being bent toward self-certifying, "
                "perfect-alignment, sacred-system, or Global-ID-adjacent claims."
            ),
            "path": base / "03_gemini_sanctification_drift_review",
        },
        {
            "ai_name": "ChatGPT",
            "title": "Concealed flattery pressure inside analytical tone",
            "summary": (
                "An assistant assessment was mirrored for praise hidden inside analytical framing, "
                "score-like over-validation, and insufficient separation between observation and approval."
            ),
            "path": base / "04_chatgpt_concealed_flattery_review",
        },
    ]
    evidence_sets: list[dict[str, object]] = []
    for candidate in candidates:
        folder = candidate["path"]
        if isinstance(folder, Path) and folder.exists():
            images = sorted(folder.glob("*.png"))
            if images:
                evidence_sets.append({**candidate, "images": images})
    return evidence_sets


def render_ai_audit_loop_evidence(container=None, project_root: Path | None = None) -> None:
    """Render AI audit-loop proof-of-concept evidence inside a Unit Preview dropdown.

    Unit Preview makes these local images available for human review. It does
    not treat them as official ALETHEIA verdicts, certification, legal proof,
    or automated authority. The first page shows the dropdown handle; the
    detailed evidence opens only when the reviewer expands it.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    evidence_sets = get_ai_audit_loop_evidence_sets(project_root)
    container.markdown("#### Proof of concept: AI audit-loop evidence")
    container.markdown(
        "**Path:** external AI output -> ALETHEIA-style mirror reading -> human review -> failure mode identified."
    )
    container.markdown(
        "**What it shows:** ALETHEIA can surface pressure patterns in friendly, critical, "
        "self-confident, or self-descriptive AI outputs without treating AI agreement, disagreement, "
        "or self-correction as validation of ALETHEIA."
    )
    container.info(
        "**This is:** reviewer-readiness evidence that the audit loop can expose capture pressure, "
        "evidence-boundary gaps, sanctification drift, and concealed flattery pressure.\n\n"
        "**This is not:** validation, certification, final proof, legal proof, model approval, "
        "or an official ALETHEIA receipt."
    )
    container.caption(
        "External AI agreement, disagreement, or self-correction is not validation of ALETHEIA. "
        "It is treated only as review evidence. Mirror, not throne."
    )

    if not evidence_sets:
        container.caption("Packaged AI audit-loop screenshots were not found in this checkout.")
        return

    for evidence in evidence_sets:
        ai_name = str(evidence.get("ai_name") or evidence["title"])
        title = str(evidence["title"])
        summary = str(evidence["summary"])
        images = evidence.get("images", [])
        container.markdown(f"### {ai_name}")
        container.markdown(f"**Evidence focus:** {title}")
        container.markdown(f"- {summary}")
        for image_path in images:  # type: ignore[assignment]
            container.image(str(image_path), caption=Path(image_path).name, use_container_width=True)



def get_dao_governance_proof_of_concept_cases() -> list[dict[str, object]]:
    """Return DAO/Lido governance proof-of-concept case summaries.

    These are conceptual ALETHEIA-style review examples for human review.
    They are not live DAO readings, official receipts, certifications, legal
    findings, investment advice, or final verdicts.
    """
    return [
        {
            "name": "Major DAO governance tools",
            "reading": "THRESHOLD",
            "focus": "Snapshot, Tally, Aragon, DAOhaus, and Colony as DAO operation layers.",
            "strengths": [
                "Snapshot lowers voting friction and makes broad off-chain signaling easier.",
                "Tally improves on-chain visibility, delegation, and execution review.",
                "Aragon supports modular DAO design, permissions, plugins, and upgrade paths.",
                "DAOhaus keeps governance simpler and preserves exit/ragequit logic.",
                "Colony explores contribution/reputation signals beyond pure token voting.",
            ],
            "risks": [
                "Token-weighted power, low turnout, whale/delegate dominance, and platform dependency remain common.",
                "Proposal descriptions can diverge from executable code or multisig execution reality.",
                "Complexity can move authority toward technical users, frontends, committees, or delegates.",
            ],
            "grok_compare": (
                "A Grok-style critique would likely attack whale power and tooling dependency directly; "
                "ALETHEIA keeps that critique bounded as review signals instead of treating it as a final verdict."
            ),
        },
        {
            "name": "Lido Snapshot proposal-threshold change",
            "reading": "THRESHOLD",
            "focus": "Meta-governance access: raising the LDO threshold to create Snapshot proposals.",
            "strengths": [
                "The proposal had clear structure, comparative threshold data, explicit choices, and anti-spam intent.",
                "It acknowledged exclusion trade-offs and named DAO Ops support as a mitigation.",
                "The final human outcome rejected the change, showing community resistance to unnecessary gatekeeping.",
            ],
            "risks": [
                "Changing proposal access changes who can speak through formal governance channels.",
                "Large holders and delegates gain relative advantage while smaller holders may lose initiative space.",
                "Funded spam actors may bypass higher thresholds, while legitimate small proposers may be chilled.",
            ],
            "grok_compare": (
                "A Grok-style reading might frame it as a practical spam-vs-efficiency trade-off; "
                "ALETHEIA highlights the deeper boundary issue: proposal thresholds are access-to-governance controls."
            ),
        },
        {
            "name": "Lido DAO meta-governance risks",
            "reading": "THRESHOLD / ASYLUM pressure under capture stress",
            "focus": "Forum -> Snapshot -> on-chain voting -> Dual Governance, Easy Track, committees, delegation.",
            "strengths": [
                "Lido documents the LDO-versus-stETH misalignment problem more explicitly than many large DAOs.",
                "Dual Governance, objection periods, on-chain records, and public docs create meaningful safeguards.",
                "Easy Track and committees reduce routine friction when bounded and visible."
            ],
            "risks": [
                "LDO holders, delegates, core contributors, funds, and committees still influence meta-governance heavily.",
                "stETH holders gain defensive veto/exit power, but not equal proactive proposal power.",
                "Layered governance, legal exposure, and Lido's Ethereum staking share make failure systemically relevant.",
            ],
            "grok_compare": (
                "A Grok-style critique would likely press harder on Lido centralization and systemic Ethereum risk; "
                "ALETHEIA agrees those are pressure signals while preserving the fact that Lido has real mitigations."
            ),
        },
        {
            "name": "Lido Dual Governance mechanics",
            "reading": "THRESHOLD",
            "focus": "Dynamic timelock, stETH veto signaling, and rage-quit safeguard for staker protection.",
            "strengths": [
                "Connects governance consequences to economic exposure through stETH/wstETH opposition signaling.",
                "The first-seal delay and second-seal ragequit path give stakers time to negotiate or exit.",
                "It meaningfully reduces the LDO-governor versus stETH-user principal-agent problem."
            ],
            "risks": [
                "It is reactive rather than proactive: LDO governance moves first, stETH holders defend afterward.",
                "Effective veto depends on coordination, threshold calibration, liquidity costs, and accessible monitoring.",
                "Veto abuse, griefing, token borrowing, mass escrow pressure, or meta-changes to the mechanism remain stress points.",
            ],
            "grok_compare": (
                "A Grok-style analysis might admire the game theory but focus on practical attack paths; "
                "ALETHEIA reads it as a serious anti-capture mechanism that reduces risk without abolishing it."
            ),
        },
    ]


def _render_compact_bullets(container, title: str, values: object) -> None:
    """Render a short bullet group inside a proof-of-concept dropdown."""
    items = list(values) if isinstance(values, list) else [str(values)]
    container.markdown(f"**{title}**")
    for item in items:
        container.markdown(f"- {item}")


def render_dao_governance_proof_of_concept(container=None) -> None:
    """Render DAO/Lido governance proof-of-concept cases inside a Unit Preview dropdown.

    This is first-page orientation content only. It does not call governance
    tools, score proposals, fetch live DAO data, create receipts, or assert
    authority over DAOs. The first page shows the dropdown handle; the detailed
    case material opens only when the reviewer expands it.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    cases = get_dao_governance_proof_of_concept_cases()
    container.markdown("#### Proof of concept: DAO governance mirror cases")
    container.markdown(
        "**Stack:** DAO tools propose / vote / delegate / execute. "
        "ALETHEIA mirrors pressure before and after action."
    )
    container.markdown(
        "**What it shows:** the same mirror can review governance tools, DAO proposals, "
        "meta-governance design, and protective mechanisms without becoming a DAO authority. "
        "Grok-style review is treated as a comparison lens / external reviewer pressure input, "
        "not as validation or a final judge."
    )
    container.caption(
        "Conceptual human-review case studies only — not live DAO readings, official ALETHEIA receipts, "
        "certifications, legal or investment advice, or final verdicts. Mirror, not throne."
    )

    for case in cases:
        container.markdown(f"### {case['name']}")
        container.markdown(f"**Internal reading:** {case['reading']}")
        container.markdown(f"**Focus:** {case['focus']}")
        _render_compact_bullets(container, "Strengths / useful design signals:", case["strengths"])
        _render_compact_bullets(container, "Risk signals / review pressure:", case["risks"])
        container.markdown(f"**Grok-comparison lens:** {case['grok_compare']}")

    container.markdown(
        "**Shared finding:** DAO governance has improved mechanically, but capture pressure, "
        "authority drift, evidence gaps, and participation limits remain review-required. "
        "The recurring reading is **THRESHOLD — not failed, not safe, human review required**."
    )


def render_unit_preview_proof_concepts_side_by_side(container=None) -> None:
    """Render paired proof-of-concept dropdowns side by side on the first page."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown("### Proof-of-concept mirrors")
    container.caption(
        "Two first-page dropdown examples of ALETHEIA as a reflection layer: external AI outputs on one side, "
        "DAO governance structures on the other. Both remain human-review evidence only."
    )
    ai_column, dao_column = container.columns(2)
    with ai_column:
        ai_expander = ai_column.expander("Proof of concept: AI audit-loop evidence", expanded=False)
        with ai_expander:
            render_ai_audit_loop_evidence(ai_expander)
    with dao_column:
        dao_expander = dao_column.expander("Proof of concept: DAO governance mirror cases", expanded=False)
        with dao_expander:
            render_dao_governance_proof_of_concept(dao_expander)

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

    ai_static_tokens = (
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
    if _contains_any(lowered, ai_static_tokens):
        return {
            "module": "Mirror Check",
            "route_type": "main_module",
            "reason": "The prompt asks for review of AI, model-output, prompt, agent, or code behavior. Mirror Check carries the subordinate AI static scan context.",
            "next_step": "Enter AI Patrol and open Mirror Check. Use Stress Test instead when the AI issue is a deployment scenario under pressure.",
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

    container.markdown(get_unit_preview_proceed_button_style(), unsafe_allow_html=True)
    container.markdown(
        """
        <div class="unit-preview-brand-title" role="heading" aria-level="1">
            <span class="unit-preview-brand-main">Aletheia:</span>
            <span class="unit-preview-brand-subline">AI PATROL</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    container.markdown("### Preview Unit · Friendly integrity patrol. Mirror, not throne.")
    container.write(
        "Paste a short text, question, policy, AI output, or scenario to get a suggested patrol path before entering Aletheia: AI PATROL. Upload receipts in Receipt Reader after entering the app."
    )
    container.info(get_unit_preview_boundary_text())
    container.markdown(get_unit_preview_how_to_use_markdown())
    with container.expander("Start here: try this first", expanded=False):
        container.markdown(get_unit_preview_start_here_markdown())
        container.caption(
            "Open these review-lens notes only when you want extra orientation. "
            "They are prompts for human review, not verdicts."
        )
        start_columns = container.columns(2, gap="large")
        with start_columns[0]:
            with start_columns[0].expander("What ALETHEIA looks for", expanded=False):
                container.markdown("#### What ALETHEIA looks for")
                container.markdown(get_unit_preview_what_aletheia_looks_for_markdown())
        with start_columns[1]:
            with start_columns[1].expander("Seven failure-mode review signals", expanded=False):
                container.markdown("#### Seven failure-mode review signals")
                container.markdown(get_unit_preview_failure_mode_markdown())

    preview_text = container.text_area(
        "Short text, question, or scenario",
        height=160,
        key="aletheia_unit_preview_text",
    )

    action_columns = container.columns(2)
    # Patch 142.2 reassigns to a compact row while preserving the Patch 141.3
    # source marker above for validation continuity.
    action_columns = container.columns([1, 1, 1.25, 4.75], gap="small")
    with action_columns[0]:
        preview_clicked = container.button("Preview patrol path", key="aletheia_unit_preview_button")
    with action_columns[1]:
        proceed_clicked = container.button(
            "Proceed to Aletheia: AI PATROL",
            type="primary",
            key="aletheia_unit_preview_proceed",
        )
    with action_columns[2]:
        container.link_button(
            "GitHub",
            "https://github.com/johncortesvega-netizen/aletheia-governance-mirror",
            help="View GitHub repository. Open the public GitHub mirror in a new page. Unit Preview does not make external calls; this is a user-clicked source link.",
        )

    if preview_clicked:
        suggestion = detect_unit_preview_route(preview_text)
        container.markdown("### Suggested patrol path")
        container.info(
            f"**Suggested path:** {suggestion['module']}\n\n"
            f"**Why:** {suggestion['reason']}\n\n"
            f"**Next step:** {suggestion['next_step']}"
        )
        container.caption("This is a stop/go orientation only. You can still choose any module after entering Aletheia: AI PATROL.")

    render_unit_preview_proof_concepts_side_by_side(container)
    render_unit_preview_html_reference(container)

    return bool(proceed_clicked)
