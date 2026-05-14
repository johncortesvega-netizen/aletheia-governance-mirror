# Receipt Reader - Standard View

Patch 133 defines the Receipt Reader - Standard View before any runtime implementation.

## Purpose

Receipt Reader - Standard View will make pasted ALETHEIA receipts easier for humans and external governance/compliance systems to understand. It maps native ALETHEIA receipt values into plain-language review bands.

The Receipt Reader explains and maps receipts. It does not rescore, certify, approve, reject, override, enforce, or decide.

## Inputs

The future reader should accept pasted ALETHEIA receipt text. Native receipt values are the source of truth. The reader may look for fields such as:

- module or source;
- native risk state or protocol label;
- protocol-adjusted state;
- integrity;
- friction;
- collapse probability;
- trust;
- alignment;
- ego;
- repair questions.

Missing fields must remain missing. The reader must not infer values that are not present in the pasted receipt.

## Outputs

The Standard View should show native values first and standard review bands second:

1. Native ALETHEIA receipt values.
2. Plain-language review-band mapping.
3. Human-review note.
4. Non-certification note.
5. Parsing limits.

Standard View is an interpretation and interoperability layer only. It is not a replacement for the original receipt and must not modify receipt schema.

## Native Values First

SANCTUARY, THRESHOLD, ASYLUM, and QUESTION_PROMPT remain ALETHEIA-native receipt language. They are internal taxonomy states or review-tool modes, not external approvals.

Native receipt values are source of truth. Standard View labels are secondary.

## Standard Review Bands

Initial mapping language:

| Native ALETHEIA value | Standard View band |
| --- | --- |
| SANCTUARY | Low review pressure |
| THRESHOLD | Elevated review pressure |
| ASYLUM | High review pressure / escalation review required |
| QUESTION_PROMPT | Not scored / review-tool mode |

This mapping is for interoperability, not certification.

## Boundaries

Receipt Reader - Standard View must not:

- rescore a receipt;
- override native ALETHEIA values;
- approve or reject a system, policy, model, artifact, or actor;
- certify compliance, safety, truth, privacy, legality, ethics, or legitimacy;
- enforce action;
- claim final truth;
- use external standards as authority;
- make external calls;
- collect telemetry or create storage.

Human review remains required.

## Parsing Limits

Receipt formats may vary by module and patch history. The future reader should parse obvious fields only. If a value is missing, unclear, duplicated, or malformed, the reader should say that the field was not found or could not be read. It must not guess.

## Future Test Requirements

A future implementation should test that:

- native values are displayed before Standard View bands;
- Standard View is labeled as interoperability only;
- QUESTION_PROMPT remains not scored / review-tool mode;
- SANCTUARY, THRESHOLD, and ASYLUM remain internal taxonomy states;
- missing fields are handled calmly;
- no scoring, receipt schema, routing, signal, telemetry, storage, external-call, certification, enforcement, approval, rejection, privacy-guarantee, or final-truth behavior is introduced.
