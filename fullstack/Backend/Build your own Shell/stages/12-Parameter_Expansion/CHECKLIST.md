# Checklist - Stage 12: Parameter Expansion

Lista de tareas para completar el motor de variables y expansiones de parámetros:

- [ ] **1. Almacenamiento Local de Variables**
  - [ ] Implementar la estructura en memoria (diccionario/mapa) para guardar variables locales del shell.
  - [ ] Mantener separadas las variables locales de las variables de entorno heredadas por el sistema.

- [ ] **2. Comando Integrado `declare` y Asignaciones**
  - [ ] Implementar el built-in `declare` y dar soporte a asignaciones simples de la forma `var=valor`.
  - [ ] Validar nombres de variables (e.g. no empezar con números, sin caracteres especiales inválidos).
  - [ ] Imprimir un error descriptivo ante nombres de variable inválidos sin detener el shell.

- [ ] **3. Expansión Básica de Parámetros (`$`)**
  - [ ] Detectar el símbolo `$` y extraer el identificador subsiguiente.
  - [ ] Buscar la coincidencia en las variables locales y, de no existir, en las variables de entorno del sistema (`getenv`).
  - [ ] Sustituir la variable en la cadena del comando antes del proceso de ejecución.

- [ ] **4. Expansión con Llaves (`${}`)**
  - [ ] Soportar la delimitación por llaves de la variable para resolver ambigüedades.
  - [ ] Sustituir `${var}` de forma correcta aun si tiene texto contiguo sin espacios.

- [ ] **5. Gestión de Variables Inexistentes o Vacías**
  - [ ] Garantizar que las variables no definidas se expandan a una cadena vacía.
  - [ ] Verificar que no queden rastros del nombre de la variable no definida en los argumentos finales pasados a los comandos.
