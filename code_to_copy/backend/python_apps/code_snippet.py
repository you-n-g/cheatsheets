#!/usr/bin/env python
#-*- coding:utf8 -*-

# 美丽的输出  pretty print of json
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
