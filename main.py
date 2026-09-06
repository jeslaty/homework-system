import streamlit as st

st.set_page_config(
    page_title="801 導師班級管理系統",
    page_icon="🏫",
    layout="wide"
)

# 1. 關鍵修復：優先讀取 URL 參數，還原登入狀態（防止 switch_page 時狀態丟失）
if "auth" in st.query_params and st.query_params["auth"] == "true":
    st.session_state["authenticated"] = True

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
# CSS 樣式：畫面 100% 還原，乾乾淨淨，沒有任何多餘按鈕
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

    /* 整張方格即連結 */
    .card-link {
        text-decoration: none !important;
        display: block;
        margin-bottom: 20px;
    }

    /* 馬卡龍卡片本體 */
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
    .card:hover {
        transform: translateY(-8px) scale(1.02);
    }

    .card-pink {
        background: #FFF0F5;
        border: 2px solid #FFD1DC;
        box-shadow: 0 8px 20px rgba(255, 182, 193, 0.25);
    }
    .card-pink:hover { box-shadow: 0 16px 30px rgba(255, 182, 193, 0.45); }

    .card-blue {
        background: #F0F8FF;
        border: 2px solid #BAE6FD;
        box-shadow: 0 8px 20px rgba(173, 216, 230, 0.25);
    }
    .card-blue:hover { box-shadow: 0 16px 30px rgba(173, 216, 230, 0.45); }

    .card-purple {
        background: #F5F0FF;
        border: 2px solid #DDD6FE;
        box-shadow: 0 8px 20px rgba(221, 160, 221, 0.25);
    }
    .card-purple:hover { box-shadow: 0 16px 30px rgba(221, 160, 221, 0.45); }

    .card-icon { font-size: 3.2rem; margin-bottom: 12px; }
    .card-title { font-size: 1.35rem; font-weight: 800; color: #1E293B; margin-bottom: 6px; }
    .card-subtitle { font-size: 0.9rem; color: #64748B; font-weight: 600; }

    /* 登出按鈕樣式 */
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

# 2. 未登入：安全驗證畫面
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
                st.query_params["auth"] = "true"
                st.rerun()
            else:
                st.error("帳號或密碼錯誤，請重新輸入！")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 3. 驗證通過：純粹美麗的大方格主控台
st.markdown("""
    <div class="header-banner">
        <div class="main-title">🏫 班級經營主控台</div>
        <div class="sub-title">點擊下方任一功能大方格，即可快速進入管理系統</div>
    </div>
""", unsafe_allow_html=True)

# 第一排 3 個大方格（整張方格直接點擊跳轉）
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <a href="/每日聯絡簿?auth=true" target="_self" class="card-link">
            <div class="card card-pink">
                <div class="card-icon">📖</div>
                <div class="card-title">班級聯絡簿</div>
                <div class="card-subtitle">(801導師專屬)</div>
            </div>
        </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <a href="/作業登記?auth=true" target="_self" class="card-link">
            <div class="card card-blue">
                <div class="card-icon">📚</div>
                <div class="card-title">作業登記專區</div>
                <div class="card-subtitle">(各任課班級)</div>
            </div>
        </a>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <a href="/座位表?auth=true" target="_self" class="card-link">
            <div class="card card-purple">
                <div class="card-icon">🪑</div>
                <div class="card-title">座位表管理</div>
                <div class="card-subtitle">(排座位/印表)</div>
            </div>
        </a>
    """, unsafe_allow_html=True)

# 第二排 3 個擴充大方格
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
        <div class="card card-blue" style="opacity: 0.8; cursor: not-allowed;">
            <div class="card-icon">🎲</div>
            <div class="card-title">學生抽籤學輪播</div>
            <div class="card-subtitle">(課堂互動/提問)</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
        <div class="card card-pink" style="opacity: 0.8; cursor: not-allowed;">
            <div class="card-icon">⏳</div>
            <div class="card-title">考試倒數計時器</div>
            <div class="card-subtitle">(段考/倒數提醒)</div>
        </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
        <div class="card card-purple" style="opacity: 0.8; cursor: not-allowed;">
            <div class="card-icon">➕</div>
            <div class="card-title">新增功能預留區</div>
            <div class="card-subtitle">(點擊可擴充)</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# 最底下的獨立橫排登出按鈕
st.markdown('<div class="logout-btn-container">', unsafe_allow_html=True)
if st.button("🔒 登出班級管理系統", use_container_width=True):
    st.session_state["authenticated"] = False
    st.query_params.clear()
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
