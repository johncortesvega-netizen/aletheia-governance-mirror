# Protocol Baseline Self-Audit

Patch 101 adds a **human-auditable protocol baseline self-audit** for ALETHEIA.

The audit compares selected core protocol, release-boundary, and AI Integrity files against a local SHA-256 baseline manifest. It is designed to answer a narrow question:

> Do watched files still match the known local baseline, or do differences need human review before release?

## Statuses

- `MATCHES_BASELINE` — the watched file exists and its hash matches the manifest.
- `MODIFIED_REQUIRES_HUMAN_REVIEW` — the watched file exists but differs from the manifest.
- `MISSING_REQUIRES_HUMAN_REVIEW` — the watched file listed in the manifest is missing.
- `UNKNOWN_FILE_REQUIRES_HUMAN_REVIEW` — optional mode only; a reviewable file exists outside the manifest.

## How to run

```bat
python tools\run_protocol_baseline_self_audit.py
```

Optional expanded scan:

```bat
python tools\run_protocol_baseline_self_audit.py --include-unknown
python tools\run_protocol_baseline_self_audit.py --json
```

## Boundary

This is a local static comparison only. It is not tamper-proof, not a security guarantee, not privacy certification, not model certification, not automated approval, not enforcement, and not proof that the repository is safe.

Only humans can audit, interpret, approve, reject, or release changes. ALETHEIA can surface differences for review; it cannot certify its own integrity.
