from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def test_world_lens_docs_and_prompt_exist_with_safe_boundaries():
    doc = read("docs/world_lens_simulation.md")
    prompt = read("prompts/world_lens_prompt.md")
    combined = doc + "\n" + prompt

    assert "World Lens Simulation" in combined
    assert "Simulated threshold signal" in combined or "simulated threshold signal" in combined
    assert "not a real Global ID system" in combined
    assert "not a real 9k selection" in combined
    assert "not a command layer" in combined or "Do not command" in combined
    assert "Human review" in combined or "human review" in combined


def test_world_lens_app_ui_contains_simulation_report_and_questions():
    app = read("app.py")

    assert "World Lens Simulation" in app
    assert "Affected groups" in app
    assert "Power gains" in app
    assert "Protection losses" in app
    assert "Basic-rights risk" in app
    assert "Minority-rights risk" in app
    assert "Ambient capture risk" in app
    assert "Appealability" in app
    assert "Exit" in app
    assert "Repair" in app


def test_world_lens_forbidden_authority_language_is_constrained():
    app = read("app.py")
    doc = read("docs/world_lens_simulation.md")
    prompt = read("prompts/world_lens_prompt.md")
    combined = app + "\n" + doc + "\n" + prompt

    assert "automatic reset" in combined.lower()
    assert "World Leader deactivated" in combined
    assert "Global ID sync" in combined
    assert "The AI has decided" in combined
    assert "Forbidden" in combined or "must not say" in combined or "must not" in combined
    assert "not a real Global ID system" in combined


def test_patch_status_and_progress_track_patch_42():
    status = read("PATCH_STATUS.md")
    progress = read("docs/progress_database.md")
    readme = read("README.md")
    about = read("about_page.py")

    assert "Patch 42" in status
    assert "World Lens Simulation" in status
    assert "Patch 42" in progress
    assert "World Lens Simulation" in progress
    assert "World Lens Simulation" in readme
    assert "World Lens Simulation" in about
