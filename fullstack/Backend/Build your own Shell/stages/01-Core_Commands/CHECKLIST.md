# Checklist - Stage 01: Core Commands

Lista de tareas para completar los fundamentos básicos de tu shell:

- [x] **1. Inicialización y Prompt**
  - [x] Imprimir el prompt `$ ` de forma correcta.
  - [ ] Forzar el vaciado del búfer de salida estándar (`flush`).
  - [x] Leer entrada de usuario de forma básica bloqueante por líneas.

- [x] **2. Manejo de Comandos Inválidos y Salida**
  - [x] Implementar la salida limpia al escribir `exit 0`.
  - [x] Responder con `[comando]: command not found` cuando un comando no es válido.

- [x] **3. Comando Integrado `echo`**
  - [x] Reconocer y parsear argumentos para `echo`.
  - [x] Imprimir la salida seguida de una nueva línea.

- [ ] **4. Búsqueda en el PATH y Ejecución**
  - [ ] Leer la variable de entorno `$PATH`.
  - [ ] Implementar un buscador que localice archivos ejecutables en directorios de `$PATH`.
  - [ ] Utilizar llamadas del sistema para iniciar ejecutables externos con argumentos.
  - [ ] Esperar a que el proceso hijo finalice antes de volver a mostrar el prompt.

- [ ] **5. Comando Integrado `type`**
  - [ ] Dar soporte para identificar built-ins (`exit`, `echo`, `type`).
  - [ ] Dar soporte para identificar ejecutables de `$PATH` (e.g. `type cat` -> `cat is /bin/cat`).
  - [ ] Devolver un error controlado si no se encuentra en el shell ni en el `$PATH`.
