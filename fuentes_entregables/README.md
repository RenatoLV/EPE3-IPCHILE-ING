# Fuentes auxiliares de los documentos

Estos scripts se conservan para poder revisar o regenerar el informe, la presentación y las capturas. No se necesitan para ejecutar la aplicación ni para abrir los DOCX/PDF/PPTX de `entregables/`.

- `make_report.py`: genera el Word a partir de métricas, ejemplos y capturas versionadas. Requiere Python con `python-docx` y Pillow. Para PDF, exportar el Word con Microsoft Word.
- `make_deck.mjs`: genera un PowerPoint editable mediante el paquete `@oai/artifact-tool` del entorno Codex. Requiere definir `CODEX_PRESENTATIONS_SKILL_DIR`, `CODEX_BUNDLED_PYTHON` y `RUNTIME_NODE_MODULES` según las rutas del equipo actual. Genera un archivo `Presentacion_EPE3_regenerada.pptx` para revisar antes de reemplazar el entregable publicado.
- `capture.mjs`: captura la web y `/docs` desde una instancia local usando Playwright y Edge. Requiere ambos servicios iniciados.
- `render_pdf.py`: genera imágenes temporales de cada página para revisar la diagramación del PDF. Requiere `pypdfium2` y Pillow.

Ejecuta los scripts desde la raíz del repositorio. Los resultados temporales se guardan en `build/`, que está excluido de Git. Las cifras y capturas del informe son de un modelo entrenado con datos sintéticos.
