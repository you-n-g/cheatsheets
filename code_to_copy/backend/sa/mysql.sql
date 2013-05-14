-- BEGIN 参数配置
-- 编码问题
collation-server = utf8_general_ci
character-set-server = utf8
-- 设置引擎
default_storage_engine = MyISAM
-- END   参数配置



-- 忘记用户名密码
-- 1) 让mysql以 不验证权限的方式启动 
--    /usr/local/mysql/bin/mysqld_safe --datadir=/data/mysql --pid-file=/data/mysql/localhost.localdomain.pid
./bin/mysqld_safe --skip-grant-tables --datadir=/data/mysql --pid-file=/data/mysql/localhost.localdomain.pid

-- 2) 登陆mysql 设置密码
USE mysql
update user set password=password("XXX") where user="root";
flush privileges;


-- 暂时解除外键 约束
SET FOREIGN_KEY_CHECKS = 0;
-- your sql 
SET FOREIGN_KEY_CHECKS = 1;


-- 不用缓存
select SQL_NO_CACHE ....


-- 新建数据库(包含编码)
CREATE DATABASE  `XXXX` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
