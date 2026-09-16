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

`GET /health` en FastAPI devuelve 200 si el modelo está cargado, 503 si falta. `GET /health` en Flask consulta a FastAPI con un timeout de un segundo y devuelve `{"servicio":"web","api":"ok"}` o `{"servicio":"web","api":"caida"}` con estado 503. `/docs` funciona sin internet e incluye una prueba interactiva; `/openapi.json` entrega el esquema generado por FastAPI. Cada `POST /predict` válido se registra como JSON en stdout del servicio API. No cargues archivos pickle de procedencia desconocida.

## Archivos

- `train_model.py`: genera 2 años sintéticos en 4 zonas, compara regresión lineal y 4 configuraciones Random Forest. Divide por fechas completas, usa 5 ventanas temporales sobre el primer 80% y reserva el último 20% para test. Selecciona por MAE de validación.
- `api.py`, `templates/api_docs.html`: API FastAPI, validación Pydantic y documentación interactiva autónoma.
- `app.py`, `templates/index.html`: interfaz Flask adaptable a móviles, historial sintético y métricas visibles. El gráfico usa Chart.js por CDN cuando está disponible y un SVG local cuando no hay acceso a internet.
- `test_app.py`: pruebas de entradas, integración, disponibilidad y separación temporal.
- `benchmark.py`: 100 solicitudes con concurrencia 10 a cada servicio local.
- `run.py`, `iniciar.ps1`, `instalar.ps1`: preparación, arranque supervisado y verificación real del flujo HTTP.
- `data/`: conjunto sintético reproducible, semilla 42.
- `artifacts/`: métricas, predicciones por fila, pruebas, medición de carga y evidencias.
- `entregables/`: maqueta del informe en Word/PDF y presentación editable.
- `PROTOCOLO_USABILIDAD.md`: tarea de 5 minutos y tabla vacía para 3–5 participantes reales.
- `CHECKLIST_ENTREGA_FINAL.md`: portada, capturas, EPE 2, GitHub y ensayo desde otro equipo.

Los rezagos del test usan observaciones reales del pasado simulado. El protocolo representa una predicción diaria con datos disponibles, no un pronóstico de varios meses emitido de una sola vez. El generador es aditivo y puede favorecer modelos simples. MAE y RMSE corresponden a regresión; Precision, Recall y F1 no aplican al objetivo continuo.

La interfaz presenta cuatro rutas referenciales para contextualizar el caso en Coquimbo: Centro y Guayacán, Peñuelas y La Herradura, Tierras Blancas, y Parte Alta y San Juan. El calendario deriva día de semana y mes para la API. Estas rutas no representan una división comercial real ni datos reales de demanda; deben reemplazarse o validarse antes de utilizar registros empresariales.

La cifra muestra ± RMSE de test como referencia de error típico aproximado. **No es un intervalo de confianza.** La recomendación compara la predicción con el promedio de los últimos 21 registros sintéticos de la ruta. El gráfico muestra esos registros de 2024 y un punto de escenario elegido por el usuario, que puede pertenecer a otra fecha y no es una continuación temporal del historial.

## Entregables de la EPE 3

- [Informe editable en Word](entregables/Maqueta_Informe_EPE3.docx)
- [Informe en PDF](entregables/Maqueta_Informe_EPE3.pdf)
- [Presentación ejecutiva en PowerPoint](entregables/Presentacion_EPE3.pptx)

Los tres archivos están versionados en GitHub junto al código. Antes de la entrega académica, completa los datos de portada, confirma la continuidad con EPE 2 y agrega resultados de usabilidad obtenidos con personas reales; consulta [CHECKLIST_ENTREGA_FINAL.md](CHECKLIST_ENTREGA_FINAL.md).

## GitHub y entrega

Repositorio: https://github.com/RenatoLV/EPE3-IPCHILE-ING. Para seguir trabajando desde otro equipo:

```powershell
git clone https://github.com/RenatoLV/EPE3-IPCHILE-ING.git
cd EPE3-IPCHILE-ING
docker compose up --build -d --wait
docker compose ps
```

El contenedor se reconstruye desde el Dockerfile y los archivos del repositorio. Iniciar sesión en Docker Desktop no traslada automáticamente los contenedores del otro equipo. Antes de entregar, confirma acceso del docente al enlace, completa los datos personales y aplica las pruebas de usabilidad; los resultados de estas pruebas deben ser reales.

## Docker

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
