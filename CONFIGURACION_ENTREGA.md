# Configuración para una entrega correcta

## Estado de esta versión

La aplicación funciona en local con datos sintéticos reproducibles. La sesión del 16 de septiembre de 2026 verificó 22 pruebas aprobadas, una carga local de 100 solicitudes con concurrencia 10 y cero errores, y Docker Compose con API y web en estado `healthy`. Estas evidencias demuestran funcionamiento técnico local; no desempeño empresarial.

## Antes de la demostración

1. Abrir PowerShell en la carpeta del proyecto.
2. Ejecutar `.\\instalar.ps1` una vez. Instala versiones bloqueadas, reentrena el modelo y ejecuta pruebas.
3. Ejecutar `.\\iniciar.ps1`. Abre la aplicación en `http://127.0.0.1:5000` y deja la consola abierta.
4. Abrir `http://127.0.0.1:8000/docs` y realizar una solicitud POST a `/predict` con el ejemplo mostrado en la documentación.
5. En otra terminal, ejecutar `.\\.venv\\Scripts\\python.exe ejemplos_operativos.py` y conservar el resultado generado solo como evidencia de esa ejecución.
6. En otra terminal, ejecutar `.\\.venv\\Scripts\\python.exe benchmark.py`. Guardar fecha, sistema y resultados antes de incorporarlos al informe.

La aplicación necesita los puertos locales 5000 y 8000 libres. Si el arranque informa que están ocupados, cerrar solo la instancia anterior de NexaFlow; no cerrar procesos desconocidos.

## Datos reales

Antes de reemplazar el conjunto sintético se requiere un CSV autorizado con, como mínimo, `fecha`, `zona`, `promocion` y `demanda`. Para que el proyecto sea comparable con el prototipo, se recomienda:

| Campo | Tipo esperado | Regla de calidad |
|---|---|---|
| fecha | AAAA-MM-DD | Una fecha por registro; calendario definido |
| zona | entero o código | Identificador consistente en todo el período |
| promocion | 0 o 1 | Regla documentada para promociones activas |
| demanda | número no negativo | Definir unidad y distinguir venta de demanda no atendida |

También se debe acordar qué hacer con feriados, devoluciones, días sin operación, stock agotado, zonas nuevas, filas duplicadas y valores faltantes. No subir datos con información personal, clientes o datos internos no autorizados a GitHub.

La adaptación pendiente está en `train_model.py`: leer el CSV autorizado, validar los cuatro campos, ordenar por zona y fecha, calcular `demanda_lag7` dentro de cada zona y repetir la separación temporal. Mantener un período final de test que no participe en la selección del modelo. Reemplazar todas las métricas, capturas y ejemplos después de ese entrenamiento.

## Requisitos de informe y presentación

- Completar nombre, sección, docente y fecha. El repositorio indicado es `https://github.com/RenatoLV/EPE3-IPCHILE-ING`; verificar acceso del docente y que contiene el último commit.
- Vincular NexaFlow con el diagnóstico de EPE 2 y explicar la decisión que apoya.
- Reportar MAE, RMSE y R² porque el problema es regresión. Precision, Recall y F1 no aplican al objetivo continuo; explicarlo en el informe.
- Incluir la tabla de métricas por zona y comentar el segmento con peor error. En esta ejecución sintética, zona 1 tiene MAE 7,13 y zona 4, 5,84.
- Incorporar capturas propias de formulario, respuesta de `/docs`, pruebas, carga y ejemplos operativos.
- Ejecutar `PROTOCOLO_USABILIDAD.md` con 3 a 5 participantes. Registrar tiempos, ayuda y comentarios reales. No afirmar que se hizo si aún no se realiza.
- Verificar desde un clon limpio; no subir secretos ni datos empresariales.

## Docker opcional

Se prepararon `Dockerfile`, `docker-compose.yml` y `.dockerignore`. Los contenedores incluyen comprobaciones de salud para API y web. La ejecución se validó el 16 de septiembre de 2026: ambos servicios llegaron a `healthy`, la API respondió `200` a `/health` y `/predict`, y el formulario web mostró una predicción de 113,7 unidades para el escenario documentado. El valor cambia cuando cambian los campos de entrada.

Para volver a iniciar los contenedores, usar:

```powershell
docker compose up --build
```

Después comprobar `http://127.0.0.1:5000` y `http://127.0.0.1:8000/docs`; al terminar ejecutar `docker compose down`. Para demostrar que ambos quedaron listos, usar `docker compose ps` y conservar una captura de los estados `healthy`. Docker es opcional según la pauta, por lo que no hace falta para una entrega correcta si la demostración local y su evidencia funcionan.
