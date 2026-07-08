# Patch 201 — Receipt Semantic Layer Framing and Plain-English Main View

## Purpose

Patch 201 corrects the conceptual framing of Receipt Reader semantics. The semantic scan is no longer presented to users as a "current semantic re-read." It is now presented as a **Semantic pressure layer**: one diagnostic layer inside the receipt reading.

This reduces confusion between the native/original receipt state and the semantic diagnostic layer. It also aligns the Reader with the layered causal-chain model introduced in Patch 199.

## What changed

- Visible wording now uses **Semantic pressure layer** / **Semantic layer**.
- Batch tables now use `Semantic Layer` instead of `Current Semantic`.
- The main Receipt Reader view now foregrounds the Simple English walkthrough.
- Technical/supporting material is opt-in:
  - original status and metrics;
  - semantic pressure layer;
  - layered causal audit trail;
  - repair questions and operator hand-off;
  - diagnostics and failure-mode signals;
  - AI/static context and World Lens internals;
  - native receipt audit values.

## Boundary preservation

Patch 201 is a Receipt Reader presentation/framing patch only. It does not change:

- native receipt values;
- receipt schema;
- stored receipt meaning;
- semantic scanner logic;
- module scoring;
- World Lens math;
- Evidence Lab calculations;
- external calls;
- telemetry;
- storage;
- certification/enforcement behavior;
- final-truth claims.

Human review remains required.

## Validation target

```bat
python -m py_compile ui/receipt_reader.py
```
