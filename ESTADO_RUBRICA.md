# Estado de implementación y ruta de cierre

Actualización: 16 de septiembre de 2026. Esta tabla registra evidencia, no asigna puntajes ni garantiza una calificación.

| Criterio de la pauta | Implementado y comprobado | Para cerrar el criterio |
|---|---|---|
| 3.1 Diseño de solución, 25 puntos | Demanda diaria por zona, cinco entradas, entrenamiento temporal, separación web/API | Vincular el problema con EPE 2, justificar datos y definir criterios empresariales de aceptación |
| 3.2 Aplicación interactiva, 25 puntos | Formulario Flask, listas, resultado, mensajes de error, captura móvil de la primera versión | Probar tareas con usuarios, documentar dificultades y verificar mejoras |
| 4.1 Integración API, 25 puntos | FastAPI, /predict, /health y /docs; flujo HTTP web/API comprobado | Documentar ejemplos válidos e inválidos y preparar demostración del contrato |
| 4.3 Funcionalidad y optimización, 25 puntos | Entorno virtual, 22 pruebas aprobadas, Docker `healthy`, arranque supervisado, carga local y métricas segmentadas | Justificar límites del entorno local y probar usabilidad con personas reales |

## Punto de partida operativo

El entorno `.venv` se instaló y `pip check` no encontró dependencias incompatibles. Se verificó el modelo existente sin reentrenarlo. Los registros de esta sesión están en `artifacts/pruebas_actuales.txt`, `artifacts/pruebas_actuales.xml` y `artifacts/verificacion_operativa.json`.

El lanzador inicia la API, espera su disponibilidad, inicia la web y realiza una predicción HTTP en ambos recorridos. Comprueba que la web muestra el mismo resultado. Si falla un proceso, termina los procesos que inició; si encuentra puertos ocupados, informa el conflicto. La modalidad `--check` verifica el flujo y cierra los servicios.

Comando de inicio desde la carpeta del proyecto:

```powershell
.\.venv\Scripts\python.exe run.py --open
```

Mantener la terminal abierta y usar Ctrl+C para detener. Web: http://127.0.0.1:5000. Contrato: http://127.0.0.1:8000/docs. No iniciar dos instancias simultáneamente.

## Orden de trabajo acordable

1. **Base operativa:** entorno, arranque y comunicación comprobados en esta sesión.
2. **Diseño y datos:** confirmar contexto NexaFlow y continuidad con EPE 2. Mantener datos sintéticos identificados hasta disponer de registros autorizados. Verificar con el docente su aceptación si no existe una base real.
3. **Evaluación del modelo:** añadir error por zona, análisis de casos difíciles y justificación del algoritmo. Acordar umbral de error con el contexto de negocio.
4. **Validación de la aplicación:** ejecutar el protocolo de usuarios de PLAN_DE_TRABAJO.md y ampliar pruebas de carga relevantes para la demostración.
5. **Entrega:** completar informe, actualizar PowerPoint, publicar repositorio y comprobar reproducción desde una carpeta limpia.

Los documentos y el ZIP de la primera sesión siguen siendo una maqueta fechada el 14 de septiembre. No incluyen todavía los nuevos scripts de arranque ni constituyen la entrega final actualizada. El código de esta carpeta es la versión de trabajo vigente.

## Datos pendientes del estudiante

Nombre, sección, docente, antecedentes de la EPE 2, disponibilidad y origen de datos reales, participantes de usabilidad y cuenta/repositorio GitHub. Estos datos no impiden continuar la implementación técnica, pero son necesarios para cerrar una entrega fundamentada.
