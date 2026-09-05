import streamlit as st

st.set_page_config(page_title="801班務管理主控台", page_icon="🏛️", layout="wide")

# 🎨 注入【Apple 經典深色暗黑美學 UI - 雙格儀表板版】
st.markdown("""
    <style>
    *, .stApp, p, span, label, div, h1, h2, h3, input, button, textarea {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", sans-serif !important;
    }
    .stApp { background-color: #1E293B !important; }
    [data-testid="stSidebar"], button[data-testid="collapsedControl"], [data-testid="stSidebarCollapse"] { display: none !important; visibility: hidden !important; }
    .apple-title, h3, h2, h1, div[data-testid="stForm"] label { color: #FFFFFF !important; font-weight: 800 !important; }
    .apple-title { font-size: 32px !important; margin-bottom: 20px !important; border-bottom: 3px solid #334155; padding-bottom: 10px; }
    
    /* 🎯 密碼眼睛髒字徹底蒸發技術 */
    div[data-testid="stTextInput"] button span, div[data-testid="stTextInput"] div div div { font-size: 0px !important; color: transparent !important; -webkit-text-fill-color: transparent !important; }
    
    /* 🎯 全站白底框、按鈕文字 100% 強制深色，黑白分明 */
    input, select, textarea, button, .stTextInput input, .stButton button, .stButton button p {
        color: #0F172A !important; -webkit-text-fill-color: #0F172A !important; font-weight: 800 !important;
    }
    
    /* 📦 儀表板九宮格：白底獨立大卡片框 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 2.5px solid #0F172A !important; border-radius: 16px !important; background-color: #FFFFFF !important; 
        padding: 24px !important; margin: 10px !important; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4) !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] p, div[data-testid="stVerticalBlockBorderWrapper"] h2 {
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

if "contact_logged_in" not in st.session_state:
    st.session_state["contact_logged_in"] = False

# 🔒 帳號密碼登入機制（安全小眼睛完美保留）
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

# ----------------- 🏛️ 登入後：九宮格主儀表板畫面 -----------------
st.markdown('<div class="apple-title">🏛️ 801 導師班務管理主控台</div>', unsafe_allow_html=True)
st.write("### 📅 請選擇今日要處理的獨立班務項目：")
st.write("")

# 建立一橫排 2 個獨立大方塊（九宮格）
dash_grid = st.columns(2)

with dash_grid[0].container(border=True):
    st.markdown("## 📝 01_每日聯絡簿管理")
    st.write("包含：聯絡簿簽名登記、生活札記完成檢視、學校催收項目建立、以及家長群組即時文字廣播功能。")
    st.write("")
    st.page_link("pages/01_每日聯絡簿.py", label="點擊開啟 01_每日聯絡簿網頁 ➔", use_container_width=True)

with dash_grid[1].container(border=True):
    st.markdown("## 📊 02_學生作業與成績登記")
    st.write("包含：日常各科小考成績輸入、各單元作業繳交狀況追蹤、學期成績落點唯讀總表與紀錄導出功能。")
    st.write("")
    st.page_link("pages/02_成績作業登記.py", label="點擊開啟 02_成績作業登記網頁 ➔", use_container_width=True)
