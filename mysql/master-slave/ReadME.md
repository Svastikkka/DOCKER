



CREATE USER 'replication_user'@'192.168.240.3' IDENTIFIED BY 'replication_user';
GRANT REPLICATION SLAVE ON *.* TO 'replication_user'@'192.168.240.3';
FLUSH PRIVILEGES;
SHOW MASTER STATUS\G

*************************** 1. row ***************************
             File: mysql-bin.000003
         Position: 3055
     Binlog_Do_DB: mydb
 Binlog_Ignore_DB: 
Executed_Gtid_Set: f8d808a2-7886-11ee-bd26-0242c0a8f002:1-4
1 row in set (0.00 sec)


STOP SLAVE;
CHANGE MASTER TO MASTER_HOST ='192.168.240.2', MASTER_USER ='replication_user', MASTER_PASSWORD='replication_user', MASTER_LOG_FILE = 'mysql-bin.000004', MASTER_LOG_POS = 3250;

START SLAVE;
SHOW SLAVE STATUS\G

CHANGE REPLICATION SOURCE TO
SOURCE_HOST='192.168.240.2',
SOURCE_USER='replication_user',
SOURCE_PASSWORD='replication_user',
SOURCE_LOG_FILE='mysql-bin.000003',
SOURCE_LOG_POS=899;

mysql  Ver 14.14 Distrib 5.7.42, for Linux (x86_64) using  EditLine wrapper
mysql -h master -u root -p



mysqldump --set-gtid-purged=OFF -u root -p mydb > backup.sql