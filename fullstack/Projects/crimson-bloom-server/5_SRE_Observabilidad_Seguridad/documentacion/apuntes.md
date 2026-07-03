# 📚 Apuntes y Conceptos Clave - Módulo 5: SRE, Observabilidad & Seguridad

Notas sobre monitoreo de producción, métricas dimensionales y aseguramiento de contenedores.

---

## 🏛️ Las 4 Señales Doradas del Monitoreo (SRE)
De acuerdo con el libro de Ingeniería de Confiabilidad de Sitios (SRE) de Google, un sistema en producción debe observarse a través de cuatro métricas críticas:
1.  **Latencia:** El tiempo que toma procesar una petición de red. Es vital medir la latencia de peticiones exitosas por separado de las fallidas.
2.  **Tráfico:** La demanda general del sistema, expresada habitualmente en peticiones por segundo (RPS) o consultas por segundo (QPS).
3.  **Errores:** La tasa de peticiones que fallan. Se miden errores explícitos (ej. códigos HTTP 500) e implícitos (ej. respuestas HTTP 200 que tardan más del tiempo tolerable).
4.  **Saturación:** Qué tan saturados están los recursos del servidor físico (CPU, memoria RAM, tasa de entrada/salida de disco, ancho de banda de red).

---

## 📊 Prometheus: Modelo de Datos y Scraping
Prometheus almacena datos estructurados en **series temporales (TSDB)**.
*   **Modelo Multidimensional:** Cada métrica consta de un nombre y un conjunto de etiquetas clave-valor (labels) que permiten agregar o segmentar los datos de forma flexible.
    *   Ejemplo: `http_requests_total{method="POST", handler="/predict", status="200"}`
*   **Modelo de Extracción (Scraping/Pulling):** A diferencia de otros sistemas donde las aplicaciones empujan sus métricas a una base de datos centralizada (modelo Push), Prometheus realiza peticiones HTTP de forma periódica (scrape intervals) a las aplicaciones configuradas para descargar sus métricas.
    *   Cada servicio debe exponer un endpoint HTTP (usualmente `/metrics`) en texto plano estructurado según el formato estándar de Prometheus.

---

## 🔍 Trivy y Análisis de Vulnerabilidades (CVEs)
*   **CVE (Common Vulnerabilities and Exposures):** Base de datos internacional que documenta agujeros de seguridad de software conocidos.
*   **Escaneo Estático:** Herramientas como **Trivy** descomponen una imagen de Docker analizando capa por capa y revisando los paquetes instalados en la distribución base (ej. Alpine, Debian, Ubuntu) y las dependencias (ej. paquetes de npm, pip, go.mod) contra la base de datos de CVEs actualizada.
*   Permite bloquear despliegues en caliente si el software empaquetado contiene brechas explotables críticas.

---

## 🛡️ Lynis y Hardening de Sistemas Operativos
Lynis es una herramienta de auditoría de seguridad para sistemas Unix/Linux. Corre directamente sobre el Host (servidor Debian físico) y verifica:
*   Configuración del cargador de arranque (GRUB) y contraseñas.
*   Aseguramiento del Kernel de Linux (parámetros sysctl).
*   Estado de los permisos de archivos sensibles (ej. `/etc/passwd`, `/etc/shadow`).
*   Servicios activos redundantes e innecesarios ejecutándose en segundo plano.
*   Políticas de cortafuegos y cifrado de conexiones SSH.
*   Genera un **Hardening Index** (Índice de Endurecimiento) de 0 a 100 indicando el estado general de blindaje del servidor.
