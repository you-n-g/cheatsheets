#!/usr/bin/env python
#-*- coding:utf8 -*-


# 设置python的默认编码方式, 可以解决如下问题
#   在shell中运行可行， 在stdout(如修改sys.stdout或者直接用shell流)中出错
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# 或者直接这样也行 ：  export PYTHONIOENCODING=UTF-8

# 模仿这个就能得到相对当前脚本的一个绝对路径
DIRNAME = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))  # 注意这得到的是上级目录的绝对路径
