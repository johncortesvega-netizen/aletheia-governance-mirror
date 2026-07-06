# ALETHEIA Patch: Evidence Lab Declutter + S3 World Lens / Receipt Reader

Changed files:
- `app.py`
- `ui/receipt_reader.py`

## Evidence Lab layout declutter
- Keeps the semantic claim/mechanism evidence check near the top.
- Moves the upload/build country-year evidence workflow behind `Advanced: build/upload country-year evidence table`.
- Keeps the semantic evidence check separate from empirical country-year scoring.
- Does not change empirical scoring, country-year data, allocation, or receipts.

## Patch S3 — World Lens semantic regional flags
- Adds `Semantic regional interpretation flags` under World Lens.
- Uses the semantic scanner on the optional World Lens context note.
- Translates semantic terms into regional interpretation flags, such as:
  - identity / verification language
  - access / basic-service language
  - soft legitimacy claims
  - compliance / permanence language
  - visible safeguards
- Adds human-review questions for regional interpretation.
- Does not rescore World Lens evidence, receipts, selected-year rows, or taxonomy labels.

## Patch S3 — Receipt Reader current re-read
- Adds optional `Current semantic re-read` for single uploaded receipt files.
- The re-read is button-triggered and clearly marked as not part of the original receipt.
- It does not change native receipt fields, Standard View, metrics, receipt schema, or uploaded artifact meaning.
- It is only a current scanner comparison for human review.

## Validation
- `python -m py_compile app.py ui/receipt_reader.py` succeeded in the patch workspace.
