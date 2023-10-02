#### Execution
 
1. The image was built but only on the first time (it was necessary to rebuilt in case of changes of DockerFile):
```shell
     docker-compose build
```

2. I initialized the Airflow scheduler, DB, and other config
```shell
    docker compose up airflow-init
```

3. Kick up the all the services from the container:
```shell
    docker-compose up -d
```

4. Login to Airflow web UI on `localhost:8080` with default creds: `airflow/airflow`



# Postgresql

```
psql -h localhost -p 5432 -U airflow -W airflow
```

## Dump

```
pg_dump -U airflow -W -F t testing > testing.dump
```

# Reference
- [Github Airflow Docker](https://github.com/coder2j/airflow-docker)
- [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- [Airflow Tutorial for Beginners - Full Course in 2 Hours 2022](https://www.youtube.com/watch?v=K9AnJ9_ZAXE&list=PLwFJcsJ61oujAqYpMp1kdUBcPG0sE0QMT)
- [Getting Started with PostgreSQL](https://www3.ntu.edu.sg/home/ehchua/programming/sql/PostgreSQL_GetStarted.html)
- [PostgreSQL pg_dump Backup and pg_restore Restore Guide](https://snapshooter.com/learn/postgresql/pg_dump_pg_restore#pg-dump-example)
- [How to create S3 connection for AWS and MinIO in latest airflow version | Airflow Tutorial Tips 3](https://www.youtube.com/watch?v=sVNvAtIZWdQ)
- [Airflow Hooks S3 PostgreSQL: Airflow Tutorial P13](https://www.youtube.com/watch?v=rcG4WNwi900&list=PLwFJcsJ61oujAqYpMp1kdUBcPG0sE0QMT&index=14)

# Errors
- [No module named 'airflow' when initializing Apache airflow docker](https://stackoverflow.com/questions/66791752/no-module-named-airflow-when-initializing-apache-airflow-docker)

- Establishing connection with minio 
```json
    {
        "login": "minioadmin",
        "password": "minioadmin",
        "host": "http://host.docker.internal:9000"
    }
```