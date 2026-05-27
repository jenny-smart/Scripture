import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date

st.set_page_config(
    page_title="讀經打卡",
    page_icon="🙏",
    layout="wide"
)

DATA_FILE = Path("records.csv")

# ---------- 資料 ----------

def load_data():
    if DATA_FILE.exists():
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["date", "type", "count"])


def save_record(practice_type, count):
    df = load_data()

    new_row = {
        "date": str(date.today()),
        "type": practice_type,
        "count": count
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")


def get_total(practice_type):
    df = load_data()
    if df.empty:
        return 0

    return int(
        df[df["type"] == practice_type]["count"].sum()
    )


# ---------- Style ----------

st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top,
        #fff7ed 0%,
        #fffdf8 45%,
        #fde68a 100%);
}

.block-container {
    padding-top: 2rem;
}

.card {
    background: rgba(255,255,255,0.92);
    border-radius: 28px;
    padding: 24px;
    border: 1px solid rgba(217,119,6,.15);
    box-shadow: 0 20px 40px rgba(120,72,24,.12);
}

.title {
    text-align: center;
    font-size: 34px;
    font-weight: 800;
    color: #92400e;
}

.subtitle {
    text-align: center;
    color: #a16207;
    margin-bottom: 18px;
}

.scripture {
    background: #fffaf0;
    border-radius: 20px;
    padding: 18px;
    border: 1px solid #fde68a;
    max-height: 420px;
    overflow-y: auto;
    line-height: 2.1;
    color: #78350f;
    font-size: 15px;
}

.count-box {
    background: white;
    border-radius: 20px;
    padding: 18px;
    text-align: center;
    border: 1px solid #fed7aa;
    margin-top: 18px;
}

.big-number {
    font-size: 42px;
    font-weight: 900;
    color: #b45309;
}

.small-text {
    color: #92400e;
}

.stButton button {
    width: 100%;
    border-radius: 18px;
    height: 52px;
    border: none;
    font-weight: 800;
    font-size: 16px;
    background: linear-gradient(
        135deg,
        #f59e0b,
        #b45309
    );
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------- Tabs ----------

tab1, tab2 = st.tabs([
    "🪷 懺悔三昧",
    "🙏 高王觀世音經"
])

# ---------- 懺悔三昧 ----------

with tab1:

    st.markdown("""
    <div class="card">
    <div class="title">🪷 懺悔三昧</div>
    <div class="subtitle">
    每日懺悔 × 修行打卡
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="scripture">

    懺悔三昧，每天念三遍，不要小看。<br><br>

    無論是過去，現在，或是未來。<br><br>

    因身，口，意的造作，<br>
    被我傷害過的（因緣）眾生。<br><br>

    或因身，口，意的造作，<br>
    所招感的諸多不順和苦難。<br><br>

    不管是身體上的，還是精神上的。<br><br>

    我都願意接受（業果法則）。<br><br>

    並慚愧的懺悔。<br><br>

    因為無明，因未聞四種真諦，<br>
    無量劫來，我們彼此傷害，冤冤相報，<br>
    枉受諸苦於六道中，無有出期。<br><br>

    我們都希望解脫。<br><br>

    願一切被我傷害過的眾生，<br>
    無精神的痛苦，無身體的痛苦，<br>
    願你們保持快樂。<br><br>

    願一切與我有因緣的鬼道，非人眾生，<br>
    得聞佛法，投生善道，趨向解脫。<br><br>

    願一切與我有因緣的人或非人眾生，<br>
    分享我善業的功德，<br>
    並回答；善哉！善哉！善哉！<br><br>

    願一切眾生分享我的功德。

    </div>
    """, unsafe_allow_html=True)

    st.subheader("今日打卡")

    repent_count = st.number_input(
        "今日持誦次數",
        min_value=0,
        step=1,
        key="repent"
    )

    if st.button("完成今日懺悔 ✨"):
        save_record("懺悔三昧", repent_count)
        st.success("已記錄 🙏")

    total = get_total("懺悔三昧")

    st.markdown(f"""
    <div class="count-box">
        <div class="big-number">{total}</div>
        <div class="small-text">
            累積次數
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- 高王觀世音經 ----------

with tab2:

    st.markdown("""
    <div class="card">
    <div class="title">🙏 高王觀世音經</div>
    <div class="subtitle">
    每日持誦 × 功課打卡
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="scripture">

    高王觀世音經（高王經）<br><br>

    奉請八大菩薩：<br>
    南摩觀世音菩薩摩訶薩。<br>
    南摩彌勒菩薩摩訶薩。<br>
    南摩虛空藏菩薩摩訶薩。<br>
    南摩普賢菩薩摩訶薩。<br>
    南摩金剛手菩薩摩訶薩。<br>
    南摩妙吉祥菩薩摩訶薩。<br>
    南摩除蓋障菩薩摩訶薩。<br>
    南摩地藏王菩薩摩訶薩。<br>
    南摩諸尊菩薩摩訶薩。<br><br>

    高王觀世音經<br>
    觀世音菩薩。<br>
    南摩佛。南摩法。南摩僧。<br>
    佛國有緣。佛法相因。<br>
    常樂我淨。有緣佛法。<br>

    ⋯⋯

    十方觀世音。一切諸菩薩。<br>
    誓願救眾生。稱名悉解脫。<br>
    願以此功德。普及於一切。<br>

    高王觀世音經　終。

    </div>
    """, unsafe_allow_html=True)

    st.subheader("今日打卡")

    guanyin_count = st.number_input(
        "今日持誦次數",
        min_value=0,
        step=1,
        key="guanyin"
    )

    if st.button("完成今日持誦 ✨"):
        save_record("高王觀世音經", guanyin_count)
        st.success("已記錄 🙏")

    total = get_total("高王觀世音經")

    st.markdown(f"""
    <div class="count-box">
        <div class="big-number">{total}</div>
        <div class="small-text">
            累積次數
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
