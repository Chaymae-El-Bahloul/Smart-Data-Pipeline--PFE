import streamlit as st
import json
import pandas as pd
import os
import time
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Smart IoT Adaptive AI Monitoring")
st.markdown("---")

history_file = "data/history.json"

# =====================
# SIDEBAR
# =====================

st.sidebar.header("Configuration")

limit_points = st.sidebar.slider("Points affichés", 50, 500, 200)

if st.sidebar.button("Reset Historique"):
    with open(history_file, "w") as f:
        json.dump([], f)
    st.sidebar.success("Historique réinitialisé")

placeholder = st.empty()

while True:

    try:
        with open(history_file, "r") as f:
            history = json.load(f)
    except:
        history = []

    if len(history) > 0:

        df = pd.DataFrame(history)

        df["moving_avg"] = df["temperature"].rolling(5).mean()

        df_recent = df.tail(limit_points)

        anomaly_rate = (df["anomaly"].sum() / len(df)) * 100

        # ===== Score IA simple (normalisation)
        ai_score = np.clip(
            (df["temperature"].mean() / 40) * 100,
            0, 100
        )

        with placeholder.container():

            # ================= KPIs =================
            st.header("KPIs Intelligents")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Messages", len(df))
            col2.metric("Temp Moyenne", round(df["temperature"].mean(), 2))

            if anomaly_rate > 20:
                col3.error(f"Taux Anomalie: {round(anomaly_rate,2)}%")
            else:
                col3.success(f"Taux Anomalie: {round(anomaly_rate,2)}%")

            col4.metric("Moteur Dominant", df["engine"].mode()[0])

            st.markdown("---")

            # ================= Gauge IA =================
            st.header("Score IA Global")

            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=ai_score,
                title={'text': "AI Stability Score"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'thickness': 0.3},
                    'steps': [
                        {'range': [0, 40], 'color': "red"},
                        {'range': [40, 70], 'color': "orange"},
                        {'range': [70, 100], 'color': "green"},
                    ],
                }
            ))

            st.plotly_chart(fig_gauge, use_container_width=True)

            st.markdown("---")

            # ================= Animation Courbe =================
            st.header("Evolution Température (Temps Réel)")

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                y=df_recent["temperature"],
                mode='lines',
                name='Température',
            ))

            fig.add_trace(go.Scatter(
                y=df_recent["moving_avg"],
                mode='lines',
                name='Moyenne Glissante',
                line=dict(dash='dash')
            ))

            fig.add_hline(y=30, line_dash="dot")

            fig.update_layout(height=400)

            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")

            # ================= Heatmap Anomalies =================
            st.header("Heatmap Anomalies")

            df["anomaly_numeric"] = df["anomaly"].astype(int)

            heatmap = px.density_heatmap(
                df,
                x=df.index,
                y="temperature",
                z="anomaly_numeric",
                nbinsx=30,
            )

            st.plotly_chart(heatmap, use_container_width=True)

            st.markdown("---")

            # ================= Performance simulée =================
            st.header("Comparaison Performance Simulée")

            pandas_perf = np.random.uniform(0.1, 0.5)
            spark_perf = np.random.uniform(0.05, 0.3)

            perf_df = pd.DataFrame({
                "Moteur": ["Pandas", "Spark"],
                "Temps (s)": [pandas_perf, spark_perf]
            })

            perf_fig = px.bar(
                perf_df,
                x="Moteur",
                y="Temps (s)",
            )

            st.plotly_chart(perf_fig, use_container_width=True)

    time.sleep(2)
