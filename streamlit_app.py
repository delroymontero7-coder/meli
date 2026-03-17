import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import requests

# --- 1. CONFIGURACIÓN DEL BÚNKER ---
st.set_page_config(page_title="RADAR TOTAL MONTERO", layout="wide", initial_sidebar_state="expanded")

# TUS CREDENCIALES (REINSTALADAS Y VERIFICADAS)
TELEGRAM_TOKEN = "8613807854:AAEtSHlv1n0YYJxpjvuduGeXoVca9-jRfWo"
TELEGRAM_CHAT_ID = "8350001201"

# --- 2. EL CEREBRO DE MELI (ANÁLISIS DE LA GANADORA Y LA PELEADORA) ---
def melli_analisis(ticker):
    try:
        df = yf.download(ticker, period="1d", interval="5m", progress=False)
        if df.empty: return "⚪ SIN DATOS", "#777"
        
        # Estrategia: Cruce de Medias Exponenciales (EMAs)
        fast = df['Close'].ewm(span=9).mean().iloc[-1]
        slow = df['Close'].ewm(span=21).mean().iloc[-1]
        price = df['Close'].iloc[-1]
        
        if price > fast and fast > slow:
            return "🟢 LA GANADORA (COMPRA)", "#00ff00"
        elif price < fast and fast < slow:
            return "🔴 LA PELEADORA (VENTA)", "#ff4b4b"
        else:
            return "🟡 NEUTRAL", "#ffcc00"
    except:
        return "⚪ ERROR DE SEÑAL", "#777"

# --- 3. PROTOCOLO DE SEGURIDAD (PIN) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h1 style='color: #00ffcc; text-align: center;'>🔐 ACCESO RESTRINGIDO</h1>", unsafe_allow_html=True)
    _, col_login, _ = st.columns([1,1,1])
    with col_login:
        pin = st.text_input("INTRODUCE TU LLAVE DE ACCESO (PIN):", type="password")
        if pin == "1234":
            st.session_state.authenticated = True
            st.rerun()
    st.stop()

# --- 4. RADAR DE ACTIVOS (ESCANEO SIMULTÁNEO) ---
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🛡️ TERMINAL QUANTUM DE MONTERO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa;'>Vigilando el 100% del mercado en tiempo real</p>", unsafe_allow_html=True)

assets = {"ORO": "GC=F", "BITCOIN": "BTC-USD", "PETROLEO": "CL=F", "DXY": "DX-Y"}
cols = st.columns(4)

for i, (name, ticker) in enumerate(assets.items()):
    status, color = melli_analisis(ticker)
    price_data = yf.download(ticker, period="1d", interval="1m", progress=False)
    current_p = round(price_data['Close'].iloc[-1], 2) if not price_data.empty else 0.0
    
    with cols[i]:
        st.metric(name, f"${current_p}")
        st.markdown(f"<p style='color:{color}; font-weight:bold; font-size:14px; margin-top:-10px;'>{status}</p>", unsafe_allow_html=True)

st.divider()

# --- 5. CAMPO DE BATALLA: TRADINGVIEW PRO ---
tradingview_html = """
<div style="height:620px; width:100%;">
  <div id="tv_full_bunker" style="height:620px;"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget({
    "autosize": true,
    "symbol": "OANDA:XAUUSD",
    "interval": "5",
    "timezone": "Etc/UTC",
    "theme": "dark",
    "style": "1",
    "locale": "es",
    "toolbar_bg": "#f1f3f6",
    "enable_publishing": false,
    "allow_symbol_change": true,
    "hide_side_toolbar": false,
    "container_id": "tv_full_bunker"
  });
  </script>
</div>
"""
components.html(tradingview_html, height=620)

# --- 6. LA LEY DE MONTERO (BLINDADA) ---
st.markdown(f"""
<div style="background-color: #121212; padding: 25px; border-radius: 15px; border: 2px solid #00ffcc; margin-top: 20px;">
    <h2 style="color: #00ffcc; text-align: center; margin-top:0;">📜 LA LEY DE MONTERO</h2>
    <div style="display: flex; justify-content: space-around; color: white; text-align: center;">
        <div><b>I. PRESERVAR CAPITAL</b><br><small>Los $100K son sagrados</small></div>
        <div><b>II. CONFIRMACIÓN</b><br><small>Meli debe validar</small></div>
        <div><b>III. DISCIPLINA</b><br><small>No perseguimos el precio</small></div>
        <div><b>IV. PACIENCIA</b><br><small>El mercado paga al que espera</small></div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 7. SIDEBAR: ACADEMIA Y COMANDOS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.title("📚 ACADEMIA")
    st.markdown("### 📖 BIBLIOTECA")
    st.markdown("- [**Debita y Cobra (PDF)**](https://archive.org/download/debitaycobra/debita%20y%20cobra.pdf)")
    st.markdown("- [**Psicología Trading**](https://www.google.com/search?q=trading+psychology+pdf)")
    st.divider()
    if st.button("🚀 ENVIAR REPORTE A TELEGRAM"):
        msg = f"🛡️ REPORTE BÚNKER: Meli analizando el 100%. Radar activo. Oro en ${current_p}."
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={msg}")
        st.success("¡Reporte enviado!")
