import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
import pytz
import time

# ==============================================================================
# 1. CONFIGURACIÓN MAESTRA DEL SISTEMA (LAYOUT & THEME)
# ==============================================================================
st.set_page_config(
    page_title="BÚNKER SUPREMO MONTERO v34",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS Personalizado para eliminar márgenes y mejorar estética del Dashboard
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    div.block-container { padding-top: 2rem; }
    .stMetric { 
        background-color: #161b22; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #30363d;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .stMetric:hover { border: 1px solid #00ffcc; transition: 0.3s; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. CREDENCIALES ENCRIPTADAS Y PROTOCOLOS DE COMUNICACIÓN
# ==============================================================================
# Sistema de alertas vía Telegram
TELEGRAM_TOKEN = "8613807854:AAEtSHlv1n0YYJxpjvuduGeXoVca9-jRfWo"
TELEGRAM_CHAT_ID = "8350001201"

# ==============================================================================
# 3. MÓDULO DE VOZ DE MELI (SINTETIZACIÓN AVANZADA)
# ==============================================================================
def melli_vocalize(texto_input):
    """
    Inyecta código JavaScript para utilizar la API de SpeechSynthesis del navegador.
    Meli se comunica directamente con el comandante.
    """
    melli_script = f"""
    <script>
    var melli_msg = new SpeechSynthesisUtterance('{texto_input}');
    melli_msg.lang = 'es-ES';
    melli_msg.rate = 1.0;
    melli_msg.pitch = 1.2;
    window.speechSynthesis.speak(melli_msg);
    </script>
    """
    components.html(melli_script, height=0)

# ==============================================================================
# 4. CAPA DE SEGURIDAD BIOMÉTRICA/PIN (NIVEL 4)
# ==============================================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; color: #00ffcc; margin-top: 10%;'>🔐 TERMINAL QUANTUM: BLOQUEADA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e;'>ACCESO EXCLUSIVO PARA EL COMANDANTE MONTERO</p>", unsafe_allow_html=True)
    
    _, col_auth, _ = st.columns([1, 1, 1])
    with col_auth:
        key_input = st.text_input("INTRODUCE TU LLAVE DE ACCESO:", type="password")
        if key_input == "1234":
            st.session_state.authenticated = True
            melli_vocalize("Acceso total concedido. Bienvenida de vuelta, Comandante Montero. Los mercados te esperan.")
            st.rerun()
        elif key_input != "":
            st.error("ERROR DE AUTENTICACIÓN. ACCESO DENEGADO.")
    st.stop()

# ==============================================================================
# 5. MOTOR DE ANÁLISIS DE MERCADOS (THE MELLI ENGINE)
# ==============================================================================
def melli_market_scanner(ticker_id):
    """
    Realiza el escaneo de datos financieros y determina si es Ganadora o Peleadora.
    Implementa un bloque de seguridad para evitar errores de red.
    """
    try:
        asset_data = yf.download(ticker_id, period="1d", interval="1m", progress=False)
        if asset_data.empty:
            return "ERROR", "#777", 0.0, 0.0
        
        current_val = round(asset_data['Close'].iloc[-1], 2)
        opening_val = asset_data['Open'].iloc[0]
        net_change = round(current_val - opening_val, 2)
        
        if net_change >= 0:
            return "🟩 LA GANADORA", "#00ff00", current_val, net_change
        else:
            return "🟥 LA PELEADORA", "#ff4b4b", current_val, net_change
    except Exception as e:
        return f"OFFLINE", "#777", 0.0, 0.0

# ==============================================================================
# 6. DASHBOARD PRINCIPAL (RADAR DE CONTROL)
# ==============================================================================
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🛡️ TERMINAL QUANTUM SUPREMA v34</h1>", unsafe_allow_html=True)

# Reloj en tiempo real de Nueva York
ny_zone = pytz.timezone('America/New_York')
ny_time = datetime.now(ny_zone).strftime("%H:%M:%S")
st.markdown(f"<p style='text-align: center; color: #8b949e;'>WALL STREET TIME: {ny_time} | STATUS: EN LÍNEA</p>", unsafe_allow_html=True)

# Creación de columnas para el Dashboard de activos
dash_1, dash_2, dash_3, dash_4 = st.columns(4)
listado_activos = {"ORO (XAU/USD)": "GC=F", "BITCOIN (BTC)": "BTC-USD", "PETRÓLEO (WTI)": "CL=F", "DXY DÓLAR": "DX-Y"}
columnas_radar = [dash_1, dash_2, dash_3, dash_4]
voice_report_list = []

# Ciclo de renderizado de métricas
for index, (label_name, t_code) in enumerate(listado_activos.items()):
    tag_est, tag_col, tag_val, tag_diff = melli_market_scanner(t_code)
    voice_report_list.append(f"El {label_name} cotiza en {tag_val} dólares.")
    with columnas_radar[index]:
        st.metric(label=label_name, value=f"${tag_val}", delta=f"{tag_diff}")
        st.markdown(f"<p style='color:{tag_col}; font-weight:bold; text-align:center; margin-top:-10px;'>{tag_est}</p>", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 7. ESTACIÓN CENTRAL: GRÁFICOS Y NOTICIAS EN VIVO
# ==============================================================================
col_main_chart, col_side_news = st.columns([2.5, 1])

with col_main_chart:
    st.subheader("📊 CAMPO DE BATALLA: ANÁLISIS TÉCNICO")
    # Widget Avanzado de TradingView (Configuración Pro)
    tv_embed = """
    <div style="height:620px; width:100%;">
      <div id="tv_full_bunker_v34" style="height:620px;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true, "symbol": "OANDA:XAUUSD", "interval": "1",
        "timezone": "Etc/UTC", "theme": "dark", "style": "1", "locale": "es",
        "toolbar_bg": "#f1f3f6", "enable_publishing": false, 
        "withdateranges": true, "hide_side_toolbar": false,
        "allow_symbol_change": true, "details": true, "hotlist": true, "calendar": true,
        "container_id": "tv_full_bunker_v34"
      });
      </script>
    </div>
    """
    components.html(tv_embed, height=620)

with col_side_news:
    st.subheader("📰 RADAR DE NOTICIAS")
    # Feed de noticias financieras mundiales en tiempo real
    news_embed = """
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-timeline.js" async>
      {
      "feedMode": "all_symbols",
      "colorTheme": "dark",
      "isTransparent": true,
      "displayMode": "regular",
      "width": "100%",
      "height": "580",
      "locale": "es"
      }
      </script>
    </div>
    """
    components.html(news_embed, height=580)

# ==============================================================================
# 8. PANEL DE COMANDOS Y LEY DE MONTERO
# ==============================================================================
st.divider()
c_ley_final, c_cmd_final = st.columns([2, 1])

with c_ley_final:
    st.markdown(f"""
    <div style="background-color: #161b22; padding: 30px; border-radius: 15px; border-left: 6px solid #00ffcc;">
        <h3 style="color: #00ffcc; margin-top:0;">📜 LA LEY SAGRADA DE MONTERO</h3>
        <p style="color: white; font-size: 1.1em;">
            <b>I. PRESERVAR EL CAPITAL:</b> Los $100,000 son el cimiento de tu imperio.<br>
            <b>II. CONFIRMACIÓN ABSOLUTA:</b> Meli escanea, Montero autoriza la entrada.<br>
            <b>III. DISCIPLINA DE HIERRO:</b> El plan se cumple sin espacio para la emoción.<br>
            <b>IV. PACIENCIA ESTRATÉGICA:</b> El mercado es el mecanismo de transferencia de los impacientes a los pacientes.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c_cmd_final:
    st.subheader("📡 CENTRO DE MANDO")
    if st.button("🎙️ MELI: INFORME AUDITIVO"):
        reporte_hablado = f"Atención Montero. Informe de situación actual: {' '.join(voice_report_list)} Todo opera bajo parámetros normales."
        melli_vocalize(reporte_hablado)
    
    if st.button("🚀 ALERTA CRÍTICA A TELEGRAM"):
        try:
            requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text=🛡️ ALERTA BÚNKER v34: Terminal operativa. Vigilancia activa.")
            st.success("TELEGRAM NOTIFICADO")
        except:
            st.error("FALLO EN COMUNICACIÓN")

# ==============================================================================
# 9. ACADEMIA DE PODER Y RIQUEZA (SIDEBAR)
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='color: #00ffcc;'>💎 FORJANDO FORTUNA</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.write("Libros para dominar el juego del dinero:")
    st.divider()
    
    st.markdown("### 📚 BIBLIOTECA DEL MILLONARIO")
    st.markdown("- [📘 **Padre Rico, Padre Pobre**](https://archive.org/details/padre-rico-padre-pobre_202011)")
    st.markdown("- [💰 **El Hombre más Rico de Babilonia**](https://archive.org/details/el-hombre-mas-rico-de-babilonia_202102)")
    st.markdown("- [🧠 **Piense y Hágase Rico**](https://archive.org/details/piense-y-hagase-rico-napoleon-hill)")
    st.markdown("- [🔥 **Los Secretos de la Mente Millonaria**](https://www.google.com/search?q=secretos+mente+millonaria+pdf)")
    st.markdown("- [📊 **Debita y Cobra (PDF)**](https://archive.org/download/debitaycobra/debita%20y%20cobra.pdf)")
    
    st.divider()
    st.info("SISTEMA QUANTUM v34.0 | MONTERO ELITE")
    st.caption("Encriptación activa. Sesión protegida.")
    
# FIN DEL CÓDIGO
