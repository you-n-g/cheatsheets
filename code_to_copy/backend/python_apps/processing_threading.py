#!/usr/bin/env python
#-*- coding:utf8 -*-

# 关键问题：
# - 什么时候共享变量
# - 会不会阻塞


# multiprocessing
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

# ipyparallel 的使用方法
# http://nbviewer.jupyter.org/github/ipython/ipyparallel/blob/master/examples/Index.ipynb








# BEGIN gevent ---------------------------------------
# http://sdiehl.github.io/gevent-tutorial/

# end gevent ---------------------------------------
