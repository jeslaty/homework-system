import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="02_作業登記專區", page_icon="📚", layout="wide")

# CSS 視覺優化
st.markdown("""
    <style>
    [data-testid="stSidebar"], button[data-testid="collapsedControl"], header[data-testid="stHeader"] {
        display: none !important;
    }
    .title-banner {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: white; padding: 16px 20px; border-radius: 12px; margin-bottom: 20px;
    }
    .title-banner h1 { color: #FFFFFF !important; font-size: 1.6rem !important; margin: 0 !important; }
    .control-card { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; margin-bottom: 12px; }
    </style>
""", unsafe_allow_html=True)

# 密碼驗證
if "page_hw_auth" not in st.session_state:
    st.session_state["page_hw_auth"] = False

if not st.session_state["page_hw_auth"]:
    st.write("### 🔒 教師安全驗證專區")
    with st.form("hw_auth_form"):
        p = st.text_input("請輸入 5 位數導師密碼：")
        if st.form_submit_button("確認通行"):
            if p.strip() == "12345":
                st.session_state["page_hw_auth"] = True
                st.rerun()
            else: st.error("❌ 密碼錯誤。")
    if st.button("⬅️ 返回管理主控台", use_container_width=True):
        st.switch_page("main.py")
    st.stop()

# 頁頭
col_top_title, col_top_back = st.columns([0.80, 0.20])
with col_top_title:
    st.markdown('<div class="title-banner"><h1>📚 全校各科作業登記系統</h1></div>', unsafe_allow_html=True)
with col_top_back: 
    if st.button("🏛️ 返回管理主控台", use_container_width=True):
        st.switch_page("main.py")

# 名單資料
CLASSES_DATA = {
    "801班": [(1, '王喬昕'), (2, '吳岢曈'), (3, '李巧彤'), (4, '岳昀軒'), (5, '林晏以'), (6, '林晨琳'), (7, '林芮妘'), (8, '林苡嫻'), (9, '黃榆涵'), (10, '黃榆涵'), (11, '蔡可琳'), (12, '戴彤竹'), (13, '羅羽翎'), (14, '羅昕彤'), (15, '林禹彤'), (16, '王楷文'), (17, '王駿展'), (18, '吳軒佑'), (19, '李宇哲'), (20, '林柏辰'), (21, '張品御'), (22, '陳正澤'), (23, '陳秉玄'), (24, '陳鼎硯'), (25, '黃楙軒'), (26, '董子以'), (27, '劉家佑'), (28, '魏辰恩')],
    "903班": [(1, '張莘妍'), (2, '梁芯瑜'), (3, '吳佳錹'), (4, '許秧秧'), (5, '陳又綺'), (6, '高筱媗'), (7, '莊子玉'), (8, '吳愷昕'), (9, '陳以恩'), (10, '蕭妤柔'), (11, '吳璥齡'), (12, '魏品儀'), (15, '邱子恆'), (16, '張本維'), (17, '謝易宸'), (18, '游子宥'), (19, '吳宇曜'), (20, '吳嘉恩'), (21, '丁沛紳'), (22, '林子佑'), (23, '陳冠成'), (24, '徐國睿'), (25, '余冠憲'), (26, '黃家寶'), (27, '張瑋志'), (28, '方仲祺'), (29, '林昱嘉')],
    "904班": [(1, '戴嘉妤'), (2, '陳資晴'), (3, '傅詩穎'), (4, '張瞳恩'), (5, '黃宇婕'), (6, '吳沛媛'), (7, '李妍芯'), (8, '鄭羽恩'), (9, '林子桐'), (10, '許詠晴'), (11, '吳宸彤'), (12, '林品妍'), (15, '趙右群'), (16, '林定毅'), (17, '潘子堯'), (18, '郭羿楷'), (19, '張明哲'), (20, '吳宇曜'), (21, '魏永聖'), (22, '游承恩'), (23, '胡琮浩'), (24, '李柏沅'), (25, '許育政'), (26, '宗旻恩'), (27, '吳博硯')],
    "906班": [(1, '陳亮妤'), (3, '董宜洳'), (4, '林庭瑜'), (5, '許淯淳'), (6, '陳鈺軒'), (7, '林郁庭'), (8, '陳雅竹'), (9, '陳睿瑤'), (10, '楊淇暄'), (11, '陳雨萱'), (12, '江霈穎'), (15, '陳逸恩'), (16, '劉哲皓'), (17, '陳士愷'), (18, '李開哲'), (19, '林翊凱'), (20, '林晉宇'), (21, '林釉荏'), (22, '林均昊'), (23, '賴羿軒'), (24, '鄧仲喆'), (25, '吳羽翔'), (26, '林擎宇'), (27, '林旻勳'), (28, '鄭凱軒'), (29, '李秉叡'), (31, '曾群文'), (32, '吳立丞')]
}

def get_csv_path(class_name): return f"{class_name}_作業登記表.csv"

def load_class_df(class_name):
    path = get_csv_path(class_name)
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            df['座號'] = df['座號'].astype(int)
            return df
        except: pass
    student_info = CLASSES_DATA[class_name]
    data = {"座號": [s[0] for s in student_info], "姓名": [s[1] for s in student_info]}
    if class_name != "801班": data["英文作業"] = [False] * len(student_info)
    return pd.DataFrame(data)

def save_class_df(class_name, df):
    path = get_csv_path(class_name)
    df.to_csv(path, index=False, encoding="utf-8-sig")

# 介面配置
col_control, col_table = st.columns([0.30, 0.70], gap="medium")

with col_control:
    st.markdown('<div class="control-card">', unsafe_allow_html=True)
    st.write("### 🏫 選擇班級")
    selected_class = st.selectbox("請選擇班級：", list(CLASSES_DATA.keys()), key="sel_class")
    st.markdown('</div>', unsafe_allow_html=True)
    
    df_current = load_class_df(selected_class)

    st.markdown('<div class="control-card">', unsafe_allow_html=True)
    st.write("### ➕ 新增作業欄位")
    placeholder_text = "例如：國文聯絡簿" if selected_class == "801班" else "例如：英文雜誌 L3"
    new_hw_title = st.text_input("輸入新作業名稱：", placeholder=placeholder_text, key=f"new_hw_{selected_class}")
    if st.button("✨ 建立作業欄位", use_container_width=True, type="primary"):
        if new_hw_title.strip():
            title = new_hw_title.strip()
            if title in df_current.columns:
                st.warning("⚠️ 該作業名稱已存在！")
            else:
                df_current[title] = False
                save_class_df(selected_class, df_current)
                st.success(f"已成功新增【{title}】！")
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="control-card">', unsafe_allow_html=True)
    st.write("### 📢 缺交廣播複製區")
    hw_columns = [col for col in df_current.columns if col not in ["座號", "姓名"]]
    if hw_columns:
        target_hw = st.selectbox("選擇要催繳的作業：", hw_columns)
        unpaid_df = df_current[df_current[target_hw] == False]
        if len(unpaid_df) > 0:
            broadcast_text = f"【{selected_class} {target_hw} 缺交名單】\n"
            for _, row in unpaid_df.iterrows():
                broadcast_text += f"{int(row['座號'])}號 {row['姓名']}\n"
            st.text_area("📋 一鍵複製 LINE 催繳文字：", value=broadcast_text, height=180)
        else:
            st.success(f"💯 【{selected_class}】{target_hw} 全班皆已繳齊！")
    else: st.info("💡 目前尚無作業欄位。")
    st.markdown('</div>', unsafe_allow_html=True)

with col_table:
    st.write(f"### 📋 【{selected_class}】作業登記總表")
    
    # 核心智慧功能：表格檢視過濾器
    hw_columns = [col for col in df_current.columns if col not in ["座號", "姓名"]]
    
    # 自動偵測有哪些作業已經「全班繳齊 (全 True)」
    completed_hws = [col for col in hw_columns if df_current[col].all()]
    
    filter_col1, filter_col2 = st.columns([0.6, 0.4])
    with filter_col1:
        hide_completed = st.checkbox("🙈 自動隱藏全班已繳齊的作業", value=True)
    
    # 決定要呈現的欄位
    display_columns = ["座號", "姓名"]
    for col in hw_columns:
        if hide_completed and col in completed_hws:
            continue
        display_columns.append(col)

    st.caption("💡 提示：點擊勾選框 ☑️ 表示【已繳】。全班繳齊且勾選「隱藏」後，該欄位會自動收合保持介面乾淨。")

    # 設定欄位寬度（加大寬度避免文字擠壓）
    column_config = {
        "座號": st.column_config.NumberColumn("座號", disabled=True, width=70),
        "姓名": st.column_config.TextColumn("姓名", disabled=True, width=110),
    }
    
    for col in hw_columns:
        column_config[col] = st.column_config.CheckboxColumn(
            col,
            help="點擊打勾代表已繳交",
            default=False,
            width=130  # 設定固定適中寬度，修復標頭選單重疊問題
        )
            
    # 只顯示過濾後的資料欄位
    df_display = df_current[display_columns]

    edited_display_df = st.data_editor(
        df_display,
        column_config=column_config,
        hide_index=True,
        use_container_width=True,
        height=500,
        key=f"editor_{selected_class}"
    )
    
    st.write("")
    if st.button("💾 儲存變更", use_container_width=True, type="primary"):
        # 將修改後的過濾資料回寫至原始完整的 DataFrame
        for col in edited_display_df.columns:
            df_current[col] = edited_display_df[col]
        save_class_df(selected_class, df_current)
        st.success("✅ 作業繳交狀態已成功儲存！")
