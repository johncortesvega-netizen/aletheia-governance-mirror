"""Receipt Reader - Standard View helpers.

This module explains uploaded ALETHEIA receipts. It does not rescore, approve,
reject, certify, enforce, override, or change the original receipt.
"""
from __future__ import annotations

import csv
import io
import json
import re
from typing import Any


RECEIPT_READER_BOUNDARY = (
    "Receipt Reader - Standard View explains uploaded ALETHEIA receipts. "
    "It does not rescore, certify, approve, reject, or override the original receipt."
)

MISSING_VALUE = "Not found in uploaded receipt"

STANDARD_BANDS = {
    "SANCTUARY": "Low review pressure",
    "THRESHOLD": "Elevated review pressure",
    "ASYLUM": "High review pressure / escalation review required",
    "QUESTION_PROMPT": "Not scored / review-tool mode",
}

FIELD_PATTERNS = {
    "module_source": [r"(?im)^\s*(?:module|source|active modules)\s*:\s*(.+?)\s*$"],
    "risk_state": [r"(?im)^\s*(?:risk state|risk|state|verdict|judgment)\s*:\s*(.+?)\s*$"],
    "protocol_adjusted_state": [
        r"(?im)^\s*(?:protocol-adjusted state|protocol adjusted state|adjusted state)\s*:\s*(.+?)\s*$",
    ],
    "protocol_label": [r"(?im)^\s*(?:protocol label|protocol state|protocol judgment)\s*:\s*(.+?)\s*$"],
    "integrity": [r"(?im)^\s*integrity\s*:\s*(.+?)\s*$"],
    "friction": [r"(?im)^\s*friction\s*:\s*(.+?)\s*$"],
    "collapse_probability": [r"(?im)^\s*(?:collapse probability|collapse)\s*:\s*(.+?)\s*$"],
    "trust": [r"(?im)^\s*(?:trust index|trust)\s*:\s*(.+?)\s*$"],
    "alignment": [r"(?im)^\s*alignment\s*:\s*(.+?)\s*$"],
    "ego": [r"(?im)^\s*ego\s*:\s*(.+?)\s*$"],
}

WORLD_LENS_PATTERNS = {
    "selected_year": [r"(?im)^\s*-\s*Selected year:\s*\*\*(.+?)\*\*\s*$"],
    "source_state": [r"(?im)^\s*-\s*World Lens source state:\s*\*\*(.+?)\*\*\s*$"],
    "evidence_allocation_status": [r"(?im)^\s*-\s*Evidence allocation status:\s*\*\*(.+?)\*\*\s*$"],
    "allocated_country_rows": [r"(?im)^\s*-\s*Allocated country rows:\s*\*\*(.+?)\*\*\s*$"],
    "active_selected_year_seats": [r"(?im)^\s*-\s*Active selected-year seats:\s*\*\*(.+?)\*\*\s*$"],
    "rows_excluded_diagnostic": [r"(?im)^\s*-\s*Rows excluded / diagnostic:\s*\*\*(.+?)\*\*\s*$"],
    "hidden_zero_seat_rows": [r"(?im)^\s*-\s*Hidden zero-seat diagnostic rows:\s*\*\*(.+?)\*\*\s*$"],
    "weighted_integrity": [r"(?im)^\s*-\s*Weighted integrity:\s*\*\*(.+?)\*\*\s*$"],
    "weighted_friction": [r"(?im)^\s*-\s*Weighted friction:\s*\*\*(.+?)\*\*\s*$"],
    "weighted_collapse_probability": [r"(?im)^\s*-\s*Weighted collapse probability:\s*\*\*(.+?)\*\*\s*$"],
    "average_empirical_coverage": [r"(?im)^\s*-\s*Average empirical coverage:\s*\*\*(.+?)\*\*\s*$"],
}


WORLD_LENS_FIELD_LABELS = [
    ("Selected year", "selected_year"),
    ("Source state", "source_state"),
    ("Evidence allocation status", "evidence_allocation_status"),
    ("Allocated country rows", "allocated_country_rows"),
    ("Active selected-year seats", "active_selected_year_seats"),
    ("Rows excluded / diagnostic", "rows_excluded_diagnostic"),
    ("Hidden zero-seat diagnostic rows", "hidden_zero_seat_rows"),
    ("Weighted integrity", "weighted_integrity"),
    ("Weighted friction", "weighted_friction"),
    ("Weighted collapse probability", "weighted_collapse_probability"),
    ("Average empirical coverage", "average_empirical_coverage"),
]

AI_INTEGRITY_PATTERNS = {
    "review_mode": [r"(?im)^\s*Review mode:\s*(.+?)\s*$"],
    "artifact_type": [r"(?im)^\s*Artifact type:\s*(.+?)\s*$"],
    "internal_taxonomy_label": [r"(?im)^\s*Internal taxonomy label:\s*(.+?)\s*$"],
    "risk_reading": [r"(?im)^\s*Risk reading:\s*(.+?)\s*$"],
    "integrity_reading": [r"(?im)^\s*Integrity reading:\s*(.+?)\s*$"],
    "capture_pressure": [r"(?im)^\s*Capture pressure:\s*(.+?)\s*$"],
    "risk_pressure": [r"(?im)^\s*Risk pressure:\s*(.+?)\s*$"],
    "positive_review_signals": [r"(?im)^\s*Positive review signals:\s*(.+?)\s*$"],
}

AI_INTEGRITY_FIELD_LABELS = [
    ("Review mode", "review_mode"),
    ("Artifact type", "artifact_type"),
    ("Internal taxonomy label", "internal_taxonomy_label"),
    ("Risk reading", "risk_reading"),
    ("Integrity reading", "integrity_reading"),
    ("Capture pressure", "capture_pressure"),
    ("Risk pressure", "risk_pressure"),
    ("Positive review signals", "positive_review_signals"),
]


def _first_match(text: str, patterns: list[str]) -> str:
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return MISSING_VALUE


def _native_state_from_text(value: str) -> str:
    upper = value.upper()
    for state in STANDARD_BANDS:
        if state in upper:
            return state
    return MISSING_VALUE


def _first_native_state(fields: dict[str, str], receipt_text: str) -> str:
    for key in ["protocol_adjusted_state", "risk_state", "protocol_label", "internal_taxonomy_label"]:
        state = _native_state_from_text(fields.get(key, ""))
        if state != MISSING_VALUE:
            return state
    return _native_state_from_text(receipt_text)


def _format_value(value: Any) -> str:
    if value is None:
        return MISSING_VALUE
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, float):
        return f"{value:.4f}"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, list):
        if not value:
            return MISSING_VALUE
        return ", ".join(_format_value(item) for item in value)
    text = str(value).strip()
    return text if text else MISSING_VALUE


def _json_after_machine_readable_marker(text: str) -> dict[str, Any] | None:
    marker = "MACHINE-READABLE RECEIPT JSON"
    lower_text = text.lower()
    marker_index = lower_text.find(marker.lower())
    search_start = marker_index + len(marker) if marker_index != -1 else 0
    brace_index = text.find("{", search_start)
    if brace_index == -1:
        return None
    try:
        payload, _ = json.JSONDecoder().raw_decode(text[brace_index:])
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def _json_from_receipt_text(text: str) -> dict[str, Any] | None:
    stripped = text.strip()
    if stripped.startswith("{"):
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError:
            payload = None
        if isinstance(payload, dict):
            return payload
    return _json_after_machine_readable_marker(text)


def _extract_json_fields(payload: dict[str, Any]) -> dict[str, str]:
    verdict = payload.get("verdict") if isinstance(payload.get("verdict"), dict) else {}
    metrics = payload.get("metrics") if isinstance(payload.get("metrics"), dict) else {}
    return {
        "module_source": _format_value(payload.get("module") or payload.get("active_modules")),
        "risk_state": _format_value(verdict.get("risk") or payload.get("risk")),
        "protocol_adjusted_state": _format_value(
            verdict.get("protocol_adjusted_state")
            or payload.get("protocol_adjusted_state")
            or payload.get("canonical_state")
        ),
        "protocol_label": _format_value(verdict.get("protocol_label") or payload.get("protocol_label")),
        "integrity": _format_value(metrics.get("integrity")),
        "friction": _format_value(metrics.get("friction")),
        "collapse_probability": _format_value(metrics.get("collapse_probability")),
        "trust": _format_value(metrics.get("trust_index") or metrics.get("trust")),
        "alignment": _format_value(metrics.get("alignment")),
        "ego": _format_value(metrics.get("ego")),
    }


def _extract_json_repair_questions(payload: dict[str, Any]) -> str:
    questions = payload.get("repair_questions")
    if not isinstance(questions, list):
        return MISSING_VALUE
    cleaned = [str(item).strip() for item in questions if str(item).strip()]
    if not cleaned:
        return MISSING_VALUE
    return "\n".join(f"- {item}" for item in cleaned)


def _repair_questions_from_text(text: str) -> str:
    lines = text.splitlines()
    start = None
    allowed_headings = {
        "silent operator repair questions",
        "repair questions",
        "repair questions found in uploaded receipt",
    }
    for index, line in enumerate(lines):
        normalized = line.strip().strip(":").lower()
        if normalized in allowed_headings:
            start = index
            break
    if start is None:
        return MISSING_VALUE

    collected: list[str] = []
    for line in lines[start + 1 :]:
        stripped = line.strip()
        if not stripped:
            if collected:
                break
            continue
        if re.match(r"^[A-Z][A-Z0-9 /_-]{2,}:\s*$", stripped) and collected:
            break
        if stripped.startswith(("-", "*")) or re.match(r"^\d+[\.)]\s+", stripped):
            collected.append(stripped)
            continue
        if collected:
            break
    return "\n".join(collected) if collected else MISSING_VALUE


def _markdown_table_rows_after_heading(text: str, heading: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    start = None
    heading_lower = heading.strip().lower()
    for index, line in enumerate(lines):
        if line.strip().lower() == heading_lower:
            start = index + 1
            break
    if start is None:
        return []
    table_lines: list[str] = []
    for line in lines[start:]:
        stripped = line.strip()
        if not stripped:
            if table_lines:
                break
            continue
        if stripped.startswith("## ") and table_lines:
            break
        if stripped.startswith("|"):
            table_lines.append(stripped)
        elif table_lines:
            break
    if len(table_lines) < 3:
        return []
    header = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for raw_row in table_lines[2:]:
        cells = [cell.strip() for cell in raw_row.strip("|").split("|")]
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def _detect_receipt_kind(text: str, fields: dict[str, str]) -> str:
    lower_text = text.lower()
    module = fields.get("module_source", "").lower()
    if "aletheia world lens receipt" in lower_text or "world lens source state" in lower_text:
        return "World Lens"
    if "world lens" in module:
        return "World Lens"
    if "ai integrity receipt context" in lower_text or "ai integrity mirror" in module:
        return "AI Integrity Mirror"
    if "stress test" in lower_text or module in {"simulation", "stress test"}:
        return "Stress Test"
    return fields.get("module_source") or "Generic"


def _world_lens_fields_from_text(text: str) -> dict[str, str]:
    fields = {key: _first_match(text, patterns) for key, patterns in WORLD_LENS_PATTERNS.items()}
    coverage_rows = _markdown_table_rows_after_heading(text, "## Coverage")
    distribution_rows = _markdown_table_rows_after_heading(text, "## Internal taxonomy distribution")
    trust_raw = next((row for row in coverage_rows if row.get("source") == "Trust raw survey"), {})
    trust_prior = next((row for row in coverage_rows if row.get("source") == "Trust prior"), {})
    fields.update({
        "trust_raw_survey_coverage": trust_raw.get("coverage", MISSING_VALUE) or MISSING_VALUE,
        "trust_prior_coverage": trust_prior.get("coverage", MISSING_VALUE) or MISSING_VALUE,
        "taxonomy_distribution_rows": str(len(distribution_rows)) if distribution_rows else MISSING_VALUE,
    })
    return fields


def _ai_integrity_fields_from_text(text: str) -> dict[str, str]:
    return {key: _first_match(text, patterns) for key, patterns in AI_INTEGRITY_PATTERNS.items()}


def read_uploaded_receipt_file(uploaded_file: Any) -> str:
    """Decode an uploaded ALETHEIA receipt file without storing or rescoring it."""
    if uploaded_file is None:
        return ""
    raw = uploaded_file.getvalue() if hasattr(uploaded_file, "getvalue") else uploaded_file.read()
    if isinstance(raw, str):
        return raw
    return bytes(raw or b"").decode("utf-8", errors="replace")


def parse_receipt_standard_view(receipt_text: str) -> dict[str, object]:
    """Extract uploaded receipt fields without inferring missing values or changing the receipt."""
    text = receipt_text or ""
    json_payload = _json_from_receipt_text(text)
    if json_payload is not None:
        fields = _extract_json_fields(json_payload)
        fields["repair_questions"] = _extract_json_repair_questions(json_payload)
    else:
        fields = {key: _first_match(text, patterns) for key, patterns in FIELD_PATTERNS.items()}
        fields["repair_questions"] = _repair_questions_from_text(text)

    # Module-aware overlays keep each uploaded receipt in its native context.
    receipt_kind = _detect_receipt_kind(text, fields)
    world_lens_fields = _world_lens_fields_from_text(text) if receipt_kind == "World Lens" else {}
    ai_integrity_fields = _ai_integrity_fields_from_text(text) if receipt_kind == "AI Integrity Mirror" else {}

    if receipt_kind == "World Lens":
        fields["module_source"] = "World Lens"
        fields["integrity"] = world_lens_fields.get("weighted_integrity", MISSING_VALUE)
        fields["friction"] = world_lens_fields.get("weighted_friction", MISSING_VALUE)
        fields["collapse_probability"] = world_lens_fields.get("weighted_collapse_probability", MISSING_VALUE)
        fields["trust"] = "Raw survey unavailable; trust prior recorded" if world_lens_fields.get("trust_raw_survey_coverage") == "0.0" else MISSING_VALUE
        fields["protocol_label"] = "World Lens selected-year evidence view"
        fields["risk_state"] = "Distribution view"
        fields["protocol_adjusted_state"] = MISSING_VALUE
    elif receipt_kind == "AI Integrity Mirror":
        fields["module_source"] = "AI Integrity Mirror"
        if ai_integrity_fields.get("risk_reading") != MISSING_VALUE:
            fields["risk_state"] = ai_integrity_fields["risk_reading"]
        if ai_integrity_fields.get("internal_taxonomy_label") != MISSING_VALUE:
            fields["protocol_adjusted_state"] = ai_integrity_fields["internal_taxonomy_label"]
        if ai_integrity_fields.get("integrity_reading") != MISSING_VALUE:
            fields["integrity"] = ai_integrity_fields["integrity_reading"]
        if ai_integrity_fields.get("capture_pressure") != MISSING_VALUE:
            fields["friction"] = ai_integrity_fields["capture_pressure"]

    native_state = _first_native_state(fields, text)
    if receipt_kind == "World Lens":
        native_state = "WORLD_LENS_EVIDENCE_VIEW"
        standard_band = "Country-year evidence distribution / human interpretation required"
        explanation = (
            "Standard View is reading this as a World Lens receipt. It keeps the selected-year evidence, "
            "9k seat allocation, empirical coverage, trust-prior note, and taxonomy distribution separate from "
            "Mirror Check scenario wording. It does not certify a country, government, institution, or system."
        )
        parsing_limits = (
            "World Lens receipts are evidence-distribution receipts. Country rows and distribution tables are summarized only when obvious fields are present; missing fields are not inferred."
        )
    elif receipt_kind == "AI Integrity Mirror":
        standard_band = STANDARD_BANDS.get(native_state, MISSING_VALUE)
        explanation = (
            "Standard View is reading this as an AI Integrity Mirror receipt. It reflects a static artifact review only; "
            "it does not test a live model, vendor, deployment, training data, hidden system prompt, or future behavior."
        )
        parsing_limits = "Only obvious uploaded AI Integrity receipt fields are shown. Missing or unclear fields are not inferred."
    elif receipt_kind == "Stress Test":
        standard_band = STANDARD_BANDS.get(native_state, MISSING_VALUE)
        explanation = (
            "Standard View is reading this as a Stress Test / Simulation receipt. It preserves the scenario receipt's native state, "
            "metrics, and repair questions without re-running the scenario or changing the tree/scoring output."
        )
        parsing_limits = "Only obvious uploaded Stress Test receipt fields are shown. Missing or unclear fields are not inferred."
    else:
        standard_band = STANDARD_BANDS.get(native_state, MISSING_VALUE)
        explanation = (
            "Standard View is a verbal reading aid for the uploaded receipt. It keeps native "
            "ALETHEIA values first and maps them into a secondary review band without creating a new verdict."
        )
        parsing_limits = "Only obvious uploaded receipt fields are shown. Missing or unclear fields are not inferred."

    return {
        "receipt_kind": receipt_kind,
        "native_state": native_state,
        "standard_band": standard_band,
        "fields": fields,
        "world_lens_fields": world_lens_fields,
        "ai_integrity_fields": ai_integrity_fields,
        "boundary": RECEIPT_READER_BOUNDARY,
        "plain_language_explanation": explanation,
        "human_review_note": "Human review remains required before relying on this reading.",
        "non_certification_note": "This is not certification, approval, rejection, enforcement, or final truth.",
        "parsing_limits": parsing_limits,
    }


def _render_card(container: Any, title: str, body: str) -> None:
    container.markdown(f"**{title}**")
    container.write(body)


def _render_value_list(container: Any, values: list[tuple[str, str]]) -> None:
    for label, value in values:
        container.markdown(f"- **{label}:** {value}")


def _render_world_lens_cards(container: Any, view: dict[str, object]) -> None:
    world_fields = view.get("world_lens_fields") if isinstance(view.get("world_lens_fields"), dict) else {}
    card_a, card_b = container.columns(2)
    with card_a:
        card_a.markdown("**World Lens scope card**")
        _render_value_list(card_a, [(label, str(world_fields.get(key, MISSING_VALUE))) for label, key in WORLD_LENS_FIELD_LABELS[:7]])
    with card_b:
        card_b.markdown("**World Lens evidence values card**")
        _render_value_list(card_b, [(label, str(world_fields.get(key, MISSING_VALUE))) for label, key in WORLD_LENS_FIELD_LABELS[7:]])
        _render_value_list(card_b, [
            ("Trust raw survey coverage", str(world_fields.get("trust_raw_survey_coverage", MISSING_VALUE))),
            ("Trust prior coverage", str(world_fields.get("trust_prior_coverage", MISSING_VALUE))),
            ("Distribution rows", str(world_fields.get("taxonomy_distribution_rows", MISSING_VALUE))),
        ])


def _render_ai_integrity_cards(container: Any, view: dict[str, object]) -> None:
    fields = view["fields"]
    ai_fields = view.get("ai_integrity_fields") if isinstance(view.get("ai_integrity_fields"), dict) else {}
    card_a, card_b = container.columns(2)
    with card_a:
        card_a.markdown("**Native state card**")
        _render_value_list(card_a, [
            ("Native receipt state", str(view["native_state"])),
            ("Standard review band", str(view["standard_band"])),
            ("Module/source", fields["module_source"]),
        ])
    with card_b:
        card_b.markdown("**AI Integrity artifact card**")
        _render_value_list(card_b, [(label, str(ai_fields.get(key, MISSING_VALUE))) for label, key in AI_INTEGRITY_FIELD_LABELS])


def _render_generic_cards(container: Any, view: dict[str, object]) -> None:
    fields = view["fields"]
    card_a, card_b = container.columns(2)
    with card_a:
        card_a.markdown("**Native state card**")
        _render_value_list(card_a, [
            ("Native receipt state", str(view["native_state"])),
            ("Standard review band", str(view["standard_band"])),
        ])
    with card_b:
        card_b.markdown("**Values card**")
        _render_value_list(card_b, [
            ("Module/source", fields["module_source"]),
            ("Risk state", fields["risk_state"]),
            ("Protocol-adjusted state", fields["protocol_adjusted_state"]),
            ("Protocol label", fields["protocol_label"]),
            ("Integrity", fields["integrity"]),
            ("Friction", fields["friction"]),
            ("Collapse probability", fields["collapse_probability"]),
            ("Trust index", fields["trust"]),
            ("Alignment", fields["alignment"]),
            ("Ego", fields["ego"]),
        ])


def render_receipt_reader_standard_view(container=None) -> None:
    """Render the upload-only Receipt Reader - Standard View."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.subheader("Receipt Reader - Standard View")
    container.caption(RECEIPT_READER_BOUNDARY)
    uploaded_file = container.file_uploader(
        "Upload an ALETHEIA receipt file",
        type=["txt", "md", "json"],
        accept_multiple_files=False,
        key="receipt_reader_uploaded_file",
        help="Receipt Reader reads uploaded ALETHEIA receipt files only. It does not rescore or create a new receipt.",
    )

    if uploaded_file is None:
        container.info("Upload an ALETHEIA receipt file to read it in Standard View.")
        return

    receipt_text = read_uploaded_receipt_file(uploaded_file)
    if not receipt_text.strip():
        container.warning("The uploaded receipt file appears empty. No values were inferred.")
        return

    view = parse_receipt_standard_view(receipt_text)
    fields = view["fields"]
    receipt_kind = str(view.get("receipt_kind", "Generic"))

    if receipt_kind == "World Lens":
        _render_world_lens_cards(container, view)
    elif receipt_kind == "AI Integrity Mirror":
        _render_ai_integrity_cards(container, view)
    else:
        _render_generic_cards(container, view)

    _render_card(container, "Plain-language explanation card", str(view["plain_language_explanation"]))
    _render_card(container, "Standard View card", str(view["human_review_note"]))
    container.info(str(view["non_certification_note"]))
    container.caption(str(view["parsing_limits"]))
    if fields["repair_questions"] != MISSING_VALUE:
        container.markdown("**Repair questions found in uploaded receipt**")
        container.write(fields["repair_questions"])
