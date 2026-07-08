# ALETHEIA Patch Notes

## Current patch

### Patch 258 — Behavior Regression Review

Patch 258 adds a narrow active behavior-regression review suite for current
semantic-pressure behavior after the legacy-test quarantine and modularization
path repair work.

It adds `tests/active/test_behavior_regression_review.py`, covering:

- opaque hidden-power claims;
- emergency authority with weak safeguards;
- claim/mechanism gaps;
- identity-gated public-benefit access;
- concrete safeguard language.

The goal is not to bulk-accept or bulk-delete the remaining legacy behavior
bucket. The goal is to protect the current release behavior that matters for the
public mirror boundary while leaving stale historical calibration tests for
separate manual review.

No runtime behavior changed.

## Recent architecture and cleanup sequence

- Patch 245 — Modularization Bridge Inventory
- Patch 246 — App-wide Copy Cleanup Pass
- Patch 247 — Mirror Check Bridge Removal
- Patch 248 — Stress Test Bridge Inventory / Prep
- Patch 249 — Stress Test Bridge Removal
- Patch 250 — Evidence Lab Bridge Removal
- Patch 251 — Evidence Lab `hashlib` Import Hotfix
- Patch 252 — World Lens Bridge Inventory / Prep
- Patch 253 — World Lens Bridge Removal
- Patch 254 — Modularization Final Audit
- Patch 255 — Patch Notes Final Cleanup
- Patch 256 — Legacy Test Quarantine / Import-Break Cleanup
- Patch 257 — Modularization Test Path Repair
- Patch 258 — Behavior Regression Review

## Runtime boundary

Patch 258 is active-test and documentation hygiene only. It does not change
governance logic, scanner behavior, scoring, receipts, World Lens math, Evidence
Lab calculations, telemetry, storage, or the mirror-not-throne boundary.
