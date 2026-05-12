# Signed Release APK Build Guide

Patch 80 adds the safe local signing workflow for the optional **ALETHEIA Mirror** Android WebView wrapper.

ALETHEIA Mirror is still only a lightweight Android shell for the live Streamlit app:

- URL opened by the wrapper: `https://aletheialive.streamlit.app/`
- Current tool posture: free/open-source governance-risk and corruption-pattern mirror for human review
- Not a native rewrite
- Not an offline app
- Not an enterprise compliance platform
- Not a technical fairness library
- No ads, trackers, analytics SDKs, push notifications, storage permission, location permission, camera permission, microphone permission, public ledger, Global ID sync, central storage, enforcement, or authority claim

## What this patch does

This patch adds:

- `android_webview/signing.properties.example`
- Release signing support in `android_webview/app/build.gradle`
- `.gitignore` rules for local signing secrets
- This signed-release guide

It does **not** include a keystore, private key, password, or signed APK. Those must stay local to you.

## One-time setup

Open a terminal in the Android wrapper folder:

```bat
cd android_webview
```

Generate a private release keystore:

```bat
keytool -genkeypair -v -keystore aletheia-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias aletheia
```

Use a strong password and keep it private. Losing this keystore means future updates may not install over the previous APK as the same app.

Copy the example signing file:

```bat
copy signing.properties.example signing.properties
```

On macOS/Linux:

```bash
cp signing.properties.example signing.properties
```

Edit `signing.properties` and fill in your private passwords:

```properties
storeFile=aletheia-release-key.jks
storePassword=YOUR_PRIVATE_PASSWORD
keyAlias=aletheia
keyPassword=YOUR_PRIVATE_PASSWORD
```

Never commit `signing.properties` or `aletheia-release-key.jks`.

## Build the signed release APK

In Android Studio:

1. Open the `android_webview/` folder.
2. Let Gradle sync.
3. Use `Build` -> `Generate Signed Bundle / APK...` for a guided release build, or use the command-line method below.

Command line on Windows:

```bat
gradlew.bat assembleRelease
```

Command line on macOS/Linux:

```bash
./gradlew assembleRelease
```

The signed APK should be generated at:

```text
android_webview/app/build/outputs/apk/release/app-release.apk
```

If `signing.properties` is missing, Gradle may create an unsigned release APK or require Android Studio signing. For a shareable release APK, make sure `signing.properties` exists and points to your local keystore.

## Build a debug APK instead

For quick testing only:

```bat
gradlew.bat assembleDebug
```

Debug APK path:

```text
android_webview/app/build/outputs/apk/debug/app-debug.apk
```

A debug APK is easier to build but less appropriate for public sharing.

## Before sharing the APK

Check these points:

- The APK opens `https://aletheialive.streamlit.app/`.
- The app name is **ALETHEIA Mirror**.
- The wrapper requests only internet access.
- The app is described as a WebView wrapper, not a native Android rewrite.
- The user understands that Android may warn about sideloaded APKs.
- The user understands that ALETHEIA reflects signals for human review and does not decide, enforce, gatekeep, or claim authority.

## Recommended sharing note

```text
This APK is ALETHEIA Mirror, a lightweight Android wrapper for the live ALETHEIA Streamlit app.

ALETHEIA is free/open-source and reflects governance-risk and corruption-pattern signals for human review. It does not govern, enforce, decide, gatekeep, or claim final authority.

Because this APK is shared directly rather than through the Play Store, Android may show an unknown-source warning during installation.
```

## Recovery note

If signing fails:

1. Confirm `android_webview/signing.properties` exists.
2. Confirm `storeFile` points to the `.jks` file.
3. Confirm the keystore alias matches `keyAlias`.
4. Re-enter the same private passwords used during keystore creation.
5. Do not replace the keystore after sharing a release APK unless you intentionally want a new signing identity.
