from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3_key import S3KeySensor


default_args = {
    'owner': 'coder2j',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}


with DAG(
    dag_id='minio_v1',
    start_date=datetime(2022, 2, 12),
    schedule_interval='@daily',
    default_args=default_args
) as dag:
    task1 = S3KeySensor(
        task_id='minio_example_sensor',
        bucket_name='airflow',
        bucket_key='data.csv',
        aws_conn_id='minio_testing',
        mode='poke',
        poke_interval=5,
        timeout=30
    )