# Stage 06: Filename Completion (Autocompletado de Nombres de Archivos)

## 📋 Descripción
Tras dominar el autocompletado de comandos en la primera posición de la línea de entrada, en este stage ampliarás la interactividad de tu shell para autocompletar nombres de archivos y directorios cuando el usuario escribe argumentos para un comando (e.g. `cat do` + Tab -> `cat documento.txt`). Aprenderás a determinar el contexto de la palabra actual y a escanear directorios específicos en el sistema de archivos local.

## 🎯 Objetivos de Aprendizaje
- Distinguir la posición léxica de los argumentos en una entrada del shell.
- Realizar consultas y listados dinámicos de directorios en el sistema de archivos local (`opendir`/`readdir` o equivalentes).
- Manejar caracteres especiales y convenciones de rutas de archivos (como barras inclinadas `/` para directorios).
- Soportar el autocompletado en múltiples argumentos secuenciales de una misma línea de comandos.

## 🛠️ Requerimientos Técnicos
- **Detección de Argumentos**: Si la palabra parcial en el cursor no es la primera palabra, debe autocompletarse como un archivo/directorio en lugar de un comando o ejecutable.
- **Rutas Locales y Anidadas**:
  - Si el argumento parcial no contiene `/`, buscar coincidencias en el directorio de trabajo actual (`.`).
  - Si contiene `/` (e.g. `src/ut`), aislar la ruta del directorio (`src/`) y buscar los archivos en él que comiencen con el prefijo (`ut`).
- **Autocompletar Directorios**: Si el elemento coincidente es un directorio, en lugar de añadir un espacio de separación al final del autocompletado, se debe añadir una barra inclinada `/` (e.g. `stages/`) para que el usuario pueda seguir completando elementos anidados de inmediato.
- **Múltiples Argumentos**: Soportar que un comando tenga múltiples argumentos autocompletados (e.g. `cat file1.txt file` + Tab -> `cat file1.txt file2.txt`).

## 📖 Guía de Implementación Paso a Paso

1. **Aislar la Palabra Actual (Token en el Cursor)**:
   Cuando el usuario presione Tab, analiza la posición de la palabra parcial que se está editando. Si no es la primera palabra de la línea, activa el flujo de autocompletado de archivos.
2. **Dividir Directorio y Prefijo**:
   - Analiza el token parcial. Si tiene barras diagonales (e.g. `doc/te`), divídelo en el directorio base (`doc/`) y el prefijo de archivo (`te`).
   - Si no contiene barras, el directorio base es el actual (`.`) y el prefijo es todo el token.
3. **Escanear el Directorio Base**:
   - Lee el directorio base y filtra sus entradas por aquellas que empiecen por el prefijo indicado.
   - Ignora las entradas especiales `.` y `..` a menos que el prefijo del usuario empiece explícitamente con un punto.
4. **Formatear el Autocompletado**:
   - Si el archivo encontrado es un directorio, añade `/` (o `\` en Windows). No añadas espacio.
   - Si es un archivo regular, completa el nombre y añade un espacio al final.
   - Si hay múltiples coincidencias, calcula el prefijo común más largo (LCP) y redibuja.
5. **Escribir el Texto en Pantalla**:
   Actualiza el búfer interno e inserta los caracteres autocompletados en la posición correcta de la terminal.
