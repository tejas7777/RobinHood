from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 7, 16),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),  # Adjust this as needed
}


def print_hello():
    return "Hello World from Airflow!"


dag = DAG(
    dag_id="hello_airflow",
    description="Hello World Program in Airflow",
    schedule_interval=timedelta(minuites=10),
    start_date=datetime(2023, 7, 16),
    default_args= default_args
)

hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)
hello_operator