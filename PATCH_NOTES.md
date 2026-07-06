# ALETHEIA combined clarity patch

Changed files only.

## Included
- Patch A/A2/A3/A4: Unit Preview first-60-seconds landing, decluttered layout, column fix, clearer main-entry button.
- Patch B: authority-language cleanup, compact disclaimers, score/label framing as readings rather than verdicts/certification.
- Patch C: shared compact module header pattern: what it does / does not / when to use / output meaning, with details behind expanders.
- Patch D: Receipt Reader repositioned as support utility, cleaner Standard View, stronger non-certification framing.
- Patch E/F direction: heavy philosophy/examples stay opt-in; module machinery and examples are increasingly behind expanders.
- Module declutter pass: Boundary Cases diagnostics/receipt example moved behind expanders; Evidence Lab advanced tables moved behind expanders; World Lens context reflection moved behind an expander.

## Validation
- `python -m py_compile app.py ui/module_page_template.py ui/unit_preview.py ui/receipt_reader.py` passed.
