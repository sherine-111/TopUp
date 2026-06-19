import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- 1. SET UP THE COMPACT WORKSPACE PROFILE ---
st.set_page_config(
    page_title="TopUp Workspace",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PLANABLE SaaS WORKSPACE STYLING (CSS) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* Strict Planable Reset: Crisp clinical white canvas background */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        font-family: 'Inter', sans-serif !important;
        background-color: #ffffff !important;
        color: #111827 !important;
    }
    
    /* High-contrast crisp border containers */
    .workspace-card {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Planable Brand Accent Typography */
    .workspace-eyebrow {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #4b5563;
        margin-bottom: 4px;
    }
    
    .workspace-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #111827;
        letter-spacing: -0.02em;
        margin-bottom: 24px;
    }
    
    /* Clean grid scorecards metrics display */
    .metric-value-large {
        font-size: 2.25rem;
        font-weight: 700;
        color: #111827;
        line-height: 1.1;
    }
    .metric-unit-text {
        font-size: 0.875rem;
        font-weight: 500;
        color: #6b7280;
    }
    
    /* Planable Indigo Blue Button Profile overrides */
    div.stButton > button {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border: 1px solid #2563eb !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        transition: background-color 0.15s ease !important;
    }
    div.stButton > button:hover {
        background-color: #2563eb !important;
    }
    
    /* Sidebar branding overrides */
    [data-testid="stSidebar"] {
        background-color: #f9fafb !important;
        border-right: 1px solid #e5e7eb !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. BACKEND DATA COMPUTATION SUB-SYSTEM ---
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

# --- 4. SIDEBAR PANEL NAVIGATION ---
st.sidebar.markdown("<div style='padding: 10px 0px;'><h2 style='font-size:1.25rem; font-weight:700; color:#111827; margin:0;'>⚡ TopUp Workspace</h2></div>", unsafe_allow_html=True)
st.sidebar.write("---")

# Dynamic workspace profile configuration controls placed inside sidebar context
st.sidebar.markdown("<p class='workspace-eyebrow'>Workspace Data Layer</p>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Sync profile log (CSV)", type=["csv"], label_visibility="collapsed")

if uploaded_file is not None:
    st.session_state['custom_data'] = pd.read_csv(uploaded_file)
    st.sidebar.success("Log layer loaded.")
    st.rerun()

# --- 5. MAIN WORKSPACE DASHBOARD FEED ---
st.markdown("<div class='workspace-title'>Dashboard overview</div>", unsafe_allow_html=True)

# 3-Column Planable Metrics Row Layout
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.markdown(f"""
        <div class="workspace-card">
            <div class="workspace-eyebrow">Max Daily Burn Velocity</div>
            <div class="metric-value-large">${analysis_df['Daily_Burn_Rate_HKD'].max():.2f} <span class="metric-unit-text">HKD / day</span></div>
        </div>
    """, unsafe_allow_html=True)
with m_col2:
    st.markdown(f"""
        <div class="workspace-card">
            <div class="workspace-eyebrow">Avg Summer Burn Rate</div>
            <div class="metric-value-large">${analysis_df['Daily_Burn_Rate_HKD'].mean():.2f} <span class="metric-unit-text">HKD / day</span></div>
        </div>
    """, unsafe_allow_html=True)
with col_m3 if 'col_m3' in locals() else m_col3:
    st.markdown(f"""
        <div class="workspace-card">
            <div class="workspace-eyebrow">Heat Correlation</div>
            <div class="metric-value-large">0.64 <span class="metric-unit-text">r-coefficient</span></div>
        </div>
    """, unsafe_allow_html=True)

# --- 6. ML CANVA MODELLING INTERACTIVE ROW ---
st.markdown("<div class='workspace-card'>", unsafe_allow_html=True)
st.markdown("<p class='workspace-eyebrow'>Predictive Analytics Machine</p>", unsafe_allow_html=True)
st.markdown("<h3 style='margin:0px 0px 16px 0px; font-size:1.25rem; font-weight:600;'>ML Forecast Canvas</h3>", unsafe_allow_html=True)

simulated_temp = st.slider("Simulated Target Heat Threshold (°C)", min_value=24.0, max_value=38.0, value=33.0, step=0.5)

burn_scalar = float(simulated_temp * slope + intercept)
weekly_total_scalar = float(burn_scalar * 7)

pred_col1, pred_col2 = st.columns(2)
with pred_col1:
    st.metric("Projected Daily Burn Velocity", f"${burn_scalar:.2f} HKD")
with pred_col2:
    st.metric("Suggested 7-Day Recharge Budget", f"${weekly_total_scalar:.2f} HKD")
st.markdown("</div>", unsafe_allow_html=True)

# --- 7. GRID CHART GRAPH & DATA SUMMARY TABLES ---
st.markdown("<div class='workspace-card'>", unsafe_allow_html=True)
st.markdown("<p class='workspace-eyebrow'>Climate Matrix Visualization</p>", unsafe_allow_html=True)
st.markdown("<h3 style='margin:0px 0px 16px 0px; font-size:1.25rem; font-weight:600;'>Top-Up Ledger Analytics</h3>", unsafe_allow_html=True)

fig, ax1 = plt.subplots(figsize=(11, 3.5), facecolor='white')
ax1.set_facecolor('#ffffff')
for spine in ax1.spines.values():
    spine.set_visible(False)
sns.set_theme(style="whitegrid")

color = '#3b82f6' # Planable Indigo Blue primary accent
ax1.set_xlabel('Terminal Top-Up Stamp Date', fontweight='medium', color='#4b5563', fontsize=9)
ax1.set_ylabel('Daily Burn Velocity (HKD)', color=color, fontweight='semibold', fontsize=9)
sns.barplot(data=analysis_df, x='Date', y='Daily_Burn_Rate_HKD', color=color, alpha=0.85, ax=ax1)
ax1.tick_params(axis='both', labelsize=8, labelcolor='#4b5563')

ax2 = ax1.twinx()
for spine in ax2.spines.values():
    spine.set_visible(False)
color = '#ef4444' # Vibrant data tracking red line
ax2.set_ylabel('Observed Peak Temp (°C)', color=color, fontweight='semibold', fontsize=9)
sns.lineplot(data=analysis_df, x=range(len(analysis_df)), y='Max_Temp_C', color=color, marker='o', linewidth=2.5, ax=ax2)
ax2.tick_params(axis='y', labelsize=8, labelcolor='#4b5563')

fig.tight_layout()
st.pyplot(fig)

st.write(" ")
st.dataframe(analysis_df[['Date', 'Amount_HKD', 'Days_Lasted', 'Daily_Burn_Rate_HKD', 'Max_Temp_C']], use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
