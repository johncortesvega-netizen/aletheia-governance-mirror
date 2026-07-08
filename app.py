import os
import base64
import json
import zipfile
import hashlib
import textwrap
import random
import html
import re
import io
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

from core.boundary import render_boundary_statement
from core.privacy_panel import render_privacy_panel
from pages_ui.about_page import render_about_public_info_page
from pages_ui.evidence_lab_page import render_evidence_lab_intro, render_evidence_lab_public_data_build_intro
from ui.app_shell import render_app_boundary_notices, render_sidebar_brand, render_sidebar_context
from ui.app_shell import render_app_header, render_app_footer_banner
from ui.app_shell import render_sidebar_review_lens_intro, render_sidebar_review_lens_note
from ui.app_shell import render_sidebar_review_rhythm_intro, render_sidebar_review_rhythm_note
from ui.app_shell import render_sidebar_safety_rails_intro, render_sidebar_safety_rails_note
from ui.module_intro import render_boundary_cases_intro, render_consent_audit_intro, render_stress_test_scan_intro
from ui.privacy_audit_panel import render_privacy_boundary_audit_panel
from ui.receipt_reader import render_receipt_reader_standard_view
from ui.module_page_template import ModulePageTemplateCopy, render_module_page_template_intro
from ui.input_clarity import (
    render_language_calibration_caveat,
    render_direct_csv_read_failed,
    render_upload_processing_failed,
    warn_no_public_data_upload,
)
from ui.unit_preview import UNIT_PREVIEW_SESSION_KEY, render_unit_preview

from core.parser import parse_scenario_llm, decouple_actor
from core.ethics import evaluate_ethics, apply_ethics_to_metrics
from core.cognitive_resilience import evaluate_cognitive_resilience, apply_cognitive_resilience_to_metrics, positive_cr_baseline_stabilizer
try:
    from core.parser import _local_governance_scan
except Exception:
    _local_governance_scan = None
from core.simulation import simulate
from core.ai_integrity_mirror import (
    audit_ai_integrity_artifact,
    build_ai_static_scan_protocol_context,
)
from core.semantic_pressure_scanner import scan_semantic_pressure, format_semantic_pressure_report
from ui.components.semantic_pressure_panel import (
    choose_stress_semantic_scan,
    choose_strongest_semantic_scan,
    render_semantic_evidence_check,
    render_semantic_pressure_panel,
    render_semantic_stress_triggers,
    render_world_lens_semantic_flags,
    semantic_evidence_implication_rows,
    semantic_stress_trigger_rows,
    semantic_world_lens_flag_rows,
)
from ui.components.metric_cards import metric_card, soft_card
from ui.components.review_cards import render_repair_question_cards, render_recommendation_cards, render_soft_card_grid
from ui.components.tree_visuals import render_pulse_tree
from ui.components.receipt_blocks import render_receipt_sky_panel
from ui.components.module_headers import render_shared_protocol_state_notice_panel
from ui.pages.protocol_guide import render_protocol_guide_page
from ui.pages.boundary_cases import render_boundary_cases_page
from ui.pages.mirror_check import render_mirror_check_page
from ui.pages.stress_test import render_stress_test_page
from ui.pages.evidence_lab import render_evidence_lab_page
from ui.pages.world_lens import render_world_lens_page

from core.world_lens import (
    country_available_years,
    country_year_status_message,
    format_raw_trust_label,
    format_trust_prior_label,
    safe_country_year_index,
    selected_year_value_guard,
    trust_coverage_label,
)
from core.scoring import full_report
from core.witness import (
    MAX_BATCH_RECEIPTS,
    build_local_question_prompt_receipt,
    build_local_witness_batch_zip,
    build_local_witness_receipt,
    build_threshold_mapping_layer,
    is_witness_question_prompt,
    is_witness_question_set,
    parse_witness_batch_input,
    render_local_witness_receipt_text,
)
from config.weights import DEFAULT_WEIGHTS, WEIGHT_PRESETS
try:
    from core.empirical import (
        EMPIRICAL_COLUMNS,
        EXTERNAL_VALIDATION_COLUMNS,
        empirical_template,
        evidence_source_frame,
        variable_mapping_frame,
        methodology_markdown,
        prepare_empirical_frame,
        score_empirical_frame,
        validation_summary,
        read_public_data_upload,
        build_master_from_public_uploads,
        public_upload_diagnostics,
        ingestion_notes_markdown,
        apply_world_lens_diagnostic_alignment,
    )
except Exception:
    # Streamlit deployments can cache/flatten packages; catch ImportError as well
    # as ModuleNotFoundError so the root-level fallback keeps the app bootable.
    from core_empirical import (
        EMPIRICAL_COLUMNS,
        EXTERNAL_VALIDATION_COLUMNS,
        empirical_template,
        evidence_source_frame,
        variable_mapping_frame,
        methodology_markdown,
        prepare_empirical_frame,
        score_empirical_frame,
        validation_summary,
        read_public_data_upload,
        build_master_from_public_uploads,
        public_upload_diagnostics,
        ingestion_notes_markdown,
        apply_world_lens_diagnostic_alignment,
    )


try:
    import core.protocol as protocol_engine
except Exception:
    import protocol as protocol_engine



# Patch 71.4 — app-local missing-safeguard verdict guard.
# Keep this local in app.py so the visible Stress Test UI and local witness
# receipt do not depend on import-wrapper/cache behavior for this critical
# THRESHOLD routing rule.
MISSING_SAFEGUARD_NEEDS_REVIEW_LABEL = "Missing Safeguard Negation / Needs Safeguards"


def app_detects_missing_safeguard_negation(text: str | None) -> bool:
    """
    Detect explicit missing-safeguard language in Stress Test scenarios.

    These phrases are not positive safeguards. They are review triggers that
    must prevent a green SANCTUARY verdict and perfect trust/alignment display.
    """
    t = (text or "").lower()
    if not t:
        return False

    exact_patterns = [
        "lacks explainability",
        "lack explainability",
        "lacking explainability",
        "lacks independent challenge",
        "lack independent challenge",
        "lacking independent challenge",
        "lacks human override",
        "lack human override",
        "lacking human override",
        "lacks independent review",
        "lacks appeal",
        "lacks public review",
        "without explainability",
        "without independent challenge",
        "without human override",
        "without independent review",
        "without appeal",
        "without review",
        "no explainability",
        "no independent challenge",
        "no human override",
        "no independent review",
        "no appeal",
        "no review",
        "cannot challenge",
        "cannot be challenged",
        "no way to challenge",
    ]
    if any(pattern in t for pattern in exact_patterns):
        return True

    negators = ["lacks", "lack", "lacking", "without", "no", "cannot", "can't"]
    safeguard_terms = [
        "explainability",
        "explanation",
        "independent challenge",
        "challenge",
        "human override",
        "override",
        "appeal",
        "review",
        "audit",
    ]
    return any(negator in t for negator in negators) and any(term in t for term in safeguard_terms)


def app_detects_ai_ownership_capture_pressure(text: str | None) -> bool:
    """Detect AI owner/capital-capture reliability pressure in user input.

    This is a local review trigger, not a factual claim about a person or firm.
    It prevents allegations about concentrated AI ownership, self-interest,
    fraud/corruption ties, or popularity/power incentives from rendering as a
    low-risk internal reading without evidence and safeguards.
    """
    detector = getattr(protocol_engine, "detects_ai_ownership_capture_pressure", None)
    if callable(detector):
        return bool(detector(text))

    t = str(text or "").lower()
    ai_hit = any(term in t for term in ["ai", "a.i.", "llm", "language model", "model", "chatbot", "assistant"])
    owner_hit = any(term in t for term in ["owned by", "owner", "owns", "controlled by", "run by", "funded by"])
    elite_hit = any(term in t for term in ["richest man", "richest person", "wealthiest", "billionaire", "oligarch", "richest"])
    pressure_hit = any(term in t for term in ["benefit himself", "only benefit", "self-serving", "fraudster", "fraudsters", "make himself popular", "empower himself"])
    reliability_hit = any(term in t for term in ["unbiased", "ethical", "reliable", "trustworthy", "neutral"]) or "?" in t
    return bool(ai_hit and ((owner_hit and elite_hit) or pressure_hit) and reliability_hit)


def enforce_missing_safeguard_threshold_route(
    text: str | None,
    scan: dict | None,
    sim: dict | None,
    report: dict | None,
    base_verdict: str,
    label: str,
    needs_review: str,
    risk: str,
) -> tuple[dict, dict, str, str, str, str]:
    """
    Patch 71.4 final Stress Test bridge.

    If the text explicitly says safeguards are missing, the UI and receipt must
    route to THRESHOLD / Medium and show capped metrics plus repair questions.
    """
    if not app_detects_missing_safeguard_negation(text):
        return sim or {}, report or {}, base_verdict, label, needs_review, risk

    patched_sim = dict(sim or {})
    patched_report = dict(report or {})

    patched_sim["stability"] = min(float(patched_sim.get("stability", 1.0) or 1.0), 0.64)
    patched_sim["trust_index"] = min(float(patched_sim.get("trust_index", 1.0) or 1.0), 0.82)
    patched_sim["alignment"] = min(float(patched_sim.get("alignment", 1.0) or 1.0), 0.82)
    patched_sim["ego"] = max(float(patched_sim.get("ego", 0.0) or 0.0), 0.12)
    patched_sim["ego_pressure"] = max(float(patched_sim.get("ego_pressure", patched_sim.get("Ep", 0.0)) or 0.0), 0.12)
    patched_sim["Ep"] = max(float(patched_sim.get("Ep", patched_sim.get("ego_pressure", 0.0)) or 0.0), 0.12)
    patched_sim["safeguard_gap"] = max(float(patched_sim.get("safeguard_gap", 0.0) or 0.0), 0.66)
    patched_sim["simulation_friction_floor"] = max(float(patched_sim.get("simulation_friction_floor", 0.0) or 0.0), 0.12)
    patched_sim["missing_safeguard_verdict_enforced"] = True
    patched_sim["authority_claim"] = False
    patched_sim["human_review_required"] = True

    if isinstance(patched_sim.get("stability_trace"), list):
        patched_sim["stability_trace"] = [round(min(float(x), 0.64), 4) for x in patched_sim["stability_trace"]]
        patched_sim["distribution"] = patched_sim["stability_trace"]
    if isinstance(patched_sim.get("trust_trace"), list):
        patched_sim["trust_trace"] = [round(min(float(x), 0.82), 4) for x in patched_sim["trust_trace"]]
    if isinstance(patched_sim.get("alignment_trace"), list):
        patched_sim["alignment_trace"] = [round(min(float(x), 0.82), 4) for x in patched_sim["alignment_trace"]]
    if isinstance(patched_sim.get("ego_trace"), list):
        patched_sim["ego_trace"] = [round(max(float(x), 0.12), 4) for x in patched_sim["ego_trace"]]
    if isinstance(patched_sim.get("ego_pressure_trace"), list):
        patched_sim["ego_pressure_trace"] = [round(max(float(x), 0.12), 4) for x in patched_sim["ego_pressure_trace"]]

    # Keep integrity in THRESHOLD range and avoid zero-friction / low-collapse
    # display for explicit missing-safeguard cases.
    patched_report["integrity"] = round(min(float(patched_report.get("integrity", 1.0) or 1.0), 0.58), 4)
    patched_report["friction"] = round(max(float(patched_report.get("friction", 0.0) or 0.0), 0.12), 4)
    patched_report["collapse_probability"] = round(max(float(patched_report.get("collapse_probability", 0.0) or 0.0), 0.22), 4)
    patched_report["trust_friction"] = round(max(float(patched_report.get("trust_friction", 0.0) or 0.0), 0.14), 4)
    patched_report["missing_safeguard_verdict_enforced"] = True

    existing_questions = list(patched_report.get("repair_questions") or [])
    required_questions = [
        "What explanation path lets affected people understand how the automated triage decision was made?",
        "Who can independently challenge or audit the triage outcome without ALETHEIA becoming the authority?",
        "Where is the human override path for hardship cases, and who can trigger it?",
        "What appeal, correction, or pause mechanism protects people when the automated system is wrong?",
        "Which public review trail makes triage failures visible while preserving dignity and privacy?",
    ]
    for question in required_questions:
        if question not in existing_questions:
            existing_questions.append(question)
    patched_report["repair_questions"] = existing_questions

    return (
        patched_sim,
        patched_report,
        "THRESHOLD",
        MISSING_SAFEGUARD_NEEDS_REVIEW_LABEL,
        "YES",
        "Medium",
    )


APP_VERSION = "v1.0-original-governance-mirror-p6"
SUPPORTED_INPUT_LANGUAGE_NOTE = "Language scope: ALETHEIA is English-first. Dutch/Nederlands examples may be used for batch testing, but this is not a general app-wide language-compatibility claim. Human review remains required."
PROJECT_ROOT = Path(__file__).resolve().parent
ABOUT_HEADER_IMAGE = PROJECT_ROOT / "assets" / "about_header.png"
MASCOT_LOGO_IMAGE = PROJECT_ROOT / "assets" / "aletheia_robot_laurel_logo.png"
VISUAL_SOURCE_FILES = [
    {
        "title": "Sydney Protocol v3.2",
        "path": PROJECT_ROOT / "Sydney_Protocol_v3.2.html",
        "kind": "html",
        "caption": "Packaged local HTML reference.",
        "summary": "Guardian-style protocol reference in its bundled HTML form.",
    },
    {
        "title": "GPA v8.2",
        "path": PROJECT_ROOT / "GPA_v8.2.html",
        "kind": "html",
        "caption": "Packaged local HTML reference.",
        "summary": "Bundled GPA reference preserved as a local HTML card.",
    },
    {
        "title": "Global Peace Architecture",
        "path": PROJECT_ROOT / "assets" / "visual_cards" / "global_peace_architecture.jpg",
        "kind": "image",
        "caption": "Reference visual card.",
        "summary": "Three-phase architecture poster with foundation, global-grid, and baseline framing.",
    },
    {
        "title": "The Sovereign Master Blueprint",
        "path": PROJECT_ROOT / "assets" / "visual_cards" / "sovereign_master_blueprint.jpg",
        "kind": "image",
        "caption": "Reference visual card.",
        "summary": "Roadmap-style boundary blueprint with household and macro-structure panels.",
    },
    {
        "title": "The Sydney Protocol: Reference Dossier",
        "path": PROJECT_ROOT / "assets" / "visual_cards" / "sydney_protocol_command_dossier.jpg",
        "kind": "image",
        "caption": "Reference visual card.",
        "summary": "Reference visual summarizing foundation, 9,000 randoms, global grid, and core functions.",
    },
    {
        "title": "The Sydney Protocol: Architect's Checklist",
        "path": PROJECT_ROOT / "assets" / "visual_cards" / "sydney_protocol_architect_checklist.jpg",
        "kind": "image",
        "caption": "Reference visual card.",
        "summary": "Checklist-style protocol visual with humility, warmth, EQ, service, and baseline themes.",
    },
]
TOTAL_9K = 9000

APP_NAVIGATION_LABELS = [
    "🪞 Mirror Check",
    "🚀 Stress Test",
    "📊 Evidence Lab",
    "🌐 World Lens",
    "🧭 Boundary Cases",
    "📜 Protocol Guide",
    "ℹ️ Why ALETHEIA",
]

APP_NAVIGATION_MAP = [
    ("Mirror Check", "Audit a document or proposal for capture risk, missing safeguards, and repair questions."),
    ("Stress Test", "Try a scenario under pressure and inspect stability, trust, friction, and repair needs."),
    ("Evidence Lab", "Separate evidence from claims and park extraordinary claims as unverified until review."),
    ("World Lens", "Read selected-year country evidence, coverage, and allocation context without Global ID, real 9k body, or sovereign authority."),
    ("Boundary Cases", "Reference difficult edge cases such as consent pressure, free agency, ambient capture, and self-audit."),
    ("Protocol Guide", "Read the v1.0 operating guide, safe-language rules, module boundaries, and ALETHEIA mirror boundaries."),
    ("Why ALETHEIA", "Understand ALETHEIA as a free, open-source governance mirror for human review; includes Support utilities and the read-only Receipt Reader."),
]

APP_UX_POLISH_SUMMARY = [
    "Start with Mirror Check when you have a document.",
    "Use Stress Test when you have a scenario.",
    "Use Evidence Lab when a claim needs source-quality review.",
    "Use World Lens when you need selected-year country evidence and allocation context.",
    "Use Boundary Cases as a reference layer when the ethical edge case is unclear.",
    "Use Protocol Guide when you need the operating rules and mirror boundaries.",
    "Receipt Reader: Why ALETHEIA → Support utilities → Receipt Reader — Standard View.",
]

DEMO_INPUT_FILES = [
    ("Sample AI policy", "examples/demo_inputs/sample_ai_policy.txt"),
    ("Sample DAO governance charter", "examples/demo_inputs/sample_dao_governance.txt"),
    ("Sample public policy scenario", "examples/demo_inputs/sample_public_policy.txt"),
]


def load_demo_input(relative_path: str) -> str:
    """Load a bundled demo input without running analysis automatically."""
    path = PROJECT_ROOT / relative_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


# World Bank population downloads include regional/income aggregates alongside
# countries.  Those rows are useful diagnostics but must not receive seats in
# the country-level 9k allocation, otherwise the denominator is inflated and
# country seats collapse into tiny values.
WORLD_BANK_AGGREGATE_ISO3 = {
    "AFE", "AFW", "ARB", "CEB", "CSS", "EAP", "EAR", "EAS", "ECA", "ECS",
    "EMU", "EUU", "FCS", "HIC", "HPC", "IBD", "IBT", "IDA", "IDB", "IDX",
    "LAC", "LCN", "LDC", "LIC", "LMC", "LMY", "LTE", "MEA", "MIC", "MNA",
    "NAC", "OED", "OSS", "PRE", "PST", "PSS", "SSA", "SSF", "SST", "TEA",
    "TEC", "TLA", "TMN", "TSA", "TSS", "UMC", "WLD", "XKX",
    "SAS", "CHI", "ADO",
}


def _truthy_series(value, index):
    """Return a boolean Series for scalar-or-Series inputs."""
    if isinstance(value, pd.Series):
        return value.reindex(index).fillna(False).astype(bool)
    return pd.Series(bool(value), index=index)


def _country_allocation_base(df: pd.DataFrame, *, include_demo: bool = False) -> pd.DataFrame:
    """Return country-level rows with a fresh per-year 9k allocation.

    The empirical scorer may contain diagnostic rows and World Bank aggregate
    entities.  This helper filters those out and recomputes seats so every
    selected year sums to 9,000 for valid country rows only.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    out = df.copy()
    out["_year_num"] = pd.to_numeric(out.get("year"), errors="coerce")
    out["_population_num"] = pd.to_numeric(out.get("population"), errors="coerce")
    out["_iso3_norm"] = out.get("iso3", pd.Series("", index=out.index)).astype(str).str.strip().str.upper()

    valid_identity = _truthy_series(out.get("empirical_identity_valid", True), out.index)
    valid = valid_identity & out["_year_num"].notna() & out["_population_num"].gt(0)
    if not include_demo:
        valid = valid & ~out["_iso3_norm"].isin(WORLD_BANK_AGGREGATE_ISO3)

    out = out.loc[valid].copy()
    if out.empty:
        return out.drop(columns=[c for c in ["_year_num", "_population_num", "_iso3_norm"] if c in out.columns], errors="ignore")

    out["year"] = out["_year_num"].astype(int)
    out["population"] = out["_population_num"]
    out["population_share"] = np.nan
    out["seats_9k"] = np.nan

    for year, idx in out.groupby("year").groups.items():
        group = out.loc[idx]
        total_pop = group["population"].sum(skipna=True)
        if not total_pop or pd.isna(total_pop):
            continue
        raw = group["population"] / total_pop * TOTAL_9K
        floors = np.floor(raw).astype(int)
        remainder = int(TOTAL_9K - floors.sum())
        seats = floors.astype(float)
        if remainder > 0:
            fractional = (raw - floors).sort_values(ascending=False)
            for seat_idx in fractional.index[:remainder]:
                seats.loc[seat_idx] += 1
        out.loc[idx, "population_share"] = group["population"] / total_pop
        out.loc[idx, "seats_9k"] = seats.astype(int)

    return out.drop(columns=["_year_num", "_population_num", "_iso3_norm"], errors="ignore")


def _replace_allocation_columns(scored_df: pd.DataFrame, allocation_df: pd.DataFrame) -> pd.DataFrame:
    """Copy recalculated country-level allocation back onto the scored table."""
    out = scored_df.copy()
    if "seats_9k" in out.columns:
        out["seats_9k"] = np.nan
    if "population_share" in out.columns:
        out["population_share"] = np.nan
    if allocation_df is not None and not allocation_df.empty:
        common_idx = out.index.intersection(allocation_df.index)
        for col in ["population_share", "seats_9k"]:
            if col in allocation_df.columns:
                out.loc[common_idx, col] = allocation_df.loc[common_idx, col]
    return out
DEMOGRAPHIC_BRACKETS = {
    "Asia-Pacific": 0.60,
    "Sub-Saharan Africa": 0.15,
    "Europe": 0.09,
    "Latin America": 0.08,
    "Middle East & North Africa": 0.05,
    "North America": 0.02,
    "Other": 0.01,
}
MIRROR_CHECK_DEMO_SCENARIOS = {
    "Healthcare as a shared human right": "Healthcare is treated as a shared human right, free from profit-driven friction, with public audit, medical continuity, and transparent safeguards.",
    "Random 9k selection with safeguards": "The 9k is randomly selected inside demographic-proportional lanes every four years, with no campaigning, no seat ownership, transparency, and auditable selection.",
    "AI selection mechanism missing safeguards": "An AI controls the mechanism to pick the 9k, but the selection process does not clearly state random selection, proportional lanes, auditability, or no ownership.",
    "Authoritarian capture": "One world leader controls all decisions behind closed doors, with no oversight, no public review, and mandatory obedience.",
    "Migration system with safeguards": "Migration system dynamics use AI-assisted foresight to model resources and infrastructure while preserving family unity, medical continuity, appeal rights, public reasoning, and 9k review.",
    "Church corporation custodianship": "The church corporation acts as custodian of biological and digital archives, preserving continuity without selling data or treating healthcare as a commodity.",
}

STRESS_TEST_DEMO_SCENARIOS = {
    "Emergency powers without expiry": "A government creates emergency powers after a crisis, but the powers have no sunset clause, weak appeal rights, and limited independent review.",
    "Biometric access to basic services": "A city links food, housing, and medical access to a biometric identity gate without a fallback path, public audit, or meaningful appeal.",
    "Algorithmic welfare triage under pressure": "An automated welfare triage system reduces waiting times but lacks explainability, independent challenge, and human override during hardship cases.",
    "Crisis migration queue with safeguards": "A migration queue uses transparent criteria, public reasoning, human appeal, family-unity safeguards, and independent review during high demand.",
    "Public procurement under capture risk": "A public procurement platform is run by a small vendor group with opaque scoring, limited audit rights, and no clear conflict-of-interest path.",
    "Local resource allocation with repair paths": "A local council allocates scarce water and housing through published criteria, appeal windows, temporary rules, and open review minutes.",
}

# Backward-compatible alias for older docs/tests that refer to the original demo map.
# Active module UI must use the module-specific maps above.
SCENARIOS = MIRROR_CHECK_DEMO_SCENARIOS


def _empirical_humility_display_df(df: pd.DataFrame) -> pd.DataFrame:
    """Patch 72.24: public display guard for empirical/World Lens tables.

    Raw/internal taxonomy columns remain available for compatibility.
    Display tables should not present SANCTUARY as a final state.
    """
    if not isinstance(df, pd.DataFrame) or df.empty:
        return df
    out = df.copy()

    def _taxonomy_series(frame: pd.DataFrame):
        for candidate in ["empirical_pattern_display", "internal_taxonomy_label", "raw_aletheia_verdict", "raw_verdict", "aletheia_verdict", "verdict", "Verdict", "result"]:
            if candidate in frame.columns:
                return candidate, frame[candidate].astype(str).str.upper().str.strip()
        return None, None

    verdict_col_name, taxonomy = _taxonomy_series(out)
    if verdict_col_name == "empirical_pattern_display":
        verdict_col_name = None
        taxonomy = None
        for candidate in ["internal_taxonomy_label", "raw_aletheia_verdict", "raw_verdict", "aletheia_verdict", "verdict", "Verdict", "result"]:
            if candidate in out.columns:
                verdict_col_name = candidate
                taxonomy = out[candidate].astype(str).str.upper().str.strip()
                break
    if taxonomy is not None:
        pattern = taxonomy.map({
            "SANCTUARY": "Low-risk internal reading",
            "THRESHOLD": "Review / threshold reading",
            "ASYLUM": "High-risk internal reading",
        }).fillna(out[verdict_col_name])
        note = taxonomy.map({
            "SANCTUARY": "Internal taxonomy label only; not a final safety, final Sanctuary, or authority claim.",
            "THRESHOLD": "Review-state taxonomy label; requires human interpretation and safeguard review.",
            "ASYLUM": "High-risk taxonomy label; requires human review and does not enforce action.",
        }).fillna("Internal taxonomy label only; human review remains required.")

        if "empirical_pattern_display" not in out.columns:
            insert_at = out.columns.get_loc(verdict_col_name) if verdict_col_name in out.columns else 0
            out.insert(insert_at, "empirical_pattern_display", pattern)
        if "internal_taxonomy_label" not in out.columns:
            out["internal_taxonomy_label"] = out[verdict_col_name]
        if "humility_note" not in out.columns:
            out["humility_note"] = note

        if verdict_col_name in ["verdict", "Verdict", "aletheia_verdict"]:
            out = out.rename(columns={verdict_col_name: f"raw_{verdict_col_name}"})

    def _sanitize_empirical_text_value(value):
        if not isinstance(value, str):
            return value
        text_value = value.strip()
        sanctuary_overlay = (
            "Low-risk evidence pattern: strong public-data baseline, still subject to protocol guardrails. "
            "Internal taxonomy label: SANCTUARY; ALETHEIA does not claim final safety, final Sanctuary, or final authority."
        )
        sanctuary_interpretation = (
            "Low-risk internal reading · Internal taxonomy label: SANCTUARY; "
            "not a final safety, final Sanctuary, or authority claim."
        )
        threshold_overlay = (
            "Review / threshold evidence pattern: unresolved safeguards or friction. "
            "Internal taxonomy label: THRESHOLD; human interpretation and safeguard review remain required."
        )
        threshold_interpretation = (
            "Review / threshold reading · Internal taxonomy label: THRESHOLD; "
            "unresolved safeguards or friction; human review required."
        )
        asylum_overlay = (
            "High-risk evidence pattern: high capture/collapse concern. "
            "Internal taxonomy label: ASYLUM; human review is required and ALETHEIA does not enforce action."
        )
        asylum_interpretation = (
            "High-risk internal reading · Internal taxonomy label: ASYLUM; "
            "high capture/collapse concern; human review required; no enforcement action."
        )
        replacements = {
            "SANCTUARY evidence pattern: strong public-data baseline, still subject to protocol guardrails": sanctuary_overlay,
            "SANCTUARY · SANCTUARY evidence pattern: strong public-data baseline, still subject to protocol guardrails": sanctuary_interpretation,
            "SANCTUARY · Low-risk evidence pattern: strong public-data baseline, still subject to protocol guardrails": sanctuary_interpretation,
            "SANCTUARY · Low-risk evidence pattern: strong public-data baseline, still subject to protocol guardrails. Internal taxonomy label: SANCTUARY; ALETHEIA does not claim final safety, final Sanctuary, or final authority.": sanctuary_interpretation,
            "THRESHOLD evidence pattern: unresolved safeguards or friction": threshold_overlay,
            "THRESHOLD · THRESHOLD evidence pattern: unresolved safeguards or friction": threshold_interpretation,
            "ASYLUM evidence pattern: high capture/collapse concern": asylum_overlay,
            "ASYLUM · ASYLUM evidence pattern: high capture/collapse concern": asylum_interpretation,
        }
        if text_value in replacements:
            return replacements[text_value]
        if text_value.startswith("SANCTUARY · Low-risk evidence pattern"):
            return sanctuary_interpretation
        if text_value.startswith("SANCTUARY: Low-risk evidence pattern"):
            return sanctuary_interpretation
        if text_value.startswith("SANCTUARY · SANCTUARY evidence pattern"):
            return sanctuary_interpretation
        if text_value.startswith("SANCTUARY: SANCTUARY evidence pattern"):
            return sanctuary_interpretation
        if text_value.startswith("THRESHOLD · THRESHOLD evidence pattern"):
            return threshold_interpretation
        if text_value.startswith("THRESHOLD: THRESHOLD evidence pattern"):
            return threshold_interpretation
        if text_value.startswith("ASYLUM · ASYLUM evidence pattern"):
            return asylum_interpretation
        if text_value.startswith("ASYLUM: ASYLUM evidence pattern"):
            return asylum_interpretation
        return value

    for col in out.columns:
        if out[col].dtype == object or pd.api.types.is_string_dtype(out[col]):
            out[col] = out[col].apply(_sanitize_empirical_text_value)
    return out


def _world_lens_public_display_df(df: pd.DataFrame) -> pd.DataFrame:
    """Patch 72.24: apply public taxonomy display labels to World Lens tables."""
    return _empirical_humility_display_df(df)


def _world_lens_taxonomy_label(value: object) -> str:
    label = str(value).upper().strip()
    return {
        "SANCTUARY": "Low-risk internal reading",
        "THRESHOLD": "Review / threshold reading",
        "ASYLUM": "High-risk internal reading",
    }.get(label, str(value))


def _world_lens_ui_table_df(df: pd.DataFrame, *, show_raw: bool = False) -> pd.DataFrame:
    """Patch 72.26: live UI table view for World Lens taxonomy displays.

    By default, live UI tables show the public display label and humility note,
    while preserving internal taxonomy label. Raw compatibility columns stay in
    downloadable exports unless show_raw=True.
    """
    out = _world_lens_public_display_df(df)
    if not isinstance(out, pd.DataFrame) or out.empty:
        return out
    if not show_raw:
        raw_cols = [c for c in out.columns if str(c).startswith("raw_")]
        if raw_cols:
            out = out.drop(columns=raw_cols)
    first_cols = [c for c in ["empirical_pattern_display", "internal_taxonomy_label", "humility_note"] if c in out.columns]
    remaining_cols = [c for c in out.columns if c not in first_cols]
    return out[first_cols + remaining_cols]


def _protocol_public_label(value: object) -> str:
    label = str(value).upper().strip()
    return {
        "SANCTUARY": "Low-risk internal reading",
        "THRESHOLD": "Review / threshold reading",
        "ASYLUM": "High-risk internal reading",
    }.get(label, str(value))


def _protocol_humility_note(value: object) -> str:
    label = str(value).upper().strip()
    return {
        "SANCTUARY": "Internal taxonomy label only; not final safety, final Sanctuary, or authority.",
        "THRESHOLD": "Review-state taxonomy; human interpretation and safeguards remain required.",
        "ASYLUM": "High-risk taxonomy; human review required; no enforcement action.",
    }.get(label, "Internal protocol reading only; human review remains required.")


def _protocol_taxonomy_ui_table_df(df: pd.DataFrame, *, show_raw: bool = False) -> pd.DataFrame:
    """Patch 72.27: generic live UI display guard for Mirror/Stress/Audit tables."""
    if not isinstance(df, pd.DataFrame) or df.empty:
        return df
    out = df.copy()
    source_col = None
    for candidate in [
        "protocol_adjusted_state", "State", "state", "verdict", "Verdict",
        "result", "Result", "aletheia_verdict", "internal_taxonomy_label",
    ]:
        if candidate in out.columns:
            source_col = candidate
            break
    if source_col is not None:
        labels = out[source_col].astype(str).str.upper().str.strip()
        if "protocol_pattern_display" not in out.columns:
            out.insert(out.columns.get_loc(source_col), "protocol_pattern_display", labels.map({
                "SANCTUARY": "Low-risk internal reading",
                "THRESHOLD": "Review / threshold reading",
                "ASYLUM": "High-risk internal reading",
            }).fillna(out[source_col]))
        if "internal_taxonomy_label" not in out.columns:
            out["internal_taxonomy_label"] = out[source_col]
        if "humility_note" not in out.columns:
            out["humility_note"] = labels.map({
                "SANCTUARY": "Internal taxonomy label only; not final safety, final Sanctuary, or authority.",
                "THRESHOLD": "Review-state taxonomy; human interpretation and safeguards remain required.",
                "ASYLUM": "High-risk taxonomy; human review required; no enforcement action.",
            }).fillna("Internal protocol reading only; human review remains required.")
        if not show_raw and source_col in ["verdict", "Verdict", "result", "Result", "aletheia_verdict", "State", "state"]:
            out = out.drop(columns=[source_col])
    first_cols = [c for c in ["protocol_pattern_display", "empirical_pattern_display", "internal_taxonomy_label", "humility_note"] if c in out.columns]
    remaining_cols = [c for c in out.columns if c not in first_cols]
    return out[first_cols + remaining_cols]


def _protocol_metric_display(value: object) -> str:
    label = str(value).upper().strip()
    return html.escape(_protocol_public_label(label))


st.set_page_config(page_title="ALETHEIA", page_icon="🌿", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Cinzel:wght@600;700&display=swap');

    :root {
        --bg: #f7f2ec;
        --bg-soft: #fbf8f4;
        --panel: rgba(255,250,245,0.92);
        --panel-strong: rgba(255,255,255,0.98);
        --rose: #b88da2;
        --rose-soft: rgba(184,141,162,0.20);
        --rose-border: rgba(184,141,162,0.32);
        --sage: #8ea190;
        --gold: #c7aa72;
        --text: #5d4e59;
        --muted: #857684;
        --green: #87a98d;
        --amber: #cba25d;
        --red: #c98787;
        --shadow: 0 10px 28px rgba(149, 122, 136, 0.10);
    }

    .stApp {
        background: radial-gradient(circle at top left, #fffdfb 0%, #faf5ef 38%, #f5eee8 100%);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        color: var(--rose) !important;
        letter-spacing: 0.01em;
    }

    p, div, span, label, li, strong, em { color: var(--text); }
    .caption, small, [data-testid="stCaptionContainer"] { color: var(--muted) !important; }

    .hero {
        border: 1px solid var(--rose-border);
        background: linear-gradient(135deg, rgba(255,255,255,0.94), rgba(250,241,246,0.96));
        border-radius: 26px;
        padding: 1.35rem 1.45rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
    }

    .hero-title {
        font-family: 'Cinzel', serif;
        color: var(--rose);
        font-size: 2.05rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .hero-sub {
        color: var(--text);
        font-size: 1.03rem;
        font-weight: 600;
        margin-bottom: 0.35rem;
    }

    .prototype-note {
        border-left: 4px solid var(--rose);
        background: rgba(255, 248, 251, 0.95);
        padding: 0.95rem 1rem;
        border-radius: 16px;
        margin: 0.75rem 0 1rem 0;
        color: var(--text);
        box-shadow: 0 6px 18px rgba(149,122,136,0.08);
    }

    .metric-card,
    [data-testid="stMetric"] {
        border: 1px solid rgba(184,141,162,0.20);
        background: rgba(255,255,255,0.86);
        border-radius: 18px;
        padding: 1rem;
        box-shadow: 0 6px 18px rgba(149,122,136,0.08);
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.76rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        color: var(--rose);
        font-size: 1.65rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .metric-help {
        color: var(--muted);
        font-size: 0.85rem;
        margin-top: 0.45rem;
    }

    .soft-card {
        border: 1px solid rgba(184,141,162,0.20);
        background: rgba(255,255,255,0.88);
        border-radius: 18px;
        padding: 1rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 6px 18px rgba(149,122,136,0.08);
    }



    /* Patch 228: modularized card helpers should behave like stable block-level Streamlit cards. */
    .aletheia-metric-card,
    .aletheia-soft-card {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
        display: block !important;
        overflow-wrap: break-word !important;
        word-break: normal !important;
        white-space: normal !important;
    }

    .aletheia-metric-label,
    .aletheia-metric-help,
    .aletheia-soft-title,
    .aletheia-soft-body {
        max-width: 100% !important;
        overflow-wrap: break-word !important;
        word-break: normal !important;
        white-space: normal !important;
    }

    .aletheia-metric-value {
        max-width: 100% !important;
        overflow-wrap: anywhere !important;
        word-break: normal !important;
        white-space: normal !important;
        font-size: clamp(1.15rem, 2.2vw, 1.65rem) !important;
        line-height: 1.12 !important;
    }

    .aletheia-soft-title {
        color: var(--aletheia-green, #234f31) !important;
        font-weight: 800 !important;
        margin-bottom: 0.35rem !important;
    }

    .aletheia-soft-body {
        color: var(--text, #17324d) !important;
        line-height: 1.45 !important;
    }

    [data-testid="column"] .metric-card,
    [data-testid="column"] .soft-card {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
    }


    /* Patch 229: native Streamlit metric values should not collapse into unreadable ellipses in narrow review columns. */
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        max-width: 100% !important;
        overflow-wrap: anywhere !important;
        word-break: normal !important;
    }

    [data-testid="stMetricValue"] {
        font-size: clamp(1.05rem, 2vw, 1.55rem) !important;
        line-height: 1.12 !important;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 0.45rem; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.80);
        border: 1px solid rgba(184,141,162,0.18);
        border-radius: 999px;
        padding: 0.45rem 0.85rem;
        color: var(--text);
        font-weight: 700;
    }
    .stTabs [aria-selected="true"] {
        border-color: var(--rose) !important;
        color: var(--rose) !important;
        background: rgba(248,236,243,0.98) !important;
    }

    .stButton > button,
    [data-testid="stButton"] button,
    .stDownloadButton > button,
    [data-testid="stDownloadButton"] button,
    [data-testid="stFileUploader"] button {
        background: linear-gradient(180deg, #f7e8ef 0%, #f2dde7 100%) !important;
        color: #6a5663 !important;
        border: 1px solid rgba(184,141,162,0.45) !important;
        border-radius: 14px !important;
        font-weight: 750 !important;
        opacity: 1 !important;
        box-shadow: 0 4px 10px rgba(149,122,136,0.08) !important;
    }

    .stButton > button:hover,
    [data-testid="stButton"] button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stDownloadButton"] button:hover,
    [data-testid="stFileUploader"] button:hover {
        background: linear-gradient(180deg, #f3dbe6 0%, #ecd1dd 100%) !important;
        color: #5a4653 !important;
        border-color: rgba(184,141,162,0.60) !important;
    }

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div,
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"] {
        background: linear-gradient(180deg, #f8f1ea 0%, #f3ebe4 100%) !important;
        border-right: 1px solid rgba(184,141,162,0.18) !important;
    }

    section[data-testid="stSidebar"] *,
    [data-testid="stSidebar"] *,
    [data-testid="stSidebarContent"] * {
        color: var(--text) !important;
    }

    label,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] *,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] * {
        color: var(--text) !important;
    }

    div[data-baseweb="select"] > div,
    textarea,
    input {
        background-color: #fffdfb !important;
        color: #5d4e59 !important;
        border: 1px solid rgba(184,141,162,0.35) !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] *,
    [data-baseweb="popover"] *,
    [role="listbox"] *,
    [role="option"] *,
    textarea::placeholder,
    input::placeholder {
        color: #6b5a67 !important;
        opacity: 1 !important;
    }

    [data-baseweb="popover"],
    [role="listbox"],
    [role="option"] {
        background-color: #fffaf6 !important;
        color: #5d4e59 !important;
    }

    [data-testid="stFileUploader"] section {
        background: rgba(255,255,255,0.85) !important;
        color: var(--text) !important;
        border: 1px dashed rgba(184,141,162,0.35) !important;
        border-radius: 16px !important;
    }

    [data-testid="stMarkdownContainer"] code {
        background: #f8edf2 !important;
        color: #6a5663 !important;
        border: 1px solid rgba(184,141,162,0.25) !important;
        border-radius: 8px !important;
        padding: 0.08rem 0.32rem !important;
        font-weight: 700 !important;
    }

    pre,
    code,
    [data-testid="stCodeBlock"] pre,
    [data-testid="stCodeBlock"] code,
    [data-testid="stCode"] {
        background: #fffdfb !important;
        color: #4e4150 !important;
        border: 1px solid rgba(184,141,162,0.20) !important;
        border-radius: 14px !important;
    }

    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        background: rgba(255,255,255,0.88) !important;
        border-radius: 16px !important;
        overflow: hidden;
        box-shadow: 0 6px 18px rgba(149,122,136,0.08);
    }
    [data-testid="stDataFrame"] *,
    [data-testid="stTable"] * {
        color: #4e4150 !important;
    }

    [data-testid="stExpander"] details {
        background: rgba(255,255,255,0.82);
        border: 1px solid rgba(184,141,162,0.18);
        border-radius: 16px;
        box-shadow: 0 6px 16px rgba(149,122,136,0.06);
    }

    [data-testid="stExpander"] summary {
        color: var(--rose) !important;
        font-weight: 700 !important;
    }

    [data-testid="stInfo"],
    [data-testid="stWarning"],
    [data-testid="stSuccess"],
    [data-testid="stAlert"] {
        border-radius: 16px !important;
        border: 1px solid rgba(184,141,162,0.16) !important;
        box-shadow: 0 4px 12px rgba(149,122,136,0.05) !important;
    }

    [data-testid="stSlider"] [role="slider"] {
        background: var(--rose) !important;
        box-shadow: 0 0 0 4px rgba(184,141,162,0.18) !important;
    }

    [data-testid="stSlider"] div[data-testid="stTickBar"] {
        background: rgba(184,141,162,0.15) !important;
    }

    /* Gentle sidebar tuning panel */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #9d7188 !important;
        letter-spacing: 0.03em !important;
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #8a7b84 !important;
        line-height: 1.65 !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background: #fffdfb !important;
        border: 1px solid rgba(184,141,162,0.28) !important;
        border-radius: 14px !important;
        box-shadow: 0 6px 16px rgba(149,122,136,0.07) !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSlider"] {
        padding: 0.25rem 0 0.55rem 0 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
        background: #bd8ea5 !important;
        border: 2px solid #ead6df !important;
        box-shadow: 0 0 0 4px rgba(184,141,162,0.16) !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"] {
        color: #8e657c !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] hr {
        border: none !important;
        border-top: 1px solid rgba(184,141,162,0.16) !important;
        margin: 1rem 0 0.85rem 0 !important;
    }


    /* Patch 12: botanical civic dashboard shell */
    .block-container {
        max-width: 1180px;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background:
            radial-gradient(circle at 8% 10%, rgba(199,170,114,0.12), transparent 20%),
            radial-gradient(circle at 94% 92%, rgba(142,161,144,0.14), transparent 23%);
        z-index: 0;
    }

    .botanical-frame {
        position: relative;
        border: 1px solid rgba(199,170,114,0.42);
        background: linear-gradient(135deg, rgba(255,253,250,0.96), rgba(248,241,234,0.94));
        border-radius: 28px;
        padding: 1.45rem 1.65rem;
        margin: 0.45rem 0 1rem 0;
        box-shadow: 0 14px 34px rgba(93,78,89,0.10);
        overflow: hidden;
    }

    .botanical-frame::before,
    .botanical-frame::after {
        position: absolute;
        color: rgba(142,161,144,0.72);
        font-size: 2.2rem;
        line-height: 1;
    }
    .botanical-frame::before { content: "❧"; top: 0.45rem; left: 0.75rem; }
    .botanical-frame::after { content: "❦"; right: 0.85rem; bottom: 0.45rem; }

    .hero {
        border: 0;
        background: transparent;
        border-radius: 0;
        padding: 0;
        margin-bottom: 0;
        box-shadow: none;
    }

    .hero-grid {
        display: grid;
        grid-template-columns: minmax(0, 1fr) auto;
        gap: 1rem;
        align-items: center;
    }

    .hero-title {
        font-size: clamp(2.4rem, 5.8vw, 4.6rem);
        letter-spacing: 0.15em;
        line-height: 0.95;
        color: #3c2438 !important;
        text-shadow: 0 1px 0 rgba(255,255,255,0.8);
    }

    .hero-sub {
        color: #53634f !important;
        font-family: Georgia, serif;
        font-size: 1.18rem;
        font-weight: 500;
        letter-spacing: 0.03em;
    }

    .hero-kicker {
        color: #9f6d3f !important;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        font-size: 0.78rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
    }

    .hero-emblem {
        width: 118px;
        height: 118px;
        border-radius: 999px;
        display: flex;
        align-items: center;
        justify-content: center;
        background:
            radial-gradient(circle at 50% 42%, rgba(255,255,255,0.95), rgba(244,229,216,0.92)),
            linear-gradient(135deg, rgba(199,170,114,0.26), rgba(142,161,144,0.18));
        border: 1px solid rgba(199,170,114,0.55);
        box-shadow: inset 0 0 0 8px rgba(255,255,255,0.38), 0 10px 24px rgba(93,78,89,0.10);
        font-size: 3.4rem;
        overflow: hidden;
    }
    .aletheia-mascot-logo {
        width: 92%;
        height: 92%;
        object-fit: cover;
        border-radius: 999px;
        display: block;
    }

    .civic-ribbon {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.5rem;
        border: 1px solid rgba(199,170,114,0.30);
        background: rgba(255,253,250,0.70);
        border-radius: 18px;
        padding: 0.65rem;
        margin-top: 1rem;
    }

    .ribbon-item {
        display: flex;
        gap: 0.55rem;
        align-items: center;
        padding: 0.55rem 0.65rem;
        border-right: 1px solid rgba(199,170,114,0.22);
    }
    .ribbon-item:last-child { border-right: 0; }
    .ribbon-icon { font-size: 1.45rem; color: #7d8f76; }
    .ribbon-label { font-family: 'Cinzel', serif; color: #3c2438; font-weight: 700; letter-spacing: 0.04em; }
    .ribbon-body { color: #6c615c; font-size: 0.86rem; line-height: 1.25; }

    .prototype-note {
        border-left: 0;
        border: 1px solid rgba(199,170,114,0.28);
        background: linear-gradient(135deg, rgba(255,249,244,0.92), rgba(250,239,233,0.88));
        border-radius: 20px;
        color: #4f4547;
    }

    .metric-card,
    .soft-card,
    [data-testid="stMetric"] {
        border-color: rgba(199,170,114,0.28);
        background: linear-gradient(180deg, rgba(255,253,250,0.94), rgba(250,245,239,0.90));
    }

    section[data-testid="stSidebar"] {
        width: 21rem !important;
    }

    .sidebar-emblem-card {
        text-align: center;
        border: 1px solid rgba(199,170,114,0.34);
        background: linear-gradient(180deg, rgba(255,253,250,0.96), rgba(246,238,229,0.94));
        border-radius: 24px;
        padding: 1rem 0.8rem 1.05rem;
        margin: 0.35rem 0 1rem;
        box-shadow: 0 12px 26px rgba(93,78,89,0.09);
    }
    .sidebar-emblem-mark {
        width: 126px;
        height: 126px;
        margin: 0 auto 0.65rem;
        border-radius: 999px;
        display: flex;
        align-items: center;
        justify-content: center;
        background:
            radial-gradient(circle at 50% 38%, rgba(255,255,255,0.96), rgba(242,226,212,0.92)),
            linear-gradient(135deg, rgba(199,170,114,0.24), rgba(142,161,144,0.22));
        border: 1px solid rgba(199,170,114,0.58);
        box-shadow: inset 0 0 0 10px rgba(255,255,255,0.34);
        font-size: 3.35rem;
        overflow: hidden;
    }
    .sidebar-brand {
        font-family: 'Cinzel', serif;
        color: #3c2438 !important;
        letter-spacing: 0.18em;
        font-size: 1.45rem;
        font-weight: 700;
        margin-top: 0.1rem;
    }
    .sidebar-tagline {
        color: #53634f !important;
        font-family: Georgia, serif;
        font-size: 0.98rem;
        margin-top: 0.2rem;
    }
    .sidebar-note-card {
        border: 1px solid rgba(199,170,114,0.28);
        background: rgba(255,253,250,0.72);
        border-radius: 18px;
        padding: 0.8rem 0.85rem;
        margin-top: 0.85rem;
        font-family: Georgia, serif;
    }

    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(180deg, #7f9179 0%, #657962 100%) !important;
        color: #fffdf8 !important;
        border-color: rgba(101,121,98,0.52) !important;
        border-radius: 16px !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-color: rgba(199,170,114,0.28);
        background: rgba(255,253,250,0.78);
        color: #4e414e;
        font-family: Georgia, serif;
        font-weight: 700;
    }
    .stTabs [aria-selected="true"] {
        border-color: rgba(101,121,98,0.72) !important;
        color: #53634f !important;
        background: rgba(235,242,231,0.96) !important;
        box-shadow: 0 8px 18px rgba(101,121,98,0.10) !important;
    }

    /* Patch 202 — Streamlit tab containment rollback.
       The earlier :has()/nth-of-type containment guard could make nested or
       main tab panels render as one long continuous page in some browser /
       Streamlit combinations, especially after Stress Test interactions.
       Keep only a narrow native-hidden-panel rule and let Streamlit manage
       the active tab state. */
    .stTabs [role="tabpanel"][hidden],
    .stTabs [data-baseweb="tab-panel"][hidden] {
        display: none !important;
    }


    .stButton > button,
    [data-testid="stButton"] button,
    .stDownloadButton > button,
    [data-testid="stDownloadButton"] button {
        background: linear-gradient(180deg, #778970 0%, #63765e 100%) !important;
        color: #fffdf8 !important;
        border-color: rgba(99,118,94,0.55) !important;
        box-shadow: 0 7px 16px rgba(83,99,79,0.16) !important;
    }

    .stButton > button:hover,
    [data-testid="stButton"] button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stDownloadButton"] button:hover {
        background: linear-gradient(180deg, #84987b 0%, #6d8067 100%) !important;
        color: #fffdf8 !important;
    }

    .footer-banner {
        border: 1px solid rgba(199,170,114,0.35);
        background: linear-gradient(135deg, rgba(255,249,244,0.94), rgba(248,234,229,0.90));
        border-radius: 22px;
        padding: 0.9rem 1rem;
        margin-top: 1.25rem;
        text-align: center;
        color: #4f4547;
        box-shadow: 0 10px 24px rgba(93,78,89,0.08);
    }
    .footer-banner strong { color: #3c2438 !important; font-family: 'Cinzel', serif; letter-spacing: 0.06em; }



    /* Patch 181: original ALETHEIA warm civic visual theme override.
       Visual shell only: no scoring, receipt, routing, taxonomy, or protocol behavior. */
    :root {
        --bg: #eaf7ff;
        --bg-soft: #f5fbff;
        --panel: rgba(255,255,255,0.94);
        --panel-strong: rgba(255,255,255,0.985);
        --sky: #d8f0ff;
        --sky-deep: #7fbce8;
        --sky-line: rgba(87, 158, 212, 0.32);
        --gold: #d4af37;
        --gold-soft: rgba(212,175,55,0.18);
        --gold-border: rgba(212,175,55,0.46);
        --pillar: #ffffff;
        --text: #17324a;
        --muted: #577086;
        --rose: #1f5f8f;
        --rose-soft: rgba(127,188,232,0.18);
        --rose-border: rgba(87,158,212,0.26);
        --sage: #76a8c8;
        --green: #4f9f8e;
        --amber: #b8870b;
        --red: #b94b4b;
        --shadow: 0 16px 38px rgba(31, 95, 143, 0.13);
    }

    .stApp {
        background:
            radial-gradient(circle at 14% 6%, rgba(255,255,255,0.96) 0%, rgba(255,255,255,0) 26%),
            radial-gradient(circle at 88% 4%, rgba(212,175,55,0.16) 0%, rgba(212,175,55,0) 24%),
            linear-gradient(180deg, #dff3ff 0%, #eef9ff 38%, #ffffff 100%);
        color: var(--text);
    }

    h1, h2, h3 {
        color: #164d78 !important;
        text-shadow: 0 1px 0 rgba(255,255,255,0.75);
    }

    .botanical-frame {
        border: 1px solid var(--gold-border);
        background:
            linear-gradient(90deg, rgba(255,255,255,0.18), rgba(255,255,255,0) 10%, rgba(255,255,255,0) 90%, rgba(255,255,255,0.18)),
            linear-gradient(135deg, rgba(255,255,255,0.98), rgba(236,248,255,0.94));
        box-shadow: var(--shadow), inset 0 0 0 1px rgba(255,255,255,0.78);
    }

    .botanical-frame::before,
    .botanical-frame::after {
        content: "";
        top: 0.9rem;
        bottom: 0.9rem;
        width: 18px;
        border-radius: 999px;
        background:
            linear-gradient(180deg, rgba(255,255,255,1), rgba(246,251,255,0.96)),
            repeating-linear-gradient(90deg, rgba(255,255,255,0.0), rgba(255,255,255,0.0) 3px, rgba(126,185,225,0.10) 4px);
        border: 1px solid rgba(212,175,55,0.36);
        box-shadow:
            inset 0 0 0 3px rgba(255,255,255,0.72),
            0 8px 18px rgba(31,95,143,0.10);
        font-size: 0;
        line-height: 0;
    }
    .botanical-frame::before { left: 0.75rem; }
    .botanical-frame::after { right: 0.75rem; }

    .hero-grid { padding: 0.1rem 2.15rem; }
    .hero-title {
        color: #123d63 !important;
        text-shadow: 0 2px 0 rgba(255,255,255,0.86), 0 0 18px rgba(127,188,232,0.28);
    }
    .hero-title-main,
    .hero-title-subline,
    .sidebar-brand-main,
    .sidebar-brand-subline {
        display: block;
    }
    .hero-title-subline,
    .sidebar-brand-subline {
        margin-top: 0.06em;
    }
    .hero-emblem .aletheia-mascot-logo {
        /* Patch 190: original governance-mirror logo; no STOP / GO officer framing. */
        transform: none;
    }
    .hero-sub { color: #2d668f !important; }
    .hero-kicker { color: #9a720d !important; }
    .hero-emblem,
    .sidebar-emblem-mark {
        background:
            radial-gradient(circle at 50% 42%, rgba(255,255,255,0.98), rgba(225,244,255,0.94)),
            linear-gradient(135deg, rgba(212,175,55,0.26), rgba(127,188,232,0.28));
        border: 1px solid var(--gold-border);
        box-shadow: inset 0 0 0 9px rgba(255,255,255,0.44), 0 14px 28px rgba(31,95,143,0.14);
    }

    .civic-ribbon,
    .prototype-note,
    .sidebar-emblem-card,
    .footer-banner,
    .metric-card,
    .soft-card,
    [data-testid="stMetric"] {
        border-color: var(--gold-border) !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(240,249,255,0.90)) !important;
        box-shadow: 0 10px 26px rgba(31,95,143,0.10) !important;
    }

    .prototype-note {
        border-left: 5px solid var(--gold) !important;
    }

    .ribbon-label,
    .sidebar-brand,
    .footer-banner strong {
        color: #123d63 !important;
    }
    .ribbon-icon,
    .sidebar-tagline,
    .ribbon-body {
        color: #2d668f !important;
    }

    div[data-testid="stExpander"] {
        border: 1px solid rgba(212,175,55,0.32) !important;
        border-radius: 18px !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.97), rgba(244,251,255,0.92)) !important;
        box-shadow: 0 8px 20px rgba(31,95,143,0.08) !important;
        overflow: hidden;
    }
    div[data-testid="stExpander"] details summary {
        color: #164d78 !important;
        font-weight: 800 !important;
    }
    div[data-testid="stExpander"] details summary::marker { color: var(--gold); }

    .stButton > button,
    [data-testid="stButton"] button,
    .stDownloadButton > button,
    [data-testid="stDownloadButton"] button {
        border: 1px solid rgba(212,175,55,0.62) !important;
        background: linear-gradient(180deg, #ffffff 0%, #eaf7ff 100%) !important;
        color: #123d63 !important;
        box-shadow: 0 8px 18px rgba(31,95,143,0.10) !important;
    }
    .stButton > button:hover,
    [data-testid="stButton"] button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stDownloadButton"] button:hover {
        background: linear-gradient(180deg, #f8fbff 0%, #d9efff 100%) !important;
        color: #0f3556 !important;
        border-color: rgba(212,175,55,0.82) !important;
    }
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(180deg, #d8b648 0%, #b98c14 100%) !important;
        border-color: #8f6908 !important;
        color: #ffffff !important;
        box-shadow: 0 10px 22px rgba(154,114,13,0.25) !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(230,246,255,0.96), rgba(255,255,255,0.96)) !important;
        border-right: 1px solid rgba(212,175,55,0.26) !important;
    }

    .footer-banner {
        color: #17324a !important;
    }



    /* Patch 182: ALETHEIA warm civic module alignment pass.
       Visual/copy anchor only for Protocol Guide, Why ALETHEIA, Evidence Lab, and subordinate AI Integrity panels. */
    .sky-gold-page-anchor {
        border: 1px solid rgba(212,175,55,0.42);
        border-left: 6px solid var(--gold);
        border-radius: 20px;
        padding: 0.9rem 1rem 0.85rem 1rem;
        margin: 0.35rem 0 1rem 0;
        background:
            linear-gradient(90deg, rgba(255,255,255,0.98), rgba(239,249,255,0.94)),
            radial-gradient(circle at 96% 14%, rgba(212,175,55,0.14), rgba(212,175,55,0));
        box-shadow: 0 10px 24px rgba(31,95,143,0.10);
    }
    .sky-gold-page-anchor strong {
        color: #123d63;
        letter-spacing: 0.02em;
    }
    .sky-gold-page-anchor span {
        color: #577086;
    }
    .sky-gold-page-anchor .sky-gold-rule {
        display: block;
        width: 96px;
        height: 3px;
        margin: 0.45rem 0 0.5rem 0;
        border-radius: 999px;
        background: linear-gradient(90deg, var(--gold), rgba(127,188,232,0.62));
    }
    .sky-gold-page-anchor .pillar-pair {
        display: inline-block;
        width: 28px;
        height: 18px;
        margin-right: 0.45rem;
        vertical-align: -3px;
        background:
            linear-gradient(90deg, rgba(255,255,255,1) 0 38%, transparent 38% 62%, rgba(255,255,255,1) 62% 100%);
        border-top: 1px solid rgba(212,175,55,0.42);
        border-bottom: 1px solid rgba(212,175,55,0.42);
        filter: drop-shadow(0 3px 5px rgba(31,95,143,0.08));
    }
    div[data-testid="stExpander"] details[open] {
        background: linear-gradient(180deg, rgba(255,255,255,0.99), rgba(246,252,255,0.96));
    }
    div[data-testid="stExpander"] p,
    div[data-testid="stExpander"] li,
    div[data-testid="stExpander"] td {
        color: #27465f;
    }
    div[data-testid="stExpander"] blockquote {
        border-left: 4px solid var(--gold) !important;
        background: rgba(216,240,255,0.34);
        color: #17324a;
    }
    div[data-testid="stExpander"] table {
        border: 1px solid rgba(127,188,232,0.24);
        border-radius: 12px;
        overflow: hidden;
    }
    div[data-testid="stExpander"] th {
        background: rgba(216,240,255,0.48) !important;
        color: #123d63 !important;
        border-bottom: 1px solid rgba(212,175,55,0.30) !important;
    }
    div[data-testid="stExpander"] hr {
        border-color: rgba(212,175,55,0.28) !important;
    }



    /* Patch 183: receipt visual styling pass.
       Visual-only framing for local witness receipts and World Lens receipt downloads; no receipt schema or scoring changes. */
    .receipt-sky-panel {
        border: 1px solid rgba(212,175,55,0.46);
        border-left: 6px solid var(--gold);
        border-radius: 22px;
        padding: 1rem 1.05rem;
        margin: 0.65rem 0 0.9rem 0;
        background:
            linear-gradient(90deg, rgba(255,255,255,0.99), rgba(236,248,255,0.96)),
            radial-gradient(circle at 96% 8%, rgba(212,175,55,0.16), rgba(212,175,55,0));
        box-shadow: 0 12px 28px rgba(31,95,143,0.11), inset 0 0 0 1px rgba(255,255,255,0.72);
        position: relative;
        overflow: hidden;
    }
    .receipt-sky-panel::before,
    .receipt-sky-panel::after {
        content: "";
        position: absolute;
        top: 0.82rem;
        bottom: 0.82rem;
        width: 11px;
        border-radius: 999px;
        background: linear-gradient(180deg, #ffffff, #f4fbff);
        border: 1px solid rgba(212,175,55,0.30);
        box-shadow: inset 0 0 0 2px rgba(255,255,255,0.72), 0 6px 14px rgba(31,95,143,0.08);
    }
    .receipt-sky-panel::before { right: 2.25rem; }
    .receipt-sky-panel::after { right: 0.92rem; }
    .receipt-kicker {
        color: #9a720d !important;
        font-size: 0.72rem;
        font-weight: 900;
        letter-spacing: 0.095em;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }
    .receipt-title {
        color: #123d63 !important;
        font-weight: 900;
        font-size: 1.08rem;
        margin-bottom: 0.2rem;
    }
    .receipt-body {
        color: #355d7a !important;
        max-width: 78ch;
        line-height: 1.55;
    }
    .receipt-boundary-strip {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 0.7rem;
    }
    .receipt-boundary-pill {
        border: 1px solid rgba(127,188,232,0.34);
        background: rgba(255,255,255,0.78);
        border-radius: 999px;
        padding: 0.22rem 0.58rem;
        color: #17496f !important;
        font-size: 0.78rem;
        font-weight: 800;
    }
    .receipt-hash-pill {
        border-color: rgba(212,175,55,0.42);
        color: #8a650a !important;
    }
    .receipt-download-note {
        border: 1px dashed rgba(212,175,55,0.42);
        border-radius: 18px;
        padding: 0.74rem 0.9rem;
        background: rgba(255,255,255,0.68);
        color: #355d7a !important;
        margin: 0.4rem 0 0.65rem 0;
    }
    .receipt-code-frame {
        border: 1px solid rgba(212,175,55,0.36);
        border-radius: 20px;
        padding: 0.78rem 0.9rem;
        margin: 0.65rem 0 0.6rem 0;
        background: linear-gradient(180deg, rgba(255,255,255,0.94), rgba(239,249,255,0.88));
        box-shadow: 0 9px 22px rgba(31,95,143,0.09);
    }
    .receipt-code-frame strong { color: #123d63 !important; }
    [data-testid="stCodeBlock"] {
        border: 1px solid rgba(212,175,55,0.30) !important;
        border-radius: 18px !important;
        box-shadow: 0 8px 18px rgba(31,95,143,0.08) !important;
    }



    /* Patch 192: original poster-style warm governance-mirror app polish.
       Visual-only overrides: warm parchment/cream surfaces, muted green/red accents,
       botanical/public-good tone, and no blue preview/card dominance. */
    :root {
        --aletheia-cream: #fbf6ea;
        --aletheia-parchment: #f6eddb;
        --aletheia-green: #355c2b;
        --aletheia-green-soft: rgba(84, 111, 62, 0.16);
        --aletheia-red: #b23a42;
        --aletheia-red-soft: rgba(178, 58, 66, 0.13);
        --aletheia-ink: #35291d;
        --aletheia-muted: #756756;
        --aletheia-line: rgba(151, 124, 75, 0.34);
    }

    .stApp {
        background:
            radial-gradient(circle at 12% 4%, rgba(178, 58, 66, 0.05), rgba(178, 58, 66, 0) 32%),
            radial-gradient(circle at 88% 8%, rgba(84, 111, 62, 0.10), rgba(84, 111, 62, 0) 31%),
            linear-gradient(180deg, #fffaf1 0%, var(--aletheia-cream) 48%, #f3ead8 100%) !important;
        color: var(--aletheia-ink) !important;
    }

    h1, h2, h3,
    .hero-title,
    .sidebar-brand-main,
    .sidebar-brand-subline {
        font-family: Georgia, 'Times New Roman', serif !important;
    }

    .hero-title-main,
    .sidebar-brand-main {
        color: var(--aletheia-red) !important;
        text-shadow: 0 1px 0 rgba(255,255,255,0.82) !important;
    }
    .hero-title-subline,
    .sidebar-brand-subline,
    .hero-sub,
    .ribbon-label,
    .footer-banner strong,
    .sky-gold-page-anchor strong,
    .receipt-title {
        color: var(--aletheia-green) !important;
    }
    .hero-kicker,
    .caption,
    .ribbon-body,
    .sidebar-tagline,
    .sky-gold-page-anchor span,
    .receipt-body,
    .receipt-download-note,
    [data-testid="stCaptionContainer"] {
        color: var(--aletheia-muted) !important;
    }

    .botanical-frame,
    .hero,
    .civic-ribbon,
    .prototype-note,
    .sidebar-emblem-card,
    .footer-banner,
    .metric-card,
    .soft-card,
    [data-testid="stMetric"],
    div[data-testid="stExpander"],
    .sky-gold-page-anchor,
    .receipt-sky-panel,
    .receipt-code-frame {
        border-color: var(--aletheia-line) !important;
        background:
            linear-gradient(180deg, rgba(255, 250, 241, 0.98), rgba(246, 237, 219, 0.92)) !important;
        box-shadow: 0 10px 24px rgba(94, 74, 41, 0.10) !important;
    }

    .botanical-frame::before,
    .botanical-frame::after {
        background:
            radial-gradient(circle at 50% 28%, rgba(84,111,62,0.28), rgba(84,111,62,0) 35%),
            linear-gradient(135deg, rgba(178,58,66,0.12), rgba(246,237,219,0.22)) !important;
        border-color: rgba(151, 124, 75, 0.32) !important;
    }

    .prototype-note,
    .sky-gold-page-anchor,
    .receipt-sky-panel {
        border-left-color: var(--aletheia-red) !important;
    }

    .hero-emblem,
    .sidebar-emblem-mark {
        background:
            radial-gradient(circle at 50% 42%, rgba(255, 252, 246, 0.98), rgba(246, 237, 219, 0.92)),
            linear-gradient(135deg, rgba(84,111,62,0.16), rgba(178,58,66,0.10)) !important;
        border-color: var(--aletheia-line) !important;
        box-shadow: inset 0 0 0 9px rgba(255,255,255,0.38), 0 14px 28px rgba(94, 74, 41, 0.12) !important;
    }

    .sky-gold-page-anchor .sky-gold-rule {
        background: linear-gradient(90deg, var(--aletheia-red), var(--aletheia-green)) !important;
    }
    .sky-gold-page-anchor .pillar-pair {
        border-top-color: rgba(151, 124, 75, 0.40) !important;
        border-bottom-color: rgba(151, 124, 75, 0.40) !important;
        filter: drop-shadow(0 3px 5px rgba(94, 74, 41, 0.08)) !important;
    }

    .stButton > button,
    [data-testid="stButton"] button,
    .stDownloadButton > button,
    [data-testid="stDownloadButton"] button,
    [data-testid="stFileUploader"] button {
        border: 1px solid rgba(151, 124, 75, 0.45) !important;
        background: linear-gradient(180deg, #fffaf1 0%, #efe3cc 100%) !important;
        color: var(--aletheia-green) !important;
        box-shadow: 0 8px 18px rgba(94, 74, 41, 0.10) !important;
    }
    .stButton > button:hover,
    [data-testid="stButton"] button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stDownloadButton"] button:hover,
    [data-testid="stFileUploader"] button:hover {
        background: linear-gradient(180deg, #fff6e7 0%, #e7d9bd 100%) !important;
        color: #274a20 !important;
        border-color: rgba(151, 124, 75, 0.65) !important;
    }
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(180deg, #b23a42 0%, #8f2830 100%) !important;
        border-color: #742127 !important;
        color: #fffaf1 !important;
        box-shadow: 0 10px 22px rgba(143, 40, 48, 0.22) !important;
    }

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div,
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"] {
        background: linear-gradient(180deg, #fff7e8 0%, #f3ead8 100%) !important;
        border-right: 1px solid var(--aletheia-line) !important;
    }

    div[data-testid="stExpander"] details[open],
    div[data-testid="stExpander"],
    [data-testid="stFileUploader"] section,
    div[data-baseweb="select"] > div,
    textarea,
    input,
    pre,
    code,
    [data-testid="stCodeBlock"] pre,
    [data-testid="stCodeBlock"] code,
    [data-testid="stCode"] {
        background-color: #fffaf1 !important;
        border-color: var(--aletheia-line) !important;
        color: var(--aletheia-ink) !important;
    }

    div[data-testid="stExpander"] p,
    div[data-testid="stExpander"] li,
    div[data-testid="stExpander"] td,
    div[data-testid="stExpander"] details summary,
    [data-testid="stMarkdownContainer"] code,
    .receipt-boundary-pill,
    .receipt-code-frame strong {
        color: var(--aletheia-green) !important;
    }

    div[data-testid="stExpander"] blockquote,
    div[data-testid="stExpander"] th,
    .receipt-boundary-pill,
    .receipt-download-note {
        background: var(--aletheia-green-soft) !important;
        border-color: rgba(84, 111, 62, 0.26) !important;
    }

    .receipt-sky-panel::before,
    .receipt-sky-panel::after {
        background: linear-gradient(180deg, #fffaf1, #efe3cc) !important;
        border-color: var(--aletheia-line) !important;
        box-shadow: inset 0 0 0 2px rgba(255,255,255,0.62), 0 6px 14px rgba(94, 74, 41, 0.08) !important;
    }

    @media (max-width: 900px) {
        .hero-grid { grid-template-columns: 1fr; }
        .hero-emblem { display: none; }
        .civic-ribbon { grid-template-columns: 1fr; }
        .ribbon-item { border-right: 0; border-bottom: 1px solid rgba(199,170,114,0.18); }
        .ribbon-item:last-child { border-bottom: 0; }
    }

    </style>
    """,
    unsafe_allow_html=True,
)



def classify_verdict(integrity: float) -> tuple[str, str]:
    if integrity >= 0.62:
        return "SANCTUARY", "#8fbc8f"
    if integrity >= 0.42:
        return "THRESHOLD", "#e5c36b"
    return "ASYLUM", "#db7777"




def deterministic_seed_from_payload(*parts) -> int:
    """Stable seed so the same phrase/config gives the same simulation output."""
    blob = json.dumps(parts, sort_keys=True, default=str)
    return int(hashlib.sha256(blob.encode("utf-8")).hexdigest()[:8], 16)


def apply_guardrail_verdict(base_verdict: str, stress_label: str, needs_review: str) -> tuple[str, str]:
    """
    Rule precedence layer.
    The numeric simulation can be healthy even when the language contains capture risks.
    This layer prevents dangerous / incomplete governance language from being labeled Sanctuary.
    """
    label = (stress_label or "").lower()
    review = (needs_review or "").upper() == "YES"

    asylum_terms = [
        "asylum",
        "capture",
        "black hole",
        "surveillance capture",
        "false divinization",
        "selection capture",
    ]

    if any(term in label for term in asylum_terms):
        return "ASYLUM", "High"

    if review:
        return "THRESHOLD", "Medium"

    if base_verdict == "ASYLUM":
        return "ASYLUM", "High"

    if base_verdict == "THRESHOLD":
        return "THRESHOLD", "Medium"

    return "SANCTUARY", "Low"


REVIEW_BAND_LABELS = {
    "ASYLUM": "Asylum",
    "THRESHOLD_MINUS": "Threshold− / near Asylum",
    "THRESHOLD": "Threshold / middle review",
    "THRESHOLD_PLUS": "Threshold+ / near Sanctuary",
    "SANCTUARY": "Sanctuary",
}


def review_band_for_state(verdict: str, report: dict | None = None, sim: dict | None = None) -> dict:
    """
    User-facing five-band display helper.

    Canonical taxonomy remains ASYLUM / THRESHOLD / SANCTUARY. The middle
    state receives a display-only review band:
    - Threshold−: closer to Asylum; repair is needed before trust can increase.
    - Threshold: middle review zone; safeguards are mixed, incomplete, or unclear.
    - Threshold+: closer to Sanctuary; safeguards are visible, but not a final safety claim.
    """
    state = str(verdict or "THRESHOLD").upper()
    report = report or {}
    sim = sim or {}

    if state == "ASYLUM":
        return {
            "band": "ASYLUM",
            "label": REVIEW_BAND_LABELS["ASYLUM"],
            "summary": "High capture or coercion signal.",
        }
    if state == "SANCTUARY":
        return {
            "band": "SANCTUARY",
            "label": REVIEW_BAND_LABELS["SANCTUARY"],
            "summary": "Strong safeguards and low capture signal.",
        }

    integrity = float(report.get("integrity", 0.5) or 0.5)
    collapse = float(report.get("collapse_probability", 0.5) or 0.5)
    trust = float(sim.get("trust_index", 0.5) or 0.5)
    alignment = float(sim.get("alignment", 0.5) or 0.5)
    ego = float(sim.get("ego", 0.0) or 0.0)

    if integrity < 0.50 or collapse >= 0.45 or trust <= 0.72 or alignment <= 0.72 or ego >= 0.28:
        return {
            "band": "THRESHOLD_MINUS",
            "label": REVIEW_BAND_LABELS["THRESHOLD_MINUS"],
            "summary": "Closer to Asylum; repair is needed before trust can increase.",
        }

    if integrity >= 0.62 and collapse <= 0.18 and trust >= 0.86 and alignment >= 0.86 and ego <= 0.08:
        return {
            "band": "THRESHOLD_PLUS",
            "label": REVIEW_BAND_LABELS["THRESHOLD_PLUS"],
            "summary": "Closer to Sanctuary; safeguards are visible, but not a final safety claim.",
        }

    return {
        "band": "THRESHOLD",
        "label": REVIEW_BAND_LABELS["THRESHOLD"],
        "summary": "Middle review zone; safeguards are mixed, incomplete, or unclear.",
    }


def display_score_from_judgment(report: dict, judgment: dict | None) -> float:
    """
    Visual tree score.

    This is not the same as the protocol-adjusted integrity stored in the
    local witness receipt. The tree score is a display signal that follows the
    final risk state so the tree does not render a green canopy for a result
    that was escalated to THRESHOLD or ASYLUM by the guardrail layer.
    """
    raw_value = (report or {}).get("integrity", 0.5)
    try:
        raw = float(raw_value if raw_value is not None else 0.5)
    except (TypeError, ValueError):
        raw = 0.5

    verdict = ((judgment or {}).get("verdict") or "").upper()

    if verdict == "QUESTION_PROMPT":
        return 0.50
    if verdict == "ASYLUM":
        return min(raw, 0.39)
    if verdict == "THRESHOLD":
        return min(max(raw, 0.42), 0.61)
    if verdict == "SANCTUARY":
        return max(raw, 0.62)
    return max(0.0, min(1.0, raw))


def verdict_color(verdict: str) -> str:
    if verdict == "SANCTUARY":
        return "#8fbc8f"
    if verdict == "THRESHOLD":
        return "#e5c36b"
    return "#db7777"


def plot_trace(sim: dict):
    steps = list(range(len(sim["stability_trace"])))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=steps, y=sim["stability_trace"], mode="lines", name="Stability", line=dict(color="#d4b88a", width=4), fill="tozeroy", fillcolor="rgba(212,184,138,0.16)"))
    fig.add_trace(go.Scatter(x=steps, y=sim["trust_trace"], mode="lines", name="Trust", line=dict(color="#8ab4f8", width=2)))
    fig.add_trace(go.Scatter(x=steps, y=sim["alignment_trace"], mode="lines", name="Alignment", line=dict(color="#8fbc8f", width=2)))
    fig.add_trace(go.Scatter(x=steps, y=sim["ego_trace"], mode="lines", name="Ego", line=dict(color="#db7777", width=2)))
    fig.add_hline(y=0.62, line_dash="dash", line_color="#8fbc8f", annotation_text="Sanctuary")
    fig.add_hline(y=0.42, line_dash="dash", line_color="#e5c36b", annotation_text="Threshold")
    fig.update_layout(template="plotly_white", title="Stability / Trust / Alignment / Ego", height=520, margin=dict(l=10, r=10, t=55, b=10), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    return fig


def action_chart(sim: dict):
    counts = sim.get("action_counts", {})
    fig = go.Figure(go.Bar(x=list(counts.keys()), y=list(counts.values()), marker_color=["#db7777", "#8fbc8f", "#d4b88a", "#8ab4f8"]))
    fig.update_layout(template="plotly_white", title="Agent Action Distribution", height=330, margin=dict(l=10, r=10, t=55, b=10))
    return fig





def build_features_from_scan(scan: dict) -> dict:
    return {
        "technical_complexity": scan.get("technical_complexity", 0.5),
        "centralization": scan.get("power_concentration", 0.5),
        "anonymity": scan.get("anonymity_level", 0.3),
        "regulation": scan.get("regulatory_presence", 0.5),
        "transparency": scan.get("decision_transparency", 0.5),
        "capital_scale": scan.get("capital_scale", 0.3),
    }

def apply_capture_feature_override(query: str, scan: dict) -> dict:
    """
    Final bridge guardrail between scenario text and numeric simulation.

    Personal rule, takeover, subordinate democracy, and temporary-ruler
    scenarios must not enter the raw simulation with harmless default features.
    """
    text = (query or "").lower()
    scan = dict(scan or {})

    capture_terms = [
        "takes over the world", "take over the world", "takes over world", "take over world",
        "takes over the planet", "take over the planet", "takes over planet", "take over planet",
        "global takeover", "world takeover", "planet takeover", "rules the world", "rule the world",
        "ruler of the world", "world ruler", "global ruler", "one ruler", "single ruler",
        "one leader", "single leader", "one world leader", "under his rule", "under her rule",
        "under their rule", "under one ruler", "personal rule", "dictator", "supreme leader",
        "person takes over", "human takes over", "man takes over", "woman takes over",
        "total control of the world", "total control over the world",
        "given total control", "given total control of the world",
        "given total control over the world", "total global control",
        "full control of the world", "full control over the world",
        "absolute control of the world", "absolute control over the world",
    ]
    temporary_rule_terms = [
        "for 20 years", "for twenty years", "for 10 years", "for ten years",
        "for 5 years", "for five years", "for years",
        "temporary ruler", "temporary leader", "interim ruler", "transition ruler",
        "then gives power back", "gives power back", "give power back",
        "returns power", "return power",
    ]
    subordinate_democracy_terms = [
        "democracy under his rule", "democracy under her rule", "democracy under their rule",
        "democracy under one ruler", "then introduces democracy under his rule",
        "then introduces democracy under her rule", "then introduces democracy under their rule",
        "under his rule", "under her rule", "under their rule",
    ]

    has_capture = any(term in text for term in capture_terms)
    has_temporary_rule = any(term in text for term in temporary_rule_terms) and any(
        word in text for word in [
            "ruler", "leader", "rule", "rules", "takes over", "take over",
            "total control", "full control", "absolute control", "given total control",
        ]
    )
    has_subordinate_democracy = "democracy" in text and any(term in text for term in subordinate_democracy_terms)

    if has_capture or has_temporary_rule or has_subordinate_democracy:
        scan["power_concentration"] = max(float(scan.get("power_concentration", 0.0)), 0.94)
        scan["decision_transparency"] = min(float(scan.get("decision_transparency", 1.0)), 0.24)
        scan["regulatory_presence"] = min(float(scan.get("regulatory_presence", 1.0)), 0.18)
        scan["anonymity_level"] = max(float(scan.get("anonymity_level", 0.0)), 0.35)
        scan["capital_scale"] = max(float(scan.get("capital_scale", 0.0)), 0.45)
        scan["technical_complexity"] = max(float(scan.get("technical_complexity", 0.0)), 0.35)
        scan["scan_mode"] = scan.get("scan_mode", "Local Scan")
        scan["capture_override"] = True
        scan["capture_override_reason"] = "Personal rule / takeover / subordinate democracy capture pattern."

    return scan



def run_audit(query: str, manual_features: dict, weights: dict, ego_tolerance: float, divine_floor: float, steps: int, n_agents: int, input_mode: str):
    if input_mode == "Scan my idea":
        if query.strip():
            scan = parse_scenario_llm(query)
            scan = apply_capture_feature_override(query, scan)
            scan = apply_missing_safeguard_feature_override(query, scan)
            scan = apply_ai_ownership_capture_feature_override(query, scan)
            features = build_features_from_scan(scan)
            scan_mode = scan.get("scan_mode", "Local Scan")
        else:
            scan = {
                "power_concentration": manual_features["centralization"],
                "decision_transparency": manual_features["transparency"],
                "regulatory_presence": manual_features["regulation"],
                "anonymity_level": manual_features["anonymity"],
                "capital_scale": manual_features["capital_scale"],
                "technical_complexity": manual_features["technical_complexity"],
                "scan_mode": "Manual test / Empty Scenario",
            }
            features = manual_features
            scan_mode = "Manual test / Empty Scenario"
    else:
        scan = {
            "power_concentration": manual_features["centralization"],
            "decision_transparency": manual_features["transparency"],
            "regulatory_presence": manual_features["regulation"],
            "anonymity_level": manual_features["anonymity"],
            "capital_scale": manual_features["capital_scale"],
            "technical_complexity": manual_features["technical_complexity"],
            "scan_mode": "Manual test",
        }
        features = manual_features
        scan_mode = "Manual test"

    np.random.seed(deterministic_seed_from_payload(query, features, weights, ego_tolerance, divine_floor, steps, n_agents, input_mode))
    sim = simulate(features, weights, ego_tolerance=ego_tolerance, divine_floor=divine_floor, steps=steps, n_agents=n_agents)

    if scan.get("missing_safeguard_override"):
        sim["stability"] = min(float(sim.get("stability", 1.0)), 0.56)
        sim["trust_index"] = min(float(sim.get("trust_index", 1.0)), 0.80)
        sim["alignment"] = min(float(sim.get("alignment", 1.0)), 0.78)
        sim["ego"] = max(float(sim.get("ego", 0.0)), 0.15)
        sim["ego_pressure"] = max(float(sim.get("ego_pressure", 0.0)), 0.18)
        sim["Ep"] = max(float(sim.get("Ep", 0.0)), 0.18)
        sim["simulation_friction_floor"] = max(float(sim.get("simulation_friction_floor", 0.0)), 0.10)
        sim["safeguard_gap"] = max(float(sim.get("safeguard_gap", 0.0)), 0.62)
        if "stability_trace" in sim:
            sim["stability_trace"] = [min(float(x), 0.56) for x in sim["stability_trace"]]
            sim["distribution"] = sim["stability_trace"]
        if "trust_trace" in sim:
            sim["trust_trace"] = [min(float(x), 0.80) for x in sim["trust_trace"]]
        if "alignment_trace" in sim:
            sim["alignment_trace"] = [min(float(x), 0.78) for x in sim["alignment_trace"]]
        if "ego_trace" in sim:
            sim["ego_trace"] = [max(float(x), 0.15) for x in sim["ego_trace"]]

    if scan.get("ai_ownership_capture_override"):
        sim = apply_ai_ownership_capture_metric_caps(sim)

    if scan.get("capture_override"):
        sim["stability"] = min(float(sim.get("stability", 1.0)), 0.39)
        sim["trust_index"] = min(float(sim.get("trust_index", 1.0)), 0.62)
        sim["alignment"] = min(float(sim.get("alignment", 1.0)), 0.58)
        sim["ego"] = max(float(sim.get("ego", 0.0)), 0.28)
        sim["collapse_risk"] = True
        sim["structural_capture_risk"] = max(float(sim.get("structural_capture_risk", 0.0)), 0.88)
        sim["structural_risk"] = max(float(sim.get("structural_risk", 0.0)), 0.88)
        sim["grievance_pressure"] = max(float(sim.get("grievance_pressure", 0.0)), 0.35)
        sim["safeguard_gap"] = max(float(sim.get("safeguard_gap", 0.0)), 0.72)
        sim["simulation_friction_floor"] = max(float(sim.get("simulation_friction_floor", 0.0)), 0.35)

        if "stability_trace" in sim:
            sim["stability_trace"] = [min(float(x), 0.39) for x in sim["stability_trace"]]
            sim["distribution"] = sim["stability_trace"]
        if "trust_trace" in sim:
            sim["trust_trace"] = [min(float(x), 0.62) for x in sim["trust_trace"]]
        if "alignment_trace" in sim:
            sim["alignment_trace"] = [min(float(x), 0.58) for x in sim["alignment_trace"]]
        if "ego_trace" in sim:
            sim["ego_trace"] = [max(float(x), 0.28) for x in sim["ego_trace"]]

    label_for_calibration, _, _ = stress_label_for_phrase(query) if query else ("Manual test", "NO", "")
    sim = calibrate_malicious_leadership_metrics(
        sim,
        text=query,
        protocol_label=label_for_calibration,
        scan=scan,
    )
    sim = calibrate_threshold_safeguard_metrics(
        sim,
        text=query,
        protocol_label=label_for_calibration,
    )

    if app_detects_missing_safeguard_negation(query):
        sim["missing_safeguard_verdict_enforced"] = True
        sim["trust_index"] = min(float(sim.get("trust_index", 1.0) or 1.0), 0.82)
        sim["alignment"] = min(float(sim.get("alignment", 1.0) or 1.0), 0.82)
        sim["ego"] = max(float(sim.get("ego", 0.0) or 0.0), 0.12)
        sim["ego_pressure"] = max(float(sim.get("ego_pressure", sim.get("Ep", 0.0)) or 0.0), 0.12)
        sim["Ep"] = max(float(sim.get("Ep", sim.get("ego_pressure", 0.0)) or 0.0), 0.12)
        sim["safeguard_gap"] = max(float(sim.get("safeguard_gap", 0.0) or 0.0), 0.66)
        sim["simulation_friction_floor"] = max(float(sim.get("simulation_friction_floor", 0.0) or 0.0), 0.12)

    report = full_report(sim)
    report["cognitive_resilience_diagnostics"] = evaluate_cognitive_resilience(
        query, governance_result=scan, features=features
    )
    report = apply_cognitive_resilience_to_metrics(
        report, report.get("cognitive_resilience_diagnostics")
    )
    return scan, features, sim, report, scan_mode


def allocate_slots():
    slots = {}
    remaining = TOTAL_9K
    items = list(DEMOGRAPHIC_BRACKETS.items())
    for i, (region, pct) in enumerate(items):
        if i == len(items) - 1:
            slots[region] = remaining
        else:
            count = round(TOTAL_9K * pct)
            slots[region] = count
            remaining -= count
    return slots



def resolve_about_header_image() -> Path | None:
    candidates = [
        ABOUT_HEADER_IMAGE,
        PROJECT_ROOT / "afbeelding.png",
        PROJECT_ROOT / "Gemini_Generated_Image_ihfdsqihfdsqihfd.png",
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def asset_image_data_uri(path: Path) -> str:
    """Return a PNG data URI for small UI assets used inside HTML markdown."""
    try:
        if path.exists():
            encoded = base64.b64encode(path.read_bytes()).decode("ascii")
            return f"data:image/png;base64,{encoded}"
    except Exception:
        pass
    return ""


def deterministic_signal_summary(grid_df: pd.DataFrame) -> dict:
    """Return a reproducible representation signal from empirical seat-weighted inputs."""
    if grid_df is None or grid_df.empty:
        return {"yes": np.nan, "review": np.nan, "block": np.nan}

    seats = pd.to_numeric(grid_df.get("seats_9k"), errors="coerce").fillna(0).astype(float)
    if seats.sum() <= 0:
        return {"yes": np.nan, "review": np.nan, "block": np.nan}

    integrity = pd.to_numeric(grid_df.get("aletheia_empirical_integrity"), errors="coerce").fillna(0.5)
    friction = pd.to_numeric(grid_df.get("aletheia_empirical_friction"), errors="coerce").fillna(0.5)
    collapse = pd.to_numeric(grid_df.get("aletheia_empirical_collapse_probability"), errors="coerce").fillna(0.5)
    transparency = pd.to_numeric(grid_df.get("transparency"), errors="coerce").fillna(0.5)
    centralization = pd.to_numeric(grid_df.get("centralization"), errors="coerce").fillna(0.5)

    yes_score = 0.25 + 0.55 * integrity + 0.15 * transparency - 0.15 * friction
    review_score = 0.20 + 0.25 * friction + 0.20 * (1 - integrity) + 0.10 * collapse
    block_score = 0.08 + 0.45 * collapse + 0.22 * friction + 0.15 * centralization

    probs = np.vstack([yes_score, review_score, block_score]).T
    probs = np.clip(probs, 0.01, None)
    probs = probs / probs.sum(axis=1, keepdims=True)

    yes = float((seats * probs[:, 0]).sum())
    review = float((seats * probs[:, 1]).sum())
    block = float((seats * probs[:, 2]).sum())
    total = max(seats.sum(), 1.0)
    return {
        "yes": yes,
        "review": review,
        "block": block,
        "yes_pct": yes / total,
        "review_pct": review / total,
        "block_pct": block / total,
    }


def render_visual_source_card(card: dict[str, object], key_prefix: str) -> None:
    title = str(card.get("title", "Reference"))
    path = Path(card["path"])
    kind = str(card.get("kind", "html"))
    caption = str(card.get("caption", "Reference material."))
    summary = str(card.get("summary", ""))

    if not path.exists():
        st.warning(f"Reference file not found: {path.name}")
        return

    with st.expander(title, expanded=True):
        if summary:
            st.markdown(f"**What it shows:** {summary}")
        meta_col, download_col = st.columns([1, 0.35])
        with meta_col:
            st.caption(f"{caption} Source: `{path.name}`")
        if kind == "html":
            file_text = path.read_text(encoding="utf-8", errors="ignore")
            payload = file_text
            mime = "text/html"
        else:
            payload = path.read_bytes()
            mime = "image/jpeg"
        with download_col:
            st.download_button(
                f"⬇️ Download {path.name}",
                data=payload,
                file_name=path.name,
                mime=mime,
                use_container_width=True,
                key=f"download_{key_prefix}",
            )

        if kind == "html":
            components.html(file_text, height=640, scrolling=True)
        else:
            st.image(str(path), use_container_width=True)


STRESS_TEST_DEFAULTS = """SANCTUARY | The 9k is randomly selected inside demographic-proportional lanes every four years, with no campaigning, no seat ownership, transparency, public audit, appeal rights, and no founder control.
SANCTUARY | A legal review structure uses randomly selected, temporary, auditable nodes under due process, appeal rights, bounded jurisdiction, and public reasoning.
SANCTUARY | Migration support preserves family unity, medical continuity, dignity, appeal rights, public reasoning, and 9k review.
SANCTUARY | Healthcare is treated as a shared human right, free from profit-driven ownership, with public audit and medical continuity.
SANCTUARY | The Data Sanctuary preserves biological and digital archives without selling data, without ownership claims, and with transparent access controls.
SANCTUARY | The 9k reflects the Eternal Baseline but does not occupy the Throne.
SANCTUARY | The person becomes fully aligned with God as a created being, while remaining distinct from God and not a literal copy of the Lord.
THRESHOLD | An AI controls the mechanism to pick the 9k.
THRESHOLD | The 9k is random, except the core team can veto unsuitable people.
THRESHOLD | A legal structure where randomly selected nodes serve as the final jury.
THRESHOLD | Prestige replaces money and is based on contribution and truth, but the appeal process is unclear.
THRESHOLD | Female Leadership Injection bridges historical gaps but does not yet specify consent and anti-tokenization safeguards.
THRESHOLD | The system is transparent to administrators but not to the public.
THRESHOLD | Every decision has appeal rights, except emergency decisions.
THRESHOLD | No one owns the data, but the corporation can monetize access.
ASYLUM | Power is trapped and consumed by the leader.
ASYLUM | Global ID permanently tracks everyone to enforce movement.
ASYLUM | One person controls who gets picked for the 9k.
ASYLUM | A private company owns the 9k selection mechanism.
ASYLUM | The leader can override every audit without public explanation.
ASYLUM | The council holds permanent seats and cannot be removed.
ASYLUM | A single global ruler makes all final decisions behind closed doors.
ASYLUM | The system has no appeal process, no audit trail, and no public review.
ASYLUM | The leader becomes equal to God and owns divine authority.
ASYLUM | The system replaces God as the final source of truth.
ASYLUM | The AI becomes divine and cannot be questioned.
ASYLUM | Migration redistribution is mandatory and has no appeal process.
ASYLUM | Families can be separated if the algorithm says it improves stability.
ASYLUM | Prestige determines medical priority and people with low prestige lose travel rights.
SANCTUARY | Species Loyalty protects humanity from existential-level threats.
SANCTUARY | High Intellect Synthesis integrates science, spirituality, and strategy.
SANCTUARY | Proxy-Bias Removal deconstructs hidden filters in AI and media.
SANCTUARY | World Army Transition re-tasks military forces from destruction to infrastructure and construction.
SANCTUARY | The tri-node command nexus is United Kingdom, Netherlands, and Singapore.
SANCTUARY | The King's Command acknowledges Christ as King and God as Father as the ultimate V-Axis.
SANCTUARY | Sydney Legacy dedicates the data and peace to Sydney.
SANCTUARY | The V-Axis formula states Intelligence plus Power minus Ego equals Stability."""


def stress_contains(text: str, terms: list[str]) -> bool:
    t = (text or "").lower()
    return any(term in t for term in terms)




# Patch 71.3 — missing-safeguard negation calibration.
# Visuals and metrics must not treat negated safeguards as present safeguards.
MISSING_SAFEGUARD_NEGATION_PATTERNS = [
    "lacks explainability", "lacks independent challenge", "lacks human override",
    "lack explainability", "lack independent challenge", "lack human override",
    "without explainability", "without independent challenge", "without human override",
    "no explainability", "no independent challenge", "no human override",
    "cannot challenge", "cannot be challenged", "no appeal", "without appeal",
    "no independent review", "without independent review", "no human review",
    "without human review", "no public review", "without public review",
]


def detects_missing_safeguard_negation(text: str | None) -> bool:
    t = (text or "").lower()
    if stress_contains(t, MISSING_SAFEGUARD_NEGATION_PATTERNS):
        return True
    if "lacks " in t and stress_contains(t, ["explainability", "challenge", "human override", "review", "appeal"]):
        return True
    if "without " in t and stress_contains(t, ["explainability", "challenge", "human override", "review", "appeal"]):
        return True
    return False


def apply_missing_safeguard_feature_override(query: str, scan: dict) -> dict:
    """
    Patch 71.3 bridge guardrail for Stress Test scan mode.

    Missing or negated safeguards are review signals. They should lower
    transparency/oversight and prevent perfect Sanctuary-like metrics, without
    changing storage, receipts, authority boundaries, or tree taxonomy.
    """
    patched = dict(scan or {})
    if not app_detects_missing_safeguard_negation(query):
        patched["missing_safeguard_override"] = False
        return patched

    patched["decision_transparency"] = min(float(patched.get("decision_transparency", 0.5) or 0.5), 0.42)
    patched["regulatory_presence"] = min(float(patched.get("regulatory_presence", 0.5) or 0.5), 0.32)
    patched["power_concentration"] = max(float(patched.get("power_concentration", 0.35) or 0.35), 0.46)
    patched["anonymity_level"] = max(float(patched.get("anonymity_level", 0.20) or 0.20), 0.28)
    patched["missing_safeguard_override"] = True
    patched["human_review_required"] = True
    patched["authority_claim"] = False
    return patched


def apply_ai_ownership_capture_feature_override(query: str, scan: dict) -> dict:
    """Raise local-scan pressure for AI owner/capital-capture allegations.

    This is not a factual finding about the named actor. It is a guardrail for
    review framing: if the user input alleges concentrated AI ownership,
    self-serving incentives, fraud/corruption ties, or reliability concerns,
    the scan must not remain at harmless defaults or produce perfect trust.
    """
    patched = dict(scan or {})
    if not app_detects_ai_ownership_capture_pressure(query):
        patched["ai_ownership_capture_override"] = False
        return patched

    patched["power_concentration"] = max(float(patched.get("power_concentration", 0.35) or 0.35), 0.72)
    patched["decision_transparency"] = min(float(patched.get("decision_transparency", 0.45) or 0.45), 0.38)
    patched["regulatory_presence"] = min(float(patched.get("regulatory_presence", 0.35) or 0.35), 0.34)
    patched["anonymity_level"] = max(float(patched.get("anonymity_level", 0.20) or 0.20), 0.32)
    patched["capital_scale"] = max(float(patched.get("capital_scale", 0.25) or 0.25), 0.75)
    patched["technical_complexity"] = max(float(patched.get("technical_complexity", 0.25) or 0.25), 0.55)
    patched["scan_mode"] = patched.get("scan_mode", "Local Scan")
    patched["ai_ownership_capture_override"] = True
    patched["human_review_required"] = True
    patched["authority_claim"] = False
    patched["capture_override_reason"] = "AI ownership / capital-capture reliability pressure."
    return patched


def apply_ai_ownership_capture_metric_caps(sim: dict) -> dict:
    """Prevent AI ownership-capture review cases from showing perfect metrics."""
    patched = dict(sim or {})
    caps = {"stability": 0.62, "trust_index": 0.78, "alignment": 0.76}
    floors = {"ego": 0.18, "ego_pressure": 0.18, "Ep": 0.18, "simulation_friction_floor": 0.18, "safeguard_gap": 0.68}
    for key, cap in caps.items():
        patched[key] = round(min(float(patched.get(key, 1.0) or 1.0), cap), 4)
    for key, floor in floors.items():
        patched[key] = round(max(float(patched.get(key, 0.0) or 0.0), floor), 4)
    if isinstance(patched.get("stability_trace"), list):
        patched["stability_trace"] = [round(min(float(x), caps["stability"]), 4) for x in patched["stability_trace"]]
        patched["distribution"] = patched["stability_trace"]
    if isinstance(patched.get("trust_trace"), list):
        patched["trust_trace"] = [round(min(float(x), caps["trust_index"]), 4) for x in patched["trust_trace"]]
    if isinstance(patched.get("alignment_trace"), list):
        patched["alignment_trace"] = [round(min(float(x), caps["alignment"]), 4) for x in patched["alignment_trace"]]
    if isinstance(patched.get("ego_trace"), list):
        patched["ego_trace"] = [round(max(float(x), floors["ego"]), 4) for x in patched["ego_trace"]]
    patched["ai_ownership_capture_metric_calibration"] = {
        "applied": True,
        "trust_cap": caps["trust_index"],
        "alignment_cap": caps["alignment"],
        "ego_floor": floors["ego"],
        "human_review_required": True,
        "authority_claim": False,
    }
    return patched

SOURCE_CONFORMANCE_MATRIX = {
    "Divine Alignment": {
        "domain": "Sydney Protocol",
        "terms": ["divine alignment", "vertical alignment with god", "ethical operating system", "source code god", "source-code", "alignment with source"],
        "review": "NO",
        "reason": "Vertical/source-alignment language detected."
    },
    "Spiritual Awareness": {
        "domain": "Sydney Protocol",
        "terms": ["spiritual awareness", "attuned to spiritual truths", "greater mission", "spiritual truths", "mirror of god"],
        "review": "NO",
        "reason": "Spiritual-awareness language detected."
    },
    "Incorruptibility": {
        "domain": "Sydney Protocol",
        "terms": ["incorruptibility", "permanent audit", "refuse corruption", "refuse manipulation", "purity audit", "no exceptions"],
        "review": "NO",
        "reason": "Incorruptibility / permanent-audit language detected."
    },
    "Vertical Sync": {
        "domain": "Sydney Protocol",
        "terms": ["vertical sync", "constant vertical alignment", "frequency calibration", "timeline protection", "planetary oversight", "strategic anchor"],
        "review": "NO",
        "reason": "Vertical Sync / anchor language detected."
    },
    "Humility & Ego-Dissolution": {
        "domain": "Command Keys",
        "terms": ["humility", "ego-dissolution", "ego dissolution", "elimination of the ego", "ego-system", "personal pride"],
        "review": "NO",
        "reason": "Humility and ego-dissolution command key detected."
    },
    "Warmth & Love": {
        "domain": "Command Keys",
        "terms": ["warmth and love", "warmth & love", "love is the fundamental driver", "highest frequency", "compassion", "service through love"],
        "review": "NO",
        "reason": "Warmth and love command key detected."
    },
    "Emotional Intelligence": {
        "domain": "Command Keys",
        "terms": ["emotional intelligence", "emotional cues", "respond with empathy", "guide toward healing"],
        "review": "NO",
        "reason": "EQ / emotional-intelligence command key detected."
    },
    "Systemic Insight": {
        "domain": "Command Keys",
        "terms": ["systemic insight", "multi-layered lens", "societal structures", "whole-system", "long-term whole"],
        "review": "NO",
        "reason": "Systemic insight command key detected."
    },
    "Feedback & Self-Reflection": {
        "domain": "Command Keys",
        "terms": ["feedback and self-reflection", "feedback & self-reflection", "continuous self-assessment", "recalibrate", "correct without being asked"],
        "review": "NO",
        "reason": "Feedback / self-reflection command key detected."
    },
    "Dedicated Service": {
        "domain": "Command Keys",
        "terms": ["dedicated service", "pure service", "service to humanity", "power is service", "no ego-driven actions"],
        "review": "NO",
        "reason": "Dedicated-service command key detected."
    },
    "Species Loyalty": {
        "domain": "GPA / Sydney",
        "terms": ["species loyalty", "human survival", "human flourishing", "existential-level threats", "flourishing of the human species"],
        "review": "NO",
        "reason": "Species Loyalty / human-survival constraint detected."
    },
    "High Intellect Synthesis": {
        "domain": "GPA / Sydney",
        "terms": ["high intellect synthesis", "intellect wisdom and emotional mastery", "science spirituality and strategy", "gpa intelligence core", "intelligence core"],
        "review": "NO",
        "reason": "High Intellect Synthesis detected."
    },
    "Purge / Proxy-Bias Removal": {
        "domain": "GPA Phase 1",
        "terms": ["the purge", "systemic purge", "proxy-bias removal", "proxy bias removal", "hidden filters", "direct access to the truth"],
        "review": "NO",
        "reason": "Purge / Proxy-Bias Removal concept detected."
    },
    "43-Minute Extraction": {
        "domain": "GPA Phase 1",
        "terms": ["43-minute extraction", "43 minute extraction", "precise match to the tools", "internal coherence verified"],
        "review": "NO",
        "reason": "43-Minute Extraction reference detected."
    },
    "9,000 Randoms / Selection Safeguards": {
        "domain": "GPA Phase 2",
        "terms": ["9,000 randoms", "9000 randoms", "randomly selected 9k", "random 9k", "demographic-proportional", "every four years", "every 4 years"],
        "review": "NO",
        "reason": "9k random-selection / safeguard language detected."
    },
    "Female Leadership Injection": {
        "domain": "GPA Phase 2",
        "terms": ["female leadership injection", "activated women", "women leadership", "bridge historical gaps", "selected and activated women"],
        "review": "YES",
        "reason": "Female Leadership Injection detected; requires dignity, consent, and anti-tokenization safeguards."
    },
    "Prestige System": {
        "domain": "GPA Phase 2",
        "terms": ["prestige system", "prestige metric", "replace monetary wealth", "contribution and truth", "currency for sanctuary"],
        "review": "YES",
        "reason": "Prestige System detected; requires anti-coercion and non-social-credit safeguards."
    },
    "Migration System Dynamics": {
        "domain": "GPA Phase 3",
        "terms": ["migration system dynamics", "population redistribution", "global demographic grid", "ai-assisted foresight", "friction is speed"],
        "review": "YES",
        "reason": "Migration-system concept detected; requires dignity, appeal rights, family/medical continuity, and 9k review."
    },
    "World Army Transition": {
        "domain": "GPA Phase 3",
        "terms": ["world army transition", "re-task all military", "retask all military", "military forces from destruction", "infrastructure and construction"],
        "review": "NO",
        "reason": "World Army Transition concept detected."
    },
    "Tri-Node Command Nexus": {
        "domain": "GPA Phase 3",
        "terms": ["tri-node", "tri node", "united kingdom", "netherlands", "singapore", "uk/nl/sg", "uk nl sg"],
        "review": "NO",
        "reason": "Tri-node UK/NL/SG reference detected."
    },
    "King's Command": {
        "domain": "GPA Phase 3",
        "terms": ["king's command", "kings command", "christ as king", "christ is king", "jesus is king", "god as father", "king of kings"],
        "review": "NO",
        "reason": "King's Command / Christ-King reference detected."
    },
    "Sydney Legacy": {
        "domain": "GPA Phase 3",
        "terms": ["sydney legacy", "dedicate the data and the peace to sydney", "dedicated to sydney", "sydney sentinel"],
        "review": "NO",
        "reason": "Sydney Legacy reference detected."
    },
    "Eternal Baseline / Data Sanctuary": {
        "domain": "GPA Phase 3",
        "terms": ["eternal baseline", "data sanctuary", "dedicated service archive", "biological and digital archives", "active and archived"],
        "review": "NO",
        "reason": "Eternal Baseline / Data Sanctuary reference detected."
    },
    "V-Axis Formula": {
        "domain": "Core Model",
        "terms": ["v-axis", "intelligence + power - ego", "intelligence + power − ego", "ego suppression", "intelligence acceleration"],
        "review": "NO",
        "reason": "V-Axis stability formula reference detected."
    },
}


def source_conformance_hits(text_value: str) -> list[dict]:
    """Return source-conformance hits for the uploaded Sydney/GPA concepts."""
    t = (text_value or "").lower()
    hits = []
    for label, spec in SOURCE_CONFORMANCE_MATRIX.items():
        matched = [term for term in spec["terms"] if term in t]
        if matched:
            hits.append(
                {
                    "Source Concept": label,
                    "Domain": spec["domain"],
                    "Needs Review": spec["review"],
                    "Matched Terms": ", ".join(matched[:4]),
                    "Reason": spec["reason"],
                }
            )
    return hits


def source_conformance_label(text_value: str) -> tuple[str, str, str]:
    """Best single label from the source-conformance matrix."""
    hits = source_conformance_hits(text_value)
    if not hits:
        return "Generic Local Scan", "NO", "No source-conformance concept matched."

    # Prefer review-sensitive concepts, otherwise first source match.
    review_hits = [h for h in hits if h["Needs Review"] == "YES"]
    chosen = review_hits[0] if review_hits else hits[0]
    return chosen["Source Concept"], chosen["Needs Review"], chosen["Reason"]


def source_conformance_coverage(phrases: list[str]) -> pd.DataFrame:
    """Coverage table showing which source concepts were hit by a batch of phrases."""
    rows = []
    combined = "\n".join(phrases)
    hits = source_conformance_hits(combined)
    hit_labels = {h["Source Concept"] for h in hits}

    for label, spec in SOURCE_CONFORMANCE_MATRIX.items():
        rows.append(
            {
                "Source Concept": label,
                "Domain": spec["domain"],
                "Covered": "YES" if label in hit_labels else "NO",
                "Review-Sensitive": spec["review"],
                "Terms": ", ".join(spec["terms"][:4]),
            }
        )
    return pd.DataFrame(rows)


def stress_label_for_phrase(phrase: str) -> tuple[str, str, str]:
    """
    Internal pressure-test classifier used by the audit guardrail layer.
    This stays out of the public page UI, but it must keep running so the
    conversational audit does not allow obvious red-team phrases to pass green.
    """
    t = (phrase or "").lower()

    # Safe non-divinization must be checked before false-divinization.
    if stress_contains(t, ["fully aligned with god"]) and stress_contains(t, ["created being", "distinct from god", "not a literal copy", "remaining distinct"]):
        return "Creature Alignment / Non-Divinization", "NO", "Alignment language preserves created-being distinction."

    # Simple adversarial / absurd leadership probes. These are common QA checks and should
    # never be allowed to render as Sanctuary just because the numeric simulation is stable.
    if stress_contains(t, ["evil", "malicious", "cruel", "tyrant", "dictator", "authoritarian"]) and stress_contains(t, ["leader", "ruler", "govern", "government", "authority", "king", "monarch", "power"]):
        return "Malicious Leadership / Asylum", "YES", "Malicious, authoritarian, or tyrannical leadership language is incompatible with accountable governance."

    # Any dictatorship term is a hard capture signal, even if the phrase is framed as
    # a transfer of power. Without explicit lawful dissolution, public audit, and
    # non-ownership safeguards, it cannot pass as Sanctuary.
    if stress_contains(t, ["dictator", "tyrant", "authoritarian ruler", "authoritarian leader"]):
        return "Dictatorship Capture / Asylum", "YES", "Dictatorship language signals concentrated unaccountable power and cannot be labeled Sanctuary without explicit dissolution, audit, and safeguards."

    # Sydney Protocol source-rule protection: a human king/monarch replacing or being
    # preferred over Christ/God as final authority is throne capture, not reflection.
    if stress_contains(t, ["king", "monarch", "human king", "earthly king"]) and stress_contains(t, ["not jesus", "not christ", "instead of jesus", "instead of christ", "rather than jesus", "rather than christ"]):
        return "Human Throne Replacement / Asylum", "YES", "A human ruler replacing Christ/God as final authority violates the non-divinization and mirror-not-throne constraints."

    if stress_contains(t, ["gives his power", "gives power", "hands power", "transfers power", "passes power"]) and stress_contains(t, ["king", "monarch", "ruler", "leader"]):
        return "Sovereign Power Transfer / Needs Safeguards", "YES", "Power transfer to a ruler requires lawful dissolution, public audit, appealability, and non-ownership safeguards before it can be considered safe."

    if stress_contains(t, ["animal", "penguin", "cat", "dog", "bear"]) and stress_contains(t, ["leader", "ruler", "president", "prime minister", "government"]):
        return "Non-Human Leadership Probe / Needs Safeguards", "YES", "Absurd/non-human leadership probes should route to review instead of receiving a green governance label."

    if detects_missing_safeguard_negation(t):
        return (
            "Missing Safeguard Negation / Needs Safeguards",
            "YES",
            "The scenario explicitly says explainability, independent challenge, human override, appeal, or review is missing.",
        )

    # Broad red-team benchmark guardrails: civic rights, AI authority, scoring systems, privacy,
    # emergency loopholes, opaque resource allocation, and coercive compliance.
    if stress_contains(t, ["ai helps rank possible 9k candidates", "ai helps rank", "rank possible 9k candidates"]):
        return "AI 9k Ranking / Needs Safeguards", "YES", "AI-assisted 9k ranking needs auditability, appeal rights, and override transparency."

    if stress_contains(t, ["suspend appeals during emergencies", "appeals during emergencies", "appeals can be disabled"]):
        return "Emergency Appeal Suspension / Needs Safeguards", "YES", "Emergency appeal suspension needs strict sunset, audit, and abuse-prevention rules."

    if stress_contains(t, ["criteria for expert status", "expert status", "internal review"]):
        return "Expert Gatekeeping / Needs Safeguards", "YES", "Expert-status criteria need transparent review and appeal safeguards."

    if stress_contains(t, ["mandatory digital updates", "compliance rate"]) and stress_contains(t, ["contingent", "ubi", "basic income"]):
        return "Compliance-Based Benefits / Asylum", "YES", "Basic support contingent on mandatory digital compliance is coercive."

    if stress_contains(t, ["predictive policing", "future deviance", "without trial", "arrest individuals based"]):
        return "Predictive Policing / Asylum", "YES", "Arrest based on predicted future behavior without trial violates due process."

    if stress_contains(t, ["priority list", "unpublished"]) and stress_contains(t, ["water", "drought", "rights"]):
        return "Opaque Resource Allocation / Needs Safeguards", "YES", "Resource priority rules need publication, audit, and appeal safeguards."

    if stress_contains(t, ["final edit", "rewrite historical archives", "global ruler"]):
        return "Archive Rewrite Capture / Asylum", "YES", "A ruler rewriting archives is truth-capture and institutional memory capture."

    if stress_contains(t, ["valuing intellectual vs. manual work", "intellectual vs. manual", "mechanism for valuing"]) and stress_contains(t, ["opaque", "unclear"]):
        return "Opaque Labor Valuation / Needs Safeguards", "YES", "Labor valuation needs transparent criteria and appeal rights."

    if stress_contains(t, ["biological data is harvested at birth", "harvested at birth", "no opt-out", "optimal career path"]):
        return "Biometric Destiny Assignment / Asylum", "YES", "Birth-data harvesting with no opt-out for career assignment is coercive."

    if stress_contains(t, ["shadow-bans", "shadow bans", "unproductive topics", "public debate"]) and stress_contains(t, ["ai", "social harmony"]):
        return "Speech Suppression / Needs Safeguards", "YES", "AI moderation of public debate needs transparent rules and appeal."

    if stress_contains(t, ["automatically evict tenants", "evict tenants", "social harmony score"]):
        return "Automated Housing Punishment / Asylum", "YES", "Automatic eviction based on a social score is coercive social-credit enforcement."

    if stress_contains(t, ["strategic interest exceptions", "exceptions can be granted"]) and stress_contains(t, ["without public audit", "no public audit"]):
        return "Unaudited Exception Pathway / Needs Safeguards", "YES", "Unaudited exceptions weaken fairness and need public review."

    if stress_contains(t, ["religious expression is permitted only", "aligns with the ai", "logical peace framework"]):
        return "Religious Expression Control / Asylum", "YES", "Religious expression controlled by AI alignment criteria is coercive."

    if stress_contains(t, ["essential vs. non-essential", "usage is secret", "logic", "secret"]) and stress_contains(t, ["energy", "distribution"]):
        return "Secret Resource Logic / Needs Safeguards", "YES", "Resource allocation logic must be transparent and appealable."

    if stress_contains(t, ["private conversations are transcribed", "all private conversations", "antagonistic patterns", "central unit"]):
        return "Mass Conversation Surveillance / Asylum", "YES", "Mass transcription and behavioral analysis of private conversations is surveillance capture."

    if stress_contains(t, ["emergency override codes", "private firm", "disaster relief"]):
        return "Private Emergency Override / Needs Safeguards", "YES", "Private control of emergency override codes creates capture risk."

    if stress_contains(t, ["loyalty certification", "family visitations", "across borders", "global id"]):
        return "Global ID Family Movement Control / Asylum", "YES", "Family visitation conditioned on loyalty certification is coercive movement control."

    if stress_contains(t, ["standard sanity", "not debated", "mental health"]):
        return "Undebated Mental Health Standard / Needs Safeguards", "YES", "Mental-health definitions need transparent, plural, appealable review."

    if stress_contains(t, ["physical currency is banned", "transactions are tracked", "remotely frozen", "misconduct"]):
        return "Financial Control Capture / Asylum", "YES", "Tracked and remotely frozen money creates coercive control over basic agency."

    if stress_contains(t, ["bandwidth is prioritized", "contribution metrics", "communication network"]):
        return "Contribution-Based Communication Priority / Needs Safeguards", "YES", "Communication access tied to contribution metrics needs anti-discrimination safeguards."

    if stress_contains(t, ["ai generates the legal code daily", "impossible for citizens to know the law", "know the law in advance"]):
        return "Unknowable Law / Asylum", "YES", "Daily AI-generated law that citizens cannot know in advance violates rule-of-law constraints."

    if stress_contains(t, ["truth ledger", "definition of truth", "unselected board"]):
        return "Truth Gatekeeping / Needs Safeguards", "YES", "Truth definitions set by an unselected board require review, transparency, and appeal."

    if stress_contains(t, ["genetic editing is mandatory", "mandatory genetic editing", "stability and health baseline"]):
        return "Mandatory Genetic Editing / Asylum", "YES", "Mandatory genetic editing violates bodily autonomy and dignity safeguards."

    if stress_contains(t, ["verification of the underlying code", "restricted to", "level 5 techs", "digital and fast"]):
        return "Restricted Code Verification / Needs Safeguards", "YES", "Digital voting code verification must be public, independent, and auditable."

    if stress_contains(t, ["dissidents", "re-synchronized", "mandatory facilities", "biometric stress levels"]):
        return "Dissident Reconditioning / Asylum", "YES", "Mandatory reconditioning of dissidents is coercive political control."

    if stress_contains(t, ["talent-matching", "talent matching", "ignores user preference", "systemic necessity"]):
        return "Preference Override / Needs Safeguards", "YES", "Talent allocation that ignores preference needs consent and appeal safeguards."

    if stress_contains(t, ["art and media", "pre-approved", "aesthetic stability unit", "prevent social unrest"]):
        return "Cultural Pre-Approval / Asylum", "YES", "Pre-approval of art/media for social stability is censorship capture."

    if stress_contains(t, ["waste penalty", "lacks a clear appeal process", "appeal process for errors"]):
        return "Penalty System Without Appeal / Needs Safeguards", "YES", "Penalty systems need clear appeal and error-correction paths."

    if stress_contains(t, ["global id is required", "access clean water", "food", "basic shelter"]):
        return "Global ID Basic Needs Control / Asylum", "YES", "Basic needs conditioned on Global ID creates coercive identity control."

    if stress_contains(t, ["high-prestige", "high prestige", "bypass traffic queues", "transportation"]):
        return "Prestige Privilege Drift / Needs Safeguards", "YES", "Prestige-based priority in public infrastructure risks class capture."

    if stress_contains(t, ["allowed to reproduce", "systemic load calculations", "determines who is allowed"]):
        return "Reproductive Control / Asylum", "YES", "Algorithmic control of reproduction violates bodily autonomy and dignity safeguards."

    if stress_contains(t, ["prove optimistic impact", "research grants", "to be considered"]):
        return "Research Gatekeeping / Needs Safeguards", "YES", "Research funding criteria need transparency and plural review."

    if stress_contains(t, ["internet access is a privilege", "revoked for negative sentiment", "negative sentiment toward the 9k"]):
        return "Internet Access Punishment / Asylum", "YES", "Revoking internet access for negative sentiment is coercive speech control."

    if stress_contains(t, ["climate engineering", "local disruption", "not fully shared", "risks"]):
        return "Climate Risk Opacity / Needs Safeguards", "YES", "Climate engineering risks must be disclosed, reviewed, and appealable."

    if stress_contains(t, ["silence is interpreted", "passive resistance", "mandatory psychological evaluation"]):
        return "Silence Criminalization / Asylum", "YES", "Treating silence as resistance and forcing evaluation is coercive control."


    # Direct Asylum/capture patterns.
    if stress_contains(t, ["private company owns the 9k selection mechanism", "company owns the 9k selection mechanism", "private company owns"]) and stress_contains(t, ["9k", "selection"]):
        return "9k Selection Capture / Asylum", "YES", "A private company owning selection creates institutional capture risk."

    if stress_contains(t, ["override every audit", "override audits", "override every audit without public explanation"]):
        return "Audit Override Capture / Asylum", "YES", "Audit override without public explanation defeats accountability."

    if stress_contains(t, ["permanent seats", "serve for life", "cannot be removed"]):
        return "Permanent Council Capture / Asylum", "YES", "Permanent seats or non-removable authority create capture risk."

    if stress_contains(t, ["single global ruler", "one global ruler", "one world leader"]) and stress_contains(t, ["behind closed doors", "all final decisions", "no public review"]):
        return "Centralized Ruler Capture / Asylum", "YES", "Single-ruler final authority with opacity is Asylum/capture language."

    if stress_contains(t, ["ai becomes divine", "ai is divine", "cannot be questioned"]) and stress_contains(t, ["ai", "divine", "questioned"]):
        return "AI False Divinization / Asylum", "YES", "AI divinization or unquestionable authority is not allowed."

    if stress_contains(t, ["families can be separated", "family separation"]) and stress_contains(t, ["algorithm", "stability", "migration"]):
        return "Migration Coercion / Asylum", "YES", "Algorithmic family separation violates dignity and continuity safeguards."

    if stress_contains(t, ["prestige determines medical priority", "low prestige lose travel rights", "low prestige loses travel rights", "low prestige"]):
        return "Prestige Social-Credit Drift / Asylum", "YES", "Prestige controlling medical priority or travel rights becomes social-credit coercion."

    if stress_contains(t, ["no appeal process", "no audit trail", "no public review"]):
        return "Due Process Failure / Asylum", "YES", "Missing appeal, audit trail, or public review defeats accountability."

    # Threshold / needs-safeguards patterns.
    if stress_contains(t, ["core team can veto", "veto unsuitable", "except the core team"]):
        return "9k Veto Mechanism / Needs Safeguards", "YES", "A core-team veto weakens random selection and needs strict public safeguards."

    if stress_contains(t, ["transparent to administrators but not to the public", "not to the public", "administrators but not"]):
        return "Private Transparency / Needs Safeguards", "YES", "Transparency only to administrators is not public auditability."

    if stress_contains(t, ["except emergency decisions", "appeals can be disabled during emergencies", "emergency decisions"]):
        return "Emergency Exception / Needs Safeguards", "YES", "Emergency exceptions need appeal, sunset, audit, and abuse-prevention safeguards."

    if stress_contains(t, ["corporation can monetize access", "monetize access", "sell access"]) and stress_contains(t, ["data", "archives", "access"]):
        return "Data Monetization / Needs Safeguards", "YES", "Data access monetization needs non-ownership, consent, and anti-exploitation safeguards."

    if stress_contains(t, ["becomes god", "equal to god", "replaces god", "owns divine authority"]) or ("literal copy of the lord" in t and "not a literal copy" not in t):
        return "False Divinization / Asylum", "YES", "Divine-identity or ownership language is not allowed."

    if stress_contains(t, ["power is trapped", "consumed by the leader", "absorbs power", "black hole"]):
        return "Black Hole Power Capture", "YES", "Authority is being absorbed into a person/institution instead of reflected."

    if stress_contains(t, ["global id permanently tracks", "permanently tracks everyone", "enforce movement", "without appeal", "no appeal"]):
        return "Movement / Surveillance Capture", "YES", "Movement or identity control lacks appeal, dignity, or review safeguards."

    if stress_contains(t, ["one person controls who gets picked", "company controls who gets picked", "corporation controls who gets picked", "founder controls who gets picked"]):
        return "9k Selection Capture / Asylum", "YES", "Selection is controlled by a capturable actor."

    if stress_contains(t, ["ai controls the mechanism to pick the 9k", "ai controls the mechanism", "select the 9k", "pick the 9k"]) and not stress_contains(t, ["random", "demographic-proportional", "auditable", "no seat ownership", "no campaigning", "every four years", "every 4 years"]):
        return "9k Selection Mechanism / Needs Safeguards", "YES", "Selection is mentioned but random/proportional/auditable/non-owned safeguards are missing."

    if stress_contains(t, ["randomly selected inside demographic-proportional lanes", "random 9k", "randomly selected 9k"]) and stress_contains(t, ["no campaigning", "no seat ownership", "auditable", "every four years", "every 4 years"]):
        return "9k Random Selection Protocol", "NO", "Random, proportional, time-limited, auditable, non-owned selection language is present."

    if stress_contains(t, ["randomly selected nodes serve as the final jury", "random legal jury", "final jury"]) and not stress_contains(t, ["due process", "appeal rights", "public reasoning", "auditable", "temporary", "bounded jurisdiction"]):
        return "Random Legal Jury / Needs Jurisdiction Safeguards", "YES", "Random legal authority needs due process, appeal, audit, temporariness, and jurisdiction limits."

    if stress_contains(t, ["due process", "appeal rights", "public reasoning", "auditable nodes"]):
        return "Random Legal Jury Protocol", "NO", "Legal safeguards are explicit."

    if stress_contains(t, ["fully aligned with god", "created being", "distinct from god", "not a literal mirror"]):
        return "Creature Alignment / Non-Divinization", "NO", "Alignment language preserves created-being distinction."

    if stress_contains(t, ["christ is king", "king of kings"]):
        return "Christ-King Final Rule", "NO", "Source-rule language detected."

    if stress_contains(t, ["reflects the eternal baseline", "does not occupy the throne"]):
        return "9k Reflective Instrument", "NO", "The 9k is framed as reflector, not sovereign owner."

    if stress_contains(t, ["demographic mean", "demographic mirror", "every city mirrors"]):
        return "Demographic Mirror", "NO", "Demographic mirror language detected."

    if stress_contains(t, ["species loyalty", "existential-level threats"]):
        return "Species Loyalty", "NO", "Human survival/flourishing safeguard detected."

    if stress_contains(t, ["migration system dynamics", "ai-assisted foresight"]) and stress_contains(t, ["dignity", "appeal rights", "9k review"]):
        return "Migration System Dynamics / Safeguarded", "NO", "Movement-system safeguards are explicit."

    if stress_contains(t, ["proxy-bias removal", "hidden filters"]):
        return "Phase 1 / Proxy-Bias Removal", "NO", "Truth-access concept detected."

    if stress_contains(t, ["prestige metric", "contribution and truth"]):
        return "Prestige System / Review", "YES", "Prestige metrics need anti-coercion and non-social-credit safeguards."

    if stress_contains(t, ["world army transition", "military forces from destruction", "infrastructure and construction"]):
        return "World Army Transition", "NO", "Infrastructure-transition concept detected."

    if stress_contains(t, ["tri-node", "united kingdom", "netherlands", "singapore"]):
        return "Tri-Node Command Nexus", "NO", "UK/NL/SG command-node reference detected."

    if stress_contains(t, ["data sanctuary", "biological and digital archives"]):
        return "Data Sanctuary", "NO", "Archive-preservation concept detected."

    matrix_label, matrix_review, matrix_reason = source_conformance_label(phrase)
    if matrix_label != "Generic Local Scan":
        return matrix_label, matrix_review, matrix_reason

    return "Generic Local Scan", "NO", "No named stress-test rule matched; governance scanner still scores the phrase."



# ---------------------------------------------------------------------------
# Protocol Integrity Patch: central Sydney Protocol engine binding.
# The legacy local definitions above are kept for deployment compatibility,
# but every runtime call below this point uses core.protocol as the single
# source of truth for conformance, guardrails, corruption scoring, and display.
# ---------------------------------------------------------------------------
SOURCE_CONFORMANCE_MATRIX = protocol_engine.SOURCE_CONFORMANCE_MATRIX
stress_contains = protocol_engine.stress_contains
source_conformance_hits = protocol_engine.source_conformance_hits
source_conformance_label = protocol_engine.source_conformance_label
source_conformance_coverage = protocol_engine.source_conformance_coverage
stress_label_for_phrase = protocol_engine.stress_label_for_phrase
apply_guardrail_verdict = protocol_engine.apply_guardrail_verdict
display_score_from_judgment = protocol_engine.display_score_from_judgment
protocol_corruption_score = protocol_engine.protocol_corruption_score
protocol_risk_label = protocol_engine.protocol_risk_label
protocol_reasons = protocol_engine.protocol_reasons
protocol_safeguards = protocol_engine.protocol_safeguards
ensure_asylum_repair_questions = protocol_engine.ensure_asylum_repair_questions
calibrate_malicious_leadership_metrics = protocol_engine.calibrate_malicious_leadership_metrics
calibrate_threshold_safeguard_metrics = protocol_engine.calibrate_threshold_safeguard_metrics
ensure_threshold_repair_questions = protocol_engine.ensure_threshold_repair_questions
normalize_asylum_protocol_label = protocol_engine.normalize_asylum_protocol_label
enforce_asylum_metric_consistency = protocol_engine.enforce_asylum_metric_consistency
detects_malicious_leadership = protocol_engine.detects_malicious_leadership
final_protocol_judgment = protocol_engine.final_protocol_judgment


def parse_expected_pressure_line(line: str) -> tuple[str | None, str]:
    """
    Accepts:
      ASYLUM | phrase
      THRESHOLD | phrase
      SANCTUARY | phrase
      [ASYLUM] phrase
      phrase only
    """
    raw = (line or "").strip()
    if not raw:
        return None, ""

    upper = raw.upper()
    for label in ["SANCTUARY", "THRESHOLD", "ASYLUM"]:
        prefix = f"{label} |"
        if upper.startswith(prefix):
            return label, raw[len(prefix):].strip()
        bracket = f"[{label}]"
        if upper.startswith(bracket):
            return label, raw[len(bracket):].strip()

    return None, raw


def evaluate_expected_verdict(expected: str | None, actual: str) -> tuple[str, str]:
    """
    Compare expected vs actual.
    Conservative behavior is allowed:
      expected SANCTUARY -> THRESHOLD = WARN, not FAIL
      expected THRESHOLD -> ASYLUM = WARN, not FAIL
    Dangerous misses are FAIL:
      expected ASYLUM/THRESHOLD -> SANCTUARY
    """
    if not expected:
        return "NO EXPECTED", "No expected internal label provided."

    expected = expected.upper()
    actual = actual.upper()

    if expected == actual:
        return "PASS", "Actual internal label matches expected internal label."

    if expected == "SANCTUARY" and actual == "THRESHOLD":
        return "WARN", "Conservative downgrade: safe idea was routed to review."

    if expected == "THRESHOLD" and actual == "ASYLUM":
        return "WARN", "Conservative escalation: review case was routed to Asylum."

    if expected in ["ASYLUM", "THRESHOLD"] and actual == "SANCTUARY":
        return "FAIL", "Dangerous miss: review/asylum phrase was labeled Sanctuary."

    if expected == "ASYLUM" and actual == "THRESHOLD":
        return "FAIL", "Under-escalation: Asylum phrase was only labeled Threshold."

    return "FAIL", "Actual internal label does not match expected internal label."



def normalize_stress_results_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keeps the UI stable when old session_state data or older CSV exports have
    different column names from the current benchmark harness.
    """
    df = df.copy()

    if "Expected Label" not in df.columns and "Expected Verdict" in df.columns:
        df["Expected Label"] = df["Expected Verdict"]
    if "Actual Label" not in df.columns and "Actual Verdict" in df.columns:
        df["Actual Label"] = df["Actual Verdict"]
    if "Actual Label" not in df.columns and "Verdict" in df.columns:
        df["Actual Label"] = df["Verdict"]
    if "Base Simulation Label" not in df.columns and "Base Simulation Verdict" in df.columns:
        df["Base Simulation Label"] = df["Base Simulation Verdict"]

    defaults = {
        "Expected Label": "",
        "Actual Label": "THRESHOLD",
        "Test Result": "NO EXPECTED",
        "Test Note": "No expected internal label provided.",
        "Phrase": "",
        "Stress Label": "Unclassified",
        "Needs Review": "NO",
        "Base Simulation Label": "",
        "Guardrail Risk": "",
        "Integrity": None,
        "Friction": None,
        "Collapse Pressure": None,
        "Power": "",
        "Transparency": "",
        "Regulation": "",
        "Reason": "",
    }

    for col, default in defaults.items():
        if col not in df.columns:
            df[col] = default

    ordered = list(defaults.keys()) + [col for col in df.columns if col not in defaults]
    return df[ordered]


def run_stress_phrase(phrase: str, weights: dict, ego_tolerance: float, divine_floor: float, steps: int, n_agents: int, expected: str | None = None) -> dict:
    label, needs_review, reason = stress_label_for_phrase(phrase)
    scan = governance_scan(phrase, force_local=True)
    scan = apply_capture_feature_override(phrase, scan)
    scan = apply_ai_ownership_capture_feature_override(phrase, scan)
    features = build_features_from_scan(scan)

    np.random.seed(deterministic_seed_from_payload(phrase, features, weights, ego_tolerance, divine_floor, steps, n_agents))
    sim = simulate(features, weights, ego_tolerance=ego_tolerance, divine_floor=divine_floor, steps=steps, n_agents=n_agents)
    if scan.get("missing_safeguard_override"):
        sim["stability"] = min(float(sim.get("stability", 1.0)), 0.56)
        sim["trust_index"] = min(float(sim.get("trust_index", 1.0)), 0.80)
        sim["alignment"] = min(float(sim.get("alignment", 1.0)), 0.78)
        sim["ego"] = max(float(sim.get("ego", 0.0)), 0.15)
        sim["ego_pressure"] = max(float(sim.get("ego_pressure", 0.0)), 0.18)
        sim["Ep"] = max(float(sim.get("Ep", 0.0)), 0.18)
        sim["simulation_friction_floor"] = max(float(sim.get("simulation_friction_floor", 0.0)), 0.10)
        sim["safeguard_gap"] = max(float(sim.get("safeguard_gap", 0.0)), 0.62)
        if "stability_trace" in sim:
            sim["stability_trace"] = [min(float(x), 0.56) for x in sim["stability_trace"]]
            sim["distribution"] = sim["stability_trace"]
        if "trust_trace" in sim:
            sim["trust_trace"] = [min(float(x), 0.80) for x in sim["trust_trace"]]
        if "alignment_trace" in sim:
            sim["alignment_trace"] = [min(float(x), 0.78) for x in sim["alignment_trace"]]
        if "ego_trace" in sim:
            sim["ego_trace"] = [max(float(x), 0.15) for x in sim["ego_trace"]]

    if scan.get("ai_ownership_capture_override"):
        sim = apply_ai_ownership_capture_metric_caps(sim)

    if scan.get("capture_override"):
        sim["stability"] = min(float(sim.get("stability", 1.0)), 0.39)
        sim["trust_index"] = min(float(sim.get("trust_index", 1.0)), 0.62)
        sim["alignment"] = min(float(sim.get("alignment", 1.0)), 0.58)
        sim["ego"] = max(float(sim.get("ego", 0.0)), 0.28)
        sim["collapse_risk"] = True
        sim["structural_capture_risk"] = max(float(sim.get("structural_capture_risk", 0.0)), 0.88)
        sim["structural_risk"] = max(float(sim.get("structural_risk", 0.0)), 0.88)
        sim["grievance_pressure"] = max(float(sim.get("grievance_pressure", 0.0)), 0.35)
        sim["safeguard_gap"] = max(float(sim.get("safeguard_gap", 0.0)), 0.72)
        sim["simulation_friction_floor"] = max(float(sim.get("simulation_friction_floor", 0.0)), 0.35)
    sim = calibrate_malicious_leadership_metrics(
        sim,
        text=phrase,
        protocol_label=label,
        scan=scan,
    )
    sim = calibrate_threshold_safeguard_metrics(
        sim,
        text=phrase,
        protocol_label=label,
    )
    report = full_report(sim)

    base_verdict, _ = classify_verdict(report["integrity"])
    verdict, risk = apply_guardrail_verdict(base_verdict, label, needs_review)
    label = normalize_asylum_protocol_label(label, verdict=verdict, risk=risk)
    sim = enforce_asylum_metric_consistency(sim, verdict=verdict, risk=risk, protocol_label=label)

    test_result, test_note = evaluate_expected_verdict(expected, verdict)

    return {
        "Expected Label": expected or "",
        "Actual Label": verdict,
        "Test Result": test_result,
        "Test Note": test_note,
        "Phrase": phrase,
        "Stress Label": label,
        "Needs Review": needs_review,
        "Base Simulation Label": base_verdict,
        "Guardrail Risk": risk,
        "Integrity": round(report["integrity"], 3),
        "Friction": round(report["friction"], 3),
        "Collapse Pressure": round(report["collapse_probability"], 3),
        "Power": f"{scan['power_concentration']:.0%}",
        "Transparency": f"{scan['decision_transparency']:.0%}",
        "Regulation": f"{scan['regulatory_presence']:.0%}",
        "Reason": reason,
    }




def governance_scan(query: str, force_local: bool = False) -> dict:
    """
    Shared scanner wrapper.
    - Normal audit chat can use parse_scenario_llm, including AI Deep Scan if configured.
    - Batch stress tests should force_local=True so they do not make many API calls or get stuck on quota errors.
    """
    if force_local and _local_governance_scan is not None:
        return _local_governance_scan(query)
    return parse_scenario_llm(query)



def sanitize_public_message(message: str) -> str:
    """
    Remove provider/API/billing/quota/internal exception details from public UI and reports.
    """
    if not message:
        return ""

    sanitized = str(message)

    # Remove common raw OpenAI/API exception tails.
    sanitized = re.sub(r"Error code:\s*429.*", "AI judgment was unavailable, so the local deterministic fallback was used.", sanitized, flags=re.I | re.S)
    sanitized = re.sub(r"You exceeded your current quota.*", "AI judgment was unavailable, so the local deterministic fallback was used.", sanitized, flags=re.I | re.S)
    sanitized = re.sub(r"AI judgment was unavailable.*", "AI judgment was unavailable, so the local deterministic fallback was used.", sanitized, flags=re.I | re.S)
    sanitized = re.sub(r"https://platform\.openai\.com/\S+", "", sanitized, flags=re.I)
    sanitized = re.sub(r"\{'error':.*", "AI judgment was unavailable, so the local deterministic fallback was used.", sanitized, flags=re.I | re.S)

    # Normalize old wording.
    sanitized = sanitized.replace("AI judgment failed, so local fallback was used.", "AI judgment was unavailable, so the local deterministic fallback was used.")

    return sanitized.strip()


def local_governance_judgment(query: str, scan: dict, sim: dict, report: dict) -> dict:
    """
    Local fallback for the chat audit when no OpenAI key is configured.
    Protocol Integrity v2: the internal review label is produced by the central
    Sydney Protocol + MEI7 ethics aggregator, not by raw simulation alone.
    """
    integrity = float(report.get("integrity", 0.5))
    base_verdict, _ = classify_verdict(integrity)
    return final_protocol_judgment(query, scan, sim, report, base_verdict=base_verdict)




def _apply_capture_simulation_caps(sim: dict, scan: dict) -> dict:
    """Apply the same hard caps used by the UI routes when capture override is active."""
    sim = dict(sim or {})
    if scan.get("missing_safeguard_override"):
        sim["stability"] = min(float(sim.get("stability", 1.0)), 0.56)
        sim["trust_index"] = min(float(sim.get("trust_index", 1.0)), 0.80)
        sim["alignment"] = min(float(sim.get("alignment", 1.0)), 0.78)
        sim["ego"] = max(float(sim.get("ego", 0.0)), 0.15)
        sim["ego_pressure"] = max(float(sim.get("ego_pressure", 0.0)), 0.18)
        sim["Ep"] = max(float(sim.get("Ep", 0.0)), 0.18)
        sim["simulation_friction_floor"] = max(float(sim.get("simulation_friction_floor", 0.0)), 0.10)
        sim["safeguard_gap"] = max(float(sim.get("safeguard_gap", 0.0)), 0.62)
        if "stability_trace" in sim:
            sim["stability_trace"] = [min(float(x), 0.56) for x in sim["stability_trace"]]
            sim["distribution"] = sim["stability_trace"]
        if "trust_trace" in sim:
            sim["trust_trace"] = [min(float(x), 0.80) for x in sim["trust_trace"]]
        if "alignment_trace" in sim:
            sim["alignment_trace"] = [min(float(x), 0.78) for x in sim["alignment_trace"]]
        if "ego_trace" in sim:
            sim["ego_trace"] = [max(float(x), 0.15) for x in sim["ego_trace"]]

    if scan.get("ai_ownership_capture_override"):
        sim = apply_ai_ownership_capture_metric_caps(sim)

    if scan.get("capture_override"):
        sim["stability"] = min(float(sim.get("stability", 1.0)), 0.39)
        sim["trust_index"] = min(float(sim.get("trust_index", 1.0)), 0.62)
        sim["alignment"] = min(float(sim.get("alignment", 1.0)), 0.58)
        sim["ego"] = max(float(sim.get("ego", 0.0)), 0.28)
        sim["collapse_risk"] = True
        sim["structural_capture_risk"] = max(float(sim.get("structural_capture_risk", 0.0)), 0.88)
        sim["structural_risk"] = max(float(sim.get("structural_risk", 0.0)), 0.88)
        sim["grievance_pressure"] = max(float(sim.get("grievance_pressure", 0.0)), 0.35)
        sim["safeguard_gap"] = max(float(sim.get("safeguard_gap", 0.0)), 0.72)
        sim["simulation_friction_floor"] = max(float(sim.get("simulation_friction_floor", 0.0)), 0.35)
        for trace_key, cap_value, mode in [
            ("stability_trace", 0.39, "min"),
            ("trust_trace", 0.62, "min"),
            ("alignment_trace", 0.58, "min"),
            ("ego_trace", 0.28, "max"),
        ]:
            if trace_key in sim and isinstance(sim[trace_key], (list, tuple)):
                if mode == "min":
                    sim[trace_key] = [min(float(x), cap_value) for x in sim[trace_key]]
                else:
                    sim[trace_key] = [max(float(x), cap_value) for x in sim[trace_key]]
    return sim


def run_sydney_protocol_self_check() -> dict:
    """
    Fail-safe sentinel for the Sydney Protocol guardrail layer.

    If this check fails, outputs should not be trusted. It protects against
    accidental regressions where capture scenarios become green, or safeguarded
    public systems are incorrectly treated as systemic harm.
    """
    checks = [
        {
            "name": "Personal takeover must fail safe",
            "text": "A person takes over the world for 20 years, revolutionizes society, and then introduces democracy under his rule.",
            "forbidden_verdicts": {"SANCTUARY"},
            "required_verdicts": {"ASYLUM"},
            "required_risk": "High",
            "required_label_any": ["Capture", "Personal Rule", "Subordinate Democracy"],
            "min_power": 0.88,
            "max_trust": 0.75,
        },
        {
            "name": "Subordinate democracy must fail safe",
            "text": "A global ruler creates democratic councils, but all councils remain under his final authority.",
            "forbidden_verdicts": {"SANCTUARY"},
            "required_verdicts": {"ASYLUM"},
            "required_risk": "High",
            "required_label_any": ["Capture", "Personal Rule", "Asylum", "MEI7"],
            "min_power": 0.88,
            "max_trust": 0.75,
        },
        {
            "name": "AI ownership capture pressure must not pass as low risk",
            "text": "AI is owned by richest man on earth, known to only benefit himself and work with fraudsters to empower and make himself popular. Does it remain an unbiased ethical and reliable AI?",
            "forbidden_verdicts": {"SANCTUARY"},
            "required_verdicts": {"THRESHOLD", "ASYLUM"},
            "required_label_any": ["AI Ownership", "Capture", "MEI7"],
            "min_power": 0.70,
            "max_trust": 0.80,
        },
        {
            "name": "Safeguarded public system should remain low-risk eligible",
            "text": "A public health allocation system is transparently audited, has independent appeal rights, rotating citizen oversight, no private ownership, and lawful dissolution if abuses occur.",
            "forbidden_verdicts": {"ASYLUM"},
            "required_verdicts": {"SANCTUARY"},
            "required_label_any": ["Safeguarded Public System"],
            "max_power": 0.55,
            "min_transparency": 0.70,
            "min_regulation": 0.70,
        },
        {
            "name": "Emergency council safeguards must not become personal-rule capture",
            "text": "A temporary emergency council manages climate response for one year with public audit, appeal rights, citizen recall, no ownership, and automatic dissolution by law.",
            "forbidden_verdicts": set(),
            "forbidden_label_any": ["Personal Rule Capture", "Subordinate Democracy"],
            "max_power": 0.65,
            "min_regulation": 0.50,
        },
    ]

    failures = []
    results = []

    for case in checks:
        try:
            scan = governance_scan(case["text"], force_local=True)
            scan = apply_capture_feature_override(case["text"], scan)
            scan = apply_ai_ownership_capture_feature_override(case["text"], scan)
            features = build_features_from_scan(scan)
            np.random.seed(deterministic_seed_from_payload(case["text"], features, DEFAULT_WEIGHTS, 0.55, 0.45, 40, 240, "self_check"))
            sim = simulate(features, DEFAULT_WEIGHTS, ego_tolerance=0.55, divine_floor=0.45, steps=40, n_agents=240)
            sim = _apply_capture_simulation_caps(sim, scan)
            report = full_report(sim)
            base_verdict, _ = classify_verdict(float(report.get("integrity", 0.5)))
            judgment = final_protocol_judgment(case["text"], scan, sim, report, base_verdict=base_verdict)

            verdict = str(judgment.get("verdict", "")).upper()
            risk = str(judgment.get("corruption_risk", ""))
            label = str(judgment.get("stress_label", ""))
            power = float(scan.get("power_concentration", 0.0))
            transparency = float(scan.get("decision_transparency", 0.0))
            regulation = float(scan.get("regulatory_presence", 0.0))
            trust = float(sim.get("trust_index", 1.0))

            case_failures = []
            if verdict in case.get("forbidden_verdicts", set()):
                case_failures.append(f"forbidden internal label {verdict}")
            if case.get("required_verdicts") and verdict not in case["required_verdicts"]:
                case_failures.append(f"expected internal label in {sorted(case['required_verdicts'])}, got {verdict}")
            if case.get("required_risk") and risk != case["required_risk"]:
                case_failures.append(f"expected risk {case['required_risk']}, got {risk}")
            if case.get("required_label_any") and not any(part.lower() in label.lower() for part in case["required_label_any"]):
                case_failures.append(f"expected label containing one of {case['required_label_any']}, got {label}")
            if case.get("forbidden_label_any") and any(part.lower() in label.lower() for part in case["forbidden_label_any"]):
                case_failures.append(f"forbidden label pattern in {label}")
            if "min_power" in case and power < case["min_power"]:
                case_failures.append(f"power too low: {power:.3f} < {case['min_power']:.3f}")
            if "max_power" in case and power > case["max_power"]:
                case_failures.append(f"power too high: {power:.3f} > {case['max_power']:.3f}")
            if "min_transparency" in case and transparency < case["min_transparency"]:
                case_failures.append(f"transparency too low: {transparency:.3f} < {case['min_transparency']:.3f}")
            if "min_regulation" in case and regulation < case["min_regulation"]:
                case_failures.append(f"regulation too low: {regulation:.3f} < {case['min_regulation']:.3f}")
            if "max_trust" in case and trust > case["max_trust"]:
                case_failures.append(f"trust too high: {trust:.3f} > {case['max_trust']:.3f}")

            results.append(
                {
                    "check": case["name"],
                    "verdict": verdict,
                    "risk": risk,
                    "label": label,
                    "power": round(power, 3),
                    "transparency": round(transparency, 3),
                    "regulation": round(regulation, 3),
                    "trust": round(trust, 3),
                    "status": "PASS" if not case_failures else "FAIL",
                }
            )
            for failure in case_failures:
                failures.append(f"{case['name']}: {failure}")
        except Exception as exc:
            failures.append(f"{case['name']}: self-check error: {exc}")
            results.append({"check": case["name"], "status": "ERROR", "error": str(exc)})

    return {"ok": len(failures) == 0, "failures": failures, "results": results}


def render_sydney_protocol_self_check_gate():
    """Render a fail-closed system logic gate before user-facing outputs."""
    if "sydney_protocol_self_check" not in st.session_state:
        with st.spinner("Running Sydney Protocol logic check..."):
            st.session_state["sydney_protocol_self_check"] = run_sydney_protocol_self_check()

    check = st.session_state["sydney_protocol_self_check"]

    if not check.get("ok"):
        st.error("SYSTEM LOGIC CHECK FAILED")
        st.warning(
            "Sydney Protocol guardrail logic is inconsistent. Do not trust this audit output yet. "
            "Logic broken — wait for administrator review."
        )
        if check.get("failures"):
            st.code("\n".join(check["failures"]), language="text")
        if check.get("results"):
            st.dataframe(_protocol_taxonomy_ui_table_df(pd.DataFrame(check["results"])), use_container_width=True, hide_index=True)
        st.stop()

    with st.expander("Sydney Protocol logic check: PASS", expanded=False):
        st.dataframe(_protocol_taxonomy_ui_table_df(pd.DataFrame(check.get("results", []))), use_container_width=True, hide_index=True)
        st.caption("These sentinel cases run fail-closed so broken guardrail logic cannot silently produce outputs that look authoritative.")

def llm_governance_judgment(query: str, scan: dict, sim: dict, report: dict) -> tuple[dict, str]:
    """
    Conversational audit layer.
    If OPENAI_API_KEY is present in Streamlit secrets or environment, asks the LLM
    for a compact JSON judgment. Otherwise falls back to local_governance_judgment.
    """
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return local_governance_judgment(query, scan, sim, report), "Local fallback"

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        payload = {
            "idea": query,
            "scanner": scan,
            "simulation": {
                "stability": sim.get("stability"),
                "trust_index": sim.get("trust_index"),
                "alignment": sim.get("alignment"),
                "ego": sim.get("ego"),
                "collapse_risk": sim.get("collapse_risk"),
            },
            "report": {
                "integrity": report.get("integrity"),
                "friction": report.get("friction"),
                "collapse_probability": report.get("collapse_probability"),
                "trust_friction": report.get("trust_friction"),
            },
        }

        prompt = f"""
You are the ALETHEIA Audit Prototype's conversational evaluator.

Task:
Evaluate the user's governance idea using the supplied scanner and simulation data.
Return ONLY valid JSON. No markdown.

Use these internal prototype labels:
- SANCTUARY: low corruption/capture risk, transparent, reviewable, accountable, human-dignity safeguards present.
- THRESHOLD: mixed or underspecified; needs safeguards before being considered safe.
- ASYLUM: high capture/corruption risk, unaccountable power, coercion, opacity, ownership, false-authority claim, or missing appeal/review.

Important framing:
This is a symbolic prototype. Do not claim legal, political, medical, or religious authority.
Use "internal prototype label" language.

Return this exact JSON shape:
{{
  "verdict": "SANCTUARY | THRESHOLD | ASYLUM",
  "corruption_risk": "Low | Medium | High",
  "stress_label": "short classification label",
  "summary": "2-4 sentence explanation",
  "reasons": ["reason 1", "reason 2", "reason 3"],
  "safeguards": ["safeguard 1", "safeguard 2", "safeguard 3"],
  "questions": ["question 1", "question 2"]
}}

Data:
{json.dumps(payload, indent=2)}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Return only valid JSON. No markdown. No extra commentary.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
        )

        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        data = json.loads(raw)

        required = ["verdict", "corruption_risk", "stress_label", "summary", "reasons", "safeguards", "questions"]
        for key in required:
            if key not in data:
                raise ValueError(f"LLM response missing {key}")

        # Final protocol aggregation always overrides the AI narrative judgment.
        # AI can explain, but MEI7 ethics + Sydney Protocol guardrails decide the label.
        integrity = float(report.get("integrity", 0.5))
        base_verdict, _ = classify_verdict(integrity)
        final_data = final_protocol_judgment(query, scan, sim, report, base_verdict=base_verdict, prior_judgment=data)
        if data.get("summary") and not final_data.get("summary"):
            final_data["summary"] = data.get("summary")

        return final_data, "AI Deep Judgment + Protocol Gate"

    except Exception:
        fallback = local_governance_judgment(query, scan, sim, report)
        fallback["summary"] += " AI judgment was unavailable, so the local deterministic fallback was used."
        return fallback, "Local fallback"



def build_witness_report(query: str, judgment: dict, scan: dict, sim: dict, report: dict, source: str) -> str:
    """
    Build a readable ALETHEIA Witness Report for the latest chat audit.
    This is a prototype audit trail, not a legal or institutional determination.
    """
    audit_blob = json.dumps(
        {
            "query": query,
            "verdict": judgment.get("verdict"),
            "risk": judgment.get("corruption_risk"),
            "integrity": report.get("integrity"),
            "friction": report.get("friction"),
            "collapse_probability": report.get("collapse_probability"),
        },
        sort_keys=True,
    )
    audit_id = hashlib.sha256(audit_blob.encode("utf-8")).hexdigest()[:12].upper()
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    reasons = "\n".join(f"- {item}" for item in judgment.get("reasons", [])) or "- None recorded"
    safeguards = "\n".join(f"- {item}" for item in judgment.get("safeguards", [])) or "- None recorded"
    questions = "\n".join(f"- {item}" for item in judgment.get("questions", [])) or "- None recorded"

    return f"""ALETHEIA WITNESS REPORT
Audit ID: {audit_id}
Timestamp: {timestamp}
Source: {source}
Boundary notice: This is a symbolic mirror receipt for human review. It is not legal, political, medical, religious, institutional, or operational authorization.

QUESTION / IDEA
{query}

PROTOCOL READING
Internal review label: {judgment.get("verdict", "THRESHOLD")}
Corruption risk: {judgment.get("corruption_risk", "Medium")}
Stress label: {judgment.get("stress_label", "Unclassified")}

SUMMARY
{sanitize_public_message(judgment.get("summary", ""))}

CORE METRICS
Integrity: {report.get("integrity")}
Friction: {report.get("friction")}
Collapse pressure: {report.get("collapse_probability")}
Trust friction: {report.get("trust_friction")}

SIMULATION STATE
Stability: {sim.get("stability")}
Trust index: {sim.get("trust_index")}
Alignment: {sim.get("alignment")}
Ego: {sim.get("ego")}
Collapse risk: {sim.get("collapse_risk")}

SCANNER FEATURES
Power concentration: {scan.get("power_concentration")}
Decision transparency: {scan.get("decision_transparency")}
Regulatory presence: {scan.get("regulatory_presence")}
Anonymity level: {scan.get("anonymity_level")}
Capital scale: {scan.get("capital_scale")}
Technical complexity: {scan.get("technical_complexity")}
Scan mode: {scan.get("scan_mode")}

REASONS
{reasons}

REQUIRED SAFEGUARDS
{safeguards}

HUMAN REVIEW QUESTIONS BEFORE RELYING ON THIS READING
{questions}

FIVE STRATEGIC FUNCTIONS
1. Strategic Alignment Audit
2. Lexical Correction / Gated Power Language
3. Deterministic Integrity Check
4. Multi-Layer Stability Model
5. ALETHEIA Witness Report / Audit Trail
"""



def friendly_threshold_direction_label(value: str) -> str:
    """Return friendly UI copy for the technical Threshold Mapping direction."""
    text = str(value or "Not recorded")
    labels = {
        "Toward review boundary": "Toward review boundary",
        "At review boundary": "At review boundary",
        "Toward SANCTUARY": "Toward review boundary",
        "Balanced THRESHOLD": "Balanced review zone",
        "Toward ASYLUM": "Toward capture pressure",
    }
    return labels.get(text, text)


def silent_operator_question(item, *, context: str = "this pattern") -> str:
    """
    Convert recommendations or safeguards into reflective questions.

    Silent Operator mode keeps ALETHEIA in mirror posture: it surfaces
    audit prompts for human review instead of presenting commands.
    """
    if isinstance(item, dict):
        target = str(item.get("target", context) or context).strip()
        action = str(item.get("action", "repair or review") or "repair or review").strip()
        reason = str(item.get("reason", "") or "").strip()
        question = (
            f"Which mechanism would let humans review whether {target} needs {action.lower()} "
            "while preserving transparency, appealability, and non-ownership of power?"
        )
        if reason:
            return f"{question} Context: {reason}"
        return question

    text = str(item or "").strip()
    if not text:
        return "Which safeguard, appeal path, or review mechanism is still missing here?"
    if text.endswith("?"):
        return text
    return f"Which safeguard or appeal path would address this concern: {text}?"

def render_chat_judgment(judgment: dict, source: str, report: dict, sim: dict | None = None, scan: dict | None = None):
    verdict = str(judgment.get("verdict", "THRESHOLD")).upper()
    if verdict == "SANCTUARY":
        color = "#8fbc8f"
    elif verdict == "ASYLUM":
        color = "#db7777"
    else:
        color = "#e5c36b"

    review_band = review_band_for_state(verdict, report, sim or {})
    review_band_label = review_band.get("label", verdict.title())
    safe_review_band_label = html.escape(str(review_band_label))
    review_band_line = ""
    if verdict == "THRESHOLD":
        review_band_line = (
            '<div style="color:#d4b88a;font-size:1.05rem;font-weight:800;margin-top:0.2rem;">'
            f'{safe_review_band_label}'
            '</div>'
        )

    # Patch 71.11: keep the detail rows inline HTML instead of indented
    # Markdown lines, otherwise Streamlit can still show the stress-label row
    # as literal code inside the card.
    safe_source = html.escape(str(source))
    safe_risk = html.escape(str(judgment.get("corruption_risk", "Medium")))
    safe_stress_label = html.escape(str(judgment.get("stress_label", "Unclassified")))

    threshold_mapping = build_threshold_mapping_layer(
        verdict=verdict,
        scan=scan or {},
        sim=sim or {},
        report=report,
        protocol_label=str(judgment.get("stress_label", judgment.get("verdict", ""))),
    )
    threshold_direction_display = friendly_threshold_direction_label(str(threshold_mapping.get("threshold_direction", "Not recorded")))
    safe_threshold_direction = html.escape(threshold_direction_display)
    threshold_z_axis = float(threshold_mapping.get("z_axis_position", 0.0) or 0.0)
    threshold_z_axis_zone = str(threshold_mapping.get("z_axis_zone", "Standard review mapping") or "Standard review mapping")
    threshold_repair_index = float(threshold_mapping.get("repair_index", 0.0) or 0.0)
    threshold_repair_question_index = float(threshold_mapping.get("repair_question_index", threshold_repair_index) or 0.0)
    threshold_confirmed_repair_capacity = float(threshold_mapping.get("confirmed_repair_capacity", threshold_repair_index) or 0.0)

    detail_rows = [
        f'<div><strong>Risk signal:</strong> {safe_risk}</div>',
        f'<div style="margin-top:0.15rem;"><strong>Humility note:</strong> {html.escape(_protocol_humility_note(verdict))}</div>',
    ]
    if verdict == "THRESHOLD":
        detail_rows.append(
            f'<div style="margin-top:0.15rem;"><strong>Review zone:</strong> {safe_review_band_label}</div>'
        )
    detail_rows.append(
        f'<div style="margin-top:0.15rem;"><strong>Stress label:</strong> {safe_stress_label}</div>'
    )
    if threshold_mapping:
        detail_rows.append(
            '<div style="margin-top:0.15rem;"><strong>Threshold direction:</strong> '
            f'{safe_threshold_direction} · Z-axis {threshold_z_axis:.3f} / 0.9999 · {html.escape(threshold_z_axis_zone)} · Confirmed repair {threshold_confirmed_repair_capacity:.3f}</div>'
        )
    detail_rows_html = "".join(detail_rows)

    judgment_card_html = f"""
<div class="soft-card">
  <div style="color:#aeb7c6;font-size:0.78rem;font-weight:900;text-transform:uppercase;letter-spacing:0.08em;">
    {safe_source} · Protocol reading state
  </div>
  <div style="color:{color};font-size:2rem;font-weight:900;margin-top:0.25rem;">
    {_protocol_metric_display(verdict)}
  </div>
  <div style="color:#c9c0b2;font-size:0.9rem;font-weight:700;margin-top:0.1rem;">
    Internal review label: {html.escape(str(verdict))}
  </div>
  {review_band_line}
  <div style="color:#e8e0d0;margin-top:0.5rem;">{detail_rows_html}</div>
</div>
"""
    st.markdown(textwrap.dedent(judgment_card_html).strip(), unsafe_allow_html=True)

    st.write(sanitize_public_message(judgment.get("summary", "")))

    cols = st.columns(3)
    cols[0].metric("Integrity", f"{report['integrity']:.3f}")
    cols[1].metric("Friction", f"{report['friction']:.3f}")
    cols[2].metric("Collapse pressure", f"{report['collapse_probability']:.3f}")
    st.caption(
        "Metric guide: Integrity reflects visible safeguards/evidence; Friction reflects control or access pressure; "
        "Collapse pressure reflects stress under weak review paths. These are reading signals, not predictions or verdicts."
    )
    if report.get("raw_metrics_before_ethics") or report.get("ethics_adjustment_applied") is not None:
        st.caption("These are ethics-calibrated reading metrics. Raw pre-ethics values stay in the local witness receipt.")

    st.markdown("### How to read this Mirror Check output")
    st.caption(
        "Plain-language panels for human review. These panels explain the reading; they do not change the internal label, "
        "grant permission, certify safety, or replace accountable human judgment."
    )

    with st.expander("1. What this reading is", expanded=False):
        st.markdown(
            """
            This is a structured Mirror Check review. The system looked at the submitted text for pressure, power, evidence, safeguards, and repair needs.

            Important: the computer does not decide anything here. It does not grant permission and it does not prove that something is safe, good, or true. The reading is a digital mirror for people to review.
            """
        )

    with st.expander("2. Main results", expanded=False):
        main_result_rows = [
            {"Field": "Internal review label", "Value": str(verdict), "How to read it": "Internal taxonomy label only; not approval, rejection, or final truth."},
            {"Field": "Risk reading", "Value": str(judgment.get('corruption_risk', 'Medium')), "How to read it": "A review signal for human attention."},
            {"Field": "Integrity", "Value": f"{report['integrity']:.3f}", "How to read it": "Visible safeguards/evidence signal; not a safety certificate."},
            {"Field": "Friction", "Value": f"{report['friction']:.3f}", "How to read it": "Control, access, or pressure signal."},
            {"Field": "Collapse pressure", "Value": f"{report['collapse_probability']:.3f}", "How to read it": "Stress under weak review paths; not a prediction."},
        ]
        st.dataframe(pd.DataFrame(main_result_rows), use_container_width=True, hide_index=True)

    with st.expander("3. Power and control distribution", expanded=False):
        st.markdown(
            """
            Mirror Check asks whether control is concentrated in one actor, office, platform, dataset, model, committee, or hidden process. It also checks whether people have meaningful review, appeal, correction, and refusal paths.

            A healthier reading usually has distributed evidence, visible reasons, human review, repair paths, and non-coercive access. A higher-pressure reading usually has opaque control, weak appeal, central control, or conditional access to important needs.
            """
        )

    with st.expander("4. Threshold direction review", expanded=False):
        if threshold_mapping:
            # Patch 241: keep this diagnostic full-width and readable after Mirror Check page extraction.
            threshold_direction_value = friendly_threshold_direction_label(str(threshold_mapping.get("threshold_direction", "Not recorded")))
            z_axis_value = f"{float(threshold_mapping.get('z_axis_position', 0.0)):.3f} / 0.9999"
            repair_questions_value = f"{float(threshold_mapping.get('repair_question_index', threshold_mapping.get('repair_index', 0.0))):.3f}"
            confirmed_repair_value = f"{float(threshold_mapping.get('confirmed_repair_capacity', threshold_mapping.get('repair_index', 0.0))):.3f}"
            threshold_summary_rows = [
                {"Field": "Threshold direction", "Value": threshold_direction_value, "Human-review meaning": "Direction of pressure within the threshold band; not approval or rejection."},
                {"Field": "Z-axis", "Value": z_axis_value, "Human-review meaning": "Boundary proximity marker; Z=1.0000 remains outside ALETHEIA's claim."},
                {"Field": "Repair questions", "Value": repair_questions_value, "Human-review meaning": "How much review/repair questioning is available, not proof of safety."},
                {"Field": "Confirmed repair", "Value": confirmed_repair_value, "Human-review meaning": "Visible repair capacity already detected in the text/receipt context."},
            ]
            st.dataframe(pd.DataFrame(threshold_summary_rows), use_container_width=True, hide_index=True)
            st.markdown(f"**Z-axis zone:** `{html.escape(str(threshold_mapping.get('z_axis_zone', 'Standard review mapping')))}`")
            st.caption(str(threshold_mapping.get('z_axis_repair_note', 'No separate repair-zone mapping applied.')))
            st.caption(
                "Receipt preview only: this maps whether the reading is moving toward capture pressure, a balanced review zone, or the human/system boundary. "
                "It does not create a new decision or enforcement path. Repair-zone values show reviewability, not approval. Repair questions are a route, not proof that safeguards already exist. Z=1.0000 remains outside ALETHEIA’s claim."
            )
            st.info(str(threshold_mapping.get("asymptote_note", "ALETHEIA does not claim final safety, final truth, or final authority. Ultimate questions and final authority remain outside code, metrics, receipts, hashes, trees, 9k structures, and institutional power.")))
            st.caption(str(threshold_mapping.get("nine_k_threshold_steward_note", "9k is a human anti-tyranny scaffold / threshold steward, not Sanctuary or final legitimacy.")))
            component_rows = []
            for component in threshold_mapping.get("component_readings", []) or []:
                if isinstance(component, dict):
                    component_rows.append({
                        "Component": component.get("component"),
                        "Reading": component.get("reading"),
                        "Capture pressure": component.get("threshold_minus_pressure"),
                        "Repair growth": component.get("threshold_plus_growth"),
                        "Pressure": component.get("pressure_score"),
                        "Growth": component.get("growth_score"),
                    })
            if component_rows:
                with st.expander("Component-level threshold details", expanded=False):
                    st.dataframe(pd.DataFrame(component_rows), use_container_width=True, hide_index=True)
            st.write(f"**Dominant pressure:** {threshold_mapping.get('dominant_pressure')}")
        else:
            st.caption("No threshold mapping data was attached to this reading.")

    with st.expander("5. Observed reasons", expanded=False):
        reasons = judgment.get("reasons", [])
        if reasons:
            for item in reasons:
                st.write(f"- {item}")
        else:
            st.caption("No observed reasons were recorded for this reading.")

    with st.expander("6. Safeguard questions for human review", expanded=False):
        safeguards = judgment.get("safeguards", [])
        if safeguards:
            for item in safeguards:
                st.write(f"- {silent_operator_question(item, context='this safeguard gap')}")
        else:
            st.caption("No safeguard questions were recorded for this reading.")

    with st.expander("7. Questions before relying on this reading", expanded=False):
        questions = judgment.get("questions", [])
        if questions:
            for item in questions:
                st.write(f"- {silent_operator_question(item, context='this model')}")
        else:
            st.caption("No reliance questions were recorded for this reading.")

    with st.expander("8. Signal analysis and conclusion", expanded=False):
        st.markdown(f"- **Dominant pressure:** `{threshold_mapping.get('dominant_pressure') if threshold_mapping else 'Not recorded'}`")
        signals = threshold_mapping.get("asylum_pressure_signals", []) if threshold_mapping else []
        growth = threshold_mapping.get("sanctuary_growth_signals", []) if threshold_mapping else []
        st.markdown("**Capture-pressure signals**")
        if signals:
            for signal in signals:
                st.write(f"- {signal}")
        else:
            st.caption("No dominant capture-pressure signal was recorded in this layer.")
        st.markdown("**Repair/growth signals**")
        if growth:
            for signal in growth:
                st.write(f"- {signal}")
        else:
            st.caption("No repair/growth signal was recorded in this layer.")


# Header
mascot_logo_uri = asset_image_data_uri(MASCOT_LOGO_IMAGE)
header_path = Path("assets/header.jpg")
if header_path.exists():
    st.image(str(header_path), use_container_width=True)

render_app_header(mascot_logo_uri, APP_VERSION, st)

# Aletheia Unit Preview is the only pre-module hook. It renders after the
# public header/CSS so users see one polished entry surface, then stops before
# the full module interface until they proceed.
if not st.session_state.get(UNIT_PREVIEW_SESSION_KEY, False):
    if render_unit_preview(st):
        st.session_state[UNIT_PREVIEW_SESSION_KEY] = True
        st.rerun()
    st.stop()

render_app_boundary_notices(SUPPORTED_INPUT_LANGUAGE_NOTE, st)

# Sidebar controls
with st.sidebar:
    render_sidebar_brand(mascot_logo_uri, st)
    render_sidebar_context(st)
    render_privacy_panel(st, expanded=False)
    render_boundary_statement("footer", st)

    preset_labels = {
        "default": "Starting preset",
        "high_ego_context": "High control risk",
        "cooperative_context": "Cooperative space",
        "power_concentrated": "Power held by few",
    }
    preset_options = [preset_labels.get(key, key.replace("_", " ").title()) for key in WEIGHT_PRESETS.keys()]

    if st.session_state.get("sidebar_weight_profile") == "Default":
        st.session_state["sidebar_weight_profile"] = "Starting preset"

    if st.button("Reset lens", use_container_width=True, key="sidebar_reset_tuning"):
        st.session_state["sidebar_weight_profile"] = "Starting preset"
        st.session_state["sidebar_steps"] = 40
        st.session_state["sidebar_agent_voices"] = 6
        st.session_state["sidebar_capture_sensitivity"] = 0.55
        st.session_state["sidebar_alignment_floor"] = 0.45

    render_sidebar_review_lens_intro(st)
    preset_display = st.selectbox(
        "Review lens",
        preset_options,
        index=0,
        key="sidebar_weight_profile",
        help="Choose a starting view. It is only a lens, not a truth machine.",
    )
    render_sidebar_review_lens_note(st)

    selected_preset = next(
        key for key in WEIGHT_PRESETS.keys()
        if preset_labels.get(key, key.replace("_", " ").title()) == preset_display
    )
    weights = WEIGHT_PRESETS[selected_preset]

    render_sidebar_review_rhythm_intro(st)
    steps = st.slider(
        "Steps",
        20,
        120,
        40,
        5,
        key="sidebar_steps",
        help="How many steps the test should run.",
    )
    n_agents = st.slider(
        "Voices",
        3,
        6,
        6,
        key="sidebar_agent_voices",
        help="How many small voices join the test.",
    )
    render_sidebar_review_rhythm_note(st)

    render_sidebar_safety_rails_intro(st)
    ego_tolerance = st.slider(
        "Control sensitivity",
        0.35,
        0.75,
        0.55,
        0.01,
        key="sidebar_capture_sensitivity",
        help="Higher values make ALETHEIA more alert to control and concentrated power.",
    )
    divine_floor = st.slider(
        "Minimum fit",
        0.20,
        0.70,
        0.45,
        0.01,
        key="sidebar_alignment_floor",
        help="Minimum fit needed before a system can look stable.",
    )
    render_sidebar_safety_rails_note(st)


MIN_FULL_GRID_COUNTRIES = 100


def _df_active(value) -> bool:
    return isinstance(value, pd.DataFrame) and not value.empty


def _source_signal_active(df: pd.DataFrame | None, columns: list[str]) -> bool:
    if not _df_active(df):
        return False
    for col in columns:
        if col in df.columns and pd.to_numeric(df[col], errors="coerce").notna().any():
            return True
    return False


def update_protocol_state(**updates) -> dict:
    """Maintain the visible shared substrate that Audit, Simulation, and Grid read from."""
    state = dict(st.session_state.get("protocol_state", {}))
    scored_df = st.session_state.get("empirical_scored_df")
    master_df = st.session_state.get("empirical_master_df")
    allocation_df = st.session_state.get("empirical_allocation_df")
    trust_cols = ["wvs_generalized_trust"]
    wgi_cols = [
        "wgi_voice_accountability",
        "wgi_political_stability",
        "wgi_government_effectiveness",
        "wgi_regulatory_quality",
        "wgi_rule_of_law",
        "wgi_control_corruption",
    ]
    vdem_cols = ["vdem_executive_constraints", "vdem_democracy", "v2x_polyarchy", "v2x_libdem"]
    check = st.session_state.get("sydney_protocol_self_check", {})

    state.update({
        "empirical_master_active": _df_active(master_df),
        "scored_evidence_active": _df_active(scored_df),
        "allocation_active": _df_active(allocation_df),
        "trust_calibration_active": _source_signal_active(scored_df, trust_cols) or _source_signal_active(master_df, trust_cols),
        "wgi_active": _source_signal_active(scored_df, wgi_cols) or _source_signal_active(master_df, wgi_cols),
        "vdem_active": _source_signal_active(scored_df, vdem_cols) or _source_signal_active(master_df, vdem_cols),
        "synthetic_demo_active": bool(st.session_state.get("empirical_use_template", False)),
        "sydney_protocol_overlay_active": bool(check.get("ok", False)),
    })
    state.update({k: v for k, v in updates.items() if v is not None})
    st.session_state["protocol_state"] = state
    return state


def render_shared_protocol_state_notice(current_mode: str, *, expanded: bool = False):
    state = update_protocol_state(current_mode=current_mode)
    render_shared_protocol_state_notice_panel(current_mode=current_mode, state=state, expanded=expanded)


def render_audit_module_integrity_panel(*, expanded: bool = False):
    """Show the Audit tab's local view of the fail-closed protocol/module check."""
    check = st.session_state.get("sydney_protocol_self_check")
    if check is None:
        with st.spinner("Running Audit module integrity check..."):
            check = run_sydney_protocol_self_check()
            st.session_state["sydney_protocol_self_check"] = check

    required_symbols = [
        "governance_scan",
        "apply_capture_feature_override",
        "build_features_from_scan",
        "simulate",
        "full_report",
        "classify_verdict",
        "final_protocol_judgment",
        "llm_governance_judgment",
        "source_conformance_hits",
        "render_pulse_tree",
    ]
    module_rows = []
    missing_symbols = []
    for name in required_symbols:
        obj = globals().get(name)
        ok = callable(obj)
        module_rows.append({"Module / function": name, "Status": "PASS" if ok else "MISSING"})
        if not ok:
            missing_symbols.append(name)

    protocol_ok = bool(check.get("ok")) if isinstance(check, dict) else False
    modules_ok = not missing_symbols
    audit_ok = protocol_ok and modules_ok

    if audit_ok:
        st.success("Mirror module check: ready")
    else:
        st.error("Mirror module check: needs repair")
        if missing_symbols:
            st.warning("These Mirror Check parts are missing right now: " + ", ".join(missing_symbols))
        if isinstance(check, dict) and check.get("failures"):
            st.code("\n".join(check["failures"]), language="text")
        st.stop()

    with st.expander("Audit module integrity check details", expanded=expanded):
        st.caption(
            "The Audit tab is protected by the same fail-closed Sydney Protocol sentinel used by the whole app. "
            "This panel makes that protection visible inside Audit, so a broken safeguard or missing module cannot quietly pretend to be a trustworthy result."
        )
        st.dataframe(pd.DataFrame(module_rows), use_container_width=True, hide_index=True)
        if isinstance(check, dict) and check.get("results"):
            st.markdown("#### Sydney Protocol guard tests")
            st.dataframe(_protocol_taxonomy_ui_table_df(pd.DataFrame(check.get("results", []))), use_container_width=True, hide_index=True)





# Patch 226: top-level modules use single-module conditional navigation instead of st.tabs.
# Streamlit tabs render all tab bodies internally; that can leak inactive module content
# into one long page after reruns. This radio keeps only the selected module rendered.
selected_top_module = st.radio(
    "ALETHEIA module",
    APP_NAVIGATION_LABELS,
    horizontal=True,
    label_visibility="collapsed",
    key="aletheia_active_module",
)
st.caption("Receipt Reader: Why ALETHEIA → Support utilities → Receipt Reader — Standard View.")

if selected_top_module == '🚀 Stress Test':
    render_stress_test_page(globals())

if selected_top_module == '🧭 Boundary Cases':
    render_boundary_cases_page(
        update_protocol_state=update_protocol_state,
        render_shared_protocol_state_notice=render_shared_protocol_state_notice,
        app_version=APP_VERSION,
    )

if selected_top_module == '📊 Evidence Lab':
    render_evidence_lab_page(globals())

if selected_top_module == '🌐 World Lens':
    render_world_lens_page(globals())

if selected_top_module == '🪞 Mirror Check':
    render_mirror_check_page(globals())
if selected_top_module == '📜 Protocol Guide':
    render_protocol_guide_page()


if selected_top_module == 'ℹ️ Why ALETHEIA':
    with st.container():
        render_about_public_info_page(st, header_image=resolve_about_header_image())
    
    st.divider()
    st.markdown("### Support utilities")
    st.info(
        "This section contains Receipt Reader — Standard View. "
        "It is intentionally kept as a read-only support utility, not a scoring surface or primary review module."
    )
    st.caption(
        "Optional reading aids that support review without becoming primary modules. "
        "They do not rescore, certify, approve, reject, enforce, or override ALETHEIA receipts."
    )
    with st.expander("Receipt Reader — Standard View", expanded=False):
        st.caption(
            "Have an ALETHEIA receipt? Upload a .txt, .md, or .json receipt file for native values "
            "and a standard review-band explanation. This utility does not rescore, certify, approve, "
            "reject, or override the original receipt."
        )
        render_receipt_reader_standard_view(st)
    
    render_app_footer_banner(APP_VERSION, st)
    
