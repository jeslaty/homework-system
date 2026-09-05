import os
import pandas as pd
import streamlit as st
from datetime import datetime

# 1. 設定網頁標題與寬版佈局
st.set_page_config(page_title="801聯絡簿管理系統", page_icon="📝", layout="wide")

# 🎨 注入【Apple 經典深色暗黑美學 UI - 徹底拔除密碼框怪字、滑鼠懸停 3D 浮起與發光特效版】
st.markdown("""
    <style>
    /* 🍏 全局強制使用現代無襯線字體 */
    *, .stApp, p, span, label, div, h1, h2, h3, input, button, textarea {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", sans-serif !important;
    }
    
    /* 🛑【徹底封鎖原廠側邊欄】全站不使用 sidebar，怪字發源地直接消失 */
    [data-testid="stSidebar"], button[data-testid="collapsedControl"], [data-testid="stSidebarCollapse"] { 
        display: none !important; visibility: hidden !important; 
    }
    
    /* 🎯【終極大必殺：徹底封印並隱藏原廠密碼框右側的 Visibility 按鈕，讓 visibili 殘留字當場徹底蒸發！】 */
    button[data-testid="stTextInputPasswordVisibility"], 
    [data-testid="stTextInputPasswordVisibility"] {
        display: none !important;
        visibility: hidden !important;
        width: 0px !important;
    }
    
    /* 📦 針對右側學生的獨立卡片容器（st.container border=True）進行動畫柔和微調 */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important; /* 讓浮起和降落的動畫極度流暢 */
    }
    
    /* 🚀【滑鼠懸停 3D 特效：滑鼠移到學生格子上時（Hover），向上懸浮 6px 並加上精緻亮藍色發光陰影】 */
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-6px) !important; /* 向上懸浮 6px */
        box-shadow: 0 14px 28px rgba(56,189,248,0.25), 0 10px 10px rgba(56,189,248,0.22) !important; /* 亮藍色科技感發光陰影 */
        border: 2.5px solid #38BDF8 !important; /* 外框線同步亮化為亮藍色 */
    }
    </style>
""", unsafe_allow_html=True)

# 🔑 帳號密碼登入機制
if "contact_logged_in" not in st.session_state:
    st.session_state["contact_logged_in"] = False

if not st.session_state["contact_logged_in"]:
    st.markdown("### 🔒 801 導師班務管理系統")
    with st.form("login_form"):
        # 🎯 改用 100% 必定成功顯色的純白字體指令，直接繞過原廠標籤發黑的系統限制
        st.markdown("**🔑 教師帳號：**")
        u = st.text_input("u_input", label_visibility="collapsed")
        
        st.markdown("**🔒 登入密碼：**")
        p = st.text_input("p_input", type="password", label_visibility="collapsed")
        
        if st.form_submit_button("確認登入"):
            if u.strip() == "teacher" and p.strip() == "12345":
                st.session_state["contact_logged_in"] = True
                st.rerun()
            else:
                st.error("❌ 帳號或密碼錯誤。")
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
    st.write(f"### 📢 {date_str} 即時催繳廣播台")
    
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
                    html_badge = f'<div style="background-color:#FFF1F2;border:2.5px solid #E11D48;border-radius:10px;padding:8px;text-align:center;"><span style="color:#991B1B;font-size:20px;font-weight:900;white-space:nowrap;">{gender_icon} {seat_num}號 {name_s}</span></div>'
                else:
                    html_badge = f'<div style="background-color:#F0F7FF;border:2.5px solid #2563EB;border-radius:10px;padding:8px;text-align:center;"><span style="color:#1E40AF;font-size:20px;font-weight:900;white-space:nowrap;">{gender_icon} {seat_num}號 {name_s}</span></div>'

                with grid[idx_grid].container(border=True):
                    st.markdown(html_badge, unsafe_allow_html=True)
                    st.write("")
                    
                    ns = st.radio(f"聯絡簿_{seat_num}", ["已簽 📝", "未簽 ❌"], index=(0 if row_s["聯絡簿簽名"] == "已簽 📝" else 1), horizontal=True, key=f"s_{seat_num}_{date_str}")
                    nd = st.radio(f"札記_{seat_num}", ["已寫 🗒️", "未寫 ❌"], index=(0 if row_s["生活札記"] == "已寫 🗒️" else 1), horizontal=True, key=f"d_{seat_num}_{date_str}")
                    
                    if ns != row_s["聯絡簿簽名"] or nd != row_s["生活札記"]:
                        df.loc[df["座號"] == seat_num, "聯絡簿簽名"], df.loc[df["座號"] == seat_num, "生活札記"] = ns, nd
                        save_data(df, date_str); st.rerun()
                    
                    if extra_items:
                        for item in extra_items:
                            st.write(f"📋 **學校收發：{item}**")
                            ni = st.radio(f"{item}_{seat_num}", ["已繳 ✅", "未繳 ❌"], index=(0 if row_s[item] == "已繳 ✅" else 1), horizontal=True, key=f"i_{item}_{seat_num}_{date_str}", label_visibility="collapsed")
                            if ni != row_s[item]:
                                df.loc[df["座號"] == seat_num, item] = ni
                                save_data(df, date_str); st.rerun()
                    
                    st.write("✍️ **隨手備註：**")
                    current_memo = "" if pd.isna(row_s["備註事項"]) else str(row_s["備註事項"])
                    nm = st.text_input(f"備註_{seat_num}", value=current_memo, placeholder="輸入日常備註...", label_visibility="collapsed", key=f"m_{seat_num}_{date_str}")
                    if nm != current_memo:
                        df.loc[df["座號"] == seat_num, "備註事項"] = nm
                        save_data(df, date_str)

st.markdown("---")
st.write("### 📊 綜合班務總表（唯讀檢視）")
st.dataframe(df, use_container_width=True)
