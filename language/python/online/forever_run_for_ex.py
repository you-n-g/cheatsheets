"""
conda install -y gdb


PID=2951138
sudo `which gdb` `which python` $PID
# - NOTE: 这里的 python 用绝对路径, 不然找不到对的 program， 也就无法加载正确的 debug symbols

# 我感觉输出中这表示它是有用的: Reading symbols from /data/home/xiaoyang/miniconda3/bin/python3.10...
# - 主要靠安装的python版本包含正确的debug symbol (似乎现在新版的conda都有正常安装)
# - Otherwise会出现如下错误
#   Reading symbols from python...
#   (No debugging symbols found in python)
#   如果没有的话，目前我还没找到好的方， 做过如下尝试都没有稳定有效:
#   - 法这个得靠安装了 debugging symbols 的包: 不知道是那个生效的; 可能是 python-dev  python*-dbg(比较可能); 也可能是受conda安装版本影响(可能是这个，3.11好像自带 debugging symbols)
#   - "For that, we need python-dbg. Not provided by Conda AFAIK. But the system version works."  https://schwifty50.medium.com/debugging-conda-python-with-gdb-b5d9944f1e2d



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
