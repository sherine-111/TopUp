import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime
from sklearn.linear_model import LinearRegression

# --- 1. DYNAMIC TIME-OF-DAY THEME ENGINE ---
# Set hardcoded timezone for Hong Kong to match HKUST local environment
try:
    import pytz
    hk_tz = pytz.timezone('Asia/Hong_Kong')
    current_hour = datetime.datetime.now(hk_tz).hour
except:
    # Reliable backup shift if pytz is environment-restricted
    current_hour = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).hour

# Determine background color scheme and text colors dynamically
if 5 <= current_hour < 12:
    # Morning Mode: Warm, clean sunrise pastel gradient
    bg_gradient = "linear-gradient(135deg, #fef9c3 0%, #e0f2fe 100%)"
    text_color = "#1e293b"
    ui_mode_label = "Morning Mode Activated"
elif 12 <= current_hour < 18:
    # Afternoon Mode: Crisp, high-clarity daylight gradient
    bg_gradient = "linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%)"
    text_color = "#1e293b"
    ui_mode_label = "Afternoon Mode Activated"
else:
    # Evening Mode: Premium deep tech dark mode
    bg_gradient = "linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)"
    text_color = "#f8fafc"
    ui_mode_label = "Evening Mode Activated"

# --- 2. BRANDING & MODERN TYPOGRAPHY INJECTION ---
st.set_page_config(page_title="TopUp", layout="wide")

# Injecting 'Inter' Font styling & custom thematic canvas backgrounds via standard HTML wrappers
st.markdown(f"""
    <style>
    @import url('https://googleapis.com');
    
    html, body, [data-testid="stAppViewContainer"], .stApp {{
        background: {bg_gradient} !important;
        color: {text_color} !important;
        font-family: 'Inter', sans-serif !important;
    }}
    h1, h2, h3, h4, h5, h6, p, span, label, div {{
        font-family: 'Inter', sans-serif !important;
    }}
    </style>
""", unsafe_allow_html=True)

st.title("TopUp: AC Expense Velocity & Climate Forecaster")
st.caption(f"System Canvas: {ui_mode_label} (Inter Premium Typeface Framework)")

# --- 3. SIDEBAR: DATA UPLOADER FEATURE ---
st.sidebar.header("📁 Step 1: Upload Portfolio Log")
uploaded_file = st.sidebar.file_uploader("Upload your raw topups.csv file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.sidebar.info("Using active TopUp transaction baseline.")
    raw_data = """Date,Time,Amount_HKD
2026-05-29,06:07,20.0
2026-05-30,18:44,50.0
2026-06-04,00:53,20.0
2026-06-06,04:18,20.0
2026-06-07,22:49,50.0
2026-06-19,07:56,0.0"""
    df = pd.read_csv(io.StringIO(raw_data))

# --- 4. QUANTITATIVE PROCESSING ENGINE ---
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

# High-Level Scorecards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Max Daily Burn Velocity", f"${analysis_df['Daily_Burn_Rate_HKD'].max():.2f} HKD/Day")
with col2:
    st.metric("Average Summer Burn Rate", f"${analysis_df['Daily_Burn_Rate_HKD'].mean():.2f} HKD/Day")
with col3:
    st.metric("Mathematical Heat Correlation", "0.64 (Strong)")

st.subheader("Processed Financial & Climate Logs")
st.dataframe(analysis_df[['Date', 'Amount_HKD', 'Days_Lasted', 'Daily_Burn_Rate_HKD', 'Max_Temp_C']], use_container_width=True)

# --- 5. VISUAL CORRELATION MAP ---
st.subheader("Dual-Axis Correlation Visualizer")

fig, ax1 = plt.subplots(figsize=(10, 3.5), facecolor='none')
ax1.set_facecolor('none')
sns.set_theme(style="whitegrid")

color = '#cc0000'
ax1.set_xlabel('Top-Up Start Date', fontweight='bold')
ax1.set_ylabel('Daily Burn Rate (HKD / Day)', color=color, fontweight='bold')
sns.barplot(data=analysis_df, x='Date', y='Daily_Burn_Rate_HKD', color=color, alpha=0.6, ax=ax1)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = '#0066cc'
ax2.set_ylabel('Observed Max Temperature (°C)', color=color, fontweight='bold')
sns.lineplot(data=analysis_df, x=range(len(analysis_df)), y='Max_Temp_C', color=color, marker='o', linewidth=2.5, ax=ax2)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
st.pyplot(fig)

# --- 6. PREDICTIVE MACHINE LEARNING FORECASTER ---
st.subheader("Step 6: Predictive Machine Learning Engine")
st.markdown("Adjust the weather simulation slider below to dynamically estimate your upcoming card balance strain.")

X_train = np.array([31.2, 32.5, 33.1, 32.8, 29.4]).reshape(-1, 1)
y_train = np.array([13.11, 11.75, 9.34, 11.29, 4.39])
model = LinearRegression().fit(X_train, y_train)

simulated_temp = st.slider("Simulated Next-Week Temperature Peak (°C)", min_value=24.0, max_value=38.0, value=33.0, step=0.5)

predicted_burn = model.predict(np.array([[simulated_temp]]))
estimated_weekly_total = predicted_burn * 7

col_pred1, col_pred2 = st.columns(2)
with col_pred1:
    st.info(f"Predicted Daily Cash Burn Velocity: ${predicted_burn[0]:.2f} HKD / Day")
with col_pred2:
    st.success(f"Suggested 7-Day Card Top-Up Target: ${estimated_weekly_total[0]:.2f} HKD")
