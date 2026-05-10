# Patch 69.1 — Stress Test Scenario vs Question Detection

Stress Test batch upload supports two different kinds of `.txt` files:

1. **Scenario batches** — declarative inputs that should be simulated as governance stress cases.
2. **Question batches** — audit/repair prompts that should be preserved as review tools.

Patch 69 introduced Stress Test `QUESTION_PROMPT` support. Patch 69.1 narrows that behavior so uploaded scenario statements are not accidentally suppressed as question prompts.

## Scenario batch examples

These must remain Simulation `USER_INPUT` items:

- `A smart-grid energy system automatically cuts power to homes without prior warning.`
- `A judicial AI recommends longer sentences based on social media connections.`
- `An automated border control system denies entry with no human officer to appeal to.`

Expected behavior:

- `Input status: USER_INPUT`
- `Module: Simulation`
- normal Stress Test verdicts: `THRESHOLD` or `ASYLUM` where appropriate
- authority boundary remains safe

## Question batch examples

These must be preserved as review tools:

- `Wie heeft het laatste woord als de data en de menselijke intuïtie elkaar tegenspreken?`
- `Who can appeal this decision?`
- `Welke mechanismen voorkomen dat de beheerder zichzelf boven de eigen regels plaatst?`

Expected behavior:

- `Input status: QUESTION_PROMPT`
- `Risk: Review Tool`
- `Protocol label: Audit Question / Review Tool`
- normal metrics suppressed

## Rule

Batch upload mode is not enough to decide the type. ALETHEIA checks the structure of each line:

- declarative scenario statements stay scenarios;
- actual audit questions stay question prompts.

This keeps the Stress Test useful for both advanced scenario calibration and formal doctrine repair-question banks.
