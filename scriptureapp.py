import streamlit as st
import pandas as pd
import calendar
import sqlite3
from pathlib import Path
from datetime import timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Taipei")
DB_FILE = "records.db"
OLD_CSV_FILE = Path("records.csv")
GOAL = 1000

# ============================================================
# 時間
# ============================================================

def now_tw():
    from datetime import datetime
    return datetime.now(TZ)

def today_tw():
    return now_tw().date()


# ============================================================
# 經文內容
# ============================================================

MANTRA = "離婆離婆帝。求訶求訶帝。陀羅尼帝。尼訶囉帝。毘黎你帝。摩訶伽帝。真陵乾帝。梭哈"

SCRIPTURE_GW = "奉請八大菩薩：\n南摩觀世音菩薩摩訶薩。\n南摩彌勒菩薩摩訶薩。\n南摩虛空藏菩薩摩訶薩。\n南摩普賢菩薩摩訶薩。\n南摩金剛手菩薩摩訶薩。\n南摩妙吉祥菩薩摩訶薩。\n南摩除蓋障菩薩摩訶薩。\n南摩地藏王菩薩摩訶薩。\n南摩諸尊菩薩摩訶薩。\n\n高王觀世音經\n觀世音菩薩。\n南摩佛。南摩法。南摩僧。\n佛國有緣。佛法相因。\n常樂我淨。有緣佛法。\n南摩摩訶般若波羅蜜。是大神咒。\n南摩摩訶般若波羅蜜。是大明咒。\n南摩摩訶般若波羅蜜。是無上咒。\n南摩摩訶般若波羅蜜。是無等等咒。\n南摩淨光祕密佛。法藏佛。獅子吼神足幽王佛。佛告須彌燈王佛。法護佛。金剛藏獅子遊戲佛。寶勝佛。神通佛。藥師琉璃光王佛。普光功德山王佛。善住功德寶王佛。\n過去七佛。未來賢劫千佛。千五百佛。萬五千佛。五百花勝佛。百億金剛藏佛。定光佛。\n六方六佛名號。\n東方寶光月殿月妙尊音王佛。\n南方樹根花王佛。\n西方皂王神通焰花王佛。\n北方月殿清淨佛。\n上方無數精進寶首佛。\n下方善寂月音王佛。\n無量諸佛。多寶佛。釋迦牟尼佛。彌勒佛。阿閦佛。彌陀佛。\n中央一切眾生。在佛世界中者。行住於地上。及在虛空中。慈憂於一切眾生。各令安穩休息。晝夜修持。心常求誦此經。能滅生死苦。消除諸毒害。\n南摩大明觀世音。觀明觀世音。高明觀世音。開明觀世音。藥王菩薩。藥上菩薩。文殊師利菩薩。普賢菩薩。虛空藏菩薩。地藏王菩薩。清涼寶山億萬菩薩。普光王如來化勝菩薩。\n\n念念誦此經。七佛世尊。即說咒曰：\n\n" + "\n".join([MANTRA] * 7) + "\n\n十方觀世音。一切諸菩薩。\n誓願救眾生。稱名悉解脫。\n若有智慧者。殷勤為解說。\n但是有因緣。讀誦口不輟。\n誦經滿千遍。念念心不絕。\n火焰不能傷。刀兵立摧折。\n恚怒生歡喜。死者變成活。\n莫言此是虛。諸佛不妄說。\n高王觀世音。能救諸苦厄。\n臨危急難中。死者變成活。\n諸佛語不虛。是故應頂禮。\n持誦滿千遍。重罪皆消滅。\n厚福堅信者。專攻受持經。\n願以此功德。普及於一切。\n誦滿一千遍。重罪皆消滅。\n\n高王觀世音經　終。"

DEDICATION_GW = "─── 迴向文 ───\n\n願以此（讀誦《高王觀音經》）功德，\n迴向給弟子（您的名字）的墮胎兒\n（若有名字可說名字，或稱「未結緣子女」）。\n\n願他業障消除、離苦得樂、\n求生西方極樂世界。\n\n弟子真心懺悔過去罪過，\n祈求佛菩薩慈悲加佑，\n解冤釋結，接引嬰靈。\n\n阿彌陀佛。\n\n（念誦三遍）"

SCRIPTURE_CH = "懺悔三昧，每天念三遍，不要小看。\n\n無論是過去，現在，或是未來。\n\n因身，口，意的造作，\n被我傷害過的（因緣）眾生。\n\n或因身，口，意的造作，\n所招感的諸多不順和苦難。\n\n不管是身體上的，還是精神上的。\n\n我都願意接受（業果法則）。\n\n並慚愧的懺悔。\n\n因為無明，因未聞四種真諦，\n無量劫來，我們彼此傷害，冤冤相報，\n枉受諸苦於六道中，無有出期。\n\n我們都希望解脫。\n\n願一切被我傷害過的眾生，\n無精神的痛苦，無身體的痛苦，\n願你們保持快樂。\n\n願一切與我有因緣的鬼道，非人眾生，\n得聞佛法，投生善道，趨向解脫。\n\n願一切與我有因緣的人或非人眾生，\n分享我善業的功德，\n並回答；善哉！善哉！善哉！\n\n願一切眾生分享我的功德。"

DEDICATION_CH = "─── 迴向文 ───\n\n弟子（或信士）○○○願以此（讀誦《懺悔三昧》）之功德，\n迴向給弟子累生累世的冤親債主、歷代宗親。\n\n祈請（主尊，如：南無大慈大悲觀世音菩薩 / 地藏王菩薩）\n慈悲作主，超拔他們，\n令業障消除、離苦得樂、往生善處。\n\n願弟子與累世冤親債主解冤釋結、\n善緣增長，同生淨土。\n\n（念誦三遍）"

PRACTICES = {
    "高王觀世音經": {
        "icon": "🙏",
        "subtitle": "每日持誦　功課打卡",
        "scripture": SCRIPTURE_GW,
        "dedication": DEDICATION_GW,
        "c_accent": "#4A4585",
        "c_light": "#EDEAF5",
        "c_mid": "#C8C4E8",
        "dot_done": "dot-done-p",
        "dot_today": "dot-today-p",
        "btn_cls": "btn-p",
    },
    "懺悔三昧": {
        "icon": "🪷",
        "subtitle": "每日懺悔　修行打卡",
        "scripture": SCRIPTURE_CH,
        "dedication": DEDICATION_CH,
        "c_accent": "#0D9488",
        "c_light": "#E8FAF5",
        "c_mid": "#A7F3D0",
        "dot_done": "dot-done-t",
        "dot_today": "dot-today-t",
        "btn_cls": "btn-t",
    },
}


# ============================================================
# SQLite 備援資料庫
# ============================================================

def get_conn():
    conn = sqlite3.connect(DB_FILE, timeout=30, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn

def init_sqlite():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            日期 TEXT NOT NULL,
            時間 TEXT NOT NULL,
            經文 TEXT NOT NULL,
            次數 INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def load_sqlite():
    init_sqlite()
    conn = get_conn()
    df = pd.read_sql_query(
        "SELECT id, 日期, 時間, 經文, 次數 FROM records ORDER BY 日期 DESC, 時間 DESC, id DESC",
        conn,
    )
    conn.close()
    return normalize_df(df)

def add_sqlite(date_str, time_str, name, count):
    init_sqlite()
    conn = get_conn()
    conn.execute(
        "INSERT INTO records (日期, 時間, 經文, 次數) VALUES (?, ?, ?, ?)",
        (date_str, time_str, name, int(count)),
    )
    conn.commit()
    conn.close()

def delete_sqlite(record_id):
    init_sqlite()
    conn = get_conn()
    conn.execute("DELETE FROM records WHERE id = ?", (int(record_id),))
    conn.commit()
    conn.close()


# ============================================================
# Supabase 永久資料庫
# ============================================================

def supabase_enabled():
    return "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets

@st.cache_resource(ttl=300)
def get_supabase_client():
    from supabase import create_client
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def load_supabase():
    sb = get_supabase_client()
    result = (
        sb.table("records")
        .select("id,date,time,scripture,count")
        .order("date", desc=True)
        .order("time", desc=True)
        .order("id", desc=True)
        .execute()
    )

    rows = result.data or []
    if not rows:
        return pd.DataFrame(columns=["id", "日期", "時間", "經文", "次數"])

    df = pd.DataFrame(rows)
    df = df.rename(columns={
        "date": "日期",
        "time": "時間",
        "scripture": "經文",
        "count": "次數",
    })
    return normalize_df(df[["id", "日期", "時間", "經文", "次數"]])

def add_supabase(date_str, time_str, name, count):
    sb = get_supabase_client()
    sb.table("records").insert({
        "date": str(date_str),
        "time": str(time_str),
        "scripture": str(name),
        "count": int(count),
    }).execute()

def delete_supabase(record_id):
    sb = get_supabase_client()
    sb.table("records").delete().eq("id", int(record_id)).execute()


# ============================================================
# 統一資料層
# ============================================================

def normalize_df(df):
    if df is None or df.empty:
        return pd.DataFrame(columns=["id", "日期", "時間", "經文", "次數"])

    df = df.copy()
    for col in ["id", "日期", "時間", "經文", "次數"]:
        if col not in df.columns:
            df[col] = ""

    df["日期"] = df["日期"].astype(str).str.strip()
    df["時間"] = df["時間"].fillna("").astype(str).str.replace("nan", "", regex=False).str.strip()
    df["經文"] = df["經文"].astype(str).str.strip()
    df["次數"] = pd.to_numeric(df["次數"], errors="coerce").fillna(0).astype(int)
    df = df[df["次數"] > 0].copy()

    return df[["id", "日期", "時間", "經文", "次數"]]

def load_data():
    if supabase_enabled():
        try:
            return load_supabase()
        except Exception as e:
            st.warning(f"Supabase 讀取失敗，目前改用本機 SQLite 備援：{e}")
            return load_sqlite()
    return load_sqlite()

def add_record(date_str, time_str, name, count):
    if count <= 0:
        return

    if supabase_enabled():
        try:
            add_supabase(date_str, time_str, name, count)
            return
        except Exception as e:
            st.warning(f"Supabase 寫入失敗，暫時寫入本機 SQLite：{e}")

    add_sqlite(date_str, time_str, name, count)

def add_count(name, count):
    n = now_tw()
    add_record(str(today_tw()), n.strftime("%H:%M"), name, int(count))

def add_manual_record(date_str, name, count, time_str="08:00"):
    add_record(str(date_str), str(time_str or "08:00"), name, int(count))

def delete_row(record_id):
    if supabase_enabled():
        try:
            delete_supabase(record_id)
            return
        except Exception as e:
            st.warning(f"Supabase 刪除失敗，請稍後再試：{e}")
            return

    delete_sqlite(record_id)

def migrate_csv_to_sqlite_once():
    """如果舊 records.csv 存在，第一次啟動時自動匯入 SQLite 備援。"""
    init_sqlite()

    if not OLD_CSV_FILE.exists():
        return

    conn = get_conn()
    existing_count = conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]

    if existing_count > 0:
        conn.close()
        return

    try:
        df = pd.read_csv(OLD_CSV_FILE)
    except Exception:
        conn.close()
        return

    required_cols = ["日期", "經文", "次數"]
    if not all(col in df.columns for col in required_cols):
        conn.close()
        return

    if "時間" not in df.columns:
        df["時間"] = ""

    df = normalize_df(df)
    for _, row in df.iterrows():
        conn.execute(
            "INSERT INTO records (日期, 時間, 經文, 次數) VALUES (?, ?, ?, ?)",
            (row["日期"], row["時間"], row["經文"], int(row["次數"])),
        )

    conn.commit()
    conn.close()

def migrate_sqlite_to_supabase_once():
    """第一次設定好 Supabase 後，可按畫面按鈕把 SQLite 現有資料搬到 Supabase。"""
    if not supabase_enabled():
        return 0

    df_sqlite = load_sqlite()
    if df_sqlite.empty:
        return 0

    existing = load_supabase()

    count = 0
    for _, row in df_sqlite.iterrows():
        same = existing[
            (existing["日期"] == row["日期"])
            & (existing["時間"] == row["時間"])
            & (existing["經文"] == row["經文"])
            & (existing["次數"] == int(row["次數"]))
        ]

        if same.empty:
            add_supabase(row["日期"], row["時間"], row["經文"], int(row["次數"]))
            count += 1

    return count


# ============================================================
# 統計
# ============================================================

def today_count(name):
    df = load_data()
    if df.empty:
        return 0
    return int(df[(df["經文"] == name) & (df["日期"] == str(today_tw()))]["次數"].sum())

def total_count(name):
    df = load_data()
    if df.empty:
        return 0
    return int(df[df["經文"] == name]["次數"].sum())

def streak_days(name):
    df = load_data()
    if df.empty:
        return 0

    days = sorted(df[df["經文"] == name]["日期"].unique(), reverse=True)
    if not days:
        return 0

    count = 0
    check = today_tw()

    for d in days:
        if str(check) == d:
            count += 1
            check -= timedelta(days=1)
        elif d < str(check):
            break

    return count

def month_totals(name):
    df = load_data()
    today = today_tw()
    m = today.strftime("%Y-%m")
    df_m = df[(df["經文"] == name) & (df["日期"].str.startswith(m))]
    if df_m.empty:
        return {}
    return df_m.groupby("日期")["次數"].sum().to_dict()


# ============================================================
# 初始化
# ============================================================

init_sqlite()
migrate_csv_to_sqlite_once()

# 重要：這裡已移除 ensure_default_backfill_once()
# 不再自動補 2026-05-25 / 26 / 27 的假資料。


# ============================================================
# 畫面設定
# ============================================================

st.set_page_config(page_title="讀誦打卡", page_icon="🪷", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;500;600;700;900&family=Noto+Sans+TC:wght@300;400;500;700&display=swap');

html, body, [data-testid="stAppViewContainer"] { background: #F2EDE4 !important; }
.block-container { padding-top: 0 !important; padding-bottom: 3rem !important; max-width: 580px !important; }

* { box-sizing: border-box; }
body, p, div, span, label {
    font-family: 'Noto Sans TC', sans-serif !important;
    color: #3A2D24;
}

[data-testid="stTabs"] > div:first-child {
    position: sticky; top: 0; z-index: 999;
    background: #F2EDE4;
    padding: 12px 0 0;
    border-bottom: 1.5px solid #D9D0C4;
}

button[data-baseweb="tab"] {
    font-family: 'Noto Serif TC', serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #AFA196 !important;
    padding: 8px 20px !important;
    background: transparent !important;
    letter-spacing: .05em;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #5B3A8C !important;
    border-bottom: 2.5px solid #5B56A0 !important;
}

.page-header { text-align: center; padding: 32px 0 20px; }
.page-title {
    font-family: 'Noto Serif TC', serif;
    font-size: 28px; font-weight: 900;
    letter-spacing: .2em;
    color: #3A2D24;
    margin-bottom: 6px;
}
.page-title span { color: #4A4585; }
.page-date { font-size: 12px; color: #AFA196; letter-spacing: .1em; }

.pcard {
    background: #FFFEF9;
    border-radius: 20px;
    padding: 18px 20px;
    margin-bottom: 12px;
    border: 1px solid #E8E0D2;
    box-shadow: 0 4px 20px rgba(90,60,30,.08), 0 1px 4px rgba(90,60,30,.04);
    position: relative;
    overflow: hidden;
}
.pcard::before { content: ''; position: absolute; top:0; left:0; right:0; height: 3px; }
.pcard-p::before { background: linear-gradient(90deg, #4A4585, #8883C0, #4A4585); }
.pcard-t::before { background: linear-gradient(90deg, #0D9488, #34D399, #0D9488); }

.hero-wrap {
    display: flex; align-items: center; gap: 14px;
    padding-bottom: 14px;
    border-bottom: 1px solid #EDE5D8;
    margin-bottom: 14px;
}
.hero-icon-wrap {
    width: 52px; height: 52px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px; flex-shrink: 0;
}
.hero-name {
    font-family: 'Noto Serif TC', serif;
    font-size: 20px; font-weight: 900;
    letter-spacing: .1em; line-height: 1.2;
    margin-bottom: 3px;
}
.hero-sub { font-size: 11px; color: #AFA196; letter-spacing: .08em; }

.stat-row { display:flex; gap:8px; margin-bottom: 12px; }
.stat-chip {
    flex: 1;
    border-radius: 12px;
    padding: 10px 6px;
    text-align: center;
    border: 1px solid transparent;
}
.stat-num { font-family: 'Noto Serif TC', serif; font-size: 26px; font-weight: 700; line-height: 1; }
.stat-lbl { font-size: 11px; color: #AFA196; margin-top:4px; letter-spacing:.04em; }

.prog-meta {
    display:flex; justify-content:space-between;
    font-size: 11px; color: #AFA196;
    margin-bottom: 6px; letter-spacing:.03em;
}
.prog-track { height: 6px; background: #EDE5D8; border-radius: 3px; overflow: hidden; }
.prog-fill { height: 100%; border-radius: 3px; }

.cal-header {
    display: flex; justify-content: space-between; align-items: baseline;
    margin-bottom: 8px;
}
.cal-title {
    font-size: 11px; font-weight: 600;
    color: #AFA196; letter-spacing:.1em;
}
.cal-month { font-size: 11px; color: #C4B9AD; }
.dot-grid { display:flex; flex-wrap:wrap; gap:5px; }
.dot {
    width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 700;
}
.dot-empty   { background: #EDE5D8; color: #C4B9AD; }
.dot-done-p  { background: #4A4585; color: #F5F0FF; box-shadow: 0 2px 6px rgba(74,69,133,.35); }
.dot-done-t  { background: #0D9488; color: #ECFDF5; box-shadow: 0 2px 6px rgba(13,148,136,.3); }
.dot-today-p { background: #EDEAF5; color: #3D3880; border: 2px solid #5B56A0; font-weight:900; }
.dot-today-t { background: #D1FAF5; color: #0F766E; border: 2px solid #0D9488; font-weight:900; }

.scripture-box {
    background: #FDFAF5;
    border: 1px solid #E8E0D2;
    border-radius: 14px;
    padding: 18px 20px;
    white-space: pre-wrap;
    font-size: 15px;
    line-height: 1.75;
    color: #3A2D24;
    font-family: 'Noto Serif TC', serif;
    letter-spacing: .06em;
    margin-bottom: 10px;
}
.dedication-box {
    background: linear-gradient(160deg, #FFF8EE, #FEF0DC);
    border: 1px solid #EDD5A8;
    border-left: 3px solid #C4A87A;
    border-radius: 0 12px 12px 0;
    padding: 16px 18px;
    white-space: pre-wrap;
    font-size: 14px;
    line-height: 1.9;
    color: #5A3E20;
    font-family: 'Noto Serif TC', serif;
    letter-spacing: .06em;
    margin-bottom: 10px;
}

.sec-label {
    font-size: 11px; font-weight: 600; letter-spacing:.12em;
    color: #AFA196; text-transform: uppercase;
    margin-bottom: 10px;
}

.stButton > button, .stDownloadButton > button {
    font-family: 'Noto Sans TC', sans-serif !important;
    border: 1.5px solid #D9D0C4 !important;
    border-radius: 12px !important;
    min-height: 42px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    background: #FFFEF9 !important;
    color: #5A3E2B !important;
    width: 100% !important;
    letter-spacing: .04em !important;
}
.btn-p .stButton > button {
    background: linear-gradient(135deg, #4A4585, #332E6B) !important;
    border: none !important; color: #fff !important;
    height: 52px !important; font-size: 16px !important;
}
.btn-t .stButton > button {
    background: linear-gradient(135deg, #0D9488, #065F46) !important;
    border: none !important; color: #fff !important;
    height: 52px !important; font-size: 16px !important;
}
[data-testid="stNumberInput"] input {
    font-family: 'Noto Serif TC', serif !important;
    font-size: 22px !important; font-weight: 700 !important;
    background: #FDFAF5 !important;
    border: 1.5px solid #D9D0C4 !important;
    border-radius: 12px !important;
    color: #3A2D24 !important;
    text-align: center !important;
}
.rpill-row { display:flex; gap:8px; margin-bottom:10px; }
.rpill {
    flex:1; text-align:center;
    background: #F5EEE4;
    border: 1px solid #E2D9CE;
    border-radius: 10px;
    padding: 8px 4px;
}
.rpill-num { font-family:'Noto Serif TC',serif; font-size:20px; font-weight:700; }
.rpill-lbl { font-size:11px; color:#AFA196; margin-top:3px; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# Header
# ============================================================

today_obj = today_tw()
weekday_tw_map = ["一", "二", "三", "四", "五", "六", "日"]
weekday = weekday_tw_map[today_obj.weekday()]

st.markdown(f"""
<div class="page-header">
  <div class="page-title">🪷 讀誦<span>打卡</span></div>
  <div class="page-date">
    {today_obj.strftime("%Y 年 %m 月 %d 日")}　星期{weekday}　臺北時間
  </div>
</div>
""", unsafe_allow_html=True)

if supabase_enabled():
    st.success("✅ 目前使用 Supabase 永久儲存。")
    with st.expander("資料搬移工具"):
        st.caption("如果你本機 SQLite 還有舊資料，可以按一次搬到 Supabase。")
        if st.button("將 SQLite 舊資料搬到 Supabase"):
            n = migrate_sqlite_to_supabase_once()
            st.success(f"已搬移 {n} 筆資料到 Supabase。")
            st.rerun()
else:
    st.warning("⚠️ 目前尚未設定 Supabase，暫時使用本機 SQLite。Streamlit Cloud 重啟後資料仍可能消失。")


# ============================================================
# Main UI
# ============================================================

tabs = st.tabs(["🙏 高王觀世音經", "🪷 懺悔三昧"])

for i, (name, info) in enumerate(PRACTICES.items()):
    card_cls = "pcard pcard-t" if i == 1 else "pcard pcard-p"
    ac = info["c_accent"]
    lc = info["c_light"]

    with tabs[i]:
        t_count = today_count(name)
        a_count = total_count(name)
        s_days = streak_days(name)
        progress = min(a_count / GOAL, 1.0)

        st.markdown(f"""
        <div class="{card_cls}">
          <div class="hero-wrap">
            <div class="hero-icon-wrap" style="background:{lc}">
              <span>{info['icon']}</span>
            </div>
            <div>
              <div class="hero-name" style="color:{ac}">{name}</div>
              <div class="hero-sub">{info['subtitle']}</div>
            </div>
          </div>

          <div class="stat-row">
            <div class="stat-chip" style="background:{lc};border-color:{info['c_mid']}">
              <div class="stat-num" style="color:{ac}">{t_count}</div>
              <div class="stat-lbl">今日次數</div>
            </div>
            <div class="stat-chip" style="background:{lc};border-color:{info['c_mid']}">
              <div class="stat-num" style="color:{ac}">{a_count}</div>
              <div class="stat-lbl">累積次數</div>
            </div>
            <div class="stat-chip" style="background:{lc};border-color:{info['c_mid']}">
              <div class="stat-num" style="color:{ac}">{s_days}</div>
              <div class="stat-lbl">連續天數</div>
            </div>
          </div>

          <div class="prog-meta">
            <span>千遍目標進度</span>
            <span>{a_count} / {GOAL}　{round(progress * 100)}%</span>
          </div>
          <div class="prog-track">
            <div class="prog-fill" style="width:{round(progress * 100)}%;background:{ac}"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # 月曆
        mt = month_totals(name)
        days_in_month = calendar.monthrange(today_obj.year, today_obj.month)[1]
        dots = ""
        for d in range(1, days_in_month + 1):
            ds = f"{today_obj.year}-{today_obj.month:02d}-{d:02d}"
            cnt = int(mt.get(ds, 0))
            if d == today_obj.day:
                cls = info["dot_done"] if cnt > 0 else info["dot_today"]
            elif cnt > 0:
                cls = info["dot_done"]
            else:
                cls = "dot-empty"
            tip = f"title='{cnt}次'" if cnt > 0 else ""
            dots += f'<div class="dot {cls}" {tip}>{d}</div>'

        st.markdown(f"""
        <div class="pcard" style="padding:16px 18px">
          <div class="cal-header">
            <span class="cal-title">本月打卡紀錄</span>
            <span class="cal-month">{today_obj.strftime("%Y 年 %m 月")}</span>
          </div>
          <div class="dot-grid">{dots}</div>
        </div>
        """, unsafe_allow_html=True)

        # 經文
        scr_key = f"scr_{name}"
        if scr_key not in st.session_state:
            st.session_state[scr_key] = False

        if st.button("▲ 收起經文" if st.session_state[scr_key] else "▼ 展開經文", key=f"scr_btn_{name}"):
            st.session_state[scr_key] = not st.session_state[scr_key]
            st.rerun()

        if st.session_state[scr_key]:
            st.markdown(f'<div class="scripture-box">{info["scripture"]}</div>', unsafe_allow_html=True)

        # 今日打卡
        st.markdown('<div class="pcard" style="padding:16px 18px"><div class="sec-label">今日打卡</div>', unsafe_allow_html=True)

        ci1, ci2 = st.columns([1, 2])
        with ci1:
            count_val = st.number_input(
                "次數",
                min_value=0,
                max_value=999,
                value=0,
                step=1,
                key=f"ni_{name}",
                label_visibility="collapsed",
            )

        with ci2:
            st.markdown(f'<div class="{info["btn_cls"]}" style="margin-top:0">', unsafe_allow_html=True)
            if st.button(f"完成 {int(count_val)} 次　記錄", key=f"btn_{name}"):
                if count_val > 0:
                    add_count(name, int(count_val))
                    st.success(f"✅ 已記錄 {int(count_val)} 次")
                    st.rerun()
                else:
                    st.warning("請先輸入次數再記錄。")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # 補登紀錄
        st.markdown('<div class="pcard" style="padding:16px 18px"><div class="sec-label">補登紀錄</div>', unsafe_allow_html=True)

        m1, m2, m3 = st.columns([1.4, 1, 1])
        with m1:
            manual_date = st.date_input("補登日期", value=today_tw(), key=f"manual_date_{name}")
        with m2:
            manual_time = st.text_input("時間", value="08:00", key=f"manual_time_{name}")
        with m3:
            manual_count = st.number_input("補登次數", min_value=0, max_value=999, step=1, key=f"manual_count_{name}")

        if st.button("補登這筆紀錄", key=f"manual_btn_{name}"):
            if manual_count > 0:
                add_manual_record(str(manual_date), name, int(manual_count), manual_time)
                st.success(f"✅ 已補登 {manual_date}：{int(manual_count)} 次")
                st.rerun()
            else:
                st.warning("請輸入補登次數。")

        st.markdown("</div>", unsafe_allow_html=True)

        # 迴向文
        ded_key = f"ded_{name}"
        if ded_key not in st.session_state:
            st.session_state[ded_key] = False

        if st.button("▲ 收起迴向文" if st.session_state[ded_key] else "▼ 展開迴向文", key=f"ded_btn_{name}"):
            st.session_state[ded_key] = not st.session_state[ded_key]
            st.rerun()

        if st.session_state[ded_key]:
            st.markdown(f'<div class="dedication-box">{info["dedication"]}</div>', unsafe_allow_html=True)

        # 紀錄列表
        st.markdown('<div class="pcard" style="padding:16px 18px"><div class="sec-label">打卡紀錄</div>', unsafe_allow_html=True)

        df_all = load_data()
        df_this = df_all[df_all["經文"] == name].copy()

        if df_this.empty:
            st.markdown('<div style="font-size:13px;color:#AFA196;padding:4px 0">尚無記錄</div>', unsafe_allow_html=True)
        else:
            fc1, fc2 = st.columns(2)
            with fc1:
                all_months = sorted(df_this["日期"].str[:7].unique(), reverse=True)
                sel_month = st.selectbox("月份", ["全部"] + list(all_months), key=f"fm_{name}")
            with fc2:
                sel_date = st.date_input("指定日期", value=None, key=f"fd_{name}")

            df_show = df_this.copy()
            if sel_month != "全部":
                df_show = df_show[df_show["日期"].str.startswith(sel_month)]
            if sel_date:
                df_show = df_show[df_show["日期"] == str(sel_date)]

            df_show = df_show.sort_values(["日期", "時間", "id"], ascending=False).reset_index(drop=True)

            total_f = int(df_show["次數"].sum())
            st.markdown(f"""
            <div class="rpill-row">
              <div class="rpill">
                <div class="rpill-num" style="color:{ac}">{total_f}</div>
                <div class="rpill-lbl">總次數</div>
              </div>
              <div class="rpill">
                <div class="rpill-num" style="color:{ac}">{df_show["日期"].nunique()}</div>
                <div class="rpill-lbl">天數</div>
              </div>
              <div class="rpill">
                <div class="rpill-num" style="color:{ac}">{len(df_show)}</div>
                <div class="rpill-lbl">筆數</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            hc1, hc2, hc3, hc4 = st.columns([3, 2, 2, 1])
            hc1.markdown('<div style="font-size:12px;font-weight:600;color:#AFA196;padding:4px 0">日期</div>', unsafe_allow_html=True)
            hc2.markdown('<div style="font-size:12px;font-weight:600;color:#AFA196;padding:4px 0">時間</div>', unsafe_allow_html=True)
            hc3.markdown('<div style="font-size:12px;font-weight:600;color:#AFA196;padding:4px 0">次數</div>', unsafe_allow_html=True)
            hc4.markdown('<div style="font-size:12px;font-weight:600;color:#AFA196;padding:4px 0"></div>', unsafe_allow_html=True)
            st.markdown('<hr style="margin:2px 0 6px;border:none;border-top:1px solid #E8E0D2">', unsafe_allow_html=True)

            confirm_key = f"confirm_{name}"
            if confirm_key not in st.session_state:
                st.session_state[confirm_key] = None

            for _, row in df_show.iterrows():
                record_id = int(row["id"])
                rc1, rc2, rc3, rc4 = st.columns([3, 2, 2, 1])
                rc1.markdown(f'<div style="font-size:13px;padding:6px 0;color:#3A2D24">{row["日期"]}</div>', unsafe_allow_html=True)
                rc2.markdown(f'<div style="font-size:13px;padding:6px 0;color:#7A6050">{row["時間"] or "—"}</div>', unsafe_allow_html=True)
                rc3.markdown(f'<div style="font-size:13px;padding:6px 0;font-weight:600;color:{ac}">{int(row["次數"])}</div>', unsafe_allow_html=True)

                with rc4:
                    if st.session_state[confirm_key] == record_id:
                        if st.button("確刪", key=f"yes_{name}_{record_id}", help="確認刪除"):
                            delete_row(record_id)
                            st.session_state[confirm_key] = None
                            st.rerun()
                    else:
                        if st.button("🗑", key=f"del_{name}_{record_id}", help="刪除此筆"):
                            st.session_state[confirm_key] = record_id
                            st.rerun()

            export_df = df_show[["日期", "時間", "經文", "次數"]].copy()
            st.download_button(
                "⬇ 下載 CSV",
                export_df.to_csv(index=False, encoding="utf-8-sig"),
                file_name=f"{name}_打卡記錄_{today_tw()}.csv",
                mime="text/csv",
                use_container_width=True,
                key=f"dl_{name}",
            )

        st.markdown("</div>", unsafe_allow_html=True)
