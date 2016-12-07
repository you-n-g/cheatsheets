#!/usr/bin/env python
#-*- coding:utf8 -*-



# BEGIN PDB
# https://docs.python.org/2/library/pdb.html
# !!!!  调试 django 时超赞的！！！
import pdb

pdb.set_trace()
(Pdb) p a  # 即打印a

# TODO 优化的版本是 ipdb， 把上面的 pdb都换成ipdb
# END   PDB


# remote pdb 特别好用
# https://pypi.python.org/pypi/rpdb/
import rpdb; rpdb.set_trace()


# BEGIN traceback
import traceback
for line in traceback.format_stack():
    print line
# 可以配合 os.getpid() 来得到当前进程的pid 看看在哪里运行

# 如果是想输出抓住的异常的traceback
import sys, traceback
import StringIO
output = StringIO.StringIO()

try:
    raise Exception
except Exception:
    ex_type, ex, tb = sys.exc_info()
    traceback.print_tb(tb, file=output)
    del tb

    logging.getLogger("ex")  # TODO: 据说这个可以把exception直接打印到logger里

print output.getvalue()
# END   traceback


# 查看将要调用的方法到底来自哪里
import inspect
inspect.getmodule(XXX_FUNC)
inspect.getsourcelines(XXX_FUNC)


# BEGIN trace what your script is doing

# 1) trace all action
python -m trace --trace YOURSCRIPT.py

# 2) TODO 理解, 通过发送signal获得运行中的python程序的信息
http://stackoverflow.com/questions/132058/showing-the-stack-trace-from-a-running-python-application
# 这个可能有参考意义 http://acooke.org/cute/DebuggingA0.html

# DONE  trace what your script is doing





# BEGIN logging

# 常识
# level: debug info warning error critical, 只显示 大于等于level的logger
# 默认root logger的 level 一般是 warning, 即只显示 warning error critical
# 默认是输出到 console 中

# config log; 这个是针对root logger 配置的
import logging
logging.basicConfig(
        filename="XXX.log",
        level=logging.DEBUG,
        format='%(asctime)s %(name)s [%(levelname)s]:%(message)s', # name 是 logger的name
        # filemode='w', # 加上我就不会append而是覆盖之前的
) # *只有第一次配置会生效，之后就完全无效了*。


# 几个比较特殊的 log
LOG.exception("XXX") # level是ERROR， 但是会把 exception的 stack trace 加上，  所以一定要在 exception handler


# LOG的组件

# formatters: log的格式

# Handler: 具体的handler，在此设置level, formatter

# logger: logger之间有层级关系，  名字随意取，有从属关系; propagate=True时， message会一直向父节点传;  a是 a.b的parent， 根层级是root(不知对应的名字是"root"还是"")，root logger是必须要设置的;  *主要为了知道message从哪里来的*
LOG = logging.getLogger("XXX") # 不加名字或者 只用用 logging的方法 就是用root; logger没有设定level的自动从parent找
# 可以被logger 设置handler， level(TODO: 这个level和 handler的level有什么关系)



# 配置logger 可以使用三种方法
# 1) 上面用函数定义的方法
# 2) 用fileConfig() 定义
# 3) 用dictConfig() 定义
# 描述的信息量都是一样的


# 典型的层级
import logging
import logging.config
dictLogConfig = {
    "version": 1,
    "handlers":{
                "consoleHandler":{
                    "class":"logging.StreamHandler",
                    "formatter":"myFormatter",
                    }
                },
    "loggers":{
        "foo.bar":{
            "handlers":["consoleHandler"],
            "level":"INFO",
            "propagate": True,
        },
        "foo":{
            "handlers":["consoleHandler"],
            "level":"INFO",
            "propagate": False,
            },
        "":{
            "handlers":["consoleHandler"],
            "level":"INFO",
            }
        },
    "formatters":{
        "myFormatter":{
            "format":"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
}
logging.config.dictConfig(dictLogConfig)
logger = logging.getLogger("foo.bar")

# logging坑就坑在新的logger配置不会覆盖旧的logger配置

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




#================================== profiler and tuning ===================


#  可以直接输出, 也可以输出统计文件后再排序
import cProfile
cProfile.run('foo()', , 'stat_out')

python -m cProfile [-s time] [-o stat_out] myscript.py


# 得到输出后就可以用

import pstats
p = pstats.Stats('stat_out') # 再重新统计输出了

p.strip_dirs().sort_stats("time").print_stats(100)


# 支持 control+c 中断输出

# python profiling 代码
# short answer: http://stackoverflow.com/questions/582336/how-can-you-profile-a-python-script
# ppt && video:  http://lanyrd.com/2013/pycon/scdywg/
# document: https://docs.python.org/2/library/profile.html
