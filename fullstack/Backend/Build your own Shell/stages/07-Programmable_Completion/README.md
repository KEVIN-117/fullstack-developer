# Stage 07: Programmable Completion (Autocompletado Programable)

## 📋 Descripción
En esta etapa avanzada, dotarás a tu shell de capacidades de autocompletado dinámico e inteligente, similar a cómo funciona `bash-completion`. Implementarás el comando integrado `complete` para registrar funciones o scripts que deciden qué sugerir cuando el usuario pulsa Tab en un comando específico. Aprenderás a transferir el contexto de la línea de comandos actual a través de argumentos de ejecución y variables de entorno del sistema.

## 🎯 Objetivos de Aprendizaje
- Diseñar un registro o mapa en memoria para almacenar configuraciones de autocompletado programable.
- Ejecutar funciones o comandos del shell en subprocesos aislados para obtener opciones de autocompletado dinámicas.
- Soportar el paso de estados de contexto mediante variables de entorno estándar (e.g. `COMP_LINE`, `COMP_POINT`, `COMP_WORDS`).
- Resolver e integrar las respuestas generadas por los completadores dinámicos de forma no intrusiva.

## 🛠️ Requerimientos Técnicos
- **Comando Built-in `complete`**:
  - `complete -F [función] [comando]`: Registra que para autocompletar el `[comando]`, se debe ejecutar la `[función]` o script.
  - `complete` (sin argumentos): Lista todos los autocompletados registrados actualmente.
- **Comando Built-in `uncomplete`** / **Anulación**: Permitir anular el registro de un autocompletado específico.
- **Contexto de Autocompletado**: Al disparar el autocompletado programable, el shell debe exponer en el entorno:
  - `COMP_LINE`: La línea completa que el usuario ha escrito hasta ahora.
  - `COMP_POINT`: La posición actual del cursor (en número de caracteres).
  - `COMP_WORDS`: Un array o lista con las palabras individuales de la línea.
  - `COMP_CWORD`: El índice de la palabra en `COMP_WORDS` que contiene el cursor.
- **Manejo de Candidatos**: Leer las salidas generadas (generalmente a través de un descriptor de tubería o del stdout de la función del completador) e integrarlas en el prompt del usuario.

## 📖 Guía de Implementación Paso a Paso

1. **Diseñar el Registro de Completadores**:
   Crea una tabla hash o diccionario en la memoria del shell para asociar un nombre de comando (e.g. `git`) con su función o script de autocompletado.
2. **Implementar el Comando `complete`**:
   - Agrega lógica en los built-ins para procesar `complete`. Si se ejecuta sin parámetros, itera sobre el registro e imprime las reglas en formato `complete -F [función] [comando]`.
   - Soporta la bandera `-r` para anular un registro (e.g., `complete -r git`).
3. **Interceptar Tab para Comandos Registrados**:
   - Cuando se pulsa Tab en un argumento, verifica si el primer comando de la línea tiene una regla de autocompletado registrada.
   - Si es así, no utilices el completador genérico de archivos de la etapa 6.
4. **Ejecutar el Completador y Transferir Entorno**:
   - Crea un entorno controlado para el subproceso ejecutor.
   - Configura las variables `COMP_LINE`, `COMP_POINT`, etc.
   - Ejecuta la función o el comando asociado y captura su salida estándar.
5. **Procesar los Resultados**:
   - Convierte la salida del completador (separada por nuevas líneas) en una lista de candidatos.
   - Si hay una sola opción, escribe la coincidencia. Si hay varias, busca el prefijo común más largo, redibuja y pípalo si corresponde.
   - Si no hay resultados de salida, cae en el comportamiento por defecto (autocompletado de archivos estándar).
