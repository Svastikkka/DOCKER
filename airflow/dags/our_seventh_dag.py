from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'svastikkka',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def greet(age,ti):
    firstname = ti.xcom_pull(task_ids="get_name", key="firstname")
    lastname = ti.xcom_pull(task_ids="get_name", key="lastname")
    print(f"Hello My name is {firstname} {lastname} and I am {age} years old.")


def get_name(ti):
    ti.xcom_push(key="firstname",value="Manshu")
    ti.xcom_push(key="lastname",value="Sharma")

with DAG(
    dag_id='our_seventh_dag_v7',
    default_args=default_args,
    description='This is our seventh dag using python operator',
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
