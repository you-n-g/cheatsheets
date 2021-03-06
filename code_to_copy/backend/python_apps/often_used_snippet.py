#!/usr/bin/env python
#-*- coding:utf8 -*-


# 设置python的默认编码方式, 可以解决如下问题
#   在shell中运行可行， 在stdout(如修改sys.stdout或者直接用shell流)中出错
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# 或者直接这样也行 ：  export PYTHONIOENCODING=UTF-8


# 模仿这个就能得到相对当前脚本的一个绝对路径
# 如果一个文件有多个link，对应的path应该会随被import时对应的路径变化
DIRNAME = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))  # 注意这得到的是上级目录的绝对路径
DIRNAME = os.path.abspath(os.path.dirname(__file__))  # 为了拷贝方便


# python3
# https://docs.python.org/3/library/pathlib.html
from pathlib import Path
DIRNAME = Path(__file__).absolute().resolve().parent  #  Path('.') 的parent还是Path('.')， 所以absolute要加在前面
# ../../file.py  的 parent.parent 是 ..， parent两层非常容易出bug!!!!!!


# python package加载顺序
# http://stackoverflow.com/questions/26193193/change-the-priority-of-python-sys-path
# 本来的加载顺序, 你修改 PYTHONPATH 就好， 但是
# setuptools会通过/usr/local/lib/python2.7/dist-packages/easy-install.pth
# 再prepend 一堆路径，这里导致了 /usr/lib/python2.7/dist-packages
# 总是在 /usr/local/lib/python2.7/dist-packages 之前， 而且你改了后还可能被改回来





# https://docs.python.org/2/library/glob.html#module-glob
import glob




# 配置文件，从磁盘读取
# 这个 quick start 就可以了
# https://docs.python.org/3/library/configparser.html#quick-start




# 美丽的输出/pretty print
import json
json.dumps(XXX_JSONABLE_OBJECT, sort_keys=True, indent=4, separators=(',', ': '))#, ensure_ascii = False) # 加上这个可以让中文直接显示出来




# 正则表达式
import re
# re.match(pattern, string)
assert(re.match('string', 'NOT_BEGIN_string') is None)
assert(re.match('string', 'string_ENDING') is not None)
assert(re.match('string$', 'string_ENDING') is None)  # limit the ending

# re.seach(pattern, string)
# https://docs.python.org/2/library/re.html#search-vs-match
m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
print(m.groupdict())




# 编程
# 为你的小功能搭建一个interactive环境: https://stackoverflow.com/a/16717949
from IPython import embed
embed()
# 你的程序调用了很多包，你有可能会改很多包的内容，那么autoreload可以帮你解决这个问题
