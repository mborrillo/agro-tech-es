import os
import sys
import time
from datetime import datetime
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL_NEON = os.getenv("DATABASE_URL_NEON")
AEMET_KEY = os.getenv("AEMET_KEY") or os.getenv("AEMET_API_KEY")

if not DATABASE_URL_NEON:
    print("❌ Error: DATABASE_URL_NEON no está configurada.", file=sys.stderr)
    sys.exit(1)

if not AEMET_KEY:
    print("❌ Error: AEMET_KEY no está configurada.", file=sys.stderr)
    sys.exit(1)


def obtener_estaciones_catalogo():
    """Obtiene el listado completo de estaciones del catálogo independientemente de si id_estacion es NULL."""
    conn = psycopg2.connect(DATABASE_URL_NEON)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_estacion, estacion FROM public.estaciones_comarca;")
        return cursor.fetchall()
    except Exception as e:
        print(f"⚠️ Error al consultar catálogo de estaciones: {e}", file=sys.stderr)
        return []
    finally:
        cursor.close()
        conn.close()


def consultar_aemet_estaciones():
    """Descarga las observaciones recientes de todas las estaciones de AEMET."""
    url_base = f"https://opendata.aemet.es/opendata/api/observacion/convencional/todas?api_key={AEMET_KEY}"
    headers = {"cache-control": "no-cache"}

    try:
        res = requests.get(url_base, headers=headers, timeout=15)
        res.raise_for_status()
        json_res = res.json()

        if json_res.get("estado") != 200:
            print(f"⚠️ API AEMET respondió con estado {json_res.get('estado')}: {json_res.get('descripcion')}")
            return []

        url_datos = json_res.get("datos")
        if not url_datos:
            return []

        time.sleep(1)  # Pausa técnica evitar rate limit
        res_datos = requests.get(url_datos, headers=headers, timeout=20)
        res_datos.raise_for_status()
        return res_datos.json()

    except Exception as e:
        print(f"❌ Error al conectar con AEMET: {e}", file=sys.stderr)
        return []


def procesar_datos_aemet(raw_data, estaciones_catalogo):
    """
    Empareja las observaciones de AEMET con el catálogo usando nombre/ubicación.
    Toma la lectura más reciente de AEMET para cada estación encontrada.
    """
    if not raw_data:
        return []

    # Mapeo por nombre normalizado (mayúsculas sin espacios)
    nombres_cat = {nom.strip().upper(): (id_est, nom) for id_est, nom in estaciones_catalogo if nom}
    
    # Ordenar lecturas por fecha/hora descendente para asegurar tomar la MÁS RECIENTE disponible
    raw_sorted = sorted(raw_data, key=lambda x: str(x.get("fint", "")), reverse=True)

    registros_finales = {}

    for obs in raw_sorted:
        ubi_aemet = str(obs.get("ubi", "")).strip().upper()
        indicativo_aemet = obs.get("idema")

        # Buscar coincidencia de nombre entre el catálogo y AEMET
        estacion_match = None
        for nom_cat in nombres_cat:
            if nom_cat in ubi_aemet or ubi_aemet in nom_cat:
                estacion_match = nombres_cat[nom_cat][1]
                break

        if estacion_match and estacion_match not in registros_finales:
            fecha_str = obs.get("fint", "")
            try:
                fecha_dt = datetime.fromisoformat(fecha_str.replace("Z", "+00:00")).date()
            except Exception:
                fecha_dt = datetime.now().date()

            temp_actual = obs.get("ta")
            temp_max = obs.get("tam") or obs.get("tmax") or temp_actual
            temp_min = obs.get("tami") or obs.get("tmin") or temp_actual
            precipitacion = obs.get("prec") or 0.0
            humedad = obs.get("hr")
            viento_vel = obs.get("vv")

            if viento_vel is not None and viento_vel < 50:
                viento_vel = round(viento_vel * 3.6, 1)

            registros_finales[estacion_match] = {
                "fecha": fecha_dt,
                "estacion": estacion_match,
                "temp_max": temp_max,
                "temp_min": temp_min,
                "precipitacion": float(precipitacion) if precipitacion is not None else 0.0,
                "humedad": humedad,
                "viento_vel": viento_vel,
                "id_estacion": indicativo_aemet,
                "temp_actual": temp_actual,
                "latitud": obs.get("lat"),
                "longitud": obs.get("lon")
            }

    return list(registros_finales.values())


def guardar_datos_clima(datos):
    """Guarda/actualiza las lecturas en la tabla datos_clima de Neon de forma segura."""
    if not datos:
        print("ℹ️ No hay registros para guardar.")
        return

    conn = psycopg2.connect(DATABASE_URL_NEON)
    cursor = conn.cursor()

    sql_delete = """
        DELETE FROM public.datos_clima 
        WHERE fecha = %s AND UPPER(TRIM(estacion)) = UPPER(TRIM(%s));
    """

    sql_insert = """
        INSERT INTO public.datos_clima (
            fecha, estacion, temp_max, temp_min, precipitacion, humedad, 
            viento_vel, id_estacion, temp_actual, latitud, longitud
        ) VALUES (
            %(fecha)s, %(estacion)s, %(temp_max)s, %(temp_min)s, %(precipitacion)s, %(humedad)s,
            %(viento_vel)s, %(id_estacion)s, %(temp_actual)s, %(latitud)s, %(longitud)s
        );
    """

    try:
        registros_procesados = 0
        for fila in datos:
            # 1. Limpiar registro previo del mismo día y estación para evitar duplicados sin depender de restricciones
            cursor.execute(sql_delete, (fila["fecha"], fila["estacion"]))
            # 2. Insertar la lectura más reciente
            cursor.execute(sql_insert, fila)
            registros_procesados += 1

        conn.commit()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Clima: {registros_procesados} estaciones registradas/actualizadas correctamente en datos_clima.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error al guardar datos_clima: {e}", file=sys.stderr)
        raise
    finally:
        cursor.close()
        conn.close()


def ejecutar_pipeline_clima():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 Ejecutando monitor de clima...")
    estaciones_cat = obtener_estaciones_catalogo()
    print(f"📍 Estaciones en catálogo: {len(estaciones_cat)}")

    raw_data = consultar_aemet_estaciones()
    print(f"📡 Lecturas brutas AEMET: {len(raw_data)}")

    datos_listos = procesar_datos_aemet(raw_data, estaciones_cat)
    print(f"⚙️ Estaciones emparejadas procesadas: {len(datos_listos)}")

    guardar_datos_clima(datos_listos)


if __name__ == "__main__":
    ejecutar_pipeline_clima()
