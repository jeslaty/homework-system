import os
import pandas as pd
import streamlit as st
from datetime import datetime

# 設定網頁標題與圖示
st.set_page_config(page_title="801聯絡簿管理系統", page_icon="📝", layout="wide")

# 🎨 注入【Apple 旗艦暗黑模式：極黑大背景、純白高對比懸浮卡片】頂級設計
st.markdown(
    """
    <style>
    /* 🍏 全局強制使用 Apple 經典無襯線字體，乾淨、高雅、絕不死板 */
    *, .stApp, p, span, label, div, h1, h2, h3, input, button, textarea {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "Microsoft JhengHei", sans-serif !important;
    }
    
    /* 🍏 1. 全局大背景：曜石極黑色，強迫純白卡片如發光般跳出來 */
    .stApp { background-color: #090D16 !important; }
    
    /* 🍏 2. 左側邊欄：深太空灰（保持乾淨俐落） */
    [data-testid="stSidebar"] { background-color: #111827 !important; }
    
    /* 🍏 3. 徹底阻斷側邊欄頂部可能導致爆字的按鈕圖示 */
    button[data-testid="collapsedControl"], [data-testid="stSidebarCollapse"] { 
        display: none !important; 
        visibility: hidden !important; 
    }
    
    /* 🍏 標題：純白發光加大字體，在黑底上極度氣派 */
    .apple-title { 
        color: #FFFFFF !important; 
        font-size: 38px !important; 
        font-weight: 900 !important; 
        margin-bottom: 20px !important; 
        border-bottom: 2px solid #1E293B;
        padding-bottom: 12px;
    }
    
    /* 👤 學生姓名：純黑、超大粗體 */
    .student-title {
        color: #000000 !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        margin-bottom: 12px !important;
    }
    
    /* 📋 學校項目與備註標籤：耀眼鮮藍 */
    .item-label { 
        color: #0256CF !important; 
        font-size: 16px !important; 
        font-weight: 800 !important; 
        margin-top: 12px !important; 
    }

    /* 📋 內文與按鈕文字 */
    .stText, p, span, label { color: #000000 !important; font-weight: 700 !important; font-size: 15px !important; }
    
    /* 📦【3D 浮雕發光卡片框】利用極黑背景，搭配 3px 藍粗框與強大白底，立體感達到最頂峰！ */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 3px solid #0056FF !important;   /* 3px 蘋果標誌性極光亮藍粗框 */
        border-radius: 16px !important;         /* 圓角 */
        background-color: #FFFFFF !important;    /* 卡片內部維持 100% 純白，與背景形成終極黑白強烈對比 */
        padding: 20px !important; 
        margin: 16px !important;                 /* 強制拆開格子間距 */
        
        /* 注入超強立體發光陰影，讓純白卡片在極黑夜空中「浮出螢幕」 */
        box-shadow: 0 15px 30px rgba(0, 86, 255, 0.25) !important;
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
st.markdown('<div class="apple-title">📝 801聯絡簿管理系統</div>', unsafe_allow_html=True)

# 📅 1. 側邊欄大優化：只留下最純淨的日期與管理，視覺不暗沉、不擁擠
st.sidebar.markdown("<h2 style='color:#FFFFFF;'>📅 日期與管理</h2>", unsafe_allow_html=True)
current_date = st.sidebar.date_input("選擇登記/查看日期：", datetime.now(), key="sb_date")
date_str = current_date.strftime("%Y-%m-%d")

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color:#FFFFFF;'>➕ 學校項目</h3>", unsafe_allow_html=True)
new_item = st.sidebar.text_input("輸入催收項目名稱：", placeholder="例如：疫苗施打同意書", key="sb_item")

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
    except Exception:
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a", if_sheet_exists="replace") as w: df_def.to_excel(w, sheet_name=target_date, index=False)
        return df_def

df = load_data(date_str)

def save_data(updated_df, target_date):
    with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a", if_sheet_exists="replace") as w: updated_df.to_excel(w, sheet_name=target_date, index=False)

if st.sidebar.button("建立催收欄位"):
    if new_item and new_item not in df.columns:
        df[new_item] = "未繳 ❌"
        save_data(df, date_str)
        st.rerun()

if st.sidebar.button("🔒 安全登出"):
    st.session_state["contact_logged_in"] = False
    st.rerun()

# 2. 🎴 主畫面大版面配置：左邊放學生登記區（75%），右邊放催繳廣播台（25%）
col_register_zone, col_broadcast_zone = st.columns([3, 1])

with col_register_zone:
    st.markdown(f"<h3 style='color:#FFFFFF;'>📅 日期：{date_str} 紀錄登記區</h3>", unsafe_allow_html=True)
    st.write("")

    extra_items = list(df.columns[5:])

    # 四個一組進行一橫排排列
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

                    st.markdown('<div class="item-label">✍️ 隨手備註：</div>', unsafe_allow_html=True)
                    nm = st.text_input(
                        f"備註_{seat_num}",
                        value="" if pd.isna(row_s["備註事項"]) else str(row_s["備註事項"]),
                        placeholder="輸入日常備註...", label_visibility="collapsed", key=f"m_{seat_num}_{date_str}"
                    )
                    if nm != ("" if pd.isna(row_s["備註事項"]) else str(row_s["備註事項"])):
                        df.loc[df["座號"] == seat_num, "備註事項"] = nm
                        save_data(df, date_str)

with col_broadcast_zone:
    st.markdown(f"<h3 style='color:#FFFFFF;'>📢 即時催繳廣播台</h3>", unsafe_allow_html=True)
    st.write("")

    # A. 聯絡簿
    df_ns = df[df["聯絡簿簽名"] == "未簽 ❌"]
    if not df_ns.empty:
        t_s = f"【801班 {date_str} 聯絡簿未簽名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_ns.iterrows()])
        st.text_area("📋 複製傳至家長群組：", value=t_s, height=130, key="c_s")
    else:
        st.success("🎉 聯絡簿全班皆已簽名！")

    # B. 札記
    df_nd = df[df["生活札記"] == "未寫 ❌"]
    if not df_nd.empty:
        t_d = f"•【801班 {date_str} 札記未完成名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_nd.iterrows()])
        st.text_area("📋 複製傳至班級群組：", value=t_d, height=130, key="c_d")

    # C. 學校項目
    if extra_items:
        st.markdown("<hr style='border:1px solid #1E293B;'>", unsafe_allow_html=True)
        for item in extra_items:
            df_ni = df[df[item] == "未繳 ❌"]
            if not df_ni.empty:
                t_i = f"【801班 {item} 尚未繳交名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_ni.iterrows()])
                st.text_area(f"📋 {item} 催繳：", value=t_i, height=130, key=f"c_{item}")
            else:
                st.success(f"💯 {item} 皆已繳齊！")

st.markdown("<hr style='border:1px solid #1E293B;'>", unsafe_allow_html=True)
st.markdown(f"<h3 style='color:#FFFFFF;'>📊 801班 {date_str} 綜合班務總表（唯讀檢視）</h3>", unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)
