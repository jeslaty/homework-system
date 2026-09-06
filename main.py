import streamlit as st

st.set_page_config(
    page_title="801 導師班級管理系統",
    page_icon="🏫",
    layout="wide"
)

# 馬卡龍風美化 CSS (含懸浮動畫) 與隱藏預設元件
st.markdown("""
    <style>
    [data-testid="stSidebar"], button[data-testid="collapsedControl"], header[data-testid="stHeader"] {
        display: none !important;
    }
    .stApp {
        background: linear-gradient(135deg, #FFF5F5 0%, #F0F4FF 50%, #F5F3FF 100%);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #4A5568;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.05);
    }
    
    /* 馬卡龍卡片基礎與懸浮效果 */
    .card-macaron-pink {
        background: #FFF0F5;
        border-radius: 20px;
        padding: 24px 16px 16px 16px;
        box-shadow: 0 6px 16px rgba(255, 182, 193, 0.3);
        border: 2px solid #FFD1DC;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .card-macaron-pink:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(255, 182, 193, 0.5);
    }

    .card-macaron-blue {
        background: #F0F8FF;
        border-radius: 20px;
        padding: 24px 16px 16px 16px;
        box-shadow: 0 6px 16px rgba(173, 216, 230, 0.3);
        border: 2px solid #BAE6FD;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .card-macaron-blue:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(173, 216, 230, 0.5);
    }

    .card-macaron-purple {
        background: #F5F0FF;
        border-radius: 20px;
        padding: 24px 16px 16px 16px;
        box-shadow: 0 6px 16px rgba(221, 160, 221, 0.3);
        border: 2px solid #DDD6FE;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .card-macaron-purple:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(221, 160, 221, 0.5);
    }

    .card-macaron-yellow {
        background: #FEFCE8;
        border-radius: 20px;
        padding: 24px 16px 16px 16px;
        box-shadow: 0 6px 16px rgba(254, 240, 138, 0.4);
        border: 2px solid #FEF08A;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .card-macaron-yellow:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(250, 204, 21, 0.4);
    }
    
    .card-icon { font-size: 3.5rem; margin-bottom: 8px; }
    .card-title { font-size: 1.4rem; font-weight: 800; color: #2D3748; margin-bottom: 4px; }
    .card-subtitle { font-size: 0.95rem; color: #718096; font-weight: 600; margin-bottom: 8px; }
    </style>
""", unsafe_allow_html=True)

# 初始化全域登入狀態
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# ----------------- 未登入：馬卡龍登入驗證關卡 -----------------
if not st.session_state["authenticated"]:
    st.markdown('<div class="main-title">🔒 801 導師安全驗證專區</div>', unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 1.2, 1])
    with col_b:
        st.markdown('<div style="background: #FFFFFF; padding: 28px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 2px solid #FFE4E6;">', unsafe_allow_html=True)
        
        username = st.text_input("👤 請輸入導師帳號：", placeholder="例如：801")
        password = st.text_input("🔑 請輸入導師密碼：", type="password", placeholder="請輸入密碼")
        
        st.write("")
        if st.button("✨ 確認通行", use_container_width=True, type="primary"):
            if username == "801" and password == "12345":
                st.session_state["authenticated"] = True
                st.success("驗證成功！即將進入主控台...")
                st.rerun()
            else:
                st.error("帳號或密碼錯誤，請重新輸入！")
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ----------------- 驗證成功：馬卡龍懸浮風主控台 -----------------

st.markdown('<div class="main-title">🏫 801 導師班級管理系統</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="card-macaron-pink">
            <div class="card-icon">📖</div>
            <div class="card-title">班級聯絡簿</div>
            <div class="card-subtitle">（801導師專屬）</div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("進入聯絡簿 ➔", key="btn_contact", use_container_width=True):
        st.switch_page("pages/01_每日聯絡簿.py")

with col2:
    st.markdown("""
        <div class="card-macaron-blue">
            <div class="card-icon">📋</div>
            <div class="card-title">作業登記專區</div>
            <div class="card-subtitle">（任教班作業）</div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("進入作業登記 ➔", key="btn_homework", use_container_width=True):
        st.switch_page("pages/02_作業登記.py")

with col3:
    st.markdown("""
        <div class="card-macaron-purple">
            <div class="card-icon">🪑</div>
            <div class="card-title">班級座位表</div>
            <div class="card-subtitle">（座位安排與列印）</div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("進入座位表 ➔", key="btn_seating", use_container_width=True):
        st.switch_page("pages/03_座位表.py")

st.write("")
st.write("")

# 登出按鈕
col_l, col_r = st.columns([0.85, 0.15])
with col_r:
    if st.button("🔒 登出系統", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()
