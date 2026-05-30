import streamlit as st
from datetime import date

st.set_page_config(page_title="經文打卡", page_icon="📖", layout="centered")

st.markdown("""
<style>
:root {
  --bg: #f4eee4;
  --card: #fffdf9;
  --line: #e7ded2;
  --text: #3f352d;
  --muted: #a99f94;
  --btn: #f4f1ee;
  --btn-hover: #ebe5de;
}

.stApp {
  background: var(--bg);
  color: var(--text);
}

.block-container {
  max-width: 760px;
  padding-top: 1rem;
  padding-left: 1rem;
  padding-right: 1rem;
}

.counter-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 24px;
  padding: 18px;
  box-shadow: 0 2px 12px rgba(60, 45, 25, .08);
  margin: 18px 0;
}

.counter-title {
  font-size: 18px;
  font-weight: 800;
  color: var(--muted);
  margin-bottom: 12px;
}

div[data-testid="stNumberInput"] {
  display: none;
}

/* 讓三顆按鈕在手機上平均分配，+ / - 不會擠到最右邊 */
.counter-grid [data-testid="column"] {
  display: flex;
  align-items: stretch;
}

.counter-grid div.stButton {
  width: 100%;
}

.counter-grid div.stButton > button {
  width: 100%;
  height: 58px;
  border-radius: 16px;
  border: 1px solid var(--line);
  background: var(--btn);
  color: var(--text);
  font-size: 28px;
  font-weight: 900;
  box-shadow: none;
}

.counter-grid div.stButton > button:hover {
  background: var(--btn-hover);
  border-color: #d9cec1;
}

.counter-value {
  height: 58px;
  border-radius: 16px;
  border: 1px solid var(--line);
  background: #fffaf4;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  font-weight: 900;
  color: var(--text);
}

.main-btn div.stButton > button {
  min-height: 56px;
  border-radius: 16px;
  font-size: 20px;
  font-weight: 800;
  padding: 0 20px;
  border: 1px solid var(--line);
  background: #fffdf9;
  color: var(--text);
}

/* 手機版加大觸控區 */
@media (max-width: 768px) {
  .block-container {
    padding-left: 0.75rem;
    padding-right: 0.75rem;
  }

  .counter-card {
    padding: 16px;
    border-radius: 22px;
  }

  .counter-grid div.stButton > button {
    height: 64px;
    font-size: 32px;
    border-radius: 18px;
  }

  .counter-value {
    height: 64px;
    font-size: 32px;
    border-radius: 18px;
  }

  .main-btn div.stButton > button {
    width: 100%;
    min-height: 58px;
    font-size: 20px;
  }
}
</style>
""", unsafe_allow_html=True)


def init_state(key: str, default: int = 0) -> None:
    if key not in st.session_state:
        st.session_state[key] = default


def mobile_counter(label: str, key: str, min_value: int = 0, step: int = 1) -> int:
    """
    手機好按版次數元件：
    [ － ]    數字    [ ＋ ]

    使用方式：
        count = mobile_counter("今日打卡", "today_count")
    """
    init_state(key, min_value)

    st.markdown('<div class="counter-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="counter-title">{label}</div>', unsafe_allow_html=True)
    st.markdown('<div class="counter-grid">', unsafe_allow_html=True)

    minus_col, value_col, plus_col = st.columns([1, 2.2, 1], gap="small")

    with minus_col:
        if st.button("－", key=f"{key}_minus", use_container_width=True):
            st.session_state[key] = max(min_value, int(st.session_state[key]) - step)
            st.rerun()

    with value_col:
        st.markdown(
            f'<div class="counter-value">{int(st.session_state[key])}</div>',
            unsafe_allow_html=True,
        )

    with plus_col:
        if st.button("＋", key=f"{key}_plus", use_container_width=True):
            st.session_state[key] = int(st.session_state[key]) + step
            st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
    return int(st.session_state[key])


# ===== 範例主畫面，可整段併回你的原本 app =====

st.title("📖 經文打卡")

with st.expander("展開經文", expanded=False):
    st.write("這裡放經文內容。")

today_count = mobile_counter("今日打卡", "today_count")

st.markdown('<div class="main-btn">', unsafe_allow_html=True)
if st.button(f"完成 {today_count} 次　記錄", use_container_width=False):
    st.success(f"已記錄今日打卡 {today_count} 次")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

st.markdown('<div class="counter-card">', unsafe_allow_html=True)
st.markdown('<div class="counter-title">補登記錄</div>', unsafe_allow_html=True)

makeup_date = st.date_input("補登日期", value=date.today())
makeup_time = st.time_input("時間")
makeup_count = mobile_counter("補登次數", "makeup_count")

st.markdown('<div class="main-btn">', unsafe_allow_html=True)
if st.button(f"補登 {makeup_count} 次", use_container_width=True):
    st.success(f"已補登：{makeup_date} {makeup_time}，{makeup_count} 次")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
