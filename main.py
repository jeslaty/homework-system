import streamlit as st

st.set_page_config(
    page_title="801 導師班級管理系統",
    page_icon="🏫",
    layout="wide"
)

# 注入 CSS 樣式：將按鈕直接改造為馬卡龍大方格
st.markdown("""
    <style>
    /* 隱藏預設選單與頁首 */
    [data-testid="stSidebar"], button[data-testid="collapsedControl"], header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 背景漸層 */
    .stApp {
        background: linear-gradient(135deg, #FFF0F5 0%, #F0F4FF 50%, #F5F0FF 100%);
    }
    
    /* 頂部 Banner */
    .header-banner {
        background: rgba(255, 255, 255, 0.6);
        border-radius: 24px;
        padding: 24px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
    }
    .main-title { font-size: 2.2rem; font-weight: 800; color: #334155; margin-bottom: 8px; }
    .sub-title { font-size: 1rem; color: #64748B; font-weight: 500; }

    /* 重設卡片按鈕的基本架構 */
    .stButton > button {
        height: 220px !important;
        border-radius: 24px !important;
        padding: 20px !important;
        text-align: center !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        white-space: pre-line !important; /* 支援換行 */
        line-height: 1.5 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .stButton > button:hover {
        transform: translateY(-8px) scale(1.02) !important;
    }

    /* 粉紅卡片（聯絡簿、倒數） */
    .pink-card > button {
        background: #FFF0F5 !important;
        border: 2px solid #FFD1DC !important;
        box-shadow: 0 8px 20px rgba(255, 182, 193, 0.25) !important;
    }
    .pink-card > button:hover {
        box-shadow: 0 16px 30px rgba(255, 182, 193, 0.45) !important;
    }

    /* 藍色卡片（作業、抽籤） */
    .blue-card > button {
        background: #F0F8FF !important;
        border: 2px solid #BAE6FD !important;
        box-shadow: 0 8px 20px rgba(173, 216, 230, 0.25) !important;
    }
    .blue-card > button:hover {
        box-shadow: 0 16px 30px rgba(173, 216, 230, 0.45) !important;
    }

    /* 紫色卡片（座位表、預留） */
    .purple-card > button {
        background: #F5F0FF !important;
        border: 2px solid #DDD6FE !important;
        box-shadow: 0 8px 20px rgba(221, 160, 221, 0.25) !important;
    }
    .purple-card > button:hover {
        box-shadow: 0 16px 30px rgba(221, 160, 221, 0.45) !important;
    }

    /* 按鈕內的文字大小調整 */
    .stButton > button p {
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        color: #1E293B !important;
    }
    </style>
""", unsafe_allow_html=True)

# 1. 初始化全域登入狀態
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 2. 未登入：一次性驗證
if not st.session_state["authenticated"]:
    st.markdown("""
        <div class="header-banner">
            <div class="main-title">🔒 801 導師安全驗證專區</div>
            <div class="sub-title">請輸入帳號與密碼以進入班級管理系統</div>
        </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 1.2, 1])
    with col_b:
        st.markdown('<div style="background: rgba(255,255,255,0.8); padding: 28px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #E2E8F0;">', unsafe_allow_html=True)
        username = st.text_input("👤 請輸入導師帳號：", placeholder="例如：801")
        password = st.text_input("🔑 請輸入導師密碼：", type="password", placeholder="請輸入密碼")
        st.write("")
        if st.button("✨ 確認通行", use_container_width=True, type="primary", key="login_btn"):
            if username == "801" and password == "12345":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("帳號或密碼錯誤，請重新輸入！")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 3. 驗證通過：純大方格主控台（點擊方格本身即進入）
st.markdown("""
    <div class="header-banner">
        <div class="main-title">🏫 班級經營主控台</div>
        <div class="sub-title">點擊下方任一功能大方格，即可快速進入管理系統</div>
    </div>
""", unsafe_allow_html=True)

# 第一排 3 個大方格
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="pink-card">', unsafe_allow_html=True)
    if st.button("📖\n\n班級聯絡簿\n(801導師專屬)", key="card_01", use_container_width=True):
        st.switch_page("pages/01_每日聯絡簿.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="blue-card">', unsafe_allow_html=True)
    if st.button("📚\n\n作業登記專區\n(全校各科)", key="card_02", use_container_width=True):
        st.switch_page("pages/02_作業登記.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="purple-card">', unsafe_allow_html=True)
    if st.button("🪑\n\n座位表管理\n(排座位/印表)", key="card_03", use_container_width=True):
        st.switch_page("pages/03_座位表.py")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# 第二排 3 個擴充大方格
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown('<div class="blue-card">', unsafe_allow_html=True)
    st.button("🎲\n\n學生抽籤學輪播\n(課堂互動/提問)", key="card_04", use_container_width=True, disabled=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="pink-card">', unsafe_allow_html=True)
    st.button("⏳\n\n考試倒數計時器\n(段考/倒數提醒)", key="card_05", use_container_width=True, disabled=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="purple-card">', unsafe_allow_html=True)
    st.button("➕\n\n新增功能預留區\n(點擊可擴充)", key="card_06", use_container_width=True, disabled=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")
st.write("")

# 登出按鈕
col_l, col_r = st.columns([0.85, 0.15])
with col_r:
    if st.button("🔒 登出系統", use_container_width=True, key="logout_btn"):
        st.session_state["authenticated"] = False
        st.rerun()
