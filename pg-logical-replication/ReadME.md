# Logical Replication
1. `psql --username=postgresadmin postgresdb`
2. `CREATE DATABASE chiragLogicalRep;` # on both host
3. `\c chiraglogicalrep` # switch to chiraglogicalrep
4. `CREATE TABLE products (id SERIAL,name TEXT,price DECIMAL);` # on both host
5. `CREATE ROLE chirag WITH REPLICATION LOGIN PASSWORD 'admin@123';` # on publisher host
6. `GRANT ALL PRIVILEGES ON DATABASE chiraglogicalrep TO chirag;` # on publisher host
7. `GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO chirag;` # on publisher host
8. `CREATE PUBLICATION my_publication;` # on publisher host
9. `ALTER PUBLICATION my_publication ADD TABLE products;` # on publisher host
10. `CREATE SUBSCRIPTION my_subscription CONNECTION 'host=192.168.0.123 port=5000 password=admin@123 user=chirag dbname=chiraglogicalrep' PUBLICATION my_publication;` # on subscriber host
11. `INSERT INTO products (name, price) VALUES ('Pen', 5.90), ('Notebook', 9.10), ('Pencil', 8.50);` # on publisher host
12. `SELECT * FROM products;` # verify on bath host
13. `ALTER TABLE products REPLICA IDENTITY FULL;` # enable replica identity so we can perform update operations as well

<!-- 
14. `CREATE TABLE orders (quantity INT,price DECIMAL);`
15. `ALTER PUBLICATION my_publication ADD TABLE orders;` 
16. `INSERT INTO orders (quantity, price) VALUES (10, 99.99),(5, 49.50);`
-->

#### Emergency purpose
- `DROP SUBSCRIPTION my_subscription;`
- `ALTER SUBSCRIPTION my_subscription REFRESH PUBLICATION;` 
[Logical Replication](https://www.youtube.com/watch?v=qKdcwkRMaNI)

UPDATE products SET price = 10.00 WHERE name = 'Pencil';
#### Some commands
- `\d products` # TO CHECK TABLE STRUCTURE
- `DELETE FROM products WHERE name = 'Notebook';`  # TO ELEMENTS
- `UPDATE products SET price = 10.00 WHERE name = 'Pencil';` # TO UPDATE ELEMENT
- `SELECT * FROM pg_publication_tables WHERE pubname = 'my_publication';` # TO CHECK REPLICATION STATUS FOR TABLE

Scenarios
- postgrsql-1 RESTARTED and postgresql-2 UP => Replication Worked
- postgrsql-1 UP and postgresql-2 RESTARTED => Replication Worked
- Without Primary Key => Replication Worked
- Perform CURD operations
    - INSERT CHECKED
    - DELETE CHECKED
    - UPDATE CHECKED # need enable replica identity



# PG Logical Replication

```
docker compose -f docker-compose1.yml up -d
docker compose -f docker-compose2.yml up -d
```

```
docker compose -f docker-compose1.yml down
docker compose -f docker-compose2.yml down
```

```
docker exec -it postgres-1 bash 
docker exec -it postgres-2 bash 
```

```
docker restart postgres-1
docker restart postgres-2 
```

```
psql --username=postgresadmin postgresdb
psql --username=postgresadmin postgresdb
```

```sql
CREATE USER appuser WITH PASSWORD 'apppass' SUPERUSER;
CREATE DATABASE appdb WITH OWNER appuser;
\c appdb;
***Create a sample table***
CREATE TABLE public.sample_table (
    id serial PRIMARY KEY,
    name text
);
CREATE TABLE public.sample_table2 (
    id serial PRIMARY KEY,
    name text
);
CREATE EXTENSION pglogical;
```

### INSTANCE 1

```sql
select pglogical.create_node(node_name := 'provider1', dsn := 'host=192.168.0.123 port=5001 dbname=appdb user=appuser password=apppass');

# SELECT pglogical.replication_set_add_all_tables('default', ARRAY['public']);
SELECT pglogical.replication_set_add_table(
    set_name := 'default',    -- The replication set name
    relation := 'sample_table' -- The table name
);
SELECT pglogical.replication_set_add_table(
    set_name := 'default',    -- The replication set name
    relation := 'sample_table2' -- The table name
);
CREATE ROLE appdb;
grant usage on schema pglogical to appdb;
```

### INSTANCE 2
```sql
SELECT pglogical.create_node( node_name := 'subscriber1', dsn := 'host=192.168.0.213 port=5001 dbname=appdb user=appuser password=apppass');
SELECT pglogical.create_subscription( subscription_name := 'subscription1', provider_dsn := 'host=192.168.0.123 port=5001 dbname=appdb user=appuser password=apppass');
select subscription_name, status FROM pglogical.show_subscription_status();
SELECT pglogical.wait_for_subscription_sync_complete('subscription1');
```

***Insert data***
```sql
INSERT INTO public.sample_table (name) VALUES ('Data from Provider Instance');
INSERT INTO public.sample_table2 (name) VALUES ('Data from Provider Instance');
```
***See data***
```sql
SELECT * FROM public.sample_table;
SELECT * FROM sample_table;
SELECT * FROM sample_table2;
```

```sql
SELECT pglogical.drop_subscription('subscription1');
```

# FROM 213 to 211

CREATE DATABASE appdb2 WITH OWNER appuser;
\c appdb2;
***Create a sample table***
CREATE TABLE public.sample_table (
    id serial PRIMARY KEY,
    name text
);
CREATE TABLE public.sample_table2 (
    id serial PRIMARY KEY,
    name text
);
CREATE EXTENSION pglogical;


### INSTANCE 1
select pglogical.create_node(node_name := 'provider1', dsn := 'host=192.168.0.213 port=5001 dbname=appdb2 user=appuser password=apppass');

// SELECT pglogical.replication_set_add_all_tables('default', ARRAY['public']);
SELECT pglogical.replication_set_add_table(
    set_name := 'default',    -- The replication set name
    relation := 'sample_table' -- The table name
);
SELECT pglogical.replication_set_add_table(
    set_name := 'default',    -- The replication set name
    relation := 'sample_table2' -- The table name
);
CREATE ROLE appdb2;
grant usage on schema pglogical to appdb2;


### INSTANCE 2
SELECT pglogical.create_node( node_name := 'subscriber1', dsn := 'host=192.168.0.123 port=5001 dbname=appdb2 user=appuser password=apppass');
SELECT pglogical.create_subscription( subscription_name := 'subscription1', provider_dsn := 'host=192.168.0.213 port=5001 dbname=appdb2 user=appuser password=apppass');
select subscription_name, status FROM pglogical.show_subscription_status();
SELECT pglogical.wait_for_subscription_sync_complete('subscription1');
```
