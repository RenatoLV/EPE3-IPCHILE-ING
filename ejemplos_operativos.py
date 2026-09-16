"""Genera ejemplos de negocio y verifica las respuestas HTTP de la API local."""
from datetime import datetime, timezone
import json
from pathlib import Path
import httpx

API_URL = 'http://127.0.0.1:8000/predict'
ROOT = Path(__file__).resolve().parent
SCENARIOS = [
    {'id': 'laboral_sin_promocion', 'descripcion': 'Zona 1, día laboral y sin promoción',
     'input': {'zona': 1, 'dia_semana': 2, 'mes': 4, 'promocion': 0, 'demanda_lag7': 90.0}},
    {'id': 'fin_de_semana_promocion', 'descripcion': 'Zona 3, sábado y promoción activa',
     'input': {'zona': 3, 'dia_semana': 5, 'mes': 12, 'promocion': 1, 'demanda_lag7': 135.0}},
    {'id': 'zona_alta_demanda', 'descripcion': 'Zona 4, domingo y promoción activa',
     'input': {'zona': 4, 'dia_semana': 6, 'mes': 7, 'promocion': 1, 'demanda_lag7': 150.0}},
]


def main():
    results = []
    with httpx.Client(timeout=10) as client:
        for scenario in SCENARIOS:
            response = client.post(API_URL, json=scenario['input'])
            response.raise_for_status()
            results.append({**scenario, 'status_http': response.status_code,
                            'resultado': response.json()})
    output = {'fecha_utc': datetime.now(timezone.utc).isoformat(),
              'origen': 'API local FastAPI; modelo entrenado con datos sintéticos',
              'escenarios': results}
    destination = ROOT/'artifacts/ejemplos_operativos.json'
    destination.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    for scenario in results:
        print(f"{scenario['id']}: {scenario['resultado']['prediccion_demanda']} unidades")


if __name__ == '__main__':
    main()
