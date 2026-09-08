import os
import sys
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL_NEON = os.getenv("DATABASE_URL_NEON")

def verificar_estado_sistema():
    conn = psycopg2.connect(DATABASE_URL_NEON)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT current_timestamp, current_database();")
        res = cursor.fetchone()
        print(f"[{datetime.now()}] AgroTech Check OK - Base de datos conectada: {res[1]} a las {res[0]}")
    except Exception as e:
        print(f"Error en monitor_agrotech global: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    verificar_estado_sistema()
