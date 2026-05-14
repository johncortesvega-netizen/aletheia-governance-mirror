"""Receipt Reader - Standard View helpers.

This module explains uploaded ALETHEIA receipts. It does not rescore, approve,
reject, certify, enforce, override, or change the original receipt.
"""
from __future__ import annotations

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
    "risk_state": [r"(?im)^\s*(?:risk state|state|verdict|judgment)\s*:\s*(.+?)\s*$"],
    "protocol_adjusted_state": [
        r"(?im)^\s*(?:protocol-adjusted state|protocol adjusted state|adjusted state)\s*:\s*(.+?)\s*$",
    ],
    "protocol_label": [r"(?im)^\s*(?:protocol label|protocol state|protocol judgment)\s*:\s*(.+?)\s*$"],
    "integrity": [r"(?im)^\s*integrity\s*:\s*(.+?)\s*$"],
    "friction": [r"(?im)^\s*friction\s*:\s*(.+?)\s*$"],
    "collapse_probability": [r"(?im)^\s*(?:collapse probability|collapse)\s*:\s*(.+?)\s*$"],
    "trust": [r"(?im)^\s*trust\s*:\s*(.+?)\s*$"],
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


def _repair_questions(text: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if "repair question" in line.lower():
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
        if re.match(r"^[A-Za-z][A-Za-z /_-]{2,}:\s+", stripped) and collected:
            break
        if stripped.startswith(("-", "*")) or re.match(r"^\d+[\.)]\s+", stripped):
            collected.append(stripped)
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
    """Extract obvious uploaded receipt fields without inferring missing values."""
    text = receipt_text or ""
    fields = {key: _first_match(text, patterns) for key, patterns in FIELD_PATTERNS.items()}
    fields["repair_questions"] = _repair_questions(text)
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
        _render_card(card_a, "Native state card", f"Native receipt state: {view['native_state']}\n\nStandard review band: {view['standard_band']}")
    with card_b:
        _render_card(card_b, "Values card", "\n".join([
            f"Module/source: {fields['module_source']}",
            f"Risk state: {fields['risk_state']}",
            f"Protocol-adjusted state: {fields['protocol_adjusted_state']}",
            f"Protocol label: {fields['protocol_label']}",
            f"Integrity: {fields['integrity']}",
            f"Friction: {fields['friction']}",
            f"Collapse probability: {fields['collapse_probability']}",
            f"Trust: {fields['trust']}",
            f"Alignment: {fields['alignment']}",
            f"Ego: {fields['ego']}",
        ]))

    _render_card(container, "Plain-language explanation card", str(view["plain_language_explanation"]))
    _render_card(container, "Standard View card", str(view["human_review_note"]))
    container.info(str(view["non_certification_note"]))
    container.caption(str(view["parsing_limits"]))
    if fields["repair_questions"] != MISSING_VALUE:
        container.markdown("**Repair questions found in uploaded receipt**")
        container.write(fields["repair_questions"])
