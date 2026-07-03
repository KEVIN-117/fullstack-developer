# Stage 08: Background Jobs (Trabajos en Segundo Plano)

## 📋 Descripción
En este stage, harás que tu shell soporte multitarea asíncrona implementando la ejecución de procesos en segundo plano usando el operador ampersand (`&`). Aprenderás a gestionar grupos de procesos (Process Groups), evitar que las señales interrupan tus procesos asíncronos y monitorear el cambio de estado de estos mediante llamadas no bloqueantes para evitar procesos huérfanos o zombie.

## 🎯 Objetivos de Aprendizaje
- Comprender la diferencia entre procesos en primer plano (foreground) y segundo plano (background).
- Manejar grupos de procesos (`setpgid`) y sesiones de terminal.
- Capturar y procesar de forma no bloqueante la terminación de subprocesos (`waitpid` con `WNOHANG`).
- Diseñar e implementar una tabla interna de control de trabajos (Job Table).

## 🛠️ Requerimientos Técnicos
- **Operador `&`**: Si una línea de comando finaliza con el token `&`, el shell debe ejecutarlo en segundo plano.
- **Sin Bloqueo**: El shell no debe esperar a que el subproceso termine; debe imprimir inmediatamente información sobre el trabajo (e.g. `[1] 12345` donde `1` es el ID de trabajo y `12345` es el PID) y volver a mostrar el prompt.
- **Comando Built-in `jobs`**: Lista todos los trabajos activos en segundo plano con su número de trabajo, PID, estado (`Running`, `Done`, `Terminated`) y la línea de comandos ejecutada.
- **Limpieza de Zombies (Reaping)**: Detectar la terminación de los procesos en segundo plano y limpiar sus recursos. Al finalizar un proceso asíncrono, se debe imprimir un aviso en la terminal indicando que ha terminado, idealmente justo antes de redibujar el siguiente prompt.
- **Reciclaje de IDs**: Los números de trabajos (Job IDs) liberados deben ser reutilizados de manera eficiente.

## 📖 Guía de Implementación Paso a Paso

1. **Detectar el Operador `&`**:
   Durante el parsing, verifica si el último argumento es exactamente `&`. Si es así, elimina el token de la lista de argumentos y marca una bandera `run_in_background` a verdadero.
2. **Crear Grupos de Procesos Independientes**:
   En el proceso hijo generado por `fork()`, antes de ejecutar `execvp`, llama a `setpgid(0, 0)`. Esto coloca al hijo en un nuevo grupo de procesos cuya identificación coincide con su PID. Así, las señales de teclado del padre (como `Ctrl+C`) no afectarán al hijo en segundo plano.
3. **Registrar en la Tabla de Trabajos**:
   - En el proceso padre, añade el PID, el comando y el ID de trabajo a una estructura de datos interna (e.g. un array o lista enlazada).
   - Asigna el menor ID de trabajo disponible (comenzando en `1`).
4. **Verificación No Bloqueante en el REPL**:
   - En cada iteración del bucle REPL (justo antes de mostrar el prompt) y opcionalmente mediante la señal `SIGCHLD`, llama de manera iterativa a `waitpid(-1, &status, WNOHANG)`.
   - Si `waitpid` retorna un PID mayor a 0, significa que un proceso en segundo plano terminó. Busca ese PID en la tabla de trabajos, actualiza su estado a `Done`, imprime el aviso (e.g., `[1]+ Done [comando]`) y remuévelo de la tabla para liberar su ID de trabajo.
5. **Implementar el comando `jobs`**:
   Itera sobre la lista de trabajos activos e imprime la lista formateada.
