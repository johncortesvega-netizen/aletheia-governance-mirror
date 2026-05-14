"""Receipt Reader - Standard View helpers.

This module explains pasted ALETHEIA receipts. It does not rescore, approve,
reject, certify, enforce, override, or change the original receipt.
"""
from __future__ import annotations

import re


RECEIPT_READER_BOUNDARY = (
    "Receipt Reader - Standard View explains pasted ALETHEIA receipts. "
    "It does not rescore, certify, approve, reject, or override the original receipt."
)

MISSING_VALUE = "Not found in pasted receipt"

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


def parse_receipt_standard_view(receipt_text: str) -> dict[str, object]:
    """Extract obvious receipt fields without inferring missing values."""
    text = receipt_text or ""
    fields = {key: _first_match(text, patterns) for key, patterns in FIELD_PATTERNS.items()}
    fields["repair_questions"] = _repair_questions(text)
    native_state = _first_native_state(fields, text)
    return {
        "native_state": native_state,
        "standard_band": STANDARD_BANDS.get(native_state, MISSING_VALUE),
        "fields": fields,
        "boundary": RECEIPT_READER_BOUNDARY,
        "parsing_limits": "Only obvious pasted receipt fields are shown. Missing or unclear fields are not inferred.",
    }


def render_receipt_reader_standard_view(container=None) -> None:
    """Render the Receipt Reader - Standard View."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.subheader("Receipt Reader - Standard View")
    container.caption(RECEIPT_READER_BOUNDARY)
    receipt_text = container.text_area("Paste an ALETHEIA receipt", height=220)

    if not receipt_text.strip():
        container.info("Paste a receipt to see native values and standard review bands.")
        return

    view = parse_receipt_standard_view(receipt_text)
    fields = view["fields"]

    container.markdown("### Native receipt state")
    container.write(f"Native state: {view['native_state']}")
    container.write(f"Standard review band: {view['standard_band']}")

    container.markdown("### Native ALETHEIA values")
    rows = [
        ("Module/source", fields["module_source"]),
        ("Risk state", fields["risk_state"]),
        ("Protocol-adjusted state", fields["protocol_adjusted_state"]),
        ("Protocol label", fields["protocol_label"]),
        ("Integrity", fields["integrity"]),
        ("Friction", fields["friction"]),
        ("Collapse probability", fields["collapse_probability"]),
        ("Trust", fields["trust"]),
        ("Alignment", fields["alignment"]),
        ("Ego", fields["ego"]),
        ("Repair questions", fields["repair_questions"]),
    ]
    container.table([{"Field": label, "Value": value} for label, value in rows])

    container.markdown("### Plain-language explanation")
    container.write(
        "Standard View is secondary to native ALETHEIA values. It helps humans read the receipt; it does not create a new verdict."
    )
    container.warning("Human review remains required.")
    container.info(str(view["parsing_limits"]))
