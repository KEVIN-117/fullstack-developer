# 📝 Ejercicios Prácticos - Módulo 0: SysAdmin & Redes

Para asimilar los conocimientos del Módulo 0, resuelve los siguientes desafíos técnicos en tu servidor Debian local.

---

## 🏃‍♂️ Ejercicio 1: Cambio de Puerto SSH
Por seguridad, muchos administradores cambian el puerto por defecto `22` por un puerto no estándar (ej. `2222` o `2022`).
*   **Instrucciones:**
    1. Configura el servidor SSH para escuchar en el puerto `2022`.
    2. Modifica las reglas del firewall `ufw` para permitir el nuevo puerto.
    3. Cierra la regla anterior para el puerto `22`.
    4. Conéctate desde tu PC cliente especificando el nuevo puerto.
*   **Pista:** Revisa `/etc/ssh/sshd_config` y recuerda reiniciar el servicio SSH. La conexión cliente se realiza como: `ssh -p 2022 usuario@ip`.

---

## 📊 Ejercicio 2: Auditoría y Detección de Intrusos (Logs)
En este ejercicio aprenderás a inspeccionar logs para identificar intentos de inicio de sesión fallidos.
*   **Instrucciones:**
    1. Desde tu máquina cliente, intenta conectarte de forma errónea a propósito por SSH (por ejemplo, con un usuario que no existe):
       ```bash
       ssh noexiste@<IP_SERVIDOR>
       ```
    2. En la terminal del servidor, usa `grep` o `journalctl` para buscar e identificar este registro de error en el sistema.
    3. Extrae la dirección IP del atacante simulado y la marca de tiempo de la agresión.
*   **Pista:** Los logs de autenticación de Debian se guardan en `/var/log/auth.log` o se pueden ver con `journalctl -u ssh`.

---

## 💾 Ejercicio 3: Scripting Básico y Tarea Programada (Cron)
Aprenderás a automatizar una tarea de administración habitual utilizando Bash y Cron.
*   **Instrucciones:**
    1. Crea un script en Bash en la carpeta `/home/homelab_admin/backup_logs.sh`.
    2. El script debe comprimir el archivo `/var/log/auth.log` en un archivo `.tar.gz` y guardarlo en un directorio `/var/backups/auth/` con la fecha actual en el nombre del archivo (ej. `auth_backup_2026-06-11.tar.gz`).
    3. Asegúrate de que el script tenga permisos de ejecución y de que solo pueda ser ejecutado por el usuario administrador o `root`.
    4. Configura el `cron` del sistema (`crontab -e`) para que este script se ejecute automáticamente todos los domingos a las 00:00.
*   **Pista:** Utiliza los comandos `tar`, `date` y `chmod`. Configura el crontab con la expresión `0 0 * * 0`.

---

## ⛔ Ejercicio 4: Banner de Advertencia SSH
Configura un banner que muestre un mensaje de advertencia legal o un arte ASCII personalizado para cualquiera que intente conectarse al servidor por SSH.
*   **Instrucciones:**
    1. Crea o edita el archivo `/etc/issue.net`.
    2. Coloca un mensaje como: `¡ADVERTENCIA! Acceso solo para personal autorizado. Todas las conexiones son registradas.`.
    3. Configura `/etc/ssh/sshd_config` para que apunte a este banner (`Banner /etc/issue.net`).
    4. Reinicia el servicio SSH y pruébalo conectándote desde tu terminal local.
