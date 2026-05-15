# Patch 142.6 Recovery Note — Receipt Reader World Lens Binding Fix

Patch 142.6 is a bounded Receipt Reader parser/UI helper fix.

To recover, revert the changed files listed in `PATCH_142_6_MANIFEST.txt`.

This patch does not alter ALETHEIA scoring, verdict routing, taxonomy, receipt schema, receipt generation, World Lens math, Stress Test scoring/tree logic, AI Integrity scan behavior, Privacy Audit scan behavior, uploads/downloads outside Receipt Reader parsing, or any external/network behavior.

Human review remains required. Receipt Reader only translates uploaded receipts into Standard View. It does not rescore, merge verdicts, certify, approve, reject, enforce, or create final truth.
