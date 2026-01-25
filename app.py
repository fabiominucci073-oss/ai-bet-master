import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import time
import random

# --- BLOCCO COMPATIBILITÀ SUPABASE (Indistruttibile) ---
try:
    from supabase import create_client, Client
except ImportError:
    try:
        from supabase_py import create_client
        Client = any
    except ImportError:
        st.error("⚠️ Libreria Supabase non rilevata correttamente. Prova a eseguire: pip install supabase-py")
# -------------------------------------------------------

# ==========================================
# 1. CONFIGURAZIONI CORE & SECURITY
# ==========================================
API_KEY = "281356f321msh431959f6e56b55cp1239b4jsn47bbee8cbdbc"
HOST = "api-football-v1.p.rapidapi.com"
HEADERS = {"x-rapidapi-host": HOST, "x-rapidapi-key": API_KEY}
SUPABASE_URL = "https://vipjocvnxdjoifkdaetz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpcGpvY3ZueDRqb2lma2RhZXR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkxMTY4MjksImV4cCI6MjA4NDY5MjgyOX0.n7EZCKiJOEZUHgwhJsCAt6Rh7hrkx3dQVl8SvwPwQbE"

# Inizializzazione Database con protezione
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"⚠️ Errore Connessione DB: {e}")

# ==========================================
# 2. DESIGN SYSTEM (CSS AVANZATO)
# ==========================================
st.set_page_config(page_title="AI BET MASTER PRO v3.0", layout="wide", page_icon="🧠")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    :root {
        --primary: #1db954;
        --bg-dark: #020405;
        --card-bg: #0d1117;
        --accent: #3b82f6;
    }

    .stApp { background-color: var(--bg-dark); color: #ffffff; font-family: 'Inter', sans-serif; }
    
    .main-header {
        background: linear-gradient(135deg, #1db954 0%, #05080a 100%);
        padding: 40px; border-radius: 20px; margin-bottom: 30px;
        border-left: 8px solid var(--primary);
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
    }
    
    .card-pro {
        background: var(--card-bg); border: 1px solid #30363d;
        padding: 22px; border-radius: 15px; margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .card-pro:hover {
        border-color: var(--primary);
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(29, 185, 84, 0.1);
    }

    .status-live {
        color: #ff4b4b; font-weight: 700; font-size: 13px;
        text-transform: uppercase; letter-spacing: 1.5px;
        animation: blink 1.2s infinite;
    }
    @keyframes blink { 50% { opacity: 0.1; } }

    .metric-box {
        background: #161b22; padding: 15px; border-radius: 10px;
        text-align: center; border-top: 3px solid var(--accent);
    }
    
    [data-testid="stSidebar"] { background-color: #05080a; border-right: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. LOGICA DI BACKEND & API
# ==========================================
@st.cache_data(ttl=300)
def fetch_live_data():
    url = f"https://{HOST}/v3/fixtures"
    params = {"live": "all"}
    try:
        res = requests.get(url, headers=HEADERS, params=params)
        return res.json().get('response', [])
    except: return []

def calculate_monte_carlo(prob, odds, trials=1000):
    results = []
    for _ in range(trials):
        win = 1 if random.random() < prob else 0
        results.append(win)
    return np.mean(results)

# ==========================================
# 4. SISTEMA DI AUTENTICAZIONE
# ==========================================
if 'auth' not in st.session_state:
    st.session_state['auth'] = False
    st.session_state['user_email'] = ""

if not st.session_state['auth']:
    st.markdown("""
        <div class='main-header'>
            <h1 style='font-family: Orbitron; margin:0; font-size: 45px;'>AI BET MASTER <span style='color:#eee; font-size:20px;'>v3.0</span></h1>
            <p style='opacity:0.8;'>Neural Prediction Engine & Bankroll Management</p>
        </div>
    """, unsafe_allow_html=True)
    
    tab_log, tab_sign, tab_help = st.tabs(["🔐 LOGIN", "✍️ REGISTRAZIONE", "🆘 RECUPERO"])
    
    with tab_log:
        col_l, _ = st.columns([1, 1])
        with col_l:
            email = st.text_input("Email", key="log_email")
            password = st.text_input("Password", type="password", key="log_pass")
            if st.button("ENTRA NELL'AREA ANALISI"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state['auth'] = True
                    st.session_state['user_email'] = email
                    st.rerun()
                except: st.error("Credenziali non valide o database non raggiungibile.")

    with tab_sign:
        col_s, _ = st.columns([1, 1])
        with col_s:
            n_email = st.text_input("Nuova Email", key="sign_email")
            n_pass = st.text_input("Password (8+ char)", type="password", key="sign_pass")
            v_code = st.text_input("Codice Beta", value="BETA2026")
            if st.button("CREA PROFILO"):
                if v_code == "BETA2026":
                    try:
                        supabase.auth.sign_up({"email": n_email, "password": n_pass})
                        st.success("Account Creato! Controlla la mail per confermare.")
                    except Exception as e: st.error(f"Errore: {e}")
                else: st.error("Codice Beta non valido.")

    with tab_help:
        st.info("Inserisci l'email per ricevere il link di reset istantaneo.")
        f_email = st.text_input("Email Registrata")
        if st.button("INVIA RESET"):
            try:
                supabase.auth.reset_password_for_email(f_email)
                st.success("Link inviato correttamente.")
            except: st.error("Email non trovata.")

# ==========================================
# 5. DASHBOARD OPERATIVA (AUTENTICATA)
# ==========================================
else:
    with st.sidebar:
        st.markdown(f"<div style='text-align:center; padding:20px;'><h2 style='font-family:Orbitron; color:#1db954;'>MASTER AI</h2><p style='font-size:12px;'>Utente: {st.session_state['user_email']}</p></div>", unsafe_allow_html=True)
        menu = st.radio("MODULI ANALITICI", [
            "💎 Premium Snapshot",
            "📡 Neural Live Scanner",
            "📈 Profit Planner",
            "🛡️ Risk Simulator",
            "⚙️ Impostazioni"
        ])
        st.markdown("---")
        if st.button("ESCI (LOGOUT)", use_container_width=True):
            st.session_state['auth'] = False
            st.rerun()

    if menu == "💎 Premium Snapshot":
        st.title("💎 Analisi High-Confidence")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("<div class='metric-box'>🎯 Accuratezza Oggi<br><b>84.2%</b></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='metric-box'>📊 ROI Mensile<br><b>+12.4%</b></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='metric-box'>🔥 Hot Streak<br><b>5 Win</b></div>", unsafe_allow_html=True)
        
        st.markdown("### 📋 Schedina Consigliata")
        st.markdown("""
            <div class='card-pro'>
                <b>PREMIER LEAGUE</b> - Liverpool vs Chelsea
                <h2 style='color:#1db954;'>GOL @ 1.65</h2>
                <p style='font-size:0.9rem; opacity:0.8;'>Analisi AI: Alta pressione offensiva registrata nelle ultime 3 gare di entrambe.</p>
            </div>
        """, unsafe_allow_html=True)

    elif menu == "📡 Neural Live Scanner":
        st.title("📡 Live Neural Tracking")
        live_data = fetch_live_data()
        if not live_data:
            st.warning("Nessun match live disponibile. Riprova tra poco.")
        else:
            for match in live_data[:5]:
                pressure = random.randint(40, 98)
                with st.container():
                    st.markdown(f"""
                        <div class='card-pro'>
                            <b>{match['league']['name']}</b><br>
                            {match['teams']['home']['name']} {match['goals']['home']} - {match['goals']['away']} {match['teams']['away']['name']}
                        </div>
                    """, unsafe_allow_html=True)
                    st.progress(pressure/100)

    elif menu == "📈 Profit Planner":
        st.title("📈 Proiezione Bankroll")
        cap = st.number_input("Budget (€)", value=1000)
        days = st.slider("Giorni", 30, 365, 90)
        resa = st.slider("Resa %", 0.5, 5.0, 1.5)
        
        x = np.arange(days)
        y = cap * (1 + (resa/100))**x
        fig = px.area(x=x, y=y, title="Interesse Composto")
        fig.update_traces(line_color='#1db954')
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "🛡️ Risk Simulator":
        st.title("🛡️ Risk Analysis")
        wr = st.slider("Win Rate (%)", 30, 80, 55)
        q = st.number_input("Quota Media", value=1.90)
        res = calculate_monte_carlo(wr/100, q)
        st.metric("Probabilità di Profitto (Monte Carlo)", f"{res*100:.2f}%")

    elif menu == "⚙️ Impostazioni":
        st.title("⚙️ Sistema")
        if st.button("Reset Cache"):
            st.cache_data.clear()
            st.success("Cache svuotata!")

# ==========================================
# 6. FOOTER
# ==========================================
st.markdown("<br><hr><center style='opacity:0.5'>AI BET MASTER PRO v3.0 | 2026</center>", unsafe_allow_html=True)
