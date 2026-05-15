# Patch 61C — Country-Year Available-Year Filter

Status: ready for local verification.

Patch 61C scopes the Country-Year Explorer year dropdown to the selected country/ISO3 only. It prevents the UI from implying that every country has every global year and documents the no-silent-fallback rule.

## Boundaries

- No Global ID sync.
- No real 9k selection.
- No automatic reset.
- No enforcement.
- No authority claim.
- No fallback to stale/global/default country-year values.

## Check

```bat
tools\run_patch_checks.bat 61C
```
