# 📝 Ejercicios Prácticos - Módulo 3: Data Engineering

Aplica técnicas avanzadas de transformación, auditoría y recuperación de datos en tu servidor.

---

## 🏃‍♂️ Ejercicio 1: Cola de Errores (Dead Letter Queue)
Cuando un lote contiene datos rotos o corruptos, no queremos que el pipeline falle por completo, pero tampoco que inserte datos incorrectos en la tabla principal.
*   **Instrucciones:**
    1. En PostgreSQL, crea una tabla llamada `facturas_rechazadas` con columnas para: `datos_crudos` (tipo JSONB), `motivo_rechazo` (VARCHAR) y `fecha_rechazo`.
    2. Modifica el paso de **Transformación** en tu DAG de Airflow.
    3. Si una factura tiene un monto negativo o carece de emisor/receptor, márcala como inválida.
    4. En la fase de **Carga**, inserta estas facturas corruptas en la tabla `facturas_rechazadas` y continúa procesando el resto de facturas correctas del lote de manera ininterrumpida.
*   **Criterio de Aceptación:** Al correr un lote de pruebas con 10 facturas correctas y 2 corruptas, la tabla `facturas` debe sumar 10 registros y la tabla `facturas_rechazadas` debe capturar los 2 errores.

---

## 🔄 Ejercicio 2: Orquestación Retroactiva (Backfill)
Aprenderás a explotar una de las características más potentes de Airflow: el procesamiento histórico retroactivo.
*   **Instrucciones:**
    1. Define en tu DAG una fecha de inicio (`start_date`) correspondiente a 7 días en el pasado.
    2. Configura el parámetro `catchup=True` en la declaración del DAG.
    3. Modifica tu script de extracción para que use la variable de contexto de ejecución de Airflow `{{ ds }}` (fecha de ejecución actual en formato `YYYY-MM-DD`). La extracción debe buscar el archivo de datos correspondiente a ese día específico.
    4. Ejecuta el DAG y observa cómo Airflow arranca automáticamente 7 ejecuciones consecutivas independientes para procesar todo el historial restante.

---

## 💾 Ejercicio 3: Expiración de Caché (TTL en Redis)
Mantener los IDs de facturas en Redis por siempre saturará la memoria RAM del servidor eventualmente. Debes definir políticas de expiración.
*   **Instrucciones:**
    1. Modifica la tarea del DAG que guarda el ID de la factura en Redis.
    2. Configura la inserción para que expire automáticamente (TTL - Time To Live) después de 24 horas (`86400` segundos).
    3. Escribe un script corto en Python (o comando de terminal `redis-cli`) para inspeccionar el TTL restante de una clave de factura insertada recientemente.
*   **Pistas:** Usa el comando `SETEX key seconds value` en Redis, o la función `redis_client.setex(name, time, value)` en la librería de Python.

---

## 📊 Ejercicio 4: Almacenamiento en Formato Semi-estructurado (JSONB)
Aprende a gestionar datos que cambian de esquema con frecuencia sin modificar la estructura física de PostgreSQL.
*   **Instrucciones:**
    1. Modifica la tabla `facturas` agregando una columna llamada `metadatos` de tipo `JSONB`.
    2. Modifica tu DAG para capturar datos adicionales no estructurados de la factura (como "impuestos_detalle", "moneda", "descuentos") y guardarlos en esta columna.
    3. Escribe una consulta SQL que filtre registros buscando una clave dentro del campo JSONB (ej: facturas donde la moneda sea "USD").
*   **Pistas:** En PostgreSQL, puedes consultar campos JSONB con el operador `->>` (ej. `SELECT * FROM facturas WHERE metadatos->>'moneda' = 'USD';`).
