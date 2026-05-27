import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date

st.set_page_config(
    page_title="讀經打卡",
    page_icon="🙏",
    layout="centered",
)

DATA_FILE = Path("records.csv")
GOAL = 1000

PRACTICES = {
    "懺悔三昧": {
        "icon": "🪷",
        "subtitle": "每日懺悔 × 修行打卡",
        "button": "完成一次懺悔三昧 ✨",
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
    "高王觀世音經": {
        "icon": "🙏",
        "subtitle": "每日持誦 × 功課打卡",
        "button": "完成一次高王觀世音經 ✨",
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
過去七佛。未來賢劫千佛。千五百佛h。萬五千佛。五百花勝佛。百億金剛藏佛。定光佛。
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
離婆離婆帝。求訶求訶帝。陀羅尼帝。尼訶囉帝。毘黎你帝。摩訶伽帝。真陵乾帝。梭哈

離婆離婆帝。求訶求訶帝。陀羅尼帝。尼訶囉帝。毘黎你帝。摩訶伽帝。真陵乾帝。梭哈

離婆離婆帝。求訶求訶帝。陀羅尼帝。尼訶囉帝。毘黎你帝。摩訶伽帝。真陵乾帝。梭哈

離婆離婆帝。求訶求訶帝。陀羅尼帝。尼訶囉帝。毘黎你帝。摩訶伽帝。真陵乾帝。梭哈

離婆離婆帝。求訶求訶帝。陀羅尼帝。尼訶囉帝。毘黎你帝。摩訶伽帝。真陵乾帝。梭哈

離婆離婆帝。求訶求訶帝。陀羅尼帝。尼訶囉帝。毘黎你帝。摩訶伽帝。真陵乾帝。梭哈

離婆離婆帝。求訶求訶帝。陀羅尼帝。尼訶囉帝。毘黎你帝。摩訶伽帝。真陵乾帝。梭哈

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
}


def load_data():
    if DATA_FILE.exists():
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["日期", "經文", "次數"])


def save_data(df):
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")


def add_count(name, count):
    if count <= 0:
        return
    df = load_data()
    row = pd.DataFrame([{"日期": str(date.today()), "經文": name, "次數": int(count)}])
    df = pd.concat([df, row], ignore_index=True)
    save_data(df)


def total_count(name):
    df = load_data()
    if df.empty:
        return 0
    return int(df[df["經文"] == name]["次數"].sum())


def today_count(name):
    df = load_data()
    if df.empty:
        return 0
    today = str(date.today())
    return int(df[(df["經文"] == name) & (df["日期"] == today)]["次數"].sum())


def seed_records():
    df = load_data()
    seed = pd.DataFrame([
        {"日期": "2026-05-25", "經文": "高王觀世音經", "次數": 15},
        {"日期": "2026-05-26", "經文": "高王觀世音經", "次數": 15},
    ])
    df = pd.concat([df, seed], ignore_index=True)
    save_data(df)


st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #fff7ed 0%, #fffdf8 42%, #fde68a 100%);
}
.block-container {
    padding-top: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 780px;
}
.card {
    background: rgba(255,255,255,0.94);
    border: 1px solid rgba(217,119,6,.16);
    border-radius: 28px;
    padding: 24px;
    box-shadow: 0 20px 45px rgba(120,72,24,.12);
    margin-bottom: 18px;
}
.hero {
    text-align: center;
    padding: 20px 10px;
}
.title {
    font-size: 38px;
    font-weight: 900;
    color: #92400e;
    margin-bottom: 6px;
}
.subtitle {
    font-size: 19px;
    color: #a16207;
    font-weight: 600;
}
.scripture {
    background: #fffaf0;
    border: 1px solid #fde68a;
    border-radius: 22px;
    padding: 20px;
    max-height: 560px;
    overflow-y: auto;
    white-space: pre-wrap;
    font-size: 19px;
    line-height: 1.62;
    color: #78350f;
}
.section-title {
    font-size: 32px;
    font-weight: 900;
    color: #1f2937;
    margin-top: 20px;
    margin-bottom: 12px;
}
.stat-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 16px;
}
.stat {
    background: white;
    border: 1px solid #fed7aa;
    border-radius: 20px;
    text-align: center;
    padding: 16px 8px;
}
.num {
    font-size: 34px;
    font-weight: 900;
    color: #b45309;
}
.label {
    font-size: 14px;
    color: #92400e;
}
.stButton button {
    width: 100%;
    border: none;
    border-radius: 18px;
    height: 54px;
    color: white;
    font-size: 17px;
    font-weight: 900;
    background: linear-gradient(135deg, #f59e0b, #b45309);
}
[data-testid="stNumberInput"] input {
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

if "seed_done" not in st.session_state:
    st.session_state.seed_done = True
    if not DATA_FILE.exists():
        seed_records()

practice_names = list(PRACTICES.keys())
selected = st.tabs([f"{PRACTICES[name]['icon']} {name}" for name in practice_names])

for tab, name in zip(selected, practice_names):
    info = PRACTICES[name]
    with tab:
        st.markdown(f"""
        <div class="card hero">
            <div class="title">{info['icon']} {name}</div>
            <div class="subtitle">{info['subtitle']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <div class="scripture">{info['scripture']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-title">今日打卡</div>', unsafe_allow_html=True)

        count = st.number_input(
            "今日持誦次數",
            min_value=1,
            max_value=999,
            value=1,
            step=1,
            key=f"count_{name}",
        )

        if st.button(info["button"], key=f"btn_{name}"):
            add_count(name, count)
            st.success(f"已增加 {count} 次 🙏")
            st.rerun()

        today_total = today_count(name)
        all_total = total_count(name)
        progress = min(all_total / GOAL, 1.0)

        st.markdown(f"""
        <div class="stat-row">
            <div class="stat">
                <div class="num">{today_total}</div>
                <div class="label">今日次數</div>
            </div>
            <div class="stat">
                <div class="num">{all_total}</div>
                <div class="label">累積次數</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.progress(progress)
        st.caption(f"千遍目標：{all_total} / {GOAL}")

with st.expander("查看紀錄"):
    df = load_data()
    st.dataframe(df.sort_values("日期", ascending=False), use_container_width=True, hide_index=True)
    st.download_button(
        "下載 CSV",
        df.to_csv(index=False, encoding="utf-8-sig"),
        file_name="讀經打卡紀錄.csv",
        mime="text/csv",
        use_container_width=True,
    )
