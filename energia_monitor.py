# ══════════════════════════════════════════════════════════════════
# ARCHIVO: energia_monitor.py
# PROYECTO: Monitor Campo Extremadura — Ingesta de Energía
# PLATAFORMA: Script ETL · ejecutado via GitHub Actions (1x día)
# FUENTE: Red Eléctrica de España (REE) — precio PVPC
# DESTINO: Supabase → tabla datos_energia
# REPO: https://github.com/mborrillo/agro-tech-es
#
# LÓGICA: La API de REE publica las 24 horas del día de una sola vez.
# Guardamos 1 registro diario con analítica real extraída de esas 24h:
#   - precio_medio   → media del día completo
#   - precio_min     → precio más bajo del día
#   - hora_min       → hora a la que se produce el precio mínimo
#   - precio_max     → precio más alto del día
#   - hora_max       → hora a la que se produce el precio máximo
#   - tramo_mayoria  → tramo predominante del día (Valle/Llano/Punta)
#   - var_per_prev   → variación % respecto al período anterior
# ══════════════════════════════════════════════════════════════════

import os
import requests
from supabase import create_client, Client
from datetime import datetime, timedelta
from collections import Counter

# --- CONFIGURACIÓN ---
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://zzucvsremavkikecsptg.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Inicialización robusta para GitHub Actions y Service Role
supabase: Client = create_client(
    SUPABASE_URL, 
    SUPABASE_KEY,
    options=ClientOptions(
        postgrest_client_timeout=20,
        storage_client_timeout=20,
        persist_session=False
    )
)

def obtener_tramo(hora, es_fin_de_semana):
    if es_fin_de_semana:
        return "Valle"
    if 0 <= hora < 8:
        return "Valle"
    elif hora in [10, 11, 12, 13, 18, 19, 20, 21]:
        return "Punta"
    else:
        return "Llano"

def obtener_precios_luz():
    print("⚡ Consultando Precios de Energía (REE)...")

    ahora = datetime.now()
    fecha_hoy = ahora.strftime("%Y-%m-%d")
    fecha_ayer = (ahora - timedelta(days=1)).strftime("%Y-%m-%d")
    es_fin_de_semana = ahora.weekday() >= 5

    url = f"https://api.esios.ree.es/archives/70/download_json?locale=es&date={fecha_hoy}"

    try:
        # Paso 1: Obtener precio_medio del período anterior para var_per_prev
        precio_medio_anterior = None
        try:
            r_ant = supabase.table("datos_energias") \
                .select("precio_medio") \
                .eq("fecha", fecha_ayer) \
                .execute()
            if r_ant.data:
                precio_medio_anterior = r_ant.data[0]["precio_medio"]
                print(f"📅 Período anterior ({fecha_ayer}): {round(precio_medio_anterior, 4)} €/kWh")
            else:
                print(f"⚠️  Sin datos del período anterior ({fecha_ayer}) — var_per_prev quedará null")
        except Exception as e:
            print(f"⚠️  No se pudo obtener período anterior: {e}")

        # Paso 2: Llamar a la API de REE
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            print(f"⚠️  Error API REE: {response.status_code}")
            return

        datos = response.json()
        pvpc = datos.get("PVPC", [])

        if not pvpc:
            print("⚠️  No se encontraron datos PVPC.")
            return

        # Paso 3: Parsear las 24 horas
        # enumerate() en lugar de campo 'Dia' — ESIOS cambió su formato en Feb 2026
        horas = {}
        for hora_int, hora_dato in enumerate(pvpc):
            try:
                precio = float(hora_dato["PCB"].replace(",", ".")) / 1000
            except (KeyError, ValueError):
                try:
                    precio = float(hora_dato["TCHA"].replace(",", ".")) / 1000
                except (KeyError, ValueError):
                    continue
            horas[hora_int] = precio

        if not horas:
            print("⚠️  No se pudieron parsear precios.")
            return

        print(f"📋 {len(horas)} horas recibidas de REE")

        # Paso 4: Calcular analítica del día
        precios = list(horas.values())
        precio_medio = sum(precios) / len(precios)

        hora_min = min(horas, key=horas.get)
        hora_max = max(horas, key=horas.get)
        precio_min = horas[hora_min]
        precio_max = horas[hora_max]

        tramos = [obtener_tramo(h, es_fin_de_semana) for h in horas]
        tramo_mayoria = Counter(tramos).most_common(1)[0][0]

        # Paso 5: Calcular variación vs período anterior
        if precio_medio_anterior:
            var_per_prev = round(((precio_medio - precio_medio_anterior) / precio_medio_anterior) * 100, 2)
            signo = "+" if var_per_prev > 0 else ""
            print(f"📊 Media hoy: {round(precio_medio, 4)} €/kWh  |  var_per_prev: {signo}{var_per_prev}%")
        else:
            var_per_prev = None
            print(f"📊 Media hoy: {round(precio_medio, 4)} €/kWh  |  var_per_prev: sin referencia")

        print(f"🔋 Hora más barata: {hora_min}h ({round(precio_min, 4)} €/kWh)  |  Hora más cara: {hora_max}h ({round(precio_max, 4)} €/kWh)")
        print(f"⚡ Tramo predominante: {tramo_mayoria}")

        # Paso 6: Guardar 1 registro diario en Supabase
        registro = {
            "fecha":          fecha_hoy,
            "precio_medio":   round(precio_medio, 5),
            "precio_min":     round(precio_min, 5),
            "hora_min":       hora_min,
            "precio_max":     round(precio_max, 5),
            "hora_max":       hora_max,
            "tramo_mayoria":  tramo_mayoria,
            "var_per_prev":   var_per_prev,
        }

        supabase.table("datos_energias").upsert(
            registro,
            on_conflict="fecha"
        ).execute()

        print(f"✅ ¡Éxito! Registro del {fecha_hoy} guardado.")

    except Exception as e:
        print(f"❌ Error en monitor de energía: {e}")

if __name__ == "__main__":
    obtener_precios_luz()
