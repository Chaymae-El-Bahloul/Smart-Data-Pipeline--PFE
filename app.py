import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest
import os
import time
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Smart Data Pipeline",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  THEME STATE
# ─────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

D = st.session_state.dark_mode

# ─────────────────────────────────────────────
#  THEME TOKENS
# ─────────────────────────────────────────────
if D:
    T = {
        "bg":          "#07090f",
        "card":        "#0f1923",
        "border":      "rgba(56,189,248,0.13)",
        "border2":     "rgba(56,189,248,0.32)",
        "text":        "#e8edf5",
        "muted":       "#5a6a80",
        "muted2":      "#8fa3b8",
        "accent":      "#38bdf8",
        "ac_rgb":      "56,189,248",
        "accent2":     "#10b981",
        "ac2_rgb":     "16,185,129",
        "accent3":     "#f59e0b",
        "ac3_rgb":     "245,158,11",
        "danger":      "#ef4444",
        "dan_rgb":     "239,68,68",
        "sb_bg":       "#0b1018",
        "sb_text":     "#d0e0f0",
        "sb_label":    "#38bdf8",
        "sb_input_bg": "#13202e",
        "sb_border":   "rgba(56,189,248,0.2)",
        "plot":        "plotly_dark",
        "plot_grid":   "rgba(56,189,248,0.06)",
        "hgrad":       "linear-gradient(135deg,#e2e8f0 0%,#38bdf8 55%,#10b981 100%)",
        "glow":        "0 0 30px rgba(56,189,248,0.06)",
    }
else:
    T = {
        "bg":          "#eef2f7",
        "card":        "#ffffff",
        "border":      "rgba(15,98,148,0.12)",
        "border2":     "rgba(15,98,148,0.30)",
        "text":        "#0f172a",
        "muted":       "#64748b",
        "muted2":      "#475569",
        "accent":      "#0369a1",
        "ac_rgb":      "3,105,161",
        "accent2":     "#059669",
        "ac2_rgb":     "5,150,105",
        "accent3":     "#d97706",
        "ac3_rgb":     "217,119,6",
        "danger":      "#dc2626",
        "dan_rgb":     "220,38,38",
        "sb_bg":       "#dde8f2",
        "sb_text":     "#1e293b",
        "sb_label":    "#0369a1",
        "sb_input_bg": "#f0f6fc",
        "sb_border":   "rgba(15,98,148,0.18)",
        "plot":        "plotly_white",
        "plot_grid":   "rgba(15,98,148,0.07)",
        "hgrad":       "linear-gradient(135deg,#0f172a 0%,#0369a1 55%,#059669 100%)",
        "glow":        "0 4px 20px rgba(3,105,161,0.07)",
    }

def rgba(rgb, a): return f"rgba({rgb},{a})"

# ─────────────────────────────────────────────
#  CSS — solution définitive sidebar
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;900&family=JetBrains+Mono:wght@400;600&display=swap');

/* ══ BASE ══ */
*, *::before, *::after {{ box-sizing: border-box; }}
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
section.main > div.block-container {{
    background: {T["bg"]} !important;
    color: {T["text"]} !important;
    font-family: 'Outfit', sans-serif !important;
}}
#MainMenu, footer, header, [data-testid="stDecoration"] {{ visibility: hidden !important; display: none !important; }}
.block-container {{ padding: 2rem 2.5rem 5rem !important; max-width: 1560px; }}
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: {T["bg"]}; }}
::-webkit-scrollbar-thumb {{ background: {T["accent"]}; border-radius: 2px; }}

/* ══ SIDEBAR — solution définitive ══ */
/* Fond */
[data-testid="stSidebar"] > div:first-child,
[data-testid="stSidebar"] {{
    background-color: {T["sb_bg"]} !important;
    border-right: 1px solid {T["sb_border"]} !important;
}}

/* TOUT le texte sans exception */
[data-testid="stSidebar"] *:not(button) {{
    color: {T["sb_text"]} !important;
    font-family: 'Outfit', sans-serif !important;
}}

/* Labels de widgets */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSlider p,
[data-testid="stSidebar"] .stNumberInput p,
[data-testid="stSidebar"] .stSelectbox p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
    color: {T["sb_text"]} !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}}
/* Inputs texte et nombre */
[data-testid="stSidebar"] input[type="number"],
[data-testid="stSidebar"] input[type="text"],
[data-testid="stSidebar"] input {{
    background: {T["sb_input_bg"]} !important;
    color: {T["sb_text"]} !important;
    border: 1px solid {T["sb_border"]} !important;
    border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important;
}}

/* Selectbox */
[data-testid="stSidebar"] [data-baseweb="select"] div,
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] input,
[data-testid="stSidebar"] [data-baseweb="select"] {{
    background: {T["sb_input_bg"]} !important;
    color: {T["sb_text"]} !important;
    border-color: {T["sb_border"]} !important;
}}

/* Slider valeurs */
[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] .stSlider [aria-label],
[data-testid="stSidebar"] .stSlider span {{
    color: {T["sb_text"]} !important;
}}
/* Slider track */
[data-testid="stSidebar"] [data-testid="stSlider"] div[data-baseweb="slider"] div {{
    background: {T["sb_border"]} !important;
}}
[data-testid="stSidebar"] [data-testid="stSlider"] div[role="slider"] {{
    background: {T["accent"]} !important;
    border-color: {T["accent"]} !important;
}}

/* Radio */
[data-testid="stSidebar"] [data-testid="stRadio"] label,
[data-testid="stSidebar"] [data-testid="stRadio"] p {{
    color: {T["sb_text"]} !important;
}}

/* Bouton générique sidebar */
[data-testid="stSidebar"] .stButton > button {{
    background: transparent !important;
    border: 1px solid {T["sb_border"]} !important;
    color: {T["sb_text"]} !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    border-radius: 9px !important;
    width: 100% !important;
    padding: 10px !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    border-color: {T["accent"]} !important;
    color: {T["accent"]} !important;
    background: {rgba(T["ac_rgb"], 0.07)} !important;
}}

/* Bouton theme toggle — classe spéciale */
[data-testid="stSidebar"] .theme-btn > div > button,
[data-testid="stSidebar"] .theme-btn button {{
    background: linear-gradient(135deg, {T["accent"]}, {T["accent2"]}) !important;
    border: none !important;
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 18px {rgba(T["ac_rgb"], 0.30)} !important;
}}
[data-testid="stSidebar"] .theme-btn button:hover {{
    opacity: 0.87 !important;
    transform: translateY(-1px) !important;
}}

/* Section headers */
.sb-sec {{
    display: flex;
    align-items: center;
    gap: 9px;
    margin: 1.3rem 0 0.6rem 0;
    padding-bottom: 6px;
    border-bottom: 1px solid {T["sb_border"]};
}}
.sb-bar {{
    width: 3px; height: 16px;
    border-radius: 2px;
    background: {T["accent"]};
    flex-shrink: 0;
}}
.sb-label {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    color: {T["sb_label"]} !important;
}}
/* ══ HEADER ══ */
.site-header {{
    position: relative;
    padding: 2.5rem 0 1.8rem 0;
    margin-bottom: 1.6rem;
}}
.site-header::after {{
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, {T["accent"]}, {T["accent2"]}, transparent);
    opacity: 0.3;
}}
.h-eyebrow {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 3.5px;
    text-transform: uppercase;
    color: {T["accent"]};
    margin-bottom: 14px;
    opacity: 0.85;
}}
.h-title {{
    font-family: 'Outfit', sans-serif;
    font-size: clamp(28px, 4vw, 52px);
    font-weight: 900;
    line-height: 1.0;
    background: {T["hgrad"]};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    margin: 0 0 10px 0;
}}
.h-sub {{
    font-size: 15px;
    font-weight: 300;
    color: {T["muted2"]};
    line-height: 1.6;
}}
.live-pill {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-top: 16px;
    background: {rgba(T["ac2_rgb"], 0.09)};
    border: 1px solid {rgba(T["ac2_rgb"], 0.26)};
    border-radius: 100px;
    padding: 6px 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: {T["accent2"]};
    letter-spacing: 1px;
}}
.live-dot {{
    width: 7px; height: 7px;
    border-radius: 50%;
    background: {T["accent2"]};
    animation: livepulse 1.6s ease-in-out infinite;
    flex-shrink: 0;
}}
@keyframes livepulse {{
    0%,100% {{ opacity:1; transform:scale(1); }}
    50%      {{ opacity:0.4; transform:scale(0.7); }}
}}

/* ══ ALERTES ══ */
.al {{ border-radius: 10px; padding: 13px 20px; font-family: 'JetBrains Mono', monospace; font-size: 12px; margin-bottom: 22px; display: block; }}
.al-ok   {{ background:{rgba(T["ac2_rgb"],0.07)}; border:1px solid {rgba(T["ac2_rgb"],0.22)}; border-left:3px solid {T["accent2"]}; color: {T["text"]}; }}
.al-warn {{ background:{rgba(T["ac3_rgb"],0.07)}; border:1px solid {rgba(T["ac3_rgb"],0.22)}; border-left:3px solid {T["accent3"]}; color: {T["text"]}; }}
.al-crit {{ background:{rgba(T["dan_rgb"],0.08)};  border:1px solid {rgba(T["dan_rgb"],0.25)};  border-left:3px solid {T["danger"]}; color: {T["text"]}; }}
@keyframes flicker {{ 0%,89%,91%,100% {{ opacity:1; }} 90% {{ opacity:0.6; }} }}

/* ══ SECTIONS ══ */
.sec-wrap {{ margin: 2.2rem 0 0.2rem 0; }}
.sec-title {{ font-family:'Outfit',sans-serif; font-size:18px; font-weight:700; color:{T["text"]}; display:flex; align-items:center; }}
.sec-dot {{ width:8px; height:8px; border-radius:50%; background:{T["accent"]}; flex-shrink:0; box-shadow:0 0 8px {T["accent"]}; }}
.sec-line {{ flex:1; height:1px; background:linear-gradient(90deg,{T["border2"]},transparent); }}
.sec-sub {{ font-size:13px; color:{T["muted"]}; margin:5px 0 18px 18px; font-weight:300; }}

/* ══ KPI ══ */
.kpi-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin:18px 0 8px 0; }}
.kpi-card {{
    position:relative; background:{T["card"]}; border:1px solid {T["border"]};
    border-radius:14px; padding:26px 22px 22px; overflow:hidden;
    transition:transform 0.25s cubic-bezier(0.34,1.56,0.64,1),border-color 0.25s,box-shadow 0.25s;
    box-shadow:{T["glow"]}; cursor:default;
}}
.kpi-card::before {{ content:''; position:absolute; top:0; left:0; right:0; height:3px; background:var(--kc); border-radius:14px 14px; }}
.kpi-card::after {{ content:attr(data-val); position:absolute; right:14px; bottom:-6px; font-family:'Outfit',sans-serif; font-weight: 900; font-size: 120px; opacity: 0; color: var(--ks); }}
.kpi-card:hover {{ transform:translateY(-5px) scale(1.02); border-color:var(--kc); box-shadow:0 14px 38px var(--ks); }}
.kpi-card:hover::after {{ opacity:0.08; }}
.kpi-label {{ font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{T["muted"]}; }}
.kpi-val {{ font-family:'Outfit',sans-serif; font-size:40px; font-weight:900; color:var(--kc); line-height:1; letter-spacing:-1px; }}
.kpi-unit {{ font-size:12px; color:{T["muted"]}; margin-top:8px; font-weight:300; }}

/* ══ PIPELINE ══ */
.pipe-row {{ display:flex; align-items:stretch; margin:18px 0; }}
.pipe-node {{ flex:1; background:{T["card"]}; border:1px solid {T["border"]}; border-radius:12px; padding:18px 12px; text-align:center; }}
.pipe-node:hover {{ border-color:{T["border2"]}; transform:translateY(-3px); }}
.pipe-tag {{ font-family:'JetBrains Mono',monospace; font-size:9px; letter-spacing:2px; text-transform:uppercase; color:{T["muted"]}; }}
.pipe-name {{ font-family:'Outfit',sans-serif; font-size:15px; font-weight:700; color:{T["text"]}; }}
.pipe-badge {{ display:inline-block; margin-top:9px; background:{rgba(T["ac2_rgb"],0.11)}; border:1px solid {rgba(T["ac2_rgb"],0.26)}; border-radius: 6px; padding: 4px 12px; font-size: 10px; color: {T["accent2"]}; }}
.pipe-conn {{ display:flex; align-items:center; justify-content:center; width:34px; flex-shrink:0; }}
.pipe-arrow {{ font-size:16px; color:{T["accent"]}; opacity:0.7; }}

/* ══ TABLE / DOWNLOAD ══ */
[data-testid="stDataFrame"] {{ border:1px solid {T["border"]} !important; border-radius:12px !important; overflow:hidden !important; }}
[data-testid="stDownloadButton"] button {{ background:transparent !important; border:1px solid {T["border2"]} !important; color:{T["text"]} !important; }}
[data-testid="stDownloadButton"] button:hover {{ background:{rgba(T["ac_rgb"],0.06)} !important; }}

/* ══ FOOTER ══ */
.site-footer {{ text-align:center; font-family:'JetBrains Mono',monospace; font-size:11px; color:{T["muted"]}; margin-top:4rem; padding: 2rem 0; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    # ── Toggle thème ──
    st.markdown('<div class="theme-btn">', unsafe_allow_html=True)
    label_btn = "☀️  Passer en mode Clair" if D else "🌙  Passer en mode Sombre"
    if st.button(label_btn, key="toggle_theme", use_container_width=True):
        st.session_state.dark_mode = not D
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Rafraîchissement ──
    st.markdown('<div class="sb-sec"><div class="sb-bar"></div><span class="sb-label">Rafraîchissement</span></div>', unsafe_allow_html=True)
    refresh_value = st.number_input("Intervalle", min_value=1, value=3, key="rv")
    refresh_unit  = st.selectbox("Unité de temps", ["Secondes", "Minutes", "Heures"], key="ru")
    mult = {"Secondes": 1, "Minutes": 60, "Heures": 3600}
    refresh_interval = refresh_value * mult[refresh_unit]

    # ── Données ──
    st.markdown('<div class="sb-sec"><div class="sb-bar"></div><span class="sb-label">Données</span></div>', unsafe_allow_html=True)
    max_records   = st.slider("Enregistrements affichés", 100, 2000, 500, key="mr")
    contamination = st.slider("Sensibilité anomalies", 0.01, 0.20, 0.05, step=0.01, key="co")

    # ── Système ──
    st.markdown('<div class="sb-sec"><div class="sb-bar"></div><span class="sb-label">Système</span></div>', unsafe_allow_html=True)
    if st.button("Réinitialiser les données", key="reset_btn", use_container_width=True):
        confirm = st.radio("Confirmer ?", ["Non", "Oui"], key="confirm_reset")
        if confirm == "Oui":
            with open("/app/data/history.json", "w") as f:
                json.dump([], f)
            st.success("Réinitialisé.")
            st.rerun()

# ─────────────────────────────────────────────
#  AUTO-REFRESH
# ─────────────────────────────────────────────
st_autorefresh(interval=refresh_interval * 1000, key="autorefresh")

# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────
history_file = "/app/data/history.json"
if not os.path.exists(history_file):
    st.warning("Pipeline actif — aucune donnée reçue.")
    st.stop()

for _ in range(3):
    try:
        with open(history_file, "r") as f:
            history = json.load(f)
        break
    except json.JSONDecodeError:
        time.sleep(0.2)
else:
    st.warning("Mise à jour en cours — veuillez patienter.")
    st.stop()

df = pd.DataFrame(history)
if df.empty:
    st.warning("Aucune donnée disponible.")
    st.stop()
df = df.tail(max_records).reset_index(drop=True)

# ─────────────────────────────────────────────
#  IA
# ─────────────────────────────────────────────
model = IsolationForest(contamination=contamination, random_state=42)
if len(df) > 20:
    model.fit(df[["temperature"]])
    df["anomaly"]  = model.predict(df[["temperature"]])
    df["anomaly"]  = df["anomaly"].apply(lambda x: 1 if x == -1 else 0)
    df["ia_score"] = model.decision_function(df[["temperature"]])
else:
    df["anomaly"]  = 0
    df["ia_score"] = 0.0

df["moving_avg"]  = df["temperature"].rolling(10).mean()
anomaly_count     = int(df["anomaly"].sum())
anomaly_rate      = round(anomaly_count / len(df) * 100, 1)
stability_score   = round((df["ia_score"].mean() + 0.5) * 100, 1)
temp_mean         = round(df["temperature"].mean(), 2)

c_anom = T["accent2"] if anomaly_count == 0 else T["accent3"] if anomaly_count < len(df)*0.10 else T["danger"]
r_anom = T["ac2_rgb"] if anomaly_count == 0 else T["ac3_rgb"] if anomaly_count < len(df)*0.10 else T["dan_rgb"]
c_stab = T["accent2"] if stability_score > 70 else T["accent3"] if stability_score > 40 else T["danger"]
r_stab = T["ac2_rgb"] if stability_score > 70 else T["ac3_rgb"] if stability_score > 40 else T["dan_rgb"]

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def sec(title, sub):
    st.markdown(f"""
    <div class="sec-wrap">
      <div class="sec-title"><span class="sec-dot"></span>{title}<span class="sec-line"></span></div>
      <p class="sec-sub">{sub}</p>
    </div>""", unsafe_allow_html=True)

LAYOUT = dict(
    template=T["plot"],
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="JetBrains Mono, monospace", color=T["muted2"], size=11),
    margin=dict(l=8, r=8, t=38, b=8),
    xaxis=dict(showgrid=False, zeroline=False, color=T["muted"]),
    yaxis=dict(showgrid=True, gridcolor=T["plot_grid"], zeroline=False, color=T["muted"]),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=T["border"], borderwidth=1),
)

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="site-header">
  <div class="h-eyebrow">Université Cadi Ayyad &nbsp;·&nbsp; EST El Kelâa des Sraghna &nbsp;·&nbsp; DUT Ingénierie des Données</div>
  <h1 class="h-title">Smart Data Pipeline</h1>
  <p class="h-sub">Plateforme intelligente de monitoring et d'analyse des flux IoT en temps réel — moteur auto-adaptatif Pandas&nbsp>
  <div class="live-pill"><span class="live-dot"></span>LIVE &nbsp;—&nbsp; {len(df)} enregistrements actifs</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  ALERTE
# ─────────────────────────────────────────────
if anomaly_count > len(df) * 0.25:
    msg = "ALERTE CRITIQUE"
    cls = "al-crit"
    icon = "&#9888;"

elif anomaly_count > len(df) * 0.10:
    msg = "ATTENTION — Taux en hausse"
    cls = "al-warn"
    icon = "&#9651;"

else:
    msg = "SYSTÈME NOMINAL — Pipeline opérationnel"
    cls = "al-ok"
    icon = "&#10003;"

st.markdown(f"""
<div class="al {cls}">
{icon} {msg} &nbsp;|&nbsp;
Taux d'anomalies : <strong>{anomaly_rate}%</strong>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  KPI
# ─────────────────────────────────────────────
sec("Indicateurs clés", "Métriques en temps réel du pipeline de traitement")
st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card" style="--kc:{T['accent']};--ks:{rgba(T['ac_rgb'],0.18)}" data-val="{len(df)}">
    <div class="kpi-label">Messages traités</div>
    <div class="kpi-val">{len(df)}</div>
    <div class="kpi-unit">enregistrements dans la fenêtre active</div>
  </div>
  <div class="kpi-card" style="--kc:{c_anom};--ks:{rgba(r_anom,0.18)}" data-val="{anomaly_count}">
    <div class="kpi-label">Anomalies détectées</div>
    <div class="kpi-val">{anomaly_count}</div>
    <div class="kpi-unit">{anomaly_rate}% du flux analysé</div>
  </div>
  <div class="kpi-card" style="--kc:{T['accent3']};--ks:{rgba(T['ac3_rgb'],0.18)}" data-val="{int(temp_mean)}">
    <div class="kpi-label">Température moyenne</div>
    <div class="kpi-val">{temp_mean}</div>
    <div class="kpi-unit">degrés Celsius — capteurs IoT</div>
  </div>
  <div class="kpi-card" style="--kc:{c_stab};--ks:{rgba(r_stab,0.18)}" data-val="{int(stability_score)}">
    <div class="kpi-label">Stabilité système</div>
    <div class="kpi-val">{stability_score}</div>
    <div class="kpi-unit">score global Isolation Forest</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PIPELINE
# ─────────────────────────────────────────────
sec("Architecture du pipeline", "Flux de données en temps réel — de l'ingestion à la visualisation")
st.markdown("""
<div class="pipe-row">
  <div class="pipe-node"><div class="pipe-tag">source</div><div class="pipe-name">Capteurs IoT</div><span class="pipe-badge">ACTIF</span></div>
  <div class="pipe-conn"><span class="pipe-arrow">&#8594;</span></div>
  <div class="pipe-node"><div class="pipe-tag">broker</div><div class="pipe-name">Apache Kafka</div><span class="pipe-badge">ACTIF</span></div>
  <div class="pipe-conn"><span class="pipe-arrow">&#8594;</span></div>
  <div class="pipe-node"><div class="pipe-tag">moteur adaptatif</div><div class="pipe-name">Pandas / Spark</div><span class="pipe-badge">ACTIF</span></div>
  <div class="pipe-conn"><span class="pipe-arrow">&#8594;</span></div>
  <div class="pipe-node"><div class="pipe-tag">intelligence artificielle</div><div class="pipe-name">Isolation Forest</div><span class="pipe-badge">ACTIF</span></div>
  <div class="pipe-conn"><span class="pipe-arrow">&#8594;</span></div>
  <div class="pipe-node"><div class="pipe-tag">visualisation</div><div class="pipe-name">Dashboard</div><span class="pipe-badge">ACTIF</span></div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  GRAPHIQUES
# ─────────────────────────────────────────────
sec("Évolution de la température", "Signal brut IoT et moyenne glissante sur 10 points")
fig_temp = go.Figure()
fig_temp.add_trace(go.Scatter(
    y=df["temperature"], mode="lines", name="Signal brut",
    line=dict(color=rgba(T["ac_rgb"], 0.45), width=1.5),
    fill="tozeroy", fillcolor=rgba(T["ac_rgb"], 0.05)
))
fig_temp.add_trace(go.Scatter(
    y=df["moving_avg"], mode="lines", name="Moyenne glissante",
    line=dict(color=T["accent"], width=2.5)
))
fig_temp.update_layout(**LAYOUT, title=dict(text="TEMPERATURE (°C)", font=dict(size=10, color=T["accent"]), x=0.01))
st.plotly_chart(fig_temp, use_container_width=True)

sec("Détection des anomalies", "Points normaux vs anomalies identifiées par Isolation Forest")
n_df = df[df["anomaly"] == 0]
a_df = df[df["anomaly"] == 1]
fig_anom = go.Figure()
fig_anom.add_trace(go.Scatter(x=n_df.index, y=n_df["temperature"], mode="markers", name="Normal",
    marker=dict(color=rgba(T["ac_rgb"], 0.6), size=5)))
fig_anom.add_trace(go.Scatter(x=a_df.index, y=a_df["temperature"], mode="markers", name="Anomalie",
    marker=dict(color=T["danger"], size=9, symbol="x", line=dict(width=2, color=T["danger"]))))
fig_anom.update_layout(**LAYOUT, title=dict(text="SCATTER — ANOMALIES ISOLATION FOREST", font=dict(size=10, color=T["accent"]), x=0.01))
st.plotly_chart(fig_anom, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    sec("Distribution des scores IA", "Histogramme des scores Isolation Forest")
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(x=df["ia_score"], nbinsx=40,
        marker=dict(color=rgba(T["ac_rgb"], 0.65), line=dict(color=T["border2"], width=0.5))))
    lh = {**LAYOUT}
    lh["xaxis"] = dict(showgrid=False, zeroline=True, zerolinecolor=rgba(T["dan_rgb"], 0.4), color=T["muted"])
    fig_hist.update_layout(**lh, title=dict(text="DECISION SCORE DISTRIBUTION", font=dict(size=10, color=T["accent"]), x=0.01))
    st.plotly_chart(fig_hist, use_container_width=True)
with col2:
    sec("Comparaison des moteurs", "Pandas vs Spark selon 3 axes de performance")
    fig_eng = go.Figure()
    cats = ["Performance", "Scalabilité", "Latence faible"]
    fig_eng.add_trace(go.Bar(name="Pandas", x=cats, y=[85, 40, 90],
        marker=dict(color=rgba(T["ac_rgb"], 0.7), line=dict(color=T["accent"], width=1))))
    fig_eng.add_trace(go.Bar(name="Spark", x=cats, y=[95, 95, 75],
        marker=dict(color=rgba(T["ac3_rgb"], 0.7), line=dict(color=T["accent3"], width=1))))
    le = {**LAYOUT}
    le["yaxis"] = dict(showgrid=True, gridcolor=T["plot_grid"], range=[0, 100], color=T["muted"])
    fig_eng.update_layout(**le, barmode="group",
        title=dict(text="MOTEURS — SCORE COMPARATIF", font=dict(size=10, color=T["accent"]), x=0.01))
    st.plotly_chart(fig_eng, use_container_width=True)

sec("Indicateur de stabilité globale", "Score synthétique basé sur l'analyse Isolation Forest")
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=stability_score,
    delta={"reference": 70, "valueformat": ".1f",
           "increasing": {"color": T["accent2"]}, "decreasing": {"color": T["danger"]}},
    number={"font": {"family": "Outfit", "size": 56, "color": T["text"]}, "suffix": ""},
    gauge={
        "axis": {"range": [0, 100], "tickcolor": T["muted"], "tickfont": {"size": 10, "color": T["muted"]}},
        "bar": {"color": c_stab, "thickness": 0.22},
        "bgcolor": "rgba(0,0,0,0)", "borderwidth": 0,
        "steps": [
            {"range": [0,  40],  "color": rgba(T["dan_rgb"],  0.12)},
            {"range": [40, 70],  "color": rgba(T["ac3_rgb"],  0.12)},
            {"range": [70, 100], "color": rgba(T["ac2_rgb"],  0.12)},
        ],
        "threshold": {"line": {"color": T["text"], "width": 2}, "thickness": 0.75, "value": 70}
    }
))
fig_gauge.update_layout(template=T["plot"], paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="JetBrains Mono, monospace", color=T["muted"]),
    height=290, margin=dict(l=30, r=30, t=10, b=10))
st.plotly_chart(fig_gauge, use_container_width=True)

# ─────────────────────────────────────────────
#  TABLE
# ─────────────────────────────────────────────
sec("Table des données traitées", "Derniers enregistrements enrichis — anomaly : 1 = anomalie détectée")
cols = [c for c in ["temperature","humidity","co","lpg","smoke","anomaly","ia_score"] if c in df.columns]
st.dataframe(df[cols], use_container_width=True, height=300)
st.download_button("Exporter le dataset (CSV)", df.to_csv(index=False), "smart_pipeline_data.csv", "text/csv")

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="site-footer">
  Smart Data Pipeline &mdash; Projet de Fin d'Études &mdash; Groupe G2<br>
  Université Cadi Ayyad &nbsp;·&nbsp; EST El Kelâa des Sraghna &nbsp;·&nbsp; 2025 / 2026
</div>
""", unsafe_allow_html=True)

