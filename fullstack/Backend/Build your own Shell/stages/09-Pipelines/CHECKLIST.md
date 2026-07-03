# Checklist - Stage 09: Pipelines

Lista de tareas para completar la integración de tuberías:

- [ ] **1. Identificación y Parsing de Pipelines**
  - [ ] Dividir la entrada en segmentos usando el delimitador `|` respetando escapes y comillas.
  - [ ] Validar que cada segmento contenga comandos válidos y no queden tuberías vacías (e.g. `cat |`).

- [ ] **2. Inicialización de Canales (Pipes)**
  - [ ] Calcular la cantidad de tuberías necesarias ($N - 1$ para $N$ comandos).
  - [ ] Crear descriptores de lectura y escritura para cada canal usando `pipe(fds)`.

- [ ] **3. Redirección de Entradas/Salidas en Subprocesos**
  - [ ] Ejecutar `fork()` para cada subcomando.
  - [ ] Duplicar con `dup2` la salida estándar en el extremo de escritura del pipe correspondiente.
  - [ ] Duplicar con `dup2` la entrada estándar en el extremo de lectura del pipe anterior.

- [ ] **4. Gestión y Cierre Preventivo de File Descriptors**
  - [ ] Cerrar descriptores no utilizados en cada proceso hijo inmediatamente tras hacer `dup2`.
  - [ ] Cerrar todos los descriptores de pipes en el proceso padre (shell) antes de hacer `waitpid` para evitar deadlocks de EOF.

- [ ] **5. Espera Síncrona Multi-Proceso**
  - [ ] Realizar un seguimiento de todos los PIDs creados en el pipeline.
  - [ ] Esperar a todos los hijos antes de retomar la interactividad del prompt.
  - [ ] Capturar el código de retorno del último comando de la tubería como el estado global del shell.
