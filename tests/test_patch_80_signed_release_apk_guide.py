from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_signed_release_docs_and_template_exist():
    guide = read("docs/signed_release_apk.md")
    template = read("android_webview/signing.properties.example")

    assert "Signed Release APK Build Guide" in guide
    assert "keytool -genkeypair" in guide
    assert "assembleRelease" in guide
    assert "app-release.apk" in guide
    assert "Never commit" in guide or "must not be committed" in guide
    assert "signing.properties" in guide
    assert "aletheia-release-key.jks" in template
    assert "CHANGE_ME" in template


def test_release_signing_config_uses_local_properties_only():
    gradle = read("android_webview/app/build.gradle")

    assert "signing.properties" in gradle
    assert "hasReleaseSigning" in gradle
    assert "signingConfigs" in gradle
    assert "buildTypes" in gradle
    assert "assembleRelease" not in gradle
    assert "storePassword signingProperties.getProperty('storePassword')" in gradle
    assert "keyPassword signingProperties.getProperty('keyPassword')" in gradle
    assert "storePassword '" not in gradle
    assert "keyPassword '" not in gradle


def test_signing_secrets_are_ignored_and_not_committed():
    gitignore = read(".gitignore")

    assert "android_webview/signing.properties" in gitignore
    assert "android_webview/*.jks" in gitignore
    assert "android_webview/*.keystore" in gitignore

    forbidden_paths = [
        ROOT / "android_webview" / "signing.properties",
        ROOT / "android_webview" / "aletheia-release-key.jks",
    ]
    for path in forbidden_paths:
        assert not path.exists(), f"Local signing secret should not be committed: {path}"


def test_readme_and_wrapper_docs_link_signed_release_guide():
    readme = read("README.md")
    wrapper_doc = read("docs/android_apk_wrapper.md")

    assert "docs/signed_release_apk.md" in readme
    assert "docs/signed_release_apk.md" in wrapper_doc
    assert "private keystores" in readme or "private keystores" in wrapper_doc
    assert "must stay local" in readme or "must stay local" in wrapper_doc


def test_patch_80_ledgers_and_manifest_preserve_boundaries():
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")
    manifest = read("PATCH_80_MANIFEST.txt")
    recovery = read("PATCH_80_RECOVERY_NOTE.md")

    for text in (status, progress, manifest, recovery):
        assert "Patch 80" in text or "PATCH 80" in text

    combined = "\n".join([status, progress, manifest, recovery])
    assert "No keystore" in combined
    assert "No signed APK" in combined
    assert "No native rewrite" in combined
    assert "No scoring" in combined or "No ALETHEIA scoring" in combined
    assert "No authority" in combined or "authority" in combined
