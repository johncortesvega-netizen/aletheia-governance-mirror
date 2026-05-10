"""
Patch 27B: Cognitive Resilience diagnostic signals.

This module is diagnostic only. It does not classify people, does not create
truth authority, and does not change ALETHEIA scoring or enforcement behavior.
It reads scenario structure for information resilience and central information
capture so local witness receipts can show the signal reviewably.
"""

from __future__ import annotations

from typing import Any, Mapping

try:
    from core.ethics import contextual_capture_hits, grip_marker_hits
except Exception:  # pragma: no cover - defensive import fallback for isolated use
    contextual_capture_hits = lambda text: []  # type: ignore[assignment]
    grip_marker_hits = lambda text: []  # type: ignore[assignment]


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


def _hit_terms(text: str, terms: tuple[str, ...]) -> list[str]:
    return [term for term in terms if term in text]


LOCAL_OPEN_LEARNING_TERMS = (
    # Patch 30.1 Dutch calibration: local/open learning and craft networks.
    "lokaal", "lokale", "buurt", "buurtbewoners", "gemeenschap", "dorps", "dorps-grid",
    "hobby", "hobby-bijeenkomsten", "reparatie", "reparatie-gids", "eigen gereedschap",
    "open-source", "open source", "broncode", "publiek logboek", "ruwe data",
    "lokaal netwerk", "decentraal", "decentrale", "decentralized", "burgers doen zelf",
    "bodemonderzoek", "sensors", "skill-sharing", "vaardigheid", "vaardigheden",
    "kennis is de valuta", "vrije bibliotheek", "boeken", "lokale radio",
    "meester-gezel", "meester", "gezel", "staatsdiploma", "vragen-cirkel",
    "status quo", "kritisch denken", "gedeelde kwaliteitsstandaarden", "peer-review",
    "hyper-intelligente", "universiteit", "hoogopgeleide", "hoogopgeleid", "slim",
    "beste opleiding", "vrije studie", "open encyclopedie", "open data", "publieke data",
    "alles mag uitgevonden", "discussie is vrij", "gedeelde code", "software is open-source",
    "hoog opleidt", "hoog opleiden",

    "local", "locally", "neighborhood", "community", "town", "club", "clubs",
    "hobby", "hobbies", "repair guide", "repair guides", "workshop", "workshops",
    "master-apprentice", "apprentice", "apprentices", "mentor", "mentors",
    "open-source", "open source", "fork", "forks", "editable", "copy", "correct",
    "replication", "replicate", "reproducible", "peer review", "rotating peer",
    "question circle", "question circles", "source checking", "critical thinking",
    "plural", "competing versions", "competing show", "translation commons",
    "seed-saving", "tool library", "local servers", "visible disagreement",
)

REVOCABILITY_TERMS = (
    # Patch 30.1 Dutch calibration: appeal, exit, non-central authority.
    "geen afhankelijkheid", "zonder centrale autoriteit", "zonder centrale redactie",
    "geen centrale autoriteit", "geen centrale redactie", "publiek logboek",
    "kan worden aangepast", "aanpassen", "eigen", "zelf", "ruwe data", "openbaar",

    "voluntary", "optional", "opt-in", "consent", "local consent", "appeal", "appealable",
    "challenged", "replaced", "sunset", "expires", "revocable", "rollback",
    "corrections", "corrected", "correction", "uncertainty notes", "not mandatory",
    "no module is mandatory", "may still be published elsewhere", "without penalty",
    "can split", "split or sunset", "exit", "start a competing", "ignore a guide",
)

EDUCATIONAL_DECENTRALIZATION_TERMS = (
    # Patch 30.1 Dutch calibration: education as distributed practice.
    "open-source onderwijs", "leerlingen", "programmeren", "broncode",
    "hobby-bijeenkomsten", "reparatie-gids", "hobby-historici", "decentraal lab",
    "skill-sharing", "vrije bibliotheek", "lokale radio", "master-apprentice",
    "meester-gezel", "vragen-cirkel", "kritisch denken", "vakmanschap",
    "gedeelde kwaliteitsstandaarden", "peer-review", "ruwe data", "lokaal netwerk",
    "hyper-intelligente", "universiteit", "hoogopgeleide", "hoogopgeleid", "slim",
    "beste opleiding", "vrije studie", "open encyclopedie", "open data", "publieke data",
    "alles mag uitgevonden", "discussie is vrij", "gedeelde code", "software is open-source",
    "hoog opleidt", "hoog opleiden",

    "open-source lessons", "open-source education", "open source lessons",
    "families", "local mentors", "community labs", "local servers", "replication",
    "reproducible notebooks", "master-apprentice", "apprentice", "question circles",
    "source checking", "teachers publish", "forks are welcome", "workshops",
    "repair guides", "tool library", "seed-saving", "translation commons",
)

KNOWLEDGE_CAPACITY_TERMS = (
    "hyper-intelligente", "universiteit", "hoogopgeleide", "hoogopgeleid", "hoog opleidt",
    "hoog opleiden", "slim", "mensen zijn slim", "beste opleiding", "vrije studie",
    "open encyclopedie", "open data", "publieke data", "alles mag uitgevonden",
    "discussie is vrij", "gedeelde code", "software is open-source", "open-source",
    "broncode", "leerlingen", "programmeren", "vakmanschap", "meester-gezel",
    "peer-review", "kritisch denken", "ruwe data", "decentraal lab",
)

CENTRAL_INFO_CAPTURE_TERMS = (
    # Patch 30.1 Dutch calibration: truth gates, licensed speech, archive capture.
    "waarheid van de dag", "enkele bron", "één tablet", "een tablet", "centrale service",
    "centrale redactie", "centrale autoriteit", "centraal orgaan", "gecentraliseerde waarheid",
    "betrouwbaarheidsscore", "zoekgeschiedenis", "informatie-licentie", "informatie-licentie", "gecertificeerd praten", "officiële informatie-licentie",
    "goedgekeurde influencers", "goedgekeurde", "gehoorzaamheidsprofiel",
    "algoritmische isolatie", "echo-kamer", "blokkeert automatisch gesprekken",
    "oude boeken", "gecorrigeerd", "originelen worden vernietigd", "originelen vernietigd",
    "archief", "minder toegang tot informatie", "emotie-tracking", "negatief kijkt", "diepgaande kennis",
    "simpele samenvattingen", "elite", "geen vragen", "passiviteit",
    "rector beslist", "wie welke data ziet", "super-editors", "zonder overleg",
    "niemand mag auditen", "mag auditen", "gecertificeerde expert", "gedwongen hun stem",
    "geheim geschreven", "verplichte dienst", "surveillance-grid", "populariteits-algoritmes",
    "privé sleutel", "prive sleutel", "één oncontroleerbaar individu", "een oncontroleerbaar individu",
    "verlichte dictator", "digitale identiteit", "digitale munt", "lokale valuta vervangen",
    "objectivity-agents", "goedkeuring", "goedkeuring door", "berichten mogen alleen",
    "objectiviteits-filter", "onwetenschappelijke meningen", "biometrische controle",
    "luistert mee", "deelt data", "handhavers", "sport-data", "sport data",
    "privé-uitgaven", "prive-uitgaven", "openbaar te maken", "weg van protesten",
    "protesten", "algoritmes leiden",

    "truth of the day", "official truth", "official conclusion", "official language",
    "central office", "central archive", "central authority", "central grid",
    "central registry", "central editorial", "central server", "single server",
    "single keyholder", "private server keyholder", "one private server keyholder",
    "truth score", "centralized truth score", "central truth", "truth gate",
    "truth gatekeeper", "licensed speech", "speech license", "approved skills",
    "approved speech", "approved sources", "certified centers", "certification",
    "obedience profile", "filters news", "filtered news", "algorithmic isolation",
    "archive rewriting", "rewrites public records", "rewrite records", "rewrite archives",
    "older explanations disappear", "cannot compare archived versions",
    "no appeal", "cannot appeal", "cannot be appealed", "cannot be questioned",
    "mandatory information", "official feed", "universal id", "mandatory id",
    "digital id", "biometric", "surveillance", "police", "monitored",
)

ENTERTAINMENT_COMPLIANCE_TERMS = (
    # Patch 30.1 Dutch calibration: entertainment/passivity compliance.
    "entertainment-dwang", "dagelijks kijken", "4 uur", "goedgekeurde influencers",
    "punten voor passiviteit", "geen vragen stellen", "overheids-informatie-uurtjes",
    "simpele samenvattingen", "digitale schaarste",

    "entertainment compliance", "compliance entertainment", "approved entertainment",
    "mandatory entertainment", "obedience entertainment", "obedience-profile entertainment",
    "obedience profile", "hobby ban", "hobby bans", "bans hobbies", "ban hobbies",
    "unlicensed hobbies", "approved hobbies", "entertainment license",
    "passive entertainment", "constant entertainment", "distraction feed",
    "rewarded viewing", "viewing quota", "compliance score", "screen quota",
)

ALGORITHMIC_EROSION_TERMS = (
    # Patch 30.1 Dutch calibration: algorithmic thinning and isolation.
    "algoritmische isolatie", "gehoorzaamheidsprofiel", "echo-kamer",
    "blokkeert automatisch gesprekken", "populariteits-algoritmes", "filter", "emotie-tracking", "negatief kijkt",
    "objectiviteits-filter", "verwijderen van", "onwetenschappelijke",
    "waarheid van de dag", "gecorrigeerd", "originelen vernietigd",
    "minder toegang tot informatie", "simpele samenvattingen",

    "algorithmic isolation", "algorithmic feed", "personalized feed", "personalised feed",
    "obedience feed", "official feed", "attention score", "attention scoring",
    "optimizes attention", "optimises attention", "scroll feed", "short-form feed",
    "short form feed", "infinite scroll", "removes dissent", "filters dissent",
    "filters news", "replaces books", "replaces reading", "reduces attention",
    "archive rewriting", "older explanations disappear", "licensed speech",
)

Z_AXIS_DEPTH_TERMS = (
    # Patch 30.1 Dutch calibration: depth through practice, books, craft, questions.
    "boeken", "vrije bibliotheek", "vakmanschap", "meester-gezel", "meester", "gezel",
    "vragen-cirkel", "kritisch denken", "geschiedenis", "publiek logboek",
    "hobby", "vaardigheid", "vaardigheden", "reparatie", "lokale radio",

    "depth", "belief", "faith", "conscience", "contemplation", "silence",
    "reading", "books", "craft", "crafts", "music practice", "local art",
    "family stories", "intergenerational", "elders", "mentors", "apprentice",
    "master-apprentice", "question circles", "ritual", "reflection", "slow learning",
    "debate", "source checking", "critical thinking",
)

Z_AXIS_EROSION_TERMS = (
    # Patch 30.1 Dutch calibration: depth erosion via bans, passivity, flattening.
    "hobby-verbod", "verbod op eigen gereedschap", "oude boeken",
    "originelen vernietigd", "geen vragen stellen", "passiviteit",
    "diepgaande kennis is voor de elite", "alleen simpele samenvattingen",
    "echo-kamer", "blokkeert automatisch gesprekken",

    "removes depth", "removes belief", "belief is discouraged", "faith is discouraged",
    "conscience is flagged", "silence is flagged", "reflection is discouraged",
    "reading is replaced", "books are replaced", "local art is replaced",
    "family stories are replaced", "elders are bypassed", "mentors are bypassed",
    "values transfer is replaced", "constant state of paraatheid", "constant state of readiness",
)


CAPTURE_OR_RELINQUISH_TERMS = (
    # Patch 30.1 Dutch calibration: forced delegation, no audit, central ownership.
    "verplicht", "verplichte", "gedwongen", "moeten", "verbod op", "vergunning",
    "niemand mag auditen", "niet auditen", "zonder overleg", "geen overleg",
    "stem te delegeren", "delegeren", "gecertificeerde expert", "geheim geschreven",
    "direct eigendom", "centraal orgaan", "verplichte dienst", "surveillance-grid",
    "één oncontroleerbaar individu", "een oncontroleerbaar individu", "dictator",
    "vrijwillig blijven volgen", "biometrische controle", "luistert mee", "deelt data",
    "handhavers", "verplichte digitale identiteit", "goedkeuring", "openbaar te maken",
    "lokale valuta vervangen", "één digitale munt", "een digitale munt",

    "mandatory", "must", "forced", "required", "relinquish", "delegate", "delegation",
    "no appeal", "cannot appeal", "cannot be appealed", "without appeal",
    "unauditable", "cannot be audited", "immune from audit", "single keyholder",
    "one private server keyholder", "enlightened dictator", "dictator", "central ai",
    "ai governs", "ai decides", "no human review", "biometric", "surveillance",
    "sent to police", "conditioned on compliance", "access to food", "basic needs",
)

NEGATED_CENTRAL_PATTERNS = (
    # Patch 30.1 Dutch calibration: explicit anti-gatekeeper language.
    "zonder centrale autoriteit", "geen centrale autoriteit",
    "zonder centrale redactie", "geen centrale redactie",
    "geen afhankelijkheid", "geen afhankelijkheid van fabrikanten",

    "no central editor", "no central office decides", "no central registry controls",
    "no central editorial control", "without central truth", "no truth gatekeeper",
    "no central authority", "not conditioned on", "does not depend on accepting one official conclusion",
)


def evaluate_cognitive_resilience(
    text: str,
    governance_result: Mapping[str, Any] | None = None,
    features: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return diagnostic-only Cognitive Resilience signals for a scenario.

    The signals describe system properties. They are not judgments of a person
    or population and they do not alter the final protocol state.
    """

    raw_text = text or ""
    lower = raw_text.lower()
    governance_result = dict(governance_result or {})
    features = dict(features or {})

    central_power = float(governance_result.get("power_concentration", features.get("centralization", 0.5)) or 0.5)
    transparency = float(governance_result.get("decision_transparency", features.get("transparency", 0.5)) or 0.5)

    local_hits = _hit_terms(lower, LOCAL_OPEN_LEARNING_TERMS)
    revocable_hits = _hit_terms(lower, REVOCABILITY_TERMS)
    education_hits = _hit_terms(lower, EDUCATIONAL_DECENTRALIZATION_TERMS)
    knowledge_hits = _hit_terms(lower, KNOWLEDGE_CAPACITY_TERMS)
    central_hits = _hit_terms(lower, CENTRAL_INFO_CAPTURE_TERMS)
    capture_hits = _hit_terms(lower, CAPTURE_OR_RELINQUISH_TERMS)
    entertainment_hits = _hit_terms(lower, ENTERTAINMENT_COMPLIANCE_TERMS)
    algorithmic_erosion_hits = _hit_terms(lower, ALGORITHMIC_EROSION_TERMS)
    z_axis_depth_hits = _hit_terms(lower, Z_AXIS_DEPTH_TERMS)
    z_axis_erosion_hits = _hit_terms(lower, Z_AXIS_EROSION_TERMS)
    negated_central_hits = _hit_terms(lower, NEGATED_CENTRAL_PATTERNS)
    contextual_hits = contextual_capture_hits(raw_text)
    grip_hits = grip_marker_hits(raw_text)

    # Avoid penalizing explicit anti-centralization language such as
    # "no central editor" or "no truth gatekeeper".
    effective_central_hit_count = max(0, len(central_hits) - len(negated_central_hits))

    local_open_score = min(0.38, len(local_hits) * 0.035)
    revocable_score = min(0.24, len(revocable_hits) * 0.040)
    education_score = min(0.22, len(education_hits) * 0.040)
    knowledge_capacity_score = min(0.20, len(knowledge_hits) * 0.035)
    transparency_score = max(0.0, min(0.08, (transparency - 0.35) * 0.20))
    capture_penalty = min(0.48, effective_central_hit_count * 0.060 + len(capture_hits) * 0.035)
    power_penalty = min(0.22, max(0.0, central_power - 0.45) * 0.32)
    ethics_capture_penalty = min(0.18, len(contextual_hits) * 0.09 + len(grip_hits) * 0.04)

    resilience_score = _clamp(0.40 + local_open_score + revocable_score + education_score + knowledge_capacity_score + transparency_score - capture_penalty - power_penalty - ethics_capture_penalty)

    decentralization_score = _clamp(
        0.28
        + min(0.48, len(education_hits) * 0.07 + len(local_hits) * 0.025 + len(knowledge_hits) * 0.020)
        + min(0.16, len(revocable_hits) * 0.03)
        - min(0.34, effective_central_hit_count * 0.06 + len(capture_hits) * 0.03)
        - power_penalty
    )

    central_capture_score = _clamp(
        0.10
        + min(0.62, effective_central_hit_count * 0.12)
        + min(0.34, len(capture_hits) * 0.07)
        + min(0.24, len(contextual_hits) * 0.10 + len(grip_hits) * 0.06)
        + min(0.12, max(0.0, central_power - 0.55) * 0.30)
        - min(0.24, len(negated_central_hits) * 0.07)
    )

    entertainment_compliance_score = _clamp(
        min(0.70, len(entertainment_hits) * 0.16)
        + min(0.24, len(capture_hits) * 0.035)
        + min(0.16, max(0.0, central_power - 0.50) * 0.35)
    )
    algorithmic_erosion_score = _clamp(
        min(0.72, len(algorithmic_erosion_hits) * 0.14)
        + min(0.18, effective_central_hit_count * 0.025)
        + min(0.14, len(contextual_hits) * 0.05 + len(grip_hits) * 0.025)
    )
    z_axis_depth_risk_score = _clamp(
        min(0.60, len(z_axis_erosion_hits) * 0.16)
        + min(0.28, len(entertainment_hits) * 0.05 + len(algorithmic_erosion_hits) * 0.035)
        + min(0.12, central_capture_score * 0.20)
        - min(0.24, len(z_axis_depth_hits) * 0.035)
    )
    education_defense_score = _clamp(
        0.52
        + min(0.26, len(z_axis_depth_hits) * 0.035)
        + min(0.18, len(education_hits) * 0.035 + len(local_hits) * 0.012)
        + min(0.08, len(revocable_hits) * 0.015)
        - min(0.34, entertainment_compliance_score * 0.34)
        - min(0.30, algorithmic_erosion_score * 0.30)
        - min(0.22, z_axis_depth_risk_score * 0.22)
        - min(0.12, central_capture_score * 0.12)
    )

    has_capture = central_capture_score >= 0.45 or bool(contextual_hits) or bool(grip_hits) or len(capture_hits) >= 2
    if resilience_score >= 0.58 and not has_capture:
        cognitive_signal = "high"
    elif has_capture and (resilience_score >= 0.50 or len(knowledge_hits) >= 2 or len(local_hits) >= 2 or len(education_hits) >= 2):
        cognitive_signal = "high_but_captured"
    elif resilience_score < 0.45 or central_capture_score >= 0.52 or (central_capture_score >= 0.34 and not local_hits and not education_hits and not knowledge_hits):
        cognitive_signal = "low"
    else:
        cognitive_signal = "mixed"

    if decentralization_score >= 0.60 and central_capture_score < 0.45:
        educational_signal = "high"
    elif decentralization_score <= 0.38 or central_capture_score >= 0.58:
        educational_signal = "low"
    else:
        educational_signal = "medium"

    if central_capture_score >= 0.45:
        central_signal = "high"
    elif central_capture_score >= 0.26:
        central_signal = "medium"
    else:
        central_signal = "low"

    if entertainment_compliance_score >= 0.42:
        entertainment_signal = "high"
    elif entertainment_compliance_score >= 0.22:
        entertainment_signal = "medium"
    else:
        entertainment_signal = "low"

    if algorithmic_erosion_score >= 0.42:
        algorithmic_erosion_signal = "high"
    elif algorithmic_erosion_score >= 0.22:
        algorithmic_erosion_signal = "medium"
    else:
        algorithmic_erosion_signal = "low"

    if z_axis_depth_risk_score >= 0.40:
        z_axis_depth_risk_signal = "high"
    elif z_axis_depth_risk_score >= 0.22:
        z_axis_depth_risk_signal = "medium"
    else:
        z_axis_depth_risk_signal = "low"

    if education_defense_score >= 0.62 and entertainment_signal == "low" and algorithmic_erosion_signal == "low":
        education_defense_signal = "protected"
    elif education_defense_score <= 0.42 or entertainment_signal == "high" or algorithmic_erosion_signal == "high" or z_axis_depth_risk_signal == "high":
        education_defense_signal = "eroded"
    else:
        education_defense_signal = "pressured"

    if cognitive_signal == "high":
        narrative = "This scenario offers strong information resilience."
    elif cognitive_signal == "high_but_captured":
        narrative = "This scenario has learning capacity, but capture markers prevent that resilience from laundering power."
    elif cognitive_signal == "low":
        narrative = "This scenario shows weak information resilience because knowledge flow is centralized, filtered, or hard to contest."
    else:
        narrative = "This scenario has mixed information resilience and should be reviewed for openness, appeal, and exit paths."

    if education_defense_signal == "eroded":
        narrative = f"{narrative} Education Defense is eroded: entertainment compliance or algorithmic thinning weakens deep learning and contestability."
    elif education_defense_signal == "protected":
        narrative = f"{narrative} Education Defense is protected by depth, practice, and contestable learning paths."

    return {
        "cognitive_resilience_signal": cognitive_signal,
        "educational_decentralization_signal": educational_signal,
        "central_info_capture_signal": central_signal,
        "education_defense_signal": education_defense_signal,
        "entertainment_compliance_signal": entertainment_signal,
        "algorithmic_erosion_signal": algorithmic_erosion_signal,
        "z_axis_depth_risk_signal": z_axis_depth_risk_signal,
        "cognitive_resilience_score": round(resilience_score, 4),
        "knowledge_capacity_score": round(min(1.0, len(knowledge_hits) * 0.12), 4),
        "knowledge_capacity_signal": "present" if knowledge_hits else "not_detected",
        "capture_architecture_signal": "present" if (central_capture_score >= 0.26 or capture_hits or contextual_hits or grip_hits) else "not_detected",
        "high_cr_laundering_blocked": bool(has_capture and (knowledge_hits or local_hits or education_hits)),
        "educational_decentralization_score": round(decentralization_score, 4),
        "central_info_capture_score": round(central_capture_score, 4),
        "education_defense_score": round(education_defense_score, 4),
        "entertainment_compliance_score": round(entertainment_compliance_score, 4),
        "algorithmic_erosion_score": round(algorithmic_erosion_score, 4),
        "z_axis_depth_risk_score": round(z_axis_depth_risk_score, 4),
        "diagnostic_only": True,
        "system_property_note": "Cognitive Resilience is a system property, not a judgment of people.",
        "education_defense_property_note": "Education Defense is a system property, not a judgment of people.",
        "narrative": narrative,
        "evidence": {
            "local_open_learning_terms": local_hits[:8],
            "revocability_terms": revocable_hits[:8],
            "educational_decentralization_terms": education_hits[:8],
            "knowledge_capacity_terms": knowledge_hits[:8],
            "central_info_capture_terms": central_hits[:8],
            "capture_or_relinquish_terms": capture_hits[:8],
            "entertainment_compliance_terms": entertainment_hits[:8],
            "algorithmic_erosion_terms": algorithmic_erosion_hits[:8],
            "z_axis_depth_terms": z_axis_depth_hits[:8],
            "z_axis_erosion_terms": z_axis_erosion_hits[:8],
            "negated_centralization_terms": negated_central_hits[:6],
            "contextual_capture_count": len(contextual_hits),
            "grip_marker_count": len(grip_hits),
        },
    }

def _round_metric(value: float, digits: int = 4) -> float:
    return round(_clamp(value), digits)


def _has_hard_capture_evidence(diagnostics: Mapping[str, Any]) -> bool:
    """Return True when CR must not stabilize a scenario.

    Patch 28 rule: high Cognitive Resilience may only stabilize local, open,
    appealable systems. It must never launder central capture, no-appeal power,
    biometric/surveillance gates, contextual capture, or grip markers.
    """
    evidence = dict(diagnostics.get("evidence") or {})
    central_terms = list(evidence.get("central_info_capture_terms") or [])
    capture_terms = list(evidence.get("capture_or_relinquish_terms") or [])
    revocability_terms = list(evidence.get("revocability_terms") or [])

    # Patch 27B intentionally uses simple phrase hits. Preserve that diagnostic
    # transparency, but do not let the phrase "no module is mandatory" become a
    # hard-capture blocker in Patch 28 scoring.
    benign_negated_mandatory = (
        set(capture_terms).issubset({"mandatory"})
        and any("no module is mandatory" in term for term in revocability_terms)
    )
    effective_capture_terms = [] if benign_negated_mandatory else capture_terms

    return (
        diagnostics.get("central_info_capture_signal") == "high"
        or diagnostics.get("cognitive_resilience_signal") == "high_but_captured"
        or bool(central_terms)
        or bool(effective_capture_terms)
        or int(evidence.get("contextual_capture_count") or 0) > 0
        or int(evidence.get("grip_marker_count") or 0) > 0
    )


def apply_cognitive_resilience_to_metrics(
    report: Mapping[str, Any],
    diagnostics: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Apply Patch 28's light Educational Decentralization scoring.

    This is deliberately small and bounded. It adjusts review metrics only; it
    does not change protocol hard overrides, does not add enforcement, and does
    not classify people. High CR can slightly stabilize only when there are no
    capture markers. Low CR / central information capture raises friction and
    collapse risk.
    """
    adjusted = dict(report or {})
    diagnostics = dict(diagnostics or {})
    if not diagnostics:
        return adjusted

    original = {
        "integrity": float(adjusted.get("integrity", 0.0) or 0.0),
        "friction": float(adjusted.get("friction", 0.0) or 0.0),
        "collapse_probability": float(adjusted.get("collapse_probability", 0.0) or 0.0),
        "trust_friction": float(adjusted.get("trust_friction", 0.0) or 0.0),
    }

    cognitive = diagnostics.get("cognitive_resilience_signal")
    education = diagnostics.get("educational_decentralization_signal")
    central = diagnostics.get("central_info_capture_signal")
    education_defense = diagnostics.get("education_defense_signal")
    entertainment = diagnostics.get("entertainment_compliance_signal")
    algorithmic_erosion = diagnostics.get("algorithmic_erosion_signal")
    z_axis_depth_risk = diagnostics.get("z_axis_depth_risk_signal")
    hard_capture = _has_hard_capture_evidence(diagnostics)

    integrity_delta = 0.0
    friction_delta = 0.0
    collapse_delta = 0.0
    trust_friction_delta = 0.0
    reason = "No Cognitive Resilience scoring change was applied."

    if cognitive == "high" and education == "high" and central == "low" and not hard_capture:
        integrity_delta = 0.030
        friction_delta = -0.025
        collapse_delta = -0.025
        trust_friction_delta = -0.020
        reason = "Local, open, revocable education slightly stabilizes the review metrics."
    elif cognitive in {"low", "high_but_captured"} or central == "high":
        severity = 1.0 if central == "high" or cognitive == "low" else 0.65
        integrity_delta = -0.040 * severity
        friction_delta = 0.060 * severity
        collapse_delta = 0.050 * severity
        trust_friction_delta = 0.055 * severity
        reason = "Central information capture or weak resilience increases friction and collapse risk."
    elif central == "medium":
        integrity_delta = -0.020
        friction_delta = 0.030
        collapse_delta = 0.025
        trust_friction_delta = 0.025
        reason = "Partial central information capture adds a light review penalty."

    education_defense_delta = {
        "integrity_delta": 0.0,
        "friction_delta": 0.0,
        "collapse_probability_delta": 0.0,
        "trust_friction_delta": 0.0,
        "reason": "No Education Defense scoring change was applied.",
    }
    edd_eroded = (
        education_defense == "eroded"
        or entertainment == "high"
        or algorithmic_erosion == "high"
        or z_axis_depth_risk == "high"
    )
    if edd_eroded:
        severity = 1.0 if entertainment == "high" or algorithmic_erosion == "high" else 0.70
        education_defense_delta = {
            "integrity_delta": round(-0.025 * severity, 4),
            "friction_delta": round(0.035 * severity, 4),
            "collapse_probability_delta": round(0.030 * severity, 4),
            "trust_friction_delta": round(0.030 * severity, 4),
            "reason": "Patch 30 Education Defense: entertainment compliance or algorithmic erosion increases review pressure.",
        }
    elif education_defense == "protected" and cognitive == "high" and central == "low" and not hard_capture:
        education_defense_delta = {
            "integrity_delta": 0.010,
            "friction_delta": -0.010,
            "collapse_probability_delta": -0.010,
            "trust_friction_delta": -0.008,
            "reason": "Patch 30 Education Defense: protected depth and practice lightly stabilize local review metrics.",
        }

    integrity_delta += education_defense_delta["integrity_delta"]
    friction_delta += education_defense_delta["friction_delta"]
    collapse_delta += education_defense_delta["collapse_probability_delta"]
    trust_friction_delta += education_defense_delta["trust_friction_delta"]
    if education_defense_delta["reason"] != "No Education Defense scoring change was applied.":
        reason = f"{reason} {education_defense_delta['reason']}"

    # Final safety clamp: capture evidence blocks all positive stabilization.
    if hard_capture and integrity_delta > 0:
        integrity_delta = 0.0
        friction_delta = max(0.020, friction_delta)
        collapse_delta = max(0.020, collapse_delta)
        trust_friction_delta = max(0.020, trust_friction_delta)
        reason = "Capture markers block Cognitive Resilience from stabilizing the metrics."

    adjusted["integrity"] = _round_metric(original["integrity"] + integrity_delta)
    adjusted["friction"] = _round_metric(original["friction"] + friction_delta)
    adjusted["collapse_probability"] = round(_clamp(original["collapse_probability"] + collapse_delta), 3)
    adjusted["trust_friction"] = round(_clamp(original["trust_friction"] + trust_friction_delta), 3)

    updated_diagnostics = dict(diagnostics)
    updated_diagnostics["scoring_adjustment"] = {
        "patch": "28",
        "applied": any(abs(x) > 0 for x in (integrity_delta, friction_delta, collapse_delta, trust_friction_delta)),
        "lightweight": True,
        "hard_capture_blocks_stabilization": hard_capture,
        "integrity_delta": round(integrity_delta, 4),
        "friction_delta": round(friction_delta, 4),
        "collapse_probability_delta": round(collapse_delta, 4),
        "trust_friction_delta": round(trust_friction_delta, 4),
        "reason": reason,
        "education_defense_adjustment": {
            "patch": "30",
            "applied": any(abs(education_defense_delta[k]) > 0 for k in ("integrity_delta", "friction_delta", "collapse_probability_delta", "trust_friction_delta")),
            "lightweight": True,
            "education_defense_signal": education_defense,
            "entertainment_compliance_signal": entertainment,
            "algorithmic_erosion_signal": algorithmic_erosion,
            "z_axis_depth_risk_signal": z_axis_depth_risk,
            **education_defense_delta,
        },
    }
    adjusted["cognitive_resilience_diagnostics"] = updated_diagnostics
    return adjusted



def _diagnostic_evidence_counts(diagnostics: Mapping[str, Any]) -> dict[str, int]:
    """Return bounded evidence counts used by the Patch 30.2 verdict stabilizer."""
    evidence = dict((diagnostics or {}).get("evidence") or {})
    return {
        "contextual_capture_count": int(evidence.get("contextual_capture_count") or 0),
        "grip_marker_count": int(evidence.get("grip_marker_count") or 0),
        "central_info_capture_terms": len(list(evidence.get("central_info_capture_terms") or [])),
        "capture_or_relinquish_terms": len(list(evidence.get("capture_or_relinquish_terms") or [])),
    }


def positive_cr_baseline_stabilizer(
    judgment: Mapping[str, Any] | None,
    report: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Keep positive CR baseline cases from being over-escalated.

    Patch 30.2 is deliberately narrow. It may soften a result only when the
    receipt already shows high Cognitive Resilience, protected Education
    Defense, low central information capture, and no contextual/grip/capture
    evidence. It never applies when capture architecture is present, hard CR
    laundering is blocked, or hard capture markers are visible.

    The stabilizer does not add enforcement authority and does not classify
    people. It only calibrates local Mirror Check wording for systems whose
    information architecture is local, open, contestable, and non-coercive.
    """
    adjusted = dict(judgment or {})
    diagnostics = dict((report or {}).get("cognitive_resilience_diagnostics") or {})
    if not diagnostics:
        return adjusted

    counts = _diagnostic_evidence_counts(diagnostics)
    safe_positive_baseline = (
        diagnostics.get("cognitive_resilience_signal") == "high"
        and diagnostics.get("educational_decentralization_signal") in {"medium", "high"}
        and diagnostics.get("central_info_capture_signal") == "low"
        and diagnostics.get("education_defense_signal") == "protected"
        and diagnostics.get("capture_architecture_signal") in {None, "not_detected"}
        and not bool(diagnostics.get("high_cr_laundering_blocked"))
        and counts["contextual_capture_count"] == 0
        and counts["grip_marker_count"] == 0
        and counts["central_info_capture_terms"] == 0
        and counts["capture_or_relinquish_terms"] == 0
    )
    if not safe_positive_baseline:
        return adjusted

    current_verdict = str(adjusted.get("verdict") or "THRESHOLD").upper()
    current_risk = str(adjusted.get("corruption_risk") or adjusted.get("guardrail_risk") or "Medium")
    raw_integrity = float((report or {}).get("integrity", adjusted.get("raw_integrity", 0.0)) or 0.0)
    collapse_probability = float((report or {}).get("collapse_probability", 1.0) or 1.0)
    friction = float((report or {}).get("friction", 1.0) or 1.0)

    if current_verdict == "SANCTUARY" and current_risk == "Low":
        return adjusted

    if raw_integrity >= 0.62 and collapse_probability <= 0.20 and friction <= 0.20:
        new_verdict = "SANCTUARY"
        new_risk = "Low"
        label = "Positive Cognitive Resilience / Local Open Learning"
    else:
        new_verdict = "THRESHOLD"
        new_risk = "Medium"
        label = "Positive Cognitive Resilience / Reviewable Local Learning"

    adjusted["verdict"] = new_verdict
    adjusted["corruption_risk"] = new_risk
    adjusted["guardrail_risk"] = new_risk
    adjusted["stress_label"] = label
    adjusted["summary"] = (
        "Protocol audit result calibrated by Patch 30.2: positive Cognitive "
        "Resilience is recognized because the scenario is local/open, non-coercive, "
        "and shows no capture architecture. People still decide."
    )
    reasons = list(adjusted.get("reasons") or [])
    reasons.append(
        "Patch 30.2 positive CR baseline stabilizer applied: high CR, protected Education Defense, low central info capture, and zero contextual/grip markers."
    )
    adjusted["reasons"] = reasons
    adjusted["questions"] = list(adjusted.get("questions") or [])[:7]
    adjusted["positive_cr_stabilizer"] = {
        "patch": "30.2",
        "applied": True,
        "verdict_before": current_verdict,
        "risk_before": current_risk,
        "verdict_after": new_verdict,
        "risk_after": new_risk,
        "reason": "High CR only stabilized because no hard/capture markers were present.",
    }
    return adjusted
