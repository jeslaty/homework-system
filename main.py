import streamlit as st

st.set_page_config(
    page_title="班級經營管理系統",
    page_icon="🏫",
    layout="wide"
)

# 隱藏預設選單與頁首，並注入完美結合的 CSS 樣式
st.markdown("""
    <style>
    /* 隱藏 Streamlit 預設側邊欄與頁首 */
    [data-testid="stSidebar"], button[data-testid="collapsedControl"], header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 右圖漸層背景 */
    .stApp {
        background: linear-gradient(135deg, #FFF0F5 0%, #F0F4FF 50%, #F5F0FF 100%);
    }
    
    /* 左圖圓角頂部 Banner (配右圖溫和底色) */
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
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #334155;
        margin-bottom: 8px;
    }
    .sub-title {
        font-size: 1rem;
        color: #64748B;
        font-weight: 500;
    }

    /* 左圖卡片形式 + 右圖馬卡龍配色與懸浮效果 */
    .card-link {
        text-decoration: none !important;
        color: inherit !important;
        display: block;
    }
    
    .card {
        border-radius: 24px;
        padding: 36px 20px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        cursor: pointer;
        height: 220px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
    }
    .card:hover {
        transform: translateY(-8px) scale(1.02);
    }

    /* 右圖馬卡龍三色 + 擴充色 */
    .card-pink {
        background: #FFF0F5;
        border: 2px solid #FFD1DC;
        box-shadow: 0 8px 20px rgba(255, 182, 193, 0.25);
    }
    .card-pink:hover {
        box-shadow: 0 16px 30px rgba(255, 182, 193, 0.45);
    }

    .card-blue {
        background: #F0F8FF;
        border: 2px solid #BAE6FD;
        box-shadow: 0 8px 20px rgba(173, 216, 230, 0.25);
    }
    .card-blue:hover {
        box-shadow: 0 16px 30px rgba(173, 216, 230, 0.45);
    }

    .card-purple {
        background: #F5F0FF;
        border: 2px solid #DDD6FE;
        box-shadow: 0 8px 20px rgba(221, 160, 221, 0.25);
    }
    .card-purple:hover {
        box-shadow: 0 16px 30px rgba(221, 160, 221, 0.45);
    }

    /* 文字與圖示樣式 */
    .card-icon { font-size: 3.2rem; margin-bottom: 12px; }
    .card-title { font-size: 1.35rem; font-weight: 800; color: #1E293B; margin-bottom: 6px; }
    .card-subtitle { font-size: 0.9rem; color: #64748B; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# 1. 初始化登入狀態
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 2. 未登入：顯示帳號密碼驗證
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

# 3. 驗證通過：主控台（使用原生按鈕保持登入狀態）
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
        <div class="card card-pink">
            <div class="card-icon">📖</div>
            <div class="card-title">班級聯絡簿</div>
            <div class="card-subtitle">(801導師專屬)</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("點擊進入 ➔", key="btn_01", use_container_width=True):
        st.switch_page("pages/01_每日聯絡簿.py")  # 👈 請確認檔名與路徑一致

with col2:
    st.markdown("""
        <div class="card card-blue">
            <div class="card-icon">📚</div>
            <div class="card-title">作業登記專區</div>
            <div class="card-subtitle">(全校各科)</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("點擊進入 ➔", key="btn_02", use_container_width=True):
        st.switch_page("pages/02_作業登記.py")

with col3:
    st.markdown("""
        <div class="card card-purple">
            <div class="card-icon">🪑</div>
            <div class="card-title">座位表管理</div>
            <div class="card-subtitle">(排座位/印表)</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("點擊進入 ➔", key="btn_03", use_container_width=True):
        st.switch_page("pages/03_座位表.py")

# 第二排 3 個擴充大方格
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
        <div class="card card-blue">
            <div class="card-icon">🎲</div>
            <div class="card-title">學生抽籤學輪播</div>
            <div class="card-subtitle">(課堂互動/提問)</div>
        </div>
    """, unsafe_allow_html=True)
    st.button("點擊進入 ➔", key="btn_04", use_container_width=True, disabled=True)

with col5:
    st.markdown("""
        <div class="card card-pink">
            <div class="card-icon">⏳</div>
            <div class="card-title">考試倒數計時器</div>
            <div class="card-subtitle">(段考/倒數提醒)</div>
        </div>
    """, unsafe_allow_html=True)
    st.button("點擊進入 ➔", key="btn_05", use_container_width=True, disabled=True)

with col6:
    st.markdown("""
        <div class="card card-purple">
            <div class="card-icon">➕</div>
            <div class="card-title">新增功能預留區</div>
            <div class="card-subtitle">(點擊可擴充)</div>
        </div>
    """, unsafe_allow_html=True)
    st.button("點擊進入 ➔", key="btn_06", use_container_width=True, disabled=True)

st.write("")

# 登出按鈕
col_l, col_r = st.columns([0.85, 0.15])
with col_r:
    if st.button("🔒 登出系統", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()
