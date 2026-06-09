import streamlit as st

# ── Data laptop (Format Desimal Asli Sesuai Excel Rumus Awal) ─────────────────────
DEFAULT_LAPTOPS = [
    {"nama": 'MacBook Air 13" (M1 2020)',         "storage": 256,  "ram": 8,  "processor_score": 40,  "battery": 4300, "harga": 9.0},
    {"nama": 'MacBook Air 13" (M2 2022)',         "storage": 256,  "ram": 8,  "processor_score": 60,  "battery": 4730, "harga": 13.3},
    {"nama": 'MacBook Air 13" (M3 2024)',         "storage": 256,  "ram": 8,  "processor_score": 100, "battery": 4730, "harga": 14.0},
    {"nama": 'MacBook Air 15" (M3 2024)',         "storage": 512,  "ram": 12, "processor_score": 100, "battery": 5849, "harga": 26.0},
    {"nama": 'MacBook Pro 14" (M3 2023)',         "storage": 512,  "ram": 8,  "processor_score": 100, "battery": 6068, "harga": 22.0},
    {"nama": "HP 14-EP1711TU",                    "storage": 512,  "ram": 16, "processor_score": 90,  "battery": 3560, "harga": 9.9},
    {"nama": "HP 14s-dq4016TU",                  "storage": 512,  "ram": 16, "processor_score": 70,  "battery": 3560, "harga": 9.5},
    {"nama": "HP Victus 15-fb3150AX",             "storage": 512,  "ram": 16, "processor_score": 100, "battery": 4550, "harga": 20.1},
    {"nama": "HP Victus 15-fa2666TX",             "storage": 512,  "ram": 16, "processor_score": 90,  "battery": 4550, "harga": 17.5},
    {"nama": "HP 14s-FQ1036AU/FQ Series",         "storage": 512,  "ram": 16, "processor_score": 70,  "battery": 3560, "harga": 18.3},
    {"nama": "Huawei MateBook D14 (2024)",        "storage": 512,  "ram": 16, "processor_score": 80,  "battery": 3665, "harga": 10.5},
    {"nama": "Huawei MateBook D15",               "storage": 512,  "ram": 8,  "processor_score": 60,  "battery": 3665, "harga": 7.4},
    {"nama": "Huawei MateBook D16 (2024)",        "storage": 1024, "ram": 16, "processor_score": 90,  "battery": 6000, "harga": 13.0},
    {"nama": "Huawei MateBook 14",                "storage": 1024, "ram": 16, "processor_score": 100, "battery": 6000, "harga": 14.5},
    {"nama": "Huawei MateBook X Pro Premium",     "storage": 2048, "ram": 32, "processor_score": 60,  "battery": 6000, "harga": 34.8},
    {"nama": "Lenovo IdeaPad Slim 3",             "storage": 512,  "ram": 8,  "processor_score": 60,  "battery": 4156, "harga": 6.5},
    {"nama": "Lenovo IdeaPad Slim 3 Intel",       "storage": 256,  "ram": 8,  "processor_score": 70,  "battery": 4950, "harga": 6.1},
    {"nama": "Lenovo ThinkPad L14 Gen 4",         "storage": 512,  "ram": 16, "processor_score": 80,  "battery": 4156, "harga": 14.5},
    {"nama": "Lenovo LOQ Gaming 15IRX9",          "storage": 512,  "ram": 12, "processor_score": 100, "battery": 3896, "harga": 15.5},
    {"nama": "Lenovo IdeaPad Flex 3 Touch",       "storage": 256,  "ram": 4,  "processor_score": 80,  "battery": 3240, "harga": 6.4},
    {"nama": "DELL 14 DC14250",                   "storage": 1024, "ram": 16, "processor_score": 80,  "battery": 3420, "harga": 46220.0},
    {"nama": "DELL Inspiron 3530",                "storage": 1024, "ram": 16, "processor_score": 90,  "battery": 3600, "harga": 46253.0},
    {"nama": "DELL Vostro 3405 (4GB)",            "storage": 1024, "ram": 4,  "processor_score": 50,  "battery": 3550, "harga": 46180.0},
    {"nama": "DELL Latitude 3320",                "storage": 512,  "ram": 8,  "processor_score": 80,  "battery": 3500, "harga": 15.0},
    {"nama": "DELL Vostro 3405 (16GB)",           "storage": 512,  "ram": 16, "processor_score": 50,  "battery": 3500, "harga": 46151.0},
    {"nama": "Acer Aspire Lite 14 (AL14-37P)",    "storage": 512,  "ram": 8,  "processor_score": 40,  "battery": 3900, "harga": 6.8},
    {"nama": "Acer Aspire Go 14 (AG14-31P)",      "storage": 512,  "ram": 8,  "processor_score": 45,  "battery": 4700, "harga": 8.0},
    {"nama": "Acer Aspire Lite 15 (AL15 Ryzen 7)","storage": 512,  "ram": 16, "processor_score": 100, "battery": 5100, "harga": 11.8},
    {"nama": "Acer Swift Go 14 AI (SFG14-71T)",   "storage": 512,  "ram": 16, "processor_score": 90,  "battery": 5570, "harga": 12.9},
    {"nama": "Acer Nitro V15 (ANV15-42-R60U)",    "storage": 512,  "ram": 16, "processor_score": 90,  "battery": 5100, "harga": 17.6},
]

DEFAULT_USERS = [
    {"username": "admin",     "password": "123", "role": "admin"},
    {"username": "mahasiswa", "password": "123", "role": "mahasiswa"},
]

_MAX_S = 2048;  _MIN_S = 256
_MAX_R = 32;    _MIN_R = 4
_MAX_P = 100;   _MIN_P = 40
_MAX_B = 6068;  _MIN_B = 3240
_MAX_H = 46253; _MIN_H = 6.1

W_S = 0.25227680   
W_R = 0.20120370   
W_P = 0.26027991   
W_B = 0.14819219   
W_H = 0.13804739   

# Diubah ke v20 untuk memaksa Streamlit menghapus total data cache bermasalah dari memori browser
_DATA_VERSION = 20  

def init_state():
    defaults = {"logged_in": False, "username": "", "role": "", "rec_history": [], "flash": None}
    for k, v in defaults.items():
        if k not in st.session_state: st.session_state[k] = v
    if "users" not in st.session_state: st.session_state.users = DEFAULT_USERS.copy()
    if "laptops" not in st.session_state or st.session_state.get("_data_version") != _DATA_VERSION:
        st.session_state.laptops = [l.copy() for l in DEFAULT_LAPTOPS]
        st.session_state["_data_version"] = _DATA_VERSION

def set_flash(kind, msg): st.session_state.flash = (kind, msg)
def show_flash():
    if st.session_state.flash:
        kind, msg = st.session_state.flash
        colors = {"ok": ("#0a2218", "#4ade80", "#16a34a"), "err": ("#2a0a0a", "#f87171", "#dc2626"), "warn": ("#2d1a00", "#fcd34d", "#7c4a00"), "info": ("#0d1f3c", "#60a5fa", "#1d4ed8")}
        bg, fg, border = colors.get(kind, colors["info"])
        st.markdown(f'<div style="background:{bg}; color:{fg}; border:1px solid {border}; padding:10px 16px; border-radius:8px; margin:10px 0; font-size:14px; font-weight:500;">{msg}</div>', unsafe_allow_html=True)
        st.session_state.flash = None

def get_global_minmax():
    return {"MAX_S": _MAX_S, "MIN_S": _MIN_S, "MAX_R": _MAX_R, "MIN_R": _MIN_R, "MAX_P": _MAX_P, "MIN_P": _MIN_P, "MAX_B": _MAX_B, "MIN_B": _MIN_B, "MAX_H": _MAX_H, "MIN_H": _MIN_H}

def utility(lp):
    mm = get_global_minmax()
    return {
        "storage": (lp["storage"] - mm["MIN_S"]) / (mm["MAX_S"] - mm["MIN_S"]) if mm["MAX_S"] != mm["MIN_S"] else 1.0,
        "ram": (lp["ram"] - mm["MIN_R"]) / (mm["MAX_R"] - mm["MIN_R"]) if mm["MAX_R"] != mm["MIN_R"] else 1.0,
        "processor": (lp["processor_score"] - mm["MIN_P"]) / (mm["MAX_P"] - mm["MIN_P"]) if mm["MAX_P"] != mm["MIN_P"] else 1.0,
        "battery": (lp["battery"] - mm["MIN_B"]) / (mm["MAX_B"] - mm["MIN_B"]) if mm["MAX_B"] != mm["MIN_B"] else 1.0,
        "harga": (mm["MAX_H"] - lp["harga"]) / (mm["MAX_H"] - mm["MIN_H"]) if mm["MAX_H"] != mm["MIN_H"] else 1.0,
    }

def smart_score(u): return round(W_S * u["storage"] + W_R * u["ram"] + W_P * u["processor"] + W_B * u["battery"] + W_H * u["harga"], 6)

def rank_laptops(max_harga=None):
    results = []
    for lp in st.session_state.laptops:
        u = utility(lp)
        skor = smart_score(u)
        results.append({**lp, "utilitas": u, "skor": skor})
    if max_harga is not None:
        results = [r for r in results if r["harga"] <= max_harga]
    results.sort(key=lambda x: x["skor"], reverse=True)
    for i, r in enumerate(results, 1): r["ranking"] = i
    return results

def get_minmax(): return get_global_minmax()
def proc_label(s):
    if s <= 45: return "⚪ Entry-Level"
    elif s <= 60: return "🔵 Low-Mid"
    elif s <= 75: return "🟡 Mid-Range"
    elif s <= 90: return "🟠 High-Mid"
    else: return "🔴 High-End"

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
    if h <= 10: tips.append("harga ramah mahasiswa")
    else: tips.append("investasi premium")
    if not cocok: cocok = ["Penggunaan Umum"]
    return f"🎯 {', '.join(cocok)}. 💡 {'. '.join(t.capitalize() for t in tips)}."