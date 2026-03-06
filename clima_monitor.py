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

# DICCIONARIO DE GEOPOSICIÓN
ESTACIONES_EXTREMADURA = {
    "4478X": {"nombre": "BADAJOZ", "lat": 38.882, "lon": -6.845, "altitud": 174},
    "3469A": {"nombre": "CÁCERES", "lat": 39.482, "lon": -6.340, "altitud": 394},
    "4410X": {"nombre": "MÉRIDA", "lat": 38.922, "lon": -6.350, "altitud": 228},
    "4436Y": {"nombre": "ALMENDRALEJO", "lat": 38.681, "lon": -6.408, "altitud": 371},
    "4358X": {"nombre": "DON BENITO", "lat": 38.946, "lon": -5.845, "altitud": 273},
    "4486X": {"nombre": "OLIVENZA", "lat": 38.685, "lon": -7.098, "altitud": 275},
    "4427X": {"nombre": "ZAFRA", "lat": 38.423, "lon": -6.405, "altitud": 433},
    "3504X": {"nombre": "HERVÁS", "lat": 40.274, "lon": -5.861, "altitud": 724},
    "3519X": {"nombre": "PLASENCIA", "lat": 40.034, "lon": -6.075, "altitud": 415},
    "3434X": {"nombre": "NAVALMORAL DE LA MATA", "lat": 39.889, "lon": -5.541, "altitud": 269},
    "4386B": {"nombre": "LLERENA", "lat": 38.238, "lon": -6.012, "altitud": 655},
    "4411C": {"nombre": "ALCUESCAR", "lat": 39.181, "lon": -6.230, "altitud": 467},
    "3463Y": {"nombre": "TRUJILLO", "lat": 39.462, "lon": -5.877, "altitud": 523},
    "4511C": {"nombre": "JEREZ DE LOS CABALLEROS", "lat": 38.324, "lon": -6.772, "altitud": 381},
    "4501X": {"nombre": "FUENTE DE CANTOS", "lat": 38.243, "lon": -6.311, "altitud": 602},
    "4499X": {"nombre": "MONESTERIO", "lat": 38.087, "lon": -6.273, "altitud": 771},
    "3576X": {"nombre": "VALENCIA DE ALCÁNTARA", "lat": 39.412, "lon": -7.243, "altitud": 444},
    "4244X": {"nombre": "HERRERA DEL DUQUE", "lat": 39.167, "lon": -5.048, "altitud": 447},
    "4520X": {"nombre": "FREGENAL DE LA SIERRA", "lat": 38.169, "lon": -6.654, "altitud": 586},
    "4468X": {"nombre": "PUEBLA DE OBANDO", "lat": 39.176, "lon": -6.632, "altitud": 392},
    "4395X": {"nombre": "VILLAFRANCA DE LOS BARROS", "lat": 38.563, "lon": -6.335, "altitud": 430},
    "4362X": {"nombre": "RETAMAL DE LLERENA", "lat": 38.577, "lon": -5.836, "altitud": 474},
    "3562X": {"nombre": "ALISEDA", "lat": 39.421, "lon": -6.691, "altitud": 321},
    "3475X": {"nombre": "CAÑAVERAL", "lat": 39.790, "lon": -6.391, "altitud": 373},
    "3436D": {"nombre": "GARGANTA LA OLLA", "lat": 40.111, "lon": -5.773, "altitud": 690},
    "3455X": {"nombre": "JARAICEJO", "lat": 39.667, "lon": -5.811, "altitud": 559},
    "4236Y": {"nombre": "PUERTO REY", "lat": 39.423, "lon": -5.025, "altitud": 689},
    "4492F": {"nombre": "BARCARROTA", "lat": 38.282, "lon": -6.5524, "altitud": 377},
    "4325Y": {"nombre": "CASTUERA", "lat": 38.443, "lon": -5.3145, "altitud": 459},
    "3531X": {"nombre": "TORRECILLA DE LOS ANGELES", "lat": 40.245, "lon": -6.467, "altitud": 459},
    "4452X": {"nombre": "ALCONCHEL", "lat": 38.800, "lon": -7.000, "altitud": 170},
    "3484X": {"nombre": "AZUAGA", "lat": 38.367, "lon": -5.800, "altitud": 581},
    "3525X": {"nombre": "BROZAS", "lat": 39.600, "lon": -5.700, "altitud": 425},
    "3489X": {"nombre": "CAÑAMERO", "lat": 39.700, "lon": -5.600, "altitud": 590},
    "3550X": {"nombre": "CORIA", "lat": 40.000, "lon": -6.400, "altitud": 313},
    "3540X": {"nombre": "GARGANTA DE TORRECILLA", "lat": 40.200, "lon": -6.500, "altitud": 690},
    "3580X": {"nombre": "GUADALUPE", "lat": 39.700, "lon": -5.600, "altitud": 660},
    "3570X": {"nombre": "GUIJO DE GRANADILLA", "lat": 39.500, "lon": -6.000, "altitud": 393},
    "3520X": {"nombre": "HOYOS", "lat": 40.000, "lon": -5.700, "altitud": 560},
    "3560X": {"nombre": "JARAICEJO", "lat": 39.667, "lon": -5.811, "altitud": 559},
    "3590X": {"nombre": "MADRIAGAL DE LA VERA", "lat": 40.000, "lon": -5.800, "altitud": 464},
    "3510X": {"nombre": "MONTEHERMOSO", "lat": 39.300, "lon": -6.500, "altitud": 351},
    "3530X": {"nombre": "NAVALVILLAR DE IBO", "lat": 39.700, "lon": -5.600, "altitud": 923},
    "3545X": {"nombre": "NAVALVILLAR DE PELA", "lat": 39.700, "lon": -5.600, "altitud": 313},
    "3515X": {"nombre": "NUÑOMORAL", "lat": 40.000, "lon": -5.700, "altitud": 470},
    "3585X": {"nombre": "PERALEDAD DEL ZAUCHEJO", "lat": 38.600, "lon": -6.700, "altitud": 542},
    "3595X": {"nombre": "PIORNAL", "lat": 40.000, "lon": -5.800, "altitud": 1260},
    "3505X": {"nombre": "SANTA MARTA DE LOS BARROS", "lat": 38.600, "lon": -6.300, "altitud": 345},
    "3522X": {"nombre": "SERRADILLA", "lat": 39.600, "lon": -5.700, "altitud": 406},
    "3535X": {"nombre": "TORNACAUCAS", "lat": 40.000, "lon": -5.700, "altitud": 991},
    "3575X": {"nombre": "VALVERDE DE FRENSO", "lat": 39.700, "lon": -5.600, "altitud": 450},
    "3555X": {"nombre": "VILLANUEVA DEL FRENSO", "lat": 38.500, "lon": -6.800, "altitud": 247},
    "4490X": {"nombre": "ZARZA LA MAYOR", "lat": 38.600, "lon": -6.700, "altitud": 336}
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
    
    ciudades = {"BADAJOZ": "4478X", "CÁCERES": "3469A", "MÉRIDA": "4410X", "ALMENDRALEJO": "4436Y", "DON BENITO": "4358X", "OLIVENZA": "4486X", "ZAFRA": "4427X","HERVÁS":"3504X","PLASENCIA":"3519X","NAVALMORAL DE LA MATA":"3434X","LLERENA":"4386B","ALCUESCAR":"4411C","TRUJILLO - Espáña":"3463Y", 
                "JEREZ DE LOS CABALLEROS":"4511C", "FUENTE DE CANTOS":"4501X", "MONESTERIO":"4499X", "VALENCIA DE ALCÁNTARA":"3576X","HERRERA DEL DUQUE":"4244X","FREGENAL DE LA SIERRA":"4520X","PUEBLA DE OBANDO":"4468X","VILLAFRANCA DE LOS BARROS":"4395X","RETAMAL DE LLERENA":"4362X",
                "ALISEDA":"3562X","CAÑAVERAL-España":"3475X","GARGANTA LA OLLA":"3436D","JARAICEJO":"3455X","PUERTO REY":"4236Y","TORRECILLA DE LOS ANGELES":"3531X"}
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    for ciudad, id_estacion in ciudades.items():
        url_aemet = f"https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/{id_estacion}"
        params = {"api_key": AEMET_API_KEY}

        try:
            r = requests.get(url_aemet, params=params)
            if r.status_code == 200:
                datos_url = r.json().get('datos')
                resp_datos = requests.get(datos_url)
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
