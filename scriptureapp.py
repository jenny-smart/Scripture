import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date, datetime, timedelta

st.set_page_config(
    page_title="讀經打卡",
    page_icon="🪷",
    layout="centered",
)

DATA_FILE = Path("records.csv")
GOAL = 1000

PRACTICES = {
    "高王觀世音經": {
        "icon": "🙏",
        "color_main": "#7C3AED",
        "color_light": "#EDE9FE",
        "color_border": "#C4B5FD",
        "color_btn": "linear-gradient(135deg,#7C3AED,#5B21B6)",
        "subtitle": "每日持誦 × 功課打卡",
        "scripture": """高王觀世音經（高王經）

奉請八大菩薩：
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
念念誦此經。七佛世尊。即說咒曰：「
離婆離婆帝。求訶求訶帝。陀羅尼帝。尼訶囉帝。毘黎你帝。摩訶伽帝。真陵乾帝。梭哈（三遍）

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

高王觀世音經　終。""",
    },
    "懺悔三昧": {
        "icon": "🪷",
        "color_main": "#0D9488",
        "color_light": "#CCFBF1",
        "color_border": "#99F6E4",
        "color_btn": "linear-gradient(135deg,#0D9488,#065F46)",
        "subtitle": "每日懺悔 × 修行打卡",
        "scripture": """懺悔三昧，每天念三遍，不要小看。

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

願一切眾生分享我的功德。""",
    },
}


# ── data helpers ──────────────────────────────────────────────────────────────

def load_data() -> pd.DataFrame:
    if DATA_FILE.exists():
        df = pd.read_csv(DATA_FILE)
        if "時間" not in df.columns:
            df["時間"] = ""
        return df
    return pd.DataFrame(columns=["日期", "時間", "經文", "次數"])


def save_data(df: pd.DataFrame):
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")


def add_count(name: str, count: int):
    if count <= 0:
        return
    df = load_data()
    now = datetime.now()
    row = pd.DataFrame([{
        "日期": str(date.today()),
        "時間": now.strftime("%H:%M"),
        "經文": name,
        "次數": int(count),
    }])
    df = pd.concat([df, row], ignore_index=True)
    save_data(df)


def today_count(name: str) -> int:
    df = load_data()
    if df.empty:
        return 0
    return int(df[(df["經文"] == name) & (df["日期"] == str(date.today()))]["次數"].sum())


def total_count(name: str) -> int:
    df = load_data()
    if df.empty:
        return 0
    return int(df[df["經文"] == name]["次數"].sum())


def streak(name: str) -> int:
    """連續打卡天數（有記錄即算）"""
    df = load_data()
    if df.empty:
        return 0
    days = sorted(df[df["經文"] == name]["日期"].unique(), reverse=True)
    if not days:
        return 0
    today = date.today()
    count = 0
    check = today
    for d in days:
        if str(check) == d:
            count += 1
            check -= timedelta(days=1)
        elif str(check - timedelta(days=1)) < d:
            break
    return count


def month_totals(name: str) -> dict:
    """本月每日次數"""
    df = load_data()
    today = date.today()
    month_str = today.strftime("%Y-%m")
    df_m = df[(df["經文"] == name) & (df["日期"].str.startswith(month_str))]
    if df_m.empty:
        return {}
    return df_m.groupby("日期")["次數"].sum().to_dict()


# ── styles ────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: #faf5ff !important;
}
[data-testid="stAppViewContainer"] > .main {
    background: transparent;
}
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    max-width: 640px !important;
}

/* ── 修正 tab 被蓋住 ── */
[data-testid="stTabs"] {
    margin-top: 0 !important;
}
[data-testid="stTabs"] > div:first-child {
    position: sticky;
    top: 0;
    z-index: 999;
    background: #faf5ff;
    padding-top: 6px;
    padding-bottom: 4px;
    border-bottom: 1px solid #E9D5FF;
}
button[data-baseweb="tab"] {
    font-size: 15px !important;
    font-weight: 700 !important;
    padding: 8px 18px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #7C3AED !important;
    border-bottom: 3px solid #7C3AED !important;
}

/* ── cards ── */
.card {
    background: white;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 14px;
    border: 1px solid #EDE9FE;
    box-shadow: 0 2px 12px rgba(124,58,237,.07);
}
.card-teal {
    border-color: #CCFBF1;
    box-shadow: 0 2px 12px rgba(13,148,136,.07);
}

/* ── hero ── */
.hero-icon { font-size: 48px; line-height: 1; margin-bottom: 6px; }
.hero-title { font-size: 26px; font-weight: 900; margin-bottom: 2px; }
.hero-sub { font-size: 14px; opacity: .7; }

/* ── scripture ── */
.scripture {
    background: #FDFCFF;
    border: 1px solid #EDE9FE;
    border-radius: 14px;
    padding: 18px 20px;
    max-height: 420px;
    overflow-y: auto;
    white-space: pre-wrap;
    font-size: 17px;
    line-height: 1.75;
    color: #3B1F6E;
}
.scripture-teal {
    background: #F0FDFA;
    border-color: #CCFBF1;
    color: #0D3D38;
}

/* ── counter ── */
.count-big {
    font-size: 64px;
    font-weight: 900;
    line-height: 1;
    text-align: center;
    letter-spacing: -2px;
}
.count-label {
    text-align: center;
    font-size: 13px;
    margin-top: 2px;
    opacity: .6;
}

/* ── stat boxes ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-top: 4px;
}
.stat-box {
    background: #F5F3FF;
    border-radius: 14px;
    padding: 12px 6px;
    text-align: center;
}
.stat-box-teal { background: #F0FDFA; }
.stat-num { font-size: 26px; font-weight: 900; }
.stat-lbl { font-size: 12px; opacity: .65; margin-top: 1px; }

/* ── progress ── */
.prog-wrap { margin: 10px 0 4px; }
.prog-row { display: flex; justify-content: space-between; font-size: 12px; opacity: .6; margin-bottom: 4px; }

/* ── buttons ── */
.stButton > button {
    border: none !important;
    border-radius: 14px !important;
    height: 52px !important;
    font-size: 16px !important;
    font-weight: 800 !important;
    color: white !important;
    width: 100% !important;
    background: linear-gradient(135deg,#7C3AED,#5B21B6) !important;
    box-shadow: 0 4px 14px rgba(124,58,237,.35) !important;
    transition: opacity .15s;
}
.stButton > button:hover { opacity: .88 !important; }
.teal-btn .stButton > button {
    background: linear-gradient(135deg,#0D9488,#065F46) !important;
    box-shadow: 0 4px 14px rgba(13,148,136,.35) !important;
}

/* ── dot calendar ── */
.dot-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-top: 8px;
}
.dot {
    width: 28px; height: 28px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700;
}
.dot-done-p { background:#7C3AED; color:white; }
.dot-done-t { background:#0D9488; color:white; }
.dot-today-p { background:#EDE9FE; color:#7C3AED; border:2px solid #7C3AED; }
.dot-today-t { background:#CCFBF1; color:#0D9488; border:2px solid #0D9488; }
.dot-empty  { background:#F3F4F6; color:#9CA3AF; }

/* ── record table ── */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

/* ── section title ── */
.section-h { font-size: 18px; font-weight: 800; margin: 18px 0 10px; color:#1F1235; }

/* number input */
[data-testid="stNumberInput"] input { font-size: 20px !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)


# ── page header ───────────────────────────────────────────────────────────────

today_str = date.today().strftime("%Y 年 %m 月 %d 日")
weekday_map = ["週一","週二","週三","週四","週五","週六","週日"]
weekday = weekday_map[date.today().weekday()]

st.markdown(f"""
<div style="text-align:center;padding:14px 0 8px">
  <div style="font-size:32px">🪷</div>
  <div style="font-size:22px;font-weight:900;color:#3B1F6E">讀誦打卡</div>
  <div style="font-size:13px;color:#6B7280;margin-top:2px">{today_str}　{weekday}</div>
</div>
""", unsafe_allow_html=True)


# ── tabs ──────────────────────────────────────────────────────────────────────

tab_names = [f"{PRACTICES[n]['icon']} {n}" for n in PRACTICES] + ["📋 查看記錄"]
tabs = st.tabs(tab_names)

practice_list = list(PRACTICES.items())

for i, (name, info) in enumerate(practice_list):
    is_teal = info["color_main"] == "#0D9488"
    card_cls = "card card-teal" if is_teal else "card"
    scr_cls  = "scripture scripture-teal" if is_teal else "scripture"
    stat_cls = "stat-box stat-box-teal" if is_teal else "stat-box"
    num_col  = info["color_main"]

    with tabs[i]:
        # hero
        st.markdown(f"""
        <div class="{card_cls}" style="text-align:center">
          <div class="hero-icon">{info['icon']}</div>
          <div class="hero-title" style="color:{info['color_main']}">{name}</div>
          <div class="hero-sub">{info['subtitle']}</div>
        </div>
        """, unsafe_allow_html=True)

        # scripture
        with st.expander("📖 展開經文 / 懺悔文", expanded=False):
            st.markdown(f'<div class="{scr_cls}">{info["scripture"]}</div>', unsafe_allow_html=True)

        # stats
        today_total = today_count(name)
        all_total   = total_count(name)
        streak_days = streak(name)
        progress    = min(all_total / GOAL, 1.0)

        st.markdown(f"""
        <div class="stat-grid">
          <div class="{stat_cls}">
            <div class="stat-num" style="color:{num_col}">{today_total}</div>
            <div class="stat-lbl">今日次數</div>
          </div>
          <div class="{stat_cls}">
            <div class="stat-num" style="color:{num_col}">{all_total}</div>
            <div class="stat-lbl">累積次數</div>
          </div>
          <div class="{stat_cls}">
            <div class="stat-num" style="color:{num_col}">{streak_days}</div>
            <div class="stat-lbl">連續天數</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # progress toward 1000
        st.markdown(f"""
        <div class="prog-wrap">
          <div class="prog-row">
            <span>千遍目標進度</span>
            <span>{all_total} / {GOAL}　{round(progress*100)}%</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(progress)

        # dot calendar (本月)
        st.markdown('<div class="section-h">本月打卡</div>', unsafe_allow_html=True)
        mt = month_totals(name)
        today_obj = date.today()
        days_in_month = (date(today_obj.year, today_obj.month % 12 + 1, 1) - timedelta(days=1)).day if today_obj.month < 12 else 31
        dot_done  = "dot-done-t" if is_teal else "dot-done-p"
        dot_today = "dot-today-t" if is_teal else "dot-today-p"

        dots_html = '<div class="dot-grid">'
        for d in range(1, days_in_month + 1):
            day_str = today_obj.strftime(f"%Y-%m-{d:02d}")
            cnt = mt.get(day_str, 0)
            if d == today_obj.day:
                cls = dot_today if cnt == 0 else dot_done
            elif cnt > 0:
                cls = dot_done
            else:
                cls = "dot-empty"
            tooltip = f"title='{cnt}次'" if cnt > 0 else ""
            dots_html += f'<div class="dot {cls}" {tooltip}>{d}</div>'
        dots_html += "</div>"
        st.markdown(dots_html, unsafe_allow_html=True)

        # counter + button
        st.markdown('<div class="section-h">今日打卡</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("－", key=f"dec_{name}", help="減一次"):
                # store pending decrement
                key = f"pending_{name}"
                st.session_state[key] = st.session_state.get(key, 0) - 1
                if st.session_state[key] < 0:
                    st.session_state[key] = 0

        count_key = f"count_{name}"
        if count_key not in st.session_state:
            st.session_state[count_key] = 1

        with col2:
            count_val = st.number_input(
                "次數",
                min_value=1, max_value=999,
                value=st.session_state[count_key],
                step=1,
                key=f"ni_{name}",
                label_visibility="collapsed",
            )

        with col3:
            if st.button("＋", key=f"inc_{name}", help="加一次"):
                pass  # handled by number_input

        btn_wrap = "teal-btn" if is_teal else ""
        with st.container():
            st.markdown(f'<div class="{btn_wrap}">', unsafe_allow_html=True)
            if st.button(f"{info['icon']} 完成 {count_val} 次　記錄", key=f"btn_{name}"):
                add_count(name, int(count_val))
                st.success(f"✅ 已記錄 {count_val} 次　南無觀世音菩薩 🙏")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)


# ── record tab ────────────────────────────────────────────────────────────────

with tabs[2]:
    st.markdown('<div class="section-h">📋 打卡記錄</div>', unsafe_allow_html=True)

    df = load_data()

    if df.empty:
        st.info("目前還沒有任何記錄 🙏")
    else:
        # ── filters ──
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            filter_name = st.selectbox("經文", ["全部"] + list(PRACTICES.keys()), key="filter_name")
        with col_f2:
            all_months = sorted(df["日期"].str[:7].unique(), reverse=True)
            filter_month = st.selectbox("月份", ["全部"] + list(all_months), key="filter_month")
        with col_f3:
            filter_date = st.date_input("指定日期（可清空）", value=None, key="filter_date")

        df_show = df.copy()
        if filter_name != "全部":
            df_show = df_show[df_show["經文"] == filter_name]
        if filter_month != "全部":
            df_show = df_show[df_show["日期"].str.startswith(filter_month)]
        if filter_date:
            df_show = df_show[df_show["日期"] == str(filter_date)]

        df_show = df_show.sort_values(["日期", "時間"], ascending=False).reset_index(drop=True)

        # summary
        total_filtered = int(df_show["次數"].sum())
        days_filtered  = df_show["日期"].nunique()
        st.markdown(f"""
        <div style="display:flex;gap:14px;margin-bottom:12px">
          <div class="stat-box" style="flex:1;padding:10px">
            <div class="stat-num" style="color:#7C3AED;font-size:22px">{total_filtered}</div>
            <div class="stat-lbl">篩選總次數</div>
          </div>
          <div class="stat-box" style="flex:1;padding:10px">
            <div class="stat-num" style="color:#7C3AED;font-size:22px">{days_filtered}</div>
            <div class="stat-lbl">天數</div>
          </div>
          <div class="stat-box" style="flex:1;padding:10px">
            <div class="stat-num" style="color:#7C3AED;font-size:22px">{len(df_show)}</div>
            <div class="stat-lbl">筆記錄</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(
            df_show[["日期", "時間", "經文", "次數"]],
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇ 下載 CSV",
            df_show.to_csv(index=False, encoding="utf-8-sig"),
            file_name=f"讀經打卡_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True,
        )
