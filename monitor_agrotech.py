# ══════════════════════════════════════════════════════════════════
# ARCHIVO: monitor_agrotech.py
# PROYECTO: Monitor Campo Extremadura — Orquestador / Lonja Local
# PLATAFORMA: Script ETL · ejecutado via GitHub Actions
# FUNCIÓN: Sincroniza precios de la Lonja de Extremadura con
#          los parámetros internacionales (correlaciones_agro)
# DESTINO: Supabase → tabla precios_agricolas
# REPO: https://github.com/mborrillo/agro-tech-es
# ══════════════════════════════════════════════════════════════════

import os
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURACIÓN ---
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_precios_locales():
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    print(f"🚜 Sincronizando Lonja: {fecha_hoy}")
    
    # 1. OBTENEMOS EL DICCIONARIO DE MAPEO DESDE SUPABASE
    # Esto elimina la necesidad de tener los nombres hardcodeados aquí
    res_mapeo = supabase.table("mapeo_productos").select("*").execute()
    mapeo = {item['producto_nombre_lonja']: item for item in res_mapeo.data}

    # 2. DATOS DE LA LONJA (Simulamos la captura de hoy)
    # En el futuro, aquí iría tu scraper o integración directa
    sectores_hoy = {
        "Aceites": [
            {"prod": "AOVE", "var": "Multivarietal", "min": 8.80, "max": 9.30, "uni": "€/kg"},
            {"prod": "Aceite Virgen", "var": "Estándar", "min": 8.20, "max": 8.60, "uni": "€/kg"}
        ],
        "Porcino": [
            {"prod": "Cerdos de Bellota (100% Ibérico)", "var": "Bellota", "min": 3.90, "max": 4.20, "uni": "€/kg"},
            {"prod": "Cebo de Campo", "var": "Ibérico", "min": 2.55, "max": 2.75, "uni": "€/kg"}
        ],
        "Cereales": [
            {"prod": "Trigo Duro", "var": "RGT Pelayo", "min": 0.29, "max": 0.31, "uni": "€/kg"},
            {"prod": "Maíz", "var": "Standard", "min": 0.23, "max": 0.25, "uni": "€/kg"}
        ],
        "Vacuno": [
            {"prod": "Ternero Pastero (200kg)", "var": "Cruzado", "min": 3.50, "max": 3.90, "uni": "€/kg"},
            {"prod": "Vaca de Desvieje", "var": "Industria", "min": 1.20, "max": 1.60, "uni": "€/kg"}
        ]
    }

    registros_finales = []

    for sector, productos in sectores_hoy.items():
        for p in productos:
            precio_med_hoy = (p["min"] + p["max"]) / 2
            # Código robusto para evitar errores de tildes o mayúsculas
            nombre_buscado = p["prod"].strip().lower()
            info_mapeo = next((v for k, v in mapeo.items() if k.strip().lower() == nombre_buscado), {})
            
            # Buscamos historial para calcular variación
            med_ant = None
            variacion = 0
            try:
                res_hist = supabase.table("precios_agricolas")\
                    .select("precio_min, precio_max")\
                    .eq("producto", p["prod"])\
                    .lt("fecha", fecha_hoy)\
                    .order("fecha", desc=True)\
                    .limit(1).execute()
                
                if res_hist.data:
                    ant = res_hist.data[0]
                    med_ant = (ant["precio_min"] + ant["precio_max"]) / 2
                    variacion = ((precio_med_hoy - med_ant) / med_ant) * 100
            except:
                pass

            registros_finales.append({
                "fecha": fecha_hoy,
                "sector": sector,
                "producto": p["prod"],
                "variedad": p["var"],
                "precio_min": p["min"],
                "precio_max": p["max"],
                "precio_anterior_med": round(med_ant, 4) if med_ant else None,
                "variacion_p": round(variacion, 2),
                "unidad": p["uni"],
                "lonja_id": 1, # ID de Extremadura
                "mapping_slug": info_mapeo.get("mapping_slug"), # Aquí se hace la magia
                "fuente": "Lonja de Extremadura"
            })

    # 3. UPSERT A LA BASE DE DATOS
    if registros_finales:
        try:
            supabase.table("precios_agricolas").upsert(
                registros_finales, on_conflict="fecha, producto"
            ).execute()
            print(f"✅ Sincronizados {len(registros_finales)} productos con éxito.")
        except Exception as e:
            print(f"❌ Error al subir datos: {e}")

if __name__ == "__main__":
    obtener_precios_locales()


