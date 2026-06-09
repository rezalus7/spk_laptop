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
            self.set_y(7)
            self.cell(0, 8, 'SPK LAPTOP - METODE SMART', align='C', new_x='LMARGIN', new_y='NEXT')
            self.set_font('Helvetica', '', 9)
            self.set_text_color(148, 163, 184)
            self.cell(0, 6, 'Sistem Pendukung Keputusan Pemilihan Laptop', align='C', new_x='LMARGIN', new_y='NEXT')
            self.ln(4)

        def footer(self):
            self.set_y(-12)
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(148, 163, 184)
            self.cell(0, 10, f'Halaman {self.page_no()} | Digenerate otomatis oleh SPK Laptop', align='C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(15, 32, 15)

    now_str = datetime.now().strftime("%d %B %Y, %H:%M:%S")

    # Meta info
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(30, 64, 175)
    pdf.cell(0, 7, 'Laporan Riwayat Analisis', new_x='LMARGIN', new_y='NEXT')
    pdf.set_draw_color(59, 130, 246)
    pdf.set_line_width(0.4)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(3)

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 5, f'Dicetak oleh : {username} ({role.upper()})', new_x='LMARGIN', new_y='NEXT')
    pdf.cell(0, 5, f'Tanggal cetak: {now_str}', new_x='LMARGIN', new_y='NEXT')
    pdf.cell(0, 5, f'Total data   : {len(history)} analisis', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(5)

    # Summary stats
    if history:
        unique_laptops = len(set(h["laptop"] for h in history))
        avg_budget = sum(h["budget"] for h in history) // len(history)
        best = max(history, key=lambda x: x["skor"])

        stats = [
            ("Total Pencarian", str(len(history))),
            ("Laptop Unik", str(unique_laptops)),
            ("Rata-rata Budget", f"Rp {avg_budget:,}"),
            ("Skor Terbaik", str(best["skor"])),
        ]
        col_w = 180 / 4
        pdf.set_font('Helvetica', 'B', 8)
        pdf.set_fill_color(30, 58, 95)
        pdf.set_text_color(255, 255, 255)
        for lbl, _ in stats:
            pdf.cell(col_w, 7, lbl, border=1, align='C', fill=True)
        pdf.ln()
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_fill_color(239, 246, 255)
        pdf.set_text_color(30, 64, 175)
        for _, val in stats:
            pdf.cell(col_w, 9, val, border=1, align='C', fill=True)
        pdf.ln(12)

    # Table header
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(30, 64, 175)
    pdf.cell(0, 6, 'Detail Riwayat Analisis', new_x='LMARGIN', new_y='NEXT')
    pdf.set_draw_color(59, 130, 246)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(3)

    cols      = ["No","User","Budget","Proc","RAM","Stor","Bat","Rekomendasi","Skor"]
    col_widths = [8, 22, 28, 12, 14, 14, 14, 52, 16]

    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.set_fill_color(30, 58, 95)
    pdf.set_text_color(255, 255, 255)
    pdf.set_draw_color(203, 213, 225)
    pdf.set_line_width(0.3)
    for c, w in zip(cols, col_widths):
        pdf.cell(w, 7, c, border=1, align='C', fill=True)
    pdf.ln()

    pdf.set_font('Helvetica', '', 7.5)
    for i, d in enumerate(reversed(history), 1):
        fill = i % 2 == 0
        pdf.set_fill_color(248, 250, 252) if fill else pdf.set_fill_color(255, 255, 255)

        row = [
            str(i), d["user"], f"Rp {d['budget']:,}",
            str(d["min_proc"]), f"{d['min_ram']}G", f"{d['min_storage']}G",
            str(d["min_battery"]), d["laptop"], str(d["skor"]),
        ]
        aligns = ['C','L','L','C','C','C','C','L','C']
        for j, (val, w, al) in enumerate(zip(row, col_widths, aligns)):
            if j == 7:  # rekomendasi — hijau
                pdf.set_text_color(21, 128, 61)
                pdf.set_font('Helvetica', 'B', 7.5)
            elif j == 8:  # skor — biru
                pdf.set_text_color(29, 78, 216)
                pdf.set_font('Helvetica', 'B', 7.5)
            else:
                pdf.set_text_color(51, 65, 85)
                pdf.set_font('Helvetica', '', 7.5)
            pdf.cell(w, 6.5, val, border=1, align=al, fill=fill)
        pdf.ln()

    return bytes(pdf.output())


def generate_html_report(history, username, role):
    """Fallback: buat HTML yang bisa diprint/save sebagai PDF dari browser."""
    now_str = datetime.now().strftime("%d %B %Y, %H:%M:%S")
    rows_html = ""
    for i, d in enumerate(reversed(history), 1):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        rows_html += f"""
        <tr style="background:{bg}">
            <td style="text-align:center;color:#64748b">{i}</td>
            <td>{d['user']}</td>
            <td>Rp {d['budget']:,}</td>
            <td style="text-align:center">{d['min_proc']}</td>
            <td style="text-align:center">{d['min_ram']} GB</td>
            <td style="text-align:center">{d['min_storage']} GB</td>
            <td style="text-align:center">{d['min_battery']}</td>
            <td style="color:#15803d;font-weight:600">{d['laptop']}</td>
            <td style="text-align:center;color:#1d4ed8;font-weight:700">{d['skor']}</td>
            <td style="text-align:center;color:#64748b;font-size:11px">{d['tanggal']}</td>
        </tr>"""

    unique_laptops = len(set(h["laptop"] for h in history))
    avg_budget = sum(h["budget"] for h in history) // len(history)
    best = max(history, key=lambda x: x["skor"])

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Riwayat SPK Laptop</title>
<style>
  @page {{ size: A4 landscape; margin: 15mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; background: #fff; }}
  .header {{ background: #1e3a5f; color: white; padding: 16px 24px; border-radius: 8px; margin-bottom: 16px; }}
  .header h1 {{ margin:0; font-size:20px; letter-spacing:2px; }}
  .header p  {{ margin:4px 0 0; font-size:11px; color:#94a3b8; }}
  .meta {{ font-size:11px; color:#475569; margin-bottom:16px; line-height:1.8; }}
  .stats {{ display:flex; gap:12px; margin-bottom:20px; }}
  .stat-card {{ flex:1; border:1px solid #bfdbfe; border-radius:8px; padding:10px 14px; background:#eff6ff; text-align:center; }}
  .stat-card .lbl {{ font-size:10px; color:#64748b; font-weight:600; text-transform:uppercase; }}
  .stat-card .val {{ font-size:18px; font-weight:700; color:#1e40af; margin-top:4px; }}
  table {{ width:100%; border-collapse:collapse; font-size:11px; }}
  thead tr {{ background:#1e3a5f; color:white; }}
  th {{ padding:8px 6px; text-align:center; font-weight:600; font-size:10px; text-transform:uppercase; letter-spacing:0.5px; }}
  td {{ padding:6px 6px; border-bottom:1px solid #e2e8f0; }}
  .footer {{ margin-top:20px; font-size:9px; color:#94a3b8; text-align:center; border-top:1px solid #e2e8f0; padding-top:10px; }}
  @media print {{ body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }} }}
</style>
</head>
<body>
<div class="header">
  <h1>💻 SPK LAPTOP — METODE SMART</h1>
  <p>Sistem Pendukung Keputusan Pemilihan Laptop</p>
</div>
<div class="meta">
  <b>Laporan Riwayat Analisis</b><br>
  Dicetak oleh : <b>{username}</b> ({role.upper()})<br>
  Tanggal cetak: {now_str}<br>
  Total data   : <b>{len(history)}</b> analisis
</div>
<div class="stats">
  <div class="stat-card"><div class="lbl">Total Pencarian</div><div class="val">{len(history)}</div></div>
  <div class="stat-card"><div class="lbl">Laptop Unik</div><div class="val">{unique_laptops}</div></div>
  <div class="stat-card"><div class="lbl">Rata-rata Budget</div><div class="val">Rp {avg_budget:,}</div></div>
  <div class="stat-card"><div class="lbl">Skor Terbaik</div><div class="val">{best['skor']}</div></div>
</div>
<table>
  <thead>
    <tr>
      <th>No</th><th>User</th><th>Budget</th>
      <th>Min Proc</th><th>Min RAM</th><th>Min Stor</th><th>Min Bat</th>
      <th>Rekomendasi</th><th>Skor</th><th>Waktu</th>
    </tr>
  </thead>
  <tbody>{rows_html}</tbody>
</table>
<div class="footer">Dokumen ini digenerate otomatis oleh Sistem SPK Laptop — Metode SMART</div>
</body>
</html>"""
    return html.encode("utf-8")


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

# Filter by role
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
    <div class="mini-card"><div class="lbl">Total Pencarian</div><div class="val accent">{len(history)}</div></div>
    <div class="mini-card"><div class="lbl">Laptop Unik Muncul</div><div class="val">{len(unique_laptops)}</div></div>
    <div class="mini-card"><div class="lbl">Rata-rata Budget</div><div class="val">Rp {avg_budget:,}</div></div>
    <div class="mini-card"><div class="lbl">Rekomendasi Terbaru</div><div class="val" style="font-size:13px;color:#60a5fa;">{history[-1]['laptop']}</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ── Download buttons ──────────────────────────────────────
now_fn = datetime.now().strftime("%Y%m%d_%H%M%S")

col_pdf, col_html, col_clear = st.columns([1, 1, 1]) if st.session_state.role == "admin" else st.columns([1, 1, 2])

with col_pdf:
    # Coba fpdf2 dulu
    pdf_bytes = generate_pdf_bytes(history, st.session_state.username, st.session_state.role)
    if pdf_bytes:
        st.download_button(
            label="⬇️ Unduh PDF",
            data=pdf_bytes,
            file_name=f"riwayat_spk_{now_fn}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary",
            help="Unduh laporan dalam format PDF",
        )
    else:
        st.markdown("""
        <div class="info-banner" style="font-size:12px; padding:8px 12px;">
            Install <code>fpdf2</code> untuk unduh PDF native.
        </div>""", unsafe_allow_html=True)

with col_html:
    html_bytes = generate_html_report(history, st.session_state.username, st.session_state.role)
    st.download_button(
        label="🖨️ Unduh / Print HTML",
        data=html_bytes,
        file_name=f"riwayat_spk_{now_fn}.html",
        mime="text/html",
        use_container_width=True,
        type="secondary",
        help="Unduh sebagai HTML — buka di browser lalu Ctrl+P untuk save PDF",
    )

if st.session_state.role == "admin":
    with col_clear:
        if st.button("🗑️ Hapus Semua Riwayat", type="secondary", use_container_width=True, key="clear_hist"):
            st.session_state.rec_history = []
            state.set_flash("ok", "✅ Riwayat berhasil dihapus.")
            st.rerun()

# ── History table ─────────────────────────────────────────
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
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
<div class="spk-table-wrap" style="margin-top:8px;">
<table class="spk-table">
    <thead><tr>
        <th class="tc">No</th><th>User</th><th>Budget</th>
        <th class="tc">Min Proc</th><th class="tc">Min RAM</th>
        <th class="tc">Min Stor</th><th class="tc">Min Bat</th>
        <th>Rekomendasi</th><th class="tc">Skor</th><th class="tc">Waktu</th>
    </tr></thead>
    <tbody>{rows}</tbody>
</table>
</div>
""", unsafe_allow_html=True)