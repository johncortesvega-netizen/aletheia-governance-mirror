# Android WebView Troubleshooting — ALETHEIA Mirror

Patch 81 adds a hard check for the most common APK-wrapper mistake: building a default Android template instead of the ALETHEIA WebView wrapper.

## Symptom: the APK only says “Hello Android!”

If the installed app only shows a default **Hello Android!** screen, the APK was not built from the patched ALETHEIA WebView activity.

The ALETHEIA wrapper should open:

```text
https://aletheialive.streamlit.app/
```

It should not show a default Compose or template screen.

## Correct project folder

In Android Studio, open this folder directly:

```text
android_webview/
```

Do not create a new Android project and do not open a separate template app. The repo root is the Python/Streamlit project; the Android wrapper project is the nested `android_webview/` folder.

## Correct activity file

The wrapper entry point is:

```text
android_webview/app/src/main/java/net/johncortesvega/aletheia/MainActivity.java
```

That file must:

- create an Android `WebView`;
- call `setContentView(webView)`;
- load `https://aletheialive.streamlit.app/`;
- not contain `Hello Android`, Compose `setContent { ... }`, or a default template layout.

## Clean rebuild steps in Android Studio

1. Open `android_webview/` in Android Studio.
2. Let Gradle sync complete.
3. Use **Build > Clean Project**.
4. Use **Build > Rebuild Project**.
5. Use **Build > Generate Signed Bundle / APK...**.
6. Choose **APK**.
7. Use your existing release key if you already made one.
8. Select the **release** variant and create the APK.

Expected release APK paths may include:

```text
android_webview/app/release/app-release.apk
android_webview/app/build/outputs/apk/release/app-release.apk
```

## Quick source check

From the repo root, run:

```bat
tools\run_patch_checks.bat 81
```

This patch check fails if the committed Android wrapper contains default-template text such as `Hello Android`, Compose entry code, or a replacement activity that does not call `setContentView(webView)`.


## Patch 82 note: default template source neutralized

Patch 82 also neutralizes stale Android Studio default-template source files and aligns the wrapper Gradle configuration to the active Java WebView package. If an APK still shows `Hello Android!` after Patch 82, Android Studio is almost certainly building another project folder or an old cached app install. Uninstall the old app from the phone, open `android_webview/` directly, clean/rebuild, and generate the signed APK again.

Patch 82 also adds the ALETHEIA launcher icon. If the installed app still shows a default green Android icon, rebuild the release APK after applying Patch 82 and reinstall the new APK.

## Boundary preserved

This troubleshooting patch does not change ALETHEIA scoring, verdict routing, receipts, Evidence Lab, World Lens, storage, authority boundaries, or the live Streamlit app. The Android app remains a lightweight WebView shell requiring only internet access.
