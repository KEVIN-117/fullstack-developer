# 📚 Apuntes y Conceptos Clave - Módulo 1: Docker & Nginx

Notas de estudio enfocadas en el aislamiento con contenedores y la administración del proxy inverso.

---

## 🐋 Contenedores vs. Máquinas Virtuales
A diferencia de las máquinas virtuales (que emulan hardware completo y corren un kernel de sistema operativo entero sobre un hipervisor), los contenedores de Linux:
1.  **Comparten el Kernel del Host:** Todos los contenedores usan el mismo kernel del sistema Debian subyacente.
2.  **Aislamiento vía Namespaces:** El kernel de Linux aísla procesos utilizando *namespaces*:
    *   `PID` (Process ID): Aísla la jerarquía de procesos.
    *   `NET` (Network): Proporciona interfaces de red y tablas de enrutamiento aisladas.
    *   `MNT` (Mount): Aísla los puntos de montaje del sistema de archivos.
    *   `IPC` (Interprocess Communication): Aísla los recursos de comunicación entre procesos.
    *   `UTS` (Hostnames): Permite tener un hostname único por contenedor.
3.  **Control de Recursos vía Cgroups (Control Groups):** Limita y mide el consumo de hardware (CPU, RAM, E/S de disco) de cada contenedor.

---

## 🌐 Redes en Docker
Por defecto, Docker tiene tres redes básicas: `bridge`, `host` y `none`.
*   **Bridge (Puente):** Red virtual interna creada en el Host Debian. Docker asigna un rango IP interno (ej. `172.18.0.0/16`) a esta red. Cada contenedor recibe una IP en este rango.
*   **Host:** Elimina el aislamiento de red entre el contenedor y el host Debian. El contenedor usa directamente la IP y puertos físicos del servidor.
*   **None:** Deshabilita toda red para el contenedor.

En entornos de producción (y en este Home Lab), se crean **redes personalizadas (custom bridges)**. Esto permite la resolución de nombres DNS automática mediante el nombre del servicio en el archivo `docker-compose.yml` (por ejemplo, Nginx puede hacer ping a `api-backend` en lugar de necesitar conocer su IP interna cambiante).

---

## 🔀 Proxy Inverso Nginx e Hitos de Configuración
Un proxy inverso recibe peticiones HTTPS entrantes en la frontera del servidor y las reenvía a los servicios backend adecuados que corren internamente.

### Directivas Esenciales de Nginx
*   `proxy_pass`: Define la dirección del servidor backend al que se reenviará el tráfico.
    *   `proxy_pass http://api-backend:3000;`
*   `proxy_set_header`: Inyecta o modifica cabeceras HTTP de la petición antes de enviarla al backend.
    *   `proxy_set_header Host $host;`
    *   `proxy_set_header X-Real-IP $remote_addr;` (Permite al backend saber la IP real del cliente que se conecta, de lo contrario vería la IP interna del proxy Nginx).
    *   `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;` (Mantiene el historial de las IPs por las que ha pasado la petición).
*   `ssl_certificate` y `ssl_certificate_key`: Rutas a la clave pública y privada del certificado digital para desencriptar el tráfico HTTPS (Terminación SSL).
