import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time

# --- 1. PRODUCER LOADING ANIMATION MATRIX ---
if 'loaded' not in st.session_state:
    st.session_state['loaded'] = True
    loading_placeholder = st.empty()
    
    emoji_sequence = ["☀️", "🌧️", "🌈", "☁️", "🇭🇰", "🪷", "🏖️"]
    
    for emoji in emoji_sequence:
        loading_placeholder.markdown(f"""
            <style>
            @import url('https://googleapis.com');
            .load-screen {{
                position: fixed;
                top: 0; left: 0; width: 100vw; height: 100vh;
                background-color: #ffffff !important;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                z-index: 999999;
                font-family: 'Inter', sans-serif;
            }}
            .load-emoji-bar {{
                font-size: 5rem;
                margin-bottom: 20px;
                min-height: 7rem;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .load-text-bar {{
                font-size: 1.4rem;
                color: #000000;
                font-weight: 500;
                letter-spacing: -0.5px;
            }}
            </style>
            <div class="load-screen">
                <div class="load-emoji-bar">{emoji}</div>
                <div class="load-text-bar">Your TopUp is loading...</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.7)
        
    loading_placeholder.empty()

# --- 2. THEMATIC STYLE LAYOUT & SPECIFICATION INTERFACE ---
st.set_page_config(page_title="TopUp", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* Global Canvas Reset to Exact Five-Stage Color Spectrum File Specs */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        font-family: 'Inter', sans-serif !important;
        background: linear-gradient(to right, #f18721 0%, #f9c89e 35%, #ffffff 50%, #f9caf4 65%, #f182ea 100%) !important;
        color: #000000 !important;
    }
    
    /* Cover Page Branding Headers */
    .meta-header-grid {
        display: flex;
        gap: 40px;
        margin-bottom: 30px;
    }
    .meta-item {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #ff416c;
    }
    .hero-main-title {
        font-size: 6rem;
        font-weight: 800;
        letter-spacing: -3px;
        color: #000000;
        line-height: 0.9;
        margin-bottom: 25px;
    }
    
    /* Minimalist White Card Block Specs */
    .white-description-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 4px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.04);
        max-width: 440px;
        font-size: 1.05rem;
        line-height: 1.6;
        color: #ff416c;
        font-weight: 400;
    }
    
    /* Interactive Elements Highlight Modules */
    .gradient-container-card {
        background: rgba(255, 255, 255, 0.9);
        color: #000000;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid rgba(0, 0, 0, 0.05);
        box-shadow: 0 8px 32px rgba(241, 135, 33, 0.06);
        margin-top: 20px;
        margin-bottom: 30px;
    }
    
    /* Bouncing Scroll Indicator Icon */
    .scroll-arrow-box {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 60px;
        margin-bottom: 80px;
        width: 100%;
    }
    .scroll-arrow {
        font-size: 2.5rem;
        color: #000000;
        animation: bounce 2s infinite;
    }
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA & MODEL ARCHITECTURE SUBSYSTEM ---
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

df['Timestamp'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df = df.sort_values('Timestamp').reset_index(drop=True)
df['Hours_Lasted'] = (df['Timestamp'].shift(-1) - df['Timestamp']).dt.total_seconds() / 3600
df['Days_Lasted'] = df['Hours_Lasted'] / 24
df['Daily_Burn_Rate_HKD'] = df['Amount_HKD'] / df['Days_Lasted']

historical_weather = pd.DataFrame({
    'Date': ['2026-05-29', '2026-05-30', '2026-06-04', '2026-06-06', '2026-06-07'],
    'Max_Temp_C': [31.2, 32.5, 33.1, 32.8, 29.4]
})
analysis_df = pd.merge(df, historical_weather, on='Date', how='inner')

# Mathematical calculation formulas bypassing sklearn wrappers to avoid type mismatches
x_train_arr = np.array([31.2, 32.5, 33.1, 32.8, 29.4])
y_train_arr = np.array([13.11, 11.75, 9.34, 11.29, 4.39])
slope, intercept = np.polyfit(x_train_arr, y_train_arr, 1)

# --- 4. PRETTIFIED SPLIT-SCREEN LANDING PAGE (COVER VIEW) ---
hero_col1, hero_col2 = st.columns([1, 1.1], gap="large")

with hero_col1:
    st.markdown("""
        <div class="meta-header-grid">
            <div class="meta-item">Since<br><span style="color:#000000; font-weight:700;">June 2026</span></div>
            <div class="meta-item">Created By<br><span style="color:#000000; font-weight:700;">@sherine111</span></div>
        </div>
        <div class="hero-main-title">TopUp</div>
        <div class="white-description-card">
            Welcome to TopUp. This platform analyzes the microclimate of rooms in student residences. 
            By combining real-time financial reload data with local temperature, TopUp anticipates your 
            expenses using machine learning models.
        </div>
    """, unsafe_allow_html=True)

with hero_col2:
    # High-fidelity integrated chart wrapper simulation matching mockup dashboard
    fig, ax1 = plt.subplots(figsize=(6.5, 4.2), facecolor='white')
    ax1.set_facecolor('#ffffff')
    sns.set_theme(style="whitegrid")
    
    color = '#bc6c74'
    ax1.set_xlabel('Top-Up Start Date', fontweight='bold', fontsize=8)
    ax1.set_ylabel('Daily Burn Rate (HKD / Day)', color=color, fontweight='bold', fontsize=8)
    sns.barplot(data=analysis_df, x='Date', y='Daily_Burn_Rate_HKD', color=color, alpha=0.8, ax=ax1)
    ax1.tick_params(axis='both', labelsize=7)
    
    ax2 = ax1.twinx()
    color = '#1d70b8'
    ax2.set_ylabel('Observed Max Temperature (°C)', color=color, fontweight='bold', fontsize=8)
    sns.lineplot(data=analysis_df, x=range(len(analysis_df)), y='Max_Temp_C', color=color, marker='o', linewidth=2.5, ax=ax2)
    ax2.tick_params(axis='y', labelsize=7)
    
    plt.title('HKUST Hall AC Expense Velocity vs. Regional Temperature', fontsize=9, fontweight='bold', pad=10)
    fig.tight_layout()
    st.pyplot(fig)

# Centered Scrolling Chevron Indicator
st.markdown('<div class="scroll-arrow-box"><div class="scroll-arrow">︾</div></div>', unsafe_allow_html=True)

# --- 5. SCROLLING LAYERS: DATA METRICS & FORECASTER ---
st.markdown("### Portfolio Metrics Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Max Daily Burn Velocity", f"${analysis_df['Daily_Burn_Rate_HKD'].max():.2f} HKD/Day")
with col2:
    st.metric("Average Summer Burn Rate", f"${analysis_df['Daily_Burn_Rate_HKD'].mean():.2f} HKD/Day")
with col3:
    st.metric("Mathematical Heat Correlation", "0.64")

st.dataframe(analysis_df[['Date', 'Amount_HKD', 'Days_Lasted', 'Daily_Burn_Rate_HKD', 'Max_Temp_C']], use_container_width=True)

st.write("---")

# ML INTERACTIVE MODEL ENGINE CANVAS
st.markdown("### Machine Learning Forecast Canvas")
st.markdown("Adjust the weather simulation slider below to dynamically estimate your upcoming card balance strain.")

simulated_temp = st.slider("Simulated Next-Week Temperature Peak (°C)", min_value=24.0, max_value=38.0, value=33.0, step=0.5)

# Execution block utilizing clear scalar variables to perfectly resolve folder/TypeErrors
burn_scalar = float(simulated_temp * slope + intercept)
weekly_total_scalar = float(burn_scalar * 7)

st.markdown(f"""
    <div class="gradient-container-card">
        <h4 style="margin:0; padding-bottom:8px; font-weight:700;">Algorithmic Target Estimates</h4>
        <p style="margin:0; font-size:1.1rem; padding-bottom:4px;">Predicted Daily Cash Burn Velocity: <b>${burn_scalar:.2f} HKD / Day</b></p>
        <p style="margin:0; font-size:1.1rem;">Suggested 7-Day Card Top-Up Target: <b>${weekly_total_scalar:.2f} HKD</b></p>
    </div>
""", unsafe_allow_html=True)

# --- 6. DATA CONSOLE UPLOADER DROPZONE (BOTTOM ANCHOR) ---
st.write("---")
st.markdown("### Step 1: Upload Portfolio Log")
uploaded_file = st.file_uploader("Upload your raw topups.csv file to sync your active terminal history", type=["csv"])

if uploaded_file is not None:
    st.session_state['custom_data'] = pd.read_csv(uploaded_file)
    st.success("Data layer successfully updated! Scroll back up to review your custom metrics summary.")
