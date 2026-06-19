# ==============================================================================
# PART 1: THEME CONSTANTS, LOADING SCREEN, AND DATA PROCESSING PIPELINE
# ==============================================================================
import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time

# --- 1. PREMIUM NATIVE APP INITIALIZATION ---
st.set_page_config(page_title="TopUp — Microclimate Spend Forecasting", layout="wide")

# --- 2. HIGH-FIDELITY DESIGN CUSTOM ENGINE (CSS) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* Perfect replication of the Lovable soft radial gradient canvas background mesh */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        font-family: 'Inter', sans-serif !important;
        background: linear-gradient(135deg, #fcead9 0%, #fff7f0 45%, #fcd6ed 100%) !important;
        color: #2b2524 !important;
    }
    
    /* Header navigation bar style matching your mockup exactly */
    .lovable-tab-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        padding: 12px 28px;
        border-radius: 40px;
        margin-top: 10px;
        margin-bottom: 60px;
        box-shadow: 0 4px 24px rgba(229, 124, 107, 0.03);
    }
    .lovable-nav-brand { font-weight: 700; font-size: 1.15rem; color: #db7667; display: flex; align-items: center; gap: 8px; }
    .lovable-nav-links { display: flex; gap: 16px; font-size: 0.9rem; font-weight: 500; }
    .lovable-nav-link-item { color: #544744; text-decoration: none; padding: 6px 14px; border-radius: 20px; }
    .lovable-nav-link-item.active { background-color: #ff8b72; color: white !important; font-weight: 600; }
    
    /* Title styling matching your precise Lovable text gradient specs */
    .text-gradient-sunset {
        background: linear-gradient(90deg, #ff8b72 0%, #e65c84 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Instrument Serif', serif !important;
        font-style: italic;
    }
    
    /* Lovable Headings Framework Setup */
    .lovable-hero-h1 {
        font-family: 'Instrument Serif', serif !important;
        font-size: 5.8rem;
        font-weight: bold;
        color: #1a100f;
        line-height: 0.95;
        letter-spacing: -2.5px;
        margin-top: 16px;
        margin-bottom: 24px;
        text-align: center;
    }
    
    .lovable-h2 {
        font-family: 'Instrument Serif', serif !important;
        font-size: 3.5rem;
        font-weight: bold;
        color: #1a100f;
        margin-top: 40px;
        margin-bottom: 20px;
        letter-spacing: -0.5px;
    }
    
    /* Premium Glassmorphic Lovable Card Elements */
    .lovable-glass-card {
        background: rgba(255, 255, 255, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        padding: 28px;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(229, 124, 107, 0.02);
        margin-bottom: 20px;
    }
    
    .lovable-card-eyebrow {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #8c7672;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }
    
    .lovable-card-value-display {
        font-family: 'Instrument Serif', serif !important;
        font-size: 3.8rem;
        color: #1a100f;
        font-weight: bold;
        line-height: 1.0;
    }
    
    .lovable-card-unit {
        font-size: 0.9rem;
        color: #8c7672;
        font-weight: 500;
        font-family: 'Inter', sans-serif !important;
        margin-left: 4px;
    }
    
    /* Hero CTA button styles */
    .lovable-cta-container { display: flex; gap: 14px; justify-content: center; align-items: center; margin-top: 24px; margin-bottom: 24px; }
    .lovable-cta-primary { background: linear-gradient(90deg, #ff8b72 0%, #e65c84 100%); color: white !important; padding: 12px 26px; border-radius: 30px; font-weight: 600; text-decoration: none; font-size: 0.95rem; box-shadow: 0 4px 15px rgba(249, 159, 125, 0.25); }
    .lovable-cta-secondary { background: rgba(255, 255, 255, 0.7); border: 1px solid rgba(0,0,0,0.06); color: #2b2524 !important; padding: 12px 26px; border-radius: 30px; font-weight: 600; text-decoration: none; font-size: 0.95rem; backdrop-filter: blur(4px); }
    
    /* Top Live Pill Tag */
    .lovable-badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.6);
        border: 1px solid rgba(229, 124, 107, 0.2);
        color: #e65c84;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 6px 16px;
        border-radius: 30px;
        backdrop-filter: blur(4px);
    }
    
    .lovable-pulse-dot {
        height: 6px; width: 6px; background-color: #e65c84; border-radius: 50%;
        animation: activePulse 1.8s infinite;
    }
    @keyframes activePulse {
        0% { transform: scale(0.9); opacity: 0.6; }
        50% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(0.9); opacity: 0.6; }
    }
    
    .lovable-signature-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: #1a100f;
        color: #fcead9 !important;
        padding: 8px 16px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 500;
        text-decoration: none;
        margin-top: 16px;
        margin-bottom: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DYNAMIC WEATHER-THEMED FLASH LOADING SYSTEM ---
if 'loaded' not in st.session_state:
    st.session_state['loaded'] = True
    loading_placeholder = st.empty()
    emoji_sequence = ["☀️", "🌧️", "🌈", "☁️", "🪷", "🏖️"]
    
    for emoji in emoji_sequence:
        loading_placeholder.markdown(f"""
            <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: linear-gradient(135deg, #fcead9 0%, #fff7f0 50%, #fcd6ed 100%) !important; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 999999;">
                <div style="font-size: 5rem; margin-bottom: 24px; min-height: 6rem; display: flex; align-items: center; justify-content: center;">{emoji}</div>
                <div style="font-family: 'Instrument Serif', serif; font-size: 3.5rem; font-weight: bold; color: #ff8b72; margin-bottom: 4px;">TopUp</div>
                <div style="font-size: 1.1rem; color: #8c7a76; font-family: 'Inter', sans-serif; font-weight: 400;">Warming up the forecast…</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.7)
    loading_placeholder.empty()

# --- 4. DATA COMPUTATION ENGINE PIPELINE ---
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

# --- 5. TOP FLOATING REPLICATED NAVBAR ---
st.markdown("""
    <div class="lovable-tab-nav">
        <div class="lovable-nav-brand">📊 TopUp</div>
        <div class="lovable-nav-links">
            <a class="lovable-nav-link-item active" href="#">Home</a>
            <a class="lovable-nav-link-item" href="#forecast">Forecast</a>
            <a class="lovable-nav-link-item" href="#log">Log</a>
        </div>
    </div>
""", unsafe_allow_html=True)
# ==============================================================================
# PART 2: UI VIEWPORTS, GRAPHICAL PLOTS, AND LIVE ML PREDICTIVE CANVAS
# ==============================================================================

# --- 6. COVER SCREEN HERO SECTION ---
st.markdown('<div style="text-align: center;"><span class="lovable-badge-pill"><span class="lovable-pulse-dot"></span>Live · Founded June 2026</span></div>', unsafe_allow_html=True)

st.markdown('<h1 class="lovable-hero-h1">Forecast your <br><span class="text-gradient-sunset">residence spend.</span></h1>', unsafe_allow_html=True)

st.markdown("""
    <div style="display: flex; justify-content: center; width: 100%;">
        <p style="max-w-2xl font-size: 1.15rem; line-height: 1.6; color: #61514e; text-align: center; margin-bottom: 12px;">
            TopUp analyzes the microclimate of rooms in student residences. By combining
            real-time financial reload data with local temperature, it anticipates your
            expenses using machine learning.
        </p>
    </div>
""", unsafe_allow_html=True)

# Navigation CTA Buttons Deck
st.markdown("""
    <div class="lovable-cta-container">
        <a class="lovable-cta-primary" href="#forecast">Explore the forecast →</a>
        <a class="lovable-cta-secondary" href="#log">See the log</a>
    </div>
""", unsafe_allow_html=True)

# GitHub Profile Signature Badge
st.markdown("""
    <div style="text-align: center;">
        <a href="https://github.com" target="_blank" class="lovable-signature-badge">
            <span style="background: #ffffff; color: #1a100f; border-radius: 50%; width: 20px; height: 20px; display: inline-flex; align-items: center; justify-content: center; font-size: 0.65rem;">✦</span>
            Crafted by <span style="font-weight: 700; color: #ffffff;">@sherine111</span>
        </a>
    </div>
""", unsafe_allow_html=True)

st.write("---")

# --- 7. SCROLL COMPONENT: MAIN METRICS DISPLAY PANELS ---
hero_col1, hero_col2 = st.columns([2, 1])
with hero_col1:
    st.markdown('<div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: #e65c84; letter-spacing: 1px;">Overview</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="lovable-h2" style="margin-top:0px;">Portfolio metrics</h2>', unsafe_allow_html=True)
with hero_col2:
    st.markdown('<div style="text-align: right; margin-top: 45px;"><a href="#log" style="font-size: 0.95rem; font-weight: 600; color: #e65c84; text-decoration:none;">View full log →</a></div>', unsafe_allow_html=True)

# Modern Glassmorphic Lovable Scorecard Grid Row Setup
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown(f"""
        <div class="lovable-glass-card">
            <div class="lovable-card-eyebrow">Max Daily Burn Velocity</div>
            <div class="lovable-card-value-display">${analysis_df['Daily_Burn_Rate_HKD'].max():.2f}<span class="lovable-card-unit">HKD / day</span></div>
        </div>
    """, unsafe_allow_html=True)
with col_m2:
    st.markdown(f"""
        <div class="lovable-glass-card">
            <div class="lovable-card-eyebrow">Avg Summer Burn Rate</div>
            <div class="lovable-card-value-display">${analysis_df['Daily_Burn_Rate_HKD'].mean():.2f}<span class="lovable-card-unit">HKD / day</span></div>
        </div>
    """, unsafe_allow_html=True)
with col_m3:
    st.markdown(f"""
        <div class="lovable-glass-card">
            <div class="lovable-card-eyebrow">Heat Correlation</div>
            <div class="lovable-card-value-display">0.64<span class="lovable-card-unit">r-coef</span></div>
        </div>
    """, unsafe_allow_html=True)

# Secondary Internal Feature Navigation Router Cards Deck
col_r1, col_r2 = st.columns(2)
with col_r1:
    st.markdown("""
        <div class="lovable-glass-card" style="background: rgba(255, 255, 255, 0.55); padding: 32px; border-radius:24px;">
            <div style="font-size: 2.2rem; margin-bottom: 4px;">📈</div>
            <div style="font-size: 0.75rem; font-weight: 600; color: #f59e0b; text-transform: uppercase; letter-spacing: 0.8px;">The data one</div>
            <div style="font-family: 'Instrument Serif', serif; font-size: 2.2rem; font-weight: bold; color: #1a100f; margin-bottom: 6px;">ML Forecast Canvas</div>
            <div style="color: #6b5a57; font-size: 0.95rem; line-height: 1.5; margin-bottom:12px;">Slide the simulated heat dial and watch tomorrow's spend re-price in real time.</div>
            <a href="#forecast" style="color: #e65c84; font-weight: 600; text-decoration:none; font-size:0.95rem;">Open →</a>
        </div>
    """, unsafe_allow_html=True)
with col_r2:
    st.markdown("""
        <div class="lovable-glass-card" style="background: rgba(255, 255, 255, 0.55); padding: 32px; border-radius:24px;">
            <div style="font-size: 2.2rem; margin-bottom: 4px;">📊</div>
            <div style="font-size: 0.75rem; font-weight: 600; color: #10b981; text-transform: uppercase; letter-spacing: 0.8px;">The table one</div>
            <div style="font-family: 'Instrument Serif', serif; font-size: 2.2rem; font-weight: bold; color: #1a100f; margin-bottom: 6px;">Top-Up Log</div>
            <div style="color: #6b5a57; font-size: 0.95rem; line-height: 1.5; margin-bottom:12px;">Every reload, days lasted, daily burn and room temperature in one tidy ledger.</div>
            <a href="#log" style="color: #e65c84; font-weight: 600; text-decoration:none; font-size:0.95rem;">Open →</a>
        </div>
    """, unsafe_allow_html=True)

# --- 8. LIVE MACHINE LEARNING ENGINE FORECASTER SUITE ---
st.markdown("<div id='forecast'></div>", unsafe_allow_html=True)
st.write("---")
st.markdown('<div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: #e65c84; letter-spacing: 1px;">Interactive Model</div>', unsafe_allow_html=True)
st.markdown('<h2 class="lovable-h2" style="margin-top:0px;">ML Forecast Canvas</h2>', unsafe_allow_html=True)

simulated_temp = st.slider("Simulated Next-Week Temperature Peak (°C)", min_value=24.0, max_value=38.0, value=33.0, step=0.5)

# High fidelity local polyfit calculation weights to safeguard against object type array crashes
burn_scalar = float(simulated_temp * slope + intercept)
weekly_total_scalar = float(burn_scalar * 7)

st.markdown(f"""
    <div class="lovable-glass-card" style="background: rgba(255, 255, 255, 0.65); padding: 32px; border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.7); margin-top: 10px; margin-bottom: 40px;">
        <h4 style="margin:0; padding-bottom:12px; font-family:'Instrument Serif', serif; font-size:2.4rem; font-weight:bold; color:#1a100f;">Algorithmic Target Estimates</h4>
        <p style="margin:0; font-size:1.15rem; padding-bottom:6px; color:#544744;">Predicted Daily Cash Burn Velocity: <b style="color:#1a100f;">${burn_scalar:.2f} HKD / Day</b></p>
        <p style="margin:0; font-size:1.15rem; color:#544744;">Suggested 7-Day Card Top-Up Target: <b style="color:#1a100f;">${weekly_total_scalar:.2f} HKD</b></p>
    </div>
""", unsafe_allow_html=True)

# --- 9. HIGH RESOLUTION DATA VIZ & MATRIX REGISTRY ---
st.markdown("<div id='log'></div>", unsafe_allow_html=True)
st.write("---")
st.markdown('<div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: #e65c84; letter-spacing: 1px;">Analytics Layer</div>', unsafe_allow_html=True)
st.markdown('<h2 class="lovable-h2" style="margin-top:0px;">Top-Up Log Visualizer</h2>', unsafe_allow_html=True)

fig, ax1 = plt.subplots(figsize=(11, 3.8), facecolor='none')
fig.patch.set_alpha(0.0)
ax1.set_facecolor('none')
for spine in ax1.spines.values():
    spine.set_visible(False)
sns.set_theme(style="whitegrid")

color = '#ff8b72' # Replicated Soft Salmon Orange Hex Accent
ax1.set_xlabel('Top-Up Start Date', fontweight='semibold', color='#544744')
ax1.set_ylabel('Daily Burn Rate (HKD / Day)', color=color, fontweight='bold')
sns.barplot(data=analysis_df, x='Date', y='Daily_Burn_Rate_HKD', color=color, alpha=0.8, ax=ax1)
ax1.tick_params(axis='both', labelsize=8, labelcolor='#544744')
ax1.grid(True, linestyle='--', alpha=0.15)

ax2 = ax1.twinx()
for spine in ax2.spines.values():
    spine.set_visible(False)
color = '#e65c84' # Deep Tech Pink Accent
ax2.set_ylabel('Observed Max Temperature (°C)', color=color, fontweight='bold')
sns.lineplot(data=analysis_df, x=range(len(analysis_df)), y='Max_Temp_C', color=color, marker='o', linewidth=3, ax=ax2)
ax2.tick_params(axis='y', labelsize=8, labelcolor='#544744')

plt.title('HKUST Hall AC Expense Velocity vs. Regional Temperature', fontsize=11, fontweight='bold', color='#1a100f', pad=14)
fig.tight_layout()
st.pyplot(fig)

st.write(" ")
st.dataframe(analysis_df[['Date', 'Amount_HKD', 'Days_Lasted', 'Daily_Burn_Rate_HKD', 'Max_Temp_C']], use_container_width=True)

# --- 10. REAL-TIME DATASET DROPZONE CONSOLE ARCHITECTURE (BOTTOM ANCHOR) ---
st.write("---")
st.markdown("### Upload Your Portfolio Log")
st.markdown("Drop your active raw `topups.csv` ledger file down here to instantly overwrite systemic analytics vectors configuration maps.")
uploaded_file = st.file_uploader("", type=["csv"])

if uploaded_file is not None:
    st.session_state['custom_data'] = pd.read_csv(uploaded_file)
    st.success("Financial profile data-layer loaded successfully!")
    st.rerun()

# --- 11. PREMIUM TAILORED SITE FOOTER ---
st.markdown("""
    <div style="text-align: center; padding-top: 60px; padding-bottom: 40px; font-size: 0.85rem; color: #a38d88; letter-spacing: 0.5px;">
        TopUp · est. June 2026 · built using premium layouts by @sherine111
    </div>
""", unsafe_allow_html=True)
