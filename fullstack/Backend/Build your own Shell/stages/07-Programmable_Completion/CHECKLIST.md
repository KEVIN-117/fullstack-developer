# Checklist - Stage 07: Programmable Completion

Lista de tareas para completar el autocompletado programable interactivo:

- [ ] **1. Comando Integrado `complete`**
  - [ ] Implementar el registro de autocompletado dinámico (`complete -F [función] [comando]`).
  - [ ] Mostrar en formato legible las reglas existentes al invocar `complete` sin argumentos.
  - [ ] Implementar la eliminación de reglas registradas con `complete -r [comando]`.

- [ ] **2. Entorno y Contexto de Autocompletado**
  - [ ] Parsear la entrada en palabras separadas para rellenar la variable `COMP_WORDS`.
  - [ ] Calcular y exportar las variables de entorno `COMP_LINE`, `COMP_POINT`, `COMP_WORDS` y `COMP_CWORD` al subproceso de autocompletado.

- [ ] **3. Ejecución del Completador y Captura de Salida**
  - [ ] Interceptar la pulsación de Tab y desviar la petición al completador registrado.
  - [ ] Crear un pipe temporal para capturar el stdout del proceso completador ejecutable o función interna.
  - [ ] Tratar los fallos o cuelgues del completador de forma segura (con timeout o manejo de señales).

- [ ] **4. Resolución de Candidatos y Prefijos**
  - [ ] Parsear la salida estándar capturada como líneas independientes (los candidatos).
  - [ ] Calcular el prefijo común más largo (LCP) de los candidatos recibidos.
  - [ ] Insertar y redibujar el texto en la línea de comandos interactiva basándose en la coincidencia.

- [ ] **5. Manejo de Fallback**
  - [ ] Caer en el autocompletado por defecto (archivos locales) si el completador no arroja resultados o no está registrado.
