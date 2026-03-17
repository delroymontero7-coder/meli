import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
import pytz

# ==============================================================================
# 1. CONFIGURACIÓN DEL BÚNKER DE ALTA VELOCIDAD
# ==============================================================================
st.set_page_config(
    page_title="MELI BÚNKER v36 - HISTORIAL",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Avanzados para el Dashboard y la Librería
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    .stMetric { 
        background-color: #161b22; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #30363d;
    }
    .status-card {
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin-top: 5px;
    }
    .library-box {
        background-color: #1c2128;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #00ffcc;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. CREDENCIALES Y VOZ DE MELI
# ==============================================================================
TELEGRAM_TOKEN = "8613807854:AAEtSHlv1n0YYJxpjvuduGeXoVca9-jRfWo"
TELEGRAM_CHAT_ID = "8350001201"

def melli_vocalize(text):
    js = f"""<script>
    var msg = new SpeechSynthesisUtterance('{text}');
    msg.lang = 'es-ES';
    window.speechSynthesis.speak(msg);
    </script>"""
    components.html(js, height=0)

# ==============================================================================
# 3. PROTOCOLO DE SEGURIDAD
# ==============================================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "history" not in st.session_state:
    st.session_state.history = []

if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; color: #00ffcc; margin-top: 10%;'>🔐 ACCESO RESTRINGIDO MONTERO</h1>", unsafe_allow_html=True)
    _, col_auth, _ = st.columns([1, 1, 1])
    with col_auth:
        pin = st.text_input("PIN MAESTRO:", type="password")
        if pin == "1234":
            st.session_state.authenticated = True
            melli_vocalize("Acceso concedido. Iniciando escaneo de ganadores y perdedores.")
            st.rerun()
    st.stop()

# ==============================================================================
# 4. MOTOR DE ESCANEO Y CLASIFICACIÓN (EL ARCHIVADOR)
# ==============================================================================
def get_market_status(ticker):
    try:
        t = yf.Ticker(ticker)
        df = t.history(period="1d", interval="5m")
        if df.empty: return 0.0, 0.0, "N/A", "#777"
        
        current = df['Close'].iloc[-1]
        change_pct = ((current - df['Open'].iloc[0]) / df['Open'].iloc[0]) * 100
        
        if change_pct >= 0:
            return round(current, 2), round(change_pct, 2), "GANADORA", "#00ff00"
        else:
            return round(current, 2), round(change_pct, 2), "PELEADORA", "#ff4b4b"
    except:
        return 0.0, 0.0, "ERROR", "#777"

# Lista de activos para analizar
activos_radar = {
    "ORO": "GC=F", "BITCOIN": "BTC-USD", "PETRÓLEO": "CL=F", 
    "DXY": "DX-Y", "S&P 500": "ES=F", "NASDAQ": "NQ=F"
}

# ==============================================================================
# 5. DASHBOARD PRINCIPAL (RADAR)
# ==============================================================================
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🛡️ TERMINAL QUANTUM v36</h1>", unsafe_allow_html=True)

c1, c2, c3, c4, c5, c6 = st.columns(6)
cols = [c1, c2, c3, c4, c5, c6]
current_results = []

for i, (name, ticker) in enumerate(activos_radar.items()):
    val, pct, state, color = get_market_status(ticker)
    current_results.append({"Activo": name, "Precio": val, "Cambio %": pct, "Estado": state})
    with cols[i]:
        st.metric(name, f"${val}", f"{pct}%")
        st.markdown(f"<div class='status-card' style='background-color:{color}22; color:{color};'>{state}</div>", unsafe_allow_html=True)

# Guardar en el historial si es una sesión nueva
if st.button("💾 ARCHIVAR SESIÓN EN LIBRERÍA"):
    st.session_state.history.append({
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Datos": current_results
    })
    st.success("Sesión guardada en la librería.")

st.divider()

# ==============================================================================
# 6. CAMPO DE BATALLA Y NOTICIAS
# ==============================================================================
col_main, col_news = st.columns([2.5, 1])

with col_main:
    st.subheader("📊 ANÁLISIS TÉCNICO PROFESIONAL")
    components.html("""
        <div style="height:550px;"><div id="tv_chart"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({"autosize": true, "symbol": "OANDA:XAUUSD", "interval": "1", "theme": "dark", "style": "1", "locale": "es", "container_id": "tv_chart"});
        </script></div>
    """, height=550)

with col_news:
    st.subheader("📰 NOTICIAS DE IMPACTO")
    components.html("""
        <div class="tradingview-widget-container"><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-timeline.js" async>
        {"feedMode": "all_symbols", "colorTheme": "dark", "width": "100%", "height": "500", "locale": "es"}
        </script></div>
    """, height=500)

# ==============================================================================
# 7. LA LIBRERÍA DEL COMANDANTE (EL ARCHIVO)
# ==============================================================================
st.divider()
st.subheader("📚 LIBRERÍA DE SESIONES (GANADORES Y PERDEDORES)")

if not st.session_state.history:
    st.warning("La librería está esperando tu primera orden. Dale al botón 'ARCHIVAR SESIÓN' arriba.")
else:
    for session in reversed(st.session_state.history):
        with st.expander(f"📂 Reporte del {session['Fecha']}"):
            df_hist = pd.DataFrame(session['Datos'])
            # Clasificar los 3 mejores y 3 peores
            top_3 = df_hist.sort_values(by="Cambio %", ascending=False).head(3)
            bot_3 = df_hist.sort_values(by="Cambio %", ascending=True).head(3)
            
            col_t, col_b = st.columns(2)
            with col_t:
                st.markdown("### 🏆 TOP 3 GANADORES")
                st.table(top_3)
            with col_b:
                st.markdown("### 💀 TOP 3 PELEADORES")
                st.table(bot_3)

# ==============================================================================
# 8. SIDEBAR: ACADEMIA Y LEY
# ==============================================================================
with st.sidebar:
    st.title("💎 ACADEMIA MONTERO")
    st.divider()
    st.markdown("### 📜 LA LEY DE MONTERO")
    st.info("1. Protege los $100K\n2. Meli Confirma\n3. Disciplina de Hierro\n4. Paciencia")
    st.divider()
    st.markdown("### 📖 LIBROS MAESTROS")
    st.markdown("- [Padre Rico, Padre Pobre](https://archive.org/details/padre-rico-padre-pobre_202011)")
    st.markdown("- [El Hombre más Rico de Babilonia](https://archive.org/details/el-hombre-mas-rico-de-babilonia_202102)")
    st.markdown("- [Piense y Hágase Rico](https://archive.org/details/piense-y-hagase-rico-napoleon-hill)")
    st.divider()
    if st.button("🎙️ MELI: RESUMEN DE VOZ"):
        melli_vocalize("Comandante, he actualizado la librería. Revise los reportes históricos para ajustar su estrategia.")
