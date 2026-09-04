import os
import pandas as pd
import streamlit as st
from datetime import datetime

# 設定網頁標題與圖示
st.set_page_config(page_title="801聯絡簿管理系統", page_icon="📝", layout="wide")

# 🎨 注入全站字體高對比優化（只留下 100% 穩定的 CSS，其餘交給官方原生彩色元件）
st.markdown(
    """
    <style>
    /* 🍏 全局強制使用現代、不嚴肅的微軟正黑體與蘋方字體 */
    *, .stApp, p, span, label, div, h1, h2, h3, input, button, textarea {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", "微軟正黑體", sans-serif !important;
    }
    
    /* 🍏 網頁大背景改為純淨發亮白，徹底消滅暗沉 */
    .stApp { background-color: #FFFFFF !important; }
    
    /* 🛑【最關鍵：彻底封鎖與拔除側邊欄】全站不使用 sidebar，怪字發源地直接消失，永遠不會再跑出來！ */
    [data-testid="stSidebar"], button[data-testid="collapsedControl"], [data-testid="stSidebarCollapse"] { 
        display: none !important; 
        visibility: hidden !important; 
    }
    
    /* 🍏 標題精簡高級化：太空灰高級感，字體適中絕不爆字 */
    .apple-title { 
        color: #0F172A !important; 
        font-size: 32px !important; 
        font-weight: 800 !important; 
        margin-bottom: 20px !important; 
        border-bottom: 3px solid #E2E8F0;
        padding-bottom: 10px;
    }
    
    /* 📋 學校項目與備註標籤 */
    .item-label { 
        color: #1E3A8A !important; 
        font-size: 15px !important; 
        font-weight: 800 !important; 
        margin-top: 10px !important; 
        margin-bottom: 4px !important;
    }

    /* 📋 全局文字與選項：特粗、純黑高清晰 */
    .stText, p, span, label, div { color: #000000 !important; font-weight: 800 !important; font-size: 15px !important; }
    
    /* 📦【3D 原生獨立卡片框設定】拉開格子間距，讓 4 欄排版極度整齊、凸顯 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 2px solid #0F172A !important;   /* 曜石黑清晰實線邊框 */
        border-radius: 16px !important;         /* 大圓角 */
        background-color: #FFFFFF !important;    /* 卡片內部維持乾淨高亮白 */
        padding: 16px !important; 
        margin: 10px !important;                 /* 強制拉開卡片間距 */
        box-shadow: 0 4px 6px rgba(0,0,0,0.03) !important;
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
st.markdown('<div class="apple-title">📝 801聯絡簿系統</div>', unsafe_allow_html=True)

# 基礎數據加載設定
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

# 🏛️ 【自訂黃金排版：左欄放管理與廣播，右邊放大畫面一排 4 人登記區】
col_left_panel, col_right_students = st.columns([1, 3]) # 精準分配 1:3 比例

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
            save_data(df, date_str)
            st.rerun()
            
    if st.button("🔒 安全登出系統", use_container_width=True):
        st.session_state["contact_logged_in"] = False
        st.rerun()

    st.markdown("---")
    st.write(f"### 📢 {date_str} 即時催繳廣播台")
    
    # A. 聯絡簿
    df_ns = df[df["聯絡簿簽名"] == "未簽 ❌"]
    if not df_ns.empty:
        t_s = f"【801班 {date_str} 聯絡簿未簽名單】\n" + "".join([f"{int(r['座號'])}號 {r['姓名']}\n" for _, r in df_ns.iterrows()])
        st.text_area("📋 複製傳至家長群組：", value=t_s, height=130, key="c_s")
    else: st.success("🎉 本日聯絡簿全班皆已簽名！")

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
                st.text_area(f"📋 複製 {item} 催繳：", value=t_i, height=130, key=f"c_{item}")
            else: st.success(f"💯 {item} 皆已繳齊！")

with col_right_students:
    st.write(f"### 📅 日期：{date_str} 紀錄登記區")
    st.write("")

    # 四個一組進行迴圈排列 (一橫排 4 個學生卡片)
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
                    
                    # 💡【必成功原生美化招】利用 100% 無法被系統封鎖的官方原色彩色狀態字卡，強制注入層次感！
                    if seat_num <= 15:
                        # 女生：使用 warning 框（強迫秀出極度醒目、高對比的馬卡龍愛馬仕橘金色卡片名牌）
                        with st.status(f"{gender_icon} {seat_num}號 {name_s}", expanded=False, state="warning"):
                            st.write("801班 女生成員")
                    else:
                        # 男生：使用 info 框（強迫秀出極度醒目、清透好看的馬卡龍極光亮藍色卡片名牌）
                        with st.status(f"{gender_icon} {seat_num}號 {name_s}", expanded=False, state="info"):
                            st.write("801班 男生成員")

                    # 聯絡簿與札記單選鈕（文字特粗純黑，姓名保證大而醒目且絕對不會被切斷換行）
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

                    # 自訂項目
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
                    st.markdown('<div class="item-label">✍ *隨手備註：*</div>', unsafe_allow_html=True)
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
st.dataframe(df, use_container_width=True)
