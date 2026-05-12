from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANDROID = ROOT / "android_webview"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_project_gradle_declares_android_plugin_version_apply_false():
    root_gradle = read("android_webview/build.gradle")
    root_kts = read("android_webview/build.gradle.kts")

    assert "com.android.application" in root_gradle
    assert "version '9.1.1'" in root_gradle
    assert "apply false" in root_gradle
    assert "android {" not in root_gradle
    assert "signingConfigs" not in root_gradle

    assert "com.android.application" in root_kts
    assert 'version "9.1.1"' in root_kts
    assert "apply false" in root_kts
    assert "android {" not in root_kts
    assert "signingConfigs" not in root_kts


def test_settings_define_plugin_repositories_and_single_app_include():
    settings = read("android_webview/settings.gradle")
    settings_kts = read("android_webview/settings.gradle.kts")

    for text in (settings, settings_kts):
        assert "pluginManagement" in text
        assert "google()" in text
        assert "mavenCentral()" in text
        assert "gradlePluginPortal()" in text
        assert "dependencyResolutionManagement" in text
        assert "ALETHEIA Mirror Android" in text

    assert settings.count("include ':app'") == 1
    assert settings_kts.count('include(":app")') == 1


def test_app_module_remains_only_android_application_module_and_preserves_signing():
    app_gradle = read("android_webview/app/build.gradle")
    app_kts = read("android_webview/app/build.gradle.kts")

    assert "id 'com.android.application'" in app_gradle
    assert "version '" not in app_gradle
    assert "namespace 'net.johncortesvega.aletheia'" in app_gradle
    assert "applicationId 'net.johncortesvega.aletheia'" in app_gradle
    assert "signing.properties" in app_gradle
    assert "signingConfigs" in app_gradle
    assert "compileOptions" in app_gradle
    assert "JavaVersion.VERSION_17" in app_gradle

    assert 'id("com.android.application")' in app_kts
    assert " version " not in app_kts
    assert 'namespace = "net.johncortesvega.aletheia"' in app_kts
    assert 'applicationId = "net.johncortesvega.aletheia"' in app_kts
    assert "signing.properties" in app_kts
    assert "signingConfigs" in app_kts
    assert "compileOptions" in app_kts
    assert "JavaVersion.VERSION_17" in app_kts


def test_patch_83_docs_ledgers_and_boundaries_are_present():
    doc = read("docs/android_gradle_plugin_resolution.md")
    wrapper_doc = read("docs/android_apk_wrapper.md")
    readme = read("README.md")
    manifest = read("PATCH_83_MANIFEST.txt")
    recovery = read("PATCH_83_RECOVERY_NOTE.md")
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")

    for text in (doc, wrapper_doc, readme, manifest, recovery, status, progress):
        assert "Patch 83" in text or "PATCH 83" in text
        assert "Android Gradle Plugin" in text or "Gradle Plugin" in text

    combined = "\n".join([manifest, recovery, status, progress, doc])
    assert "No Streamlit engine change" in combined
    assert "No new Android permissions" in combined or "no new Android permissions" in combined
    assert "No keystore" in combined or "no keystore" in combined
    assert "signed APK" in combined
    assert "https://aletheialive.streamlit.app/" in combined
