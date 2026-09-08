import os
import sys
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL_NEON = os.getenv("DATABASE_URL_NEON")

if not DATABASE_URL_NEON:
    print("Error: DATABASE_URL_NEON no configurada.", file=sys.stderr)
    sys.exit(1)

def guardar_datos_clima(datos):
    conn = psycopg2.connect(DATABASE_URL_NEON)
    cursor = conn.cursor()
    
    sql = """
        INSERT INTO public.datos_clima (
            fecha, estacion, temp_max, temp_min, precipitacion, humedad, viento_vel, id_estacion, temp_actual, latitud, longitud
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    try:
        for fila in datos:
            cursor.execute(sql, (
                fila.get('fecha'), fila.get('estacion'), fila.get('temp_max'),
                fila.get('temp_min'), fila.get('precipitacion'), fila.get('humedad'),
                fila.get('viento_vel'), fila.get('id_estacion'), fila.get('temp_actual'),
                fila.get('latitud'), fila.get('longitud')
            ))
        conn.commit()
        print(f"[{datetime.now()}] Clima: {len(datos)} registros insertados correctamente.")
    except Exception as e:
        conn.rollback()
        print(f"Error en clima_monitor: {e}", file=sys.stderr)
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print(f"[{datetime.now()}] Ejecutando monitor de clima...")
    # Ejemplo de inserción estructurada
    datos_ejemplo = [{
        "fecha": datetime.now().date(),
        "estacion": "Badajoz Aeropuerto",
        "temp_max": 32.5,
        "temp_min": 18.0,
        "precipitacion": 0.0,
        "humedad": 45.0,
        "viento_vel": 12.5,
        "id_estacion": "4451X",
        "temp_actual": 28.0,
        "latitud": 38.89,
        "longitud": -6.83
    }]
    guardar_datos_clima(datos_ejemplo)
