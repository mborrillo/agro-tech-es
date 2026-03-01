# ══════════════════════════════════════════════════════════════════
# ARCHIVO: energia_monitor.py
# PROYECTO: Monitor Campo Extremadura — Ingesta de Energía
# PLATAFORMA: Script ETL · ejecutado via GitHub Actions
# FUENTE: Red Eléctrica de España (REE) — precio PVPC
# DESTINO: Supabase → tabla datos_energia
# REPO: https://github.com/mborrillo/agro-tech-es
# ══════════════════════════════════════════════════════════════════

import requests
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
    print("⚡ Consultando Precios de Energía (REE) con Analítica y Limpieza...")
    
    ahora = datetime.now()
    fecha_hoy = ahora.strftime("%Y-%m-%d")
    es_fin_de_semana = ahora.weekday() >= 5
    
    url = f"https://api.esios.ree.es/archives/70/download_json?locale=es&date={fecha_hoy}"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"⚠️ Error API REE: {response.status_code}")
            return

        datos = response.json()
        dict_limpio = {} # Usamos un diccionario para asegurar que cada hora sea única
        
        # Paso 1: Recolectar y limpiar (si la hora ya existe, se sobrescribe con el último valor)
        for hora_dato in datos.get('PVPC', []):
            precio_kwh = float(hora_dato['PCB'].replace(',', '.')) / 1000
            hora_int = int(hora_dato['Dia'].split('-')[0]) if '-' in hora_dato['Dia'] else 0
            
            # Esto elimina el error 21000: solo queda un registro por hora
            dict_limpio[hora_int] = precio_kwh

        if not dict_limpio:
            print("⚠ No se encontraron datos de PVPC.")
            return

        # Paso 2: Calcular la media con datos únicos
        precios_unicos = list(dict_limpio.values())
        media_dia = sum(precios_unicos) / len(precios_unicos)

        # Paso 3: Preparar registros finales
        registros_finales = []
        for hora_int, precio in dict_limpio.items():
            vs_media = ((precio - media_dia) / media_dia) * 100
            tramo = obtener_tramo(hora_int, es_fin_de_semana)
            
            registros_finales.append({
                "fecha": fecha_hoy,
                "hora": hora_int,
                "precio_kwh": round(precio, 5),
                "tramo": tramo,
                "vs_media": round(vs_media, 2)
            })

        # Paso 4: Guardar en Supabase
        if registros_finales:
            supabase.table("datos_energia").upsert(
                registros_finales, 
                on_conflict="fecha, hora"
            ).execute()
            print(f"✅ ¡Éxito! Datos limpios y guardados. (Media: {round(media_dia, 4)} €/kWh).")

    except Exception as e:
        print(f"❌ Error en monitor de energía: {e}")

if __name__ == "__main__":
    obtener_precios_luz()
