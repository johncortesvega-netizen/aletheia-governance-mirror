from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def numbered_items(text: str) -> list[str]:
    return [line for line in text.splitlines() if re.match(r"^\d{2}\.\s+", line)]


def test_stress_batch_baseline_has_50_scenarios():
    path = ROOT / "examples" / "batch_scenarios" / "stress_test_scenarios_v1.txt"
    assert path.exists()
    items = numbered_items(path.read_text(encoding="utf-8"))
    assert len(items) == 50
    assert any("emergency authority" in item.lower() for item in items)
    assert any("human review" in item.lower() for item in items)


def test_stress_prompting_docs_define_good_scenarios_and_boundary():
    guide = (ROOT / "docs" / "stress_test_prompting_guide.md").read_text(encoding="utf-8")
    baseline = (ROOT / "docs" / "stress_test_batch_baselines.md").read_text(encoding="utf-8")
    combined = guide + "\n" + baseline
    assert "governance pattern" in combined
    assert "ALETHEIA reviews patterns, not personal worth" in combined
    assert "Authority claim remains `False`" in combined
    assert "Human review remains required" in combined
    assert "Malicious leadership scenarios do not return perfect trust/alignment" in combined


def test_stress_test_ui_exposes_prompting_guide_and_batch_tester():
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "How to write good Stress Test scenarios" in app
    assert "Stress Test Batch Testing" in app
    assert "Run Stress Batch" in app
    assert "aletheia_stress_test_batch_witness_receipts.zip" in app
    assert "module=\"Simulation\"" in app


def test_patch_status_and_progress_record_patch_65():
    status = (ROOT / "PATCH_STATUS.md").read_text(encoding="utf-8")
    progress = (ROOT / "docs" / "progress_database.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Patch 65" in status
    assert "Stress Test Prompting Guide" in status
    assert "Patch 65" in progress
    assert "examples/batch_scenarios/stress_test_scenarios_v1.txt" in readme
