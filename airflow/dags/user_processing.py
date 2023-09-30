from airflow import DAG

from datetime import datetime

with DAG('user_processing', start_date=datetime(2022, 1, 1), 
        schedule_interval='@daily', catchup=False) as dag:
    None