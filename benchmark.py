"""Carga HTTP local de API y flujo web. Servicios activos requeridos."""
import concurrent.futures
import json
import platform
import time
from datetime import datetime, timezone
from pathlib import Path
import httpx
import numpy as np

PAYLOAD={'zona':1,'dia_semana':5,'mes':12,'promocion':1,'demanda_lag7':95.0}

def measure(url,web=False):
    with httpx.Client(timeout=15) as client:
        def call(_):
            t=time.perf_counter()
            try:
                r=client.post(url,**({'data':PAYLOAD} if web else {'json':PAYLOAD}))
                ok=r.status_code == 200
            except httpx.HTTPError:
                ok=False
            return (time.perf_counter()-t)*1000,ok
        call(0)
        t=time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            rows=list(pool.map(call,range(100)))
        elapsed=time.perf_counter()-t
    return {'url':url,'solicitudes':100,'concurrencia':10,'errores':sum(not r[1] for r in rows),
            'p50_ms':float(np.percentile([r[0] for r in rows],50)),
            'p95_ms':float(np.percentile([r[0] for r in rows],95)),
            'solicitudes_segundo':100/elapsed}

if __name__ == '__main__':
    result={'fecha_utc':datetime.now(timezone.utc).isoformat(),'entorno':platform.platform(),
            'alcance':'Medición local breve. No certifica capacidad de producción ni usabilidad humana.',
            'api':measure('http://127.0.0.1:8000/predict'), 'web':measure('http://127.0.0.1:5000/',True)}
    Path('artifacts/carga.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(result,indent=2,ensure_ascii=False))
