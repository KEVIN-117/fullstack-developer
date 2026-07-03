# 📊 Módulo 3: Ingeniería de Datos y Pipelines ETL (Data Engineering)

Este módulo introduce las bases para el flujo de información sistemático en tu Home Lab, permitiéndote ingestar, limpiar y almacenar datos estructurados de forma periódica.

---

## 🗺️ Roadmaps de Referencia Integrados
Para profundizar en la teoría de este módulo, abre y estudia las siguientes rutas de especialización:
*   📄 **[data-engineer.pdf](../roadmaps/Role%20Based%20Roadmaps/data-engineer.pdf)** & **[postgresql-dba.pdf](../roadmaps/Role%20Based%20Roadmaps/postgresql-dba.pdf)**: Esquemas transaccionales, normalización y optimización física de PostgreSQL.
*   📄 **[sql.pdf](../roadmaps/Skill%20Based%20Roadmaps/sql.pdf)** & **[redis.pdf](../roadmaps/Skill%20Based%20Roadmaps/redis.pdf)**: Sentencias SQL avanzadas y caching rápido con estructuras clave-valor y TTLs.
*   📄 **[python.pdf](../roadmaps/Skill%20Based%20Roadmaps/python.pdf)** & **[data-analyst.pdf](../roadmaps/Role%20Based%20Roadmaps/data-analyst.pdf)**: Scripting para ingesta, extracción y calendarización de tareas batch (DAGs).

---

## 📋 Checklist General del Módulo
- [ ] Desplegar PostgreSQL (OLTP) y Redis (Caché) utilizando Docker Compose.
- [ ] Diseñar el esquema de base de datos SQL con tablas y restricciones de unicidad adecuadas.
- [ ] Desplegar Apache Airflow o Prefect de forma contenerizada y funcional.
- [ ] Conectar Airflow con PostgreSQL y Redis a través de conexiones seguras.
- [ ] Programar un DAG de Python en Airflow que implemente un flujo ETL (Extract, Transform, Load).
- [ ] Implementar un mecanismo de deduplicación de registros usando Redis.
- [ ] Resolver todos los desafíos prácticos de la sección `/ejercicios`.
- [ ] Validar la idempotencia del pipeline de datos ejecutándolo múltiples veces consecutivas.

---

## 📚 Tópicos y Submódulos de Aprendizaje

### 🗄️ Submódulo 3.1: Almacenamiento Relacional (PostgreSQL) y No Relacional (Redis)
*   **Objetivo:** Configurar bases de datos transaccionales persistentes y capas de almacenamiento ultra-rápidas en memoria.
*   **Tópicos Relacionados:** [3.1_Postgres_Redis.md](./topicos/3.1_Postgres_Redis.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] ¿Qué diferencia hay entre una base de datos relacional (Postgres) y una clave-valor en memoria (Redis)?
    - [ ] Concepto de consistencia transaccional (propiedades ACID).
    - [ ] Estructuras de datos básicas en Redis (Strings, Hashes, Sets) y políticas de expiración (TTL).

---

### 🕸️ Submódulo 3.2: Orquestación con Apache Airflow
*   **Objetivo:** Automatizar la ejecución cronológica de tareas de procesamiento complejas mediante grafos acíclicos dirigidos.
*   **Tópicos Relacionados:** [3.2_Orquestacion_Airflow.md](./topicos/3.2_Orquestacion_Airflow.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] ¿Qué es un Grafo Acíclico Dirigido (DAG) y por qué se utiliza en flujos de datos?
    - [ ] Componentes fundamentales de Airflow: Scheduler, Webserver, MetaDB, y Executor.
    - [ ] ¿Cómo funciona el intercambio de datos temporal entre tareas (XComs) y variables de entorno?

---

### 🔄 Submódulo 3.3: Diseño de Pipelines ETL Idempotentes
*   **Objetivo:** Desarrollar flujos de datos capaces de autolimpiarse y ejecutarse múltiples veces sin generar distorsiones.
*   **Tópicos Relacionados:** [3.3_Pipelines_ETL_Idempotentes.md](./topicos/3.3_Pipelines_ETL_Idempotentes.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] Principio de Idempotencia en ingeniería de datos.
    - [ ] Técnicas de manejo de conflictos en SQL (`ON CONFLICT DO NOTHING` / `UPSERT`).
    - [ ] Validación de negocio y formateo de datos sucios (limpieza de tipos, manejo de nulos).

---

## 🔍 Guía de Diagnóstico (Troubleshooting)

| Error Común | Causa Probable | Comando de Diagnóstico / Solución |
| :--- | :--- | :--- |
| **Scheduler congelado** | Falta de memoria RAM en el servidor local. | Monitorea el uso de hardware en el host: `free -m` o `docker stats`. |
| **`Connection refused` en Postgres** | Airflow no puede resolver la IP o Postgres no está listo. | Usa el nombre de red interna de Docker (`postgres-db`). |
| **`FATAL: password authentication failed`** | Credenciales de metadatos de Airflow incorrectas. | Revisa las variables `POSTGRES_USER` contra `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN`. |
| **Las llaves de Redis no expiran** | No configuraste el TTL al guardar el ID de la factura. | Abre el CLI de Redis y ejecuta `TTL factura_id`. |
