#!/usr/bin/env python
#-*- coding:utf8 -*-


# # Outlines: debugging

# BEGIN PDB
# https://docs.python.org/2/library/pdb.html
# !!!!  调试 django 时超赞的！！！
import pdb

pdb.set_trace()
(Pdb) p a  # 即打印a

# TODO 优化的版本是 ipdb， 把上面的 pdb都换成ipdb

# 一个比较舒服的技巧是退回到相应的出错层级运行embed
# END   PDB


# remote pdb 特别好用
# https://pypi.python.org/pypi/rpdb/
import rpdb; rpdb.set_trace()
# rpdb的异常显示有问题



# 在IPython中实时动态地debug某个函数 https://stackoverflow.com/a/12647065
import ipdb
ipdb.runcall(runner.run_strategy, strategy, run_len=10000)

# 这个命令要方便的多!!!!! 直接以debug模式开始整个cell
%%debug



# Profling 和 tuning 中很多工具也可以放到 trace中



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








# https://github.com/cool-RR/PySnooper
# 用这个函数可以代替print来debug python: Never use print for debugging again
# [ ] 在jupyter中是否有用
# [ ] 和autoreload 在一起是否可以用:
# - 出现过打印的代码是老代码的情况(value赋值没有问题)
# - 通过装饰器的方式没有用, 最后是通过with才生效的; (后来改回函数装饰器后， 又有用了。。。但是一直会报错)






#========================================= normal debug ===================

# 看一文件夹下的所有log输出
tail -f *.log




# # Outlines: ================================== profiler and tuning ===================

# 可能有用的工具包
# https://github.com/AhmadIbrahiim/awesome-python#debugging-tools

# 一般思路
## 先 prun/cProfile 看卡在哪个函数
## 再 line profile profile特定的函数


#  可以直接输出, 也可以输出统计文件后再排序
import cProfile
cProfile.run('foo()', , 'stat_out')

python -m cProfile [-s time] [-o stat_out] myscript.py


# 得到输出后就可以用

import pstats
p = pstats.Stats('stat_out') # 再重新统计输出了

p.strip_dirs().sort_stats("cumtime").print_stats(100)
# pycharm 有一个profile viewer可以比较方便地看这个结果 https://stackoverflow.com/a/43616343
# - Run Profiler 可以直接profiler整个程序(依靠'python profiler'这个plugin)
# - 优点是任意地方stop都没问题
# - strip_dirs 是为了显示方便


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
# 安装的时候用conda会比用pip更方便:  conda install -y line_profiler
# %load_ext line_profiler
# %lprun -f FUNC1 -f FUNC2 STATEMENT
# 可以看到 func1 func2 中每一行的开销

# 在ipython之外还可以用下面的命令调优 https://github.com/rkern/line_profiler
# kernprof -l <script_to_profile>.py
# python -m line_profiler <script_to_profile>.py.lprof
# 这个会自动在我 __builtins__ 中加一 @profile 装饰器
# - cons: 这个在有test的时候会失效


# 别忘了还有内置的 %prun !!!!!!!!  可以直接 %%prun profile整个cell .
# 存储pstats.Stats信息可以  %%prun -D stats_out  或者   p = %prun -r <statement>
# 同时还有一系列的其他profile工具:
# [ ] https://towardsdatascience.com/speed-up-jupyter-notebooks-20716cbe2025

# 我自己觉得最好用的
# 1. 找到耗时函数
# 1.1 snakeviz
# pip install snakeviz  && snakeviz -s -H `hostname` stats_out    # 可以达到可视化的效果, 强烈推荐!!!!!!!
# - 这个server是绑定地址的，如果绑定了hostname，那么127.0.0.1是无法访问的
# 1.2 pip install py-spy
# 好处在于
# - 显示调用关系会从文件哪行命令被执行的角度分析(类似于traceback), 而 snakeviz只会显示调用的是哪个函数
#   - 人一般会更关注是哪行导致的性能问题， snakeviz缺了函数是被哪行调用的信息
#     - 同一个函数被多次调用, 各种魔法函数不知道会去哪里会让人很晕
#   - 配合 goto define 体验会很好
# - 显示路径更全，不容易看晕;
# - 生成的图显示性能更高
# 2. 总体思路
# - 先用 py-spy 看调用层级，找到耗时的调用
# - 当某个函数调内某一层调用同一个函数多次， 不知道是那次调用耗时比较多时，需要用line_profile区分

# TODO: vprof 有可能有用



# ## Outlines: memory profiling

# 释放一个object: 下面的函数可能有用
# https://stackoverflow.com/questions/11891755/find-all-references-to-an-object-in-python
import gc
gc.collect()
sys.getrefcount(x)
gc.get_referrers()
gc.get_objects()

# memory_profiler
# - https://github.com/pythonprofilers/memory_profiler
mprof attach <pid>  # 可以统计特程序的的内存使用情况
mprof plot --output <XXX>  <mprofile>.dat





#  BEGIN  多进程/线程DEBUG经验  -------------------------

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



# 可能出问题的地方
# - 思路:
#     - 先改成单进程， 进入单进程debug模式
#     - 如果单进程不出错，则重点关注一下单进程多进程的区别
# - 单进程&多进程区别:
#     - 多进程都是要经过pickle的， 注意是否干扰了pickle的过程(例如 Serializable)。


#  END    多进程/线程DEBUG经验  -------------------------
