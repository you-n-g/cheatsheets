#!/usr/bin/env python
#coding:utf8


'''
NOTICE:
    If parser.parse_args() is used in a module, please avoid using it in another module again !!!
'''

import argparse


# # Outlines: special case
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
        DESCRIPTION with linebreak
''')

from datetime import datetime
get_date = lambda x: datetime.strptime(x, "%Y%m%d").date()
parser.add_argument('--train_s', type=get_date, help='datetime args', required=True)
print(parser.parse_args('--train_s 20121010'.split()))

args = parser.parse_args('--train_s 20121010'.split())
getattr(args, "test_attr", "test")  # some time we want to be compatible


# # Outlines: boolean
parser2 = argparse.ArgumentParser()
parser2.add_argument('--exist-then-true', action='store_true', help='the exist_then_true will be True if present, otherwise False')
print(parser2.parse_args())
print(parser2.parse_args("--exist-then-true".split()))
# 变量名中的`-` 会被换成 `_`


# %% [markdown]
# # Outlines: 多重变量
parser3 = argparse.ArgumentParser()

# multi args
parser3.add_argument('--file', action='append')
parser3.add_argument('--file_with_default', action='append', default=[1,2,3])

print(parser3.parse_args("".split()))  # 没有默认值且没有传参时， 默认为None
print(parser3.parse_args("--file f1".split()))  # 传了参数就变成 list
print(parser3.parse_args("--file_with_default fwd".split())) # 有默认值时，直接往默认值上传参


# # Outlines: 我训练模型常常会用的多次 kwargs update (方便设置默认dict)
class DictUpdate(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest, {})
        if items is None: items = {}
        if isinstance(values, str):
            values = eval(values)
        items.update(values)
        setattr(namespace, self.dest, items)

parser4 = argparse.ArgumentParser()
parser4.add_argument('--kwargs', action=DictUpdate)
parser4.add_argument('--kwargs_wd', action=DictUpdate, default={})
print(parser4.parse_args("".split()))
print(parser4.parse_args(["--kwargs", "{1: 2}", "--kwargs", "{3: 4}"]))


# # Outlines: 多重变量

parser5 = argparse.ArgumentParser()
parser5.add_argument('--multi_arg', nargs='*')
parser5.add_argument('--multi_arg_with_default',  nargs='*', default=[1,2,3])
parser5.add_argument('default_args', nargs='*')

print('''For normal multi args, it will be none of no arguments provided.
For default args, it will return a list even if no arguments provided.''')
print(parser5.parse_args(''.split()))
print(parser5.parse_args('--multi_arg default_args'.split()))
print("The arguments will comsumed by normal arguments.")
print(parser5.parse_args('--multi_arg 1 2 3 4'.split()))
print(parser5.parse_args('1  2  3'.split()))


# TODO: sub commands
# https://docs.python.org/2.7/library/argparse.html#sub-commands
# 对于两者只有一个是required的参数(比如config和其他的参数),
# sub commands是非常好的选择.

# ArgumentParser.add_mutually_exclusive_group只能实现多个单个argument互斥




# Turn object into CLI
# https://github.com/google/python-fire

