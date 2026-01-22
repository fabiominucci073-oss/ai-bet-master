import streamlit as st
import requests
import pandas as pd
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURAZIONI DEFINITIVE ---
API_KEY = "281356f321msh431959f6e56b55cp1239b4jsn47bbee8cbdbc"
HOST = "api-football-v1.p.rapidapi.com"
HEADERS = {"x-rapidapi-host": HOST, "x-rapidapi-key": API_KEY}

# DATI SUPABASE (URL e KEY ANON PUBLIC)
SUPABASE_URL = "https://vipjocvnxdjoifkdaetz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpcGpvY3ZueGRqb2lma2RhZXR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkxMTY4MjksImV4cCI6MjA4NDY5MjgyOX0.n7EZCKiJOEZUHgwhJsCAt6Rh7hrkx3dQVl8SvwPwQbE" 

# Inizializzazione Database
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    st.error("Errore di configurazione Database.")

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

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; border-radius: 12px; height: 3em; }
    .card { background-color: #1e2130; padding: 20px; border-radius: 15px; border-left: 6px solid #ff4b4b; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# --- LOGIN / REGISTRAZIONE ---
if not st.session_state['auth']:
    st.title("🤖 AI Bet Master")
    tab_auth = st.tabs(["Accedi", "Registrati"])
    
    with tab_auth[0]:
        email_l = st.text_input("Email", key="login_email")
        pass_l = st.text_input("Password", type="password", key="login_pass")
        if st.button("ACCEDI"):
            try:
                supabase.auth.sign_in_with_password({"email": email_l, "password": pass_l})
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
                    st.success("Registrazione completata! Adesso puoi fare il login.")
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
                    if st.button(f"Analizza AI: {p['teams']['home']['name']}", key=p['fixture']['id']):
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
            with st.spinner("Analisi in corso..."):
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
                st.warning("Nessun match trovato.")

    elif scelta == "💬 AI Prompt":
        st.header("💬 Consulenza Privata AI")
        domanda = st.text_input("Fai una domanda all'algoritmo:")
        if st.button("Analizza"):
            st.info("L'AI suggerisce di puntare sui match con vantaggio casa superiore al 75%.")

    elif scelta == "💰 Gestione Budget":
        st.header("💰 Gestione Rischio")
        cassa = st.number_input("Cassa Totale (€)", value=100.0)
        st.metric("Stake Consigliato", f"€{cassa * 0.05:.2f}")
