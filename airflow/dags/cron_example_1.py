from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'svastikkka',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='cron',
    default_args=default_args,
    description='This is our first cron dag that we write',
    start_date=datetime(2021, 7, 29, 2),
    schedule_interval='0 0 * * *'
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command="echo hello world, this is the first task!"
    )
    task1