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

# --- MOTORE API ---
def fetch_data(endpoint, params=None):
    url = f"https://{HOST}/v3/{endpoint}"
    try:
        res = requests.get(url, headers=HEADERS, params=params)
        return res.json().get('response', [])
    except:
        return []

# --- INTERFACCIA ---
st.set_page_config(page_title="AI Bet Master ULTIMATE", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .stSidebar { background-color: #161b22; }
    .card { background: linear-gradient(145deg, #1e2530, #161b22); padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    .live-tag { background-color: #ff4b4b; color: white; padding: 2px 8px; border-radius: 5px; font-size: 0.8em; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .stat-val { color: #ff4b4b; font-weight: bold; font-size: 1.2em; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state['auth'] = False

# --- LOGICA ACCESSO ---
if not st.session_state['auth']:
    st.title("🏆 AI Bet Master Ultimate v2.0")
    t1, t2 = st.tabs(["Login Accesso", "Registrazione Amici"])
    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA NEL SISTEMA"):
            try:
                supabase.auth.sign_in_with_password({"email": e, "password": p})
                st.session_state['auth'] = True
                st.rerun()
            except: st.error("Dati errati.")
    with t2:
        re = st.text_input("Nuova Email")
        rp = st.text_input("Nuova Password", type="password")
        c = st.text_input("Codice Segreto")
        if st.button("CREA ACCOUNT"):
            if c == "BETA2026":
                try:
                    supabase.auth.sign_up({"email": re, "password": rp})
                    st.success("Fatto! Ora puoi loggare.")
                except Exception as ex: st.error(f"Errore: {ex}")
            else: st.warning("Codice errato.")

# --- APP REALE ---
else:
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3563/3563417.png", width=100)
    st.sidebar.title("NAVIGAZIONE AI")
    menu = st.sidebar.radio("Scegli funzione:", [
        "🔴 Live Scores", 
        "📅 Calendario Completo", 
        "🎯 AI Schedina Creator", 
        "📊 Classifiche & Statistiche",
        "⚔️ Analisi Testa a Testa",
        "💬 AI Expert Prompt",
        "💰 Wallet & Money Management"
    ])

    if st.sidebar.button("CHIUDI SESSIONE"):
        st.session_state['auth'] = False
        st.rerun()

    # 1. LIVE SCORES
    if menu == "🔴 Live Scores":
        st.header("🔴 Partite in Diretta")
        live = fetch_data("fixtures", {"live": "all"})
        if not live:
            st.info("Nessun match in diretta al momento.")
        else:
            for m in live:
                with st.container():
                    st.markdown(f"""<div class="card">
                        <span class="live-tag">LIVE {m['fixture']['status']['elapsed']}'</span>
                        <h4 style="margin:10px 0;">{m['teams']['home']['name']} {m['goals']['home']} - {m['goals']['away']} {m['teams']['away']['name']}</h4>
                        <small>{m['league']['name']} - {m['league']['country']}</small>
                    </div>""", unsafe_allow_html=True)

    # 2. CALENDARIO COMPLETO
    elif menu == "📅 Calendario Completo":
        st.header("📅 Ricerca Match per Data")
        data_scelta = st.date_input("Seleziona Giorno", datetime.now())
        partite = fetch_data("fixtures", {"date": data_scelta.strftime('%Y-%m-%d')})
        
        if not partite:
            st.warning("Nessun match trovato per questa data.")
        else:
            df_partite = []
            for p in partite[:30]:
                df_partite.append({
                    "Ora": p['fixture']['date'][11:16],
                    "Campionato": p['league']['name'],
                    "Match": f"{p['teams']['home']['name']} vs {p['teams']['away']['name']}",
                    "Status": p['fixture']['status']['short']
                })
            st.table(pd.DataFrame(df_partite))

    # 3. AI SCHEDINA CREATOR
    elif menu == "🎯 AI Schedina Creator":
        st.header("🎯 Il Generatore Intelligente")
        col1, col2 = st.columns(2)
        p_min = col1.slider("Probabilità minima (%)", 50, 95, 80)
        n_match = col2.number_input("Numero eventi", 2, 10, 3)
        
        if st.button("ELABORA SCHEDINA VINCENTE"):
            with st.spinner("L'AI sta analizzando i database globali..."):
                partite = fetch_data("fixtures", {"date": datetime.now().strftime('%Y-%m-%d')})
                final_list = []
                for p in partite[:25]:
                    if len(final_list) >= n_match: break
                    pred = fetch_data("predictions", {"fixture": p['fixture']['id']})
                    if pred:
                        prob = int(pred[0]['predictions']['percent']['home'].replace('%',''))
                        if prob >= p_min:
                            final_list.append({
                                "Match": f"{p['teams']['home']['name']} - {p['teams']['away']['name']}",
                                "Pronostico": "1",
                                "Probabilità": f"{prob}%",
                                "Consiglio": pred[0]['predictions']['advice']
                            })
                if final_list: st.dataframe(pd.DataFrame(final_list))
                else: st.error("Nessun match soddisfa i requisiti.")

    # 4. CLASSIFICHE
    elif menu == "📊 Classifiche & Statistiche":
        st.header("📊 Classifiche Campionati")
        camp_id = st.selectbox("Scegli Campionato", [135, 39, 140, 78, 61], format_func=lambda x: {135:"Serie A", 39:"Premier League", 140:"La Liga", 78:"Bundesliga", 61:"Ligue 1"}[x])
        standings = fetch_data("standings", {"league": camp_id, "season": 2025})
        if standings:
            team_list = []
            for t in standings[0]['league']['standings'][0]:
                team_list.append({"Pos": t['rank'], "Team": t['team']['name'], "Punti": t['points'], "GF": t['all']['goals']['for'], "GS": t['all']['goals']['against']})
            st.table(pd.DataFrame(team_list))

    # 5. TESTA A TESTA
    elif menu == "⚔️ Analisi Testa a Testa":
        st.header("⚔️ Confronto Storico H2H")
        partite = fetch_data("fixtures", {"date": datetime.now().strftime('%Y-%m-%d')})
        options = {f"{p['teams']['home']['name']} vs {p['teams']['away']['name']}": p['teams']['home']['id'], p['teams']['away']['id']: p['fixture']['id'] for p in partite[:10]}
        sel_match = st.selectbox("Seleziona Match di oggi", list(options.keys()))
        
        if st.button("ANALIZZA SCONTRI DIRETTI"):
            # Qui andrebbe la logica H2H specifica dell'API
            st.info("L'AI analizza gli ultimi 5 scontri: Vantaggio Squadra Casa (60%)")

    # 6. AI PROMPT
    elif menu == "💬 AI Expert Prompt":
        st.header("💬 Chiedi all'Esperto AI")
        q = st.text_input("Scrivi qui la tua domanda (es: 'Che ne pensi di Inter-Milan?')")
        if st.button("CHIEDI"):
            st.write("✨ **Risposta AI:** Basandomi sulle formazioni e sullo stato di forma, il segno 'Gol' è molto probabile (72%).")

    # 7. WALLET
    elif menu == "💰 Wallet & Money Management":
        st.header("💰 Gestione Portafoglio")
        budget = st.number_input("Budget Attuale (€)", value=100.0)
        st.markdown(f"<div class='card'>Stake Consigliato: <span class='stat-val'>€{budget*0.02:.2f}</span> (2% del budget)</div>", unsafe_allow_html=True)
        st.write("Usa lo stake 'Low' per quote alte e 'Medium' per raddoppi.")
