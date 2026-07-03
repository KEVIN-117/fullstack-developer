# Stage 11: History Persistence (Persistencia del Historial)

## 📋 Descripción
En este stage, harás que el historial de tu shell persista más allá de la vida del proceso actual. Implementarás la lectura y escritura automatizada del historial en un archivo de configuración ubicado en el directorio de inicio del usuario (como `.bash_history` o `.sh_history`). Aprenderás a estructurar archivos de log planos y a controlar los flujos de inicio y salida ordenada del programa.

## 🎯 Objetivos de Aprendizaje
- Interactuar con archivos a nivel del sistema (lectura línea a línea y escritura al final del archivo).
- Definir ciclos de vida de arranque (Startup) y finalización (Shutdown) en una aplicación de consola.
- Controlar errores de permisos de archivos y directorios de forma segura (graceful degradation).

## 🛠️ Requerimientos Técnicos
- **Ruta del Historial**: Utilizar una ruta persistente por defecto basada en el directorio del usuario (e.g. `$HOME/.sh_history` o `%USERPROFILE%\.sh_history`).
- **Carga al Iniciar (Startup)**: Al arrancar el shell, abrir el archivo en modo lectura, procesar cada línea como un comando histórico separado y poblar la lista del historial en memoria.
- **Escritura / Guardado al Salir (Shutdown)**:
  - Al ejecutar `exit` o recibir `EOF` (Ctrl+D), escribir todas las nuevas entradas agregadas durante la sesión activa en el archivo del historial.
  - Soportar el modo **Adición** (Appending) para evitar sobrescribir comandos de sesiones concurrentes abiertas en otras terminales.

## 📖 Guía de Implementación Paso a Paso

1. **Definir el Archivo de Historial**:
   Resuelve la ruta absoluta del archivo de destino al arrancar. Si `$HOME` no está definido, puedes caer en una ruta relativa en el directorio actual (e.g., `./.shell_history`).
2. **Cargar el Historial**:
   - Intenta abrir el archivo. Si no existe, ignora la operación de lectura en lugar de lanzar una excepción catastrófica.
   - Lee el archivo línea por línea y guárdalo en tu estructura de memoria de la etapa anterior. Limita el número de líneas importadas para evitar retrasos de inicio si el archivo de historial es muy grande (e.g., un límite de 1000 líneas).
3. **Guardado en la Salida**:
   - Registra el guardado en la función de tu built-in `exit` y en la lógica que captura el carácter `EOF` (Ctrl+D).
   - Abre el archivo del historial en modo adición (`O_APPEND` o similar en tu lenguaje de programación).
   - Escribe los comandos nuevos y cierra el archivo correctamente.
4. **Resistencia a Fallos**:
   Asegúrate de que si el usuario ejecuta tu shell sin permisos de escritura en su directorio personal, el programa siga funcionando omitiendo la persistencia sin crashear.
