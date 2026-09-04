import os
import pandas as pd
import streamlit as st
from datetime import datetime

# 設定網頁標題與圖示
st.set_page_config(page_title="801聯絡簿管理系統", page_icon="📝", layout="wide")

# 🎨 注入【Apple 官網極致清透美學：純白底、深藍粗框、高對比字體】
st.markdown(
    """
    <style>
    /* 🍏 全局強制使用現代、不嚴肅的微軟正黑體與蘋方字體 */
    *, .stApp, p, span, label, div, h1, h2, h3, input, button, textarea {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", "微軟正黑體", sans-serif !important;
    }
    
    /* 🍏 全局大背景：改用純淨高亮白，完全擺脫暗沉與莫蘭迪灰調 */
    .stApp { background-color: #FFFFFF !important; }
    
    /* 🍏 簡約主標題：太空灰高級感 */
    .apple-title { 
        color: #0F172A !important; 
        font-size: 34px !important; 
        font-weight: 800 !important; 
        margin-bottom: 20px !important; 
        border-bottom: 3px solid #E2E8F0;
        padding-bottom: 12px;
    }
    
    /* 👤 學生姓名：純黑、巨大粗體，一秒對焦 */
    .student-title {
        color: #000000 !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        margin-bottom: 12px !important;
    }
    
    /* 📋 學校項目與備註標籤 */
    .item-label { 
        color: #1E40AF !important; 
        font-size: 16px !important; 
        font-weight: 800 !important; 
        margin-top: 12px !important; 
    }

    /* 📋 全局文字高清晰純黑 */
    .stText, p, span, label { color: #000000 !important; font-weight: 700 !important; font-size: 16px !important; }
    
    /* 📦【Apple 視窗立體獨立卡片框】拉開格子間距，搭配海軍藍粗框與強烈對比 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 3px solid #1E3A8A !important;   /* 3px 皇家海軍藍粗邊框，清晰分明 */
        border-radius: 16px !important;         /* 圓角 */
        background-color: #FFFFFF !important;    /* 卡片內部維持極亮純白，拉開最大對比 */
        padding: 20px !important; 
        margin: 16px !important;                 /* 強制拉開格子間距，不再黏在一起 */
        box-shadow: 0 10px 20px rgba(30, 58, 138, 0.08) !important; /* 精緻立體陰影 */
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 🔑 帳號密碼設定
if "contact_logged_in" not in st.session_state:
    st.session_state["contact_logged_in"] = False

if not st.session_state["contact_logged_in"]:
    st.markdown('<div class="apple-title">🔒 801 導師班務管理系統</div>', unsafe_allow_html=True)
    with st.form("login_form"):
        u = st.text_input("教師帳號：")
        p = st.text_input("登入密碼：", type="password")
        if st.form_submit_button("確認登入"):
            if u == "teacher" and p == "12345":
                st.session_state["contact_logged_in"] = True
                st.rerun()
            else:
                st.error("❌ 帳號或密碼錯誤。")
    st.stop()

# ----------------- 系統主畫面 (登入後) -----------------
# 1. 頂級簡約的主標題
st.markdown('<div class="apple-title">📝 801聯絡簿管理系統</div>', unsafe_allow_html=True)

# 2. 🎛️ 【頂部高效管理區】將原本在側邊欄的功能，整齊排在主畫面最上方
col_date, col_add_item, col_logout = st.columns([3, 5, 2])
with col_date:
    current_date = st.date_input("📅 選擇登記/查看日期：", datetime.now())
    date_str = current_date.strftime("%Y-%m-%d")
with col_add_item:
    new_item = st.text_input("➕ 新增學校催收項目：", placeholder="例如：疫苗施打同意書")
    if st.button("建立催收欄位"):
        # 在此處重新讀取資料，防止重複建立
        FILE_NAME = "801班_導師班務紀錄總表.xlsx"
        seats_str = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28"
        student_names = ["王喬昕", "吳岢曈", "李巧彤", "岳昀軒", "林晏以", "林晨琳", "林芮妘", "林苡嫻", "黃榆涵", "黃榆涵", "蔡可琳", "戴彤竹", "羅羽翎", "羅昕彤", "林禹彤", "王楷文", "王駿展", "吳軒佑", "李宇哲", "林柏辰", "張品御", "陳正澤", "陳秉玄", "陳鼎硯", "黃楙軒", "董子以", "劉家佑", "魏辰恩"]
        seat_list = [int(x) for x in seats_str.split(",")]
        
        # 讀取現有 Excel
        if os.path.exists(FILE_NAME):
            try: df_temp = pd.read_excel(FILE_NAME, sheet_name=date_str)
            except: df_temp = pd.DataFrame({"座號": seat_list, "姓名": student_names, "聯絡簿簽名": "已簽 📝", "生活札記": "已寫 🗒️", "備註事項": ""})
        else:
            df_temp = pd.DataFrame({"座號": seat_list, "姓名": student_names, "聯絡簿簽名": "已簽 📝", "生活札記": "已寫 🗒️", "備註事項": ""})
            
        if new_item and new_item not in df_temp.columns:
            df_temp[new_item] = "未繳 ❌"
            with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a" if os.path.exists(FILE_NAME) else "w", if_sheet_exists="replace" if os.path.exists(FILE_NAME) else None) as w:
                df_temp.to_excel(w, sheet_name=date_str, index=False)
            st.rerun()
with col_logout:
    st.write("") # 往下對齊
    if st.button("🔒 安全登出", use_container_width=True):
        st.session_state["contact_logged_in"] = False
        st.rerun()

st.markdown("---")

# 3. 資料初始化與加載
FILE_NAME = "801班_導師班務紀錄總表.xlsx"
seats_str = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28"
student_names = ["王喬昕", "吳岢曈", "李巧彤", "岳昀軒", "林晏以", "林晨琳", "林芮妘", "林苡嫻", "黃榆涵", "黃榆涵", "蔡可琳", "戴彤竹", "羅羽翎", "羅昕彤", "林禹彤", "王楷文", "王駿展", "吳軒佑", "李宇哲", "林柏辰", "張品御", "陳正澤", "陳秉玄", "陳鼎硯", "黃楙軒", "董子以", "劉家佑", "魏辰恩"]
seat_list = [int(x) for x in seats_str.split(",")]

def load_data(target_date):
    df_def = pd.DataFrame({"座號": seat_list, "姓名": student_names, "聯絡簿簽名": "已簽 📝", "生活札記": "已寫 🗒️", "備註事項": ""})
    if not os.path.exists(FILE_NAME):
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as w:
            df_def.to_excel(w, sheet_name=target_date, index=False)
        return df_def
    try: return pd.read_excel(FILE_NAME, sheet_name=target_date)
    except Exception:
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a", if_sheet_exists="replace") as w:
            df_def.to_excel(w, sheet_name=target_date, index=False)
        return df_def

df = load_data(date_str)

def save_data(updated_df, target_date):
    with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a", if_sheet_exists="replace") as w:
        updated_df.to_excel(w, sheet_name=target_date, index=False)

# 4. 📢 【即時催繳廣播台】橫向放大呈現在登記區正上方
st.write(f"### 📢 {date_str} 即時催繳廣播台")
col_broadcast1, col_broadcast2 = st.columns(2)

extra_items = list(df.columns[5:])

with col_broadcast1:
    df_ns = df[df["聯絡簿簽名"] == "未簽 ❌"]
    if not df_ns.empty:
        t_s = f"【801班 {date_str} 聯絡簿未簽名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_ns.iterrows()])
        st.text_area("📋 複製傳至家長群組：", value=t_s, height=120, key="c_s")
    else: st.success("🎉 本日聯絡簿全班皆已簽名！")

with col_broadcast2:
    df_nd = df[df["生活札記"] == "未寫 ❌"]
    if not df_nd.empty:
        t_d = f"【801班 {date_str} 札記未完成名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_nd.iterrows()])
        st.text_area("📋 複製傳至班級群組：", value=t_d, height=120, key="c_d")

if extra_items:
    st.write("👉 學校項目催繳：")
    cols_extra = st.columns(len(extra_items) if len(extra_items) <= 4 else 4)
    for idx_item, item in enumerate(extra_items):
        df_ni = df[df[item] == "未繳 ❌"]
        with cols_extra[idx_item % 4]:
            if not df_ni.empty:
                t_i = f"【801班 {item} 尚未繳交名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_ni.iterrows()])
                st.text_area(f"📋 {item} 催繳：", value=t_i, height=120, key=f"c_{item}")
            else: st.success(f"💯 {item} 皆已繳齊！")

st.markdown("---")

# 5. 🎴 【主畫面：一橫排 4 個學生的卡片網格登記區】
st.write(f"### 📅 日期：{date_str} 紀錄登記區")
st.write("")

for i in range(0, len(df), 4):
    grid = st.columns(4)  # 一排切成 4 個格子

    for idx_grid in range(4):
        student_idx = i + idx_grid
        if student_idx < len(df):
            row_s = df.iloc[student_idx]
            seat_num = int(row_s["座號"])
            name_s = row_s["姓名"]

            gender_icon = "🌸" if seat_num <= 15 else "🍀"

            with grid[idx_grid].container(border=True):
                st.markdown(f'<div class="student-title">{gender_icon} {seat_num}號 {name_s}</div>', unsafe_allow_html=True)

                # 聯絡簿與札記單選鈕
                ns = st.radio(
                    f"聯絡簿_{seat_num}", ["已簽 📝", "未簽 ❌"],
                    index=(["已簽 📝", "未簽 ❌"].index(row_s["聯絡簿簽名"]) if row_s["聯絡簿簽名"] in ["已簽 📝", "未簽 ❌"] else 0),
                    horizontal=True, key=f"s_{seat_num}_{date_str}"
                )
                nd = st.radio(
                    f"札記_{seat_num}", ["已寫 🗒️", "未寫 ❌"],
                    index=(["已寫 🗒️", "未寫 ❌"].index(row_s["生活札記"]) if row_s["生活札記"] in ["已寫 🗒️", "未寫 ❌"] else 0),
                    horizontal=True, key=f"d_{seat_num}_{date_str}"
                )

                if ns != row_s["聯絡簿簽名"] or nd != row_s["生活札記"]:
                    df.loc[df["座號"] == seat_num, "聯絡簿簽名"], df.loc[df["座號"] == seat_num, "生活札記"] = ns, nd
                    save_data(df, date_str)
                    st.rerun()

                # 自訂學校收發項目
                if extra_items:
                    for item in extra_items:
                        st.markdown(f'<div class="item-label">📋 學校收發：{item}</div>', unsafe_allow_html=True)
                        ni = st.radio(
                            f"{item}_{seat_num}", ["已繳 ✅", "未繳 ❌"],
                            index=(["已繳 ✅", "未繳 ❌"].index(row_s[item]) if row_s[item] in ["已繳 ✅", "未繳 ❌"] else 1),
                            horizontal=True, key=f"i_{item}_{seat_num}_{date_str}", label_visibility="collapsed"
                        )
                        if ni != row_s[item]:
                            df.loc[df["座號"] == seat_num, item] = ni
                            save_data(df, date_str)
                            st.rerun()

                # 隨手備註欄
                st.markdown('<div class="item-label">✍️ 隨手備註：</div>', unsafe_allow_html=True)
                nm = st.text_input(
                    f"備註_{seat_num}",
                    value="" if pd.isna(row_s["備註事項"]) else str(row_s["備註事項"]),
                    placeholder="輸入日常備註...", label_visibility="collapsed", key=f"m_{seat_num}_{date_str}"
                )
                if nm != ("" if pd.isna(row_s["備註事項"]) else str(row_s["備註事項"])):
                    df.loc[df["座號"] == seat_num, "備註事項"] = nm
                    save_data(df, date_str)

st.markdown("---")
st.write(f"### 📊 801班 {date_str} 綜合班務總表（唯讀檢視）")
