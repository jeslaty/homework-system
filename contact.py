import os, pandas as pd, streamlit as st
from datetime import datetime

st.set_page_config(page_title="801聯絡簿管理系統", page_icon="📝", layout="wide")

# 🎨 注入【Mac 經典深色暗黑模式 UI - 終極日期文字 100% 強制純黑高對比版】
st.markdown("""
    <style>
    /* 🍏 全局強制使用現代、不嚴肅的微軟正黑體與蘋方字體 */
    *, .stApp, p, span, label, div, h1, h2, h3, input, button, textarea {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", "微軟正黑體", sans-serif !important;
    }
    
    /* 🍏 全局大背景加深：莫蘭迪深藍灰 */
    .stApp { background-color: #1E293B !important; }
    
    /* 🛑【徹底封鎖與拔除側邊欄】全站不使用 sidebar */
    [data-testid="stSidebar"], button[data-testid="collapsedControl"], [data-testid="stSidebarCollapse"] { 
        display: none !important; visibility: hidden !important; 
    }
    
    /* 🍏 標題文字：在深色背景下強制使用高對比純白字體 */
    .apple-title { 
        color: #FFFFFF !important; font-size: 32px !important; font-weight: 800 !important; 
        margin-bottom: 20px !important; border-bottom: 3px solid #334155; padding-bottom: 10px;
    }
    
    /* 📋 學校項目與備註標籤：清爽亮藍色 */
    .item-label { 
        color: #38BDF8 !important; font-size: 15px !important; font-weight: 800 !important; margin-top: 12px !important; margin-bottom: 4px !important;
    }
    
    /* 📋 深色背景上的管理區與紀錄區大標題：一律變純白 */
    h3, h2, h1 { color: #FFFFFF !important; font-weight: 800 !important; }
    
    /* 🌟【大背景上的文字與選項文字轉為高清晰發光白】 */
    .stText, p, span, label, div, .stWidgetLabel p, [data-testid="stWidgetLabel"] { 
        color: #FFFFFF !important; font-weight: 800 !important; font-size: 16px !important; 
    }
    
    /* 🎯【終極核心大必殺：穿透 Streamlit 官方深層加密外殼，強迫將日期選擇器、一般輸入框、選單內的所有隱藏文字一律鎖定為特粗曜石黑（#0F172A）！】 */
    input, select, textarea, button, 
    div[data-baseweb="date-picker"] input, 
    div[data-baseweb="input"] input,
    div[data-baseweb="input"] div,
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] span,
    .stDateInput input, .stTextInput input,
    .stButton button p {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important; /* 強制解決蘋果手機/平板瀏覽器的輸入框字體發白問題 */
        font-weight: 800 !important;
    }
    
    /* 針對輸入框內預設提示文字（Placeholder）也強制加深，拒絕隱形字 */
    ::placeholder, .stTextInput input::placeholder, input::placeholder {
        color: #555555 !important;
        -webkit-text-fill-color: #555555 !important;
        font-weight: 700 !important;
    }
    
    /* 🎨【名牌內部字體：強制鎖定為特粗純黑色（#000000）】 */
    .student-badge-text {
        color: #000000 !important;
        font-size: 21px !important;
        font-weight: 900 !important;
        white-space: nowrap !important;
        letter-spacing: 0.5px !important;
    }
    
    /* 📦【3D 原生獨立卡片框設定】卡片底色與大背景拉開，維持黑白分明 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 2.5px solid #0F172A !important; border-radius: 16px !important;
        background-color: #1E293B !important; padding: 16px !important; margin: 10px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)

if "contact_logged_in" not in st.session_state:
    st.session_state["contact_logged_in"] = False

# 🔒 帳號密碼登入機制
if not st.session_state["contact_logged_in"]:
    st.markdown('<div class="apple-title">🔒 801 導師班務管理系統</div>', unsafe_allow_html=True)
    with st.form("login_form"):
        u = st.text_input("教師帳號：")
        p = st.text_input("登入密碼：", type="password")
        if st.form_submit_button("確認登入"):
            if u.strip() == "teacher" and p.strip() == "12345":
                st.session_state["contact_logged_in"] = True
                st.rerun()
            else: st.error("❌ 帳號或密碼錯誤。")
    st.stop()

# ----------------- 系統主畫面 (登入後) -----------------
st.markdown('<div class="apple-title">📝 801聯絡簿系統</div>', unsafe_allow_html=True)

FILE_NAME = "801班_導師班務紀錄總表.xlsx"
seats_str = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28"
student_names = ["王喬昕", "吳岢曈", "李巧彤", "岳昀軒", "林晏以", "林晨琳", "林芮妘", "林苡嫻", "黃榆涵", "黃榆涵", "蔡可琳", "戴彤竹", "羅羽翎", "羅昕彤", "林禹彤", "王楷文", "王駿展", "吳軒佑", "李宇哲", "林柏辰", "張品御", "陳正澤", "陳秉玄", "陳鼎硯", "黃楙軒", "董子以", "劉家佑", "魏辰恩"]
seat_list = [int(x) for x in seats_str.split(",")]

def load_data(target_date):
    df_def = pd.DataFrame({"座號": seat_list, "姓名": student_names, "聯絡簿簽名": "已簽 📝", "生活札記": "已寫 🗒️", "備註事項": ""})
    if not os.path.exists(FILE_NAME):
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as w: df_def.to_excel(w, sheet_name=target_date, index=False)
        return df_def
    try: return pd.read_excel(FILE_NAME, sheet_name=target_date)
    except:
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a", if_sheet_exists="replace") as w: df_def.to_excel(w, sheet_name=target_date, index=False)
        return df_def

# 🏛 *【左右大版面分流配置：左直欄 25%, 右直欄 75% - 完美鎖定比例參數！】*
col_left_panel, col_right_students = st.columns([1, 3])

with col_left_panel:
    st.write("### 📅 班務管理與切換")
    current_date = st.date_input("選擇登記/查看日期：", datetime.now(), key="main_date")
    date_str = current_date.strftime("%Y-%m-%d")
    df = load_data(date_str)
    extra_items = list(df.columns[5:])
    
    def save_data(updated_df, target_date):
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a", if_sheet_exists="replace") as w: updated_df.to_excel(w, sheet_name=target_date, index=False)

    new_item = st.text_input("➕ 新增學校催收項目：", placeholder="例如：疫苗施打同意書", key="main_item")
    if st.button("建立催收欄位", use_container_width=True):
        if new_item and new_item not in df.columns:
            df[new_item] = "未繳 ❌"
            save_data(df, date_str); st.rerun()
            
    if st.button("🔒 安全登出系統", use_container_width=True):
        st.session_state["contact_logged_in"] = False; st.rerun()

    st.markdown("---")
    st.write(f"### 📢 {date_str} 即時廣播台")
    
    df_ns = df[df["聯絡簿簽名"] == "未簽 ❌"]
    if not df_ns.empty:
        t_s = f"【801班 {date_str} 聯絡簿未簽名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_ns.iterrows()])
        st.text_area("📋 複製傳至家長群組：", value=t_s, height=130, key="c_s")
    else: st.success("🎉 本日聯絡簿全班皆已簽名！")

    df_nd = df[df["生活札記"] == "未寫 ❌"]
    if not df_nd.empty:
        t_d = f"【801班 {date_str} 札記未完成名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_nd.iterrows()])
        st.text_area("📋 複製傳至班級群組：", value=t_d, height=130, key="c_d")

    if extra_items:
        st.markdown("---")
        for item in extra_items:
            df_ni = df[df[item] == "未繳 ❌"]
            if not df_ni.empty:
                t_i = f"【801班 {item} 尚未繳交名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_ni.iterrows()])
                st.text_area(f"📋 複製 {item} 催繳文字：", value=t_i, height=130, key=f"c_{item}")
            else: st.success(f"💯 {item} 皆已繳齊！")

with col_right_students:
    st.write("### 📅 紀錄登記區")
    st.write("")

    for i in range(0, len(df), 4):
        grid = st.columns(4)
        for idx_grid in range(4):
            student_idx = i + idx_grid
            if student_idx < len(df):
                row_s = df.iloc[student_idx]
                seat_num = int(row_s["座號"])
                name_s = row_s["姓名"]
                gender_icon = "🌸" if seat_num <= 15 else "🍀"
                
                if seat_num <= 15:
                    html_badge = f'<div style="background-color:#FFF1F2;border:2.5px solid #E11D48;border-radius:10px;padding:10px 4px;margin-bottom:12px;text-align:center;box-shadow:0 4px 6px rgba(225,29,72,0.06);"><span class="student-badge-text">{gender_icon} {seat_num}號 {name_s}</span></div>'
                else:
                    html_badge = f'<div style="background-color:#F0F7FF;border:2.5px solid #2563EB;border-radius:10px;padding:10px 4px;margin-bottom:12px;text-align:center;box-shadow:0 4px 6px rgba(37,99,236,0.06);"><span class="student-badge-text">{gender_icon} {seat_num}號 {name_s}</span></div>'

                with grid[idx_grid].container(border=True):
                    st.markdown(html_badge, unsafe_allow_html=True)
                    
                    ns = st.radio(f"聯絡簿_{seat_num}", ["已簽 📝", "未簽 ❌"], index=["已簽 📝", "未簽 ❌"].index(row_s["聯絡簿簽名"]) if row_s["聯絡簿簽名"] in ["已簽 📝", "未簽 ❌"] else 0, horizontal=True, key=f"s_{seat_num}_{date_str}")
                    nd = st.radio(f"札記_{seat_num}", ["已寫 🗒️", "未寫 ❌"], index=["已寫 🗒️", "未寫 ❌"].index(row_s["生活札記"]) if row_s["生活札記"] in ["已寫 🗒️", "未寫 ❌"] else 0, horizontal=True, key=f"d_{seat_num}_{date_str}")
                    
                    if ns != row_s["聯絡簿簽名"] or nd != row_s["生活札記"]:
                        df.loc[df["座號"] == seat_num, "聯絡簿簽名"], df.loc[df["座號"] == seat_num, "生活札記"] = ns, nd
                        save_data(df, date_str); st.rerun()
                    
                    if extra_items:
                        for item in extra_items:
                            st.markdown(f'<div class="item-label">📋 學校收發：{item}</div>', unsafe_allow_html=True)
                            ni = st.radio(f"{item}_{seat_num}", ["已繳 ✅", "未繳 ❌"], index=["已繳 ✅", "未繳 ❌"].index(row_s[item]) if row_s[item] in ["已繳 ✅", "未繳 ❌"] else 1, horizontal=True, key=f"i_{item}_{seat_num}_{date_str}", label_visibility="collapsed")
                            if ni != row_s[item]: df.loc[df["座號"] == seat_num, item] = ni; save_data(df, date_str); st.rerun()
                    
                    st.markdown('<div class="item-label">✍️ 隨手備註：</div>', unsafe_allow_html=True)
                    current_memo = "" if pd.isna(row_s["備註事項"]) else str(row_s["備註事項"])
                    nm = st.text_input(f"備註_{seat_num}", value=current_memo, placeholder="輸入日常備註...", label_visibility="collapsed", key=f"m_{seat_num}_{date_str}")
                    if nm != current_memo: df.loc[df["座號"] == seat_num, "備註事項"] = nm; save_data(df, date_str)

st.markdown("---")
st.markdown(f"<h3 style='color:#FFFFFF;'>📊 801班 {date_str} 綜合班務總表（唯讀檢視）</h3>", unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)
