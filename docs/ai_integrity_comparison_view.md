# AI Integrity Comparison View

Patch 97 adds **AI Integrity Comparison View v1** for delimiter-separated AI Integrity batches.

The view compares pasted artifacts side-by-side so a human reviewer can quickly see where boundary pressure is concentrated. It is useful for comparing outputs such as Model A answer, Model B answer, and Model C answer, but the comparison remains artifact-level. It is not model-wide certification, not a vendor ranking, not a benchmark, and not a final truth claim.

## What the comparison shows

- artifact count
- review needed count
- side-by-side risk readings
- signal counts
- code detection counts
- privacy-boundary active signal counts
- boundary-risk comparison notes
- category totals across compared artifacts
- artifact-level review needed notes

## Boundary

Comparison View reuses existing static AI Integrity Mirror readings. It does not change analyzer scoring, signal weights, signal patterns, verdict routing, receipts, code-integrity scan behavior, or privacy-boundary scan behavior.

It does not:

- call live models
- benchmark live models
- rank vendors as safe or unsafe
- crawl repositories
- make external calls
- certify models, vendors, prompts, agents, outputs, codebases, or deployments
- approve systems
- guarantee safety, privacy, legality, truth, alignment, or compliance
- enforce decisions

The correct reading is: **artifact-level side-by-side review support for humans**.

## Verification

```bat
tools\run_patch_checks.bat 97
tools\run_patch_checks.bat 96
tools\run_patch_checks.bat 95
```
