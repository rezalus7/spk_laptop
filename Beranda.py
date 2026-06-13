import streamlit as st
import theme, state

st.set_page_config(
    page_title="SPK Laptop — SMART",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed", # Sembunyikan sidebar bawaan sejak awal
)

theme.inject()
state.init_state()

# ─── Redirect logged-in users ────────────────────────────
if st.session_state.logged_in:
    st.switch_page("pages/1_Dashboard.py")

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

mode = st.session_state.auth_mode

# ─── Extra CSS untuk UI Modern Tanpa Sidebar ──────────────
st.markdown("""
<style>
/* Sembunyikan total sidebar bawaan Streamlit di PC dan HP */
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], 
button[data-testid="baseButton-header"], [data-testid="collapsedControl"] {
    display: none !important;
    visibility: hidden !important;
    width: 0px !important;
}

/* Optimasi lebar kontainer utama agar simetris di tengah */
[data-testid="stMainBlockContainer"] {
    max-width: 100% !important;
    padding-left: 16px !important;
    padding-right: 16px !important;
}

@keyframes fadeUp {
    from { opacity:0; transform:translateY(24px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}
.login-wrapper {
    animation: fadeUp 0.6s cubic-bezier(0.16,1,0.3,1) both;
}
.login-card-title {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 5px;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 24px;
    background: linear-gradient(90deg, #60a5fa, #06b6d4, #60a5fa);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
}

/* Style form login modern */
.login-page [data-testid="stForm"] {
    background: rgba(15,21,34,0.7) !important;
    border: 1px solid rgba(59,130,246,0.15) !important;
    border-radius: 20px !important;
    padding: 32px 28px !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 24px 64px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.03) !important;
}
.login-page [data-testid="stTextInput"] input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.2), 0 0 20px rgba(59,130,246,0.1) !important;
}

/* Tombol Register */
.register-btn .stButton > button {
    background: linear-gradient(135deg, #16a34a, #15803d) !important;
    color: #fff !important;
    border-radius: 12px !important;
    height: 46px !important;
    font-size: 14px !important;
    letter-spacing: 1px !important;
    box-shadow: 0 4px 20px rgba(22,163,74,0.3) !important;
    transition: all 0.2s ease !important;
}
.register-btn .stButton > button:hover {
    box-shadow: 0 8px 32px rgba(22,163,74,0.45) !important;
    transform: translateY(-1px) !important;
}

/* Tombol Login Submit */
.login-page [data-testid="stForm"] .stFormSubmitButton > button {
    background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
    border-radius: 12px !important;
    height: 46px !important;
    font-size: 14px !important;
    letter-spacing: 1px !important;
    box-shadow: 0 4px 20px rgba(59,130,246,0.35) !important;
    transition: all 0.2s ease !important;
    color: #fff !important;
}
.login-page [data-testid="stForm"] .stFormSubmitButton > button:hover {
    box-shadow: 0 8px 32px rgba(59,130,246,0.5) !important;
    transform: translateY(-1px) !important;
}

/* Latar belakang dekoratif */
.dot-bg {
    position: fixed; inset: 0; pointer-events: none; z-index: -1;
    background-image: radial-gradient(circle, rgba(59,130,246,0.06) 1px, transparent 1px);
    background-size: 32px 32px;
}
.glow-orb {
    position: fixed; border-radius: 50%; pointer-events: none; z-index: -1; filter: blur(80px);
}

/* Responsivitas ukuran teks di HP */
@media (max-width: 768px) {
    .branding-title { font-size: 22px !important; letter-spacing: 2px !important; }
    .branding-sub { font-size: 10px !important; }
}
</style>
<div class="dot-bg"></div>
<div class="glow-orb" style="width:400px;height:400px;top:-100px;right:10%;background:rgba(59,130,246,0.06);"></div>
<div class="glow-orb" style="width:300px;height:300px;bottom:0;left:30%;background:rgba(6,182,212,0.05);"></div>
""", unsafe_allow_html=True)

# ─── Layout Konten Tengah ────────────────────────────────
st.markdown('<div class="login-page">', unsafe_allow_html=True)

# Memakai kolom tengah yang pas (tidak terlalu lebar di PC, aman di HP)
_, center, _ = st.columns([1.1, 1, 1.1])

with center:
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)

    # BRANDING LOGO & TULISAN DI ATAS FORM LOGIN
    st.markdown("""
    <div style="text-align: center; margin-bottom: 32px;">
        <div style="
            width: 64px; height: 64px; margin: 0 auto 16px auto;
            background: linear-gradient(135deg, #1e3a5f 0%, #0f2040 100%);
            border-radius: 16px; display: flex; align-items: center; justify-content: center;
            font-size: 32px; border: 1px solid rgba(59,130,246,0.25);
            box-shadow: 0 8px 32px rgba(59,130,246,0.15);
        ">🖥️</div>
        <div class="branding-title" style="color:#f1f5f9; font-weight:800; font-size:26px; letter-spacing:4px; font-family:'DM Sans',sans-serif;">SPK LAPTOP</div>
        <div class="branding-sub" style="color:#3b82f6; font-size:11px; margin-top:4px; font-family:'Space Mono',monospace; letter-spacing:3px;">METODE SMART</div>
        <div style="width:32px; height:2px; background:linear-gradient(90deg,#3b82f6,#06b6d4); margin:16px auto 0 auto; border-radius:2px;"></div>
    </div>
    """, unsafe_allow_html=True)

    state.show_flash()

    if mode == "login":
        with st.form("form_login", clear_on_submit=False):
            st.markdown(f'<p class="login-card-title">Masuk ke akun</p>', unsafe_allow_html=True)
            username = st.text_input("", placeholder="✦  Username", label_visibility="collapsed")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            password = st.text_input("", type="password", placeholder="✦  Password", label_visibility="collapsed")
            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            submit = st.form_submit_button("Login  →", use_container_width=True, type="primary")

        if submit:
            matched = next((u for u in st.session_state.users
                            if u["username"] == username and u["password"] == password), None)
            if matched:
                st.session_state.logged_in = True
                st.session_state.username  = username
                st.session_state.role      = matched["role"]
                state.set_flash("ok", f"✅ Selamat datang, <b>{username}</b>!")
                st.switch_page("pages/1_Dashboard.py")
            else:
                state.set_flash("err", "❌ Username atau password salah.")
                st.rerun()

        # ─── KOTAK KETERANGAN AKUN DEFAULT (TEMA INTEGRASI BIRU) ───
        st.markdown("""
        <div style="
            background-color: rgba(59, 130, 246, 0.08); 
            border-radius: 12px; 
            padding: 14px 18px; 
            margin-top: 12px;
            margin-bottom: 4px;
            border: 1px solid rgba(59, 130, 246, 0.15);
            font-family: sans-serif;
        ">
            <div style="color: #60a5fa; font-size: 13px; line-height: 1.6; font-weight: 500;">
                <b>Admin:</b> admin / 123 <br>
                <b>Mahasiswa:</b> mahasiswa / 123
            </div>
        </div>
        """, unsafe_allow_html=True)
        # ────────────────────────────────────────────────────────────

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="register-btn">', unsafe_allow_html=True)
        if st.button("Register  →", use_container_width=True, key="go_register"):
            st.session_state.auth_mode = "register"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        with st.form("form_reg", clear_on_submit=True):
            st.markdown('<p class="login-card-title">Buat akun baru</p>', unsafe_allow_html=True)
            new_user  = st.text_input("", placeholder="✦  Username baru", label_visibility="collapsed")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            new_pass  = st.text_input("", type="password", placeholder="✦  Password", label_visibility="collapsed")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            new_pass2 = st.text_input("", type="password", placeholder="✦  Konfirmasi password", label_visibility="collapsed")
            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            reg_btn = st.form_submit_button("Buat Akun  →", use_container_width=True, type="primary")

        if reg_btn:
            if not new_user or not new_pass:
                state.set_flash("warn", "⚠️ Username dan password wajib diisi.")
            elif new_pass != new_pass2:
                state.set_flash("err", "❌ Konfirmasi password tidak cocok.")
            elif any(u["username"] == new_user for u in st.session_state.users):
                state.set_flash("err", "❌ Username sudah terdaftar.")
            else:
                st.session_state.users.append({"username": new_user, "password": new_pass, "role": "mahasiswa"})
                state.set_flash("ok", "✅ Akun berhasil dibuat! Silakan masuk.")
                st.session_state.auth_mode = "login"
            st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("← Kembali ke Login", use_container_width=True, key="go_login", type="secondary"):
            st.session_state.auth_mode = "login"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)