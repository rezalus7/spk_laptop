import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import theme, state
import io
from datetime import datetime

st.set_page_config(page_title="Riwayat — SPK Laptop", page_icon="🕐", layout="wide", initial_sidebar_state="expanded")
theme.inject()
state.init_state()

if not st.session_state.logged_in:
    st.switch_page("Beranda.py")

# ── PDF Generator ─────────────────────────────────────────
def generate_pdf_riwayat(history, username, role):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    buffer = io.BytesIO()
    W, H = A4
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=20*mm, leftMargin=20*mm,
        topMargin=20*mm, bottomMargin=20*mm,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('CT', parent=styles['Normal'], fontSize=18,
        fontName='Helvetica-Bold', textColor=colors.HexColor('#1e3a5f'),
        alignment=TA_CENTER, spaceAfter=4)
    subtitle_style = ParagraphStyle('CS', parent=styles['Normal'], fontSize=10,
        fontName='Helvetica', textColor=colors.HexColor('#64748b'),
        alignment=TA_CENTER, spaceAfter=2)
    meta_style = ParagraphStyle('CM', parent=styles['Normal'], fontSize=9,
        fontName='Helvetica', textColor=colors.HexColor('#475569'),
        alignment=TA_LEFT, spaceAfter=3)
    section_style = ParagraphStyle('CSec', parent=styles['Normal'], fontSize=11,
        fontName='Helvetica-Bold', textColor=colors.HexColor('#1e40af'), spaceAfter=6)
    footer_style = ParagraphStyle('CF', parent=styles['Normal'], fontSize=8,
        textColor=colors.HexColor('#94a3b8'), alignment=TA_CENTER)

    story = []

    # ── Header ─────────────────────────────────────────────
    story.append(Paragraph("SPK LAPTOP — METODE SMART", title_style))
    story.append(Paragraph("Sistem Pendukung Keputusan Pemilihan Laptop", subtitle_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#3b82f6')))
    story.append(Spacer(1, 8))

    # ── Meta info ──────────────────────────────────────────
    now_str = datetime.now().strftime("%d %B %Y, %H:%M:%S")
    story.append(Paragraph("Laporan Riwayat Analisis", section_style))
    story.append(Paragraph(f"Dicetak oleh : <b>{username}</b> ({role.upper()})", meta_style))
    story.append(Paragraph(f"Tanggal cetak: {now_str}", meta_style))
    story.append(Paragraph(f"Total data   : <b>{len(history)}</b> analisis", meta_style))
    story.append(Spacer(1, 10))

    # ── Summary stats ──────────────────────────────────────
    if history:
        unique_laptops = len(set(h["laptop"] for h in history))
        avg_budget = sum(h["budget"] for h in history) // len(history)
        best = max(history, key=lambda x: x["skor"])

        stat_data = [
            ["Total Pencarian", "Laptop Unik", "Rata-rata Budget", "Skor Terbaik"],
            [str(len(history)), str(unique_laptops), f"Rp {avg_budget:,}", str(best["skor"])],
        ]
        cw = (W - 40*mm) / 4
        stat_tbl = Table(stat_data, colWidths=[cw]*4)
        stat_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a5f')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 9),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ROWHEIGHT', (0,0), (-1,-1), 24),
            ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#eff6ff')),
            ('TEXTCOLOR', (0,1), (-1,1), colors.HexColor('#1e40af')),
            ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,1), (-1,1), 12),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bfdbfe')),
        ]))
        story.append(stat_tbl)
        story.append(Spacer(1, 16))

    # ── Main table ─────────────────────────────────────────
    story.append(Paragraph("Detail Riwayat Analisis", section_style))

    col_widths = [10*mm, 22*mm, 28*mm, 14*mm, 14*mm, 14*mm, 14*mm, 43*mm, 12*mm]
    header = ["No", "User", "Budget", "Min\nProc", "Min\nRAM", "Min\nStor", "Min\nBat", "Rekomendasi", "Skor"]
    table_data = [header]

    for i, d in enumerate(reversed(history), 1):
        table_data.append([
            str(i),
            d["user"],
            f"Rp {d['budget']:,}",
            str(d["min_proc"]),
            f"{d['min_ram']} GB",
            f"{d['min_storage']} GB",
            str(d["min_battery"]),
            d["laptop"],
            str(d["skor"]),
        ])

    tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
    row_styles = [
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 7.5),
        ('ROWHEIGHT', (0,0), (-1,-1), 18),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#cbd5e1')),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (7,1), (7,-1), 'LEFT'),
        ('ALIGN', (2,1), (2,-1), 'LEFT'),
    ]
    for r in range(1, len(table_data)):
        bg = colors.HexColor('#f8fafc') if r % 2 == 0 else colors.white
        row_styles.append(('BACKGROUND', (0,r), (-1,r), bg))
        row_styles.append(('TEXTCOLOR', (8,r), (8,r), colors.HexColor('#1d4ed8')))
        row_styles.append(('FONTNAME', (8,r), (8,r), 'Helvetica-Bold'))
        row_styles.append(('TEXTCOLOR', (7,r), (7,r), colors.HexColor('#15803d')))

    tbl.setStyle(TableStyle(row_styles))
    story.append(tbl)

    # ── Footer ─────────────────────────────────────────────
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e1')))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Dokumen ini digenerate otomatis oleh Sistem SPK Laptop — Metode SMART",
        footer_style,
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


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

# ── Download PDF button ───────────────────────────────────
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

col_dl, col_clear = st.columns([1, 1]) if st.session_state.role == "admin" else (st.columns([1, 2]))

with col_dl:
    try:
        pdf_bytes = generate_pdf_riwayat(
            history,
            st.session_state.username,
            st.session_state.role,
        )
        now_fn = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button(
            label="⬇️ Unduh Laporan PDF",
            data=pdf_bytes,
            file_name=f"riwayat_spk_laptop_{now_fn}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary",
            help="Unduh seluruh riwayat analisis sebagai file PDF",
        )
    except Exception as e:
        st.error(f"Gagal generate PDF: {e}")

# ── Clear history (admin only) ────────────────────────────
if st.session_state.role == "admin":
    with col_clear:
        if st.button("🗑️ Hapus Semua Riwayat", type="secondary", use_container_width=True, key="clear_hist"):
            st.session_state.rec_history = []
            state.set_flash("ok", "✅ Riwayat berhasil dihapus.")
            st.rerun()

# ── History table ─────────────────────────────────────────
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

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