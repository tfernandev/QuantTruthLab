import requests
import json
import pandas as pd

API_URL = "http://localhost:8000/api/backtest/run/"

def verify_scenario(scenario_id, label):
    print(f"\n--- VERIFICANDO ESCENARIO: {label} ({scenario_id}) ---")
    payload = {
        "symbol": "BTC/USDT",
        "timeframe": "1h",
        "strategy_name": "SmaCrossover",
        "scenario_id": scenario_id,
        "initial_capital": 10000
    }
    
    r = requests.post(API_URL, json=payload)
    if r.status_code != 200:
        print(f"Error: {r.text}")
        return

    data = r.json()
    print(f"Resultado Algoritmo: {data['total_return']}%")
    print(f"Resultado Mercado (B&H): {data['benchmark_return']}%")
    print(f"Diagnóstico Robustez: {data['robusticitiy_score']}")
    print(f"Análisis de Estrés: {data['stress_moment_explanation']}")
    
    # Verificación de "Vida Real" (facts)
    if scenario_id == "bull_2021":
        if data['benchmark_return'] > 50:
            print("[OK] PRECISION HISTORICA: El bot detecto correctamente el crecimiento masivo de 2021.")
        else:
            print("[ERROR] El benchmark de 2021 debería ser muy positivo.")
            
    if scenario_id == "bear_2022":
        if data['benchmark_return'] < -50:
            print("[OK] PRECISION HISTORICA: El bot detecto correctamente el crash sistemico de 2022.")
        else:
            print(f"[ERROR] El benchmark de 2022 debería ser negativo (detectado: {data['benchmark_return']}%).")
        
        if "desmoronamiento del precio" in data['stress_moment_explanation'].lower() or "riesgo de mercado" in data['stress_moment_explanation'].lower():
            print("[OK] ANALISIS FORENSE: El bot identifico correctamente que las perdidas de 2022 fueron por caida de mercado.")

if __name__ == "__main__":
    verify_scenario("bull_2021", "BULL RUN 2021")
    verify_scenario("bear_2022", "INVIERNO CRIPTO 2022")
