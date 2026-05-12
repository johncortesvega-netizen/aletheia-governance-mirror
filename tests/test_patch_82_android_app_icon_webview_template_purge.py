from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANDROID = ROOT / "android_webview"
RES = ANDROID / "app" / "src" / "main" / "res"
LIVE_URL = "https://aletheialive.streamlit.app/"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_android_manifest_binds_aletheia_launcher_icons_and_webview_activity():
    manifest = read("android_webview/app/src/main/AndroidManifest.xml")

    assert 'android:name=".MainActivity"' in manifest
    assert 'android:icon="@mipmap/ic_launcher"' in manifest
    assert 'android:roundIcon="@mipmap/ic_launcher_round"' in manifest
    assert '<uses-permission android:name="android.permission.INTERNET" />' in manifest
    assert 'android:usesCleartextTraffic="false"' in manifest
    assert 'android:allowBackup="false"' in manifest

    forbidden_permissions = [
        "ACCESS_FINE_LOCATION",
        "ACCESS_COARSE_LOCATION",
        "CAMERA",
        "RECORD_AUDIO",
        "READ_CONTACTS",
        "WRITE_CONTACTS",
        "READ_SMS",
        "SEND_SMS",
        "READ_EXTERNAL_STORAGE",
        "WRITE_EXTERNAL_STORAGE",
        "MANAGE_EXTERNAL_STORAGE",
        "POST_NOTIFICATIONS",
        "BLUETOOTH",
        "READ_CALENDAR",
        "WRITE_CALENDAR",
        "GET_ACCOUNTS",
    ]
    for permission in forbidden_permissions:
        assert permission not in manifest


def test_launcher_icon_resources_are_aletheia_assets_not_default_android_only():
    expected_files = [
        "drawable/aletheia_launcher_foreground.png",
        "drawable/ic_launcher_background.xml",
        "drawable/ic_launcher_foreground.xml",
        "mipmap-anydpi/ic_launcher.xml",
        "mipmap-anydpi/ic_launcher_round.xml",
        "mipmap-anydpi-v26/ic_launcher.xml",
        "mipmap-anydpi-v26/ic_launcher_round.xml",
        "mipmap-mdpi/ic_launcher.webp",
        "mipmap-mdpi/ic_launcher_round.webp",
        "mipmap-hdpi/ic_launcher.webp",
        "mipmap-hdpi/ic_launcher_round.webp",
        "mipmap-xhdpi/ic_launcher.webp",
        "mipmap-xhdpi/ic_launcher_round.webp",
        "mipmap-xxhdpi/ic_launcher.webp",
        "mipmap-xxhdpi/ic_launcher_round.webp",
        "mipmap-xxxhdpi/ic_launcher.webp",
        "mipmap-xxxhdpi/ic_launcher_round.webp",
    ]
    for rel in expected_files:
        path = RES / rel
        assert path.exists(), rel
        assert path.stat().st_size > 100, rel

    foreground_xml = read("android_webview/app/src/main/res/drawable/ic_launcher_foreground.xml")
    background_xml = read("android_webview/app/src/main/res/drawable/ic_launcher_background.xml")
    fallback_icon = read("android_webview/app/src/main/res/mipmap-anydpi/ic_launcher.xml")
    fallback_round = read("android_webview/app/src/main/res/mipmap-anydpi/ic_launcher_round.xml")
    adaptive_icon = read("android_webview/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml")
    adaptive_round = read("android_webview/app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml")

    assert "@drawable/aletheia_launcher_foreground" in foreground_xml
    assert "#F7F0E6" in background_xml
    assert "<adaptive-icon" not in fallback_icon
    assert "<adaptive-icon" not in fallback_round
    assert "@drawable/aletheia_launcher_foreground" in fallback_icon
    assert "@drawable/aletheia_launcher_foreground" in fallback_round
    assert "@drawable/ic_launcher_background" in adaptive_icon
    assert "@drawable/ic_launcher_foreground" in adaptive_icon
    assert "@drawable/ic_launcher_background" in adaptive_round
    assert "@drawable/ic_launcher_foreground" in adaptive_round

    default_foreground = read("android_webview/app/src/main/res/drawable/ic_launcher_foreground.xml")
    assert "#3DDC84" not in default_foreground
    assert "android:pathData" not in default_foreground


def test_android_wrapper_is_webview_only_and_default_template_is_purged():
    main_java = read("android_webview/app/src/main/java/net/johncortesvega/aletheia/MainActivity.java")
    stale_kotlin = read("android_webview/app/src/main/java/V1/Aletheia/MainActivity.kt")
    app_gradle = read("android_webview/app/build.gradle")
    libs = read("android_webview/gradle/libs.versions.toml")

    assert "new WebView(this)" in main_java
    assert "setContentView(webView)" in main_java
    assert LIVE_URL in main_java
    assert "webView.loadUrl(ALETHEIA_URL)" in main_java
    assert "setAllowFileAccess(false)" in main_java
    assert "setAllowContentAccess(false)" in main_java

    assert "LegacyTemplateNeutralized" in stale_kotlin
    assert "com.android.application" in app_gradle
    assert "namespace 'net.johncortesvega.aletheia'" in app_gradle
    assert "applicationId 'net.johncortesvega.aletheia'" in app_gradle
    assert "compose" not in app_gradle.lower()
    assert "androidx.compose" not in libs

    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in ANDROID.rglob("*")
        if path.is_file()
        and ".gradle" not in path.parts
        and "build" not in path.parts
        and path.suffix.lower() not in {".png", ".webp", ".jar", ".lock", ".bin"}
    )
    forbidden_template_markers = [
        "Hello Android",
        "Hello World",
        "setContent {",
        "ComponentActivity",
        "androidx.compose",
        "Greeting(",
    ]
    for marker in forbidden_template_markers:
        assert marker not in combined


def test_patch_82_docs_ledgers_and_boundary_are_present():
    readme = read("README.md")
    wrapper_doc = read("docs/android_apk_wrapper.md")
    troubleshooting = read("docs/android_webview_troubleshooting.md")
    manifest = read("PATCH_82_MANIFEST.txt")
    recovery = read("PATCH_82_RECOVERY_NOTE.md")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    assert "Patch 82" in readme
    assert "launcher icon" in wrapper_doc.lower()
    assert "Patch 82 note" in troubleshooting
    assert "Hello Android" in troubleshooting

    for text in (manifest, recovery, status, progress):
        assert "Patch 82" in text or "PATCH 82" in text
        assert "Android App Icon" in text or "launcher icon" in text
        assert "No Streamlit engine change" in text or "does not change ALETHEIA scoring" in text or "No scoring" in text
        assert "No new Android permissions" in text or "No new Android permission" in text
        assert "No keystore" in text
