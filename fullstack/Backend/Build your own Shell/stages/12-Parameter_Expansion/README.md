# Stage 12: Parameter Expansion (Expansión de Parámetros)

## 📋 Descripción
En esta última etapa, implementarás el motor de variables locales del shell y expandirás parámetros en la línea de entrada. Diseñarás almacenamiento para variables que no necesariamente se exportan al entorno del sistema operativo. Desarrollarás el comando integrado `declare`, validarás identificadores y soportarás expansiones complejas con y sin llaves.

## 🎯 Objetivos de Aprendizaje
- Distinguir entre variables locales del shell y variables globales del entorno (Environment Variables).
- Aplicar expresiones regulares o autómatas simples para validar nombres de variables válidos.
- Implementar algoritmos de sustitución de texto en la fase previa del análisis léxico.
- Comprender el orden de evaluación del shell (expansión de parámetros antes de la tokenización final).

## 🛠️ Requerimientos Técnicos
- **Comando Built-in `declare`**: Permite definir variables locales (e.g. `declare mi_var="valor"`).
- **Asignaciones Directas**: Soportar la sintaxis standard de asignación directa sin espacios (e.g. `mi_var=valor`).
- **Validación de Identificadores**: Los nombres de variables solo pueden contener caracteres alfanuméricos y guiones bajos (`_`), y no pueden comenzar con un número. Si es inválido, devolver `declare: not a valid identifier`.
- **Expansión de Variables (`$`)**:
  - `echo $mi_var`: Reemplazar `$mi_var` por su valor almacenado.
  - `${mi_var}`: Soportar la notación de llaves para evitar ambigüedades con caracteres contiguos (e.g. `${mi_var}TextoExtra`).
- **Variables no Definidas / Vacías**: Si la variable no existe en la tabla de variables del shell ni en el entorno global del sistema, se debe expandir a una cadena vacía (eliminando la subcadena `$variable` de la entrada final).

## 📖 Guía de Implementación Paso a Paso

1. **Diseñar el Almacén de Variables**:
   Implementa un mapa hash interno para las variables locales del shell (`shell_variables`).
2. **Implementar las Asignaciones**:
   - Detecta si la entrada coincide con el patrón `nombre=valor` o es invocada con `declare nombre=valor`.
   - Verifica las reglas de nomenclatura (primer carácter no numérico, solo letras, números o `_`).
   - Si la validación es correcta, inserta o actualiza la clave en tu mapa `shell_variables`.
3. **Analizar la Expansión de Parámetros**:
   - Antes de tokenizar los argumentos para ejecutarlos, escanea la entrada buscando el carácter `$`.
   - Si está seguido de `{`, busca la llave de cierre `}` y extrae el nombre dentro (e.g. `${var}`).
   - Si no tiene llaves, lee los caracteres alfanuméricos y `_` subsiguientes para determinar el nombre de la variable (e.g. `$var`).
4. **Resolver los Valores**:
   - Primero busca en el mapa interno `shell_variables`.
   - Si no está, busca en el entorno global de tu proceso llamando a `getenv` o su equivalente.
   - Si sigue sin estar definido, el valor resultante es una cadena vacía `""`.
5. **Reemplazar y Evaluar**:
   Sustituye la ocurrencia de la variable por su valor resuelto en la cadena original y luego continúa con el parsing de comillas y ejecución usuales.
