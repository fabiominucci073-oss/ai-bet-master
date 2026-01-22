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
def get_data(endpoint, params=None):
    url = f"https://{HOST}/v3/{endpoint}"
    try:
        res = requests.get(url, headers=HEADERS, params=params)
        return res.json().get('response', [])
    except:
        return []

# --- INTERFACCIA ---
st.set_page_config(page_title="AI BET MASTER ULTIMATE", layout="wide", page_icon="⚽")

# CSS Avanzato per stile "Sito Scommesse"
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .card { background-color: #161b22; padding: 20px; border-radius: 15px; border-left: 6px solid #ff4b4b; margin-bottom: 15px; border-right: 1px solid #30363d; }
    .live-tag { background-color: #ff4b4b; color: white; padding: 2px 8px; border-radius: 5px; font-weight: bold; font-size: 12px; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background: linear-gradient(90deg, #ff4b4b, #cc0000); color: white; height: 3.5em; transition: 0.3s; border: none; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4); }
    .bet-slip { background-color: #1e2530; border: 1px solid #ff4b4b; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'slip' not in st.session_state: st.session_state['slip'] = []

# --- ACCESSO / REGISTRAZIONE ---
if not st.session_state['auth']:
    st.title("🤖 AI Bet Master Ultimate")
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ACCEDI AL PORTALE"):
            try:
                supabase.auth.sign_in_with_password({"email": e, "password": p})
                st.session_state['auth'] = True
                st.rerun()
            except: st.error("Dati errati.")
    with t2:
        re = st.text_input("Tua Email")
        rp = st.text_input("Crea Password", type="password")
        c = st.text_input("Codice Invito Amministratore")
        if st.button("REGISTRATI ORA"):
            if c == "BETA2026":
                try:
                    supabase.auth.sign_up({"email": re, "password": rp})
                    st.success("Registrazione completata! Effettua il login.")
                except: st.error("Errore registrazione.")
            else: st.warning("Codice non valido.")

# --- APP PRINCIPALE ---
else:
    # Sidebar potenziata
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3563/3563417.png", width=80)
    st.sidebar.title("PRO-BET PANEL")
    
    menu = st.sidebar.radio("Navigazione:", [
        "🏠 Dashboard Live", 
        "📅 Palinsesto & Orari", 
        "🎯 AI Prediction Engine", 
        "⚔️ Analisi Testa a Testa",
        "📊 Classifiche & Marcatori",
        "💬 AI Expert Chat",
        "💰 Portafoglio & Stake"
    ])
    
    # Sezione Schedina Virtuale in Sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Schedina Virtuale")
    if st.session_state['slip']:
        for s in st.session_state['slip']:
            st.sidebar.caption(f"✅ {s}")
        if st.sidebar.button("Pulisci Schedina"):
            st.session_state['slip'] = []
            st.rerun()
    else:
        st.sidebar.info("Aggiungi match dai pronostici")

    if st.sidebar.button("LOGOUT"):
        st.session_state['auth'] = False
        st.rerun()

    # 1. PARTITE LIVE
    if menu == "🏠 Dashboard Live":
        st.header("🔴 Match Live in Diretta")
        live = get_data("fixtures", {"live": "all"})
        if not live:
            st.info("Nessuna partita live. Controlla il calendario.")
        else:
            col_a, col_b = st.columns(2)
            for i, m in enumerate(live[:16]):
                target_col = col_a if i % 2 == 0 else col_b
                with target_col:
                    st.markdown(f"""<div class="card">
                        <span class="live-tag">LIVE {m['fixture']['status']['elapsed']}'</span>
                        <h4 style="margin:8px 0;">{m['teams']['home']['name']} {m['goals']['home']} - {m['goals']['away']} {m['teams']['away']['name']}</h4>
                        <p style="font-size:0.8em; color:#888;">{m['league']['name']} | {m['fixture']['status']['long']}</p>
                    </div>""", unsafe_allow_html=True)

    # 2. CALENDARIO & ORARI
    elif menu == "📅 Palinsesto & Orari":
        st.header("📅 Palinsesto Mondiale")
        data_sel = st.date_input("Scegli data:", datetime.now())
        fixtures = get_data("fixtures", {"date": data_sel.strftime('%Y-%m-%d')})
        if not fixtures:
            st.warning("Nessun match trovato.")
        else:
            df = pd.DataFrame([{
                "Ora": f['fixture']['date'][11:16],
                "Lega": f['league']['name'],
                "Evento": f"{f['teams']['home']['name']} vs {f['teams']['away']['name']}",
                "Stato": f['fixture']['status']['short']
            } for f in fixtures[:60]])
            st.dataframe(df, use_container_width=True)

    # 3. GENERATORE SCHEDINE AI
    elif menu == "🎯 AI Prediction Engine":
        st.header("🎯 Analisi Predittiva AI")
        c1, c2 = st.columns(2)
        min_p = c1.select_slider("Fiducia AI (%)", options=[60, 70, 80, 90, 95], value=80)
        max_m = c2.number_input("Max Match", 1, 10, 3)
        
        if st.button("ELABORA PRONOSTICI"):
            with st.spinner("L'AI sta analizzando i big data..."):
                match_oggi = get_data("fixtures", {"date": datetime.now().strftime('%Y-%m-%d')})
                count = 0
                for m in match_oggi[:40]:
                    if count >= max_m: break
                    p = get_data("predictions", {"fixture": m['fixture']['id']})
                    if p:
                        prob = int(p[0]['predictions']['percent']['home'].replace('%',''))
                        if prob >= min_p:
                            with st.expander(f"⭐ {m['teams']['home']['name']} - {m['teams']['away']['name']} ({prob}%)"):
                                st.write(f"**Pronostico:** {p[0]['predictions']['advice']}")
                                st.write(f"**Analisi:** {p[0]['predictions']['winner']['name']} favorito")
                                if st.button("Aggiungi alla schedina", key=f"bet_{m['fixture']['id']}"):
                                    st.session_state['slip'].append(f"{m['teams']['home']['name']} - {p[0]['predictions']['advice']}")
                                    st.rerun()
                            count += 1

    # 4. ANALISI TESTA A TESTA
    elif menu == "⚔️ Analisi Testa a Testa":
        st.header("⚔️ Confronto Storico H2H")
        st.write("Cerca la cronologia degli scontri tra due squadre.")
        t1 = st.number_input("ID Squadra Casa (vedi classifiche)", value=494)
        t2 = st.number_input("ID Squadra Ospite", value=497)
        if st.button("VEDI H2H"):
            h2h = get_data("fixtures/headtohead", {"h2h": f"{t1}-{t2}"})
            for h in h2h[:5]:
                st.write(f"📅 {h['fixture']['date'][:10]}: {h['teams']['home']['name']} {h['goals']['home']}-{h['goals']['away']} {h['teams']['away']['name']}")

    # 5. CLASSIFICHE & MARCATORI
    elif menu == "📊 Classifiche & Marcatori":
        st.header("📊 Statistiche Leghe")
        l_id = st.selectbox("Campionato", [135, 39, 140, 78, 61], format_func=lambda x: {135:"Serie A", 39:"Premier League", 140:"La Liga", 78:"Bundesliga", 61:"Ligue 1"}[x])
        tab_a, tab_b = st.tabs(["Classifica", "Top Scorers"])
        
        with tab_a:
            data = get_data("standings", {"league": l_id, "season": 2025})
            if data:
                df_s = pd.DataFrame([{"Pos": t['rank'], "Team": t['team']['name'], "Pt": t['points'], "ID": t['team']['id']} for t in data[0]['league']['standings'][0]])
                st.table(df_s)
        
        with tab_b:
            scorers = get_data("players/topscorers", {"league": l_id, "season": 2025})
            if scorers:
                df_p = pd.DataFrame([{"Nome": p['player']['name'], "Gol": p['statistics'][0]['goals']['total'], "Team": p['statistics'][0]['team']['name']} for p in scorers[:10]])
                st.table(df_p)

    # 6. AI CHAT
    elif menu == "💬 AI Expert Chat":
        st.header("💬 Chiedi all'Algoritmo")
        txt = st.text_area("Descrivi la tua scommessa per un parere tecnico:")
        if st.button("Ricevi Analisi"):
            st.warning("L'AI consiglia: Evita le multiple sopra i 5 eventi. La probabilità di successo cala del 45%.")

    # 7. PORTAFOGLIO
    elif menu == "💰 Portafoglio & Stake":
        st.header("💰 Money Management Professionale")
        cassa = st.number_input("Cassa Totale (€)", value=100.0)
        col1, col2, col3 = st.columns(3)
        col1.metric("Stake Safe (2%)", f"€{cassa*0.02:.2f}")
        col2.metric("Stake Medium (5%)", f"€{cassa*0.05:.2f}")
        col3.metric("Stake High (10%)", f"€{cassa*0.10:.2f}")
        st.markdown("""<div class='bet-slip'><b>Consiglio del Giorno:</b> Mantieni una gestione costante. L'80% dei perdenti scommette senza una strategia di stake fissa.</div>""", unsafe_allow_html=True)
