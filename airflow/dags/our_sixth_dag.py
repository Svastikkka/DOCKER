from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'svastikkka',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def greet(age,ti):
    name=ti.xcom_pull(task_ids="get_name")
    print(f"Hello My name is {name} and I am {age} years old.")


def get_name():
    return "Manshu"

with DAG(
    dag_id='our_sixth_dag_v6',
    default_args=default_args,
    description='This is our sixth dag using python operator',
    start_date=datetime(2021, 7, 29, 2),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={"age": 26}
    )

    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )
    task2 >> task1
