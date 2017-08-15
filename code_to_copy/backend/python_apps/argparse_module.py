#!/usr/bin/env python
#coding:utf8

import argparse
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
        DESCRIPTION with linebreak
''')

from datetime import datetime
get_date = lambda x: datetime.strptime(x, "%Y%m%d").date()
parser.add_argument('--train_s', type=get_date, help='dattime args', required=True)
parser.add_argument('--exist-then-true', action='store_true', help='the exist_then_true will be true if present')
args = parser.parse_args()
print args
