# Logical Replication
1. `psql --username=postgresadmin postgresdb`
2. `CREATE DATABASE chiragLogicalRep;` # on both host
3. `\c chiraglogicalrep` # switch to chiraglogicalrep
4. `CREATE TABLE products(id SERIAL,name TEXT,price DECIMAL,CONSTRAINT products_pkey PRIMARY KEY (id));` # on both host
5. `CREATE ROLE chirag WITH REPLICATION LOGIN PASSWORD 'admin@123';` # on publisher host
6. `GRANT ALL PRIVILEGES ON DATABASE chiraglogicalrep TO chirag;` # on publisher host
7. `GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO chirag;` # on publisher host
8. `CREATE PUBLICATION my_publication;` # on publisher host
9. `ALTER PUBLICATION my_publication ADD TABLE products;` # on publisher host
10. `CREATE SUBSCRIPTION my_subscription CONNECTION 'host=192.168.0.211 port=5000 password=admin@123 user=chirag dbname=chiraglogicalrep' PUBLICATION my_publication;` # on subscriber host
11. `INSERT INTO products (name, price) VALUES ('Pen', 5.90), ('Notebook', 9.10), ('Pencil', 8.50);` # on publisher host
12. `SELECT * FROM products;` # verify on bath host
#### Emergency purpose
- `DROP SUBSCRIPTION my_subscription;`
[Logical Replication](https://www.youtube.com/watch?v=qKdcwkRMaNI)