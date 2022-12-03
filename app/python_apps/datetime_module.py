
# 将字符串转化为datetime对象
import datetime
print(datetime.datetime.strptime('2011-03-07', '%Y-%m-%d'))
print(datetime.datetime.now().isoformat())

# d1 = datetime.datetime.strptime('2011-03-07', '%Y-%m-%d').date()
d1 = datetime.datetime(2011, 3, 7).date()
d2 = datetime.datetime.strptime('2011-03-11', '%Y-%m-%d').date()
gap = d1 - d2
gap == datetime.timedelta(days=-4)

datetime.datetime.fromtimestamp(1521365700) # from int timestamp to datetime




# pendulum:  is much slower than datetime
# https://github.com/sdispater/pendulum
import pendulum
dt = pendulum.parse('2018-03-11T13:23:16.365083')  # 这种会自动当成utc时间来解析
print(dt.format('%Y-%m-%d'))
# 加了时区之后会当成本地时间来解析

# equivalence
pendulum.fromtimestamp


pendulum.now()  # 如果不带时区，你会得到UTC时间！！！

# 注意的坑
# pendulum所有时间自带时区！  所以时间比较时，都是转化为utc时间比较！！！！
# pendas不支持 pendulum,  如果datetime带时区也会出错


# timestamp的值永远都是以utc时间为准的。 无视时区，全球统一。
# datetime 表现为本地时间，但timestamp也代表utc时间, 所以两个库的now的timestamp是能对的上的
# pendulum 的fromtimestamp 会得到utc时间
# datetime 的fromtimestamp 会得到本地时间


# 两者的不同
# utc默认将字符串
|------------------------------+---------------------+------------------|
| function                     | pendulum            | dateime          |
|------------------------------+---------------------+------------------|
| 解析时间字符串或者构建新对象 | 默认当成utc时间解读 | 当成本地时间解读 |
|------------------------------+---------------------+------------------|

# 转化成datetime

# 并且带时区
pendulum.parse('2018-04-03 08:52:24.183000+00:00')._datetime
# got datetime.datetime(2018, 4, 3, 8, 52, 24, 183000, tzinfo=<TimezoneInfo [+00:00, , +00:00:00, STD]>)

# 转化后不带时区，但是对应的时间是本地时间
datetime.datetime.fromtimestamp(pendulum.parse('2018-04-03 08:52:24.183000+00:00').timestamp())
# got datetime.datetime(2018, 4, 3, 16, 52, 24, 183000)
