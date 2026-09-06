import streamlit as st

st.set_page_config(page_title="班級經營主控台", page_icon="🏫", layout="wide")

# CSS 強制覆蓋與高度修復
st.markdown("""
    <style>
    /* 1. 隱藏預設元件 */
    [data-testid="stSidebar"], 
    button[data-testid="collapsedControl"], 
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 2. 修正頁面內邊距與溫柔莫蘭迪奶茶色背景 */
    .stApp, .stApp > header, [data-testid="stAppViewContainer"] {
        background-color: #F2EFE9 !important; /* 暖調莫蘭迪米灰/奶茶底色 */
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", sans-serif;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }
    
    /* 3. 頂部 Banner */
    .main-title-banner {
        background: linear-gradient(135deg, #E6E2DD 0%, #D8D2C9 100%);
        padding: 24px;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 30px;
        border: 1px solid #C8C2B9;
    }
    .main-title-banner h1 {
        color: #4A443E !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
    }
    .main-title-banner p {
        color: #787067 !important;
        margin-top: 8px !important;
        font-size: 1.05rem;
        font-weight: 500;
    }
    
    /* 4. 強制突破按鈕限制：大方格與色彩設定 */
    div[data-testid="stColumn"] div.stButton > button {
        min-height: 220px !important;       /* 強制形成正方感大格 */
        height: 220px !important;
        width: 100% !important;
        border: none !important;
        border-radius: 28px !important;     /* 質感大圓角 */
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 20px !important;
        white-space: pre-wrap !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        line-height: 1.6 !important;
    }
    
    /* 動態懸浮效果 */
    div[data-testid="stColumn"] div.stButton > button:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 16px 30px rgba(0, 0, 0, 0.12) !important;
    }

    /* 淺粉馬卡龍格子 */
    div.card-pink div.stButton > button {
        background-color: #FFE5EC !important;
        color: #8C2F39 !important;
    }
    div.card-pink div.stButton > button:hover {
        background-color: #FFC2D1 !important;
        color: #6B1D26 !important;
    }

    /* 淺藍馬卡龍格子 */
    div.card-blue div.stButton > button {
        background-color: #E0F2FE !important;
        color: #0369A1 !important;
    }
    div.card-blue div.stButton > button:hover {
        background-color: #BAE6FD !important;
        color: #0284C7 !important;
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

# --- 九宮格第一排 ---
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown('<div class="card-pink">', unsafe_allow_html=True)
    if st.button("📖\n\n班級聯絡簿\n(801導師專屬)", key="btn_p1", use_container_width=True):
        st.switch_page("pages/01_班級聯絡簿.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card-blue">', unsafe_allow_html=True)
    if st.button("📚\n\n作業登記專區\n(全校各科)", key="btn_p2", use_container_width=True):
        st.switch_page("pages/02_作業登記.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card-pink">', unsafe_allow_html=True)
    if st.button("🪑\n\n座位表管理\n(排座位/印表)", key="btn_p3", use_container_width=True):
        st.switch_page("pages/03_座位表.py")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("") # 上下排間距

# --- 九宮格第二排 ---
col4, col5, col6 = st.columns(3, gap="large")

with col4:
    st.markdown('<div class="card-blue">', unsafe_allow_html=True)
    if st.button("🎲\n\n學生抽籤與輪播\n(課堂互動工具)", key="btn_p4", use_container_width=True):
        st.switch_page("pages/04_抽籤與輪播.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="card-pink">', unsafe_allow_html=True)
    if st.button("⏳\n\n考試倒數計時器\n(班級公播畫面)", key="btn_p5", use_container_width=True):
        st.switch_page("pages/05_倒數計時器.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="card-blue">', unsafe_allow_html=True)
    if st.button("➕\n\n新增功能預留區\n(未來擴充)", key="btn_p6", use_container_width=True):
        st.toast("💡 此功能尚未開放，敬請期待！", icon="✨")
    st.markdown('</div>', unsafe_allow_html=True)
