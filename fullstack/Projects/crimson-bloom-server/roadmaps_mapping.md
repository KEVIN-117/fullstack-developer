# 🗺️ Mapeo de Roadmaps de Especialidad (Skill & Role Based)

Para garantizar que el Home Lab se alinee con los estándares más altos de la industria, hemos integrado **34 guías de ruta oficiales (roadmaps)** organizadas por Rol de Trabajo (Role-Based) y por Habilidad Técnica (Skill-Based). 

A continuación se muestra el mapeo detallado de cómo cada archivo PDF dentro de la carpeta `roadmaps/` se distribuye e integra en los 6 módulos del Home Lab:

---

## 🏛️ Tabla de Distribución por Módulo

| Módulo | Role Based Roadmaps Integrados | Skill Based Roadmaps Integrados |
| :--- | :--- | :--- |
| **Módulo 0: SysAdmin & Redes** | `network-engineer.pdf`, `cyber-security.pdf` | `linux.pdf`, `shell-bash.pdf` |
| **Módulo 1: Docker & Nginx** | `devops.pdf` (Containers/Proxy) | `docker.pdf` |
| **Módulo 2: Desarrollo & CI/CD** | `backend.pdf`, `frontend.pdf`, `full-stack.pdf`, `devsecops.pdf` (CI/CD) | `golang.pdf`, `nodejs.pdf`, `api-design.pdf`, `design-system.pdf`, `git-github.pdf` |
| **Módulo 3: Data Engineering** | `data-engineer.pdf`, `postgresql-dba.pdf`, `bi-analyst.pdf`, `data-analyst.pdf` | `sql.pdf`, `redis.pdf`, `python.pdf` |
| **Módulo 4: AI & MLOps** | `ai-engineer.pdf`, `machine-learning.pdf`, `mlops.pdf`, `ai-data-scientist.pdf` | `python.pdf`, `system-design.pdf` (ML Serving patterns) |
| **Módulo 5: SRE & Observabilidad** | `devsecops.pdf` (Auditoría), `devops.pdf` (SRE & Telemetry) | `system-design.pdf` (Saturación y Tolerancia a Fallos) |

---

## 🎯 Detalle de Integración de Habilidades por Módulo

### [Módulo 0: Cimientos del Servidor y Hardening](./0_SysAdmin_Redes/README.md)
*   **Habilidades de `linux.pdf`:** Jerarquía de directorios (FHS), redirecciones de flujos (`stdout/stderr`), procesamiento de textos con `grep/awk/sed`, permisos POSIX octales, administración de almacenamiento físico (LVM, discos, mounts) y administración de servicios con Systemd.
*   **Habilidades de `shell-bash.pdf`:** Scripts de Bash, automatización de tareas con variables, condicionales, bucles y control de flujos.
*   **Habilidades de `network-engineer.pdf`:** Pila de protocolos TCP/IP, resolución DNS, tablas de enrutamiento locales, SSH y transporte de archivos seguro (SFTP).
*   **Habilidades de `cyber-security.pdf`:** Hardening de sistemas operativos, control de acceso de usuarios, políticas de denegación predeterminada (UFW) y seguridad SSH.

### [Módulo 1: Aislamiento, Orquestación y Enrutamiento](./1_Orquestacion_Enrutamiento/README.md)
*   **Habilidades de `docker.pdf`:** Aislamiento a nivel de Kernel (Namespaces y Cgroups), almacenamiento de capas OverlayFS, comandos de administración y volúmenes virtuales.
*   **Habilidades de `devops.pdf` (Sección Contenedores y Redes):** Declaración de arquitecturas compuestas con Compose, redes virtuales puente (bridge) y gateway perimetral (Proxy Inverso Nginx).
*   **Conceptos SSL/TLS:** Autoridades de Certificación locales (CA), llaves de cifrado asimétrico y protocolo TLS v1.3.

### [Módulo 2: Desarrollo e Integración Continua](./2_Desarrollo_CICD/README.md)
*   **Habilidades de `golang.pdf` & `nodejs.pdf`:** Sintaxis del lenguaje, concurrencia (goroutines y channels en Go) y patrones estructurales de inyección de dependencias (NestJS).
*   **Habilidades de `api-design.pdf`:** Diseño RESTful limpio, códigos de estado semánticos HTTP, versionado de endpoints.
*   **Habilidades de `design-system.pdf` & `frontend.pdf`:** Metodología Component Driven Development (CDD), modularización visual de UI pura, CSS Modules.
*   **Habilidades de `git-github.pdf` & `devsecops.pdf` (CI/CD):** Flujo de trabajo Git branch, runners de CI/CD autohospedados (Self-hosted) y empaquetado seguro en Dockerfiles multi-stage con usuarios sin privilegios (No-root).

### [Módulo 3: Ingeniería de Datos y Pipelines ETL](./3_Data_Engineering/README.md)
*   **Habilidades de `data-engineer.pdf` & `postgresql-dba.pdf`:** Esquemas relacionales normalizados, integridad referencial SQL, indexación física de tablas y almacenamiento semi-estructurado JSONB.
*   **Habilidades de `sql.pdf`:** Consultas complejas, filtros y sentencias de actualización Upsert (`ON CONFLICT`).
*   **Habilidades de `redis.pdf`:** Caching en memoria ultrarrápido, expiración automática (TTLs) y prevención de duplicación en lotes.
*   **Habilidades de `python.pdf` & `bi-analyst.pdf`:** Scripts de ingesta y validación de tipos e orquestación de flujos de trabajo (DAGs en Airflow).

### [Módulo 4: AI Engineering, Tracking y Serving (MLOps)](./4_AI_MLOps/README.md)
*   **Habilidades de `ai-engineer.pdf` & `machine-learning.pdf`:** Análisis exploratorio de datos (EDA), feature engineering (Label Encoding/One-Hot), modelos supervisados Scikit-Learn y métricas de desempeño.
*   **Habilidades de `mlops.pdf`:** Control de ciclo de vida del modelo (MLflow Tracking), Model Registry y versionado de hiperparámetros.
*   **Habilidades de `system-design.pdf` (ML Serving):** APIs de inferencia síncronas de baja latencia con FastAPI y esquemas de validación de datos con Pydantic.

### [Módulo 5: SRE, Observabilidad y DevSecOps Avanzado](./5_SRE_Observabilidad_Seguridad/README.md)
*   **Habilidades de `devops.pdf` (Sección SRE):** Recolección de telemetría, base de datos de series temporales (TSDB Prometheus), cAdvisor y Node Exporter.
*   **Habilidades de `system-design.pdf` (Monitoreo):** Diseño de alertas automatizadas (Alertmanager) e instrumentación de métricas de negocio personalizadas.
*   **Habilidades de `devsecops.pdf` (Seguridad Activa):** Escaneo de dependencias e imágenes de Docker en busca de brechas (Trivy) y auditorías de hardening del host (Lynis).
