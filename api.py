"""API FastAPI. Carga únicamente el pickle generado localmente por train_model.py."""
from contextlib import asynccontextmanager
from pathlib import Path
import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict

MODEL_PATH = Path(__file__).resolve().parent/'artifacts/modelo.pkl'

class PredictionInput(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)
    zona: int = Field(ge=1,le=4,strict=True)
    dia_semana: int = Field(ge=0,le=6,strict=True)
    mes: int = Field(ge=1,le=12,strict=True)
    promocion: int = Field(ge=0,le=1,strict=True)
    demanda_lag7: float = Field(ge=0,le=100000,strict=True)

@asynccontextmanager
async def lifespan(app):
    app.state.bundle = None
    if MODEL_PATH.exists():
        with MODEL_PATH.open('rb') as f:
            app.state.bundle = pickle.load(f)
    yield

app = FastAPI(title='NexaFlow API',version='1.0.0',lifespan=lifespan,
              description='Prototipo académico entrenado con datos sintéticos.')

@app.get('/health')
def health():
    if not getattr(app.state,'bundle',None):
        raise HTTPException(503,'Modelo no disponible. Ejecuta train_model.py y reinicia la API.')
    return {'status':'ok','modelo':app.state.bundle['name'],'datos':'sinteticos'}

@app.post('/predict')
def predict(data:PredictionInput):
    health()
    bundle = app.state.bundle
    frame = pd.DataFrame([data.model_dump()],columns=bundle['features'])
    value = max(0.,float(bundle['model'].predict(frame)[0]))
    return {'prediccion_demanda':round(value,1),'unidad':'unidades/día','modelo':bundle['name'],'datos':'sinteticos'}
