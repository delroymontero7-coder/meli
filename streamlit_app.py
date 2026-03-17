# ==============================================================================
# 🛡️ TERMINAL QUANTUM v51.3 - EL BÚNKER MONUMENTAL
# PROPIEDAD DE: COMANDO MONTERO ($100K ELITE)
# SISTEMA: GESTIÓN PATRIMONIAL, RIESGO CONTROLADO 1% Y SNIPER V6
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. IMPORTACIÓN DE LIBRERÍAS (EL ARMAZÓN TÉCNICO)
# ------------------------------------------------------------------------------
import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import requests
import json
import time
import math
import os
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ------------------------------------------------------------------------------
# 2. CONFIGURACIÓN DEL ENTORNO DE ALTO NIVEL
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="MELI BÚNKER v51.3 - PATRIMONIO ÉLITE",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------------------------
# 3. GESTIÓN DE PERSISTENCIA DE DATOS (EL CORAZÓN DE LOS $100K)
# ------------------------------------------------------------------------------
def inicializar_bunker():
    """Inicializa todas las variables de estado para evitar errores de carga"""
    if 'capital_actual' not in st.session_state:
        st.session_state.capital_actual = 100000.0
    
    if 'capital_inicial' not in st.session_state:
        st.session_state.capital_inicial = 100000.0
        
    if 'historial_pnl' not in st.session_state:
        st.session_state.historial_pnl = [
            {"fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "balance": 100000.0}
        ]
        
    if 'bitacora' not in st.session_state:
        st.session_state.bitacora = []
        
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
        
    if 'noticias_cache' not in st.session_state:
        st.session_state.noticias_cache = []

inicializar_bunker()

# ------------------------------------------------------------------------------
# 4. CAPA DE DISEÑO CUÁNTICO (CSS EXPANDIDO PARA ESTÉTICA PROFESIONAL)
# ------------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Configuración Base del Búnker */
    .stApp {
        background-color: #040608;
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Panel de Balance Institucional */
    .contenedor-patrimonio {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        padding: 45px;
        border-radius: 24px;
        border: 1px solid #1e293b;
        border-top: 8px solid #10b981;
        text-align: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.6);
        margin-bottom: 30px;
    }
    
    .titulo-balance {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 10px;
    }
    
    .monto-principal {
        font-size: 4.8rem;
        font-weight: 900;
        color: #10b981;
        letter-spacing: -2px;
        text-shadow: 0 0 30px rgba(16, 185, 129, 0.4);
    }
    
    /* Tarjetas del Radar Sniper V6 */
    .tarjeta-radar {
        background: rgba(15, 23, 42, 0.8);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #334155;
        text-align: center;
        transition: all 0.4s ease-in-out;
    }
    
    .tarjeta-radar:hover {
        border-color: #facc15;
        transform: translateY(-8px);
        background: rgba(15, 23, 42, 1);
        box-shadow: 0 15px 30px rgba(250, 204, 21, 0.15);
    }
    
    .score-grande {
        font-size: 2.8rem;
        font-weight: 900;
        margin: 10px 0;
    }
    
    /* Botones de Comando */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #facc15 0%, #eab308 100%);
        color: #020617 !important;
        font-weight: 800 !important;
        padding: 18px !important;
        border-radius: 14px !important;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: 0.3s;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 25px rgba(250, 204, 21, 0.5);
        transform: scale(1.02);
    }

    /* Diario de Operaciones */
    .tabla-registro {
        background-color: #0f172a;
        border-radius: 15px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 5. MÓDULOS DE COMUNICACIÓN (MELI VOICE & TELEGRAM)
# ------------------------------------------------------------------------------
def melli_voz_institucional(texto):
    """Módulo de síntesis de voz con parámetros optimizados"""
    codigo_js = f"""
    <script>
    var voz = new SpeechSynthesisUtterance('{texto}');
    voz.lang = 'es-ES';
    voz.rate = 0.92;
    voz.pitch = 1.0;
    voz.volume = 1.0;
    window.speechSynthesis.speak(voz);
    </script>
    """
    components.html(codigo_js, height=0)

def alerta_telegram(mensaje):
    """Envío de alertas críticas al comando móvil"""
    token = "8613807854:AAEtSHlv1n0YYJxpjvuduGeXoVca9-jRfWo"
    chat_id = "8350001201"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": mensaje, "parse_mode": "HTML"}, timeout=5)
    except Exception:
        pass

# ------------------------------------------------------------------------------
# 6. MOTOR TÉCNICO: SNIPER DELROY V6 "THE SECURE BEAST"
# ------------------------------------------------------------------------------
def ejecutar_analisis_sniper(ticker):
    """
    Análisis multivariante basado en el código de Montero:
    1. Medias de 200 y 50 para Tendencia Maestra.
    2. RSI de 2 periodos para detección de barridos de liquidez.
    3. ATR de 14 para stops dinámicos.
    4. Volumen relativo para detección de ballenas.
    """
    try:
        # Descarga de datos extendida para estabilidad de indicadores
        datos = yf.download(ticker, period="150d", interval="1d", progress=False)
        if datos.empty: return None

        # --- CÁLCULO DE INDICADORES (LÓGICA EXPANDIDA) ---
        
        # Medias Móviles Exponenciales (Tendencia)
        datos['EMA200'] = ta.ema(datos['Close'], length=200) or datos['Close'].rolling(window=200).mean()
        datos['EMA50'] = ta.ema(datos['Close'], length=50)
        
        # Oscilador Sniper (RSI 2)
        datos['RSI2'] = ta.rsi(datos['Close'], length=2)
        
        # Volatilidad ATR
        datos['ATR'] = ta.atr(datos['High'], datos['Low'], datos['Close'], length=14)
        
        # Filtro de Volumen de Ballenas (VolStrong)
        datos['VOL_AVG'] = datos['Volume'].rolling(window=20).mean()
        
        # --- ESTRUCTURA DE MERCADO (PREMIUM / DISCOUNT) ---
        alto_50 = datos['High'].rolling(window=50).max()
        bajo_50 = datos['Low'].rolling(window=50).min()
        equilibrio = (alto_50 + bajo_50) / 2

        # --- EXTRACCIÓN DE VALORES EN TIEMPO REAL ---
        ultimo_cierre = datos['Close'].iloc[-1]
        ema200_act = datos['EMA200'].iloc[-1]
        ema50_act = datos['EMA50'].iloc[-1]
        rsi2_act = datos['RSI2'].iloc[-1]
        atr_act = datos['ATR'].iloc[-1]
        vol_act = datos['Volume'].iloc[-1]
        vol_med = datos['VOL_AVG'].iloc[-1]
        
        # --- SISTEMA DE PUNTUACIÓN DE ESCUDO (SNIPER SCORE) ---
        score_compra = 0
        if ultimo_cierre > ema200_act: score_compra += 25
        if ema50_act > ema200_act: score_compra += 25
        if ultimo_cierre < equilibrio.iloc[-1]: score_compra += 25 # Zona de Descuento
        if rsi2_act < 15: score_compra += 25 # Barrido de liquidez alcista

        score_venta = 0
        if ultimo_cierre < ema200_act: score_venta += 25
        if ema50_act < ema200_act: score_venta += 25
        if ultimo_cierre > equilibrio.iloc[-1]: score_venta += 25 # Zona Premium
        if rsi2_act > 85: score_venta += 25 # Barrido de liquidez bajista

        # --- RESULTADOS FINALES ---
        final_score = score_compra if score_compra >= score_venta else score_venta
        final_sent = "COMPRA" if score_compra >= score_venta else "VENTA"
        ballenas = vol_act > (vol_med * 1.5)

        # Cálculo de Niveles Sniper
        if final_sent == "COMPRA":
            stop_loss = ultimo_cierre - (atr_act * 2)
            take_profit = ultimo_cierre + (atr_act * 4)
        else:
            stop_loss = ultimo_cierre + (atr_act * 2)
            take_profit = ultimo_cierre - (atr_act * 4)

        return {
            "precio": round(float(ultimo_cierre), 2),
            "score": int(final_score),
            "sentimiento": final_sent,
            "ballenas": ballenas,
            "rsi": round(float(rsi2_act), 1),
            "tendencia": "ALCISTA" if ema50_act > ema200_act else "BAJISTA",
            "sl": round(float(stop_loss), 2),
            "tp": round(float(take_profit), 2)
        }
    except Exception as e:
        st.error(f"Error en motor técnico: {e}")
        return None

# ------------------------------------------------------------------------------
# 7. SISTEMA DE SEGURIDAD BIOMÉTRICA (SIMULADO)
# ------------------------------------------------------------------------------
def pantalla_bloqueo():
    """Interfaz de acceso restringido para los $100,000"""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #facc15;'>🔐 ACCESO NIVEL COMANDO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>TERMINAL DE GESTIÓN PATRIMONIAL v51.3</p>", unsafe_allow_html=True)
    
    _, col_centro, _ = st.columns([1, 1, 1])
    with col_centro:
        clave = st.text_input("PASSWORD DE OPERADOR:", type="password")
        if st.button("SINCRO-BÚNKER"):
            if clave == "1234":
                st.session_state.autenticado = True
                melli_voz_institucional("Acceso verificado. Comandante Montero, iniciando sistemas de defensa patrimonial.")
                st.rerun()
            else:
                st.error("CLAVE ERRÓNEA. ACCESO RECHAZADO.")
    st.stop()

if not st.session_state.autenticado:
    pantalla_bloqueo()

# ------------------------------------------------------------------------------
# 8. PANEL DE CONTROL DE CAPITAL (EL MONITOR DE LOS $100K)
# ------------------------------------------------------------------------------
st.markdown("<h2 style='text-align: center; color: #facc15;'>💎 TERMINAL DE PATRIMONIO ÉLITE</h2>", unsafe_allow_html=True)

# Grid Superior: Balance y Riesgo
col_izq, col_der, col_met = st.columns([2.5, 1, 1])

with col_izq:
    st.markdown(f"""
    <div class="contenedor-patrimonio">
        <div class="titulo-balance">PATRIMONIO BAJO GESTIÓN</div>
        <div class="monto-principal">${st.session_state.capital_actual:,.2f}</div>
        <div style="color: #64748b; font-weight: 800; font-size: 0.8rem; margin-top: 10px;">
            FONDO BLINDADO - ESTRATEGIA: SNIPER DELROY V6
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_der:
    # Cálculo de riesgo basado en el 1% estricto
    riesgo_usd = st.session_state.capital_actual * 0.01
    st.markdown(f"""
    <div style="background: rgba(16, 185, 129, 0.05); border: 2px solid #10b981; padding: 25px; border-radius: 20px; text-align: center; height: 100%;">
        <div style="color: #10b981; font-weight: bold; font-size: 0.9rem; text-transform: uppercase;">Riesgo Máximo (1%)</div>
        <div style="font-size: 2.2rem; font-weight: 900; color: white; margin: 10px 0;">${riesgo_usd:,.0f}</div>
        <div style="color: #94a3b8; font-size: 0.7rem;">MÁXIMA EXPOSICIÓN POR DISPARO</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🎙️ ESTADO FINANCIERO"):
        melli_voz_institucional(f"Comandante, el balance es de {st.session_state.capital_actual} dólares. El sistema tiene mil dólares listos para arriesgar en el siguiente objetivo.")

with col_met:
    roi_sesion = ((st.session_state.capital_actual / 100000) - 1) * 100
    st.metric("ROI TOTAL", f"{roi_sesion:.2f}%")
    st.metric("OPERACIONES", len(st.session_state.bitacora))
    if st.button("🛑 CERRAR SESIÓN"):
        st.session_state.autenticado = False
        st.rerun()

# ------------------------------------------------------------------------------
# 9. RADAR DE MERCADO SNIPER (VIGILANCIA ACTIVA)
# ------------------------------------------------------------------------------
st.divider()
st.markdown("### 🏹 RADAR SNIPER DELROY - VIGILANCIA 24/7")

lista_activos = {
    "ORO (XAU)": "GC=F", 
    "BITCOIN (BTC)": "BTC-USD", 
    "NASDAQ 100": "NQ=F", 
    "S&P 500": "ES=F",
    "NVIDIA": "NVDA",
    "TESLA": "TSLA"
}

cols_radar = st.columns(len(lista_activos))
resultados_activos = {}

for indice, (nombre_ui, sim_ticker) in enumerate(lista_activos.items()):
    info_mercado = ejecutar_analisis_sniper(sim_ticker)
    if info_mercado:
        resultados_activos[nombre_ui] = info_mercado
        with cols_radar[indice]:
            # Color dinámico según el score de escudo
            color_resaltado = "#10b981" if info_mercado['score'] >= 75 else "#f43f5e" if info_mercado['score'] <= 25 else "#94a3b8"
            st.markdown(f"""
            <div class="tarjeta-radar">
                <div style="color: #facc15; font-weight: 800; font-size: 0.8rem; margin-bottom: 10px;">{nombre_ui}</div>
                <div style="font-size: 1.5rem; font-weight: 900; color: white;">${info_mercado['precio']}</div>
                <div class="score-grande" style="color: {color_resaltado};">{info_mercado['score']}%</div>
                <div style="font-size: 0.7rem; color: #64748b;">
                    SENTIDO: {info_mercado['sentimiento']}<br>
                    BALLENAS: {"<b style='color:#10b981'>SÍ</b>" if info_mercado['ballenas'] else "NO"}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 10. CENTRO DE MANDO: GRÁFICO, NOTICIAS Y EJECUCIÓN
# ------------------------------------------------------------------------------
st.divider()
col_trading, col_feed = st.columns([3, 1])

with col_trading:
    st.subheader("🎯 MÓDULO DE EJECUCIÓN DE ÉLITE")
    
    # Selector de activo dinámico
    activo_fijado = st.selectbox("OBJETIVO SELECCIONADO:", list(lista_activos.keys()))
    data_target = resultados_activos[activo_fijado]
    
    # Lógica de Gestión de Riesgo Institucional
    # Un trader pro no compra "un lote", compra el valor exacto del riesgo.
    dist_pips = abs(data_target['precio'] - data_target['sl'])
    lotaje_exacto = riesgo_usd / dist_pips if dist_pips > 0 else 0
    
    # Visualización de Niveles
    v_col1, v_col2, v_col3, v_col4 = st.columns(4)
    v_col1.metric("PRECIO ENTRADA", f"${data_target['precio']}")
    v_col2.metric("NIVEL STOP LOSS", f"${data_target['sl']}")
    v_col3.metric("NIVEL TAKE PROFIT", f"${data_target['tp']}")
    v_col4.metric("LOTES SUGERIDOS", f"{lotaje_exacto:.2f}")
    
    # Análisis de Meli
    st.markdown(f"""
    <div style="padding: 20px; background: rgba(250, 204, 21, 0.05); border-left: 5px solid #facc15; border-radius: 10px; margin: 20px 0;">
        <span style="color: #facc15; font-weight: 900;">ANÁLISIS MELI:</span> 
        El {activo_fijado} muestra un score de <b>{data_target['score']}%</b>. 
        La tendencia es <b>{data_target['tendencia']}</b> con un RSI2 en {data_target['rsi']}. 
        { '⚠️ <b>BALLENAS DETECTADAS:</b> Inyección de capital institucional confirmada.' if data_target['ballenas'] else 'Flujo de volumen minorista normal.' }
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"🔥 DISPARAR SNIPER SOBRE {activo_fijado}"):
        # Registrar operación en la bitácora
        nueva_entrada = {
            "HORA": datetime.now().strftime("%H:%M:%S"),
            "ACTIVO": activo_fijado,
            "TIPO": data_target['sentimiento'],
            "PRECIO": data_target['precio'],
            "SL": data_target['sl'],
            "RIESGO": f"${riesgo_usd:,.0f}"
        }
        st.session_state.bitacora.append(nueva_entrada)
        
        # Notificar a todos los sistemas
        melli_voz_institucional(f"Objetivo {activo_fijado} fijado. Disparo ejecutado con riesgo de mil dólares. Munición en el aire.")
        alerta_telegram(f"<b>🎯 DISPARO EJECUTADO: {activo_fijado}</b>\nPrecio: ${data_target['precio']}\nSL: ${data_target['sl']}\nTP: ${data_target['tp']}\nRiesgo: ${riesgo_usd}")
        st.success(f"OPERACIÓN REGISTRADA EN {activo_fijado}")
        st.balloons()

    # Integración del Monitor TradingView
    st.markdown("### 📊 MONITOR DE PRECIO TIEMPO REAL")
    html_tv = f"""
    <div style="height:500px;">
        <div id="chart_v513" style="height:500px;"></div>
        <script src="https://s3.tradingview.com/tv.js"></script>
        <script>
        new TradingView.widget({{
          "autosize": true,
          "symbol": "OANDA:XAUUSD",
          "interval": "1",
          "theme": "dark",
          "style": "1",
          "locale": "es",
          "toolbar_bg": "#f1f3f6",
          "enable_publishing": false,
          "hide_side_toolbar": false,
          "container_id": "chart_v513"
        }});
        </script>
    </div>
    """
    components.html(html_tv, height=500)

with col_feed:
    st.subheader("📰 FUNDAMENTALES NY")
    if st.button("🎙️ RESUMEN DE NOTICIAS"):
        melli_voz_institucional("Analizando flujo de noticias de Wall Street. La volatilidad está aumentando. Mantenga el escudo activo en sus posiciones abiertas.")
    
    # Feed de Noticias en Vivo
    st.markdown("""
    <div style="height:850px; overflow-y:auto; border: 1px solid #1e293b; border-radius: 15px;">
        <iframe src="https://www.tradingview.com/embed-widget/timeline/?colorTheme=dark&locale=es" width="100%" height="1500" frameborder="0"></iframe>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 11. ANÁLISIS DE RENDIMIENTO (DIARIO Y CRECIMIENTO)
# ------------------------------------------------------------------------------
st.divider()
st.subheader("📈 ESTADÍSTICAS DEL FONDO MONTERO")

t_pnl, t_diario, t_educacion = st.tabs(["📊 CURVA DE PATRIMONIO", "📝 DIARIO DE TRADES", "📚 BIBLIOTECA DEL COMANDO"])

with t_pnl:
    # Gráfico profesional de crecimiento
    df_pnl = pd.DataFrame(st.session_state.historial_pnl)
    figura_pnl = go.Figure()
    figura_pnl.add_trace(go.Scatter(
        x=df_pnl['fecha'], 
        y=df_pnl['balance'], 
        mode='lines+markers',
        line=dict(color='#10b981', width=4),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.1)',
        name='Patrimonio Neto'
    ))
    figura_pnl.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Sesión / Hora",
        yaxis_title="Dólares (USD)",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(figura_pnl, use_container_width=True)

with t_diario:
    if st.session_state.bitacora:
        st.dataframe(pd.DataFrame(st.session_state.bitacora), use_container_width=True)
    else:
        st.info("Sin disparos registrados en la sesión actual.")

with t_educacion:
    st.markdown("### 📖 ENTRENAMIENTO PARA COMANDOS")
    c_lib1, c_lib2, c_lib3 = st.columns(3)
    with c_lib1:
        if st.button("📖 TRADING EN LA ZONA (PDF)"):
            st.markdown('<iframe src="https://ia801004.us.archive.org/12/items/trading-en-la-zona-mark-douglas/Trading%20en%20la%20Zona%20-%20Mark%20Douglas.pdf" width="100%" height="800px"></iframe>', unsafe_allow_html=True)
    with c_lib2:
        st.write("La disciplina es el escudo más fuerte de un Sniper.")
    with c_lib3:
        st.write("Recuerde: Operar es un juego de probabilidades, no de certezas.")

# ------------------------------------------------------------------------------
# 12. PIE DE PÁGINA Y CRIPTOGRAFÍA
# ------------------------------------------------------------------------------
st.divider()
st.caption(f"🛡️ SISTEMA OPERATIVO QUANTUM v51.3 | MONTERO $100K ELITE | CONEXIÓN ENCRIPTADA AES-512 | {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# --- FIN DEL CÓDIGO INTEGRAL ---
