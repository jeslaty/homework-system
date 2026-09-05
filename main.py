import os, pandas as pd, streamlit as st

st.set_page_config(page_title="801班務管理主控台", page_icon="🏛️", layout="wide")

# 🎨 注入【全站文字 100% 發光純白、物理就地消滅右上角亂碼原廠選單】最高優先權指令
st.markdown("""
    <style>
    *, .stApp, p, span, label, div, h1, h2, h3, input, button, textarea {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", sans-serif !important;
    }
    /* 🍏 永久鎖定莫蘭迪深藍灰大背景 */
    .stApp { background-color: #1E293B !important; }
    
    /* 🛑【徹底消滅側邊欄與右上角亂碼原廠選單】按鈕直接就地隱藏蒸發，全站乾乾淨淨！ */
    [data-testid="stSidebar"], button[data-testid="collapsedControl"], [data-testid="stSidebarCollapse"],
    #MainMenu, header[data-testid="stHeader"] { 
        display: none !important; visibility: hidden !important; width: 0px !important; height: 0px !important;
    }
    
    /* 🌟【大廳文字 300% 暴風亮化】強迫九宮格大格子內的所有標題、說明小字、點選標籤一律鎖死為「高清晰發光純白」！】 */
    .apple-title, h3, h2, h1, p, span, label, div[data-testid="stMarkdownContainer"] p { 
        color: #FFFFFF !important; 
        -webkit-text-fill-color: #FFFFFF !important; /* 強制解決所有手機與電腦瀏覽器字體發暗發灰的問題 */
        font-weight: 800 !important; 
    }
    .apple-title { font-size: 32px !important; margin-bottom: 20px !important; border-bottom: 3px solid #334155; padding-bottom: 10px; }
    
    /* 🎯 密碼眼睛髒字徹底蒸發技術 */
    div[data-testid="stTextInput"] button span, div[data-testid="stTextInput"] div div div { font-size: 0px !important; color: transparent !important; -webkit-text-fill-color: transparent !important; }
    
    /* 🎯 密碼與帳號白底輸入框、以及連結按鈕內部的字體，維持最好讀的曜石純黑 */
    .stTextInput input, .stPageLink a p {
        color: #0F172A !important; -webkit-text-fill-color: #0F172A !important; font-weight: 800 !important;
    }
    
    /* 📦 儀表板九宮格：使用極致透明灰外殼，配上曜石黑明顯外框，與發光白字形成最強烈黑白對比 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 2.5px solid #334155 !important; border-radius: 16px !important; 
        background-color: #0F172A !important; /* 🌟 物理硬改：卡片底色直接換成曜石深黑底色，襯托白字 */
        padding: 24px !important; margin: 10px !important; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5) !important;
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

# 🏛️ 左右大方塊佈局比例
dash_grid = st.columns(2)

p1_small, p1_big = "pages/01_每日聯絡簿.py", "Pages/01_每日聯絡簿.py"
p2_small, p2_big = "pages/02_成績作業登記.py", "Pages/02_成績作業登記.py"

with dash_grid.container(border=True):
    st.markdown("<h2>📝 01_每日聯絡簿管理</h2>", unsafe_allow_html=True)
    st.write("包含：聯絡簿簽名登記、生活札記完成檢視、學校催收項目建立、以及家長群組即時文字廣播功能。")
    st.write("")
    
    if os.path.exists(p1_small): st.page_link(p1_small, label="點擊開啟 01_每日聯絡簿網頁 ➔", use_container_width=True)
    elif os.path.exists(p1_big): st.page_link(p1_big, label="點擊開啟 01_每日聯絡簿網頁 ➔", use_container_width=True)
    else: st.warning("⚠️ 提示：請確認您的聯絡簿代碼確實上傳在 pages 資料夾中。")

with dash_grid.container(border=True):
    st.markdown("<h2>📊 02_學生作業與成績登記</h2>", unsafe_allow_html=True)
    st.write("包含：日常各科小考成績輸入、各單元作業繳交狀況追蹤、學期成績落點唯讀總表與紀錄導出功能。")
    st.write("")
    
    if os.path.exists(p2_small): st.page_link(p2_small, label="點擊開啟 02_成績作業登記網頁 ➔", use_container_width=True)
    elif os.path.exists(p2_big): st.page_link(p2_big, label="點擊開啟 02_成績作業登記網頁 ➔", use_container_width=True)
    else: st.info("💡 提示：此模組已預留，等您將 02_成績作業登記.py 上傳後將自動啟用。")
