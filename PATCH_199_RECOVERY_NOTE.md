# Patch 199 — Layered Causal Receipt Chain

Status: READY FOR LOCAL REVIEW

Patch 199 turns Receipt Reader Standard View into a clearer causal audit path. Instead of reading like a flat list of variables, uploaded receipts now show a five-layer explanation chain:

1. **Raw ingestion / phenomenological layer** — raw input excerpt and current invisibility-filter status.
2. **Linguistic and semantic pressure** — claim-to-mechanism ratio, modal pressure, proximity hits, and semantic notes from the current semantic re-read.
3. **Zero-point baseline / raw metrics** — raw/pre-ethics integrity, friction, collapse pressure, alignment, and ego when those fields exist in the uploaded receipt.
4. **Sydney Protocol gate / ethical correction** — native receipt state, protocol label, adjusted integrity, and an integrity-gap explanation when raw and adjusted values can be compared.
5. **Human hand-off / boundary of code** — Z-Axis/humility-cap note and parsed repair questions.

The causal chain is explanatory only. It does not mutate or reinterpret native receipt values. Missing raw metrics are shown as missing rather than inferred.

## Boundary notes

- Receipt Reader explanation/layout only.
- No native receipt values changed.
- No receipt schema changed.
- No stored receipt meaning changed.
- No current semantic scanner logic changed.
- No module scoring, World Lens math, Evidence Lab calculations, external calls, telemetry, storage, certification, enforcement, or final-truth behavior changed.
- The current semantic reading remains a comparison layer only.
- Human review remains required.

## Validation target

```bat
python -m py_compile ui/receipt_reader.py
```
