#!/usr/bin/env python
#-*- coding:utf8 -*-

# BEGIN joblib - Embarrassingly parallel for loops
# 优势
# - 用cloudpickle 解决了很多pickle不能做的事情
# - 有特殊的接口可以高效地share numpy array
# - joblib还可以用并行地生产和消费模式，prefetch模式

# [ ] 是否可以和 autoreload 完美结合

# ref: https://joblib.readthedocs.io/en/latest/parallel.html#serialization-and-processes

# END   joblib - Embarrassingly parallel for loops


# # Outlines: concurrent.futures
# BEGIN concurrent.futures — Launching parallel tasks--------
# 最方便的解决方案
# https://docs.python.org/3/library/concurrent.futures.html
# - with语句，不容易出现忘了关进程、线程的错误
# - 进程线程无缝切换

# 容易出错的地方
# - 如果要向子进程传输奇怪的数据，会比较麻烦(lightgbm, pandas 都出过类似的问题)
#   - 可能将task存放在磁盘上会比较好
#   - to_dict再 pd.DataFrame 也可以
# - future_object.result() , 而不是get!!!

# END   concurrent.futures — Launching parallel tasks--------



# 关键问题：
# - 什么时候共享变量
# - 会不会阻塞

# # Outlines: multiprocessing
# https://docs.python.org/2/library/multiprocessing.html

## process 之间传递数据
# 这个Queue是线程&&进程安全的
from multiprocessing import Queue

# Pipe的特点是它是双工的, TODO: 这个和两个队列有什么区别呢
from multiprocessing import Pipe

# 这个锁可以用于同步
from multiprocessing import Lock

# 共享内存
from multiprocessing import Value, Array

# 似乎是个新东西
# 1) 支持丰富的数据，由server process 管理，其他进程可以共享。
# 2) 可以通过网络共享
# 3) 速度比Value 和 Array慢一点
# 有下面的地方不懂
# 1) 什么叫 allows other processes to manipulate them using proxies ?????? 什么叫 proxies
# 2) Also, a single manager can be shared by processes on different computers over a network. 居然支持不同机器的进程之间通信，太强大了吧 ????
# 3) 什么叫 server process
# 要注意的地方
# 1) proxy object是进程安全的，但是不是线程安全的。
from multiprocessing import Manager
Manager()


## multiprocessing编程的原则
# multiprocessing 假设所有的子进程都可以 import父进程的 main module, 所以如果父进程无法被import进来，那么会报错
# 1. 主要不要产生僵尸进程
# 1. 使用Queue的process会卡在那里，join时会导致调用join的进程也被卡主，最终产生死锁。
# 1. 虽然在Unix下可以 不要使用全局变量在父子进程中实现共享，但是windows不行， 而且父进程相应的全局变量被回收会导致子进程出问题。
# 1. multiprocessing会把stdin close掉，对它读取可能会出错


# https://docs.python.org/3/library/multiprocessing.html
# - 想单独运行一个子进程: https://stackoverflow.com/a/2046630

# For fast implementing
from multiprocessing import Pool

def worker(x):
    return x*x
pool = Pool(5)
res = []
for kwargs in [{'x': 1}, {'x': 2}, {'x': 3}]:
    res.append(pool.apply_async(worker, [], kwargs))

# get result and prevent the main process from exiting
for r in res:
    try:
        print 'task ended:', r.get()
        # 子进程如果出现异常，会在r.get()这里reraise异常. 导致父进程挂掉，子进程无法继续执行
        # TODO: 如果在另外一个进程里core dumped，会在r.get()这一步卡住
    except Exception, e:
        print u"Type=%s, Args=%s" % (type(e), e.args)
pool.close()
# TODO: If I put it before r.get(). The print info above will never output the data.
# 在并行地分配任务的代码结束后调用它，这样pool在完成所有任务后就会自动关闭了
# Indicate that no more data will be put on this queue by the current process.

pool.join()
# one must call close or terminate() before call join. 不然主进程会等子进程结束，子进程会等主进程分配任务



# 在Interactive script中，parallel运行子程序会出错 https://stackoverflow.com/questions/34086112/python-multiprocessing-pool-stuck
# 因为它的原理是先fork，然后子程序再从当前的 python file来import 需要运行的程序. 所以要注意加__main__，解释器本身没有python file ， 无法被import

from multiprocessing import Pool
# if __name__ == '__main__':
p = Pool(5)
def f(x):
    return x*x
p.map(f, [1,2,3])

# IPython需要用更复杂的并行处理的程序  http://ipython.org/ipython-doc/dev/parallel/


# # Outlines: ipyparallel
# ipyparallel 的使用方法
# http://nbviewer.jupyter.org/github/ipython/ipyparallel/blob/master/examples/Index.ipynb
% ipcluster start -n 40   # 执行程序的目录和 这个目录最好一样，否则可能找不到包 --cluster-id=<cluster_str>

import ipyparallel as ipp
rc = ipp.Client()  # ipp.Client(cluster_id='us_stock')
view = rc.load_balanced_view()
ares = view.apply_async(...)  # apply_sync(f, *args, **kwargs)
if ares.ready():
    res = ares.get()

# 注意事项
# 个人理解可能这个是把代码打成文本包，发过去调用
# 优点：
# - 在interactive 环境下的函数现在也可以是多线程了
# 缺点
# - 函数调用的所有全局变量似乎都不能用；比如包需要在函数里重新import才能看到!!!!!!!!!!!!!!!!!!
# - 开ipp的$cwd和调用ipp的$cwd如果不同，有可能会出错
# - 报错依然看不到，得调用get才能看到
# - 通过接口发送过去的函数是可以让最新代码生效， 但是函数间接调用的module里面的函数需要重启服务才能得到最新代码

# 使用技巧:
# - 尽量将函数写在单独的包里面(一般很难)
# - 如果不行就只能
#    - 在函数的顶部写一些 import 了
#    - 用到的相关的函数当成参数穿进去






# # Outlines: gevent
# BEGIN gevent ---------------------------------------
# http://sdiehl.github.io/gevent-tutorial/
# 之前我写爬虫的体验非常不好，程序老是内存爆掉
# END   gevent ---------------------------------------




# # Outlines: threading
# BEGIN threading -----------------------
# https://www.geeksforgeeks.org/multithreading-python-set-1/
# 仿照这边写

# 坑
# 用Threading 拿到线程的 return 和 exception比较麻烦，用from multiprocessing.pool import ThreadPool会比较容易
# https://stackoverflow.com/a/14299004

# END   threading -----------------------




# 内存爆掉的启示
# 其实在主程序中不断调用 gc.collect() 就可以回收内存。
