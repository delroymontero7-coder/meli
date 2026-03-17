# ==============================================================================
# TERMINAL QUANTUM v45 - EDICIÓN DE GESTIÓN DE CAPITAL MONTERO
# PROPIEDAD DE: COMANDO MONTERO ($100K PORTFOLIO)
# FECHA DE ACTUALIZACIÓN: 2026
# ==============================================================================

import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
import pytz
import json

# ------------------------------------------------------------------------------
# 1. CONFIGURACIÓN ESTRUCTURAL DEL SISTEMA
# ------------------------------------------------------------------------------
# Definimos el comportamiento de la ventana y el estado inicial del sidebar
st.set_page_config(
    page_title="MELI BÚNKER v45 - TITÁN ESTRUCTURAL",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------------------------
# 2. CAPA DE DISEÑO Y ESTILOS AVANZADOS (CSS)
# ------------------------------------------------------------------------------
# Expandimos el CSS para asegurar que cada elemento tenga su espacio
st.markdown("""
    <style>
    /* Fondo principal y contenedores */
    .main { 
        background-color: #0d1117; 
    }
    
    /* Diseño de los Tickers de Precios */
    [data-testid="stMetricValue"] { 
        font-size: 1.8rem !important; 
        color: #00ffcc !important; 
    }
    
    .stMetric { 
        background-color: #161b22; 
        padding: 25px; 
        border-radius: 15px; 
        border: 1px solid #30363d; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    /* Estilo del Diario de Operaciones */
    .journal-card {
        background-color: #1c2128; 
        padding: 25px; 
        border-radius: 20px; 
        border-left: 10px solid #00ffcc; 
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.6);
    }
    
    /* Paleta de Colores Estratégica */
    .text-gold { color: #ffd700; font-weight: bold; font-size: 1.2rem; }
    .text-cyan { color: #00ffcc; font-weight: bold; font-size: 1.2rem; }
    .text-red { color: #ff4b4b; font-weight: bold; font-size: 1.2rem; }
    
    /* Personalización del Slider (La Petaca) */
    .stSlider > div [data-baseweb="slider"] {
        background-color: #161b22;
    }
    </style>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 3. VARIABLES DE ENTORNO Y CONECTIVIDAD
# ------------------------------------------------------------------------------
# Credenciales del Búnker Móvil
TELEGRAM_TOKEN = "8613807854:AAEtSHlv1n0YYJxpjvuduGeXoVca9-jRfWo"
TELEGRAM_CHAT_ID = "8350001201"

# ------------------------------------------------------------------------------
# 4. FUNCIONES DE COMUNICACIÓN (TELEGRAM & VOZ)
# ------------------------------------------------------------------------------
def send_telegram_broadcast(message_text):
    """
    Motor de envío masivo a Telegram. 
    Usa POST para evitar limitaciones de longitud de URL.
    """
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data_payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_text,
        "parse_mode": "HTML"
    }
    
    try:
        req = requests.post(api_url, data=data_payload)
        if req.status_code == 200:
            st.toast("REPORTE ENVIADO CON ÉXITO", icon="📡")
        else:
            st.error(f"Error de Servidor: {req.status_code}")
    except Exception as error:
        st.error(f"Fallo de Conexión: {error}")

def melli_vocalize(speech_input):
    """
    Módulo de Síntesis de Voz. 
    Meli se comunica por audio con el Comandante.
    """
    vocal_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{speech_input}');
    msg.lang = 'es-ES';
    msg.rate = 0.95;
    window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(vocal_code, height=0)

# ------------------------------------------------------------------------------
# 5. GESTIÓN DE SESIÓN Y SEGURIDAD
# ------------------------------------------------------------------------------
if "journal" not in st.session_state:
    st.session_state.journal = []

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Protocolo de Bloqueo
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; color: #00ffcc; margin-top: 10%;'>🔒 ACCESO RESTRINGIDO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Introduzca la clave maestra para activar el búnker.</p>", unsafe_allow_html=True)
    
    _, auth_center, _ = st.columns([1, 1, 1])
    with auth_center:
        pin = st.text_input("PIN DE MANDO:", type="password")
        if pin == "1234":
            st.session_state.authenticated = True
            melli_vocalize("Sistemas Titán en línea. Bienvenido, Montero.")
            st.rerun()
    st.stop()

# ------------------------------------------------------------------------------
# 6. MOTOR DE ANÁLISIS DE MERCADO (DATA CLOUD)
# ------------------------------------------------------------------------------
def fetch_market_insights(ticker_symbol):
    """
    Extrae datos históricos y actuales de Yahoo Finance.
    """
    try:
        ticker_obj = yf.Ticker(ticker_symbol)
        history = ticker_obj.history(period="5d")
        
        if history.empty:
            return None
            
        current_price = history['Close'].iloc[-1]
        previous_price = history['Close'].iloc[-2]
        price_change = ((current_price - previous_price) / previous_price) * 100
        
        return {
            "last": round(current_price, 2),
            "change": round(price_change, 2)
        }
    except:
        return None

# Lista de activos bajo vigilancia
radar_list = {
    "ORO": "GC=F", 
    "BITCOIN": "BTC-USD", 
    "NASDAQ": "NQ=F", 
    "NVIDIA": "NVDA", 
    "TESLA": "TSLA"
}

# ------------------------------------------------------------------------------
# 7. INTERFAZ: RADAR DE PRECIOS
# ------------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🛡️ TERMINAL TITÁN v45</h1>", unsafe_allow_html=True)

ticker_columns = st.columns(len(radar_list))

for index, (name, symbol) in enumerate(radar_list.items()):
    market_data = fetch_market_insights(symbol)
    if market_data:
        with ticker_columns[index]:
            st.metric(name, f"${market_data['last']}", f"{market_data['change']}%")

st.divider()

# ------------------------------------------------------------------------------
# 8. INTERFAZ: REGISTRO ESTRATÉGICO Y GRÁFICO
# ------------------------------------------------------------------------------
col_input, col_view = st.columns([1.5, 2])

with col_input:
    st.subheader("📝 REGISTRO DE POSICIÓN")
    
    # Formulario de entrada de datos
    with st.container():
        asset_choice = st.selectbox("ACTIVO:", list(radar_list.keys()))
        trade_dir = st.radio("DIRECCIÓN:", ["LONG (COMPRA)", "SHORT (VENTA)"], horizontal=True)
        
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            entry_p = st.number_input("PUNTO DE ENTRADA:", format="%.2f")
        with row1_col2:
            sl_p = st.number_input("STOP LOSS (RIESGO):", format="%.2f")
            
        tp_p = st.number_input("TAKE PROFIT (META):", format="%.2f")
        strategy_note = st.text_area("ANÁLISIS DE LA OPERACIÓN:")
        
        if st.button("💾 CONFIRMAR Y NOTIFICAR AL MÓVIL"):
            # Guardar en memoria local
            trade_record = {
                "id": len(st.session_state.journal) + 1,
                "time": datetime.now().strftime("%H:%M:%S"),
                "asset": asset_choice,
                "type": trade_dir,
                "entry": entry_p,
                "sl": sl_p,
                "tp": tp_p,
                "note": strategy_note
            }
            st.session_state.journal.append(trade_record)
            
            # Construcción del reporte para Telegram
            report_body = (
                f"<b>🚀 ALERTA DE TRADE: {asset_choice}</b>\n\n"
                f"<b>Tipo:</b> {trade_dir}\n"
                f"<b>Entrada:</b> ${entry_p}\n"
                f"<b>Stop Loss:</b> ${sl_p}\n"
                f"<b>Take Profit:</b> ${tp_p}\n\n"
                f"<i>Estrategia: {strategy_note}</i>"
            )
            
            send_telegram_broadcast(report_body)
            melli_vocalize(f"Operación en {asset_choice} enviada a Telegram.")

with col_view:
    st.subheader("📊 MONITOR TÉCNICO")
    
    # Control de la Petaca (Slider)
    graph_h = st.slider("📏 ALTURA DEL MONITOR:", 300, 1000, 600, 50)
    
    # Widget de TradingView
    tv_code = f"""
    <div style="height:{graph_h}px;">
      <div id="tv_frame" style="height:{graph_h}px;"></div>
      <script src="https://s3.tradingview.com/tv.js"></script>
      <script>
      new TradingView.widget({{
        "autosize": true,
        "symbol": "OANDA:XAUUSD",
        "interval": "1",
        "theme": "dark",
        "container_id": "tv_frame"
      }});
      </script>
    </div>
    """
    components.html(tv_code, height=graph_h)

# ------------------------------------------------------------------------------
# 9. LIBRERÍA: HISTORIAL DE BATALLAS
# ------------------------------------------------------------------------------
st.divider()
st.subheader("📚 LIBRERÍA DE OPERACIONES")

if not st.session_state.journal:
    st.info("No hay registros previos en esta sesión.")
else:
    # Mostramos los registros en orden inverso (más reciente primero)
    for record in reversed(st.session_state.journal):
        st.markdown(f"""
        <div class="journal-card">
            <div style="display: flex; justify-content: space-between;">
                <span style="font-size: 24px; font-weight: bold; color: #00ffcc;">
                    {record['asset']} | {record['type']}
                </span>
                <span style="color: #8b949e;">ID: #{record['id']} | {record['time']}</span>
            </div>
            <hr style="border-color: #30363d;">
            <div style="display: flex; justify-content: space-around;">
                <div><small>ENTRADA</small><br><span class="text-cyan">${record['entry']}</span></div>
                <div><small>STOP LOSS</small><br><span class="text-red">${record['sl']}</span></div>
                <div><small>TAKE PROFIT</small><br><span class="text-gold">${record['tp']}</span></div>
            </div>
            <div style="margin-top: 15px; font-style: italic; color: #fff;">
                <strong>Análisis:</strong> {record['note']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 10. BARRA LATERAL (SIDEBAR) Y UTILIDADES
# ------------------------------------------------------------------------------
with st.sidebar:
    st.title("💎 COMANDO ELITE")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=120)
    
    st.divider()
    if st.button("🎙️ MELI: RESUMEN DE SISTEMA"):
        melli_vocalize("Reporte Titan 45 activo. Telegram conectado y diario listo para el registro.")
        
    st.divider()
    st.markdown("### 📖 BIBLIOTECA")
    st.markdown("- [Mente Millonaria](https://www.google.com)")
    st.markdown("- [Padre Rico, Padre Pobre](https://archive.org)")
    
    st.divider()
    if st.button("🚀 TEST DE CONEXIÓN TELEGRAM"):
        send_telegram_broadcast("🛡️ <b>TEST TITÁN:</b> Conexión exitosa desde la v45.")

# Créditos Técnicos
st.caption("v45.0 | Arquitectura Titán | Montero Elite | 300+ Líneas de Código Estructural")
# ==============================================================================
# FIN DEL SISTEMA
# ==============================================================================
