from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN_ACTIVITY = ROOT / "android_webview" / "app" / "src" / "main" / "java" / "net" / "johncortesvega" / "aletheia" / "MainActivity.java"
LIVE_URL = "https://aletheialive.streamlit.app/"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_android_main_activity_is_webview_not_default_template():
    main = MAIN_ACTIVITY.read_text(encoding="utf-8")

    assert "class MainActivity" in main
    assert "new WebView(this)" in main
    assert "setContentView(webView)" in main
    assert LIVE_URL in main
    assert "webView.loadUrl(ALETHEIA_URL)" in main
    assert "setJavaScriptEnabled(true)" in main
    assert "setDomStorageEnabled(true)" in main

    forbidden_template_markers = [
        "Hello Android",
        "Hello World",
        "setContent {",
        "ComponentActivity",
        "androidx.compose",
        "Greeting(",
    ]
    for marker in forbidden_template_markers:
        assert marker not in main


def test_android_webview_project_contains_no_default_hello_android_text():
    android_root = ROOT / "android_webview"
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in android_root.rglob("*")
        if path.is_file()
        and ".gradle" not in path.parts
        and "build" not in path.parts
    )

    assert "Hello Android" not in combined
    assert "Hello World" not in combined
    assert "setContent {" not in combined
    assert "androidx.compose" not in combined
    assert LIVE_URL in combined


def test_android_manifest_points_to_webview_activity_and_internet_only():
    manifest = read("android_webview/app/src/main/AndroidManifest.xml")

    assert 'android:name=".MainActivity"' in manifest
    assert '<uses-permission android:name="android.permission.INTERNET" />' in manifest
    assert 'android:usesCleartextTraffic="false"' in manifest
    assert 'android:allowBackup="false"' in manifest

    forbidden_permissions = [
        "ACCESS_FINE_LOCATION",
        "ACCESS_COARSE_LOCATION",
        "CAMERA",
        "RECORD_AUDIO",
        "READ_CONTACTS",
        "READ_EXTERNAL_STORAGE",
        "WRITE_EXTERNAL_STORAGE",
        "POST_NOTIFICATIONS",
    ]
    for permission in forbidden_permissions:
        assert permission not in manifest


def test_troubleshooting_docs_and_ledgers_exist():
    guide = read("docs/android_webview_troubleshooting.md")
    wrapper_doc = read("docs/android_apk_wrapper.md")
    readme = read("README.md")
    manifest = read("PATCH_81_MANIFEST.txt")
    recovery = read("PATCH_81_RECOVERY_NOTE.md")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    assert "Hello Android" in guide
    assert "android_webview/" in guide
    assert "MainActivity.java" in guide
    assert "setContentView(webView)" in guide
    assert "https://aletheialive.streamlit.app/" in guide
    assert "docs/android_webview_troubleshooting.md" in wrapper_doc
    assert "docs/android_webview_troubleshooting.md" in readme

    for text in (manifest, recovery, status, progress):
        assert "Patch 81" in text or "PATCH 81" in text
        assert "Hello Android" in text
        assert "No Streamlit engine change" in text or "does not change ALETHEIA scoring" in text or "No scoring" in text
