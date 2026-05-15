# Patch 83 Recovery Note — Android Gradle Plugin Resolution Fix

Patch 83 only changes the Android WebView wrapper build configuration.

If the patch causes problems, restore the previous Android wrapper Gradle files from your backup or previous patch state:

- `android_webview/settings.gradle`
- `android_webview/settings.gradle.kts`
- `android_webview/build.gradle`
- `android_webview/build.gradle.kts`
- `android_webview/app/build.gradle`
- `android_webview/app/build.gradle.kts`

This patch does not include a keystore or signed APK. Do not commit or share:

- `android_webview/signing.properties`
- `*.jks`
- `*.keystore`
- release APK artifacts unless intentionally distributing the APK

After applying Patch 83, open `android_webview/` directly in Android Studio, then run:

1. `File -> Sync Project with Gradle Files`
2. `Build -> Clean Project`
3. `Build -> Rebuild Project`
4. `Build -> Generate Signed Bundle / APK...`

Boundary: no ALETHEIA scoring, receipt, authority-boundary, storage, or permission behavior is changed.
