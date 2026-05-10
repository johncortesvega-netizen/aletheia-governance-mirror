# Patch 32 — Plain Language UI Copy Polish

## Type
UI copy / wording polish only.

## Goal
Make ALETHEIA's app wording match the improved Patch 27–31 logic while staying simple, calm, and readable for lower-grade readers.

## What changed
- Updated app version to `v9.6.12-patch32-plain-language-ui`.
- Reworded the main header, sidebar, Mirror Check, Stress Test, Evidence Lab, World Lens, and Protocol Guide labels/captions toward plain language.
- Added a small plain-language glossary note:
  - Sanctuary means safer.
  - Threshold means check it.
  - Asylum means high risk.
  - A receipt is local proof of what was reviewed.
- Replaced heavier terms where possible:
  - `Grid` → `World Lens` in user-facing copy where appropriate.
  - `judgment` → `reading` where appropriate.
  - `capture pressure` → `control pressure` where helpful.
  - `diagnostics` → `checks` in user-facing text where appropriate.

## What did not change
- No scoring logic changed.
- No ethics logic changed.
- No protocol logic changed.
- No empirical/World Lens calculations changed.
- No Global ID sync, public ledger, push-warning layer, automatic enforcement, or authority handoff was added.

## Recovery
If this patch causes unwanted UI wording, revert `app.py` to the previous committed version. The tests in `tests/test_patch_32_plain_language_ui_copy.py` only assert the presence of the new plain-language UI contract.
