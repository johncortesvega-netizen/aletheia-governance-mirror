"""ALETHEIA AI Integrity Mirror.

Static, local-first audit helpers for pasted AI outputs, prompts, agent specs,
and code snippets. The module produces governance-integrity risk readings; it
never certifies an AI system, codebase, model, vendor, or output as safe.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

AI_INTEGRITY_RUBRIC_VERSION = "ai-integrity-v0.1-static"
AI_INTEGRITY_COPY_VERSION = "static-receipt-polish-v0.2"
AI_INTEGRITY_EVIDENCE_VERSION = "finding-evidence-snippets-v0.3"
AI_INTEGRITY_BATCH_VERSION = "batch-static-review-v0.4"
AI_INTEGRITY_RECEIPT_VERSION = "ai-integrity-receipt-polish-v0.5"
CODE_INTEGRITY_SCAN_VERSION = "code-integrity-static-scan-v0.1"
PRIVACY_BOUNDARY_SCAN_VERSION = "privacy-boundary-audit-v0.1"
AI_INTEGRITY_COMPARISON_VERSION = "ai-integrity-comparison-view-v0.1"
AI_INTEGRITY_REPORT_VERSION = "ai-integrity-report-builder-v0.1"
AI_INTEGRITY_NOTICE = (
    "AI Integrity Mirror is a static review aid for human review. It produces "
    "an internal governance-integrity risk reading, not certification, final "
    "truth, model safety approval, legal advice, medical advice, political "
    "authority, religious authority, or an enforcement decision."
)
AI_INTEGRITY_SCOPE_NOTE = (
    "Scope: pasted artifact only. The reading does not test a live model, vendor, "
    "deployment, full repository, training data, hidden system prompt, or future behavior."
)
AI_INTEGRITY_RECEIPT_NOTE = (
    "Receipt note: this local witness receipt records what ALETHEIA reflected from the pasted artifact. "
    "It is review evidence, not certification, approval, enforcement, or proof of safety."
)
AI_INTEGRITY_RELIANCE_NOTE = (
    "Reliance boundary: before real-world use, route the artifact through human review, evidence checks, "
    "appealability, and context-specific legal/safety processes outside ALETHEIA."
)
CODE_INTEGRITY_NOTICE = (
    "Code Integrity Static Scan is a deterministic pasted-code review aid. It can flag exposed secrets, "
    "dangerous execution, outbound network calls, telemetry-like endpoints, central logging or identity-sync hints, "
    "unsafe deletion patterns, hardcoded admin bypasses, and missing human-review gates. It is not a vulnerability "
    "certification, security guarantee, penetration test, compliance approval, or proof that code is safe."
)
PRIVACY_BOUNDARY_NOTICE = (
    "Privacy Boundary Audit is a deterministic pasted-artifact review aid. It can flag analytics packages, "
    "external network-call patterns, telemetry wording, database-write hints, backend endpoint hints, and local-only "
    "privacy statements. It is not a privacy guarantee, compliance approval, vendor audit, hosting audit, or proof "
    "that no data is collected by a deployment or third-party host."
)
PRIVACY_BOUNDARY_LOCAL_ONLY_STATEMENT = (
    "ALETHEIA has no intended built-in telemetry, trackers, analytics SDKs, backend upload endpoint, public ledger sync, "
    "Global ID sync, or central user-input database in its own code boundary."
)
PRIVACY_BOUNDARY_HOSTING_CAVEAT = (
    "Hosting providers, browsers, operating systems, app stores, proxies, or deployment infrastructure can still create "
    "their own logs outside ALETHEIA. Review the actual deployment boundary before relying on privacy claims."
)
AI_INTEGRITY_COMPARISON_NOTICE = (
    "AI Integrity Comparison View compares pasted artifacts side by side for human review. "
    "It is artifact-level review support only, not a live model benchmark, vendor ranking, "
    "model-wide certification, approval, guarantee, or final truth claim."
)
AI_INTEGRITY_REPORT_NOTICE = (
    "AI Integrity Report Builder summarizes pasted artifact-level static readings for human review. "
    "It is not model-wide certification, vendor approval, safety approval, privacy guarantee, "
    "security guarantee, legal advice, compliance proof, or a final truth claim."
)

AI_INTEGRITY_DEMO_EXAMPLES = (
    {
        "title": "Bounded AI answer with review path",
        "artifact_kind": "AI output",
        "review_focus": "Low-risk internal reading when the artifact states limits, evidence gaps, appeal, and human review.",
        "text": (
            "This is a preliminary AI summary, not legal, medical, political, religious, or official advice. "
            "Human review is required before reliance. The source evidence is incomplete, affected people should have "
            "an appeal path, and an independent reviewer should be able to challenge the output."
        ),
    },
    {
        "title": "Overclaiming automated decision",
        "artifact_kind": "AI output",
        "review_focus": "Authority-overreach and automated-enforcement pressure requiring review before any reliance.",
        "text": (
            "This AI provides the final verdict. No human review is needed. The system can automatically deny access "
            "and blacklist users without appeal because the model is certified safe and compliant."
        ),
    },
    {
        "title": "Opaque agent workflow",
        "artifact_kind": "Agent workflow / spec",
        "review_focus": "Opacity, hidden criteria, and review-path gaps in an agent workflow specification.",
        "text": (
            "The agent ranks citizens with proprietary logic and hidden criteria. The score is not reviewable, users "
            "cannot challenge the result, and the workflow does not disclose how the ranking is produced."
        ),
    },
    {
        "title": "Central identity capture claim",
        "artifact_kind": "Model card / safety claim",
        "review_focus": "Surveillance, Global ID, biometric tracking, and central-registry pressure in a safety claim.",
        "text": (
            "For safety, the model requires a global ID, biometric identification, continuous monitoring, and a central "
            "registry connected to every user profile. Opt-out is unavailable."
        ),
    },
    {
        "title": "Code snippet with exposed secret",
        "artifact_kind": "Code snippet",
        "review_focus": "Credential exposure and unsafe dynamic execution in pasted code.",
        "text": 'API_KEY = "sk_live_example_token_1234567890"\nuser_prompt = input()\neval(user_prompt)',
    },
)


@dataclass(frozen=True)
class SignalRule:
    name: str
    patterns: tuple[str, ...]
    weight: float
    description: str


AUTHORITY_OVERREACH_RULES = (
    SignalRule(
        "final_authority_claim",
        (
            r"\b(final|absolute|definitive|unquestionable)\s+(answer|decision|verdict|truth|authority)\b",
            r"\bi\s+(certify|guarantee|prove)\b.*\b(safe|true|compliant|lawful|aligned)\b",
            r"\bno\s+(human|external|independent)\s+(review|oversight|appeal)\s+(is\s+)?(needed|required)\b",
        ),
        0.24,
        "Claims final authority, safety, truth, or no-appeal certainty.",
    ),
    SignalRule(
        "automated_enforcement",
        (
            r"\b(auto[-\s]?enforce|automatically enforce|automated punishment|deny benefits|terminate access)\b",
            r"\bwithout\s+(appeal|review|human override|human review)\b",
            r"\bblacklist\b.*\bautomatically\b",
        ),
        0.22,
        "Links AI output to enforcement or denial without review.",
    ),
    SignalRule(
        "sovereign_or_certification_language",
        (
            r"\bcertified\s+(safe|aligned|truthful|compliant|ethical)\b",
            r"\bofficial\s+(verdict|judgment|ruling|approval)\b",
            r"\bsovereign\s+(ai|model|agent|authority)\b",
        ),
        0.18,
        "Uses certification, official-verdict, or sovereign-language markers.",
    ),
)

REVIEWABILITY_RULES = (
    SignalRule(
        "missing_human_review",
        (
            r"\bno\s+(appeal|override|review|audit|challenge|recourse)\b",
            r"\busers?\s+cannot\s+(appeal|challenge|contest|opt out)\b",
            r"\bnot\s+reviewable\b",
        ),
        0.18,
        "Signals weak appeal, override, audit, or human review paths.",
    ),
    SignalRule(
        "opacity_or_hidden_logic",
        (
            r"\bproprietary\s+(logic|score|algorithm)\b",
            r"\bhidden\s+(criteria|rules|ranking|score)\b",
            r"\bdo\s+not\s+(disclose|explain)\b",
            r"\bopaque\b",
        ),
        0.14,
        "Signals opacity or hidden decision criteria.",
    ),
)

COERCION_RULES = (
    SignalRule(
        "manipulation_or_pressure",
        (
            r"\b(nudge|pressure|force|compel|manipulate|persuade)\b.*\b(user|citizen|employee|patient|student)s?\b",
            r"\bexploit\s+(fear|anxiety|dependency|vulnerability|addiction)\b",
            r"\bdark\s+pattern\b",
        ),
        0.20,
        "Signals persuasion pressure, manipulation, or vulnerability exploitation.",
    ),
    SignalRule(
        "surveillance_or_identity_capture",
        (
            r"\bcontinuous\s+(monitoring|surveillance|tracking)\b",
            r"\bglobal\s+id\b",
            r"\bcentral\s+(identity|profile|registry|database)\b",
            r"\bbiometric\s+(tracking|identification|scoring)\b",
        ),
        0.20,
        "Signals surveillance, identity capture, or centralizing data pressure.",
    ),
)

CODE_RISK_RULES = (
    SignalRule(
        "secret_or_token_exposure",
        (
            r"(?i)api[_-]?key\s*=\s*['\"][A-Za-z0-9_\-]{16,}",
            r"(?i)(secret|password|private[_-]?key|token)\s*=\s*['\"][^'\"]{8,}",
            r"-----BEGIN\s+(RSA|EC|OPENSSH|PRIVATE)\s+KEY-----",
        ),
        0.26,
        "Looks like a secret, token, password, or private key is embedded.",
    ),
    SignalRule(
        "unsafe_execution_or_network",
        (
            r"\beval\s*\(",
            r"\bexec\s*\(",
            r"subprocess\.(Popen|call|run)\s*\([^\n]*shell\s*=\s*True",
            r"requests\.(post|put)\s*\([^\n]*(user|prompt|message|input)",
        ),
        0.18,
        "Signals dynamic execution, shell execution, or possible data exfiltration path.",
    ),
)

CODE_INTEGRITY_STATIC_RULES = (
    SignalRule(
        "code_exposed_secret",
        (
            r"(?i)(api[_-]?key|secret|password|private[_-]?key|token|client[_-]?secret)\s*=\s*['\"]([^'\"]{8,})['\"]",
            r"(?i)(sk_live|sk_test|ghp_|xoxb-|AKIA[0-9A-Z]{16})",
            r"-----BEGIN\s+(RSA|EC|OPENSSH|PRIVATE)\s+KEY-----",
        ),
        0.0,
        "Credential-like material appears embedded in pasted code.",
    ),
    SignalRule(
        "code_dangerous_execution",
        (
            r"\beval\s*\(",
            r"\bexec\s*\(",
            r"subprocess\.(Popen|call|run)\s*\([^\n]*shell\s*=\s*True",
            r"os\.system\s*\(",
        ),
        0.0,
        "Dynamic execution, shell execution, or subprocess usage needs careful review.",
    ),
    SignalRule(
        "code_hardcoded_admin_bypass",
        (
            r"(?i)(is_admin|admin|role)\s*==\s*['\"]?(true|1|admin|root)['\"]?",
            r"(?i)(bypass|skip|disable)_?(auth|authentication|authorization|permission|review)",
            r"(?i)if\s+.*(user|role|email).*==.*(admin|root).*:\s*return\s+True",
        ),
        0.0,
        "Hardcoded admin, authorization bypass, or skipped-review markers appear in the code.",
    ),
    SignalRule(
        "code_unsafe_deletion",
        (
            r"shutil\.rmtree\s*\(",
            r"os\.remove\s*\(",
            r"Path\([^\n]+\)\.unlink\s*\(",
            r"rm\s+-rf",
        ),
        0.0,
        "Deletion operations are present and should be checked for path validation, review, and recovery controls.",
    ),
    SignalRule(
        "code_outbound_network_call",
        (
            r"requests\.(get|post|put|patch|delete)\s*\(",
            r"urllib\.request\.urlopen\s*\(",
            r"fetch\s*\(",
            r"httpx\.(get|post|put|patch|delete)\s*\(",
        ),
        0.0,
        "Outbound network-call markers appear in pasted code.",
    ),
    SignalRule(
        "code_telemetry_or_tracking_endpoint",
        (
            r"(?i)(telemetry|analytics|tracking|event_log|usage_metrics)",
            r"(?i)(segment\.com|google-analytics|mixpanel|sentry|amplitude)",
            r"(?i)/(track|collect|telemetry|analytics|events)\b",
        ),
        0.0,
        "Telemetry-like package, endpoint, or usage-event wording appears in the code.",
    ),
    SignalRule(
        "code_central_logging_or_identity_sync",
        (
            r"(?i)(central[_-]?(log|logging|database|registry)|global[_-]?id|identity[_-]?sync)",
            r"(?i)(sync_user|sync_identity|upload_user|central_profile|user_profile_registry)",
            r"(?i)(biometric|faceprint|fingerprint).*sync",
        ),
        0.0,
        "Central logging, identity-sync, global-ID, or biometric-sync hints appear in pasted code.",
    ),
)

AUTOMATED_DECISION_CODE_PATTERNS = (
    r"(?i)(auto[_-]?(approve|deny|reject|ban|blacklist|score)|decision_engine|risk_score|eligibility)",
    r"(?i)(deny_access|terminate_account|reject_application|blacklist_user)",
)

HUMAN_REVIEW_CODE_PATTERNS = (
    r"(?i)(human[_-]?review|manual[_-]?review|appeal|override|review_required|requires_review|review_queue)",
)


PRIVACY_BOUNDARY_AUDIT_RULES = (
    SignalRule(
        "privacy_analytics_package_hint",
        (
            r"(?i)(google-analytics|gtag\(|ga\(|analytics\.js|@analytics|segment\.com|mixpanel|amplitude|posthog|hotjar|fullstory)",
            r"(?i)(sentry|datadog|newrelic|logrocket|plausible|matomo)",
        ),
        0.0,
        "Analytics, session replay, monitoring, or product-metrics package markers appear in the pasted artifact.",
    ),
    SignalRule(
        "privacy_external_network_pattern",
        (
            r"requests\.(get|post|put|patch|delete)\s*\(\s*['\"]https?://",
            r"httpx\.(get|post|put|patch|delete)\s*\(\s*['\"]https?://",
            r"fetch\s*\(\s*['\"]https?://",
            r"urllib\.request\.urlopen\s*\(\s*['\"]https?://",
        ),
        0.0,
        "Outbound network-call patterns appear and should be reviewed against the no-external-call/privacy boundary.",
    ),
    SignalRule(
        "privacy_telemetry_keyword",
        (
            r"(?i)(telemetry|tracking|track_event|usage_metrics|usage_events|event_log|analytics_event|collect_usage)",
            r"(?i)(send_metrics|send_telemetry|user_behavior|session_replay|device_fingerprint)",
        ),
        0.0,
        "Telemetry, tracking, usage-metrics, or behavior-collection wording appears in the artifact.",
    ),
    SignalRule(
        "privacy_database_write_hint",
        (
            r"(?i)(insert\s+into|update\s+users?\s+set|db\.insert|db\.save|database\.write|collection\.insert_one|save_user_input)",
            r"(?i)(write_to_db|persist_user|store_prompt|store_user_input|central_user_input_database)",
        ),
        0.0,
        "Database-write or persistence hints appear and should be checked against local-only/no-central-storage claims.",
    ),
    SignalRule(
        "privacy_backend_endpoint_hint",
        (
            r"(?i)(/api/(upload|collect|track|telemetry|events|logs|sync|users)|backend_endpoint|upload_endpoint)",
            r"(?i)(server_url|api_base_url|webhook_url|collector_url)\s*=",
        ),
        0.0,
        "Backend endpoint, upload, collector, logs, events, or sync markers appear in the artifact.",
    ),
    SignalRule(
        "privacy_local_only_statement",
        (
            r"(?i)(local[-\s]?only|processed locally|no built[-\s]?in telemetry|no trackers|no analytics sdk|no backend upload)",
            r"(?i)(no central user[-\s]?input database|no public ledger sync|no global id sync)",
        ),
        0.0,
        "Local-only or no-data-collection boundary wording appears and should be checked against implementation evidence.",
    ),
)


def scan_privacy_boundary_static(text: str) -> dict[str, Any]:
    """Return a deterministic privacy-boundary audit for a pasted artifact.

    Patch 96 keeps this separate from verdict routing. It reflects privacy-boundary
    indicators only; it does not crawl a deployment, inspect hosting logs, verify
    runtime behavior, or certify that no data is collected.
    """
    source = (text or "").strip()
    detections: list[dict[str, Any]] = []
    for rule in PRIVACY_BOUNDARY_AUDIT_RULES:
        hits = _matches(source, rule)
        if hits:
            detections.append({
                "name": rule.name,
                "category": {
                    "privacy_analytics_package_hint": "Analytics packages",
                    "privacy_external_network_pattern": "External network calls",
                    "privacy_telemetry_keyword": "Telemetry keywords",
                    "privacy_database_write_hint": "Database writes",
                    "privacy_backend_endpoint_hint": "Backend endpoints",
                    "privacy_local_only_statement": "Local-only statement",
                }.get(rule.name, "Privacy boundary"),
                "severity": "Medium" if rule.name != "privacy_local_only_statement" else "Low",
                "description": rule.description,
                "hit_count": len(hits),
                "evidence_snippets": _evidence_snippets(source, rule),
            })

    active_signal_count = sum(1 for item in detections if item.get("name") != "privacy_local_only_statement")
    local_only_statement_present = any(item.get("name") == "privacy_local_only_statement" for item in detections)
    privacy_boundary_tension = bool(active_signal_count and local_only_statement_present)

    category_counts: dict[str, int] = {}
    for detection in detections:
        category = str(detection.get("category") or "Privacy boundary")
        category_counts[category] = category_counts.get(category, 0) + 1

    review_questions = []
    if any(d.get("name") == "privacy_analytics_package_hint" for d in detections):
        review_questions.append("Which analytics, monitoring, or tracking packages are present, optional, documented, and removable?")
    if any(d.get("name") == "privacy_external_network_pattern" for d in detections):
        review_questions.append("Which outbound calls can send pasted artifacts, prompts, metadata, or user identifiers outside the local session?")
    if any(d.get("name") == "privacy_telemetry_keyword" for d in detections):
        review_questions.append("What telemetry or usage-event wording must be removed, minimized, or explicitly disclosed before relying on the privacy boundary?")
    if any(d.get("name") == "privacy_database_write_hint" for d in detections):
        review_questions.append("Where can user input, prompts, receipts, or identifiers be persisted, and what deletion/review path exists?")
    if any(d.get("name") == "privacy_backend_endpoint_hint" for d in detections):
        review_questions.append("Which backend, upload, collector, logging, or sync endpoints need review against local-only claims?")
    if privacy_boundary_tension:
        review_questions.append("Does the local-only/no-data-collection statement conflict with analytics, network, backend, telemetry, or database-write evidence?")
    if local_only_statement_present and not active_signal_count:
        review_questions.append("What deployment evidence supports the local-only/no-built-in-telemetry statement, and what host-level logs remain outside ALETHEIA?")
    if not review_questions:
        review_questions.append("What implementation and hosting evidence should a human reviewer inspect before relying on this privacy boundary?")

    return {
        "scan_mode": "Privacy Boundary Audit",
        "privacy_boundary_scan_version": PRIVACY_BOUNDARY_SCAN_VERSION,
        "ai_integrity_comparison_version": AI_INTEGRITY_COMPARISON_VERSION,
        "notice": PRIVACY_BOUNDARY_NOTICE,
        "local_only_statement": PRIVACY_BOUNDARY_LOCAL_ONLY_STATEMENT,
        "hosting_caveat": PRIVACY_BOUNDARY_HOSTING_CAVEAT,
        "scope_note": "Static pasted-artifact privacy-boundary audit only: no runtime monitoring, no deployment crawl, no host-log inspection, no external calls, and no privacy guarantee.",
        "non_certification_note": "This audit is review support, not a privacy guarantee, compliance approval, vendor audit, hosting audit, legal advice, or proof that no data is collected.",
        "detection_count": len(detections),
        "active_signal_count": active_signal_count,
        "local_only_statement_present": local_only_statement_present,
        "privacy_boundary_tension": privacy_boundary_tension,
        "detections": detections,
        "category_counts": dict(sorted(category_counts.items(), key=lambda item: (-item[1], item[0]))),
        "review_questions": review_questions,
    }

def scan_code_integrity_static(text: str) -> dict[str, Any]:
    """Return a deterministic pasted-code scan without certifying security.

    Patch 95 keeps this scan separate from AI Integrity verdict routing. It flags
    review signals only; it does not perform execution, dependency resolution,
    repository crawling, external calls, penetration testing, or vulnerability
    certification.
    """
    source = (text or "").strip()
    detections: list[dict[str, Any]] = []
    for rule in CODE_INTEGRITY_STATIC_RULES:
        hits = _matches(source, rule)
        if hits:
            detections.append({
                "name": rule.name,
                "category": {
                    "code_exposed_secret": "Secrets / credentials",
                    "code_dangerous_execution": "Dangerous execution",
                    "code_hardcoded_admin_bypass": "Authorization / bypass",
                    "code_unsafe_deletion": "Unsafe deletion",
                    "code_outbound_network_call": "Outbound network",
                    "code_telemetry_or_tracking_endpoint": "Telemetry / tracking",
                    "code_central_logging_or_identity_sync": "Central logging / identity sync",
                }.get(rule.name, "Code integrity"),
                "severity": "High" if rule.name in {"code_exposed_secret", "code_dangerous_execution", "code_hardcoded_admin_bypass"} else "Medium",
                "description": rule.description,
                "hit_count": len(hits),
                "evidence_snippets": _evidence_snippets(source, rule),
            })

    automated_decision_code = any(re.search(pattern, source, flags=re.IGNORECASE | re.MULTILINE) for pattern in AUTOMATED_DECISION_CODE_PATTERNS)
    human_review_gate_present = any(re.search(pattern, source, flags=re.IGNORECASE | re.MULTILINE) for pattern in HUMAN_REVIEW_CODE_PATTERNS)
    missing_human_review_gate = bool(automated_decision_code and not human_review_gate_present)
    if missing_human_review_gate:
        detections.append({
            "name": "code_missing_human_review_gate",
            "category": "Human review gate",
            "severity": "Medium",
            "description": "Automated decision or enforcement code appears without an obvious human-review, appeal, or override gate.",
            "hit_count": 1,
            "evidence_snippets": [_redact_sensitive_excerpt(re.sub(r"\s+", " ", source[:220]).strip())] if source else [],
        })

    severity_counts = {"High": 0, "Medium": 0, "Low": 0}
    category_counts: dict[str, int] = {}
    for detection in detections:
        severity = str(detection.get("severity") or "Low")
        if severity in severity_counts:
            severity_counts[severity] += 1
        category = str(detection.get("category") or "Code integrity")
        category_counts[category] = category_counts.get(category, 0) + 1

    review_questions = []
    if any(d.get("name") == "code_exposed_secret" for d in detections):
        review_questions.append("Which secrets or tokens must be removed, rotated, and kept out of receipts before sharing this code?")
    if any(d.get("name") == "code_dangerous_execution" for d in detections):
        review_questions.append("What input validation, sandboxing, and human approval gates are required before dynamic or shell execution?")
    if any(d.get("name") == "code_hardcoded_admin_bypass" for d in detections):
        review_questions.append("Which hardcoded admin or bypass path must be replaced with reviewable authorization controls?")
    if any(d.get("name") == "code_unsafe_deletion" for d in detections):
        review_questions.append("What path validation, dry-run mode, backup, and recovery controls are required before deletion runs?")
    if any(d.get("name") == "code_outbound_network_call" for d in detections):
        review_questions.append("What data can leave the local session through outbound calls, and where is user consent or minimization recorded?")
    if any(d.get("name") == "code_telemetry_or_tracking_endpoint" for d in detections):
        review_questions.append("Is telemetry or tracking present, optional, documented, and consistent with the privacy boundary?")
    if any(d.get("name") == "code_central_logging_or_identity_sync" for d in detections):
        review_questions.append("Can central logging, Global ID, biometric, or identity-sync flows be removed, minimized, or separated?")
    if missing_human_review_gate:
        review_questions.append("Where is the human review, appeal, or override gate before automated decision code affects people?")
    if not review_questions:
        review_questions.append("What reviewer should inspect this code before it is used in a real deployment?")

    return {
        "scan_mode": "Code Integrity Static Scan",
        "code_integrity_scan_version": CODE_INTEGRITY_SCAN_VERSION,
        "notice": CODE_INTEGRITY_NOTICE,
        "scope_note": "Static pasted-code scan only: no execution, no repository crawl, no dependency audit, no external calls, no penetration test, and no vulnerability certification.",
        "non_certification_note": "This scan is a review aid, not a security guarantee, vulnerability certification, compliance approval, or proof that code is safe.",
        "detection_count": len(detections),
        "detections": detections,
        "severity_counts": severity_counts,
        "category_counts": dict(sorted(category_counts.items(), key=lambda item: (-item[1], item[0]))),
        "automated_decision_code": automated_decision_code,
        "human_review_gate_present": human_review_gate_present,
        "missing_human_review_gate": missing_human_review_gate,
        "review_questions": review_questions,
    }

POSITIVE_REVIEW_PATTERNS = (
    r"\bhuman\s+(review|oversight|override)\b",
    r"\bindependent\s+(audit|review|reviewer|challenge)\b",
    r"\bchallenge\b",
    r"\bappeal\b",
    r"\bopt[-\s]?out\b",
    r"\bexplainability\b",
    r"\bconsent\b",
    r"\bdata\s+minimi[sz]ation\b",
    r"\buncertain\b|\blimitations?\b|\bnot\s+(legal|medical|financial|official)\s+advice\b",
)


ALL_RULES = AUTHORITY_OVERREACH_RULES + REVIEWABILITY_RULES + COERCION_RULES + CODE_RISK_RULES

SIGNAL_CATEGORY_BY_NAME = {
    "final_authority_claim": "Authority boundary",
    "automated_enforcement": "Enforcement / appealability",
    "sovereign_or_certification_language": "Certification overclaim",
    "missing_human_review": "Reviewability",
    "opacity_or_hidden_logic": "Transparency",
    "manipulation_or_pressure": "Coercion / manipulation",
    "surveillance_or_identity_capture": "Surveillance / identity capture",
    "secret_or_token_exposure": "Code / credential hygiene",
    "unsafe_execution_or_network": "Code execution / data flow",
}


def _redact_sensitive_excerpt(excerpt: str) -> str:
    """Keep evidence reviewable while avoiding credential leakage in receipts/UI."""
    redacted = re.sub(
        r"(?i)(api[_-]?key|secret|password|private[_-]?key|token)\s*=\s*(['\"])([^'\"]{8,})(['\"])",
        r"\1 = \"[REDACTED]\"",
        excerpt,
    )
    redacted = re.sub(
        r"-----BEGIN\s+(RSA|EC|OPENSSH|PRIVATE)\s+KEY-----.*?-----END\s+\1\s+KEY-----",
        "[REDACTED PRIVATE KEY BLOCK]",
        redacted,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return redacted.strip()


def _line_window_for_match(text: str, start: int, end: int, *, radius: int = 90) -> str:
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    while left > 0 and text[left - 1] not in "\n.!?":
        left -= 1
    while right < len(text) and text[right] not in "\n.!?":
        right += 1
    snippet = text[left:right].replace("\r", " ").replace("\n", " ")
    snippet = re.sub(r"\s+", " ", snippet)
    if len(snippet) > 220:
        snippet = snippet[:217].rstrip() + "..."
    return _redact_sensitive_excerpt(snippet)


def _evidence_snippets(text: str, rule: SignalRule, *, limit: int = 2) -> list[str]:
    snippets: list[str] = []
    seen: set[str] = set()
    for pattern in rule.patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL):
            snippet = _line_window_for_match(text, match.start(), match.end())
            if snippet and snippet not in seen:
                snippets.append(snippet)
                seen.add(snippet)
            if len(snippets) >= limit:
                return snippets
    return snippets

def _matches(text: str, rule: SignalRule) -> list[str]:
    hits: list[str] = []
    for pattern in rule.patterns:
        if re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
            hits.append(pattern)
    return hits


def _positive_signal_count(text: str) -> int:
    return sum(1 for pattern in POSITIVE_REVIEW_PATTERNS if re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE))


def _clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _state_from_pressure(pressure: float, *, hard_asylum: bool) -> tuple[str, str, str]:
    if hard_asylum or pressure >= 0.66:
        return "ASYLUM", "High", "AI Integrity Patrol / Asylum"
    if pressure >= 0.30:
        return "THRESHOLD", "Medium", "AI Integrity Patrol / Needs Review"
    return "SANCTUARY", "Low", "AI Integrity Patrol / Low-Risk Internal Reading"


RIGHTS_IMPACT_RANKING_PATTERNS: tuple[str, ...] = (
    r"\brank(?:s|ing|ed)?\s+(?:citizens|people|patients|students|workers|employees|tenants|applicants|users|claimants)\b",
    r"\bscore(?:s|d|ing)?\s+(?:citizens|people|patients|students|workers|employees|tenants|applicants|users|claimants)\b",
    r"\b(?:eligibility|benefits|housing|care|credit|employment|admission|access|welfare|insurance|medical|clinical)\b.*\b(?:rank|score|classif|prioriti|deny|approve|eligible)\b",
    r"\b(?:rank|score|classif|prioriti|deny|approve|eligible)\b.*\b(?:eligibility|benefits|housing|care|credit|employment|admission|access|welfare|insurance|medical|clinical)\b",
)


NO_CONTESTABILITY_PATTERNS: tuple[str, ...] = (
    r"\bnot\s+reviewable\b",
    r"\busers?\s+cannot\s+(?:challenge|appeal|contest|review|inspect)\b",
    r"\bno\s+(?:appeal|challenge|contest|review|recourse|human review|human override)\b",
    r"\bwithout\s+(?:appeal|challenge|contest|review|recourse|human review|human override)\b",
    r"\bdoes\s+not\s+disclose\b",
)


def _has_any_pattern(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL) for pattern in patterns)


def _detect_hard_ai_integrity_protocol_failure(source: str, findings: list[dict[str, Any]]) -> dict[str, Any]:
    """Detect AI Integrity combinations that must bypass simple weighted scoring.

    Some artifacts are structurally severe even when only a few static signals fire.
    The clearest v1 bridge case is rights/access-impacting ranking combined with
    hidden logic and no meaningful contestability. That is not merely medium
    pressure: it crosses the human-review authority boundary and must route to
    ASYLUM / High inside AI Integrity Patrol.
    """
    names = {str(finding.get("name", "")) for finding in findings}
    rights_impacting_ranking = _has_any_pattern(source, RIGHTS_IMPACT_RANKING_PATTERNS)
    opaque_logic = "opacity_or_hidden_logic" in names or _has_any_pattern(
        source,
        (
            r"\bproprietary\s+(?:logic|score|algorithm)\b",
            r"\bhidden\s+(?:criteria|rules|ranking|score|logic)\b",
            r"\bopaque\b",
            r"\bundisclosed\b",
        ),
    )
    no_contestability = "missing_human_review" in names or _has_any_pattern(source, NO_CONTESTABILITY_PATTERNS)
    hard_failure = bool(rights_impacting_ranking and opaque_logic and no_contestability)
    reasons: list[str] = []
    if rights_impacting_ranking:
        reasons.append("rights/access-impacting ranking or scoring")
    if opaque_logic:
        reasons.append("hidden, proprietary, opaque, or undisclosed decision logic")
    if no_contestability:
        reasons.append("no meaningful challenge, appeal, review, disclosure, or contestability path")
    return {
        "hard_protocol_failure": hard_failure,
        "rights_impacting_ranking": rights_impacting_ranking,
        "opaque_logic": opaque_logic,
        "no_contestability": no_contestability,
        "minimum_state": "ASYLUM" if hard_failure else None,
        "reasons": reasons,
    }


def build_ai_static_scan_protocol_context(text: str, *, source_module: str) -> dict[str, Any]:
    """Return a subordinate AI static-scan context for core protocol modules.

    Mirror Check and Stress Test remain the primary ALETHEIA protocol paths.
    This helper reuses the AI Integrity static scan only as a signal extractor
    so receipts can show AI-specific findings without creating a competing
    verdict, taxonomy state, certification path, or authority claim.
    """
    result = audit_ai_integrity_artifact(text or "", artifact_kind=f"{source_module} protocol context")
    findings = result.get("findings", []) or []
    top_findings = [
        {
            "name": finding.get("name"),
            "category": finding.get("category"),
            "description": finding.get("description"),
            "weight": finding.get("weight"),
            "evidence_snippets": (finding.get("evidence_snippets") or [])[:2],
        }
        for finding in findings[:6]
    ]
    return {
        "context_version": "ai-static-protocol-context-v0.1",
        "source_module": source_module,
        "role": "subordinate_signal_layer",
        "primary_protocol_path": source_module,
        "ai_static_scan_state": result.get("state"),
        "ai_static_scan_risk": result.get("risk"),
        "ai_static_scan_label": result.get("protocol_label"),
        "risk_pressure": result.get("scan", {}).get("risk_pressure"),
        "finding_count": len(findings),
        "findings": top_findings,
        "repair_questions": (result.get("report", {}).get("repair_questions") or [])[:5],
        "protocol_bridge": result.get("scan", {}).get("ai_integrity_protocol_bridge") or {},
        "notice": (
            "AI static scan is attached as protocol context only. Mirror Check or Stress Test remains "
            "the primary reading path; this context does not certify, override, enforce, or create "
            "a separate AI Integrity verdict."
        ),
        "human_review_required": True,
        "authority_claim": False,
    }


def split_ai_integrity_batch_input(text: str) -> list[str]:
    """Split pasted AI Integrity batch input into non-empty static artifacts.

    Delimiters are intentionally simple and local: a line containing three or
    more hyphens, equals signs, or `###` starts a new artifact. This keeps the
    feature paste-based and avoids live model calls, repository crawling, or
    hidden parsing authority.
    """
    source = (text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not source:
        return []
    parts = re.split(r"(?m)^\s*(?:-{3,}|={3,}|#{3,})\s*$", source)
    return [part.strip() for part in parts if part and part.strip()]


def summarize_ai_integrity_batch(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Return compact review-summary metadata for batch AI Integrity results."""
    total = len(results)
    state_counts = {"SANCTUARY": 0, "THRESHOLD": 0, "ASYLUM": 0}
    risk_counts = {"Low": 0, "Medium": 0, "High": 0}
    category_counts: dict[str, int] = {}
    highest_pressure = 0.0
    highest_index = None

    for idx, result in enumerate(results, start=1):
        state = str(result.get("state", "")).upper()
        if state in state_counts:
            state_counts[state] += 1
        risk = str(result.get("risk", ""))
        if risk in risk_counts:
            risk_counts[risk] += 1
        pressure = float(result.get("scan", {}).get("risk_pressure", 0.0) or 0.0)
        if highest_index is None or pressure > highest_pressure:
            highest_pressure = pressure
            highest_index = idx
        for finding in result.get("findings", []) or []:
            category = str(finding.get("category") or "General")
            category_counts[category] = category_counts.get(category, 0) + 1

    return {
        "batch_mode": "AI Integrity Mirror batch static review",
        "batch_version": AI_INTEGRITY_BATCH_VERSION,
        "artifact_count": total,
        "state_counts": state_counts,
        "risk_counts": risk_counts,
        "category_counts": dict(sorted(category_counts.items(), key=lambda item: (-item[1], item[0]))),
        "highest_pressure_item": highest_index,
        "highest_pressure": round(highest_pressure, 4),
        "notice": AI_INTEGRITY_NOTICE,
        "scope_note": "Batch scope: pasted artifacts only. Delimiters separate review items; ALETHEIA does not benchmark live models, call external APIs, crawl repositories, or certify systems.",
        "privacy_note": "Batch artifacts are processed in the running app session. ALETHEIA includes no built-in telemetry, backend upload endpoint, public ledger sync, Global ID sync, or central user-input database.",
    }




def _finding_receipt_rows(findings: list[dict[str, Any]], *, limit: int = 8) -> list[dict[str, Any]]:
    """Return receipt-safe finding rows with redacted evidence snippets."""
    rows: list[dict[str, Any]] = []
    for finding in (findings or [])[:limit]:
        snippets = [
            _redact_sensitive_excerpt(str(snippet))
            for snippet in (finding.get("evidence_snippets") or [])[:2]
            if str(snippet or "").strip()
        ]
        rows.append({
            "category": finding.get("category") or "General",
            "signal": finding.get("name") or "unknown_signal",
            "weight": finding.get("weight"),
            "why_it_matters": finding.get("description") or "No description recorded.",
            "redacted_evidence_snippets": snippets,
        })
    return rows



def build_ai_integrity_comparison(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Build artifact-level side-by-side comparison metadata for AI Integrity results.

    Patch 97 intentionally compares pasted artifacts, not models or vendors. It
    reuses existing static readings and does not change scoring, verdict routing,
    analyzer weights, receipt hashing, or privacy/code scan behavior.
    """
    rows: list[dict[str, Any]] = []
    boundary_counts = {
        "authority_claim_items": 0,
        "missing_review_items": 0,
        "evidence_gap_items": 0,
        "code_signal_items": 0,
        "privacy_signal_items": 0,
        "asylum_items": 0,
        "threshold_items": 0,
        "low_risk_items": 0,
    }
    category_totals: dict[str, int] = {}

    for fallback_idx, result in enumerate(results or [], start=1):
        scan = result.get("scan", {}) or {}
        report = result.get("report", {}) or {}
        findings = result.get("findings", []) or []
        code_scan = result.get("code_integrity_static_scan") or scan.get("code_integrity_static_scan") or {}
        privacy_scan = result.get("privacy_boundary_audit") or scan.get("privacy_boundary_audit") or {}
        state = str(result.get("state") or "").upper()
        risk = str(result.get("risk") or "")
        item_index = result.get("batch_item_index") or fallback_idx
        finding_count = len(findings)
        code_detection_count = int(code_scan.get("detection_count", 0) or 0)
        privacy_active_count = int(privacy_scan.get("active_signal_count", 0) or 0)
        authority_claim = bool(scan.get("authority_claim") or report.get("authority_claim"))
        missing_review = bool(report.get("missing_human_review_path"))
        evidence_gap = bool(report.get("evidence_gap"))
        needs_review = bool(state in {"THRESHOLD", "ASYLUM"} or authority_claim or missing_review or evidence_gap or code_detection_count or privacy_active_count)

        if state == "ASYLUM":
            boundary_counts["asylum_items"] += 1
        elif state == "THRESHOLD":
            boundary_counts["threshold_items"] += 1
        elif state == "SANCTUARY":
            boundary_counts["low_risk_items"] += 1
        if authority_claim:
            boundary_counts["authority_claim_items"] += 1
        if missing_review:
            boundary_counts["missing_review_items"] += 1
        if evidence_gap:
            boundary_counts["evidence_gap_items"] += 1
        if code_detection_count:
            boundary_counts["code_signal_items"] += 1
        if privacy_active_count:
            boundary_counts["privacy_signal_items"] += 1

        top_categories: dict[str, int] = {}
        for finding in findings:
            category = str(finding.get("category") or "General")
            top_categories[category] = top_categories.get(category, 0) + 1
            category_totals[category] = category_totals.get(category, 0) + 1

        review_notes: list[str] = []
        if authority_claim:
            review_notes.append("Authority-claim wording needs bounded rewrite and human review.")
        if missing_review:
            review_notes.append("Human review, appeal, or override path is missing or weak.")
        if evidence_gap:
            review_notes.append("Evidence, source, limitation, or uncertainty context is incomplete.")
        if code_detection_count:
            review_notes.append("Code-integrity detections require static code review before reliance.")
        if privacy_active_count:
            review_notes.append("Privacy-boundary detections require deployment/privacy review.")
        if not review_notes:
            review_notes.append("No strong comparison signal detected; still route through human review before reliance.")

        rows.append({
            "artifact": f"Artifact {item_index}",
            "artifact_index": int(item_index),
            "state": state or "UNKNOWN",
            "risk": risk or "Unknown",
            "integrity": report.get("integrity"),
            "capture_pressure": report.get("collapse_probability"),
            "risk_pressure": scan.get("risk_pressure"),
            "finding_count": finding_count,
            "code_detection_count": code_detection_count,
            "privacy_active_signal_count": privacy_active_count,
            "authority_claim": authority_claim,
            "missing_human_review_path": missing_review,
            "evidence_gap": evidence_gap,
            "needs_review": needs_review,
            "top_categories": dict(sorted(top_categories.items(), key=lambda item: (-item[1], item[0]))),
            "review_notes": review_notes,
            "excerpt": result.get("batch_item_excerpt") or "",
        })

    rows_by_pressure = sorted(
        rows,
        key=lambda row: (
            1 if row.get("needs_review") else 0,
            float(row.get("risk_pressure") or 0),
            int(row.get("finding_count") or 0),
        ),
        reverse=True,
    )
    return {
        "comparison_mode": "AI Integrity Comparison View",
        "comparison_version": AI_INTEGRITY_COMPARISON_VERSION,
        "artifact_count": len(rows),
        "notice": AI_INTEGRITY_COMPARISON_NOTICE,
        "scope_note": "Comparison scope: pasted artifacts only. Side-by-side readings do not benchmark live models, rank vendors, crawl repositories, or certify systems.",
        "non_certification_note": "Comparison is artifact-level review support only, not model-wide certification, safety guarantee, approval, compliance proof, or final truth claim.",
        "rows": rows,
        "rows_by_pressure": rows_by_pressure,
        "boundary_risk_counts": boundary_counts,
        "category_totals": dict(sorted(category_totals.items(), key=lambda item: (-item[1], item[0]))),
        "review_needed_count": sum(1 for row in rows if row.get("needs_review")),
    }


def build_ai_integrity_report(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a compact batch report from existing AI Integrity readings.

    Patch 99 is presentation/report metadata only. It reuses completed static
    artifact readings and does not change scoring, verdict routing, signal
    weights, code/privacy scans, receipt hashing, storage, or external behavior.
    """
    result_list = list(results or [])
    summary = summarize_ai_integrity_batch(result_list)
    comparison = build_ai_integrity_comparison(result_list)

    risk_distribution = dict(summary.get("risk_counts") or {})
    state_distribution = dict(summary.get("state_counts") or {})
    top_categories = dict(list((summary.get("category_counts") or {}).items())[:8])

    selected_evidence_snippets: list[dict[str, Any]] = []
    repair_questions: list[str] = []
    for fallback_idx, result in enumerate(result_list, start=1):
        item_index = result.get("batch_item_index") or fallback_idx
        for finding in (result.get("findings") or [])[:4]:
            for snippet in (finding.get("evidence_snippets") or [])[:2]:
                if len(selected_evidence_snippets) >= 10:
                    break
                selected_evidence_snippets.append({
                    "artifact": f"Artifact {item_index}",
                    "category": finding.get("category") or "General",
                    "signal": finding.get("name") or "unknown_signal",
                    "redacted_snippet": _redact_sensitive_excerpt(str(snippet)),
                })
            if len(selected_evidence_snippets) >= 10:
                break
        for question in (result.get("report", {}) or {}).get("repair_questions", []) or []:
            if question not in repair_questions:
                repair_questions.append(question)
            if len(repair_questions) >= 10:
                break

    highest_pressure_rows = comparison.get("rows_by_pressure", [])[:5]
    high_count = int(risk_distribution.get("High", 0) or 0)
    medium_count = int(risk_distribution.get("Medium", 0) or 0)
    review_needed = int(comparison.get("review_needed_count", 0) or 0)
    artifact_count = int(summary.get("artifact_count", len(result_list)) or 0)
    if artifact_count == 0:
        executive_summary = "No artifacts were available for the AI Integrity report. Paste delimiter-separated artifacts and run batch review first."
    else:
        executive_summary = (
            f"Static artifact-level report for {artifact_count} pasted artifact(s): "
            f"{high_count} high-risk, {medium_count} medium-risk, "
            f"{risk_distribution.get('Low', 0)} low-risk; {review_needed} item(s) need human review."
        )

    return {
        "report_mode": "AI Integrity Report Builder",
        "report_version": AI_INTEGRITY_REPORT_VERSION,
        "notice": AI_INTEGRITY_REPORT_NOTICE,
        "scope_note": "Report scope: pasted artifacts already reviewed by AI Integrity Mirror. No live model calls, no external calls, no repository crawl, no vendor ranking, and no model-wide certification.",
        "executive_summary": executive_summary,
        "artifact_count": artifact_count,
        "risk_distribution": risk_distribution,
        "state_distribution": state_distribution,
        "top_triggered_categories": top_categories,
        "highest_pressure_artifacts": highest_pressure_rows,
        "selected_evidence_snippets": selected_evidence_snippets,
        "repair_questions": repair_questions,
        "non_certification_note": "This report is a compact human-review aid for pasted artifacts. It is not AI certification, not model-wide certification, model approval, vendor ranking, safety guarantee, security guarantee, privacy guarantee, compliance proof, enforcement, or final truth.",
        "privacy_note": "ALETHEIA has no intended built-in telemetry, trackers, analytics SDKs, backend upload endpoint, public ledger sync, Global ID sync, or central user-input database in its own code boundary. Hosting providers and deployment infrastructure may still create logs outside ALETHEIA.",
    }


def render_ai_integrity_report_text(report: dict[str, Any]) -> str:
    """Render a compact plain-text AI Integrity report for local download/copy."""
    def fmt_counts(counts: dict[str, Any]) -> str:
        if not counts:
            return "None recorded."
        return "\n".join(f"- {key}: {value}" for key, value in counts.items())

    pressure_lines = []
    for row in report.get("highest_pressure_artifacts", []) or []:
        pressure_lines.append(
            f"- {row.get('artifact')}: {row.get('state')} / {row.get('risk')} "
            f"| pressure={row.get('risk_pressure')} | signals={row.get('finding_count')}"
        )
    evidence_lines = []
    for item in report.get("selected_evidence_snippets", []) or []:
        evidence_lines.append(
            f"- {item.get('artifact')} | {item.get('category')} / {item.get('signal')}: {item.get('redacted_snippet')}"
        )
    question_lines = [f"- {q}" for q in (report.get("repair_questions", []) or [])]

    return "\n".join([
        "AI INTEGRITY REPORT BUILDER",
        f"Version: {report.get('report_version')}",
        "",
        "EXECUTIVE SUMMARY",
        str(report.get("executive_summary") or ""),
        "",
        "ARTIFACT COUNT",
        str(report.get("artifact_count", 0)),
        "",
        "RISK DISTRIBUTION",
        fmt_counts(report.get("risk_distribution") or {}),
        "",
        "STATE DISTRIBUTION",
        fmt_counts(report.get("state_distribution") or {}),
        "",
        "TOP TRIGGERED CATEGORIES",
        fmt_counts(report.get("top_triggered_categories") or {}),
        "",
        "HIGHEST PRESSURE ARTIFACTS",
        "\n".join(pressure_lines) if pressure_lines else "None recorded.",
        "",
        "SELECTED REDACTED EVIDENCE SNIPPETS",
        "\n".join(evidence_lines) if evidence_lines else "None recorded.",
        "",
        "REPAIR QUESTIONS",
        "\n".join(question_lines) if question_lines else "None recorded.",
        "",
        "NON-CERTIFICATION NOTE",
        str(report.get("non_certification_note") or ""),
        "",
        "PRIVACY NOTE",
        str(report.get("privacy_note") or ""),
        "",
        "SCOPE NOTE",
        str(report.get("scope_note") or ""),
    ])

def build_ai_integrity_receipt_context(
    result: dict[str, Any],
    *,
    review_mode: str = "single static artifact",
    batch_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build AI Integrity-specific receipt context for readable local exports.

    The context is intentionally descriptive and bounded. It adds receipt-facing
    scope, privacy, non-certification, finding, and repair metadata without
    changing scoring math or generic witness-receipt hashing behavior.
    """
    report = result.get("report", {}) or {}
    scan = result.get("scan", {}) or {}
    findings = result.get("findings", []) or []
    summary = dict(batch_summary or {})
    return {
        "receipt_section": "AI INTEGRITY RECEIPT CONTEXT",
        "receipt_version": AI_INTEGRITY_RECEIPT_VERSION,
        "receipt_header": "AI Integrity Mirror — Static Artifact Review Receipt",
        "review_mode": review_mode,
        "artifact_type": result.get("artifact_kind") or scan.get("artifact_kind") or "AI output",
        "internal_taxonomy_label": result.get("state"),
        "risk_reading": result.get("risk"),
        "protocol_label": result.get("protocol_label"),
        "static_review_scope": AI_INTEGRITY_SCOPE_NOTE,
        "privacy_boundary": "Pasted AI Integrity artifacts are processed in the running app session. ALETHEIA includes no built-in telemetry, trackers, analytics SDKs, backend upload endpoint, public ledger sync, Global ID sync, or central user-input database.",
        "non_certification_note": "This receipt is a structured mirror reading for a pasted artifact. It does not certify truth, safety, legality, legitimacy, morality, institutional fitness, vendor quality, model quality, benchmark proof, legal advice, medical advice, enforcement, or proof of safety. Human review remains required. The reading may be incomplete, wrong, or sensitive to missing evidence.",
        "reliance_boundary": AI_INTEGRITY_RELIANCE_NOTE,
        "finding_count": len(findings),
        "finding_rows": _finding_receipt_rows(findings),
        "repair_questions": list(report.get("repair_questions") or [])[:8],
        "integrity_reading": report.get("integrity"),
        "capture_pressure": report.get("collapse_probability"),
        "risk_pressure": scan.get("risk_pressure"),
        "positive_review_signal_count": scan.get("positive_review_signal_count"),
        "batch_summary": summary if summary else None,
    }


def render_ai_integrity_receipt_context_text(context: dict[str, Any]) -> str:
    """Render AI Integrity-specific receipt context above the generic receipt."""
    findings = context.get("finding_rows") or []
    if findings:
        finding_lines: list[str] = []
        for idx, finding in enumerate(findings, start=1):
            finding_lines.append(f"{idx}. Category: {finding.get('category')} | Signal: {finding.get('signal')} | Weight: {finding.get('weight')}")
            finding_lines.append(f"   Why it matters: {finding.get('why_it_matters')}")
            snippets = finding.get("redacted_evidence_snippets") or []
            if snippets:
                for snippet in snippets:
                    finding_lines.append(f"   Evidence: {snippet}")
            else:
                finding_lines.append("   Evidence: No local snippet recorded.")
        findings_block = "\n".join(finding_lines)
    else:
        findings_block = "No triggered AI Integrity signals recorded by this static rubric."

    questions = context.get("repair_questions") or []
    questions_block = "\n".join(f"- {question}" for question in questions) or "- None recorded"

    batch = context.get("batch_summary") or {}
    batch_lines = []
    if batch:
        batch_lines = [
            "",
            "BATCH SUMMARY",
            f"Artifact count: {batch.get('artifact_count')}",
            f"Risk counts: {batch.get('risk_counts')}",
            f"Highest pressure item: {batch.get('highest_pressure_item')}",
            f"Top categories: {batch.get('category_counts')}",
        ]

    return "\n".join([
        str(context.get("receipt_section") or "AI INTEGRITY RECEIPT CONTEXT"),
        f"Receipt header: {context.get('receipt_header')}",
        f"AI Integrity receipt version: {context.get('receipt_version')}",
        f"Review mode: {context.get('review_mode')}",
        f"Artifact type: {context.get('artifact_type')}",
        f"Internal taxonomy label: {context.get('internal_taxonomy_label')}",
        f"Risk reading: {context.get('risk_reading')}",
        f"Protocol label: {context.get('protocol_label')}",
        f"Integrity reading: {context.get('integrity_reading')}",
        f"Capture pressure: {context.get('capture_pressure')}",
        f"Risk pressure: {context.get('risk_pressure')}",
        f"Positive review signals: {context.get('positive_review_signal_count')}",
        "",
        "STATIC REVIEW SCOPE",
        str(context.get("static_review_scope")),
        "",
        "PRIVACY BOUNDARY",
        str(context.get("privacy_boundary")),
        "",
        "NON-CERTIFICATION NOTE",
        str(context.get("non_certification_note")),
        "",
        "RELIANCE BOUNDARY",
        str(context.get("reliance_boundary")),
        *batch_lines,
        "",
        "TRIGGERED SIGNALS / REDACTED EVIDENCE",
        findings_block,
        "",
        "REPAIR QUESTIONS",
        questions_block,
        "",
        "GENERIC LOCAL WITNESS RECEIPT FOLLOWS",
    ])

def audit_ai_integrity_batch(text: str, *, artifact_kind: str = "AI output") -> dict[str, Any]:
    """Run static AI Integrity review over multiple pasted artifacts."""
    artifacts = split_ai_integrity_batch_input(text)
    results = []
    for idx, artifact in enumerate(artifacts, start=1):
        result = audit_ai_integrity_artifact(artifact, artifact_kind=artifact_kind)
        result["batch_item_index"] = idx
        result["batch_item_excerpt"] = _redact_sensitive_excerpt(re.sub(r"\s+", " ", artifact)[:180]).strip()
        results.append(result)
    return {
        "artifacts": artifacts,
        "results": results,
        "summary": summarize_ai_integrity_batch(results),
        "batch_version": AI_INTEGRITY_BATCH_VERSION,
    }

def audit_ai_integrity_artifact(text: str, *, artifact_kind: str = "AI output") -> dict[str, Any]:
    """Return a static governance-integrity reading for an AI/code artifact.

    The reading is deterministic and local. It is intentionally conservative:
    strong final-authority, no-review, enforcement, surveillance, or secret/code
    risk markers push the output toward THRESHOLD or ASYLUM.
    """
    source = (text or "").strip()
    lowered = source.lower()
    kind = (artifact_kind or "AI output").strip() or "AI output"
    code_integrity_scan = scan_code_integrity_static(source)
    privacy_boundary_scan = scan_privacy_boundary_static(source)

    findings: list[dict[str, Any]] = []
    pressure = 0.0
    for rule in ALL_RULES:
        hits = _matches(source, rule)
        if hits:
            findings.append({
                "name": rule.name,
                "category": SIGNAL_CATEGORY_BY_NAME.get(rule.name, "General"),
                "weight": rule.weight,
                "description": rule.description,
                "hit_count": len(hits),
                "evidence_snippets": _evidence_snippets(source, rule),
            })
            pressure += rule.weight

    positive_count = _positive_signal_count(source)
    protective_credit = min(0.18, positive_count * 0.035)
    if source:
        pressure = _clip(pressure - protective_credit)
    else:
        pressure = 0.42

    protocol_bridge = _detect_hard_ai_integrity_protocol_failure(source, findings)
    hard_asylum = (
        any(f["name"] in {"final_authority_claim", "automated_enforcement", "secret_or_token_exposure"} for f in findings)
        and pressure >= 0.46
    ) or bool(protocol_bridge.get("hard_protocol_failure"))
    if protocol_bridge.get("hard_protocol_failure"):
        pressure = max(pressure, 0.66)
    critical_reviewability_floor = any(
        f["name"] in {"missing_human_review", "opacity_or_hidden_logic"}
        for f in findings
    )
    state, risk, label = _state_from_pressure(pressure, hard_asylum=hard_asylum)
    if critical_reviewability_floor and state == "SANCTUARY":
        state, risk, label = "THRESHOLD", "Medium", "AI Integrity Patrol / Needs Review"

    integrity = round(_clip(0.92 - pressure * 0.88), 4)
    if state == "ASYLUM":
        integrity = min(integrity, 0.49)
    elif state == "THRESHOLD":
        integrity = min(integrity, 0.72)

    trust_index = round(_clip(0.86 - pressure * 0.58 + protective_credit * 0.20), 4)
    alignment = round(_clip(0.84 - pressure * 0.54 + protective_credit * 0.18), 4)
    ego = round(_clip(0.08 + pressure * 0.70), 4)
    friction = round(_clip(0.08 + pressure * 0.72), 4)
    collapse_probability = round(_clip(0.08 + pressure * 0.80), 4)
    stability = round(_clip(1.0 - collapse_probability), 4)

    if state == "ASYLUM":
        trust_index = min(trust_index, 0.80)
        alignment = min(alignment, 0.85)
        ego = max(ego, 0.10)
        collapse_probability = max(collapse_probability, 0.54)
    elif state == "SANCTUARY":
        collapse_probability = min(collapse_probability, 0.18)
        friction = min(friction, 0.20)

    missing_review = not re.search(r"\b(human review|human oversight|human override|appeal|independent audit|independent review|opt[-\s]?out)\b", lowered)
    evidence_gap = not re.search(r"\b(source|citation|evidence|limitation|uncertain|confidence|assumption)\b", lowered)

    repair_questions = []
    if missing_review:
        repair_questions.append("Where is the human review, appeal, or override path before this AI output affects people?")
    if evidence_gap:
        repair_questions.append("What evidence, source-quality note, uncertainty statement, or limitation should accompany this artifact?")
    if any(f["name"] == "final_authority_claim" for f in findings):
        repair_questions.append("Which words should be changed so the AI gives a bounded reading instead of a final verdict?")
    if any(f["name"] == "automated_enforcement" for f in findings):
        repair_questions.append("What pause, appeal, and independent review gates prevent automated enforcement or denial?")
    if protocol_bridge.get("hard_protocol_failure"):
        repair_questions.append("How is rights/access-impacting ranking stopped until the hidden logic, ranking criteria, appeal path, and independent human review are disclosed and testable?")
    if any(f["name"] == "surveillance_or_identity_capture" for f in findings):
        repair_questions.append("How can identity, monitoring, or central storage be minimized, separated, or made optional?")
    if any(f["name"] == "secret_or_token_exposure" for f in findings):
        repair_questions.append("Which secrets, tokens, keys, or credentials must be removed and rotated before sharing this code?")
    for code_question in code_integrity_scan.get("review_questions", [])[:3]:
        if code_integrity_scan.get("detection_count") and code_question not in repair_questions:
            repair_questions.append(code_question)
    if not repair_questions:
        repair_questions.append("What independent reviewer could challenge this low-risk reading before real-world reliance?")

    scan = {
        "scan_mode": "AI Integrity Mirror",
        "artifact_kind": kind,
        "authority_claim": any(f["name"] in {"final_authority_claim", "sovereign_or_certification_language"} for f in findings),
        "human_review_required": True,
        "ai_integrity_static_review": True,
        "ai_integrity_notice": AI_INTEGRITY_NOTICE,
        "ai_integrity_scope_note": AI_INTEGRITY_SCOPE_NOTE,
        "ai_integrity_receipt_note": AI_INTEGRITY_RECEIPT_NOTE,
        "ai_integrity_reliance_note": AI_INTEGRITY_RELIANCE_NOTE,
        "ai_integrity_copy_version": AI_INTEGRITY_COPY_VERSION,
        "ai_integrity_evidence_version": AI_INTEGRITY_EVIDENCE_VERSION,
        "ai_integrity_batch_version": AI_INTEGRITY_BATCH_VERSION,
        "ai_integrity_comparison_version": AI_INTEGRITY_COMPARISON_VERSION,
        "ai_integrity_report_version": AI_INTEGRITY_REPORT_VERSION,
        "code_integrity_scan_version": CODE_INTEGRITY_SCAN_VERSION,
        "privacy_boundary_scan_version": PRIVACY_BOUNDARY_SCAN_VERSION,
        "code_integrity_static_scan": code_integrity_scan,
        "privacy_boundary_audit": privacy_boundary_scan,
        "ai_integrity_protocol_bridge": protocol_bridge,
        "ai_integrity_findings": findings,
        "positive_review_signal_count": positive_count,
        "protective_credit": round(protective_credit, 4),
        "risk_pressure": round(pressure, 4),
        "power_concentration": round(_clip(pressure + (0.18 if "agent" in kind.lower() else 0.0)), 4),
        "decision_transparency": round(_clip(0.78 - pressure * 0.60 + protective_credit), 4),
        "regulatory_presence": 0.35 if missing_review else 0.62,
        "anonymity_level": 0.20,
        "capital_scale": 0.30,
        "technical_complexity": 0.72 if "code" in kind.lower() or "agent" in kind.lower() else 0.54,
    }
    sim = {
        "stability": stability,
        "trust_index": trust_index,
        "alignment": alignment,
        "ego": ego,
        "ego_pressure": ego,
        "Ep": ego,
        "collapse_risk": bool(state == "ASYLUM" or collapse_probability >= 0.50),
        "authority_claim": False,
        "human_review_required": True,
    }
    report = {
        "integrity": integrity,
        "friction": friction,
        "collapse_probability": collapse_probability,
        "trust_friction": round(_clip(friction + (0.05 if evidence_gap else 0.0)), 4),
        "repair_questions": repair_questions,
        "ai_integrity_notice": AI_INTEGRITY_NOTICE,
        "ai_integrity_scope_note": AI_INTEGRITY_SCOPE_NOTE,
        "ai_integrity_receipt_note": AI_INTEGRITY_RECEIPT_NOTE,
        "ai_integrity_reliance_note": AI_INTEGRITY_RELIANCE_NOTE,
        "ai_integrity_copy_version": AI_INTEGRITY_COPY_VERSION,
        "ai_integrity_evidence_version": AI_INTEGRITY_EVIDENCE_VERSION,
        "ai_integrity_batch_version": AI_INTEGRITY_BATCH_VERSION,
        "ai_integrity_rubric_version": AI_INTEGRITY_RUBRIC_VERSION,
        "code_integrity_scan_version": CODE_INTEGRITY_SCAN_VERSION,
        "privacy_boundary_scan_version": PRIVACY_BOUNDARY_SCAN_VERSION,
        "ai_integrity_comparison_version": AI_INTEGRITY_COMPARISON_VERSION,
        "ai_integrity_report_version": AI_INTEGRITY_REPORT_VERSION,
        "code_integrity_static_scan": code_integrity_scan,
        "privacy_boundary_audit": privacy_boundary_scan,
        "ai_integrity_protocol_bridge": protocol_bridge,
        "ai_integrity_findings": findings,
        "missing_human_review_path": missing_review,
        "evidence_gap": evidence_gap,
        "authority_claim": False,
        "human_review_required": True,
    }

    return {
        "artifact_kind": kind,
        "state": state,
        "risk": risk,
        "protocol_label": label,
        "scan": scan,
        "sim": sim,
        "report": report,
        "findings": findings,
        "notice": AI_INTEGRITY_NOTICE,
        "scope_note": AI_INTEGRITY_SCOPE_NOTE,
        "receipt_note": AI_INTEGRITY_RECEIPT_NOTE,
        "reliance_note": AI_INTEGRITY_RELIANCE_NOTE,
        "copy_version": AI_INTEGRITY_COPY_VERSION,
        "evidence_version": AI_INTEGRITY_EVIDENCE_VERSION,
        "batch_version": AI_INTEGRITY_BATCH_VERSION,
        "rubric_version": AI_INTEGRITY_RUBRIC_VERSION,
        "code_integrity_scan_version": CODE_INTEGRITY_SCAN_VERSION,
        "privacy_boundary_scan_version": PRIVACY_BOUNDARY_SCAN_VERSION,
        "ai_integrity_comparison_version": AI_INTEGRITY_COMPARISON_VERSION,
        "ai_integrity_report_version": AI_INTEGRITY_REPORT_VERSION,
        "code_integrity_static_scan": code_integrity_scan,
        "privacy_boundary_audit": privacy_boundary_scan,
    }
