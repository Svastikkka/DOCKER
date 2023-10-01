from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'coder2j',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}
def greet(name,age):
    print(f"Hello My name is {name} and I am {age} years old.")

with DAG(
    dag_id='our_fifth_dag_v5',
    default_args=default_args,
    description='This is our fifth dag using python operator',
    start_date=datetime(2021, 7, 29, 2),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={"name": "Anshu","age": 20}
    )
    task1
