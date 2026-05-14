# Receipt Reader - Standard View v1

Patch 134 implements a simple Receipt Reader - Standard View for pasted ALETHEIA receipts.

## What It Does

The reader accepts pasted receipt text, extracts obvious fields when present, and displays:

- native receipt state;
- native ALETHEIA values;
- plain-language explanation;
- standard review bands;
- human-review note;
- non-certification note;
- parsing limits.

If a field is missing, the reader shows `Not found in pasted receipt`. It does not infer missing values.

## Standard Bands

| Native ALETHEIA value | Standard View band |
| --- | --- |
| SANCTUARY | Low review pressure |
| THRESHOLD | Elevated review pressure |
| ASYLUM | High review pressure / escalation review required |
| QUESTION_PROMPT | Not scored / review-tool mode |

Native receipt values remain the source of truth. Standard View is secondary.

## Boundary

Receipt Reader - Standard View explains pasted ALETHEIA receipts. It does not rescore, certify, approve, reject, or override the original receipt.

It also does not change receipt generation, receipt schema, scoring, routing, signal patterns, signal weights, Privacy Audit scan behavior, AI Integrity scan behavior, World Lens math, uploads, downloads, or any original analysis behavior.

The reader does not make external calls, use LLM calls, create embeddings, use a database, create storage, collect telemetry, or claim compliance certification, legal authority, medical authority, political authority, institutional authority, or final truth.

Human review remains required.

## Parsing Limits

The parser is intentionally simple and transparent. It looks for obvious line-based fields such as risk state, protocol-adjusted state, integrity, friction, collapse probability, trust, alignment, ego, repair questions, protocol label, and module/source. If text is malformed or uses unknown labels, those fields are shown as missing rather than guessed.
