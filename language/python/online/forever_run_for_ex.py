"""
conda install gdb

sudo /home/xiaoyang/miniconda3/bin/gdb python <pid>
# 我感觉输出中这表示它是有用的: Reading symbols from /data/home/xiaoyang/miniconda3/bin/python3.10...


# 看更多的 py-能用的 commonds
(gdb) help py-
Ambiguous command "py-": py-bt, py-bt-full, py-down, py-list, py-locals, py-print, py-up.

py-print才能准确地把变量打出来


Weakness
- I still don't know how to run python scripts in gdb python;

"""
a = 1
while True:
    a += 1
