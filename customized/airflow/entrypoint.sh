#!/bin/bash
set -e

# Initialize the Airflow database
/opt/conda/envs/env_balte_0.0.3/bin/airflow db init

# Create the Airflow admin user
/opt/conda/envs/env_balte_0.0.3/bin/airflow users create --username admin \
                     --password admin \
                     --firstname Manshu \
                     --lastname Sharma \
                     --role Admin \
                     --email manshu.sharma@example.com

# Create the Airflow viewer user
/opt/conda/envs/env_balte_0.0.3/bin/airflow users create --username viewer \
                     --password viewer \
                     --firstname John \
                     --lastname Doe \
                     --role Viewer \
                     --email john.doe@example.com

chmod 4777 -R  ~/airflow/*
# Continue with the CMD command
exec "$@"
