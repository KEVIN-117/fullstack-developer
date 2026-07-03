# Checklist - Stage 11: History Persistence

Lista de tareas para completar la persistencia del historial en disco:

- [ ] **1. Ubicación Dinámica del Archivo**
  - [ ] Obtener la ruta del directorio home (`$HOME` o `%USERPROFILE%`).
  - [ ] Definir el nombre del archivo de persistencia (e.g. `.shell_history`).
  - [ ] Resolver la ruta de fallback si la variable de entorno de usuario no está disponible.

- [ ] **2. Carga Inicial al Arrancar (Bootstrap)**
  - [ ] Validar la existencia previa del archivo de historial antes de intentar leerlo.
  - [ ] Leer secuencialmente el archivo línea a línea.
  - [ ] Poblar el historial interactivo en memoria con los registros leídos.
  - [ ] Aplicar un límite de importación seguro para no desbordar la memoria o ralentizar el shell.

- [ ] **3. Guardado al Finalizar (Tear Down)**
  - [ ] Conectar la función de escritura al built-in `exit`.
  - [ ] Conectar la función de escritura a la intercepción de `Ctrl+D` (EOF).
  - [ ] Asegurar la persistencia si el shell recibe señales de apagado no forzadas (como `SIGTERM`).

- [ ] **4. Modo de Adición (Append Mode)**
  - [ ] Abrir el archivo utilizando la bandera de adición (`append` / `>>`) para no truncar la actividad previa de otras sesiones.
  - [ ] Escribir únicamente los comandos agregados durante la sesión actual (llevar un control del índice inicial).

- [ ] **5. Tolerancia y Robustez**
  - [ ] Proteger el código con bloques try-catch o verificaciones de errores en la apertura de archivos.
  - [ ] Garantizar el funcionamiento íntegro del shell ante fallos de escritura de historial (e.g. disco lleno, falta de permisos).
