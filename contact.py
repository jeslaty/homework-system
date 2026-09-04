import os
import pandas as pd
import streamlit as st
from datetime import datetime

# 設定網頁標題與圖示
st.set_page_config(page_title="801聯絡簿管理系統", page_icon="📝", layout="wide")

# 🎨 注入【Apple 官網白金美學】全文字體優化
st.markdown(
    """
    <style>
    /* 🍏 全局強制使用現代、不嚴肅的微軟正黑體與蘋方字體，線條最流暢舒服 */
    *, .stApp, p, span, label, div, h1, h2, h3, input, button, textarea {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", "微軟正黑體", sans-serif !important;
    }
    
    /* 🍏 網頁大背景改為純淨發亮白，徹底消滅暗沉黑底 */
    .stApp { background-color: #FFFFFF !important; }
    
    /* 🍏 左側邊欄：內斂白灰色 */
    [data-testid="stSidebar"] { background-color: #F1F5F9 !important; }
    
    /* 🍏 徹底隱藏任何會導致爆字的官方控制按鈕 */
    button[data-testid="collapsedControl"], [data-testid="stSidebarCollapse"] { 
        display: none !important; 
        visibility: hidden !important; 
    }
    
    /* 🍏 標題精簡精緻化：字體適中（28px），展現 Apple 簡約精品感，絕不爆字 */
    .apple-title { 
        color: #0F172A !important; 
        font-size: 28px !important; 
        font-weight: 800 !important; 
        margin-bottom: 15px !important; 
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 8px;
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
# 1. 簡約俐落的全新主標題
st.markdown('<div class="apple-title">📝 801聯絡簿系統</div>', unsafe_allow_html=True)

# 2. 📅 日期與管理放左側邊欄
st.sidebar.header("📅 日期與管理")
current_date = st.sidebar.date_input("選擇登記/查看日期：", datetime.now(), key="sb_date")
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
    except Exception:
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a", if_sheet_exists="replace") as w: df_def.to_excel(w, sheet_name=target_date, index=False)
        return df_def

df = load_data(date_str)

def save_data(updated_df, target_date):
    with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a", if_sheet_exists="replace") as w: updated_df.to_excel(w, sheet_name=target_date, index=False)

st.sidebar.markdown("---")
new_item = st.sidebar.text_input("➕ 新增學校催收項目：", placeholder="例如：疫苗施打同意書", key="sb_item")
if st.sidebar.button("建立催收欄位"):
    if new_item and new_item not in df.columns:
        df[new_item] = "未繳 ❌"
        save_data(df, date_str)
        st.rerun()

# 3. ⚖️ 左右主排版配置：左邊放紀錄登記區（75%），右邊放廣播台（25%）
col_register_zone, col_broadcast_zone = st.columns([3, 1])

with col_register_zone:
    st.write(f"### 📅 日期：{date_str} 紀錄登記區")
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

                # 💡【大滿貫絕招】改用 100% 絕對成功變色、對比度最強的原生深色框（st.info）
                with grid[idx_grid].info(f"{gender_icon} {seat_num}號 {name_s}"):
                    
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

                    if extra_items:
                        for item in extra_items:
                            st.write(f"📋 **學校收發：{item}**")
                            ni = st.radio(
                                f"{item}_{seat_num}", ["已繳 ✅", "未繳 ❌"],
                                index=(["已繳 ✅", "未繳 ❌"].index(row_s[item]) if row_s[item] in ["已繳 ✅", "未繳 ❌"] else 1),
                                horizontal=True, key=f"i_{item}_{seat_num}_{date_str}", label_visibility="collapsed"
                            )
                            if ni != row_s[item]:
                                df.loc[df["座號"] == seat_num, item] = ni
                                save_data(df, date_str)
                                st.rerun()

                    st.write("✍️ **隨手備註：**")
                    nm = st.text_input(
                        f"備註_{seat_num}",
                        value="" if pd.isna(row_s["備註事項"]) else str(row_s["備註事項"]),
                        placeholder="輸入日常備註...", label_visibility="collapsed", key=f"m_{seat_num}_{date_str}"
                    )
                    if nm != ("" if pd.isna(row_s["備註事項"]) else str(row_s["備註事項"])):
                        df.loc[df["座號"] == seat_num, "備註事項"] = nm
                        save_data(df, date_str)

with col_broadcast_zone:
    st.write(f"### 📢 即時催繳廣播台")
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
        t_d = f"【801班 {date_str} 札記未完成名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_nd.iterrows()])
        st.text_area("📋 複製傳至班級群組：", value=t_d, height=130, key="c_d")

    # C. 學校項目
    if extra_items:
        st.markdown("---")
        for item in extra_items:
            df_ni = df[df[item] == "未繳 ❌"]
            if not df_ni.empty:
                t_i = f"【801班 {item} 尚未繳交名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_ni.iterrows()])
                st.text_area(f"📋 {item} 催繳：", value=t_i, height=130, key=f"c_{item}")
            else:
                st.success(f"💯 {item} 皆已繳齊！")

st.markdown("---")
st.write(f"### 📊 801班 {date_str} 綜合班務總表（唯讀檢視）")
st.dataframe(df, use_container_width=True)
