import os
import random
import pandas as pd
import streamlit as st

st.set_page_config(page_title="03_座位表與幹部管理", page_icon="🪑", layout="wide")

# CSS 視覺優化
st.markdown("""
    <style>
    [data-testid="stSidebar"], button[data-testid="collapsedControl"], header[data-testid="stHeader"] {
        display: none !important;
    }
    .stApp {
        background-color: #F8FAFC;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", sans-serif;
    }
    .title-banner {
        background: linear-gradient(135deg, #0284C7 0%, #38BDF8 100%);
        color: white; padding: 18px 24px; border-radius: 16px; margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.15);
    }
    .title-banner h1 { color: #FFFFFF !important; font-size: 1.7rem !important; margin: 0 !important; }
    
    .podium {
        background-color: #334155; color: white; text-align: center;
        padding: 10px; font-weight: bold; font-size: 1rem;
        border-radius: 10px; margin-bottom: 20px; letter-spacing: 2px;
    }
    .col-header {
        text-align: center; font-weight: 700; color: #0284C7;
        margin-bottom: 8px; background-color: #E0F2FE; padding: 5px;
        border-radius: 6px; font-size: 0.9rem;
    }
    
    /* 幹部與名單卡片 */
    .cadre-tag {
        font-size: 0.75rem; color: #0369A1; background-color: #E0F2FE;
        padding: 2px 6px; border-radius: 4px; display: inline-block; margin-top: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# 學生與幹部資料庫
STUDENTS_801 = [
    {"座號": 1, "姓名": "王喬昕", "職務": "家政小老師"},
    {"座號": 2, "姓名": "吳岢曈", "職務": "公民+閩南語小老師"},
    {"座號": 3, "姓名": "李巧彤", "職務": "副班長 / 歷史小老師"},
    {"座號": 4, "姓名": "岳昀軒", "職務": ""},
    {"座號": 5, "姓名": "林晏以", "職務": "班長"},
    {"座號": 6, "姓名": "林晨琳", "職務": "地理小老師"},
    {"座號": 7, "姓名": "林芮妘", "職務": ""},
    {"座號": 8, "姓名": "林苡嫻", "職務": "視覺藝術小老師"},
    {"座號": 9, "姓名": "黃榆涵", "職務": ""},
    {"座號": 10, "姓名": "黃榆涵", "職務": "副衛生股長 / 數學小老師"},
    {"座號": 11, "姓名": "蔡可琳", "職務": "國文小老師"},
    {"座號": 12, "姓名": "戴彤竹", "職務": "輔導股長 / 綜合(一)小老師"},
    {"座號": 13, "姓名": "羅羽翎", "職務": "學藝股長 / 童軍小老師"},
    {"座號": 14, "姓名": "羅昕彤", "職務": "表藝小老師"},
    {"座號": 15, "姓名": "林禹彤", "職務": "衛生股長"},
    {"座號": 16, "姓名": "王楷文", "職務": "自然小老師 / 事務股長"},
    {"座號": 17, "姓名": "王駿展", "職務": "康樂股長 / 健教小老師"},
    {"座號": 18, "姓名": "吳軒佑", "職務": ""},
    {"座號": 19, "姓名": "李宇哲", "職務": ""},
    {"座號": 20, "姓名": "林柏辰", "職務": "風紀股長 / 生科小老師"},
    {"座號": 21, "姓名": "張品御", "職務": "音樂小老師"},
    {"座號": 22, "姓名": "陳正澤", "職務": "美感幾何小老師"},
    {"座號": 23, "姓名": "陳秉玄", "職務": ""},
    {"座號": 24, "姓名": "陳鼎硯", "職務": "食勤股長"},
    {"座號": 25, "姓名": "黃楙軒", "職務": "保健股長"},
    {"座號": 26, "姓名": "董子以", "職務": "本土語小老師"},
    {"座號": 27, "姓名": "劉家佑", "職務": "英語小老師"},
    {"座號": 28, "姓名": "魏辰恩", "職務": "資訊小老師"}
]

# 座位位置定義（共 28 個可排位置：前 5 列各 5 人，第 6 列 3 人）
POSITIONS = []
for r in range(5):
    for c in range(6):
        if c == 5 and r >= 3:
            continue
        POSITIONS.append((r, c))

SEAT_FILE = "801班_座位表_點選排位.csv"

def load_seats():
    if os.path.exists(SEAT_FILE):
        try:
            df = pd.read_csv(SEAT_FILE)
            seats_dict = {}
            for _, row in df.iterrows():
                seats_dict[(int(row['r']), int(row['c']))] = int(row['座號'])
            return seats_dict
        except: pass
    # 預設按順序排滿座位
    seats_dict = {}
    for idx, pos in enumerate(POSITIONS):
        if idx < len(STUDENTS_801):
            seats_dict[pos] = STUDENTS_801[idx]["座號"]
    return seats_dict

def save_seats(seats_dict):
    data = [{"r": k[0], "c": k[1], "座號": v} for k, v in seats_dict.items()]
    pd.DataFrame(data).to_csv(SEAT_FILE, index=False, encoding="utf-8-sig")

if "seats_grid" not in st.session_state:
    st.session_state["seats_grid"] = load_seats()

# 頂部抬頭
col_top_title, col_top_back = st.columns([0.80, 0.20])
with col_top_title:
    st.markdown('<div class="title-banner"><h1>🪑 801 班級座位表與幹部管理系統</h1></div>', unsafe_allow_html=True)
with col_top_back:
    if st.button("🏛️ 返回管理主控台", use_container_width=True):
        st.switch_page("main.py")

# 版面分割：左側學生名單/排位操作台，右側座位表區域
col_left, col_right = st.columns([0.32, 0.68], gap="medium")

# Helper Functions
student_dict = {s["座號"]: s for s in STUDENTS_801}
assigned_seats = st.session_state["seats_grid"]
assigned_students = set(assigned_seats.values())

with col_left:
    st.write("### ⚙️ 座位重置與快速調整")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("🔄 一鍵隨機抽籤", use_container_width=True):
            shuffled_ids = [s["座號"] for s in STUDENTS_801]
            random.shuffle(shuffled_ids)
            new_grid = {}
            for idx, pos in enumerate(POSITIONS):
                if idx < len(shuffled_ids):
                    new_grid[pos] = shuffled_ids[idx]
            st.session_state["seats_grid"] = new_grid
            save_seats(new_grid)
            st.toast("✅ 已重新隨機安排座位！", icon="🎲")
            st.rerun()

    with col_b2:
        if st.button("🗑️ 重置清空座位", type="primary", use_container_width=True):
            st.session_state["seats_grid"] = {}
            save_seats({})
            st.toast("🗑️ 座位已全部清空，可開始重新排位！", icon="✨")
            st.rerun()

    st.markdown("---")
    st.write("### 📌 手動指派座位")
    
    # 手動指派選單
    unassigned_students = [s for s in STUDENTS_801 if s["座號"] not in assigned_students]
    student_options = {f"{s['座號']}號 {s['姓名']} ({s['職務'] if s['職務'] else '學生'})": s["座號"] for s in STUDENTS_801}
    
    selected_stu_str = st.selectbox("1. 選擇學生：", list(student_options.keys()))
    selected_stu_id = student_options[selected_stu_str]
    
    pos_options = {}
    for r, c in POSITIONS:
        current_id = assigned_seats.get((r, c))
        status = f"已有人: {student_dict[current_id]['姓名']}" if current_id else "【空位】"
        pos_options[f"第 {r+1} 排 / 第 {c+1} 列 → {status}"] = (r, c)
        
    selected_pos_str = st.selectbox("2. 選擇目標位置：", list(pos_options.keys()))
    selected_pos = pos_options[selected_pos_str]
    
    if st.button("📍 指派到該座位", use_container_width=True, type="primary"):
        # 如果該學生已在別的位置，先清除舊位置
        for p, sid in list(assigned_seats.items()):
            if sid == selected_stu_id:
                del assigned_seats[p]
        assigned_seats[selected_pos] = selected_stu_id
        save_seats(assigned_seats)
        st.toast(f"✅ 已成功將 {student_dict[selected_stu_id]['姓名']} 排入該座位！", icon="🎯")
        st.rerun()

    st.markdown("---")
    st.write("### 📋 全班名單與幹部對照表")
    
    # 顯示未安排/已安排狀態
    df_stu = pd.DataFrame(STUDENTS_801)
    df_stu["狀態"] = df_stu["座號"].apply(lambda x: "✅ 已入座" if x in assigned_students else "⚠️ 未入座")
    st.dataframe(
        df_stu[["座號", "姓名", "職務", "狀態"]],
        hide_index=True,
        use_container_width=True,
        height=320
    )

with col_right:
    st.markdown('<div class="podium">📺 黑板 / 教師講台區（老師視角：左 👈 🪑 👉 右）</div>', unsafe_allow_html=True)
    
    # 標頭 (6 列)
    col_headers = st.columns(6, gap="small")
    for c_idx in range(6):
        with col_headers[c_idx]:
            st.markdown(f'<div class="col-header">第 {c_idx+1} 列</div>', unsafe_allow_html=True)

    # 渲染 5 排 x 6 列的座位格子
    for r_idx in range(5):
        cols = st.columns(6, gap="small")
        for c_idx in range(6):
            with cols[c_idx]:
                if c_idx == 5 and r_idx >= 3:
                    # 走道/非座位區域
                    st.caption("🚫 走道")
                else:
                    stu_id = assigned_seats.get((r_idx, c_idx))
                    if stu_id:
                        stu = student_dict[stu_id]
                        cadre_info = f"<br><span class='cadre-tag'>{stu['職務']}</span>" if stu['職務'] else ""
                        st.markdown(f"""
                            <div style="background-color: #FFFFFF; border: 2px solid #BAE6FD; border-radius: 12px; padding: 10px 4px; text-align: center; margin-bottom: 10px; min-height: 80px;">
                                <div style="font-size:0.75rem; color:#64748B;">{stu['座號']} 號</div>
                                <div style="font-size:1.05rem; font-weight:700; color:#0F172A; margin-top:2px;">{stu['姓名']}</div>
                                {cadre_info}
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                            <div style="background-color: #F8FAFC; border: 2px dashed #CBD5E1; border-radius: 12px; padding: 18px 4px; text-align: center; margin-bottom: 10px; min-height: 80px; color:#94A3B8; font-weight:600; font-size:0.9rem;">
                                🪑 空位
                            </div>
                        """, unsafe_allow_html=True)
