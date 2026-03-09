# 🌿 AgroTech — Inteligencia en Mercados Agrarios

> Plataforma de inteligencia de datos para el sector agropecuario de Extremadura. Conecta el clima local, los precios de la lonja, los mercados internacionales y el coste energético en un único panel de decisión.

**🔗 Demo Streamlit:** [agro-tech.streamlit.app](https://agro-tech.streamlit.app) *(acceso libre — cualquier usuario y contraseña)*

---

## ¿Qué hace este proyecto?

Los agricultores y cooperativas de Extremadura operan con información fragmentada: el precio de la lonja local llega tarde, el mercado de futuros de Chicago parece distante, y la tarifa eléctrica cambia cada hora. Este dashboard centraliza todo eso y lo traduce en acciones concretas.

**Tres preguntas que responde esta herramienta:**

1. **¿Cuándo y dónde regar?** Cruzando clima real (AEMET) con el precio de la luz (PVPC), el sistema indica si conviene regar ahora o esperar a la franja horaria más barata.
2. **¿A qué precio vender?** Comparando el precio local (Lonja de Extremadura) con los futuros internacionales (Chicago), se detecta si el mercado local está infravalorado.
3. **¿Hay riesgo climático?** Alertas automáticas por temperaturas extremas, heladas o condiciones adversas para tratamientos fitosanitarios.

---

## ¿A quién va dirigido?

| Perfil | Qué obtiene |
|--------|------------|
| **Productor individual** | Recomendaciones de riego y tratamiento por estación, alertas de helada, precio de su cosecha vs. mercado global |
| **Gerente de cooperativa** | Visión sectorial (Cereales, Aceites, Ganadería…), comparativa local vs. internacional, exportación de datos |
| **Técnico agrónomo** | Datos históricos de clima y precios, mapa de operaciones con estado por estación |
| **Empresa de seguros agrarios** | Monitorización de alertas climáticas extremas con histórico fechado |

> **Nota:** La herramienta es funcional hoy para Extremadura, pero la arquitectura está diseñada para escalar a cualquier región con acceso a la API de AEMET y lonjas de referencia.

---

## Funcionalidades del Sistema

- **Dashboard principal** — KPIs de temperatura, humedad, precio kWh, alertas activas y salud por sector
- **Mapa de Operaciones** — Estaciones geolocalizadas con estado (Óptimo / Precaución / Crítico) según condiciones de riego y tratamiento
- **Monitor de Mercados** — Comparativa precio local vs. internacional con diferencial de arbitraje. Gráfico dual: Mercado Directo (€/kg vs Chicago) y Mercado Proxy (variación % local vs referencia global). Tabla con filtros de período que muestra el histórico completo seleccionado
- **Monitor de Productos** — Evolución histórica de precios internacionales por categoría, exportable a Excel
- **Monitor de Energía** — Panel de decisión diaria (semáforo PVPC), calculadora de ahorro por franja horaria (kW) e histórico de precios exportable a Excel
- **Centro de Alertas** — Clima extremo y seguimiento energético (en desarrollo)
- **Configuración** — Estado de conexión a Supabase y estadísticas de tablas

---

## Impacto del Cambio

| Antes | Con AgroTech |
|--------|------------|
| Riego basado en intuición o turno fijo | Riego basado en coste €/kWh en tiempo real |
| Tratamientos con riesgo de deriva o evaporación | Ventanas de aplicación con precisión meteorológica |
| Incertidumbre en el precio de venta local | Arbitraje de precios con mercados internacionales |

---

## Arquitectura

```
FUENTES EXTERNAS          SCRIPTS ETL (Python)        BASE DE DATOS           DASHBOARD
─────────────────         ────────────────────         ─────────────────       ──────────
AEMET API          ──▶   clima_monitor.py       ──▶   datos_clima
Yahoo Finance      ──▶   mercado_monitor.py     ──▶   mercados_internacionales ──▶  Streamlit
PVPC (REE)         ──▶   energia_monitor.py     ──▶   datos_energias                app_dashboard
Lonja Extremadura  ──▶   monitor_agrotech_v1    ──▶   precios_agricolas              _streamlit.py
                                                       correlaciones_agro
                                                       │
                                                Vistas SQL (lógica de negocio)
                                                v_mapa_operaciones
                                                v_comparativa_mercados
                                                v_salud_sectores
                                                v_alertas_clima_extrema
                                                v_monitor_productos
                                                v_resumen_energia
```

Los scripts ETL se ejecutan **automáticamente cada mañana** via GitHub Actions (`.github/workflows/`).

---

## Requisitos previos

- Python 3.10+
- Una cuenta en [Supabase](https://supabase.com) con las tablas y vistas del esquema (ver sección siguiente)
- Claves de API de AEMET (gratuita en [opendata.aemet.es](https://opendata.aemet.es))

---

## Instalación y puesta en marcha

### 1. Clonar el repositorio

```bash
git clone https://github.com/mborrillo/agro-tech-es.git
cd agro-tech-es
```

### 2. Instalar dependencias

Para el **dashboard**:
```bash
pip install -r requirements.txt
```

Para los **scripts de ingesta de datos** (ETL):
```bash
pip install -r requirements_monitors.txt
```

> Se usan dos archivos de requirements separados porque el dashboard (Streamlit + Plotly) y los scripts ETL (requests, yfinance, schedule) tienen dependencias distintas y se despliegan en entornos diferentes.

### 3. Configurar credenciales

Crea el archivo `.streamlit/secrets.toml` con tus claves de Supabase:

```toml
[supabase]
url = "https://xxxxxxxxxxxx.supabase.co"
key = "tu_anon_key_aqui"
```

Para los scripts ETL, configura las variables de entorno (o un archivo `.env`):

```
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_KEY=tu_anon_key_aqui
AEMET_API_KEY=tu_clave_aemet
```

**Nunca subas claves al repositorio.** El archivo `.streamlit/secrets.toml` y `.env` están en `.gitignore`.

### 4. Ejecutar el dashboard

```bash
streamlit run app_dashboard_streamlit.py
```

### 5. Ejecutar los scripts ETL manualmente (opcional)

```bash
python clima_monitor.py
python mercado_monitor.py
python energia_monitor.py
```

---

## Esquema de base de datos (Supabase/PostgreSQL)

### Tablas principales

| Tabla | Descripción |
|-------|-------------|
| `datos_clima` | Variables meteorológicas por estación y fecha (AEMET) |
| `precios_agricolas` | Precios de cierre de la Lonja de Extremadura (precio_min, precio_max en €/kg) |
| `mercados_internacionales` | Futuros internacionales (Chicago) via Yahoo Finance (precio_cierre en USD, unidades originales por activo) |
| `datos_energias` | Analytics PVPC diarios: precio medio, mínimo, máximo, hora óptima y variación vs día anterior (REE) |
| `correlaciones_agro` | Mapa de correlación entre productos locales y activos internacionales de referencia, con clasificación DIRECTO/PROXY |
| `estaciones_comarca` | Catálogo de estaciones AEMET con coordenadas y comarca asignada |

### Vistas SQL (lógica de negocio)

| Vista | Qué calcula |
|-------|-------------|
| `v_mapa_operaciones` | Estado de cada estación: coordenadas, clima actual, recomendaciones de riego y tratamiento |
| `v_comparativa_mercados` | Diferencial de arbitraje: precio local vs. internacional convertido a €/kg. Clasificación DIRECTO/PROXY y zona (FAVORABLE / EQUILIBRADO / DESFAVORABLE para directos; ACOMPAÑANDO / NEUTRO / DIVERGIENDO para proxy) |
| `v_salud_sectores` | Salud de cada sector (Cereales, Aceites, Ganadería…): variación media, porcentaje al alza y estado ÓPTIMO/ATENCIÓN/ALERTA |
| `v_alertas_clima_extrema` | Registros con condiciones fuera de rango para riego y tratamientos fitosanitarios |
| `v_resumen_energia` | Analytics PVPC diarios: estado de coste (ALTO/NORMAL/BAJO) y recomendación de consumo por franja |
| `v_monitor_productos` | Evolución histórica de productos internacionales con tendencia y variación |

---

## Despliegue en producción

El dashboard está pensado para desplegarse en **Streamlit Community Cloud**:

1. Sube el repositorio a GitHub (ya está)
2. Ve a [share.streamlit.io](https://share.streamlit.io) y conecta el repo
3. Añade los secrets de Supabase en la configuración de la app
4. El archivo principal es `app_dashboard_streamlit.py`

Los scripts ETL se ejecutan via **GitHub Actions** con el schedule definido en `.github/workflows/`.

---

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Frontend / Dashboard | Streamlit, Plotly, Matplotlib, HTML/CSS embebido |
| Base de datos | Supabase (PostgreSQL) |
| ETL / Ingesta | Python (requests, yfinance, supabase-py) |
| Automatización | GitHub Actions |
| Exportación | openpyxl (Excel) |
| Mapas | OpenStreetMap via Plotly Scattermapbox |

---

## Licencia

MIT — 2026.
