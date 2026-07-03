# 📚 Apuntes y Conceptos Clave - Módulo 0: SysAdmin & Redes

Este documento sirve como bitácora de conceptos y comandos esenciales aprendidos durante el Módulo 0.

---

## 💻 El Sistema de Permisos de Linux
Linux es un sistema operativo multiusuario con un modelo de seguridad basado en permisos sobre archivos y directorios. Cada elemento tiene tres niveles de permisos:
1. **User (Usuario):** El propietario del archivo.
2. **Group (Grupo):** Los miembros del grupo asignado.
3. **Others (Otros):** Cualquier otro usuario del sistema.

Cada nivel cuenta con tres tipos de permisos:
*   `r` (Read / Leer) = Valor octal `4`.
*   `w` (Write / Escribir) = Valor octal `2`.
*   `x` (Execute / Ejecutar) = Valor octal `1`.

### Comandos de Permisos
*   `chmod`: Cambia los permisos de lectura, escritura y ejecución.
    *   `chmod 755 script.sh`: Otorga todos los permisos al dueño (`4+2+1=7`), y lectura/ejecución al grupo (`4+1=5`) y otros (`4+1=5`).
    *   `chmod 600 id_ed25519`: Solo el dueño puede leer y escribir (permiso estándar para llaves privadas).
*   `chown`: Cambia el propietario y grupo de un archivo.
    *   `sudo chown homelab_admin:homelab_group archivo.txt`

---

## 🔑 Criptografía y SSH
El protocolo **SSH (Secure Shell)** utiliza criptografía asimétrica para la autenticación remota mediante un par de claves:
*   **Llave Privada (`id_ed25519`):** Debe mantenerse estrictamente secreta en la máquina cliente.
*   **Llave Pública (`id_ed25519.pub`):** Se copia en el servidor remoto dentro del archivo `~/.ssh/authorized_keys`.

El algoritmo **Ed25519** es preferible sobre RSA hoy en día porque ofrece firmas criptográficas mucho más rápidas y una seguridad superior con llaves de tamaño significativamente menor (256 bits vs 4096 bits de RSA).

---

## 🧱 Cortafuegos (UFW)
`ufw` (Uncomplicated Firewall) es una interfaz simplificada para `iptables` y `nftables` (el subsistema de filtrado de paquetes integrado en el kernel de Linux).
*   `sudo ufw status`: Muestra si el firewall está activo y las reglas actuales.
*   `sudo ufw default deny incoming`: Bloquea por defecto cualquier tráfico entrante que no coincida con una regla permitida (principio de "Denegar por Defecto").
*   `sudo ufw allow 22/tcp`: Permite tráfico entrante de red en el puerto 22 a través del protocolo TCP.

---

## 📝 Monitoreo de Logs en Debian
El archivo principal de logs en Debian es gestionado por `rsyslog` y el diario del sistema `systemd-journald`.
*   `/var/log/auth.log`: Registra intentos de autenticación, uso de `sudo` y accesos SSH.
*   `journalctl`: Visualiza todos los logs del sistema unificado.
    *   `journalctl -f`: Sigue los logs en tiempo real (equivalente a `tail -f`).
    *   `journalctl -u ssh`: Filtra los logs específicos del servicio SSH.
    *   `journalctl -n 50`: Muestra únicamente las últimas 50 líneas.
