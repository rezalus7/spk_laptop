import streamlit as st

DEFAULT_LAPTOPS = [
    {"nama":"MacBook Air 13 M1 2020", "processor":"Apple M1", "processor_score":40, "ram":8, "storage":256, "battery":4300, "harga":9000000},
    {"nama":"MacBook Air 13 M2 2022", "processor":"Apple M2", "processor_score":60, "ram":8, "storage":256, "battery":4730, "harga":13000000},
    {"nama":"MacBook Air 13 M3 2024", "processor":"Apple M3", "processor_score":100,"ram":8, "storage":256, "battery":4730, "harga":14000000},
    {"nama":"MacBook Air 15 M3 2024", "processor":"Apple M3", "processor_score":100,"ram":12, "storage":512, "battery":5849, "harga":26000000},
    {"nama":"MacBook Pro 14 M3 2023", "processor":"Apple M3", "processor_score":100,"ram":8, "storage":512, "battery":6068, "harga":22000000},
    {"nama":"HP 14-EP1711TU", "processor":"Intel i5-13420H", "processor_score":90, "ram":16, "storage":512, "battery":3560, "harga":10000000},
    {"nama":"HP 14s-dq4016TU", "processor":"Intel i3-1215U", "processor_score":70, "ram":16, "storage":512, "battery":3560, "harga":10000000},
    {"nama":"HP Victus 15-fb3150AX", "processor":"Ryzen 7 8840HS", "processor_score":100,"ram":16, "storage":512, "battery":4550, "harga":20000000},
    {"nama":"HP Victus 15-fa2666TX", "processor":"Intel i5-13500H", "processor_score":90, "ram":16, "storage":512, "battery":4550, "harga":18000000},
    {"nama":"HP 14s-FQ1036AU", "processor":"Ryzen 5 PRO 7530U", "processor_score":70, "ram":16, "storage":512, "battery":3560, "harga":18000000},
    {"nama":"Huawei MateBook D14 2024", "processor":"Ryzen 5 PRO 7530U", "processor_score":80, "ram":16, "storage":512, "battery":3665, "harga":11000000},
    {"nama":"Huawei MateBook D15", "processor":"Intel i5-10210U", "processor_score":60, "ram":8, "storage":512, "battery":3665, "harga":7000000},
    {"nama":"Huawei MateBook D16 2024", "processor":"Intel Core Ultra 5", "processor_score":90, "ram":16, "storage":1024, "battery":6000, "harga":13000000},
    {"nama":"Huawei MateBook 14", "processor":"Intel Core Ultra 9", "processor_score":100,"ram":16, "storage":1024, "battery":6000, "harga":15000000},
    {"nama":"Huawei MateBook X Pro Premium","processor":"Intel Core Ultra 9", "processor_score":60, "ram":32, "storage":2048, "battery":6000, "harga":35000000},
    {"nama":"Lenovo IdeaPad Slim 3", "processor":"Intel i5-10210U", "processor_score":60, "ram":8, "storage":512, "battery":4156, "harga":7000000},
    {"nama":"Lenovo IdeaPad Slim 3 Intel", "processor":"Intel i3-1215U", "processor_score":70, "ram":8, "storage":256, "battery":4950, "harga":6000000},
    {"nama":"Lenovo ThinkPad L14 Gen 4", "processor":"Ryzen 5 PRO 7530U", "processor_score":80, "ram":16, "storage":512, "battery":4156, "harga":15000000},
    {"nama":"Lenovo LOQ Gaming 15IRX9", "processor":"Intel i5-13450HX", "processor_score":100,"ram":12, "storage":512, "battery":3896, "harga":16000000},
    {"nama":"Lenovo IdeaPad Flex 3 Touch", "processor":"Intel N150", "processor_score":80, "ram":4, "storage":256, "battery":3240, "harga":6000000},
    {"nama":"DELL 14 DC14250", "processor":"Intel i7-1165G7", "processor_score":80, "ram":16, "storage":1024, "battery":3420, "harga":17700000},
    {"nama":"DELL Inspiron 3530", "processor":"Intel i7-1355U", "processor_score":90, "ram":16, "storage":1024, "battery":3600, "harga":19800000},
    {"nama":"DELL Vostro 3405 4GB", "processor":"Ryzen 5 3500", "processor_score":50, "ram":4, "storage":1024, "battery":3550, "harga":7600000},
    {"nama":"DELL Latitude 3320", "processor":"Intel i7-1165G7", "processor_score":80, "ram":8, "storage":512, "battery":3500, "harga":15000000},
    {"nama":"DELL Vostro 3405 16GB", "processor":"Ryzen 5 3500", "processor_score":50, "ram":16, "storage":512, "battery":3500, "harga":9500000},
    {"nama":"Acer Aspire Lite 14", "processor":"Intel N150", "processor_score":40, "ram":8, "storage":512, "battery":3900, "harga":7000000},
    {"nama":"Acer Aspire Go 14", "processor":"Intel i3-N305", "processor_score":45, "ram":8, "storage":512, "battery":4700, "harga":8000000},
    {"nama":"Acer Aspire Lite 15 Ryzen 7", "processor":"Ryzen 7 8840HS", "processor_score":100,"ram":16, "storage":512, "battery":5100, "harga":12000000},
    {"nama":"Acer Swift Go 14 AI", "processor":"Intel Core Ultra 5", "processor_score":90, "ram":16, "storage":512, "battery":5570, "harga":13000000},
    {"nama":"Acer Nitro V15", "processor":"Intel i5-13500H", "processor_score":90, "ram":16, "storage":512, "battery":5100, "harga":18000000},
]

DEFAULT_USERS = [
    {"username": "admin", "password": "123", "role": "admin"},
    {"username": "mahasiswa", "password": "123", "role": "mahasiswa"},
]

MAX_HARGA_REF = 46_253_000
W_P, W_S, W_R, W_B, W_H = 0.26, 0.25, 0.20, 0.15, 0.14

def init_state():
    defaults = {
        "logged_in": False,
        "username": "",
        "role": "",
        "rec_history": [],
        "flash": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    if "users" not in st.session_state:
        st.session_state.users = DEFAULT_USERS.copy()
    if "laptops" not in st.session_state:
        st.session_state.laptops = [l.copy() for l in DEFAULT_LAPTOPS]

def set_flash(kind, msg):
    st.session_state.flash = (kind, msg)

def show_flash():
    if st.session_state.flash:
        kind, msg = st.session_state.flash
        colors = {
            "ok":   ("#0a2218", "#4ade80", "#16a34a"),
            "err":  ("#2a0a0a", "#f87171", "#dc2626"),
            "warn": ("#2d1a00", "#fcd34d", "#7c4a00"),
            "info": ("#0d1f3c", "#60a5fa", "#1d4ed8"),
        }
        bg, fg, border = colors.get(kind, colors["info"])
        st.markdown(f"""
        <div style="background:{bg}; color:{fg}; border:1px solid {border};
            padding:10px 16px; border-radius:8px; margin:10px 0;
            font-size:14px; font-weight:500;">
            {msg}
        </div>""", unsafe_allow_html=True)
        st.session_state.flash = None

# ── Format harga Rupiah ───────────────────────────────────
def fmt_harga(harga):
    """Format angka integer ke string Rupiah: Rp 9.000.000"""
    return "Rp {:,.0f}".format(int(harga)).replace(",", ".")

# ── SMART calculation helpers ─────────────────────────────
def get_minmax():
    L = st.session_state.laptops
    return dict(
        MAX_P=max(l["processor_score"] for l in L), MIN_P=min(l["processor_score"] for l in L),
        MAX_S=max(l["storage"]         for l in L), MIN_S=min(l["storage"]         for l in L),
        MAX_R=max(l["ram"]             for l in L), MIN_R=min(l["ram"]             for l in L),
        MAX_B=max(l["battery"]         for l in L), MIN_B=min(l["battery"]         for l in L),
        MIN_H=min(l["harga"]           for l in L), MAX_H=max(l["harga"]           for l in L),
    )

def utility(lp, max_harga=None, mm=None):
    if mm is None:
        mm = get_minmax()
    if max_harga is None:
        max_harga = mm["MAX_H"]
    def norm(v, lo, hi): return round((v - lo) / (hi - lo), 3) if hi != lo else 1.0
    return {
        "processor": norm(lp["processor_score"], mm["MIN_P"], mm["MAX_P"]),
        "storage":   norm(lp["storage"],         mm["MIN_S"], mm["MAX_S"]),
        "ram":       norm(lp["ram"],             mm["MIN_R"], mm["MAX_R"]),
        "battery":   norm(lp["battery"],         mm["MIN_B"], mm["MAX_B"]),
        "harga":     norm(max_harga - lp["harga"], 0, max_harga - mm["MIN_H"]),
    }

def smart_score(u):
    return round(W_P*u["processor"] + W_S*u["storage"] + W_R*u["ram"] + W_B*u["battery"] + W_H*u["harga"], 4)

def proc_label(s):
    if s <= 45:  return "⚪ Entry-Level"
    elif s <= 60: return "🔵 Low-Mid"
    elif s <= 75: return "🟡 Mid-Range"
    elif s <= 90: return "🟠 High-Mid"
    else:         return "🔴 High-End"

def kegunaan(lp):
    p, r, s, b, h = lp["processor_score"], lp["ram"], lp["storage"], lp["battery"], lp["harga"]
    cocok, tips = [], []
    if p >= 80 and r >= 16: cocok.append("Coding & Programming"); tips.append("multitasking IDE lancar")
    elif p >= 60 and r >= 8: cocok.append("Belajar Pemrograman")
    if p >= 90 and r >= 16: cocok.append("Data Analysis & ML"); tips.append("komputasi data berat oke")
    if p >= 80 and r >= 16 and s >= 512: cocok.append("Video / Photo Editing"); tips.append("render responsif")
    if p >= 90 and r >= 12: cocok.append("Gaming Mid-High"); tips.append("game stabil")
    if r >= 8 and s >= 512: cocok.append("Office & Produktivitas")
    if b >= 5000: cocok.append("Mobilitas Tinggi"); tips.append("baterai seharian")
    if h <= 10_000_000: tips.append("harga ramah mahasiswa")
    else: tips.append("investasi premium")
    if not cocok: cocok = ["Penggunaan Umum"]
    return f"🎯 {', '.join(cocok)}. 💡 {'. '.join(t.capitalize() for t in tips)}."