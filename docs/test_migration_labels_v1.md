# ALETHEIA Test Migration Labels
**Patch:** 219  
**Status:** Label standard for legacy-test triage

Use these labels when reviewing historical tests.

## ACTIVE_RELEASE_GATE

Current tests that run under default pytest and are expected to pass.

Expected location:

```text
tests/active/
```

Default command:

```bat
python -m pytest
```

## PATCH_REGRESSION

Focused test added for a patch-specific behavior. It may later become active if stable and broadly relevant.

## LEGACY_INVENTORY

Historical test retained for review. Not a release gate. May fail until triaged.

## RESTORE_CANDIDATE

A legacy test with still-valid intent but outdated imports, fixtures, field names, expected copy, or module paths.

Restore path:

1. update imports;
2. replace obsolete fields;
3. remove brittle UI-copy assertions when the behavior is not copy-specific;
4. assert current boundary behavior;
5. promote only after stable pass.

## DELETE_CANDIDATE

A test whose behavior is obsolete and not useful as history. Delete through a patch with a clear note.

## ARCHIVED_HISTORICAL

A test or fixture kept only as development record. It should not be run by default and should not be cited as active validation.

## Label examples

| Situation | Label |
|---|---|
| Test protects false-SANCTUARY regression for opaque capture claims and passes | ACTIVE_RELEASE_GATE |
| Test checks Patch 214 mirror-boundary prompts | PATCH_REGRESSION |
| Test imports a function removed from the current app but may express a useful receipt behavior | RESTORE_CANDIDATE |
| Test asserts exact old Streamlit label text from a removed UI flow | DELETE_CANDIDATE or ARCHIVED_HISTORICAL |
| Test documents an old experimental module no longer shipped | ARCHIVED_HISTORICAL |

## Rule of interpretation

A label is not a verdict on the value of the old work. It is a maintenance status for current release-candidate reliability.
