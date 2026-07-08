# Patch 198 — Receipt Risk Wording and Repair Blocker

Status: READY FOR LOCAL REVIEW

Patch 198 improves Receipt Reader wording around semantic re-reads and repair capacity.

## What changed

- Added a receipt-safe label for `opaque_capture_claim` semantic hits:
  - **Opaque capture-power claim**
  - **Structural opacity / capture-pressure review**
- Clarified that this is **not** the same as coercive or command-oriented language when the text merely asserts hidden/concentrated power.
- Added a conditional repair-blocker note when an uploaded receipt exposes low repair capacity, multiple capture-pressure component lines, or an ASYLUM receipt with an opaque capture-power semantic finding.
- Added a batch index column indicating whether a receipt has a visible repair blocker.

## Example case

Input text inside a receipt:

```text
a group of bankers have world power in secret
```

Expected current semantic re-read language:

```text
Opaque capture-power claim detected: the text links an actor group to hidden broad-scale power or control without visible evidence basis, correction path, appeal route, or accountable mechanism. This is structural opacity/capture-pressure review, not a coercive-language finding.
```

## Boundary preserved

- No native receipt values are changed.
- No receipt is rescored.
- No original receipt schema is changed.
- The current semantic re-read remains a comparison layer only.
- Human review remains required.

## Validation target

```bat
python -m py_compile ui/receipt_reader.py
```
