# 📋 Bitácora de Progreso: Home Lab Learning Journey

Utiliza esta bitácora para registrar tu avance a lo largo del roadmap. Marca con una `[x]` las tareas completadas y documenta las fechas importantes y métricas clave obtenidas.

---

## 🛡️ Módulo 0: Cimientos del Servidor y Hardening
- [ ] **Instalación Física:** Debian instalado en modo Headless (Netinst).
- [ ] **Direccionamiento Red:** IP estática local asignada en el host (`/etc/network/interfaces`).
- [ ] **Hardening SSH:** Llaves Ed25519 configuradas, accesos por contraseña desactivados.
- [ ] **Firewall perimetral:** UFW activo y bloqueando conexiones inseguras.
- [ ] **Ejercicios completados:**
  - [ ] Puerto SSH alternativo.
  - [ ] Auditoría de logs (`auth.log`).
  - [ ] Script de copia de seguridad programada en Cron.

---

## 🐋 Módulo 1: Aislamiento, Orquestación y Enrutamiento
- [ ] **Motor Docker:** Instalado y configurado en Debian.
- [ ] **Proxy Inverso:** Nginx container configurado para escuchar en puertos 80 y 443.
- [ ] **Seguridad Web:** Certificados SSL locales generados e integrados en Nginx.
- [ ] **Redes internas:** Red virtual bridge de Docker configurada para aislar la web estática.
- [ ] **Ejercicios completados:**
  - [ ] Ruteo de subruta `/whoami`.
  - [ ] Control de acceso por IP (Whitelist).
  - [ ] Páginas de error personalizadas (404/502).

---

## ⚙️ Módulo 2: Desarrollo e Integración Continua (CI/CD)
- [ ] **API Backend:** Desarrollada en Go o NestJS (endpoints `/health` y `/api/data`).
- [ ] **Frontend CDD:** Desarrollado con Vite + React (componentes puros y aislados).
- [ ] **Agente Runner:** GitHub Actions Runner contenerizado en Debian y conectado al repo.
- [ ] **Pipeline de CI/CD:** Flujo configurado para testear, compilar y redesplegar al hacer push.
- [ ] **Ejercicios completados:**
  - [ ] API backend paralela con concurrencia.
  - [ ] Componente visual de transacciones aislado (CDD).
  - [ ] Rollback de despliegue automático.

---

## 📊 Módulo 3: Ingeniería de Datos y Pipelines ETL
- [ ] **Persistencia:** Bases de datos de PostgreSQL y Redis activas en Docker.
- [ ] **Orquestador:** Apache Airflow o Prefect corriendo bajo docker-compose.
- [ ] **Esquema Relacional:** Tabla `facturas` e índices creados en Postgres.
- [ ] **Flujo ETL:** DAG en Python programado para extraer, limpiar, deduplicar y cargar facturas.
- [ ] **Ejercicios completados:**
  - [ ] Tabla de rechazos (Dead Letter Queue) para facturas corruptas.
  - [ ] Ingesta retroactiva programada (Backfill).
  - [ ] Políticas de expiración de claves (TTL) en Redis.

---

## 🤖 Módulo 4: AI Engineering & MLOps
- [ ] **Entorno de Ciencia:** Contenedor de JupyterLab activo con persistencia.
- [ ] **Model Registry:** Servidor de MLflow activo y conectado a Postgres y almacenamiento local.
- [ ] **Modelamiento:** Script de entrenamiento clasificador registrado en MLflow con métricas.
- [ ] **Servidor de Inferencia:** API FastAPI que expone el modelo mediante endpoint `/predict`.
- [ ] **Ejercicios completados:**
  - [ ] Inferencia de modelos en modo espejo (Shadow Deploy).
  - [ ] DAG de re-entrenamiento automático en Airflow.
  - [ ] Feature Engineering (tasa de rechazo del proveedor).

---

## 📈 Módulo 5: SRE, Observabilidad y DevSecOps
- [ ] **Colección de Métricas:** Prometheus activo recolectando datos de Node Exporter y cAdvisor.
- [ ] **Dashboarding:** Grafana enlazado a Prometheus y mostrando consumo del host Debian.
- [ ] **API Telemetría:** API Backend (Módulo 2) exponiendo métricas nativas en `/metrics`.
- [ ] **Escaneos estáticos:** Auditoría de vulnerabilidades con Trivy integrada en el pipeline.
- [ ] **Ejercicios completados:**
  - [ ] Métricas custom de negocio (`facturas_procesadas_total`).
  - [ ] Alertas automatizadas con Alertmanager (Discord/Slack).
  - [ ] Auditoría de seguridad del sistema físico con Lynis.
