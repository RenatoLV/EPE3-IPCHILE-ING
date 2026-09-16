"""Interfaz Flask que consume FastAPI por HTTP."""
import os
from datetime import date, datetime
import httpx
from flask import Flask, render_template, request

app = Flask(__name__)
API_URL = os.getenv('NEXAFLOW_API_URL','http://127.0.0.1:8000').rstrip('/')
ZONAS = {
    1: {'nombre': 'Centro y Guayacán', 'sectores': 'Centro, Guayacán y El Llano', 'descripcion': 'Ruta referencial de cobertura urbana central.'},
    2: {'nombre': 'Peñuelas y La Herradura', 'sectores': 'Peñuelas, La Herradura y sectores costeros cercanos', 'descripcion': 'Ruta referencial de cobertura costera.'},
    3: {'nombre': 'Tierras Blancas', 'sectores': 'Tierras Blancas y sectores residenciales cercanos', 'descripcion': 'Ruta referencial de cobertura interior.'},
    4: {'nombre': 'Parte Alta y San Juan', 'sectores': 'Parte Alta, San Juan y sectores altos cercanos', 'descripcion': 'Ruta referencial de cobertura alta.'},
}
DIAS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
DEFAULTS = {'zona': 1, 'fecha': date.today().isoformat(), 'dia_semana': date.today().weekday(), 'mes': date.today().month, 'promocion': 1, 'demanda_lag7': 95}
API_FEATURES = ('zona', 'dia_semana', 'mes', 'promocion', 'demanda_lag7')


def fecha_humana(value):
    selected = datetime.strptime(value, '%Y-%m-%d').date()
    return f'{DIAS[selected.weekday()].capitalize()} {selected.day} de {MESES[selected.month - 1]} de {selected.year}'

@app.get('/health')
def health():
    """Estado simple de la interfaz, sin afirmar disponibilidad de la API."""
    return {'status': 'ok', 'servicio': 'web', 'api_url': API_URL}

@app.route('/',methods=['GET','POST'])
def index():
    values, result, error, status = dict(DEFAULTS), None, None, 200
    if request.method == 'POST':
        values.update({k: request.form[k] for k in DEFAULTS if k in request.form})
        try:
            if values.get('fecha'):
                selected = datetime.strptime(values['fecha'], '%Y-%m-%d').date()
                values['dia_semana'], values['mes'] = selected.weekday(), selected.month
            payload = {key: (float(values[key]) if key == 'demanda_lag7' else int(values[key]))
                       for key in API_FEATURES}
            resp = httpx.post(API_URL+'/predict',json=payload,timeout=5)
            if resp.status_code == 422:
                error, status = 'Revisa los rangos y completa todos los campos.', 400
            else:
                resp.raise_for_status()
                result = resp.json()
        except (ValueError, TypeError):
            error, status = 'Ingresa números válidos en todos los campos.', 400
        except httpx.HTTPError:
            error, status = 'La API no está disponible. Inicia el servicio e inténtalo otra vez.', 503
    try:
        date_label = fecha_humana(str(values['fecha']))
    except (KeyError, ValueError):
        date_label = 'Fecha por definir'
    return render_template('index.html', values=values, result=result, error=error,
                           zonas=ZONAS, zona_seleccionada=ZONAS.get(int(values['zona']), ZONAS[1]),
                           fecha_humana=date_label), status

if __name__ == '__main__':
    app.run(host=os.getenv('NEXAFLOW_WEB_HOST', '127.0.0.1'), port=5000, debug=False)
