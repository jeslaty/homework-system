import os, pandas as pd, streamlit as st

st.set_page_config(page_title="801班務管理主控台", page_icon="🏛️", layout="wide")

# 🎨 注入【Apple 經典深色暗黑美學 UI - 側邊欄永久蒸發、全文字發光白、全格一鍵跳轉版】
st.markdown("""
    <style>
    *, .stApp, p, span, label, div, h1, h2, h3, input, button, textarea {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", sans-serif !important;
    }
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { background-color: #1E293B !important; }
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], [data-testid="stSidebarContent"],
    button[data-testid="collapsedControl"], [data-testid="stSidebarCollapse"], #MainMenu { 
        display: none !important; visibility: hidden !important; width: 0px !important; height: 0px !important;
    }
    .apple-title, h3, h2, h1, label, p, span, .stText, [data-testid="stForm"] label, [data-testid="stWidgetLabel"] p { 
        color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-weight: 800 !important; 
    }
    .apple-title { font-size: 32px !important; margin-bottom: 25px !important; border-bottom: 3px solid #334155; padding-bottom: 10px; }
    div[data-testid="stTextInput"] button span, div[data-testid="stTextInput"] div div div { font-size: 0px !important; color: transparent !important; -webkit-text-fill-color: transparent !important; }
    .stTextInput input { color: #0F172A !important; -webkit-text-fill-color: #0F172A !important; font-weight: 800 !important; }
    .stPageLink a {
        background-color: #0F172A !important; border: 2.5px solid #334155 !important; border-radius: 20px !important;
        padding: 40px 24px !important; margin: 15px 0px !important; display: flex !important; align-items: center !important; justify-content: center !important;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6) !important; text-decoration: none !important; transition: border 0.2s ease, transform 0.2s ease !important;
    }
    .stPageLink a:hover { border: 2.5px solid #38BDF8 !important; transform: translateY(-4px) !important; }
    .stPageLink a p { color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-size: 28px !important; font-weight: 900 !important; }
    div[data-testid="stForm"] { border: 2px solid #334155 !important; background-color: #1E293B !important; border-radius: 16px !important; padding: 24px !important; }
    </style>
""", unsafe_allow_html=True)

# 🎯【核心技術】初始化全局共用登入狀態鎖
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
                st.session_state["contact_logged_in"] = True
                st.rerun()
            else: st.error("❌ 帳號或密碼錯誤。")
    st.stop()

# ----------------- 🏛️ 九宮格主儀表板畫面 -----------------
st.markdown('<div class="apple-title">🏛️ 801 導師班務管理主控台</div>', unsafe_allow_html=True)
st.write("### 📅 請選擇今日要處理的獨立班務項目：")
st.write("")

dash_grid = st.columns(2)
p1_small, p1_big = "pages/01_每日聯絡簿.py", "Pages/01_每日聯絡簿.py"
p2_small, p2_big = "pages/02_成績作業登記.py", "Pages/02_成績作業登記.py"

with dash_grid:
    if os.path.exists(p1_small): st.page_link(p1_small, label="📝 01_聯絡簿管理", use_container_width=True)
    elif os.path.exists(p1_big): st.page_link(p1_big, label="📝 01_聯絡簿管理", use_container_width=True)
    else: st.warning("⚠️ 提示：請確認您的聯絡簿代碼確實上傳在 pages 資料夾中。")

with dash_grid:
    if os.path.exists(p2_small): st.page_link(p2_small, label="📊 02_作業登錄系統", use_container_width=True)
    elif os.path.exists(p2_big): st.page_link(p2_big, label="📊 02_作業登錄系統", use_container_width=True)
    else: st.info("💡 提示：此模組已預留，等您將 02_成績作業登記.py 上傳後將自動啟用。")
