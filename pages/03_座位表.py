import json
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="03_座位表拖拉管理", page_icon="🪑", layout="wide")

# CSS 樣式隱藏側邊欄與頁首
st.markdown("""
    <style>
    [data-testid="stSidebar"], button[data-testid="collapsedControl"], header[data-testid="stHeader"] {
        display: none !important;
    }
    .stApp {
        background-color: #F8FAFC;
    }
    </style>
""", unsafe_allow_html=True)

# 801 班級學生資料 (28人)
STUDENTS_801 = [
    {"id": 1, "name": "王喬昕"}, {"id": 2, "name": "吳岢曈"}, {"id": 3, "name": "李巧彤"},
    {"id": 4, "name": "岳昀軒"}, {"id": 5, "name": "林晏以"}, {"id": 6, "name": "林晨琳"},
    {"id": 7, "name": "林芮妘"}, {"id": 8, "name": "林苡嫻"}, {"id": 9, "name": "黃榆涵"},
    {"id": 10, "name": "黃榆涵"}, {"id": 11, "name": "蔡可琳"}, {"id": 12, "name": "戴彤竹"},
    {"id": 13, "name": "羅羽翎"}, {"id": 14, "name": "羅昕彤"}, {"id": 15, "name": "林禹彤"},
    {"id": 16, "name": "王楷文"}, {"id": 17, "name": "王駿展"}, {"id": 18, "name": "吳軒佑"},
    {"id": 19, "name": "李宇哲"}, {"id": 20, "name": "林柏辰"}, {"id": 21, "name": "張品御"},
    {"id": 22, "name": "陳正澤"}, {"id": 23, "name": "陳秉玄"}, {"id": 24, "name": "陳鼎硯"},
    {"id": 25, "name": "黃楙軒"}, {"id": 26, "name": "董子以"}, {"id": 27, "name": "劉家佑"},
    {"id": 28, "name": "魏辰恩"}
]

# 幹部對照資料（已加入 23 陳秉玄）
CADRES_LIST = [
    {"cadre": "班長", "id": 5, "name": "林晏以"}, {"cadre": "副班長", "id": 3, "name": "李巧彤"},
    {"cadre": "風紀股長", "id": 20, "name": "林柏辰"}, {"cadre": "學藝股長", "id": 13, "name": "羅羽翎"},
    {"cadre": "衛生股長", "id": 15, "name": "林禹彤"}, {"cadre": "副衛生股長", "id": 10, "name": "黃榆涵"},
    {"cadre": "保健股長", "id": 25, "name": "黃楙軒"}, {"cadre": "康樂股長", "id": 17, "name": "王駿展"},
    {"cadre": "輔導股長", "id": 12, "name": "戴彤竹"}, {"cadre": "事務股長", "id": 16, "name": "王楷文"},
    {"cadre": "食勤股長", "id": 24, "name": "陳鼎硯"}, {"cadre": "國文小老師", "id": 11, "name": "蔡可琳"},
    {"cadre": "英語小老師", "id": 27, "name": "劉家佑"}, {"cadre": "數學小老師", "id": 10, "name": "黃榆涵"},
    {"cadre": "自然小老師", "id": 16, "name": "王楷文"}, {"cadre": "歷史小老師", "id": 3, "name": "李巧彤"},
    {"cadre": "地理小老師", "id": 6, "name": "林晨琳"}, {"cadre": "公民+閩南語", "id": 2, "name": "吳岢曈"},
    {"cadre": "音樂小老師", "id": 21, "name": "張品御"}, {"cadre": "表藝小老師", "id": 14, "name": "羅昕彤"},
    {"cadre": "視覺藝術", "id": 8, "name": "林苡嫻"}, {"cadre": "健康教育", "id": 17, "name": "王駿展"},
    {"cadre": "綜合(一)輔導", "id": 12, "name": "戴彤竹"}, {"cadre": "綜合(二)童軍", "id": 13, "name": "羅羽翎"},
    {"cadre": "綜合(三)家政", "id": 1, "name": "王喬昕"}, {"cadre": "資訊小老師", "id": 28, "name": "魏辰恩"},
    {"cadre": "生科小老師", "id": 20, "name": "林柏辰"}, {"cadre": "本土語小老師", "id": 26, "name": "董子以"},
    {"cadre": "美感幾何", "id": 22, "name": "陳正澤"}, {"cadre": "協助小老師", "id": 23, "name": "陳秉玄"}
]

# 頂部控制欄
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.title("🪑 801 班級座位表管理系統（直覺拖拉版）")
with col2:
    if st.button("🏛️ 返回主控台", use_container_width=True):
        st.switch_page("main.py")

# HTML + JavaScript 核心元件
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro TC", "PingFang TC", "Microsoft JhengHei", sans-serif;
        background-color: #F8FAFC;
        margin: 0; padding: 10px;
    }}
    .container {{
        display: flex;
        gap: 20px;
        align-items: flex-start;
    }}
    .left-panel {{
        width: 32%;
        background: #FFFFFF;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
    }}
    .right-panel {{
        width: 66%;
        background: #FFFFFF;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
    }}
    .btn-group {{
        display: flex;
        gap: 8px;
        margin-bottom: 14px;
        flex-wrap: wrap;
    }}
    button {{
        cursor: pointer;
        padding: 9px 14px;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        font-size: 0.88rem;
        transition: all 0.2s;
    }}
    .btn-primary {{ background-color: #0284C7; color: white; }}
    .btn-primary:hover {{ background-color: #0369A1; }}
    .btn-danger {{ background-color: #EF4444; color: white; }}
    .btn-danger:hover {{ background-color: #DC2626; }}
    .btn-success {{ background-color: #10B981; color: white; }}
    .btn-success:hover {{ background-color: #059669; }}
    .btn-secondary {{ background-color: #64748B; color: white; }}
    
    /* 頁籤 */
    .tab-nav {{ display: flex; gap: 6px; margin-bottom: 12px; }}
    .tab-btn {{
        flex: 1; background: #F1F5F9; color: #64748B; padding: 8px; border-radius: 8px; text-align: center;
    }}
    .tab-btn.active {{
        background: #0284C7; color: white;
    }}
    .tab-content {{ display: none; }}
    .tab-content.active {{ display: block; }}

    /* 左側學生名單：雙欄 Grid 展示，不需捲軸 */
    .student-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
    }}
    .student-card {{
        background: #F0F9FF;
        border: 1.5px solid #BAE6FD;
        border-radius: 10px;
        padding: 8px 10px;
        cursor: grab;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: bold;
        font-size: 0.9rem;
        color: #0369A1;
        user-select: none;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }}
    .student-card:hover {{
        background: #E0F2FE;
        border-color: #0284C7;
    }}
    .student-card:active {{ cursor: grabbing; }}

    /* 幹部小老師精緻卡片網格 */
    .cadre-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
        max-height: 750px;
        overflow-y: auto;
    }}
    .cadre-card {{
        background: #FFF7ED;
        border: 1.5px solid #FFEDD5;
        border-radius: 10px;
        padding: 8px 10px;
        display: flex;
        flex-direction: column;
    }}
    .cadre-title {{ font-size: 0.75rem; color: #EA580C; font-weight: 800; }}
    .cadre-user {{ font-size: 0.9rem; color: #7C2D12; font-weight: 700; margin-top: 2px; }}
    
    /* 座位網格布局 */
    .grid-container {{
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 8px;
        margin-bottom: 12px;
    }}
    .col-header {{
        text-align: center;
        background: #E0F2FE;
        color: #0284C7;
        font-weight: bold;
        padding: 7px;
        border-radius: 8px;
        font-size: 0.9rem;
    }}
    .seat-box {{
        background: #F8FAFC;
        border: 2px dashed #CBD5E1;
        border-radius: 12px;
        height: 78px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: all 0.2s;
    }}
    .seat-box.drag-over {{
        background: #E0F2FE;
        border-color: #0284C7;
        transform: scale(1.02);
    }}
    .seat-occupied {{
        background: #FFFFFF;
        border: 2px solid #38BDF8;
        box-shadow: 0 3px 6px rgba(0,0,0,0.04);
        cursor: grab;
    }}
    .seat-id {{ font-size: 0.78rem; color: #64748B; font-weight: 600; }}
    .seat-name {{ font-size: 1.1rem; font-weight: 800; color: #0F172A; margin-top: 2px; }}
    .walkway {{
        background: transparent;
        border: none;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: bold;
    }}
    
    .podium {{
        background: #334155;
        color: white;
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        font-weight: bold;
        margin: 12px 0;
        letter-spacing: 1px;
    }}

    /* A4 列印模式對應控制 */
    @media print {{
        .left-panel, .btn-group, button {{ display: none !important; }}
        .right-panel {{ width: 100% !important; border: none !important; box-shadow: none !important; }}
        body {{ background: white; margin: 0; padding: 0; }}
        .seat-box {{ border: 1.5px solid #000 !important; height: 85px !important; }}
        .col-header {{ border: 1.5px solid #000; background: #eee !important; color: #000; }}
        .podium {{ border: 1.5px solid #000; background: #ddd !important; color: #000; }}
    }}
</style>
</head>
<body>

<div class="container">
    <!-- 左側面板：學生名單/幹部小老師 -->
    <div class="left-panel">
        <div class="tab-nav">
            <button class="tab-btn active" onclick="switchTab('unassignedTab', this)">🎒 待安排學生</button>
            <button class="tab-btn" onclick="switchTab('cadreTab', this)">🎖️ 幹部小老師</button>
        </div>

        <div id="unassignedTab" class="tab-content active">
            <div id="studentPool" class="student-grid"></div>
        </div>

        <div id="cadreTab" class="tab-content">
            <div id="cadreGrid" class="cadre-grid"></div>
        </div>
    </div>

    <!-- 右側面板：座位表 -->
    <div class="right-panel">
        <div class="btn-group">
            <button class="btn-primary" onclick="autoAssign()">🎲 一鍵隨機排位</button>
            <button class="btn-danger" onclick="resetSeats()">🗑️ 清空重置座位</button>
            <button class="btn-success" onclick="window.print()">🖨️ 列印座位表</button>
            <button class="btn-secondary" onclick="toggleView()" id="viewBtn">🔄 切換為學生視角</button>
        </div>

        <div id="topPodium" class="podium" style="display:none;">📺 黑板 / 教師講台區（學生視角：面向講台）</div>

        <div class="grid-container" id="gridHeader"></div>
        <div class="grid-container" id="gridSeats"></div>

        <div id="bottomPodium" class="podium">📺 黑板 / 教師講台區（老師講台視角：站在講台面對學生）</div>
    </div>
</div>

<script>
const studentsData = {json.dumps(STUDENTS_801)};
const cadresData = {json.dumps(CADRES_LIST)};

let seatsMap = {{}}; // posKey -> studentId
let isTeacherView = true;

function init() {{
    renderCadreCards();
    renderGrid();
    renderStudentPool();
}}

function switchTab(tabId, btn) {{
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    btn.classList.add('active');
}}

function renderCadreCards() {{
    const container = document.getElementById('cadreGrid');
    container.innerHTML = cadresData.map(c => `
        <div class="cadre-card">
            <div class="cadre-title">🏷️ ${{c.cadre}}</div>
            <div class="cadre-user">${{c.id}}號 ${{c.name}}</div>
        </div>
    `).join('');
}}

function renderStudentPool() {{
    const pool = document.getElementById('studentPool');
    pool.innerHTML = '';
    const assignedIds = new Set(Object.values(seatsMap));

    const unassigned = studentsData.filter(s => !assignedIds.has(s.id));
    
    if(unassigned.length === 0) {{
        pool.innerHTML = '<div style="grid-column: span 2; text-align:center; color:#10B981; font-weight:bold; padding:20px 0;">🎉 全班同學皆已指派入座！</div>';
        return;
    }}

    unassigned.forEach(s => {{
        const card = document.createElement('div');
        card.className = 'student-card';
        card.draggable = true;
        card.innerHTML = `<span>${{s.id}}號 ${{s.name}}</span> <span style="opacity:0.4;">⋮⋮</span>`;
        card.ondragstart = (e) => e.dataTransfer.setData('text/plain', s.id);
        pool.appendChild(card);
    }});
}}

function renderGrid() {{
    const headerContainer = document.getElementById('gridHeader');
    const seatsContainer = document.getElementById('gridSeats');
    headerContainer.innerHTML = '';
    seatsContainer.innerHTML = '';

    // 渲染直列標頭 (6列)
    for(let c = 0; c < 6; c++) {{
        const colNum = isTeacherView ? (c + 1) : (6 - c);
        headerContainer.innerHTML += `<div class="col-header">第 ${{colNum}} 列</div>`;
    }}

    // 排數渲染：老師視角（5排往下到1排），學生視角（1排往後到5排）
    const rowOrder = isTeacherView ? [4, 3, 2, 1, 0] : [0, 1, 2, 3, 4];

    rowOrder.forEach(r => {{
        for(let c = 0; c < 6; c++) {{
            const realC = isTeacherView ? c : (5 - c);
            const box = document.createElement('div');
            
            if (realC === 5 && r >= 3) {{
                box.className = 'seat-box walkway';
                box.innerHTML = '🚫 走道';
            }} else {{
                const posKey = `${{r}}_${{realC}}`;
                const stuId = seatsMap[posKey];
                
                if (stuId) {{
                    const stu = studentsData.find(s => s.id === stuId);
                    box.className = 'seat-box seat-occupied';
                    box.draggable = true;
                    box.innerHTML = `<div class="seat-id">${{stu.id}} 號</div><div class="seat-name">${{stu.name}}</div>`;
                    box.ondragstart = (e) => e.dataTransfer.setData('text/plain', stu.id);
                }} else {{
                    box.className = 'seat-box';
                    box.innerHTML = `<div class="seat-id">第 ${{r+1}} 排</div><div style="color:#CBD5E1; font-weight:600;">空位</div>`;
                }}

                box.ondragover = (e) => {{ e.preventDefault(); box.classList.add('drag-over'); }};
                box.ondragleave = () => box.classList.remove('drag-over');
                box.ondrop = (e) => {{
                    e.preventDefault();
                    box.classList.remove('drag-over');
                    const droppedId = parseInt(e.dataTransfer.getData('text/plain'));
                    if (droppedId) {{
                        Object.keys(seatsMap).forEach(k => {{ if (seatsMap[k] === droppedId) delete seatsMap[k]; }});
                        seatsMap[posKey] = droppedId;
                        renderGrid();
                        renderStudentPool();
                    }}
                }};
            }}
            seatsContainer.appendChild(box);
        }}
    }});
}}

function toggleView() {{
    isTeacherView = !isTeacherView;
    document.getElementById('topPodium').style.display = isTeacherView ? 'none' : 'block';
    document.getElementById('bottomPodium').style.display = isTeacherView ? 'block' : 'none';
    document.getElementById('viewBtn').innerText = isTeacherView ? '🔄 切換為學生視角' : '🔄 切換為老師視角';
    renderGrid();
}}

function autoAssign() {{
    seatsMap = {{}};
    let idx = 0;
    const shuffled = [...studentsData].sort(() => Math.random() - 0.5);
    for(let r = 0; r < 5; r++) {{
        for(let c = 0; c < 6; c++) {{
            if (c === 5 && r >= 3) continue;
            if (idx < shuffled.length) {{
                seatsMap[`${{r}}_${{c}}`] = shuffled[idx].id;
                idx++;
            }}
        }}
    }}
    renderGrid();
    renderStudentPool();
}}

function resetSeats() {{
    seatsMap = {{}};
    renderGrid();
    renderStudentPool();
}}

window.onload = init;
</script>
</body>
</html>
"""

components.html(html_code, height=800, scrolling=False)
