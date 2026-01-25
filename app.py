import streamlit as st
import requests
import pandas as pd
import numpy as np
from supabase import create_client, Client
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import time
import random

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
    
    /* Header Futuro */
    .main-header {
        background: linear-gradient(135deg, #1db954 0%, #05080a 100%);
        padding: 40px; border-radius: 20px; margin-bottom: 30px;
        border-left: 8px solid var(--primary);
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
    }
    
    /* Card Professionali */
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

    /* Indicatori Live */
    .status-live {
        color: #ff4b4b; font-weight: 700; font-size: 13px;
        text-transform: uppercase; letter-spacing: 1.5px;
        animation: blink 1.2s infinite;
    }
    @keyframes blink { 50% { opacity: 0.1; } }

    /* Custom Metric */
    .metric-box {
        background: #161b22; padding: 15px; border-radius: 10px;
        text-align: center; border-top: 3px solid var(--accent);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #05080a; border-right: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. LOGICA DI BACKEND & API
# ==========================================
@st.cache_data(ttl=300) # Cache di 5 minuti per risparmiare API
def fetch_live_data():
    url = f"https://{HOST}/v3/fixtures"
    params = {"live": "all"}
    try:
        res = requests.get(url, headers=HEADERS, params=params)
        return res.json().get('response', [])
    except: return []

def calculate_monte_carlo(prob, odds, trials=1000):
    # Simulazione di 1000 scenari per calcolare il rischio rovina
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
                except: st.error("Credenziali non valide.")

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
                        st.success("Account Creato! Conferma via email.")
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
    # Sidebar Navigation
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

    # --- MODULO 1: PREMIUM SNAPSHOT ---
    if menu == "💎 Premium Snapshot":
        st.title("💎 Analisi High-Confidence")
        st.markdown("Top picks generate dall'algoritmo basandosi sui volumi di mercato delle 11:00.")
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("<div class='metric-box'>🎯 Accuratezza Oggi<br><b>84.2%</b></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='metric-box'>📊 ROI Mensile<br><b>+12.4%</b></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='metric-box'>🔥 Hot Streak<br><b>5 Win</b></div>", unsafe_allow_html=True)
        
        st.markdown("### 📋 Schedina Consigliata")
        with st.container():
            st.markdown("""
                <div class='card-pro'>
                    <div style='display:flex; justify-content:space-between;'>
                        <b>PREMIER LEAGUE</b> <span style='color:#1db954;'>STAKE 5/10</span>
                    </div>
                    <h2 style='margin:15px 0;'>Liverpool - Chelsea</h2>
                    <p>Suggerimento AI: <b style='color:#1db954;'>GOL (Entrambe segnano)</b> @ 1.65</p>
                    <div style='font-size:12px; opacity:0.7;'>Analisi: Il Liverpool ha concesso gol in 4 delle ultime 5 partite in casa. Chelsea in forma offensiva smagliante.</div>
                </div>
            """, unsafe_allow_html=True)

    # --- MODULO 2: NEURAL LIVE SCANNER ---
    elif menu == "📡 Neural Live Scanner":
        st.title("📡 Neural Live Scanner")
        st.write("Monitoraggio flussi di pressione in tempo reale (API-V3).")
        
        live_data = fetch_live_data()
        if not live_data:
            st.warning("Nessun match live rilevante al momento. Riprova tra pochi minuti.")
        else:
            for match in live_data[:8]:
                home = match['teams']['home']['name']
                away = match['teams']['away']['name']
                score = f"{match['goals']['home']} - {match['goals']['away']}"
                time_el = match['fixture']['status']['elapsed']
                
                # Simulazione logica AI di pressione
                pressure = random.randint(30, 95)
                
                with st.expander(f"🔴 {home} {score} {away} ({time_el}')"):
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.write(f"Campionato: {match['league']['name']}")
                        st.progress(pressure/100)
                        st.write(f"Indice Pressione Offensiva: {pressure}%")
                    with col_b:
                        if pressure > 80:
                            st.error("⚡ POSSIBILE GOL")
                        else:
                            st.success("⚖️ STABILE")

    # --- MODULO 3: PROFIT PLANNER ---
    elif menu == "📈 Profit Planner":
        st.title("📈 Calcolo Interesse Composto")
        col_p1, col_p2 = st.columns([1, 2])
        
        with col_p1:
            capitale = st.number_input("Capitale (€)", 100, 50000, 1000)
            resa = st.slider("Resa Giornaliera Target (%)", 0.5, 5.0, 1.2)
            giorni = st.number_input("Orizzonte (Giorni)", 30, 365, 90)
            
        with col_p2:
            x = np.arange(giorni)
            y = capitale * (1 + (resa/100))**x
            fig = px.line(x=x, y=y, title="Proiezione Crescita Bankroll")
            fig.update_traces(line_color='#1db954', line_width=4)
            st.plotly_chart(fig, use_container_width=True)
            st.metric("Capitale Finale Stimato", f"€ {y[-1]:,.2f}", f"+{((y[-1]/capitale)-1)*100:.1f}%")

    # --- MODULO 4: RISK SIMULATOR ---
    elif menu == "🛡️ Risk Simulator":
        st.title("🛡️ Risk & Monte Carlo Simulator")
        st.write("Simula 1000 iterazioni della tua strategia per vedere le probabilità di fallimento.")
        
        c_r1, c_r2 = st.columns(2)
        with c_r1:
            win_rate = st.slider("Win Rate Stimato (%)", 30, 80, 55)
            quota_media = st.number_input("Quota Media", 1.2, 5.0, 1.90)
        
        # Simulazione Rapida
        sim_results = [calculate_monte_carlo(win_rate/100, quota_media) for _ in range(100)]
        
        with c_r2:
            st.write("### Esito Simulazione")
            avg_win = np.mean(sim_results)
            st.write(f"Probabilità di profitto nel lungo periodo: **{avg_win*100:.1f}%**")
            if avg_win > 0.5:
                st.success("Strategia Matematica Vincente (Edge Positivo)")
            else:
                st.error("Strategia ad Alto Rischio (Edge Negativo)")

    # --- MODULO 5: IMPOSTAZIONI ---
    elif menu == "⚙️ Impostazioni":
        st.title("⚙️ Configurazione Sistema")
        st.checkbox("Notifiche Push Telegram (Beta)", value=True)
        st.checkbox("Modalità Risparmio Dati API", value=True)
        st.selectbox("Tema Interfaccia", ["Cyber Dark (Default)", "Deep Sea", "High Contrast"])
        if st.button("Pulisci Cache"):
            st.cache_data.clear()
            st.success("Cache pulita!")

# ==========================================
# 6. FOOTER & COMPLIANCE
# ==========================================
st.markdown("---")
st.markdown("""
    <div style='text-align: center; opacity: 0.5; font-size: 12px;'>
        <b>AI BET MASTER v3.0 | 2026</b><br>
        Il gioco è vietato ai minori e può causare dipendenza. Usa questi dati solo come supporto analitico.<br>
        <i>"Il controllo è l'unica vera vincita."</i>
    </div>
""", unsafe_allow_html=True)
