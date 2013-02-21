#!/usr/bin/env python
# -*- coding:utf8 -*-

from django.http import HttpResponseRedirect
from django.contrib import messages

def _can_xxx(func, vfunc, redirect_to):
    def wrapper_func(request, *args, **kwargs):
        result, reason = vfunc(request, *args, **kwargs)
        if result:
            return func(request, *args, **kwargs)
        else:
            messages.info(request, reason)
            # redirect_to 可以是一个函数， 实现灵活跳转
            local_redirect_to = redirect_to
            if callable(local_redirect_to):
                local_redirect_to = local_redirect_to(request, *args, **kwargs)
            redirect_url = request.META.get('HTTP_REFERER', '/')  if local_redirect_to == None else local_redirect_to
            return HttpResponseRedirect(redirect_url)
    return wrapper_func

def _can_XXXX(request, *args, **kwargs):
    return (True, u"") if XXX else (False, u"您没有XXX权限")

def can_examine(func):
    return _can_xxx(func, _can_XXXX, None)
