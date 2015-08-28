#!/usr/bin/env python
#-*- coding:utf8 -*-



# BEGIN PDB
# https://docs.python.org/2/library/pdb.html
# !!!!  调试 django 时超赞的！！！
import pdb

pdb.set_trace()
(Pdb) p a  # 即打印a
# END   PDB



# BEGIN traceback
import traceback
for line in traceback.format_stack():
    print line
# 可以配合 os.getpid() 来得到当前进程的pid 看看在哪里运行

# 如果是想输出抓住的异常的traceback
try:
    raise Exception
except Exception:
    ex_type, ex, tb = sys.exc_info()
    traceback.print_tb(tb)
finally:
    del tb

# END   traceback



# BEGIN trace what your script is doing

# 1) trace all action
python -m trace --trace YOURSCRIPT.py

# 2) TODO 理解, 通过发送signal获得运行中的python程序的信息
http://stackoverflow.com/questions/132058/showing-the-stack-trace-from-a-running-python-application
# 这个可能有参考意义 http://acooke.org/cute/DebuggingA0.html

# DONE  trace what your script is doing





# BEGIN logging

# 常识
# level: debug info warning error critical
# 默认root logger的 level 一般是 warning, 即只显示 warning error critical
# 默认是输出到 console 中

# config log; 
import logging
logging.basicConfig(
        filename="XXX.log", 
        level=logging.DEBUG,
        format='%(asctime)s %(name)s [%(levelname)s]:%(message)s', # name 是 logger的name
        # filemode='w', # 加上我就不会append而是覆盖之前的
) # 只有第一次配置会生效，之后就完全无效了。

# logger , 名字随意取，有从属关系; propagate=True时， message会一直向父节点传;  a是 a.b的parent， 根层级是root(不知对应的名字是"root"还是"");  *主要为了知道message从哪里来的*
LOG = logging.getLogger("XXX") # 不加名字或者 只用用 logging的方法 就是用root; logger没有设定level的自动从parent找

# 几个比较特殊的 log
LOG.exception("XXX") # level是ERROR， 但是会把 exception的 stack trace 加上，  所以一定要在 exception handler

# END   logging









#========================================= debug functions ===================


# young_utils.py

#!/usr/bin/env python
#-*- coding:utf8 -*-

import os
import time

def check_value(LOG, var_name, local_dict):
    '''
    from young_utils import check_value
    check_value(LOG, 'XXXXX', locals())
    '''
    template = """

XXXXXXXX  Young want to see #%s# | BEGIN  XXXXXXXX
                %%(%s)s
                type:%%(type_of_%s)s
XXXXXXXX  Young want to see #%s# | END    XXXXXXXX

"""
    local_dict['type_of_%s' % var_name] = type(local_dict[var_name])
    LOG.error((template % ((var_name,) * 4)) % local_dict)




def lock_program(LOG, lock_name):
    '''
    from young_utils import lock_program
    lock_program(LOG, 'XXXXX')
    '''
    lock_file = os.path.join('/tmp/', "%s_lock" % lock_name)
    with open(lock_file, 'w') as f:
        pass
    while os.path.exists(lock_file):
        LOG.error('%s Locked' % lock_name)
        time.sleep(5)







#========================================= normal debug ===================

# 看一文件夹下的所有log输出
tail -f *.log

