# Stage 10: History (Historial)

## 📋 Descripción
En este stage, añadirás memoria a tu shell para retener los comandos introducidos por el usuario durante la sesión activa. Desarrollarás el comando integrado `history` para consultar registros y limitar el número de resultados mostrados. Además, implementarás navegación interactiva por el historial utilizando las teclas de flechas Arriba (`↑`) y Abajo (`↓`) y darás soporte al re-ejecución mediante expansión de exclamación (`!`).

## 🎯 Objetivos de Aprendizaje
- Diseñar una estructura de datos de búfer circular o lista lineal para el almacenamiento de cadenas de texto.
- Gestionar y reescribir la consola interactiva en tiempo real utilizando códigos de escape ANSI.
- Interpretar secuencias de escape de teclado complejas (secuencias multiocteto de teclas de dirección).
- Implementar expansiones de texto en la fase de pre-procesamiento del analizador.

## 🛠️ Requerimientos Técnicos
- **Búfer de Historial**: Almacenar en memoria una lista de comandos ejecutados en orden cronológico (excluyendo entradas en blanco sucesivas).
- **Comando Built-in `history`**:
  - `history`: Lista todos los comandos del historial numerados consecutivamente (e.g. `  1  ls\n  2  cd src\n`).
  - `history [N]`: Muestra únicamente los últimos `N` comandos registrados.
- **Navegación Interactiva**:
  - Al presionar **Flecha Arriba (`\x1b[A`)**: Reemplaza el texto en pantalla por el comando anterior en el historial. Permite presionar repetidamente para viajar atrás en el tiempo.
  - Al presionar **Flecha Abajo (`\x1b[B`)**: Viaja hacia adelante en el historial. Si se sobrepasa la entrada más reciente, limpia la entrada a una línea en blanco (o restaura el borrador que el usuario estaba editando).
- **Expansiones del Historial (`!`)**:
  - `!!`: Se reemplaza por el último comando de inmediato antes de ejecutarse.
  - `!n`: Se reemplaza por el comando en la posición número `n` del historial.

## 📖 Guía de Implementación Paso a Paso

1. **Estructura de Historial en Memoria**:
   Define un vector o lista dinámica de cadenas de texto `history_list`. Añade una entrada al final de esta estructura cada vez que el usuario presione Enter con un comando no vacío.
2. **Implementar el comando `history`**:
   Suma el comando a tus built-ins. Al ser llamado, recorre e imprime el índice y el comando. Soporta el argumento opcional de filtrado numérico.
3. **Capturar las Teclas de Flecha**:
   En tu bucle de lectura de caracteres en modo Raw, debes procesar secuencias de escape:
   - Al recibir el byte de escape `\x1b` (`27`), verifica si le siguen `[` y luego `A` (Flecha Arriba) o `B` (Flecha Abajo).
4. **Reescribir la Consola**:
   Cuando cambies de comando del historial:
   - Borra la línea de entrada actual de la terminal. Puedes usar códigos ANSI como:
     - `\r` (Retorno de carro: mueve cursor al inicio de la línea).
     - `\x1b[K` (Borra el contenido de la línea desde el cursor hasta el final).
   - Escribe el nuevo prompt y la cadena histórica seleccionada.
   - Actualiza el búfer de entrada en memoria del shell y la posición del cursor de edición.
5. **Implementar Expansiones de Exclamación**:
   Antes del análisis léxico y tokenización, escanea el texto crudo del usuario. Reemplaza cualquier ocurrencia de `!!` o `!n` por su valor equivalente del historial de comandos y muestra el comando expandido antes de ejecutarlo.
