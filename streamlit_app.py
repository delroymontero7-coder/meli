import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

# --- 1. CONFIGURACIÓN E IDENTIDAD DEL BÚNKER ---
st.set_page_config(
    page_title="TERMINAL SUPREMA MONTERO",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CREDENCIALES DE COMUNICACIÓN CRÍTICA
TELEGRAM_TOKEN = "8613807854:AAEtSHlv1n0YYJxpjvuduGeXoVca9-jRfWo"
TELEGRAM_CHAT_ID = "8350001201"

# --- 2. PROTOCOLO DE SEGURIDAD NIVEL 4 ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🔐 SISTEMA DE COMANDO MONTERO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: red;'>ACCESO RESTRINGIDO - AUTORIZACIÓN REQUERIDA</p>", unsafe_allow_html=True)
    
    _, col_pin, _ = st.columns([1,1,1])
    with col_pin:
        pin = st.text_input("INTRODUCE TU LLAVE MAESTRA (PIN):", type="password")
        if pin == "1234":
            st.session_state.authenticated = True
            st.success("LLAVE ACEPTADA - ENTRANDO AL BÚNKER...")
            st.rerun()
    st.stop()

# --- 3. EL CEREBRO DE ANALÍTICA (Meli Engine) ---
def melli_engine(ticker):
    try:
        # Descarga de datos de alta precisión
        df = yf.download(ticker, period="1d", interval="5m", progress=False)
        if df.empty:
            return "S/D", "#777", 0.0, 0.0
        
        # Cálculo de la Ganadora y la Peleadora
        ema_ganadora = df['Close'].ewm(span=9).mean().iloc[-1]
        ema_peleadora = df['Close'].ewm(span=21).mean().iloc[-1]
        precio_actual = df['Close'].iloc[-1]
        precio_apertura = df['Close'].iloc[0]
        variacion = precio_actual - precio_apertura
        
        if precio_actual > ema_ganadora and ema_ganadora > ema_peleadora:
            return "🟢 LA GANADORA (ALCISTA)", "#00ff00", round(precio_actual, 2), round(variacion, 2)
        elif precio_actual < ema_ganadora and ema_ganadora < ema_peleadora:
            return "🔴 LA PELEADORA (BAJISTA)", "#ff4b4b", round(precio_actual, 2), round(variacion, 2)
        else:
            return "🟡 EN ESPERA (NEUTRAL)", "#ffcc00", round(precio_actual, 2), round(variacion, 2)
    except:
        return "ERROR", "#777", 0.0, 0.0

# --- 4. ENCABEZADO Y STATUS EN VIVO ---
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🛡️ TERMINAL QUANTUM SUPREMA v28</h1>", unsafe_allow_html=True)
ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"<p style='text-align: center; color: #555;'>Estado del Sistema: OPERATIVO | {ahora}</p>", unsafe_allow_html=True)

# --- 5. PANEL DE CONTROL DE ACTIVOS (LOS 4 GRANDES) ---
st.subheader("🛰️ RADAR DE MERCADOS")
col1, col2, col3, col4 = st.columns(4)

activos = [("ORO (XAU/USD)", "GC=F"), ("BITCOIN (BTC)", "BTC-USD"), ("PETRÓLEO (WTI)", "CL=F"), ("DXY (DÓLAR)", "DX-Y")]
columnas = [col1, col2, col3, col4]

for i, (nombre, ticker) in enumerate(activos):
    status, color, precio, cambio = melli_engine(ticker)
    with columnas[i]:
        st.metric(label=nombre, value=f"${precio}", delta=f"{cambio}")
        st.markdown(f"<div style='background-color: #111; padding: 5px; border-radius: 5px; border-left: 5px solid {color};'><p style='color:{color}; font-weight:bold; margin-bottom:0;'>{status}</p></div>", unsafe_allow_html=True)

st.divider()

# --- 6. CAMPO DE BATALLA: TRADINGVIEW INTERACTIVO ---
col_main, col_tools = st.columns([3, 1])

with col_main:
    st.subheader("📊 ANÁLISIS TÉCNICO AVANZADO")
    # Widget completo con herramientas de dibujo y lista de seguimiento
    tradingview_code = """
    <div class="tradingview-widget-container" style="height:650px; width:100%;">
      <div id="tv_supreme_bunker" style="height:650px;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true, "symbol": "OANDA:XAUUSD", "interval": "5", "timezone": "Etc/UTC",
        "theme": "dark", "style": "1", "locale": "es", "toolbar_bg": "#f1f3f6",
        "enable_publishing": false, "withdateranges": true, "hide_side_toolbar": false,
        "allow_symbol_change": true, "details": true, "hotlist": true, "calendar": true,
        "container_id": "tv_supreme_bunker"
      });
      </script>
    </div>
    """
    components.html(tradingview_code, height=650)

with col_tools:
    st.subheader("📜 LA LEY DE MONTERO")
    st.markdown("""
    <div style="background-color: #0e1117; padding: 15px; border: 1px solid #00ffcc; border-radius: 10px;">
        <p style="color: #00ffcc;"><b>I. PRESERVAR EL CAPITAL</b><br>Los $100K no se tocan sin plan.</p>
        <p style="color: #00ffcc;"><b>II. CONFIRMACIÓN</b><br>Ganadora manda, Peleadora avisa.</p>
        <p style="color: #00ffcc;"><b>III. DISCIPLINA</b><br>Sin emoción, solo ejecución.</p>
        <p style="color: #00ffcc;"><b>IV. PACIENCIA</b><br>El mercado entrega al que espera.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("📡 COMANDOS")
    if st.button("🚀 ENVIAR ALERTA TELEGRAM"):
        try:
            msg = f"🛡️ MONTERO BÚNKER: Terminal V28 Activa. Mercados analizados. Revisa la Ganadora."
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={msg}"
            requests.get(url)
            st.success("¡Mensaje enviado!")
        except:
            st.error("Error en conexión de Telegram")

# --- 7. ACADEMIA Y AJUSTES (SIDEBAR) ---
with st.sidebar:
    st.title("📚 ACADEMIA MONTERO")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.divider()
    st.markdown("### 📖 BIBLIOTECA")
    st.markdown("[📘 DEBITA Y COBRA (PDF)](https://archive.org/download/debitaycobra/debita%20y%20cobra.pdf)")
    st.markdown("[📙 PSICOLOGÍA DEL TRADING](https://www.google.com/search?q=trading+psychology+pdf)")
    st.divider()
    st.info("Terminal v28.0 - Construida para ganar.")
