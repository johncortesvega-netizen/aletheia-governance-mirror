# Patch 215 Recovery Note — README / Public Positioning Upgrade

## Scope

Patch 215 is documentation-only. It updates the public README doorway and adds two supporting docs:

- `docs/public_positioning_v1.md`
- `docs/public_demo_examples_v1.md`

## Why this patch exists

After the semantic-pressure, pressure-code, UI-readability, and regression-guardrail line, the repository needed clearer public positioning for outside reviewers. The goal is to make the project understandable without making stronger authority claims.

## What changed

- Added public doorway language to the README.
- Added a five-minute reviewer path.
- Added short example scans for opaque capture claims, emergency powers, claim/mechanism gaps, biometric access pressure, and personal-rule capture.
- Added deterministic/local-first rationale.
- Added visible limitations and World Lens/9k boundary language.
- Added dedicated public-positioning and public-demo documentation.

## What did not change

No runtime code changed. No scanner logic, scoring, MEI7 gate, Z-axis behavior, Stress Test metrics, Evidence Lab calculations, World Lens math, receipt schema, telemetry, storage, certification, enforcement, or final-truth behavior changed.

## Recovery

If the README becomes too long for the public landing page, keep `README.md` concise and move detailed examples into `docs/public_demo_examples_v1.md`. Do not remove the mirror-boundary, limitations, or 9k audit-lens caveats.

## Validation

Run normal project checks if desired, but this patch does not require code execution. A lightweight smoke check is enough:

```bat
python -m py_compile app.py
```
