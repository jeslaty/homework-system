import streamlit as st

st.set_page_config(
    page_title="801 導師班級管理系統",
    page_icon="🏫",
    layout="wide"
)

# 隱藏預設選單與頁首
st.markdown("""
    <style>
    [data-testid="stSidebar"], button[data-testid="collapsedControl"], header[data-testid="stHeader"] {
        display: none !important;
    }
    .stApp { background-color: #F8FAFC; }
    
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E293B;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .card-container {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .card-container:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }
    .card-icon { font-size: 3rem; margin-bottom: 12px; }
    .card-title { font-size: 1.3rem; font-weight: 700; color: #0F172A; margin-bottom: 6px; }
    .card-subtitle { font-size: 0.95rem; color: #64748B; margin-bottom: 16px; }
    </style>
""", unsafe_allow_html=True)

# 初始化全域登入狀態
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# ----------------- 未登入：顯示 帳號 + 密碼 驗證畫面 -----------------
if not st.session_state["authenticated"]:
    st.markdown('<div class="main-title">🔒 801 導師安全驗證專區</div>', unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 1.2, 1])
    with col_b:
        username = st.text_input("請輸入導師帳號：")
        # type="password" 會預設附帶小眼睛開關，點擊可切換顯示/隱藏
        password = st.text_input("請輸入導師密碼：", type="password", placeholder="請輸入密碼")
        
        st.write("")
        if st.button("確認通行", use_container_width=True, type="primary"):
            # 在此設定您的帳號與密碼（可依需求替換）
            if username == "Jeslaty" and password == "12345":
                st.session_state["authenticated"] = True
                st.success("驗證成功！即將進入主控台...")
                st.rerun()
            else:
                st.error("帳號或密碼錯誤，請重新輸入！")
    st.stop()

# ----------------- 驗證成功：顯示完整主控台 -----------------

st.markdown('<div class="main-title">🏫 801 導師班級管理系統</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="card-container">
            <div class="card-icon">📖</div>
            <div class="card-title">班級聯絡簿</div>
            <div class="card-subtitle">（801導師專屬）</div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("進入聯絡簿", key="btn_contact", use_container_width=True):
        st.switch_page("pages/01_每日聯絡簿.py")

with col2:
    st.markdown("""
        <div class="card-container">
            <div class="card-icon">📋</div>
            <div class="card-title">作業登記專區</div>
            <div class="card-subtitle">（任教班作業）</div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("進入作業登記", key="btn_homework", use_container_width=True):
        st.switch_page("pages/02_作業登記.py")

with col3:
    st.markdown("""
        <div class="card-container">
            <div class="card-icon">🪑</div>
            <div class="card-title">班級座位表</div>
            <div class="card-subtitle">（座位安排與列印）</div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("進入座位表", key="btn_seating", use_container_width=True):
        st.switch_page("pages/03_座位表.py")

st.write("")
st.write("")
# 右下角提供登出選項
col_l, col_r = st.columns([0.85, 0.15])
with col_r:
    if st.button("🔒 登出系統", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()
