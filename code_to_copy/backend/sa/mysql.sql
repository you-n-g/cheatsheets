-- 安装相关
sudo apt-get install -y mariadb-server mariadb-client

-- mysql_secure_installation  # 安装之后第一次设置


-- 数据库前迁移
-- innodb 的话，一定要拷贝整个 /var/lib/mysql 到新的服务器上
-- /etc/mysql/debian.cnf 也需要迁移，里面保存了一个看数据库状态的账号，否则出这个错误 https://stackoverflow.com/questions/11644300/access-denied-for-user-debian-sys-maint
-- 其他的看哪里改了就迁移哪里
-- 这个报错不要管 "Checking for corrupt, not cleanly closed and upgrade needing tables.." :  https://serverfault.com/questions/613533/how-to-fix-corrupt-not-cleanly-closed-and-upgrade-needing-tables-in-mysql


-- BEGIN 参数配置
-- 编码问题
collation-server = utf8_general_ci
character-set-server = utf8
-- 设置引擎
default_storage_engine = MyISAM
-- 检查配置



-- 常用查看信息操作
show status like ""; 查看数据库状态;
show variables like 'char%'; 查看数据库的参数设置;

-- binlog删除请用sql语句删除. ????


-- ubuntu 16.04 root用户无密码程登录！！！！
-- ERROR 1698 (28000): Access denied for user 'root'@'localhost'
-- solution: https://stackoverflow.com/a/42742610


-- mysql 如果发现修改配置文件后启动无效，可能mysql并不是service命令启动的，需要手动kill再重启


-- BEGIN 忘记用户名密码
-- 1) 让mysql以 不验证权限的方式启动 
--    /usr/local/mysql/bin/mysqld_safe --datadir=/data/mysql --pid-file=/data/mysql/localhost.localdomain.pid
sudo mysqld_safe --skip-grant-tables --datadir=/var/lib/mysql/  --pid-file=/var/run/mysqld/mysqld.pid
-- 等价于这些更安全的操作 https://stackoverflow.com/a/41793945
-- 实际上我使用了下面grant localhost的操作才成功


-- 2) 登陆mysql 设置密码
USE mysql
update user set password=password("XXX") where user="root";
flush privileges;
-- END   忘记用户名密码



-- 暂时解除外键 约束
SET FOREIGN_KEY_CHECKS = 0;
-- your sql 
SET FOREIGN_KEY_CHECKS = 1;



-- 存相关
-- 不用缓存
select SQL_NO_CACHE ....
-- 清理缓存:  http://stackoverflow.com/questions/5231678/clear-mysql-query-cache-without-restarting-server
RESET QUERY CACHE;



-- 新建数据库(包含编码)
-- UTF8:
CREATE DATABASE `XXXX` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
-- GBK:
CREATE DATABASE `XXXX` DEFAULT CHARACTER SET gbk COLLATE gbk_chinese_ci;  
  


-- BEGIN 给特定主机授权
CREATE USER 'root_XXX'@'XXX_host_like_192.168.%.%' IDENTIFIED BY 'XXX_password';
GRANT ALL ON *.* TO 'root_XXX'@'XXX_host_like_192.168.%.%';
-- 表的通配符是*， 主机的通配符是% ……

-- 如果不小心先运行了上面的grant， 则会自动创建用户，则需要设置密码
SET PASSWORD FOR 'root'@'10.1.241.53' = PASSWORD('20131021');

flush privileges;
-- END 给特定主机授权



-- 切换数据库到innodb的脚本
USERNAME=XXX
PASSWORD=XXX
DB=XXX
TABLES=$(mysql -p$PASSWORD -u$USERNAME --skip-column-names -B -D $DB -e 'show tables')
for T in $TABLES
do
    mysql -p$PASSWORD -u$USERNAME -D $DB -e "ALTER TABLE $T ENGINE=MYISAM;SET FOREIGN_KEY_CHECKS=1;"
done
--

-- mysql benchmark tools




-- BEGIN 数据库replication
mysqldump -u$USERNAME -p$PASSWORD -h $HOST -l $DB_NAME > $OUT_FILE.sql
-- 其实直接将整个数据库文件复制过去更好！！！
-- 原始链接 :: http://obmem.info/?p=769%20%20listen
    * 步骤
        # 授权
            * GRANT REPLICATION SLAVE ON *.* TO 'slave'@'%' IDENTIFIED BY 'YOUR_PASSWORD';
            * FLUSH PRIVILEGES;
        # 配置master  [mysqld] :: 非注释下面三行就可以 
            * log_bin = /var/log/mysql/mysql-bin.log
            * binlog_do_db=my_database
            * server-id=1
            * 重启数据库
            * SHOW MASTER STATUS; ::  获得 master 的状态, 
        # 配置 slave
            * my.cnf 加入下面那份配置
            {{{
server-id=2
replicate-do-db=XXX_database
            }}}
            * 
        # 锁定master 数据库， 并导出要备份的那份数据到slave机器, 最后配置slave
            * FLUSH TABLES WITH READ LOCK;
            * mysqldump on master && mysql on slave(曾经用source慢于innodb), 其实直接拷贝文件可能更快！！！但是innodb拷贝过去好像会出错
            * 根据在 master 上的SHOW MASTER STATUS; 的结果 在slave上运行下面的命令
            {{{
            -- slave stop; 这是早先版本的用法
            stop slave;
            CHANGE MASTER TO MASTER_HOST='MASTER_XXX_HOST', MASTER_USER='slave', MASTER_PASSWORD='slave_XXXX_password', MASTER_LOG_FILE='mysql-bin.XXXXX', MASTER_LOG_POS=XXXX;
            -- slave start;
            start slave;
            }}}
        # 解锁 master  ::  unlock tables;
    * 检查情况一般使用 show slave status; 看Slave_IO_Running 和 Slave_SQL_Running 都是 "Yes".
    * _tips_
        * binlog-do-db  和  replicate-do-db 两个参数如果需要 多个, 正确写法是 给每个数据库都 使用 "replicate-do-db="
    == mysql 语句错误 ==
    * 原始链接:: http://www.howtoforge.com/how-to-repair-mysql-replication
    * 情况
        * Slave_IO_Running: Yes
        * Slave_SQL_Running: No
    * 解决方法
        * stop slave 
        * SET GLOBAL SQL_SLAVE_SKIP_COUNTER = 1;  :: 直接忽略mysql的语句错误
        * start slave
    * tips
        * master  有的语句在 master 上正确,但是在 slave 上就错误, 原因可能是有的数据库 slave 上没有
   == 使用mysqlbinlog恢复 ==
   * mysqlbinlog [options] BIN_LOG_FILE  :: 会出现一堆 sql 语句, 从备份开始时间点到结束时间点的语句
   * options
       * --start-date="2005-04-20 9:55:00"    or   --stop-date
       * --stop-position="368312"   or  --start-position="368315"
       * 默认是从开始到最新的
-- END   数据库replication



-- innodb 暂时解除外键约束
SET FOREIGN_KEY_CHECKS = 0; ********* ; SET FOREIGN_KEY_CHECKS = 1;




