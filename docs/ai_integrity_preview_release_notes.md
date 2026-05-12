# ALETHEIA v1.0 AI Integrity Preview — Release Notes

Patch 100 closes the Patch 85-100 AI Integrity adoption arc as a public-facing preview package.

## Stabilized surface

- AI Integrity Mirror static review is documented as artifact-level only.
- Code Integrity Static Scan and Privacy Boundary Audit Panel are framed as deterministic review aids, not guarantees.
- Batch Review, Comparison View, Red Team Prompt Pack, and Report Builder now have a consolidated public adoption path.
- README and About page point users to demo files, docs, screenshot guidance, and regression checks.

## Non-authority boundary

This release does not add live model calls, external calls, repository crawling, vendor ranking, model-wide certification, code-safety certification, vulnerability certification, privacy guarantee, legal authority, medical authority, political authority, religious authority, public ledger sync, Global ID sync, central storage, or automated enforcement.

## Suggested local verification

```bat
tools\run_patch_checks.bat 100
tools\run_patch_checks.bat 99
tools\run_patch_checks.bat 98
tools\run_patch_checks.bat 97
tools\run_patch_checks.bat 96
tools\run_patch_checks.bat 95
```
