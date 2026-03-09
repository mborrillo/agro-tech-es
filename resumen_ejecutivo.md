# 🌿 AgroTech — Resumen Ejecutivo

> **"El campo extremeño produce con esfuerzo y perseverancia. AgroTech le da información de valor, para que su esfuerzo y dedicación rinda más."**

---

## Qué es AgroTech

AgroTech es una plataforma digital de monitorización y análisis para el sector agrícola de España, y Extremadura en particular. En una sola pantalla, el productor ve el estado climático de su comarca, el precio al que cotiza su cosecha frente a los mercados globales, el coste de la electricidad en tiempo real para decidir cuándo encender el sistema de riego, y las alertas activas de clima extremo.

No es una app de previsión del tiempo. Tampoco es una hoja de cálculo de precios. Es una herramienta que se conecta a datos reales y se actualiza automáticamente cada día.

**Disponible en:** [agro-tech.streamlit.app](https://agro-tech.streamlit.app)

---

## El problema que resuelve

Un agricultor de Badajoz sabe lo que vale su producción en la lonja local. Lo que no sabe — porque nunca tuvo acceso ágil a esa información — es si ese precio está por encima o por debajo de lo que marca el mercado internacional de referencia en ese mismo momento. Tampoco sabe si el precio de la luz esta tarde hace rentable encender el sistema de riego, o si es mejor esperar a la madrugada.

Esa ausencia de información tiene un coste: oportunidades de negociación perdidas, insumos como el agua y la energía malgastados en el momento menos rentable, cosechas afectadas por heladas que los datos ya anticipaban.

**AgroTech cierra esa brecha.**

---

## Lo que hace, en concreto

**🌡️ Monitorización climática por estación**
Temperatura, humedad, viento y precipitación desde estaciones de la AEMET en Badajoz, Cáceres, Mérida y otras localidades de la región. Con alertas automáticas por condiciones extremas: heladas, golpes de calor, viento fuerte que impide tratamientos fitosanitarios.

**📊 Comparativa de mercados: local vs. global**
El precio de la Lonja de Extremadura comparado directamente con los futuros internacionales de Chicago, convertidos a la misma unidad (€/kg). El sistema clasifica cada producto en dos modalidades:

- **Mercado Directo** (Trigo, Maíz): comparativa de precio absoluto en €/kg. El diferencial de arbitraje muestra cuánto se está ganando o perdiendo respecto al mercado global.
- **Mercado Proxy** (Aceites, Ganadería): la referencia internacional es un activo correlacionado, no equivalente en precio. El sistema compara la dirección de la variación semanal — ACOMPAÑANDO, NEUTRO o DIVERGIENDO — para detectar divergencias de tendencia.

**⚡ Gestión del coste energético — Monitor de Energía**
El sistema obtiene el precio PVPC de la electricidad (REE) y calcula diariamente los indicadores clave: precio medio, hora más barata, hora más cara y variación respecto al día anterior. Se presenta en tres bloques accionables:

- **Panel de Decisión Diaria:** semáforo VERDE/AMARILLO/ROJO con la recomendación del día ("Momento óptimo para riego y bombeo" / "Posponer consumo intensivo") y los KPIs de precio mínimo, máximo y ahorro potencial.
- **Calculadora de Ahorro:** el agricultor introduce la potencia de su bomba (kW) y las horas de riego previstas, y obtiene al instante el coste en hora valle, precio medio y hora punta, con el ahorro real en euros si elige la franja óptima.
- **Histórico de precios:** evolución diaria de los últimos 90 días con gráfico y tabla exportable a Excel, filtrable por período, tramo horario y estado de coste. Los filtros muestran todos los registros del período seleccionado, no solo el más reciente.

**🗺️ Mapa de operaciones**
Vista geográfica de todas las estaciones activas, con semáforo de estado (Óptimo / Precaución / Crítico) según las condiciones actuales de tratamiento y riego. Útil para cooperativas que gestionan múltiples explotaciones en distintas localidades o comarcas.

**📈 Monitor de Productos Internacionales**
Histórico de precios por categoría (cereales, aceites, ganadería…) con tendencias, variaciones y exportación de datos a Excel.

---

## Para quién es

### 🧑‍🌾 Productores individuales
Acceso a la misma información que antes solo llegaba a grandes explotaciones o intermediarios. Sabés cuándo regar, cuándo tratar, si el precio que te ofrecen es justo y si el tiempo va a acompañar esta semana.

### 🏛️ Cooperativas y agrupaciones
Visión consolidada de todos los sectores: qué está al alza, qué está cayendo, dónde están las oportunidades de comercialización. Datos para negociar mejor con mayor fundamento.

### 🏢 Administración pública e instituciones
Datos reales y actualizados sobre la salud del sector agrario regional. Útil para diseñar políticas de apoyo basadas en evidencia. Identificación inmediata de qué sectores necesitan intervención.

### 🔒 Empresas aseguradoras
Histórico fechado de eventos climáticos extremos por zona geográfica. Herramienta de valoración de riesgo con datos objetivos de temperatura, humedad y alertas registradas.

---

## Definición de Umbrales

Para más detalle sobre la lógica y configuración de los umbrales, ver:
https://github.com/mborrillo/agro-tech-es/blob/main/Interpretaci%C3%B3n%20de%20Umbrales%20AgroTech.md

---

## Vistas SQL del Modelo

### 1. `v_mapa_operaciones` — El Cerebro Operativo
**Objetivo:** Decidir cuándo actuar para no malgastar insumos.
Cruza el estado climático (temperatura, viento, humedad) con el precio de la energía para emitir recomendaciones de riego y tratamiento por estación. Estado resultante: **Óptimo / Precaución / Crítico**.

### 2. `v_comparativa_mercados` — El Escudo Comercial
**Objetivo:** Darle al agricultor poder de negociación.
Convierte los futuros internacionales (Chicago, en cents/bushel o cents/lb) a €/kg usando el tipo de cambio EUR/USD del mismo día. Clasifica cada relación como **DIRECTO** (comparativa de precio absoluto) o **PROXY** (comparativa de variación porcentual semanal). Campos principales: `tipo_referencia`, `relacion`, `precio_local_kg`, `precio_internacional_kg`, `diferencial_arbitraje`, `diferencial_pct`, `variacion_local`, `variacion_internacional`, `zona_arbitraje`, `recomendacion_arbitraje`.

### 3. `v_salud_sectores` — El Termómetro del Mercado
**Objetivo:** Diagnóstico rápido por sector (Olivar, Cereal, Ganadería…).
Agrega la variación semanal de todos los productos del sector y calcula el porcentaje al alza. Estado resultante: **ÓPTIMO** (≥ 80% de productos al alza o estables) / **ATENCIÓN** (≥ 50%) / **ALERTA** (< 50%).

### 4. `v_alertas_clima_extrema` — El Vigía Climático
**Objetivo:** Detectar condiciones fuera de rango para riego y tratamientos.
Filtra los registros de `datos_clima` que superan los umbrales de temperatura, viento o humedad definidos como críticos.

### 5. `v_resumen_energia` — El Panel de Decisión Energética
**Objetivo:** Traducir el precio de la electricidad en una acción concreta medible en euros.
Agrega las 24 horas del PVPC en un único registro diario. Campos clave: `precio_medio`, `precio_min`, `precio_max`, `hora_min`, `hora_max`, `tramo_mayoria`, `var_per_prev`, `estado_costo` (ALTO / NORMAL / BAJO), `recomendacion_consumo`.

### 6. `v_monitor_productos` — Evolución Internacional
**Objetivo:** Mostrar la tendencia histórica de productos internacionales por categoría con variación y exportación a Excel.

---

## Estado actual

- ✅ Dashboard operativo con datos reales de Supabase: [agro-tech.streamlit.app](https://agro-tech.streamlit.app/)
- ✅ Ingesta automática diaria: clima (AEMET), mercados (Yahoo Finance), energía (REE)
- ✅ Secciones activas: Dashboard, Mapa de Operaciones, Monitor de Mercados, Monitor de Productos, Monitor de Energía, Alertas (en construcción), Configuración
- ✅ Monitor de Mercados: gráfico dual DIRECTO/PROXY, tabla con filtros por período histórico completo y exportación Excel
- ✅ Monitor de Energía: panel de decisión diaria, calculadora de ahorro (kW) y histórico PVPC con ejes legibles
- ✅ Exportación de datos a Excel en todas las secciones
- 🔄 En desarrollo: frontend complementario para móviles: [agro-tech-es.lovable.app](https://agro-tech-es.lovable.app)
- 🔄 Próximo: autenticación por roles, notificaciones push, API abierta para terceros

---

## Tecnología

Construido sobre Python, Streamlit, Supabase (PostgreSQL) y GitHub Actions. Código abierto bajo licencia MIT. Diseñado para escalar a otras regiones agrarias de España con mínimos ajustes.

🔗 Repositorio: [github.com/mborrillo/agro-tech-es](https://github.com/mborrillo/agro-tech-es)

---

## 🚀 Próximos Pasos: Únete a la Inteligencia de Mercados Agrícolas

AgroTech está en fase de Validación. Nos interesa contactar con agricultores innovadores, gerentes de cooperativas y todo aquel que quiera:

- Reducir sus costes energéticos.
- Profesionalizar la toma de decisiones con datos en tiempo real.
- Informar y difundir un proyecto que aporta valor a todo un ecosistema productivo.
- Probar la herramienta en su propia explotación sin compromiso.

*Para inversión o integración institucional:*
https://marcos-borrillo.lovable.app · WhatsApp: https://wa.link/vvzmot

---

`#AgriculturaDigital` `#SmartFarming` `#Extremadura` `#AgroTech` `#Innovación` `#Sostenibilidad` `#DataDriven` `#CampoExtremeño` `#Cooperativas` `#AgTech` `#OpenData` `#Python` `#Supabase` `#AEMET` `#MercadoAgrícola` `#EficienciaEnergética` `#DigitalizaciónRural` `#StartupAgraria`
