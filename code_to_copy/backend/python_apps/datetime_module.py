
# 将字符串转化为datetime对象
import datetime
print(datetime.datetime.strptime('2011-03-07', '%Y-%m-%d'))
print datetime.datetime.now().isoformat()

# d1 = datetime.datetime.strptime('2011-03-07', '%Y-%m-%d').date()
d1 = datetime.datetime(2011, 3, 7).date()
d2 = datetime.datetime.strptime('2011-03-11', '%Y-%m-%d').date()
gap = d1 - d2
gap == datetime.timedelta(days=-4)




# pendulum
# https://github.com/sdispater/pendulum
import pendulum
dt = pendulum.parse('2018-03-11T13:23:16.365083')
print(dt.format('%Y-%m-%d'))
