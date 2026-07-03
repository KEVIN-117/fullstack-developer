# Checklist - Stage 10: History

Lista de tareas para completar el historial interactivo y las expansiones:

- [ ] **1. Estructura de Historial en Memoria**
  - [ ] Crear un almacén (array/lista) para comandos históricos.
  - [ ] Guardar la línea de comando exitosa de forma ordenada al presionar Enter.
  - [ ] Evitar duplicar entradas consecutivas en el historial.

- [ ] **2. Comando Integrado `history`**
  - [ ] Implementar el built-in `history` con visualización formateada con índices.
  - [ ] Soportar el filtrado limitador numérico (e.g. `history 5` muestra solo los últimos 5).

- [ ] **3. Intercepción de Teclas de Flecha**
  - [ ] Reconocer secuencias de escape multiocteto de teclado (`\x1b[A` y `\x1b[B`).
  - [ ] Llevar el índice del historial actual mientras el usuario navega arriba/abajo.
  - [ ] Guardar el comando en borrador que el usuario estaba editando antes de presionar Flecha Arriba para poder restaurarlo con Flecha Abajo.

- [ ] **4. Redibujado de Pantalla ANSI**
  - [ ] Limpiar la línea de comandos de forma limpia con secuencias ANSI (`\r` y `\x1b[K`).
  - [ ] Imprimir el comando recuperado del historial en el prompt sin desorganizar la terminal.
  - [ ] Actualizar el búfer de entrada interno y sincronizar la posición lógica del cursor.

- [ ] **5. Expansiones de Exclamación (`!`)**
  - [ ] Identificar `!!` y `!n` en la cadena de entrada inicial antes de tokenizar.
  - [ ] Reemplazar las expansiones con el texto del historial respectivo.
  - [ ] Imprimir por consola la línea resultante antes de proceder a evaluarla.
