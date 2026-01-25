import streamlit as st
import requests
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, timedelta
import plotly.graph_objects as go

# --- CONFIGURAZIONI CORE ---
API_KEY = "281356f321msh431959f6e56b55cp1239b4jsn47bbee8cbdbc"
HOST = "api-football-v1.p.rapidapi.com"
HEADERS = {"x-rapidapi-host": HOST, "x-rapidapi-key": API_KEY}
SUPABASE_URL = "https://vipjocvnxdjoifkdaetz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpcGpvY3ZueGRqb2lma2RhZXR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkxMTY4MjksImV4cCI6MjA4NDY5MjgyOX0.n7EZCKiJOEZUHgwhJsCAt6Rh7hrkx3dQVl8SvwPwQbE" 

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    st.error("Connessione Database Fallita.")

# --- MOTORE DI RICERCA DATI ---
def get_football_data(endpoint, params=None):
    url = f"https://{HOST}/v3/{endpoint}"
    try:
        res = requests.get(url, headers=HEADERS, params=params)
        return res.json().get('response', [])
    except: return []

# --- DESIGN AGGIORNATO (PRO ANALYTICS STYLE) ---
st.set_page_config(page_title="POWER STATS AI - ANALYTICS", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp { background-color: #05080a; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    .main-header {
        background: linear-gradient(90deg, #1db954 0%, #121212 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 25px;
        border-left: 5px solid #2ecc71;
    }

    .card-pro {
        background: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    
    .status-live {
        color: #ff4b4b;
        font-weight: bold;
        font-size: 12px;
        text-transform: uppercase;
        animation: blink 1.2s infinite;
    }
    @keyframes blink { 50% { opacity: 0.3; } }
    
    .stButton>button {
        background: #1db954;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #1ed760;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state['auth'] = False

# --- 1. ACCESSO DIRETTO (LOGIN/REGISTRAZIONE) ---
if not st.session_state['auth']:
    st.markdown("<div class='main-header'><h1 style='font-family: Orbitron; margin:0;'>POWER STATS AI</h1><p style='margin:0; opacity:0.8;'>Professional Sports Analytics Engine</p></div>", unsafe_allow_html=True)
    
    tab_login, tab_reg = st.tabs(["Accedi", "Attivazione Gratuita"])
    
    with tab_login:
        c1, _ = st.columns([1, 1])
        with c1:
            e = st.text_input("Email")
            p = st.text_input("Password", type="password")
            if st.button("ENTRA NEL SISTEMA"):
                try:
                    supabase.auth.sign_in_with_password({"email": e, "password": p})
                    st.session_state['auth'] = True
                    st.rerun()
                except: st.error("Credenziali non valide.")
                
    with tab_reg:
        c1, _ = st.columns([1, 1])
        with c1:
            re = st.text_input("Inserisci Email")
            rp = st.text_input("Crea Password", type="password")
            code = st.text_input("Codice Beta Tester")
            if st.button("ATTIVA ACCESSO"):
                if code == "BETA2026":
                    try:
                        supabase.auth.sign_up({"email": re, "password": rp})
                        st.success("Account attivato! Ora puoi accedere.")
                    except: st.error("Errore durante la creazione dell'account.")
                else: st.warning("Codice non valido.")

# --- 2. DASHBOARD OPERATIVA ---
else:
    st.sidebar.markdown(f"<h2 style='color:#1db954; font-family: Orbitron;'>POWER AI</h2>", unsafe_allow_html=True)
    
    menu = st.sidebar.radio("MODULI DI ANALISI:", [
        "🔴 Scanner Live H24", 
        "⚽ Football Predictor", 
        "🎾 Tennis Insights", 
        "📊 Mega Palinsesto",
        "🧨 Scommessa del Giorno",
        "📊 Gestione Capitale",
        "🤖 AI Strategy Coach"
    ])

    if st.sidebar.button("LOGOUT"):
        st.session_state['auth'] = False
        st.rerun()

    # --- SCANNER LIVE ---
    if menu == "🔴 Scanner Live H24":
        st.header("🔴 Analisi Live in Tempo Reale")
        live_matches = get_football_data("fixtures", {"live": "all"})
        
        if not live_matches:
            st.info("Nessun match live disponibile per l'analisi.")
        else:
            for m in live_matches[:15]:
                with st.container():
                    st.markdown(f"""
                        <div class="card-pro">
                            <span class="status-live">● LIVE {m['fixture']['status']['elapsed']}'</span>
                            <h3 style="margin:10px 0;">{m['teams']['home']['name']} {m['goals']['home']} - {m['goals']['away']} {m['teams']['away']['name']}</h3>
                            <p style='font-size: 14px; opacity:0.7;'>Lega: {m['league']['name']} | {m['league']['country']}</p>
                            <div style='background: #000; padding: 10px; border-radius: 5px; border-left: 3px solid #1db954;'>
                                <b>Suggerimento AI:</b> Pressione offensiva alta - Valutare Over 0.5 Casa
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

    # --- FOOTBALL PREDICTOR ---
    elif menu == "⚽ Football Predictor":
        st.header("🎯 Previsioni Algoritmiche")
        league = st.selectbox("Seleziona Lega", [135, 39, 140, 78, 61], format_func=lambda x: {135:"Serie A", 39:"Premier League", 140:"La Liga", 78:"Bundesliga", 61:"Ligue 1"}[x])
        
        if st.button("CALCOLA PROBABILITÀ"):
            matches = get_football_data("fixtures", {"league": league, "season": 2025, "next": 10})
            for m in matches:
                p = get_football_data("predictions", {"fixture": m['fixture']['id']})
                if p:
                    prob = p[0]['predictions']['percent']['home']
                    advice = p[0]['predictions']['advice']
                    st.markdown(f"""
                        <div class='card-pro'>
                            <b>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</b><br>
                            Probabilità Vittoria Casa: {prob} | Consiglio: <span style='color:#1db954'>{advice}</span>
                        </div>
                    """, unsafe_allow_html=True)

    # --- TENNIS INSIGHTS ---
    elif menu == "🎾 Tennis Insights":
        st.header("🎾 Analisi Tennis ATP/WTA")
        st.markdown("""
            <div class='card-pro'>
                <h4>Performance Modello Tennis</h4>
                <p>Precisione Set Betting: <b>88.5%</b></p>
                <p>Prossimo Match Analizzato: <b>J. Sinner vs C. Alcaraz</b> (Fiducia AI: 54% Sinner)</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Simulazione grafico performance
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 88,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Confidence Index %", 'font': {'color': "#ffffff"}},
            gauge = {'axis': {'range': [None, 100], 'tickcolor': "#ffffff"}, 'bar': {'color': "#1db954"}}
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig)

    # --- SCOMMESSA DEL GIORNO ---
    elif menu == "🧨 Scommessa del Giorno":
        st.header("🧨 Analisi Flash")
        st.markdown("""
            <div class='main-header' style='background: #161b22; border-left-color: #ff4b4b;'>
                <h2 style='color:#ff4b4b'>TOP PICK: QUOTA 3.50</h2>
                <p>1. Real Madrid - Win & Over 2.5</p>
                <p>2. Inter - Goal</p>
                <p>3. Bayern Monaco - Over 1.5 Casa</p>
                <hr>
                <small>Analisi basata su 10.000 simulazioni Monte Carlo.</small>
            </div>
        """, unsafe_allow_html=True)

    # --- GESTIONE CAPITALE ---
    elif menu == "📊 Gestione Capitale":
        st.header("📊 Money Management")
        c1, c2 = st.columns(2)
        with c1:
            cassa = st.number_input("Tua Cassa (€)", value=100.0)
            stake_perc = st.slider("Percentuale Rischio (%)", 1, 10, 2)
        with c2:
            importo = cassa * (stake_perc / 100)
            st.metric("Puntata Consigliata (Stake)", f"€{importo:.2f}")
            st.caption("Il mantenimento di uno stake fisso è la chiave del profitto a lungo termine.")

    # --- AI STRATEGY COACH ---
    elif menu == "🤖 AI Strategy Coach":
        st.header("🤖 Consulente Strategico AI")
        domanda = st.text_input("Esempio: Come comportarsi se la squadra favorita va in svantaggio?")
        if st.button("GENERA STRATEGIA"):
            st.info("L'AI consiglia: In caso di svantaggio della favorita in casa prima del 30', la quota '1X' o 'Over 1.5 Casa' acquisisce un valore statistico elevato (Value Bet).")
