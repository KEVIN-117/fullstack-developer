# Script de Entrenamiento y Registro en MLflow
# Archivo: train.py
# Ejecución en JupyterLab o consola local

import os
import pandas as pd
import numpy as np
import psycopg2
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
import mlflow.sklearn

# Configuración de conexiones
DB_HOST = "postgres-db"
DB_USER = "airflow_user"
DB_PASSWORD = "airflow_pass"
DB_NAME = "airflow_db"
MLFLOW_TRACKING_URI = "http://mlflow-server:5000"

def load_data_from_db():
    """Conecta a PostgreSQL y extrae la tabla de facturas."""
    conn = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    query = "SELECT monto, categoria, antiguedad_proveedor FROM facturas;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def feature_engineering(df):
    """Prepara las variables de entrada y genera una etiqueta ficticia de riesgo."""
    # Mapeo simple de categorías a números (Label Encoding)
    categories_map = {"Equipos": 1, "Suministros": 2, "Servicios": 3, "Consultoria": 4}
    df['categoria_val'] = df['categoria'].map(categories_map).fillna(0)
    
    # Crear variable objetivo ficticia para entrenamiento:
    # Si el monto es alto (> 10000) y el proveedor es nuevo (antiguedad < 2), clasificar como Riesgo Alto (1)
    df['riesgo'] = np.where((df['monto'] > 10000) & (df['antiguedad_proveedor'] < 2), 1, 0)
    
    X = df[['monto', 'antiguedad_proveedor', 'categoria_val']]
    y = df['riesgo']
    
    return X, y

def train():
    # Configurar destino de MLflow
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("riesgo_fiscal_homelab")
    
    # Cargar y preparar datos
    try:
        df = load_data_from_db()
    except Exception as e:
        print(f"Error cargando datos de la base de datos: {e}")
        # Mocking data fallback en caso de que la DB esté vacía durante la prueba
        data = {
            'monto': [12500.0, 450.5, 15000.0, 200.0, 800.0, 30000.0, 50.0, 20000.0],
            'categoria': ['Equipos', 'Suministros', 'Equipos', 'Servicios', 'Servicios', 'Consultoria', 'Suministros', 'Consultoria'],
            'antiguedad_proveedor': [1, 3, 0, 5, 2, 1, 10, 4]
        }
        df = pd.DataFrame(data)
        
    X, y = feature_engineering(df)
    
    # Dividir datos en entrenamiento y test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    # Hiperparámetros del modelo
    n_estimators = 100
    max_depth = 5
    
    # Iniciar experimento en MLflow
    with mlflow.start_run():
        # Entrenar RandomForest
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        model.fit(X_train, y_train)
        
        # Generar predicciones
        predictions = model.predict(X_test)
        
        # Calcular métricas
        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(y_test, predictions, zero_division=0)
        recall = recall_score(y_test, predictions, zero_division=0)
        f1 = f1_score(y_test, predictions, zero_division=0)
        
        print(f"Modelo entrenado con éxito. Accuracy: {accuracy:.4f}")
        
        # Registrar hiperparámetros en MLflow
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        
        # Registrar métricas en MLflow
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)
        
        # Registrar y guardar el artefacto del modelo en MLflow
        mlflow.sklearn.log_model(model, "random-forest-model", registered_model_name="RiesgoFiscalRF")
        
        print("Métricas, parámetros y modelo registrados en MLflow.")

if __name__ == "__main__":
    train()
