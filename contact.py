import os, pandas as pd, streamlit as st
from datetime import datetime

st.set_page_config(page_title="801聯絡簿管理系統", page_icon="📝", layout="wide")

# 🎨 注入【3D立體懸浮・極簡黑白高對比】外加【滑鼠懸停變色凸顯特效】
st.markdown("""
    <style>
    /* 全局背景：頂級冷霧灰 */
    .stApp { background-color: #F8FAFC !important; }
    /* 左側邊欄：沉穩石墨灰 */
    [data-testid="stSidebar"] { background-color: #E2E8F0 !important; }
    
    /* 🖤 標題層級：曜石黑、極高魄力主標題 */
    .giant-title { color: #0F172A !important; font-size: 42px !important; font-weight: 900 !important; font-family: "Noto Sans TC", sans-serif; margin-bottom: 20px !important; }
    h2 { color: #1E293B !important; font-size: 24px !important; font-weight: 800 !important; }
    h3 { color: #334155 !important; font-size: 20px !important; font-weight: 800 !important; }
    
    /* 👤 學生姓名專用樣式 */
    .student-name { color: #000000 !important; font-size: 22px !important; font-weight: 900 !important; margin-bottom: 6px !important; }
    
    /* 📋 學校項目與備註樣式 */
    .item-label { color: #0F172A !important; font-size: 16px !important; font-weight: 800 !important; }
    
    /* 📋 選項純黑高對比字體 */
    .stText, p, span, label { color: #000000 !important; font-weight: 800 !important; font-size: 15px !important; }
    
    /* 🖤 【3D立體懸浮卡片框】預設為高質感白底黑框，並加入平滑動畫過渡效果 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 3px solid #0F172A !important; 
        border-radius: 14px !important;       
        background-color: #FFFFFF !important;  
        padding: 16px !important; margin-bottom: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.1), 0 2px 4px -1px rgba(15, 23, 42, 0.06) !important;
        /* 💡 讓顏色與陰影的變化像動畫一樣平滑（動態質感關鍵） */
        transition: all 0.25s ease-in-out !important; 
    }
    
    /* ✨✨【滑鼠移過去 / 手指觸碰時的強烈凸顯特效】✨✨ */
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border: 3px solid #0D47A1 !important;        /* 邊框一秒變皇家深藍 */
        background-color: #E0F2FE !important;       /* 卡片底色變深，換成高質感亮淺藍 */
        transform: translateY(-4px) scale(1.01) !important; /* 讓格子微微往上彈起、放大，呈現 3D 浮出感 */
        /* 加深加厚下方的影子，讓立體感強烈爆發 */
        box-shadow: 0 20px 25px -5px rgba(13, 71, 161, 0.2), 0 10px 10px -5px rgba(13, 71, 161, 0.2) !important;
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
# 1. 巨大主標題呈現
st.markdown('<div class="giant-title">📝 801聯絡簿管理系統</div>', unsafe_allow_html=True)

# 2. 📅 日期與登出功能放邊欄最上方
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

# 3. ⚙️ 左側邊欄：新增收發項目
st.sidebar.markdown("---")
new_item = st.sidebar.text_input("➕ 新增學校催收項目：", placeholder="例如：疫苗施打同意書")
if st.sidebar.button("建立催收欄位"):
    if new_item and new_item not in df.columns:
        df[new_item] = "未繳 ❌"
        save_data(df, date_str)
        st.rerun()

# 4. 📢 【催繳廣播台整合至左側邊欄】
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

# 5. 🎴 主畫面：一橫排 4 個學生的格子排版 (超省空間設計)
st.subheader(f"📅 日期：{date_str} 紀錄登記區")
st.write("")

# 四個一組進行迴圈排列
for i in range(0, len(df), 4):
    grid = st.columns(4) # 一排切成 4 個格子
    
    for idx_grid in range(4):
        student_idx = i + idx_grid
        if student_idx < len(df):
            row_s = df.iloc[student_idx]
            seat_num = int(row_s["座號"])
            name_s = row_s["姓名"]
            
            # 👧 判斷男女生圖案 (1~15是女生，16~28是男生)
            gender_icon = "👧" if seat_num <= 15 else "👦"
            
            with grid[idx_grid].container(border=True):
                st.markdown(f'<div class="student-name">{gender_icon} {seat_num}號 {name_s}</div>', unsafe_allow_html=True)
                
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
                        if ni != row_s[item]: df.loc[df["座號"] == seat_num, item] = ni; save_data(df, date_str); st.rerun()
                
                # 隨手備註欄
                nm = st.text_input(f"備註_{seat_num}", value="" if pd.isna(row_s["備註事項"]) else str(row_s["備註事項"]), placeholder="✍️ 隨手備註...", label_visibility="collapsed", key=f"m_{seat_num}_{date_str}")
                if nm != ("" if pd.isna(row_s["備註事項"]) else str(row_s["備註事項"])): df.loc[df["座號"] == seat_num, "備註事項"] = nm; save_data(df, date_str)

st.markdown("---")
st.subheader(f"📊 801班 {date_str} 綜合班務總表（唯讀檢視）")
st.dataframe(df, use_container_width=True)
