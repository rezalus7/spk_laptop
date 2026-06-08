import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import theme, state
from datetime import datetime

# Paksa sidebar bawaan collapse total agar space halaman luas
st.set_page_config(page_title="Dashboard — SPK Laptop", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")
theme.inject()
state.init_state()

if not st.session_state.logged_in:
    st.switch_page("Beranda.py")

# ─── NAVIGATION BAR ATAS MODERN (GANTI SIDEBAR) ───
# Navigasi ini menggantikan sidebar agar aman dibuka di device apa saja
nav_cols = st.columns([1.5, 1, 1, 1, 1])

with nav_cols[0]:
    st.markdown(f"""
    <div style="padding-top: 6px;">
        <span style="font-weight:800; font-size:16px; color:#fff; letter-spacing:1px;">💻 SPK LAPTOP</span>
        <span style="font-size:11px; color:#60a5fa; margin-left:6px;">({st.session_state.username})</span>
    </div>
    """, unsafe_allow_html=True)

with nav_cols[1]:
    if st.button("📊 Dashboard", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Dashboard.py")

with nav_cols[2]:
    if st.button("📋 Data Laptop", use_container_width=True, type="secondary"):
        st.switch_page("pages/2_Data_Laptop.py")

with nav_cols[3]:
    if st.button("🕐 Riwayat", use_container_width=True, type="secondary"):
        st.switch_page("pages/3_Riwayat.py")

with nav_cols[4]:
    if st.button("🚪 Keluar", use_container_width=True, type="secondary"):
        for k in ["logged_in","username","role"]:
            st.session_state[k] = "" if k != "logged_in" else False
        st.switch_page("Beranda.py")

st.markdown("<hr style='border-color:#1e2d45; margin:16px 0 24px 0;'>", unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────
state.show_flash()
st.markdown("""
<p class="section-title">Dashboard Recommendation</p>
<p class="section-sub">Optimasi pemilihan laptop menggunakan metode Simple Multi-Attribute Rating Technique (SMART)</p>
""", unsafe_allow_html=True)

# ── Weight info ───────────────────────────────────────────
with st.expander("Bobot Kriteria SMART yang Digunakan", expanded=False):
    w_col = st.columns(5)
    labels = ["Processor","Storage","RAM","Baterai","Harga"]
    weights = [state.W_P, state.W_S, state.W_R, state.W_B, state.W_H]
    for c, lbl, w in zip(w_col, labels, weights):
        with c:
            st.metric(lbl, f"{int(w*100)}%")

# ── Filter panel ──────────────────────────────────────────
with st.container(border=True):
    st.markdown("<h5 style='color:#60a5fa; margin-bottom:14px; font-size:15px;'>Konfigurasi Filter Kriteria</h5>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        budget = st.slider("Batas Budget (Rp)", 6_000_000, 35_000_000, 12_000_000, 500_000,
                           format="Rp %d", help="Harga maksimum laptop yang dicari")
        proc_min = st.slider("Skor Processor Minimum", 40, 100, 60, 5,
                             help="Skor benchmark relatif (40=entry, 100=high-end)")
        st.caption(f"Kategori: **{state.proc_label(proc_min)}**")
    with c2:
        ram_min  = st.select_slider("RAM Minimum (GB)", [4, 8, 12, 16, 32], value=8)
        stor_min = st.select_slider("Storage Minimum (GB)", [256, 512, 1024, 2048], value=512)
    with c3:
        bat_min  = st.slider("Baterai Minimum (mAh)", 3240, 6068, 3500, 100)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        run_btn  = st.button("Jalankan Analisis SMART", use_container_width=True, type="primary")

# ── Computation ───────────────────────────────────────────
if run_btn:
    mm = state.get_minmax()

    filtered = [
        lp for lp in st.session_state.laptops
        if lp["harga"] <= budget
        and lp["processor_score"] >= proc_min
        and lp["ram"] >= ram_min
        and lp["storage"] >= stor_min
        and lp["battery"] >= bat_min
    ]

    if not filtered:
        st.markdown("""
        <div style="background:#2d1a00; color:#fcd34d; border:1px solid #7c4a00;
                    padding:14px 18px; border-radius:10px; font-size:14px; margin-top:12px;">
            Tidak ada laptop yang memenuhi semua kriteria. Coba longgarkan filter.
        </div>""", unsafe_allow_html=True)
        st.stop()

    mh = state.MAX_HARGA_REF if budget >= mm["MAX_H"] else budget
    results = sorted(
        [(lp, state.smart_score(state.utility(lp, mh, mm)), state.utility(lp, mh, mm)) for lp in filtered],
        key=lambda x: x[1], reverse=True
    )

    best_lp, best_sc, _ = results[0]

    # ── Stat cards ───────────────────────────────────────
    st.markdown(f"""
    <div class="mini-grid" style="margin-top:20px;">
        <div class="mini-card">
            <div class="lbl">Budget</div>
            <div class="val">Rp {budget:,}</div>
        </div>
        <div class="mini-card">
            <div class="lbl">RAM / Storage</div>
            <div class="val">{ram_min} GB / {stor_min} GB</div>
        </div>
        <div class="mini-card">
            <div class="lbl">Lolos Filter</div>
            <div class="val accent">{len(filtered)} Laptop</div>
        </div>
        <div class="mini-card">
            <div class="lbl">Skor Terbaik</div>
            <div class="val accent">{best_sc}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Best result banner ────────────────────────────────
    st.markdown(f"""
    <div class="best-result">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
            <div class="title">{best_lp['nama']}</div>
        </div>
        <div class="badge">SKOR SMART: {best_sc}</div>
        <div class="desc">{state.kegunaan(best_lp)}</div>
        <div style="display:flex; flex-wrap:wrap; gap:10px; margin-top:12px;">
            <span style="background:rgba(34,197,94,.1); color:#86efac; padding:3px 10px; border-radius:6px; font-size:12px;">
                Processor: {best_lp['processor']}
            </span>
            <span style="background:rgba(34,197,94,.1); color:#86efac; padding:3px 10px; border-radius:6px; font-size:12px;">
                RAM {best_lp['ram']} GB
            </span>
            <span style="background:rgba(34,197,94,.1); color:#86efac; padding:3px 10px; border-radius:6px; font-size:12px;">
                Storage: {best_lp['storage']} GB
            </span>
            <span style="background:rgba(34,197,94,.1); color:#86efac; padding:3px 10px; border-radius:6px; font-size:12px;">
                Baterai: {best_lp['battery']} mAh
            </span>
            <span style="background:rgba(34,197,94,.1); color:#86efac; padding:3px 10px; border-radius:6px; font-size:12px;">
                Harga: Rp {best_lp['harga']:,}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Results table ─────────────────────────────────────
    st.markdown("<h5 style='color:#e2e8f0; font-weight:600; margin:24px 0 10px;'>Matriks Pembobotan Nilai Utilitas</h5>", unsafe_allow_html=True)

    rows = ""
    for rank, (lp, sc, u) in enumerate(results, 1):
        cls = "r-best" if rank == 1 else ("r-even" if rank % 2 == 0 else "r-odd")
        rows += f"""
        <tr class="{cls}">
            <td class="tc" style="font-weight:700;">{rank}</td>
            <td><b>{lp['nama']}</b></td>
            <td style="font-size:12px; color:#94a3b8;">{lp['processor']}</td>
            <td class="tc">{lp['ram']} GB</td>
            <td class="tc">{lp['storage']} GB</td>
            <td class="tc">{lp['battery']}</td>
            <td>Rp {lp['harga']:,}</td>
            <td class="tc">{u['processor']}</td>
            <td class="tc">{u['storage']}</td>
            <td class="tc">{u['ram']}</td>
            <td class="tc">{u['battery']}</td>
            <td class="tc">{u['harga']}</td>
            <td class="tc" style="color:#3b82f6; font-weight:700; font-size:14px;">{sc}</td>
        </tr>"""

    st.markdown(f"""
    <div class="spk-table-wrap">
    <table class="spk-table">
        <thead>
            <tr>
                <th rowspan="2" style="text-align:center;">Rank</th>
                <th rowspan="2">Nama Laptop</th>
                <th rowspan="2">Processor</th>
                <th colspan="4" style="text-align:center; border-bottom:1px solid #1e2d45;">Spesifikasi</th>
                <th colspan="5" style="text-align:center; border-bottom:1px solid #1e2d45;">Nilai Utilitas (U)</th>
                <th rowspan="2" style="text-align:center;">Skor SMART</th>
            </tr>
            <tr>
                <th class="tc">RAM</th><th class="tc">Storage</th>
                <th class="tc">Baterai</th><th>Harga</th>
                <th class="tc">U-Proc</th><th class="tc">U-Stor</th>
                <th class="tc">U-RAM</th><th class="tc">U-Bat</th><th class="tc">U-Hrg</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

    # ── Save to history ───────────────────────────────────
    st.session_state.rec_history.append({
        "user":        st.session_state.username,
        "budget":      budget,
        "min_proc":    proc_min,
        "min_ram":     ram_min,
        "min_storage": stor_min,
        "min_battery": bat_min,
        "laptop":      best_lp["nama"],
        "skor":        best_sc,
        "total":       len(filtered),
        "tanggal":     datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    })

    st.markdown("""
    <div class="info-banner" style="margin-top:16px;">
        Hasil analisis telah disimpan ke riwayat.
    </div>""", unsafe_allow_html=True)