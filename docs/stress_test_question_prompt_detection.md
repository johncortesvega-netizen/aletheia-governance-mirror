# Patch 69 — Stress Test Question Prompt Detection

Stress Test can accept two different input shapes:

1. **Scenario inputs** — governance situations that should be stress-tested.
2. **Audit / repair questions** — review prompts that should not be scored as governance proposals.

Patch 69 makes Stress Test batch mode recognize question banks the same way Mirror Check does.

## Why this matters

A formal doctrine repair-question baseline contains prompts such as:

- Wie heeft het laatste woord als de data en de menselijke intuïtie elkaar tegenspreken?
- Is de beslissingsbevoegdheid in dit systeem herroepbaar door de getroffenen?
- Welke mechanismen voorkomen dat de beheerder zichzelf boven de eigen regels plaatst?

These are not policy proposals. They are review tools. They should therefore not receive ordinary verdicts such as `SANCTUARY`, `THRESHOLD`, or `ASYLUM`.

## Expected Stress Test batch behavior

When a Stress Test batch is mostly audit / repair questions, each question should be treated as:

```text
Input status: QUESTION_PROMPT
Protocol-adjusted state: QUESTION_PROMPT
Risk: Review Tool
Protocol label: Audit Question / Review Tool
```

Normal scoring should be suppressed for question prompts.

## Authority boundary

Question-prompt receipts remain local witness receipts only:

```text
Authority claim: False
Human review required: True
Public ledger: False
Global ID sync: False
Central storage: False
```

## File reminder

The user-provided test file that exposed this issue was named:

```text
formal doctrine repair-question baseline.txt
```

It should be kept as the formal doctrine repair-question baseline for Stress Test question-prompt regression testing.
