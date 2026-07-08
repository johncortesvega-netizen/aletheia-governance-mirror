"""Legacy-test collection quarantine for ALETHEIA.

Patch 256 keeps the default active test gate unchanged while making explicit
legacy full-suite collection safer after Patch 255's patch-archive cleanup.

These files are historical patch-contract tests. They are not part of the
current active release gate (`tests/active/`). They are ignored during explicit
whole-tree collection because they either import removed legacy helpers or
assert the old root-level patch-artifact layout that Patch 255 intentionally
replaced with `docs/patch_archive/`.

This file does not change runtime behavior, scanner logic, scoring, receipts,
World Lens math, Evidence Lab calculations, telemetry, storage, or authority
boundaries.
"""

# Historical tests with imports to helpers that no longer exist anywhere in
# the current codebase. They are retained on disk for audit continuity but
# quarantined from collection until deliberately restored or deleted.
BROKEN_IMPORT_QUARANTINE = [
    "tests/test_scoring_repair_questions.py",
    "tests/test_patch_20_1_batch_question_upload_mode.py",
]

# Historical root-patch-artifact contract tests. Patch 255 intentionally moved
# old patch manifests/recovery/delete artifacts from repository root into
# docs/patch_archive/. These tests check the superseded root layout, not current
# runtime behavior.
PATCH_ARTIFACT_ROOT_CONTRACT_QUARANTINE = [
    "tests/test_patch_105_patch_index_trust_navigation.py",
    "tests/test_patch_106_signal_dictionary_glossary.py",
    "tests/test_patch_109_app_shell_router_refactor_step_2.py",
    "tests/test_patch_110_app_shell_router_refactor_step_3.py",
    "tests/test_patch_111_beginner_try_this_first_ux.py",
    "tests/test_patch_112_privacy_audit_panel_v1.py",
    "tests/test_patch_113_public_trust_package_consolidation.py",
    "tests/test_patch_114_public_release_polish_v1.py",
    "tests/test_patch_115_app_shell_router_refactor_step_4.py",
    "tests/test_patch_116_app_shell_router_refactor_step_5.py",
    "tests/test_patch_117_refactor_stabilization_checkpoint.py",
    "tests/test_patch_118_beginner_ux_polish_v2.py",
    "tests/test_patch_119_app_shell_router_refactor_step_6.py",
    "tests/test_patch_121_shared_status_notice_cards.py",
    "tests/test_patch_123_about_public_info_page_extraction.py",
    "tests/test_patch_124_trust_package_page_extraction.py",
    "tests/test_patch_125_evidence_lab_static_ui_extraction.py",
    "tests/test_patch_126_final_structural_simplification_freeze.py",
    "tests/test_patch_127_encoding_cleanup_tab_icon_restore.py",
    "tests/test_patch_128_public_ui_text_consistency.py",
    "tests/test_patch_129_input_error_clarity.py",
    "tests/test_patch_130_release_candidate_freeze.py",
    "tests/test_patch_131_start_page_gate.py",
    "tests/test_patch_132_start_page_stabilization_checkpoint.py",
    "tests/test_patch_133_receipt_reader_standard_view_design.py",
    "tests/test_patch_134_receipt_reader_standard_view_v1.py",
    "tests/test_patch_135_aletheia_unit_preview_v1.py",
    "tests/test_patch_136_aletheia_unit_preview_stabilization.py",
    "tests/test_patch_137_validation_alignment_after_unit_preview.py",
    "tests/test_patch_138_single_unit_preview_entry_hotfix.py",
    "tests/test_patch_139_unit_preview_header_entry_hotfix.py",
    "tests/test_patch_140_unit_preview_orientation_cleanup.py",
    "tests/test_patch_141_2_unit_preview_reference_placement_hotfix.py",
    "tests/test_patch_141_3_unit_preview_buttons_above_reference_hotfix.py",
    "tests/test_patch_141_v1_ui_receipt_upload_cleanup.py",
    "tests/test_patch_142_11_world_lens_evidence_bundle_layout.py",
    "tests/test_patch_142_12_receipt_reader_standard_view_copy_polish.py",
    "tests/test_patch_142_13_ai_integrity_single_artifact_focus.py",
    "tests/test_patch_142_14_receipt_reader_verbal_standard_view.py",
    "tests/test_patch_142_16_boundary_cases_navigation_placement.py",
    "tests/test_patch_142_1_receipt_reader_parser_calibration.py",
    "tests/test_patch_142_4_receipt_reader_narrative_output.py",
    "tests/test_patch_142_5_receipt_reader_batch_zip_receipt_selection.py",
    "tests/test_patch_142_6_receipt_reader_world_lens_binding.py",
    "tests/test_patch_142_8_world_lens_evidence_bundle_reader.py",
    "tests/test_patch_142_9_receipt_reader_batch_per_receipt_summary.py",
    "tests/test_patch_144_readme_reviewer_clarity.py",
    "tests/test_patch_146_1_unit_preview_github_audit_evidence.py",
    "tests/test_patch_146_unit_preview_receipt_route_world_lens_context.py",
    "tests/test_patch_152_failure_mode_receipt_verbalization.py",
    "tests/test_patch_153_unit_preview_failure_mode_start_here.py",
    "tests/test_patch_154_unit_preview_nested_expanders.py",
    "tests/test_patch_157_stress_test_page_polish.py",
    "tests/test_patch_158_receipt_reader_page_polish.py",
    "tests/test_patch_161_visual_source_cards_grid.py",
    "tests/test_patch_162_artificial_mind_formation_theory.py",
    "tests/test_patch_166_ai_patrol_rebrand.py",
    "tests/test_patch_167_patrol_guide_formatting_restore.py",
    "tests/test_patch_16_1_mirror_wording_contract.py",
    "tests/test_patch_170_ai_integrity_patrol_result_layout.py",
    "tests/test_patch_174_remove_ai_integrity_module.py",
    "tests/test_patch_177_mirror_check_plain_panel_format.py",
    "tests/test_patch_20_2_separate_batch_testing_ui.py",
    "tests/test_patch_47_app_navigation_smoke.py",
    "tests/test_patch_48_release_candidate_checklist.py",
    "tests/test_patch_69_stress_question_prompt_detection.py",
    "tests/test_patch_70_1_negated_safeguard_strengths.py",
]


# Pytest resolves collect_ignore entries relative to this conftest file during
# subtree collection. Keep both repository-root-style paths and tests-local
# paths so `python -m pytest tests --collect-only` and direct full-tree
# collection behave consistently.
def _tests_local(path: str) -> str:
    return path.removeprefix("tests/")

collect_ignore = (
    BROKEN_IMPORT_QUARANTINE
    + PATCH_ARTIFACT_ROOT_CONTRACT_QUARANTINE
    + [_tests_local(path) for path in BROKEN_IMPORT_QUARANTINE]
    + [_tests_local(path) for path in PATCH_ARTIFACT_ROOT_CONTRACT_QUARANTINE]
    + ["tests/test_patch_29_hard_capture_receipt_trace.py", "test_patch_29_hard_capture_receipt_trace.py"]
)
