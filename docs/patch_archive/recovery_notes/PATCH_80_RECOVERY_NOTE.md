# Patch 80 Recovery Note - Signed Release APK Build Guide

Patch 80 is documentation/build-configuration only.

To revert Patch 80:
1. Remove `docs/signed_release_apk.md`.
2. Remove `android_webview/signing.properties.example`.
3. Restore `android_webview/app/build.gradle` to the Patch 79 version without signing-properties release configuration.
4. Remove the Patch 80 `.gitignore` Android signing-secret lines if desired.
5. Remove the Patch 80 sections from README, `docs/android_apk_wrapper.md`, `PATCH_STATUS.md`, and `docs/progress_database.md`.
6. Remove `tests/test_patch_80_signed_release_apk_guide.py`.

No ALETHEIA scoring, verdict routing, receipt schema, Streamlit UI, Evidence Lab, World Lens, or governance-mirror logic is affected.

If release signing fails locally:
- Confirm `android_webview/signing.properties` exists.
- Confirm `storeFile` points to the local `.jks` file.
- Confirm the alias and passwords match the values used during `keytool -genkeypair`.
- Do not commit the keystore, `signing.properties`, or passwords.
