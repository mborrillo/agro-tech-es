# 🌿 AgroTech ES — Resumen Ejecutivo

> **"El campo extremeño produce con esfuerzo. Nosotros le damos la información para que ese esfuerzo rinda más."**

---

## Qué es AgroTech ES

AgroTech ES es una plataforma digital de monitorización y análisis para el sector agrícola de Extremadura. En una sola pantalla, el productor ve el estado de sus parcelas, el precio al que cotiza su cosecha en los mercados globales, cuánto cuesta regar en este momento y si hay riesgo climático en las próximas horas.

No es una app de previsión del tiempo. No es una hoja de cálculo de precios. Es la combinación de ambas cosas — y más — conectada a datos reales y actualizada automáticamente cada día.

**Disponible en:** [agro-tech.streamlit.app](https://agro-tech.streamlit.app)

---

## El problema que resuelve

Un agricultor de Badajoz sabe lo que vale su aceituna en la lonja local. Lo que no sabe — porque nunca tuvo acceso fácil a esa información — es si ese precio está por encima o por debajo de lo que marca el mercado internacional de referencia en ese mismo momento. Tampoco sabe si el precio de la luz esta tarde hace rentable encender el sistema de riego, o si es mejor esperar a la madrugada.

Esa brecha de información tiene un coste real: en márgenes de negociación perdidos, en agua y energía gastadas en el momento equivocado, en cosechas afectadas por heladas que los datos ya anticipaban.

**AgroTech ES cierra esa brecha.**

---

## Lo que hace, en concreto

**🌡️ Monitorización climática por estación**
Temperatura, humedad, viento y precipitación en tiempo real desde estaciones de la AEMET en Badajoz, Cáceres, Mérida y otras localidades de la región. Con alertas automáticas por condiciones extremas: heladas, golpes de calor, viento fuerte que impide tratamientos fitosanitarios.

**📊 Comparativa de mercados: local vs. global**
El precio de la Lonja de Extremadura comparado directamente con los futuros internacionales de Chicago y Londres, convertidos a la misma unidad (€/kg). Si el trigo local está infravalorado respecto al mercado global, el sistema lo muestra en verde. Si el productor está vendiendo por encima del precio de referencia, también lo sabe.

**⚡ Gestión del coste energético**
El sistema cruza el precio de la electricidad (PVPC, actualizado por hora) con las condiciones meteorológicas. El resultado: una recomendación concreta sobre cuándo regar para minimizar el gasto en energía.

**🗺️ Mapa de operaciones**
Vista geográfica de todas las estaciones activas, con semáforo de estado (Óptimo / Precaución / Crítico) según las condiciones actuales de tratamiento y riego. Útil para cooperativas que gestionan múltiples explotaciones.

**📈 Evolución de productos internacionales**
Histórico de precios por categoría (cereales, aceites, ganadería…) con tendencias, variaciones y exportación de datos a Excel.

---

## Para quién es

### 🧑‍🌾 Productores individuales
Tienes acceso a la misma información que antes solo llegaba a grandes explotaciones o intermediarios. Sabes cuándo regar, cuándo tratar, si el precio que te ofrecen es justo y si el tiempo va a acompañar esta semana.

### 🏛️ Cooperativas y agrupaciones
Visión consolidada de todos los sectores: qué está al alza, qué está cayendo, dónde están las oportunidades de comercialización. Datos para negociar mejor y tomar decisiones de compra y venta con fundamento.

### 🏢 Administración pública e instituciones
Datos reales y actualizados sobre la salud del sector agrario regional. Útil para diseñar políticas de apoyo basadas en evidencia, no en estimaciones. Identificación inmediata de qué sectores necesitan intervención.

### 🔒 Empresas aseguradoras
Histórico fechado de eventos climáticos extremos por zona geográfica. Herramienta de valoración de riesgo con datos objetivos de temperatura, humedad y alertas registradas.

---

## Por qué ahora

La digitalización del campo ya no es una opción futura: es una ventaja competitiva presente. Las explotaciones que toman decisiones con datos tienen menores costes operativos, mejores márgenes y mayor capacidad de adaptación ante un clima cada vez más impredecible.

Extremadura tiene una producción agraria de alto valor — aceite de oliva, corcho, pimentón, ganadería extensiva — pero históricamente ha competido con información limitada. AgroTech ES cambia eso, con una herramienta construida específicamente para esta región, sus cultivos y sus mercados de referencia.

---

## Estado actual

- ✅ Dashboard operativo con datos reales de Supabase
- ✅ Ingesta automática diaria: clima (AEMET), mercados (Yahoo Finance), energía (REE)
- ✅ Seis secciones activas: Dashboard, Mapa de Operaciones, Monitor de Mercados, Monitor de Productos, Alertas, Configuración
- ✅ Exportación de datos a Excel
- 🔄 En desarrollo: frontend complementario en [agro-tech-es.lovable.app](https://agro-tech-es.lovable.app)
- 🔄 Próximo: autenticación por roles, notificaciones push, API abierta para terceros

---

## Tecnología

Construido sobre Python, Streamlit, Supabase (PostgreSQL) y GitHub Actions. Código abierto bajo licencia MIT. Diseñado para escalar a otras regiones agrarias de España con mínimos ajustes.

🔗 Repositorio: [github.com/mborrillo/agro-tech-es](https://github.com/mborrillo/agro-tech-es)

---

*Para consultas de colaboración, inversión o integración institucional, contactar a través del repositorio.*

---

`#AgriculturaDigital` `#SmartFarming` `#Extremadura` `#AgroTech` `#Innovación` `#Sostenibilidad` `#DataDriven` `#CampoExtremeño` `#Cooperativas` `#AgTech` `#OpenData` `#Python` `#Supabase` `#AEMET` `#MercadoAgrícola` `#EficienciaEnergética` `#DigitalizaciónRural` `#StartupAgraria`
