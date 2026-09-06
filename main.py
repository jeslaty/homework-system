import streamlit as st

st.set_page_config(page_title="班級經營主控台", page_icon="🏫", layout="wide")

# CSS 視覺美化：莫蘭迪奶茶底色 + 隱藏原生標頭
st.markdown("""
    <style>
    /* 隱藏側邊欄與頁首 */
    [data-testid="stSidebar"], 
    button[data-testid="collapsedControl"], 
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 全頁背景：暖色莫蘭迪奶茶底色 */
    .stApp, .stApp > header, [data-testid="stAppViewContainer"] {
        background-color: #F2EFE9 !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", sans-serif;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1100px !important;
    }
    
    /* 頁頭 Banner */
    .main-title-banner {
        background: linear-gradient(135deg, #E6E2DD 0%, #D8D2C9 100%);
        padding: 24px;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 35px;
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

    /* 將 Streamlit 原生按鈕覆蓋成透明點擊層 */
    div.stButton > button {
        height: 220px !important;
        width: 100% !important;
        margin-top: -220px !important;
        position: relative !important;
        z-index: 10 !important;
        opacity: 0 !important; /* 隱藏原生按鈕，保留透明點擊區 */
        cursor: pointer !important;
    }
    
    /* 自訂大方格視覺卡片 */
    .macaron-box {
        height: 220px;
        width: 100%;
        border-radius: 28px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
        transition: all 0.25s ease-in-out;
        text-align: center;
        padding: 20px;
        box-sizing: border-box;
    }
    
    .macaron-box:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 16px 30px rgba(0, 0, 0, 0.12);
    }
    
    /* 1. 淺粉馬卡龍色彩 */
    .bg-pink {
        background-color: #FFE5EC !important;
        color: #8C2F39 !important;
        border: 2px solid #FFC2D1;
    }
    
    /* 2. 淺藍馬卡龍色彩 */
    .bg-blue {
        background-color: #E0F2FE !important;
        color: #0369A1 !important;
        border: 2px solid #BAE6FD;
    }
    
    .card-icon { font-size: 2.5rem; margin-bottom: 8px; }
    .card-title { font-size: 1.35rem; font-weight: 800; line-height: 1.3; }
    .card-sub { font-size: 0.95rem; font-weight: 600; margin-top: 4px; opacity: 0.85; }
    </style>
""", unsafe_allow_html=True)

# 頂部 Banner
st.markdown("""
    <div class="main-title-banner">
        <h1>🏫 班級經營主控台</h1>
        <p>點擊下方任一功能大方格，即可快速進入管理系統</p>
    </div>
""", unsafe_allow_html=True)

# --- 九宮格第一排 ---
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
        <div class="macaron-box bg-pink">
            <div class="card-icon">📖</div>
            <div class="card-title">班級聯絡簿</div>
            <div class="card-sub">(801導師專屬)</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("p1", key="btn_p1", use_container_width=True):
        st.switch_page("pages/01_每日聯絡簿.py")

with col2:
    st.markdown("""
        <div class="macaron-box bg-blue">
            <div class="card-icon">📚</div>
            <div class="card-title">作業登記專區</div>
            <div class="card-sub">(任教班級作業催繳)</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("p2", key="btn_p2", use_container_width=True):
        st.switch_page("pages/02_作業登記.py")

with col3:
    st.markdown("""
        <div class="macaron-box bg-pink">
            <div class="card-icon">🪑</div>
            <div class="card-title">座位表管理</div>
            <div class="card-sub">(排座位/印表)</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("p3", key="btn_p3", use_container_width=True):
        st.switch_page("pages/03_座位表.py")

st.write("") # 上下排間距

# --- 九宮格第二排 ---
col4, col5, col6 = st.columns(3, gap="large")

with col4:
    st.markdown("""
        <div class="macaron-box bg-blue">
            <div class="card-icon">🎲</div>
            <div class="card-title">學生抽籤與輪播</div>
            <div class="card-sub">(課堂互動工具)</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("p4", key="btn_p4", use_container_width=True):
        st.switch_page("pages/04_抽籤與輪播.py")

with col5:
    st.markdown("""
        <div class="macaron-box bg-pink">
            <div class="card-icon">⏳</div>
            <div class="card-title">考試倒數計時器</div>
            <div class="card-sub">(班級公播畫面)</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("p5", key="btn_p5", use_container_width=True):
        st.switch_page("pages/05_倒數計時器.py")

with col6:
    st.markdown("""
        <div class="macaron-box bg-blue">
            <div class="card-icon">➕</div>
            <div class="card-title">新增功能預留區</div>
            <div class="card-sub">(未來擴充)</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("p6", key="btn_p6", use_container_width=True):
        st.toast("💡 此功能尚未開放，敬請期待！", icon="✨")
