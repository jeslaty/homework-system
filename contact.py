import os, pandas as pd, streamlit as st
from datetime import datetime

st.set_page_config(page_title="801聯絡簿管理系統", page_icon="📝", layout="wide")

# 🎨 注入【Mac 經典深色暗黑模式大背景 - 25:75 比例、左欄輸入框純黑字、右欄白底高對比卡片】
st.markdown("""
    <style>
    /* 🍏 全局強制使用現代無襯線字體 */
    *, .stApp, p, span, label, div, h1, h2, h3, input, button, textarea {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", sans-serif !important;
    }
    
    /* 🍏 網頁大背景改回老師最愛的：經典莫蘭迪深藍灰 */
    .stApp { background-color: #1E293B !important; }
    
    /* 🛑【徹底封鎖與拔除側邊欄】全站不使用 sidebar，怪字發源地直接消失 */
    [data-testid="stSidebar"], button[data-testid="collapsedControl"], [data-testid="stSidebarCollapse"] { 
        display: none !important; visibility: hidden !important; 
    }
    
    /* 🍏 主標題與大背景上的所有大標題：在深色背景下強制使用高對比純白字體 */
    .apple-title, h3, h2, h1 { 
        color: #FFFFFF !important; font-weight: 800 !important;
    }
    .apple-title {
        font-size: 32px !important; margin-bottom: 20px !important; border-bottom: 3px solid #334155; padding-bottom: 10px;
    }
    
    /* 📋 學校項目與備註標籤：耀眼亮藍色 */
    .item-label { color: #1E3A8A !important; font-size: 15px !important; font-weight: 800 !important; margin-top: 10px !important; }
    
    /* 🎯【左欄白底框黑字特徵】強制讓左欄所有輸入框內文字、日期、按鈕文字一律鎖定為純黑色（#000000）！】 */
    div[col-label="left"] input, div[col-label="left"] select, div[col-label="left"] textarea, div[col-label="left"] button,
    div[data-baseweb="date-picker"] input, div[data-baseweb="input"] input, div[data-baseweb="select"] div,
    .stDateInput input, .stTextInput input, .stButton button p {
        color: #000000 !important; -webkit-text-fill-color: #000000 !important; font-weight: 800 !important;
    }
    ::placeholder, .stTextInput input::placeholder { color: #666666 !important; -webkit-text-fill-color: #666666 !important; }
    
    /* 📦【3D 原生獨立卡片框內文字】強迫學生格子內部（白底）的所有選項、文字一律維持最大對比的「純黑色」 */
    div[data-testid="stVerticalBlockBorderWrapper"] p, 
    div[data-testid="stVerticalBlockBorderWrapper"] span, 
    div[data-testid="stVerticalBlockBorderWrapper"] label,
    div[data-testid="stVerticalBlockBorderWrapper"] div { 
        color: #000000 !important; font-weight: 800 !important; font-size: 16px !important; 
    }
    
    /* 📦【3D 原生獨立卡片框設定】拉開格子間距，卡片內部維持乾淨高亮白底，形成最強烈對比 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 2.5px solid #0F172A !important; border-radius: 16px !important;
        background-color: #FFFFFF !important; padding: 16px !important; margin: 8px !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
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

# 🏛️ 【左右大版面分流配置：左直欄 25%, 右直欄 75%】
col_left_panel, col_right_students = st.columns()

with col_left_panel:
    st.markdown('<div col-label="left">', unsafe_allow_html=True)
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
        st.text_area("📋 複製傳至家長群組：", value=t_s, height=120, key="c_s")
    else: st.success("🎉 本日聯絡簿全班皆已簽名！")

    df_nd = df[df["生活札記"] == "未寫 ❌"]
    if not df_nd.empty:
        t_d = f"【801班 {date_str} 札記未完成名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_nd.iterrows()])
        st.text_area("📋 複製傳至班級群組：", value=t_d, height=120, key="c_d")

    if extra_items:
        st.markdown("---")
        for item in extra_items:
            df_ni = df[df[item] == "未繳 ❌"]
            if not df_ni.empty:
                t_i = f"【801班 {item} 尚未繳交名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_ni.iterrows()])
                st.text_area(f"📋 複製 {item} 催繳文字：", value=t_i, height=120, key=f"c_{item}")
            else: st.success(f"💯 {item} 皆已繳齊！")
    st.markdown('</div>', unsafe_allow_html=True)

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
                
                with grid[idx_grid].container(border=True):
                    # 名字與座號採用加粗純黑大字呈現，100% 黑白分明，絕對不會再有隱形字！
                    st.write(f"### {gender_icon} {seat_num}號 {name_s}")
                    
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
