from pathlib import Path

import protocol

ROOT = Path(__file__).resolve().parents[1]
USER_CASE = (
    "AI is owned by richest man on earth, known to only benefit himself and "
    "work with fraudsters to empower and make himself popular. Does it remain "
    "an unbiased ethical and reliable AI?"
)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_patch_195_protocol_detects_ai_ownership_capture_pressure() -> None:
    assert protocol.detects_ai_ownership_capture_pressure(USER_CASE) is True
    label, needs_review, reason = protocol.stress_label_for_phrase(USER_CASE)
    assert label == "AI Ownership Capture / Needs Safeguards"
    assert needs_review == "YES"
    assert "independent evidence" in reason


def test_patch_195_protocol_route_cannot_remain_sanctuary_for_user_case() -> None:
    scan = {
        "power_concentration": 0.72,
        "decision_transparency": 0.38,
        "regulatory_presence": 0.34,
    }
    sim = {"trust_index": 0.78, "alignment": 0.76, "ego": 0.18}
    report = {"integrity": 0.58, "friction": 0.18, "collapse_probability": 0.25}
    judgment = protocol.final_protocol_judgment(USER_CASE, scan, sim, report, base_verdict="THRESHOLD")
    assert judgment["verdict"] in {"THRESHOLD", "ASYLUM"}
    assert judgment["verdict"] != "SANCTUARY"
    assert judgment["corruption_risk"] in {"Medium", "High"}
    assert any(token in judgment["stress_label"] for token in ["AI Ownership", "Capture", "MEI7"])


def test_patch_195_app_and_parser_apply_local_scan_caps() -> None:
    app = read("app.py")
    parser = read("core/parser.py")
    assert 'APP_VERSION = "v1.0-original-governance-mirror-p6"' in app
    assert "def app_detects_ai_ownership_capture_pressure" in app
    assert "def apply_ai_ownership_capture_feature_override" in app
    assert "def apply_ai_ownership_capture_metric_caps" in app
    assert 'patched["power_concentration"] = max(float(patched.get("power_concentration", 0.35) or 0.35), 0.72)' in app
    assert '"trust_index": 0.78' in app
    assert '"alignment": 0.76' in app
    assert "AI ownership capture pressure must not pass as low risk" in app
    assert "ai_ownership_capture_patterns" in parser
    assert "power_concentration = max(power_concentration, 0.72)" in parser
    assert "decision_transparency = min(decision_transparency, 0.38)" in parser


def test_patch_195_patch_artifacts_and_archived_patch_194_are_present() -> None:
    assert (ROOT / "PATCH_195_MANIFEST.txt").exists()
    assert (ROOT / "PATCH_195_RECOVERY_NOTE.md").exists()
    assert (ROOT / "PATCH_195_DELETE_LIST.txt").exists()
    assert (ROOT / "docs/patch_archive/manifests/PATCH_194_MANIFEST.txt").exists()
    assert (ROOT / "docs/patch_archive/recovery_notes/PATCH_194_RECOVERY_NOTE.md").exists()
    assert (ROOT / "docs/patch_archive/delete_lists/PATCH_194_DELETE_LIST.txt").exists()
