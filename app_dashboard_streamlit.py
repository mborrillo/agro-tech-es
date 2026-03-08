"""
AgroTech Extremadura — Dashboard Principal
Conectado a Supabase con datos reales.
Credenciales via st.secrets (nunca hardcodeadas).
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(
    page_title="AgroTech Extremadura",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');
:root {
    --green-900: #0d2b1a; --green-800: #14432a; --green-700: #1a5c38;
    --green-600: #1f7a48; --green-500: #27a05e; --green-400: #3dbd76;
    --green-300: #5fd494; --green-100: #d6f5e5;
    --earth-700: #5c3d1e; --earth-500: #8b5e34; --earth-300: #c49a6c;
    --amber-500: #f59e0b; --amber-100: #fef3c7;
    --red-500: #ef4444;   --red-100: #fee2e2;
    --blue-500: #3b82f6;  --blue-100: #dbeafe;
    --border: #d1ead9; --shadow: 0 4px 24px rgba(13,43,26,0.08);
    --shadow-lg: 0 8px 40px rgba(13,43,26,0.14); --radius: 16px; --radius-sm: 10px;
}
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }
.stApp { background: linear-gradient(135deg, #f0faf4 0%, #e8f5ee 50%, #f5f9f2 100%) fixed; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--green-900) 0%, var(--green-800) 60%, #0a2010 100%) !important;
    border-right: none !important; box-shadow: 4px 0 30px rgba(0,0,0,0.3) !important;
}
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div, section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] li, section[data-testid="stSidebar"] .stRadio,
section[data-testid="stSidebar"] .stMarkdown { color: #d6f5e5 !important; }
section[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: var(--radius-sm) !important; padding: 10px 16px !important;
    margin: 3px 0 !important; cursor: pointer !important; transition: all 0.2s ease !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(63,189,118,0.15) !important; border-color: var(--green-400) !important;
}
#MainMenu, footer, header { visibility: hidden; }
button[kind="header"] { display: flex !important; visibility: visible !important; opacity: 1 !important; }
[data-testid="collapsedControl"] { display: flex !important; visibility: visible !important; color: var(--green-500) !important; background: white !important; border-radius: 0 8px 8px 0 !important; box-shadow: 2px 0 8px rgba(13,43,26,0.15) !important; }
[data-testid="collapsedControl"]:hover { background: var(--green-100) !important; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1400px !important; }
.kpi-card { background: white; border-radius: var(--radius); padding: 22px 24px; box-shadow: var(--shadow); border: 1px solid var(--border); position: relative; overflow: hidden; transition: all 0.3s ease; }
.kpi-card:hover { box-shadow: var(--shadow-lg); transform: translateY(-3px); }
.kpi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; border-radius: var(--radius) var(--radius) 0 0; }
.kpi-green::before { background: linear-gradient(90deg, var(--green-500), var(--green-300)); }
.kpi-amber::before { background: linear-gradient(90deg, var(--amber-500), #fbbf24); }
.kpi-red::before   { background: linear-gradient(90deg, var(--red-500), #f87171); }
.kpi-blue::before  { background: linear-gradient(90deg, var(--blue-500), #60a5fa); }
.kpi-earth::before { background: linear-gradient(90deg, #8b5e34, #c49a6c); }
.kpi-icon  { font-size: 2rem; margin-bottom: 8px; display: block; }
.kpi-value { font-size: 2.2rem; font-weight: 800; color: #0d2b1a; line-height: 1; margin: 4px 0; }
.kpi-label { font-size: 0.78rem; font-weight: 600; color: #7aa98e; text-transform: uppercase; letter-spacing: 0.08em; }
.kpi-sub   { font-size: 0.78rem; color: #7aa98e; margin-top: 6px; }
.badge { display:inline-block; padding:3px 10px; border-radius:20px; font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; }
.badge-green { background:var(--green-100); color:var(--green-700); }
.badge-amber { background:var(--amber-100); color:#b45309; }
.badge-red   { background:var(--red-100);   color:#b91c1c; }
.badge-blue  { background:var(--blue-100);  color:#1d4ed8; }
.badge-earth { background:#fdf4e7; color:var(--earth-700); }
.badge-gray  { background:#f1f5f9; color:#475569; }
.section-header { display:flex; align-items:center; gap:12px; margin-bottom:20px; padding-bottom:14px; border-bottom:2px solid var(--border); }
.section-icon { width:40px; height:40px; background:linear-gradient(135deg,var(--green-500),var(--green-400)); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.1rem; box-shadow:0 4px 12px rgba(39,160,94,0.3); }
.section-title { font-size:1.25rem; font-weight:700; color:#0d2b1a; margin:0; }
.section-sub   { font-size:0.8rem; color:#7aa98e; margin:0; }
.alert-item { display:flex; align-items:flex-start; gap:14px; padding:14px 16px; border-radius:var(--radius-sm); margin-bottom:10px; border-left:4px solid; transition:all 0.2s; }
.alert-item:hover { transform:translateX(4px); }
.alert-critical { background:#fff5f5; border-color:var(--red-500); }
.alert-warning  { background:#fffbeb; border-color:var(--amber-500); }
.alert-info     { background:#eff6ff; border-color:var(--blue-500); }
.alert-ok       { background:#f0fdf4; border-color:var(--green-500); }
.alert-dot { width:10px; height:10px; border-radius:50%; margin-top:5px; flex-shrink:0; }
.dot-red   { background:var(--red-500);   animation: pulse-r 2s infinite; }
.dot-amber { background:var(--amber-500); }
.dot-blue  { background:var(--blue-500);  }
.dot-green { background:var(--green-500); }
@keyframes pulse-r { 0%,100%{box-shadow:0 0 0 0 rgba(239,68,68,0.4)} 50%{box-shadow:0 0 0 6px rgba(239,68,68,0)} }
.alert-title { font-weight:700; font-size:0.88rem; color:#0d2b1a; }
.alert-desc  { font-size:0.8rem; color:#4a7c5f; margin-top:2px; }
.alert-time  { font-size:0.72rem; color:#7aa98e; margin-top:4px; font-family:'DM Mono',monospace; }
.page-hero { background: linear-gradient(135deg, var(--green-900) 0%, var(--green-700) 100%); border-radius: var(--radius); padding: 28px 32px; margin-bottom: 28px; color: white; position: sticky; top: 0; z-index: 100; overflow: hidden; }
.page-hero::after { content:'🌿'; position:absolute; right:30px; top:50%; transform:translateY(-50%); font-size:5rem; opacity:0.15; }
.page-hero h1  { color:white !important; font-size:1.7rem; font-weight:800; margin:0 0 4px; }
.page-hero p   { color:rgba(255,255,255,0.7); margin:0; font-size:0.9rem; }
.page-hero .hero-badge { display:inline-block; background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.25); border-radius:20px; padding:4px 14px; font-size:0.75rem; font-weight:600; color:white; margin-bottom:10px; }
.mono { font-family:'DM Mono',monospace; }
.data-row { background:white; border-radius:12px; padding:14px 20px; margin-bottom:8px; border:1px solid var(--border); display:flex; align-items:center; gap:16px; box-shadow:0 2px 8px rgba(13,43,26,0.05); transition:all 0.2s; }
.data-row:hover { border-color:var(--green-400); box-shadow:var(--shadow); }
.stButton button { background:linear-gradient(135deg,var(--green-600),var(--green-500)) !important; color:white !important; border:none !important; border-radius:var(--radius-sm) !important; font-weight:600 !important; font-family:'Plus Jakarta Sans',sans-serif !important; box-shadow:0 4px 14px rgba(39,160,94,0.35) !important; transition:all 0.2s !important; }
.stButton button:hover { transform:translateY(-1px) !important; box-shadow:0 6px 20px rgba(39,160,94,0.45) !important; }
.login-wrap { max-width:440px; margin:60px auto; background:white; border-radius:24px; padding:48px 40px; box-shadow:var(--shadow-lg); border:1px solid var(--border); text-align:center; }
.block-container label, .block-container .stSelectbox label, .block-container .stTextInput label { color: #0d2b1a !important; font-weight: 600 !important; font-size: 0.82rem !important; }
.main label { color: #0d2b1a !important; }
.main .stSelectbox > label { color: #0d2b1a !important; }
.main .stTextInput > label { color: #0d2b1a !important; }
[data-testid="stForm"] label { color: #0d2b1a !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_supabase():
    try:
        from supabase import create_client
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"❌ Error conectando a Supabase: {e}")
        return None

@st.cache_data(ttl=300)
def load(tabla, order_col=None, desc=True, limit=200):
    sb = get_supabase()
    if not sb:
        return pd.DataFrame()
    try:
        q = sb.table(tabla).select("*")
        if order_col:
            q = q.order(order_col, desc=desc)
        q = q.limit(limit)
        r = q.execute()
        return pd.DataFrame(r.data) if r.data else pd.DataFrame()
    except Exception as e:
        st.warning(f"⚠️ {tabla}: {e}")
        return pd.DataFrame()

def section_header(icon, title, sub=""):
    st.markdown(f"""
    <div class="section-header">
        <div class="section-icon">{icon}</div>
        <div><p class="section-title">{title}</p><p class="section-sub">{sub}</p></div>
    </div>
    """, unsafe_allow_html=True)

def page_hero(badge, title, subtitle, ultima_act=None):
    fecha_str = ultima_act.strftime("%d/%m/%Y %H:%M") if ultima_act is not None else datetime.now().strftime("%d/%m/%Y")
    st.markdown(f"""
    <div class="page-hero">
        <span class="hero-badge">{badge}</span>
        <h1>{title}</h1>
        <p>{subtitle} &nbsp;·&nbsp; <span style="opacity:0.85;">🕐 Última actualización: {fecha_str}</span></p>
    </div>
    """, unsafe_allow_html=True)

def kpi_card(col, cls, icon, value, label, sub):
    with col:
        st.markdown(f"""
        <div class="kpi-card {cls}">
            <span class="kpi-icon">{icon}</span>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans", color="#0d2b1a"),
    margin=dict(l=0, r=0, t=30, b=0),
    xaxis=dict(showgrid=False, color="#7aa98e"),
    yaxis=dict(gridcolor="#e8f5ee", color="#7aa98e"),
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
        font=dict(size=12, color="#0d2b1a"),
        bgcolor="rgba(255,255,255,0.85)", bordercolor="#d1ead9", borderwidth=1,
    ),
)
COLORS = ["#27a05e", "#f59e0b", "#3b82f6", "#ef4444", "#8b5e34", "#a855f7"]

def render_login():
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("""
        <div class="login-wrap">
            <div style="font-size:3rem">🌿</div>
            <div style="font-size:1.6rem;font-weight:800;color:#0d2b1a;">AgroTech Extremadura</div>
            <div style="color:#7aa98e;font-size:0.9rem;margin:8px 0 32px;">Monitor del Campo Extremeño</div>
        </div>
        """, unsafe_allow_html=True)
        with st.form("login_form"):
            email    = st.text_input("Correo electrónico", placeholder="usuario@agrotech.es")
            password = st.text_input("Contraseña", type="password", placeholder="••••••••")
            if st.form_submit_button("Acceder al Dashboard", use_container_width=True):
                if email and password:
                    st.session_state.update({
                        "logged_in": True,
                        "user_email": email,
                        "user_name": email.split("@")[0].capitalize(),
                    })
                    st.rerun()
                else:
                    st.error("Introduce email y contraseña.")

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:20px 0 28px;">
            <div style="font-size:2.5rem;">🌿</div>
            <div style="font-size:1.1rem;font-weight:800;color:#d6f5e5;margin-top:6px;">AgroTech</div>
            <div style="font-size:0.72rem;color:#5fd494;letter-spacing:0.12em;text-transform:uppercase;">Monitor del Campo</div>
        </div>
        <hr style="border:none;border-top:1px solid rgba(255,255,255,0.1);margin-bottom:20px;">
        """, unsafe_allow_html=True)

        nav_options = [
            "🏠  Dashboard",
            "🗺️  Mapa de Operaciones",
            "📊  Monitor de Mercados",
            "🌐  Monitor de Productos",
            "⚡  Monitor de Energía",
            "🔔  Alertas",
            "⚙️  Configuración",
        ]
        default_idx = 0
        if "nav_target" in st.session_state:
            target = st.session_state.pop("nav_target")
            for i, opt in enumerate(nav_options):
                if target in opt:
                    default_idx = i
                    break

        nav = st.radio("nav", nav_options, index=default_idx, label_visibility="collapsed")
        st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.1);margin:20px 0;'>", unsafe_allow_html=True)

        user = st.session_state.get("user_name", "Usuario")
        st.markdown(f"""
        <div style="padding:12px 16px;background:rgba(255,255,255,0.07);border-radius:12px;border:1px solid rgba(255,255,255,0.1);">
            <div style="font-size:0.72rem;color:#5fd494;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">Sesión activa</div>
            <div style="font-weight:700;font-size:0.9rem;">👤 {user}</div>
            <div style="font-size:0.72rem;color:rgba(214,245,229,0.6);margin-top:2px;">{st.session_state.get('user_email','')}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if st.button("🔄 Restablecer Datos", use_container_width=True):
            st.cache_data.clear()
            # Limpiar explícitamente todos los filtros de todas las páginas
            filter_keys = [
                # Mapa de Operaciones
                "mapa_comarca", "mapa_tratamiento", "mapa_riego", "mapa_buscar",
                # Monitor de Mercados
                "merc_anio_mes", "merc_fecha", "merc_relacion", "merc_buscar",
                # Monitor de Productos
                "prod_anio_mes", "prod_fecha", "prod_categoria", "prod_tendencia", "prod_buscar",
                # Monitor de Energía
                "en_periodo", "en_tramo", "en_estado", "en_buscar",
            ]
            for k in filter_keys:
                if k in st.session_state:
                    del st.session_state[k]
            # Limpiar también cualquier otra key de estado (paginación, etc.)
            extra_keys = [k for k in st.session_state if k not in ("logged_in", "user_email", "user_name", "nav_target")]
            for k in extra_keys:
                del st.session_state[k]
            st.rerun()
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("Cerrar sesión", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()

    return nav.split("  ", 1)[-1]

def render_dashboard():
    page_hero("🌱 Vista general", "Dashboard Principal", "Estado actual del campo extremeño")
    df_mapa  = load("v_mapa_operaciones")
    df_salud = load("v_salud_sectores")

    c1, c2, c3, c4, c5 = st.columns(5)
    if not df_mapa.empty:
        temp  = df_mapa["temp_actual"].mean()     if "temp_actual"   in df_mapa else None
        hum   = df_mapa["humedad"].mean()          if "humedad"       in df_mapa else None
        kwh   = df_mapa["precio_kwh"].mean()       if "precio_kwh"    in df_mapa else None
        tramo = df_mapa["luz_estado"].mode()[0] if "luz_estado" in df_mapa else "—"
    else:
        temp = hum = kwh = None; tramo = "—"

    df_ac    = load("v_alertas_clima_extrema", order_col="fecha")
    n_alerta = 0
    if not df_ac.empty and "alerta_riesgo" in df_ac.columns:
        n_alerta = int(df_ac["alerta_riesgo"].dropna().apply(
            lambda x: str(x).strip().lower() not in ["", "none", "nan", "sin alerta", "normal", "sin alarma"]
        ).sum())

    kpi_card(c1, "kpi-green", "🌡️", f"{temp:.1f}°C" if temp is not None else "—", "Temperatura media", f"{len(df_mapa)} estaciones")
    kpi_card(c2, "kpi-blue",  "💧", f"{hum:.0f}%"   if hum  is not None else "—", "Humedad media", "Promedio campo")
    kpi_card(c3, "kpi-amber", "⚡", f"{kwh:.3f}€"   if kwh  is not None else "—", "Precio kWh", tramo)
    kpi_card(c4, "kpi-red" if n_alerta > 0 else "kpi-green", "⚠️", str(n_alerta), "Alertas clima", "Activas")
    if not df_salud.empty and "estado_mercado" in df_salud.columns:
        al_alza = int((df_salud["estado_mercado"].str.upper().str.strip() == "ÓPTIMO").sum())
        kpi_card(c5, "kpi-earth", "🌾", f"{al_alza}/{len(df_salud)}", "Sectores al alza", "Estado mercado")
    else:
        kpi_card(c5, "kpi-earth", "🌾", "—", "Sectores", "Sin datos")

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    section_header("🏷️", "Salud de Sectores", "Estado actual del mercado agrícola")
    if not df_salud.empty:
        num_cols = min(len(df_salud), 5)
        sector_cols = st.columns(num_cols)
        for i, (_, row) in enumerate(df_salud.iterrows()):
            estado = str(row.get("estado_mercado", "")).upper().strip()
            if estado == "ÓPTIMO":
                b_cls, dot, border_color, bg_color = "badge-green", "🟢", "#27a05e", "#f0fdf4"
            elif estado == "ALERTA":
                b_cls, dot, border_color, bg_color = "badge-red", "🔴", "#ef4444", "#fff5f5"
            else:  # ATENCIÓN u otro
                b_cls, dot, border_color, bg_color = "badge-amber", "🟡", "#f59e0b", "#fffbeb"
            var  = float(row.get("variacion_media_sector", 0) or 0)
            sign = "+" if var > 0 else ""
            with sector_cols[i % num_cols]:
                st.markdown(f"""
                <div style="background:{bg_color};border-radius:14px;padding:16px 18px;border:1px solid {border_color}33;box-shadow:var(--shadow);text-align:center;height:100%;">
                    <div style="font-size:1.6rem;margin-bottom:6px;">{dot}</div>
                    <div style="font-weight:700;font-size:0.9rem;color:#0d2b1a;margin-bottom:6px;">{row.get('sector','—')}</div>
                    <div style="margin-bottom:8px;"><span class="badge {b_cls}" style="font-size:0.9rem;padding:4px 14px;">{sign}{var:.1f}%</span></div>
                    <div style="font-size:0.72rem;color:#7aa98e;line-height:1.6;">{row.get('num_productos','—')} productos<br>↑ {row.get('productos_al_alza',0)} &nbsp;·&nbsp; ↓ {row.get('productos_a_la_baja',0)}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Sin datos de sectores")

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    section_header("💡", "Recomendaciones operativas", "Estaciones activas — últimas lecturas")
    if not df_mapa.empty:
        cols = st.columns(min(len(df_mapa), 3))
        for i, (_, row) in enumerate(df_mapa.head(3).iterrows()):
            with cols[i]:
                st.markdown(f"""
                <div style="background:white;border-radius:14px;padding:18px 20px;border:1px solid var(--border);box-shadow:var(--shadow);height:100%;">
                    <div style="font-weight:800;font-size:0.95rem;color:#0d2b1a;margin-bottom:12px;">📍 {row.get('estacion','—')}</div>
                    <div style="font-size:0.8rem;color:#4a7c5f;margin-bottom:8px;"><span style="font-weight:600;">💧 Riego:</span><br>{row.get('recomendacion_riego','Sin datos')}</div>
                    <div style="font-size:0.8rem;color:#4a7c5f;margin-bottom:8px;"><span style="font-weight:600;">🌿 Tratamiento:</span><br>{row.get('recomendacion_tratamiento','Sin datos')}</div>
                    <div style="font-size:0.78rem;color:#7aa98e;margin-top:10px;border-top:1px solid var(--border);padding-top:8px;">
                        ☀️ {row.get('luz_estado','—')} &nbsp;|&nbsp; 🌬️ {row.get('viento_vel','—')} km/h &nbsp;|&nbsp; 🌡️ {row.get('temp_actual','—')}°C
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        _, link_col, _ = st.columns([2, 1, 2])
        with link_col:
            if st.button("🗺️  Ver más en Mapa de Operaciones →", use_container_width=True, key="link_mapa"):
                st.session_state["nav_target"] = "Mapa de Operaciones"
                st.rerun()
    else:
        st.info("Sin datos de estaciones")

def render_mapa():
    page_hero("🗺️ Geolocalización", "Mapa de Operaciones", "Visualización geográfica de las estaciones")
    df = load("v_mapa_operaciones")
    if df.empty or "latitud" not in df.columns:
        st.warning("Sin datos de localización en v_mapa_operaciones")
        return

    f1, f2, f3, f4 = st.columns([1, 1, 1, 2])
    with f1:
        comarca_opts = ["Todas"]
        if "comarca" in df.columns:
            comarca_opts += sorted(df["comarca"].dropna().unique().tolist())
        filtro_comarca = st.multiselect("Comarca", [o for o in comarca_opts if o != "Todas"], placeholder="Todas las comarcas...", key="mapa_comarca")
    with f2:
        tratamiento_opts = ["Todos"]
        if "recomendacion_tratamiento" in df.columns:
            tratamiento_opts += sorted(df["recomendacion_tratamiento"].dropna().unique().tolist())
        filtro_trat = st.multiselect("Tratamiento", [o for o in tratamiento_opts if o != "Todos"], placeholder="Todos...", key="mapa_tratamiento")
    with f3:
        riego_opts = ["Todos"]
        if "recomendacion_riego" in df.columns:
            riego_opts += sorted(df["recomendacion_riego"].dropna().unique().tolist())
        filtro_riego = st.multiselect("Riego", [o for o in riego_opts if o != "Todos"], placeholder="Todos...", key="mapa_riego")
    with f4:
        buscar = st.text_input("🔍 Buscar estación", placeholder="Nombre de estación...", key="mapa_buscar")

    df_filtered = df.copy()
    if filtro_comarca and "comarca" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["comarca"].isin(filtro_comarca)]
    if filtro_trat and "recomendacion_tratamiento" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["recomendacion_tratamiento"].isin(filtro_trat)]
    if filtro_riego and "recomendacion_riego" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["recomendacion_riego"].isin(filtro_riego)]
    if buscar and "estacion" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["estacion"].str.contains(buscar, case=False, na=False)]

    st.markdown("""
    <div style="display:flex;align-items:center;gap:20px;margin:8px 0 16px;padding:10px 16px;background:white;border-radius:10px;border:1px solid var(--border);">
        <span style="display:flex;align-items:center;gap:6px;font-size:0.82rem;font-weight:600;color:#0d2b1a;"><span style="width:12px;height:12px;border-radius:50%;background:#27a05e;display:inline-block;"></span> Óptimo</span>
        <span style="display:flex;align-items:center;gap:6px;font-size:0.82rem;font-weight:600;color:#0d2b1a;"><span style="width:12px;height:12px;border-radius:50%;background:#f59e0b;display:inline-block;"></span> Precaución</span>
        <span style="display:flex;align-items:center;gap:6px;font-size:0.82rem;font-weight:600;color:#0d2b1a;"><span style="width:12px;height:12px;border-radius:50%;background:#ef4444;display:inline-block;"></span> Crítico</span>
    </div>
    """, unsafe_allow_html=True)

    def color_estado(row):
        trat = str(row.get("recomendacion_tratamiento", "") or "").lower()
        if any(x in trat for x in ["crític", "peligro", "no tratar", "prohibido", "suspender"]): return "#ef4444"
        if any(x in trat for x in ["precaución", "precaucion", "esperar", "vigilar", "atención", "atencion", "llano", "discrecional"]): return "#f59e0b"
        return "#27a05e"

    if not df_filtered.empty:
        df_filtered = df_filtered.copy()
        df_filtered["_color"] = df_filtered.apply(color_estado, axis=1)

    def calc_zoom_center(dff, df_base):
        if dff.empty:
            return (df_base["latitud"].mean() if not df_base.empty else 38.9), (df_base["longitud"].mean() if not df_base.empty else -6.3), 7
        lat_c, lon_c = dff["latitud"].mean(), dff["longitud"].mean()
        if len(dff) == 1: return lat_c, lon_c, 11
        max_range = max(dff["latitud"].max()-dff["latitud"].min(), dff["longitud"].max()-dff["longitud"].min())
        zoom = 11 if max_range < 0.1 else 10 if max_range < 0.3 else 9 if max_range < 0.8 else 8 if max_range < 1.5 else 7 if max_range < 3.0 else 6
        return lat_c, lon_c, zoom

    center_lat, center_lon, zoom_level = calc_zoom_center(df_filtered, df)

    try:
        fig = go.Figure()
        for hex_color, label in {"#27a05e": "Óptimo", "#f59e0b": "Precaución", "#ef4444": "Crítico"}.items():
            sub = df_filtered[df_filtered["_color"] == hex_color] if not df_filtered.empty else pd.DataFrame()
            if sub.empty: continue
            hover_texts = sub.apply(lambda r:
                f"<b>{r.get('estacion','—')}</b><br>"
                f"🌬️ Viento: {r.get('viento_vel','—')} km/h<br>"
                f"🌧️ Precipitación: {r.get('precipitacion','—')} mm<br>"
                f"🌡️ Temp. actual: {r.get('temp_actual','—')} °C<br>"
                f"💧 Humedad: {r.get('humedad','—')}%<br>"
                f"<b>Tratamiento:</b> {r.get('recomendacion_tratamiento','—')}<br>"
                f"<b>Riego:</b> {r.get('recomendacion_riego','—')}<br>"
                f"Estado luz: {r.get('luz_estado','—')}", axis=1).tolist()
            fig.add_trace(go.Scattermapbox(
                lat=sub["latitud"].tolist(), lon=sub["longitud"].tolist(),
                mode="markers", marker=go.scattermapbox.Marker(size=16, color=hex_color, opacity=1.0),
                text=hover_texts, hoverinfo="text", name=label,
            ))
        fig.update_layout(
            mapbox=dict(style="open-street-map", center=dict(lat=center_lat, lon=center_lon), zoom=zoom_level),
            height=540, margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(orientation="h", yanchor="top", y=0.01, xanchor="left", x=0.01,
                        bgcolor="rgba(255,255,255,0.92)", font=dict(size=13, color="#0d2b1a"),
                        bordercolor="#d1ead9", borderwidth=1),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    except Exception as e:
        st.warning(f"No se pudo cargar el mapa: {e}")
        if not df_filtered.empty and "latitud" in df_filtered.columns:
            st.map(df_filtered.rename(columns={"latitud": "lat", "longitud": "lon"})[["lat","lon"]], zoom=7)

    if not df_filtered.empty:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        cols_show = [c for c in ["estacion", "comarca", "temp_actual", "humedad", "viento_vel", "precipitacion",
                                  "recomendacion_tratamiento", "recomendacion_riego", "luz_estado"] if c in df_filtered.columns]
        df_tabla_mapa = df_filtered[cols_show].sort_values("estacion").reset_index(drop=True)

        hdr_mapa = st.columns([0.05, 0.78, 0.17])
        with hdr_mapa[0]:
            st.markdown('<div style="width:40px;height:40px;background:linear-gradient(135deg,#27a05e,#3dbd76);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;box-shadow:0 4px 12px rgba(39,160,94,0.3);margin-top:2px;">📋</div>', unsafe_allow_html=True)
        with hdr_mapa[1]:
            st.markdown(f'<div style="padding-top:4px;"><p style="font-size:1.25rem;font-weight:700;color:#0d2b1a;margin:0;">Estaciones filtradas</p><p style="font-size:0.8rem;color:#7aa98e;margin:0;">{len(df_tabla_mapa)} estaciones seleccionadas</p></div>', unsafe_allow_html=True)
        with hdr_mapa[2]:
            import io
            output_mapa = io.BytesIO()
            col_labels_mapa = {"estacion": "Estación", "comarca": "Comarca", "temp_actual": "Temp. Actual (°C)",
                               "humedad": "Humedad (%)", "viento_vel": "Viento (km/h)", "precipitacion": "Precipitación (mm)",
                               "recomendacion_tratamiento": "Rec. Tratamiento", "recomendacion_riego": "Rec. Riego", "luz_estado": "Estado Luz"}
            df_export_mapa = df_tabla_mapa.rename(columns=col_labels_mapa)
            with pd.ExcelWriter(output_mapa, engine="openpyxl") as writer:
                df_export_mapa.to_excel(writer, index=False, sheet_name="Estaciones")
            st.download_button(
                label="📥 Excel",
                data=output_mapa.getvalue(),
                file_name=f"estaciones_filtradas_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="excel_mapa"
            )

        st.markdown("<div style='border-bottom:2px solid #d1ead9;margin-bottom:12px;'></div>", unsafe_allow_html=True)

        col_labels_h = {"estacion": "Estación", "comarca": "Comarca", "temp_actual": "Temp (°C)",
                        "humedad": "Humedad", "viento_vel": "Viento", "precipitacion": "Lluvia",
                        "recomendacion_tratamiento": "Tratamiento", "recomendacion_riego": "Riego", "luz_estado": "Luz"}
        col_widths_mapa = "1.5fr 1.2fr " + " ".join(["1fr"] * (len(cols_show) - 2))
        header_mapa_html = "".join([f'<span style="font-size:0.75rem;font-weight:700;color:#0d2b1a;text-transform:uppercase;letter-spacing:0.06em;">{col_labels_h.get(c, c)}</span>' for c in cols_show])
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:{col_widths_mapa};gap:8px;padding:10px 20px;background:#f0faf4;border-radius:10px 10px 0 0;border:1px solid var(--border);border-bottom:2px solid var(--border);margin-bottom:2px;">
            {header_mapa_html}
        </div>
        """, unsafe_allow_html=True)

        for _, row in df_tabla_mapa.iterrows():
            luz = str(row.get("luz_estado", "") or "").upper()
            trat = str(row.get("recomendacion_tratamiento", "") or "").upper()
            luz_bg  = "#fee2e2" if luz == "CARA" else "#dcfce7" if luz == "BARATA" else "#fef3c7"
            luz_col = "#b91c1c" if luz == "CARA" else "#15803d" if luz == "BARATA" else "#b45309"
            trat_bg  = "#dcfce7" if "OPTIMO" in trat else "#fee2e2" if "NO TRATAR" in trat else "#fef3c7"
            trat_col = "#15803d" if "OPTIMO" in trat else "#b91c1c" if "NO TRATAR" in trat else "#b45309"
            riego = str(row.get("recomendacion_riego", "") or "")
            riego_col = "#b91c1c" if "SUSPENDER" in riego.upper() or "POSPONER" in riego.upper() else "#15803d" if "RECOMENDADO" in riego.upper() else "#475569"

            cells_mapa = []
            for c in cols_show:
                if c == "estacion":
                    cells_mapa.append(f'<span style="font-weight:600;font-size:0.88rem;color:#0d2b1a;">{row.get("estacion","—")}</span>')
                elif c == "comarca":
                    cells_mapa.append(f'<span style="font-size:0.82rem;color:#475569;font-weight:500;">{row.get("comarca","—")}</span>')
                elif c in ["temp_actual", "humedad", "viento_vel", "precipitacion"]:
                    val = row.get(c, "—")
                    val_str = f"{float(val):.1f}" if val not in [None, "", "—"] else "—"
                    cells_mapa.append(f'<span style="font-family:DM Mono,monospace;font-size:0.85rem;color:#1a5c38;">{val_str}</span>')
                elif c == "recomendacion_tratamiento":
                    cells_mapa.append(f'<span style="font-size:0.78rem;font-weight:700;background:{trat_bg};color:{trat_col};padding:3px 8px;border-radius:20px;">{trat}</span>')
                elif c == "recomendacion_riego":
                    cells_mapa.append(f'<span style="font-size:0.78rem;font-weight:600;color:{riego_col};">{riego}</span>')
                elif c == "luz_estado":
                    cells_mapa.append(f'<span style="font-size:0.78rem;font-weight:700;background:{luz_bg};color:{luz_col};padding:3px 8px;border-radius:20px;">{luz}</span>')
            cells_mapa_html = "".join([f"<span>{cell}</span>" for cell in cells_mapa])
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:{col_widths_mapa};gap:8px;align-items:center;padding:12px 20px;background:white;border:1px solid var(--border);border-top:none;transition:background 0.15s;">
                {cells_mapa_html}
            </div>
            """, unsafe_allow_html=True)
        st.caption(f"{len(df_tabla_mapa)} estaciones mostradas")

def render_mercados():
    page_hero("📊 Análisis de mercado", "Monitor de Mercados", "Comparativa de precios locales vs internacionales")

    df_p = load("precios_agricolas",      order_col="fecha", limit=300)
    df_c = load("v_comparativa_mercados", order_col="fecha", limit=100)

    # ── Filtros ──
    if not df_c.empty and "fecha" in df_c.columns:
        df_c["fecha"] = pd.to_datetime(df_c["fecha"])

    f1, f2, f3, f4 = st.columns([1, 1, 1, 1.5])

    with f1:
        # Año-Mes — multiselect formato YYYY-MM, orden descendente
        anio_mes_opts = []
        if not df_c.empty and "fecha" in df_c.columns:
            anio_mes_opts = sorted(
                df_c["fecha"].dropna().apply(lambda d: d.strftime("%Y-%m")).unique().tolist(),
                reverse=True
            )
        filtro_periodo = st.multiselect("Año-Mes", anio_mes_opts, placeholder="Todos los periodos...", key="merc_anio_mes")

    with f2:
        # Fecha — lista todos los días con datos, orden cronológico descendente
        fecha_opts = ["Todas"]
        if not df_c.empty and "fecha" in df_c.columns:
            fechas_unicas = sorted(df_c["fecha"].dropna().dt.normalize().unique(), reverse=True)
            fecha_opts += [pd.Timestamp(f).strftime("%d/%m/%Y") for f in fechas_unicas]
        filtro_fecha = st.multiselect("Fecha", [o for o in fecha_opts if o != "Todas"], placeholder="Todas las fechas...", key="merc_fecha")

    with f3:
        # Mercado Referencia
        relacion_opts = ["Todos"]
        if not df_c.empty and "relacion" in df_c.columns:
            relacion_opts += sorted(df_c["relacion"].dropna().unique().tolist())
        filtro_relacion = st.multiselect("Mercado Referencia", [o for o in relacion_opts if o != "Todos"], placeholder="Todos los mercados...", key="merc_relacion")

    with f4:
        buscar_prod = st.text_input("🔍 Buscar mercado", placeholder="Nombre del mercado o producto...", key="merc_buscar")

    n_emparejados = al_alza_merc = a_la_baja_merc = 0
    ultimo = None
    if not df_p.empty and "fecha" in df_p.columns:
        df_p["fecha"] = pd.to_datetime(df_p["fecha"])
        ultimo = df_p["fecha"].max()
    if not df_c.empty:
        df_ult_c_kpi = df_c.sort_values("fecha").groupby("producto").last().reset_index()
        n_emparejados = len(df_ult_c_kpi)
        if "zona_arbitraje" in df_ult_c_kpi.columns:
            zonas_up = {"FAVORABLE", "ACOMPAÑANDO"}
            zonas_dn = {"DESFAVORABLE", "DIVERGIENDO"}
            al_alza_merc   = int(df_ult_c_kpi["zona_arbitraje"].str.upper().isin(zonas_up).sum())
            a_la_baja_merc = int(df_ult_c_kpi["zona_arbitraje"].str.upper().isin(zonas_dn).sum())
        elif "diferencial_arbitraje" in df_ult_c_kpi.columns:
            al_alza_merc   = int((df_ult_c_kpi["diferencial_arbitraje"].fillna(0) > 0).sum())
            a_la_baja_merc = int((df_ult_c_kpi["diferencial_arbitraje"].fillna(0) < 0).sum())

    c1, c2, c3, c4 = st.columns(4)
    kpi_card(c1, "kpi-green", "📅",
             ultimo.strftime("%d/%m/%y") if ultimo is not None else "—", "Última cotización",
             f"{len(df_p[df_p['fecha'] == ultimo]) if ultimo is not None and not df_p.empty else 0} productos")
    kpi_card(c2, "kpi-earth", "🔗", str(n_emparejados), "Mercados Emparejados", "Local vs Internacional")
    kpi_card(c3, "kpi-green", "📈", str(al_alza_merc),  "Al alza",   "Diferencial positivo")
    kpi_card(c4, "kpi-red",   "📉", str(a_la_baja_merc), "A la baja", "Diferencial negativo")
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Dataset filtrado (gráfico + tabla) ──
    df_vis = pd.DataFrame()
    if not df_c.empty:
        df_filt = df_c.copy()
        # Filtro Año-Mes: si hay selección, quedarse solo con esos periodos
        if filtro_periodo:
            mask = df_filt["fecha"].apply(lambda d: d.strftime("%Y-%m")).isin(filtro_periodo)
            df_filt = df_filt[mask]
        # Filtro Fecha exacta
        if filtro_fecha:
            df_filt = df_filt[df_filt["fecha"].apply(lambda d: d.strftime("%d/%m/%Y")).isin(filtro_fecha)]
        # Tomar último registro por producto dentro del periodo filtrado
        if not df_filt.empty:
            df_vis = df_filt.sort_values("fecha").groupby("producto").last().reset_index()
        else:
            df_vis = df_c.sort_values("fecha").groupby("producto").last().reset_index()
        # Filtro Mercado Referencia
        if filtro_relacion and "relacion" in df_vis.columns:
            df_vis = df_vis[df_vis["relacion"].isin(filtro_relacion)]
        # Filtro texto
        if buscar_prod:
            df_vis = df_vis[df_vis["producto"].str.contains(buscar_prod, case=False, na=False)]

    # ── Gráfico diferencial de arbitraje: una barra vertical por producto ──
    section_header("📊", "Diferencial de Arbitraje (€/kg)", "Verde: precio local superior al internacional · Rojo: precio local inferior al internacional")

    # Split DIRECTO / PROXY según tipo_referencia
    if not df_vis.empty and "tipo_referencia" in df_vis.columns:
        df_directo = df_vis[df_vis["tipo_referencia"].str.upper() == "DIRECTO"].copy()
        df_proxy   = df_vis[df_vis["tipo_referencia"].str.upper() == "PROXY"].copy()
    elif not df_vis.empty:
        df_directo = df_vis.copy()
        df_proxy   = pd.DataFrame()
    else:
        df_directo = df_proxy = pd.DataFrame()

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        fig, (ax_d, ax_p) = plt.subplots(1, 2, figsize=(13, 4.0))
        fig.patch.set_facecolor("#f0faf4")
        fig.subplots_adjust(wspace=0.40)

        def _render_bars_merc(ax, df_g, col_val, col_zona, ylabel, fmt_str, empty_msg):
            """Renderiza un gráfico de barras de diferencial con el estilo estándar del dashboard."""
            if df_g.empty or col_val not in df_g.columns:
                ax.set_facecolor("#f0faf4")
                ax.text(0.5, 0.5, empty_msg, ha="center", va="center",
                        fontsize=9, color="#7aa98e", transform=ax.transAxes,
                        multialignment="center")
                ax.set_xticks([]); ax.set_yticks([])
                for sp in ax.spines.values(): sp.set_visible(False)
                return
            df_g = df_g.copy()
            df_g[col_val] = pd.to_numeric(df_g[col_val], errors="coerce").fillna(0)
            prods  = df_g["producto"].tolist()
            vals   = df_g[col_val].tolist()
            zonas  = df_g[col_zona].tolist() if col_zona in df_g.columns else [None]*len(vals)
            cols_b = []
            for z in zonas:
                zu = str(z).upper()
                if zu in ("FAVORABLE", "ACOMPAÑANDO"):      cols_b.append("#27a05e")
                elif zu in ("DESFAVORABLE", "DIVERGIENDO"): cols_b.append("#ef4444")
                else:                                        cols_b.append("#f59e0b")
            n = len(prods)
            bars = ax.bar(range(n), vals, color=cols_b, alpha=0.88, width=0.55, zorder=3)
            ax.axhline(0, color="#0d2b1a", linewidth=1.0, alpha=0.3, zorder=2)
            for bar, val in zip(bars, vals):
                va     = "bottom" if val >= 0 else "top"
                offset = max(abs(val) * 0.03, 0.001) * (1 if val >= 0 else -1)
                ax.text(bar.get_x() + bar.get_width() / 2, val + offset,
                        fmt_str.format(val), ha="center", va=va,
                        fontsize=7.5, fontweight="600", color="#0d2b1a")
            ax.set_xticks(range(n))
            ax.set_xticklabels(prods, rotation=25, ha="right", fontsize=8.5, color="#0d2b1a")
            ax.set_ylabel(ylabel, fontsize=9, color="#0d2b1a")
            ax.tick_params(axis="y", colors="#0d2b1a", labelsize=8)
            ax.yaxis.grid(True, color="#d1ead9", linewidth=0.7, zorder=0)
            ax.set_axisbelow(True)
            ax.set_facecolor("#f0faf4")
            for sp in ["top", "right"]:   ax.spines[sp].set_visible(False)
            for sp in ["left", "bottom"]: ax.spines[sp].set_color("#d1ead9")

        # ── Izquierdo: DIRECTO — diferencial €/kg vs Chicago ──
        ax_d.set_title("Mercado Directo  (€/kg vs Chicago)", fontsize=9,
                       fontweight="700", color="#0d2b1a", pad=8, loc="left")
        _render_bars_merc(ax_d, df_directo, "diferencial_arbitraje", "zona_arbitraje",
                          "€/kg", "{:+.3f}", "Sin productos directos\nen la selección actual")
        if not df_directo.empty:
            ax_d.legend(handles=[
                mpatches.Patch(color="#27a05e", alpha=0.88, label="Favorable  (>+5%)"),
                mpatches.Patch(color="#f59e0b", alpha=0.88, label="Equilibrado (±2–5%)"),
                mpatches.Patch(color="#ef4444", alpha=0.88, label="Desfavorable (<−2%)"),
            ], fontsize=7.5, framealpha=0.85, edgecolor="#d1ead9", loc="upper right")

        # ── Derecho: PROXY — variación % local vs referencia global ──
        ax_p.set_title("Mercado Proxy  (var. % local vs referencia global)", fontsize=9,
                       fontweight="700", color="#0d2b1a", pad=8, loc="left")
        if not df_proxy.empty:
            df_pp = df_proxy.copy()
            df_pp["var_loc_plot"] = pd.to_numeric(df_pp.get("variacion_local"), errors="coerce").fillna(0)
        else:
            df_pp = pd.DataFrame()
        _render_bars_merc(ax_p, df_pp, "var_loc_plot", "zona_arbitraje",
                          "Var. %", "{:+.1f}%", "Sin productos proxy\nen la selección actual")
        if not df_pp.empty:
            ax_p.legend(handles=[
                mpatches.Patch(color="#27a05e", alpha=0.88, label="Acompañando"),
                mpatches.Patch(color="#f59e0b", alpha=0.88, label="Neutro"),
                mpatches.Patch(color="#ef4444", alpha=0.88, label="Divergiendo"),
            ], fontsize=7.5, framealpha=0.85, edgecolor="#d1ead9", loc="upper right")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    except Exception as e_chart:
        st.warning(f"⚠️ Error al renderizar gráficos: {e_chart}")

    if df_vis.empty:
        st.info("No hay datos que coincidan con los filtros aplicados.")



    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    fecha_str_header = ultimo.strftime('%Y-%m-%d') if ultimo is not None else '—'

    hdr_precios = st.columns([0.05, 0.78, 0.17])
    with hdr_precios[0]:
        st.markdown('<div style="width:40px;height:40px;background:linear-gradient(135deg,#27a05e,#3dbd76);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;box-shadow:0 4px 12px rgba(39,160,94,0.3);margin-top:2px;">🗓️</div>', unsafe_allow_html=True)
    with hdr_precios[1]:
        st.markdown(f'<div style="padding-top:4px;"><p style="font-size:1.25rem;font-weight:700;color:#0d2b1a;margin:0;">Precios del Día</p><p style="font-size:0.8rem;color:#7aa98e;margin:0;">Última actualización: {fecha_str_header}</p></div>', unsafe_allow_html=True)
    with hdr_precios[2]:
        if not df_vis.empty:
            import io
            output_precios = io.BytesIO()
            cols_export_precios = ["fecha", "sector", "producto", "tipo_referencia", "activo_referencia", "precio_local_kg", "precio_internacional_kg", "diferencial_arbitraje", "diferencial_pct", "variacion_local", "variacion_internacional", "zona_arbitraje", "recomendacion_arbitraje"]
            cols_export_precios = [c for c in cols_export_precios if c in df_vis.columns]
            df_export_precios = df_vis[cols_export_precios].sort_values("fecha", ascending=False).reset_index(drop=True) if "fecha" in df_vis.columns else df_vis[cols_export_precios].reset_index(drop=True)
            with pd.ExcelWriter(output_precios, engine="openpyxl") as writer:
                df_export_precios.to_excel(writer, index=False, sheet_name="Precios del Día")
            st.download_button(
                label="📥 Excel",
                data=output_precios.getvalue(),
                file_name=f"precios_dia_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="excel_precios_dia"
            )

    st.markdown("<div style='border-bottom:2px solid #d1ead9;margin-bottom:12px;'></div>", unsafe_allow_html=True)

    if not df_vis.empty:
        st.markdown("""
        <div style="display:grid;grid-template-columns:1.2fr 2fr 1.5fr 1.5fr 1.5fr 1fr;gap:8px;
                    padding:10px 20px;background:#f0faf4;border-radius:10px 10px 0 0;
                    border:1px solid var(--border);border-bottom:2px solid var(--border);margin-bottom:2px;">
            <span style="font-size:0.75rem;font-weight:700;color:#0d2b1a;text-transform:uppercase;letter-spacing:0.06em;">Fecha</span>
            <span style="font-size:0.75rem;font-weight:700;color:#0d2b1a;text-transform:uppercase;letter-spacing:0.06em;">Producto</span>
            <span style="font-size:0.75rem;font-weight:700;color:#0d2b1a;text-transform:uppercase;letter-spacing:0.06em;">Local (€/kg)</span>
            <span style="font-size:0.75rem;font-weight:700;color:#0d2b1a;text-transform:uppercase;letter-spacing:0.06em;">Internacional (€/kg)</span>
            <span style="font-size:0.75rem;font-weight:700;color:#0d2b1a;text-transform:uppercase;letter-spacing:0.06em;">Diferencial</span>
            <span style="font-size:0.75rem;font-weight:700;color:#0d2b1a;text-transform:uppercase;letter-spacing:0.06em;">Zona</span>
        </div>
        """, unsafe_allow_html=True)

        df_vis_sorted = df_vis.sort_values("fecha", ascending=False).reset_index(drop=True) if "fecha" in df_vis.columns else df_vis
        for _, row in df_vis_sorted.iterrows():
            try:
                fecha_row_str = pd.to_datetime(row.get("fecha", "")).strftime("%d/%m/%Y")
            except Exception:
                fecha_row_str = str(row.get("fecha", "—"))
            dif   = float(row.get("diferencial_arbitraje", 0) or 0)
            local = float(row.get("precio_local_kg", 0) or 0)
            intl  = float(row.get("precio_internacional_kg", 0) or 0)
            zona    = str(row.get("zona_arbitraje", "") or "").upper()
            tipo_ref= str(row.get("tipo_referencia", "") or "").upper()
            rec     = str(row.get("recomendacion_arbitraje", "") or "")
            dif_pct = float(row.get("diferencial_pct", 0) or 0) if row.get("diferencial_pct") is not None else None
            sign    = "+" if dif > 0 else ""

            # Color y flecha según zona
            if zona in ("FAVORABLE", "ACOMPAÑANDO"):
                b_bg  = "#dcfce7"; b_col = "#15803d"
                tend_svg = """<svg width="22" height="16" viewBox="0 0 22 16"><polyline points="2,13 8,7 13,10 20,3" fill="none" stroke="#27a05e" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="15,3 20,3 20,8" fill="none" stroke="#27a05e" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>"""
            elif zona in ("DESFAVORABLE", "DIVERGIENDO"):
                b_bg  = "#fee2e2"; b_col = "#b91c1c"
                tend_svg = """<svg width="22" height="16" viewBox="0 0 22 16"><polyline points="2,3 8,9 13,6 20,13" fill="none" stroke="#ef4444" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="15,13 20,13 20,8" fill="none" stroke="#ef4444" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>"""
            else:
                b_bg  = "#fef3c7"; b_col = "#b45309"
                tend_svg = """<svg width="22" height="16" viewBox="0 0 22 16"><polyline points="2,8 20,8" fill="none" stroke="#f59e0b" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>"""
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:1.2fr 2fr 1.5fr 1.5fr 1.5fr 1fr;gap:8px;
                        align-items:center;padding:14px 20px;background:white;
                        border:1px solid var(--border);border-top:none;margin-bottom:0;">
                <span style="font-family:'DM Mono',monospace;font-size:0.8rem;color:#7aa98e;">{fecha_row_str}</span>
                <span style="font-weight:600;font-size:0.9rem;color:#0d2b1a;">{row.get('producto','—')}</span>
                <span style="font-family:'DM Mono',monospace;font-size:0.88rem;color:#1a5c38;">{local:.2f} €/kg</span>
                <span style="font-family:'DM Mono',monospace;font-size:0.88rem;color:#475569;">
                    {f"{intl:.2f} €/kg" if tipo_ref == "DIRECTO" and intl else "— (proxy)"}
                </span>
                <span style="display:inline-flex;align-items:center;gap:6px;flex-wrap:wrap;">
                    <span style="background:{b_bg};color:{b_col};font-weight:700;font-size:0.82rem;padding:4px 12px;border-radius:20px;font-family:'DM Mono',monospace;">
                        {f"{sign}{dif:.2f} €/kg" if tipo_ref == "DIRECTO" and intl else zona.title()}
                    </span>
                    {f'<span style="font-size:0.72rem;color:{b_col};font-weight:600;">{sign}{dif_pct:.1f}%</span>' if tipo_ref == "DIRECTO" and dif_pct is not None else ""}
                </span>
                <span title="{rec}">{tend_svg}</span>
            </div>
            """, unsafe_allow_html=True)

    elif not df_p.empty:
        df_tab = df_p.copy()
        if buscar_prod:
            df_tab = df_tab[df_tab["producto"].str.contains(buscar_prod, case=False, na=False)]
        if filtro_sector != "Todos" and "sector" in df_tab.columns:
            df_tab = df_tab[df_tab["sector"] == filtro_sector]
        cols_show = [c for c in ["fecha","sector","producto","precio_min","precio_max","unidad","variacion_p"] if c in df_tab.columns]
        st.dataframe(df_tab[cols_show].sort_values("fecha", ascending=False).reset_index(drop=True), use_container_width=True, height=300)
    else:
        st.info("Sin datos de mercados disponibles")

def render_monitor_productos():
    page_hero("🌐 Mercados Internacionales", "Monitor de Productos", "Seguimiento de precios internacionales por categoría")
    df = load("v_monitor_productos", order_col="fecha", limit=500)

    # Preparar fechas
    if not df.empty and "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(df["fecha"])

    f1, f2, f3, f4, f5 = st.columns([1, 1, 1, 1, 1.5])
    with f1:
        # Año-Mes — multiselect formato YYYY-MM, orden descendente
        anio_mes_opts = []
        if not df.empty and "fecha" in df.columns:
            anio_mes_opts = sorted(
                df["fecha"].dropna().apply(lambda d: d.strftime("%Y-%m")).unique().tolist(),
                reverse=True
            )
        filtro_periodo = st.multiselect("Año-Mes", anio_mes_opts, placeholder="Todos los periodos...", key="prod_anio_mes")
    with f2:
        # Fecha — días con datos, orden cronológico descendente
        fecha_dia_opts = ["Todas"]
        if not df.empty and "fecha" in df.columns:
            fechas_unicas = sorted(df["fecha"].dropna().dt.normalize().unique(), reverse=True)
            fecha_dia_opts += [pd.Timestamp(f).strftime("%d/%m/%Y") for f in fechas_unicas]
        filtro_fecha_dia = st.multiselect("Fecha", [o for o in fecha_dia_opts if o != "Todas"], placeholder="Todas las fechas...", key="prod_fecha")
    with f3:
        cat_opts = ["Todas"]
        if not df.empty and "categoria" in df.columns:
            cat_opts += sorted(df["categoria"].dropna().unique().tolist())
        filtro_cat = st.multiselect("Categoría", [o for o in cat_opts if o != "Todas"], placeholder="Todas las categorías...", key="prod_categoria")
    with f4:
        tend_opts = ["Todas"]
        if not df.empty and "tendencia" in df.columns:
            tend_opts += sorted(df["tendencia"].dropna().unique().tolist())
        filtro_tend = st.multiselect("Tendencia", [o for o in tend_opts if o != "Todas"], placeholder="Todas...", key="prod_tendencia")
    with f5:
        buscar_prod = st.text_input("🔍 Buscar producto", placeholder="Nombre del producto...", key="prod_buscar")

    ultimo_prod = None; n_productos_int = n_alza = n_baja = 0
    if not df.empty:
        ultimo_prod = df["fecha"].max() if "fecha" in df.columns else None
        if "producto" in df.columns:
            n_productos_int = df["producto"].nunique()
        if "tendencia" in df.columns:
            tend_lower = df.groupby("producto")["fecha"].idxmax().map(lambda i: str(df.loc[i, "tendencia"]).lower() if i in df.index else "")
            n_alza = int((tend_lower.str.contains("alza|sube|alcista|up|positiv", na=False)).sum())
            n_baja = int((tend_lower.str.contains("baja|baj|bajista|down|negativ", na=False)).sum())

    c1, c2, c3, c4 = st.columns(4)
    kpi_card(c1, "kpi-green", "📅", ultimo_prod.strftime("%d/%m/%y") if ultimo_prod is not None else "—", "Última cotización", "Fecha más reciente")
    kpi_card(c2, "kpi-blue",  "🌐", str(n_productos_int), "Productos Internacionales", "En seguimiento")
    kpi_card(c3, "kpi-green", "📈", str(n_alza), "En Alza",  "Tendencia positiva")
    kpi_card(c4, "kpi-red",   "📉", str(n_baja), "En Baja",  "Tendencia negativa")
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    df_f = df.copy()
    # Filtro Año-Mes
    if filtro_periodo and "fecha" in df_f.columns:
        mask = df_f["fecha"].apply(lambda d: d.strftime("%Y-%m")).isin(filtro_periodo)
        df_f = df_f[mask]
    # Filtro Fecha día exacto
    if filtro_fecha_dia and "fecha" in df_f.columns:
        df_f = df_f[df_f["fecha"].apply(lambda d: d.strftime("%d/%m/%Y")).isin(filtro_fecha_dia)]
    if filtro_cat and "categoria" in df_f.columns:
        df_f = df_f[df_f["categoria"].isin(filtro_cat)]
    if filtro_tend and "tendencia" in df_f.columns:
        df_f = df_f[df_f["tendencia"].isin(filtro_tend)]
    if buscar_prod and "producto" in df_f.columns:
        df_f = df_f[df_f["producto"].str.contains(buscar_prod, case=False, na=False)]

    section_header("📈", "Tendencia de Precios por Categoría", "Evolución del precio de cierre — más antiguo a la izquierda, más reciente a la derecha")
    if not df_f.empty and "fecha" in df_f.columns and "precio_cierre" in df_f.columns and "categoria" in df_f.columns:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates

            df_chart = df_f.copy()
            df_chart["precio_cierre"] = pd.to_numeric(df_chart["precio_cierre"], errors="coerce")
            df_chart["fecha"] = pd.to_datetime(df_chart["fecha"])
            df_chart = df_chart.dropna(subset=["precio_cierre", "fecha"])
            df_grouped = (
                df_chart.groupby(["fecha", "categoria"])["precio_cierre"]
                .mean().reset_index().sort_values("fecha")
            )
            categorias = sorted(df_grouped["categoria"].dropna().unique().tolist())
            palette = ["#27a05e", "#f59e0b", "#3b82f6", "#ef4444", "#8b5e34", "#a855f7", "#0ea5e9", "#f97316"]

            fig, ax = plt.subplots(figsize=(11, 4.5))
            fig.patch.set_facecolor("#f0faf4")
            ax.set_facecolor("#f0faf4")

            for i, cat in enumerate(categorias):
                sub = df_grouped[df_grouped["categoria"] == cat].sort_values("fecha")
                if sub.empty:
                    continue
                color = palette[i % len(palette)]
                ax.plot(sub["fecha"], sub["precio_cierre"],
                        color=color, linewidth=2.2, marker="o", markersize=4,
                        label=str(cat), zorder=3)

            ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%y"))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.xticks(rotation=30, ha="right", fontsize=9, color="#0d2b1a")
            ax.set_ylabel("Precio cierre", fontsize=10, color="#0d2b1a")
            ax.tick_params(axis="y", colors="#0d2b1a", labelsize=9)
            ax.yaxis.grid(True, color="#d1ead9", linewidth=0.8, zorder=0)
            ax.xaxis.grid(True, color="#d1ead9", linewidth=0.5, linestyle="--", zorder=0)
            ax.set_axisbelow(True)
            for spine in ["top", "right"]:
                ax.spines[spine].set_visible(False)
            for spine in ["left", "bottom"]:
                ax.spines[spine].set_color("#d1ead9")
            ax.legend(loc="upper left", bbox_to_anchor=(0, 1.13),
                      ncol=max(1, len(categorias)),
                      fontsize=9, framealpha=0.85, edgecolor="#d1ead9")
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        except Exception as e_chart:
            st.warning(f"⚠️ Error al renderizar gráfico de tendencia: {e_chart}")
    elif df_f.empty:
        st.info("No hay datos que coincidan con los filtros aplicados")
    else:
        st.info("Sin datos suficientes para el gráfico de tendencia")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    fecha_header = ultimo_prod.strftime("%Y-%m-%d") if ultimo_prod is not None else "—"
    total_rows = len(df_f) if not df_f.empty else 0

    # Fila: icono + título + Excel
    hdr_cols = st.columns([0.05, 0.78, 0.17])
    with hdr_cols[0]:
        st.markdown('<div style="width:40px;height:40px;background:linear-gradient(135deg,#27a05e,#3dbd76);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;box-shadow:0 4px 12px rgba(39,160,94,0.3);margin-top:2px;">📋</div>', unsafe_allow_html=True)
    with hdr_cols[1]:
        st.markdown(f'<div style="padding-top:4px;"><p style="font-size:1.25rem;font-weight:700;color:#0d2b1a;margin:0;">Evolución de Productos Internacionales</p><p style="font-size:0.8rem;color:#7aa98e;margin:0;">Última actualización: {fecha_header} &nbsp;·&nbsp; {total_rows} registros</p></div>', unsafe_allow_html=True)
    with hdr_cols[2]:
        if not df_f.empty:
            import io
            output = io.BytesIO()
            cols_export = [c for c in ["fecha", "producto", "precio_cierre", "moneda", "var_precio", "categoria", "tendencia"] if c in df_f.columns]
            df_export = df_f[cols_export].sort_values("fecha", ascending=False).reset_index(drop=True)
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df_export.to_excel(writer, index=False, sheet_name="Productos")
            st.download_button(
                label="📥 Excel",
                data=output.getvalue(),
                file_name=f"productos_internacionales_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

    st.markdown("<div style='border-bottom:2px solid #d1ead9;margin-bottom:12px;'></div>", unsafe_allow_html=True)

    if not df_f.empty:
        cols_tabla = [c for c in ["fecha", "producto", "precio_cierre", "moneda", "var_precio", "categoria", "tendencia"] if c in df_f.columns]
        col_widths = "1.2fr " + " ".join(["1.4fr"] * (len(cols_tabla) - 1))
        col_labels = {"fecha": "Fecha", "producto": "Producto", "precio_cierre": "Precio Cierre", "moneda": "Moneda", "var_precio": "Var. Precio", "categoria": "Categoría", "tendencia": "Tendencia"}
        header_html = "".join([f'<span style="font-size:0.75rem;font-weight:700;color:#0d2b1a;text-transform:uppercase;letter-spacing:0.06em;">{col_labels.get(c, c)}</span>' for c in cols_tabla])
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:{col_widths};gap:8px;padding:10px 20px;background:#f0faf4;border-radius:10px 10px 0 0;border:1px solid var(--border);border-bottom:2px solid var(--border);margin-bottom:2px;">
            {header_html}
        </div>
        """, unsafe_allow_html=True)

        df_tabla = df_f[cols_tabla].sort_values("fecha", ascending=False).reset_index(drop=True)
        for _, row in df_tabla.iterrows():
            tend_val = str(row.get("tendencia", "") or "").lower()
            var_val  = row.get("var_precio", None)
            if any(x in tend_val for x in ["alza", "sube", "alcista", "up", "positiv"]):
                tend_bg, tend_col, tend_svg = "#dcfce7", "#15803d", '<svg width="18" height="14" viewBox="0 0 22 16"><polyline points="2,13 8,7 13,10 20,3" fill="none" stroke="#27a05e" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="15,3 20,3 20,8" fill="none" stroke="#27a05e" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            elif any(x in tend_val for x in ["baja", "bajista", "down", "negativ"]):
                tend_bg, tend_col, tend_svg = "#fee2e2", "#b91c1c", '<svg width="18" height="14" viewBox="0 0 22 16"><polyline points="2,3 8,9 13,6 20,13" fill="none" stroke="#ef4444" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="15,13 20,13 20,8" fill="none" stroke="#ef4444" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            else:
                tend_bg, tend_col, tend_svg = "#fef3c7", "#b45309", '<svg width="18" height="14" viewBox="0 0 22 16"><line x1="2" y1="8" x2="20" y2="8" stroke="#f59e0b" stroke-width="2.2" stroke-linecap="round"/></svg>'
            try:
                var_f = float(var_val) if var_val is not None else None
                var_str = (f"+{var_f:.2f}%" if var_f > 0 else f"{var_f:.2f}%") if var_f is not None else "—"
                var_color = "#15803d" if (var_f or 0) > 0 else ("#b91c1c" if (var_f or 0) < 0 else "#475569")
            except Exception:
                var_str, var_color = str(var_val or "—"), "#475569"
            try:
                precio_str = f"{float(row.get('precio_cierre', 0) or 0):.4f}"
            except Exception:
                precio_str = str(row.get("precio_cierre", "—"))
            try:
                fecha_str = pd.to_datetime(row.get("fecha", "")).strftime("%d/%m/%Y")
            except Exception:
                fecha_str = str(row.get("fecha", ""))

            cells = []
            for c in cols_tabla:
                if c == "fecha": cells.append(f'<span style="font-family:\'DM Mono\',monospace;font-size:0.8rem;color:#7aa98e;">{fecha_str}</span>')
                elif c == "producto": cells.append(f'<span style="font-weight:600;font-size:0.88rem;color:#0d2b1a;">{row.get("producto","—")}</span>')
                elif c == "precio_cierre": cells.append(f'<span style="font-family:\'DM Mono\',monospace;font-size:0.88rem;color:#1a5c38;font-weight:600;">{precio_str}</span>')
                elif c == "moneda": cells.append(f'<span style="font-size:0.82rem;color:#475569;font-weight:500;">{row.get("moneda","—")}</span>')
                elif c == "var_precio": cells.append(f'<span style="font-family:\'DM Mono\',monospace;font-size:0.85rem;font-weight:700;color:{var_color};">{var_str}</span>')
                elif c == "categoria": cells.append(f'<span style="font-size:0.82rem;color:#1a5c38;background:#f0faf4;padding:2px 8px;border-radius:6px;font-weight:600;">{row.get("categoria","—")}</span>')
                elif c == "tendencia": cells.append(f'<span style="display:inline-flex;align-items:center;gap:6px;background:{tend_bg};color:{tend_col};font-weight:700;font-size:0.78rem;padding:3px 10px;border-radius:20px;">{tend_svg} {str(row.get("tendencia","—")).upper()}</span>')
            cells_html = "".join([f"<span>{cell}</span>" for cell in cells])
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:{col_widths};gap:8px;align-items:center;padding:12px 20px;background:white;border:1px solid var(--border);border-top:none;transition:background 0.15s;">
                {cells_html}
            </div>
            """, unsafe_allow_html=True)
        st.caption(f"{total_rows} registros totales")
    else:
        st.info("Sin datos disponibles con los filtros seleccionados")


def render_energia():
    df = load("v_resumen_energia", order_col="fecha", limit=90)

    if not df.empty and "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(df["fecha"])
        ultima_fecha = df["fecha"].max()
    else:
        ultima_fecha = None

    page_hero("⚡ Energía", "Monitor de Energía", "Precios PVPC diarios y planificación de consumo", ultima_act=ultima_fecha)

    if df.empty:
        st.info("Sin datos de energía disponibles aún. El pipeline se ejecuta una vez al día.")
        return

    # Filtros
    f1, f2, f3, f4 = st.columns([1, 1, 1, 1.5])
    with f1:
        anio_mes_opts = sorted(df["fecha"].dropna().apply(lambda d: d.strftime("%Y-%m")).unique().tolist(), reverse=True)
        filtro_periodo = st.multiselect("Año-Mes", anio_mes_opts, placeholder="Todos los períodos...", key="en_periodo")
    with f2:
        tramo_opts = ["Todos"] + sorted(df["tramo_mayoria"].dropna().unique().tolist())
        filtro_tramo = st.multiselect("Tramo predominante", [o for o in tramo_opts if o != "Todos"], placeholder="Todos los tramos...", key="en_tramo")
    with f3:
        estado_opts = ["Todos"] + sorted(df["estado_costo"].dropna().unique().tolist())
        filtro_estado = st.multiselect("Estado costo", [o for o in estado_opts if o != "Todos"], placeholder="Todos los estados...", key="en_estado")
    with f4:
        buscar_fecha = st.text_input("🔍 Buscar fecha", placeholder="ej: 2026-03...", key="en_buscar")

    df_f = df.copy()
    if filtro_periodo:
        df_f = df_f[df_f["fecha"].apply(lambda d: d.strftime("%Y-%m")).isin(filtro_periodo)]
    if filtro_tramo:
        df_f = df_f[df_f["tramo_mayoria"].isin(filtro_tramo)]
    if filtro_estado:
        df_f = df_f[df_f["estado_costo"].isin(filtro_estado)]
    if buscar_fecha:
        df_f = df_f[df_f["fecha"].astype(str).str.contains(buscar_fecha, case=False, na=False)]
    df_f = df_f.sort_values("fecha", ascending=False).reset_index(drop=True)
    hoy = df_f.iloc[0].to_dict() if not df_f.empty else None

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # BLOQUE 1 — PANEL DE DECISIÓN DIARIA
    section_header("🔋", "Panel de Decisión Diaria", "Recomendación de consumo para hoy")

    if hoy is not None:
        estado = str(hoy.get("estado_costo", "") or "").upper()
        if estado == "BAJO":
            sem_bg, sem_col, sem_icon, sem_txt = "#dcfce7", "#15803d", "🟢", "PRECIO BAJO — Momento óptimo para riego y bombeo"
        elif estado == "ALTO":
            sem_bg, sem_col, sem_icon, sem_txt = "#fee2e2", "#b91c1c", "🔴", "PRECIO ALTO — Posponer consumo intensivo"
        else:
            sem_bg, sem_col, sem_icon, sem_txt = "#fef3c7", "#b45309", "🟡", "PRECIO NORMAL — Consumo moderado permitido"

        var = hoy.get("var_per_prev", None)
        var_str = (f"{'↑' if float(var) > 0 else '↓'} {abs(float(var)):.1f}% vs ayer") if var is not None else "Sin referencia anterior"
        var_col = "#b91c1c" if (float(var) if var else 0) > 0 else "#15803d" if (float(var) if var else 0) < 0 else "#7aa98e"
        fecha_hoy_str = hoy["fecha"].strftime("%d/%m/%Y") if hasattr(hoy["fecha"], "strftime") else str(hoy["fecha"])

        st.markdown(f"""
        <div style="background:{sem_bg};border:2px solid {sem_col};border-radius:16px;padding:20px 28px;margin-bottom:20px;display:flex;align-items:center;gap:20px;">
            <span style="font-size:3rem;">{sem_icon}</span>
            <div style="flex:1">
                <div style="font-size:1.1rem;font-weight:800;color:{sem_col};margin-bottom:4px;">{sem_txt}</div>
                <div style="font-size:0.85rem;color:#475569;">📅 {fecha_hoy_str} &nbsp;·&nbsp; <span style="color:{var_col};font-weight:600;">{var_str}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        k1, k2, k3, k4 = st.columns(4)
        kpi_card(k1, "kpi-green", "⚡", f"{float(hoy.get('precio_medio', 0) or 0):.4f}€", "Precio Medio", "€/kWh hoy")
        kpi_card(k2, "kpi-blue",  "📉", f"{float(hoy.get('precio_min', 0) or 0):.4f}€", "Precio Mínimo", f"Hora {hoy.get('hora_min','—')}:00h")
        kpi_card(k3, "kpi-red",   "📈", f"{float(hoy.get('precio_max', 0) or 0):.4f}€", "Precio Máximo", f"Hora {hoy.get('hora_max','—')}:00h")
        p_min = float(hoy.get("precio_min", 0) or 0)
        p_max = float(hoy.get("precio_max", 0) or 0)
        ahorro_10kw = round((p_max - p_min) * 10, 3)
        kpi_card(k4, "kpi-amber", "💰", f"{ahorro_10kw:.3f}€", "Ahorro pot. 10kW·h", "Valle vs Punta")
    else:
        st.info("Sin datos para hoy todavía.")

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # BLOQUE 2 — CALCULADORA DE AHORRO
    section_header("💡", "Calculadora de Ahorro", "Estimación de coste según franja horaria")

    if hoy is not None:
        cc1, cc2 = st.columns([1, 1])
        with cc1:
            potencia_kw = st.number_input("Potencia de la bomba (kW)", min_value=0.5, max_value=500.0, value=10.0, step=0.5, key="en_potencia")
            horas_riego = st.number_input("Horas de riego previstas", min_value=0.5, max_value=24.0, value=4.0, step=0.5, key="en_horas")

        p_min_c = float(hoy.get("precio_min", 0) or 0)
        p_max_c = float(hoy.get("precio_max", 0) or 0)
        p_med_c = float(hoy.get("precio_medio", 0) or 0)
        h_min_c = hoy.get("hora_min", "—")
        h_max_c = hoy.get("hora_max", "—")

        coste_valle = round(potencia_kw * horas_riego * p_min_c, 4)
        coste_punta = round(potencia_kw * horas_riego * p_max_c, 4)
        coste_medio = round(potencia_kw * horas_riego * p_med_c, 4)
        ahorro_tot  = round(coste_punta - coste_valle, 4)

        with cc2:
            st.markdown(f"""
            <div style="background:white;border:1px solid var(--border);border-radius:16px;padding:20px 24px;box-shadow:0 2px 12px rgba(13,43,26,0.07);">
                <p style="font-size:0.75rem;font-weight:700;color:#7aa98e;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:14px;">Estimación para {potencia_kw} kW · {horas_riego}h</p>
                <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid var(--border);">
                    <span style="font-size:0.88rem;color:#0d2b1a;">🟢 Hora Valle (hora {h_min_c}:00)</span>
                    <span style="font-family:'DM Mono',monospace;font-weight:700;color:#15803d;font-size:1rem;">{coste_valle:.4f} €</span>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid var(--border);">
                    <span style="font-size:0.88rem;color:#0d2b1a;">🟡 Precio Medio del día</span>
                    <span style="font-family:'DM Mono',monospace;font-weight:700;color:#b45309;font-size:1rem;">{coste_medio:.4f} €</span>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid var(--border);">
                    <span style="font-size:0.88rem;color:#0d2b1a;">🔴 Hora Punta (hora {h_max_c}:00)</span>
                    <span style="font-family:'DM Mono',monospace;font-weight:700;color:#b91c1c;font-size:1rem;">{coste_punta:.4f} €</span>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0 4px;">
                    <span style="font-size:0.92rem;font-weight:700;color:#0d2b1a;">💰 Ahorro potencial</span>
                    <span style="font-family:'DM Mono',monospace;font-weight:800;color:#15803d;font-size:1.15rem;">{ahorro_tot:.4f} €</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Sin datos para calcular ahorro.")

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # BLOQUE 3 — HISTÓRICO DE PRECIOS
    total_rows = len(df_f)
    fecha_header = df_f["fecha"].max().strftime("%d/%m/%Y") if not df_f.empty else "—"

    hdr_en = st.columns([0.05, 0.78, 0.17])
    with hdr_en[0]:
        st.markdown('<div style="width:40px;height:40px;background:linear-gradient(135deg,#27a05e,#3dbd76);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;box-shadow:0 4px 12px rgba(39,160,94,0.3);margin-top:2px;">📅</div>', unsafe_allow_html=True)
    with hdr_en[1]:
        st.markdown(f'<div style="padding-top:4px;"><p style="font-size:1.25rem;font-weight:700;color:#0d2b1a;margin:0;">Histórico de Precios</p><p style="font-size:0.8rem;color:#7aa98e;margin:0;">Última actualización: {fecha_header} &nbsp;·&nbsp; {total_rows} registros</p></div>', unsafe_allow_html=True)
    with hdr_en[2]:
        if not df_f.empty:
            import io
            output_en = io.BytesIO()
            cols_exp = [c for c in ["fecha","precio_medio","precio_min","hora_min","precio_max","hora_max","tramo_mayoria","var_per_prev","estado_costo","recomendacion_consumo"] if c in df_f.columns]
            df_exp = df_f[cols_exp].copy()
            df_exp["fecha"] = df_exp["fecha"].dt.strftime("%d/%m/%Y")
            with pd.ExcelWriter(output_en, engine="openpyxl") as writer:
                df_exp.to_excel(writer, index=False, sheet_name="Energía")
            st.download_button(
                label="📥 Excel",
                data=output_en.getvalue(),
                file_name=f"energia_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="excel_energia"
            )

    st.markdown("<div style='border-bottom:2px solid #d1ead9;margin-bottom:12px;'></div>", unsafe_allow_html=True)

    if len(df_f) > 1:
        df_plot = df_f.sort_values("fecha")
        colores_bar = ["#ef4444" if str(e).upper()=="ALTO" else "#27a05e" if str(e).upper()=="BAJO" else "#f59e0b" for e in df_plot.get("estado_costo", ["NORMAL"]*len(df_plot))]
        fig_en = go.Figure()
        fig_en.add_trace(go.Bar(x=df_plot["fecha"], y=df_plot["precio_medio"], name="Precio Medio", marker_color=colores_bar, opacity=0.85, hovertemplate="%{x|%d/%m/%Y}<br>Medio: %{y:.4f} €/kWh<extra></extra>"))
        fig_en.add_trace(go.Scatter(x=df_plot["fecha"], y=df_plot["precio_min"], name="Mínimo", line=dict(color="#27a05e", width=1.5, dash="dot"), hovertemplate="%{x|%d/%m/%Y}<br>Mín: %{y:.4f} €/kWh<extra></extra>"))
        fig_en.add_trace(go.Scatter(x=df_plot["fecha"], y=df_plot["precio_max"], name="Máximo", line=dict(color="#ef4444", width=1.5, dash="dot"), hovertemplate="%{x|%d/%m/%Y}<br>Máx: %{y:.4f} €/kWh<extra></extra>"))
        layout_en = {**CHART_LAYOUT}
        layout_en["xaxis"] = dict(showgrid=False, color="#7aa98e", title="Fecha")
        layout_en["yaxis"] = dict(gridcolor="#e8f5ee", color="#7aa98e", title="€/kWh")
        layout_en["legend"] = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        fig_en.update_layout(height=260, **layout_en)
        st.plotly_chart(fig_en, use_container_width=True, config={"displayModeBar": False})

    if not df_f.empty:
        cols_t = [c for c in ["fecha","precio_medio","precio_min","hora_min","precio_max","hora_max","tramo_mayoria","var_per_prev","estado_costo"] if c in df_f.columns]
        col_labels_t = {"fecha":"Fecha","precio_medio":"P. Medio","precio_min":"P. Mínimo","hora_min":"Hora Mín","precio_max":"P. Máximo","hora_max":"Hora Máx","tramo_mayoria":"Tramo","var_per_prev":"Var. %","estado_costo":"Estado"}
        col_widths_t = "1.2fr " + " ".join(["1fr"] * (len(cols_t) - 1))
        header_t_html = "".join([f'<span style="font-size:0.75rem;font-weight:700;color:#0d2b1a;text-transform:uppercase;letter-spacing:0.06em;">{col_labels_t.get(c,c)}</span>' for c in cols_t])
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:{col_widths_t};gap:8px;padding:10px 20px;background:#f0faf4;border-radius:10px 10px 0 0;border:1px solid var(--border);border-bottom:2px solid var(--border);margin-bottom:2px;">
            {header_t_html}
        </div>
        """, unsafe_allow_html=True)

        for _, row in df_f[cols_t].iterrows():
            est_r = str(row.get("estado_costo","") or "").upper()
            est_bg  = "#fee2e2" if est_r=="ALTO" else "#dcfce7" if est_r=="BAJO" else "#fef3c7"
            est_col = "#b91c1c" if est_r=="ALTO" else "#15803d" if est_r=="BAJO" else "#b45309"
            var_r = row.get("var_per_prev", None)
            try:
                vf = float(var_r) if var_r is not None else None
                vs = (f"+{vf:.1f}%" if vf > 0 else f"{vf:.1f}%") if vf is not None else "—"
                vc = "#b91c1c" if (vf or 0) > 0 else "#15803d" if (vf or 0) < 0 else "#7aa98e"
            except Exception:
                vs, vc = "—", "#7aa98e"
            try:
                fecha_r_str = pd.to_datetime(row.get("fecha","")).strftime("%d/%m/%Y")
            except Exception:
                fecha_r_str = str(row.get("fecha","—"))

            cells_t = []
            for c in cols_t:
                if c == "fecha":
                    cells_t.append(f'<span style="font-family:DM Mono,monospace;font-size:0.8rem;color:#7aa98e;">{fecha_r_str}</span>')
                elif c in ["precio_medio","precio_min","precio_max"]:
                    v = row.get(c, 0)
                    cells_t.append(f'<span style="font-family:DM Mono,monospace;font-size:0.85rem;color:#1a5c38;font-weight:600;">{float(v):.4f}</span>')
                elif c in ["hora_min","hora_max"]:
                    cells_t.append(f'<span style="font-family:DM Mono,monospace;font-size:0.85rem;color:#475569;">{row.get(c,"—")}:00h</span>')
                elif c == "tramo_mayoria":
                    t = str(row.get(c,"") or "")
                    t_bg  = "#dcfce7" if t=="Valle" else "#fef3c7" if t=="Llano" else "#fee2e2"
                    t_col = "#15803d" if t=="Valle" else "#b45309" if t=="Llano" else "#b91c1c"
                    cells_t.append(f'<span style="font-size:0.78rem;font-weight:700;background:{t_bg};color:{t_col};padding:3px 8px;border-radius:20px;">{t}</span>')
                elif c == "var_per_prev":
                    cells_t.append(f'<span style="font-family:DM Mono,monospace;font-size:0.85rem;font-weight:700;color:{vc};">{vs}</span>')
                elif c == "estado_costo":
                    cells_t.append(f'<span style="font-size:0.78rem;font-weight:700;background:{est_bg};color:{est_col};padding:3px 8px;border-radius:20px;">{est_r}</span>')
            cells_t_html = "".join([f"<span>{cell}</span>" for cell in cells_t])
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:{col_widths_t};gap:8px;align-items:center;padding:12px 20px;background:white;border:1px solid var(--border);border-top:none;">
                {cells_t_html}
            </div>
            """, unsafe_allow_html=True)
        st.caption(f"{total_rows} registros mostrados")
    else:
        st.info("Sin datos con los filtros seleccionados.")

def render_alertas():
    page_hero("🔔 Notificaciones", "Centro de Alertas", "Clima extremo y energía")
    df_clima = load("v_alertas_clima_extrema", order_col="fecha")
    df_energ = load("v_resumen_energia",       order_col="fecha")

    c1, c2, c3, c4 = st.columns(4)
    n_cl = int(df_clima["alerta_riesgo"].notna().sum()) if not df_clima.empty and "alerta_riesgo" in df_clima.columns else 0
    n_en = int(df_energ["estado_costo"].str.contains("caro|alto|punta", case=False, na=False).sum()) if not df_energ.empty and "estado_costo" in df_energ.columns else 0
    kpi_card(c1, "kpi-red"   if n_cl > 0 else "kpi-green", "🌩️", str(n_cl), "Alertas clima",   "Temperatura extrema")
    kpi_card(c2, "kpi-amber" if n_en > 0 else "kpi-green", "⚡", str(n_en), "Alertas energía", "kWh elevado")
    kpi_card(c3, "kpi-blue", "📋", str(len(df_clima)), "Registros clima",   "Disponibles")
    kpi_card(c4, "kpi-blue", "🕐", str(len(df_energ)), "Registros energía", "Disponibles")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    col_cl, col_en = st.columns(2)

    with col_cl:
        section_header("🌩️", "Alertas de Clima Extremo", "v_alertas_clima_extrema")
        if not df_clima.empty:
            df_c = df_clima.copy()
            df_c["fecha"] = pd.to_datetime(df_c["fecha"])
            df_c = df_c.sort_values("fecha", ascending=False)
            for _, row in df_c.head(10).iterrows():
                alerta = str(row.get("alerta_riesgo", "") or "")
                alerta_l = alerta.lower()
                if not alerta or alerta_l in ["none", "nan", ""]:
                    dot, cls = "dot-green", "alert-ok"; alerta = "Sin alerta"
                elif any(x in alerta_l for x in ["alta", "extremo", "peligro", "rojo"]):
                    dot, cls = "dot-red", "alert-critical"
                else:
                    dot, cls = "dot-amber", "alert-warning"
                fecha_str = row["fecha"].strftime("%d/%m/%Y") if hasattr(row["fecha"], "strftime") else str(row["fecha"])
                st.markdown(f"""
                <div class="alert-item {cls}">
                    <div class="alert-dot {dot}"></div>
                    <div style="flex:1">
                        <div class="alert-title">{row.get('estacion','—')}</div>
                        <div class="alert-desc">🌡️ Máx: <b>{row.get('temp_max','—')}°C</b> | Mín: <b>{row.get('temp_min','—')}°C</b></div>
                        <div class="alert-desc" style="margin-top:3px;">{alerta}</div>
                        <div class="alert-time">📅 {fecha_str}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            if len(df_c) > 3:
                df_plot = df_c.sort_values("fecha").tail(30)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df_plot["fecha"], y=df_plot["temp_max"], name="Máx", line=dict(color="#ef4444", width=2), fill="tonexty"))
                fig.add_trace(go.Scatter(x=df_plot["fecha"], y=df_plot["temp_min"], name="Mín", line=dict(color="#3b82f6", width=2)))
                fig.update_layout(height=200, **CHART_LAYOUT)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Sin alertas de clima disponibles")

    with col_en:
        section_header("⚡", "Precio Energía", "v_resumen_energia — media diaria €/kWh")
        if not df_energ.empty:
            df_e = df_energ.copy()
            df_e["fecha"] = pd.to_datetime(df_e["fecha"])
            df_e = df_e.sort_values("fecha", ascending=False)
            for _, row in df_e.head(7).iterrows():
                estado = str(row.get("estado_costo", "") or "").lower()
                if any(x in estado for x in ["caro", "alto"]): dot, cls = "dot-red", "alert-critical"
                elif "normal" in estado:                        dot, cls = "dot-amber", "alert-warning"
                else:                                           dot, cls = "dot-green", "alert-ok"
                var_p  = row.get("var_per_prev", None)
                var_str = f"{'+' if var_p > 0 else ''}{var_p:.1f}% vs ayer" if var_p is not None else "sin ref."
                var_color = "#ef4444" if var_p and var_p > 0 else "#27a05e" if var_p and var_p < 0 else "#7aa98e"
                hora_min = row.get("hora_min", "—")
                hora_max = row.get("hora_max", "—")
                p_min    = row.get("precio_min", "—")
                p_max    = row.get("precio_max", "—")
                tramo    = row.get("tramo_mayoria", "—")
                fecha_str = row["fecha"].strftime("%d/%m/%Y") if hasattr(row["fecha"], "strftime") else str(row["fecha"])
                st.markdown(f"""
                <div class="alert-item {cls}">
                    <div class="alert-dot {dot}"></div>
                    <div style="flex:1">
                        <div class="alert-title">Media: <b class="mono">{row.get('precio_medio','—')} €/kWh</b> &nbsp;<span style="font-size:0.8rem;color:{var_color};font-weight:600;">{var_str}</span></div>
                        <div class="alert-desc">🔋 Mín: <b>{p_min} €</b> a las {hora_min}h &nbsp;|&nbsp; Máx: <b>{p_max} €</b> a las {hora_max}h</div>
                        <div class="alert-desc">⚡ Tramo predominante: <b>{tramo}</b> &nbsp;|&nbsp; {row.get('recomendacion_consumo','—')}</div>
                        <div class="alert-time">📅 {fecha_str}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            # Gráfico evolución precio medio diario
            df_plot = df_e.sort_values("fecha").tail(30)
            if len(df_plot) > 1 and "precio_medio" in df_plot.columns:
                colores_b = df_plot["tramo_mayoria"].apply(
                    lambda t: "#ef4444" if "punta" in str(t).lower()
                    else "#f59e0b" if "llano" in str(t).lower()
                    else "#27a05e"
                ) if "tramo_mayoria" in df_plot.columns else ["#27a05e"] * len(df_plot)
                fig2 = go.Figure(go.Bar(
                    x=df_plot["fecha"], y=df_plot["precio_medio"],
                    marker_color=colores_b, opacity=0.85,
                    hovertemplate="%{x|%d/%m}<br>%{y:.4f} €/kWh<extra></extra>"
                ))
                layout2 = {**CHART_LAYOUT}
                layout2["xaxis"] = dict(showgrid=False, color="#7aa98e", title="Fecha")
                layout2["yaxis"] = dict(gridcolor="#e8f5ee", color="#7aa98e", title="€/kWh medio")
                fig2.update_layout(height=200, **layout2)
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Sin datos de energía disponibles")

def render_configuracion():
    page_hero("⚙️ Ajustes", "Configuración del Sistema", "Secrets de Supabase, AEMET y diagnóstico de conexiones")
    col1, col2 = st.columns(2)

    with col1:
        section_header("🔐", "Estado de conexiones", "Verificación en tiempo real")
        try:
            sb = get_supabase()
            sb.table("datos_clima").select("id").limit(1).execute()
            st.markdown("""<div class="alert-item alert-ok"><div class="alert-dot dot-green"></div><div><div class="alert-title">✅ Supabase conectado</div><div class="alert-desc">Lectura de tablas OK</div></div></div>""", unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""<div class="alert-item alert-critical"><div class="alert-dot dot-red"></div><div><div class="alert-title">❌ Supabase no conectado</div><div class="alert-desc">{str(e)[:120]}</div></div></div>""", unsafe_allow_html=True)
        try:
            ak = st.secrets["AEMET_KEY"]
            st.markdown("""<div class="alert-item alert-ok"><div class="alert-dot dot-green"></div><div><div class="alert-title">✅ AEMET configurado</div><div class="alert-desc">API key presente en secrets</div></div></div>""", unsafe_allow_html=True)
        except Exception:
            st.markdown("""<div class="alert-item alert-warning"><div class="alert-dot dot-amber"></div><div><div class="alert-title">⚠️ AEMET no configurado</div><div class="alert-desc">Añade AEMET_KEY en Streamlit Secrets</div></div></div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        section_header("📖", "Cómo configurar secrets", "")
        st.markdown("""<div style="background:#f0faf4;border:1px solid #d1ead9;border-radius:12px;padding:16px 20px;font-size:0.82rem;color:#1a5c38;line-height:1.9;"><b>1.</b> En Streamlit Cloud → tu app → <b>Settings → Secrets</b><br><b>2.</b> Pega el siguiente bloque (reemplaza las claves):</div>""", unsafe_allow_html=True)
        st.code('SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"\nSUPABASE_KEY = "tu_clave_supabase"\nAEMET_KEY    = "tu_clave_aemet"', language="toml")
        st.warning("⚠️ Nunca pongas las claves directamente en el código Python.")

    with col2:
        section_header("📊", "Tablas y vistas disponibles", "Estado de cada fuente de datos")
        tablas = [
            ("datos_clima",             "🌤️", "Meteorología histórica",     "13 cols"),
            ("datos_energias",          "⚡", "Precios energía eléctrica",  "8 cols"),
            ("precios_agricolas",       "🌾", "Precios lonja",              "14 cols"),
            ("mercados_internacionales","🌍", "Mercados internacionales",   "9 cols"),
            ("mapeo_productos",         "🗂️", "Catálogo productos",        "4 cols"),
            ("v_mapa_operaciones",      "📍", "Vista mapa estaciones",      "12 cols"),
            ("v_salud_sectores",        "💚", "Vista salud sectores",       "6 cols"),
            ("v_alertas_clima_extrema", "🌩️", "Vista alertas clima",       "5 cols"),
            ("v_resumen_energia",       "⚡", "Vista alertas energía",      "6 cols"),
            ("v_comparativa_mercados",  "📊", "Vista comparativa",          "6 cols"),
        ]
        sb = get_supabase()
        for tabla, icon, desc, cols_info in tablas:
            n, color = "—", "#ef4444"
            if sb:
                try:
                    r = sb.table(tabla).select("*", count="exact").limit(1).execute()
                    n = str(r.count) if r.count is not None else "✓"; color = "#27a05e"
                except:
                    n, color = "err", "#f59e0b"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;padding:9px 14px;background:white;border-radius:10px;border:1px solid var(--border);margin-bottom:6px;">
                <span>{icon}</span>
                <div style="flex:1;">
                    <div style="font-weight:600;font-size:0.82rem;color:#0d2b1a;font-family:'DM Mono',monospace;">{tabla}</div>
                    <div style="font-size:0.72rem;color:#7aa98e;">{desc} · {cols_info}</div>
                </div>
                <span style="font-family:'DM Mono',monospace;font-size:0.85rem;font-weight:700;color:{color};">{n}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if st.button("🔄 Limpiar caché y reconectar", use_container_width=True):
            st.cache_data.clear(); st.cache_resource.clear()
            st.success("Caché limpiada. Reconectando..."); st.rerun()

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if not st.session_state["logged_in"]:
        render_login(); return
    page = render_sidebar()
    try:
        if   "Dashboard"   in page: render_dashboard()
        elif "Mapa"        in page: render_mapa()
        elif "Mercados"    in page: render_mercados()
        elif "Productos"   in page: render_monitor_productos()
        elif "Energía"     in page: render_energia()
        elif "Alertas"     in page: render_alertas()
        elif "Configuraci" in page: render_configuracion()
    except Exception as e:
        st.error(f"Error al cargar la sección: {e}")
        st.info("Pulsa '🔄 Restablecer Datos' en el menú lateral o recarga la página.")

if __name__ == "__main__":
    main()
