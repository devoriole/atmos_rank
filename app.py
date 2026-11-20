import os
import json
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(
    page_title="АтмоС Арена | Реестр разрядов и учеников",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Sleek Dark Theme Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Dark Theme Background */
    .stApp {
        background-color: #090D16 !important;
        color: #F1F5F9;
    }

    /* Hero Banner Dark Glassmorphism */
    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #131C31 40%, #1E1B4B 100%);
        border-radius: 20px;
        padding: 32px 36px;
        color: #FFFFFF;
        box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.6), 0 0 25px rgba(59, 130, 246, 0.1);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(30, 58, 138, 0.4);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(96, 165, 250, 0.3);
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #60A5FA;
        margin-bottom: 12px;
    }
    
    .hero-title {
        font-size: 2.15rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 8px;
        background: linear-gradient(180deg, #FFFFFF 0%, #CBD5E1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 0.95rem;
        color: #94A3B8;
        max-width: 680px;
        line-height: 1.55;
    }
    
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #10B981;
    }

    /* KPI Cards Dark */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 14px;
        margin-bottom: 24px;
    }
    
    .kpi-card {
        background: #111827;
        border-radius: 16px;
        padding: 18px 16px;
        border: 1px solid #1F2937;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: #374151;
        box-shadow: 0 12px 24px -4px rgba(0, 0, 0, 0.4);
    }
    
    .kpi-icon {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.15rem;
        margin-bottom: 12px;
    }
    
    .kpi-label {
        font-size: 0.74rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    
    .kpi-num {
        font-size: 1.65rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.1;
    }

    /* Dark Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #111827 !important;
        padding: 6px;
        border-radius: 14px;
        border: 1px solid #1F2937 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.9rem;
        color: #94A3B8 !important;
        padding: 0 16px;
        transition: all 0.15s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1E293B !important;
        color: #60A5FA !important;
        border: 1px solid #334155 !important;
        border-radius: 10px;
    }

    /* Dark Profile Card */
    .profile-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .avatar-circle {
        width: 58px;
        height: 58px;
        border-radius: 50%;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        font-weight: 700;
        box-shadow: 0 0 20px rgba(37, 99, 235, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    .rank-pill {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    
    .rank-pill-sport {
        background: rgba(99, 102, 241, 0.2);
        color: #A5B4FC;
        border: 1px solid rgba(99, 102, 241, 0.4);
    }
    
    .rank-pill-junior {
        background: rgba(245, 158, 11, 0.2);
        color: #FCD34D;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    
    .rank-pill-none {
        background: rgba(148, 163, 184, 0.12);
        color: #94A3B8;
        border: 1px solid rgba(148, 163, 184, 0.25);
    }
    
    /* Timeline item Dark */
    .timeline-item {
        border-left: 2px solid #3B82F6;
        padding-left: 20px;
        margin-left: 8px;
        margin-bottom: 20px;
        position: relative;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -7px;
        top: 2px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #3B82F6;
        border: 2px solid #090D16;
        box-shadow: 0 0 8px #3B82F6;
    }

    /* Dark Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0B0F19 !important;
        border-right: 1px solid #1E293B !important;
    }
    
    /* Container borders dark */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #111827 !important;
        border: 1px solid #1F2937 !important;
        border-radius: 14px !important;
    }

    /* Metric values dark */
    [data-testid="stMetricValue"] {
        color: #F8FAFC !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
    }
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "Реестр_приказов_и_разрядов.json")
XLSX_FILE = os.path.join(BASE_DIR, "Реестр_приказов_и_разрядов.xlsx")
CSV_FILE = os.path.join(BASE_DIR, "Реестр_приказов_и_разрядов.csv")
MD_FILE = os.path.join(BASE_DIR, "Реестр_приказов_и_разрядов.md")
PHOTOS_DIR = os.path.join(BASE_DIR, "photos")

# Load Data
@st.cache_data
def load_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        df_ath = pd.DataFrame(data["athletes"])
        df_ord = pd.DataFrame(data["orders"])
        df_stu = pd.DataFrame(data.get("students", []))
        return df_ath, df_ord, df_stu
    return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_athletes, df_orders, df_students = load_data()

if df_athletes.empty:
    st.error("Файл данных не найден. Убедитесь, что 'Реестр_приказов_и_разрядов.json' находится в папке приложения.")
    st.stop()

import subprocess
import shutil

# Шкала старшинства спортивных разрядов ЕВСК
RANK_WEIGHTS = {
    "ЗМС": 100,
    "МСМК": 90,
    "МС": 80,
    "Мастер спорта": 80,
    "КМС": 70,
    "Кандидат в мастера спорта": 70,
    "1 спортивный разряд": 60,
    "1 спортивный": 60,
    "2 спортивный разряд": 50,
    "2 спортивный": 50,
    "3 спортивный разряд": 40,
    "3 спортивный": 40,
    "III спортивный разряд": 40,
    "1 юношеский разряд": 30,
    "1 юношеский": 30,
    "2 юношеский разряд": 20,
    "2 юношеский": 20,
    "3 юношеский разряд": 10,
    "3 юношеский": 10,
    "Без разряда": 0,
}

def get_rank_weight(rank_str):
    if not rank_str:
        return 0
    rank_clean = str(rank_str).strip()
    for k, w in RANK_WEIGHTS.items():
        if k.lower() in rank_clean.lower():
            return w
    return 0

def get_highest_rank_record(ranks_df):
    if ranks_df is None or ranks_df.empty:
        return None
    df_sorted = ranks_df.copy()
    df_sorted["weight"] = df_sorted["rank"].map(get_rank_weight)
    df_sorted["parsed_date"] = pd.to_datetime(df_sorted["order_date"], format="%d.%m.%Y", errors="coerce")
    df_sorted = df_sorted.sort_values(by=["weight", "parsed_date"], ascending=[False, False])
    return df_sorted.iloc[0]

def save_registry_files(json_data, base_dir=BASE_DIR):
    """Синхронно сохраняет обновленные данные в JSON, CSV, XLSX и MD."""
    json_path = os.path.join(base_dir, "Реестр_приказов_и_разрядов.json")
    xlsx_path = os.path.join(base_dir, "Реестр_приказов_и_разрядов.xlsx")
    csv_path = os.path.join(base_dir, "Реестр_приказов_и_разрядов.csv")
    md_path = os.path.join(base_dir, "Реестр_приказов_и_разрядов.md")

    # 1. JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    df_ath = pd.DataFrame(json_data["athletes"])
    df_ord = pd.DataFrame(json_data["orders"])
    df_stu = pd.DataFrame(json_data.get("students", []))

    # 2. CSV
    cols_csv = {
        "fio": "ФИО спортсмена / ученика",
        "birth": "Дата / Год рожд.",
        "rank": "Присвоенный разряд / Статус",
        "rank_type": "Категория",
        "order_num": "Номер приказа",
        "order_date": "Дата приказа",
        "org": "Орган / Организация",
        "city": "Город",
        "competition": "Основание / Соревнование",
        "discipline": "Дисциплина",
        "place": "Результат / Статус",
        "club": "Филиал / Клуб",
        "notes": "Примечания / Договор"
    }
    df_c = df_ath.copy()
    df_c["birth"] = df_c.apply(lambda r: str(r.get("birth_date") or r.get("birth_year") or "-"), axis=1)
    df_c["№ п/п"] = range(1, len(df_c) + 1)
    csv_out = df_c[["№ п/п"] + list(cols_csv.keys())].rename(columns=cols_csv)
    csv_out.to_csv(csv_path, sep=";", index=False, encoding="utf-8-sig")

    # 3. XLSX
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        csv_out.to_excel(writer, sheet_name="Сводный реестр", index=False)
        sport_df = csv_out[csv_out["Категория"] == "Спортивный"]
        sport_df.to_excel(writer, sheet_name="Спортивные разряды", index=False)
        junior_df = csv_out[csv_out["Категория"] == "Юношеский"]
        junior_df.to_excel(writer, sheet_name="Юношеские разряды", index=False)
        if not df_stu.empty:
            stu_out = df_stu.copy()
            stu_out["Присвоенные разряды"] = stu_out["ranks"].apply(lambda r: ", ".join(r) if r else "-")
            stu_out.to_excel(writer, sheet_name="Ученики Академии", index=False)
        if not df_ord.empty:
            df_ord.to_excel(writer, sheet_name="Приказы (документы)", index=False)

    # 4. MD
    total_ath = len(df_ath)
    total_orders = len(df_ord)
    sport_count = (df_ath["rank_type"] == "Спортивный").sum()
    junior_count = (df_ath["rank_type"] == "Юношеский").sum()

    md_lines = [
        "# Реестр приказов и присвоенных разрядов по гонкам дронов (БВС)",
        "",
        "Данные сформированы на основе фотокопий официальных приказов органов исполнительной власти в сфере спорта и региональной спортивной федерации РФСОО «Федерация гонок дронов Ростовской области».",
        "",
        "## Общая статистика",
        f"- **Всего записей о присвоениях:** {total_ath}",
        f"- **Всего документов (приказов/выписок):** {total_orders}",
        f"- **Спортивные разряды:** {sport_count}",
        f"- **Юношеские разряды:** {junior_count}",
        "",
        "## 1. Реестр документов (приказов)",
        "| № | Орган / Организация | Номер приказа | Дата | Город | Предмет приказа | Чел. | Файл(ы) фото |",
        "|---|---|---|---|---|---|---|---|"
    ]
    for idx, r in df_ord.iterrows():
        md_lines.append(f"| {idx+1} | {r.get('org','')} | {r.get('num','')} | {r.get('date','')} | {r.get('city','')} | {r.get('subj','')} | {r.get('count','')} | `{r.get('file','')}` |")

    md_lines.extend([
        "",
        "## 2. Сводный список присвоенных разрядов",
        "| № | ФИО | Год | Разряд | Приказ | Дата | Орган / Организация | Город | Соревнование / Основание | Дисциплина / Место | Клуб / Примечания |",
        "|---|---|---|---|---|---|---|---|---|---|---|"
    ])
    for idx, r in df_ath.iterrows():
        fio_b = f"**{r.get('fio','')}**"
        yr = str(r.get('birth_year') or '')
        rk = str(r.get('rank') or '')
        onum = str(r.get('order_num') or '')
        odate = str(r.get('order_date') or '')
        org = str(r.get('org') or '')
        cty = str(r.get('city') or '')
        comp = str(r.get('competition') or '')
        disc = f"{r.get('discipline','')} - {r.get('place','')}" if r.get('place') else str(r.get('discipline') or '')
        clb = str(r.get('club') or '')
        md_lines.append(f"| {idx+1} | {fio_b} | {yr} | {rk} | {onum} | {odate} | {org} | {cty} | {comp} | {disc} | {clb} |")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines) + "\n")

def run_git_sync(repo_dir=BASE_DIR, commit_msg=None):
    if not commit_msg:
        commit_msg = f"feat: обновление реестра разрядов ({pd.Timestamp.now().strftime('%d.%m.%Y %H:%M')})"
    try:
        r1 = subprocess.run(["git", "add", "."], cwd=repo_dir, capture_output=True, text=True)
        st_res = subprocess.run(["git", "status", "--porcelain"], cwd=repo_dir, capture_output=True, text=True)
        if not st_res.stdout.strip():
            return True, "Рабочее дерево чисто. Все файлы актуальны."
        r2 = subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_dir, capture_output=True, text=True)
        if r2.returncode != 0:
            return False, f"Ошибка git commit:\n{r2.stderr}\n{r2.stdout}"
        r3 = subprocess.run(["git", "push", "origin", "main"], cwd=repo_dir, capture_output=True, text=True)
        if r3.returncode == 0:
            return True, f"Успешно выгружено на GitHub!\n{r3.stdout}"
        else:
            return False, f"Ошибка при git push:\n{r3.stderr}\n{r3.stdout}"
    except Exception as e:
        return False, f"Ошибка выполнения git: {str(e)}"

# Helper for initials
def get_initials(fio):
    parts = fio.strip().split()
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[1][0]}".upper()
    elif len(parts) == 1:
        return parts[0][:2].upper()
    return "АТ"

# Callbacks for column state management (run before widgets are instantiated)
def set_main_cols(cols):
    st.session_state["selected_main_cols"] = cols

def set_student_cols(cols):
    st.session_state["selected_student_cols"] = cols

def set_order_cols(cols):
    st.session_state["selected_order_cols"] = cols

# HERO BANNER DARK
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">
        <span class="pulse-dot"></span>
        АтмоС Арена • Федерация гонок дронов РО
    </div>
    <div class="hero-title">Единый реестр спортсменов и разрядов</div>
    <div class="hero-subtitle">
        Официальные приказы, база обучающихся Академии пилотов «АтмоС», хронология квалификаций и присвоения спортивных разрядов по гонкам дронов (беспилотных воздушных судов).
    </div>
</div>
""", unsafe_allow_html=True)

# TOP KPI STATS DARK
total_entries = len(df_athletes)
unique_people = df_athletes["fio"].nunique()
total_students = len(df_students)
sport_ranks = (df_athletes["rank_type"] == "Спортивный").sum()
junior_ranks = (df_athletes["rank_type"] == "Юношеский").sum()
no_ranks = (df_athletes["rank"] == "Без разряда").sum()

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-icon" style="background: rgba(37, 99, 235, 0.2); color: #60A5FA;">🗂️</div>
        <div class="kpi-label">Всего записей</div>
        <div class="kpi-num">{total_entries}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon" style="background: rgba(16, 185, 129, 0.2); color: #34D399;">👥</div>
        <div class="kpi-label">Спортсменов</div>
        <div class="kpi-num">{unique_people}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon" style="background: rgba(147, 51, 234, 0.2); color: #C084FC;">🎓</div>
        <div class="kpi-label">В Академии</div>
        <div class="kpi-num">{total_students}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon" style="background: rgba(99, 102, 241, 0.2); color: #818CF8;">🏆</div>
        <div class="kpi-label">Спортивные</div>
        <div class="kpi-num">{sport_ranks}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon" style="background: rgba(245, 158, 11, 0.2); color: #FBBF24;">🎖️</div>
        <div class="kpi-label">Юношеские</div>
        <div class="kpi-num">{junior_ranks}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon" style="background: rgba(148, 163, 184, 0.15); color: #94A3B8;">⏳</div>
        <div class="kpi-label">Без разряда</div>
        <div class="kpi-num">{no_ranks}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# SIDEBAR: COLUMN PICKER FOR MAIN REGISTRY
st.sidebar.markdown("### 🎛️ Столбцы сводного реестра")

ALL_MAIN_COLS = {
    "ФИО спортсмена / ученика": "fio",
    "Дата / Год": "birth",
    "Разряд / Статус": "rank",
    "Категория": "rank_type",
    "№ приказа": "order_num",
    "Дата приказа": "order_date",
    "Город": "city",
    "Орган / Организация": "org",
    "Дисциплина": "discipline",
    "Результат / Статус": "place",
    "Филиал / Клуб": "club",
    "Примечания / Договор": "notes"
}

if "selected_main_cols" not in st.session_state:
    st.session_state["selected_main_cols"] = list(ALL_MAIN_COLS.keys())

# Quick presets in sidebar
p1, p2, p3 = st.sidebar.columns(3)
p1.button("Все", key="sb_btn_all", on_click=set_main_cols, args=(list(ALL_MAIN_COLS.keys()),), help="Показать все 12 столбцов")
p2.button("Кратко", key="sb_btn_brief", on_click=set_main_cols, args=(["ФИО спортсмена / ученика", "Разряд / Статус", "№ приказа", "Дата приказа", "Город"],), help="Краткий вид: ФИО, Разряд, № приказа, Дата, Город")
p3.button("Спорт", key="sb_btn_sport", on_click=set_main_cols, args=(["ФИО спортсмена / ученика", "Разряд / Статус", "Категория", "№ приказа", "Дисциплина", "Результат / Статус"],), help="Спортивные квалификации и результаты")

selected_main_cols = st.sidebar.multiselect(
    "Удаляйте крестиком ✕ или добавляйте:",
    options=list(ALL_MAIN_COLS.keys()),
    key="selected_main_cols"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Фильтрация и поиск")

search_fio = st.sidebar.text_input("Поиск по фамилии или имени:", placeholder="например: Хлыбов, Сазонов...")

category_filter = st.sidebar.radio(
    "Категория учета:",
    options=["Все записи", "Спортивные разряды", "Юношеские разряды", "Только аттестованные", "Ученики без разряда"],
    index=0
)

all_ranks = sorted(df_athletes["rank"].unique().tolist())
selected_ranks = st.sidebar.multiselect(
    "Выбор разряда:",
    options=all_ranks,
    default=[]
)

all_cities = sorted([c for c in df_athletes["city"].dropna().unique().tolist() if c])
selected_cities = st.sidebar.multiselect(
    "Город / Муниципалитет:",
    options=all_cities,
    default=[]
)

# Apply filters
filtered_df = df_athletes.copy()

if search_fio:
    filtered_df = filtered_df[filtered_df["fio"].str.contains(search_fio, case=False, na=False)]

if category_filter == "Спортивные разряды":
    filtered_df = filtered_df[filtered_df["rank_type"] == "Спортивный"]
elif category_filter == "Юношеские разряды":
    filtered_df = filtered_df[filtered_df["rank_type"] == "Юношеский"]
elif category_filter == "Только аттестованные":
    filtered_df = filtered_df[filtered_df["rank"] != "Без разряда"]
elif category_filter == "Ученики без разряда":
    filtered_df = filtered_df[filtered_df["rank"] == "Без разряда"]

if selected_ranks:
    filtered_df = filtered_df[filtered_df["rank"].isin(selected_ranks)]

if selected_cities:
    filtered_df = filtered_df[filtered_df["city"].isin(selected_cities)]

# Downloads in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Экспорт данных")

if os.path.exists(XLSX_FILE):
    with open(XLSX_FILE, "rb") as f:
        st.sidebar.download_button(
            label="📊 Выгрузить в Excel (.xlsx)",
            data=f,
            file_name="Реестр_приказов_и_разрядов.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width='stretch'
        )

if os.path.exists(CSV_FILE):
    with open(CSV_FILE, "rb") as f:
        st.sidebar.download_button(
            label="📄 Скачать CSV (.csv)",
            data=f,
            file_name="Реестр_приказов_и_разрядов.csv",
            mime="text/csv",
            width='stretch'
        )

if os.path.exists(MD_FILE):
    with open(MD_FILE, "rb") as f:
        st.sidebar.download_button(
            label="📝 Документ Markdown (.md)",
            data=f,
            file_name="Реестр_приказов_и_разрядов.md",
            mime="text/markdown",
            width='stretch'
        )

# TABS
tab_table, tab_students, tab_orders, tab_stats, tab_athlete, tab_upload = st.tabs([
    "📋 Сводный реестр",
    "🎓 Ученики Академии АтмоС",
    "📑 Приказы и фото документов",
    "📊 Аналитика",
    "👤 Персональное досье",
    "📥 Внесение разрядов"
])

# TAB 1: MAIN REGISTRY TABLE
with tab_table:
    display_df = filtered_df.copy()
    display_df["birth"] = display_df.apply(
        lambda row: str(row["birth_date"]) if row["birth_date"] else (str(int(row["birth_year"])) if row["birth_year"] else "-"),
        axis=1
    )
    
    col_map = {
        "fio": "ФИО спортсмена / ученика",
        "birth": "Дата / Год",
        "rank": "Разряд / Статус",
        "rank_type": "Категория",
        "order_num": "№ приказа",
        "order_date": "Дата приказа",
        "city": "Город",
        "org": "Орган / Организация",
        "discipline": "Дисциплина",
        "place": "Результат / Статус",
        "club": "Филиал / Клуб",
        "notes": "Примечания / Договор"
    }
    
    table_df = display_df[list(col_map.keys())].rename(columns=col_map)
    active_cols = [c for c in selected_main_cols if c in table_df.columns]
    
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.markdown(f"#### Записи реестра (отобрано: **{len(filtered_df)}** из {len(df_athletes)})")
    with col_t2:
        st.markdown(f"<div style='text-align: right; color: #94A3B8; font-size: 0.9rem; padding-top: 6px;'>Столбцов: <b style='color: #60A5FA;'>{len(active_cols)}</b> из {len(ALL_MAIN_COLS)}</div>", unsafe_allow_html=True)
    
    with st.expander("⚙️ Настроить столбцы реестра (быстрые наборы и переключатели)", expanded=False):
        tb1, tb2, tb3, tb4 = st.columns(4)
        tb1.button("Показать все (12)", key="t_btn_all", on_click=set_main_cols, args=(list(ALL_MAIN_COLS.keys()),))
        tb2.button("Краткий вид (5)", key="t_btn_brief", on_click=set_main_cols, args=(["ФИО спортсмена / ученика", "Разряд / Статус", "№ приказа", "Дата приказа", "Город"],))
        tb3.button("Спорт и соревнования", key="t_btn_sport", on_click=set_main_cols, args=(["ФИО спортсмена / ученика", "Разряд / Статус", "Категория", "№ приказа", "Дисциплина", "Результат / Статус"],))
        tb4.button("Академия АтмоС", key="t_btn_acad", on_click=set_main_cols, args=(["ФИО спортсмена / ученика", "Дата / Год", "Разряд / Статус", "Филиал / Клуб", "Примечания / Договор"],))
        st.caption("💡 Вы также можете в любой момент удалять столбцы крестиком `✕` или добавлять их в левой боковой панели под блоком **«🎛️ Столбцы сводного реестра»**.")

    if active_cols:
        st.dataframe(
            table_df[active_cols],
            width='stretch',
            hide_index=True,
            height=540,
            column_config={
                "ФИО спортсмена / ученика": st.column_config.TextColumn(width="medium"),
                "Разряд / Статус": st.column_config.TextColumn(width="medium"),
                "Категория": st.column_config.TextColumn(width="small"),
                "№ приказа": st.column_config.TextColumn(width="small"),
                "Дата приказа": st.column_config.TextColumn(width="small"),
                "Город": st.column_config.TextColumn(width="small"),
            }
        )
    else:
        st.warning("⚠️ Все столбцы скрыты. Выберите нужные столбцы в меню настройки выше или в левой панели.")

# TAB 2: STUDENTS BASE
ALL_STUDENT_COLS = {
    "ФИО ученика": "fio",
    "Дата рождения": "birth_date",
    "Филиал / Занятия": "branch",
    "№ Договора": "contract",
    "Статус": "status_label",
    "Присвоенные разряды": "ranks_label",
    "Примечания": "notes"
}

if "selected_student_cols" not in st.session_state:
    st.session_state["selected_student_cols"] = list(ALL_STUDENT_COLS.keys())

with tab_students:
    st.markdown("#### База обучающихся Академии пилотов «АтмоС»")
    
    if not df_students.empty:
        with st.container(border=True):
            fcol1, fcol2, fcol3 = st.columns([2, 1, 1])
            with fcol1:
                search_stu = st.text_input("🔍 Быстрый поиск ученика по ФИО или договору:", key="search_stu")
            with fcol2:
                status_opt = st.selectbox("Статус квалификации:", ["Все ученики", "Только с разрядами", "Без разряда (обучаются)"], key="status_opt")
            with fcol3:
                all_branches = ["Все филиалы"] + sorted(list(set(b for b in df_students["branch"].dropna() if b)))
                branch_opt = st.selectbox("Локация / Филиал:", all_branches, key="branch_opt")
            
        stu_filtered = df_students.copy()
        if search_stu:
            mask = (
                stu_filtered["fio"].str.contains(search_stu, case=False, na=False) | 
                stu_filtered["contract"].str.contains(search_stu, case=False, na=False)
            )
            stu_filtered = stu_filtered[mask]
            
        if status_opt == "Только с разрядами":
            stu_filtered = stu_filtered[stu_filtered["has_rank"] == True]
        elif status_opt == "Без разряда (обучаются)":
            stu_filtered = stu_filtered[stu_filtered["has_rank"] == False]
            
        if branch_opt != "Все филиалы":
            stu_filtered = stu_filtered[stu_filtered["branch"] == branch_opt]
            
        stu_display = stu_filtered.copy()
        stu_display["status_label"] = stu_display["has_rank"].apply(lambda x: "🏆 Аттестован" if x else "⏳ Обучается")
        stu_display["ranks_label"] = stu_display["ranks"].apply(lambda r: ", ".join(r) if r else "-")
        
        s_renames = {
            "fio": "ФИО ученика",
            "birth_date": "Дата рождения",
            "branch": "Филиал / Занятия",
            "contract": "№ Договора",
            "status_label": "Статус",
            "ranks_label": "Присвоенные разряды",
            "notes": "Примечания"
        }
        stu_table_df = stu_display[list(s_renames.keys())].rename(columns=s_renames)
        
        with st.expander("⚙️ Настройка столбцов учеников (скрыть / показать)", expanded=False):
            sb1, sb2, sb3 = st.columns(3)
            sb1.button("Все столбцы учеников", key="stu_btn_all", on_click=set_student_cols, args=(list(ALL_STUDENT_COLS.keys()),))
            sb2.button("Кратко (ФИО + Статус + Разряд)", key="stu_btn_brief", on_click=set_student_cols, args=(["ФИО ученика", "Статус", "Присвоенные разряды"],))
            sb3.button("Контакты и филиал", key="stu_btn_contacts", on_click=set_student_cols, args=(["ФИО ученика", "Дата рождения", "Филиал / Занятия", "№ Договора"],))
                
            selected_student_cols = st.multiselect(
                "Отображаемые столбцы учеников (удаляйте крестиком ✕):",
                options=list(ALL_STUDENT_COLS.keys()),
                key="selected_student_cols"
            )
            
        active_s_cols = [c for c in selected_student_cols if c in stu_table_df.columns]
        if active_s_cols:
            st.dataframe(
                stu_table_df[active_s_cols],
                width='stretch',
                hide_index=True,
                height=500,
                column_config={
                    "ФИО ученика": st.column_config.TextColumn(width="medium"),
                    "Статус": st.column_config.TextColumn(width="medium"),
                    "Присвоенные разряды": st.column_config.TextColumn(width="large")
                }
            )
        else:
            st.warning("⚠️ Все столбцы таблицы учеников скрыты. Выберите столбцы выше.")
    else:
        st.info("Данные по ученикам не найдены.")

# TAB 3: ORDERS & PHOTO PREVIEWS
ALL_ORDER_COLS = {
    "ФИО": "fio",
    "Год": "birth_year",
    "Разряд": "rank",
    "Дисциплина": "discipline",
    "Результат": "place",
    "Примечание": "notes"
}

if "selected_order_cols" not in st.session_state:
    st.session_state["selected_order_cols"] = list(ALL_ORDER_COLS.keys())

with tab_orders:
    col_o_head1, col_o_head2 = st.columns([3, 1])
    with col_o_head1:
        st.markdown("#### Официальные приказы ведомств и федерации")
    with col_o_head2:
        expand_photo = st.toggle("🖼️ Фото на весь экран", value=False, key="toggle_expand_photo")
    
    order_options = []
    for idx, row in df_orders.iterrows():
        order_options.append(f"{row['num']} от {row['date']} • {row['org']} ({row['city']})")
    
    selected_order_idx = st.selectbox(
        "Выберите документ для подробного просмотра:",
        options=range(len(order_options)),
        format_func=lambda i: order_options[i]
    )
    
    cur_order = df_orders.iloc[selected_order_idx]
    
    photo_files = [f.strip() for f in str(cur_order["file"]).split(",")]
    img_path = None
    for pfile in photo_files:
        matches = [f for f in os.listdir(PHOTOS_DIR) if cur_order["num"].replace("№", "").strip() in f or cur_order["date"] in f] if os.path.exists(PHOTOS_DIR) else []
        if matches:
            img_path = os.path.join(PHOTOS_DIR, matches[0])
            break
        elif os.path.exists(os.path.join(BASE_DIR, pfile)):
            img_path = os.path.join(BASE_DIR, pfile)
            break
        elif os.path.exists(os.path.join(PHOTOS_DIR, pfile)):
            img_path = os.path.join(PHOTOS_DIR, pfile)
            break
            
    athletes_in_order = df_athletes[
        (df_athletes["order_num"] == cur_order["num"]) & 
        (df_athletes["order_date"] == cur_order["date"])
    ]
    
    if not expand_photo:
        col_info, col_img = st.columns([1, 1], gap="medium")
        
        with col_info:
            with st.container(border=True):
                st.markdown(f"### {cur_order['num']}")
                st.markdown(f"**Орган власти / Федерация:** {cur_order['org']}")
                st.markdown(f"**Дата приказа:** {cur_order['date']}")
                st.markdown(f"**Город / Район:** {cur_order['city']}")
                st.markdown(f"**Предмет приказа:** {cur_order['subj']}")
                st.markdown(f"**Количество спортсменов:** {cur_order['count']} чел.")
            
            st.markdown("##### 👥 Спортсмены, вошедшие в данный приказ:")
            
            with st.expander("⚙️ Настроить столбцы списка приказа", expanded=False):
                selected_order_cols = st.multiselect(
                    "Столбцы (удаляйте крестиком ✕):",
                    options=list(ALL_ORDER_COLS.keys()),
                    key="selected_order_cols"
                )
            
            sub_table = athletes_in_order[["fio", "birth_year", "rank", "discipline", "place", "notes"]].rename(columns={
                "fio": "ФИО",
                "birth_year": "Год",
                "rank": "Разряд",
                "discipline": "Дисциплина",
                "place": "Результат",
                "notes": "Примечание"
            })
            
            active_o_cols = [c for c in selected_order_cols if c in sub_table.columns]
            if active_o_cols:
                st.dataframe(sub_table[active_o_cols], width='stretch', hide_index=True)
            else:
                st.warning("⚠️ Все столбцы списка скрыты. Выберите столбцы выше.")
            
        with col_img:
            st.markdown("##### 📷 Фотокопия оригинала документа:")
            if img_path and os.path.exists(img_path):
                with st.container(border=True):
                    st.image(img_path, caption=f"Оригинал: {cur_order['num']}", width='stretch')
            else:
                st.info(f"Файл фото: `{cur_order['file']}`.")
    else:
        # Full width photo mode when requested!
        with st.container(border=True):
            ci1, ci2, ci3, ci4 = st.columns(4)
            ci1.metric("Номер приказа", cur_order['num'])
            ci2.metric("Дата", cur_order['date'])
            ci3.metric("Город", cur_order['city'])
            ci4.metric("Спортсменов", f"{cur_order['count']} чел.")
            st.caption(f"**Орган / Федерация:** {cur_order['org']} • **Предмет:** {cur_order['subj']}")
        
        st.markdown("##### 📷 Фотокопия оригинала документа (полноэкранный режим):")
        if img_path and os.path.exists(img_path):
            with st.container(border=True):
                st.image(img_path, caption=f"Оригинал: {cur_order['num']}", width='stretch')
        else:
            st.info(f"Файл фото: `{cur_order['file']}`.")

# TAB 4: ANALYTICS (DARK PLOTLY)
with tab_stats:
    st.markdown("#### Аналитический обзор квалификаций")
    
    col_chart1, col_chart2 = st.columns(2, gap="medium")
    
    with col_chart1:
        with st.container(border=True):
            rank_only = df_athletes[df_athletes["rank"] != "Без разряда"]
            rank_counts = rank_only["rank"].value_counts().reset_index()
            rank_counts.columns = ["Разряд", "Количество"]
            fig1 = px.bar(
                rank_counts,
                x="Разряд",
                y="Количество",
                color="Разряд",
                title="<b>Распределение присвоенных разрядов</b>",
                text="Количество",
                template="plotly_dark",
                color_discrete_sequence=['#3B82F6', '#6366F1', '#F59E0B', '#10B981', '#8B5CF6']
            )
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                margin=dict(t=40, b=20, l=20, r=20),
                font=dict(family="Plus Jakarta Sans", color="#E2E8F0")
            )
            st.plotly_chart(fig1, width='stretch')
        
    with col_chart2:
        with st.container(border=True):
            if not df_students.empty:
                branch_data = df_students["branch"].apply(lambda b: "Аксай" if "аксай" in str(b).lower() else ("Пушкинская" if "пушкинская" in str(b).lower() else "Другое"))
                b_counts = branch_data.value_counts().reset_index()
                b_counts.columns = ["Филиал", "Учеников"]
                fig2 = px.pie(
                    b_counts,
                    names="Филиал",
                    values="Учеников",
                    title="<b>Распределение учеников Академии по филиалам</b>",
                    hole=0.5,
                    template="plotly_dark",
                    color_discrete_sequence=['#2563EB', '#0D9488', '#F59E0B']
                )
                fig2.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=40, b=20, l=20, r=20),
                    font=dict(family="Plus Jakarta Sans", color="#E2E8F0")
                )
                st.plotly_chart(fig2, width='stretch')
            else:
                city_counts = df_athletes["city"].value_counts().reset_index()
                city_counts.columns = ["Город", "Количество"]
                fig2 = px.pie(city_counts, names="Город", values="Количество", title="<b>Распределение по городам</b>", template="plotly_dark")
                st.plotly_chart(fig2, width='stretch')
        
    # Age distribution
    with st.container(border=True):
        valid_years = df_athletes[df_athletes["birth_year"] != ""]["birth_year"].dropna().astype(int)
        valid_years = valid_years[valid_years >= 1975]
        if not valid_years.empty:
            year_counts = valid_years.value_counts().sort_index().reset_index()
            year_counts.columns = ["Год рождения", "Количество"]
            fig3 = px.bar(
                year_counts,
                x="Год рождения",
                y="Количество",
                title="<b>Возрастной состав: распределение по годам рождения</b>",
                text="Количество",
                template="plotly_dark",
                color_discrete_sequence=['#6366F1']
            )
            fig3.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=40, b=20, l=20, r=20),
                font=dict(family="Plus Jakarta Sans", color="#E2E8F0")
            )
            st.plotly_chart(fig3, width='stretch')

# TAB 5: ATHLETE / STUDENT DOSSIER
with tab_athlete:
    st.markdown("#### Персональная карточка спортсмена / ученика")
    
    all_names = sorted(df_athletes["fio"].unique().tolist())
    default_idx = all_names.index("Хлыбов Василий Васильевич") if "Хлыбов Василий Васильевич" in all_names else 0
    selected_person = st.selectbox("Выберите пилота из списка:", options=all_names, index=default_idx)
    
    if selected_person:
        records = df_athletes[df_athletes["fio"] == selected_person]
        first_r = records.iloc[0]
        initials = get_initials(selected_person)
        
        ranks_records = records[records["rank"] != "Без разряда"]
        best_rec = get_highest_rank_record(ranks_records)
        highest_rank = best_rec["rank"] if best_rec is not None else "Обучается в Академии"
        pill_class = "rank-pill-sport" if ("спортивный" in highest_rank.lower() or highest_rank in ["КМС", "МС", "МСМК"]) else ("rank-pill-junior" if "юношеский" in highest_rank.lower() else "rank-pill-none")
        
        # Profile Header Card Dark
        st.markdown(f"""
        <div class="profile-card">
            <div style="display: flex; align-items: center; gap: 20px;">
                <div class="avatar-circle">{initials}</div>
                <div>
                    <h2 style="margin: 0; font-size: 1.55rem; font-weight: 800; color: #F8FAFC;">{selected_person}</h2>
                    <div style="margin-top: 8px;">
                        <span class="rank-pill {pill_class}">🏆 {highest_rank}</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Metadata metrics
        m1, m2, m3, m4 = st.columns(4)
        b_val = first_r.get("birth_date") or first_r.get("birth_year") or "Не указана"
        br_val = first_r.get("student_branch") or first_r.get("club") or "АтмоС"
        c_val = first_r.get("student_contract") or "Не указан"
        
        with m1:
            st.metric("Дата / Год рождения", str(b_val))
        with m2:
            st.metric("Локация / Филиал", str(br_val))
        with m3:
            st.metric("Номер договора", str(c_val))
        with m4:
            st.metric("Всего присвоений", len(ranks_records))
            
        st.write("")
        
        # History
        if not ranks_records.empty:
            st.markdown("##### 📜 Хронология присвоения спортивных разрядов:")
            hist_sorted = ranks_records.copy()
            hist_sorted["parsed_date"] = pd.to_datetime(hist_sorted["order_date"], format="%d.%m.%Y", errors="coerce")
            hist_sorted = hist_sorted.sort_values(by="parsed_date", ascending=False)
            for idx, r in hist_sorted.iterrows():
                place_str = f" ({r['place']})" if r['place'] else ""
                notes_str = f" • *{r['notes']}*" if r['notes'] else ""
                club_str = f" • {r['club']}" if r['club'] else ""
                
                st.markdown(f"""
                <div class="timeline-item">
                    <div style="font-size: 0.82rem; font-weight: 600; color: #94A3B8;">{r['order_date']}</div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #F1F5F9; margin-top: 2px;">
                        {r['rank']} <span style="font-size: 0.8rem; font-weight: 500; color: #94A3B8;">({r['rank_type']})</span>
                    </div>
                    <div style="font-size: 0.88rem; color: #CBD5E1; margin-top: 4px;">
                        📄 <b>Приказ:</b> {r['order_num']} от {r['order_date']} ({r['org']}, {r['city']})
                    </div>
                    <div style="font-size: 0.88rem; color: #94A3B8; margin-top: 2px;">
                        🎯 <b>Дисциплина / Результат:</b> {r['discipline']}{place_str}{club_str}{notes_str}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            with st.container(border=True):
                st.info("ℹ️ У данного ученика пока нет присвоенных официальных спортивных разрядов. Он проходит программу подготовки в Академии пилотов.")

# TAB 6: UPLOAD AND ADD ORDERS & RANKS
with tab_upload:
    st.markdown("#### 📥 Внесение официального приказа и присвоения разрядов")
    st.caption("Заполните реквизиты приказа, прикрепите скан или фото документа и укажите спортсменов. Данные сразу сохраняются в базу реестра и могут быть выгружены на GitHub.")
    
    # 1. ORDER METADATA
    with st.container(border=True):
        st.markdown("##### 1️⃣ Реквизиты приказа / документа")
        col_u1, col_u2, col_u3 = st.columns([1, 1, 1])
        with col_u1:
            in_order_num = st.text_input("Номер приказа *", placeholder="например: № 16-ФГДРО или № 125-ПСР", key="in_order_num")
        with col_u2:
            in_order_date = st.date_input("Дата приказа *", format="DD.MM.YYYY", key="in_order_date")
        with col_u3:
            city_suggestions = ["г. Ростов-на-Дону", "г. Батайск", "г. Азов", "г. Новочеркасск", "Аксайский район", "г. Таганрог", "г. Шахты"]
            in_city = st.selectbox("Город / Муниципалитет *", options=city_suggestions + ["Другой (ввести вручную)"], key="in_city")
            if in_city == "Другой (ввести вручную)":
                in_city = st.text_input("Введите город / район:", value="г. Ростов-на-Дону", key="in_city_custom")
                
        col_u4, col_u5 = st.columns([1, 1])
        with col_u4:
            org_suggestions = [
                "РФСОО «Федерация гонок дронов Ростовской области»",
                "УФКС г. Ростова-на-Дону",
                "Отдел по ФКСиТ Администрации Аксайского района",
                "Отдел по ФК и спорту Администрации г. Азова",
                "УФКС Администрации г. Новочеркасска",
                "ДОСААФ"
            ]
            in_org = st.selectbox("Орган власти / Федерация *", options=org_suggestions + ["Другая организация (ввести вручную)"], key="in_org")
            if in_org == "Другая организация (ввести вручную)":
                in_org = st.text_input("Введите наименование органа / федерации:", key="in_org_custom")
        with col_u5:
            in_subj = st.text_input("Предмет приказа / основание", value="Присвоение спортивных / юношеских разрядов по гонкам дронов", key="in_subj")
            
        col_u6, col_u7 = st.columns([1, 1])
        with col_u6:
            disc_suggestions = ["Гонки дронов", "Гонки дронов (класс 75 мм)", "Гонки дронов (класс 200 мм)", "Технический симулятор — гонки БВС"]
            in_disc = st.selectbox("Дисциплина (по умолчанию для всех)", options=disc_suggestions + ["Другая"], key="in_disc")
            if in_disc == "Другая":
                in_disc = st.text_input("Введите дисциплину:", value="Гонки дронов", key="in_disc_custom")
        with col_u7:
            in_base_place = st.text_input("Основание / результат (по умолчанию)", value="Выполнение нормы ЕВСК", key="in_base_place")

    # 2. SCAN / PHOTO UPLOAD
    with st.container(border=True):
        st.markdown("##### 2️⃣ Фотокопия или скриншот документа")
        uploaded_doc = st.file_uploader(
            "Загрузите фотокопию или скриншот приказа (JPG, PNG, PDF):",
            type=["jpg", "jpeg", "png", "webp", "pdf"],
            help="Файл будет сохранен в каталог photos/ и привязан к приказу.",
            key="uploaded_doc"
        )
        if uploaded_doc is not None:
            col_preview1, col_preview2 = st.columns([1, 2])
            with col_preview1:
                if uploaded_doc.type.startswith("image/"):
                    st.image(uploaded_doc, caption=f"Предпросмотр: {uploaded_doc.name}", width='stretch')
                else:
                    st.info(f"📄 Загружен документ: **{uploaded_doc.name}** ({round(uploaded_doc.size / 1024, 1)} КБ)")
            with col_preview2:
                st.success(f"Файл готов к сохранению. Будет прикреплен к приказу {in_order_num or 'б/н'}.")

    # 3. ATHLETES LIST (TEXT PARSER & DATA EDITOR)
    with st.container(border=True):
        st.markdown("##### 3️⃣ Список спортсменов и присваиваемых разрядов")
        st.caption("Вы можете быстро вставить список текстом или отредактировать таблицу ниже. При совпадении с базой учеников дата рождения, филиал и договор подтянутся автоматически.")
        
        tab_input_text, tab_input_table = st.tabs(["📝 Быстрый ввод текстом списком", "📊 Таблица спортсменов"])
        
        # Init session state list of athletes
        if "order_athletes_list" not in st.session_state:
            st.session_state["order_athletes_list"] = [
                {"ФИО": "", "Разряд": "1 юношеский разряд", "Дата рождения": "", "Филиал": "", "Договор": "", "Примечания": ""}
            ]
            
        with tab_input_text:
            text_placeholder = (
                "# Вставьте список спортсменов по одной строке.\n"
                "# Формат строки: ФИО | Разряд | Дата или Год рождения (необязательно)\n"
                "# Примеры:\n"
                "Аристархова Эвелина Игоревна | 3 спортивный разряд\n"
                "Изюмов Кирилл Андреевич | 3 спортивный разряд\n"
                "Моргунова Мария Александровна | 1 юношеский разряд | 16.03.2015\n"
            )
            raw_text = st.text_area("Вставьте текст со списком:", height=150, placeholder=text_placeholder, key="raw_athletes_text")
            if st.button("📋 Разобрать список и заполнить в таблицу", key="btn_parse_text"):
                if raw_text.strip():
                    parsed_rows = []
                    # Create student lookup dict for quick auto-fill
                    stu_lookup = {}
                    if not df_students.empty:
                        for _, s_row in df_students.iterrows():
                            clean_f = " ".join(str(s_row["fio"]).strip().split()).lower()
                            stu_lookup[clean_f] = s_row
                            
                    lines = [line.strip() for line in raw_text.strip().split("\n") if line.strip() and not line.strip().startswith("#")]
                    for line in lines:
                        parts = [p.strip() for p in line.replace(";", "|").replace("\t", "|").split("|")]
                        fio_val = parts[0] if len(parts) > 0 else ""
                        rank_val = parts[1] if len(parts) > 1 else "1 юношеский разряд"
                        birth_val = parts[2] if len(parts) > 2 else ""
                        
                        branch_val = ""
                        contract_val = ""
                        
                        # Match with student DB
                        lookup_key = " ".join(fio_val.split()).lower()
                        if lookup_key in stu_lookup:
                            matched_s = stu_lookup[lookup_key]
                            if not birth_val:
                                birth_val = str(matched_s.get("birth_date") or matched_s.get("birth_year") or "")
                            branch_val = str(matched_s.get("branch") or "")
                            contract_val = str(matched_s.get("contract") or "")
                            
                        parsed_rows.append({
                            "ФИО": fio_val,
                            "Разряд": rank_val,
                            "Дата рождения": birth_val,
                            "Филиал": branch_val,
                            "Договор": contract_val,
                            "Примечания": ""
                        })
                    if parsed_rows:
                        st.session_state["order_athletes_list"] = parsed_rows
                        st.success(f"Успешно распознано {len(parsed_rows)} спортсменов! Перейдите на вкладку «Таблица спортсменов» для проверки.")
                        st.rerun()

        with tab_input_table:
            st.caption("Здесь можно отредактировать строки, изменить разряды или добавить новых участников:")
            all_known_ranks = [
                "3 спортивный разряд",
                "2 спортивный разряд",
                "1 спортивный разряд",
                "КМС",
                "МС",
                "1 юношеский разряд",
                "2 юношеский разряд",
                "3 юношеский разряд"
            ]
            
            df_editor_input = pd.DataFrame(st.session_state["order_athletes_list"])
            
            edited_athletes_df = st.data_editor(
                df_editor_input,
                num_rows="dynamic",
                width='stretch',
                column_config={
                    "ФИО": st.column_config.TextColumn("ФИО спортсмена *", width="large", required=True),
                    "Разряд": st.column_config.SelectboxColumn("Присваиваемый разряд *", options=all_known_ranks, required=True, width="medium"),
                    "Дата рождения": st.column_config.TextColumn("Дата / Год рождения", width="medium"),
                    "Филиал": st.column_config.TextColumn("Филиал / Клуб", width="medium"),
                    "Договор": st.column_config.TextColumn("№ Договора", width="small"),
                    "Примечания": st.column_config.TextColumn("Примечание", width="medium"),
                },
                key="editor_athletes"
            )

    # 4. SAVE & GIT PUSH
    with st.container(border=True):
        st.markdown("##### 4️⃣ Сохранение в реестр и выгрузка на GitHub")
        
        auto_push = st.checkbox("🚀 Автоматически выгрузить на GitHub (git push origin main) после сохранения", value=True, key="auto_push_cb")
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            btn_save = st.button("💾 СОХРАНИТЬ ПРИКАЗ И РАЗРЯДЫ", type="primary", width='stretch', key="btn_save_order")
        with col_btn2:
            btn_push_only = st.button("🔄 Выполнить Git Push текущего состояния", width='stretch', key="btn_push_only")
            
        if btn_push_only:
            with st.spinner("Синхронизация с GitHub..."):
                ok, msg = run_git_sync(BASE_DIR)
                if ok:
                    st.success(f"✅ Синхронизация с GitHub успешно выполнена!\n\n`{msg}`")
                else:
                    st.error(f"❌ Ошибка синхронизации с GitHub:\n\n`{msg}`")
                    
        if btn_save:
            # Validation
            if not in_order_num.strip():
                st.error("Пожалуйста, укажите номер приказа (например, № 16-ФГДРО)!")
            else:
                # Filter valid athlete rows
                valid_athletes = []
                for _, r in edited_athletes_df.iterrows():
                    fio_str = str(r.get("ФИО", "")).strip()
                    if fio_str and fio_str.lower() != "nan":
                        valid_athletes.append(r)
                        
                if not valid_athletes:
                    st.error("Пожалуйста, добавьте хотя бы одного спортсмена в таблицу!")
                else:
                    with st.spinner("Сохранение приказа и разрядов в реестр..."):
                        date_str = in_order_date.strftime("%d.%m.%Y")
                        
                        # Save photo if uploaded
                        saved_photo_name = "—"
                        if uploaded_doc is not None:
                            ext = os.path.splitext(uploaded_doc.name)[1].lower() or ".jpg"
                            safe_num = "".join(c for c in in_order_num if c.isalnum() or c in "-_").strip()
                            safe_city = in_city.replace("г. ", "").replace(" ", "_")
                            safe_filename = f"Приказ_{safe_num}_{safe_city}_{date_str}{ext}"
                            photo_dest = os.path.join(PHOTOS_DIR, safe_filename)
                            os.makedirs(PHOTOS_DIR, exist_ok=True)
                            with open(photo_dest, "wb") as f_out:
                                f_out.write(uploaded_doc.getbuffer())
                            saved_photo_name = safe_filename
                            
                        # Load current json
                        with open(JSON_FILE, "r", encoding="utf-8") as f_j:
                            current_data = json.load(f_j)
                            
                        # 1. Add order
                        new_order_entry = {
                            "org": in_org.strip(),
                            "num": in_order_num.strip(),
                            "date": date_str,
                            "city": in_city.strip(),
                            "subj": in_subj.strip(),
                            "count": len(valid_athletes),
                            "file": saved_photo_name
                        }
                        # Prepend new order
                        current_data["orders"].insert(0, new_order_entry)
                        
                        # 2. Add athletes
                        # Build lookup map for existing students to update
                        stu_map = {s["fio"].strip().lower(): s for s in current_data.get("students", [])}
                        
                        new_athletes_entries = []
                        for row_a in valid_athletes:
                            a_fio = str(row_a["ФИО"]).strip()
                            a_rank = str(row_a["Разряд"]).strip()
                            a_bdate = str(row_a.get("Дата рождения", "")).strip()
                            a_branch = str(row_a.get("Филиал", "")).strip()
                            a_contract = str(row_a.get("Договор", "")).strip()
                            a_notes = str(row_a.get("Примечания", "")).strip()
                            
                            # Parse year
                            b_year = None
                            if a_bdate:
                                try:
                                    if len(a_bdate) == 4 and a_bdate.isdigit():
                                        b_year = int(a_bdate)
                                    elif "." in a_bdate:
                                        b_year = int(a_bdate.split(".")[-1])
                                except:
                                    pass
                                    
                            is_sport = "спортивный" in a_rank.lower() or a_rank in ["КМС", "МС", "МСМК"]
                            rank_type_str = "Спортивный" if is_sport else "Юношеский"
                            
                            # Update student record if found
                            f_lower = a_fio.lower()
                            if f_lower in stu_map:
                                stu = stu_map[f_lower]
                                stu["has_rank"] = True
                                if "ranks" not in stu:
                                    stu["ranks"] = []
                                if a_rank not in stu["ranks"]:
                                    stu["ranks"].append(a_rank)
                                if not a_bdate and stu.get("birth_date"):
                                    a_bdate = stu["birth_date"]
                                if not b_year and stu.get("birth_year"):
                                    b_year = stu["birth_year"]
                                if not a_branch and stu.get("branch"):
                                    a_branch = stu["branch"]
                                if not a_contract and stu.get("contract"):
                                    a_contract = stu["contract"]
                                    
                            ath_entry = {
                                "fio": a_fio,
                                "birth_year": b_year or "",
                                "rank": a_rank,
                                "rank_type": rank_type_str,
                                "order_num": in_order_num.strip(),
                                "order_date": date_str,
                                "org": in_org.strip(),
                                "city": in_city.strip(),
                                "competition": in_subj.strip(),
                                "discipline": in_disc.strip(),
                                "place": in_base_place.strip(),
                                "club": a_branch or "РФСОО «Федерация гонок дронов РО»",
                                "notes": a_notes,
                                "birth_date": a_bdate,
                                "student_branch": a_branch,
                                "student_contract": a_contract
                            }
                            new_athletes_entries.append(ath_entry)
                            
                        # Prepend new athletes to maintain latest on top
                        current_data["athletes"] = new_athletes_entries + current_data["athletes"]
                        
                        # Save all files (JSON, CSV, XLSX, MD)
                        save_registry_files(current_data, base_dir=BASE_DIR)
                        
                        # Git push if requested
                        git_status_msg = ""
                        if auto_push:
                            ok_git, g_msg = run_git_sync(BASE_DIR, commit_msg=f"feat: добавлен приказ {in_order_num} от {date_str} ({len(valid_athletes)} спортсменов)")
                            if ok_git:
                                git_status_msg = "🚀 Изменения успешно отправлены на GitHub! Streamlit Cloud автоматически обновит сайт через минуту."
                            else:
                                git_status_msg = f"⚠️ Данные сохранены локально, но при git push возникла ошибка: {g_msg}"
                                
                        # Clear cache and inform user
                        st.cache_data.clear()
                        st.session_state["order_athletes_list"] = [
                            {"ФИО": "", "Разряд": "1 юношеский разряд", "Дата рождения": "", "Филиал": "", "Договор": "", "Примечания": ""}
                        ]
                        st.success(f"🎉 Приказ **{in_order_num}** успешно внесен! Добавлено **{len(valid_athletes)}** спортсменов.\n\n{git_status_msg}")
                        st.button("🔄 Обновить страницу и увидеть данные в реестре", on_click=lambda: st.rerun())
