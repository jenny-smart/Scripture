import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date, datetime, timedelta

st.set_page_config(page_title="讀誦打卡", page_icon="🪷", layout="centered")

DATA_FILE = Path("records.csv")
GOAL = 1000

MANTRA = "離婆離婆帝。求訶求訶帝。陀羅尼帝。尼訶囉帝。毘黎你帝。摩訶伽帝。真陵乾帝。梭哈"

SCRIPTURE_GW = """奉請八大菩薩：
南摩觀世音菩薩摩訶薩。
南摩彌勒菩薩摩訶薩。
南摩虛空藏菩薩摩訶薩。
南摩普賢菩薩摩訶薩。
南摩金剛手菩薩摩訶薩。
南摩妙吉祥菩薩摩訶薩。
南摩除蓋障菩薩摩訶薩。
南摩地藏王菩薩摩訶薩。
南摩諸尊菩薩摩訶薩。

高王觀世音經
觀世音菩薩。
南摩佛。南摩法。南摩僧。
佛國有緣。佛法相因。
常樂我淨。有緣佛法。
南摩摩訶般若波羅蜜。是大神咒。
南摩摩訶般若波羅蜜。是大明咒。
南摩摩訶般若波羅蜜。是無上咒。
南摩摩訶般若波羅蜜。是無等等咒。
南摩淨光祕密佛。法藏佛。獅子吼神足幽王佛。佛告須彌燈王佛。法護佛。金剛藏獅子遊戲佛。寶勝佛。神通佛。藥師琉璃光王佛。普光功德山王佛。善住功德寶王佛。
過去七佛。未來賢劫千佛。千五百佛。萬五千佛。五百花勝佛。百億金剛藏佛。定光佛。
六方六佛名號。
東方寶光月殿月妙尊音王佛。
南方樹根花王佛。
西方皂王神通焰花王佛。
北方月殿清淨佛。
上方無數精進寶首佛。
下方善寂月音王佛。
無量諸佛。多寶佛。釋迦牟尼佛。彌勒佛。阿閦佛。彌陀佛。
中央一切眾生。在佛世界中者。行住於地上。及在虛空中。慈憂於一切眾生。各令安穩休息。晝夜修持。心常求誦此經。能滅生死苦。消除諸毒害。
南摩大明觀世音。觀明觀世音。高明觀世音。開明觀世音。藥王菩薩。藥上菩薩。文殊師利菩薩。普賢菩薩。虛空藏菩薩。地藏王菩薩。清涼寶山億萬菩薩。普光王如來化勝菩薩。

念念誦此經。七佛世尊。即說咒曰：

""" + "\n".join([MANTRA for _ in range(7)]) + """

十方觀世音。一切諸菩薩。
誓願救眾生。稱名悉解脫。
若有智慧者。殷勤為解說。
但是有因緣。讀誦口不輟。
誦經滿千遍。念念心不絕。
火焰不能傷。刀兵立摧折。
恚怒生歡喜。死者變成活。
莫言此是虛。諸佛不妄說。
高王觀世音。能救諸苦厄。
臨危急難中。死者變成活。
諸佛語不虛。是故應頂禮。
持誦滿千遍。重罪皆消滅。
厚福堅信者。專攻受持經。
願以此功德。普及於一切。
誦滿一千遍。重罪皆消滅。

高王觀世音經　終。"""

SCRIPTURE_CH = """懺悔三昧，每天念三遍，不要小看。

無論是過去，現在，或是未來。

因身，口，意的造作，
被我傷害過的（因緣）眾生。

或因身，口，意的造作，
所招感的諸多不順和苦難。

不管是身體上的，還是精神上的。

我都願意接受（業果法則）。

並慚愧的懺悔。

因為無明，因未聞四種真諦，
無量劫來，我們彼此傷害，冤冤相報，
枉受諸苦於六道中，無有出期。

我們都希望解脫。

願一切被我傷害過的眾生，
無精神的痛苦，無身體的痛苦，
願你們保持快樂。

願一切與我有因緣的鬼道，非人眾生，
得聞佛法，投生善道，趨向解脫。

願一切與我有因緣的人或非人眾生，
分享我善業的功德，
並回答；善哉！善哉！善哉！

願一切眾生分享我的功德。"""

PRACTICES = {
    "高王觀世音經": {
        "icon": "🙏",
        "subtitle": "每日持誦　功課打卡",
        "scripture": SCRIPTURE_GW,
        "accent": "#6D28D9",
        "accent2": "#4C1D95",
        "pill_bg": "#EDE9FE",
        "pill_fg": "#4C1D95",
    },
    "懺悔三昧": {
        "icon": "🪷",
        "subtitle": "每日懺悔　修行打卡",
        "scripture": SCRIPTURE_CH,
        "accent": "#0F766E",
        "accent2": "#134E4A",
        "pill_bg": "#CCFBF1",
        "pill_fg": "#134E4A",
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

def add_count(name, count):
    if count <= 0:
        return
    df = load_data()
    now = datetime.now()
    row = pd.DataFrame([{"日期": str(date.today()), "時間": now.strftime("%H:%M"), "經文": name, "次數": int(count)}])
    df = pd.concat([df, row], ignore_index=True)
    save_data(df)

def today_count(name):
    df = load_data()
    if df.empty: return 0
    return int(df[(df["經文"] == name) & (df["日期"] == str(date.today()))]["次數"].sum())

def total_count(name):
    df = load_data()
    if df.empty: return 0
    return int(df[df["經文"] == name]["次數"].sum())

def streak_days(name):
    df = load_data()
    if df.empty: return 0
    days = sorted(df[df["經文"] == name]["日期"].unique(), reverse=True)
    if not days: return 0
    count, check = 0, date.today()
    for d in days:
        if str(check) == d:
            count += 1
            check -= timedelta(days=1)
        elif d < str(check):
            break
    return count

def month_totals(name):
    df = load_data()
    today = date.today()
    m = today.strftime("%Y-%m")
    df_m = df[(df["經文"] == name) & (df["日期"].str.startswith(m))]
    if df_m.empty: return {}
    return df_m.groupby("日期")["次數"].sum().to_dict()


# ── CSS ───────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;500;700;900&family=Noto+Sans+TC:wght@300;400;500;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #0E0B14 !important;
}
[data-testid="stAppViewContainer"] > .main {
    background: transparent;
}
.block-container {
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
    max-width: 600px !important;
}

/* tabs */
[data-testid="stTabs"] { margin-top:0 !important; }
[data-testid="stTabs"] > div:first-child {
    position: sticky; top: 0; z-index: 999;
    background: #0E0B14;
    padding: 10px 0 0;
    border-bottom: 1px solid rgba(255,255,255,.08);
}
button[data-baseweb="tab"] {
    font-family: 'Noto Sans TC', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: rgba(255,255,255,.45) !important;
    padding: 8px 16px !important;
    background: transparent !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #E9D5FF !important;
    border-bottom: 2px solid #A78BFA !important;
    background: transparent !important;
}
[data-testid="stTabPanel"] { padding-top: 0 !important; }

/* global text */
body, p, div, span, label {
    font-family: 'Noto Sans TC', sans-serif !important;
    color: rgba(255,255,255,.85);
}

/* page header */
.page-header {
    text-align: center;
    padding: 28px 0 18px;
}
.page-title {
    font-family: 'Noto Serif TC', serif;
    font-size: 28px;
    font-weight: 900;
    letter-spacing: .12em;
    background: linear-gradient(135deg, #E9D5FF 0%, #A78BFA 50%, #6EE7D8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
}
.page-date {
    font-size: 12px;
    color: rgba(255,255,255,.35);
    letter-spacing: .08em;
}

/* glass card */
.gcard {
    background: rgba(255,255,255,.055);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 16px;
    padding: 16px 18px;
    margin-bottom: 10px;
    backdrop-filter: blur(12px);
}
.gcard-accent-p { border-left: 3px solid #A78BFA; }
.gcard-accent-t { border-left: 3px solid #2DD4BF; }

/* hero */
.hero-icon { font-size: 36px; margin-bottom: 4px; }
.hero-name {
    font-family: 'Noto Serif TC', serif;
    font-size: 22px; font-weight: 900;
    letter-spacing: .1em;
    margin-bottom: 2px;
}
.hero-sub { font-size: 12px; color: rgba(255,255,255,.4); letter-spacing:.06em; }

/* stat chips */
.stat-row { display:flex; gap:8px; margin:10px 0 4px; }
.stat-chip {
    flex: 1;
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 10px;
    padding: 8px 4px;
    text-align: center;
}
.stat-num {
    font-family: 'Noto Serif TC', serif;
    font-size: 24px; font-weight: 700;
    line-height: 1;
}
.stat-lbl { font-size: 11px; color: rgba(255,255,255,.4); margin-top:3px; }

/* progress */
.prog-meta { display:flex; justify-content:space-between; font-size:11px; color:rgba(255,255,255,.35); margin-bottom:5px; }
.prog-track {
    height: 4px;
    background: rgba(255,255,255,.1);
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 10px;
}
.prog-fill { height: 100%; border-radius: 2px; }

/* dot calendar */
.cal-label { font-size: 12px; color:rgba(255,255,255,.35); margin-bottom:7px; letter-spacing:.04em; }
.dot-grid { display:flex; flex-wrap:wrap; gap:4px; }
.dot {
    width:26px; height:26px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:10px; font-weight:600; font-family:'Noto Sans TC',sans-serif;
}
.dot-empty  { background:rgba(255,255,255,.06); color:rgba(255,255,255,.25); }
.dot-done-p { background:#6D28D9; color:#EDE9FE; }
.dot-done-t { background:#0F766E; color:#CCFBF1; }
.dot-today-p { background:rgba(167,139,250,.18); color:#C4B5FD; border:1.5px solid #A78BFA; }
.dot-today-t { background:rgba(45,212,191,.15); color:#6EE7B7; border:1.5px solid #2DD4BF; }

/* scripture */
.scripture-box {
    background: rgba(0,0,0,.3);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 12px;
    padding: 16px 18px;
    max-height: 380px;
    overflow-y: auto;
    white-space: pre-wrap;
    font-size: 15px;
    line-height: 1.6;
    color: rgba(255,255,255,.7);
    font-family: 'Noto Serif TC', serif;
    letter-spacing: .04em;
    scrollbar-width: thin;
    scrollbar-color: rgba(167,139,250,.3) transparent;
    margin-bottom: 10px;
}

/* counter area */
.counter-wrap { text-align:center; padding: 6px 0 4px; }
.count-big {
    font-family: 'Noto Serif TC', serif;
    font-size: 72px; font-weight:900; line-height:1;
    letter-spacing:-.02em;
}
.count-sub { font-size:12px; color:rgba(255,255,255,.35); margin-top:3px; letter-spacing:.06em; }

/* buttons */
.stButton > button {
    font-family: 'Noto Sans TC', sans-serif !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    border-radius: 10px !important;
    height: 44px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    background: rgba(255,255,255,.07) !important;
    color: rgba(255,255,255,.8) !important;
    transition: all .15s;
    width: 100%;
}
.stButton > button:hover {
    background: rgba(255,255,255,.12) !important;
    border-color: rgba(255,255,255,.22) !important;
}
.checkin-p .stButton > button {
    background: linear-gradient(135deg,#6D28D9,#4C1D95) !important;
    border: none !important; color: white !important;
    height: 50px !important; font-size: 16px !important;
    box-shadow: 0 4px 20px rgba(109,40,217,.4) !important;
}
.checkin-t .stButton > button {
    background: linear-gradient(135deg,#0F766E,#134E4A) !important;
    border: none !important; color: white !important;
    height: 50px !important; font-size: 16px !important;
    box-shadow: 0 4px 20px rgba(15,118,110,.4) !important;
}

/* number input */
[data-testid="stNumberInput"] input {
    font-family: 'Noto Serif TC', serif !important;
    font-size: 22px !important; font-weight:700 !important;
    background: rgba(255,255,255,.06) !important;
    border: 1px solid rgba(255,255,255,.1) !important;
    border-radius: 10px !important;
    color: rgba(255,255,255,.9) !important;
    text-align: center;
}
[data-testid="stNumberInput"] button {
    background: rgba(255,255,255,.07) !important;
    border-radius: 8px !important;
    color: rgba(255,255,255,.6) !important;
}

/* expander */
[data-testid="stExpander"] {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(255,255,255,.07) !important;
    border-radius: 12px !important;
    margin-bottom: 10px;
}
[data-testid="stExpander"] summary {
    font-size: 13px !important;
    color: rgba(255,255,255,.5) !important;
    font-family: 'Noto Sans TC', sans-serif !important;
    padding: 10px 14px !important;
}

/* success */
[data-testid="stAlert"] {
    background: rgba(45,212,191,.12) !important;
    border: 1px solid rgba(45,212,191,.25) !important;
    border-radius: 10px !important;
    color: #6EE7B7 !important;
}

/* dataframe */
[data-testid="stDataFrame"] { border-radius:12px; overflow:hidden; }
[data-testid="stDataFrame"] table { font-family:'Noto Sans TC',sans-serif; }

/* selectbox / date input */
[data-baseweb="select"] > div {
    background: rgba(255,255,255,.07) !important;
    border-color: rgba(255,255,255,.1) !important;
    border-radius: 8px !important;
    color: rgba(255,255,255,.8) !important;
}
[data-testid="stDateInput"] input {
    background: rgba(255,255,255,.07) !important;
    border-color: rgba(255,255,255,.1) !important;
    border-radius: 8px !important;
    color: rgba(255,255,255,.8) !important;
}

/* section title */
.sec-title {
    font-family: 'Noto Serif TC', serif;
    font-size: 14px; font-weight:700;
    color: rgba(255,255,255,.5);
    letter-spacing: .1em;
    margin: 14px 0 8px;
    text-transform: uppercase;
}

/* divider */
.divider { border:none; border-top:1px solid rgba(255,255,255,.07); margin:14px 0; }

/* download btn */
.dl-btn .stDownloadButton > button {
    background: rgba(255,255,255,.06) !important;
    border: 1px solid rgba(255,255,255,.1) !important;
    border-radius: 10px !important;
    color: rgba(255,255,255,.6) !important;
    font-size:13px !important;
}
</style>
""", unsafe_allow_html=True)


# ── page header ───────────────────────────────────────────────────

today_obj = date.today()
weekday_tw = ["一","二","三","四","五","六","日"][today_obj.weekday()]
st.markdown(f"""
<div class="page-header">
  <div class="page-title">🪷 讀誦打卡</div>
  <div class="page-date">{today_obj.strftime("%Y 年 %m 月 %d 日")}　星期{weekday_tw}</div>
</div>
""", unsafe_allow_html=True)


# ── tabs ──────────────────────────────────────────────────────────

tabs = st.tabs(["🙏 高王觀世音經", "🪷 懺悔三昧"])

for i, (name, info) in enumerate(PRACTICES.items()):
    is_teal = i == 1
    accent_cls = "gcard-accent-t" if is_teal else "gcard-accent-p"
    dot_done = "dot-done-t" if is_teal else "dot-done-p"
    dot_today_cls = "dot-today-t" if is_teal else "dot-today-p"
    prog_color = "#2DD4BF" if is_teal else "#A78BFA"
    num_color  = "#2DD4BF" if is_teal else "#C4B5FD"
    checkin_cls = "checkin-t" if is_teal else "checkin-p"

    with tabs[i]:
        # hero card
        st.markdown(f"""
        <div class="gcard {accent_cls}">
          <div style="display:flex;align-items:center;gap:12px">
            <div class="hero-icon">{info['icon']}</div>
            <div>
              <div class="hero-name" style="color:{num_color}">{name}</div>
              <div class="hero-sub">{info['subtitle']}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # stats
        t_count  = today_count(name)
        a_count  = total_count(name)
        s_days   = streak_days(name)
        progress = min(a_count / GOAL, 1.0)

        st.markdown(f"""
        <div class="stat-row">
          <div class="stat-chip">
            <div class="stat-num" style="color:{num_color}">{t_count}</div>
            <div class="stat-lbl">今日</div>
          </div>
          <div class="stat-chip">
            <div class="stat-num" style="color:{num_color}">{a_count}</div>
            <div class="stat-lbl">累積</div>
          </div>
          <div class="stat-chip">
            <div class="stat-num" style="color:{num_color}">{s_days}</div>
            <div class="stat-lbl">連續天</div>
          </div>
        </div>
        <div class="prog-meta">
          <span>千遍進度</span>
          <span>{a_count} / {GOAL}　{round(progress*100)}%</span>
        </div>
        <div class="prog-track">
          <div class="prog-fill" style="width:{round(progress*100)}%;background:{prog_color}"></div>
        </div>
        """, unsafe_allow_html=True)

        # dot calendar
        mt = month_totals(name)
        import calendar
        days_in_month = calendar.monthrange(today_obj.year, today_obj.month)[1]
        dots = ""
        for d in range(1, days_in_month + 1):
            ds = today_obj.strftime(f"%Y-%m-{d:02d}")
            cnt = mt.get(ds, 0)
            if d == today_obj.day:
                cls = dot_today_cls if cnt == 0 else dot_done
            elif cnt > 0:
                cls = dot_done
            else:
                cls = "dot-empty"
            title = f"title='{cnt}次'" if cnt > 0 else ""
            dots += f'<div class="dot {cls}" {title}>{d}</div>'

        st.markdown(f"""
        <div class="gcard" style="padding:14px 16px">
          <div class="cal-label">本月打卡</div>
          <div class="dot-grid">{dots}</div>
        </div>
        """, unsafe_allow_html=True)

        # scripture expander
        with st.expander("📖 展開經文"):
            st.markdown(f'<div class="scripture-box">{info["scripture"]}</div>', unsafe_allow_html=True)

        # counter
        st.markdown('<div class="sec-title">今日打卡</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            count_val = st.number_input(
                "次數", min_value=1, max_value=999, value=1, step=1,
                key=f"ni_{name}", label_visibility="collapsed"
            )

        st.markdown(f'<div class="{checkin_cls}">', unsafe_allow_html=True)
        if st.button(f"完成　{count_val} 次　記錄", key=f"btn_{name}"):
            add_count(name, int(count_val))
            st.success(f"✅ 已記錄 {count_val} 次　南無觀世音菩薩 🙏")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # ── records section (same tab, below) ──────────────────
        st.markdown('<hr class="divider"><div class="sec-title">打卡紀錄</div>', unsafe_allow_html=True)

        df_all = load_data()
        df_this = df_all[df_all["經文"] == name].copy()

        if df_this.empty:
            st.markdown('<div style="font-size:13px;color:rgba(255,255,255,.35);padding:8px 0">尚無記錄</div>', unsafe_allow_html=True)
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

            df_show = df_show.sort_values(["日期","時間"], ascending=False).reset_index(drop=True)
            total_f = int(df_show["次數"].sum())

            st.markdown(f"""
            <div style="display:flex;gap:8px;margin-bottom:8px">
              <div class="stat-chip" style="flex:1">
                <div class="stat-num" style="color:{num_color};font-size:18px">{total_f}</div>
                <div class="stat-lbl">篩選總次數</div>
              </div>
              <div class="stat-chip" style="flex:1">
                <div class="stat-num" style="color:{num_color};font-size:18px">{df_show["日期"].nunique()}</div>
                <div class="stat-lbl">天數</div>
              </div>
              <div class="stat-chip" style="flex:1">
                <div class="stat-num" style="color:{num_color};font-size:18px">{len(df_show)}</div>
                <div class="stat-lbl">筆數</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.dataframe(
                df_show[["日期","時間","次數"]],
                use_container_width=True, hide_index=True,
            )

            st.markdown('<div class="dl-btn">', unsafe_allow_html=True)
            st.download_button(
                "⬇ 下載 CSV",
                df_show.to_csv(index=False, encoding="utf-8-sig"),
                file_name=f"{name}_打卡記錄_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True,
                key=f"dl_{name}",
            )
            st.markdown("</div>", unsafe_allow_html=True)
