import math
import pytest
import httpx
from fastapi.testclient import TestClient
from api import app as api
from app import app as web

PAYLOAD = {'zona':1,'dia_semana':5,'mes':12,'promocion':1,'demanda_lag7':95.0}

@pytest.fixture
def client():
    with TestClient(api) as c:
        yield c

def test_health(client):
    assert client.get('/health').status_code == 200

def test_docs_work_without_external_assets(client):
    response = client.get('/docs')
    assert response.status_code == 200
    assert 'POST /predict' in response.text
    assert 'cdn.' not in response.text

def test_prediction(client):
    r = client.post('/predict',json=PAYLOAD)
    assert r.status_code == 200
    assert math.isfinite(r.json()['prediccion_demanda'])
    assert r.json()['prediccion_demanda'] >= 0

@pytest.mark.parametrize('change',[{'zona':0},{'zona':True},{'mes':13},{'dia_semana':7},{'promocion':2},{'demanda_lag7':-1},{'zona':'uno'},{'extra':1}])
def test_invalid(client,change):
    assert client.post('/predict',json={**PAYLOAD,**change}).status_code == 422

def test_missing(client):
    assert client.post('/predict',json={'zona':1}).status_code == 422
    assert client.post('/predict').status_code == 422

def test_unavailable_model(client):
    old = api.state.bundle
    try:
        api.state.bundle = None
        assert client.get('/health').status_code == 503
        assert client.post('/predict',json=PAYLOAD).status_code == 503
    finally:
        api.state.bundle = old

def test_form():
    response = web.test_client().get('/')
    assert response.status_code == 200
    assert b'Centro y Guayac' in response.data


def test_form_date_is_translated_for_the_api(client, monkeypatch):
    captured = {}
    def call(url, json, timeout):
        captured.update(json)
        return client.post('/predict', json=json)
    monkeypatch.setattr(httpx, 'post', call)
    response = web.test_client().post('/', data={
        'zona': 2, 'fecha': '2026-09-19', 'promocion': 1, 'demanda_lag7': 100,
    })
    assert response.status_code == 200
    assert captured['dia_semana'] == 5
    assert captured['mes'] == 9
    assert b'S\xc3\xa1bado 19 de septiembre de 2026' in response.data


def test_web_health(monkeypatch):
    monkeypatch.setattr(httpx, 'get', lambda url, timeout: type('Response', (), {'status_code': 200, 'json': lambda self: {'status': 'ok'}})())
    response = web.test_client().get('/health')
    assert response.status_code == 200
    assert response.get_json() == {'servicio': 'web', 'api': 'ok'}


def test_web_health_when_api_is_down(monkeypatch):
    def fail(*args, **kwargs):
        raise httpx.ConnectError('offline')
    monkeypatch.setattr(httpx, 'get', fail)
    response = web.test_client().get('/health')
    assert response.status_code == 503
    assert response.get_json() == {'servicio': 'web', 'api': 'caida'}


def test_interface_explains_model_and_error(client, monkeypatch):
    monkeypatch.setattr(httpx, 'post', lambda url, json, timeout: client.post('/predict', json=json))
    response = web.test_client().post('/', data=PAYLOAD)
    assert response.status_code == 200
    assert 'Acerca del modelo'.encode() in response.data
    assert 'RMSE medido en test'.encode() in response.data
    assert 'Últimos 21 días'.encode() in response.data
    assert '±'.encode() in response.data

def test_web_api_integration(client,monkeypatch):
    monkeypatch.setattr(httpx,'post',lambda url,json,timeout:client.post('/predict',json=json))
    r = web.test_client().post('/',data=PAYLOAD)
    assert r.status_code == 200
    assert b'unidades estimadas' in r.data

def test_api_failure_message(monkeypatch):
    def fail(*args,**kwargs):
        raise httpx.ConnectError('offline')
    monkeypatch.setattr(httpx,'post',fail)
    assert web.test_client().post('/',data=PAYLOAD).status_code == 503

def test_temporal_boundaries():
    import json
    from pathlib import Path
    m=json.loads((Path(__file__).parent/'artifacts/metricas.json').read_text(encoding='utf-8'))
    assert all(f['train_end'] < f['validation_start'] <= f['validation_end'] < m['test_desde'] for f in m['fold_dates'])


def test_segment_metrics_and_operational_examples_are_defined():
    import json
    from pathlib import Path
    from ejemplos_operativos import SCENARIOS
    m = json.loads((Path(__file__).parent/'artifacts/metricas.json').read_text(encoding='utf-8'))
    assert len(m['metricas_por_zona']) == 4
    assert sum(row['filas'] for row in m['metricas_por_zona']) == m['test']
    assert len(m['mayores_errores_test']) == 10
    assert len({scenario['id'] for scenario in SCENARIOS}) == len(SCENARIOS)
    assert all(set(scenario['input']) == set(PAYLOAD) for scenario in SCENARIOS)
