import streamlit as st

st.set_page_config(
    page_title="801 導師班級管理系統",
    page_icon="🏫",
    layout="wide"
)

# 隱藏預設選單與頁首，並注入馬卡龍卡片樣式
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
    
    /* ---------------- 把 Streamlit 按鈕直接改造為馬卡龍卡片 ---------------- */
    div.stButton > button {
        width: 100% !important;
        height: 220px !important;
        border-radius: 24px !important;
        padding: 20px !important;
        white-space: pre-wrap !important;
        line-height: 1.5 !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        cursor: pointer !important;
    }

    /* 1. 粉紅馬卡龍 - 每日聯絡簿 */
    div[data-testid="column"]:nth-child(1) div.stButton > button {
        background: #FFF0F5 !important;
        border: 2px solid #FFD1DC !important;
        box-shadow: 0 8px 20px rgba(255, 182, 193, 0.3) !important;
        color: #2D3748 !important;
    }
    div[data-testid="column"]:nth-child(1) div.stButton > button:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 16px 30px rgba(255, 182, 193, 0.5) !important;
        background: #FFE4E6 !important;
    }

    /* 2. 粉藍馬卡龍 - 作業登記專區 */
    div[data-testid="column"]:nth-child(2) div.stButton > button {
        background: #F0F8FF !important;
        border: 2px solid #BAE6FD !important;
        box-shadow: 0 8px 20px rgba(173, 216, 230, 0.3) !important;
        color: #2D3748 !important;
    }
    div[data-testid="column"]:nth-child(2) div.stButton > button:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 16px 30px rgba(173, 216, 230, 0.5) !important;
        background: #E0F2FE !important;
    }

    /* 3. 粉紫馬卡龍 - 班級座位表 */
    div[data-testid="column"]:nth-child(3) div.stButton > button {
        background: #F5F0FF !important;
        border: 2px solid #DDD6FE !important;
        box-shadow: 0 8px 20px rgba(221, 160, 221, 0.3) !important;
        color: #2D3748 !important;
    }
    div[data-testid="column"]:nth-child(3) div.stButton > button:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 16px 30px rgba(221, 160, 221, 0.5) !important;
        background: #EDE9FE !important;
    }

    /* 4. 馬卡龍黃 - 榮譽榜/懲戒專區 */
    div[data-testid="column"]:nth-child(4) div.stButton > button {
        background: #FEFCE8 !important;
        border: 2px solid #FEF08A !important;
        box-shadow: 0 8px 20px rgba(254, 240, 138, 0.4) !important;
        color: #2D3748 !important;
    }
    div[data-testid="column"]:nth-child(4) div.stButton > button:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 16px 30px rgba(250, 204, 21, 0.4) !important;
        background: #FEF08A !important;
    }
    </style>
""", unsafe_allow_html=True)

# 初始化全域登入狀態
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# ----------------- 未登入：馬卡龍帳號密碼驗證 -----------------
if not st.session_state["authenticated"]:
    st.markdown('<div class="main-title">🔒 801 導師安全驗證專區</div>', unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 1.2, 1])
    with col_b:
        st.markdown('<div style="background: #FFFFFF; padding: 28px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 2px solid #FFE4E6;">', unsafe_allow_html=True)
        
        username = st.text_input("👤 請輸入導師帳號：", placeholder="例如：801")
        password = st.text_input("🔑 請輸入導師密碼：", type="password", placeholder="請輸入密碼")
        
        st.write("")
        if st.button("✨ 確認通行", key="login_btn", use_container_width=True):
            if username == "801" and password == "12345":
                st.session_state["authenticated"] = True
                st.success("驗證成功！即將進入主控台...")
                st.rerun()
            else:
                st.error("帳號或密碼錯誤，請重新輸入！")
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ----------------- 驗證成功：完整可點擊馬卡龍主控台 -----------------

st.markdown('<div class="main-title">🏫 801 導師班級管理系統</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

# 方格 1：每日聯絡簿
with col1:
    btn_text_1 = "📖\n\n班級聯絡簿\n(801導師專屬)"
    if st.button(btn_text_1, key="card_contact"):
        st.switch_page("pages/01_每日聯絡簿.py")

# 方格 2：作業登記專區
with col2:
    btn_text_2 = "📋\n\n作業登記專區\n（任教班作業）"
    if st.button(btn_text_2, key="card_homework"):
        st.switch_page("pages/02_作業登記.py")

# 方格 3：班級座位表
with col3:
    btn_text_3 = "🪑\n\n班級座位表\n（座位安排與列印）"
    if st.button(btn_text_3, key="card_seating"):
        st.switch_page("pages/03_座位表.py")

# 方格 4：榮譽榜 / 懲戒專區 (擴充模組)
with col4:
    btn_text_4 = "🏆\n\n榮譽榜 / 懲戒專區\n（學生獎懲紀錄）"
    if st.button(btn_text_4, key="card_reward"):
        # 若有建立 04_獎懲紀錄.py，可在此切換
        st.switch_page("pages/04_獎懲紀錄.py")

st.write("")
st.write("")

# 右下角登出按鈕
col_l, col_r = st.columns([0.85, 0.15])
with col_r:
    if st.button("🔒 登出系統", key="logout_btn", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()
