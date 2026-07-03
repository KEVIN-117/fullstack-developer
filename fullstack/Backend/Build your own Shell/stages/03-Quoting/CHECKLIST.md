# Checklist - Stage 03: Quoting

Lista de tareas para completar el analizador de comillas y caracteres de escape:

- [ ] **1. Analizador Carácter a Carácter**
  - [ ] Reemplazar split por un bucle iterativo o máquina de estados sobre la cadena del comando.
  - [ ] Implementar la delimitación de argumentos respetando los diferentes estados de comillas.

- [ ] **2. Comillas Simples (`'`)**
  - [ ] Agrupar espacios embebidos dentro de comillas simples en un solo argumento.
  - [ ] Desactivar el efecto de barras invertidas u otros caracteres especiales dentro de comillas simples.
  - [ ] Implementar la remoción de comillas simples al pasar argumentos finales.

- [ ] **3. Comillas Dobles (`"`)**
  - [ ] Agrupar espacios embebidos dentro de comillas dobles en un solo argumento.
  - [ ] Implementar escapes de `\n`, `\"`, `\\` y `\$` dentro de comillas dobles.
  - [ ] Conservar otros usos de `\ ` o `\a` como caracteres literales dentro de comillas dobles.
  - [ ] Implementar la remoción de comillas dobles al pasar argumentos finales.

- [ ] **4. Barra Invertida de Escape (`\`)**
  - [ ] Escapar espacios fuera de comillas (e.g. `foo\ bar` -> 1 argumento `foo bar`).
  - [ ] Escapar comillas y la propia barra invertida fuera de comillas.

- [ ] **5. Ejecutables Entrecomillados**
  - [ ] Permitir la ejecución de comandos externos donde la ruta misma esté entrecomillada.
