
# 将字符串转化为datetime对象
import datetime
print(datetime.datetime.strptime('2011-03-07', '%Y-%m-%d'))
print datetime.datetime.now().isoformat()

d1 = datetime.datetime.strptime('2011-03-07', '%Y-%m-%d').date()
d2 = datetime.datetime.strptime('2011-03-11', '%Y-%m-%d').date()
gap = d1 - d2
gap == datetime.timedelta(days=-4)
