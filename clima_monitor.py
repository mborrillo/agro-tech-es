# ══════════════════════════════════════════════════════════════════
# ARCHIVO: clima_monitor.py
# PROYECTO: Monitor Campo Extremadura — Ingesta de Datos Climáticos
# PLATAFORMA: Script ETL · ejecutado via GitHub Actions
# FUENTE: API AEMET (opendata.aemet.es)
# DESTINO: Supabase → tabla datos_clima
# REPO: https://github.com/mborrillo/agro-tech-es
# ══════════════════════════════════════════════════════════════════

import os
import requests
from supabase import create_client, Client
from datetime import datetime
import sys

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG" 
AEMET_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2OGJvcnJpc21hckBnbWFpbC5jb20iLCJqdGkiOiI1YzRjYzlkZC04OTI0LTQzZjgtOTI1OC1hZWZiZjRhOWIzNGMiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc3MTA4MjI3MSwidXNlcklkIjoiNWM0Y2M5ZGQtODkyNC00M2Y4LTkyNTgtYWVmYmY0YTliMzRjIiwicm9sZSI6IiJ9.EQqSYmGFYaCQvhzPv2gxYHkwa1Zyqr9sDLRCG8xLaV4"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# DICCIONARIO DE GEOPOSICIÓN — códigos AEMET oficiales verificados 06/03/2026
# Fuente: https://x-y.es/aemet/ca-extremadura (54 estaciones activas Extremadura)
ESTACIONES_EXTREMADURA = {
    # ── Estaciones originales (códigos correctos) ──────────────────────────
    "4478X": {"nombre": "BADAJOZ",                    "lat": 38.882, "lon": -6.845, "altitud": 174},
    "3469A": {"nombre": "CÁCERES",                    "lat": 39.482, "lon": -6.340, "altitud": 394},
    "4410X": {"nombre": "MÉRIDA",                     "lat": 38.922, "lon": -6.350, "altitud": 228},
    "4436Y": {"nombre": "ALMENDRALEJO",               "lat": 38.681, "lon": -6.408, "altitud": 371},
    "4358X": {"nombre": "DON BENITO",                 "lat": 38.946, "lon": -5.845, "altitud": 273},
    "4486X": {"nombre": "OLIVENZA",                   "lat": 38.685, "lon": -7.098, "altitud": 275},
    "4427X": {"nombre": "ZAFRA",                      "lat": 38.423, "lon": -6.405, "altitud": 433},
    "3504X": {"nombre": "HERVÁS",                     "lat": 40.274, "lon": -5.861, "altitud": 724},
    "3519X": {"nombre": "PLASENCIA",                  "lat": 40.034, "lon": -6.075, "altitud": 415},
    "3434X": {"nombre": "NAVALMORAL DE LA MATA",      "lat": 39.889, "lon": -5.541, "altitud": 269},
    "4386B": {"nombre": "LLERENA",                    "lat": 38.238, "lon": -6.012, "altitud": 655},
    "4411C": {"nombre": "ALCUESCAR",                  "lat": 39.181, "lon": -6.230, "altitud": 467},
    "3463Y": {"nombre": "TRUJILLO - Espáña",          "lat": 39.462, "lon": -5.877, "altitud": 523},
    "4511C": {"nombre": "JEREZ DE LOS CABALLEROS",    "lat": 38.324, "lon": -6.772, "altitud": 381},
    "4501X": {"nombre": "FUENTE DE CANTOS",           "lat": 38.243, "lon": -6.311, "altitud": 602},
    "4499X": {"nombre": "MONESTERIO",                 "lat": 38.087, "lon": -6.273, "altitud": 771},
    "3576X": {"nombre": "VALENCIA DE ALCÁNTARA",      "lat": 39.412, "lon": -7.243, "altitud": 444},
    "4244X": {"nombre": "HERRERA DEL DUQUE",          "lat": 39.167, "lon": -5.048, "altitud": 447},
    "4520X": {"nombre": "FREGENAL DE LA SIERRA",      "lat": 38.169, "lon": -6.654, "altitud": 586},
    "4468X": {"nombre": "PUEBLA DE OBANDO",           "lat": 39.176, "lon": -6.632, "altitud": 392},
    "4395X": {"nombre": "VILLAFRANCA DE LOS BARROS",  "lat": 38.563, "lon": -6.335, "altitud": 430},
    "4362X": {"nombre": "RETAMAL DE LLERENA",         "lat": 38.577, "lon": -5.836, "altitud": 474},
    "3562X": {"nombre": "ALISEDA",                    "lat": 39.421, "lon": -6.691, "altitud": 321},
    "3475X": {"nombre": "CAÑAVERAL-España",           "lat": 39.790, "lon": -6.391, "altitud": 373},
    "3436D": {"nombre": "GARGANTA LA OLLA",           "lat": 40.111, "lon": -5.773, "altitud": 690},
    "3455X": {"nombre": "JARAICEJO",                  "lat": 39.667, "lon": -5.811, "altitud": 559},
    "4236Y": {"nombre": "PUERTO REY",                 "lat": 39.423, "lon": -5.025, "altitud": 689},
    "4492F": {"nombre": "BARCARROTA",                 "lat": 38.282, "lon": -6.552, "altitud": 377},
    "4325Y": {"nombre": "CASTUERA",                   "lat": 38.443, "lon": -5.314, "altitud": 459},
    "3531X": {"nombre": "TORRECILLA DE LOS ANGELES",  "lat": 40.245, "lon": -6.467, "altitud": 459},
    # ── Estaciones nuevas — códigos y nombres AEMET oficiales verificados ──
    "4489X": {"nombre": "ALCONCHEL",                  "lat": 38.517, "lon": -7.052, "altitud": 170},
    "5473X": {"nombre": "AZUAGA",                     "lat": 38.259, "lon": -5.672, "altitud": 581},
    "3565X": {"nombre": "BROZAS",                     "lat": 39.617, "lon": -6.767, "altitud": 425},
    "4339X": {"nombre": "CAÑAMERO EL PINAR",          "lat": 39.397, "lon": -5.368, "altitud": 590},
    "3526X": {"nombre": "CORIA",                      "lat": 39.984, "lon": -6.535, "altitud": 313},
    "3540X": {"nombre": "ZARZA LA MAYOR",             "lat": 39.900, "lon": -6.650, "altitud": 336},
    "4245X": {"nombre": "GUADALUPE",                  "lat": 39.455, "lon": -5.330, "altitud": 660},
    "3503":  {"nombre": "GUIJO DE GRANADILLA",        "lat": 40.117, "lon": -6.233, "altitud": 393},
    "3536X": {"nombre": "HOYOS",                      "lat": 40.167, "lon": -6.717, "altitud": 560},
    "3423I": {"nombre": "MADRIGAL DE LA VERA",        "lat": 40.083, "lon": -5.467, "altitud": 464},
    "3512X": {"nombre": "MONTEHERMOSO",               "lat": 40.067, "lon": -6.350, "altitud": 351},
    "3386A": {"nombre": "NAVALVILLAR DE IBOR",        "lat": 39.633, "lon": -5.483, "altitud": 923},
    "4340":  {"nombre": "NAVALVILLAR DE PELA",        "lat": 39.083, "lon": -5.483, "altitud": 313},
    "3494U": {"nombre": "NUÑOMORAL",                  "lat": 40.233, "lon": -6.217, "altitud": 470},
    "4260":  {"nombre": "PERALEDA DEL ZAUCEJO",       "lat": 38.433, "lon": -5.517, "altitud": 542},
    "3516X": {"nombre": "PIORNAL",                    "lat": 40.100, "lon": -5.850, "altitud": 1260},
    "4442X": {"nombre": "SANTA MARTA DE LOS BARROS",  "lat": 38.533, "lon": -6.600, "altitud": 345},
    "3448X": {"nombre": "SERRADILLA",                 "lat": 39.833, "lon": -6.133, "altitud": 406},
    "3514B": {"nombre": "TORNAVACAS",                 "lat": 40.250, "lon": -5.717, "altitud": 991},
    "3547X": {"nombre": "VALVERDE DE FRESNO",         "lat": 40.250, "lon": -6.900, "altitud": 450},
    "4497X": {"nombre": "VILLANUEVA DEL FRESNO",      "lat": 38.383, "lon": -7.150, "altitud": 247},
    "4464X": {"nombre": "ALBURQUERQUE",               "lat": 39.217, "lon": -6.983, "altitud": 283},
    "4347X": {"nombre": "ZORITA",                     "lat": 39.300, "lon": -5.717, "altitud": 413},
}

def obtener_clima():
    # ... (tu lógica de llamada a la API de AEMET)
    
    registros_clima = []
    
    # Supongamos que 'dato' es el JSON que devuelve AEMET para una estación
    for dato in datos_aemet:
        id_estacion = dato.get('idema')
        
        if id_estacion in ESTACIONES_EXTREMADURA:
            info_geo = ESTACIONES_EXTREMADURA[id_estacion]
            
            registro = {
                "fecha": dato.get('fint'),
                "localidad": info_geo['nombre'],
                "latitud": info_geo['lat'],
                "longitud": info_geo['lon'],
                "temperatura": dato.get('ta'),
                "humedad": dato.get('hr'),
                "viento_velocidad": dato.get('vv'),
                "precipitacion": dato.get('prec')
            }
            registros_clima.append(registro)

    # GUARDADO EN SUPABASE
    supabase.table("datos_clima").upsert(registros_clima).execute()

def obtener_clima_inteligente():
    print(f"🌦️ Iniciando captura de clima inteligente: {datetime.now()}")
    
    # Construido dinámicamente desde ESTACIONES_EXTREMADURA — agregar estaciones solo ahí
    ciudades = {info["nombre"]: id_est for id_est, info in ESTACIONES_EXTREMADURA.items()}
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    for ciudad, id_estacion in ciudades.items():
        url_aemet = f"https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/{id_estacion}"
        params = {"api_key": AEMET_API_KEY}

        try:
            r = requests.get(url_aemet, params=params, timeout=15)
            if r.status_code == 200:
                datos_url = r.json().get('datos')
                if not datos_url:
                    print(f"⚠️  {ciudad}: AEMET no devolvió URL de datos (estación sin lecturas)")
                    continue
                resp_datos = requests.get(datos_url, timeout=15)
                if resp_datos.status_code != 200 or not resp_datos.text.strip():
                    print(f"⚠️  {ciudad}: respuesta vacía de AEMET")
                    continue
                lecturas = resp_datos.json()

                if lecturas:
                    # Filtramos solo las lecturas que pertenecen al día de hoy
                    lecturas_hoy = [l for l in lecturas if l.get('fint', '').startswith(fecha_hoy)]
                    
                    if not lecturas_hoy:
                        # Si es muy temprano, usamos la última lectura disponible para tener continuidad
                        lecturas_hoy = [lecturas[-1]]

                    # --- PROCESAMIENTO ANALÍTICO ---
                    temps = [l.get('ta') for l in lecturas_hoy if l.get('ta') is not None]
                    precips = [l.get('prec') for l in lecturas_hoy if l.get('prec') is not None]
                    
                    t_max = max(temps) if temps else None
                    t_min = min(temps) if temps else None
                    p_acumulada = sum(precips) if precips else 0
                    
                    ultima = lecturas_hoy[-1]
                    
                    # 🔧 FIX: Obtener coordenadas del diccionario de estaciones
                    info_estacion = ESTACIONES_EXTREMADURA.get(id_estacion, {})
                    lat = info_estacion.get('lat')
                    lon = info_estacion.get('lon')

                    registro = {
                        "fecha": fecha_hoy,
                        "estacion": ciudad,
                        "id_estacion": id_estacion,
                        "temp_max": t_max,
                        "temp_min": t_min,
                        "temp_actual": ultima.get('ta'),
                        "precipitacion": round(p_acumulada, 2),
                        "humedad": ultima.get('hr'),
                        "viento_vel": ultima.get('vv'),
                        "latitud": lat,
                        "longitud": lon
                    }

                    supabase.table("datos_clima").upsert(registro, on_conflict="fecha, estacion").execute()
                    print(f"✅ {ciudad}: Max {t_max}° / Min {t_min}° / Lluvia {round(p_acumulada, 2)}mm")
        
        except Exception as e:
            print(f"❌ Error procesando {ciudad}: {e}")

if __name__ == "__main__":
    obtener_clima_inteligente()
