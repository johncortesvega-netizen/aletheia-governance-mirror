from __future__ import annotations

import streamlit.components.v1 as components


def tree_copy_for_state(state: str, mode: str = "Mirror Check") -> dict:
    """Return display copy for the Mirror/Stress tree without changing metrics."""
    state_key = (state or "THRESHOLD").upper()
    mode_key = (mode or "Mirror Check").strip()

    if state_key == "QUESTION_PROMPT":
        return {
            "state": "QUESTION_PROMPT",
            "headline": "Review Tool Mode",
            "score_label": "Visual review-tool signal",
            "caption": "Audit question detected. This input is a review prompt, not a scored governance scenario.",
            "root": "Human review",
            "trunk": "Question → reflection → repair",
            "branches": ["Clarity", "Appeal", "Bias check", "Repair", "Human review"],
        }

    if mode_key.lower().startswith("stress"):
        base = {
            "root": "Human dignity",
            "trunk": "Power under stress",
            "branches": ["Consent", "Exit", "Appeal", "Time limits", "Independent review", "Evidence clarity", "Basic rights"],
        }
        if state_key == "SANCTUARY":
            return {**base, "state": "SANCTUARY", "headline": "Stable under pressure", "score_label": "Visual stability signal", "caption": "Low capture signal under this scenario. Still requires human review."}
        if state_key == "ASYLUM":
            return {**base, "state": "ASYLUM", "headline": "Protective review signal", "score_label": "Visual pressure signal", "caption": "Protective review required. This is not enforcement and not an automated decision."}
        return {**base, "state": "THRESHOLD", "headline": "Needs safeguards", "score_label": "Visual safeguard-gap signal", "caption": "Boundary condition detected. Add appeal, exit, evidence, and repair before trust can increase."}

    base = {
        "root": "Human review",
        "trunk": "Evidence + accountability",
        "branches": ["Safeguards", "Appeal", "Transparency", "Repair", "Basic rights", "Non-coercion"],
    }
    if state_key == "SANCTUARY":
        return {**base, "state": "SANCTUARY", "headline": "Low capture signal", "score_label": "Visual stability signal", "caption": "The pattern appears relatively reviewable and repairable. This is not approval."}
    if state_key == "ASYLUM":
        return {**base, "state": "ASYLUM", "headline": "Protective review signal", "score_label": "Visual pressure signal", "caption": "High capture or coercion signal. Human repair review is required; ALETHEIA does not enforce action."}
    return {**base, "state": "THRESHOLD", "headline": "Needs safeguards", "score_label": "Visual safeguard-gap signal", "caption": "The pattern sits at a review boundary. Clarify safeguards, appeal, evidence, and correction loops."}


# Patch 71.2: visual-only tree polish constants.
# The tree remains an explanatory UI element; receipt metrics stay canonical.
TREE_VISUAL_CANOPY_LAYER_COUNT = 8
TREE_VISUAL_CAPTION_CLASS = "aletheia-tree-caption-below-visual"
TREE_VISUAL_CENTRAL_GLOW_REMOVED = True

def visual_review_band_for_tree(score: float, state: str) -> dict:
    """Return visual-only band copy for the tree/canopy display.

    Canonical taxonomy remains SANCTUARY / THRESHOLD / ASYLUM. This helper
    only makes the middle THRESHOLD zone easier to understand visually.
    """
    state_key = (state or "THRESHOLD").upper()
    score = max(0.0, min(1.0, float(score)))
    if state_key == "ASYLUM":
        return {"band": "ASYLUM", "label": "Asylum", "summary": "high-risk review zone", "color": "#db7777", "position": 8}
    if state_key == "SANCTUARY":
        return {"band": "SANCTUARY", "label": "Sanctuary", "summary": "low-capture review zone", "color": "#8fbc8f", "position": 92}
    if state_key == "QUESTION_PROMPT":
        return {"band": "QUESTION_PROMPT", "label": "Review prompt", "summary": "question mode", "color": "#8ab4f8", "position": 50}
    if score < 0.49:
        return {"band": "THRESHOLD_MINUS", "label": "Threshold−", "summary": "closer to Asylum; repair needed", "color": "#d8894d", "position": 32}
    if score >= 0.56:
        return {"band": "THRESHOLD_PLUS", "label": "Threshold+", "summary": "closer to Sanctuary; safeguards visible", "color": "#b6c978", "position": 68}
    return {"band": "THRESHOLD", "label": "Threshold", "summary": "middle review zone", "color": "#e5c36b", "position": 50}


def render_pulse_tree(
    score: float,
    ego: float,
    alignment: float,
    title: str = "Live Pulse Tree",
    *,
    state_override: str | None = None,
    mode: str = "Mirror Check",
):
    """
    Streamlit HTML/SVG state tree.

    Patch Tree Visual v2: render the tree as a light-background protocol map
    instead of a dark abstract canvas. The visual makes the concept explicit:
    root = human review, trunk = evidence/accountability, canopy = current
    review band. This remains display-only; receipt metrics stay canonical.
    """
    score = max(0.0, min(1.0, float(score)))
    ego = max(0.0, min(1.0, float(ego)))
    alignment = max(0.0, min(1.0, float(alignment)))

    if score >= 0.62:
        inferred_state = "SANCTUARY"
        leaf_color = "#8fbc8f"
    elif score >= 0.42:
        inferred_state = "THRESHOLD"
        leaf_color = "#e5c36b"
    else:
        inferred_state = "ASYLUM"
        leaf_color = "#db7777"

    state = (state_override or inferred_state or "THRESHOLD").upper()
    if state == "QUESTION_PROMPT":
        leaf_color = "#8ab4f8"
    elif state == "SANCTUARY":
        leaf_color = "#8fbc8f"
    elif state == "THRESHOLD":
        leaf_color = "#e5c36b"
    elif state == "ASYLUM":
        leaf_color = "#db7777"

    visual_band = visual_review_band_for_tree(score, state)
    if state == "THRESHOLD":
        leaf_color = visual_band["color"]

    copy = tree_copy_for_state(state, mode=mode)
    canopy_opacity = 0.70 if state != "QUESTION_PROMPT" else 0.62
    fallen_count = int(round(ego * 6)) if state in {"ASYLUM", "THRESHOLD"} else 0

    branch_labels = copy.get("branches", [])[:6]
    branch_html = "".join(
        f'<span style="display:inline-block;margin:3px 5px 0 0;padding:4px 8px;border-radius:999px;background:#fff8ea;border:1px solid #ead7b5;color:#4f5f43;font-size:11px;">{b}</span>'
        for b in branch_labels
    )
    band_labels = [
        ("ASYLUM", "Asylum"),
        ("THRESHOLD_MINUS", "Threshold−"),
        ("THRESHOLD", "Threshold"),
        ("THRESHOLD_PLUS", "Threshold+"),
        ("SANCTUARY", "Sanctuary"),
    ]
    band_html = "".join(
        f'<span style="display:inline-block;margin:0 5px 6px 0;padding:5px 9px;border-radius:999px;border:1px solid {visual_band["color"] if key == visual_band["band"] else "#ead7b5"};background:{visual_band["color"] if key == visual_band["band"] else "#fff8ea"};color:{"#1f2d22" if key == visual_band["band"] else "#6b7280"};font-size:11px;font-weight:{"800" if key == visual_band["band"] else "600"};">{label}</span>'
        for key, label in band_labels
    )

    fallen_svg = ""
    for i in range(fallen_count):
        x = 58 + (i * 22) % 146
        y = 225 + ((i * 7) % 12)
        fallen_svg += (
            f'<ellipse cx="{x}" cy="{y}" rx="6" ry="3" '
            f'fill="#db7777" opacity="0.55" transform="rotate({i * 19} {x} {y})" />'
        )

    # Visual-only root/trunk/canopy captions inside the SVG.
    canopy_label = visual_band["label"]
    canopy_summary = visual_band["summary"]

    svg_html = f"""
    <div style="
        box-sizing:border-box;
        border:1px solid rgba(143,105,55,0.22);
        background:linear-gradient(180deg,#fffaf0 0%,#f7eedb 100%);
        border-radius:18px;
        padding:16px 16px 14px 16px;
        margin:0;
        font-family:Inter, Arial, sans-serif;
        color:#203040;
        width:100%;
    ">
        <div style="font-family:Georgia,serif;color:#284f2c;font-size:22px;font-weight:800;margin-bottom:6px;">
            🌳 {title}
        </div>
        <div style="color:#526071;font-size:13px;margin-bottom:10px;line-height:1.45;">
            Mode: <strong>{mode}</strong>
            · State: <strong style="color:{leaf_color};">{state}</strong>
            · Band: <strong style="color:{visual_band['color']};">{visual_band['label']}</strong>
            · {copy.get('score_label', 'Visual pressure signal')} {score:.2f}
            · Alignment {alignment:.2f}
            · Ego {ego:.2f}
        </div>
        <div style="color:#203040;font-size:13px;line-height:1.45;margin-bottom:12px;">
            <strong>{copy.get('headline', state)}</strong> — {copy.get('caption', '')}
        </div>
        <div style="border:1px solid #ead7b5;background:#fffdf7;border-radius:12px;padding:10px 11px;margin-bottom:12px;">
            <div style="color:#203040;font-size:12px;margin-bottom:7px;">
                <strong>Review band:</strong> {visual_band['label']} — {visual_band['summary']}
            </div>
            <div>{band_html}</div>
            <div style="height:10px;border-radius:999px;background:linear-gradient(90deg,#db7777 0%,#d8894d 32%,#e5c36b 50%,#b6c978 68%,#8fbc8f 100%);position:relative;margin-top:2px;box-shadow:inset 0 0 0 1px rgba(0,0,0,0.06);">
                <span style="position:absolute;left:calc({visual_band['position']}% - 7px);top:-5px;width:17px;height:17px;border-radius:999px;background:{visual_band['color']};border:2px solid #203040;display:block;"></span>
            </div>
        </div>
        <div style="color:#425466;font-size:12px;line-height:1.5;margin-bottom:12px;">
            Root: <strong>{copy.get('root', 'Human review')}</strong> · Trunk: <strong>{copy.get('trunk', 'Evidence + accountability')}</strong><br/>
            {branch_html}
        </div>

        <svg width="100%" height="360" viewBox="0 0 520 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ALETHEIA protocol tree visual: root human review, trunk evidence and accountability, canopy current review band">
            <rect x="0" y="0" width="520" height="360" rx="18" fill="#fffaf0"/>
            <rect x="16" y="16" width="488" height="328" rx="16" fill="#fffdf7" stroke="#ead7b5"/>

            <!-- Ground / root system: human review foundation -->
            <ellipse cx="260" cy="270" rx="160" ry="16" fill="#ead7b5" opacity="0.55"/>
            <path d="M260 240 C238 254 211 262 178 270" stroke="#8b5e3c" stroke-width="5" stroke-linecap="round" fill="none" opacity="0.75"/>
            <path d="M260 240 C283 254 314 264 354 272" stroke="#8b5e3c" stroke-width="5" stroke-linecap="round" fill="none" opacity="0.75"/>
            <path d="M258 245 C250 260 242 274 231 288" stroke="#8b5e3c" stroke-width="4" stroke-linecap="round" fill="none" opacity="0.62"/>
            <path d="M263 245 C272 260 285 275 300 290" stroke="#8b5e3c" stroke-width="4" stroke-linecap="round" fill="none" opacity="0.62"/>
            <text x="260" y="316" text-anchor="middle" font-size="12" font-family="Inter, Arial" fill="#425466">ROOT · human review</text>

            <!-- Trunk: evidence + accountability -->
            <path d="M246 250 C250 214 251 175 244 137 C262 176 274 214 274 250 Z" fill="#8b5e3c"/>
            <path d="M257 150 C229 127 205 96 187 64" stroke="#8b5e3c" stroke-width="11" stroke-linecap="round" fill="none"/>
            <path d="M263 148 C295 124 320 92 340 58" stroke="#8b5e3c" stroke-width="11" stroke-linecap="round" fill="none"/>
            <path d="M260 135 C263 104 263 79 260 46" stroke="#8b5e3c" stroke-width="9" stroke-linecap="round" fill="none"/>
            <text x="360" y="194" font-size="12" font-family="Inter, Arial" fill="#425466">TRUNK · evidence + accountability</text>
            <path d="M304 190 L350 190" stroke="#d4b88a" stroke-width="2" stroke-dasharray="4 4"/>

            <!-- Canopy: current review band -->
            <ellipse cx="260" cy="94" rx="86" ry="56" fill="{leaf_color}" opacity="{canopy_opacity}"/>
            <ellipse cx="202" cy="112" rx="60" ry="40" fill="{leaf_color}" opacity="{max(0.48, canopy_opacity - 0.10):.2f}"/>
            <ellipse cx="319" cy="111" rx="62" ry="42" fill="{leaf_color}" opacity="{max(0.48, canopy_opacity - 0.10):.2f}"/>
            <ellipse cx="225" cy="66" rx="52" ry="39" fill="{leaf_color}" opacity="{max(0.44, canopy_opacity - 0.14):.2f}"/>
            <ellipse cx="295" cy="66" rx="52" ry="39" fill="{leaf_color}" opacity="{max(0.44, canopy_opacity - 0.14):.2f}"/>
            <ellipse cx="260" cy="126" rx="72" ry="41" fill="{leaf_color}" opacity="{max(0.42, canopy_opacity - 0.18):.2f}"/>
            <ellipse cx="260" cy="95" rx="47" ry="34" fill="#fffdf7" opacity="0.18"/>
            <text x="260" y="88" text-anchor="middle" font-size="18" font-family="Georgia, serif" font-weight="700" fill="#203040">{canopy_label}</text>
            <text x="260" y="108" text-anchor="middle" font-size="12" font-family="Inter, Arial" fill="#203040">{canopy_summary}</text>

            <!-- Explicit taxonomy rail inside the visual -->
            <text x="28" y="32" font-size="11" font-family="Inter, Arial" fill="#6b7280">ASYLUM</text>
            <text x="421" y="32" font-size="11" font-family="Inter, Arial" fill="#6b7280">SANCTUARY</text>
            <line x1="82" y1="28" x2="412" y2="28" stroke="#d4b88a" stroke-width="3" stroke-linecap="round"/>
            <circle cx="{82 + (visual_band['position'] / 100) * 330:.1f}" cy="28" r="8" fill="{visual_band['color']}" stroke="#203040" stroke-width="2"/>

            {fallen_svg}
        </svg>
        <div class="{TREE_VISUAL_CAPTION_CLASS}" style="text-align:center;color:#526071;font-size:11px;line-height:1.45;margin-top:12px;">
            Visual tree and review band are explanatory. They do not change receipt integrity, protocol metrics, or human-review requirements.
        </div>
    </div>
    """

    components.html(svg_html, height=640, scrolling=False)

