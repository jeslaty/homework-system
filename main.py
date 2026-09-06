import streamlit as st

st.set_page_config(page_title="導師班級管理主控台", page_icon="🏫", layout="wide")

# CSS 視覺美化：馬卡龍色系與卡片化點擊效果
st.markdown("""
    <style>
    /* 隱藏側邊欄與頁首 */
    [data-testid="stSidebar"], 
    button[data-testid="collapsedControl"], 
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 頁面整體字體與背景 */
    .stApp {
        background-color: #FAFAFC;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", sans-serif;
    }
    
    /* 主標題 Banner */
    .main-title-banner {
        background: linear-gradient(135deg, #A8EDEA 0%, #FED6E3 100%);
        padding: 24px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        margin-bottom: 28px;
    }
    .main-title-banner h1 {
        color: #4A4A4A !important;
        font-size: 2.1rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
    }
    .main-title-banner p {
        color: #666666 !important;
        margin-top: 8px !important;
        font-size: 1rem;
    }
    
    /* 馬卡龍大卡片按鈕（覆蓋 Streamlit 原生按鈕） */
    div.macaron-card > div.stButton > button {
        height: 180px !important;
        width: 100% !important;
        border: none !important;
        border-radius: 20px !important;
        box-shadow: 0 6px 16px rgba(0,0,0,0.05) !important;
        transition: all 0.25s ease-in-out !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 20px !important;
        white-space: pre-wrap !important;
        line-height: 1.5 !important;
    }
    
    /* 懸浮效果：放大與微升 */
    div.macaron-card > div.stButton > button:hover {
        transform: translateY(-6px) scale(1.02) !important;
        box-shadow: 0 12px 24px rgba(0,0,0,0.1) !important;
    }
    
    /* 5 種馬卡龍專屬色彩配置 */
    /* 1. 柔粉色 (聯絡簿) */
    div.card-pink > div.stButton > button {
        background-color: #FFE5EC !important;
        color: #9E2A2B !important;
    }
    div.card-pink > div.stButton > button:hover {
        background-color: #FFC2D1 !important;
    }
    
    /* 2. 薄荷綠 (作業登記) */
    div.card-green > div.stButton > button {
        background-color: #E8F5E9 !important;
        color: #2E7D32 !important;
    }
    div.card-green > div.stButton > button:hover {
        background-color: #C8E6C9 !important;
    }
    
    /* 3. 奶油黃 (座位表) */
    div.card-yellow > div.stButton > button {
        background-color: #FFF9C4 !important;
        color: #F57F17 !important;
    }
    div.card-yellow > div.stButton > button:hover {
        background-color: #FFF59D !important;
    }
    
    /* 4. 晴空藍 (抽籤輪播) */
    div.card-blue > div.stButton > button {
        background-color: #E1F5FE !important;
        color: #0277BD !important;
    }
    div.card-blue > div.stButton > button:hover {
        background-color: #B3E5FC !important;
    }
    
    /* 5. 丁香紫 (倒數計時) */
    div.card-purple > div.stButton > button {
        background-color: #F3E5F5 !important;
        color: #7B1FA2 !important;
    }
    div.card-purple > div.stButton > button:hover {
        background-color: #E1BEE7 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 頂部迎賓 Banner
st.markdown("""
    <div class="main-title-banner">
        <h1>🏫 導師智慧班級管理主控台</h1>
        <p>點擊下方任一功能卡片，即可快速進入管理系統</p>
    </div>
""", unsafe_allow_html=True)

# 第一排：3 個功能卡片格子
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown('<div class="macaron-card card-pink">', unsafe_allow_html=True)
    if st.button("📖\n\n班級聯絡簿\n(801導師專屬)", key="btn_p1", use_container_width=True):
        st.switch_page("pages/01_班級聯絡簿.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="macaron-card card-green">', unsafe_allow_html=True)
    if st.button("📚\n\n作業登記專區\n(全校各科)", key="btn_p2", use_container_width=True):
        st.switch_page("pages/02_作業登記.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="macaron-card card-yellow">', unsafe_allow_html=True)
    if st.button("🪑\n\n座位表管理\n(排座位/印表)", key="btn_p3", use_container_width=True):
        st.switch_page("pages/03_座位表.py")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("") # 增加上下間距

# 第二排：2 個功能卡片格子
col4, col5 = st.columns(2, gap="large")

with col4:
    st.markdown('<div class="macaron-card card-blue">', unsafe_allow_html=True)
    if st.button("🎲\n\n學生抽籤與輪播\n(課堂互動工具)", key="btn_p4", use_container_width=True):
        st.switch_page("pages/04_抽籤與輪播.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="macaron-card card-purple">', unsafe_allow_html=True)
    if st.button("⏳\n\n考試倒數計時器\n(班級公播畫面)", key="btn_p5", use_container_width=True):
        st.switch_page("pages/05_倒數計時器.py")
    st.markdown('</div>', unsafe_allow_html=True)
