# ALETHEIA v0.1 — Local Witness Receipt v2

## Purpose

The Local Witness Receipt v2 records a local, user-held fingerprint of an ALETHEIA review.

It helps a user later verify what was reviewed, which module produced the report, which app/rubric/prompt version was active, and whether the report stayed inside the mirror-not-throne boundary.

The receipt is not a public ledger entry, not a Global ID sync, not a central database record, and not an authority claim.

## Core rule

ALETHEIA reflects. People decide.

A local receipt documents a review. It does not enforce action.

## Required fields

Each v2 receipt should include:

- `receipt_version`: `local-witness-v2`
- document fingerprint
- processed document fingerprint
- report fingerprint
- audit receipt fingerprint
- timestamp
- ALETHEIA app version
- rubric version
- prompt version
- active modules
- input status
- module name
- protocol-adjusted state
- risk signal
- protocol label
- authority claim: `No`
- public ledger: `No`
- Global ID sync: `No`
- central storage: `No`
- human review required: `Yes`

## Local-first boundaries

A receipt must state:

- Stored locally: Yes
- Public ledger: No
- Global ID sync: No
- Central storage: No
- Authority claim: No
- Human review required: Yes

## What a receipt can prove

A local receipt can help show:

- the input fingerprint at review time
- the processed-input fingerprint after optional actor-bias reduction
- the report fingerprint
- the app/rubric/prompt version used
- the active modules included in the review
- the fact that the output was framed for human review

## What a receipt cannot prove

A local receipt cannot prove:

- legal truth
- political authority
- religious truth
- medical truth
- moral finality
- that a leader must be removed
- that an output is objectively pure
- that human review is unnecessary

## Recovery note

If a receipt is disputed, rerun the same local input with the same app, rubric, and prompt versions, then compare the document, processed-document, report, and receipt hashes.

The receipt itself does not command, enforce, vote, govern, validate spiritual authority, or replace human judgment.

## Required safe boundary labels

- public ledger: No
- Global ID sync: No
- central storage: No
- authority claim: No
- human review required: Yes
