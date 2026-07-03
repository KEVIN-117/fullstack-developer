# Build Your Own Shell - Stages

Esta carpeta contiene la estructura incremental para construir tu propio intérprete de comandos (Shell) desde cero. Cada carpeta representa una etapa de desarrollo, progresando desde un bucle de lectura y ejecución simple (REPL) hasta características avanzadas como tuberías, control de trabajos y autocompletado programable.

## 📋 Estructura de Stages

### 1. **Core Commands** (Conceptos Básicos)
- Imprimir un prompt y leer la entrada del usuario.
- Manejar comandos inválidos con mensajes de error apropiados.
- Implementar un REPL (Read-Eval-Print Loop).
- Soporte para comandos incorporados integrados: `exit`, `echo` y `type`.
- Localizar archivos ejecutables usando la variable `$PATH` y ejecutar programas externos.
- [Guía detallada](01-Core_Commands/README.md)

### 2. **Navigation** (Navegación)
- Implementar el comando integrado `pwd` para obtener el directorio actual.
- Implementar `cd` soportando rutas absolutas, rutas relativas y el directorio de inicio (`~`).
- [Guía detallada](02-Navigation/README.md)

### 3. **Quoting** (Uso de Comillas)
- Manejo de comillas simples (`'`) y dobles (`"`) para preservar espacios y caracteres especiales.
- Manejo de la barra invertida (`\`) de escape tanto fuera como dentro de comillas.
- Ejecutar programas con nombres o rutas que contienen espacios usando comillas.
- [Guía detallada](03-Quoting/README.md)

### 4. **Redirection** (Redirección)
- Redirigir la salida estándar (`>` o `1>`) y de error estándar (`2>`) a archivos.
- Adjuntar/concatenar a la salida estándar (`>>` o `1>>`) y de error estándar (`2>>`).
- [Guía detallada](04-Redirection/README.md)

### 5. **Command Completion** (Autocompletado de Comandos)
- Leer teclas individuales y capturar la tecla Tabulación (`Tab`).
- Autocompletar comandos integrados y programas ejecutables en el `$PATH`.
- Manejar autocompletados parciales, múltiples coincidencias y mostrar opciones disponibles.
- [Guía detallada](05-Command_Completion/README.md)

### 6. **Filename Completion** (Autocompletado de Archivos)
- Autocompletar nombres de archivos y directorios basados en el prefijo actual.
- Autocompletar rutas anidadas y múltiples coincidencias.
- [Guía detallada](06-Filename_Completion/README.md)

### 7. **Programmable Completion** (Autocompletado Programable)
- Registrar reglas de autocompletado usando el comando `complete`.
- Consultar, listar y anular especificaciones de autocompletado.
- Pasar argumentos, variables de entorno y calcular el prefijo común más largo.
- [Guía detallada](07-Programmable_Completion/README.md)

### 8. **Background Jobs** (Trabajos en Segundo Plano)
- Iniciar procesos en segundo plano usando el operador `&`.
- Implementar el comando integrado `jobs` para listar procesos activos.
- Monitorear, finalizar y limpiar (reap) procesos en segundo plano para evitar procesos zombie.
- [Guía detallada](08-Background_Jobs/README.md)

### 9. **Pipelines** (Tuberías)
- Conectar la salida de un comando con la entrada del siguiente usando el operador tubería (`|`).
- Manejar tuberías de múltiples comandos e integración con comandos integrados.
- [Guía detallada](09-Pipelines/README.md)

### 10. **History** (Historial)
- Guardar comandos ejecutados en una lista de historial en memoria.
- Comando integrado `history` para listar y limitar el historial.
- Navegación interactiva usando las teclas de flecha Arriba (`↑`) y Abajo (`↓`).
- Ejecutar comandos del historial usando expansiones (como `!!` o `!n`).
- [Guía detallada](10-History/README.md)

### 11. **History Persistence** (Persistencia del Historial)
- Cargar el historial desde un archivo de configuración (e.g., `.sh_history`) al iniciar.
- Escribir o adjuntar nuevas entradas de historial en el archivo al salir de la sesión.
- [Guía detallada](11-History_Persistence/README.md)

### 12. **Parameter Expansion** (Expansión de Parámetros)
- Definir variables de shell usando el comando integrado `declare` o asignaciones directas.
- Validar nombres de variables e imprimir variables no definidas.
- Expandir variables con `$` y llaves `{}`.
- [Guía detallada](12-Parameter_Expansion/README.md)

---

## 🚀 Cómo Usar Esta Estructura

1. **Comienza con Core Commands**: Consigue la estructura base (el REPL, la lectura de comandos y la ejecución básica).
2. **Construye incrementalmente**: Cada etapa se basa en las APIs y estructuras de datos diseñadas en la anterior.
3. **Estructura por Stage**:
   - `README.md`: Guía de objetivos, diseño de sistemas y conceptos del sistema operativo aplicados a la etapa.
   - `CHECKLIST.md`: Tareas concretas marcadas para guiar tu avance.
   - `docs/`: Documentación técnica de diseño o APIs.
   - `tests/`: Scripts o suites de pruebas específicas para validar el stage.
   - `implementation/`: Espacio para organizar el código correspondiente a la etapa.

## ✅ Progreso General

| Stage | Descripción | Estado | Completitud |
| :--- | :--- | :---: | :---: |
| **01** | [Core Commands](01-Core_Commands/README.md) | ⏳ No iniciado | 0% |
| **02** | [Navigation](02-Navigation/README.md) | ⏳ No iniciado | 0% |
| **03** | [Quoting](03-Quoting/README.md) | ⏳ No iniciado | 0% |
| **04** | [Redirection](04-Redirection/README.md) | ⏳ No iniciado | 0% |
| **05** | [Command Completion](05-Command_Completion/README.md) | ⏳ No iniciado | 0% |
| **06** | [Filename Completion](06-Filename_Completion/README.md) | ⏳ No iniciado | 0% |
| **07** | [Programmable Completion](07-Programmable_Completion/README.md) | ⏳ No iniciado | 0% |
| **08** | [Background Jobs](08-Background_Jobs/README.md) | ⏳ No iniciado | 0% |
| **09** | [Pipelines](09-Pipelines/README.md) | ⏳ No iniciado | 0% |
| **10** | [History](10-History/README.md) | ⏳ No iniciado | 0% |
| **11** | [History Persistence](11-History_Persistence/README.md) | ⏳ No iniciado | 0% |
| **12** | [Parameter Expansion](12-Parameter_Expansion/README.md) | ⏳ No iniciado | 0% |

## 📚 Referencias Clave

- **Estándar POSIX Shell**: [Shell Command Language Specification](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- **CodeCrafters Challenge**: [Build your own Shell](https://app.codecrafters.io/courses/shell)
- **Manuales de Sistema**: `man fork`, `man execve`, `man dup2`, `man pipe`, `man termios`, `man waitpid`
