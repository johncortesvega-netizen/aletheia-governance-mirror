# Patch 79 Recovery Note — Android WebView APK Wrapper

Patch 79 adds an isolated Android WebView wrapper under `android_webview/`.

If this patch causes issues, remove the following:

- `android_webview/`
- `docs/android_apk_wrapper.md`
- `PATCH_79_MANIFEST.txt`
- `PATCH_79_RECOVERY_NOTE.md`
- `tests/test_patch_79_android_webview_wrapper.py`

Then revert the Patch 79 sections in:

- `README.md`
- `PATCH_STATUS.md`
- `docs/progress_database.md`

No Streamlit engine change was made. No ALETHEIA engine, scoring, routing, receipt, Evidence Lab, World Lens, Mirror Check, Stress Test, or app module behavior was changed. This is not a native rewrite.

The wrapper is intentionally minimal: it opens the hosted Streamlit app and requests only Android internet access. It does not add ads, trackers, analytics SDKs, push notifications, public ledger sync, Global ID sync, central storage, or enforcement behavior.
