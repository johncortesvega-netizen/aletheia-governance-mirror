# Patch 84 Recovery Note — Android Adaptive Icon Resource Fix

Patch 84 fixes this Android release-build failure:

```text
<adaptive-icon> elements require a sdk version of at least 26
```

## What changed

Adaptive launcher icon XML now lives in:

```text
android_webview/app/src/main/res/mipmap-anydpi-v26/
```

The unqualified fallback folder now contains non-adaptive bitmap XML:

```text
android_webview/app/src/main/res/mipmap-anydpi/
```

This lets Android resource linking succeed while preserving `minSdk 23`.

## If the same error returns

Check that these files do **not** contain `<adaptive-icon>`:

```text
android_webview/app/src/main/res/mipmap-anydpi/ic_launcher.xml
android_webview/app/src/main/res/mipmap-anydpi/ic_launcher_round.xml
```

Check that these files **do** contain `<adaptive-icon>`:

```text
android_webview/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml
android_webview/app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml
```

Then run:

```bat
tools\run_patch_checks.bat 84
```

In Android Studio, open the `android_webview/` folder and run:

```text
File → Sync Project with Gradle Files
Build → Clean Project
Build → Rebuild Project
Build → Generate Signed Bundle / APK...
```

## Boundary

No ALETHEIA logic changes were made. This patch does not include a keystore, password, private key, or signed APK. It does not add permissions or change the WebView URL. ALETHEIA remains a mirror for human review only.
