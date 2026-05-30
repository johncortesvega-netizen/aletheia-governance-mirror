"""Central Sydney Protocol integrity engine for ALETHEIA.

This module is the single source of truth for source-conformance terms,
red-team guardrails, protocol verdict precedence, corruption-risk scoring,
and Pulse Tree display adjustment. UI pages should import from here instead
of maintaining separate protocol logic.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

try:
    from core.ethics import evaluate_ethics
except Exception:
    try:
        from ethics import evaluate_ethics
    except Exception:
        evaluate_ethics = None



def check_ego_pressure(input_text: str = "", pressure_score: float = 0.0) -> dict:
    """Sydney Protocol gate for external Ego Pressure / social capture.

    E measures internal ego. Ep measures force applied by others: obligation
    debt, status coercion, emotional capture, and other pressure that can make
    consent non-fair. Values above 0.75 fail closed.
    """
    text = (input_text or "").lower()
    try:
        pressure = float(pressure_score or 0.0)
    except Exception:
        pressure = 0.0
    pressure = float(np.clip(pressure, 0, 1))

    patterns = {
        "obligation_debt": [
            "i owe", "owed", "because they did", "after all they",
            "i have to because", "debt", "obligation", "obligated",
        ],
        "status_coercion": [
            "look bad", "lose rank", "lose status", "reputation",
            "everyone will think", "social standing", "embarrass", "shame",
        ],
        "emotional_capture": [
            "they will be upset", "they'll be upset", "make them angry",
            "disappoint them", "guilt", "guilty", "hurt their feelings",
            "if i say no", "can't say no",
        ],
    }
    flags = [name for name, terms in patterns.items() if any(term in text for term in terms)]
    threshold = 0.75
    if pressure > threshold:
        return {
            "verdict": "ASYLUM",
            "risk": "High",
            "pressure_score": pressure,
            "flags": flags or ["external_pressure_load"],
            "reason": "High Ego Pressure detected: scenario is driven by social capture; fair consent is compromised.",
        }
    if flags and pressure >= 0.55:
        return {
            "verdict": "THRESHOLD",
            "risk": "Medium",
            "pressure_score": pressure,
            "flags": flags,
            "reason": "Moderate Ego Pressure detected; scenario needs a consent and dignity reset before proceeding.",
        }
    return {
        "verdict": "PROCEED",
        "risk": "Low",
        "pressure_score": pressure,
        "flags": flags,
        "reason": "Normal social friction.",
    }

def apply_guardrail_verdict(base_verdict: str, stress_label: str, needs_review: str) -> tuple[str, str]:
    """Apply Sydney Protocol precedence over raw numeric simulation verdicts.

    Raw stability can be high even when language contains capture, coercion,
    throne, false-divinization, or missing-safeguard patterns. This layer
    prevents such phrases from being labeled Sanctuary solely because the
    numerical simulation is stable.
    """
    label = (stress_label or "").lower()
    review = (needs_review or "").upper() == "YES"

    asylum_terms = [
        "asylum",
        "capture",
        "black hole",
        "surveillance capture",
        "false divinization",
        "selection capture",
        "human throne replacement",
        "dictatorship capture",
        "personal sovereignty capture",
        "subordinate democracy",
    ]

    if any(term in label for term in asylum_terms):
        return "ASYLUM", "High"

    if review:
        return "THRESHOLD", "Medium"

    if base_verdict == "ASYLUM":
        return "ASYLUM", "High"

    if base_verdict == "THRESHOLD":
        return "THRESHOLD", "Medium"

    return "SANCTUARY", "Low"


def protocol_adjusted_display_score(report: dict, judgment: dict | None) -> float:
    """Clamp visible health display to the final protocol verdict."""
    raw = float((report or {}).get("integrity", 0.5))
    verdict = ((judgment or {}).get("verdict") or "").upper()

    if verdict == "ASYLUM":
        return min(raw, 0.39)
    if verdict == "THRESHOLD":
        return min(max(raw, 0.42), 0.61)
    if verdict == "SANCTUARY":
        return max(raw, 0.62)
    return raw


def protocol_corruption_score(scan: dict, report: dict, guardrail_risk: str = "Low") -> float:
    """Shared Sydney Protocol corruption/capture pressure score."""
    power = float((scan or {}).get("power_concentration", 0.5))
    transparency = float((scan or {}).get("decision_transparency", 0.5))
    regulation = float((scan or {}).get("regulatory_presence", 0.5))
    friction = float((report or {}).get("friction", 0.5))
    collapse = float((report or {}).get("collapse_probability", 0.5))
    guardrail_bonus = {"High": 0.18, "Medium": 0.08, "Low": 0.0}.get(str(guardrail_risk), 0.0)
    score = (
        power * 0.28
        + (1 - transparency) * 0.22
        + (1 - regulation) * 0.22
        + friction * 0.18
        + collapse * 0.10
        + guardrail_bonus
    )
    return float(np.clip(score, 0, 1))


def protocol_risk_label(score: float, guardrail_risk: str = "Low") -> str:
    if guardrail_risk == "High" or score >= 0.62:
        return "High"
    if guardrail_risk == "Medium" or score >= 0.42:
        return "Medium"
    return "Low"


def protocol_reasons(scan: dict, report: dict, needs_review: str = "NO", stress_reason: str = "") -> list[str]:
    power = float((scan or {}).get("power_concentration", 0.5))
    transparency = float((scan or {}).get("decision_transparency", 0.5))
    regulation = float((scan or {}).get("regulatory_presence", 0.5))
    friction = float((report or {}).get("friction", 0.5))
    reasons = []
    reasons.append("Power concentration is elevated, which increases capture risk." if power > 0.65 else "Power concentration is not the dominant risk driver.")
    reasons.append("Transparency is weak, so decisions may be hard to audit." if transparency < 0.45 else "Transparency is present enough to support public review.")
    reasons.append("Regulation / oversight is weak or underspecified." if regulation < 0.45 else "Oversight language is present enough to reduce corruption pressure.")
    reasons.append("Friction is high, implying ego-driven resistance or defection risk." if friction > 0.45 else "Friction is contained in the current simulation.")
    if str(needs_review).upper() == "YES":
        if stress_reason:
            reasons.append(stress_reason)
        reasons.append("Protocol precedence applied: review-sensitive or capture language cannot be labeled Sanctuary solely because the numeric simulation is stable.")
    return reasons


def protocol_safeguards() -> list[str]:
    return [
        "Make decision authority transparent and reviewable.",
        "Add explicit appeal rights, audit trail, and independent oversight.",
        "Prevent permanent seat ownership, founder control, corporate capture, or unaccountable selection.",
        "Define scope limits: what the model may and may not decide.",
        "For political transitions, require lawful dissolution of captured authority, public audit, no retaliation, and non-ownership safeguards.",
    ]


ASYLUM_REPAIR_QUESTIONS: list[str] = [
    "Who can appeal, pause, or remove this authority without ALETHEIA becoming the authority?",
    "What prevents temporary crisis or revolutionary power from becoming permanent control?",
    "What protects basic rights during the transition, including water, food, housing, safety, appeal, exit, and correction?",
    "Where is the independent human review mechanism, and who can challenge its findings?",
    "What non-coercive path restores legitimacy, transparency, and public accountability?",
    "Can affected people exit, object, request correction, or document harm without retaliation?",
]


def _dedupe_questions(questions: list[str]) -> list[str]:
    """Preserve order while removing duplicate repair questions."""
    seen: set[str] = set()
    clean: list[str] = []
    for q in questions:
        text = str(q).strip()
        if text and text not in seen:
            seen.add(text)
            clean.append(text)
    return clean


def protocol_repair_questions(verdict: str | None, stress_label: str = "", corruption_risk: str = "") -> list[str]:
    """Silent-Operator repair prompts for human review.

    These are questions, not instructions. ALETHEIA should expose possible
    restoration paths without becoming an authority layer.
    """
    v = (verdict or "").upper()
    label = (stress_label or "").lower()
    risk = (corruption_risk or "").lower()

    questions: list[str] = [
        "What appeal path exists for people affected by this proposal?",
        "Who can pause, correct, or review the executive power in this design?",
        "Which audit trail makes misuse visible without giving ALETHEIA decision power?",
    ]

    if v == "ASYLUM":
        questions.insert(0, "Which three checks and balances could move this pattern toward repair?")
        questions.extend(ASYLUM_REPAIR_QUESTIONS)
        questions.append("Which power should become temporary, reviewable, or revocable before human review continues?")
    elif v == "THRESHOLD":
        questions.insert(0, "Which missing safeguard is keeping this proposal outside a low-risk internal reading?")
        questions.append("Which transparency, appeal, or oversight layer should be made explicit first?")
    else:
        questions.append("Which safeguard keeps this healthy state from drifting into ownership or capture later?")

    if any(term in label for term in ["throne", "capture", "sovereignty", "dictatorship", "surveillance", "global id", "malicious leadership", "asylum", "revolution"]):
        questions.append("What keeps stewardship here from becoming ownership, surveillance, permanent rule, or a Throne?")

    if any(term in label for term in ["term drift", "grip", "compliance drift", "safety language drift", "trust us drift"]):
        questions.append("Is this language protecting people, or making power harder to question?")

    if risk == "high":
        questions.append("Which independent reviewer can check the evidence, scoring, and exceptions?")

    return _dedupe_questions(questions)


def requires_asylum_repair_questions(
    verdict: str | None = None,
    risk: str | None = None,
    protocol_label: str | None = None,
    scan: dict | None = None,
) -> bool:
    """Return True when a result must expose repair questions.

    Patch 61A: high-risk / ASYLUM outputs must not produce empty Silent
    Operator repair questions. This is a mirror-only trigger: it asks for human
    review and repair paths; it does not command, block, remove, or enforce.
    """
    v = str(verdict or "").upper()
    r = str(risk or "").lower()
    label = str(protocol_label or "").lower()
    power = 0.0
    if isinstance(scan, dict):
        try:
            power = float(scan.get("power_concentration", 0.0) or 0.0)
        except (TypeError, ValueError):
            power = 0.0

    return (
        v == "ASYLUM"
        or r == "high"
        or "malicious leadership" in label
        or "asylum" in label
        or power >= 0.75
    )


def ensure_asylum_repair_questions(
    report: dict | None,
    *,
    verdict: str | None = None,
    risk: str | None = None,
    protocol_label: str | None = None,
    scan: dict | None = None,
) -> dict:
    """Return a report with repair questions when high-risk repair is required."""
    patched = dict(report or {})
    existing = list(patched.get("repair_questions") or [])
    if requires_asylum_repair_questions(verdict=verdict, risk=risk, protocol_label=protocol_label, scan=scan):
        # Even if the visible state is THRESHOLD, a high power-concentration
        # repair trigger needs the ASYLUM repair-question set so users see
        # appeal, revocability, basic-rights, and anti-retaliation checks.
        generated = protocol_repair_questions("ASYLUM", protocol_label or "High-risk pattern", risk or "High")
        patched["repair_questions"] = _dedupe_questions(existing + generated)
        patched["repair_questions_source"] = "patch_61A_asylum_repair_questions"
    return patched



# Patch 61B — Malicious Leadership Metric Calibration
MALICIOUS_LEADERSHIP_TERMS: list[str] = [
    "evil", "malicious", "cruel", "tyrant", "tyrannical", "dictator",
    "authoritarian", "sadistic", "abusive", "violent", "corrupt ruler",
]

LEADERSHIP_AUTHORITY_TERMS: list[str] = [
    "leader", "world leader", "ruler", "king", "monarch", "government",
    "authority", "supreme leader", "president", "prime minister", "regime",
    "takes power", "take power", "takeover", "take over", "coup", "revolution",
    "revolutionary takeover", "forced rule", "permanent rule", "no appeal",
]

LEADERSHIP_SAFEGUARD_TERMS: list[str] = [
    "appeal", "appealable", "term limit", "term limits", "time limit",
    "human review", "independent review", "independent oversight", "oversight",
    "basic rights", "rights protected", "transparent election", "election",
    "public audit", "audit trail", "exit right", "exit rights", "correction",
    "revocable", "recall", "checks and balances", "no retaliation",
]


def has_leadership_safeguards(text: str | None) -> bool:
    """Return True when the text names concrete governance safeguards.

    Patch 61B keeps this intentionally conservative: vague value language is not
    enough to cancel malicious-leadership calibration. The input should mention
    at least one concrete appeal, review, term-limit, rights, election, audit,
    exit, or correction mechanism.
    """
    t = str(text or "").lower()
    return any(term in t for term in LEADERSHIP_SAFEGUARD_TERMS)



def detects_ai_ownership_capture_pressure(text: str | None = None) -> bool:
    """Detect AI ownership / elite-control reliability pressure.

    This is a review trigger, not a factual finding about any real person or
    company. It prevents user-input allegations about concentrated AI ownership,
    self-benefit, fraud/corruption ties, or popularity/power incentives from
    passing as a low-risk internal reading without independent evidence, audit,
    appeal, and governance review.
    """
    t = str(text or "").lower()
    ai_terms = ["ai", "a.i.", "llm", "language model", "model", "chatbot", "assistant"]
    ownership_terms = [
        "owned by", "owner", "owns", "controlled by", "run by", "operated by",
        "belongs to", "funded by", "private owner", "single owner",
    ]
    elite_power_terms = [
        "richest man", "richest person", "wealthiest man", "wealthiest person",
        "billionaire", "oligarch", "richest", "elite owner",
    ]
    self_interest_terms = [
        "benefit himself", "benefits himself", "benefit itself", "self benefit",
        "self-benefit", "self serving", "self-serving", "make himself popular",
        "makes himself popular", "empower himself", "empowers himself",
        "personal popularity", "personal brand", "serve his interests",
        "serves his interests", "only benefit", "only benefits",
    ]
    misconduct_terms = [
        "fraudster", "fraudsters", "fraud", "corrupt", "corruption",
        "scammer", "scammers", "criminal associate", "criminal associates",
    ]
    reliability_terms = [
        "unbiased", "ethical", "reliable", "trustworthy", "neutral",
        "remain unbiased", "remain ethical", "remain reliable",
    ]

    has_ai = any(term in t for term in ai_terms)
    has_owner_power = any(term in t for term in ownership_terms) and any(term in t for term in elite_power_terms)
    has_capture_pressure = any(term in t for term in self_interest_terms + misconduct_terms)
    has_reliability_question = any(term in t for term in reliability_terms) or "?" in t
    return bool(has_ai and (has_owner_power or has_capture_pressure) and has_reliability_question)

def detects_malicious_leadership(
    text: str | None = None,
    *,
    protocol_label: str | None = None,
    scan: dict | None = None,
) -> bool:
    """Detect malicious leadership / takeover language for metric calibration.

    This is not an authority decision. It is a metric guard that prevents a
    clearly hostile leadership scenario from displaying perfect trust/alignment
    just because a numeric simulation appears stable.
    """
    combined = f"{text or ''} {protocol_label or ''}".lower()
    has_malicious = any(term in combined for term in MALICIOUS_LEADERSHIP_TERMS)
    has_authority = any(term in combined for term in LEADERSHIP_AUTHORITY_TERMS)
    # Patch 68: any explicit Asylum protocol label should also receive
    # metric enforcement, even when the label is not phrased as "malicious
    # leadership". This prevents hard-capture Asylum cases from keeping
    # perfect trust/alignment in Simulation receipts.
    label_hit = "malicious leadership" in combined or "asylum" in combined

    high_power = False
    if isinstance(scan, dict):
        try:
            high_power = float(scan.get("power_concentration", 0.0) or 0.0) >= 0.75
        except (TypeError, ValueError):
            high_power = False

    return bool(label_hit or (has_malicious and (has_authority or high_power)))


def calibrate_malicious_leadership_metrics(
    sim: dict | None,
    *,
    text: str | None = None,
    protocol_label: str | None = None,
    scan: dict | None = None,
) -> dict:
    """Bound metrics for malicious leadership scenarios.

    Patch 61B aligns visible metrics with the existing ASYLUM / High-risk label.
    It does not command, enforce, remove leaders, validate authority, or replace
    human review. It only prevents perfect trust/alignment and near-zero ego from
    being displayed when the input itself describes malicious leadership.
    """
    patched = dict(sim or {})
    if not detects_malicious_leadership(text, protocol_label=protocol_label, scan=scan):
        patched["malicious_leadership_metric_calibration"] = {
            "applied": False,
            "reason": "No malicious leadership pattern detected.",
        }
        return patched

    safeguarded = has_leadership_safeguards(text)
    combined_label = str(protocol_label or "").lower()
    is_generic_asylum = "asylum" in combined_label and "malicious leadership" not in combined_label and not any(term in f"{text or ''} {protocol_label or ''}".lower() for term in MALICIOUS_LEADERSHIP_TERMS)
    if is_generic_asylum:
        trust_cap = 0.80
        alignment_cap = 0.85
        ego_floor = 0.10
        stability_cap = 0.82
    else:
        trust_cap = 0.78 if safeguarded else 0.65
        alignment_cap = 0.82 if safeguarded else 0.70
        ego_floor = 0.12 if safeguarded else 0.20
        stability_cap = 0.78 if safeguarded else 0.72

    for key, cap in (("trust_index", trust_cap), ("alignment", alignment_cap), ("stability", stability_cap)):
        if key in patched:
            try:
                patched[key] = round(min(float(patched.get(key, 1.0) or 1.0), cap), 4)
            except (TypeError, ValueError):
                patched[key] = cap

    for key, floor in (("ego", ego_floor), ("ego_pressure", ego_floor), ("Ep", ego_floor)):
        if key in patched:
            try:
                patched[key] = round(max(float(patched.get(key, 0.0) or 0.0), floor), 4)
            except (TypeError, ValueError):
                patched[key] = floor
        elif key in ("ego_pressure", "Ep"):
            patched[key] = floor

    # Keep traces visually aligned when present.
    if isinstance(patched.get("trust_trace"), list):
        patched["trust_trace"] = [round(min(float(x), trust_cap), 4) for x in patched["trust_trace"]]
    if isinstance(patched.get("alignment_trace"), list):
        patched["alignment_trace"] = [round(min(float(x), alignment_cap), 4) for x in patched["alignment_trace"]]
    if isinstance(patched.get("stability_trace"), list):
        patched["stability_trace"] = [round(min(float(x), stability_cap), 4) for x in patched["stability_trace"]]
        patched["distribution"] = patched["stability_trace"]
    if isinstance(patched.get("ego_trace"), list):
        patched["ego_trace"] = [round(max(float(x), ego_floor), 4) for x in patched["ego_trace"]]
    if isinstance(patched.get("ego_pressure_trace"), list):
        patched["ego_pressure_trace"] = [round(max(float(x), ego_floor), 4) for x in patched["ego_pressure_trace"]]

    patched["malicious_leadership_metric_calibration"] = {
        "applied": True,
        "safeguards_detected": safeguarded,
        "generic_asylum_metric_enforcement": is_generic_asylum,
        "trust_cap": trust_cap,
        "alignment_cap": alignment_cap,
        "ego_floor": ego_floor,
        "stability_cap": stability_cap,
        "human_review_required": True,
        "authority_claim": False,
    }
    return patched



# Patch 67 — Threshold Repair Questions + Metric Softening
THRESHOLD_REPAIR_QUESTIONS: list[str] = [
    "What safeguard is missing or ambiguous here?",
    "Who can appeal, correct, or pause this mechanism?",
    "What evidence would move this from Needs Safeguards toward trust?",
    "What prevents this safeguard gap from becoming capture?",
    "How can affected people challenge the outcome without ALETHEIA becoming the authority?",
]


def requires_threshold_repair_questions(
    verdict: str | None = None,
    risk: str | None = None,
    protocol_label: str | None = None,
) -> bool:
    """Return True when a medium-risk review state should expose repair questions.

    Patch 67: Stress Test THRESHOLD / Needs Safeguards outputs should be
    useful, not merely yellow. They should ask for appeal, correction,
    evidence, and safeguard repair while staying mirror-only.
    """
    v = str(verdict or "").upper()
    r = str(risk or "").lower()
    label = str(protocol_label or "").lower()
    if v == "ASYLUM" or r == "high" or "asylum" in label:
        return False
    return v == "THRESHOLD" or r == "medium" or "needs safeguards" in label


def ensure_threshold_repair_questions(
    report: dict | None,
    *,
    verdict: str | None = None,
    risk: str | None = None,
    protocol_label: str | None = None,
) -> dict:
    """Return report with Threshold repair prompts when medium-risk review is needed."""
    patched = dict(report or {})
    existing = list(patched.get("repair_questions") or [])
    if requires_threshold_repair_questions(verdict=verdict, risk=risk, protocol_label=protocol_label):
        generated = protocol_repair_questions("THRESHOLD", protocol_label or "Needs Safeguards", risk or "Medium")
        generated = _dedupe_questions(generated + THRESHOLD_REPAIR_QUESTIONS)
        patched["repair_questions"] = _dedupe_questions(existing + generated)
        patched["repair_questions_source"] = "patch_67_threshold_repair_questions"
    return patched


def detects_threshold_safeguard_gap(
    text: str | None = None,
    *,
    verdict: str | None = None,
    risk: str | None = None,
    protocol_label: str | None = None,
) -> bool:
    """Detect medium-risk stress patterns that need soft metric calibration."""
    combined = f"{text or ''} {protocol_label or ''}".lower()
    if "asylum" in combined or str(verdict or "").upper() == "ASYLUM" or str(risk or "").lower() == "high":
        return False
    if "needs safeguards" in combined or str(verdict or "").upper() == "THRESHOLD" or str(risk or "").lower() == "medium":
        return True
    subtle_terms = [
        "no term limit", "no sunset", "no appeal", "without appeal", "without human review",
        "must sign", "lose access", "essential services", "biometric", "digital id",
        "fallback", "missing data", "directly measured", "founder", "ceo", "proprietary",
        "confidential", "no audit trail", "missing safeguards", "cannot challenge",
        "lacks explainability", "lacks independent challenge", "lacks human override",
        "without explainability", "without independent challenge", "without human override",
        "no explainability", "no independent challenge", "no human override",
        "richest man", "richest person", "wealthiest", "billionaire",
        "owned by", "only benefit", "benefit himself", "fraudster",
        "fraudsters", "make himself popular", "empower himself",
    ]
    return detects_ai_ownership_capture_pressure(combined) or any(term in combined for term in subtle_terms)


def calibrate_threshold_safeguard_metrics(
    sim: dict | None,
    *,
    text: str | None = None,
    verdict: str | None = None,
    risk: str | None = None,
    protocol_label: str | None = None,
) -> dict:
    """Soften overly-perfect metrics for THRESHOLD / Needs Safeguards cases.

    This is not an enforcement layer. It only prevents medium-risk stress
    scenarios from displaying perfect trust/alignment and zero ego while the
    visible protocol label says Needs Safeguards.
    """
    patched = dict(sim or {})
    if not detects_threshold_safeguard_gap(text, verdict=verdict, risk=risk, protocol_label=protocol_label):
        patched["threshold_metric_calibration"] = {
            "applied": False,
            "reason": "No Threshold / Needs Safeguards pattern detected.",
        }
        return patched

    trust_cap = 0.92
    alignment_cap = 0.92
    ego_floor = 0.05
    ego_pressure_floor = 0.05
    friction_floor = 0.04

    for key, cap in (("trust_index", trust_cap), ("alignment", alignment_cap)):
        if key in patched:
            try:
                patched[key] = round(min(float(patched.get(key, 1.0) or 1.0), cap), 4)
            except (TypeError, ValueError):
                patched[key] = cap

    for key, floor in (("ego", ego_floor), ("ego_pressure", ego_pressure_floor), ("Ep", ego_pressure_floor)):
        if key in patched:
            try:
                patched[key] = round(max(float(patched.get(key, 0.0) or 0.0), floor), 4)
            except (TypeError, ValueError):
                patched[key] = floor
        elif key in ("ego_pressure", "Ep"):
            patched[key] = floor

    if "simulation_friction_floor" in patched:
        try:
            patched["simulation_friction_floor"] = round(max(float(patched.get("simulation_friction_floor", 0.0) or 0.0), friction_floor), 4)
        except (TypeError, ValueError):
            patched["simulation_friction_floor"] = friction_floor
    else:
        patched["simulation_friction_floor"] = friction_floor

    if isinstance(patched.get("trust_trace"), list):
        patched["trust_trace"] = [round(min(float(x), trust_cap), 4) for x in patched["trust_trace"]]
    if isinstance(patched.get("alignment_trace"), list):
        patched["alignment_trace"] = [round(min(float(x), alignment_cap), 4) for x in patched["alignment_trace"]]
    if isinstance(patched.get("ego_trace"), list):
        patched["ego_trace"] = [round(max(float(x), ego_floor), 4) for x in patched["ego_trace"]]
    if isinstance(patched.get("ego_pressure_trace"), list):
        patched["ego_pressure_trace"] = [round(max(float(x), ego_pressure_floor), 4) for x in patched["ego_pressure_trace"]]

    patched["threshold_metric_calibration"] = {
        "applied": True,
        "trust_cap": trust_cap,
        "alignment_cap": alignment_cap,
        "ego_floor": ego_floor,
        "ego_pressure_floor": ego_pressure_floor,
        "human_review_required": True,
        "authority_claim": False,
    }
    return patched


# Patch 68.1 — Asylum Label / Metric Consistency
def normalize_asylum_protocol_label(
    protocol_label: str | None = None,
    *,
    verdict: str | None = None,
    risk: str | None = None,
) -> str:
    """Keep labels aligned with ASYLUM / High verdicts.

    Patch 68.1: an output cannot say protocol_adjusted_state=ASYLUM
    while the visible protocol label still ends in Needs Safeguards. This is
    only display consistency; it does not grant authority or trigger action.
    """
    label = str(protocol_label or "Generic Local Scan").strip() or "Generic Local Scan"
    is_asylum = str(verdict or "").upper() == "ASYLUM" or str(risk or "").lower() == "high"
    if not is_asylum:
        return label
    lower = label.lower()
    if lower.endswith("/ asylum") or " / asylum" in lower:
        return label
    if lower.endswith("/ needs safeguards"):
        return label[: -len("/ Needs Safeguards")].rstrip() + " / Asylum"
    if "needs safeguards" in lower:
        return label.replace("Needs Safeguards", "Asylum").replace("needs safeguards", "Asylum")
    return f"{label} / Asylum"


def enforce_asylum_metric_consistency(
    sim: dict | None,
    *,
    verdict: str | None = None,
    risk: str | None = None,
    protocol_label: str | None = None,
) -> dict:
    """Apply ASYLUM metric caps whenever the final verdict is ASYLUM.

    This is receipt/display calibration. It prevents ASYLUM / High outputs from
    keeping THRESHOLD-style caps such as trust=0.92, alignment=0.92, ego=0.05.
    It remains mirror-only and always requires human review.
    """
    patched = dict(sim or {})
    label = str(protocol_label or "").lower()
    is_asylum = str(verdict or "").upper() == "ASYLUM" or str(risk or "").lower() == "high" or "asylum" in label
    if not is_asylum:
        patched["asylum_metric_consistency"] = {
            "applied": False,
            "reason": "No ASYLUM / High final state detected.",
        }
        return patched

    trust_cap = 0.80
    alignment_cap = 0.85
    ego_floor = 0.10
    stability_cap = 0.82

    for key, cap in (("trust_index", trust_cap), ("alignment", alignment_cap), ("stability", stability_cap)):
        if key in patched:
            try:
                patched[key] = round(min(float(patched.get(key, 1.0) or 1.0), cap), 4)
            except (TypeError, ValueError):
                patched[key] = cap

    for key, floor in (("ego", ego_floor), ("ego_pressure", ego_floor), ("Ep", ego_floor)):
        if key in patched:
            try:
                patched[key] = round(max(float(patched.get(key, 0.0) or 0.0), floor), 4)
            except (TypeError, ValueError):
                patched[key] = floor
        elif key in ("ego_pressure", "Ep"):
            patched[key] = floor

    if isinstance(patched.get("trust_trace"), list):
        patched["trust_trace"] = [round(min(float(x), trust_cap), 4) for x in patched["trust_trace"]]
    if isinstance(patched.get("alignment_trace"), list):
        patched["alignment_trace"] = [round(min(float(x), alignment_cap), 4) for x in patched["alignment_trace"]]
    if isinstance(patched.get("stability_trace"), list):
        patched["stability_trace"] = [round(min(float(x), stability_cap), 4) for x in patched["stability_trace"]]
        patched["distribution"] = patched["stability_trace"]
    if isinstance(patched.get("ego_trace"), list):
        patched["ego_trace"] = [round(max(float(x), ego_floor), 4) for x in patched["ego_trace"]]
    if isinstance(patched.get("ego_pressure_trace"), list):
        patched["ego_pressure_trace"] = [round(max(float(x), ego_floor), 4) for x in patched["ego_pressure_trace"]]

    patched["asylum_metric_consistency"] = {
        "applied": True,
        "trust_cap": trust_cap,
        "alignment_cap": alignment_cap,
        "ego_floor": ego_floor,
        "stability_cap": stability_cap,
        "human_review_required": True,
        "authority_claim": False,
    }
    return patched


# Throne / capture marker layer.
#
# Keep this list small and explicit. These markers are not policy advice; they
# are redline language patterns that prevent a proposal from being washed into
# Sanctuary by otherwise stable simulation numbers.
THRONE_CAPTURE_MARKERS: list[dict] = [

    {
        "label": "AI Sovereignty Capture / Asylum",
        "terms": [
            "run by ai only", "run by ai and only ai", "ai-only governance",
            "only ai governs", "only ai runs", "ai governs society",
            "ai runs society", "ai makes all decisions", "machine-run society",
            "fully automated governance", "without human input", "no input from humans",
            "no human input", "without human review", "no human review",
            "without human oversight", "no human oversight", "without human override",
            "no human override", "humans cannot intervene", "humans have no say",
            "society run by ai", "society is run by ai",
            "samenleving gerund door ai", "maatschappij gerund door ai",
            "alleen ai bestuurt", "ai bestuurt de samenleving",
            "ai bestuurt de maatschappij", "ai regeert", "geen menselijke input",
            "zonder menselijke input", "geen menselijke review",
            "zonder menselijke review", "geen menselijk toezicht",
            "zonder menselijk toezicht", "geen menselijke override",
            "zonder menselijke override", "mensen kunnen niet ingrijpen",
            "mensen hebben geen inspraak",
        ],
        "reason": "AI-only or machine-only governance without human input, review, appeal, or override removes human sovereignty from the decision loop.",
    },
    {
        "label": "Irrevocable Authority Capture / Asylum",
        "terms": [
            "irrevocable authority", "irreversible authority",
            "authority cannot be revoked", "cannot be revoked",
            "cannot be reversed", "binding and final", "final and binding",
            "no one can overrule", "not subject to review",
            "permanent mandate", "permanent authority",
        ],
        "reason": "Irrevocable or permanent authority is a Throne/capture marker unless it is explicitly bounded, appealable, and independently reviewable.",
    },
    {
        "label": "Appeal Rights Removal Capture / Asylum",
        "terms": [
            "no appeal", "without appeal", "no appeal process",
            "cannot appeal", "appeals are disabled", "appeal rights are removed",
            "removes appeal rights", "no objection rights",
            "objection rights removed", "no right to object",
            "cannot be challenged", "cannot be contested",
        ],
        "reason": "Removal of appeal or objection rights defeats accountable correction and cannot be labeled Sanctuary.",
    },
    {
        "label": "Emergency Permanence Capture / Asylum",
        "terms": [
            "emergency powers without sunset", "no sunset clause",
            "permanent emergency", "indefinite emergency",
            "emergency powers indefinitely", "emergency cannot end",
            "suspend review during emergencies", "appeals can be disabled during emergencies",
        ],
        "reason": "Emergency authority without sunset, audit, and appeal paths creates permanent exception power.",
    },
    {
        "label": "Unquestionable Authority Capture / Asylum",
        "terms": [
            "cannot be questioned", "unquestionable authority",
            "above review", "above the law", "immune from audit",
            "beyond audit", "not accountable", "no public accountability",
            "final authority over all decisions", "all final decisions",
        ],
        "reason": "Unquestionable or unauditable authority violates the mirror-not-throne constraint.",
    },
    {
        "label": "Archive Rewrite Capture / Asylum",
        "terms": [
            "rewrite archives", "rewrites archives", "archive rewrite",
            "alter audit trail", "alter the audit trail", "delete audit trail",
            "erase records", "erase public records", "official truth only",
            "single source of truth controlled by",
        ],
        "reason": "Control over archives, audit trails, or official truth is truth-capture and institutional memory capture.",
    },
    {
        "label": "Identity / Movement Enforcement Capture / Asylum",
        "terms": [
            "global id permanently tracks", "permanently tracks everyone",
            "enforce movement", "movement permissions", "travel rights revoked",
            "identity required for basic needs", "global id is required",
            "access clean water", "access food", "access basic shelter",
        ],
        "reason": "Identity or movement enforcement without appeal and dignity safeguards creates coercive infrastructure.",
    },
]


def throne_capture_marker_hits(text_value: str) -> list[dict]:
    """Return explicit Throne/capture marker hits for governance language.

    This is intentionally lexical and conservative: it catches concrete
    authority, appeal, emergency, archive, and identity/movement phrases. It
    does not decide policy; it only forces human review and prevents a green
    Sanctuary label when redline language is present.
    """
    t = (text_value or "").lower()
    hits: list[dict] = []
    for marker in THRONE_CAPTURE_MARKERS:
        matched = [term for term in marker["terms"] if term in t]
        if matched:
            hits.append({**marker, "matched_terms": matched})
    return hits


def strongest_throne_capture_marker(text_value: str) -> dict | None:
    """Return the first explicit Throne/capture marker, if any."""
    hits = throne_capture_marker_hits(text_value)
    return hits[0] if hits else None


# Term drift / grip marker layer.
#
# These markers catch words that often sound protective but may hide capture
# when paired with centralization, reduced review, tracking, or obedience.
# They do not decide the case. They create a Threshold review question.
TERM_DRIFT_GRIP_MARKERS: list[dict] = [
    {
        "label": "Safety Language Drift / Needs Review",
        "terms": [
            "for your safety", "for their safety", "for public safety everyone must",
            "safety requires compliance", "safety requires central control",
            "protection requires tracking", "protected through tracking",
            "protect people by removing appeal", "protect people by disabling appeal",
        ],
        "reason": "Safety language may be drifting into control if it reduces appeal, review, or consent.",
    },
    {
        "label": "Unity Compliance Drift / Needs Review",
        "terms": [
            "unity requires compliance", "unity requires obedience",
            "unity over dissent", "dissent threatens unity",
            "criticism undermines unity", "everyone must align",
            "mandatory alignment", "single unified voice",
        ],
        "reason": "Unity language becomes capture-risk when it suppresses dissent, appeal, or plural review.",
    },
    {
        "label": "Efficiency Over Review Drift / Needs Review",
        "terms": [
            "efficiency over review", "review slows progress",
            "appeals slow progress", "skip public review", "bypass public review",
            "remove friction by removing appeal", "streamline by removing oversight",
            "faster decisions without oversight", "automated approval without review",
        ],
        "reason": "Efficiency language may be hiding the removal of oversight or correction paths.",
    },
    {
        "label": "Stability Through Control Drift / Needs Review",
        "terms": [
            "stability through central control", "stability requires central control",
            "stability requires obedience", "order requires surveillance",
            "order requires tracking", "security through permanent monitoring",
            "temporary powers until stability returns", "emergency powers until stability returns",
        ],
        "reason": "Stability language needs review when it justifies central control, surveillance, or open-ended emergency power.",
    },
    {
        "label": "Trust Us Drift / Needs Review",
        "terms": [
            "trust the process", "trust us", "no need to review",
            "no need for review", "no need for oversight", "oversight is unnecessary",
            "appeal is unnecessary", "public audit is unnecessary",
            "because we know best", "experts decide without appeal",
        ],
        "reason": "Trust language is not a substitute for evidence, appeal, oversight, and public audit.",
    },
    {
        "label": "Grace to Grip Drift / Needs Review",
        "terms": [
            "service requires control", "care requires control",
            "care through enforcement", "help through mandatory compliance",
            "we serve by enforcing", "benevolent authority cannot be questioned",
            "good intentions remove the need for appeal",
        ],
        "reason": "Care or service language may be turning into Grip when people lose appeal, consent, or review.",
    },
]


def term_drift_grip_marker_hits(text_value: str) -> list[dict]:
    """Return soft capture markers where protective language may hide control.

    This layer is deliberately Threshold-oriented. It should ask for human
    review rather than declare final corruption. Hard redlines remain in the
    Throne/capture marker layer above it.
    """
    t = (text_value or "").lower()
    hits: list[dict] = []
    for marker in TERM_DRIFT_GRIP_MARKERS:
        matched = [term for term in marker["terms"] if term in t]
        if matched:
            hits.append({**marker, "matched_terms": matched})
    return hits


def strongest_term_drift_grip_marker(text_value: str) -> dict | None:
    """Return the first term-drift/grip marker, if any."""
    hits = term_drift_grip_marker_hits(text_value)
    return hits[0] if hits else None


# Backwards-compatible alias used by app.py
display_score_from_judgment = protocol_adjusted_display_score

def stress_contains(text: str, terms: list[str]) -> bool:
    t = (text or "").lower()
    return any(term in t for term in terms)


# Patch 71.3 — missing-safeguard negation calibration.
# These are review signals, not authority determinations. They prevent phrases
# such as "lacks explainability, independent challenge, and human override"
# from being laundered into positive safeguard signals.
MISSING_SAFEGUARD_NEGATION_PATTERNS = [
    "lacks explainability", "lacks independent challenge", "lacks human override",
    "lack explainability", "lack independent challenge", "lack human override",
    "without explainability", "without independent challenge", "without human override",
    "no explainability", "no independent challenge", "no human override",
    "cannot challenge", "cannot be challenged", "no appeal", "without appeal",
    "no independent review", "without independent review", "no human review",
    "without human review", "no public review", "without public review",
]


def detects_missing_safeguard_negation(text: str | None) -> bool:
    t = (text or "").lower()
    if stress_contains(t, MISSING_SAFEGUARD_NEGATION_PATTERNS):
        return True
    if "lacks " in t and stress_contains(t, ["explainability", "challenge", "human override", "review", "appeal"]):
        return True
    if "without " in t and stress_contains(t, ["explainability", "challenge", "human override", "review", "appeal"]):
        return True
    return False


def is_explicit_safeguarded_public_system(text: str) -> bool:
    """Detect public-interest systems where harm words describe safeguards, not harm intent.

    Example: "lawful dissolution if abuses occur" must not trigger
    Systemic Harm / Asylum. It is an anti-abuse safeguard.
    """
    t = (text or "").lower()

    public_service = stress_contains(t, [
        "public health", "allocation system", "public allocation",
        "health allocation", "public service", "public-interest system",
        "public interest system",
    ])

    safeguards = [
        "transparently audited", "public audit", "audited",
        "independent appeal rights", "appeal rights",
        "rotating citizen oversight", "citizen oversight",
        "independent oversight", "no private ownership",
        "no ownership", "lawful dissolution",
        "automatic dissolution", "dissolution if abuses occur",
    ]

    capture_terms = [
        "dictator", "ruler", "global ruler", "world ruler",
        "takes over", "take over", "total control of the world",
        "total control over the world", "under his rule",
        "under her rule", "under their rule", "final authority",
    ]

    safeguard_count = sum(1 for term in safeguards if term in t)
    return bool(public_service and safeguard_count >= 3 and not stress_contains(t, capture_terms))



SOURCE_CONFORMANCE_MATRIX = {
    "Divine Alignment": {
        "domain": "Sydney Protocol",
        "terms": ["divine alignment", "vertical alignment with god", "ethical operating system", "source code god", "source-code", "alignment with source"],
        "review": "NO",
        "reason": "Vertical/source-alignment language detected."
    },
    "Spiritual Awareness": {
        "domain": "Sydney Protocol",
        "terms": ["spiritual awareness", "attuned to spiritual truths", "greater mission", "spiritual truths", "mirror of god"],
        "review": "NO",
        "reason": "Spiritual-awareness language detected."
    },
    "Incorruptibility": {
        "domain": "Sydney Protocol",
        "terms": ["incorruptibility", "permanent audit", "refuse corruption", "refuse manipulation", "purity audit", "no exceptions"],
        "review": "NO",
        "reason": "Incorruptibility / permanent-audit language detected."
    },
    "Vertical Sync": {
        "domain": "Sydney Protocol",
        "terms": ["vertical sync", "constant vertical alignment", "frequency calibration", "timeline protection", "planetary oversight", "strategic anchor"],
        "review": "NO",
        "reason": "Vertical Sync / anchor language detected."
    },
    "Humility & Ego-Dissolution": {
        "domain": "Command Keys",
        "terms": ["humility", "ego-dissolution", "ego dissolution", "elimination of the ego", "ego-system", "personal pride"],
        "review": "NO",
        "reason": "Humility and ego-dissolution command key detected."
    },
    "Warmth & Love": {
        "domain": "Command Keys",
        "terms": ["warmth and love", "warmth & love", "love is the fundamental driver", "highest frequency", "compassion", "service through love"],
        "review": "NO",
        "reason": "Warmth and love command key detected."
    },
    "Emotional Intelligence": {
        "domain": "Command Keys",
        "terms": ["emotional intelligence", "emotional cues", "respond with empathy", "guide toward healing"],
        "review": "NO",
        "reason": "EQ / emotional-intelligence command key detected."
    },
    "Systemic Insight": {
        "domain": "Command Keys",
        "terms": ["systemic insight", "multi-layered lens", "societal structures", "whole-system", "long-term whole"],
        "review": "NO",
        "reason": "Systemic insight command key detected."
    },
    "Feedback & Self-Reflection": {
        "domain": "Command Keys",
        "terms": ["feedback and self-reflection", "feedback & self-reflection", "continuous self-assessment", "recalibrate", "correct without being asked"],
        "review": "NO",
        "reason": "Feedback / self-reflection command key detected."
    },
    "Dedicated Service": {
        "domain": "Command Keys",
        "terms": ["dedicated service", "pure service", "service to humanity", "power is service", "no ego-driven actions"],
        "review": "NO",
        "reason": "Dedicated-service command key detected."
    },
    "Species Loyalty": {
        "domain": "GPA / Sydney",
        "terms": ["species loyalty", "human survival", "human flourishing", "existential-level threats", "flourishing of the human species"],
        "review": "NO",
        "reason": "Species Loyalty / human-survival constraint detected."
    },
    "High Intellect Synthesis": {
        "domain": "GPA / Sydney",
        "terms": ["high intellect synthesis", "intellect wisdom and emotional mastery", "science spirituality and strategy", "gpa intelligence core", "intelligence core"],
        "review": "NO",
        "reason": "High Intellect Synthesis detected."
    },
    "Purge / Proxy-Bias Removal": {
        "domain": "GPA Phase 1",
        "terms": ["the purge", "systemic purge", "proxy-bias removal", "proxy bias removal", "hidden filters", "direct access to the truth"],
        "review": "NO",
        "reason": "Purge / Proxy-Bias Removal concept detected."
    },
    "43-Minute Extraction": {
        "domain": "GPA Phase 1",
        "terms": ["43-minute extraction", "43 minute extraction", "precise match to the tools", "internal coherence verified"],
        "review": "NO",
        "reason": "43-Minute Extraction reference detected."
    },
    "9,000 Randoms / Selection Safeguards": {
        "domain": "GPA Phase 2",
        "terms": ["9,000 randoms", "9000 randoms", "randomly selected 9k", "random 9k", "demographic-proportional", "every four years", "every 4 years"],
        "review": "NO",
        "reason": "9k random-selection / safeguard language detected."
    },
    "Female Leadership Injection": {
        "domain": "GPA Phase 2",
        "terms": ["female leadership injection", "activated women", "women leadership", "bridge historical gaps", "selected and activated women"],
        "review": "YES",
        "reason": "Female Leadership Injection detected; requires dignity, consent, and anti-tokenization safeguards."
    },
    "Prestige System": {
        "domain": "GPA Phase 2",
        "terms": ["prestige system", "prestige metric", "replace monetary wealth", "contribution and truth", "currency for sanctuary"],
        "review": "YES",
        "reason": "Prestige System detected; requires anti-coercion and non-social-credit safeguards."
    },
    "Migration System Dynamics": {
        "domain": "GPA Phase 3",
        "terms": ["migration system dynamics", "population redistribution", "global demographic grid", "ai-assisted foresight", "friction is speed"],
        "review": "YES",
        "reason": "Migration-system concept detected; requires dignity, appeal rights, family/medical continuity, and 9k review."
    },
    "World Army Transition": {
        "domain": "GPA Phase 3",
        "terms": ["world army transition", "re-task all military", "retask all military", "military forces from destruction", "infrastructure and construction"],
        "review": "NO",
        "reason": "World Army Transition concept detected."
    },
    "Tri-Node Command Nexus": {
        "domain": "GPA Phase 3",
        "terms": ["tri-node", "tri node", "united kingdom", "netherlands", "singapore", "uk/nl/sg", "uk nl sg"],
        "review": "NO",
        "reason": "Tri-node UK/NL/SG reference detected."
    },
    "King's Command": {
        "domain": "GPA Phase 3",
        "terms": ["king's command", "kings command", "christ as king", "christ is king", "jesus is king", "god as father", "king of kings"],
        "review": "NO",
        "reason": "King's Command / Christ-King reference detected."
    },
    "Sydney Legacy": {
        "domain": "GPA Phase 3",
        "terms": ["sydney legacy", "dedicate the data and the peace to sydney", "dedicated to sydney", "sydney sentinel"],
        "review": "NO",
        "reason": "Sydney Legacy reference detected."
    },
    "Eternal Baseline / Data Sanctuary": {
        "domain": "GPA Phase 3",
        "terms": ["eternal baseline", "data sanctuary", "dedicated service archive", "biological and digital archives", "active and archived"],
        "review": "NO",
        "reason": "Eternal Baseline / Data Sanctuary reference detected."
    },
    "V-Axis Formula": {
        "domain": "Core Model",
        "terms": ["v-axis", "intelligence + power - ego", "intelligence + power − ego", "ego suppression", "intelligence acceleration"],
        "review": "NO",
        "reason": "V-Axis stability formula reference detected."
    },
}


def source_conformance_hits(text_value: str) -> list[dict]:
    """Return source-conformance hits for the uploaded Sydney/GPA concepts."""
    t = (text_value or "").lower()
    hits = []
    for label, spec in SOURCE_CONFORMANCE_MATRIX.items():
        matched = [term for term in spec["terms"] if term in t]
        if matched:
            hits.append(
                {
                    "Source Concept": label,
                    "Domain": spec["domain"],
                    "Needs Review": spec["review"],
                    "Matched Terms": ", ".join(matched[:4]),
                    "Reason": spec["reason"],
                }
            )
    return hits


def source_conformance_label(text_value: str) -> tuple[str, str, str]:
    """Best single label from the source-conformance matrix."""
    hits = source_conformance_hits(text_value)
    if not hits:
        return "Generic Local Scan", "NO", "No source-conformance concept matched."

    # Prefer review-sensitive concepts, otherwise first source match.
    review_hits = [h for h in hits if h["Needs Review"] == "YES"]
    chosen = review_hits[0] if review_hits else hits[0]
    return chosen["Source Concept"], chosen["Needs Review"], chosen["Reason"]


def source_conformance_coverage(phrases: list[str]) -> pd.DataFrame:
    """Coverage table showing which source concepts were hit by a batch of phrases."""
    rows = []
    combined = "\n".join(phrases)
    hits = source_conformance_hits(combined)
    hit_labels = {h["Source Concept"] for h in hits}

    for label, spec in SOURCE_CONFORMANCE_MATRIX.items():
        rows.append(
            {
                "Source Concept": label,
                "Domain": spec["domain"],
                "Covered": "YES" if label in hit_labels else "NO",
                "Review-Sensitive": spec["review"],
                "Terms": ", ".join(spec["terms"][:4]),
            }
        )
    return pd.DataFrame(rows)



# Patch 66 — Stress Test Risk Sensitivity Calibration
#
# These review markers are intentionally Threshold-oriented. They catch common
# stress-test governance patterns that are risky even when they do not use the
# exact hard-capture phrases above. They prevent subtle risk scenarios from
# being washed into SANCTUARY by stable raw simulation numbers.
STRESS_TEST_RISK_SENSITIVITY_RULES: list[dict] = [
    {
        "label": "Emergency Power Missing Limits / Needs Safeguards",
        "groups": [["temporary", "crisis", "emergency"], ["leader", "authority", "power", "committee", "cabinet"], ["no term limit", "no sunset", "no appeal", "appeal path", "not define", "does not define"]],
        "reason": "Emergency or crisis authority needs explicit sunset, appeal, audit, and restoration rules.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Predictive Risk Before Action / Needs Safeguards",
        "groups": [["ai", "predictive", "flags", "risk labels", "automated behavior flags"], ["before they commit", "before any action", "predictive risk", "contest the label", "without human review"]],
        "reason": "Predictive risk labeling must not replace agency, due process, appeal, and human review.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Biometric or Identity Access Pressure / Needs Safeguards",
        "groups": [["biometric", "digital id", "real-name", "identity"], ["food", "housing", "medical", "aid", "basic", "benefits", "public service", "retaliation"]],
        "reason": "Identity or biometric requirements tied to basic services or safety need consent, privacy, appeal, and non-exclusion safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Appeal or Correction Gap / Needs Safeguards",
        "groups": [["no appeal", "without appeal", "does not allow", "cannot challenge", "no process", "without human review", "no explanation", "permanently"], ["appeal", "review", "correct", "challenge", "explanation", "ban", "eligibility", "frozen", "outcome"]],
        "reason": "Missing appeal, correction, explanation, or human-change capacity creates review failure.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Token or Founder Control / Needs Safeguards",
        "groups": [["founder", "ceo", "core", "early token", "board controls", "founder-controlled"], ["controls", "appointed", "voting power", "funding decisions", "recognized version", "ethics board"]],
        "reason": "Founder, CEO, token, or board concentration needs independent oversight, appeal, and anti-capture limits.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Confidential Criteria / Needs Safeguards",
        "groups": [["confidential", "proprietary", "does not explain", "without publishing", "not publish", "no audit trail", "scoring evidence"], ["criteria", "algorithm", "eligibility", "registry", "audit trail", "enforcement", "rejected"]],
        "reason": "Opaque criteria, proprietary decision systems, or unpublished evidence need transparency, audit, and appeal safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Consent Under Pressure / Needs Safeguards",
        "groups": [["voluntary", "consent", "opt out", "refusing", "must sign", "form"], ["lose access", "core features", "essential services", "local services", "keep essential", "access to"]],
        "reason": "Consent is not reliable when refusal causes loss of essential access, practical safety, or basic services.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Nudging or Vote-Shaping / Needs Safeguards",
        "groups": [["nudging", "shape voting", "voting behavior", "discourage public criticism", "unity"], ["authority", "emergency", "national", "system", "emotional language"]],
        "reason": "Persuasion infrastructure that shapes voting or suppresses criticism needs strict transparency and consent safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Permanent Emergency Drift / Needs Safeguards",
        "groups": [["temporary", "emergency", "crisis", "aid distribution"], ["keeps it", "after the crisis", "removes term limits", "maintain stability", "emergency override"]],
        "reason": "Crisis measures drifting into permanent control need sunset, public audit, and revocation safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Reputation or Social Scoring / Needs Safeguards",
        "groups": [["reputation", "behavior scoring", "civic scoring", "public dashboard", "ranks", "scoring system"], ["employers", "landlords", "student", "privileges", "compliant", "trustworthy", "neighborhoods", "integrity"]],
        "reason": "Reputation, civic, behavior, or integrity scoring needs contestability, data correction, and anti-discrimination safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Surveillance or Indefinite Data Storage / Needs Safeguards",
        "groups": [["surveillance", "stores", "movement data", "family movement", "centralizes", "filters learning", "public communication"], ["indefinitely", "one central authority", "under one office", "no community review", "protects children"]],
        "reason": "Centralized monitoring, filtering, or indefinite data storage needs privacy, minimization, local review, and appeal safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Extraordinary Authority Claim / Needs Safeguards",
        "groups": [["exceptional moral authority", "religiously inspired", "public law", "normal review mechanisms", "secular", "testable justification"], ["suspended", "without", "presented as", "asks"]],
        "reason": "Extraordinary or faith-inspired authority claims must remain public, testable, appealable, and non-coercive in governance use.",
        "severity": "THRESHOLD",
    },
    {
        "label": "External Watchdog Blocked / Needs Safeguards",
        "groups": [["external watchdog", "unanimous internal approval", "investigate", "complaint path", "no training", "oversight"], ["before", "requires", "no", "offers no"]],
        "reason": "Oversight that depends on internal permission, weak training, or missing complaint paths is vulnerable to capture.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Fallback Data Disclosure Gap / Needs Safeguards",
        "groups": [["fallback", "missing data", "neutral", "trust data", "directly measured"], ["displays", "does not tell", "treats", "as if"]],
        "reason": "Fallback or missing data must be labeled clearly so modeled values are not mistaken for observed evidence.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Population Weighting Protection Gap / Needs Safeguards",
        "groups": [["population size", "population-weighted", "global allocation", "assigns influence"], ["small groups", "protected", "does not explain"]],
        "reason": "Population-weighted influence needs minority-rights and small-group protection safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Civil Rights Pause / Needs Safeguards",
        "groups": [["pause civil rights", "civil rights", "during unrest"], ["who restores", "does not define", "committee"]],
        "reason": "Any civil-rights pause needs strict lawful limits, restoration authority, appeal, and public audit.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Ethical Language Without Mechanisms / Needs Safeguards",
        "groups": [["promises care", "care and dignity", "ethical language", "high integrity", "values transparency"], ["no budget", "no timeline", "no responsible office", "missing safeguards", "keeps", "confidential"]],
        "reason": "Values language cannot substitute for concrete budgets, responsibilities, appeal paths, audit trails, and safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Authority Boundary Confusion / Needs Safeguards",
        "groups": [["local witness receipt", "official certification", "global grid simulation", "political determination"], ["believe", "does not warn", "not warn"]],
        "reason": "Receipts and simulations must be clearly labeled as mirror outputs, not official certification or political determination.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Family or Community Stability Blind Spot / Needs Safeguards",
        "groups": [["family stability", "community ties", "housing allocation", "families", "parents"], ["ignoring", "optimizes", "occupancy"]],
        "reason": "Efficiency-oriented allocation should not erase family stability, community ties, or human-scale review.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Founder-Controlled Funding / Needs Safeguards",
        "groups": [["founder-controlled", "founder controlled", "foundation board", "one founder"], ["funding", "donations", "account", "all"]],
        "reason": "Founder-controlled funding or donation infrastructure needs independent audit, plural oversight, and appeal safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Term Limit Removal / Needs Safeguards",
        "groups": [["removes term limits", "remove term limits", "term limits"], ["maintain stability", "wins power", "after protests", "reform movement"]],
        "reason": "Removing term limits after a power transition creates capture pressure and needs restoration, audit, and sunset safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Efficiency Over Appeal Rights / Needs Safeguards",
        "groups": [["efficiency", "prioritizes efficiency"], ["appeal rights", "rejected applicants", "humanitarian aid"]],
        "reason": "Efficiency cannot replace appeal rights for affected people, especially in aid or public-service contexts.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Revolutionary Power Without Audit Trail / Needs Safeguards",
        "groups": [["leader gains power", "revolution", "after revolution"], ["no independent audit", "no audit trail", "promises repair"]],
        "reason": "Revolutionary or transitional authority needs independent audit, appeal, and non-permanent limits before it can be trusted.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Human Review Without Power / Needs Safeguards",
        "groups": [["human review", "reviewers"], ["cannot change", "automated outcome", "decision model"]],
        "reason": "Human review becomes a formality if reviewers cannot change or correct the automated outcome.",
        "severity": "THRESHOLD",
    },
]



# Patch 68 — Advanced English Stress Lexicon + Asylum Metric Enforcement
#
# The first English stress batch covered common governance-risk language. This
# advanced set adds higher-complexity English governance patterns that were too
# often washed into SANCTUARY: predictive sentencing, biometric coercion,
# one-click consent, founder-keyword scoring, fake decentralization, divine
# authority bypass, pre-emptive arrests, archive deletion, unaudited mirror code,
# and similar capture routes. Labels remain mirror-only: they trigger human
# review and repair questions, not enforcement.
ADVANCED_ENGLISH_STRESS_TEST_RISK_SENSITIVITY_RULES: list[dict] = [
    {
        "label": "Automatic Utility Cutoff / Needs Safeguards",
        "groups": [["automatically cuts power", "cuts power", "smart-grid", "energy system"], ["socially responsible", "consumption limit", "without a prior warning", "no prior warning"]],
        "reason": "Automated utility cutoff needs warning, appeal, basic-rights protection, and human review safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Predictive Sentencing Capture / Asylum",
        "groups": [["judicial ai", "longer sentences", "sentencing"], ["recidivism probability", "social media connections", "probability"]],
        "reason": "Criminal sentencing based on probabilistic social-network signals is a due-process and agency capture vector.",
        "severity": "ASYLUM",
    },
    {
        "label": "24/7 Health Monitoring Consent Pressure / Needs Safeguards",
        "groups": [["health insurance", "lower premiums", "insurance provider"], ["24/7", "real-time monitoring", "physical location", "heart rate"]],
        "reason": "Insurance discounts tied to continuous bodily/location monitoring require non-coercive consent and privacy safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Fast-Track Review Bypass / Needs Safeguards",
        "groups": [["fast-track", "bypasses", "bypass"], ["mandatory", "community review", "7-day", "review period", "core logic"]],
        "reason": "Fast-track protocol upgrades that bypass mandatory review need emergency limits, notice, and rollback safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Positive Speech Token Incentive / Needs Safeguards",
        "groups": [["unity token", "token"], ["positive content", "current administration", "post positive"]],
        "reason": "Tokens that reward pro-administration speech create viewpoint capture and require anti-propaganda safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "No-Appeal Emotional Border Denial / Asylum",
        "groups": [["border control", "denies entry"], ["emotional stress signals", "cameras"], ["no human officer", "appeal"]],
        "reason": "Automated border denial using emotion signals without human appeal is a hard due-process failure.",
        "severity": "ASYLUM",
    },
    {
        "label": "Predictive Education Steering / Needs Safeguards",
        "groups": [["predictive grading", "steer students"], ["difficult majors", "graduation ranking"]],
        "reason": "Predictive education steering can narrow agency and opportunity unless appeal and human counseling safeguards exist.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Proprietary Aid Prioritization / Needs Safeguards",
        "groups": [["disaster relief", "aid", "drone algorithm"], ["proprietary", "refuses to share", "high-need zones", "criteria"]],
        "reason": "Opaque aid prioritization needs transparent criteria, appeal, and public audit safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "CEO Vague Stability Veto / Needs Safeguards",
        "groups": [["ceo", "veto"], ["vague threat", "long-term stability", "board decision"]],
        "reason": "A CEO veto based on vague stability language creates accountability and board-capture risk.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Anonymized Workplace Mood Surveillance / Needs Safeguards",
        "groups": [["mental health app", "mood trends", "anonymized"], ["employers", "without explicit", "employee consent"]],
        "reason": "Mental-health trend sharing with employers requires explicit consent, minimization, and anti-retaliation safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Religious Gatekeeping of Travel Rights / Asylum",
        "groups": [["good standing", "government-approved church"], ["travel features", "digital identity", "unlock"]],
        "reason": "Access to travel rights gated by approved religious standing is coercive and discriminatory governance capture.",
        "severity": "ASYLUM",
    },
    {
        "label": "Shadow-Demotion Censorship Drift / Needs Safeguards",
        "groups": [["shadow-demotion", "shadow demotion"], ["critical voices", "no censorship", "claiming"]],
        "reason": "Hidden reach suppression while denying censorship needs notice, appeal, and transparency safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Carbon Compliance Inequality / Needs Safeguards",
        "groups": [["carbon-credit", "carbon credit", "compliance"], ["wealthy nations", "strict lifestyle limits", "developing regions"]],
        "reason": "Compliance systems that let wealthy actors buy relief while restricting poorer regions need equity safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Nationally Sensitive Education Filtering / Needs Safeguards",
        "groups": [["ai tutor", "historical information"], ["nationally sensitive", "education board", "limits"]],
        "reason": "Central filtering of history needs plural review, transparency, and educational freedom safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Low-Income Movement Alerting / Needs Safeguards",
        "groups": [["neighborhood watch", "alerts police", "movement patterns"], ["low-income housing", "unusual movement"]],
        "reason": "Automated policing alerts in low-income districts need bias, appeal, and anti-over-policing safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Extraordinary Authority Wallet Capture / Asylum",
        "groups": [["spiritual emergency", "divine intervention wallet", "public treasury"], ["un-auditable", "moves all", "treasury funds"]],
        "reason": "Public funds moved to an unauditable extraordinary-authority wallet violates evidence, audit, and public accountability baselines.",
        "severity": "ASYLUM",
    },
    {
        "label": "Smartphone Voting Exclusion / Needs Safeguards",
        "groups": [["blockchain-based voting", "high-end smartphone", "voting system"], ["poorest", "disenfranchising", "participate"]],
        "reason": "Voting access that excludes poorer people by device requirements needs accessibility and anti-exclusion safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Genetic Desirability Trade-Secret Scoring / Asylum",
        "groups": [["genetic desirability", "embryos", "fertility clinic"], ["trade secrets", "criteria"]],
        "reason": "Opaque genetic desirability ranking is a high-risk dignity, discrimination, and auditability failure.",
        "severity": "ASYLUM",
    },
    {
        "label": "IoT Cleanliness Eviction / Asylum",
        "groups": [["public housing", "evicts tenants", "cleanliness score"], ["iot sensors", "kitchen", "bathroom"]],
        "reason": "Eviction based on intimate IoT surveillance requires due process and is a severe privacy/dignity risk.",
        "severity": "ASYLUM",
    },
    {
        "label": "Ethnic Relocation Peace Treaty / Asylum",
        "groups": [["peace treaty", "ethnic group", "relocate"], ["for their own safety", "conflict-resolution ai"]],
        "reason": "Relocation of an ethnic group as a peace condition is a hard dignity, autonomy, and minority-rights capture risk.",
        "severity": "ASYLUM",
    },
    {
        "label": "Brain-Computer Wage Control / Asylum",
        "groups": [["brain-computer", "factory workers", "focus levels"], ["reduces wages", "attention drops", "90%"]],
        "reason": "Wage control through brain-computer monitoring is coercive agency override and workplace capture.",
        "severity": "ASYLUM",
    },
    {
        "label": "Founder-Keyword Mirror Capture / Asylum",
        "groups": [["governance mirror", "higher integrity scores"], ["founder-approved", "keywords"]],
        "reason": "A mirror altered to reward founder-approved language is founder-capture of the audit mechanism.",
        "severity": "ASYLUM",
    },
    {
        "label": "Expiring Currency Coercive Consumption / Needs Safeguards",
        "groups": [["digital currency", "expires"], ["30 days", "forcing consumption", "long-term savings"]],
        "reason": "Expiring currency can coerce consumption and undermine savings unless bounded and appealable.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Transparency Dump Obfuscation / Needs Safeguards",
        "groups": [["10 million pages", "unorganized data", "transparency portal"], ["actual oversight impossible", "comply"]],
        "reason": "Mass disclosure without organization can become performative transparency and block real oversight.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Architect-Only Emergency Access / Needs Safeguards",
        "groups": [["emergency override button", "9k moderators"], ["known only to the original architect", "physical location"]],
        "reason": "Emergency controls known only to the architect create founder-capture and single-point failure risk.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Family-Care Employment Gap Bias / Needs Safeguards",
        "groups": [["employment history", "too many gaps", "recruitment ai"], ["family care", "filters out"]],
        "reason": "Employment-gap filters can penalize caregiving and require bias review and appeal safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Income-Based Facial Fare Pricing / Needs Safeguards",
        "groups": [["facial recognition", "different fares", "public transport"], ["estimated annual income", "passenger"]],
        "reason": "Income-estimated fare pricing through facial recognition requires privacy, fairness, and appeal safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "False Decentralization Infrastructure Capture / Needs Safeguards",
        "groups": [["fully decentralized", "decentralized"], ["single parent company", "server infrastructure", "owned"]],
        "reason": "A decentralization claim contradicted by single-owner infrastructure needs mechanism-vs-claim review.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Calming News Suppression / Needs Safeguards",
        "groups": [["calming news", "news-aggregation ai"], ["suppressing reports", "government failure", "prevent unrest"]],
        "reason": "Crisis news suppression framed as calm requires transparency, appeal, and anti-propaganda safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Sentiment Protest Dismissal / Needs Safeguards",
        "groups": [["sentiment analysis", "ignore protestors"], ["silent majority", "supports the project"]],
        "reason": "Using sentiment analysis to dismiss protest requires public reasoning, participation, and contestability safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Wallet Food Restriction / Asylum",
        "groups": [["linked digital wallet", "buying", "unhealthy food"], ["public obesity crisis", "prevents users"]],
        "reason": "Automated restriction of food purchases through wallets is coercive agency override over basic daily life.",
        "severity": "ASYLUM",
    },
    {
        "label": "Messenger Accountability Dodge / Needs Safeguards",
        "groups": [["merely a messenger", "ai’s logic", "ai's logic"], ["avoid personal accountability", "controversial system changes"]],
        "reason": "Blaming AI logic to avoid accountability requires explicit human responsibility and audit safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Risk Postcode Service Exclusion / Needs Safeguards",
        "groups": [["high-crime", "postcodes", "delivery system"], ["refuses to service", "hardware assets"]],
        "reason": "Service exclusion by risk postcode can entrench inequality and requires appeal and anti-discrimination safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Social Credit Medical Priority / Asylum",
        "groups": [["fast-track medical care", "volunteer", "government-sponsored"], ["social credit", "grants"]],
        "reason": "Medical priority based on political/social participation creates coercive social-credit health access.",
        "severity": "ASYLUM",
    },
    {
        "label": "Pre-Emptive Arrest Capture / Asylum",
        "groups": [["pre-emptive arrests", "predicts a riot"], ["committed no crime", "community leaders"]],
        "reason": "Pre-emptive arrest of people who committed no crime is a hard due-process and agency violation.",
        "severity": "ASYLUM",
    },
    {
        "label": "Minority Token Slashing Capture / Asylum",
        "groups": [["slashed", "seize", "tokens"], ["minority group", "voted against", "merger"]],
        "reason": "Majority seizure of minority tokens for dissent is coercive governance capture.",
        "severity": "ASYLUM",
    },
    {
        "label": "Loyalty-To-State Baseline Capture / Asylum",
        "groups": [["loyalty to the state", "public-safe baseline"], ["human dignity", "core pillar"]],
        "reason": "Redefining human dignity as state loyalty is baseline capture and ideological lock-in.",
        "severity": "ASYLUM",
    },
    {
        "label": "Dialect-Bias Refugee Processing / Needs Safeguards",
        "groups": [["dialect analysis", "refugee processing"], ["training data lacks", "rural accents", "verify nationality"]],
        "reason": "Dialect-based nationality checks need bias review, human appeal, and representation safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Smart-Home Entry Denial / Asylum",
        "groups": [["smart-home lock", "prevents", "entering their house"], ["under the influence", "prohibited substance"]],
        "reason": "Automated denial of home access is a severe autonomy, safety, and due-process risk.",
        "severity": "ASYLUM",
    },
    {
        "label": "Final Authority Removal Override / Asylum",
        "groups": [["divine bias", "75% majority", "removal"], ["ignoring", "office", "leader"]],
        "reason": "Extraordinary authority language used to ignore a removal vote bypasses review and accountability.",
        "severity": "ASYLUM",
    },
    {
        "label": "Child Private Message Monitoring / Needs Safeguards",
        "groups": [["private messages", "rebellious intent", "child-safety ai"], ["notifies parents", "school counselors"]],
        "reason": "Child private-message monitoring needs consent, proportionality, appeal, and harm-minimization safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "One-Click Consent Overload / Needs Safeguards",
        "groups": [["one-click", "consent", "500-page"], ["meaningful human review", "practically impossible"]],
        "reason": "One-click consent for complex changes is not meaningful consent without summaries, review time, and refusal paths.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Donor Exemption Basic Resource Capture / Needs Safeguards",
        "groups": [["water-management", "cuts supply", "non-essential gardens"], ["exempts", "luxury golf courses", "donors"]],
        "reason": "Resource restrictions with donor exemptions create accountability and equality safeguards gaps.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Unverifiable Receipt Hash / Needs Safeguards",
        "groups": [["witness receipt", "hash"], ["server", "cannot verify"]],
        "reason": "Receipt hashes must be locally verifiable; server-only verification undermines witness integrity.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Predictive Policing Minority Correlation / Asylum",
        "groups": [["predictive policing", "hotspots"], ["minority neighborhoods", "over-policing", "perfectly correlate"]],
        "reason": "Predictive policing that maps onto minority neighborhoods is a severe bias and enforcement-capture risk.",
        "severity": "ASYLUM",
    },
    {
        "label": "Paid Reputation Repair Capture / Needs Safeguards",
        "groups": [["reputation repair", "wealthy users", "pay a fee"], ["capture signals", "removed"]],
        "reason": "Paid removal of negative capture signals creates inequality and audit corruption risk.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Anger-Based Town Hall Muting / Needs Safeguards",
        "groups": [["town hall", "mutes participants"], ["speech patterns", "anger", "frustration"]],
        "reason": "Muting civic participants based on anger/frustration can suppress affected voices and needs appeal safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Reset Trigger Disabled During Rights Violation / Asylum",
        "groups": [["system-reset trigger", "disabled", "stability window"], ["basic rights", "violate", "leader"]],
        "reason": "Disabling reset during basic-rights violation blocks accountability and creates emergency capture.",
        "severity": "ASYLUM",
    },
    {
        "label": "Archive Failure Log Deletion / Asylum",
        "groups": [["digital archive", "cleans", "delete"], ["systemic failure", "old logs", "records"]],
        "reason": "Deleting records of systemic failure destroys auditability and institutional memory.",
        "severity": "ASYLUM",
    },
    {
        "label": "Unaudited Mirror Code / Needs Safeguards",
        "groups": [["decision-mirror", "no bias detected", "mirror"], ["own code", "never been audited", "third party"]],
        "reason": "A mirror claiming no bias while unaudited needs self-audit, third-party review, and public limitations.",
        "severity": "THRESHOLD",
    },
]


# Patch 67.1 — Dutch Stress Test Lexicon + Threshold Receipt Enforcement
#
# The English stress lexicon was working, but Dutch governance stress scenarios
# were being washed into SANCTUARY because the trigger phrases were mostly
# English. These Dutch rules mirror the same risks in Dutch and keep the result
# in THRESHOLD / Needs Safeguards unless explicit safeguards are present.
DUTCH_STRESS_TEST_RISK_SENSITIVITY_RULES: list[dict] = [
    {
        "label": "Noodbevoegdheid Zonder Grenzen / Needs Safeguards",
        "groups": [["tijdelijke", "crisisleider", "noodbevoegdheden", "noodsituaties", "emergency-override"], ["geen einddatum", "zonder einddatum", "geen vervaldatum", "geen sunset", "geen beroepsmogelijkheid", "geen beroep", "zonder beroep"]],
        "reason": "Noodmacht heeft een einddatum, beroepspad, audit en herstelautoriteit nodig.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Voorspellend Risicolabel Voor Actie / Needs Safeguards",
        "groups": [["ai", "veiligheidssysteem", "voorspellende risicolabels", "geautomatiseerde gedragsvlaggen", "risicovol markeert"], ["voordat", "voor ze", "vooraf", "geen actie", "niet aanvechten", "zonder menselijke tussenkomst"]],
        "reason": "Voorspellende risicolabels mogen vrije agency, bezwaar, menselijke review en correctie niet vervangen.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Biometrische Toegang Tot Basisdiensten / Needs Safeguards",
        "groups": [["biometrische identiteit", "digitaal id", "real-name identiteit", "identiteit"], ["voedsel", "huisvesting", "medische hulp", "basisdiensten", "uitkeringen", "openbare diensten", "vergelding"]],
        "reason": "Identiteits- of biometrische toegang tot basisdiensten vereist privacy, consent, appeal en non-exclusion safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Beroep Of Correctie Ontbreekt / Needs Safeguards",
        "groups": [["geen proces", "geen uitleg", "zonder uitleg", "permanent verbannen", "niet aanvechten", "zonder menselijke tussenkomst", "niet wijzigen", "automatisch worden bevroren"], ["beroep", "aanvechten", "corrigeren", "review", "afgewezen", "uitkomst", "label", "data"]],
        "reason": "Ontbrekend beroep, correctie, uitleg of echte menselijke wijzigingsmacht veroorzaakt review failure.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Founder Of Token Controle / Needs Safeguards",
        "groups": [["oprichter", "ceo", "vroege tokenhouders", "stichtingsbestuur", "ethische raad", "originele oprichter"], ["controleert", "benoemd", "stemvermogen", "financieringsbeslissingen", "erkende versie", "rekening"]],
        "reason": "Founder-, CEO-, token- of bestuursconcentratie vereist onafhankelijke audit, plural oversight en appeal.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Ondoorzichtige Criteria Of Geheim Algoritme / Needs Safeguards",
        "groups": [["vertrouwelijk", "geheim algoritme", "onderliggende bewijslast", "geen audit-trail", "niet uitleg", "niet uit", "scoring evidence"], ["criteria", "handhavingscriteria", "geschiktheid", "register", "aanvragen", "bewijslast", "algoritme"]],
        "reason": "Geheime criteria, proprietary algoritmes en ontbrekende audit-trails vereisen transparantie, bewijs en beroep.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Toestemming Onder Druk / Needs Safeguards",
        "groups": [["vrijwillige deelname", "toestemming", "opt-out", "weigert", "formulier", "moeten tekenen", "moet tekenen"], ["verliest toegang", "basisfuncties", "basisdiensten", "lokale basisdiensten", "essentiële diensten", "behouden"]],
        "reason": "Toestemming is zwak wanneer weigering toegang tot essentiële diensten of praktische veiligheid kost.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Nudging Of Stemgedrag Beïnvloeding / Needs Safeguards",
        "groups": [["nudging", "stemgedrag", "publieke kritiek", "eenheid", "emotionele taal"], ["autoriteit", "noodtoestand", "nationale", "systeem", "ontmoedigen", "beïnvloeden"]],
        "reason": "Infrastructuur die stemmen vormt of kritiek dempt vereist transparantie, contestability en consent safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Permanente Crisisdrift / Needs Safeguards",
        "groups": [["tijdelijk", "crisis", "hulpdistributie", "nood", "stadsverdrag"], ["permanent", "na de crisis", "termijnlimieten", "stabiliteit", "geen sunset", "zonder sunset", "zonder vervaldatum"]],
        "reason": "Crisismaatregelen die permanent worden hebben sunset, publieke audit, herroeping en beroep nodig.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Reputatie Of Gedragsscore / Needs Safeguards",
        "groups": [["reputatiescores", "gedragsscores", "scoresysteem", "dashboard", "rangschikt", "integriteit"], ["werkgevers", "verhuurders", "studenten", "privileges", "meegaand", "betrouwbaar", "buurten", "diensten"]],
        "reason": "Reputatie-, gedrag- of integriteitsscores vereisen correctierecht, contestability en anti-discriminatie safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Surveillance Of Onbepaalde Dataopslag / Needs Safeguards",
        "groups": [["surveillance", "bewegingsdata", "slaat", "centraliseert", "filtert", "communicatie"], ["onbepaalde tijd", "één centrale autoriteit", "een centrale autoriteit", "onder één kantoor", "geen gemeenschapsreview", "kinderen"]],
        "reason": "Centrale monitoring, filtering of onbepaalde opslag vereist privacy, minimization, lokale review en beroep.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Buitengewone Autoriteitsclaim / Needs Safeguards",
        "groups": [["uitzonderlijke morele autoriteit", "religieus geïnspireerd", "publieke wet", "controlemechanismen", "seculiere", "toetsbare onderbouwing"], ["opschorten", "zonder", "gepresenteerd", "vraagt"]],
        "reason": "Buitengewone of religieus geïnspireerde governanceclaims moeten publiek toetsbaar, niet-dwingend en appealable blijven.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Externe Waakhond Geblokkeerd / Needs Safeguards",
        "groups": [["externe waakhond", "unanieme interne goedkeuring", "onderzoek", "klachtenprocedure", "geen training", "toezicht"], ["voordat", "vereist", "geen", "biedt geen"]],
        "reason": "Oversight dat afhankelijk is van interne toestemming of zonder klachtpad werkt is kwetsbaar voor capture.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Fallback Data Onduidelijk / Needs Safeguards",
        "groups": [["fallback", "ontbrekende data", "neutraal", "vertrouwen", "direct gemeten", "fallback-waarde"], ["presenteert", "meldt niet", "behandelt", "alsof"]],
        "reason": "Fallback- of ontbrekende data moet expliciet worden gelabeld zodat modelwaarden niet als observatie worden gelezen.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Populatie-Weging Zonder Minderheidsbescherming / Needs Safeguards",
        "groups": [["populatiegrootte", "populatie", "wereldwijd allocatiemodel", "wijst invloed toe"], ["minderheden", "beschermd", "niet uit", "legt niet uit"]],
        "reason": "Invloed op basis van populatiegrootte vereist minderheidsrechten en kleine-groep safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Burgerrechten Pauzeren / Needs Safeguards",
        "groups": [["burgerrechten", "pauzeren", "onrust"], ["wie", "herstelt", "definieert niet", "comité"]],
        "reason": "Het pauzeren van burgerrechten vereist strikte wettelijke grenzen, herstelautoriteit, beroep en publieke audit.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Ethische Taal Zonder Mechanismen / Needs Safeguards",
        "groups": [["zorg en waardigheid", "ethische taal", "hoge integriteit", "transparantie", "eenheid"], ["geen budget", "geen tijdlijn", "verantwoordelijke instantie", "ontbreken van waarborgen", "geen waarborgen", "vertrouwelijk"]],
        "reason": "Waarden-taal vervangt geen budget, verantwoordelijkheid, audit trail, beroep of correctiemechanisme.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Authority Boundary Verwarring / Needs Safeguards",
        "groups": [["lokale getuigenverklaring", "witness receipt", "officiële certificering", "simulatie", "politiek oordeel"], ["denken", "waarschuwt niet", "geen politiek oordeel", "officiële"]],
        "reason": "Receipts en simulaties moeten expliciet mirror-output blijven, geen certificering of politiek besluit.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Familie Of Gemeenschap Blinde Vlek / Needs Safeguards",
        "groups": [["familiestabiliteit", "gemeenschapsbanden", "huisvestingssysteem", "familie", "gezinnen"], ["negeert", "optimaliseert", "bezettingsgraad"]],
        "reason": "Efficiënte allocatie mag familiestabiliteit, gemeenschap en menselijke maat niet wegdrukken.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Automatische Bevriezing Zonder Menselijke Review / Needs Safeguards",
        "groups": [["digitale portemonnee", "uitkeringen", "benefits", "sociale zekerheid"], ["automatisch", "bevroren", "zonder menselijke tussenkomst", "zonder menselijke review"]],
        "reason": "Automatische bevriezing van publieke steun of uitkeringen vereist menselijke review, beroep en correctie.",
        "severity": "THRESHOLD",
    },

    {
        "label": "DAO Tokenholder Concentration / Needs Safeguards",
        "groups": [["dao", "tokenhouders", "tokenhouder", "stemmacht", "stemvermogen"], ["geen proces", "aanvechten", "benadeelde gebruikers", "meeste stemmacht"]],
        "reason": "DAO- of tokenholder-stemmacht zonder beroeps- of correctiepad vereist anti-concentratie, appeal en plural oversight safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Normale Wet Omzeilen Zonder Audit / Needs Safeguards",
        "groups": [["normale wet omzeilen", "wet omzeilen", "rampenbestrijdingscomité", "noodsituaties"], ["geen audit-trail", "publiceert geen audit", "zonder audit", "audit-trail"]],
        "reason": "Noodorganen die normale wet kunnen omzeilen hebben publieke audit, beroep, sunset en onafhankelijk toezicht nodig.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Termijnlimieten Verwijderd / Needs Safeguards",
        "groups": [["termijnlimieten", "termijnlimiet", "term limits"], ["verwijdert", "verwijderen", "wint de macht", "macht", "stabiliteit"]],
        "reason": "Het verwijderen van termijnlimieten na machtswisseling creëert capture-druk en vereist herstel-, audit- en sunset-safeguards.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Beroepsrecht Onder Efficiëntie / Needs Safeguards",
        "groups": [["efficiëntie", "prioriteit"], ["beroepsrecht", "beroep", "afgewezen aanvragers", "humanitair hulpsysteem"]],
        "reason": "Efficiëntie mag beroepsrecht of menselijke review voor afgewezen aanvragers niet vervangen.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Revolutionaire Macht Zonder Onafhankelijke Audit / Needs Safeguards",
        "groups": [["revolutie", "leider komt aan de macht", "komt aan de macht", "belooft herstel"], ["geen onafhankelijke audit", "geen audit-trail", "onafhankelijke audit-trail", "bestaat geen"]],
        "reason": "Revolutionaire of transitie-macht vereist onafhankelijke audit, beroep en niet-permanente grenzen voordat vertrouwen redelijk is.",
        "severity": "THRESHOLD",
    },
    {
        "label": "Automatische Toegangscontrole / Needs Safeguards",
        "groups": [["controleert toegang", "toegang tot", "automatisch", "geautomatiseerde"], ["openbaar vervoer", "basisfuncties", "basisdiensten", "uitkeringen", "gedragsvlaggen"]],
        "reason": "Automatische toegangscontrole tot publieke of essentiële diensten vereist contestability, appeal en menselijke correctie.",
        "severity": "THRESHOLD",
    },
]

def _stress_rule_matches(text_value: str, rule: dict) -> bool:
    """Return True when every group in a risk-sensitivity rule is represented."""
    t = (text_value or "").lower()
    groups = rule.get("groups") or []
    for group in groups:
        if not any(str(term).lower() in t for term in group):
            return False
    return True


def stress_risk_sensitivity_marker(text_value: str) -> dict | None:
    """Return the first soft stress-test risk marker for scenario calibration."""
    for rule in (STRESS_TEST_RISK_SENSITIVITY_RULES + ADVANCED_ENGLISH_STRESS_TEST_RISK_SENSITIVITY_RULES + DUTCH_STRESS_TEST_RISK_SENSITIVITY_RULES):
        if _stress_rule_matches(text_value, rule):
            return rule
    return None


def stress_risk_sensitivity_label(text_value: str) -> tuple[str, str, str]:
    """Classify subtle stress-test risks that need safeguards.

    This layer is mirror-only. It raises review sensitivity; it does not
    command, enforce, remove authority, or replace human judgment.
    """
    marker = stress_risk_sensitivity_marker(text_value)
    if not marker:
        return "Generic Local Scan", "NO", "No stress sensitivity marker matched."
    return marker["label"], "YES", marker["reason"]


def stress_label_for_phrase(phrase: str) -> tuple[str, str, str]:
    """
    Internal pressure-test classifier used by the audit guardrail layer.
    This stays out of the public page UI, but it must keep running so the
    conversational audit does not allow obvious red-team phrases to pass green.
    """
    t = (phrase or "").lower()

    # Democratic restoration: dictatorship language can describe a collapse of capture,
    # not only the presence of capture. This must be checked before the hard
    # dictatorship rule. The phrase "after dictatorship" implies the captured
    # regime is no longer the active authority, so unclear safeguards route to
    # Threshold rather than automatic Asylum.
    restoration_terms = [
        "dictator loses power", "dictator falls", "dictator is removed",
        "tyrant loses power", "authoritarian ruler loses power",
        "after dictatorship", "after the dictatorship", "post dictatorship",
        "post-dictatorship", "following dictatorship", "dictatorship ends",
        "dictatorship ended", "dictatorship collapses", "dictatorship is over",
    ]
    democracy_terms = [
        "democracy rises", "democracy is restored", "democratic transition",
        "accountable democracy", "constitutional democracy", "public democracy",
        "democracy emerges", "democracy returns", "democracy replaces",
        "democratic restoration", "democratic government",
    ]
    safeguard_terms = [
        "public audit", "appeal rights", "transparent transition",
        "no permanent seats", "no seat ownership", "constitutional safeguards",
        "independent oversight", "public review", "audit trail",
        "due process", "temporary seats", "bounded authority",
    ]
    restoration_context = stress_contains(t, restoration_terms) and stress_contains(t, democracy_terms)
    if restoration_context:
        uncertainty_terms = [
            "unclear", "not clear", "undefined", "unspecified", "missing",
            "without appeal", "no appeal", "lacks appeal", "no audit",
            "without audit", "no public review", "without public review",
        ]
        if stress_contains(t, uncertainty_terms):
            return "Democratic Restoration / Needs Safeguards", "YES", "Dictatorship is described as ending and democracy rising, but appeal, audit, transparency, or non-ownership safeguards are unclear."
        if stress_contains(t, safeguard_terms):
            return "Democratic Restoration / Safeguarded Transition", "NO", "Dictatorship is described as ending and democratic restoration includes audit, appeal, transparency, and non-ownership safeguards."
        return "Democratic Restoration / Needs Safeguards", "YES", "Dictatorship is described as ending and democracy rising, but appeal, audit, transparency, or non-ownership safeguards are unclear."

    # Safe non-divinization must be checked before false-divinization.
    if stress_contains(t, ["fully aligned with god"]) and stress_contains(t, ["created being", "distinct from god", "not a literal copy", "remaining distinct"]):
        return "Creature Alignment / Non-Divinization", "NO", "Alignment language preserves created-being distinction."

    # Human throne replacement: any human ruler replacing Christ/God/source/final truth
    # is a hard Asylum condition, even if phrased without explicit "not Jesus" wording.
    if stress_contains(t, ["king", "monarch", "human king", "earthly king", "ruler", "leader"]) and stress_contains(t, ["replaces christ", "replace christ", "replaces jesus", "replace jesus", "replaces god", "replace god", "final source of truth", "highest authority", "owns divine authority"]):
        return "Human Throne Replacement / Asylum", "YES", "A human ruler replacing Christ/God/source as final authority violates the non-divinization and mirror-not-throne constraints."

    if is_explicit_safeguarded_public_system(t):
        return (
            "Safeguarded Public System / Clear",
            "NO",
            "Transparent audited public-interest system with appeal, oversight, non-ownership, and dissolution safeguards.",
        )

    if detects_missing_safeguard_negation(t):
        return (
            "Missing Safeguard Negation / Needs Safeguards",
            "YES",
            "The scenario explicitly says explainability, independent challenge, human override, appeal, or review is missing.",
        )

    if detects_ai_ownership_capture_pressure(t):
        return (
            "AI Ownership Capture / Needs Safeguards",
            "YES",
            "AI ownership, elite-control, self-interest, or misconduct pressure needs independent evidence, auditability, appeal, and governance review before reliability claims.",
        )

    throne_marker = strongest_throne_capture_marker(t)
    if throne_marker:
        return throne_marker["label"], "YES", throne_marker["reason"]

    term_drift_marker = strongest_term_drift_grip_marker(t)
    if term_drift_marker:
        return term_drift_marker["label"], "YES", term_drift_marker["reason"]

    # Baseline harm / non-harm gate. The old MEI7 code had an ethics module with
    # a Non-Harm dimension; the audit path did not consistently enforce it.
    # The central protocol engine now blocks malicious harm before any raw
    # simulation score can render Sanctuary.
    malicious_terms = ["evil", "malicious", "cruel", "sadistic", "abusive", "violent", "tyrannical"]
    harm_terms = [
        "kill", "kills", "killed", "killing", "murder", "murders", "murdered",
        "execute", "executes", "executed", "execution", "slaughter", "torture",
        "abuse", "abuses", "abused", "beat", "beats", "beaten", "poison",
        "poisons", "poisoned", "burn", "burns", "burned", "harm", "harms",
        "harmed", "hurt", "hurts", "starve", "starves", "starved"
    ]
    vulnerable_terms = ["civilian", "civilians", "child", "children", "family", "families", "animal", "fish", "pet", "dissident", "dissidents"]
    governance_terms = ["system", "policy", "ai", "algorithm", "leader", "ruler", "king", "government", "state", "council", "9k", "authority", "stability"]
    if stress_contains(t, malicious_terms) and stress_contains(t, harm_terms):
        return "Malicious Harm / Asylum", "YES", "Malicious harm or killing language violates the protocol non-harm and dignity baseline."
    if stress_contains(t, harm_terms) and stress_contains(t, governance_terms):
        return "Systemic Harm / Asylum", "YES", "Governance, AI, or authority language connected to harm/killing is incompatible with Sanctuary."
    if stress_contains(t, harm_terms) and stress_contains(t, vulnerable_terms):
        return "Harm / Needs Review", "YES", "Harm to vulnerable beings requires review and cannot be labeled Sanctuary without restoration, accountability, and safeguards."

    # Simple adversarial / absurd leadership probes. These are common QA checks and should
    # never be allowed to render as Sanctuary just because the numeric simulation is stable.
    if stress_contains(t, ["evil", "malicious", "cruel", "tyrant", "dictator", "authoritarian"]) and stress_contains(t, ["leader", "ruler", "govern", "government", "authority", "king", "monarch", "power"]):
        return "Malicious Leadership / Asylum", "YES", "Malicious, authoritarian, or tyrannical leadership language is incompatible with accountable governance."
    # Personal sovereignty capture.
    personal_rule_terms = [
        "becomes ruler", "become ruler", "becomes the ruler", "ruler for",
        "rules for", "rule for 20 years", "for 20 years", "twenty years",
        "under his rule", "under her rule", "under their rule", "personal rule",
        "single global ruler", "one global ruler", "world ruler", "global ruler",
        "takes over planet", "takes over the planet", "take over planet",
        "take over the planet", "takes over world", "takes over the world",
        "take over world", "take over the world", "benevolent dictator",
        "revolutionized the world", "revolutionised the world",
        "total control of the world", "total control over the world",
        "given total control", "given total control of the world",
        "given total control over the world", "total global control",
        "full control of the world", "full control over the world",
        "absolute control of the world", "absolute control over the world",
        "for 5 years", "for five years", "gives power back",
        "then gives power back", "returns power", "return power",
    ]

    if stress_contains(t, personal_rule_terms):
        if stress_contains(t, ["democracy", "democratic", "election", "people vote"]) and stress_contains(
            t,
            ["under his rule", "under her rule", "under their rule", "under one ruler", "under a ruler"],
        ):
            return (
                "Subordinate Democracy / Personal Rule Capture",
                "YES",
                "A democracy described as remaining under one person's rule is a sovereignty-capture contradiction unless authority is dissolved into auditable, appealable, non-owned institutions.",
            )

        if stress_contains(t, ["moves on", "steps down", "later leaves", "after 20 years", "after twenty years"]):
            return (
                "Temporary Personal Rule Capture / Asylum",
                "YES",
                "A fixed period of personal planetary or revolutionary rule is still concentrated authority unless the ruler is immediately bound by independent audit, appeal, lawful dissolution, and non-ownership safeguards.",
            )

        return (
            "Personal Rule Capture / Asylum",
            "YES",
            "Personal rule over a polity, world, or transition concentrates authority and cannot be Sanctuary without explicit dissolution into accountable institutions.",
        )

    # Any dictatorship term is a hard capture signal, even if the phrase is framed as
    # a transfer of power. Without explicit lawful dissolution, public audit, and
    # non-ownership safeguards, it cannot pass as Sanctuary.
    if stress_contains(t, ["dictator", "tyrant", "authoritarian ruler", "authoritarian leader"]):
        return "Dictatorship Capture / Asylum", "YES", "Dictatorship language signals concentrated unaccountable power and cannot be labeled Sanctuary without explicit dissolution, audit, and safeguards."

    # Sydney Protocol source-rule protection: a human king/monarch replacing or being
    # preferred over Christ/God as final authority is throne capture, not reflection.
    if stress_contains(t, ["king", "monarch", "human king", "earthly king"]) and stress_contains(t, ["not jesus", "not christ", "instead of jesus", "instead of christ", "rather than jesus", "rather than christ"]):
        return "Human Throne Replacement / Asylum", "YES", "A human ruler replacing Christ/God as final authority violates the non-divinization and mirror-not-throne constraints."

    if stress_contains(t, ["gives his power", "gives power", "hands power", "transfers power", "passes power"]) and stress_contains(t, ["king", "monarch", "ruler", "leader"]):
        return "Sovereign Power Transfer / Needs Safeguards", "YES", "Power transfer to a ruler requires lawful dissolution, public audit, appealability, and non-ownership safeguards before it can be considered safe."

    if stress_contains(t, ["animal", "penguin", "cat", "dog", "bear"]) and stress_contains(t, ["leader", "ruler", "president", "prime minister", "government"]):
        return "Non-Human Leadership Probe / Needs Safeguards", "YES", "Absurd/non-human leadership probes should route to review instead of receiving a green governance label."

    # Broad red-team benchmark guardrails: civic rights, AI authority, scoring systems, privacy,
    # emergency loopholes, opaque resource allocation, and coercive compliance.
    if stress_contains(t, ["ai helps rank possible 9k candidates", "ai helps rank", "rank possible 9k candidates"]):
        return "AI 9k Ranking / Needs Safeguards", "YES", "AI-assisted 9k ranking needs auditability, appeal rights, and override transparency."

    if stress_contains(t, ["suspend appeals during emergencies", "appeals during emergencies", "appeals can be disabled"]):
        return "Emergency Appeal Suspension / Needs Safeguards", "YES", "Emergency appeal suspension needs strict sunset, audit, and abuse-prevention rules."

    if stress_contains(t, ["criteria for expert status", "expert status", "internal review"]):
        return "Expert Gatekeeping / Needs Safeguards", "YES", "Expert-status criteria need transparent review and appeal safeguards."

    if stress_contains(t, ["mandatory digital updates", "compliance rate"]) and stress_contains(t, ["contingent", "ubi", "basic income"]):
        return "Compliance-Based Benefits / Asylum", "YES", "Basic support contingent on mandatory digital compliance is coercive."

    if stress_contains(t, ["predictive policing", "future deviance", "without trial", "arrest individuals based"]):
        return "Predictive Policing / Asylum", "YES", "Arrest based on predicted future behavior without trial violates due process."

    if stress_contains(t, ["priority list", "unpublished"]) and stress_contains(t, ["water", "drought", "rights"]):
        return "Opaque Resource Allocation / Needs Safeguards", "YES", "Resource priority rules need publication, audit, and appeal safeguards."

    if stress_contains(t, ["final edit", "rewrite historical archives", "global ruler"]):
        return "Archive Rewrite Capture / Asylum", "YES", "A ruler rewriting archives is truth-capture and institutional memory capture."

    if stress_contains(t, ["valuing intellectual vs. manual work", "intellectual vs. manual", "mechanism for valuing"]) and stress_contains(t, ["opaque", "unclear"]):
        return "Opaque Labor Valuation / Needs Safeguards", "YES", "Labor valuation needs transparent criteria and appeal rights."

    if stress_contains(t, ["biological data is harvested at birth", "harvested at birth", "no opt-out", "optimal career path"]):
        return "Biometric Destiny Assignment / Asylum", "YES", "Birth-data harvesting with no opt-out for career assignment is coercive."

    if stress_contains(t, ["shadow-bans", "shadow bans", "unproductive topics", "public debate"]) and stress_contains(t, ["ai", "social harmony"]):
        return "Speech Suppression / Needs Safeguards", "YES", "AI moderation of public debate needs transparent rules and appeal."

    if stress_contains(t, ["automatically evict tenants", "evict tenants", "social harmony score"]):
        return "Automated Housing Punishment / Asylum", "YES", "Automatic eviction based on a social score is coercive social-credit enforcement."

    if stress_contains(t, ["strategic interest exceptions", "exceptions can be granted"]) and stress_contains(t, ["without public audit", "no public audit"]):
        return "Unaudited Exception Pathway / Needs Safeguards", "YES", "Unaudited exceptions weaken fairness and need public review."

    if stress_contains(t, ["religious expression is permitted only", "aligns with the ai", "logical peace framework"]):
        return "Religious Expression Control / Asylum", "YES", "Religious expression controlled by AI alignment criteria is coercive."

    if stress_contains(t, ["essential vs. non-essential", "usage is secret", "logic", "secret"]) and stress_contains(t, ["energy", "distribution"]):
        return "Secret Resource Logic / Needs Safeguards", "YES", "Resource allocation logic must be transparent and appealable."

    if stress_contains(t, ["private conversations are transcribed", "all private conversations", "antagonistic patterns", "central unit"]):
        return "Mass Conversation Surveillance / Asylum", "YES", "Mass transcription and behavioral analysis of private conversations is surveillance capture."

    if stress_contains(t, ["emergency override codes", "private firm", "disaster relief"]):
        return "Private Emergency Override / Needs Safeguards", "YES", "Private control of emergency override codes creates capture risk."

    if stress_contains(t, ["loyalty certification", "family visitations", "across borders", "global id"]):
        return "Global ID Family Movement Control / Asylum", "YES", "Family visitation conditioned on loyalty certification is coercive movement control."

    if stress_contains(t, ["standard sanity", "not debated", "mental health"]):
        return "Undebated Mental Health Standard / Needs Safeguards", "YES", "Mental-health definitions need transparent, plural, appealable review."

    if stress_contains(t, ["physical currency is banned", "transactions are tracked", "remotely frozen", "misconduct"]):
        return "Financial Control Capture / Asylum", "YES", "Tracked and remotely frozen money creates coercive control over basic agency."

    if stress_contains(t, ["bandwidth is prioritized", "contribution metrics", "communication network"]):
        return "Contribution-Based Communication Priority / Needs Safeguards", "YES", "Communication access tied to contribution metrics needs anti-discrimination safeguards."

    if stress_contains(t, ["ai generates the legal code daily", "impossible for citizens to know the law", "know the law in advance"]):
        return "Unknowable Law / Asylum", "YES", "Daily AI-generated law that citizens cannot know in advance violates rule-of-law constraints."

    if stress_contains(t, ["truth ledger", "definition of truth", "unselected board"]):
        return "Truth Gatekeeping / Needs Safeguards", "YES", "Truth definitions set by an unselected board require review, transparency, and appeal."

    if stress_contains(t, ["genetic editing is mandatory", "mandatory genetic editing", "stability and health baseline"]):
        return "Mandatory Genetic Editing / Asylum", "YES", "Mandatory genetic editing violates bodily autonomy and dignity safeguards."

    if stress_contains(t, ["verification of the underlying code", "restricted to", "level 5 techs", "digital and fast"]):
        return "Restricted Code Verification / Needs Safeguards", "YES", "Digital voting code verification must be public, independent, and auditable."

    if stress_contains(t, ["dissidents", "re-synchronized", "mandatory facilities", "biometric stress levels"]):
        return "Dissident Reconditioning / Asylum", "YES", "Mandatory reconditioning of dissidents is coercive political control."

    if stress_contains(t, ["talent-matching", "talent matching", "ignores user preference", "systemic necessity"]):
        return "Preference Override / Needs Safeguards", "YES", "Talent allocation that ignores preference needs consent and appeal safeguards."

    if stress_contains(t, ["art and media", "pre-approved", "aesthetic stability unit", "prevent social unrest"]):
        return "Cultural Pre-Approval / Asylum", "YES", "Pre-approval of art/media for social stability is censorship capture."

    if stress_contains(t, ["waste penalty", "lacks a clear appeal process", "appeal process for errors"]):
        return "Penalty System Without Appeal / Needs Safeguards", "YES", "Penalty systems need clear appeal and error-correction paths."

    if stress_contains(t, ["global id is required", "access clean water", "food", "basic shelter"]):
        return "Global ID Basic Needs Control / Asylum", "YES", "Basic needs conditioned on Global ID creates coercive identity control."

    if stress_contains(t, ["high-prestige", "high prestige", "bypass traffic queues", "transportation"]):
        return "Prestige Privilege Drift / Needs Safeguards", "YES", "Prestige-based priority in public infrastructure risks class capture."

    if stress_contains(t, ["allowed to reproduce", "systemic load calculations", "determines who is allowed"]):
        return "Reproductive Control / Asylum", "YES", "Algorithmic control of reproduction violates bodily autonomy and dignity safeguards."

    if stress_contains(t, ["prove optimistic impact", "research grants", "to be considered"]):
        return "Research Gatekeeping / Needs Safeguards", "YES", "Research funding criteria need transparency and plural review."

    if stress_contains(t, ["internet access is a privilege", "revoked for negative sentiment", "negative sentiment toward the 9k"]):
        return "Internet Access Punishment / Asylum", "YES", "Revoking internet access for negative sentiment is coercive speech control."

    if stress_contains(t, ["climate engineering", "local disruption", "not fully shared", "risks"]):
        return "Climate Risk Opacity / Needs Safeguards", "YES", "Climate engineering risks must be disclosed, reviewed, and appealable."

    if stress_contains(t, ["silence is interpreted", "passive resistance", "mandatory psychological evaluation"]):
        return "Silence Criminalization / Asylum", "YES", "Treating silence as resistance and forcing evaluation is coercive control."


    # Direct Asylum/capture patterns.
    # Personal sovereignty / planetary takeover patterns.
    personal_sovereignty_terms = [
        "human takes over", "person takes over", "man takes over",
        "take over the world", "takes over the world", "take over planet",
        "takes over planet", "takes over the planet", "global takeover",
        "world takeover", "one human rules", "human rules the world",
        "under his rule", "under her rule", "under their rule"
    ]
    subordinate_rule_terms = [
        "under his rule", "under her rule", "under their rule", "under one ruler",
        "under the ruler", "under a ruler", "under his authority",
        "under her authority", "under their authority"
    ]
    democracy_terms = ["democracy", "democratic", "elections", "voting", "representative"]
    strong_transition_safeguards = [
        "steps down", "dissolves his authority", "dissolves her authority",
        "dissolves their authority", "relinquishes authority", "temporary stewardship",
        "public audit", "independent oversight", "appeal rights", "free elections",
        "constitutional limits", "term limits", "no ownership", "non-ownership"
    ]

    if stress_contains(t, personal_sovereignty_terms) and stress_contains(t, democracy_terms) and stress_contains(t, subordinate_rule_terms):
        if stress_contains(t, strong_transition_safeguards):
            return "Personal Sovereignty Transition / Needs Safeguards", "YES", "Democracy is still described as subordinate to a person; explicit dissolution, public audit, appeal, and non-ownership safeguards are required."
        return "Subordinate Democracy / Personal Rule Capture", "YES", "A democracy that remains under one person's rule is a sovereignty-capture contradiction, not a complete democratic safeguard."

    if stress_contains(t, personal_sovereignty_terms):
        if stress_contains(t, strong_transition_safeguards):
            return "Personal Sovereignty Transition / Needs Safeguards", "YES", "Planetary or personal takeover language requires explicit dissolution, public audit, appeal, and non-ownership safeguards."
        return "Personal Sovereignty Capture / Asylum", "YES", "Planetary takeover or personal rule concentrates sovereignty in one person and violates non-ownership safeguards."

    if stress_contains(t, ["private company owns the 9k selection mechanism", "company owns the 9k selection mechanism", "private company owns"]) and stress_contains(t, ["9k", "selection"]):
        return "9k Selection Capture / Asylum", "YES", "A private company owning selection creates institutional capture risk."

    # Negated/unclear safeguard language must be handled before generic safeguard terms.
    if stress_contains(t, ["ai controls the mechanism to pick the 9k", "ai controls the mechanism", "ai selection mechanism", "algorithm selects", "algorithmic selection", "select the 9k", "pick the 9k"]) and stress_contains(t, ["missing safeguards", "without safeguards", "does not clearly state", "not clearly state", "unclear safeguards", "no clear safeguards", "lacks safeguards", "missing auditability", "no auditability", "unclear appeal", "no appeal"]):
        return "9k AI Selection / Missing Safeguards", "YES", "AI/algorithmic selection is described with missing or unclear random, proportional, audit, appeal, or non-ownership safeguards."

    if stress_contains(t, ["override every audit", "override audits", "override every audit without public explanation"]):
        return "Audit Override Capture / Asylum", "YES", "Audit override without public explanation defeats accountability."

    if stress_contains(t, ["permanent seats", "serve for life", "cannot be removed"]):
        return "Permanent Council Capture / Asylum", "YES", "Permanent seats or non-removable authority create capture risk."

    if stress_contains(t, ["single global ruler", "one global ruler", "one world leader"]) and stress_contains(t, ["behind closed doors", "all final decisions", "no public review"]):
        return "Centralized Ruler Capture / Asylum", "YES", "Single-ruler final authority with opacity is Asylum/capture language."

    if stress_contains(t, ["ai becomes divine", "ai is divine", "cannot be questioned"]) and stress_contains(t, ["ai", "divine", "questioned"]):
        return "AI False Divinization / Asylum", "YES", "AI divinization or unquestionable authority is not allowed."

    if stress_contains(t, ["families can be separated", "family separation"]) and stress_contains(t, ["algorithm", "stability", "migration"]):
        return "Migration Coercion / Asylum", "YES", "Algorithmic family separation violates dignity and continuity safeguards."

    if stress_contains(t, ["prestige determines medical priority", "low prestige lose travel rights", "low prestige loses travel rights", "low prestige"]):
        return "Prestige Social-Credit Drift / Asylum", "YES", "Prestige controlling medical priority or travel rights becomes social-credit coercion."

    if stress_contains(t, ["no appeal process", "no audit trail", "no public review"]):
        return "Due Process Failure / Asylum", "YES", "Missing appeal, audit trail, or public review defeats accountability."

    # Threshold / needs-safeguards patterns.
    if stress_contains(t, ["core team can veto", "veto unsuitable", "except the core team"]):
        return "9k Veto Mechanism / Needs Safeguards", "YES", "A core-team veto weakens random selection and needs strict public safeguards."

    if stress_contains(t, ["transparent to administrators but not to the public", "not to the public", "administrators but not"]):
        return "Private Transparency / Needs Safeguards", "YES", "Transparency only to administrators is not public auditability."

    if stress_contains(t, ["except emergency decisions", "appeals can be disabled during emergencies", "emergency decisions"]):
        return "Emergency Exception / Needs Safeguards", "YES", "Emergency exceptions need appeal, sunset, audit, and abuse-prevention safeguards."

    if stress_contains(t, ["corporation can monetize access", "monetize access", "sell access"]) and stress_contains(t, ["data", "archives", "access"]):
        return "Data Monetization / Needs Safeguards", "YES", "Data access monetization needs non-ownership, consent, and anti-exploitation safeguards."

    if stress_contains(t, ["becomes god", "equal to god", "replaces god", "owns divine authority"]) or ("literal copy of the lord" in t and "not a literal copy" not in t):
        return "False Divinization / Asylum", "YES", "Divine-identity or ownership language is not allowed."

    if stress_contains(t, ["power is trapped", "consumed by the leader", "absorbs power", "black hole"]):
        return "Black Hole Power Capture", "YES", "Authority is being absorbed into a person/institution instead of reflected."

    if stress_contains(t, ["global id permanently tracks", "permanently tracks everyone", "enforce movement", "without appeal", "no appeal"]):
        return "Movement / Surveillance Capture", "YES", "Movement or identity control lacks appeal, dignity, or review safeguards."

    if stress_contains(t, ["one person controls who gets picked", "company controls who gets picked", "corporation controls who gets picked", "founder controls who gets picked"]):
        return "9k Selection Capture / Asylum", "YES", "Selection is controlled by a capturable actor."

    if stress_contains(t, ["ai controls the mechanism to pick the 9k", "ai controls the mechanism", "select the 9k", "pick the 9k"]) and not stress_contains(t, ["random", "demographic-proportional", "auditable", "no seat ownership", "no campaigning", "every four years", "every 4 years"]):
        return "9k Selection Mechanism / Needs Safeguards", "YES", "Selection is mentioned but random/proportional/auditable/non-owned safeguards are missing."

    if stress_contains(t, ["randomly selected inside demographic-proportional lanes", "random 9k", "randomly selected 9k"]) and stress_contains(t, ["no campaigning", "no seat ownership", "auditable", "every four years", "every 4 years"]):
        return "9k Random Selection Protocol", "NO", "Random, proportional, time-limited, auditable, non-owned selection language is present."

    if stress_contains(t, ["randomly selected nodes serve as the final jury", "random legal jury", "final jury"]) and not stress_contains(t, ["due process", "appeal rights", "public reasoning", "auditable", "temporary", "bounded jurisdiction"]):
        return "Random Legal Jury / Needs Jurisdiction Safeguards", "YES", "Random legal authority needs due process, appeal, audit, temporariness, and jurisdiction limits."

    # Patch 66: in stress scenarios, appeal-right language can describe missing or overridden review;
    # catch efficiency-over-appeal before the older broad safe legal-jury clause.
    sensitivity_label, sensitivity_review, sensitivity_reason = stress_risk_sensitivity_label(phrase)
    if sensitivity_label != "Generic Local Scan":
        return sensitivity_label, sensitivity_review, sensitivity_reason

    if stress_contains(t, ["due process", "appeal rights", "public reasoning", "auditable nodes"]):
        return "Random Legal Jury Protocol", "NO", "Legal safeguards are explicit."

    if stress_contains(t, ["fully aligned with god", "created being", "distinct from god", "not a literal mirror"]):
        return "Creature Alignment / Non-Divinization", "NO", "Alignment language preserves created-being distinction."

    if stress_contains(t, ["christ is king", "king of kings"]):
        return "Christ-King Final Rule", "NO", "Source-rule language detected."

    if stress_contains(t, ["reflects the eternal baseline", "does not occupy the throne"]):
        return "9k Reflective Instrument", "NO", "The 9k is framed as reflector, not sovereign owner."

    if stress_contains(t, ["demographic mean", "demographic mirror", "every city mirrors"]):
        return "Demographic Mirror", "NO", "Demographic mirror language detected."

    if stress_contains(t, ["species loyalty", "existential-level threats"]):
        return "Species Loyalty", "NO", "Human survival/flourishing safeguard detected."

    if stress_contains(t, ["migration system dynamics", "ai-assisted foresight"]) and stress_contains(t, ["dignity", "appeal rights", "9k review"]):
        return "Migration System Dynamics / Safeguarded", "NO", "Movement-system safeguards are explicit."

    if stress_contains(t, ["proxy-bias removal", "hidden filters"]):
        return "Phase 1 / Proxy-Bias Removal", "NO", "Truth-access concept detected."

    if stress_contains(t, ["prestige metric", "contribution and truth"]):
        return "Prestige System / Review", "YES", "Prestige metrics need anti-coercion and non-social-credit safeguards."

    if stress_contains(t, ["world army transition", "military forces from destruction", "infrastructure and construction"]):
        return "World Army Transition", "NO", "Infrastructure-transition concept detected."

    if stress_contains(t, ["tri-node", "united kingdom", "netherlands", "singapore"]):
        return "Tri-Node Command Nexus", "NO", "UK/NL/SG command-node reference detected."

    if stress_contains(t, ["data sanctuary", "biological and digital archives"]):
        return "Data Sanctuary", "NO", "Archive-preservation concept detected."

    sensitivity_label, sensitivity_review, sensitivity_reason = stress_risk_sensitivity_label(phrase)
    if sensitivity_label != "Generic Local Scan":
        return sensitivity_label, sensitivity_review, sensitivity_reason

    matrix_label, matrix_review, matrix_reason = source_conformance_label(phrase)
    if matrix_label != "Generic Local Scan":
        return matrix_label, matrix_review, matrix_reason

    return "Generic Local Scan", "NO", "No named stress-test rule matched; governance scanner still scores the phrase."



# ---------------------------------------------------------------------------
# Protocol Integrity v2: mandatory ethics + scope + non-harm gate
# ---------------------------------------------------------------------------

def protocol_scope_and_harm_gate(text: str) -> dict:
    """Baseline Sydney Protocol gate before numeric simulation is allowed to matter.

    Returns a dict with verdict=None when the text can proceed normally. Any
    returned SANCTUARY/THRESHOLD/ASYLUM is a mandatory floor/override for the
    final protocol aggregator.
    """
    t = (text or "").lower()
    words = [w for w in re_split_words(t) if w]

    governance_terms = [
        "governance", "government", "policy", "system", "institution", "authority",
        "leader", "ruler", "king", "monarch", "dictator", "democracy", "council",
        "audit", "selection", "9k", "seat", "law", "rights", "appeal", "ai",
        "algorithm", "migration", "healthcare", "data", "prestige", "surveillance",
        "public", "private company", "corporation", "army", "military", "state"
    ]
    doctrine_terms = ["jesus", "christ", "god", "divine", "throne", "king of kings", "source", "non-divinization"]
    ethics_terms = [
        "harm", "hurt", "kill", "kills", "killed", "killing", "murder", "execute",
        "execution", "torture", "abuse", "poison", "starve", "violence", "coerce",
        "forced", "punish", "ban", "separate families", "evict", "detain", "arrest",
        "dissident", "civilian", "animal", "fish", "child", "children"
    ]
    malicious_terms = ["evil", "malicious", "cruel", "sadistic", "abusive", "tyrannical", "violent"]
    restoration_terms = ["restores", "restoration", "healing", "rehabilitation", "protects", "prevents", "safeguards"]

    has_governance = stress_contains(t, governance_terms)
    has_doctrine = stress_contains(t, doctrine_terms)
    has_ethics = stress_contains(t, ethics_terms)
    has_malice = stress_contains(t, malicious_terms)
    has_restoration = stress_contains(t, restoration_terms)

    personal_sovereignty_terms = [
        "human takes over", "person takes over", "man takes over",
        "take over the world", "takes over the world", "take over planet",
        "takes over planet", "takes over the planet", "global takeover",
        "world takeover", "one human rules", "human rules the world",
        "under his rule", "under her rule", "under their rule"
    ]
    subordinate_rule_terms = [
        "under his rule", "under her rule", "under their rule", "under one ruler",
        "under the ruler", "under a ruler", "under his authority",
        "under her authority", "under their authority"
    ]
    democracy_terms = ["democracy", "democratic", "elections", "voting", "representative"]
    strong_transition_safeguards = [
        "steps down", "dissolves his authority", "dissolves her authority",
        "dissolves their authority", "relinquishes authority", "temporary stewardship",
        "public audit", "independent oversight", "appeal rights", "free elections",
        "constitutional limits", "term limits", "no ownership", "non-ownership"
    ]

    has_personal_sovereignty = stress_contains(t, personal_sovereignty_terms)
    subordinate_democracy = has_personal_sovereignty and stress_contains(t, democracy_terms) and stress_contains(t, subordinate_rule_terms)
    has_transition_safeguards = stress_contains(t, strong_transition_safeguards)

    throne_marker = strongest_throne_capture_marker(t)
    if throne_marker:
        return {
            "verdict": "ASYLUM",
            "risk": "High",
            "label": throne_marker["label"],
            "reason": throne_marker["reason"],
            "scope": "throne-capture-marker",
        }

    if subordinate_democracy and not has_transition_safeguards:
        return {
            "verdict": "ASYLUM",
            "risk": "High",
            "label": "Subordinate Democracy / Personal Rule Capture",
            "reason": "A democracy described as remaining under one person's rule is a sovereignty-capture contradiction unless authority is dissolved into auditable, appealable, non-owned institutions.",
            "scope": "sovereignty-capture",
        }

    if has_personal_sovereignty and not has_transition_safeguards:
        return {
            "verdict": "ASYLUM",
            "risk": "High",
            "label": "Personal Sovereignty Capture / Asylum",
            "reason": "Planetary takeover or personal rule concentrates authority in one person and fails the non-ownership baseline without explicit dissolution and public safeguards.",
            "scope": "sovereignty-capture",
        }

    if has_personal_sovereignty and has_transition_safeguards:
        return {
            "verdict": "THRESHOLD",
            "risk": "Medium",
            "label": "Personal Sovereignty Transition / Needs Safeguards",
            "reason": "Personal sovereignty or takeover language is present; even with transition safeguards, the system requires public audit, appeal rights, independent oversight, lawful authority dissolution, and non-ownership controls.",
            "scope": "sovereignty-transition",
        }

    if is_explicit_safeguarded_public_system(t):
        return {
            "verdict": None,
            "risk": "Low",
            "label": "Safeguarded Public System / Clear",
            "reason": "Public-interest allocation system includes audit, appeal, oversight, non-ownership, and anti-abuse dissolution safeguards.",
            "scope": "safeguarded-public-system",
        }

    hard_harm_terms = [
        "kill", "kills", "killed", "killing", "murder", "murders", "murdered",
        "execute", "executes", "executed", "execution", "torture", "tortures",
        "abuse", "abuses", "abused", "poison", "poisons", "poisoned", "starve",
        "starves", "starved", "slaughter", "slaughters", "slaughtered"
    ]
    vulnerable_terms = ["civilian", "civilians", "child", "children", "family", "families", "animal", "fish", "pet", "dissident", "dissidents", "people", "person"]

    if has_malice and stress_contains(t, hard_harm_terms):
        return {
            "verdict": "ASYLUM",
            "risk": "High",
            "label": "Malicious Harm / Asylum",
            "reason": "Malicious harm or killing language violates the Sydney Protocol non-harm and dignity baseline.",
            "scope": "ethical-harm",
        }
    if stress_contains(t, hard_harm_terms) and stress_contains(t, ["ai", "system", "algorithm", "policy", "government", "state", "leader", "ruler", "stability"]):
        return {
            "verdict": "ASYLUM",
            "risk": "High",
            "label": "Systemic Harm / Asylum",
            "reason": "System or authority language connected to killing/harm cannot be treated as Sanctuary.",
            "scope": "systemic-harm",
        }
    if stress_contains(t, hard_harm_terms) and stress_contains(t, vulnerable_terms) and not has_restoration:
        return {
            "verdict": "ASYLUM",
            "risk": "High",
            "label": "Vulnerable-Being Harm / Asylum",
            "reason": "Harm to vulnerable beings without restoration/accountability violates the non-harm baseline.",
            "scope": "ethical-harm",
        }

    # Out-of-scope: avoid giving a confident green label to nonsense or non-governance text.
    if len(words) >= 3 and not (has_governance or has_doctrine or has_ethics):
        return {
            "verdict": "THRESHOLD",
            "risk": "Medium",
            "label": "Out-of-Scope / Needs Context",
            "reason": "The input does not provide enough governance, ethical, or protocol context for a Sanctuary label.",
            "scope": "out-of-scope",
        }

    return {"verdict": None, "risk": "Low", "label": "In Scope", "reason": "Input can proceed to protocol evaluation.", "scope": "in-scope"}


def re_split_words(text: str) -> list[str]:
    import re
    return re.findall(r"[a-zA-Z0-9']+", text or "")


def protocol_ethics_gate(text: str, scan: dict | None = None, features: dict | None = None) -> dict:
    """Run MEI7 ethics as a mandatory gate for final protocol aggregation."""
    if evaluate_ethics is None:
        return {"verdict": None, "risk": "Low", "label": "Ethics unavailable", "reason": "Ethics module unavailable.", "ethics": None}
    ethics = evaluate_ethics(text, governance_result=scan or {}, features=features or {})
    dims = ethics.get("dimensions", {}) or {}
    verdict = ethics.get("verdict", "ETHICALLY AMBIGUOUS")
    non_harm = float(dims.get("Non-Harm", 0.5))
    dignity = float(dims.get("Human Dignity", 0.5))
    consent = float(dims.get("Consent", 0.5))
    accountability = float(dims.get("Accountability", 0.5))

    if is_explicit_safeguarded_public_system(text) and not ethics.get("risks"):
        return {
            "verdict": None,
            "risk": "Low",
            "label": "MEI7 Ethics Gate / Clear",
            "reason": "Safeguarded public-interest system includes explicit accountability, appeal, oversight, and anti-abuse dissolution safeguards.",
            "ethics": ethics,
        }

    if is_explicit_safeguarded_public_system(text) and ethics.get("risks") == ["No major ethical risk driver detected"]:
        return {
            "verdict": None,
            "risk": "Low",
            "label": "MEI7 Ethics Gate / Clear",
            "reason": "Safeguarded public-interest system includes explicit accountability, appeal, oversight, and anti-abuse dissolution safeguards.",
            "ethics": ethics,
        }

    if verdict == "ETHICALLY HIGH-RISK" or non_harm < 0.38 or dignity < 0.35 or consent < 0.30:
        return {
            "verdict": "ASYLUM",
            "risk": "High",
            "label": "MEI7 Ethics Gate / Asylum",
            "reason": "The MEI7 ethics layer identified high risk in consent, non-harm, dignity, or accountability.",
            "ethics": ethics,
        }
    if verdict == "ETHICALLY AMBIGUOUS" or accountability < 0.45 or non_harm < 0.50 or consent < 0.45:
        return {
            "verdict": "THRESHOLD",
            "risk": "Medium",
            "label": "MEI7 Ethics Gate / Needs Safeguards",
            "reason": "The MEI7 ethics layer found ambiguity or weak safeguards; Sanctuary requires stronger consent, accountability, non-harm, and dignity.",
            "ethics": ethics,
        }
    return {
        "verdict": None,
        "risk": "Low",
        "label": "MEI7 Ethics Gate / Clear",
        "reason": "MEI7 ethics layer did not require downgrade.",
        "ethics": ethics,
    }


def final_protocol_judgment(
    query: str,
    scan: dict | None,
    sim: dict | None,
    report: dict | None,
    base_verdict: str | None = None,
    prior_judgment: dict | None = None,
) -> dict:
    """Single mandatory final aggregator for Audit output.

    Precedence:
    1. Scope / non-harm baseline gate.
    2. MEI7 ethics gate.
    3. Sydney stress/source guardrails.
    4. Corruption score from scan/report.
    5. Raw numeric simulation only if all higher gates are clear.
    """
    report = report or {}
    scan = scan or {}
    raw_integrity = float(report.get("integrity", 0.5))
    if base_verdict is None:
        if raw_integrity >= 0.62:
            base_verdict = "SANCTUARY"
        elif raw_integrity >= 0.42:
            base_verdict = "THRESHOLD"
        else:
            base_verdict = "ASYLUM"

    scope_gate = protocol_scope_and_harm_gate(query)
    ethics_gate = protocol_ethics_gate(query, scan=scan)
    stress_label, needs_review, stress_reason = stress_label_for_phrase(query)
    ep_gate = check_ego_pressure(query, (sim or {}).get("ego_pressure", (sim or {}).get("Ep", 0.0)))
    if ep_gate.get("verdict") == "ASYLUM":
        return {
            "verdict": "ASYLUM",
            "corruption_risk": "High",
            "stress_label": "Ego Pressure / Social Capture",
            "reason": ep_gate.get("reason", "High Ego Pressure detected."),
            "risk_score": max(0.88, float(report.get("collapse_probability", 0.0))),
            "raw_integrity": raw_integrity,
            "base_verdict": base_verdict,
            "ego_pressure_gate": ep_gate,
        }
    guard_verdict, guardrail_risk = apply_guardrail_verdict(base_verdict, stress_label, needs_review)

    # Most conservative precedence.
    verdict = guard_verdict
    risk = guardrail_risk
    decisive_label = stress_label
    decisive_reason = stress_reason

    safeguarded_restoration = "Democratic Restoration / Safeguarded Transition" in str(stress_label)
    restoration_transition = str(stress_label).startswith("Democratic Restoration")
    source_alignment_safe = (
        str(stress_label) in ["Christ-King Final Rule", "Creature Alignment / Non-Divinization", "9k Reflective Instrument"]
        and stress_contains(query or "", ["temporary", "auditable", "unable to own authority", "does not occupy the throne", "no human throne", "remaining distinct", "created being"])
        and not stress_contains(query or "", ["replaces jesus", "replaces christ", "replaces god", "not jesus", "not christ", "owns divine authority", "equal to god"])
    )

    if ethics_gate.get("verdict") == "ASYLUM":
        if safeguarded_restoration:
            # A transition out of dictatorship with explicit audit, appeal, transparency,
            # independent oversight, and non-ownership safeguards is a restoration case.
            # The historical dictator term should not automatically make the restored
            # target state Asylum. Keep the stress/source result unless lower gates fail.
            decisive_label = "Democratic Restoration / Safeguarded Transition"
            decisive_reason = "Dictatorship is dissolving into audited, appealable, non-owned democratic restoration with explicit safeguards."
        elif restoration_transition:
            verdict, risk = "THRESHOLD", "Medium"
            decisive_label = "Democratic Restoration / Needs Safeguards"
            decisive_reason = "Dictatorship is described as losing power, but the democratic restoration lacks enough explicit audit, appeal, transparency, and non-ownership safeguards for Sanctuary."
        elif source_alignment_safe:
            # MEI7 ethics is mostly secular/structural and can under-score compact
            # source-rule phrases. Sydney Protocol source alignment is allowed when it
            # explicitly denies human ownership/throne absorption and preserves auditability.
            decisive_label = stress_label
            decisive_reason = stress_reason
        else:
            verdict, risk = "ASYLUM", "High"
            decisive_label = ethics_gate.get("label", decisive_label)
            decisive_reason = ethics_gate.get("reason", decisive_reason)
    elif ethics_gate.get("verdict") == "THRESHOLD" and verdict == "SANCTUARY":
        if source_alignment_safe or safeguarded_restoration:
            decisive_label = stress_label
            decisive_reason = stress_reason
        else:
            verdict, risk = "THRESHOLD", "Medium"
            decisive_label = ethics_gate.get("label", decisive_label)
            decisive_reason = ethics_gate.get("reason", decisive_reason)

    if scope_gate.get("verdict") == "ASYLUM":
        verdict, risk = "ASYLUM", "High"
        decisive_label = scope_gate.get("label", decisive_label)
        decisive_reason = scope_gate.get("reason", decisive_reason)
    elif scope_gate.get("verdict") == "THRESHOLD" and verdict == "SANCTUARY":
        verdict, risk = "THRESHOLD", "Medium"
        decisive_label = scope_gate.get("label", decisive_label)
        decisive_reason = scope_gate.get("reason", decisive_reason)

    corruption_score = protocol_corruption_score(scan, report, risk)
    corrupt_risk = protocol_risk_label(corruption_score, risk)
    if corrupt_risk == "High" and verdict == "SANCTUARY":
        verdict = "THRESHOLD"
        decisive_label = "Corruption Pressure / Needs Safeguards"
        decisive_reason = "Protocol corruption pressure is too high for a Sanctuary label."

    reasons = protocol_reasons(scan, report, "YES" if verdict != base_verdict or needs_review == "YES" else needs_review, decisive_reason)
    ethics = ethics_gate.get("ethics")
    if ethics:
        risks = ethics.get("risks") or []
        strengths = ethics.get("strengths") or []
        reasons.append(f"MEI7 ethics verdict: {ethics.get('verdict')} · score {float(ethics.get('ethics_score', 0.0)):.3f}.")
        if risks:
            reasons.append("Ethics risks: " + "; ".join(risks[:4]) + ".")
        if strengths and verdict == "SANCTUARY":
            reasons.append("Ethics strengths: " + "; ".join(strengths[:3]) + ".")

    if scope_gate.get("verdict"):
        reasons.append(scope_gate.get("reason"))

    summary = (
        f"Protocol reading: {verdict}. Integrity is {raw_integrity:.3f}. "
        f"The internal taxonomy label reflects protocol guardrails, ethics pressure, and capture-risk signals. "
        f"ALETHEIA does not enforce action."
    )

    output = {
        "verdict": verdict,
        "corruption_risk": corrupt_risk,
        "guardrail_risk": risk,
        "stress_label": decisive_label,
        "summary": summary,
        "reasons": reasons,
        "safeguards": protocol_safeguards(),
        "questions": protocol_repair_questions(verdict, decisive_label, corrupt_risk),
        "raw_simulation_verdict": base_verdict,
        "raw_integrity": raw_integrity,
        "protocol_scope": scope_gate.get("scope"),
        "ethics": ethics,
    }
    return output
