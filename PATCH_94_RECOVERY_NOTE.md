# Patch 94 Recovery Note — AI Integrity UI Review Table Polish

Patch 94 is a small AI Integrity Mirror UI/readability patch.

If recovery is needed, restore the patched files listed in `PATCH_94_MANIFEST.txt` from the pre-Patch 94 baseline.

## What changed

- AI Integrity batch output now surfaces highest pressure signals before the review table.
- Batch output includes a clearer compact review table section and category grouping.
- Batch item details include prominent repair questions and collapsed evidence snippets.
- Single-artifact output groups triggered signals by category.
- Evidence snippets are collapsed by category.
- Repair questions are presented as human-review prompts.
- Empty-state copy clarifies that no static trigger is not approval, certification, proof, or a safety guarantee.

## What did not change

- Analyzer scoring.
- Signal patterns.
- Signal weights.
- Verdict routing.
- Receipt generation.
- Privacy architecture.
- External behavior.
- Live model calls or benchmarks.
- Any certification, enforcement, or authority claim.

## Checks

```bat
tools\run_patch_checks.bat 94
tools\run_patch_checks.bat 93
tools\run_patch_checks.bat 92
```
