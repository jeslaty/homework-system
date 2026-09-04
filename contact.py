import os, pandas as pd, streamlit as st
from datetime import datetime

st.set_page_config(page_title="801聯絡簿管理系統", page_icon="📝", layout="wide")

# 🎨 注入【導師班專屬：莫蘭迪活力男女雙色系】與【全包覆型 3D 懸浮變色特效】
st.markdown("""
    <style>
    /* 全局背景：極致優雅的暖奶油白 */
    .stApp { background-color: #FAFAFA !important; }
    /* 左側邊欄：內斂的霧灰色 */
    [data-testid="stSidebar"] { background-color: #F1F5F9 !important; }
    
    /* 🌊 巨大化、充滿魄力的皇家藍主標題 */
    .giant-title { color: #1E3A8A !important; font-size: 42px !important; font-weight: 900 !important; font-family: "Noto Sans TC", sans-serif; margin-bottom: 25px !important; }
    
    /* 👤 學生姓名純黑大字體 */
    .student-title { color: #000000 !important; font-size: 24px !important; font-weight: 900 !important; margin-bottom: 12px !important; }
    
    /* 📋 學校項目與備註字體 */
    .item-label { color: #1E293B !important; font-size: 15px !important; font-weight: 800 !important; margin-top: 10px !important; }
    .stText, p, span, label { color: #000000 !important; font-weight: 700 !important; font-size: 14px !important; }

    /* ========================================================
       💡 這裡是最神奇的地方：直接針對 Streamlit 原生的一格一格格子 (st.container) 
       注入「滑鼠移入、整格連同按鈕備註一起 3D 變深彈起」的特效程式碼！
       ======================================================== */
       
    /* 👧 女生格子 (1~15號)：預設為莫蘭迪溫柔粉 */
    .girl-box div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 3px solid #FDA4AF !important; /* 珊瑚粉細緻粗框 */
        border-radius: 16px !important;
        background-color: #FFF5F5 !important; /* 極淡粉紅底色 */
        padding: 18px !important; margin-bottom: 14px !important;
        box-shadow: 0 4px 6px rgba(253, 164, 175, 0.1) !important;
        transition: all 0.25s ease-in-out !important;
    }
    /* 👧 女生懸浮：整格(含按鈕)一起變深粉、往上彈起、陰影爆發 */
    .girl-box div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        background-color: #FFE4E6 !important; /* 蜜桃粉色 */
        border: 3px solid #E11D48 !important;   /* 邊框變深玫瑰紅 */
        transform: translateY(-6px) scale(1.02) !important;
        box-shadow: 0 20px 25px -5px rgba(225, 29, 72, 0.15) !important;
    }

    /* 👦 男生格子 (16~28號)：預設為莫蘭迪清爽藍 */
    .boy-box div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 3px solid #93C5FD !important; /* 晴空藍細緻粗框 */
        border-radius: 16px !important;
        background-color: #F0F7FF !important; /* 極淡藍色底色 */
        padding: 18px !important; margin-bottom: 14px !important;
        box-shadow: 0 4px 6px rgba(147, 197, 253, 0.1) !important;
        transition: all 0.25s ease-in-out !important;
    }
    /* 👦 男生懸浮：整格(含按鈕)一起變深藍、往上彈起、陰影爆發 */
    .boy-box div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        background-color: #E0F2FE !important; /* 天空藍色 */
        border: 3px solid #2563EB !important;   /* 边框變皇家正藍 */
        transform: translateY(-6px) scale(1.02) !important;
        box-shadow: 0 20px 25px -5px rgba(37, 99, 236, 0.15) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🔑 帳號密碼設定
if "contact_logged_in" not in st.session_state:
    st.session_state["contact_logged_in"] = False

if not st.session_state["contact_logged_in"]:
    st.markdown('<div class="giant-title">🔒 801 導師班務管理系統</div>', unsafe_allow_html=True)
    with st.form("login_form"):
        u, p = st.text_input("教師帳號："), st.text_input("登入密碼：", type="password")
        if st.form_submit_button("確認登入"):
            if u == "Tseng" and p == "12345":
                st.session_state["contact_logged_in"] = True
                st.rerun()
            else: st.error("❌ 帳號或密碼錯誤。")
    st.stop()

# ----------------- 系統主畫面 (登入後) -----------------
st.markdown('<div class="giant-title">📝 801聯絡簿管理系統</div>', unsafe_allow_html=True)

st.sidebar.header("📅 日期與管理")
current_date = st.sidebar.date_input("選擇登記/查看日期：", datetime.now())
date_str = current_date.strftime("%Y-%m-%d")

if st.sidebar.button("🔒 安全登出"):
    st.session_state["contact_logged_in"] = False
    st.rerun()

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

df = load_data(date_str)

def save_data(updated_df, target_date):
    with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a", if_sheet_exists="replace") as w: updated_df.to_excel(w, sheet_name=target_date, index=False)

# ⚙️ 左側邊欄：新增收發項目
st.sidebar.markdown("---")
new_item = st.sidebar.text_input("➕ 新增學校催收項目：", placeholder="例如：疫苗施打同意書")
if st.sidebar.button("建立催收欄位"):
    if new_item and new_item not in df.columns:
        df[new_item] = "未繳 ❌"
        save_data(df, date_str)
        st.rerun()

# 📢 催繳廣播台整合至左側邊欄
st.sidebar.markdown("---")
st.sidebar.subheader(f"📢 {date_str} 即時催繳廣播台")

df_ns = df[df["聯絡簿簽名"] == "未簽 ❌"]
if not df_ns.empty:
    t_s = f"【801班 {date_str} 聯絡簿未簽名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_ns.iterrows()])
    st.sidebar.text_area("📋 複製傳至家長群組：", value=t_s, height=110, key="c_s")
else: st.sidebar.success("🎉 聯絡簿全班皆已簽名！")

df_nd = df[df["生活札記"] == "未寫 ❌"]
if not df_nd.empty:
    t_d = f"【801班 {date_str} 札記未完成名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_nd.iterrows()])
    st.sidebar.text_area("📋 複製傳至班級群組：", value=t_d, height=110, key="c_d")

extra_items = list(df.columns[5:])
if extra_items:
    for item in extra_items:
        df_ni = df[df[item] == "未繳 ❌"]
        if not df_ni.empty:
            t_i = f"【801班 {item} 尚未繳交名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_ni.iterrows()])
            st.sidebar.text_area(f"📋 複製 {item} 催繳：", value=t_i, height=110, key=f"c_{item}")
        else: st.sidebar.success(f"💯 {item} 皆已繳齊！")

# 🎴 主畫面：四欄網格登記區
st.subheader(f"📅 日期：{date_str} 紀錄登記區")
st.write("")

# 四個一組進行迴圈排列
for i in range(0, len(df), 4):
    grid = st.columns(4)
    
    for idx_grid in range(4):
        student_idx = i + idx_grid
        if student_idx < len(df):
            row_s = df.iloc[student_idx]
            seat_num = int(row_s["座號"])
            name_s = row_s["姓名"]
            
            # 👧 判斷男女生，決定套用哪一種卡片框的 CSS 類別
            if seat_num <= 15:
                gender_icon, box_class = "👧", "girl-box"
            else:
                gender_icon, box_class = "👦", "boy-box"
            
            # 💡 把整個 st.container 塞進男女生各自的專屬 CSS 包裝中
            with grid[idx_grid].html_container(box_class):
                with st.container(border=True):
                    st.markdown(f'<div class="student-title">{gender_icon} {seat_num}號 {name_s}</div>', unsafe_allow_html=True)
                    
                    # 聯絡簿與札記
                    ns = st.radio(f"聯絡簿_{seat_num}", ["已簽 📝", "未簽 ❌"], index=["已簽 📝", "未簽 ❌"].index(row_s["聯絡簿簽名"]) if row_s["聯絡簿簽名"] in ["已簽 📝", "未簽 ❌"] else 0, horizontal=True, key=f"s_{seat_num}_{date_str}")
                    nd = st.radio(f"札記_{seat_num}", ["已寫 🗒️", "未寫 ❌"], index=["已寫 🗒️", "未寫 ❌"].index(row_s["生活札記"]) if row_s["生活札記"] in ["已寫 🗒️", "未寫 ❌"] else 0, horizontal=True, key=f"d_{seat_num}_{date_str}")
                    
                    if ns != row_s["聯絡簿簽名"] or nd != row_s["生活札記"]:
                        df.loc[df["座號"] == seat_num, "聯絡簿簽名"], df.loc[df["座號"] == seat_num, "生活札記"] = ns, nd
                        save_data(df, date_str); st.rerun()
                    
                    # 自訂學校收發項目
                    if extra_items:
                        for item in extra_items:
                            st.markdown(f'<div class="item-label">📋 學校收發：{item}</div>', unsafe_allow_html=True)
                            ni = st.radio(f"{item}_{seat_num}", ["已繳 ✅", "未繳 ❌"], index=["已繳 ✅", "未繳 ❌"].index(row_s[item]) if row_s[item] in ["已繳 ✅", "未繳 ❌"] else 1, horizontal=True, key=f"i_{item}_{seat_num}_{date_str}", label_visibility="collapsed")
                            if ni != row_s[item]: df.loc[df["box_2d'] if 'box_2d' in df else df['座號']"] == seat_num, item] = ni; save_data(df, date_str); st.rerun()
                    
                    # 隨手備註欄
                    nm = st.text_input(f"備註_{seat_num}", value="" if pd.isna(row_s["備註事項"]) else str(row_s["備註事項"]), placeholder="✍️ 隨手備註...", label_visibility="collapsed", key=f"m_{seat_num}_{date_str}")
                    if nm != ("" if pd.isna(row_s["備註事項"]) else str(row_s["備註事項"])): df.loc[df["座號"] == seat_num, "備註事項"] = nm; save_data(df, date_str)

st.markdown("---")
st.subheader(f"📊 801班 {date_str} 綜合班務總表（唯讀檢視）")
st.dataframe(df, use_container_width=True)
