import streamlit as st
import theme, state

st.set_page_config(
    page_title="SPK Laptop — SMART",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

theme.inject()
state.init_state()

# ─── Redirect logged-in users ────────────────────────────
if st.session_state.logged_in:
    st.switch_page("pages/1_Dashboard.py")

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

mode = st.session_state.auth_mode

# ─── Sidebar branding ────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 40px 20px 32px 20px; text-align: center;">
        <div style="
            width: 72px; height: 72px; margin: 0 auto 20px auto;
            background: linear-gradient(135deg, #1e3a5f 0%, #0f2040 100%);
            border-radius: 20px; display: flex; align-items: center; justify-content: center;
            font-size: 36px; border: 1px solid rgba(59,130,246,0.3);
            box-shadow: 0 8px 32px rgba(59,130,246,0.15);
        ">🖥️</div>
        <div style="color:#f1f5f9; font-weight:800; font-size:20px; letter-spacing:3px; font-family:'DM Sans',sans-serif;">SPK LAPTOP</div>
        <div style="color:#3b82f6; font-size:11px; margin-top:6px; font-family:'Space Mono',monospace; letter-spacing:3px;">METODE SMART</div>
        <div style="width:40px; height:2px; background:linear-gradient(90deg,#3b82f6,#06b6d4); margin:20px auto;border-radius:2px;"></div>
        <div style="color:#475569; font-size:12px; line-height:1.8; font-family:'DM Sans',sans-serif;">
            <br><br>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Extra CSS untuk Menghilangkan Tombol Back (<<) ──────
st.markdown("""
<style>
/* Menyembunyikan tombol panah back / collapse (<<) di sidebar */
[data-testid="stSidebarCollapsedControl"], 
button[data-testid="baseButton-header"],
[data-testid="collapsedControl"] {
    display: none !important;
    visibility: hidden !important;
}

/* Memastikan sidebar terkunci dan tidak bisa di-collapse */
section[data-testid="stSidebar"] button {
    display: none !important;
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
    margin-bottom: 28px;
    background: linear-gradient(90deg, #60a5fa, #06b6d4, #60a5fa);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
}
.login-divider {
    display: flex; align-items: center; gap: 12px;
    margin: 20px 0; color: #334155; font-size: 12px;
}
.login-divider::before, .login-divider::after {
    content: ''; flex: 1;
    height: 1px; background: #1e2d45;
}
/* Override form background */
.login-page [data-testid="stForm"] {
    background: rgba(15,21,34,0.7) !important;
    border: 1px solid rgba(59,130,246,0.15) !important;
    border-radius: 20px !important;
    padding: 32px 28px !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 24px 64px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.03) !important;
}
/* Glowing input on focus */
.login-page [data-testid="stTextInput"] input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.2), 0 0 20px rgba(59,130,246,0.1) !important;
}
/* Register button green glow */
.register-btn .stButton > button {
    background: linear-gradient(135deg, #16a34a, #15803d) !important;
    color: #fff !important;
    border-radius: 12px !important;
    height: 48px !important;
    font-size: 15px !important;
    letter-spacing: 1px !important;
    box-shadow: 0 4px 20px rgba(22,163,74,0.3) !important;
    transition: all 0.2s ease !important;
}
.register-btn .stButton > button:hover {
    box-shadow: 0 8px 32px rgba(22,163,74,0.45) !important;
    transform: translateY(-1px) !important;
}
/* Login submit button */
.login-page [data-testid="stForm"] .stFormSubmitButton > button {
    background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
    border-radius: 12px !important;
    height: 48px !important;
    font-size: 15px !important;
    letter-spacing: 1px !important;
    box-shadow: 0 4px 20px rgba(59,130,246,0.35) !important;
    transition: all 0.2s ease !important;
    color: #fff !important;
}
.login-page [data-testid="stForm"] .stFormSubmitButton > button:hover {
    box-shadow: 0 8px 32px rgba(59,130,246,0.5) !important;
    transform: translateY(-1px) !important;
}
/* Dot accent bg */
.dot-bg {
    position: fixed; inset: 0; pointer-events: none; z-index: -1;
    background-image: radial-gradient(circle, rgba(59,130,246,0.06) 1px, transparent 1px);
    background-size: 32px 32px;
}
.glow-orb {
    position: fixed; border-radius: 50%; pointer-events: none; z-index: -1; filter: blur(80px);
}
</style>
<div class="dot-bg"></div>
<div class="glow-orb" style="width:400px;height:400px;top:-100px;right:10%;background:rgba(59,130,246,0.06);"></div>
<div class="glow-orb" style="width:300px;height:300px;bottom:0;left:30%;background:rgba(6,182,212,0.05);"></div>
""", unsafe_allow_html=True)

# ─── Layout ──────────────────────────────────────────────
st.markdown('<div class="login-page">', unsafe_allow_html=True)

# Mengembalikan ukuran kolom form ke proporsi semula (1.2) agar pas di tengah
_, center, _ = st.columns([1, 1.2, 1])

with center:
    st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)

    # Big title above card
    page_label = "LOGIN" if mode == "login" else "DAFTAR AKUN"
    st.markdown(f"""
    <h1 style="
        color:#e2e8f0; font-size:38px; font-weight:800;
        letter-spacing:10px; text-align:center;
        margin-bottom:40px; font-family:'DM Sans',sans-serif;
        text-shadow: 0 0 40px rgba(59,130,246,0.3);
    ">{page_label}</h1>
    """, unsafe_allow_html=True)

    state.show_flash()

    if mode == "login":
        with st.form("form_login", clear_on_submit=False):
            st.markdown('<p class="login-card-title">Masuk ke akun Anda</p>', unsafe_allow_html=True)
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