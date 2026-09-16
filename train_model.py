"""Experimento reproducible con datos SINTÉTICOS. Ejecutar antes de la API."""
from pathlib import Path
import json
import pickle
import hashlib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path(__file__).resolve().parent
FEATURES = ['zona', 'dia_semana', 'mes', 'promocion', 'demanda_lag7']

def generate_data():
    rng = np.random.default_rng(42)
    rows = []
    for zona in range(1, 5):
        history = []
        for date in pd.date_range('2023-01-01', '2024-12-31'):
            promo = int(rng.random() < .2)
            demand = max(0, 75 + zona*12 + 18*(date.dayofweek >= 5)
                         + 22*promo + 12*np.sin(2*np.pi*date.month/12) + rng.normal(0, 8))
            if len(history) >= 7:
                rows.append([date, zona, date.dayofweek, date.month, promo, history[-7], demand])
            history.append(demand)
    return pd.DataFrame(rows, columns=['fecha', *FEATURES, 'demanda']).sort_values(['fecha','zona']).reset_index(drop=True)

def scores(y, pred):
    return {'MAE': float(mean_absolute_error(y,pred)),
            'RMSE': float(np.sqrt(mean_squared_error(y,pred))), 'R2': float(r2_score(y,pred))}


def segment_scores(frame, columns):
    """Métricas de test por segmento. No se usan para seleccionar el modelo."""
    rows = []
    for values, group in frame.groupby(columns, dropna=False):
        values = values if isinstance(values, tuple) else (values,)
        row = {column: value.item() if hasattr(value, 'item') else value
               for column, value in zip(columns, values)}
        row['filas'] = int(len(group))
        row.update(scores(group.demanda, group.prediccion))
        rows.append(row)
    return sorted(rows, key=lambda row: tuple(row[column] for column in columns))

def train():
    (ROOT/'data').mkdir(exist_ok=True)
    (ROOT/'artifacts').mkdir(exist_ok=True)
    df = generate_data()
    df.to_csv(ROOT/'data/demanda_sintetica.csv',index=False)
    dates = df.fecha.unique()
    cutoff = dates[int(len(dates)*.8)]
    dev, test = df[df.fecha < cutoff], df[df.fecha >= cutoff]
    prep = ColumnTransformer([('categorias', OneHotEncoder(handle_unknown='ignore', sparse_output=False), FEATURES[:3])], remainder='passthrough')
    candidates = {'Lineal': make_pipeline(prep, LinearRegression())}
    for depth in [6, 12]:
        for leaf in [2, 5]:
            candidates[f'RF_depth{depth}_leaf{leaf}'] = make_pipeline(clone(prep), RandomForestRegressor(n_estimators=100,max_depth=depth,min_samples_leaf=leaf,random_state=42,n_jobs=1))
    cv, boundaries = {}, []
    devdates = dev.fecha.unique()
    splits = list(TimeSeriesSplit(n_splits=5).split(devdates))
    for a,b in splits:
        boundaries.append({'train_end':str(pd.Timestamp(devdates[a[-1]]).date()),'validation_start':str(pd.Timestamp(devdates[b[0]]).date()),'validation_end':str(pd.Timestamp(devdates[b[-1]]).date())})
    for name, model in candidates.items():
        folds = []
        for a,b in splits:
            tr, va = dev[dev.fecha.isin(devdates[a])], dev[dev.fecha.isin(devdates[b])]
            estimator = clone(model).fit(tr[FEATURES],tr.demanda)
            folds.append(scores(va.demanda, np.maximum(0,estimator.predict(va[FEATURES]))))
        cv[name] = {'MAE_media':float(np.mean([f['MAE'] for f in folds])), 'folds':folds}
    selected = min(cv,key=lambda n:cv[n]['MAE_media'])
    model = clone(candidates[selected]).fit(dev[FEATURES],dev.demanda)
    pred = np.maximum(0,model.predict(test[FEATURES]))
    evaluated = test.assign(prediccion=pred, error_absoluto=np.abs(test.demanda - pred),
                            tipo_dia=np.where(test.dia_semana >= 5, 'fin_de_semana', 'laboral'))
    by_zone = segment_scores(evaluated, ['zona'])
    by_promotion = segment_scores(evaluated, ['promocion'])
    by_day_type = segment_scores(evaluated, ['tipo_dia'])
    candidates_summary = [
        {'modelo': name, 'MAE_validacion_media': values['MAE_media']}
        for name, values in sorted(cv.items(), key=lambda item: item[1]['MAE_media'])
    ]
    worst_errors = (evaluated.sort_values('error_absoluto', ascending=False)
                    [['fecha', *FEATURES, 'demanda', 'prediccion', 'error_absoluto']]
                    .head(10).copy())
    worst_errors['fecha'] = worst_errors['fecha'].dt.strftime('%Y-%m-%d')
    result = {'datos':'SINTÉTICOS, no representan operación real de NexaFlow','semilla':42,
              'filas':len(df),'entrenamiento':len(dev),'test':len(test),
              'test_desde':str(pd.Timestamp(cutoff).date()),'cv':cv,'fold_dates':boundaries,
              'comparacion_modelos':candidates_summary,
              'seleccionado':selected,'test_metricas':scores(test.demanda,pred),
              'baseline_lag7_test':scores(test.demanda,test.demanda_lag7),
              'metricas_por_zona':by_zone,
              'metricas_por_promocion':by_promotion,
              'metricas_por_tipo_dia':by_day_type,
              'mayores_errores_test':worst_errors.to_dict(orient='records'),
              'protocolo':'Predicción diaria con demanda observada de hace 7 días disponible; no pronóstico multihorizonte.'}
    with (ROOT/'artifacts/modelo.pkl').open('wb') as f:
        pickle.dump({'model':model,'features':FEATURES,'name':selected},f)
    result['modelo_sha256'] = hashlib.sha256((ROOT/'artifacts/modelo.pkl').read_bytes()).hexdigest()
    (ROOT/'artifacts/metricas.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    evaluated.to_csv(ROOT/'artifacts/predicciones_test.csv',index=False)
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__ == '__main__':
    train()
