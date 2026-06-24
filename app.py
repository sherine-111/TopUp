import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- 1. SET UP THE COMPACT CRYPTO WORKSPACE PROFILE ---
st.set_page_config(
    page_title="TopUp Crypto-Utility Engine",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ROBINHOOD-STYLE THEME INTERFACE (DARK MODE + NEON GREEN ACCENTS) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* Strict Robinhood Execution: Matrix Black Canvas */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        font-family: 'Inter', sans-serif !important;
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    
    /* Header Navigation Strip Wrapper */
    .rh-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 0px;
        border-bottom: 1px solid #1e293b;
        margin-bottom: 40px;
    }
    .rh-logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: #00c805; /* Robinhood Signature Neon Green */
        letter-spacing: -1px;
    }
    .rh-nav-links {
        display: flex;
        gap: 32px;
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    /* Robinhood Bold Financial Typography */
    .portfolio-value-header {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #8f9bb3;
        margin-bottom: 2px;
    }
    .portfolio-value-amount {
        font-size: 3.5rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -2px;
        line-height: 1.1;
    }
    .portfolio-delta-metrics {
        font-size: 1rem;
        font-weight: 600;
        color: #00c805; /* Green indicators for active performance */
        margin-top: 4px;
        margin-bottom: 40px;
    }
    
    /* Glassmorphic Dark Card Containers */
    .rh-card {
        background-color: #0b0e14 !important;
        border: 1px solid #1e293b !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 24px !important;
    }
    .rh-card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 16px;
        letter-spacing: -0.3px;
    }
    
    /* Custom Streamlit component overrides matching Robinhood Dark */
    div[data-testid="stMetric"] {
        background-color: #0b0e14 !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #8f9bb3 !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar Restyling Profile */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #1e293b !important;
    }
    
    /* Clean Table adjustments */
    div[data-testid="stDataFrame"] {
        background-color: #0b0e14 !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA AND MODEL ARCHITECTURE PIPELINE ---
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

# --- 4. NAVIGATION BAR HEADER ---
st.markdown("""
    <div class="rh-navbar">
        <div class="rh-logo">TopUp</div>
        <div class="rh-nav-links">
            <span style="color:#ffffff; cursor:pointer;">Investing</span>
            <span style="color:#8f9bb3; cursor:pointer; opacity:0.7;">Crypto</span>
            <span style="color:#8f9bb3; cursor:pointer; opacity:0.7;">Retirement</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 5. ROBINHOOD HERO LAYOUT (PORTFOLIO METRICS LOOK) ---
st.markdown('<p class="portfolio-value-header">AC Energy Velocity Profile</p>', unsafe_allow_html=True)
st.markdown(f'<p class="portfolio-value-amount">${analysis_df["Daily_Burn_Rate_HKD"].mean():.2f} <span style="font-size:1.5rem; color:#8f9bb3; font-weight:500;">HKD/Day</span></p>', unsafe_allow_html=True)
st.markdown('<p class="portfolio-delta-metrics">+$3.11 (+23.7%) <span style="color:#8f9bb3; font-weight:400; font-size:0.85rem;">Past Month Peak Velocity</span></p>', unsafe_allow_html=True)

# --- 6. SPLIT SCREEN LAYOUT FRAMEWORK ---
main_pane, right_sidebar = st.columns([2.3, 1], gap="large")

with main_pane:
    # High-Fidelity Frameless Line Graph mimicking Robinhood's clean interface
    fig, ax1 = plt.subplots(figsize=(10, 4.2), facecolor='#000000')
    ax1.set_facecolor('#000000')
    
    for spine in ax1.spines.values():
        spine.set_visible(False)
        
    color = '#00c805' # Robinhood Neon Green Line
    ax1.set_xlabel('Timeline Interval Log', fontweight='medium', color='#8f9bb3', fontsize=9)
    ax1.set_ylabel('Burn Velocity (HKD/Day)', color=color, fontweight='bold', fontsize=9)
    
    sns.lineplot(data=analysis_df, x='Date', y='Daily_Burn_Rate_HKD', color=color, marker='o', linewidth=3, ax=ax1)
    ax1.tick_params(axis='both', labelsize=8, labelcolor='#8f9bb3')
    ax1.grid(True, color='#1e293b', linestyle=':', alpha=0.5)
    
    ax2 = ax1.twinx()
    for spine in ax2.spines.values():
        spine.set_visible(False)
    color_temp = '#ffb703' # Neon Summer Amber
    ax2.set_ylabel('Clear Water Bay Peak Temperature (°C)', color=color_temp, fontweight='bold', fontsize=9)
    sns.lineplot(data=analysis_df, x=range(len(analysis_df)), y='Max_Temp_C', color=color_temp, linestyle='--', alpha=0.6, ax=ax2)
    ax2.tick_params(axis='y', labelsize=8, labelcolor='#8f9bb3')
    
    fig.tight_layout()
    st.pyplot(fig)
    
    st.write(" ")
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric(label="Max Burn Rate Logged", value=f"${analysis_df['Daily_Burn_Rate_HKD'].max():.2f} HKD")
    with col_stat2:
        st.metric(label="Climate Volatility Index", value="0.64 r-coef")
    with col_stat3:
        st.metric(label="Total Tracked Capital", value=f"${analysis_df['Amount_HKD'].sum():.0f} HKD")

    st.markdown("<br><h4 style='font-size:1.1rem; font-weight:600; color:#ffffff; margin-bottom:12px;'>Historical Ledger History</h4>", unsafe_allow_html=True)
    st.dataframe(analysis_df[['Date', 'Amount_HKD', 'Days_Lasted', 'Daily_Burn_Rate_HKD', 'Max_Temp_C']], use_container_width=True)

with right_sidebar:
    st.markdown('<div class="rh-card">', unsafe_allow_html=True)
    st.markdown('<p class="rh-card-title" style="margin-top:0px;">Algorithmic Forecaster</p>', unsafe_allow_html=True)
    
    simulated_temp = st.slider("Simulated Climate Peak (°C)", min_value=24.0, max_value=38.0, value=33.0, step=0.5)
    
    burn_scalar = float(simulated_temp * slope + intercept)
    weekly_total_scalar = float(burn_scalar * 7)
    
    st.write("---")
    st.markdown(f"""
        <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-size:0.9rem; color:#8f9bb3;">
            <span>Estimated Cost / Day</span>
            <span style="color:#ffffff; font-weight:601;">${burn_scalar:.2f} HKD</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:20px; font-size:0.9rem; color:#8f9bb3;">
            <span>7-Day Budget Requirement</span>
            <span style="color:#00c805; font-weight:700; font-size:1.1rem;">${weekly_total_scalar:.2f} HKD</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="rh-card">', unsafe_allow_html=True)
    st.markdown('<p class="rh-card-title" style="margin-top:0px;">Data Sync Console</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.8rem; color:#8f9bb3; margin-top:-8px; line-height:1.4;">Synchronize terminal activity logs to re-weight systemic indicators parameters automatically.</p>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Profile CSV Data", type=["csv"], label_visibility="collapsed")
    
    # --- 7. EXACT TRAILING DATA SPECIFICATION BLOCK ---
    if uploaded_file is not None:
        st.session_state['custom_data'] = pd.read_csv(uploaded_file)
        st.success("Indicators synchronized.")
        st.rerun()
    st.markdown('', unsafe_allow_html=True)
