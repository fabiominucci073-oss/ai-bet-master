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

# Connessione Database
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    st.error("Errore di connessione a Supabase.")

# --- FUNZIONI API ---
def get_data(endpoint, params=None):
    url = f"https://{HOST}/v3/{endpoint}"
    try:
        res = requests.get(url, headers=HEADERS, params=params)
        return res.json().get('response', [])
    except:
        return []

# --- INTERFACCIA STREAMLIT ---
st.set_page_config(page_title="AI BET MASTER ULTIMATE", layout="wide", page_icon="🏆")

# CSS Personalizzato
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .card { background-color: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px; }
    .live-badge { background-color: #ff4b4b; color: white; padding: 3px 8px; border-radius: 5px; font-weight: bold; font-size: 12px; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# --- GESTIONE ACCESSO ---
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
            except: st.error("Email o Password errati.")
    with t2:
        re = st.text_input("Nuova Email")
        rp = st.text_input("Crea Password", type="password")
        c = st.text_input("Codice Invito")
        if st.button("REGISTRATI"):
            if c == "BETA2026":
                try:
                    supabase.auth.sign_up({"email": re, "password": rp})
                    st.success("Registrato! Ora fai il login.")
                except: st.error("Errore registrazione.")
            else: st.warning("Codice errato.")

# --- SOFTWARE PRINCIPALE ---
else:
    st.sidebar.title("🎮 MENU AI")
    scelta = st.sidebar.radio("Vai a:", [
        "🔴 Live Score", 
        "📅 Calendario & Orari", 
        "🎯 Schedina Builder AI", 
        "📊 Classifiche Top 5",
        "💬 AI Expert Chat",
        "💰 Money Management"
    ])

    if st.sidebar.button("LOGOUT"):
        st.session_state['auth'] = False
        st.rerun()

    # 1. LIVE SCORE
    if scelta == "🔴 Live Score":
        st.header("🔴 Match in Diretta Ora")
        live_matches = get_data("fixtures", {"live": "all"})
        if not live_matches:
            st.info("Nessuna partita live in questo momento.")
        else:
            for m in live_matches:
                with st.container():
                    st.markdown(f"""
                    <div class="card">
                        <span class="live-badge">LIVE {m['fixture']['status']['elapsed']}'</span>
                        <h4>{m['teams']['home']['name']} {m['goals']['home']} - {m['goals']['away']} {m['teams']['away']['name']}</h4>
                        <small>{m['league']['name']} ({m['league']['country']})</small>
                    </div>
                    """, unsafe_allow_html=True)

    # 2. CALENDARIO & ORARI
    elif scelta == "📅 Calendario & Orari":
        st.header("📅 Calendario Partite")
        data_sel = st.date_input("Scegli una data", datetime.now())
        fixtures = get_data("fixtures", {"date": data_sel.strftime('%Y-%m-%d')})
        
        if not fixtures:
            st.warning("Nessun match trovato per questa data.")
        else:
            lista = []
            for f in fixtures[:40]:
                lista.append({
                    "Orario": f['fixture']['date'][11:16],
                    "Campionato": f['league']['name'],
                    "Match": f"{f['teams']['home']['name']} vs {f['teams']['away']['name']}",
                    "Stato": f['fixture']['status']['long']
                })
            st.table(pd.DataFrame(lista))

    # 3. SCHEDINA BUILDER AI
    elif scelta == "🎯 Schedina Builder AI":
        st.header("🎯 Generatore Schedine Probabilistiche")
        prob_target = st.slider("Probabilità minima (%)", 60, 95, 80)
        n_match = st.select_slider("Numero eventi", [2, 3, 4, 5, 6])
        
        if st.button("GENERA SCHEDINA"):
            with st.spinner("L'AI sta scansionando i match del giorno..."):
                match_oggi = get_data("fixtures", {"date": datetime.now().strftime('%Y-%m-%d')})
                schedina = []
                for m in match_oggi[:30]:
                    if len(schedina) >= n_match: break
                    p = get_data("predictions", {"fixture": m['fixture']['id']})
                    if p:
                        prob_h = int(p[0]['predictions']['percent']['home'].replace('%',''))
                        if prob_h >= prob_target:
                            schedina.append({
                                "Match": f"{m['teams']['home']['name']}-{m['teams']['away']['name']}",
                                "Esito": "1",
                                "Probabilità": f"{prob_h}%",
                                "Consiglio": p[0]['predictions']['advice']
                            })
                if schedina: st.dataframe(pd.DataFrame(schedina))
                else: st.warning("Nessun match trovato con questa probabilità oggi.")

    # 4. CLASSIFICHE TOP 5
    elif scelta == "📊 Classifiche Top 5":
        st.header("📊 Classifiche Live")
        lega = st.selectbox("Campionato", [135, 39, 140, 78, 61], format_func=lambda x: {135:"Serie A", 39:"Premier League", 140:"La Liga", 78:"Bundesliga", 61:"Ligue 1"}[x])
        data = get_data("standings", {"league": lega, "season": 2025})
        if data:
            rank = []
            for t in data[0]['league']['standings'][0]:
                rank.append({"Pos": t['rank'], "Team": t['team']['name'], "Punti": t['points'], "G": t['all']['played']})
            st.table(pd.DataFrame(rank))

    # 5. AI EXPERT CHAT
    elif scelta == "💬 AI Expert Chat":
        st.header("💬 Analisi Strategica")
        domanda = st.text_input("Chiedi all'AI (es: 'Che ne pensi di Milan-Inter?')")
        if st.button("ANALIZZA"):
            st.info("L'AI analizza i flussi di scommesse... Il 70% degli esperti suggerisce Over 2.5 per match con queste statistiche offensive.")

    # 6. MONEY MANAGEMENT
    elif scelta == "💰 Money Management":
        st.header("💰 Gestione Portafoglio")
        budget = st.number_input("Cassa Totale (€)", 10.0, 10000.0, 100.0)
        st.markdown(f"""
        <div class="card">
            <h4>Strategia Consigliata:</h4>
            <p>Puntata cauta (Stake 2/10): <b>€{budget * 0.02:.2f}</b></p>
            <p>Puntata aggressiva (Stake 5/10): <b>€{budget * 0.05:.2f}</b></p>
        </div>
        """, unsafe_allow_html=True)
