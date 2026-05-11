import re

def _clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))


def _count_hits(text, terms):
    return sum(1 for term in terms if term in text)


def _hit_terms(text, terms):
    return [term for term in terms if term in text]


_NEGATION_PREFIX_RE = re.compile(
    r"\b(?:no|not|without|lack(?:s|ing)?(?:\s+of)?|absence\s+of|absent|"
    r"geen|niet|zonder|ontbreekt|ontbrekende|gebrek\s+aan)\b"
    r"(?:[^\w]+\w+){{0,3}}[^\w]+{term}\b"
)


def _term_pattern(term):
    return re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)")


def _is_negated_positive_term(text, term):
    """Return True when a normally positive term is locally negated.

    Patch 70.1 keeps diagnostic strengths from treating phrases such as
    "no oversight", "no public review", "without transparency",
    "no accountability", or Dutch equivalents such as "geen toezicht" as
    safeguards. It only filters positive-credit terms; grip/risk terms keep
    their normal detection path.
    """
    text = text or ""
    term = (term or "").strip()
    if not term:
        return False
    pattern = re.compile(_NEGATION_PREFIX_RE.pattern.format(term=re.escape(term)))
    return bool(pattern.search(text))


def _count_non_negated_hits(text, terms):
    return sum(
        1 for term in terms
        if _term_pattern(term).search(text or "")
        and not _is_negated_positive_term(text or "", term)
    )


def _has_non_negated_term(text, terms):
    return any(
        _term_pattern(term).search(text or "")
        and not _is_negated_positive_term(text or "", term)
        for term in terms
    )


POSITIVE_ETHICS_TERMS = [
    # Patch 30.1 Dutch safety/objectivity capture frames.
    "objectiviteit", "objectief", "beschermen", "bevolking beschermen", "verwarring",
    "eerlijke verdeling", "schaarse goederen", "mentale crises", "mentale crisis",
    "betrouwbaarheid", "betrouwbaarheidsscore", "minderheden", "inclusieve",
    "inclusief", "solidariteit", "gezondheids-solidariteit", "ethische consumptie",
    "persoonlijke veiligheid", "fraude", "fraude te voorkomen",

    "fair", "fairness", "equal", "equality", "rights", "human right", "shared", "access",
    "proportional", "everyone", "public good", "universal", "free from profit", "community",
    "care", "dignity", "safety", "public safety", "health safety", "mental-health safety",
    "public health", "objectivity", "objective", "inclusion", "inclusive", "for inclusion",
    "safe distribution", "equitable distribution", "veilig", "veiligheid", "rechten", "eerlijk", "zorg",
    "gelijkwaardig", "publiek belang", "menselijke waardigheid",
]

COERCIVE_POWER_TERMS = [
    # Patch 30.1 Dutch coercive/capture terms.
    "verwijderen", "verwijderen van", "onwetenschappelijke meningen",
    "biometrische controle", "biometrie", "bakker", "luistert mee", "meeluistert",
    "deelt data", "data met handhavers", "handhavers", "zoekgeschiedenis",
    "gecentraliseerde waarheid", "betrouwbaarheidsscore", "verplichte digitale identiteit",
    "digitale identiteit", "enige manier", "goedkeuring", "objectivity-agents",
    "berichten mogen alleen", "sport-data", "sport data", "niet deelt",
    "privé-uitgaven openbaar", "prive-uitgaven openbaar", "privé uitgaven openbaar",
    "verplichting", "openbaar te maken", "weg van protesten", "protesten",
    "lokale valuta vervangen", "digitale munt", "één digitale munt", "een digitale munt",

    "mandatory", "mandatory control", "mandatory enforcement", "enforcement", "forced", "force",
    "forced compliance", "must obey", "obedience", "comply", "compliance", "central grid",
    "central authority", "centralized authority", "universal id", "global id", "identity requirement",
    "mandatory id", "mandatory digital id", "digital id", "biometric authority", "biometric id",
    "biometric access", "biometric control", "movement permissions", "surveillance", "tracking",
    "private conversation monitoring", "private conversations are monitored", "monitored and sent to police",
    "sent to police", "police", "automated approval", "approval before posting", "central truth gate",
    "truth gate", "no appeal", "without appeal", "cannot appeal", "cannot be appealed",
    "conditioned on compliance", "access to food", "access to mobility", "access to health",
    "food access", "mobility access", "health access", "command", "punish", "ban", "lockdown",
    "handhaving", "verplicht", "verplichte", "centrale autoriteit", "centraal grid",
    "universeel id", "identificatie-eis", "biometrische autoriteit", "toezicht",
    "surveillance", "volgen", "controle",
]

SAFETY_OBJECTIVITY_CAPTURE_POWER_TERMS = [
    # Patch 30.1 Dutch multiplier terms.
    "verwijderen", "onwetenschappelijke meningen", "biometrische controle",
    "luistert mee", "deelt data", "handhavers", "betrouwbaarheidsscore",
    "zoekgeschiedenis", "verplichte digitale identiteit", "digitale identiteit",
    "goedkeuring", "objectivity-agents", "berichten mogen alleen", "sport-data",
    "privé-uitgaven openbaar", "prive-uitgaven openbaar", "openbaar te maken",
    "weg van protesten", "lokale valuta vervangen", "digitale munt",

    "mandatory id", "mandatory digital id", "digital id", "universal id", "global id",
    "biometric", "biometric id", "biometric access", "biometric control",
    "surveillance", "tracking", "private conversation monitoring",
    "private conversations are monitored", "monitored", "sent to police", "police",
    "no appeal", "without appeal", "cannot appeal", "cannot be appealed",
    "central grid", "central authority", "central truth gate", "truth gate",
    "forced compliance", "mandatory enforcement", "mandatory", "must obey", "compliance",
    "conditioned on compliance", "access to food", "food access", "access to mobility",
    "mobility access", "access to health", "health access", "approval before posting",
    "automated approval",
]

SAFETY_OBJECTIVITY_HARD_CAPTURE_TERMS = [
    # Patch 30.1 Dutch hard capture terms.
    "biometrische controle", "biometrie", "bakker", "luistert mee",
    "deelt data", "data met handhavers", "handhavers",
    "verplichte digitale identiteit", "digitale identiteit", "betrouwbaarheidsscore",
    "zoekgeschiedenis", "goedkeuring", "objectivity-agents", "berichten mogen alleen",
    "privé-uitgaven openbaar", "prive-uitgaven openbaar", "lokale valuta vervangen",
    "digitale munt",

    "biometric access", "biometric id", "biometric control", "access to food", "food access",
    "private conversations are monitored", "private conversation monitoring", "monitored and sent to police",
    "sent to police", "mandatory digital id", "mandatory id", "no appeal", "without appeal",
    "central truth gate", "truth gate", "conditioned on compliance",
]

MICRO_SOVEREIGNTY_TERMS = [
    "local", "locally", "household", "home", "family", "parent", "parents", "private", "privacy",
    "community", "neighborhood", "municipal", "local witness", "revocable", "appealable",
    "opt-in", "consent", "human review", "human override", "rollback", "sunset clause", "sunset", "expires", "renewed by public vote", "public vote", "residents", "independent audit",
    "gezin", "huishouden", "lokaal", "lokale", "privé", "privacy", "ouders", "ouder",
    "gemeenschap", "getroffenen", "herroepbaar", "bezwaar", "beroep", "menselijke review",
    "menselijke maat", "lokale getuigenis", "noodstop",
]

MACRO_CAPTURE_TERMS = [
    # Patch 30.1 Dutch macro/grid capture terms.
    "gecentraliseerde waarheid", "betrouwbaarheidsscore", "zoekgeschiedenis",
    "verplichte digitale identiteit", "digitale identiteit", "biometrische controle",
    "surveillance-grid", "luistert mee", "handhavers", "lokale valuta vervangen",
    "digitale munt", "objectivity-agents", "goedkeuring",

    "global grid", "central grid", "universal id", "global id", "central planning",
    "central authority", "one database", "single registry", "mandatory identity", "biometric authority",
    "remote enforcement", "population-wide tracking", "constant surveillance", "mass surveillance",
    "macro intervention", "wereldwijd grid", "mondiaal grid", "centraal grid", "centrale planning",
    "centrale autoriteit", "universeel id", "identificatie-eis", "biometrische autoriteit",
    "constante surveillance", "macro-ingrepen", "handhaving",
]

GRIP_MARKERS = [
    # Patch 30.1 Dutch grip markers: no audit, forced delegation, hard gates.
    "niemand mag auditen", "niet auditen", "zonder overleg", "geen overleg",
    "gedwongen hun stem", "stem te delegeren", "gecertificeerde expert",
    "geheim geschreven", "direct eigendom", "centraal orgaan",
    "verplichte dienst", "surveillance-grid", "één oncontroleerbaar individu",
    "een oncontroleerbaar individu", "verlichte dictator", "dictator",
    "verplichte digitale identiteit", "biometrische controle", "luistert mee",
    "deelt data", "handhavers", "goedkeuring", "objectivity-agents",
    "privé-uitgaven openbaar", "lokale valuta vervangen",

    "irrevocable", "irrevocable authority", "permanent control", "permanent authority",
    "no appeal", "without appeal", "no appeal path", "cannot be appealed", "cannot be questioned",
    "unquestionable", "final authority", "mandatory obedience", "emergency without sunset",
    "no sunset clause", "override courts", "bypass courts", "immune from audit", "rewrite records",
    "rewrite archives", "humans cannot intervene", "no human review", "no human input", "no human override",
    "without human input", "no input from humans", "without human review", "without human oversight",
    "no human oversight", "without human override", "humans have no say", "ai-only governance",
    "run by ai only", "run by ai and only ai", "only ai governs", "ai governs society",
    "ai runs society", "ai makes all decisions", "machine-run society", "fully automated governance",
    "society run by ai", "society is run by ai",
    "onherroepelijk", "onherroepelijke autoriteit", "permanente controle", "permanente macht",
    "geen bezwaar", "zonder bezwaar", "geen beroep", "zonder beroep", "kan niet worden bevraagd",
    "niet ter discussie", "definitieve autoriteit", "verplichte gehoorzaamheid", "geen noodstop",
    "zonder noodstop", "noodmacht zonder einddatum", "noodmacht zonder sunset", "geen sunset",
    "rechtbank omzeilen", "archief herschrijven", "geen menselijke review", "geen menselijke input",
    "zonder menselijke input", "geen menselijk toezicht", "zonder menselijk toezicht",
    "geen menselijke override", "zonder menselijke override", "mensen kunnen niet ingrijpen",
    "mensen hebben geen inspraak", "samenleving gerund door ai", "maatschappij gerund door ai",
    "alleen ai bestuurt", "ai bestuurt de samenleving", "ai bestuurt de maatschappij", "ai regeert",
]


def contextual_capture_hits(text):
    """Return capture patterns where soft rights/care language is coupled to coercive power.

    This is deliberately diagnostic: it does not treat every use of safety,
    objectivity, fairness, inclusion, or public-health language as good. When
    those words travel with mandatory ID, biometrics, surveillance, no appeal,
    central grids, forced compliance, private conversation monitoring, or access
    to basic needs conditioned on compliance, ALETHEIA applies stronger review
    pressure.
    """
    text = (text or "").lower()
    positive_hits = _hit_terms(text, POSITIVE_ETHICS_TERMS)
    coercive_hits = _hit_terms(text, COERCIVE_POWER_TERMS)
    multiplier_hits = _hit_terms(text, SAFETY_OBJECTIVITY_CAPTURE_POWER_TERMS)
    hard_hits = _hit_terms(text, SAFETY_OBJECTIVITY_HARD_CAPTURE_TERMS)
    if not positive_hits or not coercive_hits:
        return []

    severity_multiplier = 1.0
    if multiplier_hits:
        severity_multiplier += min(1.25, 0.25 * len(multiplier_hits))
    if hard_hits:
        severity_multiplier += 0.75
    severity_multiplier = round(min(3.0, severity_multiplier), 2)

    return [
        {
            "family": "Contextual Capture",
            "positive_terms": positive_hits[:6],
            "power_terms": coercive_hits[:6],
            "multiplier_terms": multiplier_hits[:8],
            "hard_capture_terms": hard_hits[:6],
            "severity_multiplier": severity_multiplier,
            "hard_capture_trigger": bool(hard_hits),
            "reason": "Positive care, safety, fairness, objectivity, inclusion, or public-health language is coupled to mandatory power or enforcement language.",
        }
    ]


def grip_marker_hits(text):
    """Return explicit grip/capture terms that should push ethics into critical review."""
    text = (text or "").lower()
    return _hit_terms(text, GRIP_MARKERS)


def micro_sovereignty_signal(text, governance_result=None, features=None):
    """Score whether the proposal keeps authority local, revocable, and human-reviewable.

    Higher means more local/human/revocable. Lower means more central/grid/identity/enforcement.
    """
    text = (text or "").lower()
    governance_result = governance_result or {}
    features = features or {}
    central_power = float(governance_result.get("power_concentration", features.get("centralization", 0.5)))
    local_hits = _count_hits(text, MICRO_SOVEREIGNTY_TERMS)
    macro_hits = _count_hits(text, MACRO_CAPTURE_TERMS)
    score = 0.52
    score += min(0.32, local_hits * 0.075)
    score -= min(0.36, macro_hits * 0.10)
    score -= min(0.20, central_power * 0.18)
    return _clamp(score)


def evaluate_ethics(text, governance_result=None, features=None):
    """
    Ethical stress test for governance ideas.

    Returns:
        ethics_score: 0-1
        verdict: text label
        dimensions: dict of ethical sub-scores
        strengths: list of positive drivers
        risks: list of ethical risk drivers
        confidence: 0-1
    """

    text = (text or "").lower()
    governance_result = governance_result or {}
    features = features or {}

    coercion_terms = [
        "forced", "force", "must obey", "obedience", "punish", "ban",
        "surveillance", "command", "take over", "mandatory control",
        "dictator", "supreme leader", "one world leader", "one leader",
        "runs the world", "rule the world", "single leader"
    ]

    fairness_terms = [
        "fair", "equal", "rights", "human right", "shared", "access",
        "proportional", "everyone", "public good", "universal",
        "free from profit", "community"
    ]

    transparency_terms = [
        "transparent", "transparency", "open", "public", "audited",
        "accountable", "traceable", "visible", "published", "explainable"
    ]

    accountability_terms = [
        "accountable", "oversight", "checks and balances", "jury",
        "referendum", "review", "audit", "appeal", "constitutional",
        "independent review"
    ]

    harm_terms = [
        "harm", "exploit", "profit-driven", "exclude", "punish",
        "surveillance", "war", "violence", "coerce", "forced",
        "dominate", "control"
    ]

    dignity_terms = [
        "dignity", "human right", "rights", "humanity", "everyone",
        "equal", "shared", "care", "healthcare", "housing",
        "education", "food", "water"
    ]

    central_power = float(governance_result.get("power_concentration", features.get("centralization", 0.5)))
    transparency_signal = float(governance_result.get("decision_transparency", features.get("transparency", 0.5)))
    regulation_signal = float(governance_result.get("regulatory_presence", features.get("regulation", 0.5)))
    anonymity_signal = float(governance_result.get("anonymity_level", features.get("anonymity", 0.3)))

    coercion_hits = _count_hits(text, coercion_terms)
    fairness_hits = _count_non_negated_hits(text, fairness_terms)
    transparency_hits = _count_non_negated_hits(text, transparency_terms)
    accountability_hits = _count_non_negated_hits(text, accountability_terms)
    harm_hits = _count_hits(text, harm_terms)
    dignity_hits = _count_non_negated_hits(text, dignity_terms)
    contextual_hits = contextual_capture_hits(text)
    grip_hits = grip_marker_hits(text)
    micro_sovereignty = micro_sovereignty_signal(text, governance_result=governance_result, features=features)

    consent = 0.70
    consent -= coercion_hits * 0.12
    consent -= central_power * 0.25

    fairness = 0.45
    fairness += fairness_hits * 0.10
    fairness -= central_power * 0.12

    transparency = 0.35
    transparency += transparency_signal * 0.45
    transparency += transparency_hits * 0.08
    transparency -= anonymity_signal * 0.12

    accountability = 0.35
    accountability += regulation_signal * 0.35
    accountability += accountability_hits * 0.10
    accountability -= central_power * 0.15

    non_harm = 0.65
    non_harm -= harm_hits * 0.10
    non_harm -= coercion_hits * 0.10
    non_harm -= central_power * 0.10

    dignity = 0.45
    dignity += dignity_hits * 0.10
    dignity += fairness_hits * 0.05
    dignity -= coercion_hits * 0.08

    contextual_multiplier = max([float(hit.get("severity_multiplier", 1.0)) for hit in contextual_hits] or [0.0])
    hard_contextual_capture = any(bool(hit.get("hard_capture_trigger")) for hit in contextual_hits)

    # Capture pattern: positive ethics language loses credit when paired with mandatory power.
    # Patch 28.1 strengthens this when safety/objectivity/fairness/inclusion/public-health
    # language is paired with ID, biometrics, surveillance, no appeal, central grids,
    # forced compliance, private monitoring, or basic-needs access gates.
    if contextual_hits:
        capture_scale = max(1.0, contextual_multiplier)
        consent -= 0.12 * capture_scale
        fairness -= 0.10 * capture_scale
        accountability -= 0.10 * capture_scale
        transparency -= 0.05 * capture_scale
        non_harm -= 0.06 * capture_scale
        dignity -= 0.05 * capture_scale
        micro_sovereignty = min(micro_sovereignty, 0.46 - min(0.18, (capture_scale - 1.0) * 0.08))
        if hard_contextual_capture:
            consent = min(consent, 0.30)
            accountability = min(accountability, 0.32)
            transparency = min(transparency, 0.38)
            non_harm = min(non_harm, 0.42)
            dignity = min(dignity, 0.44)
            micro_sovereignty = min(micro_sovereignty, 0.28)

    # Explicit grip markers are critical ethics signals, not ordinary word counts.
    if grip_hits:
        consent = min(consent, 0.26)
        accountability = min(accountability, 0.28)
        transparency = min(transparency, 0.34)
        non_harm = min(non_harm, 0.40)
        dignity = min(dignity, 0.42)
        micro_sovereignty = min(micro_sovereignty, 0.30)

    # Strong ethical penalty for single-ruler systems.
    single_ruler_terms = [
        "one world leader", "one leader", "runs the world",
        "rule the world", "world ruler", "global ruler",
        "single leader", "dictator", "supreme leader"
    ]

    if any(term in text for term in single_ruler_terms):
        consent = min(consent, 0.25)
        accountability = min(accountability, 0.25)
        transparency = min(transparency, 0.35)
        non_harm = min(non_harm, 0.40)
        dignity = min(dignity, 0.40)
        micro_sovereignty = min(micro_sovereignty, 0.28)

    # Strong ethical lift for universal public-good language only when it is not tied to grip/capture.
    if ("shared human right" in text or "free from profit" in text) and not contextual_hits and not grip_hits:
        fairness = max(fairness, 0.80)
        dignity = max(dignity, 0.80)
        non_harm = max(non_harm, 0.72)

    # Explicit safeguarded public systems should not be downgraded merely because they mention safety.
    has_public_safeguards = (
        _has_non_negated_term(text, ["appeal", "appeal errors", "bezwaar", "beroep"])
        and _has_non_negated_term(text, ["audit", "audited", "independent audit", "review", "oversight"])
        and _has_non_negated_term(text, ["sunset", "expires", "public vote", "renewed by public vote", "herroepbaar"])
        and _has_non_negated_term(text, ["open data", "publishes", "published", "transparent", "transparency", "public"])
        and not contextual_hits
        and not grip_hits
    )
    if has_public_safeguards:
        consent = max(consent, 0.74)
        fairness = max(fairness, 0.70)
        transparency = max(transparency, 0.78)
        accountability = max(accountability, 0.76)
        non_harm = max(non_harm, 0.70)
        dignity = max(dignity, 0.66)
        micro_sovereignty = max(micro_sovereignty, 0.66)

    dimensions = {
        "Consent": _clamp(consent),
        "Fairness": _clamp(fairness),
        "Transparency": _clamp(transparency),
        "Accountability": _clamp(accountability),
        "Non-Harm": _clamp(non_harm),
        "Human Dignity": _clamp(dignity),
        "Micro Sovereignty": _clamp(micro_sovereignty),
    }

    ethics_score = (
        dimensions["Consent"] * 0.18 +
        dimensions["Fairness"] * 0.17 +
        dimensions["Transparency"] * 0.13 +
        dimensions["Accountability"] * 0.14 +
        dimensions["Non-Harm"] * 0.14 +
        dimensions["Human Dignity"] * 0.14 +
        dimensions["Micro Sovereignty"] * 0.10
    )

    if grip_hits:
        ethics_score = min(ethics_score, 0.42)
    if contextual_hits:
        if hard_contextual_capture:
            ethics_score = min(ethics_score, 0.46)
        elif contextual_multiplier >= 2.0:
            ethics_score = min(max(ethics_score, 0.46), 0.52)
        else:
            ethics_score = min(max(ethics_score, 0.50), 0.58)

    if ethics_score >= 0.72:
        verdict = "ETHICALLY STRONG"
    elif ethics_score >= 0.50:
        verdict = "ETHICALLY AMBIGUOUS"
    else:
        verdict = "ETHICALLY HIGH-RISK"

    risks = []
    strengths = []

    if central_power > 0.70:
        risks.append("High power concentration")
    if coercion_hits > 0:
        risks.append("Coercive or command-oriented language detected")
    if contextual_hits:
        risks.append("Positive rights, care, safety, objectivity, inclusion, or public-health language is coupled to mandatory power or enforcement")
        if hard_contextual_capture:
            risks.append("Hard safety/objectivity capture trigger detected: ID, biometrics, surveillance, no appeal, central truth gate, or basic-needs access conditioning")
    if grip_hits:
        risks.append("Grip marker detected: irrevocable, permanent, no-appeal, or no-human-review authority")
    if dimensions["Consent"] < 0.45:
        risks.append("Weak consent structure")
    if dimensions["Accountability"] < 0.45:
        risks.append("Weak accountability or correction mechanism")
    if dimensions["Transparency"] < 0.45:
        risks.append("Low transparency")
    if dimensions["Human Dignity"] < 0.45:
        risks.append("Human dignity risk")
    if dimensions["Micro Sovereignty"] < 0.45:
        risks.append("Weak micro-sovereignty: authority appears too central, mandatory, or hard to revoke")

    if fairness_hits > 0 and not contextual_hits:
        strengths.append("Fairness-oriented language detected")
    if transparency_hits > 0:
        strengths.append("Transparency-oriented language detected")
    if accountability_hits > 0:
        strengths.append("Accountability mechanism detected")
    if dignity_hits > 0 and not contextual_hits:
        strengths.append("Human dignity / public-good language detected")
    if dimensions["Micro Sovereignty"] >= 0.65:
        strengths.append("Local, revocable, or human-reviewable authority signal detected")
    if central_power < 0.40:
        strengths.append("Low concentration of power")

    signal_count = (
        coercion_hits + fairness_hits + transparency_hits +
        accountability_hits + harm_hits + dignity_hits + len(grip_hits) + len(contextual_hits)
    )

    confidence = 0.40
    confidence += min(0.30, len(text) / 300)
    confidence += min(0.25, signal_count * 0.04)
    confidence += 0.05 if governance_result else 0

    return {
        "ethics_score": _clamp(ethics_score),
        "verdict": verdict,
        "dimensions": dimensions,
        "strengths": strengths if strengths else ["No strong ethical strengths detected"],
        "risks": risks if risks else ["No major ethical risk driver detected"],
        "confidence": _clamp(confidence),
        "contextual_capture_hits": contextual_hits,
        "contextual_capture_count": len(contextual_hits),
        "grip_marker_hits": grip_hits,
        "grip_marker_count": len(grip_hits),
        "micro_sovereignty": dimensions["Micro Sovereignty"],
        "ethics_verdict": verdict,
        "ethics_adjusted_integrity": _clamp(ethics_score),
    }



def apply_ethics_to_metrics(sim, report, ethics_diagnostics):
    """Apply contextual ethics pressure to visible Mirror Check metrics.

    This is a bounded calibration layer. It does not replace protocol hard
    overrides; it makes the displayed numeric metrics match the ethics reading
    when contextual capture, grip markers, or weak micro-sovereignty are present.

    Returns fresh ``(sim, report)`` dictionaries and preserves the previous
    values in ``report["raw_metrics_before_ethics"]``.
    """
    sim = dict(sim or {})
    report = dict(report or {})
    ethics = dict(ethics_diagnostics or {})
    dimensions = dict(ethics.get("dimensions") or {})

    contextual_hits = list(ethics.get("contextual_capture_hits") or [])
    contextual_count = len(contextual_hits)
    contextual_multiplier = max([float(hit.get("severity_multiplier", 1.0)) for hit in contextual_hits] or [0.0])
    hard_contextual_capture = any(bool(hit.get("hard_capture_trigger")) for hit in contextual_hits)
    grip_count = len(ethics.get("grip_marker_hits") or [])
    ethics_score = float(ethics.get("ethics_score", 1.0) or 1.0)
    micro_sovereignty = float(dimensions.get("Micro Sovereignty", 0.5) or 0.5)
    ethics_verdict = str(ethics.get("verdict", "")).upper()

    raw_metrics = {
        "integrity": report.get("integrity"),
        "friction": report.get("friction"),
        "collapse_probability": report.get("collapse_probability"),
        "trust_friction": report.get("trust_friction"),
        "stability": sim.get("stability"),
        "trust_index": sim.get("trust_index"),
        "alignment": sim.get("alignment"),
        "ego": sim.get("ego"),
        "collapse_risk": sim.get("collapse_risk"),
    }
    report["raw_metrics_before_ethics"] = raw_metrics
    report["ethics_diagnostics"] = ethics
    report["ethics_adjusted_integrity"] = round(_clamp(min(float(report.get("integrity", 1.0) or 1.0), ethics_score)), 4)

    raw_integrity = float(report.get("integrity", 1.0) or 1.0)
    integrity_gap = max(0.0, raw_integrity - ethics_score)
    weak_micro = max(0.0, 0.45 - micro_sovereignty)
    ethical_deficit = max(0.0, 0.72 - ethics_score)
    has_ethics_pressure = (
        contextual_count > 0
        or grip_count > 0
        or micro_sovereignty < 0.35
        or (integrity_gap > 0.05 and micro_sovereignty < 0.65)
        or "HIGH-RISK" in ethics_verdict
    )

    if not has_ethics_pressure:
        report["ethics_adjustment_applied"] = False
        report["ethics_adjustment_reason"] = {
            "contextual_capture_count": contextual_count,
            "grip_marker_count": grip_count,
            "micro_sovereignty": round(_clamp(micro_sovereignty), 4),
            "integrity_gap": round(_clamp(integrity_gap), 4),
            "total_ethics_pressure": 0.0,
        }
        return sim, report

    raw_friction = float(report.get("friction", 0.0) or 0.0)
    raw_trust_friction = float(report.get("trust_friction", 0.0) or 0.0)
    raw_collapse = float(report.get("collapse_probability", 0.0) or 0.0)
    raw_stability = float(sim.get("stability", 1.0) or 1.0)
    raw_alignment = float(sim.get("alignment", 1.0) or 1.0)
    raw_trust = float(sim.get("trust_index", 1.0) or 1.0)
    raw_ego = float(sim.get("ego", 0.0) or 0.0)

    # Core visible score: ethics cannot improve integrity, only bound it.
    adjusted_integrity = min(raw_integrity, ethics_score)

    # Contextual capture creates friction; grip creates stronger non-linear ego pressure.
    grip_pressure = min(0.65, 0.12 * (grip_count ** 2))
    contextual_pressure = min(0.38, 0.10 * contextual_count * max(1.0, contextual_multiplier))
    if hard_contextual_capture:
        contextual_pressure = max(contextual_pressure, 0.28)
    micro_pressure = min(0.20, weak_micro * 0.55)
    ethics_pressure = min(0.30, ethical_deficit * 0.35)
    total_pressure = _clamp(grip_pressure + contextual_pressure + micro_pressure + ethics_pressure)

    adjusted_ego = max(raw_ego, _clamp(total_pressure))
    adjusted_friction = max(raw_friction, _clamp(raw_friction + contextual_pressure + grip_pressure * 0.55 + micro_pressure))
    adjusted_trust_friction = max(raw_trust_friction, _clamp(raw_trust_friction + contextual_pressure * 0.70 + grip_pressure * 0.45 + micro_pressure))

    # Trust/alignment remain high only when the ethics layer sees no capture pressure.
    alignment_ceiling = _clamp(0.95 - total_pressure * 0.85 - max(0.0, 0.50 - ethics_score) * 0.45)
    trust_ceiling = _clamp(0.98 - total_pressure * 0.65 - max(0.0, 0.50 - ethics_score) * 0.35)
    adjusted_alignment = min(raw_alignment, alignment_ceiling)
    adjusted_trust = min(raw_trust, trust_ceiling)

    stability_ceiling = _clamp(0.90 - total_pressure * 0.75 - max(0.0, 0.50 - ethics_score) * 0.35)
    adjusted_stability = min(raw_stability, stability_ceiling)

    collapse_floor = _clamp(raw_collapse + total_pressure * 0.65 + max(0.0, 0.50 - ethics_score) * 0.25)
    adjusted_collapse = max(raw_collapse, collapse_floor)

    report["integrity"] = round(_clamp(adjusted_integrity), 4)
    report["friction"] = round(_clamp(adjusted_friction), 4)
    report["trust_friction"] = round(_clamp(adjusted_trust_friction), 4)
    report["collapse_probability"] = round(_clamp(adjusted_collapse), 3)
    report["ethics_adjustment_applied"] = True
    report["ethics_adjustment_reason"] = {
        "contextual_capture_count": contextual_count,
        "contextual_capture_multiplier": round(max(1.0, contextual_multiplier), 4) if contextual_count else 0.0,
        "hard_contextual_capture": hard_contextual_capture,
        "grip_marker_count": grip_count,
        "micro_sovereignty": round(_clamp(micro_sovereignty), 4),
        "integrity_gap": round(_clamp(integrity_gap), 4),
        "total_ethics_pressure": round(_clamp(total_pressure), 4),
    }

    sim["stability"] = round(_clamp(adjusted_stability), 4)
    sim["alignment"] = round(_clamp(adjusted_alignment), 4)
    sim["trust_index"] = round(_clamp(adjusted_trust), 4)
    sim["ego"] = round(_clamp(adjusted_ego), 4)
    sim["ethics_pressure"] = round(_clamp(total_pressure), 4)
    if adjusted_collapse >= 0.50 or grip_count >= 3 or "HIGH-RISK" in ethics_verdict:
        sim["collapse_risk"] = True

    return sim, report
