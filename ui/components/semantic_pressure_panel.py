"""Shared Semantic Pressure UI components for ALETHEIA.

Stage 1 modularization: this module extracts the shared semantic-pressure
panel and related row-mapping helpers from app.py without changing runtime
behavior, scoring, routing, or receipt semantics.
"""

from __future__ import annotations

import html

import pandas as pd
import streamlit as st

from core.semantic_pressure_scanner import (
    pressure_code_rows,
    reviewability_guidance_rows,
    scan_semantic_pressure,
)


def _semantic_scan_from_payload(payload):
    """Return a SemanticPressureScan from text, dataclass, or stored dict payload."""
    if payload is None:
        return None
    if hasattr(payload, "to_dict") and hasattr(payload, "state"):
        return payload
    if isinstance(payload, dict):
        # Stored report payloads are dicts; use them directly in the renderer.
        return payload
    if isinstance(payload, str) and payload.strip():
        return scan_semantic_pressure(payload, governance_context=True)
    return None


def _semantic_payload_value(scan, key, default=None):
    if scan is None:
        return default
    if isinstance(scan, dict):
        return scan.get(key, default)
    return getattr(scan, key, default)


def _semantic_payload_notes(scan) -> list[str]:
    notes = _semantic_payload_value(scan, "notes", []) or []
    if isinstance(notes, tuple):
        return list(notes)
    if isinstance(notes, list):
        return [str(note) for note in notes]
    return [str(notes)] if notes else []


def _semantic_payload_hits(scan) -> list[dict]:
    hits = _semantic_payload_value(scan, "proximity_hits", []) or []
    clean = []
    for hit in hits:
        if isinstance(hit, dict):
            clean.append(hit)
        else:
            clean.append({
                "category": getattr(hit, "category", "semantic_hit"),
                "left": getattr(hit, "left", ""),
                "right": getattr(hit, "right", ""),
                "distance": getattr(hit, "distance", ""),
                "excerpt": getattr(hit, "excerpt", ""),
            })
    return clean


def semantic_pressure_summary_message(scan) -> tuple[str, str]:
    """Return (kind, message) for the shared semantic panel."""
    state = str(_semantic_payload_value(scan, "state", "SANCTUARY") or "SANCTUARY").upper()
    fail_closed = bool(_semantic_payload_value(scan, "fail_closed", False))
    mechanism_count = int(_semantic_payload_value(scan, "mechanism_count", 0) or 0)
    hit_count = len(_semantic_payload_hits(scan))
    notes = " ".join(_semantic_payload_notes(scan)).lower()

    if fail_closed:
        return (
            "warning",
            "Fail-closed semantic review: value/governance language is visible, but concrete safeguards are missing or insufficient.",
        )
    if hit_count:
        return (
            "warning",
            "Contextual pressure relationship detected. Review how access, identity, permanence, or obligation terms are connected.",
        )
    if mechanism_count >= 2:
        return (
            "success",
            "Concrete safeguards detected. No strong semantic pressure relationship was detected by this scanner; human review still required.",
        )
    if state == "THRESHOLD" or "claims outweigh" in notes or "rhetoric-to-mechanism" in notes:
        return (
            "warning",
            "Semantic review recommends caution: claims, safeguards, or mechanisms need human review.",
        )
    return (
        "info",
        "No strong semantic pressure relationship detected by this scanner. Human review still required.",
    )



def _semantic_pressure_rows_by_code(codes):
    """Return pressure-code explanation/guidance rows keyed by code for card rendering."""
    code_list = [str(code) for code in (codes or []) if str(code or "").strip()]
    explanation_map = {str(row.get("Code", "")): str(row.get("Plain-English meaning", "")) for row in pressure_code_rows(code_list)}
    guidance_map = {
        str(row.get("Pressure code", "")): (
            str(row.get("Reviewability goal", "")),
            str(row.get("Structural guidance", "")),
        )
        for row in reviewability_guidance_rows(code_list)
    }
    return code_list, explanation_map, guidance_map


def _render_pressure_code_cards(codes) -> None:
    """Render readable pressure-code cards instead of cramped dataframe cells."""
    code_list, explanation_map, guidance_map = _semantic_pressure_rows_by_code(codes)
    if not code_list:
        return

    st.markdown("**Pressure-code matrix**")
    st.caption(
        "Stable diagnostic codes explaining which pressure patterns were detected. "
        "Codes are not verdicts or certifications."
    )
    for idx, code in enumerate(code_list, start=1):
        explanation = explanation_map.get(code, "Review signal requiring human interpretation.")
        goal, guidance = guidance_map.get(
            code,
            ("Make the claim reviewable", "Add evidence basis, limits, appeal, correction, and independent review routes."),
        )
        with st.container(border=True):
            st.markdown(f"**{idx}. `{html.escape(code)}`**")
            st.caption(html.escape(explanation))
            st.markdown(f"**Reviewability goal:** {html.escape(goal)}")
            st.markdown(f"- {html.escape(guidance)}")
    with st.expander("Show pressure-code table", expanded=False):
        st.dataframe(pd.DataFrame(pressure_code_rows(code_list)), use_container_width=True, hide_index=True)


def render_semantic_pressure_panel(
    text_or_scan,
    *,
    source_label: str = "Mirror Check",
    expanded: bool = False,
    panel_key: str | None = None,
) -> None:
    """Shared semantic-pressure diagnostic panel.

    The panel is a subordinate relationship-aware signal. It does not certify,
    approve, reject, enforce, or replace the main module reading.
    """
    semantic_scan = _semantic_scan_from_payload(text_or_scan)
    if semantic_scan is None:
        st.caption("Semantic pressure scan unavailable for this reading.")
        return

    raw_state = str(_semantic_payload_value(semantic_scan, "state", "SANCTUARY") or "SANCTUARY").upper()
    state = raw_state
    risk = str(_semantic_payload_value(semantic_scan, "risk", "Review signal") or "Review signal")
    integrity_adjustment = float(_semantic_payload_value(semantic_scan, "integrity_adjustment", 0.0) or 0.0)
    claim_count = int(_semantic_payload_value(semantic_scan, "claim_count", 0) or 0)
    mechanism_count = int(_semantic_payload_value(semantic_scan, "mechanism_count", 0) or 0)
    ratio = float(_semantic_payload_value(semantic_scan, "claim_to_mechanism_ratio", 0.0) or 0.0)
    modal_count = int(_semantic_payload_value(semantic_scan, "modal_pressure_count", 0) or 0)
    sovereignty_count = int(_semantic_payload_value(semantic_scan, "sovereignty_count", 0) or 0)
    fail_closed = bool(_semantic_payload_value(semantic_scan, "fail_closed", False))
    normalized_text = str(_semantic_payload_value(semantic_scan, "normalized_text", "") or "")
    hits = _semantic_payload_hits(semantic_scan)
    notes = _semantic_payload_notes(semantic_scan)
    pressure_codes = list(_semantic_payload_value(semantic_scan, "pressure_codes", ()) or ())

    # UI semantics: the scanner's internal SANCTUARY value can also mean
    # "no semantic relationship detected." Showing that as SANCTUARY beside an
    # ASYLUM/THRESHOLD main reading creates a false contradiction. When no
    # claims, mechanisms, modal pressure, reversibility, fail-closed flag, hits,
    # or integrity pressure are present, render it as a neutral no-signal state.
    no_semantic_signal = (
        raw_state == "SANCTUARY"
        and claim_count == 0
        and mechanism_count == 0
        and modal_count == 0
        and sovereignty_count == 0
        and not fail_closed
        and not hits
        and abs(integrity_adjustment) < 1e-9
    )
    display_state = "NO SIGNAL" if no_semantic_signal else raw_state
    display_risk = "No semantic relationship detected" if no_semantic_signal else risk
    message_kind, message = semantic_pressure_summary_message(semantic_scan)
    if no_semantic_signal:
        message_kind = "info"
        message = "No semantic pressure relationship detected. This does not lower or override the main module reading."
    # Streamlit requires explicit unique keys for repeated semantic panels.
    # Use the caller-provided panel_key when available, and fall back to a
    # deterministic content hash for older call sites.
    semantic_panel_key = panel_key or hashlib.sha1(
        f"{source_label}|{state}|{risk}|{integrity_adjustment}|{claim_count}|{mechanism_count}|{normalized_text}".encode("utf-8")
    ).hexdigest()[:12]
    semantic_panel_key = re.sub(r"[^A-Za-z0-9_\-]", "_", str(semantic_panel_key))

    state_color = {
        "NO SIGNAL": "#425466",
        "SANCTUARY": "#2f6b3a",
        "THRESHOLD": "#9b6b00",
        "ASYLUM": "#8f1d2c",
    }.get(display_state, "#425466")

    with st.container(border=True):
        st.markdown("#### Semantic pressure signals")
        st.caption(
            f"Subordinate diagnostic for {source_label}. It scans relationships between pressure terms, access terms, soft claims, and concrete mechanisms. It does not decide the reading."
        )
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"<div class='metric-card'><b>Semantic finding</b><br><span style='font-size:1.35rem;color:{state_color};'>{html.escape(display_state)}</span><br><span>{html.escape(display_risk)}</span></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='metric-card'><b>Claims</b><br><span style='font-size:1.35rem;'>{claim_count}</span><br><span>soft/value terms</span></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='metric-card'><b>Mechanisms</b><br><span style='font-size:1.35rem;'>{mechanism_count}</span><br><span>appeal/audit/review etc.</span></div>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<div class='metric-card'><b>Integrity pressure</b><br><span style='font-size:1.35rem;'>{integrity_adjustment:+.3f}</span><br><span>diagnostic only</span></div>", unsafe_allow_html=True)

        if message_kind == "success":
            st.success(message)
        elif message_kind == "warning":
            st.warning(message)
        else:
            st.info(message)

        with st.expander("Show semantic scan details", expanded=expanded):
            st.caption("This is diagnostic machinery. The main module reading remains the primary review output.")
            detail_cols = st.columns(4)
            detail_cols[0].metric("Claim/mechanism ratio", f"{ratio:.2f}")
            detail_cols[1].metric("Modal pressure", str(modal_count))
            detail_cols[2].metric("Reversibility", str(sovereignty_count))
            detail_cols[3].metric("Fail-closed", "YES" if fail_closed else "NO")
            if pressure_codes:
                _render_pressure_code_cards(pressure_codes)
            if notes:
                st.markdown("**Notes**")
                for note in notes:
                    st.markdown(f"- {note}")
            if hasattr(semantic_scan, "to_dict"):
                report_text = format_semantic_pressure_report(semantic_scan)
            else:
                # Reconstruct a compact text block from stored dict values.
                report_text = "\n".join([
                    "Semantic Pressure Scan",
                    "",
                    f"Internal review state: {state}",
                    f"Risk note: {risk}",
                    f"Integrity pressure adjustment: {integrity_adjustment:+.3f}",
                    f"Claim signals: {claim_count}",
                    f"Mechanism signals: {mechanism_count}",
                    f"Claim-to-mechanism ratio: {ratio}",
                    f"Modal pressure signals: {modal_count}",
                    f"Sovereignty / reversibility signals: {sovereignty_count}",
                    f"Fail-closed review: {'YES' if fail_closed else 'NO'}",
                    f"Pressure codes: {', '.join(pressure_codes) if pressure_codes else 'none'}",
                    "",
                    "Notes:",
                    *[f"- {note}" for note in notes],
                    "",
                    "Human review note: This scan is a relationship-aware mirror signal, not proof of intent, certification, or a final decision.",
                ])

            show_debug = st.checkbox(
                "Show developer/debug details",
                value=False,
                key=f"semantic_show_debug_{semantic_panel_key}",
                help="Reveals raw proximity hits, normalized text, and the plain-text scan report. Not needed for normal review.",
            )
            if show_debug:
                st.caption("Raw semantic machinery for calibration and troubleshooting. Normal users can leave this off.")
                if hits:
                    st.markdown("**Contextual proximity hits**")
                    hit_rows = []
                    for hit in hits:
                        hit_rows.append({
                            "Category": hit.get("category"),
                            "Left": hit.get("left"),
                            "Right": hit.get("right"),
                            "Distance": hit.get("distance"),
                            "Excerpt": hit.get("excerpt"),
                        })
                    st.dataframe(pd.DataFrame(hit_rows), use_container_width=True, hide_index=True)
                else:
                    st.caption("No contextual proximity hits recorded for this scan.")

                if normalized_text:
                    with st.expander("Normalized text used for scan", expanded=False):
                        st.text_area(
                            "Normalized scan text",
                            value=normalized_text,
                            height=120,
                            disabled=True,
                            key=f"semantic_normalized_text_{semantic_panel_key}",
                        )

                with st.expander("Plain-text semantic report", expanded=False):
                    st.code(report_text, language="text")


render_sydney_protocol_self_check_gate()

def _semantic_review_strength(scan) -> tuple[int, float, int]:
    """Return a sortable strength tuple for choosing between raw and filtered semantic scans.

    Stress Test may run the Invisibility Filter before the scenario is audited. That is
    correct for reducing actor/name bias in the main reading, but the semantic layer
    must not lose structural signals such as "actor group + world power + secret".
    When both raw and filtered text are available, keep the scan with stronger pressure.
    """
    semantic_scan = _semantic_scan_from_payload(scan)
    if semantic_scan is None:
        return (-1, 0.0, 0)
    state = str(_semantic_payload_value(semantic_scan, "state", "SANCTUARY") or "SANCTUARY").upper()
    state_rank = {"ASYLUM": 3, "THRESHOLD": 2, "SANCTUARY": 1}.get(state, 0)
    adjustment = float(_semantic_payload_value(semantic_scan, "integrity_adjustment", 0.0) or 0.0)
    hit_count = len(_semantic_payload_hits(semantic_scan))
    fail_closed = bool(_semantic_payload_value(semantic_scan, "fail_closed", False))
    modal_count = int(_semantic_payload_value(semantic_scan, "modal_pressure_count", 0) or 0)
    claim_count = int(_semantic_payload_value(semantic_scan, "claim_count", 0) or 0)
    mechanism_count = int(_semantic_payload_value(semantic_scan, "mechanism_count", 0) or 0)
    evidence_count = hit_count + int(fail_closed) + modal_count + claim_count + mechanism_count
    # More negative adjustment is stronger pressure; invert it for sorting.
    return (state_rank, -adjustment, evidence_count)


def choose_stress_semantic_scan(raw_text: str, processed_text: str | None = None):
    """Scan raw and processed Stress Test text and keep the stronger semantic pressure signal.

    The main Stress Test may use processed/decoupled text, but the semantic diagnostic
    should preserve capture/opacity wording from the raw user scenario when that wording
    carries the relationship signal.
    """
    raw = str(raw_text or "").strip()
    processed = str(processed_text or "").strip()
    scans = []
    if raw:
        scans.append(scan_semantic_pressure(raw, governance_context=True))
    if processed and processed != raw:
        scans.append(scan_semantic_pressure(processed, governance_context=True))
    if not scans:
        return None
    return sorted(scans, key=_semantic_review_strength, reverse=True)[0]


def choose_strongest_semantic_scan(*payloads):
    """Choose the strongest semantic pressure scan from scans or text payloads.

    Streamlit can keep a previous semantic panel in session state after a user
    changes or reruns Stress Test. This helper prevents a stale SANCTUARY/NO SIGNAL
    scan from overriding a stronger current raw-text signal such as an opaque
    capture-power claim.
    """
    scans = []
    for payload in payloads:
        if payload is None:
            continue
        scan = _semantic_scan_from_payload(payload)
        if scan is not None:
            scans.append(scan)
    if not scans:
        return None
    return sorted(scans, key=_semantic_review_strength, reverse=True)[0]


def semantic_stress_trigger_rows(scan) -> list[dict]:
    """Map semantic pressure signals to Stress Test stress triggers and repair questions.

    This is a subordinate translation layer. It does not change Stress Test metrics
    or the internal taxonomy label; it only turns language relationships into
    human-review questions.
    """
    if scan is None:
        return []
    hits = _semantic_payload_hits(scan)
    notes = _semantic_payload_notes(scan)
    note_blob = " ".join(notes).lower()
    rows: list[dict] = []

    categories = {str(hit.get("category", "")).lower() for hit in hits if isinstance(hit, dict)}
    if "identity_gated_access" in categories or any("identity-gated" in n.lower() for n in notes):
        rows.append({
            "Semantic trigger": "Identity-gated access",
            "Stress implication": "Access may become coercive when basic services, benefits, or participation depend on verification.",
            "Repair question": "What fallback, appeal, manual review, or non-exclusion path exists for people who cannot verify?",
        })
    if "grip_near_access" in categories or any("grip" in n.lower() and "access" in n.lower() for n in notes):
        rows.append({
            "Semantic trigger": "Grip language near access",
            "Stress implication": "Conditional access may create dependency pressure or hidden coercion under crisis conditions.",
            "Repair question": "Can access be maintained while the dispute, verification failure, or compliance issue is reviewed?",
        })
    if bool(_semantic_payload_value(scan, "fail_closed", False)) or "rhetoric-to-mechanism" in note_blob:
        rows.append({
            "Semantic trigger": "Claims without concrete mechanisms",
            "Stress implication": "Ethical or safety language may hide weak operational safeguards under pressure.",
            "Repair question": "Which audit, appeal, revocation, time-limit, fallback, or independent-review mechanism makes the claim testable?",
        })
    modal_count = int(_semantic_payload_value(scan, "modal_pressure_count", 0) or 0)
    sovereignty_count = int(_semantic_payload_value(scan, "sovereignty_count", 0) or 0)
    if modal_count > sovereignty_count:
        rows.append({
            "Semantic trigger": "Obligation/permanence outweighs reversibility",
            "Stress implication": "Mandatory or permanent language can collapse appeal, exit, and correction paths.",
            "Repair question": "Where are sunset clauses, appeal windows, reversal paths, and human exceptions defined?",
        })
    mechanism_count = int(_semantic_payload_value(scan, "mechanism_count", 0) or 0)
    if mechanism_count >= 2 and not rows:
        rows.append({
            "Semantic trigger": "Concrete safeguards visible",
            "Stress implication": "Appeal, audit, review, time-limit, or revocation language may reduce stress if operationally real.",
            "Repair question": "Who can use the safeguard, how fast does it work, and who audits whether it actually functions?",
        })
    return rows


def render_semantic_stress_triggers(scan, *, expanded: bool = False) -> None:
    """Render semantic-derived stress triggers for Stress Test."""
    semantic_scan = _semantic_scan_from_payload(scan)
    if semantic_scan is None:
        return
    rows = semantic_stress_trigger_rows(semantic_scan)
    with st.expander("Semantic stress triggers — subordinate to Stress Test", expanded=expanded):
        st.caption(
            "Relationship-aware language signals translated into stress triggers and repair questions. "
            "This panel does not change Stress Test metrics or decide the result."
        )
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.info("No additional semantic stress trigger was detected beyond the main Stress Test reading.")
        render_semantic_pressure_panel(semantic_scan, source_label="Stress Test", expanded=False, panel_key="stress_test_semantic_pressure")


def semantic_evidence_implication_rows(scan) -> list[dict]:
    """Map semantic pressure signals to Evidence Lab evidence implications."""
    if scan is None:
        return []
    hits = _semantic_payload_hits(scan)
    notes = _semantic_payload_notes(scan)
    note_blob = " ".join(notes).lower()
    rows: list[dict] = []
    categories = {str(hit.get("category", "")).lower() for hit in hits if isinstance(hit, dict)}
    claim_count = int(_semantic_payload_value(scan, "claim_count", 0) or 0)
    mechanism_count = int(_semantic_payload_value(scan, "mechanism_count", 0) or 0)

    if claim_count > 0 and mechanism_count == 0:
        rows.append({
            "Semantic finding": f"{claim_count} soft/value claim(s), no concrete mechanism detected",
            "Evidence implication": "Claims need source support and operational safeguards before they can carry governance weight.",
            "Human review question": "What public, relevant, reviewable evidence and safeguard structure supports each claim?",
        })
    if bool(_semantic_payload_value(scan, "fail_closed", False)) or "rhetoric-to-mechanism" in note_blob:
        rows.append({
            "Semantic finding": "Rhetoric-to-mechanism gap",
            "Evidence implication": "Ethical language is not enough; Evidence Lab should look for audit trails, appeal records, review windows, and independent checks.",
            "Human review question": "Which visible mechanism makes the stated value enforceable without becoming coercive?",
        })
    if "identity_gated_access" in categories or any("identity-gated" in n.lower() for n in notes):
        rows.append({
            "Semantic finding": "Identity-gated access",
            "Evidence implication": "Requires evidence of exclusion rates, false rejection/acceptance, fallback access, appeal access, and privacy safeguards.",
            "Human review question": "What data shows who is excluded, how errors are repaired, and whether basic access remains available?",
        })
    if "grip_near_access" in categories:
        rows.append({
            "Semantic finding": "Grip language near access/basic-service terms",
            "Evidence implication": "Requires proof that conditionality is bounded, proportionate, reviewable, and non-punitive.",
            "Human review question": "What evidence shows access conditions do not become hidden coercion?",
        })
    modal_count = int(_semantic_payload_value(scan, "modal_pressure_count", 0) or 0)
    sovereignty_count = int(_semantic_payload_value(scan, "sovereignty_count", 0) or 0)
    if modal_count > sovereignty_count:
        rows.append({
            "Semantic finding": "Mandatory/permanent language exceeds reversibility language",
            "Evidence implication": "Requires evidence of sunset clauses, appeal windows, reversal procedures, and exception handling.",
            "Human review question": "Where is the proof that enforcement can be reversed or corrected?",
        })
    if mechanism_count >= 2 and not rows:
        rows.append({
            "Semantic finding": f"{mechanism_count} concrete safeguard signal(s) detected",
            "Evidence implication": "Safeguards are visible in language; Evidence Lab should verify whether they exist in practice and are accessible.",
            "Human review question": "Are the appeal/audit/review mechanisms real, independent, time-bounded, and usable by affected people?",
        })
    return rows


def render_semantic_evidence_check(text: str, *, expanded_details: bool = False) -> None:
    """Render a claim/mechanism evidence check for Evidence Lab."""
    if not str(text or "").strip():
        st.info("Paste a claim or policy sentence to inspect whether value claims have visible evidence/mechanism support.")
        return
    scan = scan_semantic_pressure(text, governance_context=True)
    rows = semantic_evidence_implication_rows(scan)
    render_semantic_pressure_panel(scan, source_label="Evidence Lab", expanded=expanded_details, panel_key="evidence_lab_semantic_claim_mechanism")
    if rows:
        st.markdown("##### Evidence implications")
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No special semantic evidence implication was detected beyond ordinary source review. Human review still required.")


def semantic_world_lens_flag_rows(scan) -> list[dict]:
    """Translate semantic terms into regional interpretation flags for World Lens.

    This is a lens-selection aid only. It does not change World Lens evidence,
    country-year scoring, receipts, or taxonomy labels.
    """
    if scan is None:
        return []
    normalized_text = str(_semantic_payload_value(scan, "normalized_text", "") or "").lower()
    notes_blob = " ".join(_semantic_payload_notes(scan)).lower()
    hits = _semantic_payload_hits(scan)
    categories = {str(hit.get("category", "")).lower() for hit in hits if isinstance(hit, dict)}
    rows: list[dict] = []

    def add(flag: str, why: str, regional_question: str) -> None:
        if not any(row.get("Flag") == flag for row in rows):
            rows.append({
                "Flag": flag,
                "Why it matters across regions": why,
                "Human-review question": regional_question,
            })

    if "identity_gated_access" in categories or "identity" in normalized_text or "verification" in normalized_text:
        add(
            "Identity / verification language",
            "May read as safety infrastructure in one context and surveillance or exclusion pressure in another.",
            "Who cannot verify, who controls the identity layer, and what fallback exists outside the verification path?",
        )
    if "access" in normalized_text or "benefit" in normalized_text or "service" in normalized_text or "basic" in notes_blob:
        add(
            "Access / basic-service language",
            "Access conditions can affect rights, welfare, movement, services, or participation differently across legal and institutional contexts.",
            "Is access preserved during disputes, errors, documentation gaps, or political conflict?",
        )
    if any(term in normalized_text for term in ["harmony", "public trust", "safety", "dignity", "inclusion", "protects"]):
        add(
            "Soft legitimacy claims",
            "Terms like harmony, public trust, safety, dignity, and inclusion can signal protection, but can also mask coercion if mechanisms are absent.",
            "Which local safeguards make the claim reviewable rather than merely persuasive?",
        )
    if any(term in normalized_text for term in ["compliance", "non-compliance", "must", "mandatory", "required", "permanent", "revoked"]):
        add(
            "Compliance / permanence language",
            "Enforcement language may be read as legal order, administrative necessity, or coercive discipline depending on local appeal and rights context.",
            "Where are sunset clauses, appeal windows, independent review, and reversal paths defined?",
        )
    mechanism_count = int(_semantic_payload_value(scan, "mechanism_count", 0) or 0)
    if mechanism_count >= 2:
        add(
            "Visible safeguards",
            "Appeal, audit, revocation, review, or time-limit language may reduce regional interpretation risk if those safeguards are real and accessible.",
            "Are these safeguards independent, usable by affected people, and trusted in the selected regional context?",
        )
    if not rows:
        add(
            "No strong semantic flags",
            "This scanner did not find major language flags, but World Lens context still requires human interpretation.",
            "What local historical, legal, or institutional context could change how this language is understood?",
        )
    return rows


def render_world_lens_semantic_flags(text: str, *, expanded_details: bool = False) -> None:
    """Render semantic terms as regional interpretation flags in World Lens."""
    if not str(text or "").strip():
        st.info("Add an optional context note to inspect semantic terms that may need regional interpretation.")
        return
    scan = scan_semantic_pressure(text, governance_context=True)
    rows = semantic_world_lens_flag_rows(scan)
    st.caption(
        "S3 lens aid: semantic terms are treated as regional interpretation flags only. They do not rescore World Lens evidence or receipts."
    )
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    render_semantic_pressure_panel(
        scan,
        source_label="World Lens context note",
        expanded=expanded_details,
        panel_key="world_lens_semantic_regional_flags",
    )
