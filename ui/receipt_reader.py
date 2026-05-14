"""Receipt Reader - Standard View helpers.

Receipt Reader explains uploaded ALETHEIA receipts. It does not rescore,
approve, reject, certify, enforce, override, or change the original receipt.
"""
from __future__ import annotations

import io
import json
import re
import zipfile
from collections import Counter
from typing import Any


RECEIPT_READER_BOUNDARY = (
    "Receipt Reader - Standard View explains uploaded ALETHEIA receipts. "
    "It does not rescore, certify, approve, reject, enforce, or override the original receipt."
)

MISSING_VALUE = "Not found in uploaded receipt"

STANDARD_BANDS = {
    "SANCTUARY": "Low (Standard Band)",
    "THRESHOLD": "Elevated (Standard Band)",
    "ASYLUM": "High (Standard Band / escalation review required)",
    "QUESTION_PROMPT": "Not scored (review-tool mode)",
}

STATUS_LINES = {
    "SANCTUARY": "The uploaded receipt maps to a stable low-review operating context.",
    "THRESHOLD": "The uploaded receipt maps to an elevated-review context that needs human inspection.",
    "ASYLUM": "The uploaded receipt maps to high review pressure and requires careful human escalation review.",
    "QUESTION_PROMPT": "The uploaded receipt is a review-tool or question-prompt reading, not a scored scenario.",
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
    "collapse_probability": [r"(?im)^\s*(?:collapse probability|collapse)\s*:\s*(.+?)\s*$"],
    "trust": [r"(?im)^\s*(?:trust index|trust)\s*:\s*(.+?)\s*$"],
    "alignment": [r"(?im)^\s*alignment\s*:\s*(.+?)\s*$"],
    "ego": [r"(?im)^\s*ego\s*:\s*(.+?)\s*$"],
}

METRIC_ORDER = [
    ("trust", "Trust Index"),
    ("alignment", "Alignment"),
    ("integrity", "Integrity"),
    ("collapse_probability", "Collapse Probability"),
    ("friction", "Friction"),
    ("ego", "Ego"),
]


def _first_match(text: str, patterns: list[str]) -> str:
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return MISSING_VALUE


def _native_state_from_text(value: Any) -> str:
    upper = str(value or "").upper()
    for state in STANDARD_BANDS:
        if state in upper:
            return state
    return MISSING_VALUE


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


def _module_family(module: str, text: str = "") -> str:
    value = f"{module} {text}".lower()
    if "world lens" in value or "selected-year evidence" in value or "9k" in value:
        return "World Lens"
    if "ai integrity" in value or "static artifact" in value:
        return "AI Integrity Mirror"
    if "simulation" in value or "stress test" in value:
        return "Stress Test / Simulation"
    if "privacy" in value:
        return "Privacy Audit"
    if "evidence lab" in value:
        return "Evidence Lab"
    if "mirror check" in value:
        return "Mirror Check"
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
        "risk_state": _format_value(verdict.get("risk") or data.get("risk") or _first_match(text, TEXT_FIELD_PATTERNS["risk_state"])),
        "protocol_adjusted_state": _format_value(
            verdict.get("protocol_adjusted_state")
            or threshold.get("canonical_state")
            or data.get("protocol_adjusted_state")
            or _first_match(text, TEXT_FIELD_PATTERNS["protocol_adjusted_state"])
        ),
        "protocol_label": _format_value(
            verdict.get("protocol_label")
            or threshold.get("protocol_label")
            or data.get("protocol_label")
            or _first_match(text, TEXT_FIELD_PATTERNS["protocol_label"])
        ),
        "integrity": _format_value(metrics.get("integrity") or data.get("integrity")),
        "friction": _format_value(metrics.get("friction") or data.get("friction")),
        "collapse_probability": _format_value(metrics.get("collapse_probability") or data.get("collapse_probability")),
        "trust": _format_value(metrics.get("trust_index") or data.get("trust_index")),
        "alignment": _format_value(metrics.get("alignment") or data.get("alignment")),
        "ego": _format_value(metrics.get("ego") or data.get("ego")),
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
            return "Near-total reliability."
        if number >= 0.75:
            return "Strong reliability; still requires human review."
        return "Reliability pressure is visible."
    if key == "alignment":
        if number >= 0.9:
            return "High synergy with core objectives."
        if number >= 0.75:
            return "Generally aligned with review objectives."
        return "Alignment pressure needs review."
    if key == "integrity":
        if number >= 0.9:
            return "Very strong structural consistency."
        if number >= 0.7:
            return "Solid structural consistency."
        if number >= 0.5:
            return "Mixed structural consistency."
        return "Low structural consistency."
    if key == "collapse_probability":
        if number <= 0.1:
            return "Minimal risk of system failure."
        if number <= 0.3:
            return "Reviewable collapse pressure."
        return "High collapse pressure."
    if key == "friction":
        if number <= 0.01:
            return "Zero operational resistance."
        if number <= 0.15:
            return "Low operational resistance."
        return "Friction requires review."
    if key == "ego":
        if number <= 0.01:
            return "Effectively neutralized."
        if number <= 0.15:
            return "Low ego pressure."
        return "Ego pressure requires review."
    return "Shown as recorded in the uploaded receipt."


def _summary_for_state(native_state: str, fields: dict[str, str]) -> str:
    risk = fields.get("risk_state", MISSING_VALUE)
    trust = fields.get("trust", MISSING_VALUE)
    alignment = fields.get("alignment", MISSING_VALUE)
    friction = fields.get("friction", MISSING_VALUE)
    collapse = fields.get("collapse_probability", MISSING_VALUE)

    if native_state == "SANCTUARY":
        return (
            f"The uploaded receipt is operating in a {risk} risk state with friction {friction}. "
            f"Trust ({trust}) and alignment ({alignment}) are strong in the native values, and collapse probability "
            f"({collapse}) is low. This is a Standard View translation only; it does not create a new verdict."
        )
    if native_state == "THRESHOLD":
        return (
            f"The uploaded receipt is in {native_state} with {risk} risk pressure. The values should be read as a "
            "human-review checkpoint: inspect repair questions, appealability, transparency, and safeguards before relying on it."
        )
    if native_state == "ASYLUM":
        return (
            "The uploaded receipt carries high review pressure. Treat the repair questions and human-review boundary as central; "
            "do not use this reader as approval, rejection, enforcement, or certification."
        )
    if native_state == "QUESTION_PROMPT":
        return "The uploaded receipt is a review-tool prompt rather than a scored scenario. Use it to guide human inspection."
    return "The uploaded receipt could not be mapped into a native state without inferring missing values."


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
    fields = _fields_from_json(data, text) if data else _fields_from_text(text)

    repair_questions: list[str] = []
    if isinstance(data, dict) and isinstance(data.get("repair_questions"), list):
        repair_questions = [str(item).strip() for item in data["repair_questions"] if str(item).strip()]
    if not repair_questions:
        repair_questions = _repair_questions_from_text(text)

    native_state = _native_state_from_text(fields.get("protocol_adjusted_state"))
    if native_state == MISSING_VALUE:
        native_state = _native_state_from_text(fields.get("risk_state"))
    if native_state == MISSING_VALUE:
        native_state = _native_state_from_text(text)

    module_family = _module_family(fields.get("module_source", ""), text)
    metric_rows = [
        {
            "Metric": label,
            "Value": fields.get(key, MISSING_VALUE),
            "Interpretation": _interpret_metric(key, fields.get(key, MISSING_VALUE), native_state),
        }
        for key, label in METRIC_ORDER
    ]

    return {
        "native_state": native_state,
        "system_status": native_state,
        "status_line": STATUS_LINES.get(native_state, "The uploaded receipt is shown without inferring missing values."),
        "standard_band": STANDARD_BANDS.get(native_state, MISSING_VALUE),
        "module_family": module_family,
        "fields": fields,
        "metric_rows": metric_rows,
        "repair_questions": repair_questions,
        "core_logic_title": _core_logic_title(module_family),
        "core_logic_text": _core_logic_text(module_family),
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


def _read_zip_receipts(uploaded_file: Any) -> tuple[list[tuple[str, str]], str]:
    name = getattr(uploaded_file, "name", "uploaded receipts.zip") or "uploaded receipts.zip"
    raw = uploaded_file.getvalue()
    receipts: list[tuple[str, str]] = []
    with zipfile.ZipFile(io.BytesIO(bytes(raw))) as archive:
        for info in archive.infolist():
            lower = info.filename.lower()
            if info.is_dir() or not lower.endswith((".txt", ".md", ".json")):
                continue
            text = archive.read(info).decode("utf-8", errors="replace")
            receipts.append((info.filename, text))
    return receipts, name


def parse_uploaded_receipt_file(uploaded_file: Any) -> dict[str, Any]:
    """Parse one uploaded receipt file or a ZIP of receipt text files."""
    name = getattr(uploaded_file, "name", "") or ""
    if name.lower().endswith(".zip"):
        receipts, zip_name = _read_zip_receipts(uploaded_file)
        views = [(filename, parse_receipt_standard_view(text)) for filename, text in receipts]
        distribution = Counter(view.get("native_state", MISSING_VALUE) for _, view in views)
        return {
            "kind": "batch_zip",
            "name": zip_name,
            "receipt_count": len(views),
            "distribution": dict(distribution),
            "views": views,
        }
    text, filename = _read_uploaded_text(uploaded_file)
    return {"kind": "single", "name": filename, "view": parse_receipt_standard_view(text)}


def _render_single_view(container: Any, view: dict[str, Any]) -> None:
    fields = view["fields"]
    container.markdown(f"### System Status: {view['system_status']}")
    container.write(view["status_line"])

    container.markdown(
        f"**Native State:** {view['native_state']}  \n"
        f"**Review Pressure:** {view['standard_band']}  \n"
        f"**Protocol Label:** {fields.get('protocol_label', MISSING_VALUE)}  \n"
        f"**Module Source:** {fields.get('module_source', MISSING_VALUE)}"
    )

    container.markdown("### Performance & Risk Metrics")
    container.caption("Quantitative analysis of uploaded receipt health and alignment.")
    container.table(view["metric_rows"])

    container.markdown(f"### {view['core_logic_title']}")
    container.write(view["core_logic_text"])

    container.markdown("### Summary for the Reader")
    container.write(view["summary"])
    container.info("This is not certification, approval, rejection, enforcement, or final truth. Human review remains required.")
    container.caption(view["parsing_limits"])

    questions = view.get("repair_questions") or []
    if questions:
        container.markdown("### Repair questions found in uploaded receipt")
        for question in questions:
            container.markdown(f"- {question}")


def _render_batch_zip(container: Any, parsed: dict[str, Any]) -> None:
    container.markdown("### Batch Receipt Summary")
    container.write(f"Uploaded batch file: {parsed.get('name')}")
    container.write(f"Receipts read: {parsed.get('receipt_count', 0)}")
    distribution = parsed.get("distribution") or {}
    if distribution:
        container.table([{"Native State": key, "Count": value} for key, value in sorted(distribution.items())])
    container.info("Batch ZIP reading summarizes uploaded receipts only. It does not rescore, merge verdicts, or create a new receipt.")
    views = parsed.get("views") or []
    if views:
        first_name, first_view = views[0]
        with container.expander(f"Inspect first receipt: {first_name}", expanded=False):
            _render_single_view(container, first_view)


def render_receipt_reader_standard_view(container=None) -> None:
    """Render upload-only Receipt Reader - Standard View."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.subheader("Receipt Reader - Standard View")
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
