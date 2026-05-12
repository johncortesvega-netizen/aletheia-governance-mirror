from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "android_webview" / "app" / "src" / "main" / "res"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_unqualified_launcher_icons_are_not_adaptive_icons():
    icon = read("android_webview/app/src/main/res/mipmap-anydpi/ic_launcher.xml")
    round_icon = read("android_webview/app/src/main/res/mipmap-anydpi/ic_launcher_round.xml")

    for text in (icon, round_icon):
        assert "<adaptive-icon" not in text
        assert "<bitmap" in text
        assert "@drawable/aletheia_launcher_foreground" in text


def test_adaptive_launcher_icons_are_version_qualified_for_api_26_plus():
    icon_v26 = RES / "mipmap-anydpi-v26" / "ic_launcher.xml"
    round_v26 = RES / "mipmap-anydpi-v26" / "ic_launcher_round.xml"

    assert icon_v26.exists()
    assert round_v26.exists()

    for path in (icon_v26, round_v26):
        text = path.read_text(encoding="utf-8")
        assert "<adaptive-icon" in text
        assert "@drawable/ic_launcher_background" in text
        assert "@drawable/ic_launcher_foreground" in text


def test_manifest_still_uses_standard_launcher_resource_names():
    manifest = read("android_webview/app/src/main/AndroidManifest.xml")
    app_gradle = read("android_webview/app/build.gradle")

    assert 'android:icon="@mipmap/ic_launcher"' in manifest
    assert 'android:roundIcon="@mipmap/ic_launcher_round"' in manifest
    assert "minSdk 23" in app_gradle
    assert "android.permission.INTERNET" in manifest

    forbidden_permissions = [
        "ACCESS_FINE_LOCATION",
        "CAMERA",
        "RECORD_AUDIO",
        "POST_NOTIFICATIONS",
        "READ_CONTACTS",
        "WRITE_EXTERNAL_STORAGE",
    ]
    for permission in forbidden_permissions:
        assert permission not in manifest


def test_patch_84_docs_ledgers_and_boundaries_are_present():
    doc = read("docs/android_adaptive_icon_resource_fix.md")
    wrapper_doc = read("docs/android_apk_wrapper.md")
    readme = read("README.md")
    manifest = read("PATCH_84_MANIFEST.txt")
    recovery = read("PATCH_84_RECOVERY_NOTE.md")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    for text in (doc, wrapper_doc, readme, manifest, recovery, status, progress):
        assert "Patch 84" in text or "PATCH 84" in text
        assert "adaptive" in text.lower()
        assert "icon" in text.lower()

    combined = "\n".join([doc, manifest, recovery, status, progress])
    assert "No Streamlit engine change" in combined
    assert "No new Android permissions" in combined or "permissions" in combined
    assert "No keystore" in combined or "keystore" in combined
    assert "signed APK" in combined
