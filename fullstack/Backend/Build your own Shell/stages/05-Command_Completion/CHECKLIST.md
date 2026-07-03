# Checklist - Stage 05: Command Completion

Lista de tareas para completar el autocompletado básico de comandos:

- [ ] **1. Activación de Modo Raw**
  - [ ] Implementar la modificación de atributos de terminal (`ICANON`, `ECHO`) al arrancar.
  - [ ] Garantizar la restauración de la terminal al recibir señales de cierre o al salir.
  - [ ] Reemplazar la lectura bloqueante de líneas por lectura carácter a carácter (`read` de 1 byte).

- [ ] **2. Intercepción y Búfer Manual**
  - [ ] Almacenar caracteres en un búfer dinámico de texto para la línea de entrada actual.
  - [ ] Soportar y redibujar teclas normales imprimibles en la pantalla de forma manual.
  - [ ] Soportar el borrado de caracteres con Backspace (`\x7f` o `\b`) moviendo el cursor y limpiando el carácter.

- [ ] **3. Autocompletado de Comandos Integrados**
  - [ ] Detectar la tecla Tabulación (`0x09`).
  - [ ] Filtrar los built-ins (`exit`, `echo`, `type`, `pwd`, `cd`) que coincidan con el prefijo parcial de la primera palabra.
  - [ ] Completar automáticamente y añadir un espacio de cierre si hay una única coincidencia.

- [ ] **4. Autocompletado del PATH**
  - [ ] Escanear directorios del `$PATH` cuando se presione Tab y la primera palabra sea parcial.
  - [ ] Filtrar los nombres de archivos ejecutables que coincidan con el prefijo.
  - [ ] Ignorar archivos no ejecutables si tu sistema operativo lo requiere.

- [ ] **5. Gestión de Coincidencias Múltiples y Sonido**
  - [ ] Calcular el prefijo común más largo (LCP) de múltiples coincidencias y autocompletar hasta allí.
  - [ ] Emitir la campana de alerta (`\a`) si no existen opciones de autocompletado o si hay ambigüedad.
  - [ ] Imprimir la lista de comandos candidatos al presionar Tab dos veces, redibujando la entrada intacta después.
