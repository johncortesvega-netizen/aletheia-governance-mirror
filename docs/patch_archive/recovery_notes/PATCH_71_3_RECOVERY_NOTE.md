# Patch 71.3 Recovery Note — Stress Test Missing-Safeguard Negation + Tree Canopy Tune

If Patch 71.3 causes a regression, revert only the files listed in `PATCH_71_3_MANIFEST.txt`.

Expected behavior after recovery/reapply:

- Stress Test scenarios that explicitly lack safeguards, such as:
  - `lacks explainability`
  - `lacks independent challenge`
  - `lacks human override`
  - `without appeal`
  - `no independent review`

  should route to review / Needs Safeguards behavior rather than perfect Sanctuary-like metrics.

- These missing-safeguard phrases must not be counted as positive transparency, appeal, review, or accountability features.

- The explanatory tree canopy should sit lower and remain visually connected to the trunk/branches.

- ALETHEIA remains a local mirror only:
  - Authority claim: False
  - Human review required: True
  - Public ledger: False
  - Global ID sync: False
  - Central storage: False

Recommended check:

```bat
tools\run_patch_checks.bat 71_3
```
