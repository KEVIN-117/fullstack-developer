# 📚 Apuntes y Conceptos Clave - Módulo 3: Data Engineering

Notas de estudio para diseño de bases de datos, caché y orquestación de datos.

---

## 🏛️ OLTP vs. OLAP
*   **OLTP (Online Transaction Processing):** Enfocado en soportar millones de transacciones rápidas por segundo (operaciones CRUD). Las bases de datos se diseñan de forma **normalizada** (evitando redundancias) para asegurar integridad referencial y escrituras veloces. **PostgreSQL** es un ejemplo clásico de base de datos relacional OLTP.
*   **OLAP (Online Analytical Processing):** Enfocado en consultas analíticas complejas y agregaciones masivas de datos (ej. reportes anuales). Suelen estructurarse en formatos desnormalizados o de almacenamiento columnar.

---

## ⚡ Capa de Caché con Redis
Redis (Remote Dictionary Server) es una base de datos en memoria extremadamente veloz. Almacena pares clave-valor y responde en microsegundos.
*   **Uso como Deduplicador:** Antes de realizar una operación de escritura pesada en PostgreSQL, verificamos en Redis si el ID de la transacción ya existe.
    *   Si existe en Redis: Se descarta (duplicado).
    *   Si no existe: Se guarda la clave en Redis con un tiempo de expiración (TTL) y se procede a escribir en PostgreSQL.
*   **TTL (Time To Live):** Tiempo tras el cual una clave se borra automáticamente de Redis, liberando memoria RAM de forma autónoma.

---

## 🔗 Orquestación e Idempotencia en Pipelines
Un pipeline de datos debe ser, ante todo, **idempotente**.
> **Idempotencia:** Propiedad según la cual realizar una operación varias veces produce el mismo resultado que realizarla una sola vez.

Si un pipeline falla a la mitad de una ejecución y se reintenta, no debe insertar registros duplicados ni corromper las métricas. Se logra usando restricciones de unicidad (`UNIQUE` en SQL) o técnicas de actualización (`ON CONFLICT DO UPDATE` / `UPSERT`).

### Componentes de Apache Airflow
1.  **Webserver:** Interfaz gráfica para monitorear ejecuciones, logs y estados de los DAGs.
2.  **Scheduler:** El motor que analiza la planificación de los DAGs y despacha las tareas individuales al ejecutor cuando se cumplen sus dependencias.
3.  **Metadatabase:** Base de datos interna (habitualmente PostgreSQL) donde Airflow almacena el estado de los usuarios, tareas y ejecuciones.
4.  **Executor:** Define cómo y dónde se ejecutan los procesos (LocalExecutor en hilos locales, CeleryExecutor en una cola de Redis, o KubernetesExecutor).
