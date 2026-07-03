# 🐋 Módulo 1: Aislamiento, Orquestación y Enrutamiento (Docker & Nginx)

Este módulo introduce el concepto de virtualización ligera y la gestión segura del tráfico web perimetral de tu Home Lab.

---

## 🗺️ Roadmaps de Referencia Integrados
Para profundizar en la teoría de este módulo, abre y estudia las siguientes rutas de especialización:
*   📄 **[docker.pdf](../roadmaps/Skill%20Based%20Roadmaps/docker.pdf)**: Aislamiento de procesos, OverlayFS, construcción de imágenes y volúmenes.
*   📄 **[devops.pdf](../roadmaps/Role%20Based%20Roadmaps/devops.pdf)** (Sección Contenedores & Redes): Mapeo de puertos, enrutamiento bridge, proxies inversos y TLS.

---

## 📋 Checklist General del Módulo
- [ ] Instalar Docker Engine y Docker Compose CLI en Debian de forma nativa.
- [ ] Crear una red virtual personalizada de tipo `bridge` en Docker.
- [ ] Levantar un contenedor web estático y aislarlo de la red externa.
- [ ] Generar certificados SSL/TLS válidos localmente (con `mkcert` u `openssl`).
- [ ] Configurar un proxy inverso Nginx para enrutar tráfico HTTPS al contenedor estático.
- [ ] Resolver todos los desafíos prácticos de la sección `/ejercicios`.
- [ ] Validar con curl que el tráfico HTTP (puerto 80) se redirige automáticamente a HTTPS.

---

## 📚 Tópicos y Submódulos de Aprendizaje

### 📦 Submódulo 1.1: Fundamentos de Docker
*   **Objetivo:** Comprender y gestionar el ciclo de vida de procesos aislados mediante contenedores.
*   **Tópicos Relacionados:** [1.1_Fundamentos_Docker.md](./topicos/1.1_Fundamentos_Docker.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] Diferencia entre Namespaces (aislamiento) y Control Groups (cgroups - límites de hardware).
    - [ ] ¿Qué diferencia hay entre una imagen (inmutable) y un contenedor (instancia en ejecución)?
    - [ ] Comandos fundamentales: `docker run`, `docker stop`, `docker ps`, `docker logs`, `docker exec`.

---

### 🌐 Submódulo 1.2: Orquestación con Docker Compose
*   **Objetivo:** Definir infraestructuras complejas compuestas por múltiples contenedores mediante código declarativo YAML.
*   **Tópicos Relacionados:** [1.2_Orquestacion_Compose.md](./topicos/1.2_Orquestacion_Compose.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] ¿Cómo funciona la resolución DNS interna entre contenedores dentro de una red Bridge?
    - [ ] Diferencia entre volúmenes persistentes (`volumes`) y montajes directos (`bind mounts`).
    - [ ] Sintaxis del archivo `docker-compose.yml` (services, networks, volumes, ports vs expose).

---

### 🔀 Submódulo 1.3: Gateway de Entrada y Proxy Inverso con Nginx
*   **Objetivo:** Configurar un único punto de entrada HTTP/S para el servidor que enrute las peticiones entrantes.
*   **Tópicos Relacionados:** [1.3_Proxy_Inverso_Nginx.md](./topicos/1.3_Proxy_Inverso_Nginx.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] ¿Qué es un proxy inverso y en qué se diferencia de un proxy directo?
    - [ ] Comprender directivas clave: `upstream`, `server`, `location` y `proxy_pass`.
    - [ ] ¿Por qué inyectar cabeceras como `X-Real-IP` y `X-Forwarded-For` en las peticiones?

---

### 🔐 Submódulo 1.4: Cifrado SSL/TLS Local
*   **Objetivo:** Garantizar la confidencialidad de los datos que viajan al Home Lab mediante protocolos de cifrado seguros.
*   **Tópicos Relacionados:** [1.4_Cifrado_SSL_TLS.md](./topicos/1.4_Cifrado_SSL_TLS.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] ¿Cómo funciona una Autoridad de Certificación (CA) y las llaves asimétricas en HTTPS?
    - [ ] ¿Qué problemas de seguridad previene el protocolo TLS v1.3 frente a versiones antiguas?
    - [ ] Diferencia entre un certificado autofirmado y uno firmado por una CA local de confianza.

---

## 🔍 Guía de Diagnóstico (Troubleshooting)

| Error Común | Causa Probable | Comando de Diagnóstico / Solución |
| :--- | :--- | :--- |
| **`docker: command not found`** | Docker no se instaló de forma nativa o no agregaste tu usuario al grupo `docker`. | Corre `sudo usermod -aG docker $USER` y reinicia tu sesión. |
| **`Bind for 0.0.0.0:80 failed: port is already allocated`** | Otro servicio (como el Nginx del sistema operativo Debian) está usando el puerto 80. | Corre `sudo ss -tulpn \| grep :80` y deténlo con `sudo systemctl stop nginx`. |
| **`502 Bad Gateway` en el navegador** | Nginx Proxy no puede conectarse al contenedor backend. | Revisa si el contenedor corre: `docker compose ps` y revisa los logs de red del proxy. |
| **Advertencia de seguridad en el navegador** | El navegador cliente no confía en el certificado autofirmado generado en el servidor. | Importa el archivo de certificado de tu CA local (`rootCA.pem`) en tu navegador cliente. |
