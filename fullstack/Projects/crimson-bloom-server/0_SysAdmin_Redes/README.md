# 🛡️ Módulo 0: Cimientos del Servidor y Hardening (SysAdmin & Redes)

Este módulo inicial está diseñado para sentar las bases físicas, operativas y de seguridad de tu servidor Home Lab.

---

## 🗺️ Roadmaps de Referencia Integrados
Para profundizar en la teoría de este módulo, abre y estudia las siguientes rutas de especialización:
*   📄 **[linux.pdf](../roadmaps/Skill%20Based%20Roadmaps/linux.pdf)**: Comandos de navegación, gestión de archivos, procesamiento de texto ySystemd.
*   📄 **[shell-bash.pdf](../roadmaps/Skill%20Based%20Roadmaps/shell-bash.pdf)**: Variables, bucles y lógica de automatización en scripts.
*   📄 **[network-engineer.pdf](../roadmaps/Role%20Based%20Roadmaps/network-engineer.pdf)**: Redes locales, direccionamiento IP, resolución de nombres (DNS) y SSH.
*   📄 **[cyber-security.pdf](../roadmaps/Role%20Based%20Roadmaps/cyber-security.pdf)**: Hardening de sistemas operativos y filtrado perimetral con firewalls.

---

## 📋 Checklist General del Módulo
- [ ] Completar la instalación headless de Debian.
- [ ] Configurar una IP estática local en la tarjeta de red.
- [ ] Crear un usuario administrador y otorgar permisos en `sudoers`.
- [ ] Generar llaves SSH Ed25519 y desactivar autenticación por contraseña.
- [ ] Activar y configurar reglas de firewall en UFW.
- [ ] Resolver todos los desafíos prácticos de la sección `/ejercicios`.
- [ ] Ejecutar el script `validate.sh` y obtener un reporte 100% exitoso (verde).

---

## 📚 Tópicos y Submódulos de Aprendizaje

### ⚙️ Submódulo 0.1: Instalación de Debian Headless y Redes Básicas
*   **Objetivo:** Disponer de un sistema operativo Debian mínimo sin entorno gráfico y con conexión local estática.
*   **Tópicos Relacionados:** [0.1_Instalacion_Debian_Redes.md](./topicos/0.1_Instalacion_Debian_Redes.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] ¿Qué diferencia hay entre una instalación de servidor completa y una "headless/netinst"?
    - [ ] ¿Cómo funciona el direccionamiento IP local (máscaras `/24`, puertas de enlace, DNS)?
    - [ ] Comandos clave de red: `ip a`, `ping`, `ip route`, `ss`.

---

### 👥 Submódulo 0.2: Permisos de Linux y Administración de Usuarios
*   **Objetivo:** Gestionar accesos al sistema bajo el principio de privilegios mínimos.
*   **Tópicos Relacionados:** [0.2_Permisos_Usuarios.md](./topicos/0.2_Permisos_Usuarios.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] ¿Cómo funciona el archivo `/etc/passwd` y `/etc/shadow`?
    - [ ] Diferencia entre permisos de Lectura (`r`), Escritura (`w`) y Ejecución (`x`) en formato octal.
    - [ ] ¿Qué es el archivo `/etc/sudoers` y cómo funciona la delegación de comandos?

---

### 🔑 Submódulo 0.3: Acceso Seguro vía SSH Hardening
*   **Objetivo:** Proteger el canal de administración remota contra intrusos y ataques de fuerza bruta.
*   **Tópicos Relacionados:** [0.3_Hardening_SSH.md](./topicos/0.3_Hardening_SSH.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] ¿Qué ventajas ofrece el algoritmo Ed25519 frente a RSA?
    - [ ] ¿Cómo funciona el apretón de manos (handshake) criptográfico en SSH?
    - [ ] Riesgos de permitir la autenticación de usuarios root directamente.

---

### 🧱 Submódulo 0.4: Seguridad Perimetral con UFW
*   **Objetivo:** Controlar y filtrar todo el tráfico entrante y saliente del servidor.
*   **Tópicos Relacionados:** [0.4_Firewall_UFW.md](./topicos/0.4_Firewall_UFW.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] ¿Qué es iptables/nftables y qué relación tiene con UFW?
    - [ ] ¿Qué significa la política predeterminada "default deny"?
    - [ ] Diferencia entre reglas para protocolos TCP y UDP.

---

## 🔍 Guía de Diagnóstico (Troubleshooting)

| Error Común | Causa Probable | Comando de Diagnóstico / Solución |
| :--- | :--- | :--- |
| **`Permission denied (publickey)`** | La llave pública no está registrada en el servidor o el archivo tiene permisos inseguros. | En el servidor: `chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys`. |
| **Pérdida de conectividad** | Conflicto de IP local o mala sintaxis en el archivo de interfaces. | En la consola física: `ip a` y revisa `sudo systemctl status networking`. |
| **UFW bloquea la conexión SSH** | Activaste el firewall antes de abrir el puerto de escucha SSH. | En consola física: `sudo ufw allow 22/tcp`. |
| **`sudo: command not found`** | Instalaste Debian sin configurar repositorios de sudo. | Entra como root con `su -` y corre: `apt update && apt install sudo`. |
