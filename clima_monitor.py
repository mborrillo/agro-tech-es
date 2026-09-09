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
    print("❌ Error: DATABASE_URL_NEON no configurada.", file=sys.stderr)
    sys.exit(1)

if not AEMET_KEY:
    print("❌ Error: AEMET_KEY no configurada.", file=sys.stderr)
    sys.exit(1)


def obtener_estaciones_catalogo():
    """Obtiene todas las estaciones del catálogo en Neon."""
    conn = psycopg2.connect(DATABASE_URL_NEON)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_estacion, estacion FROM public.estaciones_comarca;")
        filas = cursor.fetchall()
        print(f"📋 Catálogo en DB recuperado: {len(filas)} estaciones.")
        return filas
    except Exception as e:
        print(f"⚠️ Error al consultar catálogo de estaciones: {e}", file=sys.stderr)
        return []
    finally:
        cursor.close()
        conn.close()


def consultar_aemet_estaciones():
    """Consulta las observaciones de AEMET paso a paso."""
    url_base = f"https://opendata.aemet.es/opendata/api/observacion/convencional/todas?api_key={AEMET_KEY}"
    headers = {"cache-control": "no-cache"}

    try:
        print("📡 Solicitando URL de datos a AEMET...")
        res = requests.get(url_base, headers=headers, timeout=15)
        res.raise_for_status()
        json_res = res.json()

        if json_res.get("estado") != 200:
            print(f"❌ AEMET respondió estado {json_res.get('estado')}: {json_res.get('descripcion')}")
            return []

        url_datos = json_res.get("datos")
        if not url_datos:
            print("❌ AEMET no entregó URL de descarga.")
            return []

        print("⏳ Esperando 2 segundos para descargar dataset completo...")
        time.sleep(2)

        res_datos = requests.get(url_datos, headers=headers, timeout=20)
        res_datos.raise_for_status()
        data = res_datos.json()
        print(f"📥 Observaciones recibidas de AEMET: {len(data)} registros totales de España.")
        return data

    except Exception as e:
        print(f"❌ Error conectando a la API de AEMET: {e}", file=sys.stderr)
        return []


def procesar_datos_aemet(raw_data, estaciones_catalogo):
    """Mapea las lecturas de AEMET con las estaciones del catálogo."""
    if not raw_data:
        return []

    # Mapa de nombres del catálogo normalizados
    cat_dict = {}
    for _, nom in estaciones_catalogo:
        if nom:
            cat_dict[nom.strip().upper()] = nom

    # Ordenar por fecha/hora descendente para tomar siempre la más reciente
    raw_sorted = sorted(raw_data, key=lambda x: str(x.get("fint", "")), reverse=True)

    registros_finales = {}

    for obs in raw_sorted:
        ubi_aemet = str(obs.get("ubi", "")).strip().upper()
        indicativo_aemet = obs.get("idema")

        # Buscar coincidencia
        estacion_match = None
        for nom_cat_upper, nom_real in cat_dict.items():
            # Coincidencia flexible (ej: BADAJOZ/AEROPUERTO -> BADAJOZ)
            if nom_cat_upper in ubi_aemet or ubi_aemet in nom_cat_upper:
                estacion_match = nom_real
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

    print(f"⚙️ Coincidencias encontradas con el catálogo: {len(registros_finales)} estaciones.")
    return list(registros_finales.values())


def guardar_datos_clima(datos):
    """Inserta o actualiza la base de datos sin fallos transaccionales."""
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
        count = 0
        for fila in datos:
            cursor.execute(sql_delete, (fila["fecha"], fila["estacion"]))
            cursor.execute(sql_insert, fila)
            count += 1

        conn.commit()
        print(f"✅ Exito: {count} registros insertados/actualizados en datos_clima.")
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
    raw_data = consultar_aemet_estaciones()
    datos_listos = procesar_datos_aemet(raw_data, estaciones_cat)
    guardar_datos_clima(datos_listos)


if __name__ == "__main__":
    ejecutar_pipeline_clima()
