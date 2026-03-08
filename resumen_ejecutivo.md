# 🌿 AgroTech — Resumen Ejecutivo

> **"El campo extremeño produce con esfuerzo y perseverancia. AgroTech le da la información para que su dedicación y esfuerzo rinda más."**

---

## Qué es AgroTech

AgroTech es una plataforma digital de monitorización y análisis para el sector agrícola de España, y Extremadura en particular. En una sola pantalla, el productor ve el estado de sus parcelas segun la comarca - zona, el precio al que cotiza su cosecha en los mercados globales, al momento de regar saber cuanto es el costo, si hay riesgo o existen alertas climaticas en las próximas horas, entre otros.

No es una app de previsión del tiempo. Tampoco es una hoja de cálculo de precios. Es una herramienta inteligente que se conecta a datos reales y que se actualiza automáticamente cada día.

**Disponible en:** [agro-tech.streamlit.app](https://agro-tech.streamlit.app)

---

## El problema que resuelve

Un agricultor de Badajoz sabe lo que vale su produccion en la lonja local. Lo que no sabe — porque nunca tuvo acceso ágil a la información — es si ese precio está por encima o por debajo de lo que marca el mercado internacional de referencia en ese mismo momento. Tampoco sabe si el precio de la luz esta tarde hace rentable encender el sistema de riego, o si es mejor esperar a la madrugada.

Esa ausencia de información, tiene un costo: márgenes de negociación perdidos, agua y energía gastadas en un momento no rentable, cosechas afectadas por heladas que los datos ya anticipaban, etc.

**AgroTech cierra esa brecha.**

---

## Lo que hace, en concreto

**🌡️ Monitorización climática por estación**
Temperatura, humedad, viento y precipitación en tiempo real desde estaciones de la AEMET en Badajoz, Cáceres, Mérida y otras localidades de la región. Con alertas automáticas por condiciones extremas: heladas, golpes de calor, viento fuerte que impide tratamientos fitosanitarios.

**📊 Comparativa de mercados: local vs. global**
El precio de la Lonja de Extremadura comparado directamente con los futuros internacionales de Chicago y Londres, convertidos a la misma unidad (€/kg). Si el trigo local está infravalorado respecto al mercado global, el sistema lo muestra en verde. Si el productor está vendiendo por encima del precio de referencia, también lo sabe.

**⚡ Gestión del coste energético — Monitor de Energía**
El sistema obtiene el precio PVPC de la electricidad (REE) y calcula diariamente los analytics clave: precio medio, hora más barata, hora más cara y variación respecto al día anterior. El resultado se presenta en tres bloques accionables:

- **Panel de Decisión Diaria:** semáforo VERDE/AMARILLO/ROJO con la recomendación del día ("Momento óptimo para riego y bombeo" / "Posponer consumo intensivo") y los KPIs de precio mínimo, máximo y ahorro potencial.
- **Calculadora de Ahorro:** el agricultor introduce la potencia de su bomba y las horas de riego previstas y obtiene al instante el coste en hora valle, precio medio y hora punta, con el ahorro real en euros si elige la franja óptima.
- **Histórico de precios:** evolución diaria de los últimos 90 días con gráfico y tabla exportable a Excel, filtrable por período, tramo y estado de costo.

**🗺️ Mapa de operaciones**
Vista geográfica de todas las estaciones activas, con semáforo de estado (Óptimo / Precaución / Crítico) según las condiciones actuales de tratamiento y riego. Útil para cooperativas que gestionan múltiples explotaciones en distintas localidades, e inclusive poder consultar dicha información por Comarcas.

**📈 Evolución de productos internacionales**
Histórico de precios por categoría (cereales, aceites, ganadería…) con tendencias, variaciones y exportación de datos a Excel.

---

## Para quién es

### 🧑‍🌾 Productores individuales
Tienes acceso a la misma información que antes solo llegaba a grandes explotaciones o intermediarios. Sabes cuándo regar, cuándo tratar, si el precio que te ofrecen es justo y si el tiempo va a acompañar esta semana.

### 🏛️ Cooperativas y agrupaciones
Visión consolidada de todos los sectores: qué está al alza, qué está cayendo, dónde están las oportunidades de comercialización. Datos para negociar mejor y tomar decisiones de compra y venta con mayor información y mejor fundamento.

### 🏢 Administración pública e instituciones
Datos reales y actualizados sobre la salud del sector agrario regional. Útil para diseñar políticas de apoyo basadas en evidencia, no en estimaciones. Identificación inmediata de qué sectores necesitan intervención.

### 🔒 Empresas aseguradoras
Histórico fechado de eventos climáticos extremos por zona geográfica. Herramienta de valoración de riesgo con datos objetivos de temperatura, humedad y alertas registradas.

---

## Fundamentación

La digitalización del campo ya no es una opción futura: es una ventaja competitiva presente. Las explotaciones que toman decisiones con datos tienen menores costes operativos, mejores márgenes y mayor capacidad de adaptación ante un clima cada vez más impredecible.

Extremadura tiene una producción agraria de alto valor — aceite de oliva, corcho, pimentón, ganadería extensiva — pero históricamente ha competido con información limitada. Esta herramienta fue pensada, construida y desarrollada específicamente para potenciar sus cultivos y sus mercados agricolas.

## Definicion de Umbrales
Para obtener mas detalle de la definición y configuración de los umbrales, ver: https://github.com/mborrillo/agro-tech-es/blob/main/Interpretaci%C3%B3n%20de%20Umbrales%20AgroTech.md

---

## Vistas SQL del Modelo

## 1. Vista: `v_mapa_operaciones` — El Cerebro Operativo

**Objetivo:** Decidir cuándo actuar para no tirar el dinero.

**Fundamento:** Unir el clima con la energía. Tradicionalmente, un agricultor mira el cielo para regar o fumigar. Nosotros le obligamos a mirar también la factura de la luz.

### Explicación de Umbrales

- **Temperatura (10°C - 25°C):** Es el rango fisiológico óptimo. Por debajo de 10°C, la planta está "dormida" y no absorbe el tratamiento; por encima de 25°C-30°C, el producto se evapora antes de actuar o quema la hoja (fitotoxicidad).

- **Viento (< 15-20 km/h):** Evitamos la "deriva". Si hace viento, el producto químico termina en la parcela del vecino o en el arroyo, lo cual es dinero perdido y un riesgo medioambiental.

- **Energía (> 0.15 €/kWh):** Hemos fijado este umbral porque, en los regadíos de Extremadura, bombear agua por encima de este precio suele comerse más del 40% del margen neto de la campaña.

## 2. Vista: `v_alertas_energia` — El Vigía de Costes

**Objetivo:** Traducir un número abstracto (€/kWh) en una acción empresarial (Alto/Medio/Bajo).

**Fundamento:** El precio de la energía es volátil. El agricultor no tiene tiempo de mirar la gráfica del pool eléctrico cada hora. Esta vista hace el trabajo sucio por él.

**Por qué estos umbrales:** Usamos la consistencia. Si el Mapa dice que es caro regar a 0.15 €, la Alerta debe decir lo mismo. El éxito de la herramienta es que el sistema no se contradiga.

## 3. Vista: `v_comparativa_mercados` — El Escudo Comercial

**Objetivo:** Darle al agricultor "poder de negociación".

**Fundamento:** El concepto de Arbitraje. Si el precio en la Lonja de Extremadura está a 0.20 € pero en el mercado internacional (Chicago/París) está subiendo a 0.25 €, el agricultor sabe que no debe vender todavía.

**Umbrales:** Aquí el umbral es el **Diferencial**. Visualizar barras rojas (precio local por debajo del internacional) alerta al usuario de que está perdiendo dinero por una mala comercialización, no por una mala cosecha.

## 4. Vista: `v_salud_sectores` — El Termómetro del Mercado

**Objetivo:** Diagnóstico rápido del sector (¿Cómo va el Olivar? ¿Cómo va el Ovino?).

**Fundamento:** Agregación estadística. En lugar de mirar 50 productos, miramos la "salud" del sector.

**Lógica:** Si más del 60% de los productos de un sector bajan de precio, el sector está en **Alerta Roja**. Es una señal para que las cooperativas busquen ayudas o cambien estrategia de almacenamiento.

---

## 5. Vista: `v_resumen_energia` — El Panel de Decisión Energética

**Objetivo:** Traducir el precio de la electricidad en una acción concreta y medible en euros.

**Fundamento:** El PVPC varía cada hora pero el agricultor no puede monitorizarlo constantemente. Esta vista agrega las 24 horas del día en un único registro diario con los indicadores que realmente importan: cuándo es más barato encender la bomba, cuánto más caro es el pico de tarde, y si hoy es mejor o peor que ayer.

**Estructura de datos clave:**
- `precio_medio` / `precio_min` / `precio_max` — estadística básica del día
- `hora_min` / `hora_max` — hora exacta del valle y la punta
- `tramo_mayoria` — tramo predominante del día (Valle / Llano / Punta)
- `var_per_prev` — variación porcentual vs el día anterior (se calcula en el ETL)
- `estado_costo` — clasificación ALTO / NORMAL / BAJO según umbrales (>0.15€ / <0.10€)
- `recomendacion_consumo` — texto accionable generado automáticamente por la lógica de la vista

**Por qué `datos_energias` y no `datos_energia`:** El modelo anterior almacenaba 24 filas por día (una por hora), lo que impedía calcular comparativas diarias de forma limpia. La nueva tabla guarda 1 registro/día con los analytics ya calculados, lo que simplifica todas las consultas y permite escalar el histórico sin degradar la performance.

---

## Estado actual

## Estado actual

- ✅ Dashboard operativo con datos reales de Supabase: [agro-tech.streamlit.app](https://agro-tech.streamlit.app/)
- ✅ Ingesta automática diaria: clima (AEMET), mercados (Yahoo Finance), energía (REE)
- ✅ Secciones activas: Dashboard, Mapa de Operaciones, Monitor de Mercados, Monitor de Productos, Monitor de Energía, Alertas (En construcción)
- ✅ Monitor de Energía: panel de decisión diaria, calculadora de ahorro y histórico PVPC
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
- Informar y difundir un proyecto que aporta valor a todo un Ecosistema Productivo.
- Probar la herramienta en su propia explotación sin compromiso.

¿Te interesa optimizar tu próxima campaña?

*Para inversión o integración institucional, contactarse via web:*
https://marcos-borrillo.lovable.app
Wsp: https://wa.link/vvzmot
---

`#AgriculturaDigital` `#SmartFarming` `#Extremadura` `#AgroTech` `#Innovación` `#Sostenibilidad` `#DataDriven` `#CampoExtremeño` `#Cooperativas` `#AgTech` `#OpenData` `#Python` `#Supabase` `#AEMET` `#MercadoAgrícola` `#EficienciaEnergética` `#DigitalizaciónRural` `#StartupAgraria`
