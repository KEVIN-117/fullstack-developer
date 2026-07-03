# Stage 05: Command Completion (Autocompletado de Comandos)

## 📋 Descripción
En este stage, harás que tu shell sea interactivo. Implementarás el autocompletado de comandos con la tecla Tabulación (`Tab`). Para lograrlo, deberás configurar la terminal en **Modo Raw** (crudo), lo que te permitirá interceptar caracteres individuales antes de que se envíen a la entrada estándar tradicional buffered. Resolverás comandos internos y archivos ejecutables de la variable `$PATH` en tiempo real basándote en la entrada parcial introducida por el usuario.

## 🎯 Objetivos de Aprendizaje
- Configurar y restaurar estados de terminal usando la estructura `termios`.
- Capturar e interpretar bytes en tiempo real desde `stdin` (sin esperar nueva línea).
- Comparar cadenas por prefijo común y calcular sugerencias dinámicas.
- Manejar la salida y el control del cursor usando secuencias de escape ANSI.

## 🛠️ Requerimientos Técnicos
- **Modo Raw**: Deshabilitar `ICANON` y `ECHO` en la terminal.
- **Autocompletado de Built-ins**: Si el prefijo parcial coincide con el inicio de comandos incorporados (e.g. `ec` -> `echo`), autocompletar añadiendo el resto de la palabra y un espacio al final.
- **Autocompletar Ejecutables del PATH**: Escanear los directorios de `$PATH` para buscar ejecutables que comiencen con el prefijo introducido.
- **Múltiples Opciones**: Si hay más de una coincidencia exacta, al presionar `Tab` por segunda vez se deben imprimir todas las opciones disponibles en una nueva línea y redibujar el prompt actual con el prefijo guardado.
- **Autocompletados Parciales / Sin Coincidencia**:
  - Si no hay coincidencias, emitir un sonido de campana (`\a`).
  - Si hay coincidencias múltiples pero comparten un prefijo común más largo (e.g. `para` y `parametro` -> prefijo común `para`), autocompletar hasta ese prefijo común y pitar si hay ambigüedad residual.

## 📖 Guía de Implementación Paso a Paso

1. **Implementar el Control de Entrada Interactiva**:
   Escribe un bucle de lectura carácter a carácter en lugar del `readline` por defecto. Acumula los caracteres imprimibles en un búfer en memoria y restáuralos manualmente en la pantalla (ya que `ECHO` está desactivado).
2. **Interceptar el Carácter `Tab` (`\t` / `0x09`)**:
   Cuando se detecte un tabulador, analiza el búfer de entrada actual. Si es la primera palabra, estamos autocompletando un comando.
3. **Buscar Candidatos**:
   Compara el texto acumulado con la lista de built-ins y escanea los directorios en `$PATH` buscando coincidencias.
4. **Resolver e Imprimir**:
   - **Una sola coincidencia**: Escribe el texto restante en la consola seguido de un espacio.
   - **Varias coincidencias**: Determina el prefijo común más largo entre todas las opciones. Extiende la línea del usuario hasta ese prefijo. Si se presiona `Tab` dos veces consecutivas, salta de línea, imprime las opciones separadas por espacios, y en una nueva línea vuelve a imprimir el prompt `$ ` y el texto del búfer actual.
5. **Restaurar la Terminal**:
   Asegúrate de interceptar la salida (e.g. `Ctrl+C`, `exit`) para restablecer siempre el modo canónico.
