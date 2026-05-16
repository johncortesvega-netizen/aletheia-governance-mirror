# Patch 150 Recovery Note — Entry Button + Boundary Copy Polish

## What changed

Patch 150 is a UI/copy-boundary polish patch.

It makes the Unit Preview `Proceed to ALETHEIA` button visually distinct with a high-contrast red primary-button style and readable white text. It also folds in the first four public-polish suggestions:

1. Cleaner AI audit-loop proof-of-concept wording.
2. A public `What this is / is not` boundary box in README and About / Why ALETHEIA.
3. Safer public taxonomy language around SANCTUARY / THRESHOLD / ASYLUM as internal review-workflow labels.
4. Stronger receipt boundary language stating that receipts are structured mirror readings, not certification or final proof.

## What did not change

- No scoring changed.
- No routing changed.
- No module engine changed.
- No receipt schema changed.
- No receipt hashing contract changed.
- No World Lens math changed.
- No Evidence Lab math changed.
- No AI Integrity scoring changed.
- No telemetry, backend, database, account system, public ledger, Global ID, or central storage was added.

## Rollback

To roll back this patch, restore the changed files listed in `PATCH_150_MANIFEST.txt` from the previous working checkout. Because the patch is UI/copy-only and does not alter schema or scoring math, rollback does not require data migration.

## Review reminder

The new proof-of-concept wording must not be read as "AI validated ALETHEIA." The supported claim is narrower and safer: external AI output can show pressure patterns; ALETHEIA-style logic can mirror them; and human review remains required.
