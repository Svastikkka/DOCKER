curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @register-mysql.json

docker-compose -f docker-compose.yml exec kafka /kafka/bin/kafka-console-consumer.sh \
    --bootstrap-server kafka:9092 \
    --from-beginning \
    --property print.key=true \
    --topic dbserver1.inventory.customers




    {
    "name": "inventory-connector",
    "config": {
        "connector.class": "io.debezium.connector.mysql.MySqlConnector",
        "tasks.max": "1",
        "database.hostname": "mysql",
        "database.port": "3306",
        "database.user": "debezium",
        "database.password": "dbz",
        "database.server.id": "184054",
        "topic.prefix": "dbserver1",
        "database.include.list": "inventory",
        "schema.history.internal.kafka.bootstrap.servers": "kafka:9092",
        "schema.history.internal.kafka.topic": "schema-changes.inventory",
        "publication.name": "inventory-publication",
        "database.history.kafka.topic": "inventory-changes"
    }
}





{
    "name": "sink-connector",
    "config": {
        "connector.class": "io.debezium.connector.mysql.MySqlConnector",
        "tasks.max": "1",
        "database.hostname": "mysql2",
        "database.port": "3306",
        "database.user": "debezium",
        "database.password": "dbz",
        "database.server.id": "184055",
        "topic.prefix": "dbserver2",
        "database.include.list": "inventory",
        "schema.history.internal.kafka.bootstrap.servers": "kafka:9092",
        "schema.history.internal.kafka.topic": "schema-changes.inventory",
        "publication.name": "inventory-publication",
        "database.history.kafka.topic": "inventory-changes"
    }
}


{
    "name": "sink-connector2",
    "config": {
        "connector.class": "io.debezium.connector.mysql.MySqlConnector",
        "tasks.max": "1",
        "database.hostname": "mysql2",
        "database.port": "3306",
        "database.user": "debezium",
        "database.password": "dbz",
        "database.server.id": "184055",
        "database.server.name": "my-sink-server",
        "database.whitelist": "inventory",
        "topic.prefix": "dbserver2",
        "database.history.kafka.bootstrap.servers": "kafka:9092",
        "database.history.kafka.topic": "schema-changes.inventory",
        "table.whitelist": "inventory.*",
        "snapshot.mode": "initial",
        "database.history.skip.unparseable.ddl": "true"
    }
}


# Again testing 

{
    "name": "mysql1-connector",
    "config": {
        "connector.class": "io.debezium.connector.mysql.MySqlConnector",
        "tasks.max": "1",
        "database.hostname": "mysql",
        "database.port": "3306",
        "database.user": "debezium",
        "database.password": "dbz",
        "database.server.id": "184055",
        "database.server.name": "my-sink-server",
        "database.whitelist": "inventory",
        "topic.prefix": "dbserver2",
        "database.history.kafka.bootstrap.servers": "kafka:9092",
        "database.history.kafka.topic": "schema-changes.inventory",
        "table.whitelist": "inventory.*",
        "snapshot.mode": "initial",
        "database.history.skip.unparseable.ddl": "true"
    }
}

{
    "name": "mysql2-connector",
    "config": {
        "connector.class": "io.debezium.connector.mysql.MySqlConnector",
        "tasks.max": "1",
        "database.hostname": "mysql2",
        "database.port": "3306",
        "database.user": "debezium",
        "database.password": "dbz",
        "database.server.id": "184055",
        "database.server.name": "my-sink-server",
        "database.whitelist": "inventory",
        "topic.prefix": "dbserver2",
        "database.history.kafka.bootstrap.servers": "kafka:9092",
        "database.history.kafka.topic": "schema-changes.inventory",
        "table.whitelist": "inventory.*",
        "snapshot.mode": "initial",
        "database.history.skip.unparseable.ddl": "true"
    }
}


INSERT INTO customers VALUES (default, 'Jane','Doe','jane.doe2@example.com');




kafka /kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --from-beginning --property print.key=true --topic dbserver1.inventory.customers



curl -i -X PUT -H "Accept:application/json" -H "Content-Type:application/json" http://localhost:8083/connectors/inventory-connector/config -d @connector-config-replica.json


curl -i -X PUT -H "Accept:application/json" -H "Content-Type:application/json" http://localhost:8083/connectors/inventory-connector/config -d @connector-config-master.json
