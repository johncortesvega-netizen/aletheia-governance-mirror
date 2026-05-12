# Patch 84 — Android Adaptive Icon Resource Fix

Patch 84 fixes a release-build resource-linking failure in the optional ALETHEIA Mirror Android WebView wrapper.

## Problem

Android release builds can fail with:

```text
<adaptive-icon> elements require a sdk version of at least 26
```

The wrapper supports `minSdk 23`, but adaptive launcher icon XML was placed in `mipmap-anydpi/`, where it is visible to API levels below 26. Android adaptive icons must only be used from API 26 onward.

## Fix

Patch 84 keeps broad Android compatibility and moves the adaptive icon XML into the version-qualified resource folder:

```text
android_webview/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml
android_webview/app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml
```

The unqualified fallback resources are now simple bitmap launcher icons:

```text
android_webview/app/src/main/res/mipmap-anydpi/ic_launcher.xml
android_webview/app/src/main/res/mipmap-anydpi/ic_launcher_round.xml
```

This lets API 26+ devices use adaptive icons while older devices get a non-adaptive fallback.

## Build steps after applying

Open `android_webview/` in Android Studio, then run:

```text
File → Sync Project with Gradle Files
Build → Clean Project
Build → Rebuild Project
Build → Generate Signed Bundle / APK...
```

Or from the command line:

```bat
cd android_webview
gradlew.bat assembleRelease
```

The signed release APK, if your local signing properties are configured, appears under:

```text
android_webview\app\build\outputs\apk\release\
```

## Boundary

Patch 84 changes Android launcher-icon resource placement only. It does not change ALETHEIA scoring, Mirror Check, Stress Test, Evidence Lab, World Lens, receipts, prompts, public ledger behavior, Global ID sync, central storage, authority boundaries, WebView URL, permissions, keystore handling, or signed APK distribution.
