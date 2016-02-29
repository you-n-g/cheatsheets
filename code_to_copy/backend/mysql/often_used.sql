

-- 下面的都是从 HIVE 中学会的， 自己慢慢领悟。
drop table if exists XXX_table;


CREATE TABLE XXX_table (uid string, mid string, action_sum bigint);


insert overwrite table weibo_rd_2_submit
XXXX_select;
-- insert into `XXX_table` (a ,b) values (1,1), (2,2);
-- hive 不支持 insert into table这种格式



select DISTINCT XXX
from XXXX
where XXXX like "prefix%"
ORDER BY XXXX DESC|ASC;



delete from XXX_TABLE
where XXXX
limit XXXX;


ALTER TABLE XXXX_TABLE CHANGE OLD_COLUMN_NAME NEW_COLUMN_NAME XXX_TYPE;


-- 一些函数的用法
select (rank() over (PARTITION BY uid,XXX ORDER BY blog_time,XXXX DESC)) as rank from XXXXX;
select 
case
when COL_NAME is NULL then 0
else COL_NAME_OR_VALUE
end
as action_sum
from XXXXX;


-- 常用需求的思路
-- 选择每组最高分：先group by 计算最高分， 然后再做表链接


