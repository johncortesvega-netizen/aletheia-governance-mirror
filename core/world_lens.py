"""World Lens helper utilities.

Patch 61C keeps country-year selection country-scoped: year controls must
show only years that are actually available for the selected country, and must
not silently fall back to a global/default year.
"""
from __future__ import annotations

from typing import Iterable

import pandas as pd


def _truthy_identity(series: pd.Series | None, index: pd.Index) -> pd.Series:
    """Return a safe identity-valid mask for optional identity columns."""
    if series is None:
        return pd.Series(True, index=index)
    aligned = series.reindex(index)
    if aligned.dtype == bool:
        return aligned.fillna(False)
    text = aligned.astype(str).str.strip().str.lower()
    return text.isin(["true", "1", "yes", "y", "valid"])


def country_available_years(df: pd.DataFrame, iso3: str) -> list[int]:
    """Return years that exist for one selected country/ISO3 only.

    This deliberately ignores the global year range. It is used by the
    Country-Year Explorer so selecting a country cannot silently reuse a stale
    year from another country or a global default year.
    """
    if df is None or df.empty:
        return []
    required = {"iso3", "year"}
    if not required.issubset(set(df.columns)):
        return []

    out = df.copy()
    iso = str(iso3 or "").strip().upper()
    if not iso:
        return []

    identity_col = None
    if "empirical_identity_valid" in out.columns:
        identity_col = out["empirical_identity_valid"]
    elif "identity_valid" in out.columns:
        identity_col = out["identity_valid"]
    identity_mask = _truthy_identity(identity_col, out.index)

    out["_iso3_norm"] = out["iso3"].astype(str).str.strip().str.upper()
    out["_year_int"] = pd.to_numeric(out["year"], errors="coerce")
    out = out.loc[identity_mask & out["_iso3_norm"].eq(iso) & out["_year_int"].notna()].copy()
    if out.empty:
        return []
    return sorted(out["_year_int"].astype(int).unique().tolist(), reverse=True)


def country_year_status_message(country_name: str, iso3: str, years: Iterable[int]) -> str:
    """Human-readable country-scoped year availability label."""
    years_list = sorted({int(y) for y in years}, reverse=True)
    label = f"{str(country_name or iso3).strip()} · {str(iso3 or '').strip().upper()}".strip(" ·")
    if not years_list:
        return f"No available country-year data for {label}."

    ascending = sorted(years_list)
    contiguous = len(ascending) == (ascending[-1] - ascending[0] + 1)
    if contiguous and len(ascending) > 2:
        year_text = f"{ascending[0]}–{ascending[-1]}"
    else:
        year_text = ", ".join(str(y) for y in years_list)
    return f"Available years for {label}: {year_text}."


def safe_country_year_index(session_value: object, years: list[int]) -> int:
    """Return a safe selectbox index without falling back to stale/global years."""
    if not years:
        return 0
    try:
        value = int(session_value)
    except (TypeError, ValueError):
        return 0
    return years.index(value) if value in years else 0


def _coerce_optional_float(value: object) -> float | None:
    """Return a finite float or None for missing World Lens values."""
    try:
        series = pd.to_numeric(pd.Series([value]), errors="coerce")
        num = series.iloc[0]
    except Exception:
        return None
    if pd.isna(num):
        return None
    return float(num)


def format_raw_trust_label(value: object) -> str:
    """Display raw trust as observed evidence, never as an ambiguous dash."""
    num = _coerce_optional_float(value)
    if num is None:
        return "not available"
    return f"{num:.3f}"


def format_trust_prior_label(value: object) -> str:
    """Display trust prior while making neutral/default substitution explicit."""
    num = _coerce_optional_float(value)
    if num is None:
        return "not available"
    if abs(num - 0.5) <= 1e-9:
        return "0.500 neutral default"
    return f"{num:.3f}"


def trust_coverage_label(raw_coverage: object, prior_coverage: object) -> tuple[str, str, str]:
    """Return clear coverage labels for raw trust vs neutral-prior fallback.

    Raw trust is observed survey evidence. Trust prior coverage can include
    neutral/default substitutions and must not be read as observed trust.
    """
    raw = _coerce_optional_float(raw_coverage)
    prior = _coerce_optional_float(prior_coverage)
    raw_text = "—" if raw is None else f"{raw:.1%}"
    prior_text = "—" if prior is None else f"{prior:.1%}"
    note = (
        "Trust prior coverage is fallback/model coverage, not observed survey trust coverage. "
        "When raw trust is unavailable, ALETHEIA may use a neutral 0.500 prior for continuity."
    )
    return raw_text, prior_text, note

def _first_existing_column(df: pd.DataFrame, names: list[str]) -> str | None:
    """Return the first present column name from a candidate list."""
    for name in names:
        if name in df.columns:
            return name
    return None


def selected_year_value_guard(
    df: pd.DataFrame,
    selected_year: int,
    *,
    total_9k: int = 9000,
    min_allocated_countries: int = 100,
    focus_iso3: str | None = "NLD",
) -> dict:
    """Return deterministic World Lens guard diagnostics for one selected year.

    This helper makes World Lens interpretation testable without relying on
    Streamlit state. It deliberately examines only rows from ``selected_year``
    so charts/cards cannot silently reuse a previous country/year or global
    default value.
    """
    if df is None or df.empty or "year" not in df.columns:
        return {
            "selected_year": int(selected_year),
            "rows": 0,
            "allocated_countries": 0,
            "zero_seat_rows": 0,
            "total_seats": 0,
            "seat_total_ok": False,
            "full_selected_year_grid": False,
            "no_stale_year_rows": True,
            "focus_row_available": False,
            "focus": {},
            "verdict_seats": {},
        }

    out = df.copy()
    out["_year_int_guard"] = pd.to_numeric(out["year"], errors="coerce")
    year_rows = out.loc[out["_year_int_guard"].eq(int(selected_year))].copy()
    no_stale = bool(year_rows.empty or year_rows["_year_int_guard"].eq(int(selected_year)).all())

    seats_col = _first_existing_column(year_rows, ["seats_9k", "allocated_seats", "seats"]) if not year_rows.empty else None
    if seats_col:
        seats = pd.to_numeric(year_rows[seats_col], errors="coerce").fillna(0).astype(int)
    else:
        seats = pd.Series(0, index=year_rows.index, dtype="int64")
    allocated_mask = seats.gt(0)
    total_seats = int(seats.sum()) if not year_rows.empty else 0
    allocated_countries = (
        int(year_rows.loc[allocated_mask, "iso3"].dropna().astype(str).str.upper().nunique())
        if "iso3" in year_rows.columns
        else int(allocated_mask.sum())
    )
    zero_seat_rows = int(seats.le(0).sum()) if not year_rows.empty else 0
    seat_total_ok = abs(total_seats - int(total_9k)) <= 5

    verdict_col = _first_existing_column(year_rows, ["aletheia_verdict", "verdict", "protocol_adjusted_state"]) if not year_rows.empty else None
    verdict_seats: dict[str, int] = {}
    if verdict_col and seats_col:
        temp = year_rows.copy()
        temp["_guard_seats"] = seats
        for key, val in temp.groupby(verdict_col, dropna=False)["_guard_seats"].sum().items():
            verdict_seats[str(key)] = int(val)

    focus: dict = {}
    focus_available = False
    iso = str(focus_iso3 or "").strip().upper()
    if iso and "iso3" in year_rows.columns and not year_rows.empty:
        focus_rows = year_rows.loc[year_rows["iso3"].astype(str).str.strip().str.upper().eq(iso)].copy()
        if not focus_rows.empty:
            focus_available = True
            row = focus_rows.iloc[0]
            integrity_col = _first_existing_column(focus_rows, ["aletheia_empirical_integrity", "integrity"])
            collapse_col = _first_existing_column(focus_rows, ["aletheia_empirical_collapse_probability", "collapse_probability"])
            raw_trust_col = _first_existing_column(focus_rows, ["wvs_generalized_trust", "raw_trust", "trust_raw"])
            trust_prior_col = _first_existing_column(focus_rows, ["empirical_trust_prior", "trust_prior"])
            country_col = _first_existing_column(focus_rows, ["country", "country_name", "name"])
            focus = {
                "country": str(row.get(country_col, iso)) if country_col else iso,
                "iso3": iso,
                "year": int(selected_year),
                "seats": int(pd.to_numeric(pd.Series([row.get(seats_col, 0)]), errors="coerce").fillna(0).iloc[0]) if seats_col else 0,
                "verdict": str(row.get(verdict_col, "")) if verdict_col else "",
                "integrity": _coerce_optional_float(row.get(integrity_col)) if integrity_col else None,
                "collapse_probability": _coerce_optional_float(row.get(collapse_col)) if collapse_col else None,
                "raw_trust_label": format_raw_trust_label(row.get(raw_trust_col)) if raw_trust_col else "not available",
                "trust_prior_label": format_trust_prior_label(row.get(trust_prior_col)) if trust_prior_col else "not available",
            }

    return {
        "selected_year": int(selected_year),
        "rows": int(len(year_rows)),
        "allocated_countries": allocated_countries,
        "zero_seat_rows": zero_seat_rows,
        "total_seats": total_seats,
        "seat_total_ok": seat_total_ok,
        "full_selected_year_grid": bool(allocated_countries >= int(min_allocated_countries) and seat_total_ok),
        "no_stale_year_rows": no_stale,
        "focus_row_available": focus_available,
        "focus": focus,
        "verdict_seats": verdict_seats,
    }

