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
    
    /* Global Mesh Gradient Setup matching your precise sunset theme palette */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        font-family: 'Inter', sans-serif !important;
        background: linear-gradient(135deg, #fcead9 0%, #fff7f0 45%, #fcd6ed 100%) !important;
        color: #2b2524 !important;
    }
    
    /* Lovable Sticky Header Floating Navbar Frame */
    .navbar-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(12px);
        padding: 12px 32px;
        border-radius: 50px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        margin-bottom: 60px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.02);
    }
    .nav-logo-side {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 700;
        font-size: 1.2rem;
        color: #db7667;
    }
    .nav-links-side {
        display: flex;
        gap: 24px;
        align-items: center;
    }
    .nav-btn-active {
        background-color: #ff8b72;
        color: white !important;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 500;
        font-size: 0.9rem;
        text-decoration: none;
    }
    .nav-btn-link {
        color: #544744 !important;
        font-weight: 500;
        font-size: 0.9rem;
        text-decoration: none;
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
        margin-bottom: 24px;
        border: 1px solid rgba(255, 139, 114, 0.2);
    }
    
    /* Elegant High-End Typography */
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
    
    /* Lovable Accent Interaction Action Buttons Block */
    .cta-button-deck {
        display: flex;
        gap: 16px;
        margin-bottom: 40px;
    }
    .primary-gradient-cta {
        background: linear-gradient(90deg, #f99f7d 0%, #ff85a1 100%);
        color: white !important;
        padding: 12px 28px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 1rem;
        text-decoration: none;
        box-shadow: 0 4px 15px rgba(249, 159, 125, 0.3);
    }
    .secondary-white-cta {
        background-color: #ffffff;
        color: #2b2524 !important;
        padding: 12px 28px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 1rem;
        text-decoration: none;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
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
        margin-bottom: 100px;
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
        margin-top: 40px;
        margin-bottom: 40px;
        transition: transform 0.2s ease;
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
    .nav-card-action-link {
        color: #e65c84 !important;
        font-weight: 600;
        font-size: 0.95rem;
        text-decoration: none;
    }
    
    /* Footer Frame Layout Block */
    .app-footer-bar {
        text-align: center;
        padding-top: 60px;
        padding-bottom: 40px;
        font-size: 0.85rem;
        color: #a38d88;
        letter-spacing: -0.1px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DYNAMIC SEQUENTIAL ANIMATED LOADING SEQUENCER ---
if 'loaded' not in st.session_state:
    st.session_state['loaded'] = True
    loading_placeholder = st.empty()
    emoji_sequence = ["☀️", "🌧️", "🌈", "☁️", "🪷", "🏖️"]
    
    for emoji in emoji_sequence:
        loading_placeholder.markdown(f"""
            <style>
            .lovable-load-screen {{
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                background: linear-gradient(135deg, #fcead9 0%, #fff7f0 50%, #fcd6ed 100%) !important;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                z-index: 999999; font-family: 'Inter', sans-serif;
            }}
            .lovable-load-title {{ font-family: 'Instrument Serif', serif !important; font-size: 4rem; font-weight: 400; color: #ff8b72; margin-bottom: 4px; }}
            .lovable-load-sub {{ font-size: 1.1rem; color: #8c7a76; font-weight: 400; }}
            .lovable-load-emoji-frame {{ font-size: 3rem; margin-bottom: 16px; min-height: 4rem; display: flex; align-items: center; justify-content: center; }}
            </style>
            <div class="lovable-load-screen">
                <div class="lovable-load-emoji-frame">{emoji}</div>
                <div class="lovable-load-title">TopUp</div>
                <div class="lovable-load-sub">Warming up the forecast...</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.7)
    loading_placeholder.empty()

# --- 4. BACKEND TRANSACTION HISTORY CALCULATOR ENGINE ---
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

# Local linear regression modeling weights polyfit math calculations
x_train_arr = np.array([31.2, 32.5, 33.1, 32.8, 29.4])
y_train_arr = np.array([13.11, 11.75, 9.34, 11.29, 4.39])
slope, intercept = np.polyfit(x_train_arr, y_train_arr, 1)

# --- 5. FIXED USER INTERFACE NAVIGATION FLOATING HEADER NAVBAR ---
st.markdown("""
    <div class="navbar-container">
        <div class="nav-logo-side">🌅 TopUp</div>
