# PATCH 81 RECOVERY NOTE — Android WebView Hello Android Guard

If the APK still shows a default `Hello Android!` screen after this patch, the installed APK was likely built from the wrong Android Studio project or from an older/default template build.

Recovery steps:

1. Open Android Studio.
2. Open the existing `android_webview/` folder directly.
3. Confirm this file exists and contains a WebView:
   `android_webview/app/src/main/java/net/johncortesvega/aletheia/MainActivity.java`
4. Confirm the file contains:
   - `new WebView(this)`
   - `setContentView(webView)`
   - `https://aletheialive.streamlit.app/`
5. Confirm it does not contain:
   - `Hello Android`
   - `setContent {`
   - Compose template code
6. In Android Studio, run **Build > Clean Project** and **Build > Rebuild Project**.
7. Generate the signed APK again with the existing release key.
8. Install the new APK on a device and confirm it opens the live ALETHEIA Streamlit app.

This patch is a wrapper-build troubleshooting patch only. It does not change ALETHEIA scoring, receipts, route logic, storage boundaries, or authority boundaries.
