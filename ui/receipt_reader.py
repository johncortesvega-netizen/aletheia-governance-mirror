"""Receipt Reader - Standard View helpers.

This module explains uploaded ALETHEIA receipts. It does not rescore, approve,
reject, certify, enforce, override, or change the original receipt.
"""
from __future__ import annotations

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
    for key in ["protocol_adjusted_state", "risk_state", "protocol_label"]:
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

    native_state = _first_native_state(fields, text)
    return {
        "native_state": native_state,
        "standard_band": STANDARD_BANDS.get(native_state, MISSING_VALUE),
        "fields": fields,
        "boundary": RECEIPT_READER_BOUNDARY,
        "plain_language_explanation": (
            "Standard View is a verbal reading aid for the uploaded receipt. It keeps native "
            "ALETHEIA values first and maps them into a secondary review band without creating a new verdict."
        ),
        "human_review_note": "Human review remains required before relying on this reading.",
        "non_certification_note": "This is not certification, approval, rejection, enforcement, or final truth.",
        "parsing_limits": "Only obvious uploaded receipt fields are shown. Missing or unclear fields are not inferred.",
    }


def _render_card(container: Any, title: str, body: str) -> None:
    container.markdown(f"**{title}**")
    container.write(body)


def _render_value_list(container: Any, values: list[tuple[str, str]]) -> None:
    for label, value in values:
        container.markdown(f"- **{label}:** {value}")


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

    _render_card(container, "Plain-language explanation card", str(view["plain_language_explanation"]))
    _render_card(container, "Standard View card", str(view["human_review_note"]))
    container.info(str(view["non_certification_note"]))
    container.caption(str(view["parsing_limits"]))
    if fields["repair_questions"] != MISSING_VALUE:
        container.markdown("**Repair questions found in uploaded receipt**")
        container.write(fields["repair_questions"])
