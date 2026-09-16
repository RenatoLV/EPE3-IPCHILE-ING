# NexaFlow · EPE 3

Maqueta funcional de predicción diaria de demanda agregada por zona. **Datos sintéticos:** no representa resultados empresariales reales. No modela productos individuales ni optimiza rutas.

## Inicio rápido en Windows

Entorno de referencia: Python 3.12. Desde esta carpeta, la preparación automática instala dependencias, entrena y ejecuta pruebas:

```powershell
.\instalar.ps1
.\iniciar.ps1
```

`iniciar.ps1` levanta ambos servicios, comprueba una predicción por HTTP y abre el navegador. Mantén esa terminal abierta. **Ctrl+C detiene ambos procesos.** Si el puerto 5000 u 8000 está ocupado, informa el problema sin detener procesos ajenos. Los registros se guardan en `logs/`.

`requirements-lock.txt` conserva las versiones completas verificadas, incluidas las dependencias transitivas. El instalador usa ese archivo. `requirements.txt` enumera las dependencias directas del proyecto.

Para comprobar el arranque y apagado sin dejar servicios activos:

```powershell
.\iniciar.ps1 -Comprobar
```

Si PowerShell restringe scripts, puedes usar directamente `.\.venv\Scripts\python.exe run.py --open` después de preparar el entorno con los comandos manuales siguientes. No es necesario cambiar la política de ejecución del equipo.

### Instalación manual

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe train_model.py
.\.venv\Scripts\python.exe -m pytest -q
```

Terminal 1, API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api:app --host 127.0.0.1 --port 8000
```

Terminal 2, interfaz:

```powershell
.\.venv\Scripts\python.exe app.py
```

Abre http://127.0.0.1:5000 para la interfaz y http://127.0.0.1:8000/docs para la documentación interactiva. La web envía solicitudes HTTP a FastAPI. El modelo se carga una sola vez al arrancar la API. Si entrenas nuevamente, reinicia la API.

Terminal 3, evidencia de carga:

```powershell
.\.venv\Scripts\python.exe benchmark.py
```

Para generar ejemplos de predicción que puedes mostrar en el informe y la presentación, deja la aplicación iniciada y usa otra terminal:

```powershell
.\.venv\Scripts\python.exe ejemplos_operativos.py
```

Guarda tres escenarios distintos y sus respuestas en `artifacts/ejemplos_operativos.json`. El archivo se genera en tu equipo y no se versiona para evitar presentar una ejecución antigua como evidencia final.

## Contrato de la API

`POST /predict`, cuerpo JSON:

```json
{"zona":1,"dia_semana":5,"mes":12,"promocion":1,"demanda_lag7":95.0}
```

Campos enteros: zona 1–4, día 0–6 (lunes–domingo), mes 1–12, promoción 0–1. Demanda histórica numérica, finita y entre 0 y 100000 unidades. El máximo es una restricción técnica del prototipo y debe ajustarse con la empresa. Se rechazan claves adicionales. Respuesta válida 200 con `prediccion_demanda`, `unidad`, `modelo` y `datos`; entrada inválida 422; modelo ausente 503. La interfaz traduce las entradas inválidas a un mensaje y estado 400, y los problemas del servicio a 503.

```powershell
$body = @{zona=1;dia_semana=5;mes=12;promocion=1;demanda_lag7=95.0} | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:8000/predict -Method Post -ContentType 'application/json' -Body $body
```

`GET /health` devuelve 200 si el modelo está cargado, 503 si falta. No cargues archivos pickle de procedencia desconocida.

## Archivos

- `train_model.py`: genera 2 años sintéticos en 4 zonas, compara regresión lineal y 4 configuraciones Random Forest. Divide por fechas completas, usa 5 ventanas temporales sobre el primer 80% y reserva el último 20% para test. Selecciona por MAE de validación.
- `api.py`: API FastAPI y validación Pydantic.
- `app.py`, `templates/index.html`: interfaz Flask accesible y adaptable a móviles.
- `test_app.py`: pruebas de entradas, integración, disponibilidad y separación temporal.
- `benchmark.py`: 100 solicitudes con concurrencia 10 a cada servicio local.
- `run.py`, `iniciar.ps1`, `instalar.ps1`: preparación, arranque supervisado y verificación real del flujo HTTP.
- `data/`: conjunto sintético reproducible, semilla 42.
- `artifacts/`: métricas, predicciones por fila, pruebas, medición de carga y evidencias.
- `entregables/`: maqueta del informe en Word/PDF y presentación editable.
- `PLAN_DE_TRABAJO.md`: rúbrica, pendientes y protocolo de usabilidad.

Los rezagos del test usan observaciones reales del pasado simulado. El protocolo representa una predicción diaria con datos disponibles, no un pronóstico de varios meses emitido de una sola vez. El generador es aditivo y puede favorecer modelos simples. MAE y RMSE corresponden a regresión; Precision, Recall y F1 no aplican al objetivo continuo.

La interfaz presenta cuatro rutas referenciales para contextualizar el caso en Coquimbo: Centro y Guayacán, Peñuelas y La Herradura, Tierras Blancas, y Parte Alta y San Juan. El calendario deriva día de semana y mes para la API. Estas rutas no representan una división comercial real ni datos reales de demanda; deben reemplazarse o validarse antes de utilizar registros empresariales.

## GitHub y entrega

Repositorio preparado localmente; **no publicado**. Crea un repositorio vacío en tu cuenta y luego ejecuta (reemplazando TU_USUARIO):

```powershell
git add .
git commit -m "Prototipo NexaFlow EPE 3"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/nexaflow-demanda-ml.git
git push -u origin main
```

Si ya tienes un remoto, revísalo con `git remote -v` antes de añadirlo. Copia el enlace real al informe y a la presentación. Verifica la instalación desde un clon limpio. Completa los campos pendientes y reemplaza la condición de maqueta cuando termines. Docker y despliegue cloud son opcionales.

## Docker opcional

Si Docker Desktop está instalado y en ejecución, este proyecto puede levantarse sin crear un entorno Python local:

```powershell
docker compose up --build
```

Abre `http://127.0.0.1:5000` y `http://127.0.0.1:8000/docs`. Confirma que ambos servicios están saludables con `docker compose ps` y detén los contenedores con `docker compose down`. La configuración crea el conjunto y modelo sintéticos durante la construcción. Si incorporas datos reales, no los copies al contenedor ni al repositorio sin autorización.

Consulta `CONFIGURACION_ENTREGA.md` antes de presentar: reúne los comandos de demostración, la estructura mínima de datos reales y los pendientes obligatorios del informe.

## Fuentes técnicas

- Scikit-learn: https://scikit-learn.org/stable/modules/cross_validation.html
- FastAPI: https://fastapi.tiangolo.com/tutorial/body/
- Flask: https://flask.palletsprojects.com/en/stable/quickstart/

Las cifras incluidas en el texto original del usuario se sustituyeron por resultados de esta ejecución. La pauta admite Flask o FastAPI para API, aunque también enumera FastAPI como herramienta: este proyecto usa ambos.
