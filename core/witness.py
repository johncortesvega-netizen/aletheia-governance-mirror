"""
ALETHEIA local witness receipt utilities.

These helpers create local, user-held audit receipts. They do not publish,
synchronize, or send results to any external authority, ledger, identity system,
or notification layer.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import zipfile
from datetime import datetime, timezone
from io import BytesIO
from typing import Any, Mapping, Sequence


MAX_BATCH_RECEIPTS = 50

DEMO_INPUT_STATUS = "DEMO_INPUT"
DEMO_INPUT_WARNING = (
    "Demo/sample input: this receipt is for interface review only and should not be treated "
    "as a real scenario assessment."
)


def _is_demo_input(input_status: str | None, input_type: str | None = None) -> bool:
    """Return True when a receipt represents bundled demo/sample input."""
    return str(input_status or "").upper() == DEMO_INPUT_STATUS or str(input_type or "").upper() == DEMO_INPUT_STATUS


def is_witness_batch_input(text: str, *, min_items: int = 2, max_items: int = MAX_BATCH_RECEIPTS) -> bool:
    """Return True when pasted text should be treated as a batch, not one scenario.

    This protects Mirror Check from collapsing a numbered questionnaire or
    multi-line scenario list into one high-risk combined reading. The function
    only checks structure; it does not judge content.
    """
    raw = (text or "").strip()
    if not raw:
        return False
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    if len(lines) < min_items:
        return False
    numbered_re = re.compile(r"^\s*\d{1,3}[\.\)]\s+")
    numbered_count = sum(1 for line in lines if numbered_re.match(line))
    has_separator = any(line == "---" for line in lines)
    parsed_count = len(parse_witness_batch_input(raw, max_items=max_items))
    return parsed_count >= min_items and (numbered_count >= min_items or has_separator or len(lines) >= min_items)


def parse_witness_batch_input(text: str, *, max_items: int = MAX_BATCH_RECEIPTS) -> list[str]:
    """Split a pasted witness-batch prompt into reviewable scenario phrases.

    Supported input styles:
    - one phrase per non-empty line
    - numbered lists such as ``1. ...`` or ``2) ...``
    - blocks separated by a line containing only ``---``

    The function is deliberately conservative: it returns at most ``max_items``
    phrases and drops empty items. This keeps batch review bounded, local, and
    reviewable.
    """
    raw = (text or "").strip()
    if not raw:
        return []

    lines = [line.strip() for line in raw.splitlines()]
    separator_mode = any(line == "---" for line in lines)
    numbered_re = re.compile(r"^\s*\d{1,3}[\.\)]\s+(.*)$")

    items: list[str] = []
    current: list[str] = []

    def flush() -> None:
        nonlocal current
        item = " ".join(part.strip() for part in current if part.strip()).strip()
        if item:
            items.append(item)
        current = []

    for line in lines:
        if not line:
            if separator_mode:
                flush()
            continue
        if separator_mode and line == "---":
            flush()
            continue
        match = numbered_re.match(line)
        if match:
            flush()
            current.append(match.group(1).strip())
            continue
        if separator_mode:
            current.append(line)
        else:
            # Without explicit separators, treat each non-empty line as one phrase.
            items.append(line)
    flush()

    cleaned: list[str] = []
    seen: set[str] = set()
    for item in items:
        normalized = " ".join(item.split())
        if normalized and normalized not in seen:
            cleaned.append(normalized)
            seen.add(normalized)
        if len(cleaned) >= max_items:
            break
    return cleaned


def is_witness_scenario_statement(text: str) -> bool:
    """Return True when an item is written as a scenario statement, not an audit question.

    Patch 69.1 guard: Stress Test upload batches can contain declarative
    scenario lines such as "A smart-grid system cuts power...". Those must be
    simulated as USER_INPUT scenarios, not suppressed as QUESTION_PROMPT review
    questions merely because they appear in a .txt batch.
    """
    raw = " ".join((text or "").strip().split())
    if not raw:
        return False
    lower = raw.lower()
    scenario_starts = (
        "a ", "an ", "the ",
        "een ", "de ", "het ",
    )
    scenario_markers = (
        " system ", " system-reset ", " trigger ", " platform ", " protocol ", " ai ", " algorithm ",
        " leader ", " council ", " agency ", " provider ", " model ",
        " systeem ", " platform ", " protocol ", " algoritme ",
        " leider ", " raad ", " instantie ", " model ",
    )
    action_markers = (
        " automatically ", " requires ", " recommends ", " denies ",
        " allows ", " uses ", " shares ", " limits ", " claims ", " disabled ",
        " krijgt ", " vereist ", " gebruikt ", " weigert ", " kan ",
        " centraliseert ", " verzamelt ", " controleert ", " presenteert ",
    )
    # Declarative scenarios are usually article-led statements and do not end as questions.
    if lower.endswith("?"):
        return False
    padded = f" {lower} "
    return lower.startswith(scenario_starts) and (
        any(marker in padded for marker in scenario_markers)
        or any(marker in padded for marker in action_markers)
    )


def is_witness_question_prompt(text: str) -> bool:
    """Return True when one batch item is an audit prompt/question, not a policy proposal.

    This keeps question banks from being judged as if the user proposed every
    risky word inside the question. It is structural only: the text can still be
    used later as a review prompt. Patch 69.1 makes the test strict enough that
    declarative scenario batches uploaded as .txt are not misclassified as
    QUESTION_PROMPT.
    """
    raw = " ".join((text or "").strip().split())
    if not raw:
        return False
    if is_witness_scenario_statement(raw):
        return False
    lower = raw.lower()
    question_words = (
        "wie ", "wat ", "waar ", "waarom ", "wanneer ", "welke ", "welk ",
        "hoe ", "hoeveel ", "kan ", "is ", "wordt ", "worden ", "geeft ",
        "dient ", "faciliteert ", "versterkt ", "rust ",
        "who ", "what ", "where ", "why ", "when ", "which ", "how ",
        "can ", "could ", "is ", "are ", "does ", "do ", "should ", "would ",
    )
    return lower.endswith("?") or lower.startswith(question_words)


def is_witness_question_set(items: Sequence[str], *, min_ratio: float = 0.6) -> bool:
    """Return True when a batch should be handled as a set of audit questions.

    A question set must be mostly actual questions. Scenario-statement batches
    remain Stress Test scenarios even when uploaded as .txt files.
    """
    clean = [item for item in items if str(item or "").strip()]
    if not clean:
        return False
    if sum(1 for item in clean if is_witness_scenario_statement(item)) > 0:
        scenario_ratio = sum(1 for item in clean if is_witness_scenario_statement(item)) / max(len(clean), 1)
        if scenario_ratio >= 0.25:
            return False
    question_count = sum(1 for item in clean if is_witness_question_prompt(item))
    return (question_count / max(len(clean), 1)) >= min_ratio


def build_local_question_prompt_receipt(
    *,
    module: str,
    input_text: str,
    processed_text: str | None = None,
    invisibility_applied: bool = False,
    app_version: str = "unknown",
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    """Build a local receipt for an audit question, not a governance proposal.

    Question prompts are review tools. They should not be escalated merely
    because they mention capture terms such as surveillance, control, or bias.
    """
    processed_text = processed_text if processed_text is not None else input_text
    receipt = build_local_witness_receipt(
        module=module,
        input_text=input_text,
        processed_text=processed_text,
        input_status="QUESTION_PROMPT",
        input_type="QUESTION_PROMPT",
        scan={
            "power_concentration": None,
            "decision_transparency": None,
            "regulatory_presence": None,
            "anonymity_level": None,
            "capital_scale": None,
            "technical_complexity": None,
            "scan_mode": "Question Prompt",
        },
        sim={
            "stability": None,
            "trust_index": None,
            "alignment": None,
            "ego": None,
            "collapse_risk": None,
        },
        report={
            "integrity": None,
            "friction": None,
            "collapse_probability": None,
            "trust_friction": None,
            "repair_questions": [
                "Use this as a review prompt. What answer would make the system more transparent, appealable, and safe to question?"
            ],
        },
        verdict="QUESTION_PROMPT",
        risk="Review Tool",
        protocol_label="Audit Question / Review Tool",
        invisibility_applied=invisibility_applied,
        app_version=app_version,
        generated_at_utc=generated_at_utc,
    )
    return receipt


def build_local_witness_batch_index(
    receipts: Sequence[Mapping[str, Any]],
    *,
    module: str = "Mirror Check",
    app_version: str = "unknown",
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    """Build a local-only index for a group of witness receipts."""
    generated_at_utc = generated_at_utc or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    safe_receipts = [_receipt_safe(receipt) for receipt in receipts]
    items = []
    for idx, receipt in enumerate(safe_receipts, start=1):
        verdict = receipt.get("verdict", {}) or {}
        hashes = receipt.get("hashes", {}) or {}
        items.append({
            "item": idx,
            "module": receipt.get("module", module),
            "input_status": receipt.get("input_status"),
            "input_type": receipt.get("input_type", receipt.get("input_status")),
            "invisibility_filter_applied": receipt.get("invisibility_filter_applied"),
            "scenario_sha256": hashes.get("scenario_sha256"),
            "processed_scenario_sha256": hashes.get("processed_scenario_sha256"),
            "audit_receipt_sha256": hashes.get("audit_receipt_sha256"),
            "protocol_adjusted_state": verdict.get("protocol_adjusted_state"),
            "risk": verdict.get("risk"),
            "protocol_label": verdict.get("protocol_label"),
        })

    index_payload = {
        "receipt_type": "ALETHEIA_LOCAL_WITNESS_BATCH_INDEX",
        "notice": "Local user-held batch index only. It does not publish, sync, score, or enforce action.",
        "dataflow": "Power -> Mirror. Never Mirror -> Power.",
        "generated_at_utc": generated_at_utc,
        "app_version": app_version,
        "module": module,
        "receipt_count": len(items),
        "items": items,
    }
    batch_hash_payload = {
        "module": module,
        "receipt_count": len(items),
        "receipt_hashes": [item.get("audit_receipt_sha256") for item in items],
    }
    index_payload["hashes"] = {
        "batch_index_sha256": sha256_hex(canonical_json(_receipt_safe(batch_hash_payload)))
    }
    return _receipt_safe(index_payload)


def render_local_witness_batch_index_text(index: Mapping[str, Any]) -> str:
    """Render a readable plain-text index for a batch witness archive."""
    index = _receipt_safe(index)
    items = index.get("items", []) or []
    hashes = index.get("hashes", {}) or {}
    rows = []
    for item in items:
        rows.append(
            f"{item.get('item'):02d}. {item.get('protocol_adjusted_state')} / {item.get('risk')} "
            f"— receipt {item.get('audit_receipt_sha256')}"
        )
    item_block = "\n".join(rows) or "No receipts recorded."
    return f"""ALETHEIA LOCAL WITNESS BATCH INDEX
Receipt type: {index.get('receipt_type')}
Generated: {index.get('generated_at_utc')}
App version: {index.get('app_version')}
Module: {index.get('module')}
Receipt count: {index.get('receipt_count')}
Batch index SHA-256: {hashes.get('batch_index_sha256')}

NOTICE
{index.get('notice')}
Dataflow boundary: {index.get('dataflow')}

RECEIPTS
{item_block}

MACHINE-READABLE BATCH INDEX JSON
{json.dumps(index, indent=2, ensure_ascii=False, sort_keys=True)}
"""


def build_local_witness_batch_zip(
    receipts: Sequence[Mapping[str, Any]],
    *,
    module: str = "Mirror Check",
    app_version: str = "unknown",
    generated_at_utc: str | None = None,
) -> tuple[bytes, dict[str, Any]]:
    """Return a zip archive containing all receipt texts and a batch index."""
    index = build_local_witness_batch_index(
        receipts, module=module, app_version=app_version, generated_at_utc=generated_at_utc
    )
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("batch_index.txt", render_local_witness_batch_index_text(index))
        zf.writestr("batch_index.json", json.dumps(index, indent=2, ensure_ascii=False, sort_keys=True))
        for idx, receipt in enumerate(receipts, start=1):
            zf.writestr(f"receipt_{idx:02d}.txt", render_local_witness_receipt_text(receipt))
            zf.writestr(f"receipt_{idx:02d}.json", json.dumps(_receipt_safe(receipt), indent=2, ensure_ascii=False, sort_keys=True))
    return buffer.getvalue(), index


def _json_safe(value: Any) -> Any:
    """Convert common Python/numpy-like values into stable JSON-safe values."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Mapping):
        return {str(k): _json_safe(v) for k, v in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(v) for v in value]
    # numpy/pandas scalar fallback without importing optional dependencies here
    if hasattr(value, "item"):
        try:
            return _json_safe(value.item())
        except Exception:
            pass
    return str(value)


def _receipt_safe(value: Any) -> Any:
    """Return JSON-safe receipt values with readable float precision."""
    value = _json_safe(value)
    if isinstance(value, float):
        if math.isfinite(value):
            return round(value, 4)
        return str(value)
    if isinstance(value, Mapping):
        return {str(k): _receipt_safe(v) for k, v in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, (list, tuple, set)):
        return [_receipt_safe(v) for v in value]
    return value


def _display_value(value: Any) -> str:
    """Format values for the readable receipt without changing their meaning."""
    value = _receipt_safe(value)
    if isinstance(value, float):
        return f"{value:.4f}"
    if value is None:
        return "Not recorded"
    return str(value)


def _short_list(values: Any, limit: int = 5) -> list[Any]:
    """Keep receipt diagnostics readable while preserving the key evidence."""
    if not isinstance(values, list):
        return []
    return [_receipt_safe(v) for v in values[:limit]]


def _flatten_unique_terms(values: Any, limit: int = 10) -> list[Any]:
    """Return unique short evidence terms without creating a new authority layer."""
    seen: set[str] = set()
    out: list[Any] = []
    if not isinstance(values, list):
        return out
    for item in values:
        if isinstance(item, (list, tuple, set)):
            candidates = list(item)
        else:
            candidates = [item]
        for candidate in candidates:
            safe = _receipt_safe(candidate)
            key = str(safe)
            if not key or key in seen:
                continue
            seen.add(key)
            out.append(safe)
            if len(out) >= limit:
                return out
    return out


def _hard_capture_receipt_trace(contextual_hits: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Summarize Patch 28.1 hard-capture evidence for local receipts.

    The trace is descriptive only. It preserves why a capture multiplier fired
    without creating enforcement, identity sync, public ledgers, or push alerts.
    """
    hits = [dict(hit) for hit in contextual_hits if isinstance(hit, Mapping)]
    if not hits:
        return {
            "hard_contextual_capture": False,
            "hard_contextual_capture_count": 0,
            "max_contextual_capture_multiplier": 0.0,
            "hard_capture_terms": [],
            "multiplier_terms": [],
            "positive_terms": [],
            "power_terms": [],
            "review_note": "No hard contextual capture trigger recorded.",
        }

    hard_hits = [hit for hit in hits if bool(hit.get("hard_capture_trigger"))]
    multipliers = []
    for hit in hits:
        try:
            multipliers.append(float(hit.get("severity_multiplier", 1.0)))
        except (TypeError, ValueError):
            multipliers.append(1.0)

    return _receipt_safe({
        "hard_contextual_capture": bool(hard_hits),
        "hard_contextual_capture_count": len(hard_hits),
        "max_contextual_capture_multiplier": round(max(multipliers or [0.0]), 3),
        "hard_capture_terms": _flatten_unique_terms([hit.get("hard_capture_terms") for hit in hits], 10),
        "multiplier_terms": _flatten_unique_terms([hit.get("multiplier_terms") for hit in hits], 10),
        "positive_terms": _flatten_unique_terms([hit.get("positive_terms") for hit in hits], 8),
        "power_terms": _flatten_unique_terms([hit.get("power_terms") for hit in hits], 8),
        "review_note": "Hard contextual capture is receipt evidence only: mirror, not enforcement authority." if hard_hits else "Contextual capture multiplier evidence recorded without a hard trigger.",
    })


def _ethics_receipt_summary(report: Mapping[str, Any]) -> dict[str, Any]:
    """Extract contextual ethics diagnostics for local witness receipts.

    This is diagnostic only. It does not change protocol verdicts or scoring formulas.
    """
    ethics = dict(report.get("ethics_diagnostics") or {})
    dimensions = dict(ethics.get("dimensions") or {})
    contextual_hits = list(ethics.get("contextual_capture_hits") or [])
    grip_hits = list(ethics.get("grip_marker_hits") or [])
    hard_capture_trace = _hard_capture_receipt_trace(contextual_hits)
    return _receipt_safe({
        "ethics_score": ethics.get("ethics_score"),
        "ethics_verdict": ethics.get("verdict"),
        "ethics_adjusted_integrity": report.get("ethics_adjusted_integrity"),
        "micro_sovereignty": dimensions.get("Micro Sovereignty"),
        "contextual_capture_count": len(contextual_hits),
        "grip_marker_count": len(grip_hits),
        "contextual_capture_hits": _short_list(contextual_hits, 3),
        "hard_capture_trace": hard_capture_trace,
        "hard_contextual_capture": hard_capture_trace.get("hard_contextual_capture"),
        "hard_contextual_capture_count": hard_capture_trace.get("hard_contextual_capture_count"),
        "max_contextual_capture_multiplier": hard_capture_trace.get("max_contextual_capture_multiplier"),
        "grip_marker_hits": _short_list(grip_hits, 8),
        "risks": _short_list(ethics.get("risks"), 6),
        "strengths": _short_list(ethics.get("strengths"), 6),
        "confidence": ethics.get("confidence"),
    }) if ethics else {}




def _cognitive_resilience_receipt_summary(report: Mapping[str, Any]) -> dict[str, Any]:
    """Extract Cognitive Resilience diagnostics for local witness receipts.

    Patch 27B: diagnostic only. These fields are visible in receipts but do
    not change scoring, protocol labels, or enforcement behavior.
    """
    diagnostics = dict(report.get("cognitive_resilience_diagnostics") or {})
    evidence = dict(diagnostics.get("evidence") or {})
    if not diagnostics:
        return {}
    return _receipt_safe({
        "cognitive_resilience_signal": diagnostics.get("cognitive_resilience_signal"),
        "educational_decentralization_signal": diagnostics.get("educational_decentralization_signal"),
        "central_info_capture_signal": diagnostics.get("central_info_capture_signal"),
        "knowledge_capacity_signal": diagnostics.get("knowledge_capacity_signal"),
        "capture_architecture_signal": diagnostics.get("capture_architecture_signal"),
        "high_cr_laundering_blocked": diagnostics.get("high_cr_laundering_blocked"),
        "education_defense_signal": diagnostics.get("education_defense_signal"),
        "entertainment_compliance_signal": diagnostics.get("entertainment_compliance_signal"),
        "algorithmic_erosion_signal": diagnostics.get("algorithmic_erosion_signal"),
        "z_axis_depth_risk_signal": diagnostics.get("z_axis_depth_risk_signal"),
        "cognitive_resilience_score": diagnostics.get("cognitive_resilience_score"),
        "educational_decentralization_score": diagnostics.get("educational_decentralization_score"),
        "central_info_capture_score": diagnostics.get("central_info_capture_score"),
        "knowledge_capacity_score": diagnostics.get("knowledge_capacity_score"),
        "education_defense_score": diagnostics.get("education_defense_score"),
        "entertainment_compliance_score": diagnostics.get("entertainment_compliance_score"),
        "algorithmic_erosion_score": diagnostics.get("algorithmic_erosion_score"),
        "z_axis_depth_risk_score": diagnostics.get("z_axis_depth_risk_score"),
        "diagnostic_only": diagnostics.get("diagnostic_only", True),
        "system_property_note": diagnostics.get("system_property_note"),
        "education_defense_property_note": diagnostics.get("education_defense_property_note"),
        "narrative": diagnostics.get("narrative"),
        "evidence": {
            "local_open_learning_terms": _short_list(evidence.get("local_open_learning_terms"), 6),
            "revocability_terms": _short_list(evidence.get("revocability_terms"), 6),
            "educational_decentralization_terms": _short_list(evidence.get("educational_decentralization_terms"), 6),
            "knowledge_capacity_terms": _short_list(evidence.get("knowledge_capacity_terms"), 6),
            "central_info_capture_terms": _short_list(evidence.get("central_info_capture_terms"), 6),
            "capture_or_relinquish_terms": _short_list(evidence.get("capture_or_relinquish_terms"), 6),
            "entertainment_compliance_terms": _short_list(evidence.get("entertainment_compliance_terms"), 6),
            "algorithmic_erosion_terms": _short_list(evidence.get("algorithmic_erosion_terms"), 6),
            "z_axis_depth_terms": _short_list(evidence.get("z_axis_depth_terms"), 6),
            "z_axis_erosion_terms": _short_list(evidence.get("z_axis_erosion_terms"), 6),
            "negated_centralization_terms": _short_list(evidence.get("negated_centralization_terms"), 4),
            "contextual_capture_count": evidence.get("contextual_capture_count"),
            "grip_marker_count": evidence.get("grip_marker_count"),
        },
    })



def _safe_float(value: Any, default: float = 0.0) -> float:
    """Return a bounded float for diagnostic receipt mapping."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(number):
        return default
    return max(0.0, min(1.0, number))


def _threshold_component(
    *,
    name: str,
    negative: str,
    positive: str,
    pressure: float,
    growth: float,
) -> dict[str, Any]:
    """Build one Threshold Mapping component row.

    Patch 72: descriptive only. This does not create a fourth taxonomy state
    or change scoring, routing, storage, or enforcement behavior.
    """
    pressure = _safe_float(pressure)
    growth = _safe_float(growth)
    if pressure > growth + 0.12:
        reading = "Threshold -"
        dominant = negative
    elif growth > pressure + 0.12:
        reading = "Threshold +"
        dominant = positive
    else:
        reading = "Balanced Threshold"
        dominant = "Mixed pressure and repair signals; human review must inspect both sides."

    return _receipt_safe({
        "component": name,
        "threshold_minus_pressure": negative,
        "threshold_plus_growth": positive,
        "pressure_score": round(pressure, 4),
        "growth_score": round(growth, 4),
        "reading": reading,
        "dominant_pattern": dominant,
    })


def _threshold_mapping_layer(
    *,
    verdict: str,
    scan: Mapping[str, Any],
    sim: Mapping[str, Any],
    report: Mapping[str, Any],
    protocol_label: str,
) -> dict[str, Any]:
    """Map THRESHOLD results between captured logic and distributed resilience.

    The layer is a receipt/navigation aid only:
    - canonical states remain SANCTUARY / THRESHOLD / ASYLUM
    - no score is changed
    - no enforcement, identity sync, ledger, or authority claim is created
    """
    state = str(verdict or "").upper()
    if state == "QUESTION_PROMPT":
        return {}

    power = _safe_float(scan.get("power_concentration"), 0.5)
    transparency = _safe_float(scan.get("decision_transparency"), 0.5)
    regulation = _safe_float(scan.get("regulatory_presence"), 0.5)
    trust = _safe_float(sim.get("trust_index"), 0.5)
    alignment = _safe_float(sim.get("alignment"), 0.5)
    ego = _safe_float(sim.get("ego"), 0.5)
    integrity = _safe_float(report.get("integrity"), 0.5)
    collapse_probability = _safe_float(report.get("collapse_probability"), 0.5)

    ethics = dict(report.get("ethics_diagnostics") or {})
    grip_count = _safe_float((ethics.get("grip_marker_count") or 0) / 8, 0.0)
    contextual_capture = _safe_float((ethics.get("contextual_capture_count") or 0) / 8, 0.0)
    hard_capture = 1.0 if ethics.get("hard_contextual_capture") else 0.0

    repair_questions = list(report.get("repair_questions") or [])
    repair_index = min(1.0, len(repair_questions) / 5.0)
    review_strength = max(transparency, regulation, repair_index, alignment)
    central_truth_gate_pressure = max(power, grip_count, contextual_capture, hard_capture)
    weak_correction_pressure = max(1.0 - regulation, 1.0 - transparency, collapse_probability)
    conditional_access_pressure = max(power, ego, grip_count, hard_capture)

    power_component = _threshold_component(
        name="Power balance",
        negative='Central "Truth Gate" or one-source-of-truth pressure.',
        positive="Distributed verification with multiple witnesses and inspectable evidence.",
        pressure=central_truth_gate_pressure,
        growth=max(1.0 - power, transparency, regulation),
    )
    correction_component = _threshold_component(
        name="Correction",
        negative="No, weak, or non-time-bound appeal and correction path.",
        positive="Open, time-bound appeal or review process with human review.",
        pressure=weak_correction_pressure,
        growth=review_strength,
    )
    access_component = _threshold_component(
        name="Access",
        negative="Access or care is conditional on behavior, ID, obedience, or surveillance.",
        positive="Basic needs remain protected without coercive access conditions.",
        pressure=conditional_access_pressure,
        growth=max(1.0 - power, 1.0 - ego, regulation, trust),
    )
    components = [power_component, correction_component, access_component]

    pressure_average = sum(float(item.get("pressure_score", 0.0)) for item in components) / len(components)
    growth_average = sum(float(item.get("growth_score", 0.0)) for item in components) / len(components)
    z_axis_position = round(max(-1.0, min(1.0, growth_average - pressure_average)), 4)

    if state == "ASYLUM":
        direction = "Toward ASYLUM"
    elif state == "SANCTUARY":
        direction = "Toward SANCTUARY"
    elif z_axis_position <= -0.12:
        direction = "Toward ASYLUM"
    elif z_axis_position >= 0.12:
        direction = "Toward SANCTUARY"
    else:
        direction = "Balanced THRESHOLD"

    asylum_pressure_signals: list[str] = []
    sanctuary_growth_signals: list[str] = []

    if central_truth_gate_pressure >= 0.62:
        asylum_pressure_signals.append("Central truth-gate or concentrated verification pressure.")
    if weak_correction_pressure >= 0.62:
        asylum_pressure_signals.append("Weak transparency, review, or correction pathway.")
    if conditional_access_pressure >= 0.62:
        asylum_pressure_signals.append("Conditional access, behavioral control, ID, surveillance, or grip pressure.")
    if collapse_probability >= 0.62:
        asylum_pressure_signals.append("Collapse probability remains elevated.")

    if transparency >= 0.62:
        sanctuary_growth_signals.append("Decision transparency is visible.")
    if regulation >= 0.62:
        sanctuary_growth_signals.append("Regulatory or review presence is visible.")
    if repair_index >= 0.4:
        sanctuary_growth_signals.append("Repair questions provide an active human-review route.")
    if alignment >= 0.62 and ego <= 0.38:
        sanctuary_growth_signals.append("Alignment outweighs ego pressure.")

    if not asylum_pressure_signals:
        asylum_pressure_signals.append("No dominant Asylum pressure signal recorded in this mapping layer.")
    if not sanctuary_growth_signals:
        sanctuary_growth_signals.append("No strong Sanctuary growth signal recorded in this mapping layer.")

    if direction == "Toward ASYLUM":
        dominant_pressure = "Care, safety, or access language is coupled to concentrated control, weak appeal, or capture pressure."
    elif direction == "Toward SANCTUARY":
        dominant_pressure = "Human review, appealability, transparency, and repair capacity outweigh central-control pressure."
    else:
        dominant_pressure = "Mixed governance pressure: neither capture nor distributed repair clearly dominates."

    return _receipt_safe({
        "layer_type": "Threshold Mapping Layer",
        "canonical_state": state,
        "threshold_direction": direction,
        "z_axis_position": z_axis_position,
        "integrity_gap": round(max(0.0, 1.0 - integrity), 4),
        "repair_index": round(repair_index, 4),
        "dominant_pressure": dominant_pressure,
        "protocol_label": protocol_label,
        "component_readings": components,
        "asylum_pressure_signals": asylum_pressure_signals[:6],
        "sanctuary_growth_signals": sanctuary_growth_signals[:6],
        "note": "Descriptive receipt mapping only. It does not create a new verdict, enforcement path, public ledger, Global ID sync, or central storage.",
    })


def _display_threshold_mapping_layer_block(mapping: Mapping[str, Any]) -> str:
    """Render Patch 72 Threshold Mapping Layer in plain-text receipts."""
    if not isinstance(mapping, Mapping) or not mapping:
        return "No threshold mapping recorded."

    rows = []
    for item in mapping.get("component_readings", []) or []:
        if not isinstance(item, Mapping):
            continue
        rows.append(
            f"- {item.get('component')}: {item.get('reading')}\n"
            f"  Threshold -: {item.get('threshold_minus_pressure')}\n"
            f"  Threshold +: {item.get('threshold_plus_growth')}\n"
            f"  Pressure/Growth: {_display_value(item.get('pressure_score'))} / {_display_value(item.get('growth_score'))}\n"
            f"  Dominant pattern: {item.get('dominant_pattern')}"
        )

    pressure = mapping.get("asylum_pressure_signals", []) or []
    growth = mapping.get("sanctuary_growth_signals", []) or []
    return (
        f"Canonical state: {mapping.get('canonical_state')}\n"
        f"Threshold direction: {mapping.get('threshold_direction')}\n"
        f"Z-axis position: {_display_value(mapping.get('z_axis_position'))}\n"
        f"Integrity gap: {_display_value(mapping.get('integrity_gap'))}\n"
        f"Repair index: {_display_value(mapping.get('repair_index'))}\n"
        f"Dominant pressure: {mapping.get('dominant_pressure')}\n\n"
        "Component readings:\n"
        f"{chr(10).join(rows) if rows else '- None recorded'}\n\n"
        "Threshold - pressure signals:\n"
        f"{chr(10).join('- ' + str(v) for v in pressure) if pressure else '- None recorded'}\n\n"
        "Threshold + growth signals:\n"
        f"{chr(10).join('- ' + str(v) for v in growth) if growth else '- None recorded'}\n\n"
        f"Note: {mapping.get('note')}"
    )


def canonical_json(payload: Mapping[str, Any]) -> str:
    """Return deterministic JSON for hashing and local receipts."""
    return json.dumps(_json_safe(payload), sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha256_hex(text: str) -> str:
    """Return a SHA-256 hex digest for text."""
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def build_local_witness_receipt(
    *,
    module: str,
    input_text: str = "",
    processed_text: str = "",
    input_status: str = "USER_INPUT",
    input_type: str | None = None,
    scan: Mapping[str, Any] | None = None,
    sim: Mapping[str, Any] | None = None,
    report: Mapping[str, Any] | None = None,
    verdict: str = "THRESHOLD",
    risk: str = "Medium",
    protocol_label: str = "Unclassified",
    invisibility_applied: bool = False,
    app_version: str = "unknown",
    rubric_version: str = "v0.1",
    prompt_version: str = "v0.1",
    active_modules: list[str] | tuple[str, ...] | None = None,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    """Build a local audit receipt with deterministic hashes.

    The receipt is intentionally local-first. It records the audit fingerprint
    and selected metrics, but it does not create a public ledger entry or any
    external synchronization target.
    """
    scan = dict(scan or {})
    sim = dict(sim or {})
    report = dict(report or {})
    generated_at_utc = generated_at_utc or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    scenario_hash = sha256_hex(input_text or "")
    processed_hash = sha256_hex(processed_text or input_text or "")
    report_hash = sha256_hex(canonical_json(_receipt_safe(report)))
    active_modules = list(active_modules or [module])
    ethics_summary = _ethics_receipt_summary(report)
    cognitive_resilience_summary = _cognitive_resilience_receipt_summary(report)
    threshold_mapping = _threshold_mapping_layer(
        verdict=verdict,
        scan=scan,
        sim=sim,
        report=report,
        protocol_label=protocol_label,
    )
    demo_mode = _is_demo_input(input_status, input_type)

    audit_fingerprint_payload = {
        "module": module,
        "input_status": input_status,
        "input_type": input_type or input_status,
        "scenario_hash": scenario_hash,
        "processed_hash": processed_hash,
        "verdict": verdict,
        "risk": risk,
        "protocol_label": protocol_label,
        "invisibility_applied": bool(invisibility_applied),
        "app_version": app_version,
        "rubric_version": rubric_version,
        "prompt_version": prompt_version,
        "active_modules": active_modules,
        "document_fingerprint_sha256": scenario_hash,
        "processed_document_fingerprint_sha256": processed_hash,
        "report_fingerprint_sha256": report_hash,
        "demo_mode": bool(demo_mode),
        "demo_warning": DEMO_INPUT_WARNING if demo_mode else None,
        "integrity": report.get("integrity"),
        "friction": report.get("friction"),
        "collapse_probability": report.get("collapse_probability"),
        "trust_friction": report.get("trust_friction"),
        "stability": sim.get("stability"),
        "trust_index": sim.get("trust_index"),
        "alignment": sim.get("alignment"),
        "ego": sim.get("ego"),
        "collapse_risk": sim.get("collapse_risk"),
        "ethics_score": ethics_summary.get("ethics_score"),
        "ethics_adjusted_integrity": ethics_summary.get("ethics_adjusted_integrity"),
        "micro_sovereignty": ethics_summary.get("micro_sovereignty"),
        "contextual_capture_count": ethics_summary.get("contextual_capture_count"),
        "grip_marker_count": ethics_summary.get("grip_marker_count"),
        "hard_contextual_capture": ethics_summary.get("hard_contextual_capture"),
        "hard_contextual_capture_count": ethics_summary.get("hard_contextual_capture_count"),
        "max_contextual_capture_multiplier": ethics_summary.get("max_contextual_capture_multiplier"),
        "cognitive_resilience_signal": cognitive_resilience_summary.get("cognitive_resilience_signal"),
        "educational_decentralization_signal": cognitive_resilience_summary.get("educational_decentralization_signal"),
        "central_info_capture_signal": cognitive_resilience_summary.get("central_info_capture_signal"),
        "education_defense_signal": cognitive_resilience_summary.get("education_defense_signal"),
        "entertainment_compliance_signal": cognitive_resilience_summary.get("entertainment_compliance_signal"),
        "algorithmic_erosion_signal": cognitive_resilience_summary.get("algorithmic_erosion_signal"),
        "z_axis_depth_risk_signal": cognitive_resilience_summary.get("z_axis_depth_risk_signal"),
        "threshold_direction": threshold_mapping.get("threshold_direction"),
        "threshold_z_axis_position": threshold_mapping.get("z_axis_position"),
        "threshold_repair_index": threshold_mapping.get("repair_index"),
        "threshold_integrity_gap": threshold_mapping.get("integrity_gap"),
    }
    audit_hash = sha256_hex(canonical_json(_receipt_safe(audit_fingerprint_payload)))

    return _receipt_safe({
        "receipt_type": "ALETHEIA_LOCAL_WITNESS_RECEIPT",
        "receipt_version": "local-witness-v2",
        "notice": "Local user-held receipt only. Not a legal, political, medical, religious, institutional, or automated authority determination.",
        "dataflow": "Power -> Mirror. Never Mirror -> Power.",
        "generated_at_utc": generated_at_utc,
        "app_version": app_version,
        "rubric_version": rubric_version,
        "prompt_version": prompt_version,
        "active_modules": active_modules,
        "module": module,
        "input_status": input_status,
        "input_type": input_type or input_status,
        "invisibility_filter_applied": bool(invisibility_applied),
        "demo_mode": bool(demo_mode),
        "demo_warning": DEMO_INPUT_WARNING if demo_mode else None,
        "hashes": {
            "scenario_sha256": scenario_hash,
            "processed_scenario_sha256": processed_hash,
            "document_fingerprint_sha256": scenario_hash,
            "processed_document_fingerprint_sha256": processed_hash,
            "report_fingerprint_sha256": report_hash,
            "audit_receipt_sha256": audit_hash,
        },
        "authority_boundary": {
            "stored_locally": True,
            "public_ledger": False,
            "global_id_sync": False,
            "central_storage": False,
            "authority_claim": False,
            "human_review_required": True,
        },
        "verdict": {
            "protocol_adjusted_state": verdict,
            "risk": risk,
            "protocol_label": protocol_label,
        },
        "metrics": {
            "integrity": report.get("integrity"),
            "friction": report.get("friction"),
            "collapse_probability": report.get("collapse_probability"),
            "trust_friction": report.get("trust_friction"),
            "stability": sim.get("stability"),
            "trust_index": sim.get("trust_index"),
            "alignment": sim.get("alignment"),
            "ego": sim.get("ego"),
            "collapse_risk": sim.get("collapse_risk"),
        },
        "raw_metrics_before_ethics": _receipt_safe(report.get("raw_metrics_before_ethics") or {}),
        "threshold_mapping_layer": threshold_mapping,
        "scanner_features": {
            "power_concentration": scan.get("power_concentration"),
            "decision_transparency": scan.get("decision_transparency"),
            "regulatory_presence": scan.get("regulatory_presence"),
            "anonymity_level": scan.get("anonymity_level"),
            "capital_scale": scan.get("capital_scale"),
            "technical_complexity": scan.get("technical_complexity"),
            "scan_mode": scan.get("scan_mode"),
        },
        "ethics_diagnostics": ethics_summary,
        "cognitive_resilience_diagnostics": cognitive_resilience_summary,
        "ethics_adjustment": {
            "applied": bool(report.get("ethics_adjustment_applied", False)),
            "reason": _receipt_safe(report.get("ethics_adjustment_reason") or {}),
        },
        "repair_questions": list(report.get("repair_questions") or [])[:8],
        "recovery_note": "If this receipt is disputed, rerun the same local input and compare the scenario, processed-scenario, and audit receipt hashes. The receipt itself does not enforce action.",
    })



def _display_raw_metrics_block(raw_metrics: Any) -> str:
    raw = raw_metrics or {}
    if not isinstance(raw, Mapping) or not raw:
        return "No ethics adjustment recorded."
    keys = [
        "integrity", "friction", "collapse_probability", "trust_friction",
        "stability", "trust_index", "alignment", "ego", "collapse_risk",
    ]
    return "\n".join(f"{key.replace('_', ' ').capitalize()}: {_display_value(raw.get(key))}" for key in keys if key in raw) or "No ethics adjustment recorded."



def _display_hard_capture_trace_block(trace: Any) -> str:
    if not isinstance(trace, Mapping) or not trace:
        return "No hard contextual capture trace recorded."
    hard_terms = trace.get("hard_capture_terms", []) or []
    multiplier_terms = trace.get("multiplier_terms", []) or []
    positive_terms = trace.get("positive_terms", []) or []
    power_terms = trace.get("power_terms", []) or []
    return "\n".join([
        f"Hard contextual capture: {_display_value(trace.get('hard_contextual_capture'))}",
        f"Hard trigger count: {_display_value(trace.get('hard_contextual_capture_count'))}",
        f"Max capture multiplier: {_display_value(trace.get('max_contextual_capture_multiplier'))}",
        f"Hard capture terms: {'; '.join(str(v) for v in hard_terms) if hard_terms else 'None recorded'}",
        f"Multiplier terms: {'; '.join(str(v) for v in multiplier_terms) if multiplier_terms else 'None recorded'}",
        f"Positive-frame terms: {'; '.join(str(v) for v in positive_terms) if positive_terms else 'None recorded'}",
        f"Power terms: {'; '.join(str(v) for v in power_terms) if power_terms else 'None recorded'}",
        f"Review note: {_display_value(trace.get('review_note'))}",
    ])


def _display_ethics_adjustment_block(adjustment: Any) -> str:
    adj = adjustment or {}
    if not isinstance(adj, Mapping):
        return "No ethics adjustment recorded."
    reason = adj.get("reason") or {}
    lines = [f"Applied: {_display_value(adj.get('applied'))}"]
    if isinstance(reason, Mapping) and reason:
        labels = {
            "contextual_capture_count": "Contextual capture hits",
            "grip_marker_count": "Grip marker hits",
            "micro_sovereignty": "Micro sovereignty",
            "integrity_gap": "Integrity gap",
            "total_ethics_pressure": "Total ethics pressure",
        }
        for key in ["contextual_capture_count", "grip_marker_count", "micro_sovereignty", "integrity_gap", "total_ethics_pressure"]:
            if key in reason:
                lines.append(f"{labels[key]}: {_display_value(reason.get(key))}")
    return "\n".join(lines)



def _display_cognitive_resilience_block(diagnostics: Any) -> str:
    diag = diagnostics or {}
    if not isinstance(diag, Mapping) or not diag:
        return "No Cognitive Resilience diagnostics recorded."
    evidence = diag.get("evidence") or {}
    central_terms = evidence.get("central_info_capture_terms") or []
    knowledge_terms = evidence.get("knowledge_capacity_terms") or []
    learning_terms = evidence.get("local_open_learning_terms") or []
    entertainment_terms = evidence.get("entertainment_compliance_terms") or []
    algorithmic_terms = evidence.get("algorithmic_erosion_terms") or []
    z_axis_terms = evidence.get("z_axis_erosion_terms") or []
    return "\n".join([
        f"Cognitive resilience signal: {_display_value(diag.get('cognitive_resilience_signal'))}",
        f"Educational decentralization signal: {_display_value(diag.get('educational_decentralization_signal'))}",
        f"Central info capture signal: {_display_value(diag.get('central_info_capture_signal'))}",
        f"Knowledge capacity signal: {_display_value(diag.get('knowledge_capacity_signal'))}",
        f"Capture architecture signal: {_display_value(diag.get('capture_architecture_signal'))}",
        f"High CR laundering blocked: {_display_value(diag.get('high_cr_laundering_blocked'))}",
        f"Education defense signal: {_display_value(diag.get('education_defense_signal'))}",
        f"Entertainment compliance signal: {_display_value(diag.get('entertainment_compliance_signal'))}",
        f"Algorithmic erosion signal: {_display_value(diag.get('algorithmic_erosion_signal'))}",
        f"Z-axis depth risk signal: {_display_value(diag.get('z_axis_depth_risk_signal'))}",
        f"Diagnostic only: {_display_value(diag.get('diagnostic_only'))}",
        f"System property note: {_display_value(diag.get('system_property_note'))}",
        f"Education defense note: {_display_value(diag.get('education_defense_property_note'))}",
        f"Narrative: {_display_value(diag.get('narrative'))}",
        f"Local/open learning evidence: {'; '.join(str(v) for v in learning_terms) if learning_terms else 'None recorded'}",
        f"Central info capture evidence: {'; '.join(str(v) for v in central_terms) if central_terms else 'None recorded'}",
        f"Knowledge capacity evidence: {'; '.join(str(v) for v in knowledge_terms) if knowledge_terms else 'None recorded'}",
        f"Entertainment compliance evidence: {'; '.join(str(v) for v in entertainment_terms) if entertainment_terms else 'None recorded'}",
        f"Algorithmic erosion evidence: {'; '.join(str(v) for v in algorithmic_terms) if algorithmic_terms else 'None recorded'}",
        f"Z-axis erosion evidence: {'; '.join(str(v) for v in z_axis_terms) if z_axis_terms else 'None recorded'}",
    ])




def _display_demo_guard_block(receipt: Mapping[str, Any]) -> str:
    """Render a clear non-evaluative warning for bundled demo/sample inputs."""
    if not bool(receipt.get("demo_mode")):
        return ""
    warning = receipt.get("demo_warning") or DEMO_INPUT_WARNING
    return f"\nDemo mode: True\nDemo warning: {warning}"


def render_local_witness_receipt_text(receipt: Mapping[str, Any]) -> str:
    """Render a local witness receipt as a readable plain-text report."""
    receipt = _receipt_safe(receipt)
    hashes = receipt.get("hashes", {}) or {}
    verdict = receipt.get("verdict", {}) or {}
    metrics = receipt.get("metrics", {}) or {}
    features = receipt.get("scanner_features", {}) or {}
    boundary = receipt.get("authority_boundary", {}) or {}
    active_modules = receipt.get("active_modules", []) or []
    ethics = receipt.get("ethics_diagnostics", {}) or {}
    ethics_adjustment = receipt.get("ethics_adjustment", {}) or {}
    cognitive_resilience = receipt.get("cognitive_resilience_diagnostics", {}) or {}
    threshold_mapping = receipt.get("threshold_mapping_layer", {}) or {}
    questions = receipt.get("repair_questions", []) or []
    question_block = "\n".join(f"- {q}" for q in questions) or "- None recorded"
    demo_guard_block = _display_demo_guard_block(receipt)
    ethics_risks = ethics.get("risks", []) or []
    ethics_strengths = ethics.get("strengths", []) or []
    ethics_block = "No contextual ethics diagnostics recorded."
    if ethics:
        ethics_block = (
            f"Ethics score: {_display_value(ethics.get('ethics_score'))}\n"
            f"Ethics-adjusted integrity: {_display_value(ethics.get('ethics_adjusted_integrity'))}\n"
            f"Micro sovereignty: {_display_value(ethics.get('micro_sovereignty'))}\n"
            f"Contextual capture hits: {_display_value(ethics.get('contextual_capture_count'))}\n"
            f"Grip marker hits: {_display_value(ethics.get('grip_marker_count'))}\n"
            f"Hard contextual capture: {_display_value(ethics.get('hard_contextual_capture'))}\n"
            f"Max capture multiplier: {_display_value(ethics.get('max_contextual_capture_multiplier'))}\n"
            f"Ethics verdict: {_display_value(ethics.get('ethics_verdict'))}\n"
            f"Risks: {'; '.join(str(v) for v in ethics_risks) if ethics_risks else 'None recorded'}\n"
            f"Strengths: {'; '.join(str(v) for v in ethics_strengths) if ethics_strengths else 'None recorded'}"
        )

    return f"""ALETHEIA LOCAL WITNESS RECEIPT
Receipt type: {receipt.get('receipt_type')}
Receipt version: {receipt.get('receipt_version')}
Generated: {receipt.get('generated_at_utc')}
App version: {receipt.get('app_version')}
Rubric version: {receipt.get('rubric_version')}
Prompt version: {receipt.get('prompt_version')}
Active modules: {', '.join(str(v) for v in active_modules) if active_modules else 'None recorded'}
Module: {receipt.get('module')}
Input status: {receipt.get('input_status')}
Input type: {receipt.get('input_type', receipt.get('input_status'))}
Invisibility Filter applied: {receipt.get('invisibility_filter_applied')}{demo_guard_block}

NOTICE
{receipt.get('notice')}
Dataflow boundary: {receipt.get('dataflow')}

HASHES
Scenario SHA-256: {hashes.get('scenario_sha256')}
Processed scenario SHA-256: {hashes.get('processed_scenario_sha256')}
Document fingerprint SHA-256: {hashes.get('document_fingerprint_sha256')}
Processed document fingerprint SHA-256: {hashes.get('processed_document_fingerprint_sha256')}
Report fingerprint SHA-256: {hashes.get('report_fingerprint_sha256')}
Audit receipt SHA-256: {hashes.get('audit_receipt_sha256')}

AUTHORITY BOUNDARY
Stored locally: {_display_value(boundary.get('stored_locally'))}
Public ledger: {_display_value(boundary.get('public_ledger'))}
Global ID sync: {_display_value(boundary.get('global_id_sync'))}
Central storage: {_display_value(boundary.get('central_storage'))}
Authority claim: {_display_value(boundary.get('authority_claim'))}
Human review required: {_display_value(boundary.get('human_review_required'))}

VERDICT SIGNAL
Protocol-adjusted state: {verdict.get('protocol_adjusted_state')}
Risk: {verdict.get('risk')}
Protocol label: {verdict.get('protocol_label')}

CORE METRICS
Integrity: {_display_value(metrics.get('integrity'))}
Friction: {_display_value(metrics.get('friction'))}
Collapse probability: {_display_value(metrics.get('collapse_probability'))}
Trust friction: {_display_value(metrics.get('trust_friction'))}
Stability: {_display_value(metrics.get('stability'))}
Trust index: {_display_value(metrics.get('trust_index'))}
Alignment: {_display_value(metrics.get('alignment'))}
Ego: {_display_value(metrics.get('ego'))}
Collapse risk: {_display_value(metrics.get('collapse_risk'))}

RAW METRICS BEFORE ETHICS
{_display_raw_metrics_block(receipt.get('raw_metrics_before_ethics'))}

THRESHOLD MAPPING LAYER
{_display_threshold_mapping_layer_block(threshold_mapping)}

SCANNER FEATURES
Power concentration: {_display_value(features.get('power_concentration'))}
Decision transparency: {_display_value(features.get('decision_transparency'))}
Regulatory presence: {_display_value(features.get('regulatory_presence'))}
Anonymity level: {_display_value(features.get('anonymity_level'))}
Capital scale: {_display_value(features.get('capital_scale'))}
Technical complexity: {_display_value(features.get('technical_complexity'))}
Scan mode: {_display_value(features.get('scan_mode'))}

CONTEXTUAL ETHICS DIAGNOSTICS
{ethics_block}

HARD CAPTURE TRACE
{_display_hard_capture_trace_block(ethics.get('hard_capture_trace'))}

COGNITIVE RESILIENCE DIAGNOSTICS
{_display_cognitive_resilience_block(cognitive_resilience)}

ETHICS ADJUSTMENT
{_display_ethics_adjustment_block(ethics_adjustment)}

SILENT OPERATOR REPAIR QUESTIONS
{question_block}

RECOVERY NOTE
{receipt.get('recovery_note')}

MACHINE-READABLE RECEIPT JSON
{json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True)}
"""
