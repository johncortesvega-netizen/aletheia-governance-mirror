# ALETHEIA Tests

ALETHEIA separates current release checks from historical test inventory.

## Default active suite

The default pytest command runs the active release-gate suite:

```bat
python -m pytest
```

Because Patch 218 adds `pytest.ini`, the default collection path is:

```text
tests/active/
```

These tests should pass before public release-candidate claims.

## Patch-specific tests

Patch-specific regression files may exist outside `tests/active/`. Run them directly when reviewing that patch.

Example:

```bat
python -m pytest tests/test_patch_214_regression_guardrails.py -q
```

Stable patch regressions can be promoted into `tests/active/`.

## Legacy inventory

Older tests may remain in the repository as historical inventory. They may fail because they target superseded modules, removed functions, old UI flows, or old receipt fields.

Legacy tests are not hidden validation. They must be triaged using the labels in:

```text
docs/test_migration_labels_v1.md
```

## Cleanup principle

Do not claim that the full historical test tree passes unless it actually does. The honest claim is:

> Active release-gate tests pass; legacy inventory is retained for explicit cleanup and restoration.
