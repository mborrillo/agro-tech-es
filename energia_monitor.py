import os
import sys
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno (para ejecución local o GitHub Actions)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Error: La variable de entorno DATABASE_URL no está configurada.", file=sys.stderr)
    sys.exit(1)

def conectar_db():
    """Establece la conexión con la base de datos PostgreSQL en Neon."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}", file=sys.stderr)
        sys.exit(1)

def guardar_datos_energia(datos_procesados):
    """
    Inserta o actualiza los registros en la tabla unificada 'datos_energia_consolidada'.
    """
    conn = conectar_db()
    cursor = conn.cursor()

    sql_insert = """
        INSERT INTO public.datos_energia_consolidada (
            fecha, hora, precio_kwh, precio_min, precio_max, precio_medio, tramo, vs_media, var_precio_p
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    try:
        for fila in datos_procesados:
            cursor.execute(sql_insert, (
                fila.get('fecha'),
                fila.get('hora'),
                fila.get('precio_kwh'),
                fila.get('precio_min'),
                fila.get('precio_max'),
                fila.get('precio_medio'),
                fila.get('tramo'),
                fila.get('vs_media'),
                fila.get('var_precio_p')
            ))
        
        conn.commit()
        print(f"[{datetime.now()}] Éxito: {len(datos_procesados)} registros insertados en datos_energia_consolidada.")
    except Exception as e:
        conn.rollback()
        print(f"Error durante la inserción en base de datos: {e}", file=sys.stderr)
        raise
    finally:
        cursor.close()
        conn.close()

def procesar_pipeline_energia():
    """
    Función principal del pipeline ETL para energía.
    Aquí se integraría la llamada a la API de origen (ej. Red Eléctrica / OMIE).
    """
    print(f"[{datetime.now()}] Iniciando extracción de datos de energía...")
    
    # Simulación de estructura de datos extraída lista para volcar
    # En producción, mapea aquí los campos obtenidos de tu fuente externa
    datos_ejemplo = [
        {
            "fecha": datetime.now().date(),
            "hora": datetime.now().hour,
            "precio_kwh": 0.12543,
            "precio_min": 0.09100,
            "precio_max": 0.18500,
            "precio_medio": 0.13000,
            "tramo": "P1",
            "vs_media": -2.50,
            "var_precio_p": 1.20
        }
    ]

    guardar_datos_energia(datos_ejemplo)

if __name__ == "__main__":
    procesar_pipeline_energia()
