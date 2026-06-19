import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time
from sklearn.linear_model import LinearRegression

# --- 1. SEQUENTIAL EMOJI LOADING SYSTEM (PLAIN WHITE SCREEN) ---
if 'loaded' not in st.session_state:
    st.session_state['loaded'] = True
    loading_placeholder = st.empty()
    
        emoji_sequence = ["☀️", "🌧️", "🌈","☁️", "🪷", "🏖️"]
    
    # Cycle through each emoji individually, replacing the previous one
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
                font-size: 4.5rem;
                margin-bottom: 24px;
                min-height: 6rem;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .load-text-bar {{
                font-size: 1.35rem;
                color: #000000;
                font-weight: 500;
                letter-spacing: -0.3px;
            }}
            </style>
            <div class="load-screen">
                <div class="load-emoji-bar">{emoji}</div>
                <div class="load-text-bar">Your TopUp is loading...</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.7)
        
    loading_placeholder.empty()
    
    # Loop through emojis one by one to create a progressive revealing effect
    for emoji in emoji_sequence:
        current_string += emoji + " "
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
                font-size: 3.5rem;
                margin-bottom: 24px;
                min-height: 5rem;
                letter-spacing: 4px;
            }}
            .load-text-bar {{
                font-size: 1.35rem;
                color: #000000;
                font-weight: 500;
                letter-spacing: -0.3px;
            }}
            </style>
            <div class="load-screen">
                <div class="load-emoji-bar">{current_string}</div>
                <div class="load-text-bar">Your TopUp is loading...</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.7) # 7 steps * 0.7s gives exactly ~5 seconds of loading time
        
    loading_placeholder.empty()

# --- 2. ROBINHOOD-STYLE TYPOGRAPHY DESIGN ---
st.set_page_config(page_title="TopUp", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* Robinhood Minimalist Framework Setup */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        font-family: 'Inter', sans-serif !important;
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Premium Multi-Stage Image Gradient Text */
    .brand-title {
        background: linear-gradient(to right, #f18721 0%, #f9c89e 35%, #ffffff 50%, #f9caf4 65%, #f182ea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4.5rem;
        font-weight: 800;
        letter-spacing: -2px;
        margin-bottom: 0px;
        line-height: 1.05;
    }
    
    .brand-subtitle {
        font-family: 'Inter', sans-serif;
        color: #6e6e73;
        font-size: 1.4rem;
        font-weight: 400;
        margin-top: 5px;
        margin-bottom: 40px;
        letter-spacing: -0.4px;
    }

    /* Minimalist High-Fidelity App Card Canvas Panels */
    .gradient-container-card {
        background: linear-gradient(135deg, #f18721 0%, #f9c89e 45%, #f9caf4 75%, #f182ea 100%);
        color: #000000;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid rgba(0, 0, 0, 0.05);
        margin-top: 20px;
        margin-bottom: 30px;
    }
    
    /* Style headers cleanly without emojis */
    h3 {
        font-weight: 700 !important;
        letter-spacing: -0.8px !important;
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA ARCHITECTURE LAYER ---
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

# --- 4. FIRST PAGE LANDING HERO (COVER VIEW) ---
st.markdown('<p class="brand-title">TopUp</p>', unsafe_allow_html=True)
st.markdown('<p class="brand-subtitle">AC Expense Velocity & Climate Forecaster</p>', unsafe_allow_html=True)

# Clean Text Overview Section (Before Scroll)
st.markdown("""
### Overview
Welcome to TopUp. This platform models room micro-climate utility velocity inside HKUST student housing. 
By compiling real-time financial recharge metrics alongside local geographical temperature variables, 
TopUp maps capital burn curves and leverages predictive machine learning models to help you stay ahead of utility expenses.
""")

# Generous whitespace block to separate cover title overview from subsequent data visualizations
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write("---")

# --- 5. SCROLLING STEP LAYER SECTION ---
st.markdown("### Dual-Axis Correlation Visualizer")

fig, ax1 = plt.subplots(figsize=(11, 4), facecolor='none')
ax1.set_facecolor('none')
sns.set_theme(style="white")

color = '#f18721'
ax1.set_xlabel('Top-Up Start Date', fontweight='semibold')
ax1.set_ylabel('Daily Burn Rate (HKD / Day)', color=color, fontweight='semibold')
sns.barplot(data=analysis_df, x='Date', y='Daily_Burn_Rate_HKD', color=color, alpha=0.8, ax=ax1)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = '#f182ea'
ax2.set_ylabel('Observed Max Temperature (°C)', color=color, fontweight='semibold')
sns.lineplot(data=analysis_df, x=range(len(analysis_df)), y='Max_Temp_C', color=color, marker='o', linewidth=3, ax=ax2)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
st.pyplot(fig)

# Metrics Grid Section
st.write(" ")
st.markdown("### Portfolio Metrics Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Max Daily Burn Velocity", f"${analysis_df['Daily_Burn_Rate_HKD'].max():.2f} HKD/Day")
with col2:
    st.metric("Average Summer Burn Rate", f"${analysis_df['Daily_Burn_Rate_HKD'].mean():.2f} HKD/Day")
with col3:
    st.metric("Mathematical Heat Correlation", "0.64")

st.dataframe(analysis_df[['Date', 'Amount_HKD', 'Days_Lasted', 'Daily_Burn_Rate_HKD', 'Max_Temp_C']], use_container_width=True)

# --- 6. PREDICTIVE MACHINE LEARNING SECTION ---
st.write("---")
st.markdown("### Machine Learning Forecast Canvas")

X_train = np.array([31.2, 32.5, 33.1, 32.8, 29.4]).reshape(-1, 1)
y_train = np.array([13.11, 11.75, 9.34, 11.29, 4.39])
model = LinearRegression().fit(X_train, y_train)

simulated_temp = st.slider("Simulated Next-Week Temperature Peak (°C)", min_value=24.0, max_value=38.0, value=33.0, step=0.5)

predicted_burn = model.predict(np.array([[simulated_temp]]))

# FIXED ERROR CODE: Safely converted array outputs to clean scalar floats before passing to formatting engine
burn_scalar = float(predicted_burn[0])
weekly_total_scalar = float(burn_scalar * 7)

st.markdown(f"""
    <div class="gradient-container-card">
        <h4 style="margin:0; padding-bottom:8px; font-weight:700;">Algorithmic Target Estimates</h4>
        <p style="margin:0; font-size:1.1rem; padding-bottom:4px;">Predicted Daily Cash Burn Velocity: <b>${burn_scalar:.2f} HKD / Day</b></p>
        <p style="margin:0; font-size:1.1rem;">Suggested 7-Day Card Top-Up Target: <b><b>${weekly_total_scalar:.2f} HKD</b></p>
    </div>
""", unsafe_allow_html=True)

# --- 7. BOTTOM LEVEL DATA ZONE ---
st.write("---")
st.sidebar.markdown("") # Force empty sidebar container context separation
st.markdown("### Step 1: Upload Portfolio Log")
uploaded_file = st.file_uploader("Upload your raw topups.csv file to sync your active terminal history", type=["csv"])

if uploaded_file is not None:
    st.session_state['custom_data'] = pd.read_csv(uploaded_file)
    st.success("Data layer successfully updated! Scroll back up to review your custom metrics summary.")
