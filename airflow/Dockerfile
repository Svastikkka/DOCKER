FROM apache/airflow:2.0.1
# Install PostgreSQL client package with version 13.12
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends sudo postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    usermod -aG sudo airflow && \
    echo "airflow ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/airflow
USER airflow
COPY requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt