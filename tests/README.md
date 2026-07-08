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


## Patch 256 legacy quarantine

Patch 256 adds `tests/conftest.py` to quarantine two kinds of historical tests during explicit whole-tree collection:

- tests that import helpers no longer present in the current codebase;
- tests that assert the old root-level `PATCH_N_*` artifact layout after Patch 255 intentionally moved old patch artifacts into `docs/patch_archive/`.

The files remain in the repository for audit continuity. Quarantine is not a validation claim and not a runtime change. Each quarantined file should later be restored against the current architecture, archived as historical, or deleted with an explicit note.

## Patch 257 — Modularization path repair

Patch 257 adds active current-structure tests for the post-modularization layout.
These tests replace the old habit of checking for page/component strings inside
`app.py` directly. The current contract is:

- `app.py` remains the Streamlit entrypoint/orchestrator.
- page renderers live in `ui/pages/`;
- shared visual components live in `ui/components/`;
- major extracted pages expose explicit dependency maps where broad namespace
  bridges were removed.

Legacy tests that assert historical `app.py` string locations should be treated
as stale path-contract tests, not runtime regressions. They may be repaired by
checking the current `ui/pages/` or `ui/components/` source, or replaced by
active import/path contracts.

