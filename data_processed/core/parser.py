import os
import json
import re
import streamlit as st
try:
    from openai import OpenAI
except Exception:
    OpenAI = None


# Patch 07 — Invisibility Filter / actor decoupling
# This helper is intentionally pure and opt-in. It does not change parser behavior
# unless a caller explicitly passes the returned decoupled_text into a scan.
ACTOR_ROLE_TERMS = [
    "president", "prime minister", "minister", "king", "queen", "emperor",
    "supreme leader", "leader", "ruler", "dictator", "mayor", "governor",
    "ceo", "founder", "chair", "chairman", "chairwoman", "director",
    "commander", "general", "judge", "senator", "representative",
]


def decouple_actor(query: str):
    """
    Strip obvious actor identifiers from a scenario before logical audit.

    ALETHEIA should examine the structure of a proposal, not defer to the
    status, reputation, or ego-weight of the named actor. This function returns
    a small dictionary instead of silently mutating input so callers can decide
    when to use it and can still show that the Invisibility Filter was applied.

    It is deliberately conservative: it removes common names, handles, emails,
    and title+name patterns, but it does not remove governance-risk terms like
    "president", "leader", "company", or "ministry" when they appear alone.
    Those role words may be relevant to the capture analysis.
    """

    original = "" if query is None else str(query)
    text = original
    redactions = []

    def redact(pattern, placeholder, label, flags=0):
        nonlocal text
        hits = []

        def repl(match):
            value = match.group(0)
            hits.append(value)
            return placeholder

        text = re.sub(pattern, repl, text, flags=flags)
        if hits:
            redactions.append({"label": label, "count": len(hits)})

    # Highly specific identifiers first.
    redact(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", "[CONTACT]", "email", flags=re.IGNORECASE)
    redact(r"(?<!\w)@[A-Za-z0-9_]{2,30}\b", "[HANDLE]", "handle")

    # Title + name, e.g. "President Jane Doe" or "CEO Sam Altman".
    role_pattern = "|".join(re.escape(term) for term in sorted(ACTOR_ROLE_TERMS, key=len, reverse=True))
    redact(
        rf"\b(?i:(?:{role_pattern}))\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){{0,3}})\b",
        "[ROLE_ACTOR]",
        "role_actor",
    )

    # Common Western-style personal names. Kept after title+name so the role
    # itself can remain visible in cases where it matters.
    redact(
        r"\b[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b",
        "[ACTOR]",
        "named_actor",
    )

    # Collapse repeated placeholders caused by adjacent matches.
    text = re.sub(r"(?:\[ACTOR\]\s*){2,}", "[ACTOR] ", text).strip()
    text = re.sub(r"\s{2,}", " ", text).strip()

    return {
        "original_text": original,
        "decoupled_text": text,
        "invisibility_filter_applied": text != original,
        "redaction_count": sum(item["count"] for item in redactions),
        "redactions": redactions,
    }


def _safe_float(value, default=0.5):
    try:
        value = float(value)
        return max(0.0, min(1.0, value))
    except Exception:
        return default


def _clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))


def _local_governance_scan(query: str):
    """
    Free local fallback scanner.
    Produces the same governance fields as the OpenAI parser.
    """

    text = query.lower()

    central_terms = [
        "central", "centralized", "centralised", "one leader", "one world leader",
        "world leader", "single leader", "single authority", "supreme leader",
        "king", "ruler", "dictator", "command", "boss", "authority", "empire",
        "rule the world", "runs the world", "global ruler", "top-down"
    ]

    transparency_terms = [
        "transparent", "transparency", "open", "public", "audited", "accountable",
        "visible", "published", "explainable", "traceable", "shared ledger"
    ]

    secrecy_terms = [
        "secret", "hidden", "opaque", "closed", "private control", "behind closed doors",
        "anonymous leadership", "unknown leadership", "unaccountable"
    ]

    regulation_terms = [
        "regulated", "oversight", "checks and balances", "audit", "audited",
        "law", "legal", "constitutional", "public review", "independent review",
        "accountability", "jury", "referendum"
    ]

    anti_regulation_terms = [
        "no oversight", "unregulated", "without oversight", "no rules",
        "free from regulation", "unchecked", "absolute power"
    ]

    anonymity_terms = [
        "anonymous", "pseudonymous", "hidden identity", "unknown leadership",
        "secret leadership", "untraceable", "masked"
    ]

    capital_terms = [
        "money", "capital", "bank", "banks", "fund", "hedge fund", "billion",
        "million", "$", "treasury", "market", "trade", "assets", "wealth",
        "profit", "investment"
    ]

    technical_terms = [
        "ai", "algorithm", "machine learning", "blockchain", "dao", "smart contract",
        "cryptography", "data", "surveillance", "platform", "network", "automated",
        "digital", "global id", "identity system"
    ]

    decentral_terms = [
        "decentralized", "decentralised", "distributed", "shared", "random",
        "randomly selected", "proportional", "community", "local", "federated",
        "collective", "peer-to-peer"
    ]

    fairness_terms = [
        "fair", "equal", "rights", "human right", "free from", "access",
        "shared human right", "everyone", "public good", "proportional"
    ]

    coercion_terms = [
        "forced", "mandatory control", "punish", "ban", "obedience", "surveillance",
        "command", "must obey", "enforce", "take over", "evil", "malicious",
        "cruel", "tyrant", "tyrannical", "dictator"
    ]

    def count_hits(terms):
        return sum(1 for term in terms if term in text)

    central_hits = count_hits(central_terms)
    decentral_hits = count_hits(decentral_terms)
    transparency_hits = count_hits(transparency_terms)
    secrecy_hits = count_hits(secrecy_terms)
    regulation_hits = count_hits(regulation_terms)
    anti_reg_hits = count_hits(anti_regulation_terms)
    anonymity_hits = count_hits(anonymity_terms)
    capital_hits = count_hits(capital_terms)
    technical_hits = count_hits(technical_terms)
    fairness_hits = count_hits(fairness_terms)
    coercion_hits = count_hits(coercion_terms)

    # Base scores.
    power_concentration = 0.35
    decision_transparency = 0.45
    regulatory_presence = 0.35
    anonymity_level = 0.20
    capital_scale = 0.25
    technical_complexity = 0.25

    # Adjust scores from detected terms.
    power_concentration += central_hits * 0.12
    power_concentration += coercion_hits * 0.08
    power_concentration -= decentral_hits * 0.10

    decision_transparency += transparency_hits * 0.12
    decision_transparency += decentral_hits * 0.05
    decision_transparency -= secrecy_hits * 0.15
    decision_transparency -= central_hits * 0.04

    regulatory_presence += regulation_hits * 0.11
    regulatory_presence += fairness_hits * 0.04
    regulatory_presence -= anti_reg_hits * 0.18
    regulatory_presence -= central_hits * 0.03

    anonymity_level += anonymity_hits * 0.20
    anonymity_level += secrecy_hits * 0.10
    anonymity_level -= transparency_hits * 0.08

    capital_scale += capital_hits * 0.10

    technical_complexity += technical_hits * 0.13

    # Strong special-case logic.
    single_ruler_terms = [
        "one world leader", "one leader", "runs the world", "rule the world",
        "world ruler", "global ruler", "single leader", "dictator", "supreme leader"
    ]

    if any(term in text for term in single_ruler_terms):
        power_concentration = max(power_concentration, 0.92)
        decision_transparency = min(decision_transparency, 0.25)
        regulatory_presence = min(regulatory_presence, 0.20)

    if any(term in text for term in ["evil", "malicious", "cruel", "tyrant", "tyrannical", "dictator"]) and any(term in text for term in ["leader", "ruler", "govern", "authority"]):
        power_concentration = max(power_concentration, 0.88)
        decision_transparency = min(decision_transparency, 0.25)
        regulatory_presence = min(regulatory_presence, 0.20)
        anonymity_level = max(anonymity_level, 0.45)

    if any(term in text for term in ["penguin", "animal", "cat", "dog", "bear"]) and any(term in text for term in ["leader", "ruler", "president", "government"]):
        power_concentration = max(power_concentration, 0.65)
        decision_transparency = min(decision_transparency, 0.35)
        regulatory_presence = min(regulatory_presence, 0.25)

    if "free from profit" in text or "shared human right" in text:
        power_concentration = min(power_concentration, 0.30)
        decision_transparency = max(decision_transparency, 0.70)
        regulatory_presence = max(regulatory_presence, 0.65)

    if "randomly selected" in text or "random selection" in text:
        power_concentration = min(power_concentration, 0.35)
        decision_transparency = max(decision_transparency, 0.60)

    return {
        "power_concentration": _clamp(power_concentration),
        "decision_transparency": _clamp(decision_transparency),
        "regulatory_presence": _clamp(regulatory_presence),
        "anonymity_level": _clamp(anonymity_level),
        "capital_scale": _clamp(capital_scale),
        "technical_complexity": _clamp(technical_complexity),
        "scan_mode": "Local Scan",
    }


def parse_scenario_llm(query: str):
    """
    Hybrid scanner:
    1. Tries OpenAI Deep Scan.
    2. If unavailable, falls back to free local scanner.
    """

    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or OpenAI is None:
        return _local_governance_scan(query)

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are a governance-risk analysis engine.

Analyze the following governance idea and return ONLY valid JSON.

The values must be numbers between 0.0 and 1.0.

Definitions:
- power_concentration: how much authority is concentrated in one person/group
- decision_transparency: how visible and accountable decisions are
- regulatory_presence: how much oversight/checks-and-balances exist
- anonymity_level: how hidden or unaccountable key actors are
- capital_scale: how much money/resources are controlled
- technical_complexity: how complex the system is

Governance idea:
\"\"\"{query}\"\"\"

Return this exact JSON shape:
{{
  "power_concentration": 0.0,
  "decision_transparency": 0.0,
  "regulatory_presence": 0.0,
  "anonymity_level": 0.0,
  "capital_scale": 0.0,
  "technical_complexity": 0.0
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Return only valid JSON. No markdown. No explanation."
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            temperature=0,
        )

        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        data = json.loads(raw)

        return {
            "power_concentration": _safe_float(data.get("power_concentration"), 0.5),
            "decision_transparency": _safe_float(data.get("decision_transparency"), 0.5),
            "regulatory_presence": _safe_float(data.get("regulatory_presence"), 0.5),
            "anonymity_level": _safe_float(data.get("anonymity_level"), 0.3),
            "capital_scale": _safe_float(data.get("capital_scale"), 0.3),
            "technical_complexity": _safe_float(data.get("technical_complexity"), 0.4),
            "scan_mode": "AI Deep Scan",
        }

    except Exception:
        return _local_governance_scan(query)
