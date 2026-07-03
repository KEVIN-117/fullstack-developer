# Stage 02: Navigation (Navegación)

## 📋 Descripción
En este stage, ampliarás tu shell con la capacidad de navegar a través del sistema de archivos de tu máquina. Implementarás los comandos incorporados `pwd` (print working directory) y `cd` (change directory), comprendiendo la diferencia entre rutas absolutas, relativas y el atajo para acceder al directorio personal del usuario (`~`).

## 🎯 Objetivos de Aprendizaje
- Comprender el concepto de "directorio de trabajo actual" (CWD - Current Working Directory) en sistemas operativos.
- Manejar la resolución de rutas en el sistema de archivos (absolutas vs. relativas).
- Aprender a consultar variables de entorno críticas como `$HOME` para resolver el símbolo `~`.
- Cambiar el estado del proceso actual usando la llamada de sistema `chdir`.

## 🛠️ Requerimientos Técnicos
- **Built-in `pwd`**: Imprime el directorio de trabajo absoluto actual, seguido de una nueva línea.
- **Built-in `cd`**: Modifica el directorio de trabajo del proceso del shell:
  - **Rutas Absolutas**: Si comienza con `/` (o una letra de unidad en Windows, e.g. `C:\`), navega directamente a la ubicación dada.
  - **Rutas Relativas**: Si no comienza con `/`, resuelve la ruta basándose en el directorio actual (e.g. `cd ./folder`, `cd ../parent`).
  - **Directorio Personal (`~`)**: Si el argumento es `~` o comienza con `~/`, debe expandirse a la ruta del directorio del usuario almacenado en la variable de entorno `$HOME` (o `USERPROFILE` en Windows).
- **Manejo de Errores**: Si la ruta no existe o no se puede acceder a ella, se debe imprimir `cd: [ruta]: No such file or directory` sin cambiar de directorio.

## 📖 Guía de Implementación Paso a Paso

1. **Implementar el comando `pwd`**:
   Usa la función `getcwd` o su equivalente del lenguaje de programación para recuperar y mostrar el directorio actual.
2. **Implementar `cd` con Rutas Absolutas**:
   Identifica la entrada `cd [ruta]`. Si la ruta es absoluta, intenta invocar `chdir([ruta])`. Si falla, muestra el mensaje de error correspondiente.
3. **Manejar Rutas Relativas**:
   Pasa directamente la ruta relativa a la syscall `chdir` o concaténala manualmente al directorio actual obtenido con `getcwd` para normalizarla primero.
4. **Manejar el Directorio Personal (`~`)**:
   - Detecta si el argumento del comando `cd` es exactamente `~` o si comienza con `~/`.
   - Recupera el directorio de inicio del usuario de las variables de entorno.
   - Reemplaza `~` por la ruta del directorio de inicio antes de invocar la función de cambio de directorio.
