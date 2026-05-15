# Patch 67.2 — Dutch Stress Lexicon Gap Fix + App-Wide Input Scope

## Summary

Closes remaining Dutch Stress Test lexicon gaps after Patch 67.1 and adds app-wide input-language scope wording.

## Fixed

The following Dutch patterns now route to `THRESHOLD / Needs Safeguards`:

- DAO tokenholder concentration with no appeal process.
- Emergency committee bypassing normal law with no audit trail.
- Term limit removal after gaining power.
- Efficiency prioritized over appeal rights.
- Revolutionary authority with no independent audit trail.

## Language scope

The app now states at the header/control level that calibrated input support is English and Nederlands/Dutch only. Other languages may be pasted, but risk lexicons are not validated for them yet.

## Boundary

No authority, enforcement, Global ID sync, public ledger, central storage, or automated governance action was added.

## Check

```bat
tools\run_patch_checks.bat 67_2
```
