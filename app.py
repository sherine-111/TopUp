import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="TopUp", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Cormorant+Garamond:wght@500;600;700&display=swap');

:root {
    --bg1: #f9e6cc;
    --bg2: #f4d8cf;
    --bg3: #f7d8e6;
    --card: rgba(255,255,255,0.58);
    --card2: rgba(255,255,255,0.72);
    --text: #3b2b2b;
    --muted: rgba(59,43,43,0.65);
    --accent1: #ffb07c;
    --accent2: #f49cc3;
    --accent3: #ffd2a8;
    --border: rgba(255,255,255,0.55);
    --shadow: 0 18px 50px rgba(198, 143, 125, 0.14);
}

html, body, .stApp {
    background:
        radial-gradient(circle at 18% 15%, rgba(255,255,255,0.9), transparent 26%),
        radial-gradient(circle at 75% 15%, rgba(255,255,255,0.45), transparent 20%),
        linear-gradient(135deg, var(--bg1) 0%, #f8ebdf 34%, #f7e1dd 58%, var(--bg3) 100%) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

section[data-testid="stSidebar"] { display: none !important; }
header, footer { visibility: hidden; }

div.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1320px;
}

.navbar {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding: 14px 20px;
    border-radius: 999px;
    background: rgba(255,255,255,0.62);
    border: 1px solid rgba(255,255,255,0.7);
    box-shadow: var(--shadow);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    margin-bottom: 34px;
}
.nav-left, .nav-right {
    display:flex;
    align-items:center;
    gap: 18px;
}
.brand {
    display:flex;
    align-items:center;
    gap: 12px;
    color: var(--text);
    font-weight: 700;
    font-size: 1.15rem;
    text-decoration:none;
}
.brand-dot {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display:grid;
    place-items:center;
    background: linear-gradient(135deg, var(--accent1), var(--accent2));
    color: white;
    box-shadow: 0 8px 18px rgba(244,156,195,0.35);
}
.nav-link {
    color: rgba(59,43,43,0.74);
    text-decoration:none;
    font-size: 1rem;
    font-weight: 500;
    padding: 10px 16px;
    border-radius: 999px;
}
.nav-link.active {
    color: white;
    background: linear-gradient(135deg, #ffb56b 0%, #f39bbf 100%);
    box-shadow: 0 10px 24px rgba(242,156,146,0.28);
}
.badge {
    display:inline-flex;
    align-items:center;
    gap:8px;
    padding: 8px 14px;
    border-radius:999px;
    background: rgba(255,255,255,0.55);
    border: 1px solid rgba(255,255,255,0.8);
    color: rgba(59,43,43,0.55);
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.kicker {
    color: #ea8e72;
    font-size: 0.88rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(3.8rem, 8vw, 6.9rem);
    line-height: 0.92;
    font-weight: 700;
    letter-spacing: -0.05em;
    text-align:center;
    margin: 12px 0 18px;
    color: #4a3434;
}
.hero-title .gradient {
    background: linear-gradient(90deg, #ffbf86 0%, #f4a0b8 55%, #d99ae9 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.hero-copy {
    max-width: 760px;
    margin: 0 auto;
    text-align:center;
    color: rgba(59,43,43,0.62);
    font-size: 1.08rem;
    line-height: 1.65;
}
.center {
    display:flex;
    justify-content:center;
    align-items:center;
    gap: 14px;
    flex-wrap: wrap;
    margin-top: 28px;
}
.btn-link, .btn-secondary {
    display:inline-flex;
    align-items:center;
    justify-content:center;
    gap: 10px;
    padding: 14px 22px;
    border-radius: 999px;
    text-decoration:none;
    font-weight: 700;
    border: 1px solid rgba(255,255,255,0.72);
    box-shadow: 0 10px 22px rgba(180,120,120,0.13);
}
.btn-link {
    color: white !important;
    background: linear-gradient(135deg, #ffbc7a 0%, #f39dc3 100%);
}
.btn-secondary {
    color: var(--text) !important;
    background: rgba(255,255,255,0.55);
}
.card, .metric-card, .feature-card, .panel-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 28px;
    box-shadow: var(--shadow);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
}
.metric-card {
    padding: 22px 24px;
    min-height: 140px;
}
.metric-label {
    color: rgba(59,43,43,0.62);
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.metric-value {
    color: #3f2a2a;
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(3rem, 4vw, 4.2rem);
    font-weight: 700;
    line-height: 0.95;
}
.metric-sub {
    color: rgba(59,43,43,0.72);
    font-size: 1.05rem;
    margin-left: 6px;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
}
.feature-card {
    padding: 30px;
    min-height: 290px;
}
.feature-icon {
    width: 56px;
    height: 56px;
    border-radius: 18px;
    display:grid;
    place-items:center;
    background: rgba(255,255,255,0.6);
    border: 1px solid rgba(255,255,255,0.7);
    font-size: 1.5rem;
    margin-bottom: 18px;
}
.feature-kicker {
    color: #ea8e72;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.feature-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.9rem;
    line-height: 0.95;
    font-weight: 700;
    margin: 0 0 12px 0;
    color: #3c2a2a;
}
.feature-copy {
    color: rgba(59,43,43,0.65);
    font-size: 1.03rem;
    line-height: 1.6;
    max-width: 92%;
}
.section-head {
    display:flex;
    justify-content:space-between;
    align-items:end;
    gap: 18px;
    margin: 4px 0 18px;
}
.section-head h2 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem;
    line-height: 0.95;
    margin: 0;
    color: #3c2a2a;
}
.section-head p {
    margin: 0;
    color: rgba(59,43,43,0.6);
}
.panel-card {
    padding: 24px;
}
[data-testid="stSlider"] > div { padding-top: 10px; }
[data-testid="stMetricValue"] { font-family: 'Cormorant Garamond', serif; }
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.35);
    border: 1px solid rgba(255,255,255,0.45);
    border-radius: 22px;
    padding: 18px 18px 14px;
}
button[kind="primary"] {
    background: linear-gradient(135deg, #ffbc7a 0%, #f39dc3 100%) !important;
    border: none !important;
    color: white !important;
    border-radius: 999px !important;
}
button {
    border-radius: 999px !important;
}
</style>
""", unsafe_allow_html=True)

if 'custom_data' not in st.session_state:
    st.session_state['custom_data'] = None

raw_data = """Date,Time,Amount_HKD
2026-05-29,06:07,20.0
2026-05-30,18:44,50.0
2026-06-04,00:53,20.0
2026-06-06,04:18,20.0
2026-06-07,22:49,50.0
2026-06-19,07:56,0.0"""

df = pd.read_csv(io.StringIO(raw_data)) if st.session_state['custom_data'] is None else st.session_state['custom_data']
df.columns = df.columns.str.strip()
df['Timestamp'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str))
df = df.sort_values('Timestamp').reset_index(drop=True)
df['Hours_Lasted'] = (df['Timestamp'].shift(-1) - df['Timestamp']).dt.total_seconds() / 3600
df['Days_Lasted'] = df['Hours_Lasted'] / 24
df['Daily_Burn_Rate_HKD'] = df['Amount_HKD'] / df['Days_Lasted']

historical_weather = pd.DataFrame({
    'Date': ['2026-05-29', '2026-05-30', '2026-06-04', '2026-06-06', '2026-06-07'],
    'Max_Temp_C': [31.2, 32.5, 33.1, 32.8, 29.4]
})
analysis_df = pd.merge(df, historical_weather, on='Date', how='inner')

x_train_arr = np.array([31.2, 32.5, 33.1, 32.8, 29.4])
y_train_arr = np.array([13.11, 11.75, 9.34, 11.29, 4.39])
slope, intercept = np.polyfit(x_train_arr, y_train_arr, 1)

st.markdown('''
<div class="navbar">
  <div class="nav-left">
    <a class="brand" href="#home"><span class="brand-dot">☼</span>TopUp</a>
  </div>
  <div class="nav-right">
    <a class="nav-link active" href="#home">Home</a>
    <a class="nav-link" href="#forecast">Forecast</a>
    <a class="nav-link" href="#log">Log</a>
  </div>
</div>
''', unsafe_allow_html=True)

st.markdown('<div id="home"></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; margin-top: 52px;">', unsafe_allow_html=True)
st.markdown('<div class="badge">● Live · Founded June 2026</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Forecast your<br><span class="gradient">residence spend.</span></div>', unsafe_allow_html=True)
st.markdown("<div class='hero-copy'>TopUp analyzes the microclimate of rooms in student residences. By combining real-time financial reload data with local temperature, it anticipates your expenses using machine learning.</div>", unsafe_allow_html=True)
hero_c1, hero_c2, hero_c3 = st.columns([1,1,1])
with hero_c2:
    c1, c2 = st.columns(2)
    with c1:
        st.link_button("Explore the forecast →", "#forecast")
    with c2:
        st.link_button("See the log", "#log")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<div style='height: 26px;'></div>", unsafe_allow_html=True)

st.markdown('<div class="section-head"><div><div class="kicker">Overview</div><h2>Portfolio metrics</h2></div><div style="color:#ea8e72;font-weight:700;">View full log →</div></div>', unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Max daily burn velocity</div><div class='metric-value'>${analysis_df['Daily_Burn_Rate_HKD'].max():.2f}<span class='metric-sub'>HKD / day</span></div></div>", unsafe_allow_html=True)
with m2:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Avg summer burn rate</div><div class='metric-value'>${analysis_df['Daily_Burn_Rate_HKD'].mean():.2f}<span class='metric-sub'>HKD / day</span></div></div>", unsafe_allow_html=True)
with m3:
    st.markdown("<div class='metric-card'><div class='metric-label'>Heat correlation</div><div class='metric-value'>0.64<span class='metric-sub'>r-coef</span></div></div>", unsafe_allow_html=True)

st.markdown("<div style='height: 34px;'></div>", unsafe_allow_html=True)

f1, f2 = st.columns(2)
with f1:
    st.markdown('<div id="forecast"></div>', unsafe_allow_html=True)
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("<div class='feature-icon'>📈</div>", unsafe_allow_html=True)
    st.markdown("<div class='feature-kicker'>The data one</div>", unsafe_allow_html=True)
    st.markdown("<div class='feature-title'>ML Forecast Canvas</div>", unsafe_allow_html=True)
    st.markdown("<div class='feature-copy'>Slide the simulated heat dial and watch tomorrow's spend re-price in real time.</div>", unsafe_allow_html=True)
    simulated_temp = st.slider("Simulated Target Heat Threshold (°C)", min_value=24.0, max_value=38.0, value=33.0, step=0.5)
    burn_scalar = float(simulated_temp * slope + intercept)
    weekly_total_scalar = float(burn_scalar * 7)
    p1, p2 = st.columns(2)
    with p1:
        st.metric("Projected daily burn velocity", f"${burn_scalar:.2f} HKD")
    with p2:
        st.metric("Suggested 7-day recharge budget", f"${weekly_total_scalar:.2f} HKD")
    st.markdown('</div>', unsafe_allow_html=True)

with f2:
    st.markdown('<div id="log"></div>', unsafe_allow_html=True)
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.markdown("<div class='feature-icon'>📊</div>", unsafe_allow_html=True)
    st.markdown("<div class='feature-kicker'>The table one</div>", unsafe_allow_html=True)
    st.markdown("<div class='feature-title'>Top-Up Log</div>", unsafe_allow_html=True)
    st.markdown("<div class='feature-copy'>Every reload, days lasted, daily burn and room temperature in one tidy ledger.</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV log", type=["csv"])
    if uploaded_file is not None:
        st.session_state['custom_data'] = pd.read_csv(uploaded_file)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 26px;'></div>", unsafe_allow_html=True)
st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
st.markdown("<div class='section-head'><div><div class='kicker'>Analytics</div><h2>Climate Matrix Visualization</h2></div></div>", unsafe_allow_html=True)

fig, ax1 = plt.subplots(figsize=(11, 3.9), facecolor='none')
fig.patch.set_alpha(0)
ax1.set_facecolor('none')
sns.set_theme(style='whitegrid')
for spine in ax1.spines.values():
    spine.set_visible(False)

sns.barplot(data=analysis_df, x='Date', y='Daily_Burn_Rate_HKD', color='#ffab7b', alpha=0.85, ax=ax1)
ax1.set_xlabel('Terminal top-up stamp date', color='rgba(59,43,43,0.65)', fontsize=9)
ax1.set_ylabel('Daily burn velocity (HKD)', color='#ea8e72', fontsize=9)
ax1.tick_params(axis='x', labelsize=8, labelcolor='#6d5a5a')
ax1.tick_params(axis='y', labelsize=8, labelcolor='#6d5a5a')

ax2 = ax1.twinx()
for spine in ax2.spines.values():
    spine.set_visible(False)
sns.lineplot(data=analysis_df, x=range(len(analysis_df)), y='Max_Temp_C', color='#ef93b7', marker='o', linewidth=2.5, ax=ax2)
ax2.set_ylabel('Observed peak temp (°C)', color='#ef93b7', fontsize=9)
ax2.tick_params(axis='y', labelsize=8, labelcolor='#6d5a5a')
fig.tight_layout()
st.pyplot(fig, use_container_width=True)

st.dataframe(analysis_df[['Date', 'Amount_HKD', 'Days_Lasted', 'Daily_Burn_Rate_HKD', 'Max_Temp_C']], use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)
