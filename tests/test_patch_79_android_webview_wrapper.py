from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ANDROID = ROOT / "android_webview"
LIVE_URL = "https://aletheialive.streamlit.app/"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_android_webview_project_exists_and_points_to_live_app():
    assert (ANDROID / "settings.gradle").exists()
    assert (ANDROID / "build.gradle").exists()
    assert (ANDROID / "app" / "build.gradle").exists()
    assert (ANDROID / "app" / "src" / "main" / "AndroidManifest.xml").exists()
    assert (ANDROID / "app" / "src" / "main" / "java" / "net" / "johncortesvega" / "aletheia" / "MainActivity.java").exists()

    main_activity = read("android_webview/app/src/main/java/net/johncortesvega/aletheia/MainActivity.java")
    strings = read("android_webview/app/src/main/res/values/strings.xml")
    assert LIVE_URL in main_activity
    assert LIVE_URL in strings
    assert "ALETHEIA Mirror" in strings
    assert "setJavaScriptEnabled(true)" in main_activity
    assert "setDomStorageEnabled(true)" in main_activity
    assert "setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW)" in main_activity
    assert "setAllowFileAccess(false)" in main_activity
    assert "setAllowContentAccess(false)" in main_activity


def test_android_manifest_has_only_internet_permission_and_no_authority_sync_claims():
    manifest = read("android_webview/app/src/main/AndroidManifest.xml")
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

    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in ANDROID.rglob("*")
        if path.is_file()
    )
    forbidden_claims = [
        "public ledger",
        "Global ID sync",
        "central storage",
        "enforce outcomes",
        "final authority",
    ]
    for claim in forbidden_claims:
        assert claim not in combined


def test_android_wrapper_docs_and_readme_preserve_boundaries():
    docs = read("docs/android_apk_wrapper.md")
    readme = read("README.md")

    assert "not a native rewrite" in docs
    assert "not an offline mobile version" in docs
    assert "INTERNET" in docs
    assert "does not add ads, trackers, analytics SDKs" in docs
    assert "does not rule, vote, command, gatekeep, enforce, or claim final authority" in docs
    assert "android_webview/" in readme
    assert "not a native rewrite" in readme
    assert "not an offline mobile version" in readme
    assert "does not add ads, trackers, analytics SDKs" in readme


def test_patch_79_ledgers_are_present():
    manifest = read("PATCH_79_MANIFEST.txt")
    recovery = read("PATCH_79_RECOVERY_NOTE.md")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    for text in (manifest, recovery, status, progress):
        assert "Patch 79" in text or "PATCH 79" in text
        assert "Android WebView" in text
        assert "No Streamlit engine change" in text or "does not change ALETHEIA scoring" in text
        assert "No native rewrite" in text or "not a native rewrite" in text
