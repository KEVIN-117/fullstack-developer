# Stage 01: Core Commands (Conceptos Básicos)

## 📋 Descripción
En este stage inicial, construirás los cimientos de tu propio shell. Diseñarás el bucle de lectura-evaluación-impresión (REPL), aprenderás a imprimir un prompt básico, gestionarás comandos que no son válidos, implementarás los comandos internos obligatorios (`exit`, `echo` y `type`), y darás los primeros pasos para buscar ejecutables en el sistema utilizando la variable `$PATH` para ejecutarlos en subprocesos.

## 🎯 Objetivos de Aprendizaje
- Comprender el flujo de un ciclo REPL interactivo.
- Gestionar descriptores estándar (`stdin`, `stdout`, `stderr`).
- Aprender la diferencia fundamental entre comandos integrados (built-in) y comandos externos.
- Analizar y consultar variables de entorno (específicamente `$PATH`).
- Crear procesos hijos usando `fork` y reemplazar su contexto de memoria con un ejecutable usando la familia `exec`.

## 🛠️ Requerimientos Técnicos
- **Bucle de Entrada**: Imprimir un prompt `$ ` (con un espacio al final) y leer líneas completas de forma continua.
- **Flujo de Error**: Si el comando no se reconoce y no es un built-in, imprimir `[comando]: command not found`.
- **Built-in `exit`**: Salir del shell con código de estado `0` al escribir `exit 0`.
- **Built-in `echo`**: Imprimir los argumentos pasados separados por un espacio, seguidos de una nueva línea.
- **Built-in `type`**: Identificar si un comando es un built-in (`[comando] is a shell builtin`) o un ejecutable externo indicando su ruta completa (`[comando] is [ruta]`), o si no existe.
- **Resolución de Ejecutables externos**: Analizar la variable `$PATH` usando el carácter separador `:` (o `;` en Windows si aplica) para buscar el archivo ejecutable.
- **Ejecución básica**: Usar `fork` y `exec` para ejecutar el programa externo encontrado y esperar de forma síncrona a que termine.

## 📖 Guía de Implementación Paso a Paso

1. **Estructurar el REPL**:
   Implementa un bucle infinito que imprima el prompt sin nueva línea (asegúrate de hacer flush a stdout si tu lenguaje de programación realiza buffer automático) y lee una línea desde la entrada estándar.
2. **Implementar el comando `exit`**:
   Si la entrada es exactamente `exit 0`, termina el programa.
3. **Manejar comandos inválidos**:
   Si la entrada no coincide con ningún comando conocido, escribe `[comando]: command not found`.
4. **Implementar `echo`**:
   Analiza la entrada. Si comienza con `echo `, imprime el resto de la cadena.
5. **Implementar `type` e Integrar `$PATH`**:
   - Para resolver comandos con `type`, primero comprueba si es `exit`, `echo` o `type` mismo.
   - Si no lo es, divide el valor de la variable de entorno `$PATH` y verifica si existe un archivo ejecutable con el nombre del comando en alguno de esos directorios.
6. **Ejecutar programas externos**:
   Cuando encuentres un comando válido en `$PATH`, crea un nuevo proceso utilizando `fork()` o las abstracciones equivalentes en tu lenguaje (e.g. `std::process::Command` en Rust, `subprocess` en Python, `child_process` en Node.js) y espera a que termine su ejecución.
