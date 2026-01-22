import streamlit as st
import requests
import pandas as pd
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURAZIONI INTEGRATE ---
API_KEY = "281356f321msh431959f6e56b55cp1239b4jsn47bbee8cbdbc"
HOST = "api-football-v1.p.rapidapi.com"
HEADERS = {"x-rapidapi-host": HOST, "x-rapidapi-key": API_KEY}

# DATI SUPABASE (URL e KEY)
SUPABASE_URL = "https://vipjocvnxdjoifkdaetz.supabase.co"
# NOTA: Se ricevi "Invalid API Key", sostituisci questa password con la chiave 'anon public' di Supabase
SUPABASE_KEY = "oV2I8utdWe0efLrM" 

# Inizializzazione Database
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    st.error("Errore di connessione a Supabase. Controlla le chiavi API.")

# --- FUNZIONI DATI CALCIO ---
def get_fixtures():
    url = f"https://{HOST}/v3/fixtures"
    params = {"date": datetime.now().strftime('%Y-%m-%d'), "status": "NS"}
    try:
        res = requests.get(url, headers=HEADERS, params=params)
        return res.json().get('response', [])
    except:
        return []

def get_ai_prediction(fixture_id):
    url = f"https://{HOST}/v3/predictions"
    try:
        res = requests.get(url, headers=HEADERS, params={"fixture": fixture_id})
        data = res.json().get('response', [])
        return data[0] if data else None
    except:
        return None

# --- INTERFACCIA UTENTE ---
st.set_page_config(page_title="AI Bet Master", layout="wide", page_icon="⚽")

# Stile CSS per Mobile
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; border-radius: 12px; height: 3em; }
    .card { background-color: #1e2130; padding: 20px; border-radius: 15px; border-left: 6px solid #ff4b4b; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# --- GESTIONE LOGIN / REGISTRAZIONE ---
if not st.session_state['auth']:
    st.title("🤖 AI Bet Master")
    st.write("Accedi per vedere le schedine create dall'IA")
    
    tab_auth = st.tabs(["Accedi", "Registrati"])
    
    with tab_auth[0]:
        email_l = st.text_input("Email", key="login_email")
        pass_l = st.text_input("Password", type="password", key="login_pass")
        if st.button("ACCEDI"):
            try:
                user = supabase.auth.sign_in_with_password({"email": email_l, "password": pass_l})
                st.session_state['auth'] = True
                st.rerun()
            except:
                st.error("Email o Password errati.")

    with tab_auth[1]:
        email_r = st.text_input("Tua Email", key="reg_email")
        pass_r = st.text_input("Crea Password", type="password", key="reg_pass")
        codice = st.text_input("Codice Invito Amministratore")
        if st.button("REGISTRATI"):
            if codice == "BETA2026":
                try:
                    supabase.auth.sign_up({"email": email_r, "password": pass_r})
                    st.success("Registrazione completata! Ora puoi fare il login.")
                except Exception as e:
                    st.error(f"Errore: {e}")
            else:
                st.warning("Codice invito non valido.")

# --- APP PRINCIPALE ---
else:
    st.sidebar.title("Opzioni AI")
    scelta = st.sidebar.radio("Naviga:", ["🏠 Partite Live", "🎯 Generatore Schedine", "💬 AI Prompt", "💰 Gestione Budget"])
    
    if st.sidebar.button("LOGOUT"):
        st.session_state['auth'] = False
        st.rerun()

    if scelta == "🏠 Partite Live":
        st.header("⚽ Match di Oggi")
        partite = get_fixtures()
        if not partite:
            st.info("Nessuna partita disponibile al momento.")
        else:
            for p in partite[:12]:
                with st.container():
                    st.markdown(f"""<div class="card">
                        <small>{p['league']['name']}</small>
                        <h3>{p['teams']['home']['name']} vs {p['teams']['away']['name']}</h3>
                        <p>Inizio: {p['fixture']['date'][11:16]}</p>
                    </div>""", unsafe_allow_html=True)
                    if st.button(f"Analisi AI: {p['teams']['home']['name']}", key=p['fixture']['id']):
                        d = get_ai_prediction(p['fixture']['id'])
                        if d:
                            st.write(f"💡 **Consiglio:** {d['predictions']['advice']}")
                            st.write(f"📊 **Probabilità:** Casa {d['predictions']['percent']['home']} | X {d['predictions']['percent']['draw']} | Fuori {d['predictions']['percent']['away']}")

    elif scelta == "🎯 Generatore Schedine":
        st.header("🎯 Crea Schedina con IA")
        prob_min = st.slider("Probabilità minima (%)", 60, 95, 80)
        n_eventi = st.select_slider("Numero partite", options=[2, 3, 4, 5])
        
        if st.button("GENERA ORA"):
            partite = get_fixtures()
            schedina = []
            with st.spinner("L'IA sta cercando le partite migliori..."):
                for p in partite[:20]:
                    if len(schedina) >= n_eventi: break
                    d = get_ai_prediction(p['fixture']['id'])
                    if d:
                        p_home = int(d['predictions']['percent']['home'].replace('%',''))
                        if p_home >= prob_min:
                            schedina.append({"Gara": f"{p['teams']['home']['name']}-{p['teams']['away']['name']}", "Suggerimento": "1", "Prob.": f"{p_home}%"})
            if schedina:
                st.table(pd.DataFrame(schedina))
            else:
                st.warning("Nessun match trovato con questi parametri oggi.")

    elif scelta == "💬 AI Prompt":
        st.header("💬 Consulenza Privata AI")
        domanda = st.text_input("Fai una domanda (es: 'Qual è il miglior match per Over 1.5 oggi?')")
        if st.button("Analizza"):
            st.info("Analisi in corso... L'IA suggerisce di guardare i match di Premier League per statistiche gol più alte.")

    elif scelta == "💰 Gestione Budget":
        st.header("💰 Calcolatore Gestione Rischio")
        cassa = st.number_input("Tua Cassa Totale (€)", value=100.0)
        st.metric("Puntata Consigliata (Stake)", f"€{cassa * 0.05:.2f}")
        st.write("L'IA consiglia di non superare il 5% del budget per ogni giocata.")
