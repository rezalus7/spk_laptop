import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import theme, state

st.set_page_config(page_title="Riwayat — SPK Laptop", page_icon="🕐", layout="wide", initial_sidebar_state="expanded")
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
<p class="section-title">🕐 Riwayat Analisis</p>
<p class="section-sub">Catatan seluruh pencarian rekomendasi laptop selama sesi ini</p>
""", unsafe_allow_html=True)

history = st.session_state.rec_history

# Filter by role: mahasiswa only sees own history
if st.session_state.role != "admin":
    history = [h for h in history if h["user"] == st.session_state.username]

if not history:
    st.markdown("""
    <div style="text-align:center; padding:60px 0; color:#334155;">
        <div style="font-size:48px; margin-bottom:12px;">📭</div>
        <div style="font-size:16px; font-weight:600; color:#475569;">Belum ada riwayat</div>
        <div style="font-size:13px; margin-top:4px;">Jalankan analisis dari Dashboard untuk melihat riwayat di sini.</div>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ── Summary stats ─────────────────────────────────────────
unique_laptops = list(dict.fromkeys(h["laptop"] for h in history))
avg_budget = sum(h["budget"] for h in history) // len(history)

st.markdown(f"""
<div class="mini-grid">
    <div class="mini-card">
        <div class="lbl">Total Pencarian</div>
        <div class="val accent">{len(history)}</div>
    </div>
    <div class="mini-card">
        <div class="lbl">Laptop Unik Muncul</div>
        <div class="val">{len(unique_laptops)}</div>
    </div>
    <div class="mini-card">
        <div class="lbl">Rata-rata Budget</div>
        <div class="val">Rp {avg_budget:,}</div>
    </div>
    <div class="mini-card">
        <div class="lbl">Rekomendasi Terbaru</div>
        <div class="val" style="font-size:13px; color:#60a5fa;">{history[-1]['laptop']}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── History table ─────────────────────────────────────────
rows = ""
for i, d in enumerate(reversed(history), 1):
    cls = "r-even" if i % 2 == 0 else "r-odd"
    rows += f"""
    <tr class="{cls}">
        <td class="tc" style="color:#64748b;">{i}</td>
        <td style="font-family:'Space Mono',monospace; font-size:12px;">{d['user']}</td>
        <td>Rp {d['budget']:,}</td>
        <td class="tc">{d['min_proc']}</td>
        <td class="tc">{d['min_ram']} GB</td>
        <td class="tc">{d['min_storage']} GB</td>
        <td class="tc">{d['min_battery']}</td>
        <td style="color:#4ade80; font-weight:600;">{d['laptop']}</td>
        <td class="tc" style="color:#3b82f6; font-weight:700;">{d['skor']}</td>
        <td class="tc" style="color:#64748b; font-size:12px;">{d['tanggal']}</td>
    </tr>"""

st.markdown(f"""
<div class="spk-table-wrap" style="margin-top:16px;">
<table class="spk-table">
    <thead><tr>
        <th class="tc">No</th>
        <th>User</th>
        <th>Budget</th>
        <th class="tc">Min Proc</th>
        <th class="tc">Min RAM</th>
        <th class="tc">Min Stor</th>
        <th class="tc">Min Bat</th>
        <th>Rekomendasi</th>
        <th class="tc">Skor</th>
        <th class="tc">Waktu</th>
    </tr></thead>
    <tbody>{rows}</tbody>
</table>
</div>
""", unsafe_allow_html=True)

# ── Clear history (admin only) ────────────────────────────
if st.session_state.role == "admin":
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    if st.button("🗑️ Hapus Semua Riwayat", type="secondary", key="clear_hist"):
        st.session_state.rec_history = []
        state.set_flash("ok", "✅ Riwayat berhasil dihapus.")
        st.rerun()
