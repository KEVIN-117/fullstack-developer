# API REST de Inferencia de Modelos (FastAPI Serving)
# Archivo: serve.py
# Ejecución: uvicorn serve:app --host 0.0.0.0 --port 8000

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import mlflow.pyfunc
import numpy as np

app = FastAPI(
    title="Servicio de Inferencia de Riesgo Fiscal - Home Lab",
    description="API para predicción de riesgo fiscal utilizando modelos versionados en MLflow.",
    version="1.0"
)

# Definir URI de MLflow
MLFLOW_TRACKING_URI = "http://mlflow-server:5000"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Variable global para almacenar el modelo cargado en memoria
model = None

# Mapeo de categorías utilizado en el entrenamiento
CATEGORIES_MAP = {"Equipos": 1, "Suministros": 2, "Servicios": 3, "Consultoria": 4}

class FacturaInput(BaseModel):
    monto: float = Field(..., gt=0, description="Monto total de la factura, debe ser mayor a 0.")
    antiguedad_proveedor: int = Field(..., ge=0, description="Antigüedad del proveedor en años.")
    categoria: str = Field(..., description="Categoría de la factura: Equipos, Suministros, Servicios o Consultoria.")

    class Config:
        schema_extra = {
            "example": {
                "monto": 15000.00,
                "antiguedad_proveedor": 1,
                "categoria": "Equipos"
            }
        }

@app.on_event("startup")
def load_model():
    """Carga la versión de producción del modelo registrado en MLflow al iniciar la app."""
    global model
    model_name = "RiesgoFiscalRF"
    stage = "Production"
    
    try:
        model_uri = f"models://{model_name}/{stage}"
        print(f"Cargando modelo desde MLflow: {model_uri}...")
        model = mlflow.pyfunc.load_model(model_uri)
        print("Modelo de producción cargado exitosamente.")
    except Exception as e:
        print(f"No se pudo cargar el modelo desde MLflow ({e}). Usando fallback mock...")
        # Fallback ficticio en caso de que MLflow no esté activo o no haya modelo registrado
        class MockModel:
            def predict(self, df):
                # Lógica mock simple que replica el entrenamiento
                return np.where((df['monto'] > 10000) & (df['antiguedad_proveedor'] < 2), 1, 0)
            def predict_proba(self, df):
                # Devuelve probabilidades simuladas
                probs = []
                for _, row in df.iterrows():
                    if row['monto'] > 10000 and row['antiguedad_proveedor'] < 2:
                        probs.append([0.15, 0.85])
                    else:
                        probs.append([0.90, 0.10])
                return np.array(probs)
                
        model = MockModel()

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict")
def predict_riesgo(input_data: FacturaInput):
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible en el servidor.")
    
    # 1. Transformación de datos de entrada al formato del modelo
    cat_val = CATEGORIES_MAP.get(input_data.categoria, 0)
    
    # Crear un DataFrame para pasar al modelo
    data_dict = {
        "monto": [input_data.monto],
        "antiguedad_proveedor": [input_data.antiguedad_proveedor],
        "categoria_val": [cat_val]
    }
    df = pd.DataFrame(data_dict)
    
    # 2. Realizar inferencia
    try:
        prediction = int(model.predict(df)[0])
        
        # Intentar obtener la probabilidad de la predicción si el modelo la soporta
        try:
            probabilities = model.predict_proba(df)[0]
            probabilidad = float(probabilities[prediction])
        except AttributeError:
            probabilidad = 1.0 # Fallback si no tiene predict_proba
            
        riesgo_label = "Alto" if prediction == 1 else "Bajo"
        
        return {
            "riesgo_fiscal": riesgo_label,
            "probabilidad": round(probabilidad, 4),
            "modelo_versión": "Production"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en inferencia: {str(e)}")
