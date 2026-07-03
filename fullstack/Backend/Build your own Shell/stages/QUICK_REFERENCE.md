# Referencia Rápida (Cheat Sheet) de Desarrollo de Shell

Este documento es una referencia rápida de llamadas al sistema (syscalls), estructuras, señales, secuencias de escape ANSI y códigos de retorno esenciales para programar el shell.

---

## 📞 Llamadas al Sistema Fundamentales (POSIX)

| Función | Cabecera | Descripción | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| `fork()` | `<unistd.h>` | Duplica el proceso llamador. | `pid_t pid = fork();` |
| `execvp()` | `<unistd.h>` | Reemplaza el proceso actual con un ejecutable, buscando en `$PATH`. | `execvp(args[0], args);` |
| `waitpid()` | `<sys/wait.h>` | Espera el cambio de estado en un subproceso específico. | `waitpid(pid, &status, 0);` |
| `pipe()` | `<unistd.h>` | Crea una tubería unidireccional de datos (retorna 2 descriptores). | `int fd[2]; pipe(fd);` |
| `dup2()` | `<unistd.h>` | Duplica un descriptor de archivo en otro descriptor específico. | `dup2(fd_archivo, 1); // stdout` |
| `close()` | `<unistd.h>` | Cierra un descriptor de archivo activo. | `close(fd[0]);` |
| `chdir()` | `<unistd.h>` | Cambia el directorio de trabajo actual. | `chdir("/home/user");` |
| `getcwd()` | `<unistd.h>` | Obtiene el directorio de trabajo actual. | `getcwd(buf, sizeof(buf));` |
| `setpgid()` | `<unistd.h>` | Establece el ID de grupo de proceso (útil para background jobs). | `setpgid(0, 0);` |
| `kill()` | `<signal.h>` | Envía una señal a un proceso o grupo de procesos. | `kill(pid, SIGINT);` |

---

## 🚦 Códigos de Salida del Intérprete de Comandos (Exit Codes)

| Código | Significado | Causa Común |
| :---: | :--- | :--- |
| `0` | **Éxito** | El comando finalizó correctamente sin errores. |
| `1` | **Error genérico** | Errores generales como sintaxis incorrecta o fallo en la operación. |
| `126` | **Comando invocado no ejecutable** | Problema de permisos (`EACCES`) o el destino es un directorio. |
| `127` | **Comando no encontrado** | El ejecutable no existe en `$PATH` (`ENOENT`). |
| `128 + N` | **Comando terminado por señal N** | E.g. `130` indica finalización por `SIGINT` (Ctrl+C: `128 + 2`). |

---

## 🎛️ Modificación de la Terminal (termios)

Para leer el teclado carácter a carácter sin esperar a pulsar Enter (Modo Raw):

```c
#include <termios.h>
#include <unistd.h>

struct termios original;
struct termios raw;

// 1. Obtener configuración actual
tcgetattr(STDIN_FILENO, &original);

// 2. Copiar y desactivar flags canónicos y eco
raw = original;
raw.c_lflag &= ~(ICANON | ECHO | ISIG); 
raw.c_cc[VMIN] = 1;  // Leer mínimo 1 carácter
raw.c_cc[VTIME] = 0; // Sin timeout

// 3. Aplicar configuración inmediatamente
tcsetattr(STDIN_FILENO, TCSANOW, &raw);

// 4. Restaurar al terminar
tcsetattr(STDIN_FILENO, TCSANOW, &original);
```

---

## ⌨️ Captura de Teclas Especiales en Modo Raw

En modo Raw, las teclas especiales envían secuencias de bytes específicas a `stdin`:

| Tecla | Secuencia de Escape Hexadecimal / ASCII | Notas |
| :--- | :--- | :--- |
| **Tab** | `\t` (ASCII `9` / Hex `0x09`) | Disparador de autocompletado. |
| **Retroceso (Backspace)** | `\x7f` (ASCII `127`) o `\b` (ASCII `8`) | Borrar último carácter. |
| **Ctrl+C** | `\x03` (ASCII `3`) | Señal de interrupción (`SIGINT`). |
| **Ctrl+D** | `\x04` (ASCII `4`) | Fin de archivo (`EOF`), cierra el shell. |
| **Flecha Arriba** | `\x1b[A` (Esc, `[`, `A`) | Navegar hacia atrás en el historial. |
| **Flecha Abajo** | `\x1b[B` (Esc, `[`, `B`) | Navegar hacia adelante en el historial. |
| **Flecha Derecha** | `\x1b[C` (Esc, `[`, `C`) | Mover cursor a la derecha. |
| **Flecha Izquierda** | `\x1b[D` (Esc, `[`, `D`) | Mover cursor a la izquierda. |

---

## 🎨 Secuencias de Escape ANSI (Consola Interactiva)

Útiles para borrar texto de la pantalla, mover el cursor de forma programática y redibujar el prompt al autocompletar:

- **Mover cursor a la izquierda N columnas**: `\x1b[ND` (e.g. `\x1b[3D` mueve 3 posiciones a la izquierda).
- **Borrar desde el cursor hasta el final de la línea**: `\x1b[K` (útil al reescribir con autocompletados más cortos).
- **Borrar pantalla completa**: `\x1b[2J`
- **Mover cursor a posición de origen (0,0)**: `\x1b[H`
- **Hacer sonar campana de la terminal (bell)**: `\a` (ASCII `7`, útil cuando no hay autocompletado disponible).
