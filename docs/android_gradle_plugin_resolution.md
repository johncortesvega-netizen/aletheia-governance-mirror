# Android Gradle Plugin Resolution Fix

Patch 83 fixes the Android wrapper Gradle configuration for signed APK builds.

## Problem

If Android Studio or Gradle shows an error like this:

```text
Plugin [id: 'com.android.application'] was not found in any of the following sources
```

then the project root is applying the Android application plugin without telling Gradle which Android Gradle Plugin version to download.

## Fix applied in Patch 83

Patch 83 keeps the wrapper as a simple WebView app and moves Android plugin resolution to the proper project layer:

- `android_webview/settings.gradle` defines plugin repositories: `google()`, `mavenCentral()`, and `gradlePluginPortal()`.
- `android_webview/build.gradle` declares `com.android.application` with a version and `apply false`.
- `android_webview/app/build.gradle` applies `com.android.application` only inside the app module.
- Kotlin DSL mirror files are aligned with the same structure so Android Studio cannot pick up stale root-module app settings.

## Build steps after applying Patch 83

Open this folder in Android Studio:

```text
android_webview/
```

Then run:

```text
File -> Sync Project with Gradle Files
Build -> Clean Project
Build -> Rebuild Project
Build -> Generate Signed Bundle / APK...
```

Choose `APK`, choose your existing keystore, select `release`, and create the signed APK.

Command line alternative:

```bat
cd android_webview
gradlew.bat assembleRelease
```

## Boundary note

This patch only fixes Android build configuration. It does not change ALETHEIA scoring, receipts, Streamlit logic, authority boundaries, storage behavior, permissions, or the live app URL.

The wrapper remains a WebView shell for:

```text
https://aletheialive.streamlit.app/
```

It uses only the Android `INTERNET` permission.
