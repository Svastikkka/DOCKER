from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator


default_args = {
    'owner': 'svastikkka',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='postgres_v1',
    default_args=default_args,
    description='This is our first cron dag that we write',
    start_date=datetime(2021, 7, 29, 2),
    schedule_interval='0 0 * * *'
) as dag:
    task1 = PostgresOperator(
        task_id='create_postgres_connection',
        postgres_conn_id="posgres_testing",
        sql = """create table if not exists dags_run(
        dt  date,
        dag_id character varying,
        primary key (dt,dag_id)
        )"""
    )
    task2 = PostgresOperator(
        task_id='insert_into_table',
        postgres_conn_id='posgres_testing',
        sql="""
            insert into dags_run (dt, dag_id) values ('{{ ds }}', '{{ dag.dag_id }}')
        """
    )
    task1 >> task2