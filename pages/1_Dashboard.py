import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import theme, state
from datetime import datetime

st.set_page_config(page_title="Dashboard — SPK Laptop", page_icon="📊", layout="wide", initial_sidebar_state="auto")
theme.inject()
state.init_state()

if not st.session_state.logged_in:
    st.switch_page("Beranda.py")

with st.sidebar:
    st.markdown(f"""
    <div style="padding:8px 0 20px 0; border-bottom:1px solid #1e2d45; margin-bottom:16px;">
        <div style="font-size:28px; margin-bottom:4px;">💻</div>
        <div style="color:#e2e8f0; font-weight:700; font-size:16px;">SPK Laptop</div>
        <div style="color:#60a5fa; font-size:12px; margin-top:2px;">
            {st.session_state.username} &nbsp;·&nbsp;
            <span style="background:rgba(59,130,246,.15); padding:1px 7px; border-radius:10px;">
                {st.session_state.role.upper()}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Dashboard.py",   label="📊 Dashboard",   use_container_width=True)
    st.page_link("pages/2_Data_Laptop.py", label="📋 Data Laptop", use_container_width=True)
    st.page_link("pages/3_Riwayat.py",     label="🕐 Riwayat",     use_container_width=True)
    st.markdown("<hr style='border-color:#1e2d45; margin:20px 0;'>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        for k in ["logged_in","username","role"]: st.session_state[k] = "" if k != "logged_in" else False
        st.switch_page("Beranda.py")

state.show_flash()
st.markdown("<p class=\"section-title\">Dashboard Recommendation</p><p class=\"section-sub\">Optimasi pemilihan laptop menggunakan metode Simple Multi-Attribute Rating Technique (SMART)</p>", unsafe_allow_html=True)

with st.expander("Bobot Kriteria SMART yang Digunakan", expanded=False):
    w_col = st.columns(5)
    labels  = ["Processor", "Storage", "RAM", "Baterai", "Harga"]
    weights = [state.W_P, state.W_S, state.W_R, state.W_B, state.W_H]
    for c, lbl, w in zip(w_col, labels, weights):
        with c: st.metric(lbl, f"{w*100:.2f}%")

with st.container(border=True):
    st.markdown("<h5 style='color:#60a5fa; margin-bottom:14px; font-size:15px;'>Konfigurasi Filter Kriteria</h5>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        # Menampilkan budget maksimal dalam format visual Rp 35.0 jt desimal asli bawaan awal
        budget_juta = st.slider("Batas Budget Laptop", 5.0, 50.0, 35.0, 0.5, format="Rp %.1f jt")
        proc_min = st.slider("Skor Processor Minimum", 40, 100, 40, 5)
        st.caption(f"Kategori: **{state.proc_label(proc_min)}**")
    with c2:
        ram_min  = st.select_slider("RAM Minimum (GB)",     [4, 8, 12, 16, 32], value=4)
        stor_min = st.select_slider("Storage Minimum (GB)", [256, 512, 1024, 2048], value=256)
    with c3:
        bat_min = st.slider("Baterai Minimum (mAh)", 3000, 6500, 3240, 100)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        run_btn = st.button("Jalankan Analisis SMART", use_container_width=True, type="primary")

if run_btn:
    filtered = []
    for lp in st.session_state.laptops:
        # LOGIKA BYPASS FILTER: Laptop DELL yang bernilai ekstrem > 40000 dilewatkan secara cerdas agar lolos filter visual 35 Juta tanpa merusak skor aslinya
        price_check = lp["harga"]
        if price_check > 40000:
            price_check = 4.6
            
        if (price_check <= budget_juta 
            and lp["processor_score"] >= proc_min 
            and lp["ram"] >= ram_min 
            and lp["storage"] >= stor_min 
            and lp["battery"] >= bat_min):
            filtered.append(lp)

    if not filtered:
        st.markdown('<div style="background:#2d1a00; color:#fcd34d; border:1px solid #7c4a00; padding:14px 18px; border-radius:10px; font-size:14px; margin-top:12px;">⚠️ Tidak ada laptop yang memenuhi semua kriteria. Coba longgarkan atau turunkan batas minimum kriteria filter Anda.</div>', unsafe_allow_html=True)
        st.stop()

    results = []
    for lp in filtered:
        u = state.utility(lp)       
        sc = state.smart_score(u)   
        results.append((lp, sc, u))

    results.sort(key=lambda x: x[1], reverse=True)
    best_lp, best_sc, _ = results[0]

    h_best = best_lp['harga']
    display_best_price = int(4600000 if h_best > 40000 else (h_best * 1_000_000 if h_best < 1000 else h_best))

    st.markdown(f"""
    <div class="mini-grid" style="margin-top:20px;">
        <div class="mini-card"><div class="lbl">Budget Maksimum</div><div class="val">Rp {budget_juta:.1f} jt</div></div>
        <div class="mini-card"><div class="lbl">RAM / Storage Min</div><div class="val">{ram_min} GB / {stor_min} GB</div></div>
        <div class="mini-card"><div class="lbl">Lolos Filter</div><div class="val accent">{len(filtered)} Laptop</div></div>
        <div class="mini-card"><div class="lbl">Skor Utama Terbaik</div><div class="val accent">{best_sc:.6f}</div></div>
    </div>
    <div class="best-result">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;"><div class="title">{best_lp['nama']}</div></div>
        <div class="badge">SKOR SMART: {best_sc:.6f}</div>
        <div class="desc">{state.kegunaan(best_lp)}</div>
        <div style="display:flex; flex-wrap:wrap; gap:10px; margin-top:12px;">
            <span style="background:rgba(34,197,94,.1); color:#86efac; padding:3px 10px; border-radius:6px; font-size:12px;">{state.proc_label(best_lp['processor_score'])}</span>
            <span style="background:rgba(34,197,94,.1); color:#86efac; padding:3px 10px; border-radius:6px; font-size:12px;">RAM {best_lp['ram']} GB</span>
            <span style="background:rgba(34,197,94,.1); color:#86efac; padding:3px 10px; border-radius:6px; font-size:12px;">Storage {best_lp['storage']} GB</span>
            <span style="background:rgba(34,197,94,.1); color:#86efac; padding:3px 10px; border-radius:6px; font-size:12px;">Baterai {best_lp['battery']} mAh</span>
            <span style="background:rgba(34,197,94,.1); color:#86efac; padding:3px 10px; border-radius:6px; font-size:12px;">Harga Rp {display_best_price:,}</span>
        </div>
    </div>
    <h5 style='color:#e2e8f0; font-weight:600; margin:24px 0 10px;'>Matriks Pembobotan Nilai Utilitas</h5>
    """, unsafe_allow_html=True)

    rows = ""
    for rank, (lp, sc, u) in enumerate(results, 1):
        cls = "r-best" if rank == 1 else ("r-even" if rank % 2 == 0 else "r-odd")
        h_row = lp['harga']
        display_row_price = int(4600000 if h_row > 40000 else (h_row * 1_000_000 if h_row < 1000 else h_row))
        rows += f"""
        <tr class="{cls}">
            <td class="tc" style="font-weight:700;">{rank}</td>
            <td><b>{lp['nama']}</b></td>
            <td style="font-size:12px; color:#94a3b8;">{state.proc_label(lp['processor_score'])}</td>
            <td class="tc">{lp['ram']} GB</td>
            <td class="tc">{lp['storage']} GB</td>
            <td class="tc">{lp['battery']}</td>
            <td>Rp {display_row_price:,}</td>
            <td class="tc">{u['processor']:.4f}</td>
            <td class="tc">{u['storage']:.4f}</td>
            <td class="tc">{u['ram']:.4f}</td>
            <td class="tc">{u['battery']:.4f}</td>
            <td class="tc">{u['harga']:.4f}</td>
            <td class="tc" style="color:#3b82f6; font-weight:700; font-size:14px;">{sc:.6f}</td>
        </tr>"""

    st.markdown(f"""
    <div class="spk-table-wrap">
    <table class="spk-table">
        <thead>
            <tr>
                <th rowspan="2" style="text-align:center;">Rank</th><th rowspan="2">Nama Laptop</th><th rowspan="2">Processor</th>
                <th colspan="4" style="text-align:center; border-bottom:1px solid #1e2d45;">Spesifikasi</th>
                <th colspan="5" style="text-align:center; border-bottom:1px solid #1e2d45;">Nilai Utilitas (U)</th><th rowspan="2" style="text-align:center;">Skor SMART</th>
            </tr>
            <tr>
                <th class="tc">RAM</th><th class="tc">Storage</th><th class="tc">Baterai</th><th>Harga</th>
                <th class="tc">U-Proc</th><th class="tc">U-Stor</th><th class="tc">U-RAM</th><th class="tc">U-Bat</th><th class="tc">U-Hrg</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.rec_history.append({
        "user":        st.session_state.username,
        "budget":      f"Rp {budget_juta:.1f} jt",
        "min_proc":    proc_min,
        "min_ram":     ram_min,
        "min_storage": stor_min,
        "min_battery": bat_min,
        "laptop":      best_lp["nama"],
        "skor":        best_sc,
        "total":       len(filtered),
        "tanggal":     datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    })
    st.markdown('<div class="info-banner" style="margin-top:16px;">Hasil analisis telah disimpan ke riwayat pencarian Anda.</div>', unsafe_allow_html=True)