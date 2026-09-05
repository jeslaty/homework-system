import os, pandas as pd, streamlit as st

st.set_page_config(page_title="801班務管理主控台", page_icon="🏛️", layout="wide")

# 🎨 注入【Apple 級極簡 3D 智慧功能磚 - 全文字發光白、全格子一鍵點擊跳轉版】
st.markdown("""
    <style>
    *, .stApp, p, span, label, div, h1, h2, h3, input, button, textarea {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", sans-serif !important;
    }
    .stApp { background-color: #1E293B !important; }
    
    /* 🛑【徹底拔除所有干擾】全站不使用 sidebar，徹底消滅右上角原廠亂碼選單 */
    [data-testid="stSidebar"], button[data-testid="collapsedControl"], [data-testid="stSidebarCollapse"],
    #MainMenu, header[data-testid="stHeader"] { 
        display: none !important; visibility: hidden !important; width: 0px !important; height: 0px !important;
    }
    
    /* 🌟【大廳文字 300% 亮化】強迫登入標籤、主畫面大標題一律鎖死為高清晰發光純白 */
    .apple-title, h3, h2, h1, label, p, span, .stText, [data-testid="stForm"] label, [data-testid="stWidgetLabel"] p { 
        color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-weight: 800 !important; 
    }
    .apple-title { font-size: 32px !important; margin-bottom: 25px !important; border-bottom: 3px solid #334155; padding-bottom: 10px; }
    
    /* 🎯 密碼眼睛髒字徹底蒸發技術 */
    div[data-testid="stTextInput"] button span, div[data-testid="stTextInput"] div div div { font-size: 0px !important; color: transparent !important; -webkit-text-fill-color: transparent !important; }
    
    /* 🎯 帳號密碼輸入框內部的打字體，維持最高對比曜石純黑 */
    .stTextInput input { color: #0F172A !important; -webkit-text-fill-color: #0F172A !important; font-weight: 800 !important; }
    
    /* 🚀【全格點擊卡片終極魔改】強迫整塊大方塊跟原廠跳轉連結融為一體，變成 100% 全區域可直接點擊的 3D 功能磚！ */
    .stPageLink a {
        background-color: #0F172A !important; /* 🌟 物理換色：功能磚改用高級曜石深黑色 */
        border: 2.5px solid #334155 !important; border-radius: 20px !important;
        padding: 35px 24px !important; margin: 12px 0px !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5) !important;
        text-decoration: none !important;
        transition: border 0.2s ease, transform 0.2s ease !important;
    }
    /* 🚀 當滑鼠滑入（Hover）這兩個大格子時，格子外框會瞬間亮起清爽亮藍色 */
    .stPageLink a:hover {
        border: 2.5px solid #38BDF8 !important;
    }
    /* 🚀 強制讓卡片內部的「聯絡簿管理」與「作業登錄系統」文字字體巨大化發光純白呈现 */
    .stPageLink a p {
        color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important;
        font-size: 26px !important; font-weight: 900 !important;
    }
    </style>
""", unsafe_allow_html=True)

if "contact_logged_in" not in st.session_state:
    st.session_state["contact_logged_in"] = False

# 🔒 帳號密碼登入機制
if not st.session_state["contact_logged_in"]:
    st.markdown("### 🔒 801 導師班務管理系統")
    with st.form("login_form"):
        st.markdown("**🔑 教師帳號：**")
        u = st.text_input("u_input", label_visibility="collapsed")
        st.markdown("**🔒 登入密碼：**")
        p = st.text_input("p_input", type="password", label_visibility="collapsed")
        if st.form_submit_button("確認登入"):
            if u.strip() == "teacher" and p.strip() == "12345":
                st.session_state["contact_logged_in"] = True; st.rerun()
            else: st.error("❌ 帳號或密碼錯誤。")
    st.stop()

# ----------------- 🏛️ 九宮格主儀表板畫面 (登入後) -----------------
st.markdown('<div class="apple-title">🏛️ 801 導師班務管理主控台</div>', unsafe_allow_html=True)
st.write("### 📅 請選擇今日要處理的獨立班務項目：")
st.write("")

# 🏛️ 左右大方塊佈局分流
dash_grid = st.columns(2)

p1_small, p1_big = "pages/01_每日聯絡簿.py", "Pages/01_每日聯絡簿.py"
p2_small, p2_big = "pages/02_成績作業登記.py", "Pages/02_成績作業登記.py"

# 🎯【一鍵點擊功能磚大成】徹底拿掉所有冗長說明，整塊大格子就是最乾淨、最直覺的跨頁傳送門！
with dash_grid[0]:
    if os.path.exists(p1_small): st.page_link(p1_small, label="📝 01_聯絡簿管理", use_container_width=True)
    elif os.path.exists(p1_big): st.page_link(p1_big, label="📝 01_聯絡簿管理", use_container_width=True)
    else: st.warning("⚠️ 提示：請確認您的聯絡簿代碼確實上傳在 pages 資料夾中。")

with dash_grid[1]:
    if os.path.exists(p2_small): st.page_link(p2_small, label="📊 02_作業登錄系統", use_container_width=True)
    elif os.path.exists(p2_big): st.page_link(p2_big, label="📊 02_作業登錄系統", use_container_width=True)
    else: st.info("💡 提示：此模組已預留，等您將 02_成績作業登記.py 上傳後將自動啟用。")
