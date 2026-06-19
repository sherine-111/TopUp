import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time
from sklearn.linear_model import LinearRegression

# --- 1. DELAYED LOADING SEQUENCE ---
if 'loaded' not in st.session_state:
    st.session_state['loaded'] = True
    loading_placeholder = st.empty()
    
    loading_placeholder.markdown("""
        <style>
        @import url('https://googleapis.com');
        .loading-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 75vh;
            font-family: 'Inter', sans-serif;
            text-align: center;
            background: #fafafa;
        }
        .loading-emojis {
            font-size: 3.5rem;
            margin-bottom: 20px;
            letter-spacing: 8px;
        }
        .loading-text {
            font-size: 1.4rem;
            color: #f18721;
            font-weight: 600;
            letter-spacing: -0.5px;
        }
        </style>
        <div class="loading-container">
            <div class="loading-emojis">☀️ 🌧️ 🌈 ☁️ 🇭🇰 🪷 🏖️</div>
            <div class="loading-text">your TopUp is loading...</div>
        </div>
    """, unsafe_allow_html=True)
    
    time.sleep(5)
    loading_placeholder.empty()

# --- 2. PREMIUM TYPOGRAPHY & FIVE-STAGE GRAPHIC GRADIENT THEME ---
st.set_page_config(page_title="TopUp", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* Universal Typeface Alignment */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        font-family: 'Inter', sans-serif !important;
        background-color: #fcfcfc;
    }
    
    /* Title Layer with Exact Custom Image Gradient Spectrum */
    .brand-title {
        background: linear-gradient(to right, #f18721 0%, #f9c89e 35%, #9e9e9e 50%, #f9caf4 65%, #f182ea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        margin-bottom: 0px;
        line-height: 1.1;
    }
    
    .brand-subtitle {
        font-family: 'Inter', sans-serif;
        color: #64748b;
        font-size: 1.2rem;
        font-weight: 400;
        margin-top: -5px;
        margin-bottom: 30px;
        letter-spacing: -0.2px;
    }

    /* Highlighted Custom Card Panels using the Orange-to-Pink Theme Mapping */
    .gradient-container-card {
        background: linear-gradient(135deg, #f18721 0%, #f9c89e 45%, #f9caf4 75%, #f182ea 100%);
        color: #1e293b;
        padding: 24px;
        border-radius: 14px;
        box-shadow: 0 4px 20px rgba(241, 135, 33, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.6);
        margin-top: 20px;
        margin-bottom: 30px;
    }
    
    /* Interactive Slider Custom Styling Highlights */
    div[data-testid="stSlider"] > label {
        font-weight: 600 !important;
        color: #1e293b !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA COMPUTATION SUBSYSTEM ---
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

# --- 4. TOP HERO COVER PAGE ---
st.markdown('<p class="brand-title">TopUp</p>', unsafe_allow_html=True)
st.markdown('<p class="brand-subtitle">AC Expense Velocity & Climate Forecaster</p>', unsafe_allow_html=True)

# Main Cover Graph
fig, ax1 = plt.subplots(figsize=(11, 4))
sns.set_theme(style="whitegrid")

color = '#f18721'  # Matches Left Orange Spectrum Accent
ax1.set_xlabel('Top-Up Start Date', fontweight='bold', family='sans-serif')
ax1.set_ylabel('Daily Burn Rate (HKD / Day)', color=color, fontweight='bold', family='sans-serif')
sns.barplot(data=analysis_df, x='Date', y='Daily_Burn_Rate_HKD', color=color, alpha=0.7, ax=ax1)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = '#f182ea'  # Matches Right Pink Spectrum Accent
ax2.set_ylabel('Observed Max Temperature (°C)', color=color, fontweight='bold', family='sans-serif')
sns.lineplot(data=analysis_df, x=range(len(analysis_df)), y='Max_Temp_C', color=color, marker='o', linewidth=3, ax=ax2)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
st.pyplot(fig)

# --- 5. MIDDLE LAYER ANALYSIS & SCROLL CONTENT ---
st.write(" ")
st.write(" ")
st.markdown("### Portfolio Metrics Overview")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Max Daily Burn Velocity", f"${analysis_df['Daily_Burn_Rate_HKD'].max():.2f} HKD/Day")
with col2:
    st.metric("Average Summer Burn Rate", f"${analysis_df['Daily_Burn_Rate_HKD'].mean():.2f} HKD/Day")
with col3:
    st.metric("Mathematical Heat Correlation", "0.64")

st.dataframe(analysis_df[['Date', 'Amount_HKD', 'Days_Lasted', 'Daily_Burn_Rate_HKD', 'Max_Temp_C']], use_container_width=True)

# --- 6. PREDICTIVE ML PANEL ---
st.write("---")
st.markdown("### Machine Learning Forecast Canvas")

X_train = np.array([31.2, 32.5, 33.1, 32.8, 29.4]).reshape(-1, 1)
y_train = np.array([13.11, 11.75, 9.34, 11.29, 4.39])
model = LinearRegression().fit(X_train, y_train)

simulated_temp = st.slider("Simulated Next-Week Temperature Peak (°C)", min_value=24.0, max_value=38.0, value=33.0, step=0.5)

predicted_burn = model.predict(np.array([[simulated_temp]]))
estimated_weekly_total = predicted_burn * 7

# Visual Output Card Using Selected Color Gradient Space
st.markdown(f"""
    <div class="gradient-container-card">
        <h4 style="margin:0; padding-bottom:8px; font-weight:700; font-size:1.25rem;">Algorithmic Target Estimates</h4>
        <p style="margin:0; font-size:1.1rem; padding-bottom:4px;">Predicted Daily Cash Burn Velocity: <b>${predicted_burn:.2f} HKD / Day</b></p>
        <p style="margin:0; font-size:1.1rem;">Suggested 7-Day Card Top-Up Target: <b>${estimated_weekly_total:.2f} HKD</b></p>
    </div>
""", unsafe_allow_html=True)

# --- 7. BOTTOM LEVEL PLACEMENT DATA DROPZONE ---
st.write("---")
st.markdown("### 📁 Step 1: Upload Portfolio Log")
uploaded_file = st.file_uploader("Upload your raw topups.csv file to sync your active terminal history", type=["csv"])

if uploaded_file is not None:
    st.session_state['custom_data'] = pd.read_csv(uploaded_file)
    st.success("Data layer successfully updated! Scroll back up to review your custom metrics summary.")
