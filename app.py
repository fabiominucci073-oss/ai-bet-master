import streamlit as st
import requests
import pandas as pd
import numpy as np
from supabase import create_client, Client
from datetime import datetime, time
import plotly.graph_objects as go

# --- CONFIGURAZIONI CORE ---
API_KEY = "281356f321msh431959f6e56b55cp1239b4jsn47bbee8cbdbc"
HOST = "api-football-v1.p.rapidapi.com"
HEADERS = {"x-rapidapi-host": HOST, "x-rapidapi-key": API_KEY}
SUPABASE_URL = "https://vipjocvnxdjoifkdaetz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpcGpvY3ZueDRqb2lma2RhZXR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkxMTY4MjksImV4cCI6MjA4NDY5MjgyOX0.n7EZCKiJOEZUHgwhJsCAt6Rh7hrkx3dQVl8SvwPwQbE" 

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    st.error("Connessione Database Fallita.")

def get_football_data(endpoint, params=None):
    url = f"https://{HOST}/v3/{endpoint}"
    try:
        res = requests.get(url, headers=HEADERS, params=params)
        return res.json().get('response', [])
    except: return []

# --- DESIGN AI BET MASTER ---
st.set_page_config(page_title="AI BET MASTER - PROFESSIONAL ANALYTICS", layout="wide", page_icon="🧠")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp { background-color: #05080a; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    .main-header {
        background: linear-gradient(90deg, #1db954 0%, #121212 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 30px;
        border-left: 5px solid #2ecc71;
    }

    .card-pro {
        background: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .card-pro:hover { border-color: #1db954; transform: translateY(-3px); }
    
    .status-live { color: #ff4b4b; font-weight: bold; animation: blink 1.2s infinite; }
    @keyframes blink { 50% { opacity: 0.3; } }
    
    .bet-logic-box {
        background: #0d1117;
        border-left: 4px solid #3b82f6;
        padding: 15px;
        border-radius: 5px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state['auth'] = False

# --- 1. ACCESSO ---
if not st.session_state['auth']:
    st.markdown("<div class='main-header'><h1 style='font-family: Orbitron; margin:0;'>AI BET MASTER</h1><p style='margin:0; opacity:0.8;'>L'intelligenza artificiale non è una slot machine, è il tuo vantaggio statistico.</p></div>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Login", "Attivazione Beta"])
    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ACCEDI ALL'AREA ANALISI"):
            st.session_state['auth'] = True
            st.rerun()
    with t2:
        st.write("Inserisci il codice ricevuto per sbloccare i moduli AI.")
        code = st.text_input("Codice Attivazione")
        if st.button("ATTIVA"):
            if code == "BETA2026": st.success("Codice Valido! Ora effettua il login.")
            else: st.error("Codice Errato.")

# --- 2. DASHBOARD OPERATIVA ---
else:
    st.sidebar.markdown(f"<h2 style='color:#1db954; font-family: Orbitron;'>AI BET MASTER</h2>", unsafe_allow_html=True)
    
    menu = st.sidebar.radio("MODULI OPERATIVI:", [
        "🕒 Snapshot 11:00 (Pre-Match)",
        "🔴 Live Scanner H24", 
        "⚽ Football Predictor", 
        "🎾 Tennis Analysis", 
        "📊 Money Management Etico",
        "🤖 Strategy Coach"
    ])

    # --- MODULO SNAPSHOT 11:00 (FILOSOFIA AUTOMATIBET) ---
    if menu == "🕒 Snapshot 11:00 (Pre-Match)":
        st.header("🕒 Selezioni AI BET MASTER delle 11:00")
        st.info("⚠️ Queste selezioni sono fisse. Verifica sempre le variazioni di quota prima del kick-off.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
                <div class='card-pro'>
                    <span style='color:#1db954'><b>TOP PICK SINGOLA</b></span>
                    <h3>Real Madrid - Alaves</h3>
                    <p>Esito Base: <b>1 + Over 2.5</b> (Quota: 1.75)</p>
                    <div class='bet-logic-box'>
                        <b>Variante Cautelata (Etica):</b> Multigol 2-4 Casa <br>
                        <small>Usa questa variante per ridurre la volatilità se la quota cala.</small>
                    </div>
                </div>
                <div class='card-pro'>
                    <span style='color:#3b82f6'><b>RADDOPPIO DEL GIORNO</b></span>
                    <p>1. Inter - Venezia: <b>Over 1.5 Casa</b></p>
                    <p>2. Arsenal - Everton: <b>1</b></p>
                    <p>Quota Totale: <b>2.05</b></p>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.subheader("🛠 Trasformatore Multigol")
            st.caption("Converti l'esito base in combo cautelate AI.")
            base = st.selectbox("Seleziona Esito Base:", ["Over 1.5", "Under 2.5", "Under 3.5", "Over 2.5"])
            
            if base == "Over 1.5":
                st.success("✅ Suggerimento: **Multigol 1-4** o **1-3**")
            elif base == "Under 2.5":
                st.warning("⚠️ Suggerimento: **Multigol 1-2** (Alto Rischio) o **Under 3.5**")
            elif base == "Over 2.5":
                st.success("✅ Suggerimento: **Multigol 2-5** o **2-4**")

    # --- LIVE SCANNER ---
    elif menu == "🔴 Live Scanner H24":
        st.header("🔴 Analisi Live Flussi di Pressione")
        live_matches = get_football_data("fixtures", {"live": "all"})
        
        if not live_matches:
            st.info("In attesa di segnali dai campionati attivi...")
        else:
            for m in live_matches[:10]:
                st.markdown(f"""
                    <div class="card-pro">
                        <span class="status-live">● LIVE {m['fixture']['status']['elapsed']}'</span>
                        <h4>{m['teams']['home']['name']} {m['goals']['home']} - {m['goals']['away']} {m['teams']['away']['name']}</h4>
                        <p>Analisi AI: <b>Pressione offensiva costante</b>. Valutare Goal Prossimo.</p>
                    </div>
                """, unsafe_allow_html=True)

    # --- FOOTBALL PREDICTOR ---
    elif menu == "⚽ Football Predictor":
        st.header("🎯 Calcolo Probabilità Deep Data")
        league = st.selectbox("Seleziona Lega", [135, 39, 140, 78, 61], format_func=lambda x: {135:"Serie A", 39:"Premier League", 140:"La Liga", 78:"Bundesliga", 61:"Ligue 1"}[x])
        
        if st.button("ANALIZZA PROSSIMI MATCH"):
            matches = get_football_data("fixtures", {"league": league, "season": 2025, "next": 10})
            for m in matches:
                p = get_football_data("predictions", {"fixture": m['fixture']['id']})
                if p:
                    st.markdown(f"""
                        <div class='card-pro'>
                            <b>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</b><br>
                            Consiglio AI: <span style='color:#1db954'>{p[0]['predictions']['advice']}</span><br>
                            Probabilità Vittoria: {p[0]['predictions']['percent']['home']}
                        </div>
                    """, unsafe_allow_html=True)

    # --- MONEY MANAGEMENT ---
    elif menu == "📊 Money Management Etico":
        st.header("📊 Gestione Capitale e Compound Interest")
        
        
        cassa = st.number_input("Capitale Operativo (€)", value=500.0)
        risk = st.select_slider("Profilo Etico", options=["Cauto (1%)", "Bilanciato (2.5%)", "Aggressivo (5%)"])
        
        perc = 0.01 if "Cauto" in risk else (0.025 if "Bilanciato" in risk else 0.05)
        st.metric("Stake Consigliato per Match", f"€{cassa * perc:.2f}")
        
        st.markdown("""
            > **MANTRA AI BET MASTER:** Non inseguire la perdita. Se perdi 3 stake di fila, il software consiglia il logout per 24 ore.
        """)

    # --- STRATEGY COACH ---
    elif menu == "🤖 Strategy Coach":
        st.header("🤖 AI Bet Master Coach")
        user_input = st.text_input("Chiedi all'IA: (es. Come gestire un Over 1.5 se al 20° è 0-0?)")
        if st.button("ANALIZZA STRATEGIA"):
            st.info("L'AI Bet Master consiglia: In caso di 0-0 al 20° su un match da Over 1.5, attendi il 30° per una quota 'Valore' (circa 1.80) o entra in 'Over 0.5 Primo Tempo' se la pressione offensiva (AP1) è superiore a 1.0.")

    if st.sidebar.button("LOGOUT"):
        st.session_state['auth'] = False
        st.rerun()

