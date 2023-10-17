FROM mysql:8.0

LABEL maintainer="Debezium Community"

COPY ./config/mysql.cnf /etc/mysql/conf.d/
COPY ./config/sample.sql /docker-entrypoint-initdb.d/