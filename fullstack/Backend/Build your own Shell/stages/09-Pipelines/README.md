# Stage 09: Pipelines (Tuberías)

## 📋 Descripción
En este stage, implementarás una de las características más potentes de la filosofía Unix: la composición de comandos mediante tuberías (`|`). Aprenderás a encadenar procesos haciendo que la salida estándar (`stdout`) de un comando sea redirigida a la entrada estándar (`stdin`) del siguiente. Trabajarás con buffers de comunicación a nivel de kernel y coordinarás la vida de múltiples subprocesos concurrentes.

## 🎯 Objetivos de Aprendizaje
- Comprender la comunicación unidireccional entre procesos mediante descriptores de tubería.
- Utilizar llamadas al sistema como `pipe` para abrir canales de comunicación.
- Coordinar múltiples procesos hijos creados a partir de un único comando del usuario.
- Evitar bloqueos permanentes (deadlocks) cerrando descriptores redundantes en los procesos correctos.

## 🛠️ Requerimientos Técnicos
- **Operador Tubería (`|`)**: Detectar y separar la entrada en múltiples subcomandos individuales divididos por el carácter de barra vertical.
- **Tuberías de Dos Comandos**: Ejecutar comandos como `ls | grep txt`, de forma que el primer proceso escriba en la tubería y el segundo lea de ella.
- **Tuberías de Múltiples Comandos**: Dar soporte para encadenar tres o más comandos secuencialmente (e.g. `cat file.txt | grep error | wc -l`).
- **Integración con Built-ins**: Permitir que comandos incorporados internos puedan participar en la tubería tanto a la izquierda como a la derecha (e.g., `echo "hola" | grep h` o `cat file.txt | pwd`).

## 📖 Guía de Implementación Paso a Paso

1. **Analizar la Entrada de la Tubería**:
   Divide la línea de comandos en tokens utilizando `|` como delimitador principal. Esto te dará un array de comandos (e.g. `[["cat", "file.txt"], ["grep", "error"], ["wc", "-l"]]`).
2. **Ciclo de Creación de Pipes**:
   Si tienes $N$ comandos, necesitarás crear $N - 1$ tuberías utilizando la llamada `pipe(fd)`.
3. **Encadenamiento de Procesos**:
   Itera a través de los subcomandos lanzando un `fork()` para cada uno:
   - Para el **primer proceso**: Su entrada estándar es la original de la terminal. Su salida debe redirigirse al extremo de escritura del primer pipe (`dup2(pipe_fds[1], 1)`).
   - Para **procesos intermedios** ($i$): Su entrada estándar debe leer desde el extremo de lectura del pipe anterior (`dup2(prev_pipe_fds[0], 0)`). Su salida debe escribir en el extremo de escritura del siguiente pipe (`dup2(next_pipe_fds[1], 1)`).
   - Para el **último proceso**: Su entrada lee del extremo de lectura del último pipe (`dup2(last_pipe_fds[0], 0)`). Su salida estándar es la de la terminal.
4. **Regla Crítica: Cerrar Descriptores Sobrantes**:
   Cada proceso hijo y el propio padre deben cerrar inmediatamente todos los descriptores de lectura y escritura de pipes que no vayan a usar directamente. Si el extremo de escritura de un pipe permanece abierto en el proceso padre, el proceso lector nunca recibirá la señal de fin de archivo (`EOF`) y se colgará esperando entrada de forma indefinida.
5. **Espera de Resultados**:
   El shell padre debe llamar a `waitpid` para todos los hijos iniciados en el pipeline antes de volver a mostrar el prompt.
