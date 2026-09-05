import os, streamlit as st

st.set_page_config(page_title="801班務管理主控台", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    *, .stApp, p, span, label, div, h1, h2, h3, input, button, textarea { font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", sans-serif !important; }
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { background-color: #1E293B !important; }
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], [data-testid="stSidebarContent"], button[data-testid="collapsedControl"], [data-testid="stSidebarCollapse"], #MainMenu { display: none !important; visibility: hidden !important; width: 0px !important; height: 0px !important; }
    .apple-title, h3, h2, h1, label, p, span, [data-testid="stForm"] label { color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-weight: 800 !important; }
    .apple-title { font-size: 32px !important; margin-bottom: 25px !important; border-bottom: 3px solid #334155; padding-bottom: 10px; }
    div[data-testid="stTextInput"] button span, div[data-testid="stTextInput"] div div div { font-size: 0px !important; color: transparent !important; -webkit-text-fill-color: transparent !important; }
    .stTextInput input { color: #0F172A !important; -webkit-text-fill-color: #0F172A !important; font-weight: 800 !important; }
    div[data-testid="stForm"] button, div[data-testid="stForm"] button p { color: #000000 !important; -webkit-text-fill-color: #000000 !important; font-weight: 900 !important; }
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

if "contact_logged_in" not in st.session_state:
    st.session_state["contact_logged_in"] = False

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

st.markdown('<div class="apple-title">🏛️ 801 導師班務管理主控台</div>', unsafe_allow_html=True)
st.write("### 📅 請選擇今日要處理的獨立班務項目：")
st.write("")

dash_grid = st.columns(2)
p1, p2 = "pages/01_每日聯絡簿.py", "pages/02_成績作業登記.py"

with dash_grid[0]:
    if os.path.exists(p1): st.page_link(p1 + "?auth=passed", label="📝 01_聯絡簿管理", use_container_width=True)
    else: st.warning("⚠️ 檔案未對齊")

with dash_grid[1]:
    if os.path.exists(p2): st.page_link(p2, label="📊 02_作業登錄系統", use_container_width=True)
    else: st.info("💡 模組已預留")
