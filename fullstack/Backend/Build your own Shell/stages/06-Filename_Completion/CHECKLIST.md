# Checklist - Stage 06: Filename Completion

Lista de tareas para completar el autocompletado de archivos y directorios:

- [ ] **1. Identificación del Contexto de Argumentos**
  - [ ] Determinar si la palabra actual a autocompletar no se encuentra en la posición inicial (primer comando).
  - [ ] Extraer la subcadena del argumento parcial de forma limpia considerando espacios y posibles escapes.

- [ ] **2. Escaneo de Directorio Actual**
  - [ ] Escanear el directorio de trabajo actual (`.`) cuando el argumento no contenga barras inclinadas.
  - [ ] Filtrar los nombres de archivos que comiencen con el prefijo del argumento actual.
  - [ ] Diferenciar archivos regulares de directorios para aplicar el sufijo correspondiente (espacio frente a `/`).

- [ ] **3. Escaneo de Rutas Anidadas**
  - [ ] Dividir la entrada en directorio base y nombre parcial de archivo (e.g. `tests/test_f` -> directorio `tests/`, prefijo `test_f`).
  - [ ] Escanear directorios anidados de manera relativa o absoluta.
  - [ ] Resolver adecuadamente directorios inexistentes o sin permisos arrojando un aviso o pitido.

- [ ] **4. Gestión de Sufijos Dinámicos**
  - [ ] Anexar una barra inclinada `/` al autocompletar un directorio para continuar completando su interior de inmediato.
  - [ ] Anexar un espacio `" "` al autocompletar un archivo para indicar que se terminó el argumento actual.

- [ ] **5. Soporte de Múltiples Argumentos y Coincidencias**
  - [ ] Dar soporte para autocompletar en el segundo, tercero o enésimo argumento de un mismo comando.
  - [ ] Calcular el prefijo común entre múltiples coincidencias de archivos e imprimir las opciones al presionar Tab dos veces.
