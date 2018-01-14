#!/usr/bin/env python
#coding:utf8


'''
NOTICE:
    If parser.parse_args() is used in a module, please avoid using it in another module again !!!
'''

import argparse
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
        DESCRIPTION with linebreak
''')

from datetime import datetime
get_date = lambda x: datetime.strptime(x, "%Y%m%d").date()
parser.add_argument('--train_s', type=get_date, help='datetime args', required=True)
parser.add_argument('--exist-then-true', action='store_true', help='the exist_then_true will be true if present')

# Add position argument
# If there is no  -- or -, it will be position variable. You can give it the new name by metavar


# multi args
parser.add_argument('--file', action='append')


parser.add_argument('--multi_arg', nargs='*')

parser.add_argument('--multi_arg_with_default', nargs='*', default=[1,2,3])

parser.add_argument('default_args', nargs='*')

# ARGS = parser.parse_args()
# print args


print '# None will be returned for file'
print parser.parse_args('--train_s 20121010'.split())

print '# list will be return even if there is only one args'
print parser.parse_args('--train_s 20121010 --file file1'.split())
print parser.parse_args('--train_s 20121010 --file file1 --file file2'.split())

print '# It will return a list even if there is no args. None will be returned if no appearance and no default value'
print parser.parse_args('--multi_arg --train_s 20121010 default_args'.split())


print '# If default value is specified, None will not be returned'
print parser.parse_args('--train_s 20121010'.split())




# TODO: sub models 
# https://docs.python.org/2.7/library/argparse.html#sub-commands
