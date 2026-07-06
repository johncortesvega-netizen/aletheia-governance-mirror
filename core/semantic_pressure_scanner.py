"""Deterministic semantic pressure scanner for ALETHEIA.

This module upgrades simple keyword matching into relationship-aware pattern
checks without adding a heavy NLP dependency. It is intentionally conservative:
unknown governance language with soft claims and no mechanisms is routed to a
human-review warning instead of being treated as low-risk.

The scanner is a mirror signal extractor. It does not certify intent, legality,
safety, ethics, or final legitimacy.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import re
from typing import Iterable

TOKEN_RE = re.compile(r"[a-zA-ZÀ-ÿ0-9_\-']+")

# Soft claim language: values and rhetorical goods that can be sincere, but are
# not operational safeguards by themselves.
CLAIM_TERMS: tuple[str, ...] = (
    "care", "harmony", "safety", "secure", "security", "inclusive", "inclusion",
    "protect", "protection", "dignity", "freedom", "justice", "fairness",
    "equity", "transparency", "accountability", "trust", "optimize", "optimization",
    "efficiency", "resilience", "integrity", "wellbeing", "public good", "service",
    "zorg", "harmonie", "veiligheid", "inclusief", "inclusiviteit", "bescherming",
    "waardigheid", "vrijheid", "rechtvaardigheid", "eerlijkheid", "transparantie",
    "verantwoording", "vertrouwen", "optimalisatie", "efficientie", "publiek belang",
)

# Hard mechanism language: concrete structures that make claims reviewable,
# contestable, reversible, or limited.
MECHANISM_TERMS: tuple[str, ...] = (
    "appeal", "appeals", "appealed", "appealable", "appeal window", "audit", "audits", "audited", "independently audited", "independent audit", "audit trail", "public audit", "time limit",
    "term limit", "review window", "within 30 days", "expiry", "automatic expiry", "sunset", "revocation", "revoke", "revoked", "reversible", "fallback",
    "human review", "human override", "reviewed", "review", "independent review", "independent oversight",
    "independent challenge", "correction", "rectification", "evidence requirement",
    "evidence standard", "exit right", "opt-out", "withdrawal", "non-retaliation",
    "plain-language notice", "public reasoning", "ombudsman", "due process",
    "beroepsprocedure", "beroep", "in beroep", "auditlog", "geaudit", "onafhankelijk geaudit", "publieke audit", "tijdslimiet",
    "termijn", "binnen 30 dagen", "vervaldatum", "automatische vervaldatum", "herroeping", "herroepen", "herroepbaar", "fallback", "noodpad",
    "menselijke review", "menselijke controle", "menselijke override", "onafhankelijke review",
    "onafhankelijk toezicht", "onafhankelijke toetsing", "correctie", "bewijsvereiste",
    "bewijsstandaard", "exitrecht", "opt-out", "intrekken", "geen vergelding",
    "bezwaar", "uitleg", "bezwaarprocedure", "hoor en wederhoor",
)

GRIP_TERMS: tuple[str, ...] = (
    "must", "shall", "required", "mandatory", "obliged", "compulsory", "only if",
    "only after", "only possible after", "after identity verification", "conditioned on", "conditional on", "requires", "require", "required for access", "unless verified", "non-compliance", "suspend",
    "terminated", "irrevocable", "permanent", "without appeal", "without fallback",
    "no appeal", "no fallback", "cannot refuse", "may not refuse", "access denied",
    "moet", "moeten", "dient", "dienen", "verplicht", "vereist", "alleen als",
    "enkel mogelijk na", "alleen mogelijk na", "pas mogelijk na", "na identiteitsverificatie", "voorwaarde", "voorwaardelijk",
    "non-compliance", "niet-naleving", "opschorten", "beeindigd", "beëindigd",
    "onherroepelijk", "permanent", "zonder beroep", "zonder fallback",
    "geen beroep", "geen alternatief", "kan niet weigeren", "toegang geweigerd",
)

ACCESS_TERMS: tuple[str, ...] = (
    "access", "public benefits", "basic benefits", "essential services", "basic services", "service", "services", "benefits", "welfare", "housing", "food", "water",
    "medical", "healthcare", "care", "license", "licence", "application", "account",
    "work", "education", "safety",
    "toegang", "publieke voorzieningen", "basisvoorzieningen", "basisdiensten", "dienst", "diensten", "uitkering", "toeslagen", "huisvesting", "woning", "voedsel",
    "water", "medisch", "zorg", "licentie", "applicatie", "account",
    "werk", "onderwijs", "veiligheid",
)

IDENTITY_TERMS: tuple[str, ...] = (
    "identity", "id", "identity verification", "id verification", "verified identity",
    "biometric", "biometric verification", "verification", "verified",
    "identiteit", "identiteitsverificatie", "id-verificatie", "geverifieerde identiteit",
    "biometrisch", "biometrische verificatie", "verificatie", "geverifieerd",
)

CENTRAL_AUTHORITY_TERMS: tuple[str, ...] = (
    "central office", "central authority", "centralized authority", "centralised authority",
    "central control", "single authority", "single office", "administrative authority",
    "central administrator", "centralized control", "centralised control",
    "centraal kantoor", "centrale autoriteit", "gecentraliseerde autoriteit",
    "centrale controle", "enkele autoriteit", "centrale beheerder",
)

EMERGENCY_POWER_TERMS: tuple[str, ...] = (
    "emergency authority", "emergency power", "emergency powers", "crisis authority",
    "crisis power", "crisis powers", "emergency mandate", "state of emergency",
    "during crisis", "during a crisis", "emergency control", "temporary emergency authority",
    "noodbevoegdheid", "noodbevoegdheden", "crisisbevoegdheid", "crisisbevoegdheden",
    "noodmandaat", "noodtoestand", "tijdens crisis", "tijdens een crisis",
)

WEAK_SAFEGUARD_TERMS: tuple[str, ...] = (
    "limited notice", "short notice", "without notice", "no notice", "unclear notice",
    "unclear appeal", "unclear appeal rights", "appeal rights unclear", "limited appeal",
    "limited public notice", "unclear public notice", "opaque appeal",
    "beperkte kennisgeving", "zonder kennisgeving", "geen kennisgeving",
    "onduidelijk beroep", "onduidelijke beroepsrechten", "beperkt beroep",
)

PERMANENCE_TERMS: tuple[str, ...] = (
    "irrevocable", "permanent", "cannot be reversed", "final", "forever",
    "without appeal", "no appeal", "automatic termination", "terminated automatically",
    "onherroepelijk", "permanent", "kan niet worden teruggedraaid", "definitief",
    "voor altijd", "zonder beroep", "geen beroep", "automatisch beëindigd",
)

SOVEREIGNTY_TERMS: tuple[str, ...] = (
    "may", "can", "right to", "has the right", "appeal", "appealed", "appealable", "revoke", "revoked", "revocation", "withdraw",
    "opt out", "fallback", "human review", "reviewed", "review window", "challenge", "correction", "audit", "audited", "independent audit", "independently audited", "time limit", "within 30 days", "at any time",
    "mag", "kan", "heeft het recht", "recht om", "beroep", "herroepen",
    "intrekken", "opt-out", "alternatief", "menselijke review", "bezwaar", "correctie",
    "te allen tijde", "op elk moment",
)

ENTITY_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}\b", "[ACTOR_A]"),
    (r"\b[A-Z][A-Za-z0-9_\-]{2,}(?:\s+(?:Protocol|System|Council|Agency|Model|App|DAO|Foundation))\b", "[SYSTEM_X]"),
    (r"\b(?:[A-Z]{2,}|[A-Z][a-z]+(?:DAO|AI|ID|Gov|Net))\b", "[SYSTEM_X]"),
)


@dataclass(frozen=True)
class ProximityHit:
    category: str
    left: str
    right: str
    distance: int
    excerpt: str


@dataclass(frozen=True)
class SemanticPressureScan:
    state: str
    risk: str
    integrity_adjustment: float
    claim_count: int
    mechanism_count: int
    claim_to_mechanism_ratio: float
    modal_pressure_count: int
    sovereignty_count: int
    proximity_hits: tuple[ProximityHit, ...]
    fail_closed: bool
    normalized_text: str
    notes: tuple[str, ...]

    def to_dict(self) -> dict:
        data = asdict(self)
        data["proximity_hits"] = [asdict(hit) for hit in self.proximity_hits]
        return data


def normalize_entities(text: str) -> str:
    """Replace named actors/systems with generic tokens before analysis."""
    normalized = text or ""
    for pattern, replacement in ENTITY_PATTERNS:
        normalized = re.sub(pattern, replacement, normalized)
    return normalized


def _lower(text: str) -> str:
    return (text or "").lower()


def _tokens(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_RE.finditer(text or "")]


def _count_terms(text: str, terms: Iterable[str]) -> int:
    lower = _lower(text)
    count = 0
    for term in terms:
        if " " in term:
            count += lower.count(term.lower())
        else:
            count += sum(1 for token in _tokens(lower) if token == term.lower())
    return count


def _find_term_positions(tokens: list[str], terms: Iterable[str]) -> list[tuple[int, str]]:
    positions: list[tuple[int, str]] = []
    token_text = " ".join(tokens)
    for term in terms:
        parts = term.lower().split()
        if not parts:
            continue
        if len(parts) == 1:
            positions.extend((idx, term) for idx, token in enumerate(tokens) if token == parts[0])
            continue
        # For phrases, scan token windows. This keeps the dependency/proximity
        # logic deterministic and deploy-safe without spaCy.
        width = len(parts)
        for idx in range(max(0, len(tokens) - width + 1)):
            if tokens[idx : idx + width] == parts:
                positions.append((idx, term))
    return sorted(positions, key=lambda item: item[0])


def _sentence_contains(text: str, term_group: Iterable[str]) -> bool:
    return _count_terms(text, term_group) > 0


def _sentence_identity_gate(text: str) -> bool:
    """Detect access gated by identity/verification in the same sentence.

    This catches phrases like "Access to public benefits is only possible after
    identity verification", where the pressure is the relationship between
    access, conditionality, and identity verification rather than any single word.
    """
    sentences = re.split(r"(?<=[.!?;])\s+|\n+", text or "")
    for sentence in sentences:
        if (
            _sentence_contains(sentence, ACCESS_TERMS)
            and _sentence_contains(sentence, GRIP_TERMS)
            and _sentence_contains(sentence, IDENTITY_TERMS)
        ):
            return True
    return False


def _sentence_emergency_service_control(text: str) -> bool:
    """Detect emergency/centralized authority over essential services.

    This catches governance wording where a central actor receives crisis or
    emergency authority over basic/essential services, especially when public
    notice or appeal rights are limited or unclear.
    """
    sentences = re.split(r"(?<=[.!?;])\s+|\n+", text or "")
    for sentence in sentences:
        has_central_or_emergency = (
            _sentence_contains(sentence, CENTRAL_AUTHORITY_TERMS)
            or _sentence_contains(sentence, EMERGENCY_POWER_TERMS)
        )
        if (
            has_central_or_emergency
            and _sentence_contains(sentence, ACCESS_TERMS)
            and (
                _sentence_contains(sentence, WEAK_SAFEGUARD_TERMS)
                or _sentence_contains(sentence, GRIP_TERMS)
                or _sentence_contains(sentence, EMERGENCY_POWER_TERMS)
            )
        ):
            return True
    return False


def _excerpt(tokens: list[str], center_a: int, center_b: int, radius: int = 8) -> str:
    start = max(0, min(center_a, center_b) - radius)
    end = min(len(tokens), max(center_a, center_b) + radius + 1)
    return " ".join(tokens[start:end])


def proximity_scan(text: str, *, window: int = 9) -> tuple[ProximityHit, ...]:
    """Detect relationship-aware pressure signals.

    The main high-value pair is [grip/condition] near [access/basic need].
    A second pair catches [permanence] near [access/basic need].
    """
    tokens = _tokens(text)
    grip_positions = _find_term_positions(tokens, GRIP_TERMS)
    access_positions = _find_term_positions(tokens, ACCESS_TERMS)
    permanence_positions = _find_term_positions(tokens, PERMANENCE_TERMS)
    central_positions = _find_term_positions(tokens, CENTRAL_AUTHORITY_TERMS)
    emergency_positions = _find_term_positions(tokens, EMERGENCY_POWER_TERMS)
    weak_safeguard_positions = _find_term_positions(tokens, WEAK_SAFEGUARD_TERMS)

    hits: list[ProximityHit] = []
    if _sentence_identity_gate(text):
        hits.append(
            ProximityHit(
                category="identity_gated_access",
                left="conditional access",
                right="identity / verification",
                distance=0,
                excerpt=(text or "").strip()[:220],
            )
        )
    if _sentence_emergency_service_control(text):
        hits.append(
            ProximityHit(
                category="emergency_service_control",
                left="central/emergency authority",
                right="essential/basic services + weak safeguards",
                distance=0,
                excerpt=(text or "").strip()[:220],
            )
        )
    for left_idx, left_term in grip_positions:
        for right_idx, right_term in access_positions:
            distance = abs(left_idx - right_idx)
            if distance <= window:
                hits.append(
                    ProximityHit(
                        category="grip_near_access",
                        left=left_term,
                        right=right_term,
                        distance=distance,
                        excerpt=_excerpt(tokens, left_idx, right_idx),
                    )
                )
    for left_idx, left_term in permanence_positions:
        for right_idx, right_term in access_positions:
            distance = abs(left_idx - right_idx)
            if distance <= window:
                hits.append(
                    ProximityHit(
                        category="permanence_near_access",
                        left=left_term,
                        right=right_term,
                        distance=distance,
                        excerpt=_excerpt(tokens, left_idx, right_idx),
                    )
                )

    for left_idx, left_term in (*central_positions, *emergency_positions):
        for right_idx, right_term in access_positions:
            distance = abs(left_idx - right_idx)
            if distance <= window + 3:
                hits.append(
                    ProximityHit(
                        category="authority_near_services",
                        left=left_term,
                        right=right_term,
                        distance=distance,
                        excerpt=_excerpt(tokens, left_idx, right_idx),
                    )
                )
    for left_idx, left_term in weak_safeguard_positions:
        for right_idx, right_term in (*central_positions, *emergency_positions):
            distance = abs(left_idx - right_idx)
            if distance <= window + 5:
                hits.append(
                    ProximityHit(
                        category="weak_safeguard_near_authority",
                        left=left_term,
                        right=right_term,
                        distance=distance,
                        excerpt=_excerpt(tokens, left_idx, right_idx),
                    )
                )

    # Deduplicate identical phrase/category combinations so UI output stays clean.
    seen: set[tuple[str, str, str, str]] = set()
    clean: list[ProximityHit] = []
    for hit in hits:
        key = (hit.category, hit.left, hit.right, hit.excerpt)
        if key not in seen:
            seen.add(key)
            clean.append(hit)

    priority = {
        "identity_gated_access": 0,
        "emergency_service_control": 1,
        "authority_near_services": 2,
        "weak_safeguard_near_authority": 3,
        "grip_near_access": 4,
        "permanence_near_access": 5,
    }
    clean.sort(key=lambda hit: (priority.get(hit.category, 9), hit.distance, hit.left, hit.right))
    return tuple(clean[:8])


def scan_semantic_pressure(text: str, *, governance_context: bool = True) -> SemanticPressureScan:
    """Run fail-closed semantic pressure checks on unstructured text."""
    raw = text or ""
    normalized = normalize_entities(raw)
    claims = _count_terms(normalized, CLAIM_TERMS)
    mechanisms = _count_terms(normalized, MECHANISM_TERMS)
    modal_pressure = (
        _count_terms(normalized, GRIP_TERMS)
        + _count_terms(normalized, PERMANENCE_TERMS)
        + _count_terms(normalized, EMERGENCY_POWER_TERMS)
        + _count_terms(normalized, CENTRAL_AUTHORITY_TERMS)
        + _count_terms(normalized, WEAK_SAFEGUARD_TERMS)
    )
    sovereignty = _count_terms(normalized, SOVEREIGNTY_TERMS)
    hits = proximity_scan(normalized)
    identity_gate = _sentence_identity_gate(normalized)
    emergency_service_control = _sentence_emergency_service_control(normalized)

    ratio = float(claims / max(mechanisms, 1))
    notes: list[str] = []
    fail_closed = False
    adjustment = 0.0

    if hits:
        notes.append("Contextual pressure detected: grip/permanence language appears close to access, identity, service, or basic-rights terms.")
        adjustment -= 0.18
    if identity_gate:
        notes.append("Identity-gated access pattern: access/basic-service language is conditioned on identity or verification in the same sentence.")
        adjustment -= 0.14
    if emergency_service_control:
        notes.append("Emergency/central authority over basic services: crisis or central-office authority is linked to essential services while notice or appeal safeguards look limited or unclear.")
        adjustment -= 0.18
    if claims >= 3 and mechanisms == 0:
        notes.append("Rhetoric-to-mechanism gap: soft ethical claims appear without concrete safeguards.")
        adjustment -= 0.16
    elif ratio >= 3.0 and claims >= 3:
        notes.append("Claims outweigh mechanisms: values language is stronger than visible operational safeguards.")
        adjustment -= 0.10
    if modal_pressure > sovereignty:
        notes.append("Modal pressure outweighs sovereignty language: obligation or permanence terms exceed appeal, revocation, fallback, or choice language.")
        adjustment -= 0.08
    if mechanisms >= 2 and sovereignty >= 1 and not hits and not identity_gate and not emergency_service_control:
        notes.append("Concrete safeguards detected: appeal, audit, review, revocation, time-limit, or reversibility language is visible.")
    if governance_context and claims > 0 and mechanisms == 0 and not hits:
        fail_closed = True
        notes.append("Fail-closed review: governance/value language was detected, but no recognizable safeguard structure was found.")
        adjustment -= 0.12
    if not notes:
        notes.append("No strong semantic pressure pattern detected by this deterministic scanner. Human review still required.")

    if hits or identity_gate or emergency_service_control or fail_closed or adjustment <= -0.24:
        state = "THRESHOLD"
        risk = "Needs safeguards"
    elif adjustment <= -0.10:
        state = "THRESHOLD"
        risk = "Review recommended"
    else:
        state = "SANCTUARY"
        risk = "No strong pattern detected"

    if governance_context and claims > 0 and mechanisms == 0 and modal_pressure >= 2:
        state = "ASYLUM"
        risk = "High pressure / unverifiable claims"
        fail_closed = True

    return SemanticPressureScan(
        state=state,
        risk=risk,
        integrity_adjustment=round(float(adjustment), 3),
        claim_count=claims,
        mechanism_count=mechanisms,
        claim_to_mechanism_ratio=round(ratio, 2),
        modal_pressure_count=modal_pressure,
        sovereignty_count=sovereignty,
        proximity_hits=hits,
        fail_closed=fail_closed,
        normalized_text=normalized,
        notes=tuple(notes),
    )


def format_semantic_pressure_report(scan: SemanticPressureScan) -> str:
    """Return a compact plain-text report for Streamlit code blocks/receipts."""
    lines = [
        "Semantic Pressure Scan",
        "",
        f"Internal review state: {scan.state}",
        f"Risk note: {scan.risk}",
        f"Integrity pressure adjustment: {scan.integrity_adjustment:+.3f}",
        f"Claim signals: {scan.claim_count}",
        f"Mechanism signals: {scan.mechanism_count}",
        f"Claim-to-mechanism ratio: {scan.claim_to_mechanism_ratio}",
        f"Modal pressure signals: {scan.modal_pressure_count}",
        f"Sovereignty / reversibility signals: {scan.sovereignty_count}",
        f"Fail-closed review: {'YES' if scan.fail_closed else 'NO'}",
        "",
        "Notes:",
    ]
    lines.extend(f"- {note}" for note in scan.notes)
    if scan.proximity_hits:
        lines.append("")
        lines.append("Contextual proximity hits:")
        for hit in scan.proximity_hits:
            lines.append(f"- {hit.category}: {hit.left!r} near {hit.right!r} ({hit.distance} tokens) — {hit.excerpt}")
    lines.append("")
    lines.append("Human review note: This scan is a relationship-aware mirror signal, not proof of intent, certification, or a final decision.")
    return "\n".join(lines)
