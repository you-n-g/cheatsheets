#!/usr/bin/env python

import subprocess


# TODO: use communicate instead of PIPE
process = subprocess.Popen(["XXX_COMMAND", "XXX_ARGS"], stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# this line include input, output, err info;
output, unused_err = process.communicate("XXX INPUT")
code = process.wait()  # it will blocked here, otherwize it will run parallelly

# 如果更方便地执行命令 shell 命令
output = subprocess.check_output('ls -lat', shell=True)
# shell=True 保证了 shell本身的一些功能也可以用: 解析命令(不用split), 类似~xiaoyang的扩展, 环境变量解释， 通配符等等
# 坑:
# 思路把参数和命令分开， shell=True就不起作用了...


subprocess.run('ls -lat', shell=True)  # 如果想直接运行， 让输出直接打印在stdout中
