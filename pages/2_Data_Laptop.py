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
    st.page_link("pages/3_Riwayat.py",     label="🕐 Riwayat",     use_container_width=True)

    st.markdown("<hr style='border-color:#1e2d45; margin:20px 0;'>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        for k in ["logged_in","username","role"]:
            st.session_state[k] = "" if k != "logged_in" else False
        st.switch_page("Beranda.py")

# ── Page header ───────────────────────────────────────────
state.show_flash()
st.markdown("""
<p class="section-title">📋 Master Data Laptop</p>
<p class="section-sub">Daftar seluruh unit laptop yang tersimpan dalam sistem SPK</p>
""", unsafe_allow_html=True)

# ── Table ─────────────────────────────────────────────────
rows = ""
for i, lp in enumerate(st.session_state.laptops):
    cls = "r-even" if i % 2 == 0 else "r-odd"
    p_lbl = state.proc_label(lp["processor_score"]).split(" ")[0]
    rows += f"""
    <tr class="{cls}">
        <td class="tc" style="color:#64748b;">{i+1}</td>
        <td><b>{lp['nama']}</b></td>
        <td style="font-size:12px;">{lp['processor']}</td>
        <td class="tc"><span style="background:rgba(59,130,246,.1); color:#60a5fa;
            padding:2px 8px; border-radius:10px; font-size:12px;">{lp['processor_score']}</span></td>
        <td class="tc">{lp['ram']} GB</td>
        <td class="tc">{lp['storage']} GB</td>
        <td class="tc">{lp['battery']} mAh</td>
        <td style="font-weight:600;">Rp {lp['harga']:,}</td>
    </tr>"""

st.markdown(f"""
<div class="spk-table-wrap">
<table class="spk-table">
    <thead><tr>
        <th class="tc">No</th><th>Nama Laptop</th><th>Processor</th>
        <th class="tc">Score</th><th class="tc">RAM</th>
        <th class="tc">Storage</th><th class="tc">Baterai</th><th>Harga</th>
    </tr></thead>
    <tbody>{rows}</tbody>
</table>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="mini-grid" style="margin-top:16px;">
    <div class="mini-card">
        <div class="lbl">Total Laptop</div>
        <div class="val accent">{len(st.session_state.laptops)}</div>
    </div>
    <div class="mini-card">
        <div class="lbl">Harga Terendah</div>
        <div class="val">Rp {min(l['harga'] for l in st.session_state.laptops):,}</div>
    </div>
    <div class="mini-card">
        <div class="lbl">Harga Tertinggi</div>
        <div class="val">Rp {max(l['harga'] for l in st.session_state.laptops):,}</div>
    </div>
    <div class="mini-card">
        <div class="lbl">RAM Terbesar</div>
        <div class="val">{max(l['ram'] for l in st.session_state.laptops)} GB</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Admin-only CRUD ───────────────────────────────────────
if st.session_state.role != "admin":
    st.markdown("""
    <div class="info-banner" style="margin-top:20px;">
        ℹ️ Akun <b>Mahasiswa</b> hanya dapat melihat data. Login sebagai admin untuk mengelola data.
    </div>""", unsafe_allow_html=True)
    st.stop()

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
st.markdown("<p class='section-title' style='font-size:17px;'>🛠️ Kelola Data (Admin)</p>", unsafe_allow_html=True)

tab_add, tab_edit, tab_del = st.tabs(["➕ Tambah Laptop", "✏️ Edit Data", "🗑️ Hapus Data"])

# ── TAB ADD ───────────────────────────────────────────────
with tab_add:
    with st.form("f_add", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            nm = st.text_input("Nama Seri Laptop *")
            pr = st.text_input("Model Processor *")
            ps = st.number_input("Skor Processor (0–100)", 0, 100, 70)
        with c2:
            rm  = st.number_input("RAM (GB)", 1, 128, 8)
            st2 = st.number_input("Storage (GB)", 128, 4096, 512)
            bt  = st.number_input("Baterai (mAh)", 1000, 15000, 4000)
            hg  = st.number_input("Harga (Rp)", 1_000_000, 100_000_000, 8_000_000, step=100_000)

        submitted = st.form_submit_button("💾 Tambahkan ke Database", use_container_width=True, type="primary")

    if submitted:
        if not nm.strip() or not pr.strip():
            state.set_flash("warn", "⚠️ Nama dan Processor wajib diisi.")
        else:
            st.session_state.laptops.append({
                "nama": nm.strip(), "processor": pr.strip(), "processor_score": ps,
                "ram": rm, "storage": st2, "battery": bt, "harga": hg
            })
            state.set_flash("ok", f'✅ Laptop "{nm}" berhasil ditambahkan.')
        st.rerun()

# ── TAB EDIT ──────────────────────────────────────────────
with tab_edit:
    names = [f"{i+1}. {l['nama']}" for i, l in enumerate(st.session_state.laptops)]
    sel = st.selectbox("Pilih laptop yang akan diubah", names, key="sel_edit")
    idx = int(sel.split(".")[0]) - 1
    lp  = st.session_state.laptops[idx]

    with st.form("f_edit"):
        c1, c2 = st.columns(2)
        with c1:
            nm = st.text_input("Nama Seri Laptop", value=lp["nama"])
            pr = st.text_input("Model Processor",  value=lp["processor"])
            ps = st.number_input("Skor Processor", 0, 100, lp["processor_score"])
        with c2:
            rm  = st.number_input("RAM (GB)",      1, 128,       lp["ram"])
            st2 = st.number_input("Storage (GB)",  128, 4096,    lp["storage"])
            bt  = st.number_input("Baterai (mAh)", 1000, 15000,  lp["battery"])
            hg  = st.number_input("Harga (Rp)",    1_000_000, 100_000_000, lp["harga"], step=100_000)

        upd = st.form_submit_button("📝 Simpan Perubahan", use_container_width=True, type="primary")

    if upd:
        st.session_state.laptops[idx] = {
            "nama": nm, "processor": pr, "processor_score": ps,
            "ram": rm, "storage": st2, "battery": bt, "harga": hg
        }
        state.set_flash("ok", f'✅ Data "{nm}" berhasil diperbarui.')
        st.rerun()

# ── TAB DELETE ────────────────────────────────────────────
with tab_del:
    names = [f"{i+1}. {l['nama']}" for i, l in enumerate(st.session_state.laptops)]
    sel2 = st.selectbox("Pilih laptop yang akan dihapus", names, key="sel_del")
    idx2 = int(sel2.split(".")[0]) - 1
    target_name = st.session_state.laptops[idx2]["nama"]

    st.markdown(f"""
    <div style="background:#2a0a0a; border:1px solid #7f1d1d; color:#fca5a5;
                border-radius:8px; padding:12px 16px; font-size:13px; margin:10px 0;">
        ⚠️ Anda akan menghapus permanen: <b>{target_name}</b>. Tindakan ini tidak dapat dibatalkan.
    </div>""", unsafe_allow_html=True)

    if st.button(f"❌ Hapus '{target_name}'", type="primary", use_container_width=True, key="del_btn"):
        st.session_state.laptops.pop(idx2)
        state.set_flash("ok", f'🗑️ "{target_name}" berhasil dihapus.')
        st.rerun()
