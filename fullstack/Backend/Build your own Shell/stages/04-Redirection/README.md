# Stage 04: Redirection (Redirección)

## 📋 Descripción
En este stage, añadirás la capacidad de redirigir los flujos de salida del shell y de los comandos externos hacia archivos físicos en el disco duro. Aprenderás a manipular descriptores de archivos (`stdout` con descriptor `1` y `stderr` con descriptor `2`), a abrir archivos con permisos específicos de sobreescritura y de adición, y a clonar estos descriptores usando llamadas al sistema de bajo nivel.

## 🎯 Objetivos de Aprendizaje
- Comprender el concepto de tabla de descriptores de archivos (File Descriptor Table) de un proceso.
- Utilizar llamadas al sistema de duplicación como `dup2`.
- Diferenciar entre la redirección destructiva/de sobreescritura (`>` o `1>`) y la no destructiva/de adición (`>>` o `1>>`).

## 🛠️ Requerimientos Técnicos
- **Redirigir stdout (`>` o `1>`)**: Redirige la salida estándar a un archivo. Si el archivo no existe, lo crea. Si existe, sobrescribe su contenido (truncándolo a tamaño cero).
- **Redirigir stderr (`2>`)**: Redirige la salida de error a un archivo. Sobrescribe el contenido si el archivo ya existe.
- **Adjuntar stdout (`>>` o `1>>`)**: Redirige la salida estándar a un archivo. Si existe, concatena/escribe al final de este en lugar de truncarlo.
- **Adjuntar stderr (`2>>`)**: Redirige el error estándar concatenando al final del archivo especificado.

## 📖 Guía de Implementación Paso a Paso

1. **Analizar Operadores de Redirección**:
   Durante el parsing, busca los operadores de redirección (`>`, `1>`, `2>`, `>>`, `1>>`, `2>>`) y sus argumentos asociados (el nombre del archivo de destino). Extrae esta información y remueve el operador y el archivo de la lista de argumentos finales del comando.
2. **Abrir Archivos de Destino**:
   Abre el archivo con las banderas adecuadas según el operador:
   - Para `>` / `1>` / `2>`: Usar flags de escritura, creación y truncado (e.g. en C: `O_WRONLY | O_CREAT | O_TRUNC`).
   - Para `>>` / `1>>` / `2>>`: Usar flags de escritura, creación y adición (e.g. en C: `O_WRONLY | O_CREAT | O_APPEND`).
3. **Reemplazar Descriptores (En el Proceso Hijo)**:
   Antes de llamar a `exec`, usa la llamada de sistema `dup2(fd_archivo, 1)` para desviar la salida estándar, o `dup2(fd_archivo, 2)` para desviar el error estándar.
4. **Limpieza**:
   Cierra el descriptor temporal `fd_archivo` una vez duplicado para evitar fugas de recursos (file descriptor leaks).
