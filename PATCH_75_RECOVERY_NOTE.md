# Patch 75 Recovery Note — Mirror Check ASYLUM Metric Cap + Copy Polish

If Patch 75 causes unexpected behavior, revert only the files listed in `PATCH_75_MANIFEST.txt`.

## What this patch does

Patch 75 fixes a Mirror Check consistency issue found through public evaluation testing: an ASYLUM / High reading could still show high trust/alignment and very low ego in the UI/receipt path.

This patch:

- applies the existing ASYLUM metric cap in the Mirror Check post-judgment path;
- defensively applies the same cap inside local witness receipt construction;
- changes the local protocol summary from authority-sounding copy to humility/scope copy.

## Expected check

```bat
tools\run_patch_checks.bat 75
```

Expected result:

```text
Patch checks passed.
```

## Boundary

This patch does not make ALETHEIA an authority. It only keeps display and receipt metrics internally consistent with the ASYLUM / High internal taxonomy reading. The receipt remains local, descriptive, and non-enforcing.
