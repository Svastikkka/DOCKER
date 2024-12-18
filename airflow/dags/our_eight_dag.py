from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'svastikkka',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def greet(ti):
    firstname = ti.xcom_pull(task_ids="get_name", key="firstname")
    lastname = ti.xcom_pull(task_ids="get_name", key="lastname")
    age = ti.xcom_pull(task_ids="get_age", key="age")

    print(f"Hello My name is {firstname} {lastname} and I am {age} years old.")


def get_name(ti):
    ti.xcom_push(key="firstname",value="Manshu")
    ti.xcom_push(key="lastname",value="Sharma")

def get_age(ti):
    ti.xcom_push(key="age",value="21")

with DAG(
    dag_id='our_eight_dag_v8',
    default_args=default_args,
    description='This is our eight dag using python operator',
    start_date=datetime(2021, 7, 29, 2),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet
    )

    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )

    task3 = PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )
    [task2,task3] >> task1

