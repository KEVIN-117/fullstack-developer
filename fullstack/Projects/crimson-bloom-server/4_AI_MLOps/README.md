# 🤖 Módulo 4: AI Engineering, Tracking y Serving (MLOps)

Este módulo introduce la capa de inteligencia artificial, abarcando desde la experimentación y el entrenamiento de modelos clasificadores hasta su versionado y puesta en producción mediante APIs de alto rendimiento.

---

## 🗺️ Roadmaps de Referencia Integrados
Para profundizar en la teoría de este módulo, abre y estudia las siguientes rutas de especialización:
*   📄 **[machine-learning.pdf](../roadmaps/Role%20Based%20Roadmaps/machine-learning.pdf)** & **[ai-data-scientist.pdf](../roadmaps/Role%20Based%20Roadmaps/ai-data-scientist.pdf)**: Algoritmos predictivos supervisados, entrenamiento y métricas de evaluación (F1, Curva ROC).
*   📄 **[mlops.pdf](../roadmaps/Role%20Based%20Roadmaps/mlops.pdf)** & **[ai-engineer.pdf](../roadmaps/Role%20Based%20Roadmaps/ai-engineer.pdf)**: Ciclo de vida del modelo con MLflow y Model Registry.
*   📄 **[python.pdf](../roadmaps/Skill%20Based%20Roadmaps/python.pdf)** & **[system-design.pdf](../roadmaps/Skill%20Based%20Roadmaps/system-design.pdf)** (ML Serving): Inferencia REST en tiempo real con FastAPI y esquemas Pydantic.

---

## 📋 Checklist General del Módulo
- [ ] Desplegar JupyterLab en un contenedor Docker con persistencia de archivos.
- [ ] Desplegar un servidor MLflow con backend en PostgreSQL y almacenamiento de artefactos local.
- [ ] Conectarse a PostgreSQL desde Python para extraer los datos de facturas del Módulo 3.
- [ ] Entrenar un modelo de clasificación (ej. RandomForest) para estimar riesgo fiscal.
- [ ] Registrar hiperparámetros, métricas de desempeño y el artefacto del modelo en MLflow.
- [ ] Registrar el modelo de manera centralizada en el Model Registry y promoverlo a la fase "Production".
- [ ] Desarrollar una API en FastAPI que cargue el modelo de MLflow y sirva predicciones en caliente.
- [ ] Resolver todos los desafíos prácticos de la sección `/ejercicios`.
- [ ] Validar con curl que la API de inferencia responda en menos de 100ms.

---

## 📚 Tópicos y Submódulos de Aprendizaje

### 🔬 Submódulo 4.1: JupyterLab y Feature Engineering
*   **Objetivo:** Configurar el entorno de ciencia de datos y procesar datos estructurados para su uso en machine learning.
*   **Tópicos Relacionados:** [4.1_Jupyter_Feature_Engineering.md](./topicos/4.1_Jupyter_Feature_Engineering.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] ¿Cómo funciona el ciclo de preparación de datos (manejo de nulos, limpieza y transformación)?
    - [ ] Técnicas de escalamiento de variables continuas y codificación de variables categóricas (Label Encoding).
    - [ ] ¿Qué es la variable objetivo (Target) y qué variables de entrada (Features) la componen?

---

### 📈 Submódulo 4.2: Experimentación y Model Registry con MLflow
*   **Objetivo:** Rastrear de forma sistemática y reproducible las corridas de entrenamiento y catalogar el modelo ganador.
*   **Tópicos Relacionados:** [4.2_Experimentacion_MLflow.md](./topicos/4.2_Experimentacion_MLflow.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] ¿Por qué es crítico versionar experimentos y modelos en lugar de sobrescribir archivos locales?
    - [ ] Métricas de evaluación fundamentales para clasificación: Accuracy, Precision, Recall y F1-Score.
    - [ ] Concepto de etapas del modelo en el registry (Staging, Production, Archived).

---

### ⚡ Submódulo 4.3: Serving de Modelos con FastAPI
*   **Objetivo:** Construir una API web RESTful de inferencia de baja latencia para que otras aplicaciones consuman el modelo entrenado.
*   **Tópicos Relacionados:** [4.3_Model_Serving_FastAPI.md](./topicos/4.3_Model_Serving_FastAPI.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] ¿Qué diferencia hay entre inferencia síncrona (tiempo real) e inferencia asíncrona (batch)?
    - [ ] Validación de esquemas de datos entrantes en APIs mediante Pydantic.
    - [ ] ¿Cómo cargar y almacenar un modelo predictivo en la memoria del proceso de la API para evitar latencias de lectura de disco?

---

## 🔍 Guía de Diagnóstico (Troubleshooting)

| Error Común | Causa Probable | Comando de Diagnóstico / Solución |
| :--- | :--- | :--- |
| **`ImportError: No module named 'psycopg2'`** | El entorno no cuenta con la librería para Postgres. | Corre `pip install psycopg2-binary` en tu notebook. |
| **`MlflowException: API request failed`** | El servidor de MLflow no está activo o la red interna de Docker lo bloquea. | Comprueba la conectividad haciendo `curl http://mlflow-server:5000` desde el contenedor. |
| **El modelo no se actualiza en la API** | La API de inferencia solo lee el modelo una vez al arrancar (`startup`). | Reinicia el contenedor de FastAPI (`docker compose restart ml-serving-api`). |
| **`MockModel has no predict_proba`** | El modelo mock que se carga como fallback no tiene implementadas todas las funciones. | Revisa las funciones declaradas en el script `serve.py` dentro de la clase `MockModel`. |
