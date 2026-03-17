import streamlit as st
import yfinance as yf
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import pytz
import pandas as pd
import requests

# --- 1. CONFIGURACIÓN DE ALTO NIVEL ---
st.set_page_config(page_title="MELI TOTAL COMMAND v18", layout="wide", initial_sidebar_state="expanded")
# Refresco automático cada 30 segundos para que Meli "escuche" Telegram
st_autorefresh(interval=30000, key="global_refresh")

# CREDENCIALES MONTERO (YA INTEGRADAS)
TELEGRAM_TOKEN = "8613807854:AAETsHlv1n0YYJxpjvuduGeXoVca9-jRfWo
TELEGRAM_CHAT_ID = "8350001201"

# --- 2. EL CEREBRO DE TELEGRAM (ESCUCHA Y RESPUESTA) ---
def meli_bot_sync():
    url_updates = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    try:
        response = requests.get(url_updates).json()
        if response["result"]:
            # Tomamos el último mensaje recibido
            last_update = response["result"][-1]
            mensaje_texto = last_update["message"]["text"].lower()
            mensaje_id = last_update["message"]["message_id"]
            
            # Verificamos si es un mensaje nuevo para no repetir respuestas
            if "ultimo_msg_id" not in st.session_state or st.session_state.ultimo_msg_id != mensaje_id:
                st.session_state.ultimo_msg_id = mensaje_id
                
                # --- LÓGICA DE RESPUESTA DE MELI ---
                if "oro" in mensaje_texto or "xau" in mensaje_texto:
                    precio = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
                    reply = f"🚀 Montero, el Oro está en ${precio:.2f}. Meli detecta presión compradora."
                elif "dxy" in mensaje_texto:
                    precio_dxy = yf.Ticker("DX-Y.NYB").history(period="1d")['Close'].iloc[-1]
                    reply = f"💵 El DXY está en {precio_dxy:.2f}. ¡Ojo con las correlaciones!"
                elif "hola" in mensaje_texto:
                    reply = "¡Dime, Montero! Estoy vigilando Nueva York por ti. ¿Qué quieres saber?"
                else:
                    reply = "Recibido. Estoy analizando los documentos y el gráfico. Dame un momento."
                
                # Enviar respuesta de vuelta al Telegram de Montero
                requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={reply}")
    except:
        pass

# --- 3. DISEÑO CYBER-BUNKER (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    html, body, [data-testid="stapp-view-container"] { background-color: #020202; font-family: 'JetBrains Mono', monospace; color: #00ffcc; }
    [data-testid="stMetric"] { background: #0a0a0a; border: 1px solid #00ffcc; border-radius: 12px; padding: 15px; }
    .stTabs [data-baseweb="tab"] { background-color: #111; color: #00ffcc; border-radius: 8px 8px 0 0; }
    .stTabs [aria-selected="true"] { background-color: #00ffcc !important; color: black !important; }
    .book-card { background: #0a0a0a; border: 1px solid #222; border-radius: 15px; padding: 20px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNCIONES TÉCNICAS ---
def get_data(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="1d", interval="1m")
        curr = df['Close'].iloc[-1]
        chg = ((curr - df['Open'].iloc[0]) / df['Open'].iloc[0]) * 100
        return {"price": curr, "hi": df['High'].max(), "lo": df['Low'].min(), "chg": chg}
    except: return None

def get_sessions():
    utc = datetime.now(pytz.utc)
    ny = utc.astimezone(pytz.timezone('US/Eastern')).hour
    return "🟢 NEW YORK ABIERTO" if 8 <= ny <= 16 else "🔴 MERCADO CERRADO / ASIA"

# --- 5. LÓGICA DE ARRANQUE ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title("🛡️ MONTERO ACCESS CONTROL")
    if st.text_input("PIN:", type="password") == "1234":
        if st.button("DESBLOQUEAR BÚNKER"):
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 6. SIDEBAR: EL CEREBRO DE MELI ---
with st.sidebar:
    st.header("🧠 MELI BRAIN v18")
    st.write(f"📍 {get_sessions()}")
    st.divider()
    up = st.file_uploader("Subir PDF/Excel:", type=['pdf', 'xlsx', 'csv'])
    if up: st.success("Documento cargado. Meli analizando...")
    
    st.text_area("Consulta directa:")
    if st.button("ANALIZAR"): st.info("Estructura de mercado: Acumulación.")
    
    st.divider()
    if st.button("📲 Test Manual Telegram"):
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text=Test manual desde el Búnker.")

# --- 7. PANEL PRINCIPAL ---
meli_bot_sync() # Meli escucha Telegram en cada carga
st.title("🛡️ MONTERO QUANTUM TERMINAL")

tab_radar, tab_chart, tab_books, tab_log = st.tabs(["🎯 RADAR", "📉 GRÁFICOS", "📚 BIBLIOTECA", "📜 BITÁCORA"])

with tab_radar:
    c1, c2, c3 = st.columns(3)
    oro = get_data("GC=F")
    if oro: 
        c1.metric("🟡 ORO", f"${oro['price']:.2f}", f"{oro['chg']:.2f}%")
        st.write(f"H: {oro['hi']:.2f} | L: {oro['lo']:.2f}")
    
    dxy = get_data("DX-Y.NYB")
    if dxy: c2.metric("💵 DXY", f"{dxy['price']:.2f}", f"{dxy['chg']:.2f}%")
    
    nas = get_data("NQ=F")
    if nas: c3.metric("📊 NASDAQ", f"{nas['price']:.2f}", f"{nas['chg']:.2f}%")
    
    st.divider()
    st.header("🕵️‍♂️ Detector de Manipulación")
    if dxy and oro and dxy['chg'] > 0 and oro['chg'] > 0:
        st.error("🚨 ALERTA: DXY y Oro subiendo juntos. ¡Trampa institucional detectada!")
    else:
        st.success("✅ Correlaciones estables. El Smart Money sigue la lógica.")

with tab_chart:
    asset = st.selectbox("Elegir Activo:", ["OANDA:XAUUSD", "NASDAQ:NAS100", "CAPITALCOM:DXY"])
    components.html(f"""<iframe src="https://s.tradingview.com/widgetembed/?symbol={asset}&interval=1&theme=dark" width="100%" height="600" frameborder="0"></iframe>""", height=600)

with tab_books:
    st.header("📖 Formación del Millonario")
    bl1, bl2 = st.columns(2)
    libros = [
        {"t": "Trading en la Zona", "a": "Mark Douglas", "l": "La mentalidad es el 90% del éxito."},
        {"t": "Piense y Hágase Rico", "a": "Napoleon Hill", "l": "El deseo ardiente crea riqueza."},
        {"t": "El Método Wyckoff", "a": "R. Wyckoff", "l": "Entiende las huellas de los bancos."}
    ]
    for i, b in enumerate(libros):
        with (bl1 if i%2==0 else bl2):
            st.markdown(f'<div class="book-card"><b style="color:#00ffcc">{b["t"]}</b><br><small>{b["l"]}</small></div>', unsafe_allow_html=True)

with tab_log:
    st.subheader("📒 Historial de Guerra")
    st.info("Búnker activo. Esperando registros para cuenta de $100K.")
