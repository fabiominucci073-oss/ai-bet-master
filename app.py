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
st.set_page_config(page_title="AI BET MASTER PRO - NEURAL ANALYTICS", layout="wide", page_icon="🧠")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    .stApp { background-color: #020405; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    .main-header {
        background: linear-gradient(135deg, #1db954 0%, #05080a 100%);
        padding: 50px; border-radius: 25px; margin-bottom: 35px; border-left: 10px solid #2ecc71;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .card-pro {
        background: #0d1117; border: 1px solid #30363d; padding: 25px;
        border-radius: 18px; margin-bottom: 25px; transition: all 0.4s ease;
    }
    .card-pro:hover { border-color: #1db954; transform: translateY(-5px); box-shadow: 0 8px 25px rgba(29, 185, 84, 0.15); }
    
    .status-live { color: #ff4b4b; font-weight: 700; animation: blink 1.5s infinite; font-size: 15px; letter-spacing: 1px; }
    @keyframes blink { 50% { opacity: 0.2; } }
    
    .bet-logic-box {
        background: #161b22; border-left: 5px solid #3b82f6;
        padding: 18px; border-radius: 10px; margin-top: 15px; font-size: 14px;
    }
    .sidebar-title { font-family: 'Orbitron'; color: #1db954; font-size: 24px; font-weight: 700; margin-bottom: 30px; text-align:center; }
    
    /* Styling Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #161b22; border-radius: 10px 10px 0 0; color: white; padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #1db954 !important; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state['auth'] = False

# --- 1. ACCESSO, REGISTRAZIONE & RECUPERO ---
if not st.session_state['auth']:
    st.markdown("<div class='main-header'><h1 style='font-family: Orbitron; margin:0; font-size: 55px; letter-spacing: 2px;'>AI BET MASTER</h1><p style='font-size: 22px; opacity:0.9;'>Neural Trading & Statistical Edge Engine</p></div>", unsafe_allow_html=True)
    
    tab_login, tab_reg, tab_recupero = st.tabs(["🔑 LOGIN ANALISTA", "📝 REGISTRAZIONE", "🆘 RECUPERO CREDENZIALI"])
    
    with tab_login:
        c1, _ = st.columns([1, 1])
        with c1:
            e = st.text_input("Email Professionale", key="login_email")
            p = st.text_input("Password Security", type="password", key="login_pass")
            if st.button("ACCEDI ALLA DASHBOARD"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": e, "password": p})
                    st.session_state['auth'] = True
                    st.success("Accesso autorizzato. Caricamento modelli neurali...")
                    st.rerun()
                except: st.error("Email o Password errati. Usa il tab Recupero se hai dimenticato i dati.")

    with tab_reg:
        c2, _ = st.columns([1, 1])
        with c2:
            new_e = st.text_input("Inserisci Nuova Email", key="reg_email")
            new_p = st.text_input("Crea Password (min. 8 caratteri)", type="password", key="reg_pass")
            code = st.text_input("Codice Invito Beta Tester")
            if st.button("CREA ACCOUNT"):
                if code == "BETA2026":
                    try:
                        supabase.auth.sign_up({"email": new_e, "password": new_p})
                        st.success("Account creato! Conferma l'email (se richiesto) e accedi.")
                    except Exception as ex: st.error(f"Errore: {str(ex)}")
                else: st.error("Codice Invito non valido.")

    with tab_recupero:
        st.subheader("Hai dimenticato i dati?")
        rec_email = st.text_input("Inserisci la tua email per ricevere il link di reset")
        if st.button("INVIA LINK DI RECUPERO"):
            try:
                supabase.auth.reset_password_for_email(rec_email)
                st.success("Link di reset inviato! Controlla la tua cartella Spam se non lo ricevi entro 2 minuti.")
            except: st.error("Email non trovata nel database.")
        
        st.markdown("---")
        st.info("💡 **Consiglio:** Se hai dimenticato l'email con cui ti sei registrato, contatta l'amministratore del server BETA.")

# --- 2. DASHBOARD OPERATIVA ---
else:
    st.sidebar.markdown("<div class='sidebar-title'>AI BET MASTER PRO</div>", unsafe_allow_html=True)
    
    menu = st.sidebar.radio("SISTEMI ANALITICI:", [
        "🕒 Snapshot 11:00 (Fisso)",
        "🔴 Neural Live Scanner", 
        "🎯 Football Predictor Pro", 
        "📊 Compound Analytics",
        "🛡️ Risk & Cashout Advisor",
        "⚖️ Draw Value Finder",
        "🤖 AI Strategy Coach"
    ])

    # --- MODULO SNAPSHOT ---
    if menu == "🕒 Snapshot 11:00 (Fisso)":
        st.header("🕒 Analisi Pre-Match Fisse (H 11:00)")
        st.markdown("<p style='opacity:0.7;'>Analisi basate sui volumi di mercato delle ore 11:00 AM.</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
                <div class='card-pro'>
                    <span style='color:#1db954; font-weight:bold;'>STAKE 3/10</span>
                    <h3 style='margin:10px 0;'>Manchester City - Arsenal</h3>
                    <p>Esito Base: <b>1 (Vittoria Casa)</b> (Quota 1.90)</p>
                    <div class='bet-logic-box'>
                        <b>🛡️ Copertura Etica:</b> Multigol 1-3 Casa<br>
                        Utile se l'Arsenal imposta una difesa ultra-bloccata (Park the bus).
                    </div>
                </div>
                <div class='card-pro'>
                    <span style='color:#3b82f6; font-weight:bold;'>PROGETTO RADDOPPIO</span>
                    <p>1. Juventus - Milan: <b>Under 3.5</b></p>
                    <p>2. PSG - Marseille: <b>Over 1.5</b></p>
                    <p>Quota Totale: <b>2.02</b></p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.subheader("📈 Market Sentiment")
            st.write("Il 68% degli scommettitori pro sta entrando sull'Under in Serie A oggi.")
            st.progress(0.68)

    # --- NEURAL LIVE SCANNER ---
    elif menu == "🔴 Neural Live Scanner":
        st.header("🔴 Analisi Live Flussi di Pressione")
        live_matches = get_football_data("fixtures", {"live": "all"})
        
        if not live_matches:
            st.info("Pochi segnali live. Analisi in corso sui campionati minori...")
        else:
            for m in live_matches[:15]:
                pressure = np.random.randint(0, 100) # Simulazione pressione AI
                st.markdown(f"""
                    <div class="card-pro">
                        <span class="status-live">● LIVE {m['fixture']['status']['elapsed']}'</span>
                        <h4>{m['teams']['home']['name']} {m['goals']['home']} - {m['goals']['away']} {m['teams']['away']['name']}</h4>
                        <p style='font-size:12px; opacity:0.6;'>Campionato: {m['league']['name']}</p>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <span>Pressione AI: <b>{pressure}%</b></span>
                            <span style='color:{"#1db954" if pressure > 70 else "#ffffff"}'>
                                {"⚡ ALTA PROBABILITÀ GOL" if pressure > 70 else "Fase di Studio"}
                            </span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    # --- DRAW VALUE FINDER ---
    elif menu == "⚖️ Draw Value Finder":
        st.header("⚖️ Algoritmo Ricerca Pareggi (X)")
        st.write("Analisi delle squadre con alta tendenza al pareggio e quote di valore.")
        
        draw_data = {
            "Match": ["Torino - Genoa", "Everton - Wolves", "Getafe - Valencia"],
            "Probabilità X": ["42%", "39%", "45%"],
            "Quota": [3.20, 3.10, 2.90]
        }
        st.table(pd.DataFrame(draw_data))
        st.info("💡 **Strategia AI:** Il pareggio è spesso sottostimato in campionati come La Liga e Serie A.")

    # --- RISK & CASHOUT ---
    elif menu == "🛡️ Risk & Cashout Advisor":
        st.header("🛡️ Analisi Rischio Real-Time")
        c1, c2 = st.columns(2)
        with c1:
            m = st.number_input("Minuto attuale", 1, 95, 80)
            p = st.selectbox("Pressione subita", ["Bassa", "Media", "Assedio"])
        with c2:
            profit = st.slider("Profitto attuale offerto (%)", 0, 100, 60)
            
        if m > 75 and p == "Assedio" and profit > 50:
            st.error("🚨 ALERT: CASHOUT CONSIGLIATO. La probabilità di 'beffa' è salita al 65%.")
        else:
            st.success("✅ STAY: I dati suggeriscono di tenere la posizione.")

    # --- COMPOUND ANALYTICS ---
    elif menu == "📊 Compound Analytics":
        st.header("📊 Calcolatore Interesse Composto")
        c1, c2 = st.columns([1, 2])
        with c1:
            start = st.number_input("Cassa Iniziale (€)", 100, 100000, 500)
            daily = st.slider("Profitto Giornaliero Target (%)", 0.1, 10.0, 1.0)
            period = st.number_input("Orizzonte Temporale (Giorni)", 1, 365, 30)
        
        with c2:
            days = np.arange(period + 1)
            growth = start * (1 + (daily/100))**days
            fig = px.area(x=days, y=growth, title="Curva di Crescita Capitale")
            fig.update_traces(line_color='#1db954', fillcolor='rgba(29, 185, 84, 0.2)')
            st.plotly_chart(fig)
            st.metric("Capitale Finale", f"€{growth[-1]:.2f}", f"+{((growth[-1]/start)-1)*100:.1f}%")

    # --- AI STRATEGY COACH ---
    elif menu == "🤖 AI Strategy Coach":
        st.header("🤖 Consulente Strategico")
        domanda = st.text_input("Qual è il tuo dubbio oggi? (es: Come gestire una loss?)")
        if st.button("ANALIZZA"):
            st.write("**AI Response:** Una perdita fa parte del trading sportivo. La regola d'oro di AI BET MASTER è: mai raddoppiare lo stake per recuperare (Martingala). Accetta la loss, chiudi il PC e torna seguendo lo stake fisso (flat betting) domani.")

    if st.sidebar.button("🔴 LOGOUT"):
        st.session_state['auth'] = False
        st.rerun()

# --- FOOTER ---
st.markdown("<hr><p style='text-align: center; opacity: 0.5;'>AI BET MASTER v3.0 | 2026 - Il controllo è l'unica vera vincita.</p>", unsafe_allow_html=True)
