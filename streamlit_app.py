import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz
import time

# ==============================================================================
# 1. ARQUITECTURA MAESTRA DEL SISTEMA (LAYOUT)
# ==============================================================================
# Definimos la configuración de página con el máximo detalle posible
st.set_page_config(
    page_title="MELI BÚNKER v41 - TITÁN EDITION",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CAPA DE ESTILOS PERSONALIZADOS (CSS DARK MODE)
# ==============================================================================
# Aquí expandimos el diseño para que el búnker tenga una identidad visual única
st.markdown("""
    <style>
    /* Estética General del Búnker */
    .main { background-color: #0d1117; }
    
    /* Diseño de las Métricas del Radar */
    [data-testid="stMetricValue"] { font-size: 2rem !important; color: #00ffcc !important; }
    .stMetric { 
        background-color: #161b22; 
        padding: 25px; 
        border-radius: 15px; 
        border: 1px solid #30363d;
        box-shadow: 0 5px 15px rgba(0,0,0,0.4);
        transition: transform 0.3s ease;
    }
    .stMetric:hover { transform: translateY(-5px); border-color: #00ffcc; }

    /* Tarjetas de Auditoría del 90% */
    .audit-card { 
        padding: 30px; 
        border-radius: 20px; 
        margin-bottom: 25px; 
        border-left: 12px solid; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        background: #0d1117;
    }
    .win-90 { border-left-color: #00ffcc; border-top: 1px solid #00ffcc22; }
    .loss-90 { border-left-color: #ff4b4b; border-top: 1px solid #ff4b4b22; }
    
    /* Títulos de Alto Impacto */
    .title-90 { font-size: 32px; font-weight: 800; letter-spacing: 2px; color: #fff; }
    .verdict-text { font-size: 20px; font-weight: 400; color: #8b949e; margin-top: 10px; }
    .percentage-highlight { font-size: 28px; font-weight: bold; color: #00ffcc; }
    
    /* Personalización del Slider (La Petaca) */
    .stSlider { padding: 30px 0; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. MÓDULO DE COMUNICACIÓN CRÍTICA (MELI & TELEGRAM)
# ==============================================================================
# Configuración de los canales de salida de información
TELEGRAM_TOKEN = "8613807854:AAEtSHlv1n0YYJxpjvuduGeXoVca9-jRfWo"
TELEGRAM_CHAT_ID = "8350001201"

def melli_vocalize(text_to_speak):
    """
    Función para inyectar voz sintetizada. 
    Meli se comunica directamente con el Comandante Montero.
    """
    js_vocal = f"""
    <script>
    var speech = new SpeechSynthesisUtterance('{text_to_speak}');
    speech.lang = 'es-ES';
    speech.pitch = 1.1;
    speech.rate = 0.95;
    window.speechSynthesis.speak(speech);
    </script>
    """
    components.html(js_vocal, height=0)

# ==============================================================================
# 4. CAPA DE SEGURIDAD Y ESTADO DE SESIÓN
# ==============================================================================
# Protocolo de inicio para asegurar acceso exclusivo
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; color: #00ffcc; margin-top: 10%;'>🔐 BÚNKER MONTERO: SISTEMA BLOQUEADO</h1>", unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 1, 1])
    with col_login:
        master_key = st.text_input("INTRODUCE TU LLAVE DE MANDO:", type="password")
        if master_key == "1234":
            st.session_state.authenticated = True
            melli_vocalize("Sistemas Titán en línea. Bienvenida Comandante Montero.")
            st.rerun()
    st.stop()

# ==============================================================================
# 5. MOTOR DE INTELIGENCIA SEMANAL (AUDITORÍA DEL 90%)
# ==============================================================================
def perform_deep_audit(ticker_code):
    """
    Analiza la volatilidad y el rendimiento de la semana anterior.
    Busca los movimientos que se acercan al objetivo del 90%.
    """
    try:
        # Extraemos 15 días de data para tener un contexto sólido
        asset = yf.Ticker(ticker_code)
        history_df = asset.history(period="15d")
        
        if len(history_df) < 7:
            return None
            
        final_p = history_df['Close'].iloc[-1]
        start_p = history_df['Close'].iloc[-7] # Punto de control: hace 1 semana
        
        net_performance = ((final_p - start_p) / start_p) * 100
        
        # Lógica de clasificación estratégica Montero
        if net_performance >= 10.0:
            status_label = "💥 MOVIMIENTO EXPLOSIVO: NOSOTROS GANAMOS"
            css_class = "win-90"
        elif net_performance <= -10.0:
            status_label = "⚠️ ALERTA DE COLAPSO: NOSOTROS PERDIMOS"
            css_class = "loss-90"
        else:
            status_label = "Mercado en Consolidación (Bajo impacto)"
            css_class = "neutral"
            
        return {
            "Ticker": ticker_code,
            "Rendimiento": round(net_performance, 2),
            "Precio": round(final_p, 2),
            "Veredicto": status_label,
            "Clase": css_class
        }
    except Exception as e:
        return None

# Definición del Radar de Activos (Expandido)
activos_montero = {
    "ORO (XAU/USD)": "GC=F", 
    "BITCOIN (BTC)": "BTC-USD", 
    "NVIDIA (NVDA)": "NVDA",
    "NASDAQ 100": "NQ=F", 
    "TESLA (TSLA)": "TSLA", 
    "SOLANA (SOL)": "SOL-USD",
    "PETRÓLEO WTI": "CL=F", 
    "APPLE (AAPL)": "AAPL",
    "DXY (DÓLAR)": "DX-Y"
}

# ==============================================================================
# 6. PANEL DE CONTROL FRONTAL (RADAR DE TIEMPO REAL)
# ==============================================================================
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🛡️ TERMINAL QUANTUM v41: TITÁN</h1>", unsafe_allow_html=True)

# Reloj de Wall Street
ny_tz = pytz.timezone('America/New_York')
current_ny = datetime.now(ny_tz).strftime("%H:%M:%S")
st.markdown(f"<p style='text-align: center; color: #8b949e; font-size: 1.2rem;'>ESTATUS: OPERATIVO | NY TIME: {current_ny}</p>", unsafe_allow_html=True)

# Generación del Radar de Precios
audit_data_list = []
radar_cols = st.columns(len(activos_montero))

for idx, (label, symbol) in enumerate(activos_montero.items()):
    audit_res = perform_deep_audit(symbol)
    if audit_res:
        audit_res["Nombre"] = label
        audit_data_list.append(audit_res)
        with radar_cols[idx]:
            st.metric(label, f"${audit_res['Precio']}", f"{audit_res['Rendimiento']}%")

st.divider()

# ==============================================================================
# 7. CAMPO DE BATALLA (GRÁFICO CON PETACA Y NOTICIAS)
# ==============================================================================
col_battle, col_intel = st.columns([3, 1])

with col_battle:
    st.subheader("📊 GRÁFICO TÉCNICO ADAPTATIVO")
    
    # La Petaca (Slider de Control de Dimensión)
    size_petaca = st.slider("📏 CONTROL DE DIMENSIÓN DEL GRÁFICO (PIXELES):", 300, 1200, 650, 50)
    
    # Widget de TradingView Profesional
    tradingview_widget = f"""
    <div style="height:{size_petaca}px; width:100%;">
      <div id="tv_v41" style="height:{size_petaca}px;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "autosize": true, "symbol": "OANDA:XAUUSD", "interval": "1",
        "timezone": "Etc/UTC", "theme": "dark", "style": "1", "locale": "es",
        "toolbar_bg": "#f1f3f6", "enable_publishing": false, 
        "withdateranges": true, "hide_side_toolbar": false,
        "allow_symbol_change": true, "details": true, "hotlist": true,
        "container_id": "tv_v41"
      }});
      </script>
    </div>
    """
    components.html(tradingview_widget, height=size_petaca)

with col_intel:
    st.subheader("📰 INTELIGENCIA DE NOTICIAS")
    news_ticker_widget = """
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-timeline.js" async>
      { "feedMode": "all_symbols", "colorTheme": "dark", "width": "100%", "height": "750", "locale": "es" }
      </script>
    </div>
    """
    components.html(news_ticker_widget, height=750)

# ==============================================================================
# 8. LA LIBRERÍA DE LOS 90%: AUDITORÍA DE IMPACTO MASIVO
# ==============================================================================
st.divider()
st.markdown("<h2 style='text-align: center; color: #00ffcc;'>📚 LIBRERÍA: EL REPORTE DEL 90%</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e;'>Análisis de los movimientos de mayor impacto en la semana anterior</p>", unsafe_allow_html=True)

# Procesamiento de datos para la clasificación
df_audit_final = pd.DataFrame(audit_data_list)
top_winners_nosotros = df_audit_final.sort_values(by="Rendimiento", ascending=False).head(3)
top_losers_nosotros = df_audit_final.sort_values(by="Rendimiento", ascending=True).head(3)

col_win_arch, col_loss_arch = st.columns(2)

with col_win_arch:
    st.markdown("### 🏆 LOS 3 GANADORES NOSOTROS")
    for _, row_w in top_winners_nosotros.iterrows():
        st.markdown(f"""
        <div class='audit-card win-90'>
            <div class='title-90'>{row_w['Nombre']}</div>
            <div class='percentage-highlight'>Rendimiento: {row_w['Rendimiento']}%</div>
            <div class='verdict-text'>{row_w['Veredicto']}</div>
        </div>
        """, unsafe_allow_html=True)

with col_loss_arch:
    st.markdown("### 💀 LOS 3 PERDEDORES NOSOTROS")
    for _, row_l in top_losers_nosotros.iterrows():
        st.markdown(f"""
        <div class='audit-card loss-90'>
            <div class='title-90'>{row_l['Nombre']}</div>
            <div class='percentage-highlight' style='color:#ff4b4b;'>Rendimiento: {row_l['Rendimiento']}%</div>
            <div class='verdict-text'>{row_l['Veredicto']}</div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 9. BARRA LATERAL (SIDEBAR) Y COMANDOS DE VOZ
# ==============================================================================
with st.sidebar:
    st.title("💎 COMANDO ELITE MONTERO")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=120)
    st.divider()
    
    st.markdown("### 🗣️ INTERFAZ DE VOZ")
    if st.button("🎙️ MELI: RESUMEN DE ESTRATEGIA"):
        lider = top_winners_nosotros.iloc[0]['Nombre']
        caida = top_losers_nosotros.iloc[0]['Nombre']
        speech_text = f"Comandante Montero, reporte del noventa por ciento analizado. El líder semanal es {lider}. Por el contrario, la mayor caída fue en {caida}. El gráfico adaptativo está listo para su análisis."
        melli_vocalize(speech_text)
    
    st.divider()
    st.markdown("### 📜 LEYES DEL BÚNKER")
    st.info("I. El Capital es Sagrado\nII. Meli Audita la Semana\nIII. Disciplina Ante el Gráfico\nIV. El 90% es el Objetivo")
    
    st.divider()
    st.markdown("### 📖 BIBLIOTECA DEL ÉXITO")
    st.markdown("- [Padre Rico, Padre Pobre](https://archive.org/details/padre-rico-padre-pobre_202011)")
    st.markdown("- [Mente Millonaria](https://www.google.com/search?q=secretos+mente+millonaria+pdf)")
    st.markdown("- [Debita y Cobra](https://archive.org/download/debitaycobra/debita%20y%20cobra.pdf)")
    
    st.divider()
    if st.button("🚀 ENVIAR AUDITORÍA A TELEGRAM"):
        tele_msg = f"🛡️ BÚNKER v41: Reporte del 90% completado. Ganador Semanal: {top_winners_nosotros.iloc[0]['Nombre']}."
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={tele_msg}")

# Pie de página técnico para conteo de líneas y estatus
st.caption("Terminal v41.0 | Montero Quantum Titán | Ingeniería de Datos Avanzada | 250+ Líneas")
# ==============================================================================
# FIN DEL CÓDIGO MAESTRO
# ==============================================================================
