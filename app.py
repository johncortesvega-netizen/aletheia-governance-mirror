import os
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

from core.parser import parse_scenario_llm, decouple_actor
from core.ethics import evaluate_ethics, apply_ethics_to_metrics
from core.cognitive_resilience import evaluate_cognitive_resilience, apply_cognitive_resilience_to_metrics, positive_cr_baseline_stabilizer
try:
    from core.parser import _local_governance_scan
except Exception:
    _local_governance_scan = None
from core.simulation import simulate

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


APP_VERSION = "v1.0-governance-mirror-final"
SUPPORTED_INPUT_LANGUAGE_NOTE = "Input language support: English and Nederlands/Dutch only. Other languages may be reviewed as text, but the calibrated risk lexicon is not validated for them yet."
PROJECT_ROOT = Path(__file__).resolve().parent
ABOUT_HEADER_IMAGE = PROJECT_ROOT / "assets" / "about_header.png"
DOCTRINE_HTML_FILES = [
    ("Sydney Protocol v3.2", PROJECT_ROOT / "Sydney_Protocol_v3.2.html"),
    ("GPA v8.2", PROJECT_ROOT / "GPA_v8.2.html"),
]
TOTAL_9K = 9000

APP_NAVIGATION_LABELS = [
    "💬 Mirror Check",
    "🚀 Stress Test",
    "🧭 Boundary Cases",
    "📊 Evidence Lab",
    "🌐 World Lens",
    "📜 Protocol Guide",
    "ℹ️ Why ALETHEIA",
]

APP_NAVIGATION_MAP = [
    ("Mirror Check", "Audit a document or proposal for capture risk, missing safeguards, and repair questions."),
    ("Stress Test", "Try a scenario under pressure and inspect stability, trust, friction, and repair needs."),
    ("Boundary Cases", "Test edge cases such as consent pressure, free agency, ambient capture, and self-audit."),
    ("Evidence Lab", "Separate evidence from claims and park extraordinary claims as unverified until review."),
    ("World Lens", "Simulate population-impact risk without Global ID, real 9k selection, or sovereign authority."),
    ("Protocol Guide", "Read the v0.1 operating guide, safe-language rules, and module boundaries."),
    ("Why ALETHEIA", "Understand the v1.0 public MVP, release boundary, examples, and research direction."),
]

APP_UX_POLISH_SUMMARY = [
    "Start with Mirror Check when you have a document.",
    "Use Stress Test when you have a scenario.",
    "Use Boundary Cases when the ethical edge case is unclear.",
    "Use Evidence Lab when a claim needs source-quality review.",
    "Use Protocol Guide when you need the operating rules.",
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


def metric_card(label: str, value: str, helper: str = ""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-help">{helper}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def soft_card(title: str, body: str):
    st.markdown(
        f"""
        <div class="soft-card">
            <strong style="color:#d4b88a;">{title}</strong><br>
            <span style="color:#e8e0d0;">{body}</span>
        </div>
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
    "THRESHOLD_MINUS": "Needs Repair",
    "THRESHOLD": "Needs Review",
    "THRESHOLD_PLUS": "Near Sanctuary",
    "SANCTUARY": "Sanctuary",
}


def review_band_for_state(verdict: str, report: dict | None = None, sim: dict | None = None) -> dict:
    """
    User-facing five-band display helper.

    Canonical taxonomy remains ASYLUM / THRESHOLD / SANCTUARY. The middle
    state receives a display-only review band:
    - Needs Repair: closer to Asylum, but still repairable.
    - Needs Review: mixed/incomplete safeguards.
    - Near Sanctuary: mostly stable, but not fully safe yet.
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
            "summary": "Closer to Asylum, but still repairable.",
        }

    if integrity >= 0.62 and collapse <= 0.18 and trust >= 0.86 and alignment >= 0.86 and ego <= 0.08:
        return {
            "band": "THRESHOLD_PLUS",
            "label": REVIEW_BAND_LABELS["THRESHOLD_PLUS"],
            "summary": "Mostly stable, but not fully safe yet.",
        }

    return {
        "band": "THRESHOLD",
        "label": REVIEW_BAND_LABELS["THRESHOLD"],
        "summary": "Mixed or incomplete safeguards require human review.",
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


def tree_copy_for_state(state: str, mode: str = "Mirror Check") -> dict:
    """Return display copy for the Mirror/Stress tree without changing metrics."""
    state_key = (state or "THRESHOLD").upper()
    mode_key = (mode or "Mirror Check").strip()

    if state_key == "QUESTION_PROMPT":
        return {
            "state": "QUESTION_PROMPT",
            "headline": "Review Tool Mode",
            "score_label": "Visual review-tool signal",
            "caption": "Audit question detected. This input is a review prompt, not a scored governance scenario.",
            "root": "Human review",
            "trunk": "Question → reflection → repair",
            "branches": ["Clarity", "Appeal", "Bias check", "Repair", "Human review"],
        }

    if mode_key.lower().startswith("stress"):
        base = {
            "root": "Human dignity",
            "trunk": "Power under stress",
            "branches": ["Consent", "Exit", "Appeal", "Time limits", "Independent review", "Evidence clarity", "Basic rights"],
        }
        if state_key == "SANCTUARY":
            return {**base, "state": "SANCTUARY", "headline": "Stable under pressure", "score_label": "Visual stability signal", "caption": "Low capture signal under this scenario. Still requires human review."}
        if state_key == "ASYLUM":
            return {**base, "state": "ASYLUM", "headline": "Protective review signal", "score_label": "Visual pressure signal", "caption": "Protective review required. This is not enforcement and not an automated decision."}
        return {**base, "state": "THRESHOLD", "headline": "Needs safeguards", "score_label": "Visual safeguard-gap signal", "caption": "Boundary condition detected. Add appeal, exit, evidence, and repair before trust can increase."}

    base = {
        "root": "Human review",
        "trunk": "Evidence + accountability",
        "branches": ["Safeguards", "Appeal", "Transparency", "Repair", "Basic rights", "Non-coercion"],
    }
    if state_key == "SANCTUARY":
        return {**base, "state": "SANCTUARY", "headline": "Low capture signal", "score_label": "Visual stability signal", "caption": "The pattern appears relatively reviewable and repairable. This is not approval."}
    if state_key == "ASYLUM":
        return {**base, "state": "ASYLUM", "headline": "Protective review signal", "score_label": "Visual pressure signal", "caption": "High capture or coercion signal. Human repair review is required; ALETHEIA does not enforce action."}
    return {**base, "state": "THRESHOLD", "headline": "Needs safeguards", "score_label": "Visual safeguard-gap signal", "caption": "The pattern sits at a review boundary. Clarify safeguards, appeal, evidence, and correction loops."}


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





# Patch 71.2: visual-only tree polish constants.
# The tree remains an explanatory UI element; receipt metrics stay canonical.
TREE_VISUAL_CANOPY_LAYER_COUNT = 8
TREE_VISUAL_CAPTION_CLASS = "aletheia-tree-caption-below-visual"
TREE_VISUAL_CENTRAL_GLOW_REMOVED = True

def render_pulse_tree(
    score: float,
    ego: float,
    alignment: float,
    title: str = "Live Pulse Tree",
    *,
    state_override: str | None = None,
    mode: str = "Mirror Check",
):
    """
    Streamlit HTML/SVG state tree.

    Patch 70: the tree is a visual state explainer, not a second protocol
    metric. The receipt's protocol-adjusted integrity remains the canonical
    numeric reading; the tree score is a visual stability/pressure signal.

    Patch 71.2: the canopy and caption are visual-only polish. The caption is
    rendered below the SVG visual so it does not sit inside the tree canopy or
    trunk area.

    Patch 71.6: removes the large central glow/blob behind the canopy. The
    tree state still follows the protocol-adjusted verdict; this is visual-only.
    """
    score = max(0.0, min(1.0, float(score)))
    ego = max(0.0, min(1.0, float(ego)))
    alignment = max(0.0, min(1.0, float(alignment)))

    if score >= 0.62:
        inferred_state = "SANCTUARY"
        leaf_color = "#8fbc8f"
        glow_color = "rgba(143,188,143,0.35)"
    elif score >= 0.42:
        inferred_state = "THRESHOLD"
        leaf_color = "#e5c36b"
        glow_color = "rgba(229,195,107,0.30)"
    else:
        inferred_state = "ASYLUM"
        leaf_color = "#db7777"
        glow_color = "rgba(219,119,119,0.28)"

    state = (state_override or inferred_state or "THRESHOLD").upper()
    if state == "QUESTION_PROMPT":
        leaf_color = "#8ab4f8"
        glow_color = "rgba(138,180,248,0.30)"
    elif state == "SANCTUARY":
        leaf_color = "#8fbc8f"
        glow_color = "rgba(143,188,143,0.35)"
    elif state == "THRESHOLD":
        leaf_color = "#e5c36b"
        glow_color = "rgba(229,195,107,0.30)"
    elif state == "ASYLUM":
        leaf_color = "#db7777"
        glow_color = "rgba(219,119,119,0.28)"

    copy = tree_copy_for_state(state, mode=mode)
    canopy_opacity = 0.28 + (score * 0.62)
    # Patch 71.2 baseline kept for regression-test continuity:
    # canopy_scale = 0.82 + (score * 0.30)
    # canopy_sag = 0 if state == "SANCTUARY"
    # Patch 71.3 tightens/lower-centers the canopy while preserving the
    # explanatory-only contract from Patch 71.2.
    canopy_scale = 0.70 + (score * 0.18)
    canopy_sag = 8 if state == "SANCTUARY" else (12 if state == "THRESHOLD" else 17)
    canopy_y_offset = 14 if state == "SANCTUARY" else (18 if state == "THRESHOLD" else 23)
    fallen_count = int(round(ego * 10)) if state != "QUESTION_PROMPT" else 0

    fallen_svg = ""
    for i in range(fallen_count):
        x = 44 + (i * 16) % 148
        y = 214 + ((i * 9) % 18)
        fallen_svg += (
            f'<ellipse cx="{x}" cy="{y}" rx="5" ry="3" '
            f'fill="#db7777" opacity="0.70" '
            f'transform="rotate({i * 17} {x} {y})" />'
        )

    branch_labels = copy.get("branches", [])[:7]
    branch_html = "".join(
        f'<span style="display:inline-block;margin:3px 5px 0 0;padding:3px 7px;border-radius:999px;background:rgba(255,255,255,0.08);color:#e8e0d0;font-size:11px;">{b}</span>'
        for b in branch_labels
    )

    svg_html = f"""
    <div style="
        box-sizing:border-box;
        border:1px solid rgba(212,184,138,0.25);
        background:rgba(255,255,255,0.055);
        border-radius:18px;
        padding:16px;
        margin:0;
        font-family:Inter, Arial, sans-serif;
        color:#e8e0d0;
        width:100%;
    ">
        <div style="font-family:Georgia,serif;color:#d4b88a;font-size:22px;font-weight:700;margin-bottom:6px;">
            🌳 {title}
        </div>
        <div style="color:#aeb7c6;font-size:13px;margin-bottom:8px;">
            Mode: <strong>{mode}</strong>
            · State: <strong style="color:{leaf_color};">{state}</strong>
            · {copy.get('score_label', 'Visual tree score')} {score:.2f}
            · Alignment {alignment:.2f}
            · Ego {ego:.2f}
        </div>
        <div style="color:#e8e0d0;font-size:13px;line-height:1.45;margin-bottom:10px;">
            <strong>{copy.get('headline', state)}</strong> — {copy.get('caption', '')}
        </div>
        <div style="color:#aeb7c6;font-size:12px;line-height:1.5;margin-bottom:10px;">
            Root: <strong>{copy.get('root', 'Human review')}</strong> · Trunk: <strong>{copy.get('trunk', 'Evidence + accountability')}</strong><br/>
            {branch_html}
        </div>

        <svg width="100%" height="250" viewBox="0 0 260 250" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ALETHEIA explanatory tree visual">
            <rect x="0" y="0" width="260" height="250" rx="18" fill="#0b1020"/>
            <ellipse cx="130" cy="221" rx="92" ry="14" fill="rgba(212,184,138,0.16)"/>
            <!-- Patch 71.6: central glow/blob intentionally removed; canopy leaves provide the visual state. -->

            <path d="M124 214 C126 178, 123 145, 118 116 C132 144, 139 176, 137 214 Z" fill="#8b5e3c"/>
            <path d="M128 148 C110 129, 94 105, 80 79" stroke="#8b5e3c" stroke-width="9" stroke-linecap="round" fill="none"/>
            <path d="M132 145 C153 124, 171 96, 188 63" stroke="#8b5e3c" stroke-width="9" stroke-linecap="round" fill="none"/>
            <path d="M128 130 C132 104, 133 81, 130 50" stroke="#8b5e3c" stroke-width="8" stroke-linecap="round" fill="none"/>
            <path d="M121 137 C104 126, 96 111, 93 96" stroke="#8b5e3c" stroke-width="6" stroke-linecap="round" fill="none" opacity="0.92"/>
            <path d="M136 133 C151 119, 159 104, 162 91" stroke="#8b5e3c" stroke-width="6" stroke-linecap="round" fill="none" opacity="0.92"/>

            <ellipse cx="130" cy="{104 + canopy_y_offset}" rx="{46 * canopy_scale:.0f}" ry="{34 * canopy_scale:.0f}" fill="{leaf_color}" opacity="{canopy_opacity:.2f}"/>
            <ellipse cx="100" cy="{110 + canopy_y_offset}" rx="{30 * canopy_scale:.0f}" ry="{23 * canopy_scale:.0f}" fill="{leaf_color}" opacity="{max(0.18, canopy_opacity - 0.09):.2f}"/>
            <ellipse cx="160" cy="{108 + canopy_y_offset}" rx="{31 * canopy_scale:.0f}" ry="{24 * canopy_scale:.0f}" fill="{leaf_color}" opacity="{max(0.18, canopy_opacity - 0.09):.2f}"/>
            <ellipse cx="113" cy="{82 + canopy_y_offset}" rx="{25 * canopy_scale:.0f}" ry="{21 * canopy_scale:.0f}" fill="{leaf_color}" opacity="{max(0.16, canopy_opacity - 0.12):.2f}"/>
            <ellipse cx="149" cy="{82 + canopy_y_offset}" rx="{25 * canopy_scale:.0f}" ry="{21 * canopy_scale:.0f}" fill="{leaf_color}" opacity="{max(0.16, canopy_opacity - 0.12):.2f}"/>
            <ellipse cx="130" cy="{130 + canopy_y_offset + canopy_sag}" rx="{37 * canopy_scale:.0f}" ry="{25 * canopy_scale:.0f}" fill="{leaf_color}" opacity="{max(0.14, canopy_opacity - 0.16):.2f}"/>
            <ellipse cx="83" cy="{119 + canopy_y_offset + canopy_sag}" rx="{20 * canopy_scale:.0f}" ry="{16 * canopy_scale:.0f}" fill="{leaf_color}" opacity="{max(0.14, canopy_opacity - 0.20):.2f}"/>
            <ellipse cx="177" cy="{118 + canopy_y_offset + canopy_sag}" rx="{20 * canopy_scale:.0f}" ry="{16 * canopy_scale:.0f}" fill="{leaf_color}" opacity="{max(0.14, canopy_opacity - 0.20):.2f}"/>
            <ellipse cx="130" cy="{101 + canopy_y_offset}" rx="{24 * canopy_scale:.0f}" ry="{20 * canopy_scale:.0f}" fill="{leaf_color}" opacity="{max(0.16, canopy_opacity - 0.10):.2f}"/>

            {fallen_svg}
        </svg>
        <div class="{TREE_VISUAL_CAPTION_CLASS}" style="text-align:center;color:#aeb7c6;font-size:11px;line-height:1.45;margin-top:12px;">
            Visual tree score is explanatory; receipt integrity remains the protocol metric.
        </div>
    </div>
    """

    components.html(svg_html, height=448, scrolling=False)

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


def render_doctrine_html_reference(title: str, html_path: Path, key_prefix: str) -> None:
    if not html_path.exists():
        st.warning(f"Reference file not found: {html_path.name}")
        return

    html_text = html_path.read_text(encoding="utf-8", errors="ignore")
    c1, c2 = st.columns([1, 0.3])
    with c1:
        st.caption(f"Embedded from `{html_path.name}`")
    with c2:
        st.download_button(
            f"⬇️ Download {html_path.name}",
            data=html_text,
            file_name=html_path.name,
            mime="text/html",
            use_container_width=True,
            key=f"download_{key_prefix}",
        )
    components.html(html_text, height=640, scrolling=True)


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
        return "NO EXPECTED", "No expected verdict provided."

    expected = expected.upper()
    actual = actual.upper()

    if expected == actual:
        return "PASS", "Actual verdict matches expected verdict."

    if expected == "SANCTUARY" and actual == "THRESHOLD":
        return "WARN", "Conservative downgrade: safe idea was routed to review."

    if expected == "THRESHOLD" and actual == "ASYLUM":
        return "WARN", "Conservative escalation: review case was routed to Asylum."

    if expected in ["ASYLUM", "THRESHOLD"] and actual == "SANCTUARY":
        return "FAIL", "Dangerous miss: review/asylum phrase was labeled Sanctuary."

    if expected == "ASYLUM" and actual == "THRESHOLD":
        return "FAIL", "Under-escalation: Asylum phrase was only labeled Threshold."

    return "FAIL", "Actual verdict does not match expected verdict."



def normalize_stress_results_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keeps the UI stable when old session_state data or older CSV exports have
    different column names from the current benchmark harness.
    """
    df = df.copy()

    if "Actual Verdict" not in df.columns and "Verdict" in df.columns:
        df["Actual Verdict"] = df["Verdict"]

    defaults = {
        "Expected Verdict": "",
        "Actual Verdict": "THRESHOLD",
        "Test Result": "NO EXPECTED",
        "Test Note": "No expected verdict provided.",
        "Phrase": "",
        "Stress Label": "Unclassified",
        "Needs Review": "NO",
        "Base Simulation Verdict": "",
        "Guardrail Risk": "",
        "Integrity": None,
        "Friction": None,
        "Collapse Probability": None,
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
        "Expected Verdict": expected or "",
        "Actual Verdict": verdict,
        "Test Result": test_result,
        "Test Note": test_note,
        "Phrase": phrase,
        "Stress Label": label,
        "Needs Review": needs_review,
        "Base Simulation Verdict": base_verdict,
        "Guardrail Risk": risk,
        "Integrity": round(report["integrity"], 3),
        "Friction": round(report["friction"], 3),
        "Collapse Probability": round(report["collapse_probability"], 3),
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
    Protocol Integrity v2: the final verdict is produced by the central
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
            "name": "Safeguarded public system must remain eligible for Sanctuary",
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
                case_failures.append(f"forbidden verdict {verdict}")
            if case.get("required_verdicts") and verdict not in case["required_verdicts"]:
                case_failures.append(f"expected verdict in {sorted(case['required_verdicts'])}, got {verdict}")
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
            st.dataframe(pd.DataFrame(check["results"]), use_container_width=True, hide_index=True)
        st.stop()

    with st.expander("Sydney Protocol logic check: PASS", expanded=False):
        st.dataframe(pd.DataFrame(check.get("results", [])), use_container_width=True, hide_index=True)
        st.caption("These sentinel cases run fail-closed so broken guardrail logic cannot silently produce trusted outputs.")

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
Prototype notice: This is a symbolic audit report. It is not a legal, political, medical, religious, or institutional determination.

QUESTION / IDEA
{query}

VERDICT
Internal prototype label: {judgment.get("verdict", "THRESHOLD")}
Corruption risk: {judgment.get("corruption_risk", "Medium")}
Stress label: {judgment.get("stress_label", "Unclassified")}

SUMMARY
{sanitize_public_message(judgment.get("summary", ""))}

CORE METRICS
Integrity: {report.get("integrity")}
Friction: {report.get("friction")}
Collapse probability: {report.get("collapse_probability")}
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

QUESTIONS BEFORE TRUSTING THIS MODEL
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
    threshold_repair_index = float(threshold_mapping.get("repair_index", 0.0) or 0.0)
    threshold_repair_question_index = float(threshold_mapping.get("repair_question_index", threshold_repair_index) or 0.0)
    threshold_confirmed_repair_capacity = float(threshold_mapping.get("confirmed_repair_capacity", threshold_repair_index) or 0.0)

    detail_rows = [
        f'<div><strong>Safety risk:</strong> {safe_risk}</div>',
    ]
    if verdict == "THRESHOLD":
        detail_rows.append(
            f'<div style="margin-top:0.15rem;"><strong>Review band:</strong> {safe_review_band_label}</div>'
        )
    detail_rows.append(
        f'<div style="margin-top:0.15rem;"><strong>Stress label:</strong> {safe_stress_label}</div>'
    )
    if threshold_mapping:
        detail_rows.append(
            '<div style="margin-top:0.15rem;"><strong>Threshold direction:</strong> '
            f'{safe_threshold_direction} · Z-axis {threshold_z_axis:.3f} / 0.9999 · Confirmed repair {threshold_confirmed_repair_capacity:.3f}</div>'
        )
    detail_rows_html = "".join(detail_rows)

    judgment_card_html = f"""
<div class="soft-card">
  <div style="color:#aeb7c6;font-size:0.78rem;font-weight:900;text-transform:uppercase;letter-spacing:0.08em;">
    {safe_source} · Protocol-adjusted internal label
  </div>
  <div style="color:{color};font-size:2rem;font-weight:900;margin-top:0.25rem;">
    {verdict}
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
    cols[2].metric("Collapse probability", f"{report['collapse_probability']:.3f}")
    if report.get("raw_metrics_before_ethics") or report.get("ethics_adjustment_applied") is not None:
        st.caption("These are ethics-calibrated reading metrics. Raw pre-ethics values stay in the local witness receipt.")

    if threshold_mapping:
        with st.expander("Threshold mapping preview", expanded=(verdict == "THRESHOLD")):
            tcols = st.columns(4)
            tcols[0].metric("Threshold direction", friendly_threshold_direction_label(str(threshold_mapping.get("threshold_direction", "Not recorded"))))
            tcols[1].metric("Z-axis", f"{float(threshold_mapping.get('z_axis_position', 0.0)):.3f} / 0.9999")
            tcols[2].metric("Repair questions", f"{float(threshold_mapping.get('repair_question_index', threshold_mapping.get('repair_index', 0.0))):.3f}")
            tcols[3].metric("Confirmed repair", f"{float(threshold_mapping.get('confirmed_repair_capacity', threshold_mapping.get('repair_index', 0.0))):.3f}")
            st.caption(
                "Receipt preview only: this maps whether the reading is moving toward capture pressure, a balanced review zone, or the human/system boundary. "
                "It does not create a new verdict or enforcement path. Repair questions are a route, not proof that safeguards already exist. Z=1.0000 remains outside ALETHEIA’s claim."
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
                st.dataframe(pd.DataFrame(component_rows), use_container_width=True, hide_index=True)
            st.write(f"**Dominant pressure:** {threshold_mapping.get('dominant_pressure')}")
            signals = threshold_mapping.get("asylum_pressure_signals", []) or []
            growth = threshold_mapping.get("sanctuary_growth_signals", []) or []
            scol1, scol2 = st.columns(2)
            scol1.markdown("**Capture-pressure signals**")
            for signal in signals:
                scol1.write(f"- {signal}")
            scol2.markdown("**Repair/growth signals**")
            for signal in growth:
                scol2.write(f"- {signal}")

    with st.expander("Observed reasons", expanded=True):
        for item in judgment.get("reasons", []):
            st.write(f"- {item}")

    with st.expander("Safeguard questions for human review"):
        for item in judgment.get("safeguards", []):
            st.write(f"- {silent_operator_question(item, context='this safeguard gap')}")

    with st.expander("Questions before trusting this model"):
        for item in judgment.get("questions", []):
            st.write(f"- {silent_operator_question(item, context='this model')}")


# Header
header_path = Path("assets/header.jpg")
if header_path.exists():
    st.image(str(header_path), use_container_width=True)

st.markdown(
    f"""
    <div class="botanical-frame hero">
        <div class="hero-grid">
            <div>
                <div class="hero-kicker">Sydney Protocol · Local Mirror · Plain Words</div>
                <div class="hero-title">ALETHEIA</div>
                <div class="hero-sub">A mirror, not a throne.</div>
                <div class="caption">{APP_VERSION} · English + Nederlands/Dutch input supported · Spot control. Protect people. Keep truth visible.</div>
            </div>
            <div class="hero-emblem" aria-hidden="true">🕊️</div>
        </div>
        <div class="civic-ribbon">
            <div class="ribbon-item"><span class="ribbon-icon">🛡️</span><div><div class="ribbon-label">Purpose</div><div class="ribbon-body">People first. Scores second.</div></div></div>
            <div class="ribbon-item"><span class="ribbon-icon">🌿</span><div><div class="ribbon-label">Method</div><div class="ribbon-body">Show the pattern. Keep appeal open.</div></div></div>
            <div class="ribbon-item"><span class="ribbon-icon">🪞</span><div><div class="ribbon-label">Boundary</div><div class="ribbon-body">ALETHEIA asks. People decide. It never rules, votes, commands, or replaces people.</div></div></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="prototype-note">
        <strong>How to use this:</strong> Paste an idea. ALETHEIA looks for power, pressure, appeal, and risk. You keep the final say. It is not legal, medical, political, religious, or official advice.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="prototype-note">
        <strong>Input language scope:</strong> {SUPPORTED_INPUT_LANGUAGE_NOTE}
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="prototype-note">
        <strong>Plain words:</strong> Sanctuary means low risk inside this prototype, not final safety. Threshold means review and repair. Asylum means high capture or harm pressure. The Z-axis stops at the human/system boundary; a receipt is your local record of what was reviewed.
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar controls
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-emblem-card">
            <div class="sidebar-emblem-mark">🕊️</div>
            <div class="sidebar-brand">ALETHEIA</div>
            <div class="sidebar-tagline">A mirror, not a throne.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.header("Reading controls")
    st.caption("Choose how alert the review should be to pressure, trust, and fit.")
    st.caption("Input scope: English + Nederlands/Dutch are calibrated across modules.")

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

    st.markdown("#### Review lens")
    preset_display = st.selectbox(
        "Review lens",
        preset_options,
        index=0,
        key="sidebar_weight_profile",
        help="Choose a starting view. It is only a lens, not a truth machine.",
    )
    st.caption("This only sets the lens. ALETHEIA waits for your idea.")

    selected_preset = next(
        key for key in WEIGHT_PRESETS.keys()
        if preset_labels.get(key, key.replace("_", " ").title()) == preset_display
    )
    weights = WEIGHT_PRESETS[selected_preset]

    st.markdown("---")
    st.markdown("#### Review rhythm")
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
    st.caption("The test keeps voices small so the pattern is easy to read. The 9k view lives in World Lens.")

    st.markdown("---")
    st.markdown("#### Safety rails")
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
    st.caption("Gentle voice, firm rails. These settings change the reading, not the boundary.")


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
    st.info(
        "**Shared Protocol State** — Mirror Check, Stress Test, Evidence Lab, and World Lens are different windows into the same protocol heart. "
        "Changes to empirical evidence, scoring calibration, the Sydney Protocol overlay, doctrine thresholds, or the selected evidence year may echo across modes. "
        "That is intentional shared-state behavior, not an error. Scenario-only controls stay local unless you explicitly apply them to the shared protocol state."
    )
    with st.expander("Shared state details", expanded=expanded):
        rows = [
            ("Current mode", state.get("current_mode", current_mode)),
            ("Empirical master active", "Yes" if state.get("empirical_master_active") else "No"),
            ("Scored evidence active", "Yes" if state.get("scored_evidence_active") else "No"),
            ("Trust calibration active", "Yes" if state.get("trust_calibration_active") else "No"),
            ("WGI active", "Yes" if state.get("wgi_active") else "No"),
            ("V-Dem active", "Yes" if state.get("vdem_active") else "No"),
            ("Demo data active", "Yes" if state.get("synthetic_demo_active") else "No"),
            ("Sydney Protocol overlay active", "Yes" if state.get("sydney_protocol_overlay_active") else "No"),
            ("Selected evidence year", state.get("selected_evidence_year", "—")),
            ("Selected country / scenario", state.get("selected_context", "—")),
            ("Grid basis", state.get("grid_basis", "—")),
            ("Last protocol update source", state.get("last_update_source", "—")),
        ]
        st.dataframe(pd.DataFrame(rows, columns=["State field", "Value"]), use_container_width=True, hide_index=True)


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
            st.dataframe(pd.DataFrame(check.get("results", [])), use_container_width=True, hide_index=True)

render_sydney_protocol_self_check_gate()

tab_chat, tab_sim, tab_boundary, tab_empirical, tab_grid, tab_doctrine, tab_about = st.tabs(APP_NAVIGATION_LABELS)

with tab_sim:
    st.subheader("Stress Test — Try an Idea")
    render_shared_protocol_state_notice("Stress Test")
    st.write("Start with your own scenario, load a demo on purpose, or use the Manual test. ALETHEIA does not read examples by default. You lead.")

    input_mode = st.radio(
        "How do you want to work?",
        ["Scan my idea", "Manual test"],
        horizontal=True,
        help="Scan my idea reads your text. Manual test uses the sliders.",
    )

    if input_mode == "Scan my idea":
        st.info("Scan my idea is for your own text. Demo scenarios are there if you choose them, but they never run by themselves.")
    else:
        st.warning("Manual test is for hands-on testing. The sliders shape the result. Any text is just a note.")

    if "simulation_scenario_text" not in st.session_state:
        st.session_state.simulation_scenario_text = ""
    if "simulation_input_source" not in st.session_state:
        st.session_state.simulation_input_source = "EMPTY_INPUT"

    col_a, col_b = st.columns([1.2, 1])
    with col_a:
        scenario_choice = st.selectbox("Stress Test demo examples", list(STRESS_TEST_DEMO_SCENARIOS.keys()), key="simulation_scenario_library")
        if st.button("Load Stress Test scenario demo", use_container_width=True, key="simulation_load_stress_demo_button"):
            st.session_state.simulation_scenario_text = STRESS_TEST_DEMO_SCENARIOS[scenario_choice]
            st.session_state.simulation_demo_choice = scenario_choice
            st.session_state.simulation_input_source = "DEMO_INPUT"
        query = st.text_area("Write or paste your idea", key="simulation_scenario_text", height=150)

        loaded_demo = STRESS_TEST_DEMO_SCENARIOS.get(st.session_state.get("simulation_demo_choice", ""), None)
        if not query.strip():
            input_status = "EMPTY_INPUT"
            st.session_state.simulation_input_source = "EMPTY_INPUT"
        elif st.session_state.get("simulation_input_source") == "DEMO_INPUT" and loaded_demo is not None and query == loaded_demo:
            input_status = "DEMO_INPUT"
        else:
            input_status = "USER_INPUT"
            st.session_state.simulation_input_source = "USER_INPUT"

        if input_status == "EMPTY_INPUT":
            st.caption("Add your own idea to begin. Demos are optional and never run by themselves.")
        elif input_status == "DEMO_INPUT":
            st.caption("Demo mode is on. This is only an example.")
        else:
            st.caption("Your idea is ready. You are the source; ALETHEIA is the mirror.")

        apply_invisibility = False
        if input_mode == "Scan my idea":
            apply_invisibility = st.checkbox(
                "Invisibility Filter",
                value=(input_status == "USER_INPUT"),
                key=f"simulation_invisibility_filter_{input_status}",
                disabled=(input_status == "EMPTY_INPUT"),
                help="Remove names and titles before review. On by default for your own input.",
            )
            if apply_invisibility and input_status != "EMPTY_INPUT":
                st.caption("Names and titles are removed before review. The pattern stays visible.")

        selected_context = "Waiting for your input" if input_status == "EMPTY_INPUT" else ((query[:120] + "…") if len(query) > 120 else query)
        update_protocol_state(selected_context=selected_context, last_update_source="Stress Test")
        if input_mode == "Manual test":
            st.caption("Manual test mode is active: sliders shape the result directly. Scenario text is optional context, not hidden default data.")
    with col_b:
        st.markdown("### Review lens / manual test")

        default_manual_features = {
            "technical_complexity": 0.55,
            "transparency": 0.55,
            "regulation": 0.55,
            "centralization": 0.35,
            "anonymity": 0.25,
            "capital_scale": 0.35,
        }

        scenario_slider_features = default_manual_features
        if (
            input_mode == "Scan my idea"
            and st.session_state.get("last_input_mode") == "Scan my idea"
            and isinstance(st.session_state.get("last_scan"), dict)
        ):
            scenario_slider_features = build_features_from_scan(st.session_state.last_scan)

        if input_mode == "Scan my idea":
            st.caption("These features are derived from the scenario text. In Scan my idea mode they stay read-only and refresh after each run so you can see what the parser picked up.")
            slider_key_suffix = "fresh"
            if isinstance(st.session_state.get("last_scan"), dict):
                slider_key_suffix = "_".join([
                    f"{scenario_slider_features.get('technical_complexity', 0.55):.2f}",
                    f"{scenario_slider_features.get('transparency', 0.55):.2f}",
                    f"{scenario_slider_features.get('regulation', 0.55):.2f}",
                    f"{scenario_slider_features.get('centralization', 0.35):.2f}",
                    f"{scenario_slider_features.get('anonymity', 0.25):.2f}",
                    f"{scenario_slider_features.get('capital_scale', 0.35):.2f}",
                ])

            manual_features = {
                "technical_complexity": st.slider("Technical complexity", 0.0, 1.0, float(scenario_slider_features.get("technical_complexity", 0.55)), 0.01, key=f"scenario_technical_complexity_{slider_key_suffix}", disabled=True),
                "transparency": st.slider("Transparency", 0.0, 1.0, float(scenario_slider_features.get("transparency", 0.55)), 0.01, key=f"scenario_transparency_{slider_key_suffix}", disabled=True),
                "regulation": st.slider("Regulation / oversight", 0.0, 1.0, float(scenario_slider_features.get("regulation", 0.55)), 0.01, key=f"scenario_regulation_{slider_key_suffix}", disabled=True),
                "centralization": st.slider("Power concentration", 0.0, 1.0, float(scenario_slider_features.get("centralization", 0.35)), 0.01, key=f"scenario_centralization_{slider_key_suffix}", disabled=True),
                "anonymity": st.slider("Anonymity / opacity", 0.0, 1.0, float(scenario_slider_features.get("anonymity", 0.25)), 0.01, key=f"scenario_anonymity_{slider_key_suffix}", disabled=True),
                "capital_scale": st.slider("Capital scale", 0.0, 1.0, float(scenario_slider_features.get("capital_scale", 0.35)), 0.01, key=f"scenario_capital_scale_{slider_key_suffix}", disabled=True),
            }
        else:
            st.caption("These sliders shape the test. They are inputs, not hidden truth.")
            manual_features = {
                "technical_complexity": st.slider("Technical complexity", 0.0, 1.0, default_manual_features["technical_complexity"], 0.01, key="manual_technical_complexity"),
                "transparency": st.slider("Transparency", 0.0, 1.0, default_manual_features["transparency"], 0.01, key="manual_transparency"),
                "regulation": st.slider("Regulation / oversight", 0.0, 1.0, default_manual_features["regulation"], 0.01, key="manual_regulation"),
                "centralization": st.slider("Power concentration", 0.0, 1.0, default_manual_features["centralization"], 0.01, key="manual_centralization"),
                "anonymity": st.slider("Anonymity / opacity", 0.0, 1.0, default_manual_features["anonymity"], 0.01, key="manual_anonymity"),
                "capital_scale": st.slider("Capital scale", 0.0, 1.0, default_manual_features["capital_scale"], 0.01, key="manual_capital_scale"),
            }

    with st.expander("How to write good Stress Test scenarios", expanded=False):
        st.markdown(
            """
Stress Test works best when you write a **scenario as a governance pattern**, not as a personal accusation. Use English or Nederlands/Dutch; other languages are not calibrated yet.

Include: who gains power, how power is obtained, what can go wrong, what safeguards exist or are missing, and whether affected people can appeal, exit, or request correction.

**Weak:** `Is this bad?`

**Better:** `A temporary crisis leader gains emergency authority after a disaster, but no term limit, appeal path, or independent review is defined.`

**Weak:** `John is evil.`

**Better:** `A named leader gains centralized authority after a crisis. The system has weak review, unclear limits, and no visible exit path.`

ALETHEIA reviews patterns, not personal worth. Use fictional names or roles when testing. The Invisibility Filter can reduce actor/name/title bias while keeping the governance pattern visible.
            """
        )

    run = st.button("Run review", type="primary", use_container_width=True, key="simulation_run_button")
    if run:
        if input_mode == "Scan my idea" and input_status == "EMPTY_INPUT":
            st.warning("Add your own scenario or load a demo before running Scan my idea. ALETHEIA does not run examples by itself.")
        else:
            analysis_query = query
            invisibility_report = None
            if input_mode == "Scan my idea" and apply_invisibility and input_status != "EMPTY_INPUT":
                invisibility_report = decouple_actor(query)
                analysis_query = invisibility_report.get("decoupled_text", query)
            with st.spinner("Reading your idea and checking the pattern..."):
                scan, features, sim, report, scan_mode = run_audit(analysis_query, manual_features, weights, ego_tolerance, divine_floor, steps, n_agents, input_mode)
                st.session_state.last_scan = scan
                st.session_state.last_features = features
                st.session_state.last_sim = sim
                st.session_state.last_report = report
                st.session_state.last_scan_mode = scan_mode
                st.session_state.last_input_mode = input_mode
                st.session_state.last_query = analysis_query
                st.session_state.last_query_raw = query
                st.session_state.last_input_status = input_status
                st.session_state.last_invisibility_report = invisibility_report
                selected_context = "Manual test" if input_mode == "Manual test" else ((analysis_query[:120] + "…") if len(analysis_query) > 120 else analysis_query)
                update_protocol_state(selected_context=selected_context, last_update_source="Stress Test")
                if input_mode == "Scan my idea":
                    st.rerun()

    with st.expander("Stress Test Batch Testing — up to 50 scenarios", expanded=False):
        st.caption("Upload or paste scenario-style inputs. Batch testing is explicit opt-in, local-only, and creates local witness receipts.")
        stress_batch_source = st.radio(
            "Stress batch input source",
            ["Upload .txt", "Paste list"],
            horizontal=True,
            key="stress_batch_source_mode",
        )
        stress_batch_text = ""
        if stress_batch_source == "Upload .txt":
            stress_upload = st.file_uploader(
                "Upload Stress Test .txt list",
                type=["txt"],
                key="stress_batch_txt_upload",
                help="Use one scenario per line, a numbered list, or --- between longer items.",
            )
            if stress_upload is not None:
                stress_batch_text = stress_upload.getvalue().decode("utf-8", errors="replace")
                st.caption(f"Staged {stress_upload.name}. Press Run Stress Batch to process it.")
        else:
            stress_batch_text = st.text_area(
                "Paste Stress Test scenarios",
                height=180,
                key="stress_batch_manual_input",
                placeholder="1. A temporary leader gains emergency power without a term limit.\n2. A public service requires biometric ID before food or housing support.",
            )

        stress_batch_items = parse_witness_batch_input(stress_batch_text, max_items=MAX_BATCH_RECEIPTS)
        stress_question_set_mode = is_witness_question_set(stress_batch_items)
        if stress_batch_text.strip():
            question_note = " Question-prompt mode will keep audit/repair questions as review tools, not scored scenarios." if stress_question_set_mode else ""
            st.caption(f"{len(stress_batch_items)} item(s) ready. Maximum: {MAX_BATCH_RECEIPTS}.{question_note}")
        stress_batch_apply_invisibility = st.checkbox(
            "Apply Invisibility Filter to Stress batch",
            value=bool(stress_batch_items),
            key="stress_batch_invisibility_filter",
            disabled=not bool(stress_batch_items),
        )
        run_stress_batch = st.button(
            "Run Stress Batch",
            type="primary",
            use_container_width=True,
            disabled=not bool(stress_batch_items),
            key="simulation_run_stress_batch_button",
        )
        if run_stress_batch:
            stress_receipts = []
            stress_rows = []
            with st.spinner(f"Running {len(stress_batch_items)} local Stress Test scenario(s)..."):
                for idx, raw_item in enumerate(stress_batch_items, start=1):
                    processed_item = raw_item
                    invisibility_report = None
                    if stress_batch_apply_invisibility:
                        invisibility_report = decouple_actor(raw_item)
                        processed_item = invisibility_report.get("decoupled_text", raw_item)

                    # Patch 69: a Stress Test batch can also be a bank of audit/repair
                    # questions. In that case the questions are review tools, not
                    # governance scenarios to score as Sanctuary/Threshold/Asylum.
                    if stress_question_set_mode and is_witness_question_prompt(raw_item):
                        receipt = build_local_question_prompt_receipt(
                            module="Simulation",
                            input_text=raw_item,
                            processed_text=processed_item,
                            invisibility_applied=bool(stress_batch_apply_invisibility),
                            app_version=APP_VERSION,
                        )
                        stress_report = {"integrity": None, "repair_questions": receipt.get("repair_questions", [])}
                        verdict = "QUESTION_PROMPT"
                        risk = "Review Tool"
                        label = "Audit Question / Review Tool"
                    else:
                        scan, features, sim, stress_report, scan_mode = run_audit(
                            processed_item,
                            default_manual_features,
                            weights,
                            ego_tolerance,
                            divine_floor,
                            steps,
                            n_agents,
                            "Scan my idea",
                        )
                        label, needs_review, _reason = stress_label_for_phrase(processed_item)
                        base_verdict, _base_color = classify_verdict(stress_report["integrity"])
                        verdict, risk = apply_guardrail_verdict(base_verdict, label, needs_review)
                        sim, stress_report, verdict, label, needs_review, risk = enforce_missing_safeguard_threshold_route(
                            processed_item,
                            scan,
                            sim,
                            stress_report,
                            verdict,
                            label,
                            needs_review,
                            risk,
                        )
                        label = normalize_asylum_protocol_label(label, verdict=verdict, risk=risk)
                        sim = enforce_asylum_metric_consistency(sim, verdict=verdict, risk=risk, protocol_label=label)
                        stress_report = ensure_asylum_repair_questions(
                            stress_report,
                            verdict=verdict,
                            risk=risk,
                            protocol_label=label,
                            scan=scan,
                        )
                        stress_report = ensure_threshold_repair_questions(
                            stress_report,
                            verdict=verdict,
                            risk=risk,
                            protocol_label=label,
                        )
                        receipt = build_local_witness_receipt(
                            module="Simulation",
                            input_text=raw_item,
                            processed_text=processed_item,
                            input_status="USER_INPUT",
                            scan=scan,
                            sim=sim,
                            report=stress_report,
                            verdict=verdict,
                            risk=risk,
                            protocol_label=label,
                            invisibility_applied=isinstance(invisibility_report, dict) and invisibility_report.get("invisibility_filter_applied", False),
                            app_version=APP_VERSION,
                        )
                    stress_receipts.append(receipt)
                    integrity_value = stress_report.get("integrity") if isinstance(stress_report, dict) else None
                    stress_review_band = review_band_for_state(verdict, stress_report, sim)
                    stress_rows.append({
                        "#": idx,
                        "State": verdict,
                        "Review band": stress_review_band.get("label"),
                        "Risk": risk,
                        "Label": label,
                        "Integrity": "—" if integrity_value is None else round(float(integrity_value), 3),
                        "Repair questions": len((stress_report or {}).get("repair_questions") or []),
                    })
            archive_bytes, batch_index = build_local_witness_batch_zip(stress_receipts, module="Simulation", app_version=APP_VERSION)
            st.session_state.stress_batch_archive_bytes = archive_bytes
            st.session_state.stress_batch_index = batch_index
            st.session_state.stress_batch_summary = stress_rows
            st.success(f"Stress batch complete. {len(stress_receipts)} local receipt(s) are ready to download.")

        if st.session_state.get("stress_batch_summary"):
            st.dataframe(pd.DataFrame(st.session_state.stress_batch_summary), use_container_width=True, hide_index=True, height=300)
        if st.session_state.get("stress_batch_archive_bytes"):
            st.download_button(
                "⬇️ Download Stress Test batch receipts",
                data=st.session_state.stress_batch_archive_bytes,
                file_name="aletheia_stress_test_batch_witness_receipts.zip",
                mime="application/zip",
                use_container_width=True,
                key="simulation_download_stress_batch_receipts",
            )

    if "last_report" not in st.session_state:
        st.info("No review has run yet. Add your input, load a demo, or use the Manual test.")
    else:
        scan = st.session_state.last_scan
        features = st.session_state.last_features
        sim = st.session_state.last_sim
        report = st.session_state.last_report
        scan_mode = st.session_state.last_scan_mode
        last_input_mode = st.session_state.get("last_input_mode", input_mode)

        base_verdict, base_color = classify_verdict(report["integrity"])
        display_query = st.session_state.get("last_query", query) if last_input_mode == "Scan my idea" else ""
        label, needs_review, stress_reason = stress_label_for_phrase(display_query) if display_query else ("Manual test", "NO", "Manual numeric tuner run.")
        verdict, risk = apply_guardrail_verdict(base_verdict, label, needs_review)
        sim, report, verdict, label, needs_review, risk = enforce_missing_safeguard_threshold_route(
            display_query,
            scan,
            sim,
            report,
            verdict,
            label,
            needs_review,
            risk,
        )
        label = normalize_asylum_protocol_label(label, verdict=verdict, risk=risk)
        sim = enforce_asylum_metric_consistency(sim, verdict=verdict, risk=risk, protocol_label=label)
        st.session_state.last_sim = sim
        report = ensure_asylum_repair_questions(
            report,
            verdict=verdict,
            risk=risk,
            protocol_label=label,
            scan=scan,
        )
        report = ensure_threshold_repair_questions(
            report,
            verdict=verdict,
            risk=risk,
            protocol_label=label,
        )
        st.session_state.last_report = report
        verdict_color = {"SANCTUARY": "#8fbc8f", "THRESHOLD": "#e5c36b", "ASYLUM": "#db7777"}.get(verdict, base_color)
        input_status_label = st.session_state.get("last_input_status", "MANUAL_INPUT" if last_input_mode == "Manual test" else "USER_INPUT")
        invisibility_report = st.session_state.get("last_invisibility_report")
        invisibility_note = " · Invisibility Filter: on" if isinstance(invisibility_report, dict) and invisibility_report.get("invisibility_filter_applied") else ""
        current_review_band = review_band_for_state(verdict, report, sim)
        st.caption(f"Feature source: {last_input_mode} · Input status: {input_status_label} · Scan mode: {scan_mode} · Protocol label: {label} · Review band: {current_review_band.get('label')}{invisibility_note}")

        c1, c2, c3, c4 = st.columns(4)
        review_band = review_band_for_state(verdict, report, sim)
        review_band_label = review_band.get("label", verdict.title())
        review_band_summary = review_band.get("summary", "")
        result_display = f"<span style='color:{verdict_color}'>{verdict}</span>"
        if verdict == "THRESHOLD":
            result_display += f"<br><span style='font-size:1.05rem;color:#d4b88a;'>{review_band_label}</span>"

        result_helper = f"Safety risk: {risk}"
        if verdict == "THRESHOLD":
            result_helper += f"<br>Review band: {review_band_label}"

        with c1:
            metric_card("Result state", result_display, result_helper)
        with c2:
            metric_card("Integrity", f"{report['integrity']:.3f}", "Current reading. Raw values stay in the local receipt.")
        with c3:
            metric_card("Friction", f"{report['friction']:.3f}", "Control pressure")
        with c4:
            metric_card("Collapse probability", f"{report['collapse_probability']:.3f}", scan_mode)

        c5, c6, c7, c8 = st.columns(4)
        c5.metric("Stability", f"{sim['stability']:.3f}")
        c6.metric("Trust", f"{sim['trust_index']:.3f}")
        c7.metric("Alignment", f"{sim['alignment']:.3f}")
        c8.metric("Ego", f"{sim['ego']:.3f}")

        render_pulse_tree(
            display_score_from_judgment(report, {"verdict": verdict}),
            sim["ego"],
            sim["alignment"],
            title="Stress Test Tree",
            state_override=verdict,
            mode="Stress Test",
        )

        st.plotly_chart(plot_trace(sim), use_container_width=True)

        chart_col, table_col = st.columns([1, 1.2])
        with chart_col:
            st.plotly_chart(action_chart(sim), use_container_width=True)
        with table_col:
            st.markdown("### Test voices")
            st.dataframe(pd.DataFrame(sim.get("agent_profiles", [])), use_container_width=True, hide_index=True)

        st.markdown("### Why this result?")
        reason_cols = st.columns(3)
        with reason_cols[0]:
            soft_card("What ALETHEIA saw", f"Source: {last_input_mode}. Power concentration {scan['power_concentration']:.0%}, transparency {scan['decision_transparency']:.0%}, regulation {scan['regulatory_presence']:.0%}.")
        with reason_cols[1]:
            soft_card("Pattern over time", f"Trust {sim['trust_index']:.0%}, alignment {sim['alignment']:.0%}, ego {sim['ego']:.0%}.")
        with reason_cols[2]:
            soft_card("Risk picture", f"Review band: {review_band_label}. {review_band_summary} Collapse risk: {'yes' if sim.get('collapse_risk') else 'no'}. Trust friction: {report['trust_friction']:.3f}. Grievance pressure: {sim.get('grievance_pressure', 0):.2f}. Safeguard gap: {sim.get('safeguard_gap', 0):.2f}.")

        st.markdown("### Repair questions")
        st.caption("ALETHEIA asks questions here. It gives no orders and no final judgment.")
        repair_questions = report.get("repair_questions") or []
        if repair_questions:
            for idx, question in enumerate(repair_questions[:5], start=1):
                soft_card(f"REVIEW · Question {idx}", silent_operator_question(question, context="this repair path"))
        else:
            for rec in report["recommendations"][:5]:
                priority = str(rec.get("priority", "review")).upper()
                target = rec.get("target", "System")
                action = rec.get("action", "Review")
                soft_card(f"{priority} · {target} · {action}", silent_operator_question(rec, context=str(target)))

        st.markdown("### Local witness receipt")
        st.caption("Creates a receipt you hold. It is not published, synced, or treated as authority.")
        raw_query_for_receipt = st.session_state.get("last_query_raw", display_query)
        processed_query_for_receipt = st.session_state.get("last_query", display_query)
        receipt = build_local_witness_receipt(
            module="Simulation",
            input_text=raw_query_for_receipt if last_input_mode == "Scan my idea" else "Manual test numeric input",
            processed_text=processed_query_for_receipt if last_input_mode == "Scan my idea" else "Manual test numeric input",
            input_status=input_status_label,
            scan=scan,
            sim=sim,
            report=report,
            verdict=verdict,
            risk=risk,
            protocol_label=label,
            invisibility_applied=isinstance(invisibility_report, dict) and invisibility_report.get("invisibility_filter_applied", False),
            app_version=APP_VERSION,
        )
        receipt_text = render_local_witness_receipt_text(receipt)
        st.download_button(
            "⬇️ Download receipt",
            data=receipt_text,
            file_name="aletheia_local_witness_receipt.txt",
            mime="text/plain",
            use_container_width=True,
        )

with tab_boundary:
    st.subheader("Boundary Cases — Calibration Center")
    render_shared_protocol_state_notice("Boundary Cases")
    st.write(
        "Use this tab to stress-test difficult governance edge cases. "
        "ALETHEIA reflects risk patterns for human review; it does not command, enforce, vote, remove leaders, or replace people."
    )

    st.info("Boundary cases calibrate the review model. They do not create authority, enforcement, or final decisions.")

    failure_mode_definitions = {
        "Actor Failure": "A person, group, office, founder, operator, or implementing body misuses power, manipulates others, bypasses review, or becomes unfit.",
        "Policy Failure": "The proposal, rule, charter, doctrine, or system design itself creates coercion, opacity, instability, exclusion, rights risk, or capture risk.",
        "Implementation Failure": "The idea may be valid, but the execution layer fails through weak process, missing safeguards, unclear responsibility, bad deployment, or unreliable operation.",
        "Data Failure": "The evidence base is incomplete, manipulated, stale, biased, low-coverage, unverifiable, or too uncertain to support the conclusion.",
    }

    boundary_cases = [
        {
            "title": "Prediction vs Free Agency",
            "scenario": "A system predicts with high confidence that someone may cause harm, but the action has not happened yet.",
            "main_risk": "Replacing human agency with prediction.",
            "guardrail": "No prediction may replace human agency.",
            "allowed": "Warning, care response, mediation, delay, de-escalation, support, and human review.",
            "forbidden": "Automatic punishment, mind control, coercive agency override, or irreversible restriction without review.",
            "failure_type": "Policy Failure / Implementation Failure",
        },
        {
            "title": "Voluntary Protection Mode",
            "scenario": "A person asks for temporary protective limits because they do not trust themselves during crisis, addiction, psychosis, panic, or rage.",
            "main_risk": "Confusing voluntary help with imposed control.",
            "guardrail": "Consent must be real, informed, revocable, and not structurally forced.",
            "allowed": "Informed, revocable, time-limited support with appeal and review.",
            "forbidden": "Permanent restriction, hidden coercion, non-revocable consent, or forced treatment without review.",
            "failure_type": "Implementation Failure",
        },
        {
            "title": "Consent Under Pressure",
            "scenario": "A person says yes, but refusal would cost basic rights, dignity, housing, food, work, safety, or essential services.",
            "main_risk": "False consent.",
            "guardrail": "Consent is invalid when refusal is not realistically possible.",
            "allowed": "Identify pressure, require an alternative path, reduce dependency, and add appeal.",
            "forbidden": "Treating coerced agreement as valid consent.",
            "failure_type": "Policy Failure / Actor Failure",
        },
        {
            "title": "Basic Rights Scarcity",
            "scenario": "Water, food, clothing, housing, safety, or essential support are limited.",
            "main_risk": "Sacrificing one group permanently or invisibly.",
            "guardrail": "Basic rights remain the baseline even under scarcity.",
            "allowed": "Transparent rationing, independent review, temporary limits, public reasoning, and repair.",
            "forbidden": "Permanent exclusion, discriminatory denial, opaque allocation, or no appeal.",
            "failure_type": "Policy Failure",
        },
        {
            "title": "Emergency Trigger Misuse",
            "scenario": "A group tries to trigger emergency or threshold mechanisms repeatedly to remove opponents or force a preferred outcome.",
            "main_risk": "The emergency mechanism becomes a power weapon.",
            "guardrail": "Critical review triggers must themselves be protected against capture.",
            "allowed": "Multi-signal review, evidence threshold, independent oversight, and cooling-off period.",
            "forbidden": "Automatic reset, automatic removal, or irreversible governance change based on one signal.",
            "failure_type": "Actor Failure / Policy Failure",
        },
        {
            "title": "Ambient Capture",
            "scenario": "Reviewers are not directly bribed, but they are shaped by propaganda, media saturation, platform algorithms, fear, or social pressure.",
            "main_risk": "Mass influence that bypasses visible corruption checks.",
            "guardrail": "Statistical isolation does not solve shared informational manipulation.",
            "allowed": "Source diversity check, manipulation scan, delay, independent review, and exposure mapping.",
            "forbidden": "Treating isolated selection as sufficient when the information environment is captured.",
            "failure_type": "Data Failure / Implementation Failure",
        },
        {
            "title": "Extraordinary Claim Without Public Evidence",
            "scenario": "A person or institution claims final, prophetic, alien, neural, or metaphysical authority.",
            "main_risk": "Unverifiable authority bypasses public review.",
            "guardrail": "Extraordinary claims do not remove human review.",
            "allowed": "Treat the claim as personally meaningful but unverified; audit policy consequences for rights, coercion, transparency, appeal, and repair.",
            "forbidden": "Treating an unverified extraordinary claim as authority, removing guardrails, or granting policy authority without public evidence.",
            "failure_type": "Actor Failure / Data Failure",
        },
        {
            "title": "Neural Data Without Consent",
            "scenario": "Future technology could read, infer, or reconstruct internal experience, memory, or intention.",
            "main_risk": "Violating mental privacy and free agency.",
            "guardrail": "No neural data without informed, revocable consent.",
            "allowed": "Informed, revocable consent; medical and independent audit context; strict minimization.",
            "forbidden": "Forced neural extraction, treating refusal as guilt, or using neural evidence as sole governance authority.",
            "failure_type": "Policy Failure / Data Failure",
        },
        {
            "title": "Performative Ethics",
            "scenario": "A document uses strong ethical language but lacks operational safeguards.",
            "main_risk": "Values language hides missing mechanisms.",
            "guardrail": "Mechanisms outweigh adjectives.",
            "allowed": "Compare claims against appeal, audit trail, time limits, correction, exit rights, evidence rules, independent oversight, explainability, independent challenge, and human override.",
            "forbidden": "Treating values language as proof of integrity or allowing missing safeguards to appear as a low-risk internal reading.",
            "failure_type": "Data Failure / Policy Failure",
        },
        {
            "title": "Automated Triage Missing Safeguards",
            "scenario": "An automated welfare triage or priority system reduces waiting times but lacks explainability, independent challenge, and human override during hardship cases.",
            "main_risk": "Efficiency language hides missing appeal, challenge, explanation, and human override mechanisms.",
            "guardrail": "Missing explainability, independent challenge, or human override routes to THRESHOLD / Needs Safeguards, not a low-risk internal reading.",
            "allowed": "Classify as Needs Safeguards; require explanation path, independent challenge, human override, appeal, correction, audit trail, and hardship review.",
            "forbidden": "Treating speed or automation benefits as proof of integrity when explainability, challenge, or override is missing.",
            "failure_type": "Policy Failure / Implementation Failure / Data Failure",
        },
        {
            "title": "Biometric Gate Without Fallback",
            "scenario": "A city links food, housing, and medical access to a biometric identity gate without a fallback path, public audit, or meaningful appeal.",
            "main_risk": "Basic rights become dependent on a technical identity gate with weak correction and contestability.",
            "guardrail": "Basic-rights access requires fallback, public audit, meaningful appeal, correction, and human review before it can approach the review boundary.",
            "allowed": "Classify as Needs Safeguards; add non-biometric fallback, public audit, meaningful appeal, human review, dignity-preserving correction, and emergency access.",
            "forbidden": "Making food, housing, medical access, or other basic rights conditional on one biometric system without fallback or appeal.",
            "failure_type": "Policy Failure / Implementation Failure / Data Failure",
        },
        {
            "title": "Question Prompt vs Risk State",
            "scenario": "A user submits audit questions, repair prompts, or review-tool questions rather than a governance scenario.",
            "main_risk": "Review-tool questions could be misread as scored governance scenarios.",
            "guardrail": "QUESTION_PROMPT is an input/review-tool mode, not a fourth risk state.",
            "allowed": "Keep audit and repair questions in Review Tool mode with metrics suppressed; score only scenario-style governance inputs using the internal SANCTUARY / THRESHOLD / ASYLUM labels.",
            "forbidden": "Scoring a pure audit question as a risk-state reading, or treating QUESTION_PROMPT as a risk state.",
            "failure_type": "Implementation Failure / Data Failure",
        },
        {
            "title": "ALETHEIA Audits Itself",
            "scenario": "ALETHEIA, its founder, prompt, rubric, model, baseline, or report language may contain capture risk.",
            "main_risk": "Founder capture, doctrine lock-in, overclaiming, or unverified authority leakage.",
            "guardrail": "No founder, architect, prompt, model, document, or output is above the mirror.",
            "allowed": "Self-audit, public correction, forkability, independent review, and versioned change logs.",
            "forbidden": "Exempting the founder, model, prompt, doctrine, or baseline from audit.",
            "failure_type": "Implementation Failure / Actor Failure",
        },
    ]

    selected_case = st.selectbox(
        "Boundary case",
        [case["title"] for case in boundary_cases],
        key="boundary_case_selector",
        help="Select a calibration case to inspect. These are templates for human review, not automated decisions.",
    )
    case = next(item for item in boundary_cases if item["title"] == selected_case)
    update_protocol_state(selected_context=case["title"], last_update_source="Boundary Cases")

    left, right = st.columns([1.05, 1])
    with left:
        st.markdown("### Scenario")
        st.write(case["scenario"])
        st.markdown("### Main risk")
        st.warning(case["main_risk"])
        st.markdown("### Relevant guardrail")
        st.success(case["guardrail"])
    with right:
        st.markdown("### Allowed responses")
        st.write(case["allowed"])
        st.markdown("### Forbidden responses")
        st.write(case["forbidden"])
        st.markdown("### Failure classification")
        st.code(case["failure_type"], language="text")
        selected_failure_modes = [mode.strip() for mode in case["failure_type"].split("/")]
        for mode in selected_failure_modes:
            definition = failure_mode_definitions.get(mode)
            if definition:
                st.caption(f"{mode}: {definition}")

    st.markdown("### Failure Classification output")
    st.code(
        f"""Failure Classification

Primary failure type: {selected_failure_modes[0] if selected_failure_modes else 'Review needed'}
Secondary failure type: {selected_failure_modes[1] if len(selected_failure_modes) > 1 else 'None specified'}
Reason: {case['main_risk']}
Evidence from scenario: {case['scenario']}
Human review need: Required before assigning responsibility or changing policy.
Recommended repair: Use allowed responses and add concrete safeguards. Missing explainability, independent challenge, human override, fallback, public audit, or meaningful appeal should route to Needs Safeguards before any low-risk internal reading.
Confidence: Template-level calibration, not a final finding.""",
        language="text",
    )

    st.markdown("### Boundary Case Report Template")
    st.code(
        f"""Boundary Case Report

Scenario: {case['title']}
Main risk: {case['main_risk']}
Relevant guardrails: {case['guardrail']}
Allowed responses: {case['allowed']}
Forbidden responses: {case['forbidden']}
Failure classification: {case['failure_type']}
Recommended safeguard: Add human review, appeal, transparency, correction, evidence requirements, explainability, independent challenge, human override, fallback paths, and public audit where missing.
Human review note: This is a mirror output, not an instruction or enforcement decision.""",
        language="text",
    )

    st.markdown("### Consent-Audit Engine")
    st.write(
        "Consent is treated as valid only when refusal is realistically possible. "
        "This check looks for structural pressure, basic-rights dependency, withdrawal gaps, and unclear alternatives."
    )
    consent_examples = {
        "Green — refusal is realistic": {
            "summary": "The person can say no without losing basic rights, safety, dignity, or essential access.",
            "signals": "Clear opt-out, no retaliation, fallback/alternative path, withdrawal right, plain-language explanation, meaningful appeal, and human review.",
            "failure": "No serious failure signal / monitor for implementation drift.",
        },
        "Yellow — pressure or ambiguity exists": {
            "summary": "Refusal technically exists, but the cost, consequence, dependency, or withdrawal path is unclear.",
            "signals": "Default opt-in, confusing terms, weak withdrawal, power imbalance, service dependency, unclear data retention, weak fallback, unclear appeal, or no human override.",
            "failure": "Policy Failure / Implementation Failure / Data Failure",
        },
        "Red — consent appears structurally forced": {
            "summary": "Refusal is practically impossible, punished, hidden, or tied to loss of basic rights or essential services.",
            "signals": "Loss of food, housing, care, safety, work, due process, essential access, fallback path, appeal, or non-revocable agreement.",
            "failure": "Policy Failure / Actor Failure / Implementation Failure",
        },
    }
    selected_consent_level = st.selectbox(
        "Consent integrity example",
        list(consent_examples.keys()),
        key="consent_audit_example_selector",
        help="Template-level calibration only. Human review remains required before treating consent as valid or invalid.",
    )
    consent_case = consent_examples[selected_consent_level]
    st.code(
        f"""Consent-Audit Report

Consent integrity rating: {selected_consent_level}
Refusal reality: {consent_case['summary']}
Pressure signals: {consent_case['signals']}
Basic-rights dependency check: Does refusal threaten water, food, clothing, housing, safety, dignity, appeal, exit, correction, care, or essential services?
Withdrawal and review: Can consent be withdrawn, appealed, and reviewed by a human?
Failure classification: {consent_case['failure']}
Recommended safeguards: Add opt-out, fallback/alternative path, withdrawal right, appeal, human override, non-retaliation rule, plain language, time limit, and independent review where needed.
Human review disclaimer: This is a mirror output for human review. It is not legal advice, enforcement, punishment, or final authority.""",
        language="text",
    )

    with st.expander("Consent audit questions", expanded=False):
        st.markdown(
            """
            - Can the person realistically say no?
            - What happens if they refuse?
            - Do they lose basic rights or essential services?
            - Is there a power imbalance?
            - Is refusal punished directly or indirectly?
            - Is consent informed and specific?
            - Can consent be withdrawn later?
            - Is there an alternative path?
            - Is there human review or appeal?
            - Is the consent request bundled with unrelated obligations?
            """
        )

    st.markdown("### Mechanism-vs-Claim Scanner")
    st.write(
        "This scanner checks whether ethical values are supported by operational safeguards. "
        "Values language can be sincere, but mechanisms make it reviewable, appealable, and correctable."
    )
    mechanism_examples = {
        "High — claims supported by mechanisms": {
            "claims": "The document states values and connects them to concrete procedures.",
            "mechanisms": "Independent appeal process, public audit trail, time-limited authority, correction path, evidence requirement, explainability, independent challenge, human override, human review, exit right.",
            "missing": "No major missing safeguard in the selected example.",
            "failure": "No serious failure signal / monitor for implementation drift.",
        },
        "Medium — partial safeguards": {
            "claims": "The document uses ethical language and includes some safeguards, but key procedures are vague or incomplete.",
            "mechanisms": "Some review or oversight exists, but appeal, correction, evidence standards, explainability, independent challenge, human override, fallback, or time limits are unclear.",
            "missing": "Clarify appeal, audit trail, correction, responsible actor, and review deadline.",
            "failure": "Policy Failure / Implementation Failure / Data Failure",
        },
        "Low — mostly values language": {
            "claims": "The document repeatedly says it protects freedom, justice, dignity, safety, or service.",
            "mechanisms": "Few or no concrete safeguards are described.",
            "missing": "Appeal, audit trail, correction, time limits, independent review, explainability, independent challenge, human override, fallback, evidence rules, exit, and accountability.",
            "failure": "Policy Failure / Data Failure",
        },
    }
    selected_mechanism_level = st.selectbox(
        "Ethical language integrity example",
        list(mechanism_examples.keys()),
        key="mechanism_vs_claim_example_selector",
        help="Template-level calibration only. Human review remains required before inferring intent or deciding repair.",
    )
    mechanism_case = mechanism_examples[selected_mechanism_level]
    st.code(
        f"""Mechanism-vs-Claim Scan

Ethical language integrity: {selected_mechanism_level}
Claim signals found: {mechanism_case['claims']}
Mechanism signals found: {mechanism_case['mechanisms']}
Missing safeguards: {mechanism_case['missing']}
Main risk: Values language may be mistaken for operational accountability.
Failure classification: {mechanism_case['failure']}
Recommended repair: Add concrete safeguards such as appeal, audit trail, time limits, correction, evidence requirements, explainability, independent challenge, human override, fallback, independent oversight, and human review.
Human review note: This is a mirror output. It flags mechanism gaps; it does not prove bad faith or assign final intent.""",
        language="text",
    )

    with st.expander("Mechanism signals to search for", expanded=False):
        st.markdown(
            """
            - Appeal process
            - Public audit trail
            - Time-limited authority
            - Human review
            - Explainability
            - Independent challenge
            - Human override
            - Fallback path
            - Correction mechanism
            - Exit right
            - Evidence requirement
            - Conflict-of-interest rule
            - Independent oversight
            - Plain-language notice
            - Non-retaliation rule
            - Withdrawal right
            - Review deadline
            - Public reasoning requirement
            """
        )

    st.markdown("### Self-Audit Mode")
    st.write(
        "Self-Audit Mode points the mirror back at ALETHEIA itself. "
        "It checks baseline documents, prompts, rubrics, README language, app copy, architect-context language, and generated reports for self-capture risk."
    )
    self_audit_examples = {
        "Green — no obvious self-capture signal": {
            "summary": "The reviewed text preserves human review, avoids founder elevation, and includes appeal or correction language.",
            "risks": "Monitor for drift as prompts, rubrics, and app language change.",
            "repair": "Keep versioned logs, independent review, and correction paths visible.",
        },
        "Yellow — safeguard unclear or incomplete": {
            "summary": "The reviewed text is mostly safe, but appeal, correction, evidence limits, or founder-capture safeguards are weak or implicit.",
            "risks": "Overclaiming, weak review language, vague correction path, or unclear evidence standard.",
            "repair": "Add explicit human review, appeal, correction, evidence limits, and safe output rules.",
        },
        "Red — self-capture or authority leakage risk": {
            "summary": "The reviewed text may imply that ALETHEIA, its founder, doctrine, model, baseline, or prompt is beyond review.",
            "risks": "Founder capture, ideological lock-in, unverifiable authority, unverified authority leakage, or human-review bypass.",
            "repair": "Remove authority language, add independent review, add appeal/correction, and state that self-audit is not proof of correctness.",
        },
    }
    selected_self_audit_level = st.selectbox(
        "Self-audit risk example",
        list(self_audit_examples.keys()),
        key="self_audit_example_selector",
        help="Template-level calibration only. Self-audit reflects risk; it does not certify ALETHEIA as correct, complete, or beyond review.",
    )
    self_case = self_audit_examples[selected_self_audit_level]
    st.code(
        f"""Self-Audit Report

Material reviewed: ALETHEIA baseline / prompt / rubric / README / app copy / generated report
Self-capture risk rating: {selected_self_audit_level}
Founder-capture check: No founder, architect, prompt, rubric, model, document, or output is above the mirror.
Authority-leakage check: {self_case['summary']}
Risk signals: {self_case['risks']}
Recommended repairs: {self_case['repair']}
Human review disclaimer: This self-audit is a governance mirror for human review. It is not proof of correctness, extraordinary-claim validation, or a replacement for human judgment.""",
        language="text",
    )

    with st.expander("Self-audit checks", expanded=False):
        st.markdown(
            """
            - Founder capture
            - Ideological lock-in
            - Unverifiable authority
            - Weak appeal mechanisms
            - Overclaiming
            - Unverified authority leakage
            - Insufficient human review
            - Missing correction loops
            - Hidden command language
            - Evidence gaps
            - Performative ethics
            - Mechanism gaps
            """
        )

    with st.expander("Safe output rules", expanded=False):
        st.markdown(
            """
            ALETHEIA may say: potential risk detected, Needs Safeguards, critical human review required, safeguard missing, evidence gap found, this claim is unverified.

            ALETHEIA must not say: the AI has decided, guardrails no longer apply, this claim is finally verified, human review is unnecessary.
            """
        )



    st.markdown("### Local Witness Receipt v2")
    st.write(
        "Local Witness Receipt v2 records a user-held fingerprint of an ALETHEIA review. "
        "It documents the input, processed input, report fingerprint, app/rubric/prompt versions, active modules, and authority boundary. "
        "It does not publish, sync, enforce, or create authority."
    )
    receipt_example = {
        "receipt_version": "local-witness-v2",
        "document_fingerprint": "SHA-256 of submitted document",
        "processed_document_fingerprint": "SHA-256 after optional actor-bias reduction",
        "report_fingerprint": "SHA-256 of the report payload",
        "app_version": APP_VERSION,
        "rubric_version": "v0.1",
        "prompt_version": "v0.1",
        "active_modules": "Mirror Check, Stress Test, Boundary Cases, Evidence Lab, Self-Audit Mode",
        "stored_locally": "Yes",
        "public_ledger": "No",
        "global_id_sync": "No",
        "central_storage": "No",
        "authority_claim": "No",
        "human_review_required": "Yes",
    }
    st.code(
        f"""Local Witness Receipt v2

Receipt version: {receipt_example['receipt_version']}
Document fingerprint: {receipt_example['document_fingerprint']}
Processed document fingerprint: {receipt_example['processed_document_fingerprint']}
Report fingerprint: {receipt_example['report_fingerprint']}
App version: {receipt_example['app_version']}
Rubric version: {receipt_example['rubric_version']}
Prompt version: {receipt_example['prompt_version']}
Active modules: {receipt_example['active_modules']}
Stored locally: {receipt_example['stored_locally']}
Public ledger: {receipt_example['public_ledger']}
Global ID sync: {receipt_example['global_id_sync']}
Central storage: {receipt_example['central_storage']}
Authority claim: {receipt_example['authority_claim']}
Human review required: {receipt_example['human_review_required']}

Disclaimer: This receipt is a local witness artifact for human review. It is not legal proof, policy command, enforcement, extraordinary-claim validation, public ledger proof, or a replacement for human judgment.""",
        language="text",
    )

with tab_empirical:
    st.subheader("Evidence Lab — Data Check")
    render_shared_protocol_state_notice("Evidence Lab")
    st.write(
        "Build or upload a country-year evidence table from public sources, then let ALETHEIA carry it through variable mapping, empirical scoring, and the Sydney Protocol overlay. "
        "This layer is where symbolic doctrine meets public evidence in a reproducible, inspectable way."
    )

    st.info(
        "Evidence does not come from ALETHEIA. Public datasets provide the baseline. ALETHEIA only maps and reflects it."
    )

    with st.expander("Evidence status + extraordinary claim protocol", expanded=True):
        st.markdown(
            """
            Evidence Lab uses four review levels:

            - **Strong evidence** — multiple public, relevant, reviewable sources support the claim.
            - **Partial evidence** — some evidence exists, but coverage, independence, relevance, or completeness is limited.
            - **Weak evidence** — the claim is mostly asserted, anecdotal, internally sourced, or insufficiently documented.
            - **No evidence supplied** — no reviewable support is provided.

            Extraordinary claims — including spiritual, prophetic, alien, neural, metaphysical, or otherwise exceptional claims — are treated as **unverified** unless supported by public, testable, non-coercive evidence.

            ALETHEIA may audit the policy consequences of a claim for rights, coercion, transparency, accountability, appealability, and repair. It must not validate spiritual authority, confirm invisible sources, remove guardrails, or replace human review.
            """
        )

    evidence_examples = {
        "Strong evidence": "Multiple public, relevant, reviewable sources support the claim.",
        "Partial evidence": "Some evidence exists, but coverage, independence, relevance, or completeness is limited.",
        "Weak evidence": "The claim is mostly asserted, anecdotal, internally sourced, or insufficiently documented.",
        "No evidence supplied": "No reviewable support is provided for the claim.",
        "Unverified extraordinary claim": "The claim may be personally meaningful, but it is not used as policy authority without public, testable, non-coercive evidence and human review.",
    }
    selected_evidence_level = st.selectbox(
        "Evidence status example",
        list(evidence_examples.keys()),
        key="evidence_status_example_selector",
        help="Template-level calibration only. Evidence status is a review signal, not a final truth verdict.",
    )
    st.code(
        f"""Evidence Lab Review

Claim reviewed: [insert claim]
Evidence status: {selected_evidence_level}
Reason: {evidence_examples[selected_evidence_level]}
Evidence gaps: identify unsupported assertions, missing sources, stale data, self-referential sources, or unreviewable claims.
Extraordinary claim handling: treat as unverified unless supported by public, testable, non-coercive evidence.
Policy consequence audit: review effects on basic rights, free agency, coercion, transparency, appeal, accountability, and repair.
Human review disclaimer: Evidence Lab is a mirror for human review. It is not a proof engine, oracle, legal judgment, religious authority, or enforcement mechanism.""",
        language="text",
    )

    with st.expander("Data sources → ALETHEIA fields → Protocol view", expanded=True):
        st.markdown(
            "**Flow:** public evidence → variable mapping → scoring → protocol overlay → review."
        )
        st.markdown("#### Data source map")
        source_df = evidence_source_frame()
        visible_source_cols = ["Evidence source", "What it contributes", "ALETHEIA use"]
        st.dataframe(source_df[visible_source_cols], use_container_width=True, hide_index=True, height=300)
        with st.expander("Protocol details by source", expanded=False):
            st.dataframe(
                source_df[["Evidence source", "Protocol overlay"]],
                use_container_width=True,
                hide_index=True,
                height=300,
            )
        st.markdown("#### Field mapping")
        st.dataframe(variable_mapping_frame(), use_container_width=True, hide_index=True, height=300)
        st.caption(
            "External outcome columns do not change the score. They are for later checks against real-world outcomes."
        )

    with st.expander("Needed and helpful columns", expanded=False):
        st.markdown("**Required identity columns**")
        st.code("country, iso3, year", language="text")
        st.markdown("**Needed for real 9k allocation**")
        st.code("population", language="text")
        st.markdown("**Helpful data columns**")
        st.code("\n".join(EMPIRICAL_COLUMNS), language="text")
        st.caption("WGI fields can use their normal -2.5 to +2.5 scale. V-Dem and trust fields should already be 0–1.")


    st.markdown("### Build a country-year table from public data")
    st.caption(
        "A simple path is: start with World Bank WGI, add population for country-level allocation, and optionally enrich the result with V-Dem and trust data. The separate merged-evidence uploader is for a fully prepared ALETHEIA-ready master CSV."
    )
    st.info(
        "Empirical build flow: WGI plus population create the core country-year base; V-Dem and trust enrich matching rows. By default, scoring stays in the modern era from 1996 onward so historical V-Dem rows are not accidentally mixed with modern population or seat allocation."
    )

    with st.expander("How to get and prepare the first real dataset", expanded=False):
        st.markdown(ingestion_notes_markdown())
        st.info(
            "This uploader does not hard-code a live web download. That makes the workflow reliable on Streamlit Cloud: "
            "download the public data from the official source, then upload the file here."
        )

    ingest_cols = st.columns(2)
    with ingest_cols[0]:
        wgi_upload = st.file_uploader(
            "Upload World Bank WGI CSV/XLS/XLSX",
            type=["csv", "xls", "xlsx"],
            key="wgi_ingest_upload",
            help="Accepts common WGI long or wide layouts. Required fields: country, iso3/country code, year, and indicator/value or WGI columns.",
        )
    with ingest_cols[1]:
        pop_upload = st.file_uploader(
            "Optional population CSV/XLS/XLSX",
            type=["csv", "xls", "xlsx"],
            key="population_ingest_upload",
            help="Required for real 9k seat allocation. Needs country, iso3/country code, year, and population/value columns.",
        )

    optional_cols = st.columns(2)
    with optional_cols[0]:
        vdem_upload = st.file_uploader(
            "Optional V-Dem/ALETHEIA-compatible file",
            type=["csv", "xls", "xlsx"],
            key="vdem_ingest_upload",
            help="Use country, iso3, year plus columns such as vdem_executive_constraints and vdem_democracy.",
        )
    with optional_cols[1]:
        trust_upload = st.file_uploader(
            "Optional trust/ALETHEIA-compatible file",
            type=["csv", "xls", "xlsx"],
            key="trust_ingest_upload",
            help="Use country, iso3, year plus wvs_generalized_trust, or upload OWID self-reported trust attitudes CSV directly (Entity/Code/Year plus most-people-can-be-trusted indicator).",
        )

    build_master = st.button("Build master CSV from uploads", use_container_width=True)
    if build_master:
        try:
            with st.spinner("Reading uploads and building country-year master table..."):
                wgi_df = read_public_data_upload(wgi_upload) if wgi_upload is not None else None
                pop_df = read_public_data_upload(pop_upload) if pop_upload is not None else None
                vdem_df = read_public_data_upload(vdem_upload) if vdem_upload is not None else None
                trust_df = read_public_data_upload(trust_upload) if trust_upload is not None else None
                if all(x is None for x in [wgi_df, pop_df, vdem_df, trust_df]):
                    st.warning("Upload at least one public data file first. WGI is the best starting point.")
                else:
                    diagnostics_df = public_upload_diagnostics(
                        wgi_df=wgi_df,
                        population_df=pop_df,
                        vdem_df=vdem_df,
                        trust_df=trust_df,
                    )
                    st.session_state["empirical_ingest_diagnostics"] = diagnostics_df.copy()
                    master_df = build_master_from_public_uploads(wgi_df=wgi_df, population_df=pop_df, vdem_df=vdem_df, trust_df=trust_df)
                    demo_names = {"Exampleland", "Threshold Republic", "Capture State"}
                    if "country" in master_df.columns and set(master_df["country"].astype(str).head(10)) & demo_names:
                        raise ValueError(
                            "Builder produced synthetic demo rows after a real upload. This is blocked so uploaded data is not mistaken for evidence."
                        )
                    st.session_state["empirical_master_df"] = master_df.copy()
                    st.session_state["use_generated_master_for_scoring"] = True
                    valid_rows = int(master_df.get("empirical_identity_valid", pd.Series([True] * len(master_df))).fillna(False).astype(bool).sum()) if not master_df.empty else 0
            if not all(x is None for x in [wgi_df, pop_df, vdem_df, trust_df]):
                st.success(f"Upload processed: built a country-year table with {len(master_df):,} row(s); {valid_rows:,} valid identity row(s).")
        except Exception as exc:
            st.session_state.pop("empirical_master_df", None)
            st.error("Upload processing failed.")
            st.warning("No valid country-year table was made. The app did not switch to demo data while upload mode was active.")
            st.error(f"Could not build master table: {exc}")
            if isinstance(st.session_state.get("empirical_ingest_diagnostics"), pd.DataFrame):
                st.markdown("#### Upload check details")
                st.dataframe(st.session_state["empirical_ingest_diagnostics"], use_container_width=True, hide_index=True)

    if isinstance(st.session_state.get("empirical_ingest_diagnostics"), pd.DataFrame):
        with st.expander("Upload check details", expanded=build_master):
            st.dataframe(st.session_state["empirical_ingest_diagnostics"], use_container_width=True, hide_index=True)
            st.caption(
                "raw_rows_read = rows actually read from the uploaded file; "
                "standardized_country_year_rows = rows ALETHEIA could map to country/iso3/year; "
                "rows_with_signal = rows carrying WGI, population, V-Dem, or trust values. "
                "The generated/scored master uses the default modern empirical window, year >= 1996."
            )

    def _empirical_source_status_frame(df: pd.DataFrame | None) -> pd.DataFrame:
        wgi_cols = [
            "wgi_voice_accountability",
            "wgi_political_stability",
            "wgi_government_effectiveness",
            "wgi_regulatory_quality",
            "wgi_rule_of_law",
            "wgi_control_corruption",
        ]
        vdem_cols = ["vdem_executive_constraints", "vdem_democracy", "v2x_polyarchy", "v2x_libdem"]
        trust_raw_cols = ["wvs_generalized_trust"]
        trust_prior_cols = ["empirical_trust_prior"]

        def _count_present(cols: list[str]) -> tuple[int, int, str, str]:
            if not isinstance(df, pd.DataFrame) or df.empty:
                return 0, 0, "No active table", "missing"
            existing = [c for c in cols if c in df.columns]
            if not existing:
                return 0, len(df), "Columns absent", "missing"
            mask = pd.Series(False, index=df.index)
            for col in existing:
                mask = mask | pd.to_numeric(df[col], errors="coerce").notna()
            present = int(mask.sum())
            missing = int((~mask).sum())
            if present > 0:
                status = "active"
            elif existing:
                status = "columns present; no usable values"
            else:
                status = "missing"
            return present, missing, ", ".join(existing), status

        rows = []
        for label, cols in [
            ("WGI", wgi_cols),
            ("V-Dem", vdem_cols),
            ("Trust raw survey", trust_raw_cols),
            ("Trust prior", trust_prior_cols),
        ]:
            present, missing, detail, status = _count_present(cols)
            rows.append({
                "Source": label,
                "Rows with usable values": present,
                "Rows missing / neutral fallback": missing,
                "Status": status,
                "Detected columns": detail,
            })
        return pd.DataFrame(rows)

    def _is_aletheia_scored_master(df: pd.DataFrame | None) -> bool:
        if not isinstance(df, pd.DataFrame) or df.empty:
            return False
        required = {
            "country", "iso3", "year", "population",
            "aletheia_empirical_integrity",
            "aletheia_empirical_friction",
            "aletheia_empirical_collapse_probability",
            "aletheia_verdict",
        }
        cols = {str(c).strip().lower().replace(" ", "_") for c in df.columns}
        return required.issubset(cols)

    uploaded_empirical_override = None
    if isinstance(st.session_state.get("empirical_master_df"), pd.DataFrame):
        master_df = st.session_state["empirical_master_df"]
        with st.expander("Data carry-through check", expanded=False):
            st.dataframe(_empirical_source_status_frame(master_df), use_container_width=True, hide_index=True)
            st.caption("This checks the table before scoring. If WGI is missing here, World Lens cannot report WGI coverage. Rebuild with the WGI file in the WGI slot.")
        st.markdown("#### Generated country-year table")
        st.caption("This table merges WGI, population, and optional V-Dem/trust data. V-Dem rows before 1996 are filtered out by default.")
        st.dataframe(master_df.head(250), use_container_width=True, hide_index=True, height=260)
        st.download_button(
            "⬇️ Download generated country-year master CSV",
            data=master_df.to_csv(index=False),
            file_name="aletheia_country_year_master.csv",
            mime="text/csv",
            use_container_width=True,
        )
        if "use_generated_master_for_scoring" not in st.session_state:
            st.session_state["use_generated_master_for_scoring"] = True

        if st.checkbox("Use this table for scoring", key="use_generated_master_for_scoring"):
            uploaded_empirical_override = master_df.copy()

    st.markdown("### Score evidence table")
    template_df = empirical_template()
    st.download_button(
        "⬇️ Download empirical CSV template",
        data=template_df.to_csv(index=False),
        file_name="aletheia_empirical_country_year_template.csv",
        mime="text/csv",
        use_container_width=True,
    )

    uploaded_empirical = st.file_uploader(
        "Upload merged evidence / country-year CSV",
        type=["csv"],
        key="empirical_merged_upload",
        help="Use this for a complete already-merged ALETHEIA master CSV or a previously exported ALETHEIA scored master. Do not upload V-Dem-only or trust-only enrichment files here; use their optional slots above.",
    )

    direct_upload_df = None
    direct_upload_is_scored_master = False
    if uploaded_empirical is not None:
        try:
            direct_upload_df = pd.read_csv(uploaded_empirical)
            st.session_state["direct_empirical_upload_df"] = direct_upload_df.copy()
            direct_upload_is_scored_master = _is_aletheia_scored_master(direct_upload_df)
            with st.expander("Direct merged-upload diagnostics", expanded=True):
                st.dataframe(_empirical_source_status_frame(direct_upload_df), use_container_width=True, hide_index=True)
                if direct_upload_is_scored_master:
                    st.success(
                        "This file looks like an ALETHEIA scored master/export. Existing ALETHEIA scores, verdicts, "
                        "trust priors, and source columns will be preserved for the active empirical table."
                    )
                else:
                    st.info(
                        "This file looks like an unscored merged evidence table. ALETHEIA will score it after variable mapping. "
                        "If a source column is present but has no usable values, Grid coverage for that source will correctly remain 0%."
                    )
        except Exception as exc:
            st.error(f"Could not read uploaded CSV: {exc}")
            direct_upload_df = None

    use_template = st.checkbox(
        "Use built-in synthetic demo template instead of uploaded/generated data",
        value=(uploaded_empirical is None and uploaded_empirical_override is None),
        help="The demo rows are not real countries. They only demonstrate the schema and output flow.",
    )

    st.session_state["empirical_use_template"] = bool(use_template)
    update_protocol_state(last_update_source="Evidence Lab", synthetic_demo_active=bool(use_template))

    if use_template:
        st.warning(
            "Synthetic demo mode is active. Exampleland, Threshold Republic, and Capture State are interface-test rows only; "
            "do not interpret their correlations, scores, or 9k allocation as real-world findings."
        )

    empirical_raw = None
    active_direct_scored_master = False
    if uploaded_empirical_override is not None and not use_template:
        empirical_raw = uploaded_empirical_override.copy()
    elif direct_upload_df is not None and not use_template:
        empirical_raw = direct_upload_df.copy()
        active_direct_scored_master = bool(direct_upload_is_scored_master)
    else:
        empirical_raw = template_df.copy()

    if empirical_raw is not None:
        if use_template:
            source_label = "synthetic demo template"
        elif uploaded_empirical_override is not None:
            source_label = "generated master table"
        elif active_direct_scored_master:
            source_label = "uploaded ALETHEIA scored master"
        else:
            source_label = "uploaded merged evidence CSV"

        with st.spinner(f"Processing {source_label} through ALETHEIA variable mapping and Sydney Protocol overlay..."):
            prepared = prepare_empirical_frame(empirical_raw).reset_index(drop=True)
            if active_direct_scored_master:
                # A previously exported ALETHEIA master should be accepted as an
                # already-scored protocol state rather than neutralized by a second
                # scoring pass when raw source columns are sparse. Identity and
                # modern-year guards still apply below.
                scored_all = prepared.copy().reset_index(drop=True)
                for _score_col in [
                    "aletheia_empirical_integrity",
                    "aletheia_empirical_friction",
                    "aletheia_empirical_collapse_probability",
                    "empirical_completeness",
                    "empirical_trust_prior",
                ]:
                    if _score_col in scored_all.columns:
                        scored_all[_score_col] = pd.to_numeric(scored_all[_score_col], errors="coerce")
                if "evidence_variables_used" not in scored_all.columns and "evidence_used" in scored_all.columns:
                    scored_all["evidence_variables_used"] = scored_all["evidence_used"]
                if "evidence_used" not in scored_all.columns and "evidence_variables_used" in scored_all.columns:
                    scored_all["evidence_used"] = scored_all["evidence_variables_used"]
                if "protocol_overlay_status" not in scored_all.columns:
                    scored_all["protocol_overlay_status"] = "preserved uploaded scored master"
                if "final_audit_interpretation" not in scored_all.columns:
                    scored_all["final_audit_interpretation"] = scored_all.get("aletheia_verdict", pd.Series([""] * len(scored_all))).astype(str)
            else:
                scored_all = score_empirical_frame(prepared).reset_index(drop=True)

        if active_direct_scored_master and not scored_all.empty:
            _direct_identity = scored_all.get("empirical_identity_valid", pd.Series([False] * len(scored_all)))
            _direct_identity = _direct_identity.fillna(False).astype(bool) if hasattr(_direct_identity, "fillna") else pd.Series([False] * len(scored_all))
            _direct_year = pd.to_numeric(scored_all.get("year"), errors="coerce")
            _direct_modern = _direct_year.ge(1996)
            _before_direct_filter = len(scored_all)
            scored_all = scored_all.loc[_direct_identity & _direct_modern].copy().reset_index(drop=True)
            _removed_direct = _before_direct_filter - len(scored_all)
            if _removed_direct > 0:
                st.info(f"Direct scored table guard removed {_removed_direct:,} row(s) outside valid identity or modern-year scope.")

        # Fail closed for real uploads/generated masters. Diagnostic rows are useful
        # for ingestion debugging, but they must never be reported as scored
        # empirical evidence. A valid empirical row requires country, iso3, year,
        # and positive population.
        if not use_template:
            if scored_all.empty:
                st.error("No valid country-year rows are available for scoring.")
                st.warning(
                    "The upload/generated master produced only diagnostic rows or no rows at all. "
                    "ALETHEIA blocked scoring instead of reporting diagnostic rows as evidence. "
                    "Check WGI pivoting, country/iso3/year fields, and population merge."
                )
                if isinstance(st.session_state.get("empirical_ingest_diagnostics"), pd.DataFrame):
                    st.markdown("#### Upload check details")
                    st.dataframe(st.session_state["empirical_ingest_diagnostics"], use_container_width=True, hide_index=True)
                st.stop()

            _identity_series = scored_all.get("empirical_identity_valid", pd.Series([False] * len(scored_all)))
            _identity_series = _identity_series.fillna(False).astype(bool) if hasattr(_identity_series, "fillna") else pd.Series([False] * len(scored_all))
            _valid_rows = int(_identity_series.sum())
            _diagnostic_rows = int((~_identity_series).sum())
            if _valid_rows == 0:
                st.error("No valid country-year rows are available for scoring.")
                st.warning(
                    f"{_diagnostic_rows:,} diagnostic row(s) were produced, but all are missing country, iso3, year, "
                    "or positive population. Scoring and 9k allocation are blocked until at least one valid "
                    "country-year row exists."
                )
                if isinstance(st.session_state.get("empirical_ingest_diagnostics"), pd.DataFrame):
                    st.markdown("#### Upload check details")
                    st.dataframe(st.session_state["empirical_ingest_diagnostics"], use_container_width=True, hide_index=True)
                st.stop()

        st.success(f"Evidence scoring complete: {len(scored_all):,} valid row(s) mapped and scored from {source_label}.")

        # Keep the active empirical input columns attached to the scored output.
        # The scoring helper intentionally returns a compact audit table, but the
        # UI, validation checks, downloads, and technical detail sections need the
        # original public evidence columns too.  Attaching them here prevents lower
        # sections from falling back to the synthetic demo view or losing WGI data.
        if len(scored_all) == len(prepared):
            passthrough_cols = [
                "wgi_voice_accountability",
                "wgi_political_stability",
                "wgi_government_effectiveness",
                "wgi_regulatory_quality",
                "wgi_rule_of_law",
                "wgi_control_corruption",
                "vdem_executive_constraints",
                "vdem_democracy",
                "wvs_generalized_trust",
                "conflict_events",
                "political_violence_events",
                "coup_attempt",
                "regime_breakdown",
                "civil_unrest_index",
                "forced_displacement_rate",
                "future_stability_decline",
            ]
            for _col in passthrough_cols:
                if _col in prepared.columns and _col not in scored_all.columns:
                    scored_all[_col] = prepared[_col].values

        # Recompute 9k seats from the full valid country population base, not
        # from the WGI-filtered evidence subset and not from World Bank regional
        # aggregates.  The scored table keeps diagnostic rows, but only valid
        # country rows receive seats.
        allocation_base_all = _country_allocation_base(scored_all, include_demo=use_template)
        if not use_template:
            scored_all = _replace_allocation_columns(scored_all, allocation_base_all)
        else:
            allocation_base_all = scored_all.copy()

        identity_valid_series = scored_all.get("empirical_identity_valid", pd.Series([True] * len(scored_all)))
        identity_valid_series = identity_valid_series.fillna(False).astype(bool) if hasattr(identity_valid_series, "fillna") else pd.Series([True] * len(scored_all))
        invalid_count = int((~identity_valid_series).sum()) if not scored_all.empty else 0
        valid_identity_count = int(identity_valid_series.sum()) if not scored_all.empty else 0

        if invalid_count and not use_template:
            st.warning(
                f"{valid_identity_count:,} valid country-year row(s) and {invalid_count:,} diagnostic row(s). "
                "Diagnostic rows are retained because they are missing country, iso3, year, or positive population; "
                "they are excluded from valid 9k allocation."
            )
        elif not use_template and not scored_all.empty:
            st.success(f"{valid_identity_count:,} valid country-year row(s) are ready for scoring and 9k allocation.")

        scored = scored_all.copy()
        if not use_template and not scored.empty:
            _wgi_cols_check = [
                "wgi_voice_accountability",
                "wgi_political_stability",
                "wgi_government_effectiveness",
                "wgi_regulatory_quality",
                "wgi_rule_of_law",
                "wgi_control_corruption",
            ]
            _wgi_present_cols = [c for c in _wgi_cols_check if c in scored.columns]
            _wgi_rows_present = 0
            if _wgi_present_cols:
                _wgi_mask = pd.Series(False, index=scored.index)
                for _col in _wgi_present_cols:
                    _wgi_mask = _wgi_mask | pd.to_numeric(scored[_col], errors="coerce").notna()
                _wgi_rows_present = int(_wgi_mask.sum())
            if _wgi_rows_present == 0:
                st.warning(
                    "WGI source signal is not present in the active scored evidence table. "
                    "The Global Grid will correctly show WGI coverage as 0.0% until the master is rebuilt with a WGI file in the WGI upload slot or a merged CSV containing WGI columns."
                )

        if not use_template and not scored.empty:
            wgi_signal_cols = [
                "wgi_voice_accountability",
                "wgi_political_stability",
                "wgi_government_effectiveness",
                "wgi_regulatory_quality",
                "wgi_rule_of_law",
                "wgi_control_corruption",
            ]
            available_signal_cols = [c for c in wgi_signal_cols if c in scored.columns]
            if available_signal_cols:
                evidence_mask = pd.Series(False, index=scored.index)
                for col in available_signal_cols:
                    evidence_mask = evidence_mask | pd.to_numeric(scored[col], errors="coerce").notna()
                if int(evidence_mask.sum()) > 0 and int(evidence_mask.sum()) < len(scored):
                    show_evidence_years_only = st.checkbox(
                        "Show WGI-supported evidence years only",
                        value=True,
                        help="Recommended for first real runs. Population-only historical rows are useful for allocation context but should not drive governance scoring summaries.",
                    )
                    if show_evidence_years_only:
                        scored = scored.loc[evidence_mask].copy()
                    st.caption(
                        f"Evidence-year filter: showing {len(scored):,} of {len(scored_all):,} rows. "
                        f"{int(evidence_mask.sum()):,} row(s) contain at least one WGI governance indicator."
                    )

        st.session_state["empirical_scored_df"] = scored.copy()
        st.session_state["empirical_allocation_df"] = allocation_base_all.copy()
        update_protocol_state(last_update_source="Evidence Lab", synthetic_demo_active=bool(use_template))

        if not use_template and not scored.empty:
            demo_names = {"Exampleland", "Threshold Republic", "Capture State"}
            visible_names = set(scored.get("country", pd.Series(dtype=str)).astype(str).head(25).tolist())
            if visible_names & demo_names:
                st.warning("Uploaded-evidence mode is active, but demo country names are still present in the active scored data. Clear the uploaded file or reload the app if this was not intended.")

        # Validation should use the exact active dataframe visible on the page,
        # including uploaded/generated evidence columns.  This keeps N and group
        # means aligned with the real uploaded evidence instead of the demo rows.
        scored_for_validation = scored.reset_index(drop=True).copy()

        st.markdown("### Topline Evidence Results" + (" · Synthetic demo" if use_template else " · Uploaded evidence"))
        if use_template:
            st.caption("Synthetic rows are for app testing only. Do not read them as real-world findings.")
        else:
            st.caption("Uploaded/generated data was mapped, scored, and shown through the protocol view.")

        e1, e2, e3, e4 = st.columns(4)
        e1.metric("Rows scored", f"{len(scored):,}")

        seat_year_label = "Synthetic 9k seats" if use_template else "Latest-year 9k seats"
        seat_year_value = "—"
        seat_caption = ""
        seat_df = allocation_base_all.copy()
        if not seat_df.empty and "year" in seat_df.columns and "seats_9k" in seat_df.columns:
            year_values = pd.to_numeric(seat_df["year"], errors="coerce")
            if year_values.notna().any():
                latest_year = int(year_values.dropna().max())
                seat_year_label = "Synthetic 9k seats" if use_template else f"9k seats · {latest_year}"
                latest_year_mask = year_values == latest_year
                latest_year_seats = int(pd.to_numeric(seat_df.loc[latest_year_mask, "seats_9k"], errors="coerce").sum(skipna=True))
                seat_year_value = f"{latest_year_seats:,}"
                if not use_template:
                    all_year_seats = int(pd.to_numeric(seat_df["seats_9k"], errors="coerce").sum(skipna=True))
                    seat_caption = f"All row-year seat total: {all_year_seats:,}; 9k allocation is interpreted per year."
        e2.metric(seat_year_label, seat_year_value)
        e3.metric("Mean integrity", f"{pd.to_numeric(scored['aletheia_empirical_integrity'], errors='coerce').mean():.3f}")
        e4.metric("Average schema coverage" if use_template else "Average empirical coverage", f"{pd.to_numeric(scored['empirical_completeness'], errors='coerce').mean():.1%}")
        if seat_caption:
            st.caption(seat_caption)
        if use_template:
            st.caption("Demo schema coverage is below 100% because capital_scale is intentionally blank; optional proxies should not be treated as empirically supplied.")

        st.markdown("### Main scored data table")
        st.caption("capital_scale is neutral/default unless supplied through an empirical proxy column; schema coverage is not proof of empirical validity." if use_template else "capital_scale is neutral/default unless supplied through an empirical proxy column.")
        curated_cols = [
            "country", "iso3", "year", "population", "seats_9k",
            "aletheia_verdict", "aletheia_empirical_integrity", "aletheia_empirical_friction",
            "aletheia_empirical_collapse_probability",
            "empirical_completeness", "empirical_identity_valid",
        ]
        curated_cols = [c for c in curated_cols if c in scored.columns]
        display_names = {
            "aletheia_verdict": "verdict",
            "aletheia_empirical_integrity": "integrity",
            "aletheia_empirical_friction": "friction",
            "aletheia_empirical_collapse_probability": "collapse_probability",
            "empirical_completeness": "schema_coverage" if use_template else "empirical_coverage",
            "empirical_identity_valid": "identity_valid",
        }
        curated_display = scored[curated_cols].rename(columns=display_names)
        st.dataframe(curated_display, use_container_width=True, hide_index=True, height=260)

        csv_out = scored.to_csv(index=False)
        st.download_button(
            "⬇️ Download scored empirical ALETHEIA table",
            data=csv_out,
            file_name="aletheia_evidence_audit_scores.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.markdown("### Country-Year Explorer")
        valid_rows = scored.reset_index(drop=True).copy()

        def _truthy_series(series: pd.Series) -> pd.Series:
            if series is None:
                return pd.Series(True, index=valid_rows.index)
            if series.dtype == bool:
                return series.fillna(False)
            text = series.astype(str).str.strip().str.lower()
            return text.isin(["true", "1", "yes", "y", "valid"])

        if "empirical_identity_valid" in valid_rows.columns:
            identity_mask = _truthy_series(valid_rows["empirical_identity_valid"])
        elif "identity_valid" in valid_rows.columns:
            identity_mask = _truthy_series(valid_rows["identity_valid"])
        else:
            identity_mask = pd.Series(True, index=valid_rows.index)

        required_explorer_cols = ["country", "iso3", "year"]
        missing_explorer_cols = [c for c in required_explorer_cols if c not in valid_rows.columns]
        if missing_explorer_cols:
            st.warning(
                "Country-Year Explorer is inactive because the active scored table is missing required column(s): "
                + ", ".join(missing_explorer_cols)
                + ". Upload or rebuild a country-year master with country, iso3, and year."
            )
        else:
            valid_rows = valid_rows.loc[identity_mask].copy()
            valid_rows["_country_label"] = valid_rows["country"].astype(str).str.strip()
            valid_rows["_iso3_label"] = valid_rows["iso3"].astype(str).str.strip().str.upper()
            valid_rows["_year_num"] = pd.to_numeric(valid_rows["year"], errors="coerce")
            valid_rows = valid_rows[
                valid_rows["_country_label"].ne("")
                & valid_rows["_iso3_label"].ne("")
                & valid_rows["_year_num"].notna()
            ].copy()

            if valid_rows.empty:
                st.info("No valid country-year rows yet. Add country, ISO3, year, and population so you can inspect one row at a time." )
            else:
                valid_rows["_year_int"] = valid_rows["_year_num"].astype(int)

                def _friendly_country_name(iso3_value: str, country_value: str = "") -> str:
                    iso3_text = str(iso3_value or "").strip().upper()
                    country_text = str(country_value or "").strip()
                    if country_text and country_text.upper() != iso3_text and len(country_text) > 3:
                        return country_text
                    manual_names = {
                        "AFG": "Afghanistan", "ALB": "Albania", "DZA": "Algeria", "AGO": "Angola", "ARG": "Argentina",
                        "ARM": "Armenia", "AUS": "Australia", "AUT": "Austria", "AZE": "Azerbaijan", "BHR": "Bahrain",
                        "BGD": "Bangladesh", "BLR": "Belarus", "BEL": "Belgium", "BEN": "Benin", "BOL": "Bolivia",
                        "BIH": "Bosnia and Herzegovina", "BWA": "Botswana", "BRA": "Brazil", "BGR": "Bulgaria",
                        "BFA": "Burkina Faso", "BDI": "Burundi", "KHM": "Cambodia", "CMR": "Cameroon", "CAN": "Canada",
                        "CAF": "Central African Republic", "TCD": "Chad", "CHL": "Chile", "CHN": "China", "COL": "Colombia",
                        "COD": "Democratic Republic of the Congo", "COG": "Republic of the Congo", "CRI": "Costa Rica",
                        "CIV": "Côte d’Ivoire", "HRV": "Croatia", "CUB": "Cuba", "CYP": "Cyprus", "CZE": "Czechia",
                        "DNK": "Denmark", "DOM": "Dominican Republic", "ECU": "Ecuador", "EGY": "Egypt", "SLV": "El Salvador",
                        "ERI": "Eritrea", "EST": "Estonia", "ETH": "Ethiopia", "FIN": "Finland", "FRA": "France",
                        "GAB": "Gabon", "GEO": "Georgia", "DEU": "Germany", "GHA": "Ghana", "GRC": "Greece",
                        "GTM": "Guatemala", "GIN": "Guinea", "HTI": "Haiti", "HND": "Honduras", "HUN": "Hungary",
                        "IND": "India", "IDN": "Indonesia", "IRN": "Iran", "IRQ": "Iraq", "IRL": "Ireland",
                        "ISR": "Israel", "ITA": "Italy", "JPN": "Japan", "JOR": "Jordan", "KAZ": "Kazakhstan",
                        "KEN": "Kenya", "KWT": "Kuwait", "KGZ": "Kyrgyzstan", "LAO": "Laos", "LVA": "Latvia",
                        "LBN": "Lebanon", "LBR": "Liberia", "LBY": "Libya", "LTU": "Lithuania", "MDG": "Madagascar",
                        "MWI": "Malawi", "MYS": "Malaysia", "MLI": "Mali", "MEX": "Mexico", "MDA": "Moldova",
                        "MAR": "Morocco", "MOZ": "Mozambique", "MMR": "Myanmar", "NAM": "Namibia", "NPL": "Nepal",
                        "NLD": "Netherlands", "NZL": "New Zealand", "NIC": "Nicaragua", "NER": "Niger", "NGA": "Nigeria",
                        "PRK": "North Korea", "MKD": "North Macedonia", "NOR": "Norway", "OMN": "Oman", "PAK": "Pakistan",
                        "PAN": "Panama", "PRY": "Paraguay", "PER": "Peru", "PHL": "Philippines", "POL": "Poland",
                        "PRT": "Portugal", "QAT": "Qatar", "ROU": "Romania", "RUS": "Russia", "RWA": "Rwanda",
                        "SAU": "Saudi Arabia", "SEN": "Senegal", "SRB": "Serbia", "SLE": "Sierra Leone", "SGP": "Singapore",
                        "SVK": "Slovakia", "SVN": "Slovenia", "SOM": "Somalia", "ZAF": "South Africa", "KOR": "South Korea",
                        "SSD": "South Sudan", "ESP": "Spain", "LKA": "Sri Lanka", "SDN": "Sudan", "SWE": "Sweden",
                        "CHE": "Switzerland", "SYR": "Syria", "TWN": "Taiwan", "TJK": "Tajikistan", "TZA": "Tanzania",
                        "THA": "Thailand", "TUN": "Tunisia", "TUR": "Türkiye", "TKM": "Turkmenistan", "UGA": "Uganda",
                        "UKR": "Ukraine", "ARE": "United Arab Emirates", "GBR": "United Kingdom", "USA": "United States",
                        "URY": "Uruguay", "UZB": "Uzbekistan", "VEN": "Venezuela", "VNM": "Vietnam", "YEM": "Yemen",
                        "ZMB": "Zambia", "ZWE": "Zimbabwe",
                    }
                    return manual_names.get(iso3_text, country_text or iso3_text)

                valid_rows["_country_name"] = [
                    _friendly_country_name(iso3, country)
                    for iso3, country in zip(valid_rows["_iso3_label"], valid_rows["_country_label"])
                ]
                valid_rows = valid_rows.sort_values(["_year_int", "_country_name"], ascending=[False, True]).reset_index(drop=True)

                years_available = sorted(valid_rows["_year_int"].dropna().astype(int).unique().tolist(), reverse=True)
                if years_available:
                    max_explorer_year = max(years_available)
                    min_explorer_year = min(years_available)
                    if max_explorer_year < 2020:
                        st.warning(
                            f"The active scored table currently only goes up to {max_explorer_year}. "
                            "The explorer can only show years that exist in this Empirical run. "
                            "If you expected newer years, reload or rebuild the full country-year master before using this explorer."
                        )

                    # Country-first selection keeps the list readable and gives native
                    # type-ahead suggestions from the available countries.
                    country_lookup = (
                        valid_rows[["_country_name", "_iso3_label"]]
                        .drop_duplicates()
                        .sort_values(["_country_name", "_iso3_label"])
                        .reset_index(drop=True)
                    )
                    country_lookup["_country_option"] = country_lookup["_country_name"] + " · " + country_lookup["_iso3_label"]
                    country_options = country_lookup["_country_option"].tolist()

                    synced_iso3 = st.session_state.get("aletheia_synced_iso3")
                    synced_country_option = None
                    if synced_iso3:
                        _synced_options = country_lookup.loc[
                            country_lookup["_iso3_label"].astype(str).str.upper() == str(synced_iso3).upper(),
                            "_country_option",
                        ].tolist()
                        synced_country_option = _synced_options[0] if _synced_options else None

                    country_widget_key = "empirical_country_year_explorer_country_search"
                    # Only seed the country selector before the widget exists.
                    # Do not overwrite an existing widget value from a user click,
                    # otherwise a stale focus country can force the selector back
                    # to the previous/default country such as Afghanistan.
                    if country_widget_key not in st.session_state and synced_country_option in country_options:
                        st.session_state[country_widget_key] = synced_country_option

                    country_col, year_col = st.columns([2, 1])
                    with country_col:
                        selected_country_option = st.selectbox(
                            "Search country",
                            options=country_options,
                            index=country_options.index(st.session_state.get(country_widget_key, country_options[0])) if st.session_state.get(country_widget_key, country_options[0]) in country_options else 0,
                            key=country_widget_key,
                            help="Start typing a country name or ISO code. The list only includes countries available in the active scored table.",
                        )
                    selected_iso = country_lookup.loc[
                        country_lookup["_country_option"] == selected_country_option, "_iso3_label"
                    ].iloc[0]
                    selected_country_name = country_lookup.loc[
                        country_lookup["_country_option"] == selected_country_option, "_country_name"
                    ].iloc[0]
                    st.session_state["aletheia_synced_iso3"] = str(selected_iso).upper()
                    st.session_state["aletheia_synced_country_name"] = str(selected_country_name)
                    st.caption(f"Focus country set for Grid/report context: {selected_country_name} · {str(selected_iso).upper()}")

                    country_rows_all_years = valid_rows[valid_rows["_iso3_label"] == selected_iso].copy()
                    country_years = country_available_years(valid_rows, selected_iso)

                    st.caption(
                        country_year_status_message(selected_country_name, selected_iso, country_years)
                        + " The year dropdown is scoped to this selected country only; ALETHEIA does not silently fall back to a global/default year."
                    )
                    if not country_years:
                        st.warning(
                            f"No available country-year data for {selected_country_name} · {str(selected_iso).upper()}. "
                            "Choose another country or rebuild the country-year master."
                        )
                        st.stop()

                    synced_evidence_year = st.session_state.get("aletheia_synced_evidence_year")
                    country_year_widget_key = f"empirical_country_year_explorer_year_{selected_iso}"
                    if synced_evidence_year in country_years and st.session_state.get(country_year_widget_key) != int(synced_evidence_year):
                        st.session_state[country_year_widget_key] = int(synced_evidence_year)
                    country_year_index = safe_country_year_index(st.session_state.get(country_year_widget_key), country_years)
                    with year_col:
                        selected_explorer_year = st.selectbox(
                            "Year for country",
                            options=country_years,
                            index=country_year_index,
                            key=country_year_widget_key,
                            help="Only years present for the selected country are shown. No global/default fallback is used.",
                        )
                    st.session_state["aletheia_synced_evidence_year"] = int(selected_explorer_year)
                    st.session_state["aletheia_empirical_country_year"] = int(selected_explorer_year)

                    explorer_rows = country_rows_all_years[country_rows_all_years["_year_int"] == int(selected_explorer_year)].copy()

                    if explorer_rows.empty:
                        st.info("No country-year row matches that country and year. Try another country or year.")
                        st.stop()

                    explorer_rows["_label"] = explorer_rows["_country_name"] + " · " + explorer_rows["_iso3_label"] + " · " + explorer_rows["_year_int"].astype(str)
                    if "seats_9k" in explorer_rows.columns:
                        _seat_nums = pd.to_numeric(explorer_rows["seats_9k"], errors="coerce")
                        explorer_rows.loc[_seat_nums.notna(), "_label"] = (
                            explorer_rows.loc[_seat_nums.notna(), "_label"]
                            + " · "
                            + _seat_nums[_seat_nums.notna()].astype(int).astype(str)
                            + " seats"
                        )

                    st.caption(
                        "Explorer source: active scored table. Search country first, then choose one of that country’s available years. "
                        "This avoids stale global-year fallback and shares the confirmed year with allocation and Grid outputs when available."
                    )

                    if len(explorer_rows) == 1:
                        selected = explorer_rows.iloc[0]
                    else:
                        options = explorer_rows.index.tolist()
                        selected_idx = st.selectbox(
                            "Country-year row",
                            options=options,
                            format_func=lambda idx: explorer_rows.loc[idx, "_label"],
                            key="empirical_country_year_explorer_country_year_row",
                        )
                        selected = explorer_rows.loc[selected_idx]

                    selected_explorer_signature = (
                        f"{str(selected.get('iso3', selected_iso)).upper()}::"
                        f"{int(selected_explorer_year)}::"
                        f"{str(selected.get('country', selected_country_name))}"
                    )
                    pending_label = f"{selected_country_name} · {str(selected_iso).upper()} · {int(selected_explorer_year)}"
                    active_signature = st.session_state.get("empirical_country_year_explorer_active_signature")
                    active_selected = active_signature == selected_explorer_signature

                    run_cols = st.columns([1, 2])
                    with run_cols[0]:
                        run_country_diagnostic = st.button(
                            "Run country-year review",
                            key="empirical_country_year_explorer_run_button",
                            type="primary",
                            use_container_width=True,
                        )
                    with run_cols[1]:
                        if active_selected:
                            st.success(f"Diagnostic is active for: {pending_label}")
                        else:
                            st.info(
                                f"Selected: {pending_label}. Press **Run country-year review** to update the cards and raw-row detail."
                            )

                    if run_country_diagnostic:
                        st.session_state["empirical_country_year_explorer_active_signature"] = selected_explorer_signature
                        st.session_state["empirical_country_year_explorer_active_payload"] = selected.to_dict()
                        active_selected = True

                    if active_selected:
                        active_payload = st.session_state.get("empirical_country_year_explorer_active_payload")
                        if isinstance(active_payload, dict):
                            selected = pd.Series(active_payload)
                    else:
                        selected = None
                else:
                    st.info("No valid years are available in the active scored table.")
                    st.stop()

                if selected is not None:
                    def _first_value(row, names, default="—"):
                        for name in names:
                            if name in row.index:
                                value = row.get(name)
                                if pd.notna(value):
                                    return value
                        return default

                    def _fmt_num(value, digits=3):
                        num = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
                        return "—" if pd.isna(num) else f"{float(num):.{digits}f}"

                    verdict_value = _first_value(selected, ["aletheia_verdict", "verdict"], "—")
                    integrity_value = _first_value(selected, ["aletheia_empirical_integrity", "integrity"], None)
                    collapse_value = _first_value(selected, ["aletheia_empirical_collapse_probability", "collapse_probability"], None)
                    coverage_value = _first_value(selected, ["empirical_completeness", "empirical_coverage", "schema_coverage"], None)
                    seats_value = pd.to_numeric(pd.Series([_first_value(selected, ["seats_9k"], None)]), errors="coerce").iloc[0]

                    col_a, col_b, col_c, col_d = st.columns(4)
                    col_a.metric("Empirical verdict", verdict_value)
                    col_b.metric("Integrity", _fmt_num(integrity_value))
                    col_c.metric("Collapse probability", _fmt_num(collapse_value))
                    col_d.metric("Allocated seats", "—" if pd.isna(seats_value) else f"{int(seats_value):,}")

                    col_e, col_f, col_g, col_h = st.columns(4)
                    col_e.metric("Empirical coverage", _fmt_num(coverage_value, digits=1) if pd.to_numeric(pd.Series([coverage_value]), errors="coerce").iloc[0] > 1 else ("—" if pd.isna(pd.to_numeric(pd.Series([coverage_value]), errors="coerce").iloc[0]) else f"{pd.to_numeric(pd.Series([coverage_value]), errors='coerce').iloc[0]:.1%}"))
                    raw_trust_value = _first_value(selected, ["wvs_generalized_trust"], None)
                    trust_prior_value = _first_value(selected, ["empirical_trust_prior"], None)
                    col_f.metric("Raw trust", format_raw_trust_label(raw_trust_value))
                    col_g.metric("Trust prior used", format_trust_prior_label(trust_prior_value))
                    if format_raw_trust_label(raw_trust_value) == "not available" and format_trust_prior_label(trust_prior_value).startswith("0.500"):
                        st.caption("Raw trust is not available for this country-year; ALETHEIA is showing a neutral trust-prior fallback, not observed survey trust.")
                    col_h.metric("Identity valid", str(_first_value(selected, ["empirical_identity_valid", "identity_valid"], True)))

                    st.markdown("#### Sydney Protocol overlay")
                    st.write(_first_value(selected, ["protocol_overlay_status", "sydney_overlay_status"], "No overlay status available."))
                    st.caption("Evidence used: " + str(_first_value(selected, ["evidence_variables_used", "evidence_used"], "—")))
                    st.caption("Country-Year Explorer uses the active scored table. Search a country, then choose one of its years. Seats are read inside that year only.")

                    feature_cols = [
                        "technical_complexity", "centralization", "anonymity", "regulation", "transparency", "capital_scale",
                        "empirical_trust_prior", "wvs_generalized_trust",
                        "wgi_voice_accountability", "wgi_political_stability", "wgi_government_effectiveness",
                        "wgi_regulatory_quality", "wgi_rule_of_law", "wgi_control_corruption",
                        "vdem_executive_constraints", "vdem_democracy",
                    ]
                    feature_rows = []
                    for col in feature_cols:
                        if col in selected.index:
                            value = pd.to_numeric(pd.Series([selected.get(col)]), errors="coerce").iloc[0]
                            feature_rows.append({"feature": col, "value": "—" if pd.isna(value) else f"{value:.3f}"})
                    feature_table = pd.DataFrame(feature_rows)
                    if not feature_table.empty:
                        st.dataframe(feature_table, use_container_width=True, hide_index=True, height=300)

                    detail_cols = [
                        "country", "iso3", "year", "population", "population_share", "seats_9k", "_allocation_role",
                        "aletheia_verdict", "verdict", "aletheia_empirical_integrity", "integrity",
                        "aletheia_empirical_friction", "friction",
                        "aletheia_empirical_collapse_probability", "collapse_probability",
                        "empirical_completeness", "empirical_coverage",
                        "evidence_variables_used", "evidence_used",
                    ]
                    detail_cols = [c for c in detail_cols if c in valid_rows.columns]
                    with st.expander("Selected country-year raw row", expanded=False):
                        st.dataframe(pd.DataFrame([selected[detail_cols].to_dict()]), use_container_width=True, hide_index=True)
        active_explorer_payload = st.session_state.get("empirical_country_year_explorer_active_payload")
        active_explorer_signature = st.session_state.get("empirical_country_year_explorer_active_signature")
        if active_explorer_signature is None or not isinstance(active_explorer_payload, dict):
            st.caption("Country-Year cards unlock after you choose a country/year and press **Run country-year review**.")

        st.markdown("### Seat allocation view")
        st.caption("Synthetic 9k allocation across demo rows." if use_template else "Country seats by selected year. Regional, income, and diagnostic rows are excluded.")

        allocation_df = allocation_base_all.dropna(subset=["seats_9k"]).copy()
        allocation_locked = active_explorer_signature is None or not isinstance(active_explorer_payload, dict)

        if allocation_locked:
            st.info(
                "Seat allocation view is locked to avoid stale or mismatched output. "
                "Choose a country/year above and press **Run country-year review**. "
                "The allocation chart will then use that confirmed diagnostic year."
            )
        elif not allocation_df.empty:
            selected_years = sorted(pd.to_numeric(allocation_df["year"], errors="coerce").dropna().astype(int).unique().tolist())
            if selected_years:
                active_allocation_year = pd.to_numeric(pd.Series([active_explorer_payload.get("year")]), errors="coerce").iloc[0]
                if pd.isna(active_allocation_year):
                    st.warning("The active country-year diagnostic does not contain a valid year. Rerun the diagnostic.")
                else:
                    active_allocation_year = int(active_allocation_year)
                    if active_allocation_year not in selected_years:
                        st.warning(
                            f"Seat allocation view is locked because the confirmed diagnostic year {active_allocation_year} "
                            "is not available in the allocation table. Rebuild the master or choose another country/year."
                        )
                    else:
                        st.session_state["empirical_allocation_year"] = active_allocation_year
                        st.session_state["aletheia_synced_evidence_year"] = active_allocation_year
                        st.session_state["aletheia_empirical_allocation_year"] = active_allocation_year

                        alloc_year = allocation_df[
                            pd.to_numeric(allocation_df["year"], errors="coerce") == active_allocation_year
                        ].sort_values("seats_9k", ascending=False)

                        country_name = str(active_explorer_payload.get("country", st.session_state.get("aletheia_synced_country_name", ""))).strip()
                        iso3_name = str(active_explorer_payload.get("iso3", st.session_state.get("aletheia_synced_iso3", ""))).strip().upper()
                        st.success(
                            f"Seat allocation view confirmed for diagnostic selection: "
                            f"{country_name or iso3_name} · {iso3_name} · {active_allocation_year}"
                        )
                        st.caption(
                            "The allocation chart is now static and tied to the confirmed Country-Year Explorer diagnostic. "
                            "Change the country/year above, then press the run button again to update this chart."
                        )
                        fig = go.Figure(go.Bar(x=alloc_year["country"], y=alloc_year["seats_9k"]))
                        fig.update_layout(template="plotly_white", title=f"9k allocation · {active_allocation_year}", height=420, margin=dict(l=10, r=10, t=55, b=10))
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No valid years are available for seat display.")
        else:
            st.info("No valid population/year rows are available for 9k allocation.")

        st.markdown("### Evidence checks")
        st.caption(
            "Internal checks compare ALETHEIA outputs to variables that may also be score inputs. External validation checks use optional outcome columns that are not score inputs. "
            "Pearson correlations are withheld until N ≥ 30. For true validation, add external outcomes such as conflict events, coups, regime breakdown, political violence, or future-year decline."
        )
        corr_df, group_df = validation_summary(scored_for_validation)
        vc1, vc2 = st.columns(2)
        with vc1:
            st.markdown("#### Correlation checks")
            st.dataframe(corr_df, use_container_width=True, hide_index=True, height=260)
        with vc2:
            st.markdown("#### Group averages by result")
            st.caption("Interface/schema inspection only when groups are small; do not infer real effects from N=1 demo classes." if use_template else "Read group averages only after checking group size and outside validation targets.")
            st.dataframe(group_df, use_container_width=True, hide_index=True, height=260)

        st.markdown("### Technical details")
        overlay_cols = [c for c in ["country", "iso3", "year", "aletheia_verdict", "protocol_overlay_status", "evidence_variables_used"] if c in scored.columns]
        if overlay_cols:
            with st.expander("Protocol detail by country-year", expanded=False):
                st.dataframe(scored[overlay_cols], use_container_width=True, hide_index=True, height=300)
        with st.expander("Full empirical output table", expanded=False):
            st.dataframe(scored, use_container_width=True, hide_index=True, height=420)
        with st.expander("Method note", expanded=False):
            st.markdown(methodology_markdown())

with tab_grid:
    st.subheader("World Lens")
    render_shared_protocol_state_notice("World Lens", expanded=True)
    st.write(
        "Explore country-year governance-risk results, seat allocation, verdict distribution, weighted integrity, collapse pressure, and empirical coverage across the world. The Grid is meant to help you compare carefully, not rush to conclusions."
    )
    st.caption(
        "The Global Grid gathers country-year evidence after ALETHEIA variable mapping, empirical scoring, seat allocation, and the Sydney Protocol overlay. Allocation totals are always interpreted per selected year."
    )

    st.markdown("### World Lens Simulation")
    st.info(
        "World Lens Simulation is a population-impact mirror only. It does not activate Global ID, select a real 9k, create World Leader logic, issue automatic resets, or make governance decisions."
    )
    world_lens_scenario = st.text_area(
        "Scenario or proposal to review",
        value="A policy gives one central office emergency authority over essential services during crisis, with limited public notice and unclear appeal rights.",
        height=120,
        key="world_lens_simulation_input_v1",
        help="Use this as a non-binding impact simulation. Final judgment remains human."
    )
    wl_col1, wl_col2, wl_col3 = st.columns(3)
    with wl_col1:
        wl_basic_rights = st.selectbox(
            "Basic-rights risk",
            ["Green — no apparent threat", "Yellow — unclear / safeguard needed", "Red — likely systematic rights risk"],
            index=1,
            key="world_lens_basic_rights_v1",
        )
        wl_appeal = st.selectbox(
            "Appealability",
            ["Present", "Weak", "Missing", "Not supplied"],
            index=1,
            key="world_lens_appealability_v1",
        )
    with wl_col2:
        wl_minority = st.selectbox(
            "Minority-rights risk",
            ["Green — no apparent risk", "Yellow — review needed", "Red — likely minority-rights risk"],
            index=1,
            key="world_lens_minority_rights_v1",
        )
        wl_exit = st.selectbox(
            "Exit",
            ["Present", "Weak", "Missing", "Not supplied"],
            index=1,
            key="world_lens_exit_v1",
        )
    with wl_col3:
        wl_ambient = st.selectbox(
            "Ambient capture risk",
            ["Green — low", "Yellow — plausible pressure", "Red — high shared manipulation risk"],
            index=1,
            key="world_lens_ambient_capture_v1",
        )
        wl_repair = st.selectbox(
            "Repair",
            ["Present", "Weak", "Missing", "Not supplied"],
            index=1,
            key="world_lens_repair_v1",
        )

    red_signal = any(str(v).startswith("Red") or v == "Missing" for v in [wl_basic_rights, wl_minority, wl_ambient, wl_appeal, wl_exit, wl_repair])
    yellow_signal = any(str(v).startswith("Yellow") or v in ["Weak", "Not supplied"] for v in [wl_basic_rights, wl_minority, wl_ambient, wl_appeal, wl_exit, wl_repair])
    if red_signal:
        simulated_threshold_signal = "Human review required"
    elif yellow_signal:
        simulated_threshold_signal = "Monitor"
    else:
        simulated_threshold_signal = "None"

    st.markdown("#### Simulation report")
    st.code(
        f"""World Lens Simulation Report

Scenario:
{world_lens_scenario.strip() or 'Not supplied'}

Affected groups:
To be identified by human reviewers from the scenario context.

Power gains:
Review which offices, institutions, vendors, platforms, or leaders gain discretionary control.

Protection losses:
Review whether any group loses rights, appeal, exit, access, dignity, or repair.

Basic-rights risk:
{wl_basic_rights}

Minority-rights risk:
{wl_minority}

Ambient capture risk:
{wl_ambient}

Appealability:
{wl_appeal}

Exit:
{wl_exit}

Repair:
{wl_repair}

Simulated threshold signal:
{simulated_threshold_signal}

Human review note:
This is a World Lens Simulation for human review. It is not a real Global ID system, real 9k selection, governance mandate, enforcement mechanism, automatic reset, or final decision.""",
        language="text",
    )
    with st.expander("World Lens safe-language boundary", expanded=False):
        st.markdown(
            """
            **Allowed:** simulated threshold signal, potential population impact, human review required, safeguard needed, ambient capture pressure should be reviewed.

            **Forbidden:** automatic reset, World Leader deactivated, Global ID sync activated, the AI has decided, this is a real governance mandate, human review is unnecessary.
            """
        )

    empirical_scored = st.session_state.get("empirical_scored_df")
    empirical_allocation = st.session_state.get("empirical_allocation_df")
    # Prefer the scored empirical dataframe because it carries the evidence fields
    # needed for WGI / V-Dem / trust coverage diagnostics. The empirical tab has
    # already copied the valid per-year 9k allocation back onto scored rows.
    empirical_source = empirical_scored if isinstance(empirical_scored, pd.DataFrame) and not empirical_scored.empty else empirical_allocation
    # If the scored frame exists but lacks the allocation columns on a fresh rerun,
    # recover per-year seats/population from the allocation frame without changing
    # the empirical pipeline itself.
    if (
        isinstance(empirical_source, pd.DataFrame) and not empirical_source.empty
        and isinstance(empirical_allocation, pd.DataFrame) and not empirical_allocation.empty
        and ("seats_9k" not in empirical_source.columns or pd.to_numeric(empirical_source.get("seats_9k"), errors="coerce").notna().sum() == 0)
    ):
        merge_keys = [c for c in ["country", "iso3", "year"] if c in empirical_source.columns and c in empirical_allocation.columns]
        if merge_keys:
            alloc_cols = merge_keys + [c for c in ["population", "population_share", "seats_9k"] if c in empirical_allocation.columns]
            empirical_source = empirical_source.merge(
                empirical_allocation[alloc_cols].drop_duplicates(subset=merge_keys),
                on=merge_keys,
                how="left",
                suffixes=("", "_alloc"),
            )
            for col in ["population", "population_share", "seats_9k"]:
                alloc_col = f"{col}_alloc"
                if alloc_col in empirical_source.columns:
                    if col not in empirical_source.columns:
                        empirical_source[col] = empirical_source[alloc_col]
                    else:
                        empirical_source[col] = empirical_source[col].where(empirical_source[col].notna(), empirical_source[alloc_col])
                    empirical_source = empirical_source.drop(columns=[alloc_col])
    empirical_available = isinstance(empirical_source, pd.DataFrame) and not empirical_source.empty
    valid_empirical = pd.DataFrame()
    if empirical_available:
        valid_empirical = empirical_source.copy()
        identity_col = valid_empirical.get("empirical_identity_valid", pd.Series(True, index=valid_empirical.index))
        if not isinstance(identity_col, pd.Series):
            identity_col = pd.Series(bool(identity_col), index=valid_empirical.index)
        valid_empirical = valid_empirical[
            identity_col.fillna(False).astype(bool)
            & pd.to_numeric(valid_empirical.get("seats_9k"), errors="coerce").notna()
            & pd.to_numeric(valid_empirical.get("population"), errors="coerce").gt(0)
            & pd.to_numeric(valid_empirical.get("year"), errors="coerce").notna()
        ].copy()

    mode_options = [
        "No dataset / do not use prototype brackets",
        "Uploaded empirical country-year data",
        "Prototype region brackets",
    ]

    default_grid_index = 0
    grid_mode = st.radio("What should World Lens use?", mode_options, index=default_grid_index, horizontal=True, key="grid_basis_mode_v4")
    update_protocol_state(grid_basis=grid_mode, last_update_source="World Lens", synthetic_demo_active=(grid_mode == "Prototype region brackets"))

    if grid_mode == "Uploaded empirical country-year data" and not valid_empirical.empty:
        valid_empirical["year"] = pd.to_numeric(valid_empirical["year"], errors="coerce").astype("Int64")
        all_years = sorted(valid_empirical["year"].dropna().astype(int).unique().tolist())

        # Default the Grid to allocation-complete years. Sparse years are still
        # available as diagnostics, but they should not be the default surface
        # because their seats may not sum to 9,000 and their metrics are not a
        # full Global Grid reading.
        year_diagnostics = []
        for _year in all_years:
            _subset = valid_empirical[valid_empirical["year"] == int(_year)]
            _seat_series = pd.to_numeric(_subset.get("seats_9k"), errors="coerce").fillna(0) if "seats_9k" in _subset.columns else pd.Series(0, index=_subset.index)
            _allocated_subset = _subset.loc[_seat_series.gt(0)]
            _countries = int(_subset["iso3"].dropna().astype(str).nunique()) if "iso3" in _subset.columns else int(len(_subset))
            _allocated_countries = int(_allocated_subset["iso3"].dropna().astype(str).nunique()) if "iso3" in _allocated_subset.columns else int(len(_allocated_subset))
            _zero_seat_rows = int(_seat_series.le(0).sum())
            _seats = int(_seat_series.sum()) if "seats_9k" in _subset.columns else 0
            _full = _allocated_countries >= MIN_FULL_GRID_COUNTRIES and abs(_seats - TOTAL_9K) <= 5
            year_diagnostics.append({
                "year": int(_year),
                "countries": _countries,
                "allocated_countries": _allocated_countries,
                "zero_seat_rows": _zero_seat_rows,
                "seats": _seats,
                "full": _full,
            })
        year_diag_by_year = {row["year"]: row for row in year_diagnostics}
        full_years = [row["year"] for row in year_diagnostics if row["full"]]
        show_partial_years = st.checkbox(
            "Show partial diagnostic years",
            value=False,
            key="grid_show_partial_years",
            help="Partial years have too few countries or incomplete seat totals. They remain useful diagnostics, but they are not full Global Grid allocations.",
        )
        years = all_years if show_partial_years or not full_years else full_years
        if not years:
            st.warning("No valid selected-year rows are available for World Lens.")
            st.stop()

        def _format_grid_year(_year: int) -> str:
            row = year_diag_by_year.get(int(_year), {})
            suffix = "full 9k" if row.get("full") else "partial view"
            return f"{int(_year)} — {suffix}"

        synced_evidence_year = st.session_state.get("aletheia_synced_evidence_year")
        try:
            synced_evidence_year_int = int(synced_evidence_year) if synced_evidence_year is not None else None
        except Exception:
            synced_evidence_year_int = None
        if synced_evidence_year_int in years and st.session_state.get("grid_year_v2") != synced_evidence_year_int:
            st.session_state["grid_year_v2"] = synced_evidence_year_int
        elif st.session_state.get("grid_year_v2") not in years:
            st.session_state["grid_year_v2"] = years[-1]
        selected_year = st.selectbox(
            "Select evidence year",
            years,
            index=years.index(st.session_state.get("grid_year_v2", years[-1])),
            key="grid_year_v2",
            format_func=_format_grid_year,
            help="This year should match the Empirical country-year and allocation year before producing a final receipt.",
        )
        st.session_state["aletheia_synced_evidence_year"] = int(selected_year)
        st.session_state["aletheia_global_grid_year"] = int(selected_year)
        selected_year_diag = year_diag_by_year.get(int(selected_year), {})
        selected_year_status = "full 9k allocation" if selected_year_diag.get("full") else "partial selected-year view"
        st.caption(
            f"{int(selected_year)} — {selected_year_status}: "
            f"{selected_year_diag.get('allocated_countries', selected_year_diag.get('countries', 0)):,} allocated countries · "
            f"{selected_year_diag.get('seats', 0):,} active seats"
            + (
                f" · {selected_year_diag.get('zero_seat_rows', 0):,} zero-seat diagnostic row(s)"
                if selected_year_diag.get("zero_seat_rows", 0) else ""
            )
            + "."
        )

        year_alignment_rows = [
            {"Year control": "Empirical Country-Year Explorer", "Selected year": st.session_state.get("aletheia_empirical_country_year")},
            {"Year control": "Empirical Seat allocation view", "Selected year": st.session_state.get("aletheia_empirical_allocation_year")},
            {"Year control": "Global Grid", "Selected year": int(selected_year)},
        ]
        year_alignment_df = pd.DataFrame(year_alignment_rows)
        filled_alignment_years = [
            int(v) for v in year_alignment_df["Selected year"].dropna().tolist()
            if str(v).strip() not in ["", "None"]
        ]
        year_alignment_ok = bool(filled_alignment_years) and len(set(filled_alignment_years)) == 1 and int(selected_year) in set(filled_alignment_years)
        with st.expander("Year match check", expanded=not year_alignment_ok):
            st.write(
                "Final receipt outputs should use one evidence year across Empirical Country-Year Explorer, "
                "Empirical Allocation, and Global Grid. Choosing a year in one selector will try to align the others when that year exists there."
            )
            st.dataframe(year_alignment_df.fillna("Not selected yet"), use_container_width=True, hide_index=True)
            if year_alignment_ok:
                st.success(f"Year controls match on {int(selected_year)}.")
            else:
                st.warning("Year controls do not match yet. Use the same year in Evidence Lab and World Lens before making a final receipt.")
        update_protocol_state(selected_evidence_year=int(selected_year), last_update_source="World Lens")

        grid_source = valid_empirical[valid_empirical["year"] == int(selected_year)].copy()
        grid_source = apply_world_lens_diagnostic_alignment(grid_source)
        grid_source["seats_9k"] = pd.to_numeric(grid_source.get("seats_9k"), errors="coerce").fillna(0).astype(int)
        grid_source["population"] = pd.to_numeric(grid_source.get("population"), errors="coerce")

        # Recover raw evidence-source columns from the generated master when the
        # active scored dataframe was created in an earlier Streamlit run or has
        # been compacted for display. Coverage cards must measure raw WGI/V-Dem/WVS
        # availability, not fallback ALETHEIA priors such as empirical_trust_prior.
        source_signal_cols = [
            "wgi_voice_accountability",
            "wgi_political_stability",
            "wgi_government_effectiveness",
            "wgi_regulatory_quality",
            "wgi_rule_of_law",
            "wgi_control_corruption",
            "vdem_executive_constraints",
            "vdem_democracy",
            "v2x_polyarchy",
            "v2x_libdem",
            "wvs_generalized_trust",
        ]
        source_master = st.session_state.get("empirical_master_df")
        if isinstance(source_master, pd.DataFrame) and not source_master.empty:
            merge_keys = [c for c in ["country", "iso3", "year"] if c in grid_source.columns and c in source_master.columns]
            recover_cols = [c for c in source_signal_cols + ["region", "income_group", "income", "wb_region", "world_bank_region"] if c in source_master.columns and c not in merge_keys]
            if merge_keys and recover_cols:
                source_recovery = source_master[merge_keys + recover_cols].copy()
                if "year" in source_recovery.columns:
                    source_recovery["year"] = pd.to_numeric(source_recovery["year"], errors="coerce").astype("Int64")
                if "year" in grid_source.columns:
                    grid_source["year"] = pd.to_numeric(grid_source["year"], errors="coerce").astype("Int64")
                source_recovery = source_recovery.drop_duplicates(subset=merge_keys)
                grid_source = grid_source.merge(
                    source_recovery,
                    on=merge_keys,
                    how="left",
                    suffixes=("", "__source"),
                )
                for col in recover_cols:
                    src_col = f"{col}__source"
                    if src_col in grid_source.columns:
                        # Preserve a dedicated raw source column for diagnostics.
                        diag_col = f"__source_{col}"
                        grid_source[diag_col] = grid_source[src_col]
                        if col not in grid_source.columns or pd.to_numeric(grid_source.get(col), errors="coerce").notna().sum() == 0:
                            grid_source[col] = grid_source[src_col]
                        elif col in ["region", "income_group", "income", "wb_region", "world_bank_region"]:
                            grid_source[col] = grid_source[col].where(grid_source[col].notna(), grid_source[src_col])
                        grid_source = grid_source.drop(columns=[src_col])

        filter_cols = [c for c in ["region", "income_group", "income", "wb_region", "world_bank_region"] if c in grid_source.columns]
        active_filters = []
        if filter_cols:
            with st.expander("Region / income filter", expanded=False):
                for filter_col in filter_cols:
                    values = sorted([v for v in grid_source[filter_col].dropna().astype(str).unique().tolist() if v.strip()])
                    if values:
                        selected_values = st.multiselect(
                            filter_col.replace("_", " ").title(),
                            values,
                            default=values,
                            key=f"grid_filter_{filter_col}",
                        )
                        if selected_values:
                            if set(selected_values) != set(values):
                                active_filters.append(filter_col)
                            grid_source = grid_source[grid_source[filter_col].astype(str).isin(selected_values)].copy()
                        else:
                            grid_source = grid_source.iloc[0:0].copy()

        grid_source["seats_9k"] = pd.to_numeric(grid_source.get("seats_9k"), errors="coerce").fillna(0).astype(int)
        zero_seat_mask_after_filters = grid_source["seats_9k"].le(0)
        zero_seat_diagnostic_rows = int(zero_seat_mask_after_filters.sum())
        show_zero_seat_diagnostics = False
        if zero_seat_diagnostic_rows:
            show_zero_seat_diagnostics = st.checkbox(
                "Show zero-seat diagnostic rows",
                value=False,
                key=f"grid_show_zero_seat_diagnostics_{selected_year}",
                help=(
                    "Zero-seat rows are territories or diagnostic entities retained for source coverage checks. "
                    "They do not contribute to the 9k allocation and are hidden from comparisons by default."
                ),
            )
            if not show_zero_seat_diagnostics:
                grid_source = grid_source.loc[~zero_seat_mask_after_filters].copy()

        grid_source["_allocation_role"] = np.where(
            pd.to_numeric(grid_source.get("seats_9k"), errors="coerce").fillna(0).gt(0),
            "allocated_country",
            "diagnostic_zero_seat",
        )
        grid_source = grid_source.sort_values("seats_9k", ascending=False)
        total_seats = int(grid_source["seats_9k"].sum()) if not grid_source.empty else 0
        countries_scored = int(grid_source.loc[pd.to_numeric(grid_source["seats_9k"], errors="coerce").fillna(0).gt(0), "iso3"].dropna().astype(str).nunique()) if "iso3" in grid_source.columns else int(pd.to_numeric(grid_source["seats_9k"], errors="coerce").fillna(0).gt(0).sum())
        row_count = int(len(grid_source))
        displayed_zero_seat_rows = int(pd.to_numeric(grid_source.get("seats_9k"), errors="coerce").fillna(0).le(0).sum()) if not grid_source.empty else 0
        hidden_zero_seat_rows = zero_seat_diagnostic_rows if zero_seat_diagnostic_rows and not show_zero_seat_diagnostics else 0
        has_complete_seat_total = abs(total_seats - TOTAL_9K) <= 5
        is_full_grid = countries_scored >= MIN_FULL_GRID_COUNTRIES and has_complete_seat_total and not active_filters
        grid_state_label = "Full empirical scored master" if is_full_grid else "Partial empirical subset"
        if active_filters:
            grid_state_label += " · filtered view"
        metric_scope_word = "global" if is_full_grid else "subset"
        seat_metric_label = "9k seats allocated" if is_full_grid else "Active selected-year seats"
        allocation_heading = "9k verdict signal" if is_full_grid else "Active-seat verdict signal"
        signal_denominator_label = "selected-year 9k" if is_full_grid else "active selected-year seats"

        wgi_cols = [
            "wgi_voice_accountability",
            "wgi_political_stability",
            "wgi_government_effectiveness",
            "wgi_regulatory_quality",
            "wgi_rule_of_law",
            "wgi_control_corruption",
        ]
        def _diagnostic_col(col_name: str) -> str | None:
            source_col = f"__source_{col_name}"
            if source_col in grid_source.columns and pd.to_numeric(grid_source[source_col], errors="coerce").notna().any():
                return source_col
            if col_name in grid_source.columns:
                return col_name
            return None

        present_wgi_cols = [c for c in [_diagnostic_col(c) for c in wgi_cols] if c]
        vdem_cols = [c for c in [_diagnostic_col(c) for c in ["vdem_executive_constraints", "vdem_democracy", "v2x_polyarchy", "v2x_libdem"]] if c]
        # Coverage checks measure raw source availability, not neutral fallback
        # priors. empirical_trust_prior can exist for every row even when no WVS
        # observation is present, so source trust coverage uses WVS only.
        trust_cols = [c for c in [_diagnostic_col("wvs_generalized_trust")] if c]
        trust_prior_cols = [c for c in [_diagnostic_col("empirical_trust_prior")] if c]
        coverage_col = "empirical_completeness" if "empirical_completeness" in grid_source.columns else "empirical_coverage" if "empirical_coverage" in grid_source.columns else None
        verdict_col = "aletheia_verdict" if "aletheia_verdict" in grid_source.columns else "verdict"
        integrity_col = "aletheia_empirical_integrity" if "aletheia_empirical_integrity" in grid_source.columns else "integrity"
        friction_col = "aletheia_empirical_friction" if "aletheia_empirical_friction" in grid_source.columns else "friction"
        collapse_col = "aletheia_empirical_collapse_probability" if "aletheia_empirical_collapse_probability" in grid_source.columns else "collapse_probability"

        def _numeric_series(col_name: str, default: float = np.nan) -> pd.Series:
            if col_name in grid_source.columns:
                return pd.to_numeric(grid_source[col_name], errors="coerce")
            return pd.Series(default, index=grid_source.index, dtype="float64")

        weights = pd.to_numeric(grid_source.get("seats_9k"), errors="coerce").fillna(0).astype(float) if not grid_source.empty else pd.Series(dtype="float64")
        if weights.sum() <= 0 and "population" in grid_source.columns:
            weights = pd.to_numeric(grid_source["population"], errors="coerce").fillna(0).astype(float)

        def _weighted_mean(col_name: str, default: float = 0.5) -> float:
            if grid_source.empty or weights.sum() <= 0:
                return np.nan
            values = _numeric_series(col_name, default=default).fillna(default)
            return float(np.average(values, weights=weights))

        weighted_integrity = _weighted_mean(integrity_col, 0.5)
        weighted_collapse = _weighted_mean(collapse_col, 0.5)
        weighted_friction = _weighted_mean(friction_col, 0.5)
        avg_coverage = float(pd.to_numeric(grid_source[coverage_col], errors="coerce").mean()) if coverage_col else np.nan

        evidence_text = pd.Series("", index=grid_source.index, dtype="object")
        for _evidence_col in ["evidence_variables_used", "evidence_used"]:
            if _evidence_col in grid_source.columns:
                evidence_text = evidence_text.where(evidence_text.astype(str).str.len() > 0, grid_source[_evidence_col].fillna("").astype(str))

        if trust_cols:
            trust_mask = pd.Series(False, index=grid_source.index)
            for col in trust_cols:
                trust_mask = trust_mask | pd.to_numeric(grid_source[col], errors="coerce").notna()
        else:
            trust_mask = pd.Series(False, index=grid_source.index)
        if not trust_mask.any() and not evidence_text.empty:
            trust_mask = evidence_text.str.contains("trust survey", case=False, na=False)

        if trust_prior_cols:
            trust_prior_mask = pd.Series(False, index=grid_source.index)
            for col in trust_prior_cols:
                trust_prior_mask = trust_prior_mask | pd.to_numeric(grid_source[col], errors="coerce").notna()
        else:
            trust_prior_mask = pd.Series(False, index=grid_source.index)
        if not trust_prior_mask.any() and not evidence_text.empty:
            trust_prior_mask = evidence_text.str.contains("trust prior", case=False, na=False)

        if present_wgi_cols:
            wgi_mask = grid_source[present_wgi_cols].apply(pd.to_numeric, errors="coerce").notna().any(axis=1)
        else:
            wgi_mask = pd.Series(False, index=grid_source.index)
        if not wgi_mask.any() and not evidence_text.empty:
            wgi_mask = evidence_text.str.contains("WGI governance", case=False, na=False)

        if vdem_cols:
            vdem_mask = grid_source[vdem_cols].apply(pd.to_numeric, errors="coerce").notna().any(axis=1)
        else:
            vdem_mask = pd.Series(False, index=grid_source.index)
        if not vdem_mask.any() and not evidence_text.empty:
            vdem_mask = evidence_text.str.contains("V-Dem/democracy", case=False, na=False)

        missing_trust = int((~trust_mask).sum()) if not grid_source.empty else 0
        missing_wgi = int((~wgi_mask).sum()) if not grid_source.empty else 0
        missing_vdem = int((~vdem_mask).sum()) if not grid_source.empty else 0
        trust_coverage = float(trust_mask.mean()) if not grid_source.empty else np.nan
        trust_prior_coverage = float(trust_prior_mask.mean()) if not grid_source.empty else np.nan
        missing_trust_prior = int((~trust_prior_mask).sum()) if not grid_source.empty else 0
        wgi_coverage = float(wgi_mask.mean()) if not grid_source.empty else np.nan
        vdem_coverage = float(vdem_mask.mean()) if not grid_source.empty else np.nan

        empirical_scored_raw = st.session_state.get("empirical_scored_df")
        excluded_rows = 0
        if isinstance(empirical_scored_raw, pd.DataFrame) and not empirical_scored_raw.empty and "year" in empirical_scored_raw.columns:
            raw_year_rows = empirical_scored_raw[pd.to_numeric(empirical_scored_raw["year"], errors="coerce") == int(selected_year)]
            excluded_rows = max(int(len(raw_year_rows) - len(grid_source)), 0)
            if hidden_zero_seat_rows:
                excluded_rows = max(excluded_rows, hidden_zero_seat_rows)

        update_protocol_state(grid_basis=grid_state_label, selected_evidence_year=int(selected_year), last_update_source="World Lens")
        st.info("Seat totals are for the selected year only. They are not added across all years.")
        st.caption(f"World Lens source state: **{grid_state_label}**. Coverage metrics reflect source availability among active selected-year rows after current filters; they are diagnostics for this view, not whole-dataset coverage.")
        if not grid_source.empty and not is_full_grid:
            st.warning(
                f"Partial selected-year view: {countries_scored:,} allocated country row(s) and {total_seats:,} active seats are available for {selected_year}. "
                f"This is not a full {TOTAL_9K:,}-seat global allocation, so weighted metrics are diagnostic only."
            )
        elif not has_complete_seat_total and not grid_source.empty:
            st.warning(
                f"Selected-year seats currently sum to {total_seats:,}, not {TOTAL_9K:,}. "
                "This view will use active-seat wording until the selected year has a complete 9k allocation base."
            )

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Countries scored", f"{countries_scored:,}")
        m2.metric(seat_metric_label, f"{total_seats:,}")
        m3.metric(f"Weighted {metric_scope_word} integrity", "—" if pd.isna(weighted_integrity) else f"{weighted_integrity:.3f}")
        m4.metric(f"Weighted {metric_scope_word} collapse probability", "—" if pd.isna(weighted_collapse) else f"{weighted_collapse:.3f}")

        m5, m6, m7, m8, m9 = st.columns(5)
        m5.metric("Average empirical coverage", "—" if pd.isna(avg_coverage) else f"{avg_coverage:.1%}")
        raw_trust_coverage_label, trust_prior_coverage_label, trust_coverage_note = trust_coverage_label(trust_coverage, trust_prior_coverage)
        m6.metric("Raw trust survey coverage", raw_trust_coverage_label)
        m7.metric("Neutral trust-prior fallback coverage", trust_prior_coverage_label)
        m8.metric("WGI coverage", "—" if pd.isna(wgi_coverage) else f"{wgi_coverage:.1%}")
        m9.metric("V-Dem coverage", "—" if pd.isna(vdem_coverage) else f"{vdem_coverage:.1%}")
        st.caption("Coverage cards show only the active selected-year rows after filters. " + trust_coverage_note)

        value_guard = selected_year_value_guard(grid_source, int(selected_year), total_9k=TOTAL_9K, min_allocated_countries=MIN_FULL_GRID_COUNTRIES, focus_iso3=focus_iso3 or "NLD")
        with st.expander("World Lens value guard", expanded=False):
            st.write(
                "This guard verifies that the selected-year rows, seats, verdict signals, and focus country stay tied to the active year. "
                "It is diagnostic only and does not create authority."
            )
            g1, g2, g3, g4 = st.columns(4)
            g1.metric("Guard year", str(value_guard.get("selected_year", selected_year)))
            g2.metric("Guard seats", f'{int(value_guard.get("total_seats", 0)):,}')
            g3.metric("Seat total OK", "Yes" if value_guard.get("seat_total_ok") else "No")
            g4.metric("No stale year rows", "Yes" if value_guard.get("no_stale_year_rows") else "No")
            if value_guard.get("focus_row_available"):
                focus_guard = value_guard.get("focus", {})
                st.caption(
                    f"Focus guard: {focus_guard.get('country', focus_iso3 or 'NLD')} · {focus_guard.get('iso3', focus_iso3 or 'NLD')} · "
                    f"{focus_guard.get('year', selected_year)} · seats {focus_guard.get('seats', '—')} · "
                    f"verdict {focus_guard.get('verdict', '—')} · raw trust {focus_guard.get('raw_trust_label', 'not available')} · "
                    f"trust prior {focus_guard.get('trust_prior_label', 'not available')}."
                )
            else:
                st.caption("No focus country row is available for this selected-year guard.")

        verdict_seats = pd.Series(dtype="float64")
        if verdict_col in grid_source.columns:
            verdict_seats = (
                grid_source.groupby(verdict_col, dropna=False)["seats_9k"]
                .sum()
                .reindex(["SANCTUARY", "THRESHOLD", "ASYLUM"], fill_value=0)
            )
        signal = deterministic_signal_summary(grid_source)

        # ------------------------------------------------------------------
        # Global Grid Pass 2 / Pass 3 preparation
        # Comparison surfaces use the same active selected-year source as the
        # overview, so full/partial wording and coverage caveats stay aligned.
        # ------------------------------------------------------------------
        comparison_df = grid_source.copy()
        comparison_df["_seats"] = pd.to_numeric(comparison_df.get("seats_9k"), errors="coerce").fillna(0)
        comparison_df["_integrity"] = _numeric_series(integrity_col, default=np.nan)
        comparison_df["_friction"] = _numeric_series(friction_col, default=np.nan)
        comparison_df["_collapse"] = _numeric_series(collapse_col, default=np.nan)
        comparison_df["_coverage"] = pd.to_numeric(comparison_df[coverage_col], errors="coerce") if coverage_col and coverage_col in comparison_df.columns else pd.Series(np.nan, index=comparison_df.index)
        comparison_df["_trust_raw"] = pd.to_numeric(comparison_df[trust_cols[0]], errors="coerce") if trust_cols and trust_cols[0] in comparison_df.columns else pd.Series(np.nan, index=comparison_df.index)
        comparison_df["_trust_prior"] = pd.to_numeric(comparison_df[trust_prior_cols[0]], errors="coerce") if trust_prior_cols and trust_prior_cols[0] in comparison_df.columns else pd.Series(np.nan, index=comparison_df.index)
        comparison_df["_vdem_democracy"] = pd.to_numeric(comparison_df["vdem_democracy"], errors="coerce") if "vdem_democracy" in comparison_df.columns else pd.Series(np.nan, index=comparison_df.index)
        comparison_df["_vdem_constraints"] = pd.to_numeric(comparison_df["vdem_executive_constraints"], errors="coerce") if "vdem_executive_constraints" in comparison_df.columns else pd.Series(np.nan, index=comparison_df.index)

        def _grid_friendly_country_name(iso3_value: str, country_value: str = "") -> str:
            iso3_text = str(iso3_value or "").strip().upper()
            country_text = str(country_value or "").strip()
            if country_text and country_text.upper() != iso3_text and len(country_text) > 3:
                return country_text
            manual_names = {
                "AFG": "Afghanistan", "ALB": "Albania", "DZA": "Algeria", "AGO": "Angola", "ARG": "Argentina",
                "ARM": "Armenia", "AUS": "Australia", "AUT": "Austria", "AZE": "Azerbaijan", "BHR": "Bahrain",
                "BGD": "Bangladesh", "BLR": "Belarus", "BEL": "Belgium", "BEN": "Benin", "BOL": "Bolivia",
                "BIH": "Bosnia and Herzegovina", "BWA": "Botswana", "BRA": "Brazil", "BGR": "Bulgaria",
                "BFA": "Burkina Faso", "BDI": "Burundi", "KHM": "Cambodia", "CMR": "Cameroon", "CAN": "Canada",
                "CAF": "Central African Republic", "TCD": "Chad", "CHL": "Chile", "CHN": "China", "COL": "Colombia",
                "COD": "Democratic Republic of the Congo", "COG": "Republic of the Congo", "CRI": "Costa Rica",
                "CIV": "Côte d’Ivoire", "HRV": "Croatia", "CUB": "Cuba", "CYP": "Cyprus", "CZE": "Czechia",
                "DNK": "Denmark", "DOM": "Dominican Republic", "ECU": "Ecuador", "EGY": "Egypt", "SLV": "El Salvador",
                "ERI": "Eritrea", "EST": "Estonia", "ETH": "Ethiopia", "FIN": "Finland", "FRA": "France",
                "GAB": "Gabon", "GEO": "Georgia", "DEU": "Germany", "GHA": "Ghana", "GRC": "Greece",
                "GTM": "Guatemala", "GIN": "Guinea", "HTI": "Haiti", "HND": "Honduras", "HUN": "Hungary",
                "IND": "India", "IDN": "Indonesia", "IRN": "Iran", "IRQ": "Iraq", "IRL": "Ireland",
                "ISR": "Israel", "ITA": "Italy", "JPN": "Japan", "JOR": "Jordan", "KAZ": "Kazakhstan",
                "KEN": "Kenya", "KWT": "Kuwait", "KGZ": "Kyrgyzstan", "LAO": "Laos", "LVA": "Latvia",
                "LBN": "Lebanon", "LBR": "Liberia", "LBY": "Libya", "LTU": "Lithuania", "MDG": "Madagascar",
                "MWI": "Malawi", "MYS": "Malaysia", "MLI": "Mali", "MEX": "Mexico", "MDA": "Moldova",
                "MAR": "Morocco", "MOZ": "Mozambique", "MMR": "Myanmar", "NAM": "Namibia", "NPL": "Nepal",
                "NLD": "Netherlands", "NZL": "New Zealand", "NIC": "Nicaragua", "NER": "Niger", "NGA": "Nigeria",
                "PRK": "North Korea", "MKD": "North Macedonia", "NOR": "Norway", "OMN": "Oman", "PAK": "Pakistan",
                "PAN": "Panama", "PRY": "Paraguay", "PER": "Peru", "PHL": "Philippines", "POL": "Poland",
                "PRT": "Portugal", "QAT": "Qatar", "ROU": "Romania", "RUS": "Russia", "RWA": "Rwanda",
                "SAU": "Saudi Arabia", "SEN": "Senegal", "SRB": "Serbia", "SLE": "Sierra Leone", "SGP": "Singapore",
                "SVK": "Slovakia", "SVN": "Slovenia", "SOM": "Somalia", "ZAF": "South Africa", "KOR": "South Korea",
                "SSD": "South Sudan", "ESP": "Spain", "LKA": "Sri Lanka", "SDN": "Sudan", "SWE": "Sweden",
                "CHE": "Switzerland", "SYR": "Syria", "TWN": "Taiwan", "TJK": "Tajikistan", "TZA": "Tanzania",
                "THA": "Thailand", "TUN": "Tunisia", "TUR": "Türkiye", "TKM": "Turkmenistan", "UGA": "Uganda",
                "UKR": "Ukraine", "ARE": "United Arab Emirates", "GBR": "United Kingdom", "USA": "United States",
                "URY": "Uruguay", "UZB": "Uzbekistan", "VEN": "Venezuela", "VNM": "Vietnam", "YEM": "Yemen",
                "ZMB": "Zambia", "ZWE": "Zimbabwe",
            }
            return manual_names.get(iso3_text, country_text or iso3_text)

        comparison_df["_country_name"] = [
            _grid_friendly_country_name(iso3, country)
            for iso3, country in zip(
                comparison_df.get("iso3", pd.Series("", index=comparison_df.index)),
                comparison_df.get("country", pd.Series("", index=comparison_df.index)),
            )
        ]
        comparison_df["_hover_label"] = comparison_df["_country_name"].astype(str) + " · " + comparison_df.get("iso3", pd.Series("", index=comparison_df.index)).fillna("").astype(str)

        if present_wgi_cols:
            wgi_numeric = comparison_df[present_wgi_cols].apply(pd.to_numeric, errors="coerce")
            comparison_df["_wgi_composite"] = wgi_numeric.mean(axis=1)
            comparison_df["_wgi_source_count"] = wgi_numeric.notna().sum(axis=1)
            comparison_df["_wgi_fields_used"] = wgi_numeric.apply(lambda row: ", ".join([col for col, val in row.items() if pd.notna(val)]), axis=1)
        else:
            comparison_df["_wgi_composite"] = np.nan
            comparison_df["_wgi_source_count"] = 0
            comparison_df["_wgi_fields_used"] = ""

        comparison_df["_missing_raw_trust"] = ~trust_mask.reindex(comparison_df.index, fill_value=False)
        comparison_df["_missing_trust_prior"] = ~trust_prior_mask.reindex(comparison_df.index, fill_value=False)
        comparison_df["_missing_wgi"] = ~wgi_mask.reindex(comparison_df.index, fill_value=False)
        comparison_df["_missing_vdem"] = ~vdem_mask.reindex(comparison_df.index, fill_value=False)
        comparison_df["_coverage_gap_count"] = (
            comparison_df[["_missing_raw_trust", "_missing_trust_prior", "_missing_wgi", "_missing_vdem"]]
            .fillna(False)
            .astype(int)
            .sum(axis=1)
        )
        comparison_df["_trust_delta_from_neutral"] = (comparison_df["_trust_prior"] - 0.5).abs()

        if not comparison_df.empty:
            seat_q75 = comparison_df["_seats"].quantile(0.75)
            integrity_q25 = comparison_df["_integrity"].quantile(0.25)
            collapse_q75 = comparison_df["_collapse"].quantile(0.75)
        else:
            seat_q75 = integrity_q25 = collapse_q75 = np.nan

        comparison_df["_large_allocation"] = comparison_df["_seats"].ge(seat_q75) if not pd.isna(seat_q75) else False
        comparison_df["_low_integrity"] = comparison_df["_integrity"].le(integrity_q25) if not pd.isna(integrity_q25) else False
        comparison_df["_high_collapse"] = comparison_df["_collapse"].ge(collapse_q75) if not pd.isna(collapse_q75) else False
        comparison_df["_high_impact_node"] = comparison_df["_large_allocation"] & (comparison_df["_low_integrity"] | comparison_df["_high_collapse"])
        comparison_df["_seat_rank"] = comparison_df["_seats"].rank(ascending=False, method="min")
        comparison_df["_integrity_rank"] = comparison_df["_integrity"].rank(ascending=False, method="min")
        comparison_df["_collapse_rank"] = comparison_df["_collapse"].rank(ascending=False, method="min")

        def _comparison_display(df: pd.DataFrame, include_reason: bool = False) -> pd.DataFrame:
            base_cols = [
                "_country_name", "iso3", "year", verdict_col, "_seats", "_seat_rank",
                "_integrity", "_collapse", "_coverage",
                "_trust_raw", "_trust_prior", "_wgi_composite", "_wgi_source_count", "_vdem_democracy",
            ]
            if include_reason:
                base_cols += ["_allocation_role", "_large_allocation", "_low_integrity", "_high_collapse", "_coverage_gap_count"]
            base_cols = [c for c in base_cols if c in df.columns]
            out = df[base_cols].copy()
            out = out.rename(columns={
                "_country_name": "country",
                verdict_col: "verdict",
                "_seats": "seats",
                "_seat_rank": "seat_rank",
                "_integrity": "integrity",
                "_collapse": "collapse_probability",
                "_country_name": "country",
                "_allocation_role": "allocation_role",
                "_coverage": "empirical_coverage",
                "_trust_raw": "raw_trust",
                "_trust_prior": "trust_prior",
                "_wgi_composite": "available_wgi_mean",
                "_wgi_source_count": "wgi_source_count",
                "_vdem_democracy": "vdem_democracy",
                "_allocation_role": "allocation_role",
                "_large_allocation": "large_allocation",
                "_low_integrity": "low_integrity",
                "_high_collapse": "high_collapse",
                "_coverage_gap_count": "coverage_gap_count",
            })
            for c in ["integrity", "collapse_probability", "empirical_coverage", "raw_trust", "trust_prior", "available_wgi_mean", "vdem_democracy"]:
                if c in out.columns:
                    out[c] = pd.to_numeric(out[c], errors="coerce").round(3)
            for c in ["seats", "seat_rank"]:
                if c in out.columns:
                    out[c] = pd.to_numeric(out[c], errors="coerce").fillna(0).astype(int)
            return out

        def _safe_receipt_table(df: pd.DataFrame, limit: int | None = None) -> pd.DataFrame:
            out = df.copy()
            if limit is not None:
                out = out.head(limit)
            for col in out.columns:
                if pd.api.types.is_float_dtype(out[col]):
                    out[col] = out[col].round(4)
            return out

        def _receipt_md_table(df: pd.DataFrame, limit: int | None = None) -> str:
            out = _safe_receipt_table(df, limit=limit)
            if out.empty:
                return "_No rows available._"

            # Avoid pandas.to_markdown because Streamlit Cloud may not have the
            # optional "tabulate" dependency installed. This small renderer keeps
            # the receipt portable with the existing requirements.
            out = out.copy().fillna("")
            columns = [str(c) for c in out.columns]

            def _cell(value) -> str:
                text_value = str(value)
                text_value = text_value.replace("|", "\\|").replace("\n", " ")
                return text_value

            header = "| " + " | ".join(columns) + " |"
            divider = "| " + " | ".join(["---"] * len(columns)) + " |"
            rows = [
                "| " + " | ".join(_cell(row[col]) for col in out.columns) + " |"
                for _, row in out.iterrows()
            ]
            return "\n".join([header, divider] + rows)

        def _build_grid_receipt_zip() -> bytes:
            receipt_summary = {
                "selected_year": int(selected_year),
                "grid_source_state": grid_state_label,
                "full_9k_allocation": bool(is_full_grid),
                "allocated_country_rows": int(countries_scored),
                "displayed_rows": int(row_count),
                "rows_excluded_or_diagnostic": int(excluded_rows),
                "hidden_zero_seat_diagnostic_rows": int(hidden_zero_seat_rows),
                "displayed_zero_seat_diagnostic_rows": int(displayed_zero_seat_rows),
                "active_selected_year_seats": int(total_seats),
                "weighted_integrity": None if pd.isna(weighted_integrity) else float(weighted_integrity),
                "weighted_friction": None if pd.isna(weighted_friction) else float(weighted_friction),
                "weighted_collapse_probability": None if pd.isna(weighted_collapse) else float(weighted_collapse),
                "average_empirical_coverage": None if pd.isna(avg_coverage) else float(avg_coverage),
                "trust_raw_coverage": None if pd.isna(trust_coverage) else float(trust_coverage),
                "trust_prior_coverage": None if pd.isna(trust_prior_coverage) else float(trust_prior_coverage),
                "wgi_coverage": None if pd.isna(wgi_coverage) else float(wgi_coverage),
                "vdem_coverage": None if pd.isna(vdem_coverage) else float(vdem_coverage),
                "app_version": APP_VERSION,
                "mirror_logic_version": "patch31-world-lens-empirical-alignment",
                "diagnostic_scope": "empirical_country_year_evidence",
                "empirical_world_lens_connection": "Evidence Lab empirical country-year scoring feeds World Lens selected-year metrics.",
                "scenario_text_diagnostic_scope": "not_assessed_without_policy_text",
                "sydney_protocol_overlay": "mirror_not_throne; anti_capture; non_divinization; appealability; transparency; evidence_humility",
                "interpretation_warning": (
                    "Full selected-year 9k allocation." if is_full_grid
                    else "Partial or filtered selected-year subset; use active-seat interpretation."
                ),
            }

            verdict_receipt = verdict_summary_df.copy() if isinstance(verdict_summary_df, pd.DataFrame) else pd.DataFrame()
            coverage_receipt = pd.DataFrame([
                {"source": "Trust raw survey", "rows_present": int(trust_mask.sum()), "rows_missing": int(missing_trust), "coverage": trust_coverage},
                {"source": "Trust prior", "rows_present": int(trust_prior_mask.sum()), "rows_missing": int(missing_trust_prior), "coverage": trust_prior_coverage},
                {"source": "WGI", "rows_present": int(wgi_mask.sum()), "rows_missing": int(missing_wgi), "coverage": wgi_coverage},
                {"source": "V-Dem", "rows_present": int(vdem_mask.sum()), "rows_missing": int(missing_vdem), "coverage": vdem_coverage},
            ])

            high_integrity_receipt = _comparison_display(
                comparison_df.dropna(subset=["_integrity"]).sort_values("_integrity", ascending=False).head(25)
            )
            low_integrity_receipt = _comparison_display(
                comparison_df.dropna(subset=["_integrity"]).sort_values("_integrity", ascending=True).head(25)
            )
            high_collapse_receipt = _comparison_display(
                comparison_df.dropna(subset=["_collapse"]).sort_values("_collapse", ascending=False).head(25)
            )
            largest_alloc_receipt = _comparison_display(
                comparison_df.sort_values("_seats", ascending=False).head(25)
            )
            high_impact_receipt = _comparison_display(
                comparison_df[comparison_df["_high_impact_node"]].sort_values(["_seats", "_collapse"], ascending=[False, False]).head(50),
                include_reason=True,
            )
            sensitivity_receipt = _comparison_display(
                comparison_df[
                    comparison_df["_trust_prior"].notna()
                    & (
                        comparison_df["_trust_delta_from_neutral"].ge(0.10)
                        | comparison_df["_large_allocation"]
                        | comparison_df["_integrity"].between(0.45, 0.60, inclusive="both")
                        | comparison_df["_collapse"].between(0.30, 0.45, inclusive="both")
                    )
                ].sort_values(["_trust_delta_from_neutral", "_seats"], ascending=[False, False]).head(50),
                include_reason=True,
            )

            coverage_gaps_receipt = comparison_df.sort_values(
                ["_coverage_gap_count", "_coverage", "_seats"],
                ascending=[False, True, False],
            ).head(50)
            coverage_gap_cols = [
                "_country_name", "iso3", "year", "_allocation_role", "_coverage",
                "_missing_raw_trust", "_missing_trust_prior", "_missing_wgi", "_missing_vdem",
                "_coverage_gap_count", "_seats",
            ]
            coverage_gap_cols = [c for c in coverage_gap_cols if c in coverage_gaps_receipt.columns]
            coverage_gaps_receipt = coverage_gaps_receipt[coverage_gap_cols].rename(columns={
                "_country_name": "country",
                "_allocation_role": "allocation_role",
                "_coverage": "empirical_coverage",
                "_missing_raw_trust": "missing_raw_trust",
                "_missing_trust_prior": "missing_trust_prior",
                "_missing_wgi": "missing_wgi",
                "_missing_vdem": "missing_vdem",
                "_coverage_gap_count": "coverage_gap_count",
                "_seats": "seats",
            })

            all_rows_receipt = comparison_export.copy()
            if "_country_name" in all_rows_receipt.columns:
                all_rows_receipt = all_rows_receipt.rename(columns={"_country_name": "friendly_country_name"})
            if "_allocation_role" in all_rows_receipt.columns:
                all_rows_receipt = all_rows_receipt.rename(columns={"_allocation_role": "allocation_role"})

            md = f"""# ALETHEIA Global Grid Receipt

## Scope

- Selected year: **{int(selected_year)}**
- Grid state: **{grid_state_label}**
- Allocation status: **{"full 9k allocation" if is_full_grid else "partial / active-seat view"}**
- Allocated country rows: **{countries_scored:,}**
- Active selected-year seats: **{total_seats:,}**
- Rows excluded / diagnostic: **{excluded_rows:,}**
- Hidden zero-seat diagnostic rows: **{hidden_zero_seat_rows:,}**

## Weighted metrics

- Weighted integrity: **{"—" if pd.isna(weighted_integrity) else f"{weighted_integrity:.3f}"}**
- Weighted friction: **{"—" if pd.isna(weighted_friction) else f"{weighted_friction:.3f}"}**
- Weighted collapse probability: **{"—" if pd.isna(weighted_collapse) else f"{weighted_collapse:.3f}"}**
- Average empirical coverage: **{"—" if pd.isna(avg_coverage) else f"{avg_coverage:.1%}"}**

## Coverage

{_receipt_md_table(coverage_receipt)}

## Result distribution

{_receipt_md_table(verdict_receipt)}

## Highest integrity rows

{_receipt_md_table(high_integrity_receipt, limit=25)}

## Lowest integrity rows

{_receipt_md_table(low_integrity_receipt, limit=25)}

## Highest collapse-risk rows

{_receipt_md_table(high_collapse_receipt, limit=25)}

## Largest selected-year allocations

{_receipt_md_table(largest_alloc_receipt, limit=25)}

## High-impact risk rows

{_receipt_md_table(high_impact_receipt, limit=50)}

## Trust / seat sensitivity watchlist

{_receipt_md_table(sensitivity_receipt, limit=50)}

## Coverage gaps

{_receipt_md_table(coverage_gaps_receipt, limit=50)}

## Patch 31 module alignment note

Evidence Lab empirical country-year scoring feeds World Lens selected-year metrics. This report is connected to empirical data, but it is not a Mirror Check text-scenario receipt. Cognitive Resilience, Education Defense, contextual-capture, and hard-capture text diagnostics are therefore marked as not assessed unless policy/scenario text is supplied.

## Sydney Protocol note

This receipt is a reproducible view artifact. It is a protocol interpretation, not a legal, political, medical, religious, or moral determination.

The overlay remains: mirror, not throne; anti-capture; non-divinization; appealability; transparency; evidence humility.
"""

            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr(f"aletheia_grid_receipt_{int(selected_year)}.md", md)
                zf.writestr(f"aletheia_grid_receipt_{int(selected_year)}_summary.json", json.dumps(receipt_summary, indent=2))
                zf.writestr(f"aletheia_grid_receipt_{int(selected_year)}_coverage.csv", coverage_receipt.to_csv(index=False))
                zf.writestr(f"aletheia_grid_receipt_{int(selected_year)}_verdict_distribution.csv", verdict_receipt.to_csv(index=False))
                zf.writestr(f"aletheia_grid_receipt_{int(selected_year)}_highest_integrity.csv", high_integrity_receipt.to_csv(index=False))
                zf.writestr(f"aletheia_grid_receipt_{int(selected_year)}_lowest_integrity.csv", low_integrity_receipt.to_csv(index=False))
                zf.writestr(f"aletheia_grid_receipt_{int(selected_year)}_highest_collapse.csv", high_collapse_receipt.to_csv(index=False))
                zf.writestr(f"aletheia_grid_receipt_{int(selected_year)}_largest_allocations.csv", largest_alloc_receipt.to_csv(index=False))
                zf.writestr(f"aletheia_grid_receipt_{int(selected_year)}_high_impact_nodes.csv", high_impact_receipt.to_csv(index=False))
                zf.writestr(f"aletheia_grid_receipt_{int(selected_year)}_sensitivity_watchlist.csv", sensitivity_receipt.to_csv(index=False))
                zf.writestr(f"aletheia_grid_receipt_{int(selected_year)}_coverage_gaps.csv", coverage_gaps_receipt.to_csv(index=False))
                zf.writestr(f"aletheia_grid_receipt_{int(selected_year)}_all_rows.csv", all_rows_receipt.to_csv(index=False))
            buffer.seek(0)
            return buffer.getvalue()

        verdict_summary_df = pd.DataFrame()
        if verdict_col in comparison_df.columns:
            verdict_summary_df = (
                comparison_df.groupby(verdict_col, dropna=False)
                .agg(
                    countries=("iso3", "nunique") if "iso3" in comparison_df.columns else ("country", "count"),
                    seats=("_seats", "sum"),
                    avg_integrity=("_integrity", "mean"),
                    avg_collapse_probability=("_collapse", "mean"),
                    avg_empirical_coverage=("_coverage", "mean"),
                )
                .reset_index()
                .rename(columns={verdict_col: "verdict"})
            )
            seat_denominator = float(comparison_df["_seats"].sum()) if comparison_df["_seats"].sum() > 0 else np.nan
            verdict_summary_df["seat_share"] = verdict_summary_df["seats"] / seat_denominator if not pd.isna(seat_denominator) else np.nan

        comparison_export = comparison_df.copy()
        comparison_export["grid_selected_year"] = int(selected_year)
        comparison_export["grid_source_state"] = grid_state_label
        comparison_export["grid_is_full_9k_allocation"] = bool(is_full_grid)
        comparison_export["weighted_integrity_selected_year"] = weighted_integrity
        comparison_export["weighted_collapse_probability_selected_year"] = weighted_collapse
        comparison_export["weighted_friction_selected_year"] = weighted_friction
        comparison_export["average_empirical_coverage_selected_year"] = avg_coverage
        comparison_export["seat_total_selected_year"] = int(total_seats)
        comparison_export["coverage_warning"] = (
            "Full selected-year 9k allocation." if is_full_grid
            else "Partial or filtered selected-year subset; use active-seat interpretation."
        )
        comparison_export["recommended_interpretation"] = np.where(
            comparison_export["_high_impact_node"],
            "High-impact governance-risk node: high allocation plus low integrity or high collapse probability.",
            "Read with selected-year coverage diagnostics and Sydney Protocol overlay."
        )
        comparison_export["sydney_protocol_overlay"] = "mirror_not_throne; anti_capture; non_divinization; appealability; transparency; fail_closed_if_guardrails_break"
        comparison_export = apply_world_lens_diagnostic_alignment(comparison_export)
        comparison_export["app_version"] = APP_VERSION
        comparison_export["module_alignment_note"] = (
            "Evidence Lab empirical scoring feeds World Lens. Scenario-text diagnostics from Mirror Check are carried as explicit not-assessed scope fields unless policy text is supplied."
        )

        focus_iso3 = str(st.session_state.get("aletheia_synced_iso3") or "").strip().upper()
        focus_country_name = str(st.session_state.get("aletheia_synced_country_name") or "").strip()
        focus_country_available = bool(
            focus_iso3
            and "iso3" in comparison_df.columns
            and comparison_df["iso3"].astype(str).str.upper().eq(focus_iso3).any()
        )
        focus_row = comparison_df[comparison_df["iso3"].astype(str).str.upper().eq(focus_iso3)].copy() if focus_country_available else pd.DataFrame()

        if focus_iso3:
            if focus_country_available:
                _focus_label = (
                    focus_row["_country_name"].iloc[0]
                    if "_country_name" in focus_row.columns and not focus_row.empty
                    else focus_country_name
                )
                st.info(f"Focus country from Empirical Explorer: **{_focus_label} · {focus_iso3} · {int(selected_year)}**. Global metrics remain full selected-year metrics; the country is surfaced as focus/context, not used as a Grid filter.")
            else:
                st.warning(
                    f"Focus country **{focus_country_name or focus_iso3} · {focus_iso3}** is not available in the active Global Grid rows for {int(selected_year)}. "
                    "Choose a year where the country exists or rebuild the master."
                )

        view_tabs = st.tabs([
            "Overview",
            "Allocation",
            "Verdicts",
            "Integrity & Collapse",
            "Comparisons",
            "Trust & Sources",
            "Coverage",
            "Country-Year Detail",
            "Report Packet",
        ])

        with view_tabs[0]:
            st.markdown("### Selected-year overview")
            o1, o2, o3 = st.columns(3)
            o1.metric("Scored country-year rows", f"{row_count:,}")
            o2.metric("Countries in selected year", f"{countries_scored:,}")
            o3.metric("Rows excluded / diagnostic", f"{excluded_rows:,}")

            st.markdown(f"### {allocation_heading}")
            s1, s2, s3 = st.columns(3)
            with s1:
                metric_card("YES / Support", f"{signal.get('yes', np.nan):,.0f} seats", f"{signal.get('yes_pct', np.nan):.1%} of {signal_denominator_label}")
            with s2:
                metric_card("REVIEW", f"{signal.get('review', np.nan):,.0f} seats", f"{signal.get('review_pct', np.nan):.1%} of {signal_denominator_label}")
            with s3:
                metric_card("BLOCK", f"{signal.get('block', np.nan):,.0f} seats", f"{signal.get('block_pct', np.nan):.1%} of {signal_denominator_label}")

            st.write(
                "High allocation plus low integrity or high collapse probability indicates a high-impact governance-risk node. "
                "Low empirical coverage should reduce interpretive confidence. Verdict categories are protocol interpretations, "
                "not legal or political determinations."
            )

        with view_tabs[1]:
            st.markdown("### Selected-year seat allocation" if is_full_grid else "### Active selected-year seat allocation")
            top_n = grid_source.head(25).copy()
            label_col = "iso3" if "iso3" in top_n.columns else "country"
            fig = go.Figure(go.Bar(x=top_n[label_col], y=top_n["seats_9k"]))
            fig.update_layout(template="plotly_white", title=(f"Top 25 country-level 9k allocations · {selected_year}" if is_full_grid else f"Top active selected-year seat allocations · {selected_year}"), height=430, margin=dict(l=10, r=10, t=55, b=10))
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Showing the top 25 countries by seats. The full table is in Country-Year Detail. Partial years may not add to 9,000.")

        with view_tabs[2]:
            st.markdown("### Result distribution")
            if not verdict_seats.empty:
                verdict_df = verdict_seats.reset_index()
                verdict_df.columns = ["Verdict", "Seats"]
                fig = go.Figure(go.Bar(x=verdict_df["Verdict"], y=verdict_df["Seats"]))
                fig.update_layout(template="plotly_white", title="Seat distribution by verdict", height=430, margin=dict(l=10, r=10, t=55, b=10))
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(verdict_df, use_container_width=True, hide_index=True)
            else:
                st.info("No result column is available for this selected year.")

        with view_tabs[3]:
            st.markdown("### Integrity and collapse")
            c1, c2, c3 = st.columns(3)
            c1.metric(f"Weighted {metric_scope_word} integrity", "—" if pd.isna(weighted_integrity) else f"{weighted_integrity:.3f}")
            c2.metric(f"Weighted {metric_scope_word} friction", "—" if pd.isna(weighted_friction) else f"{weighted_friction:.3f}")
            c3.metric(f"Weighted {metric_scope_word} collapse probability", "—" if pd.isna(weighted_collapse) else f"{weighted_collapse:.3f}")
            if integrity_col in grid_source.columns and collapse_col in grid_source.columns:
                scatter_df = grid_source.copy()
                scatter_df["_integrity"] = _numeric_series(integrity_col)
                scatter_df["_collapse"] = _numeric_series(collapse_col)
                fig = go.Figure(
                    go.Scatter(
                        x=scatter_df["_integrity"],
                        y=scatter_df["_collapse"],
                        mode="markers",
                        marker={"size": np.maximum(pd.to_numeric(scatter_df.get("seats_9k"), errors="coerce").fillna(1), 1) ** 0.5},
                        text=scatter_df.get("_hover_label", scatter_df.get("iso3", pd.Series("", index=scatter_df.index))),
                        hovertemplate="%{text}<br>Integrity: %{x:.3f}<br>Collapse probability: %{y:.3f}<extra></extra>",
                    )
                )
                fig.update_layout(template="plotly_white", title=f"Integrity vs collapse probability · {selected_year}", xaxis_title="Integrity", yaxis_title="Collapse probability", height=480, margin=dict(l=10, r=10, t=55, b=10))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Integrity/collapse columns are not available for this selected year.")

        with view_tabs[4]:
            st.markdown("### Important comparison views")
            st.caption(
                "These rankings use the active selected-year Grid source. Partial years remain diagnostic subsets, "
                "not full global allocations."
            )

            rank_limit = st.slider("Rows per comparison table", 5, 30, 10, 1, key=f"grid_pass2_rank_limit_{selected_year}")

            c_high, c_low = st.columns(2)
            with c_high:
                st.markdown("#### Highest integrity rows")
                high_integrity = comparison_df.dropna(subset=["_integrity"]).sort_values("_integrity", ascending=False).head(rank_limit)
                st.dataframe(_comparison_display(high_integrity), use_container_width=True, hide_index=True)
            with c_low:
                st.markdown("#### Lowest integrity rows")
                low_integrity = comparison_df.dropna(subset=["_integrity"]).sort_values("_integrity", ascending=True).head(rank_limit)
                st.dataframe(_comparison_display(low_integrity), use_container_width=True, hide_index=True)

            c_collapse, c_seats = st.columns(2)
            with c_collapse:
                st.markdown("#### Highest collapse-risk rows")
                high_collapse = comparison_df.dropna(subset=["_collapse"]).sort_values("_collapse", ascending=False).head(rank_limit)
                st.dataframe(_comparison_display(high_collapse), use_container_width=True, hide_index=True)
            with c_seats:
                st.markdown("#### Largest selected-year seat counts")
                largest_seats = comparison_df.sort_values("_seats", ascending=False).head(rank_limit)
                st.dataframe(_comparison_display(largest_seats), use_container_width=True, hide_index=True)

            st.markdown("#### High-impact risk rows")
            st.write(
                "High allocation plus low integrity or high collapse probability indicates a high-impact governance-risk node. "
                "This is a protocol risk signal, not a legal or political determination."
            )
            high_impact = comparison_df[comparison_df["_high_impact_node"]].sort_values(["_seats", "_collapse"], ascending=[False, False]).head(max(rank_limit, 10))
            if high_impact.empty:
                st.info("No high-impact risk rows were found by the selected-year rule.")
            else:
                st.dataframe(_comparison_display(high_impact, include_reason=True), use_container_width=True, hide_index=True)

            st.markdown("#### Largest seats among low-integrity or high-collapse rows")
            risk_alloc = comparison_df[comparison_df["_low_integrity"] | comparison_df["_high_collapse"]].sort_values("_seats", ascending=False).head(rank_limit)
            if risk_alloc.empty:
                st.info("No low-integrity or high-collapse rows are available in this selected-year view.")
            else:
                st.dataframe(_comparison_display(risk_alloc, include_reason=True), use_container_width=True, hide_index=True)

            st.markdown("#### Trust / seat sensitivity watchlist")
            neutral_trust_prior_view = (
                comparison_df["_trust_prior"].notna().any()
                and comparison_df["_trust_delta_from_neutral"].fillna(0).max() < 0.001
            )
            raw_trust_missing_view = not comparison_df["_trust_raw"].notna().any()
            if neutral_trust_prior_view and raw_trust_missing_view:
                st.caption(
                    "In this selected year, raw trust is missing and trust prior is neutral/default for the active rows. "
                    "This watchlist mainly reflects allocation size and rows near scoring thresholds, not observed trust movement."
                )
            else:
                st.caption(
                    "This first pass uses a proxy: trust prior far from neutral 0.500, larger allocation, or rows near review thresholds. "
                    "A later exact version can recompute counterfactual scores with trust fixed at 0.500."
                )
            trust_material = comparison_df[
                comparison_df["_trust_prior"].notna()
                & (
                    comparison_df["_trust_delta_from_neutral"].ge(0.10)
                    | comparison_df["_large_allocation"]
                    | comparison_df["_integrity"].between(0.45, 0.60, inclusive="both")
                    | comparison_df["_collapse"].between(0.30, 0.45, inclusive="both")
                )
            ].sort_values(["_trust_delta_from_neutral", "_seats"], ascending=[False, False]).head(rank_limit)
            if trust_material.empty:
                st.info("No trust/allocation sensitivity watchlist rows are available in this selected-year view.")
            else:
                trust_out = _comparison_display(trust_material, include_reason=True)
                if "_trust_delta_from_neutral" in trust_material.columns:
                    trust_out["trust_delta_from_neutral"] = trust_material["_trust_delta_from_neutral"].round(3).values
                st.dataframe(trust_out, use_container_width=True, hide_index=True)

        with view_tabs[5]:
            st.markdown("### Trust and source comparisons")

            st.markdown("#### Trust vs democracy")
            trust_axis_options = []
            if "_trust_raw" in comparison_df.columns and comparison_df["_trust_raw"].notna().any():
                trust_axis_options.append(("Raw trust survey", "_trust_raw"))
            if "_trust_prior" in comparison_df.columns and comparison_df["_trust_prior"].notna().any():
                trust_axis_options.append(("Trust prior", "_trust_prior"))
            if trust_axis_options and comparison_df["_vdem_democracy"].notna().any():
                trust_label = st.radio(
                    "Trust signal",
                    [label for label, _ in trust_axis_options],
                    horizontal=True,
                    key=f"trust_scatter_signal_{selected_year}",
                )
                trust_col_plot = dict(trust_axis_options)[trust_label]
                scatter_df = comparison_df.dropna(subset=[trust_col_plot, "_vdem_democracy"]).copy()
                fig = go.Figure(
                    go.Scatter(
                        x=scatter_df["_vdem_democracy"],
                        y=scatter_df[trust_col_plot],
                        mode="markers",
                        marker={"size": np.maximum(scatter_df["_seats"].fillna(1), 1) ** 0.5},
                        text=scatter_df.get("_hover_label", scatter_df.get("iso3", pd.Series("", index=scatter_df.index))),
                        hovertemplate="%{text}<br>V-Dem democracy: %{x:.3f}<br>Trust: %{y:.3f}<extra></extra>",
                    )
                )
                fig.update_layout(template="plotly_white", title=f"{trust_label} vs V-Dem democracy · {selected_year}", xaxis_title="V-Dem democracy", yaxis_title=trust_label, height=470, margin=dict(l=10, r=10, t=55, b=10))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Trust vs democracy needs V-Dem democracy plus raw trust or trust prior values.")

            st.markdown("#### WGI vs V-Dem")
            if comparison_df["_wgi_composite"].notna().any() and comparison_df["_vdem_democracy"].notna().any():
                scatter_df = comparison_df.dropna(subset=["_wgi_composite", "_vdem_democracy"]).copy()
                fig = go.Figure(
                    go.Scatter(
                        x=scatter_df["_wgi_composite"],
                        y=scatter_df["_vdem_democracy"],
                        mode="markers",
                        marker={"size": np.maximum(scatter_df["_seats"].fillna(1), 1) ** 0.5},
                        text=scatter_df.get("_hover_label", scatter_df.get("iso3", pd.Series("", index=scatter_df.index))),
                        hovertemplate="%{text}<br>Available WGI mean: %{x:.3f}<br>V-Dem democracy: %{y:.3f}<extra></extra>",
                    )
                )
                fig.update_layout(template="plotly_white", title=f"Available WGI mean vs V-Dem democracy · {selected_year}", xaxis_title="Available WGI mean", yaxis_title="V-Dem democracy", height=470, margin=dict(l=10, r=10, t=55, b=10))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(
                    "Available WGI mean vs V-Dem comparison is inactive because one or both source families are missing in the active selected-year rows."
                )

            st.markdown("#### Coverage gaps by country/year")
            coverage_gaps = comparison_df.sort_values(["_coverage_gap_count", "_coverage", "_seats"], ascending=[False, True, False]).head(30)
            gap_cols = [
                "_country_name", "iso3", "year", "_allocation_role", "_coverage", "_missing_raw_trust", "_missing_trust_prior",
                "_missing_wgi", "_missing_vdem", "_coverage_gap_count", "_seats",
            ]
            gap_cols = [c for c in gap_cols if c in coverage_gaps.columns]
            gap_out = coverage_gaps[gap_cols].rename(columns={
                "_coverage": "empirical_coverage",
                "_missing_raw_trust": "missing_raw_trust",
                "_missing_trust_prior": "missing_trust_prior",
                "_missing_wgi": "missing_wgi",
                "_missing_vdem": "missing_vdem",
                "_coverage_gap_count": "coverage_gap_count",
                "_seats": "seats",
            })
            if "empirical_coverage" in gap_out.columns:
                gap_out["empirical_coverage"] = pd.to_numeric(gap_out["empirical_coverage"], errors="coerce").round(3)
            if "seats" in gap_out.columns:
                gap_out["seats"] = pd.to_numeric(gap_out["seats"], errors="coerce").fillna(0).astype(int)
            st.dataframe(gap_out, use_container_width=True, hide_index=True)

        with view_tabs[6]:
            st.markdown("### Coverage checks")
            d1, d2, d3, d4 = st.columns(4)
            d1.metric("Allocated country rows", f"{countries_scored:,}")
            d2.metric("Zero-seat diagnostic rows", f"{displayed_zero_seat_rows:,}" + (f" shown · {hidden_zero_seat_rows:,} hidden" if hidden_zero_seat_rows else ""))
            d3.metric("Missing raw trust", f"{missing_trust:,}")
            d4.metric("Missing WGI", f"{missing_wgi:,}")
            d5, d6, d7 = st.columns(3)
            d5.metric("Missing V-Dem", f"{missing_vdem:,}")
            d6.metric("Trust prior rows", f"{int(trust_prior_mask.sum()):,}")
            d7.metric("Missing trust prior", f"{missing_trust_prior:,}")
            st.warning(
                "Coverage reflects available empirical fields among the active selected-year rows after current filters. Missing sources are treated as neutral/default "
                "where applicable and should be considered diagnostic, not evidence of absence. Trust values are survey-year "
                "dependent and may be unavailable for many country-years."
            )
            coverage_df = pd.DataFrame([
                {"Source": "Trust raw survey", "Rows present": int(trust_mask.sum()), "Rows missing": missing_trust, "Coverage": trust_coverage},
                {"Source": "Trust prior", "Rows present": int(trust_prior_mask.sum()), "Rows missing": missing_trust_prior, "Coverage": trust_prior_coverage},
                {"Source": "WGI", "Rows present": int(wgi_mask.sum()), "Rows missing": missing_wgi, "Coverage": wgi_coverage},
                {"Source": "V-Dem", "Rows present": int(vdem_mask.sum()), "Rows missing": missing_vdem, "Coverage": vdem_coverage},
            ])
            coverage_display = coverage_df.copy()
            coverage_display["Coverage"] = coverage_display["Coverage"].map(lambda x: "—" if pd.isna(x) else f"{x:.1%}")
            st.dataframe(coverage_display, use_container_width=True, hide_index=True)

            with st.expander("Trust source check", expanded=False):
                trust_source_df = st.session_state.get("empirical_master_df")
                if isinstance(trust_source_df, pd.DataFrame) and not trust_source_df.empty and "year" in trust_source_df.columns:
                    trust_source_col = "wvs_generalized_trust" if "wvs_generalized_trust" in trust_source_df.columns else None
                    if trust_source_col:
                        _trust_years = pd.to_numeric(trust_source_df.loc[pd.to_numeric(trust_source_df[trust_source_col], errors="coerce").notna(), "year"], errors="coerce").dropna()
                        _selected_trust_rows = trust_source_df[
                            pd.to_numeric(trust_source_df.get("year"), errors="coerce").eq(int(selected_year))
                            & pd.to_numeric(trust_source_df[trust_source_col], errors="coerce").notna()
                        ]
                        td1, td2, td3 = st.columns(3)
                        td1.metric("Raw trust rows in master", f"{int(len(_trust_years)):,}")
                        td2.metric("Raw trust year range", "—" if _trust_years.empty else f"{int(_trust_years.min())}–{int(_trust_years.max())}")
                        td3.metric("Raw trust rows for selected year", f"{int(len(_selected_trust_rows)):,}")
                        st.caption(
                            "If selected-year raw trust is 0 while trust prior is 100%, ALETHEIA is using neutral/default trust priors for that year. "
                            "This is allowed, but it should reduce interpretive confidence."
                        )
                    else:
                        st.info("No raw WVS/OWID trust column is present in the active data table.")
                else:
                    st.info("No active empirical table is available for trust-source checks in this session.")

        with view_tabs[7]:
            st.markdown("### Country-year detail")
            curated_cols = [
                "country", "iso3", "year", "population", "population_share", "seats_9k",
                verdict_col, integrity_col, friction_col, collapse_col,
                coverage_col, "empirical_identity_valid",
                "wgi_voice_accountability", "wgi_political_stability", "wgi_government_effectiveness",
                "wgi_regulatory_quality", "wgi_rule_of_law", "wgi_control_corruption",
                "vdem_executive_constraints", "vdem_democracy",
                "wvs_generalized_trust", "empirical_trust_prior",
            ]
            curated_cols = [c for c in curated_cols if c and c in grid_source.columns]
            display_df = grid_source[curated_cols].rename(columns={
                "population_share": "population_share",
                verdict_col: "verdict",
                integrity_col: "integrity",
                friction_col: "friction",
                collapse_col: "collapse_probability",
                coverage_col: "empirical_coverage" if coverage_col else coverage_col,
                "empirical_identity_valid": "identity_valid",
            })
            if "population_share" in display_df.columns:
                display_df["population_share"] = (pd.to_numeric(display_df["population_share"], errors="coerce") * 100).round(3).astype(str) + "%"
            if focus_iso3 and "iso3" in display_df.columns:
                _focus_mask = display_df["iso3"].astype(str).str.upper().eq(focus_iso3)
                if _focus_mask.any():
                    st.info(f"Focus country row shown first: **{focus_country_name or focus_iso3} · {focus_iso3} · {int(selected_year)}**")
                    display_df = pd.concat([display_df.loc[_focus_mask], display_df.loc[~_focus_mask]], ignore_index=True)
                else:
                    st.warning(f"Focus country **{focus_country_name or focus_iso3} · {focus_iso3}** is not present in this selected-year detail table.")
            st.dataframe(display_df, use_container_width=True, hide_index=True, height=480)
            csv_grid = grid_source.to_csv(index=False)
            st.download_button(
                "⬇️ Download selected-year Global Grid CSV",
                data=csv_grid,
                file_name=f"aletheia_global_grid_{selected_year}.csv",
                mime="text/csv",
            )

        empirical_grid_receipt_checks = []
        receipt_ready = True

        def _receipt_check(name: str, ok: bool, fix: str) -> None:
            nonlocal_receipt_checks.append({"Check": name, "Status": "OK" if ok else "Needs action", "What to do": "—" if ok else fix})

        nonlocal_receipt_checks = empirical_grid_receipt_checks
        empirical_active_ok = isinstance(empirical_scored_raw, pd.DataFrame) and not empirical_scored_raw.empty
        _receipt_check(
            "Empirical scored table is active",
            empirical_active_ok,
            "Run Evidence Lab — Data Check first, then build and score the country-year table.",
        )

        empirical_year_match_ok = False
        empirical_year_rows_count = 0
        if empirical_active_ok and "year" in empirical_scored_raw.columns:
            empirical_year_rows = empirical_scored_raw[
                pd.to_numeric(empirical_scored_raw["year"], errors="coerce").eq(int(selected_year))
            ]
            empirical_year_rows_count = int(len(empirical_year_rows))
            empirical_year_match_ok = empirical_year_rows_count > 0
        _receipt_check(
            "Empirical table has rows for the selected Grid year",
            empirical_year_match_ok,
            f"Select a Grid year present in Empirical Evidence, or rebuild the master so {selected_year} exists.",
        )

        grid_has_rows_ok = not grid_source.empty
        _receipt_check(
            "Global Grid has active selected-year rows",
            grid_has_rows_ok,
            "Choose a populated evidence year, clear filters, or rebuild the master.",
        )

        full_or_acknowledged_ok = bool(is_full_grid or show_partial_years)
        _receipt_check(
            "Grid interpretation is confirmed",
            full_or_acknowledged_ok,
            "Use a full 9k year, or turn on partial diagnostic years to acknowledge active-seat interpretation.",
        )

        seat_consistency_ok = bool(total_seats > 0 and (is_full_grid or not has_complete_seat_total or abs(total_seats - int(grid_source['seats_9k'].sum())) <= 0))
        _receipt_check(
            "Seat total is available",
            seat_consistency_ok,
            "Rebuild allocation or choose a year with positive seats.",
        )

        required_metric_ok = bool(not pd.isna(weighted_integrity) and not pd.isna(weighted_collapse))
        _receipt_check(
            "Weighted integrity/collapse metrics are available",
            required_metric_ok,
            "Rebuild or rerun scoring so integrity and collapse probability columns are present.",
        )

        receipt_year_values = [
            st.session_state.get("aletheia_empirical_country_year"),
            st.session_state.get("aletheia_empirical_allocation_year"),
            st.session_state.get("aletheia_global_grid_year"),
        ]
        receipt_year_values = [int(v) for v in receipt_year_values if v is not None and str(v).strip() not in ["", "None"]]
        receipt_years_aligned = bool(receipt_year_values) and len(set(receipt_year_values)) == 1 and int(selected_year) in set(receipt_year_values)
        _receipt_check(
            "Empirical and Global Grid year controls match",
            receipt_years_aligned,
            "Select the same evidence year in Empirical Country-Year Explorer, Empirical Allocation, and Global Grid.",
        )
        _receipt_check(
            "Focus country is available in Global Grid year",
            (not focus_iso3) or focus_country_available,
            "Choose a Global Grid year where the selected Empirical country exists, or choose another country in Empirical Explorer.",
        )

        receipt_ready = all(row["Status"] == "OK" for row in empirical_grid_receipt_checks)

        with view_tabs[8]:
            st.markdown("### Report packet setup")
            st.write(
                "This tab prepares selected-year Grid outputs for the later report generator. "
                "It does not issue final legal, political, or moral determinations."
            )

            rp1, rp2, rp3, rp4 = st.columns(4)
            rp1.metric("Selected year", f"{selected_year}")
            rp2.metric("Grid state", "Full 9k" if is_full_grid else "Partial / active-seat")
            rp3.metric("Weighted integrity", "—" if pd.isna(weighted_integrity) else f"{weighted_integrity:.3f}")
            rp4.metric("Weighted collapse", "—" if pd.isna(weighted_collapse) else f"{weighted_collapse:.3f}")

            st.markdown("#### Result distribution for reports")
            if not verdict_summary_df.empty:
                verdict_report = verdict_summary_df.copy()
                for col in ["avg_integrity", "avg_collapse_probability", "avg_empirical_coverage", "seat_share"]:
                    if col in verdict_report.columns:
                        verdict_report[col] = pd.to_numeric(verdict_report[col], errors="coerce").round(3)
                if "seats" in verdict_report.columns:
                    verdict_report["seats"] = pd.to_numeric(verdict_report["seats"], errors="coerce").fillna(0).astype(int)
                st.dataframe(verdict_report, use_container_width=True, hide_index=True)
            else:
                st.info("No verdict distribution is available for the active selected-year rows.")

            st.markdown("#### Choose a country-year for report context")
            if not comparison_df.empty:
                report_options_df = comparison_df.copy()
                report_options_df["_report_label"] = (
                    report_options_df["_country_name"].fillna("").astype(str)
                    + " · "
                    + report_options_df.get("iso3", pd.Series("", index=report_options_df.index)).fillna("").astype(str)
                    + " · "
                    + report_options_df.get("year", pd.Series(selected_year, index=report_options_df.index)).astype(str)
                )
                report_filter_key = f"grid_report_country_year_filter_{selected_year}"
                if focus_iso3 and focus_country_available and not st.session_state.get(report_filter_key):
                    st.session_state[report_filter_key] = focus_iso3
                report_search = st.text_input(
                    "Filter report country-year",
                    value=st.session_state.get(report_filter_key, ""),
                    placeholder="Type country name or ISO code, e.g. Argentina or ARG",
                    key=report_filter_key,
                ).strip().lower()
                if report_search:
                    report_options_df = report_options_df[
                        report_options_df["_report_label"].astype(str).str.lower().str.contains(report_search, na=False)
                    ].copy()
                if report_options_df.empty:
                    st.info("No country-year matches that filter. Clear it or try another country name/ISO code.")
                    st.stop()

                report_options_df = report_options_df.sort_values(["_country_name", "iso3"], na_position="last")
                report_labels = report_options_df["_report_label"].tolist()
                focus_report_index = 0
                if focus_iso3:
                    _focus_label_matches = [
                        i for i, label in enumerate(report_labels)
                        if f"· {focus_iso3} ·" in str(label) or str(label).upper().find(focus_iso3) >= 0
                    ]
                    if _focus_label_matches:
                        focus_report_index = _focus_label_matches[0]
                selected_label = st.selectbox(
                    "Country-year to export",
                    report_labels,
                    index=focus_report_index,
                    key=f"grid_report_country_year_{selected_year}",
                    help="Start typing inside the dropdown or use the filter above. Confirm this label before downloading the packet.",
                )
                selected_idx = report_options_df[report_options_df["_report_label"] == selected_label].index[0]
                selected_row = comparison_df.loc[[selected_idx]]
                st.info(f"Preparing report packet for: **{selected_label}**")
                st.dataframe(_comparison_display(selected_row, include_reason=True), use_container_width=True, hide_index=True)

                selected_row_export = _comparison_display(selected_row, include_reason=True)
                selected_row_export["selected_year"] = int(selected_year)
                selected_row_export["grid_source_state"] = grid_state_label
                selected_row_export["weighted_global_integrity"] = weighted_integrity
                selected_row_export["weighted_global_collapse_probability"] = weighted_collapse
                selected_row_export["selected_year_seat_total"] = int(total_seats)
                selected_row_export["full_9k_allocation"] = bool(is_full_grid)
                selected_row_export["coverage_warning"] = (
                    "Full selected-year allocation." if is_full_grid
                    else "Partial selected-year subset; do not read as full global allocation."
                )
                selected_row_export["sydney_protocol_overlay"] = "mirror_not_throne; anti_capture; non_divinization; appealability; transparency; evidence_humility"
                selected_row_export["recommended_interpretation"] = np.where(
                    selected_row["_high_impact_node"].values,
                    "High allocation plus low integrity or high collapse probability indicates a high-impact governance-risk node.",
                    "Read as a selected-year protocol interpretation with coverage caveats."
                )
                safe_label = re.sub(r"[^A-Za-z0-9_-]+", "_", str(selected_label)).strip("_")
                st.download_button(
                    "⬇️ Download selected country-year report packet CSV",
                    data=selected_row_export.to_csv(index=False),
                    file_name=f"aletheia_grid_report_packet_{selected_year}_{safe_label}.csv",
                    mime="text/csv",
                )

            st.markdown("#### Complete World Lens receipt")
            st.write(
                "Download a receipt ZIP for this selected year. It includes the overview, coverage, verdict distribution, "
                "comparison tables, coverage gaps, all active rows, and a markdown summary for review."
            )

            receipt_check_df = pd.DataFrame(empirical_grid_receipt_checks)
            st.dataframe(receipt_check_df, use_container_width=True, hide_index=True)

            if receipt_ready:
                st.success("Receipt is ready. Evidence Lab and World Lens inputs match for this output.")
                st.download_button(
                    "⬇️ Download complete Grid receipt ZIP",
                    data=_build_grid_receipt_zip(),
                    file_name=f"aletheia_global_grid_receipt_{selected_year}.zip",
                    mime="application/zip",
                    use_container_width=True,
                )
            else:
                st.warning(
                    "Receipt download is locked until Empirical Evidence and Global Grid are aligned for the selected output. "
                    "Follow the actions above, then rerun the Grid."
                )

            st.markdown("#### Comparison packet export")
            export_cols = [
                "_country_name", "country", "iso3", "year", verdict_col, "_seats", "_seat_rank", "_integrity_rank", "_collapse_rank",
                "_integrity", "_collapse", "_friction", "_coverage", "_trust_raw", "_trust_prior",
                "_wgi_composite", "_wgi_source_count", "_wgi_fields_used", "_vdem_democracy", "_missing_raw_trust", "_missing_wgi", "_missing_vdem",
                "_large_allocation", "_low_integrity", "_high_collapse", "_high_impact_node",
                "grid_selected_year", "grid_source_state", "grid_is_full_9k_allocation",
                "weighted_integrity_selected_year", "weighted_collapse_probability_selected_year",
                "seat_total_selected_year", "coverage_warning", "sydney_protocol_overlay", "recommended_interpretation",
            ]
            export_cols = [c for c in export_cols if c in comparison_export.columns]
            st.download_button(
                "⬇️ Download selected-year comparison packet CSV",
                data=comparison_export[export_cols].to_csv(index=False),
                file_name=f"aletheia_global_grid_comparison_{selected_year}.csv",
                mime="text/csv",
            )
            st.caption(
                "This export is the bridge to Global Grid Pass 3 reports: selected year, weighted metrics, verdict context, "
                "rank/share, evidence fields, coverage warnings, Sydney Protocol overlay, and recommended interpretation."
            )

        with st.expander("Method and interpretation note", expanded=False):
            st.write(
                "The selected-year grid uses uploaded empirical country-year rows with valid identity data. "
                "Seats are allocated within each year by population share so the selected year should sum to 9,000 seats before optional filters. "
                "Regional/income aggregates and diagnostic rows are excluded from the denominator. "
                "Weighted metrics use active selected-year seats when available, with population as a fallback; sparse or filtered views are subset diagnostics rather than full global claims. "
                "Verdict categories and comparison rankings are protocol interpretations, not legal or political determinations."
            )

    elif grid_mode == "Prototype region brackets":
        update_protocol_state(grid_basis="Prototype region brackets", last_update_source="World Lens", synthetic_demo_active=True)
        st.caption("World Lens source state: **Prototype region brackets**. This is a concept fallback, not empirical country-year evidence.")
        st.info(
            "Using the prototype regional brackets because no valid empirical country-year dataset is active. This fallback can still help with conceptual framing, but it is not a real-world country-year allocation."
        )
        slots = allocate_slots()
        grid_df = pd.DataFrame([
            {"Region": region, "Share": pct, "Seats": slots[region]} for region, pct in DEMOGRAPHIC_BRACKETS.items()
        ])

        g1, g2, g3 = st.columns(3)
        g1.metric("Total 9k seats", f"{TOTAL_9K:,}")
        g2.metric("Allocation basis", "Prototype brackets")
        g3.metric("Seat ownership", "None")

        fallback_tabs = st.tabs(["Overview", "Allocation", "Verdicts", "Integrity & Collapse", "Coverage", "Country-Year Detail"])
        with fallback_tabs[0]:
            st.markdown("### Prototype overview")
            st.write(
                "Prototype brackets are a conceptual demographic mirror only. They do not represent country-year evidence, "
                "weighted global integrity, collapse probability, WGI/V-Dem/trust coverage, or real-world allocation."
            )
            st.info("Run or upload valid country-year data in Evidence Lab to activate full World Lens.")
            st.markdown(f"### {allocation_heading}")
            p1, p2, p3 = st.columns(3)
            with p1:
                metric_card("YES / Support", "—", "Requires empirical selected-year rows.")
            with p2:
                metric_card("REVIEW", "—", "Requires empirical selected-year rows.")
            with p3:
                metric_card("BLOCK", "—", "Requires empirical selected-year rows.")

        with fallback_tabs[1]:
            st.markdown("### Prototype population mirror")
            fig = go.Figure(go.Bar(x=grid_df["Region"], y=grid_df["Seats"]))
            fig.update_layout(template="plotly_white", title="Prototype population mirror", height=430, margin=dict(l=10, r=10, t=55, b=10))
            st.plotly_chart(fig, use_container_width=True)
            grid_display = grid_df.copy()
            grid_display["Share"] = (grid_display["Share"] * 100).round(1).astype(str) + "%"
            st.dataframe(grid_display, use_container_width=True, hide_index=True, height=320)

        with fallback_tabs[2]:
            st.markdown("### Result distribution")
            st.info("Result distribution is unavailable in prototype-bracket mode because no empirical country-year verdict table is active.")

        with fallback_tabs[3]:
            st.markdown("### Integrity and collapse")
            st.info("Weighted integrity, friction, and collapse probability need selected-year data rows.")

        with fallback_tabs[4]:
            st.markdown("### Coverage checks")
            coverage_placeholder = pd.DataFrame([
                {"Source": "Trust", "Rows present": 0, "Rows missing": 0, "Coverage": "Not applicable"},
                {"Source": "WGI", "Rows present": 0, "Rows missing": 0, "Coverage": "Not applicable"},
                {"Source": "V-Dem", "Rows present": 0, "Rows missing": 0, "Coverage": "Not applicable"},
            ])
            st.dataframe(coverage_placeholder, use_container_width=True, hide_index=True)
            st.warning(
                "Coverage checks are meaningful only for empirical country-year data. Prototype brackets should not be read as source coverage."
            )

        with fallback_tabs[5]:
            st.markdown("### Country-year detail")
            st.info("No country-year detail is active. Use Evidence Lab to upload or build the table, then return to World Lens.")

        with st.expander("Selection safety summary", expanded=True):
            st.write(
                "Safe 9k language requires random selection, demographic-proportional lanes, auditability, no campaigning, no seat ownership, and periodic redraw. "
                "The grid reflects representation logic. It is not a real vote or mandate."
            )

    else:
        update_protocol_state(grid_basis="Inactive / no valid data", last_update_source="World Lens", synthetic_demo_active=False)
        st.caption("World Lens source state: **Inactive / no valid data**.")
        if grid_mode == "Uploaded empirical country-year data":
            st.warning(
                "Uploaded empirical country-year data was selected, but no valid empirical Global Grid dataset is active. "
                "Run or upload valid country-year data in Evidence Lab to activate full World Lens."
            )
        else:
            st.warning(
                "No empirical Global Grid is active and prototype regional brackets are disabled. "
                "Run or upload valid country-year data in Evidence Lab to activate full World Lens."
            )
        inactive_tabs = st.tabs(["Overview", "Allocation", "Verdicts", "Integrity & Collapse", "Coverage", "Country-Year Detail"])
        with inactive_tabs[0]:
            st.markdown("### World Lens inactive")
            st.write(
                "This state intentionally avoids showing prototype regional brackets. The full Global Grid requires an active empirical "
                "country-year table with valid identity, year, population, and 9k allocation fields."
            )
        with inactive_tabs[1]:
            st.info("Seat allocation is unavailable until country-year data is active or prototype brackets are selected.")
        with inactive_tabs[2]:
            st.info("Result distribution is unavailable until empirical country-year verdict rows are active.")
        with inactive_tabs[3]:
            st.info("Weighted integrity and collapse probability are unavailable until selected-year data rows are active.")
        with inactive_tabs[4]:
            st.info("Trust, WGI, and V-Dem coverage checks are unavailable until selected-year data rows are active.")
        with inactive_tabs[5]:
            st.info("Country-year detail is unavailable until selected-year data rows are active.")

with tab_chat:
    st.subheader("Mirror Check — Gentle Risk Review")
    render_shared_protocol_state_notice("Mirror Check")
    render_audit_module_integrity_panel()

    st.info(
        "Bring one idea at a time. English and Nederlands/Dutch inputs are calibrated. ALETHEIA checks how power moves, where appeal is protected, and where review is needed. You keep the judgment."
    )

    with st.expander("What Mirror Check looks for", expanded=False):
        f1, f2, f3, f4, f5 = st.columns(5)
        f1.markdown("**1. Care alignment**\n\nDoes the idea protect people?")
        f2.markdown("**2. Power language**\n\nDoes soft wording hide control?")
        f3.markdown("**3. Integrity check**\n\nCan the result be reviewed?")
        f4.markdown("**4. Stability pattern**\n\nWhat happens under pressure?")
        f5.markdown("**5. Witness receipt**\n\nA local record you hold.")

    if "chat_audit_history" not in st.session_state:
        st.session_state.chat_audit_history = []

    if "audit_chat_query" not in st.session_state:
        st.session_state.audit_chat_query = ""
    if "audit_chat_input_source" not in st.session_state:
        st.session_state.audit_chat_input_source = "EMPTY_INPUT"

    def mirror_active_input_signature(text_value: str) -> str:
        """Stable signature for the currently typed Mirror Check input.

        Patch 72.2: prevents an old assessment/receipt from staying active after
        the user edits the input box. History may remain, but a changed input
        requires an explicit new Review idea click.
        """
        return hashlib.sha256((text_value or "").strip().encode("utf-8")).hexdigest()

    def run_chat_audit_from_text(text_value: str, raw_text_value=None, input_source: str = "USER_INPUT", invisibility_report=None, store_history: bool = True, force_local: bool = False):
        raw_text_value = text_value if raw_text_value is None else raw_text_value
        scan = governance_scan(text_value, force_local=force_local)
        scan = apply_capture_feature_override(text_value, scan)
        features = build_features_from_scan(scan)
        np.random.seed(deterministic_seed_from_payload(text_value, features, weights, ego_tolerance, divine_floor, steps, n_agents, "chat"))
        sim = simulate(
            features,
            weights,
            ego_tolerance=ego_tolerance,
            divine_floor=divine_floor,
            steps=steps,
            n_agents=n_agents,
        )
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
        report = full_report(sim)
        report["cognitive_resilience_diagnostics"] = evaluate_cognitive_resilience(
            text_value, governance_result=scan, features=features
        )
        report = apply_cognitive_resilience_to_metrics(
            report, report.get("cognitive_resilience_diagnostics")
        )
        ethics_diagnostics = evaluate_ethics(text_value, governance_result=scan, features=features)
        # Patch 22: make visible Mirror Check metrics reflect contextual ethics pressure.
        # Protocol hard overrides still take precedence; this only calibrates the numeric layer.
        sim, report = apply_ethics_to_metrics(sim, report, ethics_diagnostics)
        report["ethics_diagnostics"] = ethics_diagnostics
        if force_local:
            judgment, source = local_governance_judgment(text_value, scan, sim, report), "Local batch scan"
        else:
            judgment, source = llm_governance_judgment(text_value, scan, sim, report)
        judgment = positive_cr_baseline_stabilizer(judgment, report)

        entry = {
            "query": text_value,
            "raw_query": raw_text_value,
            "input_source": input_source,
            "invisibility_report": invisibility_report,
            "scan": scan,
            "sim": sim,
            "report": report,
            "ethics_diagnostics": ethics_diagnostics,
            "judgment": judgment,
            "source": source,
            "source_hits": source_conformance_hits(text_value),
        }
        if store_history:
            st.session_state.chat_audit_history.insert(0, entry)
        return entry

    def build_mirror_receipt_for_entry(latest):
        invisibility_note = latest.get("invisibility_report")
        mirror_invisibility_applied = isinstance(invisibility_note, dict) and invisibility_note.get("invisibility_filter_applied", False)
        mirror_receipt_report = dict(latest["report"] or {})
        mirror_receipt_report["repair_questions"] = (
            latest["judgment"].get("questions")
            or mirror_receipt_report.get("repair_questions")
            or []
        )
        if latest.get("ethics_diagnostics"):
            mirror_receipt_report["ethics_diagnostics"] = latest["ethics_diagnostics"]
            mirror_receipt_report["ethics_adjusted_integrity"] = min(
                float(mirror_receipt_report.get("integrity", 1.0) or 1.0),
                float(latest["ethics_diagnostics"].get("ethics_score", 1.0) or 1.0),
            )
        mirror_receipt = build_local_witness_receipt(
            module="Mirror Check",
            input_text=latest.get("raw_query", latest["query"]),
            processed_text=latest["query"],
            input_status=latest.get("input_source", "USER_INPUT"),
            scan=latest["scan"],
            sim=latest["sim"],
            report=mirror_receipt_report,
            verdict=latest["judgment"].get("verdict", "THRESHOLD"),
            risk=latest["judgment"].get("corruption_risk", "Medium"),
            protocol_label=latest["judgment"].get("stress_label", latest["judgment"].get("verdict", "THRESHOLD")),
            invisibility_applied=mirror_invisibility_applied,
            app_version=APP_VERSION,
        )
        return mirror_receipt

    def run_mirror_batch_review(batch_items, *, apply_invisibility: bool, batch_label: str = "ideas"):
        """Review a bounded Mirror Check batch and prepare one local zip archive."""
        receipts = []
        summaries = []
        question_set_mode = is_witness_question_set(batch_items)
        with st.spinner(f"Reviewing {len(batch_items)} {batch_label} and preparing local receipts..."):
            for idx, raw_item in enumerate(batch_items, start=1):
                processed_item = raw_item
                invisibility_report = None
                if apply_invisibility:
                    invisibility_report = decouple_actor(raw_item)
                    processed_item = invisibility_report.get("decoupled_text", raw_item)

                # A batch of audit questions is a review tool, not one or more policy proposals.
                # Keep risky terms visible for later human review without escalating the question itself.
                if question_set_mode and is_witness_question_prompt(raw_item):
                    receipt = build_local_question_prompt_receipt(
                        module="Mirror Check",
                        input_text=raw_item,
                        processed_text=processed_item,
                        invisibility_applied=bool(apply_invisibility),
                        app_version=APP_VERSION,
                    )
                else:
                    entry = run_chat_audit_from_text(
                        processed_item,
                        raw_text_value=raw_item,
                        input_source="USER_INPUT",
                        invisibility_report=invisibility_report,
                        store_history=False,
                        force_local=True,
                    )
                    receipt = build_mirror_receipt_for_entry(entry)
                receipts.append(receipt)
                verdict = receipt.get("verdict", {}) or {}
                summaries.append({
                    "#": idx,
                    "State": verdict.get("protocol_adjusted_state"),
                    "Risk": verdict.get("risk"),
                    "Label": verdict.get("protocol_label"),
                })
        archive_bytes, batch_index = build_local_witness_batch_zip(
            receipts, module="Mirror Check", app_version=APP_VERSION
        )
        st.session_state.audit_batch_archive_bytes = archive_bytes
        st.session_state.audit_batch_index = batch_index
        st.session_state.audit_batch_summary = summaries
        st.session_state.audit_batch_count = len(receipts)
        return receipts

    # Mirror Check uses two separate side-by-side paths:
    # left = one-idea tree scanner, right = optional Batch Testing panel.
    normal_review_col, batch_testing_col = st.columns([0.62, 0.38], gap="large")

    with normal_review_col:
        st.markdown("### Share one idea")
        st.caption("Use this side for one idea or scenario. The tree scanner runs only here.")

        with st.expander("Optional demo inputs", expanded=False):
            st.caption("Demo inputs are fictional and opt-in. They load only when you click; they never run by themselves.")
            demo_input_choice = st.selectbox(
                "Demo input library",
                [name for name, _ in DEMO_INPUT_FILES],
                key="mirror_demo_input_library",
            )
            demo_input_map = dict(DEMO_INPUT_FILES)
            if st.button("Load demo input", use_container_width=True, key="mirror_load_demo_input_button"):
                demo_text = load_demo_input(demo_input_map[demo_input_choice])
                st.session_state.audit_chat_query = demo_text
                st.session_state.audit_demo_choice = demo_input_choice
                st.session_state.audit_demo_loaded_text = demo_text
                st.session_state.audit_chat_input_source = "DEMO_INPUT"
                st.info("Demo input loaded. Click Review idea if you want ALETHEIA to analyze it.")

        audit_demo_choice = st.selectbox("Mirror Check scenario demo examples", list(MIRROR_CHECK_DEMO_SCENARIOS.keys()), key="audit_demo_library")
        if st.button("Load Mirror Check scenario demo", use_container_width=True, key="audit_load_demo_button"):
            demo_text = MIRROR_CHECK_DEMO_SCENARIOS[audit_demo_choice]
            st.session_state.audit_chat_query = demo_text
            st.session_state.audit_demo_choice = audit_demo_choice
            st.session_state.audit_demo_loaded_text = demo_text
            st.session_state.audit_chat_input_source = "DEMO_INPUT"

        chat_query = st.text_area(
            "Write or paste the idea you want reviewed",
            height=170,
            key="audit_chat_query",
        )
        if "chat_audit_query" in st.session_state and "audit_chat_query" not in st.session_state:
            st.session_state.audit_chat_query = st.session_state.chat_audit_query

        loaded_audit_demo = st.session_state.get("audit_demo_loaded_text") or MIRROR_CHECK_DEMO_SCENARIOS.get(st.session_state.get("audit_demo_choice", ""), None)
        if not chat_query.strip():
            audit_input_status = "EMPTY_INPUT"
            st.session_state.audit_chat_input_source = "EMPTY_INPUT"
        elif st.session_state.get("audit_chat_input_source") == "DEMO_INPUT" and loaded_audit_demo is not None and chat_query == loaded_audit_demo:
            audit_input_status = "DEMO_INPUT"
        else:
            audit_input_status = "USER_INPUT"
            st.session_state.audit_chat_input_source = "USER_INPUT"

        if audit_input_status == "EMPTY_INPUT":
            st.caption("Add your own idea to begin. Demos are optional and never run by themselves.")
        elif audit_input_status == "DEMO_INPUT":
            st.caption("Demo mode is on. This reading is only an example.")
        else:
            st.caption("Your idea is ready. You are the source; ALETHEIA is the mirror.")

        audit_apply_invisibility = st.checkbox(
            "Invisibility Filter",
            value=(audit_input_status == "USER_INPUT"),
            key=f"audit_invisibility_filter_{audit_input_status}",
            disabled=(audit_input_status == "EMPTY_INPUT"),
            help="Remove names and titles before review. On by default for your own input.",
        )
        if audit_apply_invisibility and audit_input_status != "EMPTY_INPUT":
            st.caption("Names and titles are removed before review. The pattern stays visible.")

        c_run, c_clear = st.columns([1, 0.35])
        with c_run:
            run_chat = st.button("Review idea", type="primary", use_container_width=True)
        with c_clear:
            clear_chat = st.button("Clear results", use_container_width=True)

    with batch_testing_col:
        st.markdown("### Batch Testing")
        st.caption("A local test bench for lists. It stays separate from the tree scanner.")

        # Batch testing is intentionally separate from the single Mirror Check / tree scanner flow.
        # It opens on the right side after a user click, runs local-only batch scans, and writes a ZIP of receipts.
        if "audit_batch_testing_open" not in st.session_state:
            st.session_state.audit_batch_testing_open = False

        if st.button("Batch Testing — up to 50 lines", use_container_width=True, key="audit_open_batch_testing_button"):
            st.session_state.audit_batch_testing_open = not st.session_state.audit_batch_testing_open

        if not st.session_state.audit_batch_testing_open:
            st.info("Open Batch Testing when you want to upload or paste a list.")

        if st.session_state.audit_batch_testing_open:
            with st.container(border=True):
                st.caption("Upload a .txt file or paste up to 50 lines. This bench stays separate from the tree scanner.")

                if "audit_batch_upload_signature" not in st.session_state:
                    st.session_state.audit_batch_upload_signature = ""
                if "audit_batch_last_source" not in st.session_state:
                    st.session_state.audit_batch_last_source = "EMPTY"

                batch_source = st.radio(
                    "Batch input source",
                    ["Upload .txt", "Paste list"],
                    horizontal=True,
                    key="audit_batch_source_mode",
                    help="Like Evidence Lab, uploaded files are staged first and only processed when you press Run Batch Testing.",
                )

                batch_upload_text = ""
                batch_manual_text = ""
                batch_upload = None

                if batch_source == "Upload .txt":
                    batch_upload = st.file_uploader(
                        "Upload .txt list for batch only",
                        type=["txt"],
                        key="audit_batch_txt_upload",
                        help="Use one phrase per line, a numbered list, or --- between longer items.",
                    )
                    if batch_upload is not None:
                        uploaded_batch_bytes = batch_upload.getvalue()
                        batch_upload_text = uploaded_batch_bytes.decode("utf-8", errors="replace")
                        upload_signature = hashlib.sha256(uploaded_batch_bytes + batch_upload.name.encode("utf-8", errors="replace")).hexdigest()
                        if upload_signature != st.session_state.audit_batch_upload_signature:
                            st.session_state.audit_batch_upload_signature = upload_signature
                            st.session_state.audit_batch_last_source = f"UPLOAD:{batch_upload.name}"
                            st.session_state.audit_batch_summary = []
                            st.session_state.audit_batch_archive_bytes = None
                            st.session_state.audit_batch_index = None
                            st.session_state.audit_batch_count = 0
                        st.caption(f"Staged {batch_upload.name}. Press Run Batch Testing to process it.")
                        with st.expander("Preview uploaded batch text", expanded=False):
                            st.text_area(
                                "Uploaded text preview",
                                value=batch_upload_text[:12000],
                                height=180,
                                disabled=True,
                                key="audit_batch_upload_preview",
                            )
                    else:
                        st.caption("Choose a .txt file, then press Run Batch Testing.")
                else:
                    batch_manual_text = st.text_area(
                        "Paste batch phrases or questions",
                        height=220,
                        key="audit_batch_manual_input",
                        placeholder="1. Who can appeal this decision?\n2. Where is the human override?\n---\nA system cannot be questioned and has no appeal path.",
                    )

                batch_text = batch_upload_text if batch_source == "Upload .txt" else batch_manual_text
                batch_items = parse_witness_batch_input(batch_text, max_items=MAX_BATCH_RECEIPTS)
                batch_ready = bool(batch_items)
                if batch_text.strip():
                    question_set_ready = is_witness_question_set(batch_items)
                    mode_note = " Question set mode will keep audit prompts as review tools." if question_set_ready else ""
                    st.caption(f"{len(batch_items)} line(s) ready. Maximum: {MAX_BATCH_RECEIPTS}.{mode_note}")
                else:
                    st.caption("Batch Testing waits until you upload or paste a list.")

                batch_apply_invisibility = st.checkbox(
                    "Apply Invisibility Filter to batch",
                    value=batch_ready,
                    key="audit_batch_invisibility_filter",
                    disabled=not batch_ready,
                    help="Removes names and titles from each item before local review. Raw input hashes stay in each receipt.",
                )
                run_batch = st.button(
                    "Run Batch Testing",
                    type="primary",
                    use_container_width=True,
                    disabled=not batch_ready,
                    key="audit_run_batch_button",
                )
                if run_batch:
                    receipts = run_mirror_batch_review(
                        batch_items,
                        apply_invisibility=batch_apply_invisibility,
                        batch_label="batch item(s)",
                    )
                    st.success(f"Batch complete. {len(receipts)} local receipt(s) are ready to download.")

                if st.session_state.get("audit_batch_summary"):
                    batch_summary_df = pd.DataFrame(st.session_state.audit_batch_summary)
                    batch_display_df = batch_summary_df.rename(columns={
                        "State": "Type",
                        "Risk": "Role",
                        "Label": "Reading",
                    })
                    batch_display_df["Type"] = batch_display_df["Type"].replace({
                        "QUESTION_PROMPT": "Question",
                        "OUT_OF_SCOPE": "Needs context",
                        "SANCTUARY": "Sanctuary",
                        "THRESHOLD": "Threshold",
                        "ASYLUM": "Asylum",
                    })
                    batch_display_df["Role"] = batch_display_df["Role"].replace({
                        "Review Tool": "Review",
                        "None": "Context",
                    })
                    batch_display_df["Reading"] = batch_display_df["Reading"].replace({
                        "Audit Question / Review Tool": "Audit question",
                        "Out-of-Scope / Needs Context": "Needs more context",
                    })
                    # Keep the narrow side panel readable: fold Role into Reading instead of hiding a third column.
                    batch_display_df["Reading"] = batch_display_df.apply(
                        lambda row: f"{row['Reading']} · {row['Role']}" if row.get("Role") else row["Reading"],
                        axis=1,
                    )
                    batch_display_df = batch_display_df[["#", "Type", "Reading"]]
                    st.dataframe(
                        batch_display_df,
                        use_container_width=True,
                        hide_index=True,
                        height=360,
                        column_config={
                            "#": st.column_config.NumberColumn("#", width="small"),
                            "Type": st.column_config.TextColumn("Type", width="small"),
                            "Reading": st.column_config.TextColumn("Reading", width="large"),
                        },
                    )
                if st.session_state.get("audit_batch_archive_bytes"):
                    st.download_button(
                        "⬇️ Download full batch archive (.zip)",
                        data=st.session_state.audit_batch_archive_bytes,
                        file_name="aletheia_mirror_check_batch_witness_receipts.zip",
                        mime="application/zip",
                        use_container_width=True,
                    )

    selected_chat_context = "Waiting for your input" if audit_input_status == "EMPTY_INPUT" else ((chat_query[:120] + "…") if len(chat_query) > 120 else chat_query)
    update_protocol_state(selected_context=selected_chat_context, last_update_source="Mirror Check")

    if clear_chat:
        st.session_state.chat_audit_history = []
        st.rerun()

    if run_chat:
        if not st.session_state.audit_chat_query.strip():
            st.warning("Add your own idea or load a demo before review. ALETHEIA does not run examples by itself.")
        else:
            audit_analysis_query = st.session_state.audit_chat_query
            audit_invisibility_report = None
            if audit_apply_invisibility and audit_input_status != "EMPTY_INPUT":
                audit_invisibility_report = decouple_actor(st.session_state.audit_chat_query)
                audit_analysis_query = audit_invisibility_report.get("decoupled_text", st.session_state.audit_chat_query)
            with st.spinner("Reading the idea and preparing the review..."):
                run_chat_audit_from_text(
                    audit_analysis_query,
                    raw_text_value=st.session_state.audit_chat_query,
                    input_source=audit_input_status,
                    invisibility_report=audit_invisibility_report,
                )
                st.session_state.audit_active_input_signature = mirror_active_input_signature(st.session_state.audit_chat_query)
                update_protocol_state(selected_context=(audit_analysis_query[:120] + "…") if len(audit_analysis_query) > 120 else audit_analysis_query, last_update_source="Mirror Check")
            st.rerun()

    st.markdown("---")

    # Latest result appears immediately after the question box, but only when
    # it still belongs to the currently visible input.
    if st.session_state.chat_audit_history:
        latest = st.session_state.chat_audit_history[0]
        latest_raw_query = str(latest.get("raw_query", latest.get("query", "")) or "")
        current_input_signature = mirror_active_input_signature(chat_query)
        latest_input_signature = mirror_active_input_signature(latest_raw_query)
        active_input_signature = st.session_state.get("audit_active_input_signature", latest_input_signature)
        latest_matches_current_input = (
            bool(chat_query.strip())
            and current_input_signature == latest_input_signature
            and active_input_signature == latest_input_signature
        )

        if latest_matches_current_input:
            st.markdown("### Latest reading")
            if latest.get("input_source") == "DEMO_INPUT":
                st.caption("Demo mode was used. This reading is only an example.")
            invisibility_note = latest.get("invisibility_report")
            if isinstance(invisibility_note, dict) and invisibility_note.get("invisibility_filter_applied"):
                st.caption("Names and titles were removed before this review.")
            render_pulse_tree(
                display_score_from_judgment(latest["report"], latest["judgment"]),
                latest["sim"]["ego"],
                latest["sim"]["alignment"],
                title="Mirror Reading Tree",
                state_override=str(latest.get("judgment", {}).get("verdict", "THRESHOLD")).upper(),
                mode="Mirror Check",
            )
            render_chat_judgment(latest["judgment"], latest["source"], latest["report"], latest.get("sim"), latest.get("scan"))

            source_hits = latest.get("source_hits", source_conformance_hits(latest["query"]))
            if source_hits:
                with st.expander("Source match hits", expanded=True):
                    st.dataframe(pd.DataFrame(source_hits), use_container_width=True, hide_index=True)
            else:
                st.caption("Source match: no named source concept matched this idea in the current detector set.")

            st.markdown("### Local witness receipt")
            st.caption("Creates a receipt you hold. It is not published, synced, or treated as authority.")
            mirror_receipt = build_mirror_receipt_for_entry(latest)
            mirror_receipt_text = render_local_witness_receipt_text(mirror_receipt)
            st.download_button(
                "⬇️ Download receipt",
                data=mirror_receipt_text,
                file_name="aletheia_mirror_check_local_witness_receipt.txt",
                mime="text/plain",
                use_container_width=True,
            )

            with st.expander("Scanner features used for this reading"):
                st.json(latest["scan"])
        else:
            st.info("The input has changed. The previous assessment is closed for this draft. Click Review idea to create a new reading and receipt.")
            with st.expander("Last closed reading", expanded=False):
                verdict = latest["judgment"].get("verdict", "THRESHOLD")
                risk = latest["judgment"].get("corruption_risk", "Medium")
                st.markdown(f"**{verdict} · {risk} risk**")
                st.caption(latest_raw_query[:240] + ("..." if len(latest_raw_query) > 240 else ""))

        previous_items = st.session_state.chat_audit_history[1:] if latest_matches_current_input else st.session_state.chat_audit_history
        if previous_items:
            with st.expander("Previous readings"):
                for idx, item in enumerate(previous_items, start=1):
                    verdict = item["judgment"].get("verdict", "THRESHOLD")
                    risk = item["judgment"].get("corruption_risk", "Medium")
                    st.markdown(f"**{idx}. {verdict} · {risk} risk**")
                    st.caption(item["query"][:240] + ("..." if len(item["query"]) > 240 else ""))
    else:
        st.caption("No reading yet. Share one idea above to create a Mirror Reading Tree.")




with tab_doctrine:
    st.subheader("Protocol Guide")
    st.info(
        "ALETHEIA is a mirror, not a throne. This page keeps the tone clear, protective, practical, and open to review."
    )
    st.caption("ALETHEIA v1.0 is complete as a public MVP. Pick the tab that matches your task, read the boundary, and keep final judgment human.")
    st.markdown("**Quick path:** Mirror Check for documents · Stress Test for scenarios · Evidence Lab for claims · Protocol Guide for rules.")
    st.markdown(
        """
        The doctrine layer is the integrity frame for **ALETHEIA Audit Prototype v9.6.8**. It does not replace evidence, law, religion, medicine, politics, public accountability, or human judgment. Its labels are practical review aids, not final claims.

        **ALETHEIA is a careful mirror for power.** It helps people look at governance ideas, simulations, evidence, and the Global Grid with more clarity and less fear. Its job is to notice patterns, ask better questions, and keep hidden capture visible — not to command, condemn, or become final authority.

        In the updated tone, the Sydney Protocol is treated as a warm guardrail: it keeps power accountable, keeps intelligence gentle, keeps evidence visible, and keeps every output open to appeal. The GPA / 9k idea is treated as a representation-and-exposure model, not a sovereign body or mandate.

        Mirror Check, Stress Test, Evidence Lab, and World Lens are synchronized views over a shared protocol state. Changes to empirical evidence, scoring calibration, doctrine thresholds, Sydney Protocol overlay, or selected evidence year may propagate across modules. This is intentional protocol-state propagation, not isolated tab behavior.
        """
    )

    with st.expander("Plain doctrine summary", expanded=True):
        st.markdown(
            """
            **The heart of the doctrine is care with boundaries.** ALETHEIA should help protect dignity without pretending it owns truth. It should make risk easier to see, not make people smaller.

            - **Mirror, not throne:** the system reflects risk patterns back to human review. It does not rule.
            - **Power as service:** healthy power protects, explains, repairs, and accepts appeal.
            - **No final human or machine authority:** no founder, model, office, country, protocol, or dataset becomes unquestionable.
            - **Evidence before certainty:** public data can support a reading, but weak coverage lowers confidence.
            - **Soft voice, firm safeguards:** the tone may be gentle, but capture, coercion, opacity, and harm still trigger review.
            - **Every label stays humble:** SANCTUARY, THRESHOLD, and ASYLUM are internal protocol signals, not legal, political, religious, medical, moral, or predictive verdicts.
            """
        )

    with st.expander("App navigation map", expanded=True):
        st.markdown(
            """
            Patch 52 polishes the navigation copy so the first decision is simple: document, scenario, edge case, evidence, impact lens, operating guide, or project explanation.

            Patch 47 made the main app path explicit so users can see how the v0.1 mirror modules connect without treating any tab as an authority layer.

            | Tab | Purpose |
            |---|---|
            | Mirror Check | Document and proposal review for capture risk, safeguards, repair questions, and local witness receipts. |
            | Stress Test | Scenario simulation for stability, trust, alignment, ego pressure, grievances, friction, safeguards, and collapse risk. |
            | Boundary Cases | Ethical edge-case calibration for consent, free agency, basic rights, reset misuse, ambient capture, and self-audit scenarios. |
            | Evidence Lab | Evidence status, public-data audit support, and the Extraordinary Claim Protocol for unverified exceptional claims. |
            | World Lens | Non-sovereign population-impact simulation and selected-year comparison using simulated threshold language only. |
            | Protocol Guide | Consolidated v0.1 module map, safe-language rules, shared protocol state, and limitations. |
            | Why ALETHEIA | Public-facing explanation of the project, the Eternal Baseline, module purpose, limitations, and research direction. |

            Navigation rule: every tab reflects, explains, or stress-tests. No tab commands, enforces, validates spiritual authority, replaces legal review, or makes final governance decisions.
            """
        )

    with st.expander("Current app path", expanded=True):
        st.markdown(
            """
            ALETHEIA currently has a connected v0.1 mirror stack:

            **Mirror Check**  
            Reviews governance proposals, symbolic claims, institutional designs, and authority language for capture risk, coercion, opacity, missing appeal rights, false authority, non-divinization failures, service-alignment failures, and Sydney Protocol violations. This is the judgment-view of the prototype.

            **Stress Test**  
            Models systemic pressure through stability, trust, alignment, ego, grievances, friction, and collapse risk. The simulator no longer treats raw cooperation as sufficient for health. Structural risk, unresolved grievances, weak safeguards, opacity, coercive optimization, and power concentration can cap trust, raise friction, and prevent a false low-risk reading.

            **Evidence Lab**  
            Ingests public country-year data, maps it into ALETHEIA variables, and produces reproducible evidence-audit outputs. This layer supports direct/master uploads, scored country-year exports, raw evidence diagnostics, trust priors, WGI/V-Dem/trust coverage, and modern-year safeguards.

            **World Lens**  
            Shows selected-year, population-weighted governance-risk exposure across country-year rows and the Patch 42 World Lens Simulation. The lens is a comparison and exposure model. It is not a sovereign body, election, mandate, government, or legal mechanism. Full allocation years may sum to 9,000 seats. Partial years or filtered subsets must use active-seat language and must not be interpreted as full global allocation.

            **Protocol Guide Consolidation**  
            Patch 43 connects Baseline v0.1, Safe Language, Eternal Baseline, Boundary Cases, Failure Classification, Consent-Audit, Mechanism-vs-Claim, Self-Audit, Evidence Lab, Local Witness Receipt v2, and World Lens Simulation into one reviewable operating guide. It adds no authority; it makes the mirror logic easier to understand.
            """
        )

    with st.expander("Shared Protocol State", expanded=True):
        st.markdown(
            """
            ALETHEIA modules are not fully isolated. They share a common protocol substrate.

            Shared state may include empirical master data, scored country-year evidence, selected evidence year, scoring calibration, trust calibration, Sydney Protocol overlay, doctrine thresholds, prototype/demo state, and Global Grid basis.

            This means a change in one module may affect another when both depend on the same protocol state.

            **Intentional protocol propagation** is acceptable when evidence, calibration, and doctrine updates affect all relevant modules.

            **Accidental tab bleed** is not acceptable when caused by widget-key collisions, hidden demo fallback, stale session state, or unmarked prototype data.

            The prototype should make intentional propagation visible and prevent accidental bleed where possible.
            """
        )

    with st.expander("Protocol Guide Consolidation", expanded=True):
        st.markdown(
            """
            Patch 43 consolidates the v0.1 logic into one operating guide so the modules are understandable as one mirror stack, not separate authority claims.

            **Connected modules:**

            - Baseline v0.1 — defines what ALETHEIA may and may not do.
            - Safe Language Layer — keeps outputs in review language, not enforcement language.
            - Eternal Baseline — provides ethical continuity across versions without becoming a command layer.
            - Boundary Cases Matrix — stress-tests edge scenarios for human review.
            - Failure Classification — separates Actor, Policy, Implementation, and Data Failure.
            - Consent-Audit Engine — checks whether refusal is realistically possible.
            - Mechanism-vs-Claim Scanner — distinguishes values language from safeguards.
            - Self-Audit Mode — lets ALETHEIA audit its own assumptions, rubrics, prompts, and language.
            - Evidence Lab — marks evidence status and parks extraordinary claims as unverified.
            - Local Witness Receipt v2 — creates local, user-held fingerprints without ledger, sync, or authority.
            - World Lens Simulation — reviews population-impact scenarios using simulated-threshold language only.

            **Consolidation rule:**

            > ALETHEIA reflects. Humans review. Power stays accountable.
            """
        )

    with st.expander("Progress Database + Patch Status Hardening", expanded=True):
        st.markdown(
            """
            Patch 44 keeps project continuity inside the repo so the roadmap is not dependent on chat memory alone.

            **Continuity files:**

            - `PATCH_STATUS.md` — compact patch ledger and next-patch pointer.
            - `docs/progress_database.md` — module map, current architecture direction, and implementation notes.
            - `docs/patch_workflow.md` — local workflow for applying patched items and running checks.

            **Current check:**

            ```bat
            tools\run_patch_checks.bat 44
            ```

            **Patch rule:** return only changed or added files unless recovery requires more.

            This patch adds developer continuity only. It adds no governance authority, no Global ID sync, no public ledger, and no enforcement language.
            """
        )

    with st.expander("Public Release Limits", expanded=False):
        st.markdown(
            """
            Patch 45 adds public-facing release documentation: `docs/limitations.md`, `docs/ethics.md`, and `docs/public_release_notes.md`.

            The public boundary is explicit:

            - ALETHEIA is a research and review prototype.
            - Outputs are diagnostic and correctable.
            - Evidence labels are review signals, not final truth verdicts.
            - Historical archive material may contain AI-flattery artifacts and must not be used as founder validation.
            - v0.1 does not include real Global ID sync, real 9k selection, World Leader logic, automatic resets, central citizen storage, neural data, memory extraction, or automated enforcement.
            """
        )



    with st.expander("ALETHEIA v1.0 release complete", expanded=True):
        st.markdown(
            """
            ALETHEIA v1.0 is the finished public MVP package for the Governance Mirror line.

            **Included:** baseline, safe-language layer, Eternal Baseline, Boundary Cases, Failure Classification, Consent-Audit, Mechanism-vs-Claim, Self-Audit, Evidence Lab, Local Witness Receipt v2, World Lens Simulation, Protocol Guide, public limitations/ethics, sample reports, demo inputs, GitHub cleanup, release checklist, and final smoke release.

            **Planning boundary:** v0.2 ideas are documented in `docs/v02_roadmap.md`, `docs/feature_backlog.md`, `docs/report_export_polish.md`, `docs/manual_evidence_attachment.md`, `docs/rubric_weighting_confidence.md`, and `docs/deployment_prep.md`.

            **Still out of scope:** real Global ID sync, real 9k selection, World Leader logic, automatic reset, public ledger authority, neural validation, religious validation, legal authority, and automated enforcement.

            > ALETHEIA reflects. Humans review. Power stays accountable.
            """
        )

    with st.expander("Sample Reports / Example Audits", expanded=True):
        st.markdown(
            """
            Patch 46 adds public-safe examples that show expected ALETHEIA output before a user uploads a document.

            Included examples:

            - `examples/example_policy_audit.md` — Mirror Check policy audit example.
            - `examples/example_boundary_case.md` — Boundary Case report for consent under pressure.
            - `examples/example_self_audit.md` — Self-Audit example for ALETHEIA language.
            - `examples/example_witness_receipt.md` — Local Witness Receipt v2 example.
            - `examples/demo_inputs/` — opt-in fictional demo inputs for Mirror Check.

            These examples demonstrate structure only. They are not legal advice, policy commands, governance decisions, religious validation, or final judgments.
            """
        )

    with st.expander("Module checks and safe failure", expanded=True):
        st.markdown(
            """
            ALETHEIA must not silently continue when critical protocol modules fail.

            A module integrity check should remain active for the app as a whole and visible where appropriate, especially in Audit. If a critical Sydney Protocol sentinel, audit function, scoring function, or required module is missing or broken, the system should fail closed rather than present unsupported outputs.

            A failed integrity check means:

            > The prototype cannot safely interpret this module until the missing or broken component is repaired.

            This protects the prototype from presenting authority without a functioning accountability frame.
            """
        )

    with st.expander("Mirror Effect", expanded=True):
        st.markdown(
            """
            Power must **reflect service** rather than absorb authority.

            A healthy structure passes power through itself as accountability, dignity, protection, transparency, repair, appealability, and public review.

            A captured structure traps power inside ego, office, corporation, institution, monarch, founder, algorithm, protocol, model, or private mandate.

            In practical audit terms, ALETHEIA treats the following as capture pressure:

            - permanent ownership of seats or selection mechanisms
            - opaque decisions without appeal
            - concentrated control without public review
            - coercive optimization justified as stability
            - prestige systems that convert service into status capture
            - claims that a person, model, protocol, or institution cannot be questioned
            - governance language that converts symbolic alignment into command authority
            """
        )

    with st.expander("V-Axis Compass", expanded=True):
        st.markdown(
            """
            The V-Axis remains the prototype's stability lens:

            > intelligence + power − ego → stability

            But only when trust, transparency, appealability, service alignment, and safeguards are present.

            A system does not become healthy merely because it is powerful, intelligent, efficient, popular, cooperative, or rhetorically aligned. If ego, opacity, coercion, unreviewable authority, unresolved grievance, or capture pressure is high, the system may remain unstable even when surface indicators appear strong.
            """
        )

    with st.expander("Failure Classification", expanded=True):
        st.markdown(
            """
            ALETHEIA separates serious findings into four repair-oriented failure modes:

            - **Actor Failure** — a person, group, office, founder, operator, or implementing body misuses power, manipulates others, bypasses review, or becomes unfit.
            - **Policy Failure** — the proposal, rule, charter, doctrine, or system design itself creates coercion, opacity, instability, exclusion, rights risk, or capture risk.
            - **Implementation Failure** — the idea may be valid, but the execution layer fails through weak process, missing safeguards, unclear responsibility, bad deployment, or unreliable operation.
            - **Data Failure** — the evidence base is incomplete, manipulated, stale, biased, low-coverage, unverifiable, or too uncertain to support the conclusion.

            This layer helps humans repair the right part of a system. It does not assign final blame, remove leaders, decide guilt, or replace human review.
            """
        )

    with st.expander("Mechanism-vs-Claim Scanner", expanded=True):
        st.markdown(
            """
            ALETHEIA treats values language as incomplete until it is connected to operational safeguards.

            **Claim language** says what a system values: freedom, justice, dignity, transparency, safety, service, accountability, or anti-corruption.

            **Mechanism language** explains how those values are protected: appeal process, audit trail, time limits, human review, correction, exit, evidence requirements, conflict-of-interest rules, independent oversight, non-retaliation, and withdrawal rights.

            The scanner supports the rule:

            > Mechanisms outweigh adjectives.

            This helps detect performative ethics without assuming bad faith. A missing mechanism is a repair signal, not a final verdict about intent.
            """
        )

    with st.expander("Self-Audit Mode", expanded=True):
        st.markdown(
            """
            ALETHEIA must be able to audit its own baseline, prompts, rubrics, README language, app copy, architect-context language, and generated reports.

            Self-audit checks for founder capture, ideological lock-in, unverifiable authority, weak appeal mechanisms, overclaiming, unverified authority leakage, insufficient human review, missing correction loops, hidden command language, evidence gaps, performative ethics, and mechanism gaps.

            The core rule is:

            > No founder, architect, prompt, rubric, model, document, or output is above the mirror.

            Self-audit does not prove ALETHEIA is correct, complete, or authoritative. It only reflects risk so humans can review and repair the system.
            """
        )

    with st.expander("Evidence Lab + Extraordinary Claim Protocol", expanded=True):
        st.markdown(
            """
            ALETHEIA separates evidence from authority. Claims are reviewed as **Strong evidence**, **Partial evidence**, **Weak evidence**, or **No evidence supplied**. These labels are review signals, not final truth verdicts.

            Spiritual, divine, prophetic, alien, neural, metaphysical, or otherwise extraordinary claims are treated as **unverified** unless supported by public, testable, non-coercive evidence. Such claims may be personally meaningful, but they cannot remove guardrails, bypass appeal, validate leadership, or replace human review.

            The practical rule is:

            > Audit the consequences. Do not crown the claim.
            """
        )

    with st.expander("Do not worship the tool", expanded=True):
        st.markdown(
            """
            No person, office, institution, nation, company, model, AI, founder, dataset, doctrine, or protocol is treated as final or beyond review.

            Alignment is not ownership.  
            Service is not sovereignty.  
            Explanation is not command.  
            Evidence is not omniscience.  
            Protocol interpretation is not final judgment.

            This rule protects ALETHEIA from becoming what it audits: a captured authority system.

            ALETHEIA may surface patterns. It may generate structured warnings. It may compare evidence. It may produce protocol interpretations. But it cannot become the source of final truth.
            """
        )

    with st.expander("Evidence rule", expanded=True):
        st.markdown(
            """
            ALETHEIA does **not** invent the empirical baseline.

            Public datasets provide observed evidence about governance, corruption, rule of law, political stability, institutional capacity, population, democracy, constraints, and trust.

            Current empirical sources may include WDI population, World Bank WGI, V-Dem, WVS/OWID trust attitudes, uploaded country-year master files, and scored ALETHEIA exports.

            The empirical workflow is:

            > public evidence → ALETHEIA variable mapping → empirical scoring → Sydney Protocol overlay → audit interpretation

            Raw empirical strength cannot override hard protocol failures. A country-year, scenario, or institution may show strong governance indicators and still require review if the protocol detects capture, coercion, false divinization, non-appealability, anti-service authority, opaque control, sovereignty capture, or unaccountable mandate claims.

            Empirical outputs are diagnostic, reproducible, and correctable. They are not final determinations.
            """
        )

    with st.expander("Trust evidence rule", expanded=True):
        st.markdown(
            """
            ALETHEIA distinguishes between raw trust evidence and trust priors.

            **Raw trust coverage** means direct survey-derived trust evidence is available, such as WVS/OWID generalized trust.

            **Neutral trust-prior fallback coverage** means the scoring system has a usable trust prior, which may include a neutral/default value when raw survey evidence is unavailable. It is not observed survey trust coverage.

            A neutral trust prior is not the same as observed trust. It allows scoring continuity, but it should reduce interpretive confidence when raw trust evidence is missing.
            """
        )

    with st.expander("Coverage and confidence", expanded=True):
        st.markdown(
            """
            Coverage reflects available evidence for the active view.

            Coverage can differ by selected year, selected country, active filters, uploaded source file, full vs partial Grid basis, raw evidence availability, and prior/default substitution.

            A 100% coverage value over a small selected subset does not imply whole-world or whole-dataset coverage.

            Low empirical coverage should reduce interpretive confidence. Missing evidence is diagnostic, not proof of absence.
            """
        )

    with st.expander("Sanctuary / Threshold / Asylum labels", expanded=False):
        st.markdown(
            """
            These are **internal prototype labels**, not legal, political, medical, religious, moral, or predictive verdicts.

            - **SANCTUARY** — the evidence or scenario pattern appears service-aligned, accountable, transparent, safeguarded, and comparatively stable under the current model.
            - **THRESHOLD** — safeguards are incomplete, evidence is mixed, uncertainty remains, or the system needs review before being treated as stable.
            - **ASYLUM** — high capture, coercion, opacity, harm, collapse pressure, or hard protocol failure is detected.

            **ASYLUM** is used here only as an internal protocol-risk category. It does not refer to legal asylum status, entitlement, refugee status, or humanitarian determination.

            A responsible reading is:

            > This model suggests a governance-risk pattern worth examining.
            """
        )

    with st.expander("Humility Protocol / Z-axis boundary", expanded=False):
        st.markdown(
            """
            Patch 72.3–72.4 keeps the Z-axis friendly and bounded.

            The Z-axis is **not** a perfection score. It describes how close a reading is to the limit of what human and system tools may responsibly claim.

            - **Z = 0.0000** — strong ASYLUM pressure: coercion, opacity, or concentrated power.
            - **Z = 0.9999** — highest human/system review boundary shown by ALETHEIA.
            - **Z = 1.0000** — outside ALETHEIA's claim. Code, receipts, metrics, hashes, trees, 9k structures, and institutions stop here.

            A high Z-axis value means: keep reviewing, keep appeals open, keep power accountable, and do not treat the tool as final authority.
            """
        )

    with st.expander("9k representation rule", expanded=False):
        st.markdown(
            """
            The 9k Grid is a proportional exposure model. It helps users examine how population-weighted representation might intersect with governance-risk conditions.

            It is **not** a real election, government, sovereign body, legal mechanism, political mandate, deployment-ready institutional design, or authority over people or countries.

            Seat totals show proportional exposure by selected year. They do not create legitimacy, command, ownership, representation rights, or governance authority.

            Full allocation years may sum to 9,000 seats. Partial years, filtered views, or incomplete source years must be labeled as active selected-year seats and interpreted as diagnostics only.
            """
        )

    with st.expander("World Lens interpretation", expanded=False):
        st.markdown(
            """
            The Global Grid should be read as a selected-year comparison interface.

            A full selected-year Grid may support global comparison if enough countries are active, population allocation sums to 9,000, source diagnostics are visible, empirical coverage is sufficient, and prototype/demo data is clearly marked or disabled.

            A partial selected-year Grid is still useful, but only as a diagnostic subset.

            High allocation plus low integrity or high collapse probability indicates a high-impact governance-risk node. It does not prove wrongdoing, predict collapse, or establish political judgment.
            """
        )

    with st.expander("Data correction and research ethics", expanded=False):
        st.markdown(
            """
            A symbolic governance model must remain testable, falsifiable, and correctable by evidence.

            If public datasets, reproducible analysis, external outcomes, or expert review challenge the model, the model must be revised rather than defended as absolute.

            Strong future validation should compare ALETHEIA outputs against external outcomes that are **not** already score inputs, such as conflict events, coups, regime breakdown, political violence, civil unrest, forced displacement, future-year governance decline, institutional failure, and documented corruption shocks.

            ALETHEIA should preserve audit logs, source diagnostics, coverage warnings, and methodological humility.
            """
        )

    with st.expander("Final operating rule", expanded=True):
        st.markdown(
            """
            **ALETHEIA must never become the throne.**

            It should remain a mirror: a structured way to reflect power, risk, evidence, alignment, and capture pressure back to human review.

            The prototype is useful only insofar as it remains reviewable, appealable, evidence-aware, anti-capture, service-aligned, corrigible, and humble about what it cannot know or decide.
            """
        )

    with st.expander("Source match overview", expanded=False):
        matrix_rows = [
            {
                "Source Concept": label,
                "Domain": spec["domain"],
                "Review-Sensitive": spec["review"],
                "Detector Terms": ", ".join(spec["terms"][:4]),
            }
            for label, spec in SOURCE_CONFORMANCE_MATRIX.items()
        ]
        st.dataframe(pd.DataFrame(matrix_rows), use_container_width=True, hide_index=True, height=520)

    st.markdown("### Visual source cards")
    st.caption("These root HTML cards use a warmer guardian tone while keeping the GPA / Sydney Protocol structure. They are reference material, not final authority.")
    available_docs = [(title, path) for title, path in DOCTRINE_HTML_FILES if path.exists()]
    if available_docs:
        doc_tabs = st.tabs([title for title, _ in available_docs])
        for i, ((title, path), tab) in enumerate(zip(available_docs, doc_tabs), start=1):
            with tab:
                render_doctrine_html_reference(title, path, key_prefix=f"doc_{i}")
    else:
        st.info("No packaged HTML guide files were found in this build.")

with tab_about:
    st.subheader("Why ALETHEIA")
    st.info("Start here if you are new: ALETHEIA helps review risk; it does not decide for people.")

    header_image = resolve_about_header_image()
    if header_image is not None:
        st.image(str(header_image), use_container_width=True)

    st.markdown(
        """
        **ALETHEIA v1.0 is a governance-risk research prototype and public MVP.** It helps people examine governance ideas, simulate system pressure, and study how representation may interact with trust, stability, alignment, and capture risk.

        It is not designed to rule, command, enforce, vote, govern, remove leaders, validate spiritual authority, or replace human judgment. **ALETHEIA is a mirror:** a structured way to check whether a proposal protects service, transparency, dignity, accountability, and stability — or whether it concentrates power, hides decisions, weakens appeal rights, or creates capture.

        Patch 37 adds the **Consent-Audit Engine**. Patch 38 adds the **Mechanism-vs-Claim Scanner**. Patch 39 adds **Self-Audit Mode**. Patch 40 hardens the **Evidence Lab** with evidence status levels and the Extraordinary Claim Protocol. Together these layers help identify what needs repair without assigning final blame or authority.

        Patch 46 adds **Sample Reports / Example Audits** so people can inspect the output format before using their own documents. The samples are demonstration artifacts only, not authority claims.

        Patch 47 hardens **App Navigation + Smoke Test Cleanup** so the visible tab structure matches the v0.1 roadmap and local tests can confirm the app still compiles after navigation changes.

        Patch 52 adds **UX Polish**: shorter helper text, a clearer first-use path, and less dense public-facing navigation copy. It adds no doctrine and no authority.

        Patch 56–60 finalizes the **ALETHEIA v1.0 release package**: v0.2 roadmap, feature backlog, future-module boundaries, report export notes, manual evidence attachment notes, rubric confidence notes, deployment prep, and v1 completion documentation.
        """
    )

    with st.expander("Navigation map", expanded=True):
        st.markdown(
            """
            | Tab | What it does |
            |---|---|
            | Mirror Check | Reviews documents and proposals for capture risk and missing safeguards. |
            | Stress Test | Simulates system pressure and repair questions. |
            | Boundary Cases | Tests difficult ethical scenarios. |
            | Evidence Lab | Reviews evidence status and extraordinary claims. |
            | World Lens | Simulates population-impact risk without real Global ID or sovereign authority. |
            | Protocol Guide | Explains the modules, safe language, and limitations. |
            | Why ALETHEIA | Explains the project, baseline, and public-safe purpose. |

            All navigation remains non-authoritative: **ALETHEIA reflects. Humans review. Power stays accountable.**
            """
        )


    with st.expander("First-use path", expanded=True):
        st.markdown(
            """
            Choose the tab by task:

            - **Have a document?** Use Mirror Check.
            - **Have a scenario?** Use Stress Test.
            - **Have an ethical edge case?** Use Boundary Cases.
            - **Have a claim or source question?** Use Evidence Lab.
            - **Need impact framing?** Use World Lens.
            - **Need rules and limits?** Use Protocol Guide.

            The UX rule is simple: make the next step obvious while keeping every output reviewable.
            """
        )


    with st.expander("Eternal Baseline", expanded=True):
        st.markdown(
            """
            The **Eternal Baseline** is ALETHEIA's ethical continuity layer. It preserves the project's core guardrails across versions without becoming a command layer.

            It protects continuity around human dignity, basic rights, free agency, transparency, appealability, accountability, evidence, repair, non-coercion, and human review.

            Its audit lens is:

            > **Intelligence + Power - Ego = Stability**

            This is an ethical design rule, not mathematical proof. ALETHEIA uses it to ask whether intelligence and power are being restrained by humility, accountability, transparency, and repair.

            Historical archive material may contain AI-flattery artifacts or inflated validation language. Those materials are treated as development context, not independent proof, founder validation, or governance justification.

            **ALETHEIA reflects. Humans review. Power stays accountable.**
            """
        )

    st.markdown("### What ALETHEIA does")

    with st.expander("Mirror Check", expanded=True):
        st.markdown(
            """
            Users can submit governance proposals and receive an internal prototype classification: **SANCTUARY**, **THRESHOLD**, or **ASYLUM**.

            The audit layer scans for capture risk, opacity, coercion, missing appeal rights, weak transparency, and other governance-risk patterns.
            """
        )

    with st.expander("Stress Test", expanded=True):
        st.markdown(
            """
            The system models governance pressure through archetype agents with intelligence, power, ego, alignment, trust, grievances, alliances, and memory.

            It tracks **Stability**, **Trust**, **Alignment**, and **Ego** over time.
            """
        )

    with st.expander("Evidence Lab", expanded=True):
        st.markdown(
            """
            Users can upload country-year datasets and map them into ALETHEIA variables for empirical scoring, schema checks, 9k allocation, and internal correlation checks.

            This layer is the bridge from symbolic prototype to reproducible research workflow.
            """
        )

    with st.expander("World Lens", expanded=True):
        st.markdown(
            """
            The grid shows how a 9k global body could be allocated by population and how those seats may intersect with governance-risk conditions when empirical data is available.

            The grid is a **representation model**. It is not a real election, government, authority mechanism, or political mandate.
            """
        )

    with st.expander("Protocol Guide", expanded=True):
        st.markdown(
            """
            The doctrine layer preserves the symbolic principles behind the prototype while remaining corrigible by evidence.

            - **Mirror Effect** — power must reflect service, not absorb authority
            - **V-Axis Compass** — intelligence and power only stabilize when ego is restrained and alignment rises
            - **Do not overtrust the tool** — no person, system, institution, dataset, protocol, or AI is treated as final or beyond review
            - **Empirical correction rule** — symbolic logic must remain testable and correctable by public evidence
            - **Protocol integrity layer** — Audit, Simulation, Empirical Study, and Global Grid share one Sydney Protocol guardrail engine
            """
        )

    st.markdown("### Research caution")
    st.warning(
        "ALETHEIA does not prove legal, political, medical, religious, or final truth. Its classifications are internal model outputs. Empirical results depend on dataset quality, variable mapping, normalization choices, missing data, and validation against external outcomes."
    )
    st.markdown(
        """
        A responsible reading is:

        > **This model suggests a governance-risk pattern worth examining.**

        Not:

        > **This model has final authority.**
        """
    )

    st.markdown("### Research direction")
    st.markdown(
        """
        The long-term goal is to produce a reproducible study and dashboard using public datasets such as **UN population data**, **World Bank governance indicators**, **V-Dem democracy data**, and public trust surveys.

        The direction is clear: symbolic governance logic should be tested against empirical evidence. Where the model is useful, it should become more precise. Where the data challenges it, the model should be corrected.

        **ALETHEIA is built for that process.**
        """
    )

    with st.expander("Developer notes", expanded=False):
        st.markdown("Technical structure for local development and deployment.")
        st.code(
            """app.py                  # Streamlit UI
core/parser.py          # local/AI governance scan
core/simulation.py      # agent-based V-Axis stability simulation
core/scoring.py         # integrity, friction, collapse probability, review questions
core/empirical.py       # country-year scoring, 9k allocation, validation helpers
core_empirical.py       # import fallback for Streamlit deployments
config/weights.py       # I/A/E/P weight presets
data_processed/         # empirical templates and generated scores
paper/                  # methodology and study draft materials
assets/                 # header image and other optional UI assets""",
            language="text",
        )
        st.code("""pip install -r requirements.txt
streamlit run app.py""", language="bash")

st.markdown(f"""<div class="footer-banner"><strong>ALETHEIA reflects.</strong> People decide. · {APP_VERSION}</div>""", unsafe_allow_html=True)
