#!/usr/bin/env python
#-*- coding:utf8 -*-


# 设置python的默认编码方式, 可以解决如下问题
#   在shell中运行可行， 在stdout(如修改sys.stdout或者直接用shell流)中出错
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# 或者直接这样也行 ：  export PYTHONIOENCODING=UTF-8