import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import theme, state

st.set_page_config(page_title="Data Laptop — SPK", page_icon="📋", layout="wide", initial_sidebar_state="expanded")
theme.inject()
state.init_state()

if not st.session_state.logged_in:
    st.switch_page("Beranda.py")

# ── Sidebar ───────────────────────────────────────────────
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
    st.page_link("pages/3_Riwayat.py",     label="🕐 Riwayat SPK",  use_container_width=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚪 Keluar Sistem", use_container_width=True, type="secondary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()

# ── Header Halaman ───────────────────────────────────────
st.markdown('<p class="section-title">📋 Master Data Laptop</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Daftar seluruh unit laptop yang tersimpan dalam sistem SPK</p>', unsafe_allow_html=True)

state.show_flash()

# Pisahkan hak akses (Admin punya Tab Tambah/Edit/Hapus, Mahasiswa hanya Lihat Data)
if st.session_state.role == "admin":
    tab_view, tab_add, tab_edit, tab_del = st.tabs([
        "🔍 Lihat Data", "➕ Tambah Laptop", "📝 Edit Data", "❌ Hapus Laptop"
    ])
else:
    tab_view = st.tabs(["🔍 Lihat Data"])[0]
    tab_add = tab_edit = tab_del = None

# ── TAB VIEW DATA ─────────────────────────────────────────
with tab_view:
    rows = ""
    for i, lp in enumerate(st.session_state.laptops):
        cls = "r-even" if i % 2 == 0 else "r-odd"
        
        p_name = lp.get('processor', '').strip()
        if not p_name:
            p_name = state.proc_label(lp['processor_score'])
            
        # Konversi nilai harga ke Rupiah penuh jika nilai di database berupa desimal kecil
        raw_price = lp['harga']
        display_price = int(raw_price * 1_000_000) if raw_price < 1000 else int(raw_price)

        rows += f"""
        <tr class="{cls}">
            <td class="tc" style="color:#64748b;">{i+1}</td>
            <td><b>{lp['nama']}</b></td>
            <td style="font-size:12px;">{p_name}</td>
            <td class="tc"><span style="background:rgba(59,130,246,.1); color:#60a5fa;
                padding:2px 8px; border-radius:10px; font-size:12px;">{lp['processor_score']}</span></td>
            <td class="tc">{lp['ram']} GB</td>
            <td class="tc">{lp['storage']} GB</td>
            <td class="tc">{lp['battery']} mAh</td>
            <td style="font-weight:600;">Rp {display_price:,}</td>
        </tr>"""

    st.markdown(f"""
    <div class="spk-table-wrap">
    <table class="spk-table">
        <thead>
            <tr>
                <th class="tc" width="40">No</th>
                <th>Nama / Model Laptop</th>
                <th>Processor</th>
                <th class="tc">Skor Proc</th>
                <th class="tc">RAM</th>
                <th class="tc">Storage</th>
                <th class="tc">Baterai</th>
                <th>Harga</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

# ── TAB ADD DATA (ADMIN) ──────────────────────────────────
if tab_add:
    with tab_add:
        with st.form("form_add_laptop", clear_on_submit=True):
            st.markdown("<p style='font-weight:600; font-size:15px; margin-bottom:12px;'>Tambah Unit Laptop Baru</p>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                nm = st.text_input("Nama / Seri Laptop", placeholder="Contoh: ASUS Vivobook 14")
                pr = st.text_input("Model Processor", placeholder="Contoh: Intel Core i5-1240P")
                ps = st.number_input("Skor Benchmark Processor (40 - 100)", 40, 100, 70)
            with c2:
                rm = st.selectbox("Kapasitas RAM", [4, 8, 12, 16, 32], index=1, format_func=lambda x: f"{x} GB")
                st2 = st.selectbox("Kapasitas Storage", [128, 256, 512, 1024, 2048], index=2, format_func=lambda x: f"{x} GB")
                bt = st.number_input("Kapasitas Baterai (mAh)", 1000, 15000, 4000, step=100)
                # MENGGUNAKAN NOMINAL RUPIAH PENH (Contoh: 35000000)
                hg = st.number_input("Harga Laptop (Rupiah Penuh)", 500000, 150000000, 10000000, step=100000)
            
            sub = st.form_submit_button("➕ Tambahkan ke Sistem", use_container_width=True, type="primary")

        if sub:
            if not nm.strip():
                state.set_flash("warn", "⚠️ Nama laptop tidak boleh kosong.")
                st.rerun()
            else:
                # Simpan nilai harga ke session state dalam bentuk nominal penuh
                st.session_state.laptops.append({
                    "nama": nm.strip(), "processor": pr.strip(), "processor_score": ps,
                    "ram": rm, "storage": st2, "battery": bt, "harga": float(hg)
                })
                state.set_flash("ok", f'✅ Laptop "{nm.strip()}" berhasil ditambahkan.')
                st.rerun()

# ── TAB EDIT DATA (ADMIN) ─────────────────────────────────
if tab_edit:
    with tab_edit:
        names = [f"{i+1}. {l['nama']}" for i, l in enumerate(st.session_state.laptops)]
        sel = st.selectbox("Pilih laptop yang ingin diedit", names, key="sel_edit")
        
        idx = int(sel.split(".")[0]) - 1
        lp = st.session_state.laptops[idx]

        # Penyesuaian nilai default harga pada form edit data
        current_price = lp["harga"]
        if current_price < 1000:
            current_price = current_price * 1_000_000

        with st.form("form_edit_laptop"):
            c1, c2 = st.columns(2)
            with c1:
                nm = st.text_input("Nama / Seri Laptop", value=lp["nama"])
                pr = st.text_input("Model Processor", value=lp.get("processor", ""))
                ps = st.number_input("Skor Benchmark Processor (40 - 100)", 40, 100, int(lp["processor_score"]))
            with c2:
                ram_opts = [4, 8, 12, 16, 32]
                r_idx = ram_opts.index(lp["ram"]) if lp["ram"] in ram_opts else 1
                rm = st.selectbox("Kapasitas RAM", ram_opts, index=r_idx, format_func=lambda x: f"{x} GB")
                
                stor_opts = [128, 256, 512, 1024, 2048]
                s_idx = stor_opts.index(lp["storage"]) if lp["storage"] in stor_opts else 2
                st2 = st.selectbox("Kapasitas Storage", stor_opts, index=s_idx, format_func=lambda x: f"{x} GB")
                
                bt = st.number_input("Baterai (mAh)", 1000, 15000, int(lp["battery"]))
                # MENGGUNAKAN NOMINAL RUPIAH PENUH (Contoh: 35000000)
                hg = st.number_input("Harga Laptop (Rupiah Penuh)", 500000, 150000000, int(current_price), step=100000)

            upd = st.form_submit_button("📝 Simpan Perubahan", use_container_width=True, type="primary")

        if upd:
            st.session_state.laptops[idx] = {
                "nama": nm.strip(), "processor": pr.strip(), "processor_score": ps,
                "ram": rm, "storage": st2, "battery": bt, "harga": float(hg)
            }
            state.set_flash("ok", f'✅ Data "{nm.strip()}" berhasil diperbarui.')
            st.rerun()

# ── TAB DELETE (ADMIN) ────────────────────────────────────
if tab_del:
    with tab_del:
        names = [f"{i+1}. {l['nama']}" for i, l in enumerate(st.session_state.laptops)]
        sel2 = st.selectbox("Pilih laptop yang akan dihapus", names, key="sel_del")
        
        idx2 = int(sel2.split(".")[0]) - 1
        target_name = st.session_state.laptops[idx2]["nama"]

        st.markdown(f"""
        <div style="background:#2a0a0a; border:1px solid #7f1d1d; color:#f87171; 
            padding:16px; border-radius:12px; margin-bottom:20px; font-size:14px;">
            ⚠️ <b>Peringatan Penting:</b> Anda akan menghapus unit <b>{target_name}</b> secara permanen dari basis data sistem SPK ini. Tindakan ini tidak dapat dibatalkan.
        </div>""", unsafe_allow_html=True)

        if st.button("❌ Hapus Permanen", use_container_width=True, type="primary"):
            st.session_state.laptops.pop(idx2)
            state.set_flash("ok", f'🗑️ Laptop "{target_name}" berhasil dihapus dari sistem.')
            st.rerun()