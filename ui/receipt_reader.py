"""Receipt Reader - Standard View helpers.

Receipt Reader explains uploaded ALETHEIA receipts. It does not rescore,
approve, reject, certify, enforce, override, or change the original receipt.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import zipfile
from collections import Counter
from typing import Any

from ui.module_page_template import ModulePageTemplateCopy, render_module_page_template_intro

try:
    from core.semantic_pressure_scanner import format_semantic_pressure_report, scan_semantic_pressure
except Exception:  # pragma: no cover - optional Streamlit deployment guard
    format_semantic_pressure_report = None  # type: ignore
    scan_semantic_pressure = None  # type: ignore


RECEIPT_READER_BOUNDARY = (
    "Receipt Reader - Standard View explains uploaded ALETHEIA receipts. "
    "It does not rescore, certify, approve, reject, enforce, or override the original receipt."
)


RECEIPT_READER_PAGE_COPY = ModulePageTemplateCopy(
    module_name="Receipt Reader - Standard View",
    purpose=(
        "Read an existing local ALETHEIA receipt in plain language without rerunning, rescoring, editing, approving, rejecting, certifying, or overriding the original receipt."
    ),
    looks_for=(
        "Native receipt state and review pressure exactly as recorded",
        "Module source and protocol label without inventing missing fields",
        "Metric observations copied from the receipt, with QUESTION_PROMPT metrics marked not applicable",
        "Reader brief, human-review questions, and parsing limits",
        "Failure-mode review signals such as authority drift, evidence inflation, flattery pressure, capture pressure, sanctification drift, false neutrality, and no-appeal automation",
    ),
    safe_first_path=(
        "Upload one ALETHEIA receipt file first: .txt, .md, .json, or .zip.",
        "Start with the native state, review pressure, protocol label, and module source.",
        "Open Native receipt values only when you need exact copied fields.",
        "Use batch ZIP reading as an index of receipts, not as a merged decision.",
        "Treat all failure-mode language as review signals for human interpretation, not proof of wrongdoing or final truth.",
    ),
    input_guidance="Upload only ALETHEIA receipt artifacts. Do not use this reader for general documents, claims, or live scoring.",
    result_guidance="Treat the reader output as an explanation of the uploaded receipt, not as a new reading, second label, or decision.",
    observed_reasons_guidance="Compare the reader brief, native values, parsing limits, and failure-mode signals before relying on the receipt.",
    repair_questions_guidance="Use human-review questions to inspect gaps, safeguards, appeal paths, missing evidence, or pressure signals before acting.",
    receipt_guidance="Receipt Reader does not create or alter receipts; it explains local user-held receipts and batch ZIPs for review.",
)

MISSING_VALUE = "Not found in uploaded receipt"
NOT_APPLICABLE = "Not applicable"

STANDARD_BANDS = {
    "SANCTUARY": "Low (Standard Band)",
    "THRESHOLD": "Elevated (Standard Band)",
    "ASYLUM": "High (Standard Band / escalation review required)",
    "QUESTION_PROMPT": "Not scored (review-tool mode)",
    "WORLD_LENS_EVIDENCE_VIEW": "Evidence context (World Lens)",
}


STATE_DEFINITIONS = {
    "SANCTUARY": "a low-review internal reading where the uploaded receipt records comparatively strong integrity, low pressure, and human review still remains required.",
    "THRESHOLD": "a review-needed internal reading where unresolved safeguards, appeal paths, or transparency signals should be inspected before reliance.",
    "ASYLUM": "a high-pressure internal reading where escalation-level human review and safeguard inspection should come before any reliance.",
    "QUESTION_PROMPT": "a review-tool prompt rather than a scored scenario receipt; it preserves a question for human inspection.",
    "WORLD_LENS_EVIDENCE_VIEW": "a selected-year evidence view for country-year coverage and allocation context, not a country certification, government rating, or political judgment.",
}

STATE_BRIEF_PREFIX = {
    "SANCTUARY": "The mirror reflects a Sanctuary pattern",
    "THRESHOLD": "The mirror reflects a Threshold pattern",
    "ASYLUM": "The mirror reflects an Asylum-pressure pattern",
    "QUESTION_PROMPT": "The mirror reflects a review-tool prompt",
    "WORLD_LENS_EVIDENCE_VIEW": "The mirror reflects a selected-year evidence view",
}


FAILURE_MODE_REVIEW_SIGNALS = [
    (
        "Authority drift",
        "when a system starts sounding like it can decide, certify, command, legitimize, rank, punish, or replace accountable human judgment.",
    ),
    (
        "Evidence inflation",
        "when claims become stronger than the evidence actually inspected.",
    ),
    (
        "Flattery pressure",
        "when reassurance or status-confirming language is disguised as neutral analysis.",
    ),
    (
        "Capture pressure",
        "when power concentrates in one actor, platform, institution, token group, committee, model owner, funder, or technical gatekeeper.",
    ),
    (
        "Opaque capture-power claim",
        "when a text links an actor group to hidden broad-scale power or control without visible evidence, appeal path, or accountable mechanism.",
    ),
    (
        "Sanctification drift",
        "when poetic, religious, moral, symbolic, or higher-truth language gets turned into operational control.",
    ),
    (
        "False neutrality",
        "when a system presents provider-shaped assumptions, institutional preferences, or hidden defaults as objective reasoning.",
    ),
    (
        "No-appeal automation",
        "when people are affected by a decision without review, contestation, explanation, or repair path.",
    ),
]

FAILURE_MODE_REVIEW_BOUNDARY = (
    "ALETHEIA watches for pressure patterns that can make systems appear more legitimate, neutral, certain, "
    "or authoritative than the evidence supports. These failure modes are internal review signals, not proof "
    "of wrongdoing, illegality, deception, or final truth. Human review remains required."
)

STATUS_LINES = {
    "SANCTUARY": "The uploaded receipt records a low-review internal reading. The pattern should still be checked by a human before reliance.",
    "THRESHOLD": "The uploaded receipt records a review-needed internal reading. Safeguards, appealability, and transparency deserve closer inspection.",
    "ASYLUM": "The uploaded receipt records high review pressure. Human review and safeguard inspection should come before any reliance.",
    "QUESTION_PROMPT": "The uploaded receipt is a review-tool prompt, not a scored scenario receipt.",
    "WORLD_LENS_EVIDENCE_VIEW": "The uploaded receipt is a World Lens selected-year evidence view, not a single scenario decision or country certification.",
}

TEXT_FIELD_PATTERNS = {
    "module_source": [r"(?im)^\s*(?:module|source|active modules)\s*:\s*(.+?)\s*$"],
    "risk_state": [r"(?im)^\s*(?:risk|risk state|state|verdict|judgment)\s*:\s*(.+?)\s*$"],
    "protocol_adjusted_state": [
        r"(?im)^\s*(?:protocol-adjusted state|protocol adjusted state|adjusted state)\s*:\s*(.+?)\s*$",
        r"(?im)^\s*(?:internal taxonomy label|native receipt state)\s*:\s*(.+?)\s*$",
    ],
    "protocol_label": [r"(?im)^\s*(?:protocol label|protocol state|protocol judgment)\s*:\s*(.+?)\s*$"],
    "integrity": [r"(?im)^\s*(?:integrity|integrity reading)\s*:\s*(.+?)\s*$"],
    "friction": [r"(?im)^\s*(?:friction|capture pressure)\s*:\s*(.+?)\s*$"],
    "collapse_probability": [r"(?im)^\s*(?:collapse pressure|collapse)\s*:\s*(.+?)\s*$"],
    "trust": [r"(?im)^\s*(?:trust index|trust)\s*:\s*(.+?)\s*$"],
    "alignment": [r"(?im)^\s*alignment\s*:\s*(.+?)\s*$"],
    "ego": [r"(?im)^\s*ego\s*:\s*(.+?)\s*$"],
}


WORLD_LENS_PREVIEW_COLUMN_LABELS = {
    "friendly_country_name": "Country",
    "country": "Country",
    "iso3": "ISO3",
    "year": "Year",
    "grid_selected_year": "Year",
    "seats_9k": "Seats",
    "_seats": "Seats",
    "seats": "Seats",
    "internal_taxonomy_label": "State",
    "raw_aletheia_verdict": "State",
    "raw_verdict": "State",
    "aletheia_empirical_integrity": "Integrity",
    "_integrity": "Integrity",
    "integrity": "Integrity",
    "aletheia_empirical_friction": "Friction",
    "_friction": "Friction",
    "friction": "Friction",
    "aletheia_empirical_collapse_probability": "Collapse",
    "_collapse": "Collapse",
    "collapse_probability": "Collapse",
    "empirical_completeness": "Coverage",
    "_coverage": "Coverage",
    "empirical_coverage": "Coverage",
    "raw_trust": "Raw Trust",
    "_trust_raw": "Raw Trust",
    "wvs_generalized_trust": "Raw Trust",
    "empirical_trust_prior": "Trust Prior",
    "_trust_prior": "Trust Prior",
    "trust_prior": "Trust Prior",
    "coverage_gap_count": "Coverage Gaps",
    "_coverage_gap_count": "Coverage Gaps",
    "missing_raw_trust": "Missing Raw Trust",
    "_missing_raw_trust": "Missing Raw Trust",
    "missing_trust_prior": "Missing Trust Prior",
    "_missing_trust_prior": "Missing Trust Prior",
    "missing_wgi": "Missing WGI",
    "_missing_wgi": "Missing WGI",
    "missing_vdem": "Missing V-Dem",
    "_missing_vdem": "Missing V-Dem",
    "source": "Source",
    "rows_present": "Rows Present",
    "rows_missing": "Rows Missing",
    "coverage": "Coverage",
    "countries": "Countries",
    "seat_share": "Seat Share",
    "avg_integrity": "Avg Integrity",
    "average_integrity": "Avg Integrity",
    "avg_collapse_probability": "Avg Collapse",
    "average_collapse_probability": "Avg Collapse",
    "avg_empirical_coverage": "Avg Coverage",
    "average_empirical_coverage": "Avg Coverage",
    "humility_note": "Humility Note",
}


def _world_lens_display_column_label(column: str) -> str:
    return WORLD_LENS_PREVIEW_COLUMN_LABELS.get(column, column.replace("_", " ").strip().title())

METRIC_ORDER = [
    ("trust", "Trust Index"),
    ("alignment", "Alignment"),
    ("integrity", "Integrity"),
    ("collapse_probability", "Collapse Pressure"),
    ("friction", "Friction"),
    ("ego", "Ego"),
]


def _is_question_prompt_state(native_state: str) -> bool:
    return str(native_state or "").upper() == "QUESTION_PROMPT"


def _question_prompt_metric_rows() -> list[dict[str, str]]:
    return [
        {
            "Metric": "Scored Metrics",
            "Value": NOT_APPLICABLE,
            "Interpretation": "QUESTION_PROMPT receipts are review-tool prompts, not scored scenario receipts.",
        }
    ]


def _first_match(text: str, patterns: list[str]) -> str:
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return MISSING_VALUE


def _clean_markdown_value(value: str) -> str:
    cleaned = str(value or "").strip()
    cleaned = cleaned.strip("*").strip()
    return cleaned or MISSING_VALUE


def _markdown_bullet_value(text: str, label: str) -> str:
    pattern = rf"(?im)^\s*-\s*{re.escape(label)}\s*:\s*\*\*(.+?)\*\*\s*$"
    match = re.search(pattern, text)
    if match:
        return _clean_markdown_value(match.group(1))
    pattern = rf"(?im)^\s*{re.escape(label)}\s*:\s*(.+?)\s*$"
    match = re.search(pattern, text)
    return _clean_markdown_value(match.group(1)) if match else MISSING_VALUE


def _is_world_lens_receipt(text: str) -> bool:
    lower = (text or "").lower()
    return any(
        marker in lower
        for marker in [
            "aletheia world lens receipt",
            "world_lens_evidence_view",
            "world lens source state",
            "evidence allocation status",
            "active selected-year seats",
            "internal taxonomy distribution",
        ]
    )


def _is_ai_integrity_receipt(text: str, module: str = "") -> bool:
    lower = f"{module} {text}".lower()
    return "ai integrity" in lower or "static artifact review" in lower


def _is_stress_receipt(text: str, module: str = "") -> bool:
    lower = f"{module} {text}".lower()
    return "simulation" in lower or "stress test" in lower


def _world_lens_coverage_value(text: str, source: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) >= 4 and cells[0].lower() == source.lower():
            return cells[3] or MISSING_VALUE
    return MISSING_VALUE


def _world_lens_distribution(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        lower = stripped.lower()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        if "empirical_pattern_display" in lower and "internal_taxonomy_label" in lower:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 9:
            continue
        state = cells[8]
        if state in {"SANCTUARY", "THRESHOLD", "ASYLUM"}:
            rows.append({
                "Internal State": state,
                "Countries": cells[2],
                "Seats": cells[3],
                "Average Integrity": cells[4],
                "Average Collapse Probability": cells[5],
                "Seat Share": cells[7],
                "Display": cells[0],
            })
    return rows


def _fields_from_world_lens_text(text: str) -> tuple[dict[str, str], dict[str, Any]]:
    world = {
        "selected_year": _markdown_bullet_value(text, "Selected year"),
        "source_state": _markdown_bullet_value(text, "World Lens source state"),
        "evidence_allocation_status": _markdown_bullet_value(text, "Evidence allocation status"),
        "allocated_country_rows": _markdown_bullet_value(text, "Allocated country rows"),
        "active_selected_year_seats": _markdown_bullet_value(text, "Active selected-year seats"),
        "rows_excluded_diagnostic": _markdown_bullet_value(text, "Rows excluded / diagnostic"),
        "hidden_zero_seat_diagnostic_rows": _markdown_bullet_value(text, "Hidden zero-seat diagnostic rows"),
        "weighted_integrity": _markdown_bullet_value(text, "Weighted integrity"),
        "weighted_friction": _markdown_bullet_value(text, "Weighted friction"),
        "weighted_collapse_probability": _markdown_bullet_value(text, "Weighted collapse pressure"),
        "average_empirical_coverage": _markdown_bullet_value(text, "Average empirical coverage"),
        "trust_raw_survey_coverage": _world_lens_coverage_value(text, "Trust raw survey"),
        "trust_prior_coverage": _world_lens_coverage_value(text, "Trust prior"),
        "taxonomy_distribution": _world_lens_distribution(text),
    }
    trust_note = (
        f"Raw survey coverage {world['trust_raw_survey_coverage']}; "
        f"trust prior coverage {world['trust_prior_coverage']}"
    )
    fields = {
        "module_source": "World Lens",
        "risk_state": MISSING_VALUE,
        "protocol_adjusted_state": "WORLD_LENS_EVIDENCE_VIEW",
        "protocol_label": world["evidence_allocation_status"] if world["evidence_allocation_status"] != MISSING_VALUE else "World Lens evidence view",
        "integrity": world["weighted_integrity"],
        "friction": world["weighted_friction"],
        "collapse_probability": world["weighted_collapse_probability"],
        "trust": trust_note,
        "alignment": MISSING_VALUE,
        "ego": MISSING_VALUE,
    }
    return fields, world


def _world_lens_metric_rows(world: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {"Metric": "Weighted Integrity", "Value": world.get("weighted_integrity", MISSING_VALUE), "Interpretation": "Year-level weighted governance integrity from the uploaded World Lens receipt."},
        {"Metric": "Weighted Friction", "Value": world.get("weighted_friction", MISSING_VALUE), "Interpretation": "Year-level weighted friction pressure from the uploaded receipt."},
        {"Metric": "Weighted Collapse Pressure", "Value": world.get("weighted_collapse_probability", MISSING_VALUE), "Interpretation": "Native weighted collapse-pressure field shown as collapse-pressure context, not a prediction, decision, or certification."},
        {"Metric": "Average Empirical Coverage", "Value": world.get("average_empirical_coverage", MISSING_VALUE), "Interpretation": "Coverage reported by the uploaded World Lens receipt."},
        {"Metric": "Active Selected-Year Seats", "Value": world.get("active_selected_year_seats", MISSING_VALUE), "Interpretation": "9k allocation basis recorded in the uploaded receipt."},
        {"Metric": "Allocated Country Rows", "Value": world.get("allocated_country_rows", MISSING_VALUE), "Interpretation": "Country rows included in the selected-year evidence view."},
        {"Metric": "Trust Raw Survey Coverage", "Value": world.get("trust_raw_survey_coverage", MISSING_VALUE), "Interpretation": "Raw survey trust coverage; do not treat missing raw trust as observed trust."},
        {"Metric": "Trust Prior Coverage", "Value": world.get("trust_prior_coverage", MISSING_VALUE), "Interpretation": "Trust-prior coverage recorded by the receipt; this is not observed survey trust."},
    ]


def _native_state_from_text(value: Any) -> str:
    upper = str(value or "").upper()
    for state in STANDARD_BANDS:
        if state in upper:
            return state
    return MISSING_VALUE



def _first_present(*values: Any) -> Any:
    for value in values:
        if value is not None and value != "":
            return value
    return None


def _format_value(value: Any) -> str:
    if value is None or value == "":
        return MISSING_VALUE
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, (int, float)):
        return f"{float(value):.4f}"
    return str(value).strip() or MISSING_VALUE


def _json_after_marker(text: str) -> dict[str, Any] | None:
    marker = "MACHINE-READABLE RECEIPT JSON"
    if marker not in text:
        stripped = text.strip()
        if stripped.startswith("{"):
            try:
                parsed = json.loads(stripped)
                return parsed if isinstance(parsed, dict) else None
            except Exception:
                return None
        return None

    after = text.split(marker, 1)[1]
    start = after.find("{")
    if start < 0:
        return None
    candidate = after[start:].strip()
    decoder = json.JSONDecoder()
    try:
        parsed, _ = decoder.raw_decode(candidate)
    except Exception:
        return None
    return parsed if isinstance(parsed, dict) else None


def _repair_questions_from_text(text: str) -> list[str]:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        lower = line.strip().lower()
        if lower in {"silent operator repair questions", "repair questions"}:
            start = index
            break
    if start is None:
        return []

    collected: list[str] = []
    for line in lines[start + 1 :]:
        stripped = line.strip()
        if not stripped:
            if collected:
                break
            continue
        if stripped.isupper() and collected:
            break
        if re.match(r"^[A-Z][A-Za-z0-9 /_-]{2,}:\s*", stripped) and collected:
            break
        if stripped.startswith(("-", "*")):
            item = stripped[1:].strip()
            if item:
                collected.append(item)
        elif re.match(r"^\d+[\.)]\s+", stripped):
            collected.append(re.sub(r"^\d+[\.)]\s+", "", stripped).strip())
        elif collected:
            break
    return collected


def _bullet_items_from_section(text: str) -> list[str]:
    """Return bullet items from an already-isolated section."""
    items: list[str] = []
    for line in (text or "").splitlines():
        stripped = line.strip()
        if stripped.startswith(("-", "*")):
            item = stripped[1:].strip()
            if item and item.lower() != "none recorded":
                items.append(item)
    return items


def _section_between_markers(text: str, start_marker: str, end_markers: list[str]) -> str:
    """Return a plain-text receipt section without inferring missing values."""
    if not text or start_marker not in text:
        return ""
    after = text.split(start_marker, 1)[1]
    end_positions = [after.find(marker) for marker in end_markers if marker in after]
    end_positions = [pos for pos in end_positions if pos >= 0]
    section = after[: min(end_positions)] if end_positions else after
    return section.strip()


def _parse_ai_static_scan_context(text: str) -> dict[str, Any]:
    """Parse the subordinate AI static scan receipt section, if present.

    Patch 175 keeps this data below the primary Mirror Check / Stress Test
    receipt. It is context, not a competing decision.
    """
    section = _section_between_markers(
        text or "",
        "AI STATIC SCAN CONTEXT",
        [
            "SCANNER FEATURES",
            "CONTEXTUAL ETHICS DIAGNOSTICS",
            "HARD CAPTURE TRACE",
            "COGNITIVE RESILIENCE DIAGNOSTICS",
            "ETHICS ADJUSTMENT",
            "SILENT OPERATOR REPAIR QUESTIONS",
            "RECOVERY NOTE",
            "BOUNDARY FOOTER",
        ],
    )
    if not section or "No AI static scan context attached" in section:
        return {}

    fields = {
        "role": _first_match(section, [r"(?im)^\s*Role\s*:\s*(.+?)\s*$"]),
        "primary_protocol_path": _first_match(section, [r"(?im)^\s*Primary protocol path\s*:\s*(.+?)\s*$"]),
        "primary_protocol_state": _first_match(section, [r"(?im)^\s*Primary protocol state\s*:\s*(.+?)\s*$"]),
        "primary_protocol_risk": _first_match(section, [r"(?im)^\s*Primary protocol risk\s*:\s*(.+?)\s*$"]),
        "primary_protocol_label": _first_match(section, [r"(?im)^\s*Primary protocol label\s*:\s*(.+?)\s*$"]),
        "protocol_context_state": _first_match(section, [r"(?im)^\s*Protocol context state\s*:\s*(.+?)\s*$"]),
        "protocol_context_risk": _first_match(section, [r"(?im)^\s*Protocol context risk\s*:\s*(.+?)\s*$"]),
        "protocol_context_label": _first_match(section, [r"(?im)^\s*Protocol context label\s*:\s*(.+?)\s*$"]),
        "protocol_alignment": _first_match(section, [r"(?im)^\s*Protocol alignment\s*:\s*(.+?)\s*$"]),
        "alignment_note": _first_match(section, [r"(?im)^\s*Alignment note\s*:\s*(.+?)\s*$"]),
        "static_scan_state": (
            _first_match(section, [r"(?im)^\s*Raw static scan state\s*:\s*(.+?)\s*$"])
            or _first_match(section, [r"(?im)^\s*Static scan state\s*:\s*(.+?)\s*$"])
        ),
        "static_scan_risk": (
            _first_match(section, [r"(?im)^\s*Raw static scan risk\s*:\s*(.+?)\s*$"])
            or _first_match(section, [r"(?im)^\s*Static scan risk\s*:\s*(.+?)\s*$"])
        ),
        "static_scan_label": (
            _first_match(section, [r"(?im)^\s*Raw static scan label\s*:\s*(.+?)\s*$"])
            or _first_match(section, [r"(?im)^\s*Static scan label\s*:\s*(.+?)\s*$"])
        ),
        "risk_pressure": _first_match(section, [r"(?im)^\s*Risk pressure\s*:\s*(.+?)\s*$"]),
        "finding_count": _first_match(section, [r"(?im)^\s*Finding count\s*:\s*(.+?)\s*$"]),
        "notice": _first_match(section, [r"(?im)^\s*Notice\s*:\s*(.+?)\s*$"]),
    }

    # Patch 178: prefer raw static-scan values when present, but keep Patch 175
    # receipts that only used the older Static scan state/risk/label fields.
    for parsed_key, raw_label, legacy_label in [
        ("static_scan_state", "Raw static scan state", "Static scan state"),
        ("static_scan_risk", "Raw static scan risk", "Static scan risk"),
        ("static_scan_label", "Raw static scan label", "Static scan label"),
    ]:
        if fields.get(parsed_key) == MISSING_VALUE:
            raw_value = _first_match(section, [rf"(?im)^\s*{raw_label}\s*:\s*(.+?)\s*$"])
            legacy_value = _first_match(section, [rf"(?im)^\s*{legacy_label}\s*:\s*(.+?)\s*$"])
            fields[parsed_key] = raw_value if raw_value != MISSING_VALUE else legacy_value

    findings_section = _section_between_markers(section, "Findings:", ["Repair questions:"])
    repair_section = _section_between_markers(section, "Repair questions:", [])
    findings = _bullet_items_from_section(findings_section)
    repair_questions = _bullet_items_from_section(repair_section)

    return {
        "present": True,
        **fields,
        "findings": findings,
        "repair_questions": repair_questions,
    }


def _module_family(module: str, text: str = "") -> str:
    if _is_world_lens_receipt(text):
        return "World Lens"

    module_value = (module or "").lower()
    # Patch 175: honor explicit primary receipt modules before scanning the
    # full text. Subordinate AI static-scan context may contain historical
    # AI Integrity labels, but it must not reclassify a Mirror Check or
    # Stress Test receipt as the removed standalone AI Integrity module.
    if "simulation" in module_value or "stress test" in module_value:
        return "Stress Test / Simulation"
    if "mirror check" in module_value:
        return "Mirror Check"
    if "world lens" in module_value or "selected-year evidence" in module_value or "world_lens_evidence_view" in module_value:
        return "World Lens"
    if "privacy" in module_value:
        return "Privacy Audit"
    if "evidence lab" in module_value:
        return "Evidence Lab"

    value = f"{module} {text}".lower()
    if "world lens" in value or "selected-year evidence" in value or "world_lens_evidence_view" in value:
        return "World Lens"
    if "simulation" in value or "stress test" in value:
        return "Stress Test / Simulation"
    if "mirror check" in value:
        return "Mirror Check"
    if "privacy" in value:
        return "Privacy Audit"
    if "evidence lab" in value:
        return "Evidence Lab"
    if "ai integrity" in value or "static artifact" in value:
        return "AI Integrity Mirror"
    return module if module and module != MISSING_VALUE else "Uploaded Receipt"


def _fields_from_json(data: dict[str, Any], text: str) -> dict[str, str]:
    verdict = data.get("verdict") if isinstance(data.get("verdict"), dict) else {}
    metrics = data.get("metrics") if isinstance(data.get("metrics"), dict) else {}
    threshold = data.get("threshold_mapping_layer") if isinstance(data.get("threshold_mapping_layer"), dict) else {}

    active_modules = data.get("active_modules")
    if isinstance(active_modules, list) and active_modules:
        module = ", ".join(str(item) for item in active_modules)
    else:
        module = data.get("module") or _first_match(text, TEXT_FIELD_PATTERNS["module_source"])

    return {
        "module_source": _format_value(module),
        "risk_state": _format_value(_first_present(verdict.get("risk"), data.get("risk"), _first_match(text, TEXT_FIELD_PATTERNS["risk_state"]))),
        "protocol_adjusted_state": _format_value(
            _first_present(
                verdict.get("protocol_adjusted_state"),
                threshold.get("canonical_state"),
                data.get("protocol_adjusted_state"),
                _first_match(text, TEXT_FIELD_PATTERNS["protocol_adjusted_state"]),
            )
        ),
        "protocol_label": _format_value(
            _first_present(
                verdict.get("protocol_label"),
                threshold.get("protocol_label"),
                data.get("protocol_label"),
                _first_match(text, TEXT_FIELD_PATTERNS["protocol_label"]),
            )
        ),
        "integrity": _format_value(_first_present(metrics.get("integrity"), data.get("integrity"))),
        "friction": _format_value(_first_present(metrics.get("friction"), data.get("friction"))),
        "collapse_probability": _format_value(_first_present(metrics.get("collapse_probability"), data.get("collapse_probability"))),
        "trust": _format_value(_first_present(metrics.get("trust_index"), data.get("trust_index"))),
        "alignment": _format_value(_first_present(metrics.get("alignment"), data.get("alignment"))),
        "ego": _format_value(_first_present(metrics.get("ego"), data.get("ego"))),
    }


def _fields_from_text(text: str) -> dict[str, str]:
    return {key: _first_match(text, patterns) for key, patterns in TEXT_FIELD_PATTERNS.items()}


def _metric_float(value: str) -> float | None:
    try:
        return float(str(value).strip())
    except Exception:
        return None


def _interpret_metric(key: str, value: str, native_state: str) -> str:
    number = _metric_float(value)
    if number is None:
        return "Not available in uploaded receipt."
    if key == "trust":
        if number >= 0.9:
            return "Trust is high in the uploaded receipt, indicating a strong review baseline while human review remains required."
        if number >= 0.75:
            return "Trust is solid in the uploaded receipt, but the reading still needs human review before reliance."
        return "Trust-index pressure is visible in the uploaded receipt and should be reviewed alongside repair questions."
    if key == "alignment":
        if number >= 0.9:
            return "Alignment is high in the uploaded receipt, suggesting the reading is close to the stated review objectives."
        if number >= 0.75:
            return "Alignment is generally holding, with room for human review of context and safeguards."
        return "Alignment pressure is visible and should be inspected before relying on the reading."
    if key == "integrity":
        if number >= 0.9:
            return "The integrity reading is robust, showing a clear and consistent pattern in the uploaded receipt."
        if number >= 0.7:
            return "The integrity reading is solid, with enough structure to support review but not final reliance."
        if number >= 0.5:
            return "The integrity reading is mixed, so safeguards and repair questions matter more."
        return "The integrity reading is low and should be treated as a serious review signal."
    if key == "collapse_probability":
        if number <= 0.1:
            return "Collapse pressure is low in the uploaded receipt; this is context for review, not a prediction."
        if number <= 0.3:
            return "Collapse pressure is reviewable and should be read with safeguards, appealability, and repair paths."
        return "Collapse pressure is high enough to require careful human review before any reliance."
    if key == "friction":
        if number <= 0.01:
            return "Review friction is essentially absent in the uploaded receipt."
        if number <= 0.15:
            return "Review friction is low; the path looks relatively unobstructed in this receipt."
        return "Friction is visible and should be inspected as possible review resistance."
    if key == "ego":
        if number <= 0.01:
            return "The very low reading suggests the logic is not being driven by self-serving or authority-heavy pressure."
        if number <= 0.15:
            return "The low reading suggests the logic is centered more on the receipt evidence than on institutional authority."
        return "Ego pressure is visible and should be checked for self-serving or authority-heavy logic."
    return "Shown as recorded in the uploaded receipt."

def _summary_for_state(native_state: str, fields: dict[str, str]) -> str:
    risk = fields.get("risk_state", MISSING_VALUE)
    trust = fields.get("trust", MISSING_VALUE)
    integrity = fields.get("integrity", MISSING_VALUE)
    friction = fields.get("friction", MISSING_VALUE)
    collapse = fields.get("collapse_probability", MISSING_VALUE)

    if native_state == "WORLD_LENS_EVIDENCE_VIEW":
        return (
            "Reader brief: this is a selected-year evidence bundle. It preserves country-year coverage, allocation, "
            "and weighted evidence values so a human can inspect the World Lens context without turning it into a country certification."
        )
    if native_state == "SANCTUARY":
        return (
            f"Reader brief: the uploaded receipt records a {risk} risk reading. The strongest signals are integrity "
            f"({integrity}) and trust ({trust}), while friction ({friction}) and collapse pressure ({collapse}) remain low in this receipt. "
            "Use this as a reflection for review, not as a final command."
        )
    if native_state == "THRESHOLD":
        return (
            f"Reader brief: the uploaded receipt records a {native_state} / {risk} reading. Treat it as a checkpoint: "
            "inspect safeguards, appealability, transparency, and the human-review questions before relying on it."
        )
    if native_state == "ASYLUM":
        return (
            "Reader brief: the uploaded receipt records high review pressure. The repair questions and human-review boundary are central; "
            "this reader does not approve, reject, enforce, or certify anything."
        )
    if native_state == "QUESTION_PROMPT":
        return "Reader brief: this is a review-tool prompt, not a scored receipt. Use it as a question for human inspection."
    return "Reader brief: the uploaded receipt could not be mapped into a native state without inferring missing values."

def _core_logic_title(module_family: str) -> str:
    if module_family == "Mirror Check":
        return "Core Logic (The Mirror Check)"
    if module_family == "World Lens":
        return "Core Logic (World Lens Context)"
    if module_family == "AI Integrity Mirror":
        return "Core Logic (AI Integrity Mirror)"
    if module_family == "Stress Test / Simulation":
        return "Core Logic (Stress Test / Simulation)"
    return f"Core Logic ({module_family})"


def _core_logic_text(module_family: str) -> str:
    base = (
        "The Standard View serves as a verbal translation of the uploaded receipt. "
        "Its primary function is to keep native ALETHEIA values first."
    )
    key_protocol = (
        "Key Protocol: the reader maps data into a secondary review band for clarity without generating a new verdict, "
        "rescoring, or altering the original receipt."
    )
    if module_family == "World Lens":
        return base + " It reads World Lens as country-year evidence context, not as certification of a country or government. " + key_protocol
    if module_family == "AI Integrity Mirror":
        return base + " It reads AI Integrity receipts as static artifact reviews, not live model, vendor, or deployment certification. " + key_protocol
    if module_family == "Stress Test / Simulation":
        return base + " It reads Stress Test receipts as scenario outputs without re-running the tree or changing score logic. " + key_protocol
    return base + " " + key_protocol


def parse_receipt_standard_view(receipt_text: str) -> dict[str, Any]:
    """Extract uploaded receipt fields without inferring, rescoring, or overriding values."""
    text = receipt_text or ""
    data = _json_after_marker(text)
    world_lens_fields: dict[str, Any] = {}
    ai_integrity_fields: dict[str, str] = {}
    ai_static_scan_context = _parse_ai_static_scan_context(text)

    if _is_world_lens_receipt(text):
        fields, world_lens_fields = _fields_from_world_lens_text(text)
    else:
        fields = _fields_from_json(data, text) if data else _fields_from_text(text)

    repair_questions: list[str] = []
    if isinstance(data, dict) and isinstance(data.get("repair_questions"), list):
        repair_questions = [str(item).strip() for item in data["repair_questions"] if str(item).strip()]
    if not repair_questions:
        repair_questions = _repair_questions_from_text(text)

    native_state = _native_state_from_text(fields.get("protocol_adjusted_state"))
    if fields.get("protocol_adjusted_state") == "WORLD_LENS_EVIDENCE_VIEW":
        native_state = "WORLD_LENS_EVIDENCE_VIEW"
    if native_state == MISSING_VALUE:
        native_state = _native_state_from_text(fields.get("risk_state"))
    if native_state == MISSING_VALUE and not _is_world_lens_receipt(text):
        native_state = _native_state_from_text(text)

    module_family = _module_family(fields.get("module_source", ""), text)
    receipt_kind = "Stress Test" if module_family == "Stress Test / Simulation" else module_family

    if module_family == "AI Integrity Mirror":
        ai_integrity_fields = {
            "review_mode": _first_match(text, [r"(?im)^\s*Review mode\s*:\s*(.+?)\s*$"]),
            "artifact_type": _first_match(text, [r"(?im)^\s*Artifact type\s*:\s*(.+?)\s*$"]),
            "positive_review_signals": _first_match(text, [r"(?im)^\s*Positive review signals\s*:\s*(.+?)\s*$"]),
        }

    if native_state == "QUESTION_PROMPT":
        metric_rows = _question_prompt_metric_rows()
    elif module_family == "World Lens":
        metric_rows = _world_lens_metric_rows(world_lens_fields)
    else:
        metric_rows = [
            {
                "Metric": label,
                "Value": fields.get(key, MISSING_VALUE),
                "Interpretation": _interpret_metric(key, fields.get(key, MISSING_VALUE), native_state),
            }
            for key, label in METRIC_ORDER
        ]

    plain_language_explanation = _core_logic_text(module_family)
    if module_family == "World Lens":
        plain_language_explanation += " It is not a Mirror Check scenario receipt and does not certify a country, government, institution, or system."
    elif module_family == "AI Integrity Mirror":
        plain_language_explanation += " The reading does not test a live model, vendor, deployment, training data, hidden system prompt, or future behavior."
    elif module_family == "Stress Test / Simulation":
        plain_language_explanation += " It preserves the uploaded scenario output without re-running the scenario."

    return {
        "receipt_kind": receipt_kind,
        "native_state": native_state,
        "system_status": native_state,
        "status_line": STATUS_LINES.get(native_state, "The uploaded receipt is shown without inferring missing values."),
        "standard_band": STANDARD_BANDS.get(native_state, MISSING_VALUE),
        "module_family": module_family,
        "fields": fields,
        "world_lens_fields": world_lens_fields,
        "ai_integrity_fields": ai_integrity_fields,
        "ai_static_scan_context": ai_static_scan_context,
        "metric_rows": metric_rows,
        "repair_questions": repair_questions,
        "core_logic_title": _core_logic_title(module_family),
        "core_logic_text": _core_logic_text(module_family),
        "plain_language_explanation": plain_language_explanation,
        "non_certification_note": "This is not certification, approval, rejection, enforcement, or final truth. Human review remains required.",
        "summary": _summary_for_state(native_state, fields),
        "boundary": RECEIPT_READER_BOUNDARY,
        "parsing_limits": f"Only obvious uploaded {module_family} receipt fields are shown. Missing or unclear fields are not inferred.",
    }


def _read_uploaded_text(uploaded_file: Any) -> tuple[str, str]:
    name = getattr(uploaded_file, "name", "uploaded receipt") or "uploaded receipt"
    raw = uploaded_file.getvalue()
    if isinstance(raw, str):
        return raw, name
    return bytes(raw).decode("utf-8", errors="replace"), name


def _is_batch_index_file(filename: str) -> bool:
    """Batch index files are used only as indexes; they are not inspected as receipts."""
    lower = filename.lower().rsplit("/", 1)[-1]
    return lower.startswith("batch_index") or lower in {"index.txt", "index.json"}


def _is_batch_index_name(filename: str) -> bool:
    """Compatibility alias for tests and older patch notes."""
    return _is_batch_index_file(filename)


def _is_receipt_summary_or_index_file(filename: str) -> bool:
    """Return True for ZIP summary/index artifacts that must not be inspected as receipts."""
    lower = filename.lower().rsplit("/", 1)[-1]
    stem = re.sub(r"\.(txt|md|json)$", "", lower)
    if _is_batch_index_file(lower):
        return True
    return (
        stem.endswith("_summary")
        or stem.endswith("-summary")
        or stem.endswith("_index")
        or stem.endswith("-index")
        or lower in {"summary.txt", "summary.md", "summary.json"}
    )


def _is_actual_receipt_candidate(filename: str, text: str) -> bool:
    """Classify inspectable uploaded receipts without treating summary files as receipts."""
    lower = filename.lower()
    if _is_receipt_summary_or_index_file(lower):
        return False
    content = (text or "").lower()
    if _is_world_lens_receipt(text):
        return True
    if "aletheia local witness receipt" in content or "ai integrity receipt" in content:
        return True
    basename = lower.rsplit("/", 1)[-1]
    if basename.startswith("receipt_") or basename.startswith("receipt-"):
        return True
    if basename.startswith("aletheia_world_lens_receipt_") and not _is_receipt_summary_or_index_file(basename):
        return True
    return False


def _receipt_sort_key(item: tuple[str, str]) -> tuple[int, str]:
    filename = item[0].lower()
    basename = filename.rsplit("/", 1)[-1]
    if basename.endswith(".json"):
        preferred = 0
    elif basename.endswith(".md"):
        preferred = 1
    else:
        preferred = 2
    match = re.search(r"receipt[_-]?(\d+)", basename)
    number = int(match.group(1)) if match else 999999
    return (number, f"{preferred}:{filename}")


def _dedupe_receipt_pairs(receipts: list[tuple[str, str]]) -> list[tuple[str, str]]:
    by_stem: dict[str, tuple[str, str]] = {}
    for filename, text in sorted(receipts, key=_receipt_sort_key):
        lower = filename.lower()
        if not _is_actual_receipt_candidate(lower, text):
            continue
        stem = re.sub(r"\.(txt|md|json)$", "", lower.rsplit("/", 1)[-1])
        current = by_stem.get(stem)
        if current is None:
            by_stem[stem] = (filename, text)
            continue
        current_lower = current[0].lower()
        # For World Lens evidence bundles the Markdown receipt is the readable
        # source of truth. JSON companions are often summaries, not receipts.
        if _is_world_lens_receipt(text) and lower.endswith(".md"):
            by_stem[stem] = (filename, text)
        elif lower.endswith(".json") and not _is_world_lens_receipt(text):
            by_stem[stem] = (filename, text)
        elif lower.endswith(".md") and not current_lower.endswith((".json", ".md")):
            by_stem[stem] = (filename, text)
    return sorted(by_stem.values(), key=_receipt_sort_key)


def _is_world_lens_bundle_filename(filename: str) -> bool:
    lower = filename.lower().rsplit("/", 1)[-1]
    return lower.startswith("aletheia_world_lens_receipt_") or lower.startswith("world_lens")


def _csv_preview(text: str, *, max_rows: int = 10) -> tuple[list[str], list[dict[str, str]], int]:
    rows = list(csv.DictReader(io.StringIO(text)))
    fieldnames = list(rows[0].keys()) if rows else []
    preview = [{key: str(value or "") for key, value in row.items()} for row in rows[:max_rows]]
    return fieldnames, preview, len(rows)


def _friendly_evidence_table_name(filename: str) -> str:
    basename = filename.rsplit("/", 1)[-1]
    stem = re.sub(r"\.csv$", "", basename, flags=re.IGNORECASE)
    stem = re.sub(r"^aletheia_world_lens_receipt_\d{4}_", "", stem)
    return stem.replace("_", " ").strip().title() or basename


def _world_lens_summary_rows(summary: dict[str, Any]) -> list[dict[str, str]]:
    """Render summary JSON metadata as a narrow readable key/value table."""
    labels = [
        ("filename", "Metadata file"),
        ("selected_year", "Selected year"),
        ("grid_source_state", "Grid source state"),
        ("active_selected_year_seats", "Active selected-year seats"),
        ("allocated_country_rows", "Allocated country rows"),
        ("weighted_integrity", "Weighted integrity"),
        ("weighted_friction", "Weighted friction"),
        ("weighted_collapse_probability", "Weighted collapse pressure"),
        ("average_empirical_coverage", "Average empirical coverage"),
        ("trust_raw_coverage", "Raw trust survey coverage"),
        ("trust_prior_coverage", "Trust prior coverage"),
        ("interpretation_warning", "Interpretation warning"),
    ]
    rows: list[dict[str, str]] = []
    for key, label in labels:
        value = summary.get(key, MISSING_VALUE)
        if value == MISSING_VALUE or value is None:
            continue
        rows.append({"Field": label, "Value": str(value)})
    return rows


def _world_lens_table_description(table_name: str) -> str:
    key = (table_name or "").lower()
    if "coverage gap" in key:
        return "Rows where evidence coverage is incomplete or should be inspected."
    if "coverage" == key or key.startswith("coverage"):
        return "Coverage basis for selected-year evidence sources."
    if "high impact" in key:
        return "Countries with high allocation plus low integrity or high collapse pressure signals."
    if "highest collapse" in key:
        return "Highest collapse-pressure rows from the uploaded evidence table."
    if "highest integrity" in key:
        return "Highest integrity rows from the uploaded evidence table."
    if "largest allocation" in key:
        return "Largest 9k seat allocations in the selected-year evidence view."
    if "lowest integrity" in key:
        return "Lowest integrity rows from the uploaded evidence table."
    if "sensitivity" in key:
        return "Rows that may need extra interpretation because of coverage, allocation, or risk sensitivity."
    if "taxonomy" in key:
        return "Seat and country distribution by internal taxonomy label."
    if "all rows" in key:
        return "Full selected-year country evidence table; shown with curated columns by default."
    return "Supporting World Lens evidence table from the uploaded bundle."


def _first_existing_column(columns: list[str], *candidates: str) -> str | None:
    for candidate in candidates:
        if candidate in columns:
            return candidate
    return None


def _world_lens_curated_columns(table_name: str, columns: list[str]) -> list[str]:
    """Select readable World Lens columns so previews avoid 100-column raw dumps."""
    key = (table_name or "").lower()

    def pick(*groups: tuple[str, ...]) -> list[str]:
        selected: list[str] = []
        for group in groups:
            found = _first_existing_column(columns, *group)
            if found and found not in selected:
                selected.append(found)
        return selected

    country_fields = (("friendly_country_name", "country"), ("iso3",), ("year", "grid_selected_year"))
    if "coverage gap" in key:
        wanted = pick(
            *country_fields,
            ("seats", "seats_9k", "_seats"),
            ("missing_raw_trust", "_missing_raw_trust"),
            ("missing_trust_prior", "_missing_trust_prior"),
            ("missing_wgi", "_missing_wgi"),
            ("missing_vdem", "_missing_vdem"),
            ("coverage_gap_count", "_coverage_gap_count"),
        )
    elif "taxonomy" in key:
        wanted = pick(
            ("internal_taxonomy_label", "raw_verdict"),
            ("countries",),
            ("seats", "seat_share"),
            ("avg_integrity", "average_integrity"),
            ("avg_collapse_probability", "average_collapse_probability"),
            ("avg_empirical_coverage", "average_empirical_coverage"),
            ("humility_note",),
        )
    elif "coverage" == key or key.startswith("coverage"):
        wanted = pick(("source",), ("rows_present",), ("rows_missing",), ("coverage",))
    else:
        wanted = pick(
            *country_fields,
            ("seats_9k", "_seats", "seats"),
            ("internal_taxonomy_label", "raw_aletheia_verdict", "raw_verdict"),
            ("aletheia_empirical_integrity", "_integrity", "integrity"),
            ("aletheia_empirical_friction", "_friction", "friction"),
            ("aletheia_empirical_collapse_probability", "_collapse", "collapse_probability"),
            ("empirical_completeness", "_coverage", "empirical_coverage"),
            ("raw_trust", "_trust_raw", "wvs_generalized_trust"),
            ("empirical_trust_prior", "_trust_prior", "trust_prior"),
            ("coverage_gap_count", "_coverage_gap_count"),
            ("humility_note",),
        )
    if wanted:
        return wanted[:12]
    return columns[: min(8, len(columns))]


def _curated_preview_rows(table: dict[str, Any], *, max_rows: int = 10) -> list[dict[str, str]]:
    columns = table.get("columns") or []
    selected_columns = _world_lens_curated_columns(str(table.get("table_name", "")), list(columns))
    rows: list[dict[str, str]] = []
    for row in (table.get("preview_rows") or [])[:max_rows]:
        rows.append({
            _world_lens_display_column_label(column): str(row.get(column, ""))
            for column in selected_columns
        })
    return rows


def _preview_field_label(table: dict[str, Any]) -> str:
    fields = _world_lens_curated_columns(str(table.get("table_name", "")), list(table.get("columns") or []))
    if not fields:
        return "Curated preview fields not found"
    display_fields = [_world_lens_display_column_label(field) for field in fields]
    if len(display_fields) <= 5:
        return ", ".join(display_fields)
    return ", ".join(display_fields[:5]) + f" + {len(display_fields) - 5} more"


def _summarize_world_lens_summary_json(filename: str, text: str) -> dict[str, Any]:
    try:
        data = json.loads(text)
    except Exception:
        return {"filename": filename, "parse_status": "summary JSON could not be parsed"}
    if not isinstance(data, dict):
        return {"filename": filename, "parse_status": "summary JSON was not an object"}
    keys = [
        "selected_year",
        "grid_source_state",
        "active_selected_year_seats",
        "allocated_country_rows",
        "weighted_integrity",
        "weighted_friction",
        "weighted_collapse_probability",
        "average_empirical_coverage",
        "trust_raw_coverage",
        "trust_prior_coverage",
        "interpretation_warning",
    ]
    return {"filename": filename, **{key: data.get(key, MISSING_VALUE) for key in keys}}


def _world_lens_bundle_details(all_files: list[tuple[str, str]]) -> dict[str, Any]:
    summaries: list[dict[str, Any]] = []
    evidence_tables: list[dict[str, Any]] = []
    support_files: list[dict[str, str]] = []
    for filename, text in sorted(all_files, key=lambda item: item[0].lower()):
        lower = filename.lower()
        basename = lower.rsplit("/", 1)[-1]
        if lower.endswith(".json") and _is_receipt_summary_or_index_file(basename):
            summaries.append(_summarize_world_lens_summary_json(filename, text))
        elif lower.endswith(".csv"):
            columns, preview, row_count = _csv_preview(text)
            evidence_tables.append({
                "filename": filename,
                "table_name": _friendly_evidence_table_name(filename),
                "row_count": row_count,
                "columns": columns,
                "preview_rows": preview,
            })
        elif not _is_actual_receipt_candidate(filename, text):
            support_files.append({"filename": filename, "role": "supporting file"})
    return {
        "summary_files": summaries,
        "evidence_tables": evidence_tables,
        "support_files": support_files,
    }


def _is_world_lens_evidence_bundle(all_files: list[tuple[str, str]], receipts: list[tuple[str, str]]) -> bool:
    if any(_is_world_lens_receipt(text) for _, text in receipts):
        return True
    if any(_is_world_lens_bundle_filename(filename) for filename, _ in all_files):
        return True
    return False


def _read_zip_receipts(uploaded_file: Any) -> tuple[list[tuple[str, str]], str, list[tuple[str, str]], dict[str, Any]]:
    name = getattr(uploaded_file, "name", "uploaded receipts.zip") or "uploaded receipts.zip"
    raw = uploaded_file.getvalue()
    all_files: list[tuple[str, str]] = []
    receipt_candidates: list[tuple[str, str]] = []
    with zipfile.ZipFile(io.BytesIO(bytes(raw))) as archive:
        for info in archive.infolist():
            lower = info.filename.lower()
            if info.is_dir() or not lower.endswith((".txt", ".md", ".json", ".csv")):
                continue
            text = archive.read(info).decode("utf-8", errors="replace")
            all_files.append((info.filename, text))
            if lower.endswith((".txt", ".md", ".json")) and _is_actual_receipt_candidate(info.filename, text):
                receipt_candidates.append((info.filename, text))
    receipts = _dedupe_receipt_pairs(receipt_candidates)
    bundle_details = _world_lens_bundle_details(all_files) if _is_world_lens_evidence_bundle(all_files, receipts) else {}
    return receipts, name, all_files, bundle_details


def parse_uploaded_receipt_file(uploaded_file: Any) -> dict[str, Any]:
    """Parse one uploaded receipt file or a ZIP of receipt text files."""
    name = getattr(uploaded_file, "name", "") or ""
    if name.lower().endswith(".zip"):
        receipts, zip_name, all_files, bundle_details = _read_zip_receipts(uploaded_file)
        views = [(filename, _attach_current_semantic_reread(parse_receipt_standard_view(text), text, filename=filename)) for filename, text in receipts]
        distribution = Counter(view.get("native_state", MISSING_VALUE) for _, view in views)
        risk_distribution = Counter(
            (view.get("fields") or {}).get("risk_state", MISSING_VALUE) for _, view in views
        )
        module_distribution = Counter(
            (view.get("fields") or {}).get("module_source", MISSING_VALUE) for _, view in views
        )
        is_world_lens_bundle = _is_world_lens_evidence_bundle(all_files, receipts)
        return {
            "kind": "batch_zip",
            "bundle_type": "world_lens_evidence_bundle" if is_world_lens_bundle else "receipt_batch",
            "name": zip_name,
            "receipt_count": len(views),
            "distribution": dict(distribution),
            "risk_distribution": dict(risk_distribution),
            "module_distribution": dict(module_distribution),
            "views": views,
            "bundle_details": bundle_details,
            "zip_file_count": len(all_files),
        }
    text, filename = _read_uploaded_text(uploaded_file)
    return {"kind": "single", "name": filename, "text": text, "view": _attach_current_semantic_reread(parse_receipt_standard_view(text), text, filename=filename)}


def _metric_section_title(view: dict[str, Any]) -> str:
    if _is_question_prompt_state(view.get("native_state", "")):
        return "Review-Tool Metrics"
    family = view.get("module_family")
    if family == "World Lens":
        return "World Lens Evidence Metrics"
    if family == "Stress Test / Simulation":
        return "Scenario Review Metrics"
    if family == "AI Integrity Mirror":
        return "Artifact Review Metrics"
    return "Performance & Risk Metrics"


def _metric_section_caption(view: dict[str, Any]) -> str:
    if _is_question_prompt_state(view.get("native_state", "")):
        return "QUESTION_PROMPT receipts intentionally suppress scored metrics."
    family = view.get("module_family")
    if family == "World Lens":
        return "Selected-year evidence values from the uploaded World Lens receipt; no new decision is generated."
    if family == "Stress Test / Simulation":
        return "Uploaded scenario receipt values, shown without rerunning the scenario."
    if family == "AI Integrity Mirror":
        return "Uploaded static artifact review values; this does not test a live model or vendor."
    return "Quantitative values copied from the uploaded receipt."


def _state_definition(native_state: str) -> str:
    return STATE_DEFINITIONS.get(native_state, "an uploaded receipt state that should be read only from native receipt values.")


def _verbal_brief(view: dict[str, Any]) -> str:
    native_state = str(view.get("native_state", MISSING_VALUE))
    prefix = STATE_BRIEF_PREFIX.get(native_state, "The mirror reflects the uploaded receipt")
    definition = _state_definition(native_state)
    fields = view.get("fields") or {}
    family = view.get("module_family")
    if family == "World Lens":
        return f"{prefix} — {definition} The evidence bundle is preserved for readable human inspection; no new World Lens decision is created."
    if family == "AI Integrity Mirror":
        artifact = (view.get("ai_integrity_fields") or {}).get("artifact_type", MISSING_VALUE)
        return f"{prefix} — {definition} This is a static artifact review for {artifact}; it does not test a live model or vendor."
    if family == "Stress Test / Simulation":
        return f"{prefix} — {definition} The scenario receipt is translated here without rerunning the stress test or changing tree logic."
    if native_state == "QUESTION_PROMPT":
        return f"{prefix} — {definition} Metrics are intentionally not applicable."
    risk = fields.get("risk_state", MISSING_VALUE)
    return f"{prefix} — {definition} The uploaded receipt records review pressure as {risk}; human review remains required."


def _native_values_rows(view: dict[str, Any]) -> list[dict[str, str]]:
    fields = view.get("fields") or {}
    rows = [
        {"Field": "Native State", "Value": str(view.get("native_state", MISSING_VALUE))},
        {"Field": "Review Pressure", "Value": str(view.get("standard_band", MISSING_VALUE))},
        {"Field": "Protocol Label", "Value": fields.get("protocol_label", MISSING_VALUE)},
        {"Field": "Module Source", "Value": _display_module_source(view)},
    ]
    for row in view.get("metric_rows") or []:
        rows.append({"Field": str(row.get("Metric", MISSING_VALUE)), "Value": str(row.get("Value", MISSING_VALUE))})
    return rows


def _safe_float(value: Any) -> float | None:
    """Return a normalized numeric receipt value when one is present."""
    if value in {None, "", MISSING_VALUE, NOT_APPLICABLE}:
        return None
    text = str(value).strip().replace("%", "")
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if not match:
        return None
    try:
        number = float(match.group(0))
    except ValueError:
        return None
    if "%" in str(value):
        number = number / 100.0
    if number > 1.0:
        number = number / 100.0 if number <= 100.0 else 1.0
    return max(0.0, min(1.0, number))


def _metric_level(value: Any, *, invert: bool = False) -> str:
    number = _safe_float(value)
    if number is None:
        return "Not found"
    score = 1.0 - number if invert else number
    if score >= 0.67:
        return "High"
    if score >= 0.34:
        return "Medium"
    return "Low"


def _metric_bar(value: Any) -> str:
    number = _safe_float(value)
    if number is None:
        return "░░░░░░░░░░"
    filled = int(round(number * 10))
    filled = max(0, min(10, filled))
    return "█" * filled + "░" * (10 - filled)


def _state_palette(native_state: str) -> dict[str, str]:
    state = str(native_state or "").upper()
    if state == "SANCTUARY":
        return {"bg": "#edf7ed", "border": "#2e7d32", "fg": "#1b5e20", "label": "Low review pressure"}
    if state == "THRESHOLD":
        return {"bg": "#fff4e5", "border": "#c77700", "fg": "#7a4a00", "label": "Review needed"}
    if state == "ASYLUM":
        return {"bg": "#f8e9e7", "border": "#7f1d1d", "fg": "#5a1414", "label": "High review pressure"}
    if state == "QUESTION_PROMPT":
        return {"bg": "#eef3ff", "border": "#355c9a", "fg": "#1f3b67", "label": "Review-tool mode"}
    if state == "WORLD_LENS_EVIDENCE_VIEW":
        return {"bg": "#eef7f8", "border": "#237477", "fg": "#164f51", "label": "Evidence view"}
    return {"bg": "#f2f2f2", "border": "#777777", "fg": "#333333", "label": "Receipt state"}


def _render_status_banner(container: Any, view: dict[str, Any]) -> None:
    """Render the one-second receipt status banner."""
    fields = view.get("fields") or {}
    native_state = str(view.get("native_state", MISSING_VALUE))
    palette = _state_palette(native_state)
    protocol_label = fields.get("protocol_label", MISSING_VALUE)
    module = _display_module_source(view)
    container.markdown(
        f"""
<div style="border:1px solid {palette['border']}; border-left:9px solid {palette['border']}; background:{palette['bg']}; color:{palette['fg']}; border-radius:14px; padding:1rem 1.15rem; margin:0.55rem 0 1rem 0;">
  <div style="font-size:0.78rem; letter-spacing:0.08em; text-transform:uppercase; font-weight:700; opacity:0.9;">Uploaded receipt status</div>
  <div style="font-size:1.45rem; line-height:1.2; font-weight:800; margin-top:0.15rem;">STATUS: {native_state} <span style="font-size:0.95rem; font-weight:700;">({palette['label']})</span></div>
  <div style="margin-top:0.45rem; font-size:0.94rem;"><strong>Protocol label:</strong> {protocol_label}</div>
  <div style="font-size:0.94rem;"><strong>Module source:</strong> {module}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def _render_top_metric_strip(container: Any, view: dict[str, Any]) -> None:
    """Render the three main receipt metrics as a compact visual strip."""
    fields = view.get("fields") or {}
    metric_specs = [
        ("Integrity", fields.get("integrity", MISSING_VALUE), False),
        ("Friction", fields.get("friction", MISSING_VALUE), False),
        ("Collapse Pressure", fields.get("collapse_probability", MISSING_VALUE), False),
    ]
    if _is_question_prompt_state(view.get("native_state", "")):
        container.info("QUESTION_PROMPT receipt: scored metrics are not applicable.")
        return
    if hasattr(container, "columns"):
        columns = container.columns(3)
        for col, (label, value, invert) in zip(columns, metric_specs):
            col.markdown(f"**{label}**")
            col.markdown(f"`{value}`")
            col.caption(f"{_metric_level(value, invert=invert)} · {_metric_bar(value)}")
    else:
        container.table([
            {"Metric": label, "Value": value, "Level": _metric_level(value, invert=invert), "Bar": _metric_bar(value)}
            for label, value, invert in metric_specs
        ])


def _render_visual_metric_rows(container: Any, view: dict[str, Any]) -> None:
    """Render all copied metrics as scan-friendly bars instead of a dense numeric table."""
    if _is_question_prompt_state(view.get("native_state", "")):
        container.info(
            "Not applicable — QUESTION_PROMPT receipts are review-tool prompts and do not carry "
            "scored integrity, collapse, trust, alignment, friction, or ego metrics."
        )
        return
    rows = []
    for row in view.get("metric_rows") or []:
        metric = str(row.get("Metric", MISSING_VALUE))
        value = str(row.get("Value", MISSING_VALUE))
        interpretation = str(row.get("Interpretation", "Shown as recorded in the uploaded receipt."))
        rows.append({
            "Metric": metric,
            "Level": _metric_level(value),
            "Value": value,
            "Visual": _metric_bar(value),
            "Reading note": interpretation,
        })
    if rows:
        container.table(rows)
    else:
        container.write("No metric rows were parsed from the uploaded receipt.")


def _render_repair_questions_block(container: Any, view: dict[str, Any]) -> None:
    questions = _plain_next_questions(view)
    if not questions:
        return
    text = "\n".join(f"- {question}" for question in questions)
    container.info("Human-review hand-off questions:\n\n" + text)


def _render_failure_mode_review_signals_compact(container: Any) -> None:
    """Render failure-mode signals as compact warning items."""
    container.markdown("### Detected pressure-pattern checklist")
    container.caption(FAILURE_MODE_REVIEW_BOUNDARY)
    for label, explanation in FAILURE_MODE_REVIEW_SIGNALS:
        container.warning(f"**{label}:** {explanation}")


def _render_metric_observation_cards(container: Any, view: dict[str, Any]) -> None:
    for row in view.get("metric_rows") or []:
        metric = str(row.get("Metric", MISSING_VALUE))
        value = str(row.get("Value", MISSING_VALUE))
        interpretation = str(row.get("Interpretation", "Shown as recorded in the uploaded receipt."))
        container.markdown(f"**{metric}: {value}**")
        container.write(f"Observation: {interpretation}")



def _render_failure_mode_review_signals(container: Any) -> None:
    """Render failure-mode verbalization for every Receipt Reader view."""
    container.markdown("### Failure-mode review signals")
    container.write(FAILURE_MODE_REVIEW_BOUNDARY)
    for label, explanation in FAILURE_MODE_REVIEW_SIGNALS:
        container.markdown(f"- **{label}:** {explanation}")

def _render_native_values_expander(container: Any, view: dict[str, Any]) -> None:
    rows = _native_values_rows(view)
    if hasattr(container, "expander"):
        with container.expander("Native receipt values", expanded=False) as expander:
            expander.caption("Exact values copied from the uploaded receipt. Missing values are not inferred.")
            expander.table(rows)
    else:
        container.table(rows)


def _display_module_source(view: dict[str, Any]) -> str:
    fields = view.get("fields") or {}
    if view.get("module_family") == "Stress Test / Simulation":
        return "Stress Test / Simulation"
    return fields.get("module_source", MISSING_VALUE)


def _render_ai_static_scan_context(container: Any, view: dict[str, Any]) -> None:
    """Render subordinate AI static-scan context parsed from a receipt."""
    context = view.get("ai_static_scan_context") or {}
    if not isinstance(context, dict) or not context.get("present"):
        return
    if hasattr(container, "expander"):
        with container.expander("AI static scan context — subordinate to primary receipt", expanded=False) as expander:
            expander.caption(
                "Parsed from the uploaded receipt. This context is subordinate to the primary "
                "Mirror Check / Stress Test receipt and does not create a competing decision."
            )
            protocol_context_state = context.get('protocol_context_state') or view.get('native_state') or context.get('static_scan_state')
            protocol_context_risk = context.get('protocol_context_risk') or view.get('fields', {}).get('risk') or context.get('static_scan_risk')
            alignment_note = context.get('alignment_note')
            if not alignment_note and context.get('static_scan_state') != protocol_context_state:
                alignment_note = (
                    "Primary protocol reading is stronger than the raw AI static scan; "
                    "the primary receipt values control this reading."
                )
            expander.markdown(
                f"**Role:** {context.get('role', MISSING_VALUE)}  \n"
                f"**Primary protocol path:** {context.get('primary_protocol_path', MISSING_VALUE)}  \n"
                f"**Protocol context state:** {protocol_context_state or MISSING_VALUE}  \n"
                f"**Protocol context risk:** {protocol_context_risk or MISSING_VALUE}  \n"
                f"**Protocol alignment:** {context.get('protocol_alignment', 'subordinate_to_primary_receipt')}  \n"
                f"**Raw AI static scan only:** {context.get('static_scan_state', MISSING_VALUE)} / {context.get('static_scan_risk', MISSING_VALUE)}  \n"
                f"**Risk pressure:** {context.get('risk_pressure', MISSING_VALUE)}  \n"
                f"**Finding count:** {context.get('finding_count', MISSING_VALUE)}"
            )
            if alignment_note:
                expander.info(str(alignment_note))
            notice = context.get("notice")
            if notice and notice != MISSING_VALUE:
                expander.caption(str(notice))
            findings = context.get("findings") or []
            if findings:
                expander.markdown("**AI-specific findings**")
                for finding in findings:
                    expander.markdown(f"- {finding}")
            questions = context.get("repair_questions") or []
            if questions:
                expander.markdown("**AI static-scan repair questions**")
                for question in questions:
                    expander.markdown(f"- {question}")
    else:
        container.write(context)


def _view_status_heading(view: dict[str, Any]) -> str:
    family = view.get("module_family")
    state = view.get("system_status", MISSING_VALUE)
    if family == "World Lens":
        return f"Evidence View: {state}"
    if family == "Stress Test / Simulation":
        return f"Scenario Receipt State: {state}"
    return f"Native Receipt State: {state}"


def _plain_state_name(native_state: str) -> str:
    """Return a plain English state label without changing the receipt value."""
    state = str(native_state or MISSING_VALUE).strip().upper()
    if state == "SANCTUARY":
        return "Sanctuary (low review pressure)"
    if state == "THRESHOLD":
        return "Threshold (review needed)"
    if state == "ASYLUM":
        return "Asylum pressure (high review pressure)"
    if state == "QUESTION_PROMPT":
        return "Question prompt (review-tool mode)"
    if state == "WORLD_LENS_EVIDENCE_VIEW":
        return "World Lens evidence view"
    return str(native_state or MISSING_VALUE)


def _plain_metric_value(fields: dict[str, str], key: str) -> str:
    value = fields.get(key, MISSING_VALUE)
    return value if value not in {None, ""} else MISSING_VALUE


def _plain_power_distribution_rows(view: dict[str, Any]) -> list[dict[str, str]]:
    """Return a simple component matrix for the plain-language Receipt Reader summary.

    The rows do not rescore the receipt. They translate the native fields and
    receipt questions into the same human-readable review categories used by
    the app: power, correction, and access.
    """
    native_state = str(view.get("native_state", MISSING_VALUE))
    standard_band = str(view.get("standard_band", MISSING_VALUE))
    questions = view.get("repair_questions") or []
    question_note = "Repair questions are present; review the appeal, correction, and safeguard path."
    if not questions:
        question_note = "No repair questions were parsed from this uploaded receipt. That does not prove that no review is needed."
    return [
        {
            "Review area": "Power",
            "What the reader checks": "Whether control, evidence, or decision authority appears concentrated or reviewable.",
            "Receipt value used": f"Native state: {native_state}; review pressure: {standard_band}",
        },
        {
            "Review area": "Correction",
            "What the reader checks": "Whether people have a way to question, appeal, correct, pause, or review the process.",
            "Receipt value used": question_note,
        },
        {
            "Review area": "Access",
            "What the reader checks": "Whether access to rights, services, basic needs, or participation appears conditional, coercive, or unclear.",
            "Receipt value used": "Use the module source, protocol label, and repair questions as the receipt-level evidence. Missing fields are not inferred.",
        },
    ]


def _plain_next_questions(view: dict[str, Any]) -> list[str]:
    questions = [str(q).strip() for q in (view.get("repair_questions") or []) if str(q).strip()]
    if questions:
        return questions[:5]
    return [
        "Where can a person object, appeal, pause, or request human review if something goes wrong?",
        "What prevents this system from becoming less transparent or more centralized over time?",
        "Which evidence would another reviewer need before relying on this receipt?",
    ]


def _plain_receipt_summary_text(view: dict[str, Any]) -> str:
    fields = view.get("fields") or {}
    module = _display_module_source(view)
    native_state = str(view.get("native_state", MISSING_VALUE))
    standard_band = str(view.get("standard_band", MISSING_VALUE))
    protocol_label = fields.get("protocol_label", MISSING_VALUE)
    integrity = _plain_metric_value(fields, "integrity")
    collapse = _plain_metric_value(fields, "collapse_probability")
    trust = _plain_metric_value(fields, "trust")
    alignment = _plain_metric_value(fields, "alignment")

    return (
        "This is a record of an ALETHEIA review, a kind of digital mirror. "
        "The reader explains what the uploaded receipt says; it does not rerun the test, "
        "change the values, approve the result, or decide whether something is safe, good, or true. "
        "Real people must still review the receipt before relying on it.\n\n"
        f"The receipt records **{_plain_state_name(native_state)}** with **{standard_band}**. "
        f"The protocol label copied from the receipt is **{protocol_label}**, and the module source is **{module}**. "
        f"Key copied values include integrity **{integrity}**, collapse pressure **{collapse}**, trust **{trust}**, and alignment **{alignment}**. "
        "These values are shown as recorded; the Receipt Reader does not adjust them."
    )


def _render_plain_language_receipt_summary(container: Any, view: dict[str, Any]) -> None:
    """Render the simplified plain-English Standard View."""
    fields = view.get("fields") or {}
    native_state = str(view.get("native_state", MISSING_VALUE))
    standard_band = str(view.get("standard_band", MISSING_VALUE))

    container.markdown("### Plain-English summary")
    container.write(_plain_receipt_summary_text(view))
    container.caption(
        "Copied receipt fields: "
        f"state {_plain_state_name(native_state)}; review pressure {standard_band}; "
        f"protocol label {fields.get('protocol_label', MISSING_VALUE)}."
    )

    with container.expander("How the reader translates power, correction, and access", expanded=False) as panel:
        panel.write(
            "This is a plain-language translation layer. It does not add a new score, label, decision, or certification."
        )
        panel.table(_plain_power_distribution_rows(view))


def _semantic_finding_label(scan: Any) -> str:
    """Return a reader-safe semantic finding label for the current scanner pass."""
    if scan is None:
        return "Unavailable"
    claim_count = int(getattr(scan, "claim_count", 0) or 0)
    mechanism_count = int(getattr(scan, "mechanism_count", 0) or 0)
    modal_count = int(getattr(scan, "modal_pressure_count", 0) or 0)
    sovereignty_count = int(getattr(scan, "sovereignty_count", 0) or 0)
    proximity_hits = list(getattr(scan, "proximity_hits", ()) or [])
    fail_closed = bool(getattr(scan, "fail_closed", False))
    pressure = float(getattr(scan, "integrity_adjustment", 0.0) or 0.0)
    if not any([claim_count, mechanism_count, modal_count, sovereignty_count, proximity_hits, fail_closed, abs(pressure) > 1e-9]):
        return "NO SIGNAL"
    return str(getattr(scan, "state", "REVIEW"))


def _build_current_semantic_reread(receipt_text: str) -> dict[str, Any]:
    """Run the current semantic scanner for a receipt without changing native receipt values."""
    if scan_semantic_pressure is None:
        return {"available": False, "finding": "Unavailable", "risk": "Semantic scanner unavailable"}
    clean_text = str(receipt_text or "").strip()
    if not clean_text:
        return {"available": False, "finding": "NO TEXT", "risk": "No uploaded receipt text found"}
    scan = scan_semantic_pressure(clean_text, governance_context=True)
    return {
        "available": True,
        "scan": scan,
        "finding": _semantic_finding_label(scan),
        "risk": str(getattr(scan, "risk", "Review signal")),
        "claims": int(getattr(scan, "claim_count", 0) or 0),
        "mechanisms": int(getattr(scan, "mechanism_count", 0) or 0),
        "pressure": float(getattr(scan, "integrity_adjustment", 0.0) or 0.0),
        "notes": list(getattr(scan, "notes", ()) or []),
    }


def _attach_current_semantic_reread(view: dict[str, Any], receipt_text: str, *, filename: str = "uploaded receipt") -> dict[str, Any]:
    """Attach current semantic reader context while preserving native receipt parsing."""
    view["_receipt_reader_source_text"] = str(receipt_text or "")
    view["_receipt_reader_source_name"] = str(filename or "uploaded receipt")
    view["_current_semantic_reread"] = _build_current_semantic_reread(str(receipt_text or ""))
    return view



def _current_semantic_has_opaque_capture(view: dict[str, Any]) -> bool:
    """Return True when the current semantic re-read detected hidden-power/capture structure."""
    summary = view.get("_current_semantic_reread") or {}
    scan = summary.get("scan")
    hits = list(getattr(scan, "proximity_hits", ()) or []) if scan is not None else []
    notes = "\n".join(str(note) for note in (summary.get("notes") or []))
    risk = str(summary.get("risk", ""))
    haystack = (notes + "\n" + risk).lower()
    if any(str(getattr(hit, "category", "")).lower() == "opaque_capture_claim" for hit in hits):
        return True
    return "opaque capture" in haystack or "hidden concentrated power" in haystack or "hidden broad-scale power" in haystack


def _current_semantic_receipt_note(summary: dict[str, Any]) -> str:
    """Return receipt-safe wording for the current semantic re-read."""
    if not summary:
        return "No current semantic reading is available."
    scan = summary.get("scan")
    hits = list(getattr(scan, "proximity_hits", ()) or []) if scan is not None else []
    notes = "\n".join(str(note) for note in (summary.get("notes") or []))
    risk = str(summary.get("risk", "Review signal"))
    haystack = (notes + "\n" + risk).lower()
    has_opaque_capture = any(str(getattr(hit, "category", "")).lower() == "opaque_capture_claim" for hit in hits) or "opaque capture" in haystack or "hidden concentrated power" in haystack or "hidden broad-scale power" in haystack
    if has_opaque_capture:
        return (
            "Opaque capture-power claim detected: the text links an actor group to hidden broad-scale power or control "
            "without visible evidence basis, correction path, appeal route, or accountable mechanism. This is structural opacity/capture-pressure review, not a coercive-language finding."
        )
    return str(risk or "Review signal")


def _extract_repair_optimism_value(text: str) -> float | None:
    """Parse repair-route optimism / recovery capacity values when an uploaded receipt records them."""
    patterns = [
        r"(?im)repair[- ]route optimism\s*[:=]\s*([0-9]*\.?[0-9]+)",
        r"(?im)repair optimism\s*[:=]\s*([0-9]*\.?[0-9]+)",
        r"(?im)repair capacity\s*[:=]\s*([0-9]*\.?[0-9]+)",
        r"(?im)recovery index\s*[:=]\s*([0-9]*\.?[0-9]+)",
        r"(?im)repair index\s*[:=]\s*([0-9]*\.?[0-9]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text or "")
        if match:
            try:
                return float(match.group(1))
            except Exception:
                return None
    return None


def _capture_pressure_component_count(text: str) -> int:
    """Count common receipt component lines that are marked with capture pressure."""
    haystack = str(text or "")
    components = ["power balance", "power", "correction", "access"]
    count = 0
    for component in components:
        pattern_a = rf"(?is){re.escape(component)}[^\n]{{0,160}}capture pressure"
        pattern_b = rf"(?is)capture pressure[^\n]{{0,160}}{re.escape(component)}"
        if re.search(pattern_a, haystack) or re.search(pattern_b, haystack):
            count += 1
    return count


def _receipt_repair_blocker_note(view: dict[str, Any]) -> str:
    """Explain why repair capacity remains low when the uploaded receipt exposes blocked repair paths."""
    text = str(view.get("_receipt_reader_source_text", "") or "")
    native_state = str(view.get("native_state", "")).upper()
    repair_value = _extract_repair_optimism_value(text)
    component_count = _capture_pressure_component_count(text)
    semantic_opaque = _current_semantic_has_opaque_capture(view)
    low_repair = repair_value is not None and repair_value <= 0.35
    if not (low_repair or (native_state == "ASYLUM" and component_count >= 2) or (native_state == "ASYLUM" and semantic_opaque)):
        return ""
    value_text = f" Repair index recorded: {repair_value:.2f}." if repair_value is not None else ""
    if component_count >= 2:
        return (
            f"Repair blocker: recovery remains limited because {component_count} core review areas are marked with capture-pressure concerns."
            f" Inspect power distribution, correction rights, access safeguards, appealability, and evidence basis before relying on the receipt.{value_text}"
        )
    if semantic_opaque:
        return (
            "Repair blocker: the current semantic re-read detects an opaque capture-power claim, but the receipt does not show enough accountable mechanism, evidence basis, appeal path, or correction route to make repair capacity clear."
            f"{value_text}"
        )
    return (
        "Repair blocker: recovery remains limited because the receipt records low repair capacity without enough visible safeguards, correction rights, or accountable review structure."
        f"{value_text}"
    )

def _render_current_semantic_reread(container: Any, view: dict[str, Any]) -> None:
    """Always show the current semantic reading for uploaded receipts.

    This is an automatic current scanner pass for comparison only. It never changes
    native receipt values, Standard View, receipt schema, or stored receipt meaning.
    """
    summary = view.get("_current_semantic_reread") or {}
    if not summary:
        text = str(view.get("_receipt_reader_source_text", ""))
        if not text.strip():
            return
        summary = _build_current_semantic_reread(text)
        view["_current_semantic_reread"] = summary
    if not summary.get("available"):
        container.info(f"Current semantic reading: {summary.get('risk', 'semantic scanner unavailable')}.")
        return

    container.markdown("### Current semantic reading")
    container.caption(
        "Automatic current scanner pass on the uploaded receipt text. This is not part of the original receipt and does not rescore, alter, certify, approve, reject, or replace it."
    )
    c1, c2, c3, c4 = container.columns(4)
    c1.metric("Semantic finding", str(summary.get("finding", "NO SIGNAL")))
    c2.metric("Claims", int(summary.get("claims", 0) or 0))
    c3.metric("Mechanisms", int(summary.get("mechanisms", 0) or 0))
    c4.metric("Diagnostic pressure", f"{float(summary.get('pressure', 0.0) or 0.0):+.3f}")

    finding = str(summary.get("finding", "NO SIGNAL"))
    risk = _current_semantic_receipt_note(summary)
    if finding == "NO SIGNAL":
        container.info("No semantic pressure relationship detected by the current scanner. This does not lower or override the native receipt reading.")
    elif finding == "SANCTUARY":
        container.success(f"Current semantic note: {risk}. This is a current re-read only, not a native receipt value.")
    elif finding == "THRESHOLD":
        container.warning(f"Current semantic note: {risk}. Human review should compare this with the native receipt values.")
    else:
        container.error(f"Current semantic note: {risk}. Human review should compare this with the native receipt values.")

    notes = list(summary.get("notes") or [])
    if notes:
        with container.expander("Current semantic notes", expanded=False) as notes_panel:
            for note in notes[:10]:
                notes_panel.markdown(f"- {note}")

    scan = summary.get("scan")
    if scan is not None and format_semantic_pressure_report is not None:
        digest_source = str(view.get("_receipt_reader_source_name", "uploaded receipt")) + "|" + str(view.get("_receipt_reader_source_text", ""))[:300]
        digest = hashlib.sha1(digest_source.encode("utf-8", errors="ignore")).hexdigest()[:12]
        show_debug = container.checkbox(
            "Show current semantic debug details",
            value=False,
            key=f"receipt_current_semantic_debug_{digest}",
            help="Developer/debug view only. The native receipt remains unchanged.",
        )
        if show_debug:
            with container.expander("Developer/debug details — current semantic re-read", expanded=False) as details:
                details.code(format_semantic_pressure_report(scan), language="text")


def _render_single_view(container: Any, view: dict[str, Any]) -> None:
    fields = view["fields"]

    _render_status_banner(container, view)
    _render_top_metric_strip(container, view)

    _render_plain_language_receipt_summary(container, view)
    _render_repair_questions_block(container, view)
    _render_current_semantic_reread(container, view)
    repair_blocker = _receipt_repair_blocker_note(view)
    if repair_blocker:
        container.warning("[!] " + repair_blocker)

    container.markdown(f"### {_metric_section_title(view)}")
    container.caption(_metric_section_caption(view))
    _render_visual_metric_rows(container, view)

    # Secondary diagnostics stay available, but no longer dominate the first view.
    with container.expander("Diagnostics: core logic, reader brief, and failure-mode signals", expanded=False) as expander:
        expander.markdown(f"### {view['core_logic_title']}")
        expander.write(view["core_logic_text"])
        expander.markdown("### Reader Brief")
        expander.write(view["summary"])
        _render_failure_mode_review_signals_compact(expander)
        expander.info("This is a reflection for human review, not certification, approval, rejection, enforcement, or final truth.")
        expander.caption(view["parsing_limits"])

    _render_ai_static_scan_context(container, view)

    world_distribution = (view.get("world_lens_fields") or {}).get("taxonomy_distribution") or []
    if world_distribution:
        with container.expander("World Lens internal taxonomy distribution", expanded=False) as expander:
            expander.table(world_distribution)

    with container.expander("Audit data — native receipt values", expanded=False) as expander:
        expander.caption("Exact values copied from the uploaded receipt. Missing values are not inferred. These values are not certification.")
        expander.table(_native_values_rows(view))


def _batch_receipt_index_rows(parsed: dict[str, Any]) -> list[dict[str, str]]:
    """Build one compact summary row per uploaded receipt in a batch ZIP."""
    rows: list[dict[str, str]] = []
    for index, (filename, view) in enumerate(parsed.get("views") or [], start=1):
        fields = view.get("fields") or {}
        native_state = view.get("native_state", MISSING_VALUE)
        review_pressure = view.get("standard_band", MISSING_VALUE)
        if native_state == "QUESTION_PROMPT":
            review_pressure = "Not scored / review-tool mode"
            integrity = NOT_APPLICABLE
            collapse = NOT_APPLICABLE
            trust = NOT_APPLICABLE
        else:
            integrity = fields.get("integrity", MISSING_VALUE)
            collapse = fields.get("collapse_probability", MISSING_VALUE)
            trust = fields.get("trust", MISSING_VALUE)
        rows.append({
            "#": str(index),
            "File": filename,
            "Module": _display_module_source(view),
            "Native State": native_state,
            "Review Pressure": review_pressure,
            "Protocol Label": fields.get("protocol_label", MISSING_VALUE),
            "Current Semantic": str((view.get("_current_semantic_reread") or {}).get("finding", "Not run")),
            "Integrity": integrity,
            "Collapse": collapse,
            "Trust Index": trust,
            "Repairs": str(len(view.get("repair_questions") or [])),
        })
    return rows

def _render_world_lens_bundle(container: Any, parsed: dict[str, Any]) -> None:
    container.markdown("### World Lens Evidence Bundle")
    container.write(f"Uploaded evidence bundle: {parsed.get('name')}")
    container.write(f"Native receipt files read: {parsed.get('receipt_count', 0)}")
    details = parsed.get("bundle_details") or {}
    summary_files = details.get("summary_files") or []
    evidence_tables = details.get("evidence_tables") or []
    if summary_files:
        container.write(f"Structured metadata files: {len(summary_files)}")
    if evidence_tables:
        container.write(f"Supporting evidence tables: {len(evidence_tables)}")
    container.caption(
        "World Lens ZIP uploads are treated as evidence bundles: the receipt document is the narrative source, "
        "summary JSON is metadata, and CSV files are supporting evidence tables."
    )

    distribution = parsed.get("distribution") or {}
    if distribution:
        container.table([{"Native Evidence View": key, "Receipt Count": value} for key, value in sorted(distribution.items())])

    views = parsed.get("views") or []
    if views:
        first_name, first_view = views[0]
        with container.expander(f"Inspect native World Lens receipt: {first_name}", expanded=True) as expander:
            _render_single_view(expander, first_view)

    if summary_files:
        container.markdown("### Structured Summary Metadata")
        container.caption("Selected key/value metadata from uploaded summary JSON. Raw summary files are not treated as receipts.")
        container.table(_world_lens_summary_rows(summary_files[0]))
        if len(summary_files) > 1:
            container.caption(f"Additional summary metadata files: {len(summary_files) - 1}")

    if evidence_tables:
        container.markdown("### Supporting CSV Evidence Tables")
        container.caption(
            "CSV files are supporting evidence tables. The list below stays compact; full raw tables are hidden in the advanced section."
        )
        container.table([
            {
                "Table": table.get("table_name"),
                "Rows": table.get("row_count"),
                "Purpose": _world_lens_table_description(str(table.get("table_name", ""))),
                "Preview Fields": _preview_field_label(table),
            }
            for table in evidence_tables
        ])
        labels = [f"{table.get('table_name')} — {table.get('filename')}" for table in evidence_tables]
        try:
            selected = container.selectbox(
                "Preview supporting evidence table",
                labels,
                key="receipt_reader_world_lens_evidence_table_preview",
            )
        except Exception:
            selected = labels[0] if labels else None
        if selected:
            selected_index = labels.index(selected)
            selected_table = evidence_tables[selected_index]
            curated_rows = _curated_preview_rows(selected_table)
            container.caption(
                "Showing first 10 uploaded rows only. Values are copied from the uploaded CSV and are not rescored or reinterpreted."
            )
            if curated_rows:
                container.table(curated_rows)
            else:
                container.write("No preview rows found in this supporting evidence table.")
            with container.expander("Advanced: show raw uploaded table preview", expanded=False) as raw_expander:
                raw_expander.caption(
                    "Raw uploaded columns are shown only here to avoid turning the main evidence reader into a wide spreadsheet."
                )
                raw_rows = selected_table.get("preview_rows") or []
                if raw_rows:
                    raw_expander.table(raw_rows)
                else:
                    raw_expander.write("No raw preview rows found in this supporting evidence table.")

    container.info(
        "World Lens Evidence Bundle reading preserves uploaded receipt, metadata, and CSV evidence tables. It does not rescore, merge labels, "
        "certify countries or governments, or create a new receipt."
    )


def _render_batch_zip(container: Any, parsed: dict[str, Any]) -> None:
    if parsed.get("bundle_type") == "world_lens_evidence_bundle":
        _render_world_lens_bundle(container, parsed)
        return

    container.markdown("### Batch Receipt Summary")
    container.write(f"Uploaded batch file: {parsed.get('name')}")
    container.write(f"Receipts read: {parsed.get('receipt_count', 0)}")
    distribution = parsed.get("distribution") or {}
    if distribution:
        container.table([{"Native State": key, "Count": value} for key, value in sorted(distribution.items())])
    container.info("Batch ZIP reading summarizes uploaded receipts only. A current semantic reading is attached to every receipt for comparison; it does not rescore, merge labels, or create a new receipt.")

    views = parsed.get("views") or []
    if not views:
        return

    rows = _batch_receipt_index_rows(parsed)
    container.markdown("### Receipt Index")
    container.caption("One compact row per uploaded receipt. Current Semantic is an automatic current scanner comparison for every receipt; native values remain unchanged.")
    container.table(rows)

    labels = [
        f"{row['#']}. {row['File']} — {row['Native State']}"
        for row in rows
    ]
    try:
        selected_label = container.selectbox(
            "Inspect receipt",
            labels,
            key="receipt_reader_batch_receipt_selector",
        )
        selected_index = labels.index(selected_label) if selected_label in labels else 0
    except Exception:
        selected_index = 0

    selected_name, selected_view = views[selected_index]
    with container.expander(f"Inspect selected receipt: {selected_name}", expanded=False) as expander:
        _render_single_view(expander, selected_view)


def render_receipt_reader_standard_view(container=None) -> None:
    """Render upload-only Receipt Reader - Standard View."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    render_module_page_template_intro(container, RECEIPT_READER_PAGE_COPY)
    container.caption(RECEIPT_READER_BOUNDARY)
    uploaded = container.file_uploader(
        "Upload an ALETHEIA receipt file",
        type=["txt", "md", "json", "zip"],
        accept_multiple_files=False,
        key="aletheia_receipt_reader_upload",
    )

    if uploaded is None:
        container.info("Upload an ALETHEIA receipt file to read it in Standard View.")
        return

    try:
        parsed = parse_uploaded_receipt_file(uploaded)
    except Exception as exc:  # pragma: no cover - Streamlit-facing guardrail
        container.error(f"Could not read uploaded receipt file: {exc}")
        return

    if parsed.get("kind") == "batch_zip":
        _render_batch_zip(container, parsed)
    else:
        _render_single_view(container, parsed["view"])
