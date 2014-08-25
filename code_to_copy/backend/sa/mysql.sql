-- BEGIN 参数配置
-- 编码问题
collation-server = utf8_general_ci
character-set-server = utf8
-- 设置引擎
default_storage_engine = MyISAM
-- END   参数配置



-- BEGIN 忘记用户名密码
-- 1) 让mysql以 不验证权限的方式启动 
--    /usr/local/mysql/bin/mysqld_safe --datadir=/data/mysql --pid-file=/data/mysql/localhost.localdomain.pid
./bin/mysqld_safe --skip-grant-tables --datadir=/data/mysql --pid-file=/data/mysql/localhost.localdomain.pid

-- 2) 登陆mysql 设置密码
USE mysql
update user set password=password("XXX") where user="root";
flush privileges;
-- END   忘记用户名密码



-- 暂时解除外键 约束
SET FOREIGN_KEY_CHECKS = 0;
-- your sql 
SET FOREIGN_KEY_CHECKS = 1;



-- 不用缓存
select SQL_NO_CACHE ....



-- 新建数据库(包含编码)
CREATE DATABASE  `XXXX` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;



-- BEGIN 给特定主机授权
CREATE USER 'root_XXX'@'XXX_host_like_192.168.%.%' IDENTIFIED BY 'XXX_password';
GRANT ALL ON *.* TO 'root_XXX'@'XXX_host_like_192.168.%.%';

-- 如果不小心先运行了上面的grant， 则会自动创建用户，则需要设置密码
SET PASSWORD FOR 'root'@'10.1.241.53' = PASSWORD('20131021');

flush privileges;
-- END 给特定主机授权
