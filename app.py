import streamlit as st
import json
import pandas as pd
import time
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(layout="wide")

# ======================
# THEME SELECTOR
# ======================

theme_mode = st.sidebar.selectbox("Mode d'affichage", ["Sombre", "Clair"])

if theme_mode == "Sombre":
    bg_color = "#0E1117"
    card_bg = "#1C1F26"
    text_color = "white"
    border_color = "#2A2D34"
    plot_bg = "#1C1F26"
    axis_color = "white"
else:
    bg_color = "#FFFFFF"
    card_bg = "#F3F6FA"
    text_color = "#111111"
    border_color = "#E0E0E0"
    plot_bg = "#FFFFFF"
    axis_color = "black"

st.markdown(f"""
<style>
body {{
    background-color: {bg_color};
}}

.card {{
    background-color: {card_bg};
    padding: 22px;
    border-radius: 14px;
    border: 1px solid {border_color};
    text-align: center;
}}

.card h2 {{
    margin: 0;
    font-size: 30px;
    color: {text_color};
}}

.card p {{
    margin: 6px 0 0 0;
    font-size: 14px;
    color: {text_color};
}}
</style>
""", unsafe_allow_html=True)

st.title("Smart IoT Adaptive AI Monitoring")
st.markdown("---")

history_file = "data/history.json"

# ======================
# SIDEBAR CONFIG
# ======================

limit_points = st.sidebar.slider("Points affichés", 50, 500, 200)

time_value = st.sidebar.number_input("Fréquence de mise à jour", min_value=1, value=10)
time_unit = st.sidebar.selectbox("Unité", ["Secondes", "Minutes", "Heures"])

if time_unit == "Secondes":
    refresh_rate = time_value
elif time_unit == "Minutes":
    refresh_rate = time_value * 60
else:
    refresh_rate = time_value * 3600

st.sidebar.markdown("---")

# ======================
# RESET WITH CONFIRMATION
# ======================

if "confirm_reset" not in st.session_state:
    st.session_state.confirm_reset = False

if "reset_done" not in st.session_state:
    st.session_state.reset_done = False

if st.sidebar.button("Réinitialiser les données"):
    st.session_state.confirm_reset = True

if st.session_state.confirm_reset:
    st.sidebar.warning("⚠ Voulez-vous vraiment supprimer toutes les données ?")

    col1, col2 = st.sidebar.columns(2)

    if col1.button("Confirmer"):
        with open(history_file, "w") as f:
            json.dump([], f)
        st.session_state.confirm_reset = False
        st.session_state.reset_done = True
        st.rerun()

    if col2.button("Annuler"):
        st.session_state.confirm_reset = False

if st.session_state.reset_done:
    st.sidebar.success("Historique supprimé avec succès.")
    st.session_state.reset_done = False

# ======================
# LOAD DATA
# ======================

if not os.path.exists(history_file):
    os.makedirs("data", exist_ok=True)
    with open(history_file, "w") as f:
        json.dump([], f)

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
    mean_temp = df["temperature"].mean()
    ai_score = 100 - anomaly_rate
    dominant_engine = df["engine"].mode()[0]

    # ================= KPIs =================

    st.header("Indicateurs Clés")

    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f"<div class='card'><h2>{len(df)}</h2><p>Total Messages</p></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='card'><h2>{round(mean_temp,2)}°C</h2><p>Température Moyenne</p></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='card'><h2>{round(anomaly_rate,2)}%</h2><p>Anomalies IA</p></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='card'><h2>{dominant_engine}</h2><p>Moteur Dominant</p></div>", unsafe_allow_html=True)

    st.markdown("---")

    # ================= COURBE =================

    st.header("Evolution Température")

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df_recent["temperature"], mode='lines', name='Température'))
    fig.add_trace(go.Scatter(y=df_recent["moving_avg"], mode='lines', name='Moyenne glissante', line=dict(dash='dash')))

    fig.update_layout(height=400, plot_bgcolor=plot_bg, paper_bgcolor=plot_bg, font=dict(color=axis_color))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ================= SCORE IA =================

    st.header("Score IA Global")

    if ai_score < 50:
        color = "red"
    elif ai_score < 80:
        color = "orange"
    else:
        color = "green"

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=ai_score,
        number={'suffix': " /100"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': color}}
    ))

    fig_gauge.update_layout(height=350, plot_bgcolor=plot_bg, paper_bgcolor=plot_bg, font=dict(color=axis_color))
    st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("---")

    # ================= HEATMAP =================

    st.header("Heatmap des anomalies")

    df["anomaly_numeric"] = df["anomaly"].astype(int)

    heatmap = px.density_heatmap(
        df,
        x=df.index,
        y="temperature",
        z="anomaly_numeric",
        nbinsx=30,
        color_continuous_scale="Viridis"
    )

    heatmap.update_layout(height=400, plot_bgcolor=plot_bg, paper_bgcolor=plot_bg, font=dict(color=axis_color))
    st.plotly_chart(heatmap, use_container_width=True)

    st.markdown("---")

    # ================= MOTEURS =================

    st.header("Répartition des moteurs")

    engine_counts = df["engine"].value_counts().reset_index()
    engine_counts.columns = ["Moteur", "Count"]

    engine_fig = px.bar(engine_counts, x="Moteur", y="Count", text_auto=True, color="Moteur")
    engine_fig.update_layout(height=350, plot_bgcolor=plot_bg, paper_bgcolor=plot_bg, font=dict(color=axis_color))

    st.plotly_chart(engine_fig, use_container_width=True)

else:
    st.info("Aucune donnée disponible.")

time.sleep(refresh_rate)
st.rerun()
