import streamlit as st

def inject():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

:root {
  --bg: #080c14;
  --surface: #0f1522;
  --card: rgba(20, 29, 46, 0.65);
  --border: rgba(59, 130, 246, 0.15);
  --accent: #3b82f6;
  --accent2: #06b6d4;
  --accent-gradient: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
  --green: #22c55e;
  --yellow: #eab308;
  --red: #ef4444;
  --text: #e2e8f0;
  --muted: #64748b;
  --soft: #94a3b8;
}

/* ── BACKGROUND ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"], .main {
  background-color: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"]::before {
  content: "";
  position: fixed; top: -10%; right: -10%; width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(59,130,246,0.06) 0%, transparent 70%);
  pointer-events: none; z-index: 0; filter: blur(60px);
}
[data-testid="stAppViewContainer"]::after {
  content: "";
  position: fixed; bottom: -10%; left: -10%; width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(6,182,212,0.05) 0%, transparent 70%);
  pointer-events: none; z-index: 0; filter: blur(60px);
}

[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] span,
[data-testid="stAppViewContainer"] label { color: var(--text); }

/* ── STREAMLIT CHROME CLEANUP ── */
#MainMenu, footer { visibility: hidden !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stToolbarActions"] {
  display: none !important;
  visibility: hidden !important;
  opacity: 0 !important;
  pointer-events: none !important;
}
.block-container { padding-top: 2.5rem !important; position: relative; z-index: 1; }

/* ── HEADER & SIDEBAR TOGGLE BUTTON ── */
header[data-testid="stHeader"] {
  background: transparent !important;
  visibility: visible !important;
}
header[data-testid="stHeader"] button,
[data-testid="stSidebarCollapsedControl"] button,
section[data-testid="stSidebar"] button {
  color: var(--text) !important;
  background-color: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  backdrop-filter: blur(8px);
  transition: all 0.2s ease;
}
header[data-testid="stHeader"] button:hover {
  border-color: var(--accent) !important;
  background-color: rgba(59,130,246,0.1) !important;
}

/* ══════════════════════════════════════════════
   SIDEBAR — LAYOUT WEB MODERN
   Logo/user → rapat atas
   Menu navigasi → langsung di bawah logo
   Logout → anchor di paling bawah
   ══════════════════════════════════════════════ */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #05080f 0%, #080c14 100%) !important;
  border-right: 1px solid var(--border) !important;
}

/* Container utama sidebar: flex column, isi dari atas */
[data-testid="stSidebar"] > div:first-child {
  padding: 0 !important;
  margin: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: flex-start !important;
  align-items: stretch !important;
  height: 100vh !important;
  overflow-y: auto !important;
}

/* Sembunyikan nav bawaan Streamlit (file-based routing) */
[data-testid="stSidebarNav"] { display: none !important; }

/* Semua teks sidebar */
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Blok pertama (logo/branding/user info) — rapat ke atas, NO margin besar */
[data-testid="stSidebar"] [data-testid="stVerticalBlock"]:first-child {
  margin-top: 0 !important;
  padding-top: 1.25rem !important;
}

/* Gap/spacer antara elemen sidebar dikecilkan */
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] [data-testid="stPageLink"] {
  margin-bottom: 0 !important;
  padding-bottom: 0 !important;
}

/* Divider/HR di sidebar */
[data-testid="stSidebar"] hr {
  margin: 8px 0 !important;
  border-color: var(--border) !important;
}

/* ── SIDEBAR NAVIGATION LINKS ── */
[data-testid="stSidebar"] [data-testid="stPageLink"] a {
  display: flex !important;
  align-items: center !important;
  padding: 10px 16px !important;
  border-radius: 12px !important;
  color: var(--soft) !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  text-decoration: none !important;
  margin: 2px 8px !important;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
  border: 1px solid transparent !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
  background: rgba(59,130,246,0.06) !important;
  color: var(--accent2) !important;
  border-color: rgba(59,130,246,0.1) !important;
  transform: translateX(2px);
}
[data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"] {
  background: rgba(59,130,246,0.1) !important;
  color: #fff !important;
  border-color: rgba(59,130,246,0.25) !important;
  font-weight: 600 !important;
}

/* ── LOGOUT BUTTON — push ke paling bawah ── */
/* Tempatkan tombol logout di bagian bawah sidebar */
[data-testid="stSidebar"] .stButton:last-of-type {
  margin-top: auto !important;
  padding: 0 8px 2rem 8px !important;
}

[data-testid="stSidebar"] .stButton > button {
  width: 100% !important;
  border-radius: 12px !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  height: 44px !important;
  background: rgba(20, 29, 46, 0.5) !important;
  color: var(--soft) !important;
  border: 1px solid var(--border) !important;
  transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  border-color: var(--red) !important;
  color: var(--red) !important;
  background: rgba(239, 68, 68, 0.05) !important;
  transform: translateY(-1px) !important;
}

/* ── NATIVE BUTTONS ── */
.stButton > button {
  border-radius: 12px !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  height: 44px !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  border: none !important;
  letter-spacing: 0.3px !important;
}
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {
  background: var(--accent-gradient) !important;
  color: #fff !important;
  box-shadow: 0 4px 14px rgba(59,130,246,0.25) !important;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(59,130,246,0.4) !important;
  filter: brightness(1.15);
}
.stButton > button[kind="secondary"],
.stButton > button[data-testid="baseButton-secondary"] {
  background: rgba(20, 29, 46, 0.5) !important;
  color: var(--soft) !important;
  border: 1px solid var(--border) !important;
}
.stButton > button[kind="secondary"]:hover {
  border-color: var(--red) !important;
  color: var(--red) !important;
  background: rgba(239, 68, 68, 0.05) !important;
  transform: translateY(-1px);
}

/* ── INPUTS ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
  background: rgba(8, 12, 20, 0.6) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: 12px !important;
  height: 44px !important;
  font-size: 14px !important;
  transition: all 0.2s ease !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 4px rgba(59,130,246,0.15) !important;
  background: rgba(8, 12, 20, 0.8) !important;
}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label {
  color: var(--soft) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  letter-spacing: 0.3px;
}
[data-testid="stSelectbox"] > div > div {
  background: rgba(8, 12, 20, 0.6) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: 12px !important;
  height: 44px !important;
}

/* ── SLIDERS & TABS ── */
[data-testid="stSlider"] [data-testid="stThumbValue"] {
  color: var(--accent2) !important;
  font-family: 'Space Mono', monospace;
}
[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: rgba(15, 21, 34, 0.8) !important;
  border-radius: 14px !important;
  padding: 6px !important;
  gap: 6px !important;
  border: 1px solid var(--border) !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--muted) !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  transition: all 0.2s ease;
}
[data-testid="stTabs"] [aria-selected="true"] {
  background: var(--accent) !important;
  color: #fff !important;
  box-shadow: 0 4px 12px rgba(59,130,246,0.2) !important;
}

/* ── FORMS & EXPANDER ── */
[data-testid="stForm"], div[data-testid="stExpander"] {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 20px !important;
  padding: 32px 28px !important;
  backdrop-filter: blur(16px) !important;
  box-shadow: 0 20px 50px rgba(0,0,0,0.3) !important;
}

/* ── METRIC CARDS ── */
[data-testid="stMetric"] {
  background: rgba(20, 29, 46, 0.4) !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px !important;
  padding: 18px !important;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 12px !important; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
[data-testid="stMetricValue"] { color: #fff !important; font-size: 24px !important; font-weight: 700 !important; }

/* ── SPK TABLE ── */
.spk-table-wrap {
  overflow-x: auto;
  border-radius: 16px;
  border: 1px solid var(--border);
  margin-top: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}
.spk-table { width: 100%; border-collapse: collapse; font-size: 13px; background: rgba(15, 21, 34, 0.6); }
.spk-table th {
  background: rgba(59, 130, 246, 0.08);
  color: var(--accent2);
  padding: 16px 14px;
  font-weight: 700;
  border-bottom: 2px solid var(--border);
  white-space: nowrap;
  text-align: left;
  text-transform: uppercase;
  font-size: 11px;
  letter-spacing: 0.5px;
}
.spk-table td { padding: 12px 14px; border-bottom: 1px solid rgba(30, 45, 69, 0.4); color: var(--text); }
.spk-table tr.r-even td { background: rgba(8, 12, 20, 0.3); }
.spk-table tr.r-odd td { background: rgba(20, 29, 46, 0.3); }
.spk-table tr.r-best td {
  background: rgba(34, 197, 150, 0.08) !important;
  color: #4ade80;
  font-weight: 700;
  border-top: 1px solid rgba(34,197,94,0.3);
  border-bottom: 1px solid rgba(34,197,94,0.3);
}
.spk-table tr:hover td { background: rgba(59, 130, 246, 0.06) !important; filter: brightness(1.1); }
.tc { text-align: center !important; }

/* ── BEST RESULT CARD ── */
.best-result {
  background: linear-gradient(135deg, rgba(10,34,24,0.7) 0%, rgba(7,26,18,0.7) 100%) !important;
  border: 1px solid rgba(34, 197, 94, 0.3) !important;
  border-radius: 18px; padding: 22px 26px; margin: 20px 0;
  backdrop-filter: blur(12px) !important;
  box-shadow: 0 15px 35px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.05);
}
.best-result .title { color: #4ade80; font-size: 20px; font-weight: 800; margin-bottom: 6px; letter-spacing: -0.3px; }
.best-result .badge {
  display: inline-block; background: rgba(34,197,94,0.12);
  color: #4ade80; font-size: 11px; font-weight: 700;
  padding: 4px 12px; border-radius: 20px; margin-bottom: 12px;
  letter-spacing: 0.8px; font-family: 'Space Mono', monospace;
  border: 1px solid rgba(34,197,94,0.2);
}
.best-result .desc { color: #a7f3d0; font-size: 13px; line-height: 1.65; }

/* ── TYPOGRAPHY ── */
.section-title {
  color: #fff; font-size: 26px; font-weight: 800;
  letter-spacing: -0.5px; margin: 0 0 6px 0;
  background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.section-sub { color: var(--muted); font-size: 13px; margin: 0 0 24px 0; font-weight: 400; }

/* ── INFO BANNER ── */
.info-banner {
  background: rgba(59,130,246,0.06); border: 1px solid rgba(59,130,246,0.2);
  color: #93c5fd; border-radius: 10px; padding: 12px 16px; font-size: 13px;
  backdrop-filter: blur(4px);
}

/* ── MINI CARDS ── */
.mini-grid { display: flex; flex-wrap: wrap; gap: 14px; margin: 18px 0; }
.mini-card {
  flex: 1; min-width: 160px;
  background: rgba(20, 29, 46, 0.4); border: 1px solid var(--border);
  border-radius: 14px; padding: 14px 18px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.15);
  transition: all 0.2s ease;
}
.mini-card:hover {
  border-color: rgba(59, 130, 246, 0.3);
  transform: translateY(-2px);
}
.mini-card .lbl { color: var(--muted); font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.mini-card .val { color: #fff; font-size: 18px; font-weight: 700; margin-top: 4px; }
.mini-card .val.accent {
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)