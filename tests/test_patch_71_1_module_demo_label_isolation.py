from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "app.py"
APP_TEXT = APP_PATH.read_text(encoding="utf-8")


def _literal_dict(name: str) -> dict[str, str]:
    tree = ast.parse(APP_TEXT)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    value = ast.literal_eval(node.value)
                    assert isinstance(value, dict)
                    return value
    raise AssertionError(f"{name} not found in app.py")


def test_patch_71_1_defines_separate_module_demo_libraries():
    mirror = _literal_dict("MIRROR_CHECK_DEMO_SCENARIOS")
    stress = _literal_dict("STRESS_TEST_DEMO_SCENARIOS")

    assert mirror
    assert stress
    assert "Healthcare as a shared human right" in mirror
    assert "Healthcare as a shared human right" not in stress
    assert "Authoritarian capture" in mirror
    assert "Emergency powers without expiry" in stress
    assert set(mirror).isdisjoint(set(stress))


def test_patch_71_1_stress_test_uses_stress_demo_labels_and_library():
    assert 'st.subheader("Stress Test — Try an Idea")' in APP_TEXT
    assert 'st.selectbox("Stress Test demo examples", list(STRESS_TEST_DEMO_SCENARIOS.keys()), key="simulation_scenario_library")' in APP_TEXT
    assert 'st.button("Load Stress Test scenario demo", use_container_width=True, key="simulation_load_stress_demo_button")' in APP_TEXT
    assert 'st.session_state.simulation_scenario_text = STRESS_TEST_DEMO_SCENARIOS[scenario_choice]' in APP_TEXT
    assert 'loaded_demo = STRESS_TEST_DEMO_SCENARIOS.get(st.session_state.get("simulation_demo_choice", ""), None)' in APP_TEXT


def test_patch_71_1_mirror_check_uses_mirror_demo_labels_and_library():
    assert 'st.selectbox("Mirror Check scenario demo examples", list(MIRROR_CHECK_DEMO_SCENARIOS.keys()), key="audit_demo_library")' in APP_TEXT
    assert 'st.button("Load Mirror Check scenario demo", use_container_width=True, key="audit_load_demo_button")' in APP_TEXT
    assert 'demo_text = MIRROR_CHECK_DEMO_SCENARIOS[audit_demo_choice]' in APP_TEXT
    assert 'loaded_audit_demo = st.session_state.get("audit_demo_loaded_text") or MIRROR_CHECK_DEMO_SCENARIOS.get(st.session_state.get("audit_demo_choice", ""), None)' in APP_TEXT


def test_patch_71_1_no_cross_module_load_button_in_stress_block():
    stress_start = APP_TEXT.index('with tab_sim:')
    mirror_start = APP_TEXT.index('with tab_chat:')
    stress_block = APP_TEXT[stress_start:mirror_start]

    assert "Load Stress Test scenario demo" in stress_block
    assert "Load Mirror Check scenario demo" not in stress_block
    assert "MIRROR_CHECK_DEMO_SCENARIOS" not in stress_block


def test_patch_71_1_manifest_recovery_status_and_progress_are_present():
    assert (ROOT / "PATCH_71_1_MANIFEST.txt").exists()
    assert (ROOT / "PATCH_71_1_RECOVERY_NOTE.md").exists()
    assert "Patch 71.1" in (ROOT / "PATCH_STATUS.md").read_text(encoding="utf-8")
    assert "Patch 71.1" in (ROOT / "docs" / "progress_database.md").read_text(encoding="utf-8")
    manifest = (ROOT / "PATCH_71_1_MANIFEST.txt").read_text(encoding="utf-8")
    assert "app.py" in manifest
    assert "tests/test_patch_71_1_module_demo_label_isolation.py" in manifest
