import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import theme, state
import io, base64
from datetime import datetime

st.set_page_config(page_title="Riwayat — SPK Laptop", page_icon="🕐", layout="wide", initial_sidebar_state="expanded")
theme.inject()
state.init_state()

if not st.session_state.logged_in:
    st.switch_page("Beranda.py")

# ── PDF Generator (pure Python, no external lib) ──────────
def generate_pdf_bytes(history, username, role):
    """
    Buat PDF sederhana pakai struktur bytes langsung (tanpa library eksternal).
    Menggunakan fpdf2 jika ada, fallback ke HTML-based download jika tidak.
    """
    try:
        from fpdf import FPDF
        _use_fpdf = True
    except ImportError:
        _use_fpdf = False

    if _use_fpdf:
        return _pdf_fpdf(history, username, role)
    else:
        return None  # akan pakai HTML fallback

def _pdf_fpdf(history, username, role):
    from fpdf import FPDF

    class PDF(FPDF):
        def header(self):
            self.set_fill_color(30, 58, 95)
            self.rect(0, 0, 210, 28, 'F')
            self.set_font('Helvetica', 'B', 16)
            self.set_text_color(255, 255, 255)
            self.cell(0, 10, 'LAPORAN RIWAYAT REKOMENDASI SPK LAPTOP', 0, 1, 'C')
            self.set_font('Helvetica', 'I', 9)
            self.cell(0, 5, f'Dicetak oleh: {username} ({role.upper()}) | Tanggal: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}', 0, 1, 'C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Halaman {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Helvetica', '', 10)
    
    # Render Tabel di PDF
    pdf.set_fill_color(240, 244, 248)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(10, 8, 'No', 1, 0, 'C', True)
    pdf.cell(25, 8, 'User', 1, 0, 'C', True)
    pdf.cell(25, 8, 'Budget', 1, 0, 'C', True)
    pdf.cell(20, 8, 'Min RAM', 1, 0, 'C', True)
    pdf.cell(25, 8, 'Min Stor', 1, 0, 'C', True)
    pdf.cell(50, 8, 'Rekomendasi Terbaik', 1, 0, 'C', True)
    pdf.cell(30, 8, 'Skor SMART', 1, 1, 'C', True)
    
    pdf.set_font('Helvetica', '', 9)
    for i, d in enumerate(history, 1):
        # Normalisasi parsing budget untuk teks PDF
        b_val = d['budget']
        if isinstance(b_val, str):
            b_text = b_val
        else:
            b_text = f"Rp {b_val:,}" if b_val > 100000 else f"Rp {b_val:.1f} jt"

        pdf.cell(10, 7, str(i), 1, 0, 'C')
        pdf.cell(25, 7, str(d['user']), 1, 0, 'L')
        pdf.cell(25, 7, b_text, 1, 0, 'R')
        pdf.cell(20, 7, f"{d['min_ram']} GB", 1, 0, 'C')
        pdf.cell(25, 7, f"{d['min_storage']} GB", 1, 0, 'C')
        pdf.cell(50, 7, str(d['laptop']), 1, 0, 'L')
        pdf.cell(30, 7, f"{d['skor']:.6f}", 1, 1, 'C')
        
    return pdf.output(dest='S')

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
st.markdown('<p class="section-title">🕐 Riwayat Pencarian SPK</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Daftar log data pencarian rekomendasi laptop yang dilakukan oleh pengguna</p>', unsafe_allow_html=True)

state.show_flash()

# Filter riwayat (Admin bisa lihat semua, Mahasiswa hanya riwayat miliknya)
if st.session_state.role == "admin":
    history = st.session_state.rec_history
else:
    history = [h for h in st.session_state.rec_history if h["user"] == st.session_state.username]

if not history:
    st.markdown("""
    <div style="background:rgba(59,130,246,0.05); border:1px solid rgba(59,130,246,0.15); 
        color:#94a3b8; padding:20px; border-radius:12px; text-align:center; font-size:14px;">
        🍃 Belum ada riwayat pencarian rekomendasi yang tersimpan di dalam sistem.
    </div>""", unsafe_allow_html=True)
    st.stop()

# ── PERBAIKAN UTAMA: Perhitungan Statistik secara Aman & Valid ──
parsed_budgets = []
for h in history:
    b_val = h.get("budget", 0)
    if isinstance(b_val, (int, float)):
        # Jika sudah berupa angka murni
        parsed_budgets.append(b_val if b_val > 100000 else b_val * 1_000_000)
    elif isinstance(b_val, str):
        try:
            # Membersihkan string teks "Rp 35.0 jt" -> menjadi float desimal murni
            clean_str = b_val.replace("Rp", "").replace("jt", "").replace(",", "").strip()
            parsed_budgets.append(float(clean_str) * 1_000_000)
        except ValueError:
            parsed_budgets.append(0)
    else:
        parsed_budgets.append(0)

# Kalkulasi statistik rata-rata akhir budget secara aman
avg_budget = int(sum(parsed_budgets) // len(history)) if len(history) > 0 else 0

# Tampilkan Statistik Mini Grid
st.markdown(f"""
<div class="mini-grid">
    <div class="mini-card">
        <div class="lbl">Total Log Pencarian</div>
        <div class="val accent">{len(history)} Kali</div>
    </div>
    <div class="mini-card">
        <div class="lbl">Rata-rata Budget Dicari</div>
        <div class="val">Rp {avg_budget:,}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Menu Aksi Cetak PDF / Hapus ───────────────────────────
c1, c2 = st.columns([1, 4])
with c1:
    pdf_bytes = generate_pdf_bytes(history, st.session_state.username, st.session_state.role)
    if pdf_bytes:
        st.download_button(
            label="📄 Cetak PDF",
            data=pdf_bytes,
            file_name=f"Riwayat_SPK_{st.session_state.username}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        # Fallback HTML Link Download jika FPDF tidak terinstall
        st.markdown("<p style='font-size:12px; color:#64748b;'>Instal fpdf2 untuk export PDF</p>", unsafe_allow_html=True)

with c2:
    if st.session_state.role == "admin":
        if st.button("🗑️ Kosongkan Semua Riwayat Log", type="secondary"):
            st.session_state.rec_history = []
            state.set_flash("ok", "✅ Seluruh log data riwayat berhasil dikosongkan.")
            st.rerun()

# ── Render Tabel Riwayat Log ──────────────────────────────
st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
rows = ""
for i, d in enumerate(reversed(history), 1):
    cls = "r-even" if i % 2 == 0 else "r-odd"
    
    # Pengkondisian tampilan teks budget agar rapi di layar
    b_val = d['budget']
    if isinstance(b_val, str):
        b_display = b_val
    else:
        b_display = f"Rp {b_val:,}" if b_val > 100000 else f"Rp {b_val:.1f} jt"

    rows += f"""
    <tr class="{cls}">
        <td class="tc" style="color:#64748b;">{i}</td>
        <td style="font-family:'Space Mono',monospace; font-size:12px; color:#94a3b8;">{d['user']}</td>
        <td>{b_display}</td>
        <td class="tc"><span style="background:rgba(59,130,246,.1); color:#60a5fa; padding:2px 8px; border-radius:10px;">{state.proc_label(d['min_proc'])}</span></td>
        <td class="tc">{d['min_ram']} GB</td>
        <td class="tc">{d['min_storage']} GB</td>
        <td class="tc">{d['min_battery']} mAh</td>
        <td style="color:#4ade80; font-weight:600;">{d['laptop']}</td>
        <td class="tc" style="color:#3b82f6; font-weight:700;">{d['skor']:.6f}</td>
        <td class="tc" style="color:#64748b; font-size:12px;">{d['tanggal']}</td>
    </tr>"""

st.markdown(f"""
<div class="spk-table-wrap">
<table class="spk-table">
    <thead>
        <tr>
            <th class="tc" width="40">No</th>
            <th>Oleh User</th>
            <th>Kriteria Budget</th>
            <th class="tc">Min Proc</th>
            <th class="tc">Min RAM</th>
            <th class="tc">Min Storage</th>
            <th class="tc">Min Baterai</th>
            <th>Rekomendasi Terbaik</th>
            <th class="tc">Skor Akhir</th>
            <th class="tc">Waktu Cari</th>
        </tr>
    </thead>
    <tbody>{rows}</tbody>
</table>
</div>
""", unsafe_allow_html=True)