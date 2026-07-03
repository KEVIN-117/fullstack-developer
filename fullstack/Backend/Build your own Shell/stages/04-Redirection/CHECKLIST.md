# Checklist - Stage 04: Redirection

Lista de tareas para completar el soporte de redirección de archivos:

- [ ] **1. Identificación y Remoción de Operadores**
  - [ ] Buscar operadores en la línea de comandos tokenizada (`>`, `>>`, `1>`, `2>`, `1>>`, `2>>`).
  - [ ] Validar que haya un argumento de destino inmediatamente después del operador.
  - [ ] Limpiar los argumentos finales de ejecución removiendo el operador y el archivo.

- [ ] **2. Redirección de Salida Estándar (stdout)**
  - [ ] Soportar `>` y `1>`.
  - [ ] Abrir el archivo destino en modo escritura-creación-truncado (sobrescritura).
  - [ ] Duplicar el descriptor usando `dup2` sobre el descriptor `1` en el proceso hijo.

- [ ] **3. Redirección de Error Estándar (stderr)**
  - [ ] Soportar `2>`.
  - [ ] Abrir el archivo destino en modo escritura-creación-truncado (sobrescritura).
  - [ ] Duplicar el descriptor usando `dup2` sobre el descriptor `2` en el proceso hijo.

- [ ] **4. Adjuntar Contenidos (Appending)**
  - [ ] Soportar `>>` y `1>>` para stdout en modo adición.
  - [ ] Soportar `2>>` para stderr en modo adición.
  - [ ] Validar la apertura con flags de creación y adición (`O_APPEND`).

- [ ] **5. Limpieza de Descriptores**
  - [ ] Asegurarse de que el descriptor del archivo abierto se cierra adecuadamente en el hijo y no se mantiene abierto en el padre.
