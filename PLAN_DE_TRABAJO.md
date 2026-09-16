# Desarrollo y cierre de la actividad

## Estado y alcance

Este paquete es una maqueta funcional y documental. El contexto NexaFlow se toma del mensaje del estudiante; no se adjuntó la EPE 2 completa ni una base empresarial. El PDF de la actividad es la fuente de requisitos. El archivo de JavaScript adjunto es un borrador, no evidencia de ejecución.

## Correspondencia con la rúbrica

| Criterio (25 puntos) | Base preparada | Trabajo del estudiante |
|---|---|---|
| 3.1 Diseño | Problema, objetivo, variables, arquitectura y validación temporal | Acreditar continuidad con EPE 2 y contexto real |
| 3.2 App interactiva | Formulario Flask con mensajes y resultado | Ejecutar tareas con usuarios y corregir hallazgos |
| 4.1 API | FastAPI, /predict, /health y /docs | Capturar demostración propia y explicar contrato |
| 4.3 Funcionalidad y optimización | Comparación de modelos, pruebas y carga local | Repetir en equipo de entrega y justificar límites |

## Secuencia de trabajo

1. Completar nombre, sección, docente y fecha en los entregables.
2. Contrastar el problema con la EPE 2. Delimitar demanda por zona, productos incluidos, horizonte y decisión empresarial.
3. Obtener registros autorizados con fecha, zona, promoción y demanda. Documentar faltantes, duplicados, cambios de stock y días sin operación. Conservar datos privados fuera del repositorio.
4. Adaptar la lectura del dataset en `train_model.py`, calcular rezago de siete días dentro de cada zona con calendario completo y repetir el experimento. No presentar datos sintéticos como reales.
5. Ejecutar API, web, pruebas y carga. Guardar registros, capturas y versiones del entorno. Actualizar métricas en informe y slides si cambia el experimento.
6. Realizar protocolo de usabilidad y registrar resultados. Corregir la interfaz y repetir tareas que fallen.
7. Desarrollar el análisis del informe hasta completar 10–15 páginas sustantivas de desarrollo. La maqueta reserva 10 páginas; los espacios de trabajo no sustituyen contenido evaluable.
8. Publicar código en GitHub y comprobar desde un clon limpio. Añadir URL real. Exportar versión final del informe a PDF y revisar paginación.
9. Ensayar una exposición de 6–8 minutos con demostración, resultados, límites y próximos pasos.

## Protocolo de usabilidad pendiente

Reclutar 3–5 participantes representativos y explicar que se evalúa el sistema. No anotar datos personales innecesarios. Solicitar autorización antes de grabar. Cada participante realiza sin ayuda: (a) predicción para zona 2 y un día indicado, (b) cambio de promoción y nueva predicción, (c) recuperación ante campo histórico vacío o inválido, (d) interpretación de unidades y aviso de datos sintéticos. Registrar éxito, segundos, errores y claridad de 1 a 5. Metas propuestas: al menos 80% de tareas completas y mediana inferior a 60 segundos; deben acordarse antes de la prueba y no se presentan como resultados.

| Participante anónimo | Tarea | Éxito | Segundos | Errores | Claridad 1–5 | Observación |
|---|---|---|---|---|---|---|
| Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |

## Evidencia mínima

Captura del formulario con resultado, documentación /docs, solicitud y respuesta de API, salida de pytest, métricas con fecha y origen de datos, carga con concurrencia y percentiles, resultados de usabilidad y URL del repositorio. No utilizar los valores 7.09, 9.25 o 120.8 del borrador sin reproducirlos.

## Criterio de aceptación propuesto

Comparar MAE del modelo con la persistencia semanal; registrar RMSE para errores grandes y R² como medida complementaria. No convertir MAE directamente a un porcentaje de ahorro o de precisión. El umbral de error aceptable depende de costo de quiebre, costo de sobrestock y volumen de cada zona. Evaluar estos costos con la empresa antes de afirmar beneficios.
