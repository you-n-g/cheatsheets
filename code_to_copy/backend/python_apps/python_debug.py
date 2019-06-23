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
# rpdb的异常显示有问题


# BEGIN traceback
import traceback
for line in traceback.format_stack():
    print line
# 可以配合 os.getpid() 来得到当前进程的pid 看看在哪里运行

# 如果是想输出抓住的异常的traceback
import sys, traceback
try:
    from StringIO import StringIO
except ImportError as e:
    from io import StringIO
output = StringIO()
import logging

def f():
    raise Exception

try:
    f()
except Exception:
    traceback.print_exc(file=output) # may be a better choice in python3
    # ex_type, ex, tb = sys.exc_info()  # this can get tb object
    # traceback.print_tb(tb, file=output)
    # del tb

    logging.getLogger("ex")  # TODO: 据说这个可以把exception直接打印到logger里
    # 另外LOG.exception 在这里也非常好用

print(output.getvalue())

try:
    raise ValueError("I'm not fine")
except Exception, e:
    print u"Type=%s, Args=%s" % (type(e), e.args)
# END   traceback


# multiple exception
# https://stackoverflow.com/a/6470452
# python3
except (IDontLikeYouException, YouAreBeingMeanException) as e:
    pass
# python2
except (IDontLikeYouException, YouAreBeingMeanException), e:
    pass


# 如何阅读exception
一个exceptin以 traceback开头，如果有"During"继续衔接，最后到异常名结尾
由外到内，一层一层excpetion

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
        level=logging.DEBUG,  # be careful that all the subprocess may use the same config
        format='%(asctime)s %(name)s PID:%(process)d [%(levelname)s]:%(message)s', # name 是 logger的name
        # filemode='w', # 加上我就不会append而是覆盖之前的
) # *只有第一次配置会生效，之后就完全无效了*。
# 难点在于当前的系统已经有logger了，如何做到能并存


# 几个比较特殊的 log
LOG.exception("XXX") # level是ERROR， 但是会把 exception的 stack trace 加上，  所以一定要在 exception handler
# 上面的level是ERROR的，如果想要warning带有exception信息，请直接加新参数
# https://stackoverflow.com/a/193153
logger.warning("something raised an exception:", exc_info=True)
# 这个捕捉到的excpetion不是最后触发的exception
# - 捕捉到的是当前层级exception栈中的exception
# - 在某个exception的else或者try中是上一级exception, 只有进入了except中才算下一级


# Add multiple handlers dynamically:
# https://docs.python.org/3/howto/logging-cookbook.html#multiple-handlers-and-formatters
# 动态地制定handler，log名字是动态的


# LOG的组件

# formatters: log的格式

# Handler: 具体的handler，在此设置level, formatter

# logger: logger之间有层级关系，  名字随意取，有从属关系; propagate=True时， message会一直向父节点传;  a是 a.b的parent， 根层级是root(不知对应的名字是"root"还是"")，root logger是必须要设置的;  *主要为了知道message从哪里来的*
LOG = logging.getLogger(__file__) # 不加名字或者 只用用 logging的方法 就是用root; logger没有设定level的自动从parent找
# 可以被logger 设置handler， level(TODO: 这个level和 handler的level有什么关系)



# 配置logger 可以使用三种方法
# 1) 上面用函数定义的方法
# 2) 用fileConfig() 定义
# 3) 用dictConfig() 定义
# 描述的信息量都是一样的


# 在这里搜索 https://docs.python.org/3/howto/logging-cookbook.html
# dictConfig 可以找到你要的handler

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
        "fileHandler": {
            'class': 'logging.FileHandler',
            'filename': './log/assets.log',
            'mode': 'a',
            'formatter': 'myFormatter',
        },
        # Default file handler for all the warning and error
        "defaultErrFileHandler": {
            'class': 'logging.FileHandler',
            'filename': './log/error.log',
            'mode': 'a',
            'formatter': 'myFormatter',
            "level": "WARNING",
        },
    },
    "loggers":{
        "foo.bar":{
            "handlers":["fileHandler"],
            "level":"INFO",
            "propagate": True,
        },
        "foo":{
            "handlers":["consoleHandler"],
            "level":"INFO",
            "propagate": False,
        },
        "":{
            "handlers":["consoleHandler", "defaultErrFileHandler"],
            "level":"INFO",
        }
    },
    "formatters":{
        "myFormatter":{
            "format":"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }
}

# TODO: email handler
config = configparser.ConfigParser()
config.read('config.ini')
# config.ini 中的内容是
# [email]
# mailhost=127.0.0.1
# mailaddr=340448442@qq.com
# subject='Error occurred'

if 'email' in config:
    section = config['email']
    email_handler_template = {
            'class': 'logging.handlers.SMTPHandler',
            'mailhost': section['mailhost'],
            'fromaddr': section['mailaddr'],
            'toaddrs': [section['mailaddr']],
            'subject': section.get('subject', 'Error occurred'),
            'formatter': 'myFormatter',
            "level": "INFO",
        }
    # 系统中的有的信息必须发消息
    # - 一般消息
    # - 没有捕获到的可能导致程序异常退出的信息
    dictLogConfig['handlers']["EmailHandler"] = email_handler_template.copy()
    dictLogConfig['loggers']['email']['handlers'].append('EmailHandler')

    # 系统中所有ERROR级别的log信息必须发消息
    error_handler = email_handler_template.copy()
    error_handler['level'] = 'ERROR'
    dictLogConfig['handlers']["DefaultErrEmailHandler"] = error_handler
    dictLogConfig['loggers']['']['handlers'].append('DefaultErrEmailHandler')

    # 为了信息不重复，所以系统内部会被捕获的异常才log
    # exception，如果会re-raise的异常不log exception
    # 原则： 谁捕获并处理异常谁负责记录; 否则最后一层负责记录。

    # NOTE：最外层要记得捕获 KeyboardInterrupt



logging.config.dictConfig(dictLogConfig)
logger = logging.getLogger("foo.bar")


# Logging之坑！！！！！ NOTE!!!!
# 1) logging坑就坑在新的logger配置不会覆盖旧的logger配置
# 2) 如果 level 是0表示NOTSET,  我这里表现为所有的log都不记录！！！

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
# pycharm 有一个profile viewer可以比较方便地看这个结果 https://stackoverflow.com/a/43616343
# - Run Profiler 可以直接profiler整个程序(依靠'python profiler'这个plugin)
# - 优点是任意地方stop都没问题


# 支持 control+c 中断输出

# python profiling 代码
# short answer: http://stackoverflow.com/questions/582336/how-can-you-profile-a-python-script
# ppt && video:  http://lanyrd.com/2013/pycon/scdywg/
# document: https://docs.python.org/2/library/profile.html





# Ipython Debug https://github.com/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/01.06-Errors-and-Debugging.ipynb
# %debug  : 可以在出现exception之后立马跳转到相应的出错位置！！！！ 极度方便！！！！！
# Debug 和 Profiling都有
# https://github.com/jakevdp/PythonDataScienceHandbook/tree/master/notebooks
# profiling
# %load_ext line_profiler
# %lprun -f FUNC1 -f FUNC2 STATEMENT
# 可以看到 func1 func2 中每一行的开销



# 在IPython中实时动态地debug某个函数 https://stackoverflow.com/a/12647065
import ipdb
ipdb.runcall(runner.run_strategy, strategy, run_len=10000)






# https://github.com/cool-RR/PySnooper
# 用这个函数可以代替print来debug python


# Pycharm 里面有 Concurrency diagram for "XXX"
# - 这里可以显示多线程并行图




# gdb 可以debug 多线程的deadlock
gdb python [pid] with py-bt & info threads
# https://stackoverflow.com/questions/54766479/logging-multithreading-deadlock-in-python
# 用gdb debug 多进程
# https://www.podoliaka.org/2016/04/10/debugging-cpython-gdb/
# 其中有可能会用到 py-bt的一个库
# https://stackoverflow.com/questions/41160447/cant-enable-py-bt-for-gdb





# Pycharm debug
# Pycharm有一个特殊的工具，可以attach to process...
# 可以直接暂停一个正在运行的工具
