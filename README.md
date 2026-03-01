# 🚜 AgroTech : Inteligencia de Mercados Agrarios

AgroTech Extremadura es una plataforma de inteligencia de datos diseñada para transformar la toma de decisiones en el sector agropecuario. No es solo un panel de control; es un puente entre la realidad productiva de las parcelas extremeñas y los movimientos de los mercados globales.

## 💡 ¿Qué es y por qué existe esta herramienta?
En el modelo agrícola tradicional, el productor suele estar desconectado de los precios de Chicago o de la evolución horaria del mercado energético. AgroTech Extremadura democratiza el acceso a la información compleja, traduciéndola en acciones concretas.

El Diferencial: ¿Qué la hace única?
A diferencia de otras apps de clima, aquí vinculamos:

Clima Local Real: Datos directos de estaciones de la AEMET (Badajoz, Cáceres, Mérida, entre otras).

Arbitraje de Mercados: Compara el precio de la Lonja local con los futuros internacionales de Chicago, permitiendo detectar cuándo el precio local está infravalorado, o por encima del precio internacional.

Eficiencia Energética: Cruza el precio de la luz (PVPC) con la actividad de riego, consiguiendo optimizar costos.

¿Para quién es?
Productores Individuales: Optimización de riego y tratamientos.

Gerentes de Cooperativas: Visión estratégica para la comercialización de cosechas.

Empresas de Seguros Agrarios: Monitorización de riesgos climáticos extremos.

## 🏛️ Arquitectura de Datos (Supabase SQL)
El cerebro de la herramienta reside en una base de datos PostgreSQL, estructurada para ser escalable y rápida.

- Tablas (Donde guardamos los datos brutos)

| Tabla                | Qúe es/Para que sirve                       | Utilidad / Fundamento                             |
|----------------------|---------------------------------------------|---------------------------------------------------|
| datos_clima          | Registro de variables meteorológicas       | Histórico para predecir anomalías en las campañas|
| precios_agricolas    | Base de datos de la Lonja de Extremadura   | Valor real al que cierran las operaciones locales|
| mercados_internacionales | Datos de futuros (Chicago/NY) | Permite ver la tendencia global antes que llegue a Extremadura|
| datos_energia | Precios de la electricidad por hora | Fundamental para el cálculo de márgenes de beneficio en regadío |
|correlaciones_agro | El Corazón: Mapeo de productos | Vincula productos locales (ej. Cordero) con mercados de referencia (ej. Ganado Vivo |

- Vistas SQL (La Inteligencia del Sistema)

| Vista                | Para que sirve |
|----------------------|----------------|
| v_asesor_operaciones | Traduce el viento y la lluvia en un semáforo de "Apto/No Apto" para pulverizar o regar |
| v_comparativa_mercados | Realiza el cálculo de arbitraje (diferencia de precio local vs internacional) convertido a €/kg |
| v_salud_sectores| Agrupa los productos para decir si el sector (Cereales, Aceites, etc.) está en expansión o contracción |
| v_alertas_clima_extrema | Filtra automáticamente temperaturas críticas para prevenir heladas o golpes de calor |

## ⚙️ Estructura del Software (Python)
Los scripts actúan como "mayordomos digitales" que trabajan 24/7 de forma automatizada mediante GitHub Actions.

- clima_monitor.py: Conecta con la API de AEMET. Su lógica "blinda" el sistema contra fallos de conexión, asegurando que siempre tengamos el clima de localidades como Badajoz, Cáceres, Mérida (y varias mas), actualizado.

- mercado_monitor.py: Extrae datos de Yahoo Finance. Realiza una limpieza de "anomalías" para evitar que un error de valores en el mercado internacional altere o "ensucie" los informes.

- energia_monitor.py: Consulta el precio de la luz en tiempo real. Es el motor detrás del ahorro en los costos de riego.

- monitor_agrotech_v1.py: El orquestador que sincroniza la Lonja local con el resto de los parámetros internacionales.

## 📚 Glosario para el Productor
Para entender esta herramienta, usamos conceptos que ya conoces, pero con un toque tecnológico:

- Arbitraje: Es la diferencia de precio entre dos mercados. Si el Trigo en Chicago sube pero en Extremadura se mantiene, hay una oportunidad de negociación.

- Proxy Market (Mercado de Referencia): Cuando un producto no cotiza en bolsa (como el Aceite de Oliva), usamos uno similar (Aceite de Soja) para entender hacia dónde va el viento del mercado.

- ETL (Extraer, Transformar, Limpiar): Es lo que hacen nuestros scripts: recogen datos sin procesar de la web (sucios) y los entregan limpios, listos para ser analizados.

- Regadío Inteligente: Decidir no regar hoy porque la luz está cara y mañana se prevée lluvia, según la estación local de referencia, es una información de valor agregado para el productor.

NOTA: 
El sistema se actualiza automáticamente cada mañana.

## 🏷️ Hashtags & Referencias
#Extremadura #SmartFarming #BigData #Agricultura40 #OpenData #Python #Supabase #PostgreSQL #AEMET #MercadoDeFuturos #LonjaExtremadura #InnovacionRural
