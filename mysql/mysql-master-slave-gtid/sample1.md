MySQL multi-source master-slave replication for krx test environment:

### Crux
We are using GTID based master slave replication. In this replication both master and slave should have same GTID. This doc aims at providing a step-by-step guide to help you set up MySQL Replication using GTIDs and help you replicate your MySQL data with ease.

### Steps for taking dump and restoring it
1. Dump the database on the master:
   ```bash
   mysqldump --set-gtid-purged=OFF -u root -p balte_oms > backup.sql
   ```

2. Copy the dump file from the master to the local machine:
   ```bash
   docker cp krx_test_mysql:/backup.sql ./
   ```

3. Copy the dump file from the local machine to the slave machine using SCP:
   ```bash
   scp /home/krx_test/docker_balte_krx_live/backup.sql jenkins@192.168.0.209:/home/jenkins/infrastrengthening/mysql
   ```

4. Copy the dump file to the slave container:
   ```bash
   docker cp ./backup.sql replication-mysql:/
   ```

5. Restore the database on the slave:
   ```bash
   CREATE DATABASE balte_oms;
   mysql -u root -p balte_oms < backup.sql
   ```

### Step to enable replication on master
1. Create a replication user on the master:
   ```sql
   CREATE USER 'replication_user'@'192.168.0.209' IDENTIFIED WITH mysql_native_password BY 'password';
   ```

2. Grant replication privileges to the user:
   ```sql
   GRANT REPLICATION SLAVE ON *.* TO 'replication_user'@'192.168.0.209';
   FLUSH PRIVILEGES;
   ```

3. Show the master status:
   ```sql
   SHOW MASTER STATUS\G;
   ```

4. Disable WRITE operation on master till we enable replication
   ```sql
   SET @@GLOBAL.read_only = ON;
   ```

### Steps to enable replication on slave
1. Stop and reset the slave on the slave server:
   ```sql
   STOP REPLICA FOR CHANNEL "KRX_TEST";
   RESET REPLICA FOR CHANNEL "KRX_TEST";
   ```
2. Set GTID on slave
   ```sql
   SET GLOBAL gtid_purged='ccb0d141-dc54-11ee-923c-0242c0a8b005:1-33';  <!---Should be same as master--->
   ```

3. Change the master settings on the slave:
   ```sql
   CHANGE REPLICATION SOURCE TO SOURCE_HOST='192.168.0.201', SOURCE_PORT=3307, SOURCE_USER='replication_user', SOURCE_PASSWORD='password', SOURCE_AUTO_POSITION=1 FOR CHANNEL "KRX_TEST";
   ```

4. Create table filters for replication for  `KRX_TEST` channel
   ```sql
   CHANGE REPLICATION FILTER REPLICATE_DO_TABLE = (balte_oms.krx_test, balte_oms.dead_trade_krx_test_total, balte_oms.dead_trade_krx_test) FOR CHANNEL "KRX_TEST";
   ```

5. Start the slave for the specified channel:
   ```sql
   START REPLICA FOR CHANNEL "KRX_TEST";
   ```

6. Show the slave status for the specified channel:
   ```sql
   SHOW REPLICA STATUS FOR CHANNEL "KRX_TEST"\G;
   ```

7. Disable Read Only permission on master:
   ```sql
   SET @@GLOBAL.read_only = OFF;
   ```

### To verify replication working

- Check both master and slave have same GTID 
   ```sql
   show global variables like 'gtid_executed'; <!---Should be same as master--->
   ```

- Get detailed information about the replication applier status, including GTID-related information.
   ```sql
   SELECT * FROM performance_schema.replication_applier_status_by_worker;
   ```
- `replication_user` is present in master
   ```sql
   SELECT User, Host FROM mysql.user WHERE User = 'replication_user';
   ```

### Error Handling
- If you encounter the "ERROR 1776" related to SOURCE_AUTO_POSITION, execute the following on the slave:
   ```sql
   STOP REPLICA FOR CHANNEL "KRX_TEST";
   RESET REPLICA FOR CHANNEL "KRX_TEST";
   ```
- Incase both master and slave have diff gtid
   ```sql
   STOP SLAVE SQL_THREAD;
   RESET MASTER; <!--- Remove GTID from slave --->
   START SLAVE SQL_THREAD; <!--- Try now to set gtid in slave--->
   ```
- To remove table replication filters on slave
   ```sql
   CHANGE REPLICATION FILTER REPLICATE_DO_TABLE = (); <!--- Will remove for all channel--->
   ```

### Reference
[mysql-gtids-and-replication-set-up](https://hevodata.com/learn/mysql-gtids-and-replication-set-up/)
