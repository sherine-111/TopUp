import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time

# --- 1. PREMIUM NATIVE STREAMLIT INITIALIZATION ---
st.set_page_config(page_title="TopUp", layout="wide")

# --- 2. THEMATIC STYLE LAYOUT & LOVABLE HIGH-FIDELITY DESIGN ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* Fixed 100% stable background layer mapping your custom color spectrum image */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        font-family: 'Inter', sans-serif !important;
        background: linear-gradient(135deg, #fff5eb 0%, #fffbf7 45%, #fae6f4 100%) !important;
        color: #2b2524 !important;
    }
    
    /* Live Header Pill Accent Tag */
    .live-badge-pill {
        display: inline-block;
        background-color: rgba(255, 139, 114, 0.1);
        color: #ff7253;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 6px 14px;
        border-radius: 30px;
        margin-top: 40px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 139, 114, 0.2);
    }
    
    /* Elegant High-End Typography mimicking Lovable/Instrument Serif layouts */
    .editorial-hero-title {
        font-family: 'Instrument Serif', serif !important;
        font-size: 5.5rem;
        font-weight: 400;
        color: #261614;
        line-height: 1.0;
        margin-bottom: 12px;
    }
    .editorial-hero-span {
        background: linear-gradient(90deg, #ff8b72 0%, #e65c84 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Instrument Serif', serif !important;
        font-style: italic;
    }
    .editorial-hero-body {
        max-width: 600px;
        font-size: 1.15rem;
        line-height: 1.6;
        color: #61514e;
        margin-bottom: 36px;
        font-weight: 400;
    }
    
    /* Creator Signature Profile Bottom Frame Component */
    .signature-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: #261614;
        color: #fcead9 !important;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 80px;
    }
    
    /* Scroll Header Metrics Layer Grid Blocks Setup */
    .section-eyebrow {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #ff8b72;
        margin-bottom: 4px;
    }
    .section-main-heading {
        font-family: 'Instrument Serif', serif !important;
        font-size: 3.5rem;
        color: #261614;
        margin-bottom: 30px;
        font-weight: 400;
    }
    
    /* High-End Glassmorphic Scorecard Metrics Units Layout */
    .glass-metric-card {
        background: rgba(255, 255, 255, 0.45);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.01);
    }
    .glass-metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #8a7571;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    .glass-metric-num {
        font-family: 'Instrument Serif', serif !important;
        font-size: 3.5rem;
        color: #261614;
        line-height: 1.0;
        font-weight: 400;
    }
    .glass-metric-unit {
        font-size: 0.9rem;
        color: #8a7571;
        font-weight: 400;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Navigation Card Hub Blocks */
    .nav-routing-card {
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        padding: 32px;
        border-radius: 24px;
        margin-top: 20px;
        margin-bottom: 40px;
    }
    .nav-card-pill-tag {
        font-size: 0.75rem;
        font-weight: 600;
        color: #ef4444;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 12px;
        margin-bottom: 4px;
    }
    .nav-card-title {
        font-family: 'Instrument Serif', serif !important;
        font-size: 2rem;
        color: #261614;
        margin-bottom: 8px;
    }
    .nav-card-desc {
        color: #6b5a57;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 16px;
    }
    
    .app-footer-bar {
        text-align: center;
        padding-top: 60px;
        padding-bottom: 40px;
        font-size: 0.85rem;
        color: #a38d88;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DYNAMIC SEQUENTIAL ANIMATED LOADING SEQUENCER ---
if 'loaded' not in st.session_state:
    st.session_state['loaded'] = True
    loading_placeholder = st.empty()
    emoji_sequence = ["☀️", "🌧️", "🌈", "☁️", "🇭🇰", "🪷", "🏖️"]
    
    for emoji in emoji_sequence:
        loading_placeholder.markdown(f"""
            <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #ffffff; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 999999;">
                <div style="font-size: 4.5rem; margin-bottom: 24px;">{emoji}</div>
                <div style="font-size: 1.35rem; color: #000000; font-family: 'Inter', sans-serif; font-weight: 500;">Your TopUp is loading...</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.7)
    loading_placeholder.empty()

# --- 4. BACKEND PROCESSING SYSTEMS ---
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

# --- 5. FRONT COVER LANDING CONTENT (PAGE 1) ---
st.markdown('<div class="live-badge-pill">● Live · Founded June 2026</div>', unsafe_allow_html=True)
st.markdown('<h1 class="editorial-hero-title">Forecast your<br><span class="editorial-hero-span">residence spend.</span></h1>', unsafe_allow_html=True)
st.markdown("""
    <p class="editorial-hero-body">
        TopUp analyzes the microclimate of rooms in student residences. By combining 
        real-time financial reload data with local temperature, it anticipates your 
        expenses using machine learning.
    </p>
""", unsafe_allow_html=True)

st.markdown('<div class="signature-badge">✦ Crafted by @sherine111</div>', unsafe_allow_html=True)

st.write("---")

# --- 6. SCROLL DOWN LAYERS: PORTFOLIO METRICS ---
st.markdown('<p class="section-eyebrow">Overview</p>', unsafe_allow_html=True)
st.markdown('<h2 class="section-main-heading">Portfolio metrics</h2>', unsafe_allow_html=True)

m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.markdown(f"""
        <div class="glass-metric-card">
            <div class="glass-metric-label">Max Daily Burn Velocity</div>
            <div class="glass-metric-num">${analysis_df['Daily_Burn_Rate_HKD'].max():.2f} <span class="glass-metric-unit">HKD / day</span></div>
        </div>
    """, unsafe_allow_html=True)
with m_col2:
    st.markdown(f"""
        <div class="glass-metric-card">
            <div class="glass-metric-label">Avg Summer Burn Rate</div>
            <div class="glass-metric-num">${analysis_df['Daily_Burn_Rate_HKD'].mean():.2f} <span class="glass-metric-unit">HKD / day</span></div>
        </div>
    """, unsafe_allow_html=True)
with m_col3:
    st.markdown(f"""
        <div class="glass-metric-card">
            <div class="glass-metric-label">Heat Correlation</div>
            <div class="glass-metric-num">0.64 <span class="glass-metric-unit">r-coef</span></div>
        </div>
    """, unsafe_allow_html=True)

# Navigation Cards Block
route_col1, route_col2 = st.columns(2)
with route_col1:
    st.markdown("""
        <div class="nav-routing-card">
            <div style="font-size:2.2rem; margin-bottom:10px;">📈</div>
            <div class="nav-card-pill-tag">The data one</div>
            <div class="nav-card-title">ML Forecast Canvas</div>
            <div class="nav-card-desc">Slide the simulated heat dial and watch tomorrow's spend re-price in real time.</div>
        </div>
    """, unsafe_allow_html=True)
with route_col2:
    st.markdown("""
        <div class="nav-routing-card">
            <div style="font-size:2.2rem; margin-bottom:10px;">📊</div>
            <div class="nav-card-pill-tag">The table one</div>
            <div class="nav-card-title">Top-Up Log</div>
            <div class="nav-card-desc">Every reload, days lasted, daily burn and room temperature in one tidy ledger.</div>
        </div>
    """, unsafe_allow_html=True)

# --- 7. FUNCTIONAL ENGINE LOGIC MODULES ---
st.write("---")
