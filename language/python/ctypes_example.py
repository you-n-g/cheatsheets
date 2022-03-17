#!/usr/bin/env python
#-*- coding:utf8 -*-

# 获取指针的内容

i = c_int(42)
pi = pointer(i)
print type(pi.contents) # <class 'ctypes.c_int'>

