#!/usr/bin/env python
#-*- coding:utf8 -*-



# BEGIN PDB
# https://docs.python.org/2/library/pdb.html
import pdb

pdb.set_trace()
(Pdb) p a  # 即打印a
# END   PDB



# BEGIN traceback
import traceback
for line in traceback.format_stack():
    print line
# END   traceback



# BEGIN trace what your script is doing

# 1) trace all action
python -m trace --trace YOURSCRIPT.py

# 2) TODO 理解, 通过发送signal获得运行中的python程序的信息
http://stackoverflow.com/questions/132058/showing-the-stack-trace-from-a-running-python-application
# 这个可能有参考意义 http://acooke.org/cute/DebuggingA0.html

# DONE  trace what your script is doing




