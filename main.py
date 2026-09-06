import streamlit as st

st.set_page_config(page_title="班級經營主控台", page_icon="🏫", layout="wide")

# CSS 視覺美化：莫蘭迪灰背景 + 淺粉馬卡龍大方格
st.markdown("""
    <style>
    /* 隱藏側邊欄與頁首 */
    [data-testid="stSidebar"], 
    button[data-testid="collapsedControl"], 
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 頁面整體背景：深莫蘭迪灰色 */
    .stApp {
        background-color: #3A404A !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", sans-serif;
    }
    
    /* 頂部 Header Banner */
    .main-title-banner {
        background-color: #4A515D;
        padding: 24px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid #5A6270;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        margin-bottom: 35px;
    }
    .main-title-banner h1 {
        color: #F8FAFC !important;
        font-size: 2.3rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        letter-spacing: 1px;
    }
    .main-title-banner p {
        color: #CBD5E1 !important;
        margin-top: 8px !important;
        font-size: 1.05rem;
        font-weight: 400;
    }
    
    /* 淺粉馬卡龍大方格卡片按鈕 */
    div.macaron-grid-card > div.stButton > button {
        height: 260px !important;            /* 大大幅拉高高度，呈現俐落大方格 */
        width: 100% !important;
        background-color: #FFE5EC !important; /* 格子本身：淺粉馬卡龍色 */
        color: #8C2F39 !important;           /* 質感深紅/粉棕色文字 */
        border: none !important;
        border-radius: 28px !important;      /* 加大圓角 */
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.25s ease-in-out !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 24px !important;
        white-space: pre-wrap !important;
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        line-height: 1.6 !important;
    }
    
    /* 懸浮效果：放大與變色 */
    div.macaron-grid-card > div.stButton > button:hover {
        background-color: #FFC2D1 !important; /* 懸浮時顯色柔粉 */
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.3) !important;
        color: #6B1D26 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 頂部迎賓 Banner
st.markdown("""
    <div class="main-title-banner">
        <h1>🏫 班級經營主控台</h1>
        <p>點擊下方任一功能大方格，即可快速進入管理系統</p>
    </div>
""", unsafe_allow_html=True)

# --- 九宮格第一排 (3個大方格) ---
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown('<div class="macaron-grid-card">', unsafe_allow_html=True)
    if st.button("📖\n\n班級聯絡簿\n(801導師專屬)", key="btn_p1", use_container_width=True):
        st.switch_page("pages/01_班級聯絡簿.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="macaron-grid-card">', unsafe_allow_html=True)
    if st.button("📚\n\n作業登記專區\n(全校各科)", key="btn_p2", use_container_width=True):
        st.switch_page("pages/02_作業登記.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="macaron-grid-card">', unsafe_allow_html=True)
    if st.button("🪑\n\n座位表管理\n(排座位/印表)", key="btn_p3", use_container_width=True):
        st.switch_page("pages/03_座位表.py")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("") # 上下排間距

# --- 九宮格第二排 (3個大方格) ---
col4, col5, col6 = st.columns(3, gap="large")

with col4:
    st.markdown('<div class="macaron-grid-card">', unsafe_allow_html=True)
    if st.button("🎲\n\n學生抽籤與輪播\n(課堂互動工具)", key="btn_p4", use_container_width=True):
        st.switch_page("pages/04_抽籤與輪播.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="macaron-grid-card">', unsafe_allow_html=True)
    if st.button("⏳\n\n考試倒數計時器\n(班級公播畫面)", key="btn_p5", use_container_width=True):
        st.switch_page("pages/05_倒數計時器.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="macaron-grid-card">', unsafe_allow_html=True)
    if st.button("➕\n\n新增功能預留區\n(未來擴充)", key="btn_p6", use_container_width=True):
        st.toast("💡 此功能尚未開放，敬請期待！", icon="✨")
    st.markdown('</div>', unsafe_allow_html=True)
