# Patch 129 — Input and Error Clarity Pass

Patch 129 is a refinement-only pass. It makes selected user-facing input and upload messages clearer without changing ALETHEIA's scoring, routing, receipts, signal detection, privacy audit behavior, AI Integrity scan behavior, or World Lens math.

## What changed

- Added `ui/input_clarity.py` for copy-only input and error messages.
- Clarified empty AI Integrity artifact input.
- Clarified empty AI Integrity batch input.
- Clarified the English/Dutch input-language calibration caveat near pasted artifact review.
- Clarified public-data upload failure and direct CSV read failure messages.

## Boundary

This patch does not add a new module, new intelligence, semantic analysis, embeddings, LLM calls, external calls, telemetry, analytics, storage, certification, enforcement, privacy guarantee, or final-truth behavior.

The messages are review aids only. They do not approve, reject, certify, or interpret user content. Humans keep the judgment.
