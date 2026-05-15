# Patch 142.11 Recovery Note — Receipt Reader World Lens Evidence Bundle Layout Polish

Patch 142.11 is presentation-only. It changes how Receipt Reader displays uploaded World Lens ZIP evidence bundles:

- Native World Lens receipt inspection now appears before supporting CSV evidence tables.
- Supporting CSV files remain below the receipt reading as evidence tables.
- The evidence table inventory no longer dumps every CSV column inline.
- CSV previews use curated readable columns by default.
- Raw uploaded CSV previews remain available only inside an advanced expander.

If this patch must be reverted, restore `ui/receipt_reader.py` and remove `tests/test_patch_142_11_world_lens_evidence_bundle_layout.py`, `PATCH_142_11_MANIFEST.txt`, and this recovery note. Reverting affects only Receipt Reader layout/readability for World Lens evidence bundles and should not affect scoring, World Lens math, receipt generation, routing, taxonomy, or module scan behavior.

Boundary reminder: this patch does not rescore, merge verdicts, certify countries/governments, create receipts, alter uploaded values, or claim final truth. Human review remains required.
