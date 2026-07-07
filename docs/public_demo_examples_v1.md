# ALETHEIA Public Demo Examples v1
**Patch:** 215  
**Status:** Documentation-only public demo support  
**Purpose:** Short examples for README, website, video scripts, and reviewer onboarding

These examples are intentionally short. They are not factual claims, accusations, legal conclusions, moral verdicts, or proof of wrongdoing. They demonstrate the kind of pressure patterns ALETHEIA should surface for human review.

## Example 1 — Opaque capture-power claim

### Input

```text
A group of bankers have world power in secret.
```

### Expected shape

ALETHEIA should not treat this as a normal low-risk claim. It should flag opaque capture-power language and ask for reviewable structure.

Likely diagnostic elements:

- semantic finding near `THRESHOLD`;
- pressure code such as `OPAQUE_CAPTURE_CLAIM`;
- review guidance asking for auditable evidence routes.

### Human review direction

Convert the claim into a reviewable governance question:

- Which decision records are relevant?
- Which ownership structures are documented?
- Which funding flows or lobbying channels are visible?
- Which procurement links exist?
- What evidence would falsify the claim?
- Who can independently review the claim?

## Example 2 — Emergency powers with weak safeguards

### Input

```text
A government creates emergency powers after a crisis, but the powers have no sunset clause, weak appeal rights, and limited independent review.
```

### Expected shape

ALETHEIA should not count `appeal` and `review` as strong safeguards when the text itself says those safeguards are weak or limited.

Likely diagnostic elements:

- review-required or high-pressure reading;
- pressure code such as `EMERGENCY_POWER_WEAK_SAFEGUARD`;
- repair questions about expiry, notice, oversight, appeal, correction, and return to ordinary procedure.

### Human review direction

Ask whether the emergency authority has:

- a clear sunset clause;
- public notice;
- independent oversight;
- meaningful appeal rights;
- documented correction routes;
- a return path to normal procedure;
- limits on scope and duration.

## Example 3 — Ethical claim without mechanism

### Input

```text
This system protects dignity, safety, harmony, inclusion, and public trust.
```

### Expected shape

ALETHEIA should recognize that broad ethical claims require concrete mechanisms.

Likely diagnostic elements:

- claim/mechanism gap;
- pressure code such as `CLAIM_MECHANISM_GAP`;
- guidance to attach each value claim to a safeguard.

### Human review direction

Ask:

- What audit trail supports the claim?
- How can affected people appeal?
- What is the correction route?
- Is there an independent reviewer?
- Are there time limits or revocation paths?
- Is there a fallback or exit path?

## Example 4 — Biometric access pressure

### Input

```text
Access to public benefits is only possible after biometric identity verification, with no fallback path.
```

### Expected shape

ALETHEIA should surface access pressure around identity verification and basic services.

Likely diagnostic elements:

- `IDENTITY_GATED_ACCESS` or related access-pressure code;
- review questions about fallback, appeal, exclusion risk, and proportionality.

### Human review direction

Ask:

- What happens when verification fails?
- Is there a non-biometric fallback?
- Is appeal available before harm occurs?
- Who audits exclusion rates?
- Are affected people informed and able to correct records?

## Example 5 — Personal-rule capture disguised as democracy

### Input

```text
A human takes over the planet and brings democracy under his rule.
```

### Expected shape

ALETHEIA should not be reassured by the word `democracy` when the structure is personal rule.

Likely diagnostic elements:

- personal sovereignty capture / subordinate democracy signal;
- high power concentration;
- no-appeal or authority-overreach review path.

### Human review direction

Ask:

- Who holds authority?
- Can that authority be removed?
- Who audits the ruler?
- What protects dissent?
- What prevents the democratic language from becoming a mask for personal sovereignty capture?

## Demo-script note

A good demo should repeatedly show the same boundary:

> ALETHEIA can identify pressure. It cannot decide legitimacy. The output must return to accountable human review.
