# Índice de Contenidos - Shell Challenge Stages

Este archivo provee un índice rápido y accesible de todos los archivos y recursos estructurados en este proyecto para la construcción de tu propio Shell.

## 📁 Estructura Global y Guías

- [README Principal](README.md) - Visión general, mapa de progreso de stages y referencias globales.
- [Guía de Implementación General](IMPLEMENTATION_GUIDE.md) - Arquitectura general del shell, patrones de diseño recomendados y mejores prácticas de sistemas.
- [Referencia Rápida (Quick Reference)](QUICK_REFERENCE.md) - Resumen de llamadas al sistema, códigos de error y comandos de terminal de utilidad.

---

## ⚡ Directorios por Stage

### [Stage 01: Core Commands](01-Core_Commands/)
*Conceptos básicos y ejecución inicial.*
- [README de Stage](01-Core_Commands/README.md) - Objetivos y explicación del REPL y comandos base.
- [Checklist de Stage](01-Core_Commands/CHECKLIST.md) - Tareas pendientes y completadas.
- [Carpeta de Implementación](01-Core_Commands/implementation/) - Archivos fuente del stage.
- [Carpeta de Pruebas](01-Core_Commands/tests/) - Scripts de prueba locales.

### [Stage 02: Navigation](02-Navigation/)
*Navegación por el sistema de archivos.*
- [README de Stage](02-Navigation/README.md) - El comando cd, pwd y gestión de rutas.
- [Checklist de Stage](02-Navigation/CHECKLIST.md) - Tareas de navegación.

### [Stage 03: Quoting](03-Quoting/)
*Soporte de comillas y escapes.*
- [README de Stage](03-Quoting/README.md) - Comillas simples, dobles y barra invertida de escape.
- [Checklist de Stage](03-Quoting/CHECKLIST.md) - Tareas de parsing de caracteres especiales.

### [Stage 04: Redirection](04-Redirection/)
*Redirección de entrada/salida y errores.*
- [README de Stage](04-Redirection/README.md) - Redirección y appending de descriptores de archivos (`stdout`/`stderr`).
- [Checklist de Stage](04-Redirection/CHECKLIST.md) - Tareas de redirección.

### [Stage 05: Command Completion](05-Command_Completion/)
*Autocompletado de comandos y ejecutables.*
- [README de Stage](05-Command_Completion/README.md) - Manejo de teclado (modo Raw) y autocompletado con Tab.
- [Checklist de Stage](05-Command_Completion/CHECKLIST.md) - Tareas de autocompletado básico.

### [Stage 06: Filename Completion](06-Filename_Completion/)
*Autocompletado de archivos e interactividad avanzada.*
- [README de Stage](06-Filename_Completion/README.md) - Autocompletado de rutas y subdirectorios.
- [Checklist de Stage](06-Filename_Completion/CHECKLIST.md) - Tareas de autocompletado de sistema de archivos.

### [Stage 07: Programmable Completion](07-Programmable_Completion/)
*Sistema dinámico de autocompletado programable.*
- [README de Stage](07-Programmable_Completion/README.md) - El built-in `complete` y resolución dinámica.
- [Checklist de Stage](07-Programmable_Completion/CHECKLIST.md) - Tareas de autocompletado programable.

### [Stage 8: Background Jobs](08-Background_Jobs/)
*Ejecución asíncrona y control de procesos.*
- [README de Stage](08-Background_Jobs/README.md) - Manejo de subprocesos con `&` y comando `jobs`.
- [Checklist de Stage](08-Background_Jobs/CHECKLIST.md) - Tareas de control de trabajos.

### [Stage 09: Pipelines](09-Pipelines/)
*Conexión mediante tuberías.*
- [README de Stage](09-Pipelines/README.md) - Comunicación entre procesos (`pipe`/`dup2`).
- [Checklist de Stage](09-Pipelines/CHECKLIST.md) - Tareas de redirección mediante pipes.

### [Stage 10: History](10-History/)
*Historial interactivo en memoria.*
- [README de Stage](10-History/README.md) - Estructuras de datos de historial y navegación con flechas (Arriba/Abajo).
- [Checklist de Stage](10-History/CHECKLIST.md) - Tareas de historial interactivo.

### [Stage 11: History Persistence](11-History_Persistence/)
*Persistencia del historial en disco.*
- [README de Stage](11-History_Persistence/README.md) - Lectura y escritura en archivos de configuración al iniciar/salir.
- [Checklist de Stage](11-History_Persistence/CHECKLIST.md) - Tareas de persistencia.

### [Stage 12: Parameter Expansion](12-Parameter_Expansion/)
*Expansión de variables y el comando declare.*
- [README de Stage](12-Parameter_Expansion/README.md) - Entorno del shell, asignaciones y expansiones con llaves.
- [Checklist de Stage](12-Parameter_Expansion/CHECKLIST.md) - Tareas de expansión y variables.
