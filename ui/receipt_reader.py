"""Receipt Reader - Standard View helpers.

Receipt Reader explains uploaded ALETHEIA receipts. It does not rescore,
approve, reject, certify, enforce, override, or change the original receipt.
"""
from __future__ import annotations

import csv
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
    "WORLD_LENS_EVIDENCE_VIEW": "Evidence context (World Lens)",
}

STATUS_LINES = {
    "SANCTUARY": "The uploaded receipt maps to a stable low-review operating context.",
    "THRESHOLD": "The uploaded receipt maps to an elevated-review context that needs human inspection.",
    "ASYLUM": "The uploaded receipt maps to high review pressure and requires careful human escalation review.",
    "QUESTION_PROMPT": "The uploaded receipt is a review-tool or question-prompt reading, not a scored scenario.",
    "WORLD_LENS_EVIDENCE_VIEW": "The uploaded receipt is a World Lens evidence-context receipt, not a single scenario verdict.",
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
        "weighted_collapse_probability": _markdown_bullet_value(text, "Weighted collapse probability"),
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
        {"Metric": "Weighted Collapse Probability", "Value": world.get("weighted_collapse_probability", MISSING_VALUE), "Interpretation": "Year-level weighted collapse-pressure context, not a prediction or certification."},
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


def _module_family(module: str, text: str = "") -> str:
    if _is_world_lens_receipt(text):
        return "World Lens"
    value = f"{module} {text}".lower()
    if "world lens" in value or "selected-year evidence" in value or "world_lens_evidence_view" in value:
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
            return "Low collapse-pressure reading in the uploaded receipt."
        if number <= 0.3:
            return "Reviewable collapse pressure."
        return "High collapse pressure."
    if key == "friction":
        if number <= 0.01:
            return "Zero review friction in the uploaded receipt."
        if number <= 0.15:
            return "Low review friction in the uploaded receipt."
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

    if native_state == "WORLD_LENS_EVIDENCE_VIEW":
        return (
            "The uploaded receipt is a World Lens selected-year evidence view. Read it as aggregate country-year "
            "context with 9k allocation and empirical coverage notes, not as a single scenario verdict or country certification."
        )
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
    world_lens_fields: dict[str, Any] = {}
    ai_integrity_fields: dict[str, str] = {}

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

    if module_family == "World Lens":
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
        views = [(filename, parse_receipt_standard_view(text)) for filename, text in receipts]
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
    return {"kind": "single", "name": filename, "view": parse_receipt_standard_view(text)}


def _metric_section_title(view: dict[str, Any]) -> str:
    family = view.get("module_family")
    if family == "World Lens":
        return "World Lens Evidence Metrics"
    if family == "Stress Test / Simulation":
        return "Scenario Review Metrics"
    if family == "AI Integrity Mirror":
        return "Artifact Review Metrics"
    return "Performance & Risk Metrics"


def _metric_section_caption(view: dict[str, Any]) -> str:
    family = view.get("module_family")
    if family == "World Lens":
        return "Selected-year evidence values from the uploaded World Lens receipt; no new verdict is generated."
    if family == "Stress Test / Simulation":
        return "Uploaded scenario receipt values, shown without rerunning the scenario."
    if family == "AI Integrity Mirror":
        return "Uploaded static artifact review values; this does not test a live model or vendor."
    return "Quantitative values copied from the uploaded receipt."


def _display_module_source(view: dict[str, Any]) -> str:
    fields = view.get("fields") or {}
    if view.get("module_family") == "Stress Test / Simulation":
        return "Stress Test / Simulation"
    return fields.get("module_source", MISSING_VALUE)


def _render_single_view(container: Any, view: dict[str, Any]) -> None:
    fields = view["fields"]
    container.markdown(f"### System Status: {view['system_status']}")
    container.write(view["status_line"])

    container.markdown(
        f"**Native State:** {view['native_state']}  \n"
        f"**Review Pressure:** {view['standard_band']}  \n"
        f"**Protocol Label:** {fields.get('protocol_label', MISSING_VALUE)}  \n"
        f"**Module Source:** {_display_module_source(view)}"
    )

    container.markdown(f"### {_metric_section_title(view)}")
    container.caption(_metric_section_caption(view))
    container.table(view["metric_rows"])

    world_distribution = (view.get("world_lens_fields") or {}).get("taxonomy_distribution") or []
    if world_distribution:
        container.markdown("### World Lens Internal Taxonomy Distribution")
        container.table(world_distribution)

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


def _render_world_lens_bundle(container: Any, parsed: dict[str, Any]) -> None:
    container.markdown("### World Lens Evidence Bundle")
    container.write(f"Uploaded evidence bundle: {parsed.get('name')}")
    container.write(f"Native receipt files read: {parsed.get('receipt_count', 0)}")
    container.caption(
        "World Lens ZIP uploads are treated as evidence bundles: the receipt document is the narrative source, "
        "summary JSON is metadata, and CSV files are supporting evidence tables."
    )

    distribution = parsed.get("distribution") or {}
    if distribution:
        container.table([{"Native Evidence View": key, "Receipt Count": value} for key, value in sorted(distribution.items())])

    details = parsed.get("bundle_details") or {}
    summary_files = details.get("summary_files") or []
    if summary_files:
        container.markdown("#### Structured Summary Metadata")
        container.table(summary_files)

    evidence_tables = details.get("evidence_tables") or []
    if evidence_tables:
        container.markdown("#### Supporting Evidence Tables")
        container.table([
            {
                "Table": table.get("table_name"),
                "File": table.get("filename"),
                "Rows": table.get("row_count"),
                "Columns": ", ".join(table.get("columns") or []),
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
            preview_rows = evidence_tables[selected_index].get("preview_rows") or []
            container.caption("First rows only. The table is shown as uploaded and is not rescored or reinterpreted.")
            if preview_rows:
                container.table(preview_rows)
            else:
                container.write("No preview rows found in this supporting evidence table.")

    container.info("World Lens Evidence Bundle reading preserves uploaded information only. It does not rescore, merge verdicts, certify countries or governments, or create a new receipt.")

    views = parsed.get("views") or []
    if views:
        first_name, first_view = views[0]
        with container.expander(f"Inspect native World Lens receipt: {first_name}", expanded=False) as expander:
            _render_single_view(expander, first_view)


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
    container.info("Batch ZIP reading summarizes uploaded receipts only. It does not rescore, merge verdicts, or create a new receipt.")
    views = parsed.get("views") or []
    if views:
        first_name, first_view = views[0]
        with container.expander(f"Inspect first receipt: {first_name}", expanded=False) as expander:
            _render_single_view(expander, first_view)


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
