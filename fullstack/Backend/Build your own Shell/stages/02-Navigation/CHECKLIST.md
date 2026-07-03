# Checklist - Stage 02: Navigation

Lista de tareas para completar el soporte de navegación en tu shell:

- [ ] **1. Comando Integrado `pwd`**
  - [ ] Invocar la función del sistema de archivos para obtener el directorio actual de forma dinámica.
  - [ ] Formatear e imprimir la ruta absoluta actual en la salida estándar.

- [ ] **2. Comando Integrado `cd` (Rutas Absolutas)**
  - [ ] Parsear el argumento de `cd`.
  - [ ] Reconocer y cambiar de directorio con rutas absolutas usando `chdir` o equivalente.
  - [ ] Validar que un directorio no existente devuelva el error esperado y mantenga el CWD previo.

- [ ] **3. Comando Integrado `cd` (Rutas Relativas)**
  - [ ] Navegar correctamente a subdirectorios relativos (e.g. `cd src`).
  - [ ] Navegar correctamente hacia atrás usando directorios especiales (e.g. `cd ..`, `cd ../..`).

- [ ] **4. Expansión de Directorio Personal (`~`)**
  - [ ] Leer la variable de entorno `$HOME` (o `USERPROFILE` en Windows).
  - [ ] Permitir a `cd` sin argumentos o con `cd ~` navegar al directorio personal.
  - [ ] Resolver correctamente rutas anidadas que inician con el símbolo (e.g. `cd ~/proyectos`).
