#!/usr/bin/env python
#-*- coding:utf8 -*-

# Requests: HTTP for Humans
# doc: http://docs.python-requests.org/en/latest/

import requests
S = requests.Session()
try:
    r = S.post(LOGIN_URL, {}, timeout=SECONDS)
    r = S.get(url, timeout=10)
except requests.exceptions.Timeout:
    # requests.exceptions.ReadTimeout is included
    print("Timeout...")
except requests.exceptions.ConnectionError as e:
    print("ConnectionError...")
print r.status_code, r.content, r.cookies, r.headers




# Requests-HTML: HTML Parsing for Humans™
# https://github.com/kennethreitz/requests-html




# 没一个网络调用都需要考虑的事情
# 永远不返回
# - 设置Timeout
# 出错
