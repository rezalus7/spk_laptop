import streamlit as st

def inject():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

    :root {
        --bg:       #080c14;
        --surface:  #0f1522;
        --card:     #141d2e;
        --border:   #1e2d45;
        --accent:   #3b82f6;
        --accent2:  #06b6d4;
        --green:    #22c55e;
        --yellow:   #eab308;
        --red:      #ef4444;
        --text:     #e2e8f0;
        --muted:    #64748b;
        --soft:     #94a3b8;
    }

    /* ── FIX BACKGROUND PUTIH STREAMLIT ── */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"], .main {
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    
    /* Memastikan teks bawaan di dalam container berwarna terang */
    [data-testid="stAppViewContainer"] p, 
    [data-testid="stAppViewContainer"] span, 
    [data-testid="stAppViewContainer"] label {
        color: var(--text);
    }

    /* ── Sembunyikan Navigasi & Header Bawaan Total ── */
    #MainMenu, footer, header, [data-testid="stHeader"] { 
        display: none !important;
        visibility: hidden !important; 
    }
    [data-testid="stDecoration"] { display: none !important; }
    .block-container { padding-top: 2rem !important; }

    /* Sembunyikan paksa tombol bawaan collapse Streamlit (<<) agar tidak merusak layout */
    [data-testid="stSidebarCollapsedControl"], 
    button[aria-label="Collapse sidebar"],
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* ── Kustomisasi Sidebar Gelap ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1120 0%, #080c14 100%) !important;
        border-right: 1px solid rgba(59,130,246,0.1) !important;
    }
    [data-testid="stSidebar"] * { color: var(--text) !important; }

    /* ── Kustomisasi Style untuk Tombol Menu Toggle ── */
    div.element-container:has(button[key="menu_toggle_btn"]) {
        position: fixed;
        top: 16px;
        left: 16px;
        z-index: 999999;
    }

    /* ── Native buttons (all variants) ── */
    .stButton > button {
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        height: 44px !important;
        transition: all .15s ease !important;
        border: none !important;
    }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background: var(--accent) !important;
        color: #fff !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(59,130,246,.25) !important;
    }
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="baseButton-secondary"] {
        background: var(--card) !important;
        color: var(--soft) !important;
        border: 1px solid var(--border) !important;
    }
    .stButton > button[kind="secondary"]:hover {
        border-color: var(--accent) !important;
        color: var(--accent) !important;
    }

    /* ── Text inputs ── */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input {
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 8px !important;
        height: 44px !important;
        font-size: 14px !important;
    }
    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(59,130,246,.15) !important;
    }
    [data-testid="stTextInput"] label,
    [data-testid="stNumberInput"] label,
    [data-testid="stSelectbox"] label { color: var(--soft) !important; font-size: 13px !important; }

    /* ── Selectbox ── */
    [data-testid="stSelectbox"] > div > div {
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 8px !important;
    }

    /* ── Sliders ── */
    [data-testid="stSlider"] label { color: var(--soft) !important; font-size: 13px !important; }
    [data-testid="stSlider"] [data-testid="stThumbValue"] { color: var(--accent) !important; }

    /* ── Tabs ── */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        background: var(--surface) !important;
        border-radius: 10px !important;
        padding: 4px !important;
        gap: 4px !important;
        border: 1px solid var(--border) !important;
    }
    [data-testid="stTabs"] [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--muted) !important;
        border-radius: 7px !important;
        font-weight: 500 !important;
        font-size: 13px !important;
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        background: var(--accent) !important;
        color: #fff !important;
    }

    /* ── Forms ── */
    [data-testid="stForm"] {
        background: rgba(20,29,46,0.8) !important;
        border: 1px solid rgba(59,130,246,0.12) !important;
        border-radius: 20px !important;
        padding: 28px 24px !important;
        backdrop-filter: blur(16px) !important;
        box-shadow: 0 20px 60px rgba(0,0,0,0.35) !important;
    }

    /* ── Custom table ── */
    .spk-table-wrap { overflow-x: auto; border-radius: 10px; border: 1px solid var(--border); margin-top: 14px; }
    .spk-table { width: 100%; border-collapse: collapse; font-size: 13px; }
    .spk-table th {
        background: var(--surface); color: var(--accent);
        padding: 11px 14px; font-weight: 600; border-bottom: 2px solid var(--border);
        white-space: nowrap; text-align: left;
    }
    .spk-table td { padding: 10px 14px; border-bottom: 1px solid var(--border); color: var(--text); }
    .spk-table tr.r-even td { background: var(--bg); }
    .spk-table tr.r-odd  td { background: var(--card); }
    .spk-table tr.r-best td { background: #0a2218; color: var(--green); font-weight: 700; }
    .spk-table tr:hover td { filter: brightness(1.15); }
    .tc { text-align: center !important; }

    /* ── Best result card ── */
    .best-result {
        background: linear-gradient(135deg, #0a2218 0%, #071a12 100%);
        border: 1px solid var(--green);
        border-radius: 12px; padding: 18px 22px; margin: 16px 0;
    }
    .best-result .title { color: var(--green); font-size: 17px; font-weight: 700; margin-bottom: 6px; }
    .best-result .badge {
        display: inline-block; background: rgba(34,197,94,.15);
        color: var(--green); font-size: 11px; font-weight: 700;
        padding: 3px 10px; border-radius: 20px; margin-bottom: 10px; letter-spacing: .5px;
    }
    .best-result .desc { color: #86efac; font-size: 13px; line-height: 1.6; }

    /* ── Section header ── */
    .section-title {
        color: var(--text); font-size: 20px; font-weight: 700;
        letter-spacing: -.3px; margin: 0 0 4px 0;
    }
    .section-sub { color: var(--muted); font-size: 13px; margin: 0 0 20px 0; }

    /* ── Info banner ── */
    .info-banner {
        background: rgba(59,130,246,.08); border: 1px solid rgba(59,130,246,.25);
        color: #93c5fd; border-radius: 8px; padding: 10px 14px; font-size: 13px;
    }

    /* Sidebar page_link styling */
    [data-testid="stSidebar"] [data-testid="stPageLink"] a {
        display: flex !important;
        align-items: center !important;
        padding: 10px 14px !important;
        border-radius: 8px !important;
        color: #94a3b8 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        text-decoration: none !important;
        margin-bottom: 4px !important;
        transition: all .15s ease !important;
        border: 1px solid transparent !important;
    }
    [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
        background: rgba(59,130,246,.1) !important;
        color: #60a5fa !important;
        border-color: rgba(59,130,246,.2) !important;
    }

    /* ── Stat mini cards grid ── */
    .mini-grid { display: flex; flex-wrap: wrap; gap: 12px; margin: 14px 0; }
    .mini-card {
        flex: 1; min-width: 150px;
        background: var(--card); border: 1px solid var(--border);
        border-radius: 10px; padding: 12px 16px;
    }
    .mini-card .lbl { color: var(--muted); font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .5px; }
    .mini-card .val { color: var(--text); font-size: 17px; font-weight: 700; margin-top: 3px; }
    .mini-card .val.accent { color: var(--accent); }
    </style>
    """, unsafe_allow_html=True)