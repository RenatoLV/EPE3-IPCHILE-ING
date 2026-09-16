# Continuar NexaFlow desde otro equipo

Todo el código, los datos sintéticos, el modelo, las métricas, las capturas, la pauta y los entregables Word/PDF/PowerPoint están en `main` de [GitHub](https://github.com/RenatoLV/EPE3-IPCHILE-ING). El entorno virtual, los cachés, los logs y los contenedores instalados pertenecen a cada computador y se reconstruyen; no hace falta copiarlos.

## Primer inicio en casa con Docker Desktop

1. Instala Git y Docker Desktop. Comprueba que Docker Desktop muestre el motor activo.
2. Abre PowerShell y ejecuta:

```powershell
git clone https://github.com/RenatoLV/EPE3-IPCHILE-ING.git
cd EPE3-IPCHILE-ING
docker compose up --build -d --wait
docker compose ps
```

3. Ambos servicios deben decir `healthy`. Abre `http://127.0.0.1:5000/` y `http://127.0.0.1:8000/docs`.
4. Los archivos académicos están en `entregables/`; la pauta, en `documentacion/`; y las capturas, en `artifacts/`.

La cuenta de Docker Desktop no transfiere automáticamente la imagen ni los contenedores del equipo anterior. El comando `docker compose up --build` los crea de nuevo a partir de los archivos de GitHub. Para detenerlos: `docker compose down`.

## Seguir editando y respaldar cambios

Antes de trabajar: `git pull origin main`. Después de cambiar código o documentos:

```powershell
git add .
git commit -m "Describe lo que cambiaste"
git push origin main
```

Para hacer `push` debes iniciar sesión en GitHub en ese equipo cuando Git lo solicite. Comprueba en la página del repositorio que el último commit y los tres archivos de `entregables/` aparezcan. No edites simultáneamente en ambos equipos sin hacer `pull` primero.

## Pendientes académicos que requieren tus datos

Completa nombre, sección, docente y fecha en Word y PowerPoint. Contrasta el diagnóstico de EPE 2 con el texto propuesto y registra la prueba de usabilidad con personas reales en `PROTOCOLO_USABILIDAD.md`. Reexporta el PDF después de editar el Word. El modelo usa datos sintéticos y las métricas no prueban mejoras reales de NexaFlow.
