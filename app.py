import streamlit as st
import requests
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, timedelta

# --- CONFIGURAZIONI ---
API_KEY = "281356f321msh431959f6e56b55cp1239b4jsn47bbee8cbdbc"
HOST = "api-football-v1.p.rapidapi.com"
HEADERS = {"x-rapidapi-host": HOST, "x-rapidapi-key": API_KEY}
SUPABASE_URL = "https://vipjocvnxdjoifkdaetz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpcGpvY3ZueGRqb2lma2RhZXR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkxMTY4MjksImV4cCI6MjA4NDY5MjgyOX0.n7EZCKiJOEZUHgwhJsCAt6Rh7hrkx3dQVl8SvwPwQbE" 

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    st.error("Errore Database.")

# --- MOTORE API POTENZIATO ---
def get_data(endpoint, params=None):
    url = f"https://{HOST}/v3/{endpoint}"
    try:
        res = requests.get(url, headers=HEADERS, params=params)
        return res.json().get('response', [])
    except:
        return []

# --- INTERFACCIA ---
st.set_page_config(page_title="AI BET MASTER ULTIMATE", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .card { background-color: #161b22; padding: 15px; border-radius: 12px; border-left: 5px solid #ff4b4b; margin-bottom: 10px; }
    .live-tag { background-color: #ff4b4b; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state['auth'] = False

# --- ACCESSO ---
if not st.session_state['auth']:
    st.title("🤖 AI Bet Master Ultimate")
    t1, t2 = st.tabs(["Login", "Registrati"])
    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ACCEDI"):
            try:
                supabase.auth.sign_in_with_password({"email": e, "password": p})
                st.session_state['auth'] = True
                st.rerun()
            except: st.error("Errore Login.")
    with t2:
        re = st.text_input("Nuova Email")
        rp = st.text_input("Crea Password", type="password")
        c = st.text_input("Codice Invito")
        if st.button("REGISTRATI"):
            if c == "BETA2026":
                try:
                    supabase.auth.sign_up({"email": re, "password": rp})
                    st.success("Registrato! Accedi ora.")
                except: st.error("Errore registrazione.")
            else: st.warning("Codice errato.")

# --- APP ---
else:
    st.sidebar.title("🎮 MENU AI")
    scelta = st.sidebar.radio("Naviga:", ["🏠 Dashboard", "🔴 Live Ora", "📅 Calendario", "🎯 Schedina AI", "📊 Classifiche"])
    
    if st.sidebar.button("DISCONNESSIONE"):
        st.session_state['auth'] = False
        st.rerun()

    # DASHBOARD GENERALE
    if scelta == "🏠 Dashboard":
        st.header("🏠 Panoramica del Giorno")
        col1, col2 = st.columns(2)
        with col1:
            st.info("Benvenuto! Usa il menu a sinistra per analizzare i match e generare schedine.")
        with col2:
            st.metric("Sistema AI", "Attivo", "v2.5")

    # MATCH LIVE
    elif scelta == "🔴 Live Ora":
        st.header("🔴 Partite in tempo reale")
        live = get_data("fixtures", {"live": "all"})
        if not live:
            st.write("Nessun match live importante al momento.")
        else:
            for m in live[:15]:
                st.markdown(f"""<div class="card">
                    <b>{m['league']['name']}</b><br>
                    {m['teams']['home']['name']} {m['goals']['home']} - {m['goals']['away']} {m['teams']['away']['name']} 
                    <span class="live-tag">{m['fixture']['status']['elapsed']}'</span>
                </div>""", unsafe_allow_html=True)

    # CALENDARIO (Migliorato)
    elif scelta == "📅 Calendario":
        st.header("📅 Match in programma")
        data_sel = st.date_input("Cambia data", datetime.now())
        # Cerchiamo tutti i match della data, non solo quelli NS
        fixtures = get_data("fixtures", {"date": data_sel.strftime('%Y-%m-%d')})
        if not fixtures:
            st.warning("Nessun match trovato. Prova a cambiare data.")
        else:
            for f in fixtures[:20]:
                with st.expander(f"{f['fixture']['date'][11:16]} - {f['teams']['home']['name']} vs {f['teams']['away']['name']}"):
                    st.write(f"Campionato: {f['league']['name']}")
                    st.write(f"Stato: {f['fixture']['status']['long']}")

    # SCHEDINA AI
    elif scelta == "🎯 Schedina AI":
        st.header("🎯 Analisi AI per Schedine")
        if st.button("Analizza match di oggi"):
            with st.spinner("L'AI sta calcolando..."):
                match_oggi = get_data("fixtures", {"date": datetime.now().strftime('%Y-%m-%d')})
                if not match_oggi:
                    st.error("Dati non disponibili per oggi. Riprova tra poco.")
                else:
                    count = 0
                    for m in match_oggi[:10]:
                        p = get_data("predictions", {"fixture": m['fixture']['id']})
                        if p:
                            st.success(f"**{m['teams']['home']['name']} - {m['teams']['away']['name']}**")
                            st.write(f"Consiglio: {p[0]['predictions']['advice']}")
                            count += 1
                    if count == 0: st.warning("L'AI non ha trovato match sicuri al momento.")

    # CLASSIFICHE
    elif scelta == "📊 Classifiche":
        st.header("📊 Ranking Campionati")
        lega = st.selectbox("Lega", [135, 39, 140, 78, 61], format_func=lambda x: {135:"Serie A", 39:"Premier League", 140:"La Liga", 78:"Bundesliga", 61:"Ligue 1"}[x])
        data = get_data("standings", {"league": lega, "season": 2025})
        if data:
            rank = [{"Pos": t['rank'], "Team": t['team']['name'], "Punti": t['points']} for t in data[0]['league']['standings'][0]]
            st.table(pd.DataFrame(rank))
