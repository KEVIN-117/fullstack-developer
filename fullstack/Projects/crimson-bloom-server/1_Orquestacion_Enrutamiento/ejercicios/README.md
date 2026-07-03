# 📝 Ejercicios Prácticos - Módulo 1: Docker & Nginx

Lleva al límite tu entorno contenerizado de Home Lab resolviendo las siguientes tareas de configuración práctica.

---

## 🏃‍♂️ Ejercicio 1: Ruteo Multitarea (`/whoami`)
Añadirás un nuevo servicio a tu ecosistema que permita identificar información sobre la petición de red que recibe.
*   **Instrucciones:**
    1. Agrega el servicio `traefik/whoami` a tu archivo `docker-compose.yml`. Este contenedor simplemente devuelve información de cabeceras HTTP al ser consultado. Asegúrate de ponerlo en la misma red que tu proxy Nginx. No le asignes mapeo de puertos (`ports`) hacia el host, usa `expose` en su lugar.
    2. Modifica el archivo `nginx.conf` de tu proxy para añadir una nueva ruta:
       * El tráfico que ingrese a `https://homelab.local/whoami` debe ser redirigido internamente al contenedor `whoami` en su puerto `80`.
    3. Reinicia Nginx sin tumbar todo el Compose (`docker compose exec nginx-proxy nginx -s reload`).
*   **Criterio de Aceptación:** Al visitar `https://homelab.local/whoami` desde tu navegador, debes ver texto con información de tu petición (IP, headers, etc.).

---

## ⛔ Ejercicio 2: Control de Acceso por IP (Whitelist)
Aprenderás a proteger endpoints sensibles en Nginx restringiendo el acceso únicamente a ciertas direcciones IP.
*   **Instrucciones:**
    1. Crea un endpoint `/internal` en tu configuración de Nginx que apunte a tu contenedor web estático.
    2. Modifica la configuración de Nginx de ese bloque para que **solo** permita conexiones provenientes de la IP de tu computadora cliente de desarrollo.
    3. Bloquea cualquier otra dirección IP en ese bloque específico.
*   **Pistas:** Investiga el uso de las directivas `allow` y `deny` dentro de un bloque `location` en Nginx.

---

## 🛠️ Ejercicio 3: Página de Error 404 y 502 Personalizada
Configura tu servidor web para que no muestre el error predeterminado y aburrido de Nginx en caso de páginas no encontradas o caídas del servicio backend.
*   **Instrucciones:**
    1. Crea un archivo HTML de diseño personalizado (`404.html` y `502.html`) y guárdalos en el volumen del proxy Nginx.
    2. Configura Nginx para usar estos archivos cuando ocurra un error `404` (Not Found) o un error `502` (Bad Gateway).
    3. Prueba el error 502 deteniendo el contenedor de tu web estática (`docker compose stop web-static`) e intentando acceder al sitio.
*   **Pistas:** Investiga la directiva `error_page` de Nginx.

---

## 📦 Ejercicio 4: Limitación de Recursos en Contenedores
Para evitar que un contenedor con fallos consuma todos los recursos (CPU y RAM) de tu máquina física Debian, aprenderás a limitar sus capacidades.
*   **Instrucciones:**
    1. Modifica la definición de uno de tus servicios en el `docker-compose.yml` para limitar el uso de memoria RAM a un máximo de `128M` y CPU a `0.5` nucleos.
    2. Reinicia los servicios y utiliza el comando `docker stats` para verificar que el límite ha sido aplicado con éxito.
*   **Pistas:** Revisa la sintaxis de `deploy.resources.limits` en la especificación de Docker Compose V2.
