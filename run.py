"""Inicia y supervisa la demo local. Ctrl+C detiene únicamente sus procesos."""
from pathlib import Path
import argparse
import importlib.util
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

ROOT = Path(__file__).resolve().parent
PAYLOAD = {'zona': 1, 'dia_semana': 5, 'mes': 12, 'promocion': 1, 'demanda_lag7': 95.0}


def free_port(port):
    with socket.socket() as sock:
        try:
            sock.bind(('127.0.0.1', port))
        except OSError:
            return False
    return True


def wait_ready(url, process, timeout=45):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f'El servicio terminó antes de estar listo. Consulta logs/: {url}')
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError):
            pass
        time.sleep(.2)
    raise RuntimeError(f'El servicio no quedó disponible: {url}. Consulta logs/.')


def verify_flow():
    request = urllib.request.Request('http://127.0.0.1:8000/predict',
                                    data=json.dumps(PAYLOAD).encode(),
                                    headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=10) as response:
        result = json.load(response)
    form = urllib.parse.urlencode(PAYLOAD).encode()
    with urllib.request.urlopen('http://127.0.0.1:5000/', data=form, timeout=10) as response:
        page = response.read().decode('utf-8')
    if 'unidades estimadas' not in page or str(result['prediccion_demanda']) not in page:
        raise RuntimeError('La web no mostró la predicción obtenida desde la API.')
    return {'estado': 'ok', 'request': PAYLOAD, 'response': result,
            'verificacion': 'POST HTTP real a API y formulario Flask; resultado coincidente'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Comprueba el flujo y detiene los servicios.')
    parser.add_argument('--open', action='store_true', help='Abre el navegador cuando los servicios están listos.')
    args = parser.parse_args()
    missing = [name for name in ['flask', 'fastapi', 'uvicorn', 'sklearn', 'httpx', 'pandas']
               if importlib.util.find_spec(name) is None]
    if missing:
        raise RuntimeError('Faltan dependencias: ' + ', '.join(missing) + '. Ejecuta instalar.ps1.')
    if not (ROOT / 'artifacts/modelo.pkl').is_file():
        raise RuntimeError('Falta el modelo. Ejecuta .venv/Scripts/python.exe train_model.py.')
    busy = [str(port) for port in [8000, 5000] if not free_port(port)]
    if busy:
        raise RuntimeError('Puertos ocupados: ' + ', '.join(busy) + '. Cierra la instancia anterior antes de iniciar otra.')
    (ROOT / 'logs').mkdir(exist_ok=True)
    processes, streams = [], []
    env = dict(os.environ, NEXAFLOW_API_URL='http://127.0.0.1:8000')
    flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
    try:
        services = [('api', ['-m', 'uvicorn', 'api:app', '--host', '127.0.0.1', '--port', '8000'], 'http://127.0.0.1:8000/health'),
                    ('web', ['app.py'], 'http://127.0.0.1:5000/')]
        for name, command, url in services:
            log = (ROOT / 'logs' / f'{name}.log').open('w', encoding='utf-8')
            streams.append(log)
            child = subprocess.Popen([sys.executable, *command], cwd=ROOT, env=env,
                                     stdout=log, stderr=subprocess.STDOUT, creationflags=flags)
            processes.append(child)
            wait_ready(url, child)
        evidence = verify_flow()
        evidence['fecha_local'] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
        (ROOT / 'artifacts/verificacion_operativa.json').write_text(
            json.dumps(evidence, ensure_ascii=False, indent=2), encoding='utf-8')
        print('Flujo web/API verificado. Predicción:', evidence['response']['prediccion_demanda'], flush=True)
        if args.check:
            return 0
        print('Web: http://127.0.0.1:5000\nAPI: http://127.0.0.1:8000/docs\nCtrl+C para detener ambos servicios.', flush=True)
        if args.open:
            webbrowser.open('http://127.0.0.1:5000')
        while all(child.poll() is None for child in processes):
            time.sleep(.5)
        raise RuntimeError('Uno de los servicios terminó. Consulta logs/.')
    except KeyboardInterrupt:
        print('\nDeteniendo NexaFlow...', flush=True)
        return 0
    finally:
        for child in reversed(processes):
            if child.poll() is None:
                child.terminate()
                try:
                    child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.wait()
        for log in streams:
            log.close()


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print(f'No se pudo iniciar NexaFlow: {exc}', file=sys.stderr)
        sys.exit(1)
