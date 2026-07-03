# 📚 Apuntes y Conceptos Clave - Módulo 4: AI & MLOps

Notas de estudio para MLOps, empaquetado de modelos y serving.

---

## 🏛️ Ciclo de Vida del Modelo y MLflow
El ciclo de desarrollo tradicional de Machine Learning suele ser caótico: los científicos entrenan modelos en notebooks locales cambiando parámetros sin documentar. **MLflow** resuelve esto estructurando el ciclo en tres pilares:
1.  **Tracking:** Registra parámetros (ej. `learning_rate`), métricas (ej. `MSE`) y artefactos (ej. el archivo binario del modelo `.pkl`) de cada ejecución o "run".
2.  **Model Registry:** Un almacén centralizado para catalogar modelos. Permite gestionar versiones del modelo (ej. Versión 1, Versión 2) y promoverlas a diferentes fases de despliegue:
    *   `None` (Fase inicial de registro)
    *   `Staging` (Fase de pruebas)
    *   `Production` (Listo para uso comercial)
    *   `Archived` (Versiones obsoletas históricas)

---

## ⚙️ Inferencia en Tiempo Real vs. Batch
*   **Inferencia en Tiempo Real (Online Serving):** El modelo se expone detrás de una API REST/gRPC (con FastAPI). Se optimiza para **baja latencia**. La API recibe una única petición HTTP con datos de entrada, carga el modelo en memoria y responde con la predicción en milisegundos.
*   **Inferencia por Lotes (Batch Inference):** El modelo se ejecuta de forma asíncrona periódicamente (orquestado por Airflow). Carga una gran masa de datos (miles de filas de una DB), calcula las predicciones para todo el lote simultáneamente, y guarda los resultados en bloque. Se optimiza para **rendimiento volumétrico**.

---

## 🏎️ Virtualización de GPU con CUDA
Si el servidor físico Debian cuenta con una tarjeta gráfica dedicada (Nvidia), podemos exponerla a los contenedores Docker para acelerar cálculos matemáticos masivos (como redes neuronales o procesamiento de lenguaje natural).
*   **NVIDIA Container Toolkit:** Modifica el motor de Docker para inyectar las librerías del driver de la GPU del Host Debian dentro del espacio de nombres del contenedor.
*   Esto permite utilizar bibliotecas como `PyTorch` o `TensorFlow` dentro de un contenedor en docker sin necesidad de instalar controladores de gráficos complejos en cada uno de ellos.

---

## 📊 Métricas de Clasificación
Para clasificar transacciones como "Riesgo de Evasión Fiscal" (Clase Positiva) o "Transacción Normal" (Clase Negativa):
*   **Accuracy (Exactitud):** Proporción de predicciones correctas sobre el total de casos. Puede ser engañosa si las clases están desbalanceadas (ej: si solo el 1% de facturas son de riesgo).
*   **Precision (Precisión):** ¿De todas las facturas que el modelo marcó como riesgo, cuántas eran realmente de riesgo? Minimiza los falsos positivos.
*   **Recall (Sensibilidad):** ¿De todas las facturas que realmente eran de riesgo, cuántas logró encontrar el modelo? Minimiza los falsos negativos.
*   **F1-Score:** Promedio armónico entre Precision y Recall, ideal para escenarios de clases desbalanceadas.
