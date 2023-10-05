from airflow import DAG
from airflow.models import Connection
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

# Define your DAG

dag = DAG(
    dag_id='backup_postgres_v1',
    schedule_interval='@daily',  # You can adjust the schedule as needed
    start_date=datetime(2023, 10, 1),  # Set your desired start date
    catchup=False,  # Prevent catching up on past runs
    default_args = {
        'owner': 'svastikkka',
        'retries': 5,
        'retry_delay': timedelta(minutes=2)
    }
)

# Define a function to fetch connection parameters
def get_postgresql_connection_params(conn_id):
    conn = Connection.get_connection_from_secrets(conn_id)
    return {
        'username': conn.login,
        'host': conn.host,
        'password': conn.password,
        # You can add more parameters as needed
    }

def dump_to_s3():
    s3_hook = S3Hook(aws_conn_id="minio_testing")
    s3_hook.load_file(
        filename="/tmp/backup.sql",
        key=f"backup.sql",
        bucket_name="airflow",
        replace=True
    )

# Fetch PostgreSQL connection parameters
postgres_conn_id = 'posgres_testing'  # Replace with your connection ID
conn_params = get_postgresql_connection_params(postgres_conn_id)


# Define the BashOperators
list_current_dir = BashOperator(
    task_id='list_current_directory',
    bash_command='ls -l',
    dag=dag,
)

print_current_path = BashOperator(
    task_id='print_current_path',
    bash_command='pwd',
    dag=dag,
)

# Define the BashOperator to perform the backup
backup_command = (
    f"export PGPASSWORD='{conn_params['password']}' && "
    f"pg_dump -U {conn_params['username']} -h {conn_params['host']} -d airflow -t connection -f /tmp/backup.sql"
)
backup_task = BashOperator(
    task_id='perform_postgresql_backup',
    bash_command=backup_command,
    dag=dag,
)

# Define the BashOperators to list and check the path after the backup
list_backup_dir = BashOperator(
    task_id='list_backup_directory',
    bash_command='ls -l /tmp',
    dag=dag,
)

check_backup_path = BashOperator(
    task_id='check_backup_path',
    bash_command='pwd',
    dag=dag,
)

dump_to_s3 = PythonOperator(
    task_id="dump_to_s3",
    python_callable=dump_to_s3
)

[list_current_dir, print_current_path] >> backup_task >> [list_backup_dir, check_backup_path] >> dump_to_s3
