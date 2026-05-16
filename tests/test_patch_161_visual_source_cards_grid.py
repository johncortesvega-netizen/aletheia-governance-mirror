from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'app.py').read_text(encoding='utf-8')


def test_visual_source_cards_use_shared_grid_and_expander_rendering():
    assert 'VISUAL_SOURCE_FILES = [' in APP
    assert 'def render_visual_source_card(card: dict[str, object], key_prefix: str) -> None:' in APP
    assert 'with st.expander(title, expanded=True):' in APP
    assert 'for start in range(0, len(available_cards), 2):' in APP
    assert 'columns = st.columns(2)' in APP
    assert 'doc_tabs = st.tabs' not in APP


def test_visual_source_cards_include_new_image_references():
    for title in [
        'Global Peace Architecture',
        'The Sovereign Master Blueprint',
        'The Sydney Protocol: Command Dossier',
        "The Sydney Protocol: Architect's Checklist",
    ]:
        assert title in APP


def test_visual_card_assets_exist():
    for relative in [
        'assets/visual_cards/global_peace_architecture.jpg',
        'assets/visual_cards/sovereign_master_blueprint.jpg',
        'assets/visual_cards/sydney_protocol_command_dossier.jpg',
        'assets/visual_cards/sydney_protocol_architect_checklist.jpg',
    ]:
        assert (ROOT / relative).exists(), relative
