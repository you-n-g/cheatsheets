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
    print "Timeout..."
print r.status_code, r.content, r.cookies, r.headers
