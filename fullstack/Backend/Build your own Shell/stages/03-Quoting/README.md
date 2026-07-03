# Stage 03: Quoting (Uso de Comillas)

## 📋 Descripción
El analizador (parser) de tu shell se volverá más sofisticado en esta etapa. Implementarás el soporte para comillas simples (`'`), comillas dobles (`"`) y barras invertidas de escape (`\`). Aprenderás cómo estos caracteres especiales alteran el proceso de tokenización al agrupar múltiples palabras que contienen espacios en un único argumento y al evitar que ciertos caracteres sean interpretados por el shell.

## 🎯 Objetivos de Aprendizaje
- Diseñar e implementar un analizador sintáctico (lexer/parser) basado en estados.
- Diferenciar el comportamiento semántico entre comillas simples, dobles y el carácter de escape.
- Ejecutar programas cuyas rutas o argumentos contienen espacios embebidos.

## 🛠️ Requerimientos Técnicos
- **Comillas Simples (`'`)**: Todo lo que está dentro de comillas simples se trata literalmente. Ningún carácter especial (como espacios o `\`) se interpreta.
- **Comillas Dobles (`"`)**: Todo se trata literalmente excepto la barra invertida (`\`), la cual conserva su significado de escape únicamente cuando va seguida de `$`, `"`, `\`, o `\n`.
- **Barra Invertida (`\`) fuera de comillas**: Quita el significado especial al siguiente carácter (e.g. `\ ` es un espacio literal, no un separador).
- **Ejecutables Entrecomillados**: El shell debe ser capaz de ejecutar programas que tengan comillas en su propia ruta (e.g. `'/bin/my program'`).

## 📖 Guía de Implementación Paso a Paso

1. **Diseñar una Máquina de Estados (FSM)**:
   Modifica tu lógica de lectura de argumentos para iterar carácter por carácter en lugar de usar split básico:
   - **Estado Normal**: Los espacios delimitan argumentos. Si encuentras `'`, cambia al estado `SINGLE_QUOTE`. Si encuentras `"`, cambia al estado `DOUBLE_QUOTE`. Si encuentras `\`, lee el siguiente carácter literalmente.
   - **Estado Comilla Simple (`SINGLE_QUOTE`)**: Lee todo literalmente hasta encontrar otra `'`, tras la cual regresas al estado Normal.
   - **Estado Comilla Doble (`DOUBLE_QUOTE`)**: Lee todo literalmente hasta encontrar otra `"`. Si encuentras `\` seguido de `"`, `\`, `$` o `\n`, procesa el carácter de escape y añade su equivalente literal.
2. **Eliminación de Comillas (Quote Removal)**:
   Una vez tokenizados los argumentos, las comillas delimitadoras deben eliminarse antes de pasar la lista de argumentos a las llamadas de sistema de ejecución.
3. **Validación con Ejecutables**:
   Asegúrate de que un comando como `echo 'hola      mundo'` imprima `hola      mundo` (respetando los espacios), y que `echo "hola \"mundo\""` imprima `hola "mundo"`.
