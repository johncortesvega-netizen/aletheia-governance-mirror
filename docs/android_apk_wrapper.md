# Android APK Wrapper — ALETHEIA Mirror

Patch 79 adds a lightweight Android WebView wrapper for the live ALETHEIA Streamlit app.

This is **not a native rewrite** of ALETHEIA. It is a small Android shell that opens:

```text
https://aletheialive.streamlit.app/
```

## Purpose

The wrapper lets a user install an Android APK named **ALETHEIA Mirror** and open the live app in an app-like screen.

ALETHEIA remains:

- free and open-source;
- a governance-risk and corruption-pattern mirror for human review;
- anti-capture by design and capture-risk-detecting by function;
- not an authority, enforcement engine, legal/political determination, public ledger, Global ID system, central storage system, or replacement for human judgment.

## Privacy and permissions

The Android wrapper is intentionally minimal.

Requested Android permission:

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

It does **not** request location, contacts, camera, microphone, storage, SMS, phone, Bluetooth, calendar, notification, account, or background service permissions.

The wrapper does not add ads, trackers, analytics SDKs, push notifications, native storage, public ledger sync, Global ID sync, or central storage.

## Build with Android Studio

1. Open Android Studio.
2. Choose **Open**.
3. Select the repository folder `android_webview/`.
4. Let Gradle sync.
5. Choose **Build > Build Bundle(s) / APK(s) > Build APK(s)**.
6. Android Studio will show the generated debug APK path when the build completes.

## Command-line build

From the `android_webview/` folder, if Gradle and the Android SDK are installed:

```bash
./gradlew assembleDebug
```

If no Gradle wrapper exists locally, use Android Studio or run the equivalent Gradle task with your installed Gradle environment:

```bash
gradle assembleDebug
```

Expected debug APK path:

```text
android_webview/app/build/outputs/apk/debug/app-debug.apk
```

## Distribution note

Sending an APK directly to people is sideloading. Android may warn users that the app is from an unknown source. That warning is normal for APKs distributed outside an app store.

For trust, share the source code, the GitHub release, and the boundary statement with the APK.

Suggested short description:

```text
ALETHEIA Mirror is a free/open-source Android WebView wrapper for the live ALETHEIA governance-risk mirror. It opens https://aletheialive.streamlit.app/. Human review required. ALETHEIA does not rule, vote, command, gatekeep, enforce, or claim final authority.
```

## Current limitations

- Internet is required.
- Streamlit availability depends on the live hosted app.
- The wrapper is not an offline mobile version.
- The wrapper does not provide production mobile-device management, enterprise compliance workflows, or native Android data pipelines.

## Signed release APK

For direct public sharing, prefer a signed release APK over a debug APK.

Patch 80 adds local release-signing support and a safety guide:

```text
docs/signed_release_apk.md
```

The repo includes only `android_webview/signing.properties.example`. Your real `signing.properties` file, `.jks` keystore, and passwords must stay local and must not be committed.
