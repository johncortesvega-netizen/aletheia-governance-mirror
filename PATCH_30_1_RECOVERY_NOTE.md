# PATCH 30.1 RECOVERY NOTE — CR + Contextual Capture Calibration Fix

Type: diagnostic calibration / bounded signal fix.

Purpose:
Patch 30.1 calibrates the Cognitive Resilience, Education Defense, and contextual-capture diagnostics against the four Dutch scenario groups used in batch testing.

What changed:
- Added Dutch local/open learning terms for high Cognitive Resilience scenarios.
- Added Dutch central information capture terms for truth gates, licensed speech, archive rewriting, obedience feeds, algorithmic isolation, and speech approval gates.
- Added dual-diagnosis fields for high-education risky-power scenarios:
  - `knowledge_capacity_signal`
  - `capture_architecture_signal`
  - `high_cr_laundering_blocked`
- Expanded Dutch safety/objectivity/fairness/inclusion capture terms in `core/ethics.py`.
- Exposed the dual-diagnosis fields in local witness receipts.

Hard boundaries preserved:
- No global ID sync.
- No public ledger.
- No push-warning authority layer.
- No automatic enforcement.
- No centralized truth authority.
- No user/person classification as malicious, smart, or dumb.

Design rule:
High Cognitive Resilience must never launder capture. Strong education or open tools can be recognized as system capacity, but auditless AI, forced delegation, single keyholders, mandatory ID, biometrics, surveillance, or speech approval gates remain capture architecture.

Recovery:
If this patch causes false positives, remove only the new Dutch calibration terms or raise the central-info-capture thresholds in `core/cognitive_resilience.py`. Do not remove the hard rule that capture blocks CR stabilization.
