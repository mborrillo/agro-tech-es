# ══════════════════════════════════════════════════════════════════
# ARCHIVO: mercado_monitor.py
# PROYECTO: Monitor Campo Extremadura — Ingesta de Mercados
# PLATAFORMA: Script ETL · ejecutado via GitHub Actions
# FUENTE: Yahoo Finance (yfinance) — futuros internacionales
# DESTINO: Supabase → tabla mercados_internacionales
# REPO: https://github.com/mborrillo/agro-tech-es
# ══════════════════════════════════════════════════════════════════

import os
import yfinance as yf
from supabase import create_client, Client
from datetime import datetime

# --- CONFIGURACIÓN ---
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://zzucvsremavkikecsptg.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_mercados():
    print(f"=== Monitor de Mercados Pro - {datetime.now().strftime('%d/%m/%Y %H:%M')} ===")
    
    # Tickers clave para el sector agropecuario de Extremadura
    activos = {
        "Trigo": {"ticker": "ZW=F", "cat": "Cereal"},
        "Maiz": {"ticker": "ZC=F", "cat": "Cereal"},
        "Soja": {"ticker": "ZS=F", "cat": "Cereal"},
        "Arroz": {"ticker": "ZR=F", "cat": "Cereal"},
        "Aceite_Soja": {"ticker": "ZL=F", "cat": "Grasas"},
        "Ganado_Vivo": {"ticker": "LE=F", "cat": "Ganaderia"},
        "Ganado_Feeder": {"ticker": "GF=F", "cat": "Ganaderia"},
        "Gas_Natural": {"ticker": "NG=F", "cat": "Energia_Agro"},
        "Brent": {"ticker": "BZ=F", "cat": "Energia_Agro"},
        "Euro_Dolar": {"ticker": "EURUSD=X", "cat": "Divisa"}
    }

    registros = []
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    for nombre, info in activos.items():
        try:
            print(f"→ Analizando {nombre}...")
            ticket = yf.Ticker(info['ticker'])
            
            # Pedimos 5 días para asegurar que siempre haya al menos 2 sesiones de mercado
            # Esto soluciona los NULL de los fines de semana
            hist = ticket.history(period="5d")
            
            if not hist.empty and len(hist) >= 2:
                ultimo_cierre = float(hist['Close'].iloc[-1])
                precio_ant = float(hist['Close'].iloc[-2])
                
                # --- FILTRO DE ROBUSTEZ ---
                # Si el precio es 0 o la caída es superior al 80%, es un error de ticker/vencimiento
                if ultimo_cierre <= 0 or (precio_ant > 0 and (ultimo_cierre / precio_ant) < 0.2):
                    print(f"  ⚠️ Anomalía de precio detectada en {nombre} (Posible error de yfinance). Omitiendo.")
                    continue

                variacion = ((ultimo_cierre - precio_ant) / precio_ant) * 100
                
                registros.append({
                    "fecha": fecha_hoy,
                    "activo": nombre,
                    "precio_cierre": round(ultimo_cierre, 2),
                    "variacion_p": round(variacion, 2),
                    "categoria": info['cat'],
                    "moneda": "USD" if "USD" in info['ticker'] or "=F" in info['ticker'] else "EUR"
                })
                print(f"  ✓ {nombre}: {round(ultimo_cierre, 2)} ({round(variacion, 2)}%)")
            else:
                print(f"  ⚠️ No hay datos suficientes en los últimos 5 días para {nombre}")

        except Exception as e:
            print(f"  ❌ Error técnico con {nombre}: {e}")

    # Guardado masivo en Supabase
    if registros:
        print(f"\n→ Actualizando {len(registros)} activos en la base de datos...")
        try:
            supabase.table("mercados_internacionales").upsert(
                registros, 
                on_conflict="fecha, activo"
            ).execute()
            print("✅ Proceso de mercados finalizado con éxito.")
        except Exception as e:
            print(f"❌ Error al guardar en Supabase: {e}")
    else:
        print("\n⚠ No se generaron registros válidos para guardar.")

if __name__ == "__main__":
    obtener_mercados()
