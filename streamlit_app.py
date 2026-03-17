import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
import pytz

# ==========================================
# 1. CONFIGURACIÓN E IDENTIDAD VISUAL
# ==========================================
st.set_page_config(
    page_title="BÚNKER SUPREMO MONTERO",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo de Fondo y Fuentes (CSS Personalizado)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .stMetric:hover { border: 1px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. CREDENCIALES Y PROTOCOLOS CRÍTICOS
# ==========================================
TELEGRAM_TOKEN = "8613807854:AAEtSHlv1n0YYJxpjvuduGeXoVca9-jRfWo"
TELEGRAM_CHAT_ID = "8350001201"

# ==========================================
# 3. EL CEREBRO AUDITIVO DE MELI (VOZ)
# ==========================================
def melli_habla(texto):
    """Función para que Meli use la voz del sistema"""
    componente_voz = f"""
    <script>
    var mensaje = new SpeechSynthesisUtterance('{texto}');
    mensaje.lang = 'es-ES';
    mensaje.rate = 1.0;
    mensaje.pitch = 1.1;
    window.speechSynthesis.speak(mensaje);
    </script>
    """
    components.html(componente_voz, height=0)

# ==========================================
# 4. PROTOCOLO DE SEGURIDAD (PIN MAESTRO)
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; color: #00ffcc; margin-top: 50px;'>🛡️ SISTEMA ENCRIPTADO MONTERO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ff4b4b;'>BLOQUEADO: REQUIERE AUTORIZACIÓN NIVEL 4</p>", unsafe_allow_html=True)
    
    _, col_login, _ = st.columns([1, 1, 1])
    with col_login:
        pin = st.text_input("INTRODUCE TU LLAVE MAESTRA (PIN):", type="password")
        if pin == "1234":
            st.session_state.authenticated = True
            melli_habla("Acceso autorizado. Bienvenida a casa, Comandante Montero. Iniciando sistemas de radar.")
            st.rerun()
        elif pin != "":
            st.error("PIN INCORRECTO. INTENTO REGISTRADO.")
    st.stop()

# ==========================================
# 5. MOTOR DE ANÁLISIS: GANADORA vs PELEADORA
# ==========================================
def melli_engine(ticker):
    try:
        # Descarga de datos de alta frecuencia
        data_melli = yf.download(ticker, period="1d", interval="5m", progress=False)
        if data_melli.empty:
            return "N/A", "#777", 0.0, 0.0
        
        # Lógica de Medias para la Ganadora/Peleadora
        ema_rapida = data_melli['Close'].ewm(span=9).mean().iloc[-1]
        ema_lenta = data_melli['Close'].ewm(span=21).mean().iloc[-1]
        precio = data_melli['Close'].iloc[-1]
        apertura = data_melli['Open'].iloc[0]
        variacion = precio - apertura
        
        if precio > ema_rapida and ema_rapida > ema_lenta:
            return "🟩 LA GANADORA", "#00ff00", round(precio, 2), round(variacion, 2)
        elif precio < ema_rapida and ema_rapida < ema_lenta:
            return "🟥 LA PELEADORA", "#ff4b4b", round(precio, 2), round(variacion, 2)
        else:
            return "🟨 NEUTRAL", "#ffcc00", round(precio, 2), round(variacion, 2)
    except:
        return "ERROR", "#777", 0.0, 0.0

# ==========================================
# 6. DASHBOARD PRINCIPAL (EL RADAR)
# ==========================================
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🛡️ TERMINAL QUANTUM SUPREMA v32</h1>", unsafe_allow_html=True)
time_now = datetime.now(pytz.timezone('America/New_York')).strftime("%H:%M:%S")
st.markdown(f"<p style='text-align: center; color: #888;'>NY TIME: {time_now} | STATUS: ONLINE</p>", unsafe_allow_html=True)

# Distribución de Activos en el Dashboard
c1, c2, c3, c4 = st.columns(4)
dashboard_activos = [("ORO (GOLD)", "GC=F"), ("BITCOIN", "BTC-USD"), ("PETRÓLEO", "CL=F"), ("DXY DÓLAR", "DX-Y")]
dashboard_cols = [c1, c2, c3, c4]
reporte_voz = []

for i, (nombre, ticker) in enumerate(dashboard_activos):
    estado, color, valor, cambio = melli_engine(ticker)
    reporte_voz.append(f"El {nombre} está en {valor} dólares.")
    with dashboard_cols[i]:
        st.metric(label=nombre, value=f"${valor}", delta=f"{cambio}")
        st.markdown(f"<p style='color:{color}; font-weight:bold; text-align:center;'>{estado}</p>", unsafe_allow_html=True)

st.divider()

# ==========================================
# 7. CAMPO DE BATALLA: TRADINGVIEW PROFESIONAL
# ==========================================
col_graph, col_ley = st.columns([3, 1])

with col_graph:
    st.subheader("📊 ESTACIÓN DE ANÁLISIS TÉCNICO")
    tv_widget = """
    <div style="height:650px; width:100%;">
      <div id="tv_full_dashboard" style="height:650px;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true, "symbol": "OANDA:XAUUSD", "interval": "1",
        "timezone": "Etc/UTC", "theme": "dark", "style": "1", "locale": "es",
        "toolbar_bg": "#f1f3f6", "enable_publishing": false, 
        "withdateranges": true, "hide_side_toolbar": false,
        "allow_symbol_change": true, "details": true, "hotlist": true,
        "container_id": "tv_full_dashboard"
      });
      </script>
    </div>
    """
    components.html(tv_widget, height=650)

with col_ley:
    st.subheader("🎙️ COMANDOS")
    if st.button("🔊 ESCUCHAR REPORTE DE MELI"):
        melli_habla(f"Reporte del búnker. {' '.join(reporte_voz)} Todo bajo control, Montero.")
    
    st.divider()
    st.subheader("📜 LA LEY DE MONTERO")
    st.markdown("""
        <div style='background-color: #161b22; padding: 15px; border-radius: 10px; border-left: 4px solid #00ffcc;'>
            <p><b>1. PRESERVAR EL CAPITAL:</b> Los $100K son sagrados.</p>
            <p><b>2. CONFIRMACIÓN:</b> Meli valida, Montero ejecuta.</p>
            <p><b>3. DISCIPLINA:</b> Sin emoción, solo estrategia.</p>
            <p><b>4. PACIENCIA:</b> El mercado paga al que sabe esperar.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    if st.button("🚀 ENVIAR ALERTA TELEGRAM"):
        res = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text=🛡️ BÚNKER V32: Mercados en línea. Oro en ${valor}.")
        st.success("¡Mensaje enviado!")

# ==========================================
# 8. BIBLIOTECA DEL MILLONARIO (SIDEBAR)
# ==========================================
with st.sidebar:
    st.markdown("<h1 style='color: #00ffcc;'>📚 ACADEMIA</h1>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=120)
    st.write("Forjando la mente de un dueño de $100K.")
    st.divider()
    
    st.markdown("### 💎 BIBLIOTECA DE PODER")
    st.markdown("""
        - [📘 **Padre Rico, Padre Pobre**](https://archive.org/details/padre-rico-padre-pobre_202011)
        - [💰 **El Hombre más Rico de Babilonia**](https://archive.org/details/el-hombre-mas-rico-de-babilonia_202102)
        - [🧠 **Piense y Hágase Rico**](https://archive.org/details/piense-y-hagase-rico-napoleon-hill)
        - [📊 **Debita y Cobra (PDF)**](https://archive.org/download/debitaycobra/debita%20y%20cobra.pdf)
    """)
    
    st.divider()
    st.info("Terminal Montero v32.0 | 2026 | Encriptación AES-256")
    st.caption("Creado para dominar los mercados globales.")
