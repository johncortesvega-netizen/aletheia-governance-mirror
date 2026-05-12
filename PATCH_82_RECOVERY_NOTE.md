# PATCH 82 RECOVERY NOTE — Android App Icon / WebView Template Purge

Patch 82 is limited to the optional Android WebView wrapper. It adds ALETHEIA launcher icons and neutralizes stale Android default-template source that could show `Hello Android!`.

If a build fails or the installed APK still shows the wrong screen/icon:

1. Confirm Patch 82 files were copied into the existing project root, not into a nested patch folder.
2. Run:

```bat
tools\run_patch_checks.bat 82
tools\run_patch_checks.bat 81
```

3. In Android Studio, open this exact folder:

```text
android_webview/
```

4. Uninstall any old ALETHEIA Mirror app from the phone.
5. Use **Build > Clean Project**, then **Build > Rebuild Project**.
6. Generate the signed APK again with the same private release key.

The active WebView entry point is:

```text
android_webview/app/src/main/java/net/johncortesvega/aletheia/MainActivity.java
```

It must load:

```text
https://aletheialive.streamlit.app/
```

Patch 82 does not change ALETHEIA scoring, verdict routing, receipts, Evidence Lab, World Lens, storage, authority boundaries, keystore handling, or the live Streamlit app. No new Android permissions are added. No keystore, password, private key, or signed APK is included.
