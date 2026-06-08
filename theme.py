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

    /* ── SEMBUNYIKAN TOTAL SIDEBAR BAWAAN ── */
    /* Kita hilangkan total sidebar bawaan agar tampilan di HP bersih 100% */
    [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], 
    button[data-testid="baseButton-header"], [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        width: 0px !important;
    }

    #MainMenu, footer, header { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    
    /* Atur jarak atas halaman utama agar pas */
    .block-container { 
        padding-top: 2rem !important; 
        max-width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* ── KUSTOM NAVIGASI HEADER ATAS (UI MODERN) ── */
    .custom-nav {
        display: flex;
        gap: 10px;
        background: var(--surface);
        border: 1px solid var(--border);
        padding: 6px 12px;
        border-radius: 12px;
        margin-bottom: 24px;
        align-items: center;
        flex-wrap: wrap;
    }
    .custom-nav-brand {
        font-weight: 700;
        color: #fff;
        margin-right: auto;
        font-size: 14px;
        letter-spacing: 1px;
    }

    /* ── Native buttons ── */
    .stButton > button {
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        height: 38px !important;
        transition: all .15s ease !important;
        border: none !important;
    }
    .stButton > button[kind="primary"] {
        background: var(--accent) !important;
        color: #fff !important;
    }
    .stButton > button[kind="secondary"] {
        background: var(--card) !important;
        color: var(--soft) !important;
        border: 1px solid var(--border) !important;
    }
    .stButton > button[kind="secondary"]:hover {
        border-color: var(--accent) !important;
        color: var(--accent) !important;
    }

    /* ── Sliders & Inputs ── */
    [data-testid="stSlider"] label { color: var(--soft) !important; font-size: 13px !important; }
    [data-testid="stSlider"] [data-testid="stThumbValue"] { color: var(--accent) !important; }
    [data-testid="stTextInput"] input, [data-testid="stNumberInput"] input {
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 8px !important;
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

    /* ── Section header ── */
    .section-title { color: var(--text); font-size: 20px; font-weight: 700; margin: 0 0 4px 0; }
    .section-sub { color: var(--muted); font-size: 13px; margin: 0 0 20px 0; }

    /* ── Stat mini cards grid ── */
    .mini-grid { display: flex; flex-wrap: wrap; gap: 12px; margin: 14px 0; }
    .mini-card {
        flex: 1; min-width: 150px;
        background: var(--card); border: 1px solid var(--border);
        border-radius: 10px; padding: 12px 16px;
    }
    .mini-card .lbl { color: var(--muted); font-size: 11px; font-weight: 600; text-transform: uppercase; }
    .mini-card .val { color: var(--text); font-size: 17px; font-weight: 700; margin-top: 3px; }
    .mini-card .val.accent { color: var(--accent); }
    </style>
    """, unsafe_allow_html=True)