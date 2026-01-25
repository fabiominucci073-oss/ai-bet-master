import streamlit as st
import requests
import pandas as pd
import numpy as np
from supabase import create_client, Client
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# --- CONFIGURAZIONI CORE ---
API_KEY = "281356f321msh431959f6e56b55cp1239b4jsn47bbee8cbdbc"
HOST = "api-football-v1.p.rapidapi.com"
HEADERS = {"x-rapidapi-host": HOST, "x-rapidapi-key": API_KEY}
SUPABASE_URL = "https://vipjocvnxdjoifkdaetz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpcGpvY3ZueDRqb2lma2RhZXR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkxMTY4MjksImV4cCI6MjA4NDY5MjgyOX0.n7EZCKiJOEZUHgwhJsCAt6Rh7hrkx3dQVl8SvwPwQbE" 

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    st.error("Connessione Database Fallita. Verifica le credenziali Supabase.")

# --- MOTORE DATI ---
def get_football_data(endpoint, params=None):
    url = f"https://{HOST}/v3/{endpoint}"
    try:
        res = requests.get(url, headers=HEADERS, params=params)
        return res.json().get('response', [])
    except: return []

# --- DESIGN SYSTEM AI BET MASTER ---
st.set_page_config(page_title="AI BET MASTER PRO", layout="wide", page_icon="🧠")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    .stApp { background-color: #05080a; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    .main-header {
        background: linear-gradient(90deg, #1db954 0%, #05080a 100%);
        padding: 40px; border-radius: 20px; margin-bottom: 30px; border-left: 8px solid #2ecc71;
    }
    .card-pro {
        background: #161b22; border: 1px solid #30363d; padding: 25px;
        border-radius: 15px; margin-bottom: 20px; transition: 0.4s;
    }
    .card-pro:hover { border-color: #1db954; box-shadow: 0 0 20px rgba(29, 185, 84, 0.2); }
    
    .status-live { color: #ff4b4b; font-weight: bold; animation: blink 1.2s infinite; font-size: 14px; }
    @keyframes blink { 50% { opacity: 0.3; } }
    
    .bet-logic-box {
        background: #0d1117; border-left: 4px solid #3b82f6;
        padding: 15px; border-radius: 8px; margin-top: 15px;
    }
    .sidebar-title { font-family: 'Orbitron'; color: #1db954; font-size: 22px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state['auth'] = False

# --- 1. ACCESSO & REGISTRAZIONE ---
if not st.session_state['auth']:
    st.markdown("<div class='main-header'><h1 style='font-family: Orbitron; margin:0; font-size: 50px;'>AI BET MASTER</h1><p style='font-size: 20px; opacity:0.8;'>Advanced Sports Trading Intelligence</p></div>", unsafe_allow_html=True)
    
    tab_login, tab_reg = st.tabs(["🔑 LOGIN ANALISTA", "📝 REGISTRAZIONE BETA"])
    
    with tab_login:
        c1, _ = st.columns([1, 1])
        with c1:
            e = st.text_input("Email Professionale")
            p = st.text_input("Password Security", type="password")
            if st.button("ACCEDI ALLA DASHBOARD"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": e, "password": p})
                    st.session_state['auth'] = True
                    st.rerun()
                except: st.error("Accesso negato. Controlla email o password.")

    with tab_reg:
        c2, _ = st.columns([1, 1])
        with c2:
            new_e = st.text_input("Inserisci Nuova Email")
            new_p = st.text_input("Crea Password (min. 6 caratteri)", type="password")
            code = st.text_input("Codice Invito Privato")
            if st.button("CREA ACCOUNT ANALISTA"):
                if code == "BETA2026":
                    try:
                        supabase.auth.sign_up({"email": new_e, "password": new_p})
                        st.success("Registrazione completata! Controlla la mail per confermare (se richiesto) e accedi.")
                    except: st.error("Errore durante la creazione. Email forse già esistente.")
                else: st.error("Codice Invito non valido.")

# --- 2. DASHBOARD OPERATIVA ---
else:
    st.sidebar.markdown("<div class='sidebar-title'>AI BET MASTER</div>", unsafe_allow_html=True)
    
    menu = st.sidebar.radio("SISTEMI ANALITICI:", [
        "🕒 Snapshot 11:00 (Automatibet)",
        "🔴 Scanner Live & Pressione", 
        "🎯 Football Predictor Pro", 
        "🎾 Tennis Insights Core", 
        "🛡️ Cashout & Risk Assistant",
        "📊 Compound Management",
        "🤖 Strategy Coach AI"
    ])

    # --- MODULO SNAPSHOT (FILOSOFIA AUTOMATIBET) ---
    if menu == "🕒 Snapshot 11:00 (Automatibet)":
        st.header("🕒 Selezioni Fisse delle 11:00 AM")
        st.markdown("")
        st.warning("Queste analisi sono generate una volta al giorno. L'analista etico le valida prima del match.")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
                <div class='card-pro'>
                    <span style='color:#1db954; font-weight:bold;'>STAKE CONSIGLIATO: 2%</span>
                    <h3>TOP SINGOLA: Liverpool - Chelsea</h3>
                    <p>Analisi: <b>Over 2.5</b> (Quota 1.72)</p>
                    <div class='bet-logic-box'>
                        <b>🛡️ Variante Cautelata: Multigol 2-4</b><br>
                        Protegge in caso di risultato esatto 1-1 o 2-0 / 0-2 (se integrato con MG 1-3).
                    </div>
                </div>
                <div class='card-pro'>
                    <span style='color:#3b82f6; font-weight:bold;'>RADDOPPIO STATISTICO</span>
                    <p>1. Napoli - Empoli: <b>1X + Over 1.5</b></p>
                    <p>2. Dortmund - Mainz: <b>1</b></p>
                    <p>Quota: <b>2.15</b></p>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.subheader("🛠 Algoritmo di Copertura")
            st.write("Trasforma un pronostico base in una selezione professionale.")
            pick_type = st.selectbox("Cosa hai analizzato?", ["Over 2.5", "Goal", "1", "Under 2.5"])
            if pick_type == "Over 2.5":
                st.info("💡 Prova: **Multigol 2-5** (Copre più varianti di punteggio alto)")
            elif pick_type == "Goal":
                st.info("💡 Prova: **Multigol 2-4** (Più stabile statisticamente)")

    # --- LIVE SCANNER ---
    elif menu == "🔴 Scanner Live & Pressione":
        st.header("🔴 Analisi Live Flussi di Pressione")
        live_matches = get_football_data("fixtures", {"live": "all"})
        
        if not live_matches:
            st.info("Nessun segnale rilevante al momento.")
        else:
            for m in live_matches[:12]:
                with st.container():
                    st.markdown(f"""
                        <div class="card-pro">
                            <span class="status-live">● LIVE {m['fixture']['status']['elapsed']}'</span>
                            <h4>{m['teams']['home']['name']} {m['goals']['home']} - {m['goals']['away']} {m['teams']['away']['name']}</h4>
                            <p>Lega: {m['league']['name']}</p>
                            <div style='background:#0d1117; padding:10px; border-radius:5px;'>
                                <b>Trend AI:</b> { "Pressione Casa Elevata" if m['goals']['home'] < 1 else "Fase di Stallo" }
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

    # --- CASHOUT & RISK ASSISTANT ---
    elif menu == "🛡️ Cashout & Risk Assistant":
        st.header("🛡️ Assistente Gestione Rischio")
        st.markdown("")
        
        c1, c2 = st.columns(2)
        with c1:
            minuto = st.slider("Minuto del match", 1, 90, 75)
            stato = st.selectbox("La tua scommessa è:", ["In Vantaggio", "In Bilico", "In Perdita"])
        with c2:
            pressione = st.select_slider("Pressione avversaria", ["Nulla", "Leggera", "Schiacciante"])
        
        if minuto > 70 and pressione == "Schiacciante" and stato == "In Vantaggio":
            st.error("🚨 AI SUGGESTS: CASHOUT IMMEDIATO. Probabilità di subire gol: 78%")
        else:
            st.success("✅ POSIZIONE SICURA. Il modello suggerisce di mantenere.")

    # --- COMPOUND MANAGEMENT ---
    elif menu == "📊 Compound Management":
        st.header("📊 Interesse Composto & Bankroll")
        
        col_m1, col_m2 = st.columns([1, 2])
        with col_m1:
            cassa_iniziale = st.number_input("Cassa Iniziale (€)", value=1000)
            profitto_giorno = st.slider("Target Giornaliero (%)", 0.5, 5.0, 1.5)
            giorni = st.number_input("Giorni di Trading", value=30)
        
        with col_m2:
            giorni_arr = np.arange(giorni + 1)
            valori = cassa_iniziale * (1 + (profitto_giorno/100))**giorni_arr
            fig = px.line(x=giorni_arr, y=valori, title="Proiezione Crescita Etica")
            fig.update_traces(line_color='#1db954')
            st.plotly_chart(fig)
            st.metric("Capitale Finale Stimato", f"€{valori[-1]:.2f}")

    # --- FOOTBALL PREDICTOR PRO ---
    elif menu == "🎯 Football Predict Pro":
        st.header("🎯 Analisi Predittiva Avanzata")
        liga = st.selectbox("Seleziona Campionato", [135, 39, 140, 78, 61, 94, 141], format_func=lambda x: {135:"Serie A", 39:"Premier League", 140:"La Liga", 78:"Bundesliga", 61:"Ligue 1", 94:"Primeira Liga", 141:"Serie B"}[x])
        
        if st.button("GENERA ANALISI DEEP"):
            fxt = get_football_data("fixtures", {"league": liga, "season": 2025, "next": 10})
            for f in fxt:
                p = get_football_data("predictions", {"fixture": f['fixture']['id']})
                if p:
                    st.markdown(f"""
                        <div class='card-pro'>
                            <b>{f['teams']['home']['name']} vs {f['teams']['away']['name']}</b><br>
                            Predizione AI: <span style='color:#1db954'>{p[0]['predictions']['advice']}</span><br>
                            Probabilità Home: {p[0]['predictions']['percent']['home']} | Draw: {p[0]['predictions']['percent']['draw']} | Away: {p[0]['predictions']['percent']['away']}
                        </div>
                    """, unsafe_allow_html=True)

    # --- STRATEGY COACH ---
    elif menu == "🤖 Strategy Coach AI":
        st.header("🤖 Coach Strategico")
        st.markdown("")
        q = st.text_input("Domanda al Coach (es: Come gestire una singola se la quota sale?)")
        if st.button("RICEVI CONSIGLIO"):
            st.info("Se la quota di una 'Singola Automatibet' sale di oltre lo 0.20 rispetto alle 11:00, l'analista deve ricontrollare le formazioni ufficiali. Se non ci sono assenze, il valore statistico è aumentato, ma il rischio di allibramento anomalo suggerisce di dimezzare lo stake.")

    if st.sidebar.button("LOGOUT / CHIUDI SESSIONE"):
        st.session_state['auth'] = False
        st.rerun()

# --- FOOTER ---
st.markdown("<p style='text-align: center; opacity: 0.5; margin-top: 50px;'>AI BET MASTER Professional v2.5 | 2026 Powered by Neural Networks</p>", unsafe_allow_html=True)


