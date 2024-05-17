"""
conda install -y gdb

# conda install -y python-debug
# conda search dbg

PID=2951138
sudo /home/xiaoyang/miniconda3/bin/gdb python $PID

# 我感觉输出中这表示它是有用的: Reading symbols from /data/home/xiaoyang/miniconda3/bin/python3.10...
# - 这个得靠安装了 debugging symbols 的包: 不知道是那个生效的; 可能是 python-dev  python*-dbg(比较可能); 也可能是受conda安装版本影响
#   "For that, we need python-dbg. Not provided by Conda AFAIK. But the system version works."  https://schwifty50.medium.com/debugging-conda-python-with-gdb-b5d9944f1e2d
# Otherwise会出现如下错误
#   Reading symbols from python...
#   (No debugging symbols found in python)



# 看更多的 py-能用的 commonds
(gdb) help py-
Ambiguous command "py-": py-bt, py-bt-full, py-down, py-list, py-locals, py-print, py-up.

py-print才能准确地把变量打出来


Weakness
- I still don't know how to run python scripts in gdb python;

"""
import os
print(os.getpid())
a = 1
while True:
    a += 1
