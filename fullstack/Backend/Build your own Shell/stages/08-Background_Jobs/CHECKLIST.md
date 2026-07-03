# Checklist - Stage 08: Background Jobs

Lista de tareas para completar el control de trabajos en segundo plano:

- [ ] **1. Detección de Ejecución en Segundo Plano**
  - [ ] Validar la presencia de `&` al final del comando.
  - [ ] Remover el token `&` para que no se envíe al comando final.
  - [ ] Implementar la ramificación sin llamada bloqueante a `waitpid` síncrono en el proceso padre.

- [ ] **2. Aislamiento de Grupo de Procesos**
  - [ ] Llamar a `setpgid(0, 0)` en el proceso hijo antes de ejecutar `execvp`.
  - [ ] Asegurar que presionar Ctrl+C en el terminal del padre no mate al proceso hijo asíncrono.

- [ ] **3. Tabla Interna de Trabajos (Job Table)**
  - [ ] Crear la estructura de datos para almacenar `job_id`, `pid`, `status` y `command_string`.
  - [ ] Asignar e imprimir la estructura al lanzar un comando (e.g. `[1] 14598`).
  - [ ] Implementar un algoritmo para asignar el menor ID de trabajo disponible y reciclar IDs liberados.

- [ ] **4. Monitoreo No Bloqueante (Reaping)**
  - [ ] Implementar llamadas periódicas a `waitpid(-1, &status, WNOHANG)` en el ciclo REPL.
  - [ ] Notificar al usuario la finalización del trabajo (e.g., `[1]+ Done [comando]`).
  - [ ] Remover el proceso finalizado de la tabla de trabajos de forma segura.

- [ ] **5. Comando Integrado `jobs`**
  - [ ] Implementar la función de volcado formateado de todos los trabajos en ejecución.
  - [ ] Opcionalmente dar soporte para listar un trabajo individual específico (e.g. `jobs %1`).
