import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ==============================================================================
# ⚙️ TOPUP BACKEND LOGIC CORE ENGINE
# ==============================================================================

# 1. Initialize State Storage Context Layer
if 'custom_data' not in st.session_state:
    st.session_state['custom_data'] = None

# 2. Hardcoded Baseline Log Ledger Matrix
raw_baseline = """Date,Time,Amount_HKD
2026-05-29,06:07,20.0
2026-05-30,18:44,50.0
2026-06-04,00:53,20.0
2026-06-06,04:18,20.0
2026-06-07,22:49,50.0
2026-06-19,07:56,0.0"""

# 3. Pull either custom user dataset upload or fall back to verified base log
if st.session_state['custom_data'] is not None:
    df = st.session_state['custom_data']
else:
    df = pd.read_csv(io.StringIO(raw_baseline))

# 4. Data Refinement Pipeline (Clears hidden whitespace padding keys)
df.columns = df.columns.str.strip()

# 5. Delta Interval Calculations (Hours and Days Elapsed Velocity)
df['Timestamp'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str))
df = df.sort_values('Timestamp').reset_index(drop=True)
df['Hours_Lasted'] = (df['Timestamp'].shift(-1) - df['Timestamp']).dt.total_seconds() / 3600
df['Days_Lasted'] = df['Hours_Lasted'] / 24
df['Daily_Burn_Rate_HKD'] = df['Amount_HKD'] / df['Days_Lasted']

# 6. Sai Kung / Clear Water Bay Regional Weather History Coordinates Mapping
historical_weather = pd.DataFrame({
    'Date': ['2026-05-29', '2026-05-30', '2026-06-04', '2026-06-06', '2026-06-07'],
    'Max_Temp_C': [31.2, 32.5, 33.1, 32.8, 29.4]
})
analysis_df = pd.merge(df, historical_weather, on='Date', how='inner')

# 7. Algorithmic Polyfit Weights Extraction (Machine Learning Model)
x_train_arr = np.array([31.2, 32.5, 33.1, 32.8, 29.4])
y_train_arr = np.array([13.11, 11.75, 9.34, 11.29, 4.39])
slope, intercept = np.polyfit(x_train_arr, y_train_arr, 1)

# 8. Export Metrics Variables Context Dictionary for Frontend Mapping Injection
st.session_state['topup_engine'] = {
    'max_burn': float(analysis_df['Daily_Burn_Rate_HKD'].max()),
    'avg_burn': float(analysis_df['Daily_Burn_Rate_HKD'].mean()),
    'correlation': 0.64,
    'ledger_df': analysis_df[['Date', 'Amount_HKD', 'Days_Lasted', 'Daily_Burn_Rate_HKD', 'Max_Temp_C']],
    'ml_slope': slope,
    'ml_intercept': intercept
}

# ==============================================================================
# 🎨 PASTE YOUR LOVABLE HTML/CSS FRONTEND ELEMENTS DIRECTLY BELOW THIS LINE
# ==============================================================================
st.info("Backend data architecture ready. Please paste your custom Lovable UI elements directly below this card.")
import { createFileRoute, Link } from "@tanstack/react-router";
import { AnimatePresence, motion } from "motion/react";
import { useEffect, useState } from "react";
import { NavBar } from "@/components/NavBar";
import { UploadDropzone } from "@/components/UploadDropzone";
import { METRICS } from "@/lib/topup-data";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "TopUp — Microclimate Spend Forecasting" },
      { name: "description", content: "Weather-aware machine learning for student residence card top-ups." },
    ],
  }),
  component: Index,
});

const EMOJIS = ["☀️", "🌧️", "🌈", "☁️", "🪷", "🏖️"];

function Loader({ onDone }: { onDone: () => void }) {
  const [i, setI] = useState(0);
  useEffect(() => {
    const each = 5000 / EMOJIS.length;
    const t = setInterval(() => {
      setI((v) => {
        if (v + 1 >= EMOJIS.length) {
          clearInterval(t);
          setTimeout(onDone, each);
          return v + 1;
        }
        return v + 1;
      });
    }, each);
    return () => clearInterval(t);
  }, [onDone]);

  return (
    <motion.div
      exit={{ opacity: 0, scale: 1.05 }}
      transition={{ duration: 0.6 }}
      className="fixed inset-0 z-50 grid place-items-center bg-gradient-sunset-soft"
    >
      <div className="flex flex-col items-center gap-8">
        <div className="relative grid h-40 w-40 place-items-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
            className="absolute inset-0 rounded-full bg-gradient-sunset opacity-30 blur-2xl"
          />
          <AnimatePresence mode="wait">
            <motion.span
              key={i}
              initial={{ scale: 0.4, opacity: 0, y: 20 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.6, opacity: 0, y: -20 }}
              transition={{ duration: 0.4, ease: [0.2, 0.8, 0.2, 1] }}
              className="text-7xl"
            >
              {EMOJIS[Math.min(i, EMOJIS.length - 1)]}
            </motion.span>
          </AnimatePresence>
        </div>
        <div className="flex flex-col items-center gap-2">
          <div className="font-display text-3xl font-bold text-gradient-sunset">TopUp</div>
          <div className="text-sm text-muted-foreground">Warming up the forecast</div>
        </div>
      </div>
    </motion.div>
  );
}

function MetricCard({ label, value, unit, delay = 0 }: { label: string; value: string; unit?: string; delay?: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay }}
      whileHover={{ y: -4 }}
      className="glass-card group relative overflow-hidden rounded-3xl p-6"
    >
      <div className="absolute -right-10 -top-10 h-32 w-32 rounded-full bg-gradient-sunset opacity-0 blur-2xl transition group-hover:opacity-30" />
      <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{label}</div>
      <div className="mt-3 flex items-baseline gap-1">
        <span className="font-display text-4xl font-bold tracking-tight sm:text-5xl">{value}</span>
        {unit && <span className="text-sm font-medium text-muted-foreground">{unit}</span>}
      </div>
    </motion.div>
  );
}

function Index() {
  const [loading, setLoading] = useState(true);

  return (
    <>
      <AnimatePresence>{loading && <Loader onDone={() => setLoading(false)} />}</AnimatePresence>

      <div className={loading ? "pointer-events-none opacity-0" : "opacity-100 transition-opacity duration-700"}>
        <NavBar />

        {/* Hero */}
        <section className="relative mx-auto max-w-6xl px-4 pt-16 pb-24 sm:pt-24 sm:pb-32">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: loading ? 0 : 1, y: loading ? 30 : 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="flex flex-col items-center text-center"
          >
            <span className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-white/60 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-primary backdrop-blur">
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-primary" />
              Live - Founded June 2026
            </span>
            <h1 className="mt-6 font-display text-6xl font-bold leading-[0.95] tracking-tight sm:text-7xl md:text-8xl">
              Forecast your <br />
              <span className="text-gradient-sunset">residence spend.</span>
            </h1>
            <p className="mt-6 max-w-2xl text-base text-muted-foreground sm:text-lg">
              TopUp analyzes the microclimate of rooms in student residences. By combining
              real-time financial reload data with local temperature, it anticipates your
              expenses using machine learning.
            </p>
            <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
              <motion.div whileHover={{ scale: 1.04, y: -2 }} whileTap={{ scale: 0.96 }}>
                <Link
                  to="/data"
                  className="inline-flex items-center gap-2 rounded-full bg-gradient-sunset px-6 py-3 font-semibold text-primary-foreground shadow-elevated transition hover:shadow-glow"
                >
                  Explore the forecast
                </Link>
              </motion.div>
              <motion.div whileHover={{ scale: 1.04, y: -2 }} whileTap={{ scale: 0.96 }}>
                <Link
                  to="/table"
                  className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-white/60 px-6 py-3 font-semibold text-foreground backdrop-blur transition hover:bg-white"
                >
                  See the log
                </Link>
              </motion.div>
            </div>

            <a
              href="https://github.com/sherine111"
              target="_blank"
              rel="noreferrer"
              className="mt-10 inline-flex items-center gap-2 text-sm text-muted-foreground transition hover:text-foreground"
            >
              <span className="grid h-7 w-7 place-items-center rounded-full bg-foreground text-xs text-background">
              </span>
              Crafted by <span className="font-semibold text-foreground">@sherine111</span>
            </a>
          </motion.div>
        </section>

        {/* Portfolio Metrics */}
        <section className="mx-auto max-w-6xl px-4 pb-20">
          <div className="mb-8 flex items-end justify-between gap-4">
            <div>
              <div className="text-xs font-semibold uppercase tracking-wider text-primary">
                Overview
              </div>
              <h2 className="mt-2 font-display text-4xl font-bold sm:text-5xl">
                Portfolio metrics
              </h2>
            </div>
            <Link
              to="/table"
              className="hidden text-sm font-semibold text-primary hover:underline sm:inline"
            >
              View full log →
            </Link>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <MetricCard label="Max Daily Burn Velocity" value={`$${METRICS.maxDailyBurn}`} unit="HKD / day" delay={0} />
            <MetricCard label="Avg Summer Burn Rate" value={`$${METRICS.avgSummerBurn}`} unit="HKD / day" delay={0.1} />
            <MetricCard label="Heat Correlation" value={METRICS.heatCorrelation.toFixed(2)} unit="r-coef" delay={0.2} />
          </div>
        </section>

        {/* Two pages */}
        <section className="mx-auto max-w-6xl px-4 pb-20">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <PageCard
              to="/data"
              emoji="📈"
              eyebrow="The data one"
              title="ML Forecast Canvas"
              body="Slide the simulated heat dial and watch tomorrow's spend re-price in real time."
              tint="from-sunset-amber to-sunset-coral"
            />
            <PageCard
              to="/table"
              emoji="📊"
              eyebrow="The table one"
              title="Top-Up Log"
              body="Every reload, days lasted, daily burn and room temperature in one tidy ledger."
              tint="from-sunset-rose to-sunset-lavender"
            />
          </div>
        </section>

        {/* Upload */}
        <section className="mx-auto max-w-6xl px-4 pb-24">
          <UploadDropzone />
        </section>

        <footer className="border-t border-border/60 py-8 text-center text-xs text-muted-foreground">
          TopUp · est. June 2026 · made with sunsets by{" "}
          <a className="font-semibold text-foreground hover:underline" href="https://github.com/sherine111" target="_blank" rel="noreferrer">
            @sherine111
          </a>
        </footer>
      </div>
    </>
  );
}

function PageCard({
  to,
  emoji,
  eyebrow,
  title,
  body,
  tint,
}: {
  to: "/data" | "/table";
  emoji: string;
  eyebrow: string;
  title: string;
  body: string;
  tint: string;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
      whileHover={{ y: -6 }}
    >
      <Link
        to={to}
        className="group relative block overflow-hidden rounded-3xl glass-card p-8 transition hover:shadow-elevated"
      >
        <div className={`absolute -right-16 -top-16 h-48 w-48 rounded-full bg-gradient-to-br ${tint} opacity-40 blur-2xl transition group-hover:opacity-70`} />
        <div className="relative">
          <div className="text-5xl">{emoji}</div>
          <div className="mt-6 text-xs font-semibold uppercase tracking-wider text-primary">
            {eyebrow}
          </div>
          <h3 className="mt-2 font-display text-3xl font-bold">{title}</h3>
          <p className="mt-3 max-w-md text-sm text-muted-foreground">{body}</p>
          <div className="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-primary">
            Open
            <motion.span
              className="inline-block"
              initial={{ x: 0 }}
              whileHover={{ x: 4 }}
            >
              →
            </motion.span>
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
