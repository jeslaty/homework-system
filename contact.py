import os, pandas as pd, streamlit as st
from datetime import datetime

st.set_page_config(page_title="801聯絡簿管理系統", page_icon="📝", layout="wide")

# 🎨 注入【官方新版容器特徵碼】控制，實現 100% 成功的整格高對比懸浮變色
st.markdown("""
    <style>
    /* 全局背景：極致冷霧灰 */
    .stApp { background-color: #F8FAFC !important; }
    /* 左側邊欄：內斂石墨灰 */
    [data-testid="stSidebar"] { background-color: #E2E8F0 !important; }
    
    /* 🌊 巨大化主標題 */
    .giant-title { color: #0F172A !important; font-size: 42px !important; font-weight: 900 !important; font-family: "Noto Sans TC", sans-serif; margin-bottom: 25px !important; }
    
    /* 👤 學生姓名純黑加大字體 */
    .student-title { color: #000000 !important; font-size: 22px !important; font-weight: 900 !important; margin-bottom: 8px !important; }
    /* 📋 學校項目與備註字體 */
    .item-label { color: #0F172A !important; font-size: 15px !important; font-weight: 800 !important; margin-top: 10px !important; }
    .stText, p, span, label { color: #000000 !important; font-weight: 700 !important; font-size: 14px !important; }

    /* ========================================================
       💡 透過全新官方原生卡片邊框特徵 (st.container border=True) 
       強制把整格（含按鈕備註）鎖在一起，做出最高質感的變色懸浮特效
       ======================================================== */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 2px solid #1E293B !important; /* 預設高清晰深色實線框 */
        border-radius: 16px !important;       /* 圓角 */
        background-color: #FFFFFF !important;  /* 預設高對比純白底色 */
        padding: 16px !important; 
        margin-bottom: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.25s ease-in-out !important; /* 讓懸浮動態非常流暢 */
    }
    
    /* ✨✨ 當滑鼠移入、或是手指觸碰時，整格大框框【一秒變深、3D浮起、外框加粗變色】✨✨ */
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        background-color: #BAE6FD !important;        /* 100% 成功變深為：莫蘭迪湖水藍 */
        border: 3px solid #0284C7 !important;         /* 外框加粗，變色為清爽亮藍 */
        transform: translateY(-6px) scale(1.02) !important; /* 卡片向上彈起並微放大，立體感爆發 */
        box-shadow: 0 20px 25px -5px rgba(2, 132, 199, 0.2) !important; /* 藍色系質感陰影 */
    }
    </style>
""", unsafe_allow_html=True)

# 🔑 帳號密碼設定
if "contact_logged_in" not in st.session_state:
    st.session_state["contact_logged_in"] = False

if not st.session_state["contact_logged_in"]:
    st.markdown('<div class="giant-title">🔒 801 導師班務管理系統</div>', unsafe_allow_html=True)
    with st.form("login_form"):
        u = st.text_input("教師帳號：")
        p = st.text_input("登入密碼：", type="password")
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
st.write(f"### 📅 日期：{date_str} 紀錄登記區")
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
            
            # 🌸 換上老師指定的日系植物符號 (1~15是櫻花，16~28是幸運草)
            gender_icon = "🌸" if seat_num <= 15 else "🍀"
            
            # 💡 改用新版原生邊框容器，這與最新的雲端機制完全相容，絕對能完美呈現懸浮特效
            with grid[idx_grid].container(border=True):
                st.markdown(f'<div class="student-title">{gender_icon} {seat_num}號 {name_s}</div>', unsafe_allow_html=True)
                
                # 聯絡簿與札記單選鈕
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
                        if ni != row_s[item]: 
                            df.loc[df["座號"] == seat_num, item] = ni
                            save_data(df, date_str); st.rerun()
                
                # 隨手備註欄
                nm = st.text_input(f"備註_{seat_num}", value="" if pd.isna(row_s["備註事項"]) else str(row_s["備註事項"]), placeholder="✍️ 隨手備註...", label_visibility="collapsed", key=f"m_{seat_num}_{date_str}")
                if nm != ("" if pd.isna(row_s["備註事項"]) else str(row_s["備註事項"])): 
                    df.loc[df["座號"] == seat_num, "備註事項"] = nm
                    save_data(df, date_str)

st.markdown("---")
st.write(f"### 📊 801班 {date_str} 綜合班務總表（唯讀檢視）")
st.dataframe(df, use_container_width=True)
