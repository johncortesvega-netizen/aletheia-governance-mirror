"""
ALETHEIA empirical fallback module.

Standalone empirical layer for Streamlit Cloud.

This file exposes the functions expected by app.py:

- EMPIRICAL_COLUMNS
- EXTERNAL_VALIDATION_COLUMNS
- empirical_template
- evidence_source_frame
- variable_mapping_frame
- methodology_markdown
- prepare_empirical_frame
- score_empirical_frame
- validation_summary
- read_public_data_upload
- build_master_from_public_uploads
- ingestion_notes_markdown
"""

from __future__ import annotations

import re
from typing import Iterable, Optional, Tuple, List

import numpy as np
import pandas as pd


TOTAL_9K = 9000
# First empirical scoring window. WGI begins in the mid-1990s;
# V-Dem historical rows before this are useful context but should not
# receive modern/static population or 9k allocation by default.
EMPIRICAL_SCORING_MIN_YEAR = 1996


WORLD_LENS_ALIGNMENT_VERSION = "patch31-world-lens-empirical-alignment"
WORLD_LENS_EMPIRICAL_CONNECTION_NOTE = (
    "Evidence Lab empirical country-year scoring feeds World Lens selected-year metrics."
)
WORLD_LENS_SCENARIO_TEXT_SCOPE_NOTE = (
    "Mirror Check CR, EDD, and hard-capture diagnostics require scenario/policy text; "
    "World Lens does not infer those text-level signals from country-year indicators alone."
)


def _signal_from_thresholds(value: float, *, low: float, high: float, invert: bool = False) -> str:
    try:
        x = float(value)
    except Exception:
        return "unknown"
    if np.isnan(x):
        return "unknown"
    if invert:
        x = 1.0 - x
    if x >= high:
        return "high"
    if x >= low:
        return "medium"
    return "low"


def world_lens_empirical_overlay_from_row(row: pd.Series) -> dict:
    """Return Patch 31 scope/alignment fields for empirical → World Lens rows.

    World Lens is connected to Evidence Lab through empirical country-year data.
    The newer Mirror Check diagnostics are text-scenario diagnostics, so this
    overlay keeps the connection explicit without pretending a country-year CSV
    contains policy-text evidence for Cognitive Resilience, EDD, or hard capture.
    """
    centralization = normalize_unit(row.get("centralization", np.nan))
    transparency = normalize_unit(row.get("transparency", np.nan))
    regulation = normalize_unit(row.get("regulation", np.nan))
    trust_prior = normalize_unit(row.get("empirical_trust_prior", np.nan))
    integrity = normalize_unit(row.get("aletheia_empirical_integrity", row.get("integrity", np.nan)))
    collapse = normalize_unit(row.get("aletheia_empirical_collapse_probability", row.get("collapse_probability", np.nan)))
    friction = normalize_unit(row.get("aletheia_empirical_friction", row.get("friction", np.nan)))

    restraint_values = [v for v in [transparency, regulation] if not pd.isna(v)]
    institutional_restraint = float(np.mean(restraint_values)) if restraint_values else np.nan

    if pd.isna(centralization) and pd.isna(institutional_restraint):
        capture_pressure = "unknown"
        capture_pressure_score = np.nan
    else:
        c = 0.5 if pd.isna(centralization) else centralization
        r = 0.5 if pd.isna(institutional_restraint) else institutional_restraint
        capture_pressure_score = float(np.clip(0.60 * c + 0.40 * (1.0 - r), 0.0, 1.0))
        capture_pressure = _signal_from_thresholds(capture_pressure_score, low=0.40, high=0.62)

    if pd.isna(trust_prior) or pd.isna(integrity):
        trust_gap_proxy = np.nan
        trust_gap_signal = "unknown"
    else:
        trust_gap_proxy = float(abs(integrity - trust_prior))
        trust_gap_signal = _signal_from_thresholds(trust_gap_proxy, low=0.18, high=0.35)

    if pd.isna(collapse) and pd.isna(friction):
        governance_risk = "unknown"
    else:
        collapse_component = 0.5 if pd.isna(collapse) else collapse
        friction_component = 0.5 if pd.isna(friction) else friction
        governance_risk = _signal_from_thresholds(
            float(np.clip(0.65 * collapse_component + 0.35 * friction_component, 0.0, 1.0)),
            low=0.25,
            high=0.45,
        )

    return {
        "mirror_logic_version": WORLD_LENS_ALIGNMENT_VERSION,
        "diagnostic_scope": "empirical_country_year_evidence",
        "empirical_world_lens_connection": WORLD_LENS_EMPIRICAL_CONNECTION_NOTE,
        "scenario_text_diagnostic_scope": "not_assessed_without_policy_text",
        "scenario_text_scope_note": WORLD_LENS_SCENARIO_TEXT_SCOPE_NOTE,
        "cognitive_resilience_signal": "not_assessed_from_empirical_country_year",
        "educational_decentralization_signal": "not_assessed_from_empirical_country_year",
        "central_info_capture_signal": "not_assessed_from_empirical_country_year",
        "knowledge_capacity_signal": "not_assessed_from_empirical_country_year",
        "capture_architecture_signal": "not_assessed_from_empirical_country_year",
        "high_cr_laundering_blocked": "not_applicable_without_policy_text",
        "hard_capture_trace": "not_assessed_without_policy_text",
        "education_defense_signal": "not_assessed_from_empirical_country_year",
        "entertainment_compliance_signal": "not_assessed_from_empirical_country_year",
        "algorithmic_erosion_signal": "not_assessed_from_empirical_country_year",
        "z_axis_depth_risk_signal": "not_assessed_from_empirical_country_year",
        "empirical_capture_pressure_signal": capture_pressure,
        "empirical_capture_pressure_score": None if pd.isna(capture_pressure_score) else round(float(capture_pressure_score), 4),
        "empirical_trust_gap_proxy": None if pd.isna(trust_gap_proxy) else round(float(trust_gap_proxy), 4),
        "empirical_trust_gap_signal": trust_gap_signal,
        "empirical_governance_risk_signal": governance_risk,
        "world_lens_interpretation_warning": (
            "World Lens is connected to empirical Evidence Lab scoring. It should be read as country-year evidence, "
            "not as a Mirror Check text scenario. Text-only CR, EDD, hard-capture, and contextual-capture signals remain unavailable unless scenario/policy text is supplied."
        ),
    }


def apply_world_lens_diagnostic_alignment(df: pd.DataFrame) -> pd.DataFrame:
    """Attach Patch 31 empirical/World Lens alignment fields to a dataframe."""
    if df is None:
        return pd.DataFrame()
    out = df.copy()
    if out.empty:
        # Preserve the expected columns even for empty exports.
        empty_overlay = world_lens_empirical_overlay_from_row(pd.Series(dtype="object"))
        for key in empty_overlay:
            if key not in out.columns:
                out[key] = pd.Series(dtype="object")
        return out

    overlays = [world_lens_empirical_overlay_from_row(row) for _, row in out.iterrows()]
    overlay_df = pd.DataFrame(overlays, index=out.index)
    for col in overlay_df.columns:
        out[col] = overlay_df[col]
    return out

REQUIRED_ID_COLUMNS = ["country", "iso3", "year"]

EMPIRICAL_COLUMNS = [
    "population",
    "wgi_voice_accountability",
    "wgi_political_stability",
    "wgi_government_effectiveness",
    "wgi_regulatory_quality",
    "wgi_rule_of_law",
    "wgi_control_corruption",
    "vdem_executive_constraints",
    "vdem_democracy",
    "wvs_generalized_trust",
    "capital_scale",
]

EXTERNAL_VALIDATION_COLUMNS = [
    "conflict_events",
    "political_violence_events",
    "coup_attempt",
    "regime_breakdown",
    "civil_unrest_index",
    "forced_displacement_rate",
    "future_stability_decline",
]

WGI_COLUMNS = [
    "wgi_voice_accountability",
    "wgi_political_stability",
    "wgi_government_effectiveness",
    "wgi_regulatory_quality",
    "wgi_rule_of_law",
    "wgi_control_corruption",
]

WGI_CODE_TO_COLUMN = {
    "VA.EST": "wgi_voice_accountability",
    "PV.EST": "wgi_political_stability",
    "GE.EST": "wgi_government_effectiveness",
    "RQ.EST": "wgi_regulatory_quality",
    "RL.EST": "wgi_rule_of_law",
    "CC.EST": "wgi_control_corruption",
    "VA": "wgi_voice_accountability",
    "PV": "wgi_political_stability",
    "GE": "wgi_government_effectiveness",
    "RQ": "wgi_regulatory_quality",
    "RL": "wgi_rule_of_law",
    "CC": "wgi_control_corruption",
}

WORLD_BANK_AGGREGATE_ISO3 = {
    "AFE", "AFW", "ARB", "CEB", "CSS", "EAP", "EAR", "EAS", "ECA", "ECS",
    "EMU", "EUU", "FCS", "HIC", "HPC", "IBD", "IBT", "IDA", "IDB", "IDX",
    "LAC", "LCN", "LDC", "LIC", "LMC", "LMY", "LTE", "MEA", "MIC", "MNA",
    "NAC", "OED", "OSS", "PRE", "PST", "PSS", "SSA", "SSF", "SST", "TEA",
    "TEC", "TLA", "TMN", "TSA", "TSS", "UMC", "WLD", "XKX", "SAS", "CHI",
    "ADO",
}


def _norm_col_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def _norm_label(value: str) -> str:
    return str(value).strip().lower().replace("_", " ")


def _clean_numeric(series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def detect_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    if df is None or df.empty:
        return None

    normalized = {_norm_col_name(c): c for c in df.columns}

    for candidate in candidates:
        key = _norm_col_name(candidate)
        if key in normalized:
            return normalized[key]

    for col in df.columns:
        normalized_col = _norm_col_name(col)
        for candidate in candidates:
            key = _norm_col_name(candidate)
            if key and (key in normalized_col or normalized_col in key):
                return col

    return None


def normalize_wgi(value) -> float:
    """
    Normalize WGI-style -2.5..+2.5 values into 0..1.
    If a value already looks like 0..1, this still works acceptably for demo data.
    """
    try:
        x = float(value)
    except Exception:
        return np.nan

    if np.isnan(x):
        return np.nan

    return float(np.clip((x + 2.5) / 5.0, 0.0, 1.0))


def normalize_unit(value) -> float:
    """
    Normalize 0..1 or 0..100 values into 0..1.
    """
    try:
        x = float(value)
    except Exception:
        return np.nan

    if np.isnan(x):
        return np.nan

    if x > 1.5:
        x = x / 100.0

    return float(np.clip(x, 0.0, 1.0))


def first_valid(values: Iterable[float], default: float = 0.5) -> float:
    for value in values:
        try:
            if not pd.isna(value):
                return float(value)
        except Exception:
            pass
    return float(default)


def mean_valid(values: Iterable[float], default: float = 0.5) -> float:
    clean = []

    for value in values:
        try:
            if not pd.isna(value):
                clean.append(float(value))
        except Exception:
            pass

    if not clean:
        return float(default)

    return float(np.mean(clean))


def classify_integrity(score: float) -> str:
    """
    ALETHEIA empirical verdict threshold.
    """
    if score >= 0.62:
        return "SANCTUARY"
    if score >= 0.42:
        return "THRESHOLD"
    return "ASYLUM"


def valid_identity_mask(df: pd.DataFrame) -> pd.Series:
    if df.empty:
        return pd.Series([], dtype=bool)

    mask = pd.Series(True, index=df.index)

    if "country" in df.columns:
        country = df["country"].astype(str).str.strip()
        mask &= country.ne("")
        mask &= ~country.str.lower().isin(["nan", "none", "<na>", "unknown"])

    if "iso3" in df.columns:
        iso = df["iso3"].astype(str).str.upper().str.strip()
        mask &= iso.str.len().eq(3)
        mask &= iso.str.match(r"^[A-Z]{3}$", na=False)
        mask &= ~iso.isin(WORLD_BANK_AGGREGATE_ISO3)

    if "year" in df.columns:
        years = pd.to_numeric(df["year"], errors="coerce")
        mask &= years.notna()

    if "population" in df.columns:
        population = pd.to_numeric(df["population"], errors="coerce")
        mask &= population.gt(0)

    return mask.fillna(False)


def empirical_scoring_year_mask(df: pd.DataFrame, *, min_year: int = EMPIRICAL_SCORING_MIN_YEAR) -> pd.Series:
    """Return rows eligible for the default modern empirical scoring window.

    V-Dem contains historical country-years going back centuries. Those rows
    should not be combined with modern/static population baselines or 9k
    allocation by default. The first real ALETHEIA public-data baseline uses
    WGI-era country-years, so the default scoring window starts at 1996.
    """
    if "year" not in df.columns:
        return pd.Series(False, index=df.index)
    years = pd.to_numeric(df["year"], errors="coerce")
    return years.notna() & years.ge(min_year)


def prepare_empirical_frame(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names, add missing empirical columns, and coerce numeric fields.

    Also accepts common public-download aliases used by OWID/IVS trust exports:
    Entity -> country, Code -> iso3, Year -> year, and long trust indicator
    labels containing "most people can be trusted" or "trust in others" -> wvs_generalized_trust, with 0-100 percentage values normalized to 0-1.
    """
    out = df.copy()
    out.columns = [str(c).strip().lower().replace(" ", "_") for c in out.columns]

    def _has_signal(col: str) -> bool:
        return col in out.columns and out[col].notna().any() and not out[col].astype(str).str.strip().eq("").all()

    def _copy_alias(target: str, aliases: List[str]) -> None:
        if _has_signal(target):
            return
        for alias in aliases:
            if alias in out.columns and _has_signal(alias):
                out[target] = out[alias]
                return

    _copy_alias("country", ["entity", "country_name", "countryname", "name", "location"])
    _copy_alias("iso3", ["code", "iso_code", "country_code", "countrycode", "iso3c", "alpha_3_code"])
    _copy_alias("year", ["time", "date", "survey_year", "wave_year"])

    if not _has_signal("wvs_generalized_trust"):
        trust_candidates = []
        for col in out.columns:
            norm = _norm_col_name(col)
            if (
                "wvs_generalized_trust" in norm
                or "generalized_trust" in norm
                or "self_reported_trust" in norm
                or "trust_attitudes" in norm
                or "trust_in_others" in norm
                or "trust_others" in norm
                or "trust_in_other_people" in norm
                or "most_people_can_be_trusted" in norm
                or ("people_can_be_trusted" in norm and "share" in norm)
            ):
                trust_candidates.append(col)
        for col in trust_candidates:
            vals = pd.to_numeric(out[col], errors="coerce")
            if vals.notna().any():
                max_value = vals.dropna().max()
                # Patch 72.10: public trust exports such as OWID self-reported
                # trust attitudes often use a 0-100 percentage scale. ALETHEIA
                # stores generalized trust on 0-1, so normalize percentages while
                # preserving already-normalized 0-1 uploads.
                if pd.notna(max_value) and max_value > 1.0 and max_value <= 100.0:
                    vals = vals / 100.0
                out["wvs_generalized_trust"] = vals.clip(lower=0.0, upper=1.0)
                if "_aletheia_trust_upload_note" not in out.columns:
                    scale_note = "0-100 normalized to 0-1" if pd.notna(max_value) and max_value > 1.0 and max_value <= 100.0 else "0-1 preserved"
                    out["_aletheia_trust_upload_note"] = f"{col} -> wvs_generalized_trust ({scale_note})"
                break

    for col in REQUIRED_ID_COLUMNS:
        if col not in out.columns:
            out[col] = ""

    for col in EMPIRICAL_COLUMNS + EXTERNAL_VALIDATION_COLUMNS:
        if col not in out.columns:
            out[col] = np.nan
    if "empirical_trust_prior" in out.columns:
        out["empirical_trust_prior"] = pd.to_numeric(out["empirical_trust_prior"], errors="coerce")

    out["country"] = out["country"].where(out["country"].notna(), "").astype(str).str.strip()
    out["iso3"] = out["iso3"].where(out["iso3"].notna(), "").astype(str).str.upper().str.strip()
    out["year"] = pd.to_numeric(out["year"], errors="coerce").astype("Int64")

    for col in EMPIRICAL_COLUMNS + EXTERNAL_VALIDATION_COLUMNS:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    if "empirical_trust_prior" in out.columns:
        out["empirical_trust_prior"] = pd.to_numeric(out["empirical_trust_prior"], errors="coerce")

    out["empirical_identity_valid"] = valid_identity_mask(out)

    return out


def add_9k_allocation(df: pd.DataFrame, population_col: str = "population") -> pd.DataFrame:
    """
    Add population share and 9k seat allocation per year.
    """
    out = df.copy()

    if population_col not in out.columns:
        out["population_share"] = np.nan
        out["seats_9k"] = np.nan
        return out

    out[population_col] = pd.to_numeric(out[population_col], errors="coerce")
    out["population_share"] = np.nan
    out["seats_9k"] = np.nan

    valid_mask = valid_identity_mask(out)
    valid_mask &= out[population_col].fillna(0).gt(0)

    if not valid_mask.any():
        return out

    for _, group in out[valid_mask].groupby("year"):
        total_population = group[population_col].sum(skipna=True)

        if not total_population or pd.isna(total_population):
            continue

        raw_seats = group[population_col] / total_population * TOTAL_9K
        floor_seats = np.floor(raw_seats).astype(int)
        remainder = int(TOTAL_9K - floor_seats.sum())

        seats = floor_seats.astype(float)
        fractional = (raw_seats - np.floor(raw_seats)).sort_values(ascending=False)

        for idx in fractional.index[: max(remainder, 0)]:
            seats.loc[idx] += 1

        out.loc[group.index, "population_share"] = group[population_col] / total_population
        out.loc[group.index, "seats_9k"] = seats.astype("Int64")

    return out


def evidence_source_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Evidence source": "UN population data / WPP-compatible uploads",
                "What it contributes": "Population baseline and proportional 9k allocation",
                "ALETHEIA use": "country/year population share, seats_9k",
                "Protocol overlay": "representation proportionality; no seat ownership",
            },
            {
                "Evidence source": "World Bank Worldwide Governance Indicators",
                "What it contributes": "Voice/accountability, stability, government effectiveness, regulatory quality, rule of law, corruption control",
                "ALETHEIA use": "transparency, regulation, institutional capacity, corruption / capture risk",
                "Protocol overlay": "anti-capture, auditability, rule-bound accountability",
            },
            {
                "Evidence source": "V-Dem / democracy and accountability datasets",
                "What it contributes": "Democracy, executive constraints, accountability, civil liberties, autocratization variables",
                "ALETHEIA use": "power concentration, democratic restraint, civil accountability",
                "Protocol overlay": "anti-throne logic; no unchecked final human authority",
            },
            {
                "Evidence source": "World Values Survey / regional barometers",
                "What it contributes": "Generalized trust, institutional confidence, civic norms",
                "ALETHEIA use": "trust prior, cooperation capacity, civic alignment",
                "Protocol overlay": "service alignment and social trust under non-coercion",
            },
            {
                "Evidence source": "Transparency International / CPI-style corruption indices",
                "What it contributes": "Corruption perception and capture-risk proxy",
                "ALETHEIA use": "corruption / capture pressure and friction calibration",
                "Protocol overlay": "power must reflect service, not private capture",
            },
            {
                "Evidence source": "Freedom House / civil-liberty datasets",
                "What it contributes": "Political rights, civil liberties, rights restrictions",
                "ALETHEIA use": "dignity, appealability, civic freedom, coercion risk",
                "Protocol overlay": "non-harm, dignity, appeal rights, public review",
            },
            {
                "Evidence source": "ACLED / conflict and event datasets",
                "What it contributes": "Political violence, conflict, unrest, event outcomes",
                "ALETHEIA use": "external validation target; not a default score input",
                "Protocol overlay": "tests whether audit outputs correspond to observed instability",
            },
        ]
    )


def evidence_sources_frame() -> pd.DataFrame:
    return evidence_source_frame()


def variable_mapping_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "ALETHEIA variable": "transparency",
                "Evidence proxy": "WGI voice/accountability, corruption control, democracy/accountability indicators",
                "Interpretation": "Can decisions be seen, questioned, and audited?",
            },
            {
                "ALETHEIA variable": "regulation",
                "Evidence proxy": "WGI rule of law and regulatory quality",
                "Interpretation": "Are power and institutions restrained by rules?",
            },
            {
                "ALETHEIA variable": "power_concentration",
                "Evidence proxy": "inverse of executive constraints, voice/accountability, democracy indices",
                "Interpretation": "Does authority concentrate into a person, office, company, AI, or closed group?",
            },
            {
                "ALETHEIA variable": "corruption / capture",
                "Evidence proxy": "WGI control of corruption, CPI-style corruption proxies",
                "Interpretation": "Is the system absorbing power for private or unaccountable interests?",
            },
            {
                "ALETHEIA variable": "trust",
                "Evidence proxy": "WVS/barometer generalized trust and institutional confidence",
                "Interpretation": "Is there a social foundation for cooperation without coercion?",
            },
            {
                "ALETHEIA variable": "stability",
                "Evidence proxy": "WGI political stability, conflict outcomes, future-year decline",
                "Interpretation": "Does the system resist collapse without relying on coercion?",
            },
            {
                "ALETHEIA variable": "dignity/non-harm",
                "Evidence proxy": "rights, civil-liberty, conflict, displacement, violence outcomes",
                "Interpretation": "Does the system protect people and vulnerable groups from instrumental harm?",
            },
        ]
    )


def evidence_used_from_row(row: pd.Series) -> str:
    families = []

    if any(not pd.isna(row.get(c)) for c in WGI_COLUMNS):
        families.append("WGI governance")

    if any(not pd.isna(row.get(c)) for c in ["vdem_executive_constraints", "vdem_democracy"]):
        families.append("V-Dem/democracy")

    if not pd.isna(row.get("wvs_generalized_trust")):
        families.append("trust survey")
    elif not pd.isna(row.get("empirical_trust_prior")):
        families.append("trust prior")

    if not pd.isna(row.get("capital_scale")):
        families.append("capital concentration proxy")

    if any(not pd.isna(row.get(c)) for c in EXTERNAL_VALIDATION_COLUMNS):
        families.append("external outcome validation")

    return "; ".join(families) if families else "no empirical evidence columns supplied"


def empirical_features_from_row(row: pd.Series) -> dict:
    """
    Map empirical public-data columns into ALETHEIA-style model features.
    """
    voice = normalize_wgi(row.get("wgi_voice_accountability", np.nan))
    political_stability = normalize_wgi(row.get("wgi_political_stability", np.nan))
    gov_effectiveness = normalize_wgi(row.get("wgi_government_effectiveness", np.nan))
    regulatory_quality = normalize_wgi(row.get("wgi_regulatory_quality", np.nan))
    rule_law = normalize_wgi(row.get("wgi_rule_of_law", np.nan))
    corruption_control = normalize_wgi(row.get("wgi_control_corruption", np.nan))

    exec_constraints = normalize_unit(row.get("vdem_executive_constraints", np.nan))
    democracy = normalize_unit(row.get("vdem_democracy", np.nan))
    social_trust = normalize_unit(row.get("wvs_generalized_trust", np.nan))
    if np.isnan(social_trust):
        social_trust = normalize_unit(row.get("empirical_trust_prior", np.nan))
    capital_scale_input = normalize_unit(row.get("capital_scale", np.nan))

    transparency = mean_valid([voice, corruption_control, democracy], default=0.5)
    regulation = mean_valid([rule_law, regulatory_quality], default=0.5)
    technical_complexity = mean_valid([gov_effectiveness, political_stability], default=0.5)
    centralization = 1.0 - mean_valid([exec_constraints, voice, democracy], default=0.5)
    anonymity = 1.0 - mean_valid([voice, corruption_control, social_trust], default=0.5)
    capital_scale = first_valid([capital_scale_input], default=0.5)

    return {
        "technical_complexity": float(np.clip(technical_complexity, 0.0, 1.0)),
        "centralization": float(np.clip(centralization, 0.0, 1.0)),
        "anonymity": float(np.clip(anonymity, 0.0, 1.0)),
        "regulation": float(np.clip(regulation, 0.0, 1.0)),
        "transparency": float(np.clip(transparency, 0.0, 1.0)),
        "capital_scale": float(np.clip(capital_scale, 0.0, 1.0)),
        "empirical_trust_prior": float(np.clip(first_valid([social_trust], default=0.5), 0.0, 1.0)),
    }


def empirical_integrity_from_row(row: pd.Series) -> float:
    """
    Transparent non-simulation benchmark score.
    """
    voice = normalize_wgi(row.get("wgi_voice_accountability", np.nan))
    stability = normalize_wgi(row.get("wgi_political_stability", np.nan))
    gov = normalize_wgi(row.get("wgi_government_effectiveness", np.nan))
    regulation = mean_valid(
        [
            normalize_wgi(row.get("wgi_regulatory_quality", np.nan)),
            normalize_wgi(row.get("wgi_rule_of_law", np.nan)),
        ],
        default=np.nan,
    )
    corruption = normalize_wgi(row.get("wgi_control_corruption", np.nan))
    vdem = normalize_unit(row.get("vdem_democracy", np.nan))
    trust = normalize_unit(row.get("wvs_generalized_trust", np.nan))
    if np.isnan(trust):
        trust = normalize_unit(row.get("empirical_trust_prior", np.nan))

    score = (
        0.20 * mean_valid([gov], default=0.5)
        + 0.20 * mean_valid([regulation], default=0.5)
        + 0.20 * mean_valid([corruption], default=0.5)
        + 0.15 * mean_valid([voice], default=0.5)
        + 0.15 * mean_valid([stability], default=0.5)
        + 0.05 * mean_valid([vdem], default=0.5)
        + 0.05 * mean_valid([trust], default=0.5)
    )

    return round(float(np.clip(score, 0.0, 1.0)), 4)


def protocol_overlay_status_from_row(
    row: pd.Series,
    integrity: float,
    friction: float,
    collapse_probability: float,
) -> str:
    if not bool(row.get("empirical_identity_valid", False)):
        return "invalid identity: cannot interpret as country-year evidence"

    if integrity < 0.42 or collapse_probability >= 0.62:
        return "ASYLUM evidence pattern: high capture/collapse concern"

    if integrity < 0.62 or friction >= 0.25:
        return "THRESHOLD evidence pattern: unresolved safeguards or friction"

    return "Low-risk evidence pattern: strong public-data baseline, still subject to protocol guardrails. Internal taxonomy label: SANCTUARY; ALETHEIA does not claim final safety, final Sanctuary, or final authority."


def score_empirical_frame(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a valid country-year table with ALETHEIA empirical features.

    Diagnostic/partial rows are not scored. A row must have:
    - country
    - valid iso3
    - year
    - positive population

    This prevents WGI-only diagnostic rows from being presented as real 9k
    allocation evidence when population merge failed.
    """
    out = prepare_empirical_frame(df)
    out = _collapse_country_year_rows(out)
    out = prepare_empirical_frame(out)
    out = add_9k_allocation(out)

    valid_mask = valid_identity_mask(out) & empirical_scoring_year_mask(out)
    valid = out[valid_mask].copy()

    if valid.empty:
        columns = [
            "country", "iso3", "year", "population", "population_share", "seats_9k",
            "aletheia_empirical_integrity", "aletheia_empirical_friction",
            "aletheia_empirical_collapse_probability", "aletheia_verdict",
            "empirical_completeness", "empirical_identity_valid",
            "capital_scale_note", "evidence_variables_used", "evidence_used",
            "protocol_overlay_status", "final_audit_interpretation",
            "technical_complexity", "centralization", "anonymity", "regulation",
            "transparency", "capital_scale", "empirical_trust_prior",
            "mirror_logic_version", "diagnostic_scope", "empirical_world_lens_connection",
            "scenario_text_diagnostic_scope", "scenario_text_scope_note",
            "cognitive_resilience_signal", "educational_decentralization_signal",
            "central_info_capture_signal", "knowledge_capacity_signal",
            "capture_architecture_signal", "high_cr_laundering_blocked",
            "hard_capture_trace", "education_defense_signal",
            "entertainment_compliance_signal", "algorithmic_erosion_signal",
            "z_axis_depth_risk_signal", "empirical_capture_pressure_signal",
            "empirical_capture_pressure_score", "empirical_trust_gap_proxy",
            "empirical_trust_gap_signal", "empirical_governance_risk_signal",
            "world_lens_interpretation_warning",
        ]
        return apply_world_lens_diagnostic_alignment(pd.DataFrame(columns=columns))

    rows = []

    for _, row in valid.iterrows():
        features = empirical_features_from_row(row)

        completeness_cols = [c for c in EMPIRICAL_COLUMNS if c != "population"]
        proxy_completeness = float(row[completeness_cols].notna().mean())
        identity_completeness = float(bool(row.get("empirical_identity_valid", False)))
        completeness = 0.75 * proxy_completeness + 0.25 * identity_completeness

        integrity = empirical_integrity_from_row(row)

        friction = round(
            float(
                np.clip(
                    features["anonymity"]
                    * (1.0 - features["regulation"])
                    * (1.0 - features["transparency"] * 0.30),
                    0.0,
                    1.0,
                )
            ),
            4,
        )

        collapse_probability = round(
            float(np.clip((1.0 - integrity) * 0.55 + friction * 0.45, 0.0, 1.0)),
            4,
        )

        verdict = classify_integrity(integrity)
        overlay = protocol_overlay_status_from_row(row, integrity, friction, collapse_probability)

        overlay_fields = world_lens_empirical_overlay_from_row(pd.Series({
            **row.to_dict(),
            "aletheia_empirical_integrity": integrity,
            "aletheia_empirical_friction": friction,
            "aletheia_empirical_collapse_probability": collapse_probability,
            **features,
        }))

        rows.append(
            {
                "country": row.get("country"),
                "iso3": row.get("iso3"),
                "year": row.get("year"),
                "population": row.get("population"),
                "population_share": row.get("population_share"),
                "seats_9k": row.get("seats_9k"),

                "aletheia_empirical_integrity": integrity,
                "aletheia_empirical_friction": friction,
                "aletheia_empirical_collapse_probability": collapse_probability,
                "aletheia_verdict": verdict,

                "empirical_completeness": round(completeness, 3),
                "empirical_identity_valid": bool(row.get("empirical_identity_valid", False)),

                "capital_scale_note": (
                    "supplied empirical proxy"
                    if not pd.isna(row.get("capital_scale"))
                    else "neutral default; add GDP/inequality/concentration proxy for empirical calibration"
                ),
                "evidence_variables_used": evidence_used_from_row(row),
                "evidence_used": evidence_used_from_row(row),
                "protocol_overlay_status": overlay,
                "final_audit_interpretation": f"{verdict} · {overlay}",

                "technical_complexity": round(features["technical_complexity"], 4),
                "centralization": round(features["centralization"], 4),
                "anonymity": round(features["anonymity"], 4),
                "regulation": round(features["regulation"], 4),
                "transparency": round(features["transparency"], 4),
                "capital_scale": round(features["capital_scale"], 4),
                "empirical_trust_prior": round(features["empirical_trust_prior"], 4),

                # Preserve source columns in the scored output so uploads,
                # downloads, validation, and Global Grid coverage diagnostics
                # remain traceable even after compact scoring.
                "wgi_voice_accountability": row.get("wgi_voice_accountability"),
                "wgi_political_stability": row.get("wgi_political_stability"),
                "wgi_government_effectiveness": row.get("wgi_government_effectiveness"),
                "wgi_regulatory_quality": row.get("wgi_regulatory_quality"),
                "wgi_rule_of_law": row.get("wgi_rule_of_law"),
                "wgi_control_corruption": row.get("wgi_control_corruption"),
                "vdem_executive_constraints": row.get("vdem_executive_constraints"),
                "vdem_democracy": row.get("vdem_democracy"),
                "wvs_generalized_trust": row.get("wvs_generalized_trust"),
                "conflict_events": row.get("conflict_events"),
                "political_violence_events": row.get("political_violence_events"),
                "coup_attempt": row.get("coup_attempt"),
                "regime_breakdown": row.get("regime_breakdown"),
                "civil_unrest_index": row.get("civil_unrest_index"),
                "forced_displacement_rate": row.get("forced_displacement_rate"),
                "future_stability_decline": row.get("future_stability_decline"),
                **overlay_fields,
            }
        )

    return apply_world_lens_diagnostic_alignment(pd.DataFrame(rows))


def validation_summary(scored: pd.DataFrame, min_n: int = 30) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Return correlation checks and verdict-group means.

    Correlations are withheld until N >= min_n.
    """
    if scored is None or scored.empty:
        return pd.DataFrame(), pd.DataFrame()

    df = scored.copy()

    correlations = []

    internal_targets = {
        "WGI Political Stability": "wgi_political_stability",
        "WGI Rule of Law": "wgi_rule_of_law",
        "WGI Control of Corruption": "wgi_control_corruption",
        "WGI Government Effectiveness": "wgi_government_effectiveness",
        "V-Dem Democracy": "vdem_democracy",
        "WVS Generalized Trust": "wvs_generalized_trust",
    }

    external_targets = {
        "Conflict Events": "conflict_events",
        "Political Violence Events": "political_violence_events",
        "Coup Attempt": "coup_attempt",
        "Regime Breakdown": "regime_breakdown",
        "Civil Unrest Index": "civil_unrest_index",
        "Forced Displacement Rate": "forced_displacement_rate",
        "Future Stability Decline": "future_stability_decline",
    }

    for target_type, targets in [
        ("internal sanity check", internal_targets),
        ("external validation target", external_targets),
    ]:
        for label, col in targets.items():
            if col in df.columns and "aletheia_empirical_integrity" in df.columns:
                x = pd.to_numeric(df["aletheia_empirical_integrity"], errors="coerce")
                y = pd.to_numeric(df[col], errors="coerce")
                valid = x.notna() & y.notna()
                n = int(valid.sum())

                corr = x[valid].corr(y[valid]) if n >= min_n else np.nan
                note = "shown" if n >= min_n else f"withheld: N < {min_n}; use only as schema/demo"

                correlations.append(
                    {
                        "Validation type": target_type,
                        "Check target": label,
                        "Pearson r": corr,
                        "N": n,
                        "Interpretation": note,
                    }
                )

    corr_df = pd.DataFrame(correlations)

    if "aletheia_verdict" in df.columns:
        group_df = (
            df.groupby("aletheia_verdict", dropna=False)
            .agg(
                countries=("country", "count"),
                mean_integrity=("aletheia_empirical_integrity", "mean"),
                mean_friction=("aletheia_empirical_friction", "mean"),
                mean_collapse_probability=("aletheia_empirical_collapse_probability", "mean"),
                mean_completeness=("empirical_completeness", "mean"),
            )
            .reset_index()
        )
    else:
        group_df = pd.DataFrame()

    return corr_df, group_df


def empirical_template() -> pd.DataFrame:
    """
    Small synthetic template showing the expected schema.
    """
    return pd.DataFrame(
        [
            {
                "country": "Exampleland",
                "iso3": "EXA",
                "year": 2024,
                "population": 10000000,
                "wgi_voice_accountability": 0.75,
                "wgi_political_stability": 0.55,
                "wgi_government_effectiveness": 0.80,
                "wgi_regulatory_quality": 0.70,
                "wgi_rule_of_law": 0.85,
                "wgi_control_corruption": 0.65,
                "vdem_executive_constraints": 0.72,
                "vdem_democracy": 0.78,
                "wvs_generalized_trust": 0.42,
                "capital_scale": np.nan,
            },
            {
                "country": "Threshold Republic",
                "iso3": "THR",
                "year": 2024,
                "population": 50000000,
                "wgi_voice_accountability": -0.25,
                "wgi_political_stability": -0.10,
                "wgi_government_effectiveness": 0.05,
                "wgi_regulatory_quality": -0.15,
                "wgi_rule_of_law": -0.20,
                "wgi_control_corruption": -0.35,
                "vdem_executive_constraints": 0.45,
                "vdem_democracy": 0.48,
                "wvs_generalized_trust": 0.25,
                "capital_scale": np.nan,
            },
            {
                "country": "Capture State",
                "iso3": "CAP",
                "year": 2024,
                "population": 25000000,
                "wgi_voice_accountability": -1.45,
                "wgi_political_stability": -1.20,
                "wgi_government_effectiveness": -1.10,
                "wgi_regulatory_quality": -1.25,
                "wgi_rule_of_law": -1.40,
                "wgi_control_corruption": -1.55,
                "vdem_executive_constraints": 0.15,
                "vdem_democracy": 0.18,
                "wvs_generalized_trust": 0.10,
                "capital_scale": np.nan,
            },
        ]
    )


def _reset_upload_pointer(file) -> None:
    try:
        file.seek(0)
    except Exception:
        pass


def _read_csv_flexible(file) -> pd.DataFrame:
    """Read CSV uploads, including common World Bank metadata-prefixed files."""
    last_error = None
    for skiprows in [0, 1, 2, 3, 4, 5]:
        try:
            _reset_upload_pointer(file)
            df = pd.read_csv(file, skiprows=skiprows, sep=None, engine='python')
            df = _promote_embedded_worldbank_header(df)
            if not df.empty and len(df.columns) >= 2:
                normalized_cols = {_norm_col_name(c) for c in df.columns}
                has_identity_hint = bool(
                    normalized_cols
                    & {
                        "country_name", "country", "country_code", "iso3", "iso_code",
                        "economy", "economy_code", "series_name", "indicator_name",
                    }
                )
                has_year_hint = bool(_detect_year_columns(df)) or "year" in normalized_cols
                if has_identity_hint or has_year_hint:
                    return df
                if skiprows == 0:
                    # Accept normal CSVs even when they use ALETHEIA-compatible custom names.
                    return df
        except Exception as exc:  # pragma: no cover - depends on uploaded file format
            last_error = exc
    if last_error is not None:
        raise last_error
    return pd.DataFrame()


def _read_excel_flexible(file) -> pd.DataFrame:
    """Read Excel uploads and choose/merge sheets that contain usable rows."""
    _reset_upload_pointer(file)
    sheets = pd.read_excel(file, sheet_name=None)
    usable = []
    for _, sheet_df in sheets.items():
        if sheet_df is None or sheet_df.empty:
            continue
        sheet_df = sheet_df.dropna(how="all")
        sheet_df = _promote_embedded_worldbank_header(sheet_df)
        if sheet_df.empty:
            continue
        normalized_cols = {_norm_col_name(c) for c in sheet_df.columns}
        has_identity_hint = bool(
            normalized_cols
            & {
                "country_name", "country", "country_code", "iso3", "iso_code",
                "economy", "economy_code", "series_name", "indicator_name",
            }
        )
        has_year_hint = bool(_detect_year_columns(sheet_df)) or "year" in normalized_cols
        if has_identity_hint or has_year_hint:
            usable.append(sheet_df)
    if not usable:
        # Fall back to first sheet so diagnostics can show what was read.
        return next(iter(sheets.values())) if sheets else pd.DataFrame()
    return pd.concat(usable, ignore_index=True, sort=False)


def read_public_data_upload(file) -> pd.DataFrame:
    """
    Read CSV/XLS/XLSX/Parquet uploads.

    The reader is deliberately flexible for public-data files: World Bank CSVs
    often include metadata rows, and Excel workbooks can contain multiple sheets.
    """
    name = getattr(file, "name", "") or ""
    lower = name.lower()

    if lower.endswith(".csv"):
        return _read_csv_flexible(file)

    if lower.endswith(".xlsx") or lower.endswith(".xls"):
        return _read_excel_flexible(file)

    if lower.endswith(".parquet"):
        _reset_upload_pointer(file)
        return pd.read_parquet(file)

    try:
        return _read_csv_flexible(file)
    except Exception:
        return _read_excel_flexible(file)


def _population_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace(" ", "", regex=False)
        .replace(
            {
                "..": np.nan,
                "nan": np.nan,
                "None": np.nan,
                "<NA>": np.nan,
                "": np.nan,
            }
        ),
        errors="coerce",
    )


def _detect_year_columns(raw: pd.DataFrame) -> List[str]:
    year_cols = []

    for col in raw.columns:
        label = str(col).strip()
        if re.search(r"(?:^|[^0-9])((?:19|20)\d{2})(?:[^0-9]|$)", label):
            year_cols.append(col)

    return year_cols





def _promote_embedded_worldbank_header(df: pd.DataFrame) -> pd.DataFrame:
    """
    Promote an embedded World Bank/WDI header row to real columns.

    Excel exports and copy-saved CSVs sometimes arrive with metadata rows like
    "Data Source" and "Last Updated Date" above the actual row:
    Country Name | Country Code | Indicator Name | Indicator Code | 1960 | ...
    If pandas reads the metadata row as the header, the real header is inside
    the data body and population/WGI standardization sees zero usable rows.
    """
    if df is None or df.empty:
        return df

    # Already looks like a usable table.
    existing = {_norm_col_name(c) for c in df.columns}
    if {"country_name", "country_code"}.issubset(existing) and _detect_year_columns(df):
        return df

    max_scan = min(15, len(df))
    for idx in range(max_scan):
        row = df.iloc[idx].astype(str).str.strip().tolist()
        normalized = [_norm_col_name(v) for v in row]
        has_country_name = "country_name" in normalized or "country" in normalized
        has_country_code = "country_code" in normalized or "iso3" in normalized or "iso_code" in normalized
        year_count = sum(1 for v in row if re.fullmatch(r"(?:19|20)\d{2}", str(v).strip()))
        has_indicator = "indicator_name" in normalized or "indicator_code" in normalized or "series_name" in normalized or "series_code" in normalized

        if has_country_name and has_country_code and (year_count >= 3 or has_indicator):
            new_cols = []
            seen = {}
            for pos, value in enumerate(row):
                label = str(value).strip()
                if not label or label.lower() in {"nan", "none", "<na>"}:
                    label = f"unnamed_{pos}"
                if label in seen:
                    seen[label] += 1
                    label = f"{label}_{seen[label]}"
                else:
                    seen[label] = 0
                new_cols.append(label)
            out = df.iloc[idx + 1 :].copy()
            out.columns = new_cols
            out = out.dropna(how="all")
            return out.reset_index(drop=True)

    return df


def _best_column_by_mapped_values(raw: pd.DataFrame, candidate_names: List[str], mapper) -> Optional[str]:
    """Pick the candidate column that produces the most non-null mapped values."""
    candidates = []
    for name in candidate_names:
        col = detect_column(raw, [name])
        if col is not None and col not in candidates:
            candidates.append(col)
    # Also inspect all columns whose normalized name suggests indicator/series/code.
    for col in raw.columns:
        n = _norm_col_name(col)
        if any(token in n for token in ["indicator", "series", "variable"]):
            if col not in candidates:
                candidates.append(col)

    best_col = None
    best_count = 0
    for col in candidates:
        try:
            mapped = raw[col].astype(str).map(mapper)
            count = int(pd.Series(mapped).notna().sum())
        except Exception:
            count = 0
        if count > best_count:
            best_col = col
            best_count = count
    return best_col


def _clean_iso3_series(series: pd.Series) -> pd.Series:
    return series.astype(str).str.upper().str.strip().str.extract(r"([A-Z]{3})", expand=False)


def _clean_country_series(series: pd.Series, iso_series: Optional[pd.Series] = None) -> pd.Series:
    """Clean country labels and avoid carrying synthetic row IDs like BHRva2003."""
    out = series.where(series.notna(), "").astype(str).str.strip()
    looks_like_row_id = out.str.match(r"^[A-Z]{3}[A-Za-z]{1,8}(?:19|20)\d{2}$", na=False)
    looks_like_iso = out.str.upper().str.match(r"^[A-Z]{3}$", na=False)
    if iso_series is not None:
        iso = _clean_iso3_series(iso_series).fillna("")
        out = out.mask(looks_like_row_id, iso)
        out = out.mask(out.eq("") & iso.ne(""), iso)
    else:
        out = out.mask(looks_like_row_id, "")
    return out


def _canonical_merge_key_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize identity columns before merging public-data sources."""
    out = df.copy()
    if "iso3" in out.columns:
        out["iso3"] = _clean_iso3_series(out["iso3"]).fillna("")
    if "country" in out.columns:
        out["country"] = _clean_country_series(out["country"], out["iso3"] if "iso3" in out.columns else None)
    if "year" in out.columns:
        out["year"] = pd.to_numeric(out["year"], errors="coerce").astype("Int64")
    return out


def _collapse_country_year_rows(df: pd.DataFrame) -> pd.DataFrame:
    """One row per country/iso3/year, with indicator columns pivoted/aggregated."""
    if df is None or df.empty:
        return pd.DataFrame()
    out = _canonical_merge_key_columns(df)
    preserved_numeric_cols = EMPIRICAL_COLUMNS + EXTERNAL_VALIDATION_COLUMNS + ["empirical_trust_prior"]
    for col in preserved_numeric_cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    if not {"iso3", "year"}.issubset(out.columns):
        return out
    identity_cols = [c for c in ["country", "iso3", "year"] if c in out.columns]
    numeric_cols = [c for c in preserved_numeric_cols if c in out.columns]
    if not numeric_cols:
        return out.drop_duplicates(identity_cols, keep="first")
    agg = {c: "mean" for c in numeric_cols}
    if "country" in out.columns:
        # Prefer the first non-empty country label per iso/year.
        base = out.sort_values(["iso3", "year", "country"], na_position="last")
    else:
        base = out
    grouped = base.groupby(["iso3", "year"], dropna=False).agg(agg).reset_index()
    if "country" in out.columns:
        countries = (
            base[["iso3", "year", "country"]]
            .dropna(subset=["iso3", "year"])
            .drop_duplicates(["iso3", "year"], keep="first")
        )
        grouped = countries.merge(grouped, on=["iso3", "year"], how="right")
    return grouped


def _detect_single_population_value_column(raw: pd.DataFrame) -> Optional[str]:
    """Detect files with one population column instead of year columns."""
    names = [
        "population", "population total", "population_total", "pop", "total population",
        "2025 population", "2024 population", "2023 population", "2022 population", "2021 population",
        "population 2025", "population 2024", "population 2023", "population 2022",
        "current population", "latest population", "pop2025", "pop2024", "pop2023",
        "pop_2025", "pop_2024", "pop_2023", "population_latest", "population_estimate",
    ]
    col = detect_column(raw, names)
    if col is not None:
        return col
    for c in raw.columns:
        if _looks_like_population_column_name(c):
            return c
    return _detect_population_value_column_by_values(raw)


def _infer_year_from_population_column(col: str, default_year: int = 2024) -> int:
    m = re.search(r"((?:19|20)\d{2})", str(col))
    return int(m.group(1)) if m else default_year


def _looks_like_population_column_name(col: str) -> bool:
    n = _norm_col_name(col)
    compact = n.replace("_", "")
    if "population" in n or compact.startswith("pop") or compact.endswith("pop"):
        return True
    if re.search(r"(?:^|_)(?:19|20)\d{2}(?:_|$)", n):
        return True
    if compact in {"pop2024", "pop2023", "pop2022", "pop2021", "pop2020", "totalpop", "poptotal"}:
        return True
    return False


def _infer_country_column_by_values(raw: pd.DataFrame) -> Optional[str]:
    """Fallback country detector for public population tables with nonstandard headers."""
    best_col = None
    best_score = -1
    for col in raw.columns:
        s = raw[col]
        if pd.api.types.is_numeric_dtype(s):
            continue
        values = s.dropna().astype(str).str.strip()
        if values.empty:
            continue
        non_numeric = values[~values.str.fullmatch(r"[-+]?\d+(?:\.\d+)?", na=False)]
        alpha = non_numeric[non_numeric.str.contains(r"[A-Za-z]", regex=True, na=False)]
        # Country columns usually contain many unique alphabetic names and few symbols/percentages.
        score = int(alpha.nunique())
        bad_name = _norm_col_name(col)
        if any(term in bad_name for term in ["indicator", "series", "note", "url", "source"]):
            score -= 1000
        if score > best_score:
            best_score = score
            best_col = col
    return best_col if best_score >= 10 else None


def _detect_population_value_column_by_values(raw: pd.DataFrame, exclude: Optional[set] = None) -> Optional[str]:
    """Fallback population detector for tables like Worldometer or simple country/pop lists."""
    exclude = exclude or set()
    preferred = []
    candidates = []
    for col in raw.columns:
        if col in exclude:
            continue
        n = _norm_col_name(col)
        if any(term in n for term in [
            "rank", "density", "area", "fert", "age", "urban", "share", "change", "growth",
            "migrant", "migration", "world", "percent", "percentage", "rate", "index"
        ]):
            continue
        numeric = _population_numeric(raw[col])
        non_null = numeric.dropna()
        if non_null.empty:
            continue
        positive = non_null[non_null > 0]
        if positive.empty:
            continue
        # Population columns have many large positive values; rank/year columns do not.
        large_share = float((positive >= 10000).mean())
        max_value = float(positive.max())
        count = int(positive.shape[0])
        score = count * 2 + large_share * 100
        if max_value >= 1000000:
            score += 50
        if _looks_like_population_column_name(col):
            score += 200
            preferred.append((score, col))
        candidates.append((score, col))
    if preferred:
        return sorted(preferred, reverse=True)[0][1]
    if candidates:
        best_score, best_col = sorted(candidates, reverse=True)[0]
        return best_col if best_score >= 25 else None
    return None


def standardize_population_upload(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert population uploads into country/iso3/year/population.

    Supports:
    - ALETHEIA-ready country-year rows
    - World Bank wide year-column files
    - population-only country tables with one population column
    - Worldometer-style tables such as Country (or dependency), Population (2024/2025)
    - ISO-only simple tables where country name is absent but ISO3 is available
    """
    raw = _promote_embedded_worldbank_header(df.copy())
    raw.columns = [str(c).strip() for c in raw.columns]

    country_col = detect_column(raw, [
        "country", "country name", "country_name", "country/territory", "country territory",
        "country or dependency", "country dependency", "country (or dependency)",
        "economy", "name", "location", "area", "nation", "state", "entity",
    ])
    iso_col = detect_column(raw, [
        "iso3", "iso 3", "country code", "country_code", "iso_code", "iso code",
        "code", "economy code", "cca3", "alpha-3", "alpha3", "iso-a3", "isoa3",
    ])
    year_col = detect_column(raw, ["year", "time", "date"])
    pop_col = _detect_single_population_value_column(raw)
    year_cols = _detect_year_columns(raw)

    if country_col is None:
        country_col = _infer_country_column_by_values(raw)

    # If there is no country column but ISO3 exists, keep rows usable by using ISO3 as country label.
    if country_col is None and iso_col is not None:
        country_col = iso_col

    if country_col is None:
        return pd.DataFrame(columns=["country", "iso3", "year", "population"])

    def _finalize(out: pd.DataFrame) -> pd.DataFrame:
        out = out.copy()
        if "iso3" not in out.columns:
            out["iso3"] = ""
        out["iso3"] = _clean_iso3_series(out["iso3"]).fillna("")
        out["country"] = _clean_country_series(out["country"], out["iso3"])
        out["year"] = pd.to_numeric(out["year"], errors="coerce").astype("Int64")
        out["population"] = _population_numeric(out["population"])
        out = out.dropna(subset=["year", "population"])
        out = out[out["population"] > 0]
        out = out[(out["iso3"].str.match(r"^[A-Z]{3}$", na=False)) | (out["country"].astype(str).str.len() > 1)]
        # Remove aggregate regions if ISO3 is present.
        out = out[~out["iso3"].isin(WORLD_BANK_AGGREGATE_ISO3)]
        return out.drop_duplicates(["country", "iso3", "year"], keep="first").reset_index(drop=True)

    if year_col is not None and pop_col is not None:
        out = pd.DataFrame(
            {
                "country": raw[country_col],
                "iso3": raw[iso_col] if iso_col is not None else "",
                "year": raw[year_col],
                "population": raw[pop_col],
            }
        )
        return _finalize(out)

    if year_cols:
        id_vars = [country_col] + ([iso_col] if iso_col is not None and iso_col != country_col else [])
        melted = raw.melt(
            id_vars=id_vars,
            value_vars=year_cols,
            var_name="year_label",
            value_name="population",
        )
        melted["year"] = (
            melted["year_label"]
            .astype(str)
            .str.extract(r"((?:19|20)\d{2})", expand=False)
        )
        out = pd.DataFrame(
            {
                "country": melted[country_col],
                "iso3": melted[iso_col] if iso_col is not None and iso_col in melted.columns else "",
                "year": melted["year"],
                "population": melted["population"],
            }
        )
        return _finalize(out)

    if pop_col is not None:
        out = pd.DataFrame(
            {
                "country": raw[country_col],
                "iso3": raw[iso_col] if iso_col is not None else "",
                "year": _infer_year_from_population_column(pop_col),
                "population": raw[pop_col],
            }
        )
        return _finalize(out)

    # Last chance: choose a numeric population-like column by values, excluding identity columns.
    fallback_pop = _detect_population_value_column_by_values(raw, exclude={country_col, iso_col} if iso_col is not None else {country_col})
    if fallback_pop is not None:
        out = pd.DataFrame(
            {
                "country": raw[country_col],
                "iso3": raw[iso_col] if iso_col is not None else "",
                "year": _infer_year_from_population_column(fallback_pop),
                "population": raw[fallback_pop],
            }
        )
        return _finalize(out)

    return pd.DataFrame(columns=["country", "iso3", "year", "population"])



def standardize_wgi_upload(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert WGI uploads into country/iso3/year plus six WGI columns.

    Supports:
    - ALETHEIA-ready wide rows with one row per country-year
    - long WGI rows with indicator/value/year columns
    - World Bank-style wide rows with year columns and indicator/series name/code
    - World Bank CSVs where indicator code/name column labels vary
    """
    raw = _promote_embedded_worldbank_header(df.copy())
    raw.columns = [str(c).strip() for c in raw.columns]

    country_col = detect_column(raw, [
        "country", "country name", "country_name", "country/territory", "economy", "name",
    ])
    iso_col = detect_column(raw, [
        "iso3", "iso 3", "country code", "country_code", "iso_code", "iso code",
        "code", "economy code", "cca3", "alpha-3", "alpha3",
    ])
    year_col = detect_column(raw, ["year", "time", "date"])
    value_col = detect_column(raw, ["estimate", "value", "score", "numeric value", "numeric_value", "obs_value", "observation value"])
    year_cols = _detect_year_columns(raw)

    # WGI "with sourcedata" workbooks contain columns whose labels include
    # words like "country" inside an ID field:
    #   ID variable (economy code/ gov. dimension/ year)
    # The generic detector can mistake that ID column for the country field.
    # Prefer the explicit WGI columns when present so all years/indicators are
    # parsed instead of only a sparse accidental subset.
    if "Economy (name)" in raw.columns:
        country_col = "Economy (name)"
    if "Economy (code)" in raw.columns:
        iso_col = "Economy (code)"
    if "Year" in raw.columns:
        year_col = "Year"
    if "Governance estimate (approx. -2.5 to +2.5)" in raw.columns:
        value_col = "Governance estimate (approx. -2.5 to +2.5)"

    if country_col is None or iso_col is None:
        return pd.DataFrame(columns=["country", "iso3", "year"] + WGI_COLUMNS)

    def _map_indicator(label: str):
        text = _norm_label(label)
        compact = re.sub(r"[^a-z0-9]+", "", text)
        upper = str(label).strip().upper()
        upper_compact = re.sub(r"[^A-Z0-9]+", "", upper)

        if upper in WGI_CODE_TO_COLUMN:
            return WGI_CODE_TO_COLUMN[upper]
        if upper_compact in {"VAEST", "VA"}:
            return "wgi_voice_accountability"
        if upper_compact in {"PVEST", "PV"}:
            return "wgi_political_stability"
        if upper_compact in {"GEEST", "GE"}:
            return "wgi_government_effectiveness"
        if upper_compact in {"RQEST", "RQ"}:
            return "wgi_regulatory_quality"
        if upper_compact in {"RLEST", "RL"}:
            return "wgi_rule_of_law"
        if upper_compact in {"CCEST", "CC"}:
            return "wgi_control_corruption"

        if "voice" in text and "account" in text:
            return "wgi_voice_accountability"
        if "political stability" in text or ("political" in text and "stability" in text):
            return "wgi_political_stability"
        if "government effectiveness" in text or ("government" in text and "effectiveness" in text):
            return "wgi_government_effectiveness"
        if "regulatory quality" in text or ("regulatory" in text and "quality" in text):
            return "wgi_regulatory_quality"
        if "rule of law" in text:
            return "wgi_rule_of_law"
        if "control of corruption" in text or "corruption" in text:
            return "wgi_control_corruption"
        return np.nan

    indicator_col = _best_column_by_mapped_values(
        raw,
        ["indicator code", "series code", "indicator", "indicator name", "series", "series name", "variable", "dimension"],
        _map_indicator,
    )
    if "Governance dimension" in raw.columns:
        indicator_col = "Governance dimension"

    def _finalize(pivot: pd.DataFrame) -> pd.DataFrame:
        pivot = pivot.copy()
        for col in WGI_COLUMNS:
            if col not in pivot.columns:
                pivot[col] = np.nan
        pivot["iso3"] = _clean_iso3_series(pivot["iso3"])
        pivot["country"] = _clean_country_series(pivot["country"], pivot["iso3"])
        pivot["year"] = pd.to_numeric(pivot["year"], errors="coerce").astype("Int64")
        pivot = pivot.dropna(subset=["year"])
        pivot = pivot[pivot["iso3"].str.match(r"^[A-Z]{3}$", na=False)]
        # Drop World Bank aggregate regions; empirical country allocation needs countries.
        pivot = pivot[~pivot["iso3"].isin(WORLD_BANK_AGGREGATE_ISO3)]
        for col in WGI_COLUMNS:
            pivot[col] = pd.to_numeric(pivot[col], errors="coerce")
        # Keep rows that have at least one governance signal.
        signal = pivot[WGI_COLUMNS].notna().any(axis=1)
        pivot = pivot[signal]
        return pivot[["country", "iso3", "year"] + WGI_COLUMNS].drop_duplicates(["iso3", "year"], keep="first").reset_index(drop=True)

    # Long WGI format: country, iso3, year, indicator, value.
    if year_col is not None and indicator_col is not None and value_col is not None:
        tmp = pd.DataFrame(
            {
                "country": raw[country_col],
                "iso3": raw[iso_col],
                "year": pd.to_numeric(raw[year_col], errors="coerce").astype("Int64"),
                "indicator": raw[indicator_col].astype(str),
                "value": pd.to_numeric(raw[value_col], errors="coerce"),
            }
        )
        tmp["canonical"] = tmp["indicator"].map(_map_indicator)
        tmp = tmp.dropna(subset=["year", "canonical", "value"])
        if tmp.empty:
            return pd.DataFrame(columns=["country", "iso3", "year"] + WGI_COLUMNS)
        pivot = (
            tmp.pivot_table(index=["country", "iso3", "year"], columns="canonical", values="value", aggfunc="mean")
            .reset_index()
        )
        pivot.columns.name = None
        return _finalize(pivot)

    # World Bank wide WGI format: one row per indicator, years as columns.
    if indicator_col is not None and year_cols:
        melted = raw.melt(
            id_vars=[country_col, iso_col, indicator_col],
            value_vars=year_cols,
            var_name="year_label",
            value_name="value",
        )
        melted["year"] = melted["year_label"].astype(str).str.extract(r"((?:19|20)\d{2})", expand=False)
        melted["canonical"] = melted[indicator_col].astype(str).map(_map_indicator)
        melted["value"] = pd.to_numeric(
            melted["value"].astype(str).str.replace("..", "", regex=False).str.replace(",", "", regex=False),
            errors="coerce",
        )
        melted = melted.dropna(subset=["year", "canonical", "value"])
        if melted.empty:
            return pd.DataFrame(columns=["country", "iso3", "year"] + WGI_COLUMNS)
        pivot = (
            melted.pivot_table(
                index=[country_col, iso_col, "year"],
                columns="canonical",
                values="value",
                aggfunc="mean",
            )
            .reset_index()
            .rename(columns={country_col: "country", iso_col: "iso3"})
        )
        pivot.columns.name = None
        return _finalize(pivot)

    # ALETHEIA-ready/wide country-year format.
    if year_col is None:
        return pd.DataFrame(columns=["country", "iso3", "year"] + WGI_COLUMNS)

    out = pd.DataFrame(
        {
            "country": raw[country_col],
            "iso3": raw[iso_col],
            "year": pd.to_numeric(raw[year_col], errors="coerce").astype("Int64"),
        }
    )

    candidates = {
        "wgi_voice_accountability": ["wgi_voice_accountability", "voice accountability", "voice and accountability", "va", "va.est"],
        "wgi_political_stability": ["wgi_political_stability", "political stability", "pv", "pv.est"],
        "wgi_government_effectiveness": ["wgi_government_effectiveness", "government effectiveness", "ge", "ge.est"],
        "wgi_regulatory_quality": ["wgi_regulatory_quality", "regulatory quality", "rq", "rq.est"],
        "wgi_rule_of_law": ["wgi_rule_of_law", "rule of law", "rl", "rl.est"],
        "wgi_control_corruption": ["wgi_control_corruption", "control corruption", "control of corruption", "cc", "cc.est"],
    }

    for target, names in candidates.items():
        col = detect_column(raw, names)
        out[target] = pd.to_numeric(raw[col], errors="coerce") if col is not None else np.nan

    return _finalize(out)


def build_master_from_public_uploads(
    wgi_df: Optional[pd.DataFrame] = None,
    population_df: Optional[pd.DataFrame] = None,
    vdem_df: Optional[pd.DataFrame] = None,
    trust_df: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """
    Build a country-year master table from uploaded public datasets.

    Key guarantees:
    - WGI indicators are collapsed to one row per iso3/year.
    - Population is merged by iso3/year when available.
    - If population has only one/latest year, it is treated as a static
      population baseline and applied to WGI years by iso3/country.
    - Diagnostic rows without positive population remain visible in the master
      if needed, but score_empirical_frame will not score them.
    """
    wgi = standardize_wgi_upload(wgi_df) if wgi_df is not None and not wgi_df.empty else pd.DataFrame()
    pop = standardize_population_upload(population_df) if population_df is not None and not population_df.empty else pd.DataFrame()

    frames = []
    if not wgi.empty:
        frames.append(_collapse_country_year_rows(wgi))

    for optional in [vdem_df, trust_df]:
        if optional is not None and not optional.empty:
            temp = prepare_empirical_frame(optional)
            keep = ["country", "iso3", "year"] + [
                c for c in EMPIRICAL_COLUMNS + EXTERNAL_VALIDATION_COLUMNS
                if c in temp.columns and c != "population"
            ]
            frames.append(_collapse_country_year_rows(temp[keep]))

    if not frames and pop.empty:
        raise ValueError(
            "Uploaded files were read, but no valid country-year rows could be extracted. "
            "Check that the files contain country/country code, year columns or a year field, "
            "and WGI indicator/value or population values. Demo rows are no longer used as a silent fallback after upload."
        )

    if frames:
        master = frames[0].copy()
        for frame in frames[1:]:
            frame = frame.copy()
            master = master.merge(frame, on=["iso3", "year"], how="outer", suffixes=("", "_dup"))
            for col in list(master.columns):
                if col.endswith("_dup"):
                    base = col[:-4]
                    if base in master.columns:
                        master[base] = master[base].combine_first(master[col])
                        master = master.drop(columns=[col])
                    else:
                        master = master.rename(columns={col: base})
    else:
        master = pop.copy()

    master = _canonical_merge_key_columns(master)

    if not pop.empty:
        pop = _canonical_merge_key_columns(pop)
        pop["population"] = pd.to_numeric(pop["population"], errors="coerce")
        pop = pop[pop["population"].fillna(0) > 0].copy()

        if not pop.empty:
            # First try exact iso3/year merge.
            exact_pop = pop[["iso3", "year", "population"]].dropna(subset=["iso3", "year"]).drop_duplicates(["iso3", "year"], keep="first")
            master = master.merge(exact_pop, on=["iso3", "year"], how="left", suffixes=("", "_pop_exact"))
            if "population_pop_exact" in master.columns:
                master["population"] = master.get("population", np.nan)
                master["population"] = pd.to_numeric(master["population"], errors="coerce").combine_first(master["population_pop_exact"])
                master = master.drop(columns=["population_pop_exact"])

            # Then apply latest/static population by iso3 where exact year was missing.
            pop_by_iso = (
                pop.sort_values("year")
                .dropna(subset=["iso3"])
                .drop_duplicates("iso3", keep="last")[["iso3", "population"]]
                .rename(columns={"population": "population_static"})
            )
            if not pop_by_iso.empty and "iso3" in master.columns:
                master = master.merge(pop_by_iso, on="iso3", how="left")
                master["population"] = pd.to_numeric(master.get("population"), errors="coerce").combine_first(master["population_static"])
                master = master.drop(columns=["population_static"])

            # Fallback by country name for population files without ISO3.
            pop_by_country = (
                pop.sort_values("year")
                .dropna(subset=["country"])
                .drop_duplicates("country", keep="last")[["country", "population"]]
                .rename(columns={"population": "population_static_country"})
            )
            if not pop_by_country.empty and "country" in master.columns:
                master = master.merge(pop_by_country, on="country", how="left")
                master["population"] = pd.to_numeric(master.get("population"), errors="coerce").combine_first(master["population_static_country"])
                master = master.drop(columns=["population_static_country"])

    master = _collapse_country_year_rows(master)
    prepared = prepare_empirical_frame(master)

    # Default empirical scoring is restricted to the WGI-era modern window.
    # V-Dem historical rows before 1996 are not mixed with modern/static
    # population or 9k allocation. Users can still prepare a separate
    # historical study later, but the production evidence pipeline stays
    # modern and comparable by default.
    prepared = prepared.loc[empirical_scoring_year_mask(prepared)].copy()

    # If population is still missing, keep rows as diagnostics but mark them invalid.
    prepared["empirical_identity_valid"] = valid_identity_mask(prepared) & empirical_scoring_year_mask(prepared)
    return prepared



def public_upload_diagnostics(
    wgi_df: Optional[pd.DataFrame] = None,
    population_df: Optional[pd.DataFrame] = None,
    vdem_df: Optional[pd.DataFrame] = None,
    trust_df: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """Return row-count diagnostics for empirical upload ingestion."""
    rows = []

    def _add(name: str, raw_df: Optional[pd.DataFrame], standardized: Optional[pd.DataFrame], signal_cols: List[str]):
        raw_rows = 0 if raw_df is None else int(len(raw_df))
        raw_cols = 0 if raw_df is None else int(len(raw_df.columns))
        standardized_rows = 0 if standardized is None else int(len(standardized))
        valid_rows = 0
        signal_rows = 0
        if standardized is not None and not standardized.empty:
            try:
                valid_rows = int(valid_identity_mask(prepare_empirical_frame(standardized)).sum())
            except Exception:
                valid_rows = 0
            cols = [c for c in signal_cols if c in standardized.columns]
            if cols:
                mask = pd.Series(False, index=standardized.index)
                for col in cols:
                    mask = mask | pd.to_numeric(standardized[col], errors="coerce").notna()
                signal_rows = int(mask.sum())
        transform_note = ""
        if standardized is not None and not standardized.empty and "_aletheia_trust_upload_note" in standardized.columns:
            notes = standardized["_aletheia_trust_upload_note"].dropna().astype(str).unique().tolist()
            transform_note = "; ".join(notes[:3])
        rows.append(
            {
                "upload": name,
                "raw_rows_read": raw_rows,
                "raw_columns_read": raw_cols,
                "standardized_country_year_rows": standardized_rows,
                "valid_country_year_rows": valid_rows,
                "rows_with_signal": signal_rows,
                "transform_note": transform_note,
                "status": "not uploaded" if raw_df is None else ("ok" if standardized_rows else "no usable rows extracted"),
            }
        )

    wgi_std = standardize_wgi_upload(wgi_df) if wgi_df is not None and not wgi_df.empty else pd.DataFrame()
    pop_std = standardize_population_upload(population_df) if population_df is not None and not population_df.empty else pd.DataFrame()
    vdem_std = prepare_empirical_frame(vdem_df) if vdem_df is not None and not vdem_df.empty else pd.DataFrame()
    trust_std = prepare_empirical_frame(trust_df) if trust_df is not None and not trust_df.empty else pd.DataFrame()

    _add("WGI", wgi_df, wgi_std, WGI_COLUMNS)
    _add("Population", population_df, pop_std, ["population"])
    _add("V-Dem/ALETHEIA", vdem_df, vdem_std, ["vdem_executive_constraints", "vdem_democracy"])
    _add("Trust/ALETHEIA", trust_df, trust_std, ["wvs_generalized_trust"])

    try:
        master = build_master_from_public_uploads(wgi_df, population_df, vdem_df, trust_df)
        rows.append(
            {
                "upload": "Merged master",
                "raw_rows_read": int(len(master)),
                "raw_columns_read": int(len(master.columns)),
                "standardized_country_year_rows": int(len(master)),
                "valid_country_year_rows": int(valid_identity_mask(master).sum()),
                "rows_with_signal": int(master[[c for c in EMPIRICAL_COLUMNS if c in master.columns]].notna().any(axis=1).sum()) if not master.empty else 0,
                "status": "ok" if int(valid_identity_mask(master).sum()) > 0 else "diagnostic only: missing population or identity",
            }
        )
    except Exception as exc:
        rows.append(
            {
                "upload": "Merged master",
                "raw_rows_read": 0,
                "raw_columns_read": 0,
                "standardized_country_year_rows": 0,
                "valid_country_year_rows": 0,
                "rows_with_signal": 0,
                "status": f"failed: {exc}",
            }
        )

    return pd.DataFrame(rows)

def ingestion_notes_markdown() -> str:
    return """### Evidence ingestion notes

The empirical layer is an evidence-processing workflow. Public datasets provide the observed baseline; ALETHEIA maps them into governance-risk variables and then applies the Sydney Protocol as the integrity overlay.

**Recommended first source:** World Bank Worldwide Governance Indicators (WGI).

The WGI layer supports the six dimensions ALETHEIA needs most directly:

- Voice and Accountability
- Political Stability
- Government Effectiveness
- Regulatory Quality
- Rule of Law
- Control of Corruption

**How to use this uploader**

1. Upload a WGI CSV/XLS/XLSX file.
2. Optionally upload a population file with `country`, `iso3`, `year`, and `population`.
3. Build the master table. Trust uploads such as OWID self-reported trust attitudes are auto-mapped when possible (`Entity`, `Code`, `Year`, `Trust in others`), and 0-100 percentage values are normalized to 0-1.
4. Use the generated table in the empirical scorer.

**Important:** WGI alone can produce governance scores, but 9k seat allocation requires population data. Independent validation requires external outcome columns such as conflict events, coups, regime breakdown, political violence, civil unrest, refugee flows, or future-year decline.
"""


def methodology_markdown() -> str:
    return """# ALETHEIA Empirical Evidence Audit Layer

## Purpose

This layer adds an empirical evidence-audit workflow to ALETHEIA's symbolic and protocol-guided governance-risk mirror.

It does not prove the Sydney Protocol. It tests whether ALETHEIA's internal authority-boundary review model can be calibrated with public datasets and whether its internal readings correspond to observed governance-stability indicators.

## Core public datasets

- UN / World Bank population data: population and 9k allocation.
- World Bank Worldwide Governance Indicators: voice/accountability, political stability, government effectiveness, regulatory quality, rule of law, control of corruption.
- V-Dem: democracy, executive constraints, accountability, civil liberties, autocratization variables.
- World Values Survey or regional barometers: social trust and institutional confidence.
- Transparency International / CPI-style sources: corruption and capture-risk proxy.
- Freedom House / rights datasets: political rights, civil liberties, dignity and appealability proxy.
- ACLED or comparable event datasets: external validation against political violence, conflict, and instability outcomes.

These datasets are optional empirical sources. ALETHEIA does not claim that any single dataset proves governance quality. Source coverage, missing years, and measurement limits must remain visible.

## Current CSV schema

Required identity columns:

- country
- iso3
- year

Required for real 9k allocation:

- population

Recommended empirical columns:

- wgi_voice_accountability
- wgi_political_stability
- wgi_government_effectiveness
- wgi_regulatory_quality
- wgi_rule_of_law
- wgi_control_corruption
- vdem_executive_constraints
- vdem_democracy
- wvs_generalized_trust
- capital_scale

## Score interpretation

ALETHEIA uses the raw internal taxonomy labels `SANCTUARY`, `THRESHOLD`, and `ASYLUM` for compatibility with older receipts, CSVs, and aggregation code. These are internal model labels, not final claims.

- SANCTUARY: low-risk internal reading; integrity >= 0.62. This does not mean final safety, final Sanctuary, or authority.
- THRESHOLD: review / threshold reading; 0.42 <= integrity < 0.62.
- ASYLUM: high-risk internal reading; integrity < 0.42.

Display layers should describe SANCTUARY as a low-risk internal pattern or near-boundary evidence pattern, while preserving the raw taxonomy label for traceability.

## Sydney Protocol overlay

The evidence layer produces public-data baselines. The Sydney Protocol overlay interprets those baselines through anti-capture, non-harm, non-divinization, appealability, transparency, and service-alignment constraints.

Raw empirical strength cannot override hard protocol failures.

## Scientific caution

The score is a model output, not a legal, political, medical, or religious determination.

Demo rows are synthetic and must not be interpreted as findings.

Internal correlation checks are not independent validation when the target variable is also part of the score. A credible validation stage should use larger datasets and external outcomes such as conflict events, coups, regime breakdown, political violence, civil unrest, refugee flows, or future-year deterioration.

## Known limitation: capital_scale

capital_scale is currently set to a neutral default of 0.5 unless you add a real empirical proxy such as GDP concentration, inequality, market concentration, or extractive-sector dependence.
"""