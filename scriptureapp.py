import streamlit as st
import pandas as pd
import calendar
from pathlib import Path
from datetime import date, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Taipei")

def now_tw():
    from datetime import datetime
    return datetime.now(TZ)

def today_tw():
    return now_tw().date()

DATA_FILE = Path("records.csv")
GOAL = 1000

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
        "c_dark":   "#2E2960",
        "c_light":  "#EDEAF5",
        "c_mid":    "#C8C4E8",
        "c_text":   "#2E2960",
        "c_btn1":   "#4A4585",
        "c_btn2":   "#332E6B",
        "c_shadow": "rgba(74,69,133,.25)",
    },
    "懺悔三昧": {
        "icon": "🪷",
        "subtitle": "每日懺悔　修行打卡",
        "scripture": SCRIPTURE_CH,
        "dedication": DEDICATION_CH,
        "c_accent": "#0D9488",
        "c_dark":   "#065F46",
        "c_light":  "#E8FAF5",
        "c_mid":    "#A7F3D0",
        "c_text":   "#065F46",
        "c_btn1":   "#0D9488",
        "c_btn2":   "#065F46",
        "c_shadow": "rgba(13,148,136,.22)",
    },
}


# ── data ──────────────────────────────────────────────────────────

def load_data():
    if DATA_FILE.exists():
        df = pd.read_csv(DATA_FILE)
        if "時間" not in df.columns:
            df["時間"] = ""
        return df
    return pd.DataFrame(columns=["日期", "時間", "經文", "次數"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

def delete_row(orig_index: int):
    """刪除 CSV 中指定的原始行號（iloc index）"""
    df = load_data()
    df = df.drop(index=orig_index).reset_index(drop=True)
    save_data(df)

def add_count(name, count):
    if count <= 0:
        return
    df = load_data()
    n = now_tw()
    row = pd.DataFrame([{"日期": str(today_tw()), "時間": n.strftime("%H:%M"), "經文": name, "次數": int(count)}])
    df = pd.concat([df, row], ignore_index=True)
    save_data(df)

def today_count(name):
    df = load_data()
    if df.empty: return 0
    return int(df[(df["經文"] == name) & (df["日期"] == str(today_tw()))]["次數"].sum())

def total_count(name):
    df = load_data()
    if df.empty: return 0
    return int(df[df["經文"] == name]["次數"].sum())

def streak_days(name):
    df = load_data()
    if df.empty: return 0
    days = sorted(df[df["經文"] == name]["日期"].unique(), reverse=True)
    if not days: return 0
    count, check = 0, today_tw()
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
    if df_m.empty: return {}
    return df_m.groupby("日期")["次數"].sum().to_dict()


# ── CSS ───────────────────────────────────────────────────────────

st.set_page_config(page_title="讀誦打卡", page_icon="🪷", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;500;600;700;900&family=Noto+Sans+TC:wght@300;400;500;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #F2EDE4 !important;
}
[data-testid="stAppViewContainer"] > .main { background: transparent; }
.block-container {
    padding-top: 0 !important;
    padding-bottom: 3rem !important;
    max-width: 580px !important;
}

/* ─── tabs ─── */
[data-testid="stTabs"] { margin-top:0 !important; }
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
    background: transparent !important;
}
[data-testid="stTabPanel"] { padding-top: 0 !important; }

/* ─── global ─── */
* { box-sizing: border-box; }
body, p, div, span, label {
    font-family: 'Noto Sans TC', sans-serif !important;
    color: #3A2D24;
}

/* ─── page header ─── */
.page-header {
    text-align: center;
    padding: 32px 0 20px;
    position: relative;
}
.page-header::before {
    content: '';
    display: block;
    width: 60px; height: 2px;
    background: linear-gradient(90deg, transparent, #C4A87A, transparent);
    margin: 0 auto 16px;
}
.page-title {
    font-family: 'Noto Serif TC', serif;
    font-size: 28px; font-weight: 900;
    letter-spacing: .2em;
    color: #3A2D24;
    margin-bottom: 6px;
}
.page-title span { color: #4A4585; }
.page-date {
    font-size: 12px;
    color: #AFA196;
    letter-spacing: .1em;
    font-family: 'Noto Sans TC', sans-serif;
}
.page-header::after {
    content: '';
    display: block;
    width: 40px; height: 1px;
    background: linear-gradient(90deg, transparent, #C4A87A, transparent);
    margin: 12px auto 0;
}

/* ─── cards ─── */
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
.pcard::before {
    content: '';
    position: absolute; top:0; left:0; right:0;
    height: 3px;
}
.pcard-p::before { background: linear-gradient(90deg, #4A4585, #8883C0, #4A4585); }
.pcard-t::before { background: linear-gradient(90deg, #0D9488, #34D399, #0D9488); }

/* ─── hero ─── */
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
.hero-sub {
    font-size: 11px; color: #AFA196;
    letter-spacing: .08em;
}

/* ─── stat chips ─── */
.stat-row { display:flex; gap:8px; margin-bottom: 12px; }
.stat-chip {
    flex: 1;
    border-radius: 12px;
    padding: 10px 6px;
    text-align: center;
    border: 1px solid transparent;
}
.stat-num {
    font-family: 'Noto Serif TC', serif;
    font-size: 26px; font-weight: 700; line-height: 1;
}
.stat-lbl { font-size: 11px; color: #AFA196; margin-top:4px; letter-spacing:.04em; }

/* ─── progress ─── */
.prog-wrap { margin-bottom: 14px; }
.prog-meta {
    display:flex; justify-content:space-between;
    font-size: 11px; color: #AFA196;
    margin-bottom: 6px; letter-spacing:.03em;
}
.prog-track {
    height: 6px;
    background: #EDE5D8;
    border-radius: 3px;
    overflow: hidden;
}
.prog-fill { height: 100%; border-radius: 3px; }

/* ─── dot calendar ─── */
.cal-section { margin-bottom: 12px; }
.cal-header {
    display: flex; justify-content: space-between; align-items: baseline;
    margin-bottom: 8px;
}
.cal-title {
    font-size: 11px; font-weight: 600;
    color: #AFA196; letter-spacing:.1em; text-transform: uppercase;
    font-family: 'Noto Sans TC', sans-serif;
}
.cal-month { font-size: 11px; color: #C4B9AD; }
.dot-grid { display:flex; flex-wrap:wrap; gap:5px; }
.dot {
    width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 700;
    font-family: 'Noto Sans TC', sans-serif;
    transition: transform .1s;
}
.dot-empty   { background: #EDE5D8; color: #C4B9AD; }
.dot-done-p  { background: #4A4585; color: #F5F0FF; box-shadow: 0 2px 6px rgba(74,69,133,.35); }
.dot-done-t  { background: #0D9488; color: #ECFDF5; box-shadow: 0 2px 6px rgba(13,148,136,.3); }
.dot-today-p { background: #EDEAF5; color: #3D3880; border: 2px solid #5B56A0; font-weight:900; }
.dot-today-t { background: #D1FAF5; color: #0F766E; border: 2px solid #0D9488; font-weight:900; }

/* ─── scripture ─── */
.scripture-wrap { margin-bottom: 12px; }
.scripture-toggle {
    display: flex; align-items: center; gap: 8px;
    cursor: pointer;
    font-size: 13px; color: #AFA196;
    font-family: 'Noto Sans TC', sans-serif;
    padding: 8px 0;
    border: none; background: none;
    user-select: none;
    letter-spacing: .04em;
}
.scripture-toggle:hover { color: #7A6050; }
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
.dedication-header {
    display: flex; align-items: center; gap: 8px;
    margin-bottom: 12px;
}
.dedication-header-line { flex:1; height:1px; background:#EDD5A8; }
.dedication-header-text {
    font-size: 11px; font-weight: 600; color: #C4A87A;
    letter-spacing: .14em; white-space: nowrap;
    font-family: 'Noto Sans TC', sans-serif;
}

/* ─── checkin area ─── */
.checkin-section {
    border-top: 1px solid #EDE5D8;
    padding-top: 14px;
    margin-top: 2px;
}
.sec-label {
    font-size: 11px; font-weight: 600; letter-spacing:.12em;
    color: #AFA196; text-transform: uppercase;
    font-family: 'Noto Sans TC', sans-serif;
    margin-bottom: 10px;
}

/* ─── buttons ─── */
.stButton > button {
    font-family: 'Noto Sans TC', sans-serif !important;
    border: 1.5px solid #D9D0C4 !important;
    border-radius: 12px !important;
    height: 44px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    background: #FFFEF9 !important;
    color: #5A3E2B !important;
    transition: all .15s !important;
    width: 100% !important;
    letter-spacing: .04em !important;
}
.stButton > button:hover {
    background: #F5EEE4 !important;
    border-color: #C4B5A0 !important;
}
.btn-p .stButton > button {
    background: linear-gradient(135deg, #4A4585, #332E6B) !important;
    border: none !important; color: #fff !important;
    height: 52px !important; font-size: 16px !important;
    font-weight: 700 !important; letter-spacing: .08em !important;
    border-radius: 14px !important;
    box-shadow: 0 6px 22px rgba(74,69,133,.3) !important;
}
.btn-t .stButton > button {
    background: linear-gradient(135deg, #0D9488, #065F46) !important;
    border: none !important; color: #fff !important;
    height: 52px !important; font-size: 16px !important;
    font-weight: 700 !important; letter-spacing: .08em !important;
    border-radius: 14px !important;
    box-shadow: 0 6px 22px rgba(13,148,136,.28) !important;
}

/* ─── number input ─── */
[data-testid="stNumberInput"] input {
    font-family: 'Noto Serif TC', serif !important;
    font-size: 24px !important; font-weight: 700 !important;
    background: #FDFAF5 !important;
    border: 1.5px solid #D9D0C4 !important;
    border-radius: 12px !important;
    color: #3A2D24 !important;
    text-align: center !important;
}
[data-testid="stNumberInput"] button {
    background: #F0E8DC !important;
    border-radius: 8px !important;
    color: #7A6050 !important;
}

/* ─── success ─── */
[data-testid="stAlert"] {
    background: #F0FDF4 !important;
    border: 1px solid #86EFAC !important;
    border-radius: 12px !important;
    color: #14532D !important;
    font-family: 'Noto Sans TC', sans-serif !important;
}

/* ─── records section ─── */
.records-wrap {
    border-top: 1px dashed #D9D0C4;
    padding-top: 14px; margin-top: 4px;
}

/* ─── record stat pills ─── */
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

/* ─── dataframe ─── */
[data-testid="stDataFrame"] { border-radius:14px; overflow:hidden; }

/* ─── selectbox / date ─── */
[data-baseweb="select"] > div {
    background: #FDFAF5 !important;
    border-color: #D9D0C4 !important;
    border-radius: 10px !important;
    color: #3A2D24 !important;
    font-family: 'Noto Sans TC', sans-serif !important;
}
[data-testid="stDateInput"] input {
    background: #FDFAF5 !important;
    border-color: #D9D0C4 !important;
    border-radius: 10px !important;
    color: #3A2D24 !important;
}
[data-baseweb="select"] svg { color: #AFA196 !important; }

/* ─── download button ─── */
.dl-wrap .stDownloadButton > button {
    background: #F5EEE4 !important;
    border: 1px solid #D9D0C4 !important;
    border-radius: 10px !important;
    color: #7A6050 !important;
    font-size: 13px !important;
    height: 40px !important;
}

/* ─── expander: hide completely (using manual toggle instead) ─── */
[data-testid="stExpander"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)


# ── page header ───────────────────────────────────────────────────

today_obj = today_tw()
weekday_tw_map = ["一","二","三","四","五","六","日"]
weekday = weekday_tw_map[today_obj.weekday()]

st.markdown(f"""
<div class="page-header">
  <div class="page-title">🪷 讀誦<span>打卡</span></div>
  <div class="page-date">
    {today_obj.strftime("%Y 年 %m 月 %d 日")}　星期{weekday}　臺北時間
  </div>
</div>
""", unsafe_allow_html=True)


# ── tabs ──────────────────────────────────────────────────────────

tabs = st.tabs(["🙏 高王觀世音經", "🪷 懺悔三昧"])

for i, (name, info) in enumerate(PRACTICES.items()):
    is_teal     = i == 1
    card_cls    = "pcard pcard-t" if is_teal else "pcard pcard-p"
    dot_done    = "dot-done-t" if is_teal else "dot-done-p"
    dot_today_c = "dot-today-t" if is_teal else "dot-today-p"
    btn_cls     = "btn-t" if is_teal else "btn-p"
    ac          = info["c_accent"]
    lc          = info["c_light"]
    tc          = info["c_text"]

    with tabs[i]:

        # ── hero + stats + progress in one card ──
        t_count  = today_count(name)
        a_count  = total_count(name)
        s_days   = streak_days(name)
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

          <div class="prog-wrap">
            <div class="prog-meta">
              <span>千遍目標進度</span>
              <span>{a_count} / {GOAL}　{round(progress*100)}%</span>
            </div>
            <div class="prog-track">
              <div class="prog-fill" style="width:{round(progress*100)}%;background:{ac}"></div>
            </div>
          </div>

        </div>
        """, unsafe_allow_html=True)

        # ── dot calendar card ──
        mt = month_totals(name)
        days_in_month = calendar.monthrange(today_obj.year, today_obj.month)[1]
        dots = ""
        for d in range(1, days_in_month + 1):
            ds = f"{today_obj.year}-{today_obj.month:02d}-{d:02d}"
            cnt = mt.get(ds, 0)
            if d == today_obj.day:
                cls = dot_today_c if cnt == 0 else dot_done
            elif cnt > 0:
                cls = dot_done
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

        # ── 經文 toggle ──
        scr_key = f"scr_{name}"
        if scr_key not in st.session_state:
            st.session_state[scr_key] = False

        col_scr, _ = st.columns([3, 1])
        with col_scr:
            label = "▲ 收起經文" if st.session_state[scr_key] else "▼ 展開經文"
            if st.button(label, key=f"scr_btn_{name}"):
                st.session_state[scr_key] = not st.session_state[scr_key]
                st.rerun()

        if st.session_state[scr_key]:
            st.markdown(f'<div class="scripture-box">{info["scripture"]}</div>', unsafe_allow_html=True)

        # ── checkin card ──
        st.markdown(f"""
        <div class="pcard" style="padding:16px 18px">
          <div class="sec-label">今日打卡</div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            count_val = st.number_input(
                "次數", min_value=1, max_value=999, value=1, step=1,
                key=f"ni_{name}", label_visibility="collapsed"
            )

        st.markdown(f'<div class="{btn_cls}">', unsafe_allow_html=True)
        if st.button(f"完成 {int(count_val)} 次　記錄", key=f"btn_{name}"):
            add_count(name, int(count_val))
            st.success(f"✅ 已記錄 {int(count_val)} 次　南無觀世音菩薩 🙏")
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

        # ── 迴向文 toggle ──
        ded_key = f"ded_{name}"
        if ded_key not in st.session_state:
            st.session_state[ded_key] = False

        col_ded, _ = st.columns([3, 1])
        with col_ded:
            dlabel = "▲ 收起迴向文" if st.session_state[ded_key] else "▼ 展開迴向文"
            if st.button(dlabel, key=f"ded_btn_{name}"):
                st.session_state[ded_key] = not st.session_state[ded_key]
                st.rerun()

        if st.session_state[ded_key]:
            st.markdown(f"""
            <div class="dedication-box">
              <div class="dedication-header">
                <div class="dedication-header-line"></div>
                <div class="dedication-header-text">🪔 迴向文</div>
                <div class="dedication-header-line"></div>
              </div>{info["dedication"]}</div>
            """, unsafe_allow_html=True)

        # ── records ──
        st.markdown(f"""
        <div class="pcard" style="padding:16px 18px">
          <div class="sec-label">打卡紀錄</div>
        """, unsafe_allow_html=True)

        df_all  = load_data()
        df_this = df_all[df_all["經文"] == name].copy()

        if df_this.empty:
            st.markdown('<div style="font-size:13px;color:#AFA196;padding:4px 0">尚無記錄</div>', unsafe_allow_html=True)
        else:
            fc1, fc2 = st.columns(2)
            with fc1:
                all_months = sorted(df_this["日期"].str[:7].unique(), reverse=True)
                sel_month  = st.selectbox("月份", ["全部"] + list(all_months), key=f"fm_{name}")
            with fc2:
                sel_date = st.date_input("指定日期", value=None, key=f"fd_{name}")

            df_show = df_this.copy()
            if sel_month != "全部":
                df_show = df_show[df_show["日期"].str.startswith(sel_month)]
            if sel_date:
                df_show = df_show[df_show["日期"] == str(sel_date)]
            df_show["時間"] = df_show["時間"].fillna("").astype(str).str.replace("nan","",regex=False).str.strip()
            df_show = df_show.sort_values(["日期","時間"], ascending=False)
            # 保留原始 index（對應 CSV 行號）供刪除用
            df_show = df_show.reset_index()  # 原始 index 變成 'index' 欄

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

            # ── 表頭 ──
            hc1, hc2, hc3, hc4 = st.columns([3, 2, 2, 1])
            hc1.markdown('<div style="font-size:12px;font-weight:600;color:#AFA196;padding:4px 0">日期</div>', unsafe_allow_html=True)
            hc2.markdown('<div style="font-size:12px;font-weight:600;color:#AFA196;padding:4px 0">時間</div>', unsafe_allow_html=True)
            hc3.markdown('<div style="font-size:12px;font-weight:600;color:#AFA196;padding:4px 0">次數</div>', unsafe_allow_html=True)
            hc4.markdown('<div style="font-size:12px;font-weight:600;color:#AFA196;padding:4px 0"></div>', unsafe_allow_html=True)
            st.markdown('<hr style="margin:2px 0 6px;border:none;border-top:1px solid #E8E0D2">', unsafe_allow_html=True)

            # ── 每筆資料 ──
            confirm_key = f"confirm_{name}"
            if confirm_key not in st.session_state:
                st.session_state[confirm_key] = None

            for _, row in df_show.iterrows():
                orig_idx = int(row["index"])
                rc1, rc2, rc3, rc4 = st.columns([3, 2, 2, 1])
                rc1.markdown(f'<div style="font-size:13px;padding:6px 0;color:#3A2D24">{row["日期"]}</div>', unsafe_allow_html=True)
                rc2.markdown(f'<div style="font-size:13px;padding:6px 0;color:#7A6050">{row["時間"] or "—"}</div>', unsafe_allow_html=True)
                rc3.markdown(f'<div style="font-size:13px;padding:6px 0;font-weight:600;color:{ac}">{int(row["次數"])}</div>', unsafe_allow_html=True)
                with rc4:
                    if st.session_state[confirm_key] == orig_idx:
                        # 確認刪除狀態
                        st.markdown('<div style="font-size:11px;color:#C0392B;padding:2px 0">確定？</div>', unsafe_allow_html=True)
                        cc1, cc2 = st.columns(2)
                        with cc1:
                            if st.button("✓", key=f"yes_{name}_{orig_idx}", help="確認刪除"):
                                delete_row(orig_idx)
                                st.session_state[confirm_key] = None
                                st.rerun()
                        with cc2:
                            if st.button("✗", key=f"no_{name}_{orig_idx}", help="取消"):
                                st.session_state[confirm_key] = None
                                st.rerun()
                    else:
                        if st.button("🗑", key=f"del_{name}_{orig_idx}", help="刪除此筆"):
                            st.session_state[confirm_key] = orig_idx
                            st.rerun()

            st.markdown('<hr style="margin:6px 0 10px;border:none;border-top:1px solid #E8E0D2">', unsafe_allow_html=True)

            st.markdown('<div class="dl-wrap">', unsafe_allow_html=True)
            st.download_button(
                "⬇ 下載 CSV",
                df_show.to_csv(index=False, encoding="utf-8-sig"),
                file_name=f"{name}_打卡記錄_{today_tw()}.csv",
                mime="text/csv",
                use_container_width=True,
                key=f"dl_{name}",
            )
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)  # close pcard
