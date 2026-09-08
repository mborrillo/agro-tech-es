import os
import sys
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL_NEON = os.getenv("DATABASE_URL_NEON")

def guardar_precios_mercado(datos):
    conn = psycopg2.connect(DATABASE_URL_NEON)
    cursor = conn.cursor()
    
    sql = """
        INSERT INTO public.precios_agricolas (
            fecha, sector, producto, variedad, precio_min, precio_max, unidad, fuente, variacion_p
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    try:
        for fila in datos:
            cursor.execute(sql, (
                fila.get('fecha'), fila.get('sector'), fila.get('producto'),
                fila.get('variedad'), fila.get('precio_min'), fila.get('precio_max'),
                fila.get('unidad', '€/kg'), fila.get('fuente', 'Agrobservex'), fila.get('variacion_p')
            ))
        conn.commit()
        print(f"[{datetime.now()}] Mercado: {len(datos)} precios registrados.")
    except Exception as e:
        conn.rollback()
        print(f"Error en mercado_monitor: {e}", file=sys.stderr)
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print(f"[{datetime.now()}] Ejecutando monitor de mercado...")
    datos_ejemplo = [{
        "fecha": datetime.now().date(),
        "sector": "Olivar",
        "producto": "Aceite de Oliva Virgen Extra",
        "variedad": "Arbequina",
        "precio_min": 7.20,
        "precio_max": 7.50,
        "variacion_p": 0.45
    }]
    guardar_precios_mercado(datos_ejemplo)
