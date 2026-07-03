# Script de DAG de Ejemplo en Airflow (ETL Ingesta Facturas)
# Archivo: sample_dag.py
# Guardar en: /dags/sample_dag.py

from datetime import datetime, timedelta
import json
import logging
from airflow import DAG
from airflow.operators.python import PythonOperator
import redis
import psycopg2

# Configuración básica de conexión
REDIS_HOST = 'redis-cache'
REDIS_PORT = 6379
DB_HOST = 'postgres-db'
DB_USER = 'airflow_user'
DB_PASSWORD = 'airflow_pass'
DB_NAME = 'airflow_db'

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2026, 6, 10),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

def extract_data(**kwargs):
    """
    Extracción: Simula la ingesta leyendo un lote de facturas en formato JSON.
    """
    logging.info("Iniciando Extracción de Facturas...")
    
    # Mock data que simula un lote de facturas
    # En producción esto vendría de un archivo local o de una API REST.
    mock_invoices = [
        {"factura_id": "FAC-2026-001", "emisor": "ProvA", "receptor": "ClienteX", "monto": 12500.00, "fecha_emision": "2026-06-11 08:30:00", "categoria": "Equipos", "antiguedad_proveedor": 1},
        {"factura_id": "FAC-2026-002", "emisor": "ProvB", "receptor": "ClienteY", "monto": 450.50, "fecha_emision": "2026-06-11 09:15:00", "categoria": "Suministros", "antiguedad_proveedor": 3},
        # Factura duplicada a propósito para probar el deduplicador Redis
        {"factura_id": "FAC-2026-001", "emisor": "ProvA", "receptor": "ClienteX", "monto": 12500.00, "fecha_emision": "2026-06-11 08:30:00", "categoria": "Equipos", "antiguedad_proveedor": 1},
        # Factura inválida para validación
        {"factura_id": "FAC-2026-003", "emisor": "ProvC", "receptor": "ClienteZ", "monto": -100.00, "fecha_emision": "2026-06-11 10:00:00", "categoria": "Servicios", "antiguedad_proveedor": 5}
    ]
    
    # Serializar y pasar los datos a la siguiente tarea usando XCom
    kwargs['ti'].xcom_push(key='raw_data', value=json.dumps(mock_invoices))

def transform_and_deduplicate(**kwargs):
    """
    Transformación: Limpia datos erróneos y consulta Redis para eliminar duplicados.
    """
    logging.info("Iniciando Transformación y Deduplicación...")
    
    # Recuperar datos de la tarea anterior
    raw_data_str = kwargs['ti'].xcom_pull(key='raw_data', task_ids='extract_task')
    invoices = json.loads(raw_data_str)
    
    # Conectarse a Redis
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    
    clean_invoices = []
    
    for inv in invoices:
        f_id = inv['factura_id']
        monto = inv['monto']
        
        # 1. Regla de Validación de Negocios: Monto positivo
        if monto <= 0:
            logging.warning(f"Factura {f_id} RECHAZADA: Monto inválido ({monto})")
            continue
            
        # 2. Regla de Deduplicación en Caché Redis
        # setnx (Set if Not Exists) devuelve True si la clave no existía y se guardó
        is_new = r.setnx(f_id, "processed")
        if is_new:
            # Establecer un tiempo de vida (TTL) de 24 horas a la clave en Redis
            r.expire(f_id, 86400)
            clean_invoices.append(inv)
            logging.info(f"Factura {f_id} validada y agregada para carga.")
        else:
            logging.warning(f"Factura {f_id} RECHAZADA: Duplicada en caché Redis.")
            
    kwargs['ti'].xcom_push(key='clean_data', value=json.dumps(clean_invoices))

def load_data(**kwargs):
    """
    Carga: Inserta los registros en la tabla física de PostgreSQL.
    """
    logging.info("Iniciando Carga en PostgreSQL...")
    
    clean_data_str = kwargs['ti'].xcom_pull(key='clean_data', task_ids='transform_task')
    clean_invoices = json.loads(clean_data_str)
    
    if not clean_invoices:
        logging.info("No hay facturas limpias que insertar.")
        return
        
    # Conectar a PostgreSQL
    conn = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    
    insert_query = """
    INSERT INTO facturas (factura_id, emisor, receptor, monto, fecha_emision, categoria, antiguedad_proveedor)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (factura_id) DO NOTHING;
    """
    
    for inv in clean_invoices:
        try:
            cursor.execute(insert_query, (
                inv['factura_id'],
                inv['emisor'],
                inv['receptor'],
                inv['monto'],
                inv['fecha_emision'],
                inv['categoria'],
                inv['antiguedad_proveedor']
            ))
            logging.info(f"Factura {inv['factura_id']} guardada en PostgreSQL.")
        except Exception as e:
            logging.error(f"Error insertando factura {inv['factura_id']}: {e}")
            conn.rollback()
            
    conn.commit()
    cursor.close()
    conn.close()
    logging.info("Carga de datos finalizada exitosamente.")

# Declaración del DAG
with DAG(
    'etl_facturacion_homelab',
    default_args=default_args,
    description='Pipeline ETL de facturas transaccionales con deduplicador Redis',
    schedule_interval='@hourly',
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract_data
    )

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform_and_deduplicate
    )

    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load_data
    )

    # Definir secuencia
    extract_task >> transform_task >> load_task
