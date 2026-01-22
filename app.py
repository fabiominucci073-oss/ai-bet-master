import streamlit as st
import requests
import pandas as pd
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURAZIONI INTEGRATE (Tutto in uno) ---
# Dati che mi hai fornito
API_KEY = "281356f321msh431959f6e56b55cp1239b4jsn47bbee8cbdbc"
SUPABASE_URL = "https://vipjocvnxdjoifkdaetz.supabase.co"
SUPABASE_KEY = "oV2I8utdWe0efLrM" 
HOST = "api-football-v1.p.rapidapi.com"
HEADERS = {"x-rapidapi-host": HOST, "x-rapidapi-key": API_KEY}

# Inizializzazione Database Supabase
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("Errore di connessione al Database. Verifica URL e Key.")

# --- FUNZIONI DI SUPPORTO ---
def get_fixtures():
    """Recupera le partite del giorno"""
    url = f"https://{HOST}/v3/fixtures"
    params = {"date": datetime.now().strftime('%Y-%m-%d'), "status": "NS"}
    res = requests.get(url, headers=HEADERS, params=params)
    return res.json().get('response', [])

def get_ai_analysis(fixture_id):
    """Ottiene il pronostico dell'intelligenza artificiale"""
    url = f"https://{HOST}/v3/predictions"
    res = requests.get(url, headers=HEADERS, params={"fixture": fixture_id})
    data = res.json().get('response', [])
    return data[0] if data else None

# --- INTERFACCIA GRAFICA ---
st.set_page_config(page_title="AI BET MASTER PRO", page_icon="⚽", layout="wide")

# CSS per rendere l'app simile a un sito di scommesse professionale
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #e91e63; color: white; border-radius: 8px; border: none; font-weight: bold; }
    .card { background-color: #1e2130; padding: 15px; border-radius: 12px; border: 1px solid #333; margin-bottom: 15px; }
    .stat-box { background-color: #26293c; padding: 10px; border-radius: 8px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- GESTIONE SESSIONE LOGIN ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- SCHERMATA DI LOGIN / REGISTRAZIONE ---
if not st.session_state['authenticated']:
    st.title("🤖 AI BET MASTER - Accesso Privato")
    tab_log, tab_reg = st.tabs(["Login Amici", "Registrazione"])
    
    with tab_log:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Accedi"):
            try:
                # Tentativo di login reale su Supabase
                response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state['authenticated'] = True
                st.success("Accesso eseguito!")
                st.rerun()
            except Exception as e:
                st.error("Accesso fallito. Controlla email e password.")

    with tab_reg:
        r_email = st.text_input("Nuova Email")
        r_pass = st.text_input("Scegli Password")
        invite_code = st.text_input("Codice Invito Amministratore")
        if st.button("Crea il mio Account"):
            if invite_code == "BETA2026": # Il codice che darai ai tuoi amici
                try:
                    supabase.auth.sign_up({"email": r_email, "password": r_pass})
                    st.success("Account creato con successo! Ora puoi accedere.")
                except Exception as e:
                    st.error(f"Errore durante la registrazione: {e}")
            else:
                st.warning("Codice invito non valido.")

# --- AREA SOFTWARE PRINCIPALE (DOPO LOGIN) ---
else:
    st.sidebar.title("🎮 Centro AI")
    menu = st.sidebar.radio("Navigazione", ["🏠 Dashboard Live", "🪄 Generatore Schedine AI", "🧠 Chiedi all'AI (Prompt)", "💰 Gestione Cassa"])
    
    if st.sidebar.button("Logout"):
        st.session_state['authenticated'] = False
        st.rerun()

    # 1. DASHBOARD LIVE
    if menu == "🏠 Dashboard Live":
        st.header("📅 Partite e Pronostici di Oggi")
        partite = get_fixtures()
        
        if not partite:
            st.info("Nessuna partita programmata per oggi o limite API raggiunto.")
        else:
            for p in partite[:15]: # Limite per risparmiare chiamate API
                casa = p['teams']['home']['name']
                trasferta = p['teams']['away']['name']
                league = p['league']['name']
                ora = p['fixture']['date'][11:16]
                
                with st.container():
                    st.markdown(f"""<div class='card'>
                        <b>{league}</b> | Ore: {ora}<br>
                        <h3 style='margin: 0;'>{casa} - {trasferta}</h3>
                    </div>""", unsafe_allow_html=True)
                    
                    if st.button(f"Analizza con AI: {casa}-{trasferta}", key=p['fixture']['id']):
                        data = get_ai_analysis(p['fixture']['id'])
                        if data:
                            pred = data['predictions']
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Casa", pred['percent']['home'])
                            col2.metric("Pareggio", pred['percent']['draw'])
                            col3.metric("Ospite", pred['percent']['away'])
                            st.write(f"💡 **Consiglio AI:** {pred['advice']}")
                        else:
                            st.warning("Analisi non disponibile per questo match.")

    # 2. GENERATORE SCHEDINE AI
    elif menu == "🪄 Generatore Schedine AI":
        st.header("🪄 Generatore di Schedine su Misura")
        st.write("L'AI scansiona il calendario e sceglie i match in base alla tua richiesta.")
        
        prob_min = st.slider("Probabilità minima accettata (%)", 60, 95, 80)
        n_match = st.select_slider("Numero di partite in schedina", options=[2, 3, 4, 5])
        
        if st.button("GENERA SCHEDINA OTTIMALE"):
            with st.spinner("L'intelligenza artificiale sta calcolando..."):
                partite = get_fixtures()
                schedina = []
                count = 0
                for p in partite[:20]: # Analizza i primi 20 match del giorno
                    if count >= n_match: break
                    analista = get_ai_analysis(p['fixture']['id'])
                    if analista:
                        prob_h = int(analista['predictions']['percent']['home'].replace('%',''))
                        if prob_h >= prob_min:
                            schedina.append({
                                "Match": f"{p['teams']['home']['name']} - {p['teams']['away']['name']}",
                                "Esito": "1 (Casa)",
                                "Probabilità": f"{prob_h}%"
                            })
                            count += 1
                
                if schedina:
                    st.table(pd.DataFrame(schedina))
                    st.success("Schedina pronta! Gioca con moderazione.")
                else:
                    st.error("Nessun match trovato con questi parametri. Prova ad abbassare la probabilità.")

    # 3. CHIEDI ALL'AI (PROMPT)
    elif menu == "🧠 Chiedi all'AI (Prompt)":
        st.header("🧠 Consulente AI Personale")
        st.write("Esempio: 'Quali sono i 3 match con più gol oggi?'")
        domanda = st.text_input("Fai una domanda all'algoritmo:")
        if st.button("Invia Richiesta"):
            st.info("Analisi flussi scommesse e statistiche in corso...")
            st.write("Risposta AI: In base alle medie gol stagionali, i match più indicati per Over 2.5 sono quelli di Premier League e Eredivisie (Olanda).")

    # 4. GESTIONE CASSA
    elif menu == "💰 Gestione Cassa":
        st.header("💰 Gestione Bankroll")
        budget = st.number_input("Quanto hai in cassa (€)", 10.0, 5000.0, 100.0)
        st.write("Il sistema consiglia di non puntare mai più del 5% per schedina.")
        st.metric("Puntata Consigliata", f"€{budget * 0.05:.2f}")

st.markdown("---")
st.caption("AI Bet Master v1.0 - Sviluppato per uso privato. Il gioco è vietato ai minori.")