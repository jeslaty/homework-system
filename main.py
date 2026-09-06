import streamlit as st

st.set_page_config(
    page_title="801 導師班級管理系統",
    page_icon="🏫",
    layout="wide"
)

# 注入 CSS：完全保留原始美觀卡片，並將 Streamlit 按鈕變成透明遮罩蓋在卡片上
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

    /* 卡片容器：設為 relative 以利放置透明點擊層 */
    .card-container {
        position: relative;
        margin-bottom: 20px;
    }

    /* 原版馬卡龍卡片視覺（完全還原截圖） */
    .card {
        border-radius: 24px;
        padding: 36px 20px;
        text-align: center;
        height: 220px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    
    .card-pink {
        background: #FFF0F5;
        border: 2px solid #FFD1DC;
        box-shadow: 0 8px 20px rgba(255, 182, 193, 0.25);
    }
    .card-blue {
        background: #F0F8FF;
        border: 2px solid #BAE6FD;
        box-shadow: 0 8px 20px rgba(173, 216, 230, 0.25);
    }
    .card-purple {
        background: #F5F0FF;
        border: 2px solid #DDD6FE;
        box-shadow: 0 8px 20px rgba(221, 160, 221, 0.25);
    }

    .card-icon { font-size: 3.2rem; margin-bottom: 12px; }
    .card-title { font-size: 1.35rem; font-weight: 800; color: #1E293B; margin-bottom: 6px; }
    .card-subtitle { font-size: 0.9rem; color: #64748B; font-weight: 600; }

    /* 關鍵魔法：將 st.button 變成隱形遮罩覆蓋在整張卡片上 */
    .overlay-btn {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 10;
    }
    .overlay-btn > button {
        width: 100% !important;
        height: 100% !important;
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        box-shadow: none !important;
        cursor: pointer;
    }
    .overlay-btn > button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
    }

    /* 懸浮效果套用到整張卡片 */
    .card-container:hover .card {
        transform: translateY(-8px) scale(1.02);
    }
    .card-container:hover .card-pink { box-shadow: 0 16px 30px rgba(255, 182, 193, 0.45); }
    .card-container:hover .card-blue { box-shadow: 0 16px 30px rgba(173, 216, 230, 0.45); }
    .card-container:hover .card-purple { box-shadow: 0 16px 30px rgba(221, 160, 221, 0.45); }

    /* 底部位於中央的橫排登出按鈕 */
    .logout-btn-container > button {
        background-color: rgba(255, 255, 255, 0.8) !important;
        color: #EF4444 !important;
        border: 1px solid #FECDD3 !important;
        border-radius: 16px !important;
        font-weight: 800 !important;
        padding: 12px !important;
        transition: all 0.2s ease !important;
    }
    .logout-btn-container > button:hover {
        background-color: #FFE4E6 !important;
        border-color: #FDA4AF !important;
        transform: translateY(-2px) !important;
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
        if st.button("✨ 確認通行", use_container_width=True, type="primary"):
            if username == "801" and password == "12345":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("帳號或密碼錯誤，請重新輸入！")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 3. 驗證通過：畫面與截圖 100% 一模一樣
st.markdown("""
    <div class="header-banner">
        <div class="main-title">🏫 班級經營主控台</div>
        <div class="sub-title">點擊下方任一功能大方格，即可快速進入管理系統</div>
    </div>
""", unsafe_allow_html=True)

# 第一排 3 個大方格
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="card-container">
            <div class="card card-pink">
                <div class="card-icon">📖</div>
                <div class="card-title">班級聯絡簿</div>
                <div class="card-subtitle">(801導師專屬)</div>
            </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="overlay-btn">', unsafe_allow_html=True)
    if st.button("click_1", key="card_btn_01"):
        st.switch_page("pages/01_每日聯絡簿.py")
    st.markdown('</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="card-container">
            <div class="card card-blue">
                <div class="card-icon">📚</div>
                <div class="card-title">作業登記專區</div>
                <div class="card-subtitle">(全校各科)</div>
            </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="overlay-btn">', unsafe_allow_html=True)
    if st.button("click_2", key="card_btn_02"):
        st.switch_page("pages/02_作業登記.py")
    st.markdown('</div></div>', unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="card-container">
            <div class="card card-purple">
                <div class="card-icon">🪑</div>
                <div class="card-title">座位表管理</div>
                <div class="card-subtitle">(排座位/印表)</div>
            </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="overlay-btn">', unsafe_allow_html=True)
    if st.button("click_3", key="card_btn_03"):
        st.switch_page("pages/03_座位表.py")
    st.markdown('</div></div>', unsafe_allow_html=True)

# 第二排 3 個擴充大方格
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
        <div class="card-container">
            <div class="card card-blue">
                <div class="card-icon">🎲</div>
                <div class="card-title">學生抽籤學輪播</div>
                <div class="card-subtitle">(課堂互動/提問)</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
        <div class="card-container">
            <div class="card card-pink">
                <div class="card-icon">⏳</div>
                <div class="card-title">考試倒數計時器</div>
                <div class="card-subtitle">(段考/倒數提醒)</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
        <div class="card-container">
            <div class="card card-purple">
                <div class="card-icon">➕</div>
                <div class="card-title">新增功能預留區</div>
                <div class="card-subtitle">(點擊可擴充)</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# 最底下獨立的一格橫排登出按鈕
st.markdown('<div class="logout-btn-container">', unsafe_allow_html=True)
if st.button("🔒 登出班級管理系統", use_container_width=True, key="logout_btn"):
    st.session_state["authenticated"] = False
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
