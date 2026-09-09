import os
import sys
import time
from datetime import datetime
import requests
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

DATABASE_URL_NEON = os.getenv("DATABASE_URL_NEON")
AEMET_KEY = os.getenv("AEMET_KEY") or os.getenv("AEMET_API_KEY")

if not DATABASE_URL_NEON:
    print("❌ Error: DATABASE_URL_NEON no está configurada en las variables de entorno.", file=sys.stderr)
    sys.exit(1)

if not AEMET_KEY:
    print("❌ Error: AEMET_KEY no está configurada en las variables de entorno.", file=sys.stderr)
    sys.exit(1)


def obtener_estaciones_catalogo():
    """Obtiene el listado de estaciones registradas en la tabla estaciones_comarca."""
    conn = psycopg2.connect(DATABASE_URL_NEON)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_estacion, estacion FROM public.estaciones_comarca WHERE id_estacion IS NOT NULL;")
        filas = cursor.fetchall()
        return filas  # Lista de tuplas (id_estacion, nombre_estacion)
    except Exception as e:
        print(f"⚠️ Error al consultar catálogo de estaciones: {e}", file=sys.stderr)
        return []
    finally:
        cursor.close()
        conn.close()


def consultar_aemet_estaciones():
    """
    Consulta la API de AEMET para obtener las últimas observaciones convencionales
    de todas las estaciones meteorológicas disponibles.
    """
    url_base = f"https://opendata.aemet.es/opendata/api/observacion/convencional/todas?api_key={AEMET_KEY}"
    headers = {"cache-control": "no-cache"}

    try:
        # Primer llamado para obtener la URL de descarga de datos
        res = requests.get(url_base, headers=headers, timeout=15)
        res.raise_for_status()
        json_res = res.json()

        if json_res.get("estado") != 200:
            print(f"⚠️ AEMET API respondió con estado {json_res.get('estado')}: {json_res.get('descripcion')}")
            return []

        url_datos = json_res.get("datos")
        if not url_datos:
            print("⚠️ No se recibió URL de datos desde AEMET.")
            return []

        # Segundo llamado para descargar el dataset real en JSON
        time.sleep(1) # Pausa técnica para evitar rate limit
        res_datos = requests.get(url_datos, headers=headers, timeout=20)
        res_datos.raise_for_status()
        return res_datos.json()

    except Exception as e:
        print(f"❌ Error durante la conexión con AEMET: {e}", file=sys.stderr)
        return []


def procesar_datos_aemet(raw_data, estaciones_catalogo):
    """
    Filtra y transforma el JSON de AEMET para estructurar las lecturas
    correspondientes a las estaciones registradas en la base de datos.
    """
    if not raw_data:
        return []

    # Mapa para búsqueda rápida por id_estacion (indicativo AEMET)
    mapa_catalogo = {indicativo: nombre for indicativo, nombre in estaciones_catalogo}
    ids_validos = set(mapa_catalogo.keys())

    registros_procesados = {}

    for obs in raw_data:
        indicativo = obs.get("idema")
        
        # Si la estación está en nuestro catálogo (o si queremos registrar todas)
        if indicativo in ids_validos or not ids_validos:
            fecha_str = obs.get("fint")  # Formato ISO AEMET ej: 2026-09-09T20:00:00+0000
            try:
                fecha_dt = datetime.fromisoformat(fecha_str.replace("Z", "+00:00")).date()
            except Exception:
                fecha_dt = datetime.now().date()

            nombre_estacion = mapa_catalogo.get(indicativo, obs.get("ubi", "DESCONOCIDA"))

            # Extraer variables meteorológicas
            temp_actual = obs.get("ta")
            temp_max = obs.get("tam") or obs.get("tmax") or temp_actual
            temp_min = obs.get("tami") or obs.get("tmin") or temp_actual
            precipitacion = obs.get("prec") or 0.0
            humedad = obs.get("hr")
            viento_vel = obs.get("vv")  # Velocidad media del viento en m/s o km/h
            
            # Convertir viento a km/h si AEMET lo entrega en m/s
            if viento_vel is not None and viento_vel < 50:
                viento_vel = round(viento_vel * 3.6, 1)

            latitud = obs.get("lat")
            longitud = obs.get("lon")

            # Clave única por fecha y estación
            clave = (fecha_dt, indicativo)

            registro = {
                "fecha": fecha_dt,
                "estacion": nombre_estacion,
                "temp_max": temp_max,
                "temp_min": temp_min,
                "precipitacion": float(precipitacion) if precipitacion is not None else 0.0,
                "humedad": humedad,
                "viento_vel": viento_vel,
                "id_estacion": indicativo,
                "temp_actual": temp_actual,
                "latitud": latitud,
                "longitud": longitud
            }

            # Conservar la última lectura del día por estación
            registros_procesados[clave] = registro

    return list(registros_procesados.values())


def guardar_datos_clima(datos):
    """
    Inserta o actualiza las lecturas en la tabla public.datos_clima en Neon PostgreSQL.
    Maneja conflictos mediante ON CONFLICT para evitar registros duplicados.
    """
    if not datos:
        print("ℹ️ No hay registros meteorológicos procesados para guardar.")
        return

    conn = psycopg2.connect(DATABASE_URL_NEON)
    cursor = conn.cursor()

    sql_insert = """
        INSERT INTO public.datos_clima (
            fecha, estacion, temp_max, temp_min, precipitacion, humedad, 
            viento_vel, id_estacion, temp_actual, latitud, longitud
        ) VALUES (
            %(fecha)s, %(estacion)s, %(temp_max)s, %(temp_min)s, %(precipitacion)s, %(humedad)s,
            %(viento_vel)s, %(id_estacion)s, %(temp_actual)s, %(latitud)s, %(longitud)s
        )
        ON CONFLICT (fecha, id_estacion) DO UPDATE SET
            temp_actual = EXCLUDED.temp_actual,
            temp_max = GREATEST(datos_clima.temp_max, EXCLUDED.temp_max),
            temp_min = LEAST(datos_clima.temp_min, EXCLUDED.temp_min),
            precipitacion = EXCLUDED.precipitacion,
            humedad = COALESCE(EXCLUDED.humedad, datos_clima.humedad),
            viento_vel = COALESCE(EXCLUDED.viento_vel, datos_clima.viento_vel),
            latitud = COALESCE(EXCLUDED.latitud, datos_clima.latitud),
            longitud = COALESCE(EXCLUDED.longitud, datos_clima.longitud);
    """

    try:
        cursor.executemany(sql_insert, datos)
        conn.commit()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Clima: {len(datos)} registros de estaciones guardados/actualizados correctamente.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error durante la inserción en datos_clima: {e}", file=sys.stderr)
        raise
    finally:
        cursor.close()
        conn.close()


def ejecutar_pipeline_clima():
    """Función orquestadora principal del monitor de clima."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 Iniciando Ingesta de Clima AEMET...")

    # 1. Obtener listado de estaciones a rastrear
    estaciones_cat = obtener_estaciones_catalogo()
    print(f"📍 Estaciones en catálogo para rastrear: {len(estaciones_cat)}")

    # 2. Descargar observaciones de AEMET
    raw_data = consultar_aemet_estaciones()
    print(f"📡 Lecturas brutas recibidas de AEMET: {len(raw_data)}")

    # 3. Procesar y filtrar lecturas
    datos_listos = procesar_datos_aemet(raw_data, estaciones_cat)
    print(f"⚙️ Registros procesados válidos: {len(datos_listos)}")

    # 4. Guardar en Base de Datos
    guardar_datos_clima(datos_listos)


if __name__ == "__main__":
    ejecutar_pipeline_clima()
