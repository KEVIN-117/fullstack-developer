# 📝 Ejercicios Prácticos - Módulo 4: AI & MLOps

Explora las fronteras del versionado y puesta en producción de modelos predictivos en tu Home Lab.

---

## 🏃‍♂️ Ejercicio 1: Despliegue en Modo Espejo (Shadow Deploy)
Cuando entrenas un nuevo modelo candidato, no quieres sustituir el modelo de producción inmediatamente sin estar seguro de su comportamiento real.
*   **Instrucciones:**
    1. Entrena un segundo modelo (candidato) con hiperparámetros diferentes y regístralo en MLflow.
    2. Modifica el servidor FastAPI en `serve.py` para cargar ambos modelos: el de producción (`Production`) y el candidato (`Challenger`).
    3. Cuando llegue una petición a `/predict`, el servidor debe procesarla con ambos modelos de manera interna.
    4. Devuelve al usuario únicamente la respuesta del modelo de producción, pero imprime en consola o guarda en un log de control la predicción de ambos modelos junto con los datos recibidos.
*   **Criterio de Aceptación:** Verificar en los logs del contenedor de FastAPI que por cada consulta recibida, se imprime la predicción de ambos modelos (ej. `[SHADOW LOG] Prod: 0.85 | Challenger: 0.81`).

---

## 🔄 Ejercicio 2: Re-entrenamiento Programado en Airflow
Aprenderás a cerrar el círculo virtuoso de datos e inteligencia artificial, automatizando el entrenamiento cuando cambian los datos.
*   **Instrucciones:**
    1. Crea un nuevo DAG en Airflow llamado `retrain_model_pipeline`.
    2. El DAG debe tener dos tareas:
       *   **Tarea 1 (Check Data):** Hacer una consulta a PostgreSQL para ver cuántas facturas nuevas se han insertado desde el último entrenamiento. Si son menos de X (ej. 5), abortar la ejecución.
       *   **Tarea 2 (Run Training):** Si supera el umbral, ejecutar el script `train.py` para entrenar un nuevo modelo con todos los datos actualizados y registrar la nueva versión en MLflow.
    3. Planifica este DAG para correr semanalmente.

---

## 🎨 Ejercicio 3: Feature Engineering (Ingeniería de Características)
Un modelo solo es tan bueno como las variables con las que se alimenta.
*   **Instrucciones:**
    1. Modifica la consulta en tu script de entrenamiento `train.py`.
    2. Crea una variable adicional en Pandas que represente la "tasa de rechazo del proveedor". Se calcula dividiendo el número de facturas rechazadas de ese emisor (de la tabla `facturas_rechazadas` del Módulo 3) entre el total de facturas emitidas por él.
    3. Entrena tu clasificador con esta nueva variable y compara si la métrica de precisión (`Accuracy` o `F1-Score`) del modelo mejora en MLflow en comparación con el modelo original.

---

## 📦 Inferencia Batch (Procesamiento por Lotes)
No todos los modelos requieren responder en tiempo real por API. Muchos se corren en lotes masivos.
*   **Instrucciones:**
    1. Crea un script en Python llamado `batch_inference.py`.
    2. El script debe ejecutarse de forma independiente, conectarse a PostgreSQL, extraer todas las facturas que no tengan una puntuación de riesgo asignada, cargar el modelo desde MLflow, y calcular el riesgo para todas ellas simultáneamente en un lote.
    3. Escribe los resultados actualizando masivamente los registros correspondientes en la base de datos PostgreSQL.
