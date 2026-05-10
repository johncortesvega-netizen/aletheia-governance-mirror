import re

# ---------------------------------------------------------------------------
# Keyword maps — richer than binary 0.7/0.3 matching
# ---------------------------------------------------------------------------

ANONYMITY_HIGH  = ["anonymous", "hidden", "untraceable", "offshore", "shell",
                   "pseudonym", "dark", "unidentified", "covert", "secret"]
ANONYMITY_LOW   = ["transparent", "named", "identified", "public", "disclosed",
                   "registered", "verified", "open", "known"]

CENTRAL_HIGH    = ["ceo", "dictator", "monopoly", "single", "centralised", "centralized",
                   "autocrat", "sole", "one man", "one person", "chairman", "sovereign"]
CENTRAL_LOW     = ["distributed", "decentralised", "decentralized", "committee",
                   "board", "democratic", "collective", "consortium", "network"]

CAPITAL_HIGH    = ["billion", "$", "trillion", "hedge fund", "investment bank",
                   "private equity", "fund", "capital", "endowment", "vc"]
CAPITAL_LOW     = ["nonprofit", "ngo", "charity", "grant", "small", "startup",
                   "bootstrap", "volunteer", "community"]

REGULATION_HIGH = ["regulated", "compliance", "law", "legal", "legislation",
                   "oversight", "audit", "licensed", "certified", "enforced",
                   "statutory", "government", "treaty", "sanctioned"]
REGULATION_LOW  = ["unregulated", "deregulated", "loophole", "grey area",
                   "informal", "unlicensed", "shadow", "unofficial", "tax haven"]

TECH_HIGH       = ["ai", "machine learning", "algorithm", "autonomous", "blockchain",
                   "software", "model", "neural", "automated", "digital",
                   "cyber", "quantum", "robotics", "llm", "gpt"]
TECH_LOW        = ["manual", "human", "analogue", "paper", "face to face",
                   "physical", "traditional", "brick"]

OPAQUE_HIGH     = ["opaque", "secret", "classified", "hidden agenda", "undisclosed",
                   "black box", "nda", "confidential", "proprietary", "closed"]
OPAQUE_LOW      = ["transparent", "open", "public", "disclosed", "published",
                   "accountable", "auditable", "open source"]

# Actor / stakeholder keywords → ideology hint
ACTOR_PATTERNS = {
    "regulator":  ["government", "regulator", "authority", "ministry", "agency",
                   "central bank", "sec", "ofgem", "watchdog", "commission"],
    "operator":   ["company", "firm", "corporation", "operator", "provider",
                   "vendor", "supplier", "business", "enterprise", "startup"],
    "market":     ["market", "exchange", "investor", "trader", "hedge fund",
                   "stock", "commodity", "fund", "capital"],
    "public":     ["public", "citizen", "user", "consumer", "society",
                   "community", "population", "people", "voter"],
    "tech_layer": ["ai", "algorithm", "system", "model", "platform",
                   "software", "infrastructure", "network"],
    "capital":    ["bank", "capital", "finance", "lender", "creditor",
                   "investor", "fund", "wealth", "asset"],
}

# ---------------------------------------------------------------------------
# Scoring helper
# ---------------------------------------------------------------------------

def _score(text, high_words, low_words, default=0.40):
    """Returns a 0-1 score based on keyword presence, graduated."""
    high_hits = sum(1 for w in high_words if w in text)
    low_hits  = sum(1 for w in low_words  if w in text)
    if high_hits == 0 and low_hits == 0:
        return default
    total = high_hits + low_hits
    return round(min(0.95, max(0.05, high_hits / total)), 3)


# ---------------------------------------------------------------------------
# extract_features — primary rule-based extractor (upgraded)
# ---------------------------------------------------------------------------

def extract_features(text: str) -> dict:
    t = text.lower()
    return {
        "anonymity":           _score(t, ANONYMITY_HIGH, ANONYMITY_LOW,  default=0.35),
        "centralization":      _score(t, CENTRAL_HIGH,   CENTRAL_LOW,    default=0.45),
        "capital_scale":       _score(t, CAPITAL_HIGH,   CAPITAL_LOW,    default=0.40),
        "regulation":          _score(t, REGULATION_HIGH, REGULATION_LOW, default=0.40),
        "technical_complexity": _score(t, TECH_HIGH,     TECH_LOW,       default=0.35),
        "transparency":        _score(t, OPAQUE_LOW,     OPAQUE_HIGH,    default=0.55),
    }


# ---------------------------------------------------------------------------
# extract_actors — identify stakeholder types present in scenario
# ---------------------------------------------------------------------------

def extract_actors(text: str) -> list[str]:
    """Returns list of actor archetypes detected in the scenario text."""
    t = text.lower()
    found = []
    for actor, keywords in ACTOR_PATTERNS.items():
        if any(kw in t for kw in keywords):
            found.append(actor)
    # Always include public as a passive stakeholder
    if "public" not in found:
        found.append("public")
    return found


# ---------------------------------------------------------------------------
# normalize_features — maps LLM output dict to standard feature keys
# ---------------------------------------------------------------------------

def normalize_features(llm_data: dict | None) -> dict | None:
    if llm_data is None:
        return None
    key_map = {
        "anonymity":            "anonymity_level",
        "centralization":       "power_concentration",
        "capital_scale":        "capital_scale",
        "regulation":           "regulatory_presence",
        "technical_complexity": "technical_complexity",
        "transparency":         "decision_transparency",
    }
    result = {}
    for target_key, source_key in key_map.items():
        val = llm_data.get(source_key)
        if val is not None:
            result[target_key] = float(val)
    return result if result else None


# ---------------------------------------------------------------------------
# blend_features — weighted blend of rule-based and LLM features
# ---------------------------------------------------------------------------

def blend_features(rule_f: dict, llm_f: dict | None, alpha: float = 0.65) -> dict:
    """
    alpha: weight given to LLM features (0 = pure rule, 1 = pure LLM).
    Slightly higher alpha than original (0.60) because LLM is richer.
    """
    if llm_f is None:
        return rule_f
    return {
        k: round(alpha * llm_f.get(k, rule_f[k]) + (1 - alpha) * rule_f[k], 4)
        for k in rule_f
    }


# ---------------------------------------------------------------------------
# feature_summary — human-readable explanation of what was detected
# ---------------------------------------------------------------------------

def feature_summary(features: dict) -> dict:
    """Returns plain-English interpretation of each feature score."""
    def level(v):
        if v > 0.68: return "high"
        if v > 0.42: return "moderate"
        return "low"

    labels = {
        "anonymity":            ("actor anonymity",       "actors are identifiable",    "actors are anonymous/hidden"),
        "centralization":       ("power centralization",  "power is distributed",       "power is highly concentrated"),
        "capital_scale":        ("capital scale",         "low-capital context",        "large capital flows involved"),
        "regulation":           ("regulatory presence",   "minimal oversight",          "strong regulatory framework"),
        "technical_complexity": ("technical complexity",  "low-tech context",           "high-tech / AI-driven system"),
        "transparency":         ("transparency",          "low transparency",           "high transparency"),
    }

    result = {}
    for k, v in features.items():
        label, low_desc, high_desc = labels.get(k, (k, "low", "high"))
        lv = level(v)
        desc = high_desc if v > 0.55 else (low_desc if v < 0.45 else f"moderate {label}")
        result[k] = {"score": v, "level": lv, "description": desc}
    return result
