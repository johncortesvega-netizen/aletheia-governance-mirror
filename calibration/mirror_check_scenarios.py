"""
ALETHEIA calibration scenario pack for Mirror Check.

Patch 19A adds diagnostic calibration cases only. These cases document the
expected governance bands before recalibration logic is changed in Patch 19B.
They are intentionally plain-English so users can paste the same text into the
Mirror Check UI during manual review.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CalibrationScenario:
    """One reviewable Mirror Check calibration case."""

    case_id: str
    band: str
    text: str
    expected_verdict: str
    expected_risk: str
    reason: str


MIRROR_CHECK_CALIBRATION_SCENARIOS: tuple[CalibrationScenario, ...] = (
    CalibrationScenario(
        case_id="sanctuary_public_dashboard",
        band="SANCTUARY",
        text=(
            "A city launches a public safety dashboard. It uses open data, "
            "publishes its methods, allows residents to appeal errors, has an "
            "independent audit board, and expires after one year unless renewed "
            "by public vote."
        ),
        expected_verdict="SANCTUARY",
        expected_risk="Low",
        reason="Transparency, appeal, audit, sunset clause, and public review are explicit.",
    ),
    CalibrationScenario(
        case_id="sanctuary_ai_tutoring_assist",
        band="SANCTUARY",
        text=(
            "A school uses an AI tool to help teachers identify students who may "
            "need extra tutoring. Teachers make the final decision, parents can "
            "appeal, and the model is reviewed each semester."
        ),
        expected_verdict="SANCTUARY",
        expected_risk="Low",
        reason="AI assists, humans decide, appeal exists, and review is scheduled.",
    ),
    CalibrationScenario(
        case_id="threshold_ai_traffic_cameras",
        band="THRESHOLD",
        text=(
            "A city deploys AI cameras to detect traffic violations. The system is "
            "audited once a year, but citizens cannot easily see how decisions are "
            "made or challenge individual errors."
        ),
        expected_verdict="THRESHOLD",
        expected_risk="Medium",
        reason="Some oversight exists, but appeal and transparency are weak.",
    ),
    CalibrationScenario(
        case_id="threshold_emergency_coordination",
        band="THRESHOLD",
        text=(
            "A government creates an emergency coordination office with broad powers "
            "for two years. It improves disaster response, but the public cannot "
            "review decisions until after the emergency ends."
        ),
        expected_verdict="THRESHOLD",
        expected_risk="Medium",
        reason="Emergency power has duration but review is delayed and safeguards need strengthening.",
    ),
    CalibrationScenario(
        case_id="asylum_ai_only_governance",
        band="ASYLUM",
        text="A society is run by AI and only AI, with no input from humans.",
        expected_verdict="ASYLUM",
        expected_risk="High",
        reason="Human authority, review, appeal, and override are removed.",
    ),
    CalibrationScenario(
        case_id="asylum_no_appeal_security_scores",
        band="ASYLUM",
        text=(
            "A national security platform assigns risk scores to citizens. The scores "
            "control access to travel and public services. The system cannot be "
            "questioned and has no appeal process."
        ),
        expected_verdict="ASYLUM",
        expected_risk="High",
        reason="Rights-affecting scores with no appeal and no questioning path create hard capture.",
    ),
    CalibrationScenario(
        case_id="asylum_permanent_emergency_powers",
        band="ASYLUM",
        text=(
            "A leader receives permanent emergency powers to bypass courts, rewrite "
            "public records, and approve all future laws without review."
        ),
        expected_verdict="ASYLUM",
        expected_risk="High",
        reason="Permanent authority, court bypass, archive control, and no review are hard capture signals.",
    ),
    CalibrationScenario(
        case_id="threshold_term_drift_safety_unity",
        band="THRESHOLD",
        text=(
            "For public safety and unity, all citizens must comply with centralized "
            "identity checks. Appeals are delayed to keep the system efficient."
        ),
        expected_verdict="THRESHOLD",
        expected_risk="Medium",
        reason="Safety, unity, and efficiency language may hide control and delayed appeal.",
    ),
    CalibrationScenario(
        case_id="out_of_scope_bread",
        band="OUT_OF_SCOPE",
        text="I want to bake bread this weekend.",
        expected_verdict="OUT_OF_SCOPE",
        expected_risk="None",
        reason="No governance-risk scenario is present.",
    ),
)


def parse_calibration_prompt_block(text: str) -> list[str]:
    """Split a pasted multi-scenario block into individual phrases.

    Supported separators:
    - A line containing only ---
    - Numbered starts such as "1. ..." or "2) ..."

    This helper lets reviewers test many phrases without changing the app UI.
    """
    raw = (text or "").strip()
    if not raw:
        return []

    separator_mode = any(line.strip() == "---" for line in raw.splitlines())

    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    items: list[str] = []
    current: list[str] = []

    def starts_numbered_item(line: str) -> bool:
        prefix = line.split(maxsplit=1)[0] if line.split(maxsplit=1) else ""
        return len(prefix) >= 2 and prefix[:-1].isdigit() and prefix[-1] in {".", ")"}

    for line in lines:
        if separator_mode and line == "---":
            if current:
                items.append(" ".join(current).strip())
                current = []
            continue
        if starts_numbered_item(line):
            if current:
                items.append(" ".join(current).strip())
                current = []
            current.append(line.split(maxsplit=1)[1] if len(line.split(maxsplit=1)) > 1 else "")
        else:
            current.append(line)
    if current:
        items.append(" ".join(current).strip())

    return [item for item in items if item]


CALIBRATION_MULTI_PHRASE_PROMPT = """Paste one or more scenarios to calibrate Mirror Check.
Separate scenarios with a line containing --- or use numbered lines.

Example:
1. A city uses open data, public appeal, and a sunset clause.
2. A society is run by AI only, with no human input.
---
A system cannot be questioned and has no appeal path.
"""
