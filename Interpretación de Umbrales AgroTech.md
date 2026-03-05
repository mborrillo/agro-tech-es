# 📘 Manual de Interpretación de Umbrales: AgroTech Extremadura

Este manual explica la lógica detrás de cada recomendación emitida por el sistema. Nuestros umbrales no son arbitrarios; son el resultado de cruzar la agronomía de precisión con la optimización financiera.

---

## 1. Gestión de Energía (El Umbral del Beneficio)

El coste de la luz es el principal "ladrón" del margen neto en el regadío.

| Umbral (€/kWh) | Categoría | Acción del Modelo | Justificación Técnica |
| :--- | :--- | :--- | :--- |
| **< 0.10** | **BARATA (VALLE)** | **RIEGO RECOMENDADO** | Maximiza el margen. Es el momento de llenar depósitos o regar sectores de alta demanda. |
| **0.10 - 0.15** | **NORMAL** | **RIEGO DISCRECIONAL** | Coste asumible. Se permite el riego si la necesidad hídrica del cultivo es urgente. |
| **> 0.15** | **CARA (PICO)** | **POSPONER RIEGO** | El coste de bombeo por m³ reduce el beneficio operativo un 30-50%. Evitar salvo emergencia. |

> **Nota:** En Extremadura, con temperaturas estivales altas, regar en horas de luz cara no solo es costoso, sino ineficiente por la evapotranspiración.

---

## 2. Tratamientos Fitosanitarios (La Regla de la Eficacia)

Fumigar fuera de estos umbrales es, literalmente, tirar producto al suelo o al aire.

*   **Temperatura (10°C - 25°C):**
    *   **Por debajo de 10°C:** La planta cierra sus estomas o ralentiza su metabolismo. El producto no se absorbe y se lava con el rocío.
    *   **Por encima de 28-30°C:** El producto se evapora antes de tocar la hoja o, peor aún, puede causar quemaduras (fitotoxicidad) al reaccionar con el calor.
*   **Viento (< 15 km/h):**
    *   Es el límite legal y técnico para evitar la deriva. Por encima de 20 km/h, el 40% del tratamiento no llega al objetivo, contaminando parcelas colindantes y perdiendo dinero.
*   **Humedad (> 50%):**
    *   Una humedad baja reseca la gota demasiado rápido. Mantener el umbral > 50% asegura que el producto permanezca en estado líquido el tiempo suficiente para ser absorbido.

---

## 3. Arbitraje de Mercados (El Umbral de Negociación)

¿Vender ahora o esperar? Usamos el **Diferencial de Arbitraje**.

$$Diferencial = Precio_{Internacional} - Precio_{Local}$$

*   **Diferencial Positivo (> 5%):** Indica que el mercado global está pagando más que tu comprador local. **Recomendación:** Retener stock o buscar exportación.
*   **Diferencial Neutro (± 2%):** El mercado está equilibrado. **Recomendación:** Venta normal según necesidad de liquidez.
*   **Diferencial Negativo:** Alerta de posible saturación local o falta de compradores.

---

## 4. Salud del Sector (Indicador Semafórico)

Calculamos la "Salud" basándonos en la tendencia semanal del top 5 de productos de cada sector (Oliva, Cereal, Ganado).

*   🟢 **ÓPTIMO:** Más del 80% de los productos mantienen o suben precio.
*   🟡 **ATENCIÓN:** Volatilidad detectada. El 50% de los productos muestran tendencia a la baja.
*   🔴 **ALERTA:** Caída generalizada. Momento de activar coberturas o buscar ayudas sectoriales.

---

## ¿Por qué confiar en estos números?

A diferencia de un asesor tradicional que usa la "intuición", AgroTech utiliza datos en tiempo real de la AEMET, REE (Red Eléctrica Española) y Lonjas de Referencia. El sistema revisa estos umbrales cada 60 minutos, adaptándose a la volatilidad del día a día.