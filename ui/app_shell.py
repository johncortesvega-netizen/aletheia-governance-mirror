"""Shared Streamlit app-shell notices for ALETHEIA.

Patch 108 starts the gradual app.py router/shell refactor by extracting the
repeated top-of-app boundary notices into a small UI helper. This module only
renders copy; it does not score, route verdicts, collect data, call external
services, or mutate receipts.
"""
from __future__ import annotations

PUBLIC_V1_LABEL = "ALETHEIA Governance Mirror"


ALETHEIA_GLOBAL_CSS = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Cinzel:wght@600;700&display=swap');

    :root {
        --bg: #f7f2ec;
        --bg-soft: #fbf8f4;
        --panel: rgba(255,250,245,0.92);
        --panel-strong: rgba(255,255,255,0.98);
        --rose: #b88da2;
        --rose-soft: rgba(184,141,162,0.20);
        --rose-border: rgba(184,141,162,0.32);
        --sage: #8ea190;
        --gold: #c7aa72;
        --text: #5d4e59;
        --muted: #857684;
        --green: #87a98d;
        --amber: #cba25d;
        --red: #c98787;
        --shadow: 0 10px 28px rgba(149, 122, 136, 0.10);
    }

    .stApp {
        background: radial-gradient(circle at top left, #fffdfb 0%, #faf5ef 38%, #f5eee8 100%);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        color: var(--rose) !important;
        letter-spacing: 0.01em;
    }

    p, div, span, label, li, strong, em { color: var(--text); }
    .caption, small, [data-testid="stCaptionContainer"] { color: var(--muted) !important; }

    .hero {
        border: 1px solid var(--rose-border);
        background: linear-gradient(135deg, rgba(255,255,255,0.94), rgba(250,241,246,0.96));
        border-radius: 26px;
        padding: 1.35rem 1.45rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
    }

    .hero-title {
        font-family: 'Cinzel', serif;
        color: var(--rose);
        font-size: 2.05rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .hero-sub {
        color: var(--text);
        font-size: 1.03rem;
        font-weight: 600;
        margin-bottom: 0.35rem;
    }

    .prototype-note {
        border-left: 4px solid var(--rose);
        background: rgba(255, 248, 251, 0.95);
        padding: 0.95rem 1rem;
        border-radius: 16px;
        margin: 0.75rem 0 1rem 0;
        color: var(--text);
        box-shadow: 0 6px 18px rgba(149,122,136,0.08);
    }

    .metric-card,
    [data-testid="stMetric"] {
        border: 1px solid rgba(184,141,162,0.20);
        background: rgba(255,255,255,0.86);
        border-radius: 18px;
        padding: 1rem;
        box-shadow: 0 6px 18px rgba(149,122,136,0.08);
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.76rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        color: var(--rose);
        font-size: 1.65rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .metric-help {
        color: var(--muted);
        font-size: 0.85rem;
        margin-top: 0.45rem;
    }

    .soft-card {
        border: 1px solid rgba(184,141,162,0.20);
        background: rgba(255,255,255,0.88);
        border-radius: 18px;
        padding: 1rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 6px 18px rgba(149,122,136,0.08);
    }



    /* Patch 228: modularized card helpers should behave like stable block-level Streamlit cards. */
    .aletheia-metric-card,
    .aletheia-soft-card {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
        display: block !important;
        overflow-wrap: break-word !important;
        word-break: normal !important;
        white-space: normal !important;
    }

    .aletheia-metric-label,
    .aletheia-metric-help,
    .aletheia-soft-title,
    .aletheia-soft-body {
        max-width: 100% !important;
        overflow-wrap: break-word !important;
        word-break: normal !important;
        white-space: normal !important;
    }

    .aletheia-metric-value {
        max-width: 100% !important;
        overflow-wrap: anywhere !important;
        word-break: normal !important;
        white-space: normal !important;
        font-size: clamp(1.15rem, 2.2vw, 1.65rem) !important;
        line-height: 1.12 !important;
    }

    .aletheia-soft-title {
        color: var(--aletheia-green, #234f31) !important;
        font-weight: 800 !important;
        margin-bottom: 0.35rem !important;
    }

    .aletheia-soft-body {
        color: var(--text, #17324d) !important;
        line-height: 1.45 !important;
    }

    [data-testid="column"] .metric-card,
    [data-testid="column"] .soft-card {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
    }


    /* Patch 229: native Streamlit metric values should not collapse into unreadable ellipses in narrow review columns. */
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        max-width: 100% !important;
        overflow-wrap: anywhere !important;
        word-break: normal !important;
    }

    [data-testid="stMetricValue"] {
        font-size: clamp(1.05rem, 2vw, 1.55rem) !important;
        line-height: 1.12 !important;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 0.45rem; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.80);
        border: 1px solid rgba(184,141,162,0.18);
        border-radius: 999px;
        padding: 0.45rem 0.85rem;
        color: var(--text);
        font-weight: 700;
    }
    .stTabs [aria-selected="true"] {
        border-color: var(--rose) !important;
        color: var(--rose) !important;
        background: rgba(248,236,243,0.98) !important;
    }

    .stButton > button,
    [data-testid="stButton"] button,
    .stDownloadButton > button,
    [data-testid="stDownloadButton"] button,
    [data-testid="stFileUploader"] button {
        background: linear-gradient(180deg, #f7e8ef 0%, #f2dde7 100%) !important;
        color: #6a5663 !important;
        border: 1px solid rgba(184,141,162,0.45) !important;
        border-radius: 14px !important;
        font-weight: 750 !important;
        opacity: 1 !important;
        box-shadow: 0 4px 10px rgba(149,122,136,0.08) !important;
    }

    .stButton > button:hover,
    [data-testid="stButton"] button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stDownloadButton"] button:hover,
    [data-testid="stFileUploader"] button:hover {
        background: linear-gradient(180deg, #f3dbe6 0%, #ecd1dd 100%) !important;
        color: #5a4653 !important;
        border-color: rgba(184,141,162,0.60) !important;
    }

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div,
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"] {
        background: linear-gradient(180deg, #f8f1ea 0%, #f3ebe4 100%) !important;
        border-right: 1px solid rgba(184,141,162,0.18) !important;
    }

    section[data-testid="stSidebar"] *,
    [data-testid="stSidebar"] *,
    [data-testid="stSidebarContent"] * {
        color: var(--text) !important;
    }

    label,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] *,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] * {
        color: var(--text) !important;
    }

    div[data-baseweb="select"] > div,
    textarea,
    input {
        background-color: #fffdfb !important;
        color: #5d4e59 !important;
        border: 1px solid rgba(184,141,162,0.35) !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] *,
    [data-baseweb="popover"] *,
    [role="listbox"] *,
    [role="option"] *,
    textarea::placeholder,
    input::placeholder {
        color: #6b5a67 !important;
        opacity: 1 !important;
    }

    [data-baseweb="popover"],
    [role="listbox"],
    [role="option"] {
        background-color: #fffaf6 !important;
        color: #5d4e59 !important;
    }

    [data-testid="stFileUploader"] section {
        background: rgba(255,255,255,0.85) !important;
        color: var(--text) !important;
        border: 1px dashed rgba(184,141,162,0.35) !important;
        border-radius: 16px !important;
    }

    [data-testid="stMarkdownContainer"] code {
        background: #f8edf2 !important;
        color: #6a5663 !important;
        border: 1px solid rgba(184,141,162,0.25) !important;
        border-radius: 8px !important;
        padding: 0.08rem 0.32rem !important;
        font-weight: 700 !important;
    }

    pre,
    code,
    [data-testid="stCodeBlock"] pre,
    [data-testid="stCodeBlock"] code,
    [data-testid="stCode"] {
        background: #fffdfb !important;
        color: #4e4150 !important;
        border: 1px solid rgba(184,141,162,0.20) !important;
        border-radius: 14px !important;
    }

    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        background: rgba(255,255,255,0.88) !important;
        border-radius: 16px !important;
        overflow: hidden;
        box-shadow: 0 6px 18px rgba(149,122,136,0.08);
    }
    [data-testid="stDataFrame"] *,
    [data-testid="stTable"] * {
        color: #4e4150 !important;
    }

    [data-testid="stExpander"] details {
        background: rgba(255,255,255,0.82);
        border: 1px solid rgba(184,141,162,0.18);
        border-radius: 16px;
        box-shadow: 0 6px 16px rgba(149,122,136,0.06);
    }

    [data-testid="stExpander"] summary {
        color: var(--rose) !important;
        font-weight: 700 !important;
    }

    [data-testid="stInfo"],
    [data-testid="stWarning"],
    [data-testid="stSuccess"],
    [data-testid="stAlert"] {
        border-radius: 16px !important;
        border: 1px solid rgba(184,141,162,0.16) !important;
        box-shadow: 0 4px 12px rgba(149,122,136,0.05) !important;
    }

    [data-testid="stSlider"] [role="slider"] {
        background: var(--rose) !important;
        box-shadow: 0 0 0 4px rgba(184,141,162,0.18) !important;
    }

    [data-testid="stSlider"] div[data-testid="stTickBar"] {
        background: rgba(184,141,162,0.15) !important;
    }

    /* Gentle sidebar tuning panel */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #9d7188 !important;
        letter-spacing: 0.03em !important;
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #8a7b84 !important;
        line-height: 1.65 !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background: #fffdfb !important;
        border: 1px solid rgba(184,141,162,0.28) !important;
        border-radius: 14px !important;
        box-shadow: 0 6px 16px rgba(149,122,136,0.07) !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSlider"] {
        padding: 0.25rem 0 0.55rem 0 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
        background: #bd8ea5 !important;
        border: 2px solid #ead6df !important;
        box-shadow: 0 0 0 4px rgba(184,141,162,0.16) !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"] {
        color: #8e657c !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] hr {
        border: none !important;
        border-top: 1px solid rgba(184,141,162,0.16) !important;
        margin: 1rem 0 0.85rem 0 !important;
    }


    /* Patch 12: botanical civic dashboard shell */
    .block-container {
        max-width: 1180px;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background:
            radial-gradient(circle at 8% 10%, rgba(199,170,114,0.12), transparent 20%),
            radial-gradient(circle at 94% 92%, rgba(142,161,144,0.14), transparent 23%);
        z-index: 0;
    }

    .botanical-frame {
        position: relative;
        border: 1px solid rgba(199,170,114,0.42);
        background: linear-gradient(135deg, rgba(255,253,250,0.96), rgba(248,241,234,0.94));
        border-radius: 28px;
        padding: 1.45rem 1.65rem;
        margin: 0.45rem 0 1rem 0;
        box-shadow: 0 14px 34px rgba(93,78,89,0.10);
        overflow: hidden;
    }

    .botanical-frame::before,
    .botanical-frame::after {
        position: absolute;
        color: rgba(142,161,144,0.72);
        font-size: 2.2rem;
        line-height: 1;
    }
    .botanical-frame::before { content: "❧"; top: 0.45rem; left: 0.75rem; }
    .botanical-frame::after { content: "❦"; right: 0.85rem; bottom: 0.45rem; }

    .hero {
        border: 0;
        background: transparent;
        border-radius: 0;
        padding: 0;
        margin-bottom: 0;
        box-shadow: none;
    }

    .hero-grid {
        display: grid;
        grid-template-columns: minmax(0, 1fr) auto;
        gap: 1rem;
        align-items: center;
    }

    .hero-title {
        font-size: clamp(2.4rem, 5.8vw, 4.6rem);
        letter-spacing: 0.15em;
        line-height: 0.95;
        color: #3c2438 !important;
        text-shadow: 0 1px 0 rgba(255,255,255,0.8);
    }

    .hero-sub {
        color: #53634f !important;
        font-family: Georgia, serif;
        font-size: 1.18rem;
        font-weight: 500;
        letter-spacing: 0.03em;
    }

    .hero-kicker {
        color: #9f6d3f !important;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        font-size: 0.78rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
    }

    .hero-emblem {
        width: 118px;
        height: 118px;
        border-radius: 999px;
        display: flex;
        align-items: center;
        justify-content: center;
        background:
            radial-gradient(circle at 50% 42%, rgba(255,255,255,0.95), rgba(244,229,216,0.92)),
            linear-gradient(135deg, rgba(199,170,114,0.26), rgba(142,161,144,0.18));
        border: 1px solid rgba(199,170,114,0.55);
        box-shadow: inset 0 0 0 8px rgba(255,255,255,0.38), 0 10px 24px rgba(93,78,89,0.10);
        font-size: 3.4rem;
        overflow: hidden;
    }
    .aletheia-mascot-logo {
        width: 92%;
        height: 92%;
        object-fit: cover;
        border-radius: 999px;
        display: block;
    }

    .civic-ribbon {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.5rem;
        border: 1px solid rgba(199,170,114,0.30);
        background: rgba(255,253,250,0.70);
        border-radius: 18px;
        padding: 0.65rem;
        margin-top: 1rem;
    }

    .ribbon-item {
        display: flex;
        gap: 0.55rem;
        align-items: center;
        padding: 0.55rem 0.65rem;
        border-right: 1px solid rgba(199,170,114,0.22);
    }
    .ribbon-item:last-child { border-right: 0; }
    .ribbon-icon { font-size: 1.45rem; color: #7d8f76; }
    .ribbon-label { font-family: 'Cinzel', serif; color: #3c2438; font-weight: 700; letter-spacing: 0.04em; }
    .ribbon-body { color: #6c615c; font-size: 0.86rem; line-height: 1.25; }

    .prototype-note {
        border-left: 0;
        border: 1px solid rgba(199,170,114,0.28);
        background: linear-gradient(135deg, rgba(255,249,244,0.92), rgba(250,239,233,0.88));
        border-radius: 20px;
        color: #4f4547;
    }

    .metric-card,
    .soft-card,
    [data-testid="stMetric"] {
        border-color: rgba(199,170,114,0.28);
        background: linear-gradient(180deg, rgba(255,253,250,0.94), rgba(250,245,239,0.90));
    }

    section[data-testid="stSidebar"] {
        width: 21rem !important;
    }

    .sidebar-emblem-card {
        text-align: center;
        border: 1px solid rgba(199,170,114,0.34);
        background: linear-gradient(180deg, rgba(255,253,250,0.96), rgba(246,238,229,0.94));
        border-radius: 24px;
        padding: 1rem 0.8rem 1.05rem;
        margin: 0.35rem 0 1rem;
        box-shadow: 0 12px 26px rgba(93,78,89,0.09);
    }
    .sidebar-emblem-mark {
        width: 126px;
        height: 126px;
        margin: 0 auto 0.65rem;
        border-radius: 999px;
        display: flex;
        align-items: center;
        justify-content: center;
        background:
            radial-gradient(circle at 50% 38%, rgba(255,255,255,0.96), rgba(242,226,212,0.92)),
            linear-gradient(135deg, rgba(199,170,114,0.24), rgba(142,161,144,0.22));
        border: 1px solid rgba(199,170,114,0.58);
        box-shadow: inset 0 0 0 10px rgba(255,255,255,0.34);
        font-size: 3.35rem;
        overflow: hidden;
    }
    .sidebar-brand {
        font-family: 'Cinzel', serif;
        color: #3c2438 !important;
        letter-spacing: 0.18em;
        font-size: 1.45rem;
        font-weight: 700;
        margin-top: 0.1rem;
    }
    .sidebar-tagline {
        color: #53634f !important;
        font-family: Georgia, serif;
        font-size: 0.98rem;
        margin-top: 0.2rem;
    }
    .sidebar-note-card {
        border: 1px solid rgba(199,170,114,0.28);
        background: rgba(255,253,250,0.72);
        border-radius: 18px;
        padding: 0.8rem 0.85rem;
        margin-top: 0.85rem;
        font-family: Georgia, serif;
    }

    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(180deg, #7f9179 0%, #657962 100%) !important;
        color: #fffdf8 !important;
        border-color: rgba(101,121,98,0.52) !important;
        border-radius: 16px !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-color: rgba(199,170,114,0.28);
        background: rgba(255,253,250,0.78);
        color: #4e414e;
        font-family: Georgia, serif;
        font-weight: 700;
    }
    .stTabs [aria-selected="true"] {
        border-color: rgba(101,121,98,0.72) !important;
        color: #53634f !important;
        background: rgba(235,242,231,0.96) !important;
        box-shadow: 0 8px 18px rgba(101,121,98,0.10) !important;
    }

    /* Patch 202 — Streamlit tab containment rollback.
       The earlier :has()/nth-of-type containment guard could make nested or
       main tab panels render as one long continuous page in some browser /
       Streamlit combinations, especially after Stress Test interactions.
       Keep only a narrow native-hidden-panel rule and let Streamlit manage
       the active tab state. */
    .stTabs [role="tabpanel"][hidden],
    .stTabs [data-baseweb="tab-panel"][hidden] {
        display: none !important;
    }


    .stButton > button,
    [data-testid="stButton"] button,
    .stDownloadButton > button,
    [data-testid="stDownloadButton"] button {
        background: linear-gradient(180deg, #778970 0%, #63765e 100%) !important;
        color: #fffdf8 !important;
        border-color: rgba(99,118,94,0.55) !important;
        box-shadow: 0 7px 16px rgba(83,99,79,0.16) !important;
    }

    .stButton > button:hover,
    [data-testid="stButton"] button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stDownloadButton"] button:hover {
        background: linear-gradient(180deg, #84987b 0%, #6d8067 100%) !important;
        color: #fffdf8 !important;
    }

    .footer-banner {
        border: 1px solid rgba(199,170,114,0.35);
        background: linear-gradient(135deg, rgba(255,249,244,0.94), rgba(248,234,229,0.90));
        border-radius: 22px;
        padding: 0.9rem 1rem;
        margin-top: 1.25rem;
        text-align: center;
        color: #4f4547;
        box-shadow: 0 10px 24px rgba(93,78,89,0.08);
    }
    .footer-banner strong { color: #3c2438 !important; font-family: 'Cinzel', serif; letter-spacing: 0.06em; }



    /* Patch 181: original ALETHEIA warm civic visual theme override.
       Visual shell only: no scoring, receipt, routing, taxonomy, or protocol behavior. */
    :root {
        --bg: #eaf7ff;
        --bg-soft: #f5fbff;
        --panel: rgba(255,255,255,0.94);
        --panel-strong: rgba(255,255,255,0.985);
        --sky: #d8f0ff;
        --sky-deep: #7fbce8;
        --sky-line: rgba(87, 158, 212, 0.32);
        --gold: #d4af37;
        --gold-soft: rgba(212,175,55,0.18);
        --gold-border: rgba(212,175,55,0.46);
        --pillar: #ffffff;
        --text: #17324a;
        --muted: #577086;
        --rose: #1f5f8f;
        --rose-soft: rgba(127,188,232,0.18);
        --rose-border: rgba(87,158,212,0.26);
        --sage: #76a8c8;
        --green: #4f9f8e;
        --amber: #b8870b;
        --red: #b94b4b;
        --shadow: 0 16px 38px rgba(31, 95, 143, 0.13);
    }

    .stApp {
        background:
            radial-gradient(circle at 14% 6%, rgba(255,255,255,0.96) 0%, rgba(255,255,255,0) 26%),
            radial-gradient(circle at 88% 4%, rgba(212,175,55,0.16) 0%, rgba(212,175,55,0) 24%),
            linear-gradient(180deg, #dff3ff 0%, #eef9ff 38%, #ffffff 100%);
        color: var(--text);
    }

    h1, h2, h3 {
        color: #164d78 !important;
        text-shadow: 0 1px 0 rgba(255,255,255,0.75);
    }

    .botanical-frame {
        border: 1px solid var(--gold-border);
        background:
            linear-gradient(90deg, rgba(255,255,255,0.18), rgba(255,255,255,0) 10%, rgba(255,255,255,0) 90%, rgba(255,255,255,0.18)),
            linear-gradient(135deg, rgba(255,255,255,0.98), rgba(236,248,255,0.94));
        box-shadow: var(--shadow), inset 0 0 0 1px rgba(255,255,255,0.78);
    }

    .botanical-frame::before,
    .botanical-frame::after {
        content: "";
        top: 0.9rem;
        bottom: 0.9rem;
        width: 18px;
        border-radius: 999px;
        background:
            linear-gradient(180deg, rgba(255,255,255,1), rgba(246,251,255,0.96)),
            repeating-linear-gradient(90deg, rgba(255,255,255,0.0), rgba(255,255,255,0.0) 3px, rgba(126,185,225,0.10) 4px);
        border: 1px solid rgba(212,175,55,0.36);
        box-shadow:
            inset 0 0 0 3px rgba(255,255,255,0.72),
            0 8px 18px rgba(31,95,143,0.10);
        font-size: 0;
        line-height: 0;
    }
    .botanical-frame::before { left: 0.75rem; }
    .botanical-frame::after { right: 0.75rem; }

    .hero-grid { padding: 0.1rem 2.15rem; }
    .hero-title {
        color: #123d63 !important;
        text-shadow: 0 2px 0 rgba(255,255,255,0.86), 0 0 18px rgba(127,188,232,0.28);
    }
    .hero-title-main,
    .hero-title-subline,
    .sidebar-brand-main,
    .sidebar-brand-subline {
        display: block;
    }
    .hero-title-subline,
    .sidebar-brand-subline {
        margin-top: 0.06em;
    }
    .hero-emblem .aletheia-mascot-logo {
        /* Patch 190: original governance-mirror logo; no STOP / GO officer framing. */
        transform: none;
    }
    .hero-sub { color: #2d668f !important; }
    .hero-kicker { color: #9a720d !important; }
    .hero-emblem,
    .sidebar-emblem-mark {
        background:
            radial-gradient(circle at 50% 42%, rgba(255,255,255,0.98), rgba(225,244,255,0.94)),
            linear-gradient(135deg, rgba(212,175,55,0.26), rgba(127,188,232,0.28));
        border: 1px solid var(--gold-border);
        box-shadow: inset 0 0 0 9px rgba(255,255,255,0.44), 0 14px 28px rgba(31,95,143,0.14);
    }

    .civic-ribbon,
    .prototype-note,
    .sidebar-emblem-card,
    .footer-banner,
    .metric-card,
    .soft-card,
    [data-testid="stMetric"] {
        border-color: var(--gold-border) !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(240,249,255,0.90)) !important;
        box-shadow: 0 10px 26px rgba(31,95,143,0.10) !important;
    }

    .prototype-note {
        border-left: 5px solid var(--gold) !important;
    }

    .ribbon-label,
    .sidebar-brand,
    .footer-banner strong {
        color: #123d63 !important;
    }
    .ribbon-icon,
    .sidebar-tagline,
    .ribbon-body {
        color: #2d668f !important;
    }

    div[data-testid="stExpander"] {
        border: 1px solid rgba(212,175,55,0.32) !important;
        border-radius: 18px !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.97), rgba(244,251,255,0.92)) !important;
        box-shadow: 0 8px 20px rgba(31,95,143,0.08) !important;
        overflow: hidden;
    }
    div[data-testid="stExpander"] details summary {
        color: #164d78 !important;
        font-weight: 800 !important;
    }
    div[data-testid="stExpander"] details summary::marker { color: var(--gold); }

    .stButton > button,
    [data-testid="stButton"] button,
    .stDownloadButton > button,
    [data-testid="stDownloadButton"] button {
        border: 1px solid rgba(212,175,55,0.62) !important;
        background: linear-gradient(180deg, #ffffff 0%, #eaf7ff 100%) !important;
        color: #123d63 !important;
        box-shadow: 0 8px 18px rgba(31,95,143,0.10) !important;
    }
    .stButton > button:hover,
    [data-testid="stButton"] button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stDownloadButton"] button:hover {
        background: linear-gradient(180deg, #f8fbff 0%, #d9efff 100%) !important;
        color: #0f3556 !important;
        border-color: rgba(212,175,55,0.82) !important;
    }
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(180deg, #d8b648 0%, #b98c14 100%) !important;
        border-color: #8f6908 !important;
        color: #ffffff !important;
        box-shadow: 0 10px 22px rgba(154,114,13,0.25) !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(230,246,255,0.96), rgba(255,255,255,0.96)) !important;
        border-right: 1px solid rgba(212,175,55,0.26) !important;
    }

    .footer-banner {
        color: #17324a !important;
    }



    /* Patch 182: ALETHEIA warm civic module alignment pass.
       Visual/copy anchor only for Protocol Guide, Why ALETHEIA, Evidence Lab, and subordinate AI Integrity panels. */
    .sky-gold-page-anchor {
        border: 1px solid rgba(212,175,55,0.42);
        border-left: 6px solid var(--gold);
        border-radius: 20px;
        padding: 0.9rem 1rem 0.85rem 1rem;
        margin: 0.35rem 0 1rem 0;
        background:
            linear-gradient(90deg, rgba(255,255,255,0.98), rgba(239,249,255,0.94)),
            radial-gradient(circle at 96% 14%, rgba(212,175,55,0.14), rgba(212,175,55,0));
        box-shadow: 0 10px 24px rgba(31,95,143,0.10);
    }
    .sky-gold-page-anchor strong {
        color: #123d63;
        letter-spacing: 0.02em;
    }
    .sky-gold-page-anchor span {
        color: #577086;
    }
    .sky-gold-page-anchor .sky-gold-rule {
        display: block;
        width: 96px;
        height: 3px;
        margin: 0.45rem 0 0.5rem 0;
        border-radius: 999px;
        background: linear-gradient(90deg, var(--gold), rgba(127,188,232,0.62));
    }
    .sky-gold-page-anchor .pillar-pair {
        display: inline-block;
        width: 28px;
        height: 18px;
        margin-right: 0.45rem;
        vertical-align: -3px;
        background:
            linear-gradient(90deg, rgba(255,255,255,1) 0 38%, transparent 38% 62%, rgba(255,255,255,1) 62% 100%);
        border-top: 1px solid rgba(212,175,55,0.42);
        border-bottom: 1px solid rgba(212,175,55,0.42);
        filter: drop-shadow(0 3px 5px rgba(31,95,143,0.08));
    }
    div[data-testid="stExpander"] details[open] {
        background: linear-gradient(180deg, rgba(255,255,255,0.99), rgba(246,252,255,0.96));
    }
    div[data-testid="stExpander"] p,
    div[data-testid="stExpander"] li,
    div[data-testid="stExpander"] td {
        color: #27465f;
    }
    div[data-testid="stExpander"] blockquote {
        border-left: 4px solid var(--gold) !important;
        background: rgba(216,240,255,0.34);
        color: #17324a;
    }
    div[data-testid="stExpander"] table {
        border: 1px solid rgba(127,188,232,0.24);
        border-radius: 12px;
        overflow: hidden;
    }
    div[data-testid="stExpander"] th {
        background: rgba(216,240,255,0.48) !important;
        color: #123d63 !important;
        border-bottom: 1px solid rgba(212,175,55,0.30) !important;
    }
    div[data-testid="stExpander"] hr {
        border-color: rgba(212,175,55,0.28) !important;
    }



    /* Patch 183: receipt visual styling pass.
       Visual-only framing for local witness receipts and World Lens receipt downloads; no receipt schema or scoring changes. */
    .receipt-sky-panel {
        border: 1px solid rgba(212,175,55,0.46);
        border-left: 6px solid var(--gold);
        border-radius: 22px;
        padding: 1rem 1.05rem;
        margin: 0.65rem 0 0.9rem 0;
        background:
            linear-gradient(90deg, rgba(255,255,255,0.99), rgba(236,248,255,0.96)),
            radial-gradient(circle at 96% 8%, rgba(212,175,55,0.16), rgba(212,175,55,0));
        box-shadow: 0 12px 28px rgba(31,95,143,0.11), inset 0 0 0 1px rgba(255,255,255,0.72);
        position: relative;
        overflow: hidden;
    }
    .receipt-sky-panel::before,
    .receipt-sky-panel::after {
        content: "";
        position: absolute;
        top: 0.82rem;
        bottom: 0.82rem;
        width: 11px;
        border-radius: 999px;
        background: linear-gradient(180deg, #ffffff, #f4fbff);
        border: 1px solid rgba(212,175,55,0.30);
        box-shadow: inset 0 0 0 2px rgba(255,255,255,0.72), 0 6px 14px rgba(31,95,143,0.08);
    }
    .receipt-sky-panel::before { right: 2.25rem; }
    .receipt-sky-panel::after { right: 0.92rem; }
    .receipt-kicker {
        color: #9a720d !important;
        font-size: 0.72rem;
        font-weight: 900;
        letter-spacing: 0.095em;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }
    .receipt-title {
        color: #123d63 !important;
        font-weight: 900;
        font-size: 1.08rem;
        margin-bottom: 0.2rem;
    }
    .receipt-body {
        color: #355d7a !important;
        max-width: 78ch;
        line-height: 1.55;
    }
    .receipt-boundary-strip {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 0.7rem;
    }
    .receipt-boundary-pill {
        border: 1px solid rgba(127,188,232,0.34);
        background: rgba(255,255,255,0.78);
        border-radius: 999px;
        padding: 0.22rem 0.58rem;
        color: #17496f !important;
        font-size: 0.78rem;
        font-weight: 800;
    }
    .receipt-hash-pill {
        border-color: rgba(212,175,55,0.42);
        color: #8a650a !important;
    }
    .receipt-download-note {
        border: 1px dashed rgba(212,175,55,0.42);
        border-radius: 18px;
        padding: 0.74rem 0.9rem;
        background: rgba(255,255,255,0.68);
        color: #355d7a !important;
        margin: 0.4rem 0 0.65rem 0;
    }
    .receipt-code-frame {
        border: 1px solid rgba(212,175,55,0.36);
        border-radius: 20px;
        padding: 0.78rem 0.9rem;
        margin: 0.65rem 0 0.6rem 0;
        background: linear-gradient(180deg, rgba(255,255,255,0.94), rgba(239,249,255,0.88));
        box-shadow: 0 9px 22px rgba(31,95,143,0.09);
    }
    .receipt-code-frame strong { color: #123d63 !important; }
    [data-testid="stCodeBlock"] {
        border: 1px solid rgba(212,175,55,0.30) !important;
        border-radius: 18px !important;
        box-shadow: 0 8px 18px rgba(31,95,143,0.08) !important;
    }



    /* Patch 192: original poster-style warm governance-mirror app polish.
       Visual-only overrides: warm parchment/cream surfaces, muted green/red accents,
       botanical/public-good tone, and no blue preview/card dominance. */
    :root {
        --aletheia-cream: #fbf6ea;
        --aletheia-parchment: #f6eddb;
        --aletheia-green: #355c2b;
        --aletheia-green-soft: rgba(84, 111, 62, 0.16);
        --aletheia-red: #b23a42;
        --aletheia-red-soft: rgba(178, 58, 66, 0.13);
        --aletheia-ink: #35291d;
        --aletheia-muted: #756756;
        --aletheia-line: rgba(151, 124, 75, 0.34);
    }

    .stApp {
        background:
            radial-gradient(circle at 12% 4%, rgba(178, 58, 66, 0.05), rgba(178, 58, 66, 0) 32%),
            radial-gradient(circle at 88% 8%, rgba(84, 111, 62, 0.10), rgba(84, 111, 62, 0) 31%),
            linear-gradient(180deg, #fffaf1 0%, var(--aletheia-cream) 48%, #f3ead8 100%) !important;
        color: var(--aletheia-ink) !important;
    }

    h1, h2, h3,
    .hero-title,
    .sidebar-brand-main,
    .sidebar-brand-subline {
        font-family: Georgia, 'Times New Roman', serif !important;
    }

    .hero-title-main,
    .sidebar-brand-main {
        color: var(--aletheia-red) !important;
        text-shadow: 0 1px 0 rgba(255,255,255,0.82) !important;
    }
    .hero-title-subline,
    .sidebar-brand-subline,
    .hero-sub,
    .ribbon-label,
    .footer-banner strong,
    .sky-gold-page-anchor strong,
    .receipt-title {
        color: var(--aletheia-green) !important;
    }
    .hero-kicker,
    .caption,
    .ribbon-body,
    .sidebar-tagline,
    .sky-gold-page-anchor span,
    .receipt-body,
    .receipt-download-note,
    [data-testid="stCaptionContainer"] {
        color: var(--aletheia-muted) !important;
    }

    .botanical-frame,
    .hero,
    .civic-ribbon,
    .prototype-note,
    .sidebar-emblem-card,
    .footer-banner,
    .metric-card,
    .soft-card,
    [data-testid="stMetric"],
    div[data-testid="stExpander"],
    .sky-gold-page-anchor,
    .receipt-sky-panel,
    .receipt-code-frame {
        border-color: var(--aletheia-line) !important;
        background:
            linear-gradient(180deg, rgba(255, 250, 241, 0.98), rgba(246, 237, 219, 0.92)) !important;
        box-shadow: 0 10px 24px rgba(94, 74, 41, 0.10) !important;
    }

    .botanical-frame::before,
    .botanical-frame::after {
        background:
            radial-gradient(circle at 50% 28%, rgba(84,111,62,0.28), rgba(84,111,62,0) 35%),
            linear-gradient(135deg, rgba(178,58,66,0.12), rgba(246,237,219,0.22)) !important;
        border-color: rgba(151, 124, 75, 0.32) !important;
    }

    .prototype-note,
    .sky-gold-page-anchor,
    .receipt-sky-panel {
        border-left-color: var(--aletheia-red) !important;
    }

    .hero-emblem,
    .sidebar-emblem-mark {
        background:
            radial-gradient(circle at 50% 42%, rgba(255, 252, 246, 0.98), rgba(246, 237, 219, 0.92)),
            linear-gradient(135deg, rgba(84,111,62,0.16), rgba(178,58,66,0.10)) !important;
        border-color: var(--aletheia-line) !important;
        box-shadow: inset 0 0 0 9px rgba(255,255,255,0.38), 0 14px 28px rgba(94, 74, 41, 0.12) !important;
    }

    .sky-gold-page-anchor .sky-gold-rule {
        background: linear-gradient(90deg, var(--aletheia-red), var(--aletheia-green)) !important;
    }
    .sky-gold-page-anchor .pillar-pair {
        border-top-color: rgba(151, 124, 75, 0.40) !important;
        border-bottom-color: rgba(151, 124, 75, 0.40) !important;
        filter: drop-shadow(0 3px 5px rgba(94, 74, 41, 0.08)) !important;
    }

    .stButton > button,
    [data-testid="stButton"] button,
    .stDownloadButton > button,
    [data-testid="stDownloadButton"] button,
    [data-testid="stFileUploader"] button {
        border: 1px solid rgba(151, 124, 75, 0.45) !important;
        background: linear-gradient(180deg, #fffaf1 0%, #efe3cc 100%) !important;
        color: var(--aletheia-green) !important;
        box-shadow: 0 8px 18px rgba(94, 74, 41, 0.10) !important;
    }
    .stButton > button:hover,
    [data-testid="stButton"] button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stDownloadButton"] button:hover,
    [data-testid="stFileUploader"] button:hover {
        background: linear-gradient(180deg, #fff6e7 0%, #e7d9bd 100%) !important;
        color: #274a20 !important;
        border-color: rgba(151, 124, 75, 0.65) !important;
    }
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(180deg, #b23a42 0%, #8f2830 100%) !important;
        border-color: #742127 !important;
        color: #fffaf1 !important;
        box-shadow: 0 10px 22px rgba(143, 40, 48, 0.22) !important;
    }

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div,
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"] {
        background: linear-gradient(180deg, #fff7e8 0%, #f3ead8 100%) !important;
        border-right: 1px solid var(--aletheia-line) !important;
    }

    div[data-testid="stExpander"] details[open],
    div[data-testid="stExpander"],
    [data-testid="stFileUploader"] section,
    div[data-baseweb="select"] > div,
    textarea,
    input,
    pre,
    code,
    [data-testid="stCodeBlock"] pre,
    [data-testid="stCodeBlock"] code,
    [data-testid="stCode"] {
        background-color: #fffaf1 !important;
        border-color: var(--aletheia-line) !important;
        color: var(--aletheia-ink) !important;
    }

    div[data-testid="stExpander"] p,
    div[data-testid="stExpander"] li,
    div[data-testid="stExpander"] td,
    div[data-testid="stExpander"] details summary,
    [data-testid="stMarkdownContainer"] code,
    .receipt-boundary-pill,
    .receipt-code-frame strong {
        color: var(--aletheia-green) !important;
    }

    div[data-testid="stExpander"] blockquote,
    div[data-testid="stExpander"] th,
    .receipt-boundary-pill,
    .receipt-download-note {
        background: var(--aletheia-green-soft) !important;
        border-color: rgba(84, 111, 62, 0.26) !important;
    }

    .receipt-sky-panel::before,
    .receipt-sky-panel::after {
        background: linear-gradient(180deg, #fffaf1, #efe3cc) !important;
        border-color: var(--aletheia-line) !important;
        box-shadow: inset 0 0 0 2px rgba(255,255,255,0.62), 0 6px 14px rgba(94, 74, 41, 0.08) !important;
    }

    @media (max-width: 900px) {
        .hero-grid { grid-template-columns: 1fr; }
        .hero-emblem { display: none; }
        .civic-ribbon { grid-template-columns: 1fr; }
        .ribbon-item { border-right: 0; border-bottom: 1px solid rgba(199,170,114,0.18); }
        .ribbon-item:last-child { border-bottom: 0; }
    }

    </style>
"""


def apply_app_page_config_and_theme(container=None) -> None:
    """Apply the global Streamlit page config and ALETHEIA CSS theme.

    Patch 260 moves app-level page setup and the large global CSS block out of
    ``app.py`` so the entrypoint can keep becoming a thin orchestrator. This is
    shell rendering only: it does not read inputs, mutate session state, route
    modules, run analysis, change scoring, or alter receipt behavior.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.set_page_config(page_title="ALETHEIA", page_icon="🌿", layout="wide")
    container.markdown(ALETHEIA_GLOBAL_CSS, unsafe_allow_html=True)


def render_app_boundary_notices(supported_input_language_note: str, container=None) -> None:
    """Render the stable top-of-app boundary notices.

    ``container`` may be ``st`` or any object exposing ``markdown``. Streamlit
    is imported lazily so tests can import this helper without opening a UI
    runtime.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown(
        f"""
        <div class="prototype-note">
            <strong>Input language scope:</strong> {supported_input_language_note}
        </div>
        """,
        unsafe_allow_html=True,
    )

    container.markdown(
        """
        <div class="prototype-note">
            <strong>Plain words:</strong> ALETHEIA uses mirror-review language for humans. Sanctuary means low risk inside this prototype, not final safety. Threshold means review and repair. Asylum means high capture or harm pressure. The Z-axis stops at the human/system boundary; a receipt is your local record of what was reviewed.
        </div>
        """,
        unsafe_allow_html=True,
    )

    container.markdown(
        """
        <div class="prototype-note">
            <strong>Privacy by design:</strong> This repository includes no telemetry, trackers, analytics SDKs, backend upload endpoint, public ledger sync, Global ID sync, or central user-input database. Inputs are processed in the running app session; receipts are user-held downloads. Hosting providers may still have their own server logs.
        </div>
        """,
        unsafe_allow_html=True,
    )



def render_app_header(mascot_logo_uri: str, app_version: str, container=None) -> None:
    """Render the stable public header/hero block.

    This is static shell copy only. It does not read or write session state,
    run analysis, alter navigation, or change scoring/receipt behavior.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown(
        f"""
        <div class="botanical-frame hero">
            <div class="hero-grid">
                <div>
                    <div class="hero-kicker">Free · Open Source · Human Review Required</div>
                    <div class="hero-title"><span class="hero-title-main">ALETHEIA</span><span class="hero-title-subline">GOVERNANCE MIRROR</span></div>
                    <div class="hero-sub">Protocol-guided audit and simulation framework for human review.</div>
                    <div class="caption">Audit · Simulation · Evidence · Global comparison · Reports · English-first; Dutch batch-test examples only · Protect people. Keep truth visible.</div>
                </div>
                <div class="hero-emblem" aria-hidden="true"><img class="aletheia-mascot-logo" src="{mascot_logo_uri}" alt="" /></div>
            </div>
            <div class="civic-ribbon">
                <div class="ribbon-item"><span class="ribbon-icon">🛡️</span><div><div class="ribbon-label">Purpose</div><div class="ribbon-body">Protect people. Keep review human.</div></div></div>
                <div class="ribbon-item"><span class="ribbon-icon">📋</span><div><div class="ribbon-label">Method</div><div class="ribbon-body">Reflect pressure. Keep appeal open.</div></div></div>
                <div class="ribbon-item"><span class="ribbon-icon">🪞</span><div><div class="ribbon-label">Boundary</div><div class="ribbon-body">ALETHEIA reflects. People decide. It never rules, certifies, commands, or replaces people.</div></div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_how_to_use_note(container=None) -> None:
    """Render the stable first-use note under the header.

    This helper keeps static public copy outside ``app.py`` while preserving
    behavior. It does not collect inputs, route modules, or run analysis.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown(
        """
        <div class="prototype-note">
            <strong>How to use this:</strong> Paste an idea. ALETHEIA looks for power, pressure, appeal, and risk. It offers a mirror reading for review, and you keep the final say. It is not legal, medical, political, religious, or official advice.
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar_brand(mascot_logo_uri: str, container=None) -> None:
    """Render the stable sidebar identity card.

    This is static shell copy only. It does not read or write session state,
    run analysis, or alter scoring/receipt behavior.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown(
        f"""
        <div class="sidebar-emblem-card">
            <div class="sidebar-emblem-mark"><img class="aletheia-mascot-logo" src="{mascot_logo_uri}" alt="" /></div>
            <div class="sidebar-brand"><span class="sidebar-brand-main">ALETHEIA</span><span class="sidebar-brand-subline">Governance Mirror</span></div>
            <div class="sidebar-tagline">Free open-source governance mirror. Mirror, not throne.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_context(container=None) -> None:
    """Render stable sidebar context above interactive controls.

    The sidebar context explains the review lens, calibrated language scope,
    and application-code privacy boundary. Interactive control state remains in
    ``app.py`` so Patch 109 stays a shell extraction rather than a behavior
    refactor.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.header("Reading controls")
    container.caption("Choose how alert the mirror lens should be to pressure, trust, and fit.")
    container.caption("Input scope: English-first. Dutch/Nederlands examples may be used for batch testing, not as a general app-wide compatibility claim.")
    container.caption(
        "Privacy boundary: no built-in telemetry, trackers, analytics SDKs, backend upload endpoint, "
        "public ledger sync, Global ID sync, or central user-input database."
    )


def render_sidebar_review_lens_intro(container=None) -> None:
    """Render the static Review lens sidebar section heading and note.

    Interactive preset selection remains in ``app.py``. This helper only
    renders copy for the gradual app-shell refactor.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown("#### Review lens")


def render_sidebar_review_lens_note(container=None) -> None:
    """Render the static note below the Review lens selector."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.caption("This only sets the mirror lens. ALETHEIA waits for your idea.")


def render_sidebar_review_rhythm_intro(container=None) -> None:
    """Render the static Review rhythm sidebar section boundary."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown("---")
    container.markdown("#### Review rhythm")


def render_sidebar_review_rhythm_note(container=None) -> None:
    """Render the static note below the Review rhythm sliders."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.caption("The mirror keeps voices small so the pattern is easy to read. The 9k view lives in World Lens.")


def render_sidebar_safety_rails_intro(container=None) -> None:
    """Render the static Safety rails sidebar section boundary."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown("---")
    container.markdown("#### Safety rails")


def render_sidebar_safety_rails_note(container=None) -> None:
    """Render the static note below the Safety rails sliders."""
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.caption("Gentle voice, firm review rails. These settings change the reading, not the boundary.")

def render_app_footer_banner(app_version: str, container=None) -> None:
    """Render the stable footer banner.

    This is static shell copy only. It does not read or write session state,
    route modules, run analysis, alter scoring, or change receipt behavior.
    """
    if container is None:
        import streamlit as st  # type: ignore

        container = st

    container.markdown(
        f"""<div class="footer-banner"><strong>ALETHEIA reflects.</strong> People decide. · Free/open-source governance mirror · Mirror, not throne.</div>""",
        unsafe_allow_html=True,
    )

